#!/usr/bin/env python3
"""
similaridade.py: similaridade dos recortes anotados por altitude, sem detector (revisao de 17/10/2026,
agente D3). Resposta ao audio do revisor que pediu "um metodo de reducao de ordem, uma matriz de
co-similaridade ou outro dispositivo matematico" antes (ou em vez) do detector de tres classes.

O que faz, em quatro etapas:

  extrair   recorta cada figura anotada (caixa com margem de 25% de cada lado, cortada na borda do
            quadro) dos corpora de tres classes, encaixa o recorte em 224 x 224 (lado maior em 224,
            reamostragem bilinear, preenchimento cinza 114 como no Ultralytics) e passa pelo tronco
            do YOLO11s pre-treinado no COCO (C:/arma3-favela/blender/yolo11s.pt, o mesmo peso
            inicial de todos os treinos), congelado. O vetor de cada recorte e a media espacial da
            saida das camadas 4 (P3, 256-d), 6 (P4, 256-d) e 10 (C2PSA, fim do tronco, 512-d).
            Guarda em C:/arma3-favela/blender/similaridade/emb_<corpus>.npz (fora do git).
  analisar  por altitude e por camada: matriz de co-similaridade (cosseno medio entre pares de
            recortes, por classe), silhueta, centroide mais proximo e 5 vizinhos mais proximos em
            validacao cruzada de 5 dobras estratificada por classe, PCA a 2 e 10 dimensoes
            (reducao de ordem), LDA a 2 dimensoes (reducao supervisionada, extra), taxa por tipo de
            objeto, intervalo por reamostragem de quadros, comparacao e concordancia com o detector.
            Escreve similaridade.json.
  treinado  suplemento: repete extracao e analise (so camada P5, protocolos cv_eval e ref_para_eval)
            com o tronco do detector treinado em cada corpus (runs/detect/<modelo>/weights/best.pt),
            como referencia superior do que um classificador por similaridade consegue com o melhor
            extrator disponivel. Nao e livre de modelo: o tronco viu a divisao de treino e o val
            selecionou o checkpoint; os quadros novos sao os unicos nunca vistos. Acrescenta a chave
            extrator_treinado_na_tarefa ao similaridade.json.
  figura    fig13_similaridade.png: PCA 2-D por altitude e as tres matrizes de co-similaridade.

Nenhum treino alem dos classificadores triviais; nenhum render; nenhum corpus derivado da PCERJ
(os corpora ds_armado_* vem de gen_morro.py, braco OSM + Poly Haven).

  C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa extrair   (cerca de 5 min em CPU)
  C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa analisar  (cerca de 6 min)
  C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa treinado  (cerca de 8 min)
  C:/arma3-favela/venv/Scripts/python.exe similaridade.py --etapa figura
"""
import argparse
import datetime as dt
import json
import math
import os
import time

import numpy as np
from PIL import Image

BL = "C:/arma3-favela/blender"
PESOS = os.path.join(BL, "yolo11s.pt")
CACHE = os.path.join(BL, "similaridade")
AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(AQUI)                      # 06-resultados
FIGS = os.path.join(RES, "figuras")
JSON_SAIDA = os.path.join(AQUI, "similaridade.json")
CLASSES = ["armada", "desarmada", "objeto"]
CLASSES_EN = ["armed", "unarmed", "object"]
CAMADAS = {"P3": 4, "P4": 6, "P5": 10}          # nome -> indice da camada do tronco
CAMADA_PRINCIPAL = "P5"
LADO = 224
MARGEM = 0.25
K_VIZ = 5
K_DOBRAS = 5
N_BOOT = 2000
SEMENTE = 2026

# Uma "altitude" e um corpus de referencia (train/val) mais, quando existe, o corpus de quadros novos
# (indices 200 a 279, todos em validacao). GSD como no artigo: 9,76 cm/px a 150 m em 1920 px, logo
# 4,88 em 3840; 2,44 a 75 m; 1,1 a 35 m. `detector` e o modelo treinado nesse corpus.
POOLS = {
    "35":   dict(corpus="ds_armado_35",   extra="ds_armado_35_extra",  alt_m=35,  gsd_cm=1.1,
                 rotulo="35 m, 1.1 cm/px", detector="armado_35"),
    "75g":  dict(corpus="ds_armado_75g",  extra="ds_armado_75g_extra", alt_m=75,  gsd_cm=2.44,
                 rotulo="75 m twin, 2.4 cm/px", detector="armado_75g"),
    "150g": dict(corpus="ds_armado_150g", extra=None,                  alt_m=150, gsd_cm=4.88,
                 rotulo="150 m twin, 4.9 cm/px", detector="armado_150g"),
    "75":   dict(corpus="ds_armado_75",   extra=None,                  alt_m=75,  gsd_cm=2.44,
                 rotulo="75 m original, 2.4 cm/px", detector="armado_75"),
}
# arquivos do detector com destino por instancia (quadro, indice da caixa, classe, tipo, coluna):
# coluna 0 armada, 1 desarmada, 2 objeto, 3 perdida (confusao_armado.py)
DETECTOR = {
    ("35", "val"): "confusao_armado_35_inst.json",
    ("35", "novos"): "extra_armado_35.json",
    ("75g", "val"): "confusao_armado_75g_inst.json",
    ("75g", "novos"): "extra_armado_75g.json",
    ("150g", "val"): "confusao_armado_150g.json",
    ("75", "val"): "confusao_armado_75_inst.json",
}


# ----------------------------------------------------------------------------------------------
# etapa 1: recortes e vetores
# ----------------------------------------------------------------------------------------------
def le_manifest(ds):
    recs = [json.loads(l) for l in open(os.path.join(BL, ds, "manifest.jsonl"), encoding="utf-8")]
    return {os.path.splitext(r["img"])[0]: r for r in recs}


def le_rotulos(ds, split, base):
    p = os.path.join(BL, ds, "labels", split, base + ".txt")
    out = []
    if os.path.exists(p):
        for l in open(p):
            t = l.split()
            if len(t) >= 5:
                out.append((int(t[0]), *map(float, t[1:5])))
    return out


def tipos_por_caixa(rec, rotulos):
    """Tipo do objeto carregado em cada linha de rotulo. Usa `caixas` quando o manifest tem (uma
    entrada por linha, na mesma ordem); senao reconstroi de `tipos` pela regra do gerador
    (gen_morro.py: tipos = [l[7] for l in rotulos if l[7]], isto e, os tipos das linhas que
    carregam algo, classes 0 e 2, na ordem das linhas). Devolve (tipos, origem, ok)."""
    n = len(rotulos)
    cx = rec.get("caixas")
    if cx is not None and len(cx) == n:
        return [c[1] for c in cx], "caixas", True
    tipos = list(rec.get("tipos", []))
    out, k = [], 0
    for r in rotulos:
        if r[0] in (0, 2) and k < len(tipos):
            out.append(tipos[k])
            k += 1
        else:
            out.append("")
    ok = (k == len(tipos)) and sum(1 for r in rotulos if r[0] in (0, 2)) == len(tipos)
    return out, "tipos", ok


def recorta(im, cx, cy, w, h, margem=MARGEM):
    H, W = im.shape[:2]
    x1 = max(0, int(math.floor((cx - w / 2 - margem * w) * W)))
    x2 = min(W, int(math.ceil((cx + w / 2 + margem * w) * W)))
    y1 = max(0, int(math.floor((cy - h / 2 - margem * h) * H)))
    y2 = min(H, int(math.ceil((cy + h / 2 + margem * h) * H)))
    return im[y1:y2, x1:x2], (x2 - x1, y2 - y1)


def letterbox(crop, lado=LADO, cor=114):
    h, w = crop.shape[:2]
    s = lado / max(h, w)
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    im = Image.fromarray(crop).resize((nw, nh), Image.BILINEAR)
    tela = np.full((lado, lado, 3), cor, np.uint8)
    ox, oy = (lado - nw) // 2, (lado - nh) // 2
    tela[oy:oy + nh, ox:ox + nw] = np.asarray(im)
    return tela


class Extrator:
    """Tronco do YOLO11s (camadas 0 a 10 do DetectionModel, todas sequenciais, f = -1), congelado.
    Entrada RGB em [0, 1] como no Ultralytics. Saida: media espacial das camadas pedidas."""

    def __init__(self, pesos, device, camadas):
        import torch
        from ultralytics import YOLO
        self.torch = torch
        self.m = YOLO(pesos).model.eval().to(device)
        for p in self.m.parameters():
            p.requires_grad_(False)
        self.camadas = camadas
        self.device = device
        self.ultima = max(camadas.values())

    def __call__(self, lote):
        torch = self.torch
        with torch.no_grad():
            x = torch.from_numpy(np.ascontiguousarray(lote)).permute(0, 3, 1, 2).float().div_(255.0)
            x = x.to(self.device)
            saidas = {}
            for i, camada in enumerate(self.m.model[: self.ultima + 1]):
                x = camada(x)
                for nome, idx in self.camadas.items():
                    if idx == i:
                        saidas[nome] = x.mean(dim=(2, 3)).float().cpu().numpy()
        return saidas


def extrai_corpus(ds, ext, lote_max=64, limite=0):
    man = le_manifest(ds)
    meta = []            # dicionarios por recorte
    emb = {k: [] for k in CAMADAS}
    buffer = []
    validacao = dict(quadros=0, regra_tipos_bate=0, regra_tipos_falha=0, sem_tipo_em_0_ou_2=0,
                     tipo_em_classe_1=0, origem_caixas=0, origem_tipos=0, caixas_degeneradas=0)

    def despeja():
        if not buffer:
            return
        lote = np.stack(buffer)
        s = ext(lote)
        for k in CAMADAS:
            emb[k].append(s[k])
        buffer.clear()

    t0 = time.time()
    for split in ("train", "val"):
        pasta = os.path.join(BL, ds, "images", split)
        if not os.path.isdir(pasta):
            continue
        for fn in sorted(os.listdir(pasta)):
            if not fn.endswith(".png"):
                continue
            base = os.path.splitext(fn)[0]
            rec = man[base]
            rot = le_rotulos(ds, split, base)
            if not rot:
                continue
            if limite and validacao["quadros"] >= limite:
                break
            tipos, origem, ok = tipos_por_caixa(rec, rot)
            validacao["quadros"] += 1
            validacao["origem_" + origem] += 1
            if origem == "caixas":
                # confere a regra de reconstrucao nos corpora que tem as duas informacoes
                rec2 = dict(rec)
                rec2.pop("caixas")
                t2, _, ok2 = tipos_por_caixa(rec2, rot)
                validacao["regra_tipos_bate" if (ok2 and t2 == tipos) else "regra_tipos_falha"] += 1
            elif not ok:
                validacao["regra_tipos_falha"] += 1
            vis = rec.get("vis") or [None] * len(rot)
            laje = [c[2] for c in rec["caixas"]] if rec.get("caixas") else [None] * len(rot)
            im = np.asarray(Image.open(os.path.join(pasta, fn)).convert("RGB"))
            H, W = im.shape[:2]
            for gi, r in enumerate(rot):
                cls, cx, cy, w, h = r
                if cls in (0, 2) and not tipos[gi]:
                    validacao["sem_tipo_em_0_ou_2"] += 1
                if cls == 1 and tipos[gi]:
                    validacao["tipo_em_classe_1"] += 1
                crop, (cw, ch) = recorta(im, cx, cy, w, h)
                if cw < 2 or ch < 2:
                    validacao["caixas_degeneradas"] += 1
                    continue
                buffer.append(letterbox(crop))
                meta.append(dict(corpus=ds, split=split, quadro=base, gi=gi, cls=cls, tipo=tipos[gi],
                                 vis=vis[gi] if gi < len(vis) else None,
                                 laje=laje[gi] if gi < len(laje) else None,
                                 cw=cw, ch=ch, bw=round(w * W, 1), bh=round(h * H, 1),
                                 alt=rec.get("alt"), clima=rec.get("clima")))
                if len(buffer) >= lote_max:
                    despeja()
            if validacao["quadros"] % 20 == 0:
                print(f"[sim] {ds} {validacao['quadros']} quadros, {len(meta)} recortes, "
                      f"{time.time() - t0:.0f} s", flush=True)
    despeja()
    out = {k: np.concatenate(v).astype(np.float32) for k, v in emb.items()}
    print(f"[sim] {ds}: {len(meta)} recortes em {time.time() - t0:.0f} s; validacao {validacao}", flush=True)
    return meta, out, validacao


def caminho_cache(ds, sufixo=""):
    return os.path.join(CACHE, f"emb_{ds}{sufixo}.npz")


def extrai_e_grava(ds, ext, args, sufixo=""):
    alvo = caminho_cache(ds, sufixo)
    if os.path.exists(alvo) and not args.refazer and not args.limite:
        print(f"[sim] {ds}: ja existe {alvo}", flush=True)
        return
    meta, emb, validacao = extrai_corpus(ds, ext, limite=args.limite)
    if args.limite:   # teste de fumaca: nao grava
        print(f"[sim] teste: {len(meta)} recortes, formas {[(k, v.shape) for k, v in emb.items()]}; "
              f"exemplo {meta[0]}", flush=True)
        return
    np.savez_compressed(alvo, meta=json.dumps(meta), validacao=json.dumps(validacao), **emb)
    print(f"[sim] gravado {alvo}", flush=True)


def prepara_torch(args):
    import torch
    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"
    if device == "cpu":
        torch.set_num_threads(args.threads)
    return device


def etapa_extrair(args):
    os.makedirs(CACHE, exist_ok=True)
    device = prepara_torch(args)
    ext = Extrator(PESOS, device, CAMADAS)
    for p in POOLS.values():
        for ds in (p["corpus"], p["extra"]):
            if ds:
                extrai_e_grava(ds, ext, args)


# ----------------------------------------------------------------------------------------------
# etapa 2: analise
# ----------------------------------------------------------------------------------------------
def carrega(ds, sufixo=""):
    z = np.load(caminho_cache(ds, sufixo))
    meta = json.loads(str(z["meta"]))
    emb = {k: z[k] for k in CAMADAS}
    return meta, emb, json.loads(str(z["validacao"]))


def monta_dados(alt, sufixo=""):
    """Junta o corpus de referencia (train/val) e os quadros novos de uma altitude."""
    p = POOLS[alt]
    meta, emb, val = carrega(p["corpus"], sufixo)
    validacoes = {p["corpus"]: val}
    pool = np.array([m["split"] for m in meta])
    if p["extra"]:
        meta2, emb2, val2 = carrega(p["extra"], sufixo)
        validacoes[p["extra"]] = val2
        meta = meta + meta2
        emb = {k: np.concatenate([emb[k], emb2[k]]) for k in CAMADAS}
        pool = np.concatenate([pool, np.array(["novos"] * len(meta2))])
    return dict(meta=meta, emb=emb, pool=pool,
                y=np.array([m["cls"] for m in meta]),
                tipos=np.array([m["tipo"] for m in meta]),
                quadros=np.array([m["corpus"] + "/" + m["quadro"] for m in meta]),
                validacoes=validacoes)


def normaliza(X, mu):
    Z = X - mu
    return Z / np.maximum(np.linalg.norm(Z, axis=1, keepdims=True), 1e-9)


def cosim_pares(Z, y):
    """Cosseno medio entre pares (i de a, j de b); na diagonal, pares distintos da mesma classe."""
    S = np.stack([Z[y == c].sum(0) for c in range(3)])
    n = np.array([(y == c).sum() for c in range(3)], float)
    M = S @ S.T
    out = M / np.outer(n, n)
    for c in range(3):
        out[c, c] = (M[c, c] - n[c]) / (n[c] * (n[c] - 1))
    return out


def cosim_centroides(Z, y):
    C = np.stack([Z[y == c].mean(0) for c in range(3)])
    C /= np.linalg.norm(C, axis=1, keepdims=True)
    return C @ C.T


def silhueta(Z, y):
    D = 1.0 - Z @ Z.T
    n = len(y)
    s = np.zeros(n)
    md = np.zeros((n, 3))
    for c in range(3):
        m = (y == c)
        soma = D[:, m].sum(1)
        cnt = m.sum() - m.astype(int)          # exclui o proprio
        md[:, c] = soma / np.maximum(cnt, 1)
    for i in range(n):
        a = md[i, y[i]]
        b = min(md[i, c] for c in range(3) if c != y[i])
        s[i] = (b - a) / max(a, b, 1e-12)
    return float(s.mean()), [float(s[y == c].mean()) for c in range(3)]


def dobras_estratificadas(y, k, rng):
    f = np.empty(len(y), int)
    for c in range(3):
        idx = np.where(y == c)[0]
        rng.shuffle(idx)
        f[idx] = np.arange(len(idx)) % k
    return f


def dobras_por_quadro(quadros, k, rng):
    q = np.unique(quadros)
    rng.shuffle(q)
    fq = {qq: i % k for i, qq in enumerate(q)}
    return np.array([fq[qq] for qq in quadros])


def centroides(Z, y):
    C = np.stack([Z[y == c].mean(0) for c in range(3)])
    return C / np.maximum(np.linalg.norm(C, axis=1, keepdims=True), 1e-9)


def prediz_knn(Ztr, ytr, Zte, k=K_VIZ):
    S = Zte @ Ztr.T
    idx = np.argpartition(-S, k, axis=1)[:, :k]
    votos = np.zeros((len(Zte), 3))
    ar = np.arange(len(Zte))
    for j in range(k):
        votos[ar, ytr[idx[:, j]]] += 1.0 + 1e-3 * S[ar, idx[:, j]]   # desempate pela similaridade
    return votos.argmax(1)


def pca_ajusta(Ztr, d):
    mu = Ztr.mean(0)
    _, s, Vt = np.linalg.svd(Ztr - mu, full_matrices=False)
    var = s ** 2 / (s ** 2).sum()
    return mu, Vt[:d], float(var[:d].sum()), var


def pca_projeta(mu, V, Z):
    return (Z - mu) @ V.T


def lda_ajusta(Ztr, ytr, d=2, encolhimento=0.1):
    """Fisher: direcoes que maximizam a dispersao entre classes sobre a dispersao dentro delas,
    com encolhimento da matriz interna para a identidade (p = 512 contra n de centenas)."""
    p = Ztr.shape[1]
    mu = Ztr.mean(0)
    Sw = np.zeros((p, p))
    Sb = np.zeros((p, p))
    for c in range(3):
        Zc = Ztr[ytr == c]
        mc = Zc.mean(0)
        Sw += (Zc - mc).T @ (Zc - mc)
        Sb += len(Zc) * np.outer(mc - mu, mc - mu)
    Sw /= len(Ztr)
    Sw = (1 - encolhimento) * Sw + encolhimento * (np.trace(Sw) / p) * np.eye(p)
    w, U = np.linalg.eigh(Sw)
    Swm = U @ np.diag(1 / np.sqrt(np.maximum(w, 1e-12))) @ U.T
    M = Swm @ Sb @ Swm
    w2, U2 = np.linalg.eigh(M)
    W = Swm @ U2[:, ::-1][:, :d]
    return mu, W


def nc_euclid(Ptr, ytr, Pte):
    C = np.stack([Ptr[ytr == c].mean(0) for c in range(3)])
    D = ((Pte[:, None, :] - C[None, :, :]) ** 2).sum(2)
    return D.argmin(1)


def rankdata(a):
    a = np.asarray(a, float)
    ordem = np.argsort(a, kind="mergesort")
    sa = a[ordem]
    r = np.empty(len(a))
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        r[ordem[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return r


def auc(pos, neg):
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    r = rankdata(np.concatenate([pos, neg]))
    u = r[:len(pos)].sum() - len(pos) * (len(pos) + 1) / 2
    return float(u / (len(pos) * len(neg)))


def z_inv(p):
    """inversa da normal padrao por bissecao em erf (sem scipy)."""
    p = min(max(p, 1e-6), 1 - 1e-6)
    lo, hi = -8.0, 8.0
    for _ in range(80):
        m = (lo + hi) / 2
        if 0.5 * (1 + math.erf(m / math.sqrt(2))) < p:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def d_linha(taxa_acerto, taxa_alarme):
    return z_inv(taxa_acerto) - z_inv(taxa_alarme)


def resume_predicoes(y, pred, tipos, quadros, score_armada=None, score_dif=None, rng=None):
    """Matriz de confusao, recall por classe, taxas de chamada de armada, d', AUC, por tipo e
    intervalo de 95% por reamostragem de quadros."""
    cm = np.zeros((3, 3), int)
    for a, b in zip(y, pred):
        cm[a, b] += 1
    n = cm.sum(1)
    rec = cm.diagonal() / np.maximum(n, 1)
    chamada_armada = cm[:, 0] / np.maximum(n, 1)
    out = dict(n=int(len(y)), n_por_classe={CLASSES[c]: int(n[c]) for c in range(3)},
               matriz_confusao={CLASSES[a]: {CLASSES[b]: int(cm[a, b]) for b in range(3)} for a in range(3)},
               recall={CLASSES[c]: round(float(rec[c]), 4) for c in range(3)},
               acuracia=round(float(cm.diagonal().sum() / max(len(y), 1)), 4),
               acuracia_balanceada=round(float(rec.mean()), 4),
               chamada_de_armada={CLASSES[c]: round(float(chamada_armada[c]), 4) for c in range(3)},
               objeto_chamado_de_armada=round(float(chamada_armada[2]), 4),
               desarmada_chamada_de_armada=round(float(chamada_armada[1]), 4),
               d_linha_armada_contra_objeto=round(d_linha(rec[0], chamada_armada[2]), 3),
               d_linha_armada_contra_desarmada=round(d_linha(rec[0], chamada_armada[1]), 3))
    if score_armada is not None:
        a = auc(score_armada[y == 0], score_armada[y == 2])
        out["auc_armada_vs_objeto_sim_centroide_armada"] = round(a, 4)
        out["d_linha_da_auc"] = round(math.sqrt(2) * z_inv(a), 3)
        out["auc_armada_vs_desarmada_sim_centroide_armada"] = round(auc(score_armada[y == 0], score_armada[y == 1]), 4)
    if score_dif is not None:
        out["auc_armada_vs_objeto_diferenca_centroides"] = round(auc(score_dif[y == 0], score_dif[y == 2]), 4)
    # por tipo de objeto (classe 2) e por modelo de arma (classe 0)
    por_tipo = {}
    for c, nome in ((2, "objeto_por_tipo"), (0, "armada_por_modelo")):
        d = {}
        for t in sorted(set(tipos[y == c])):
            m = (y == c) & (tipos == t)
            d[t] = dict(n=int(m.sum()), chamada_de_armada=round(float((pred[m] == 0).mean()), 4))
        por_tipo[nome] = d
    out.update(por_tipo)
    # reamostragem de quadros (percentil 2,5 a 97,5) para as taxas centrais
    if rng is not None:
        q = np.unique(quadros)
        qi = {qq: i for i, qq in enumerate(q)}
        qidx = np.array([qi[qq] for qq in quadros])

        def conta(mask_num, mask_den):
            num = np.bincount(qidx[mask_num], minlength=len(q))
            den = np.bincount(qidx[mask_den], minlength=len(q))
            return num, den
        alvos = {"objeto_chamado_de_armada": ((y == 2) & (pred == 0), y == 2),
                 "recall_armada": ((y == 0) & (pred == 0), y == 0),
                 "desarmada_chamada_de_armada": ((y == 1) & (pred == 0), y == 1)}
        ic = {}
        amostras = rng.integers(0, len(q), size=(N_BOOT, len(q)))
        for k, (mn, md) in alvos.items():
            num, den = conta(mn, md)
            est = num[amostras].sum(1) / np.maximum(den[amostras].sum(1), 1)
            ic[k] = [round(float(np.percentile(est, 2.5)), 4), round(float(np.percentile(est, 97.5)), 4)]
        if score_armada is not None:
            vals = []
            for s in amostras[:500]:
                sel = np.concatenate([np.where(qidx == j)[0] for j in s])
                ys, sc = y[sel], score_armada[sel]
                vals.append(auc(sc[ys == 0], sc[ys == 2]))
            ic["auc_armada_vs_objeto"] = [round(float(np.nanpercentile(vals, 2.5)), 4),
                                          round(float(np.nanpercentile(vals, 97.5)), 4)]
        out["ic95_reamostragem_quadros"] = ic
    return out


def roda_cv(X, y, tipos, quadros, dobras, rng):
    """Validacao cruzada: centraliza e normaliza com a media das dobras de treino; centroide,
    kNN, PCA 2 e 10, LDA 2. Devolve as predicoes fora da dobra de cada metodo e os scores."""
    n = len(y)
    pred = {m: np.full(n, -1) for m in ("centroide", "knn5", "pca2_centroide", "pca10_centroide", "lda2_centroide")}
    score_armada = np.zeros(n)
    score_dif = np.zeros(n)
    var2, var10 = [], []
    for f in range(K_DOBRAS):
        tr, te = dobras != f, dobras == f
        mu = X[tr].mean(0)
        Ztr, Zte = normaliza(X[tr], mu), normaliza(X[te], mu)
        C = centroides(Ztr, y[tr])
        S = Zte @ C.T
        pred["centroide"][te] = S.argmax(1)
        score_armada[te] = S[:, 0]
        score_dif[te] = S[:, 0] - S[:, 2]
        pred["knn5"][te] = prediz_knn(Ztr, y[tr], Zte)
        for d, nome, lista in ((2, "pca2_centroide", var2), (10, "pca10_centroide", var10)):
            pmu, V, ve, _ = pca_ajusta(Ztr, d)
            lista.append(ve)
            pred[nome][te] = nc_euclid(pca_projeta(pmu, V, Ztr), y[tr], pca_projeta(pmu, V, Zte))
        lmu, W = lda_ajusta(Ztr, y[tr], 2)
        pred["lda2_centroide"][te] = nc_euclid((Ztr - lmu) @ W, y[tr], (Zte - lmu) @ W)
    out = {}
    for m, p in pred.items():
        out[m] = resume_predicoes(y, p, tipos, quadros,
                                  score_armada if m == "centroide" else None,
                                  score_dif if m == "centroide" else None, rng)
    out["pca_variancia_explicada"] = {"2_dim": round(float(np.mean(var2)), 4), "10_dim": round(float(np.mean(var10)), 4)}
    return out, pred, score_armada


def roda_ref(Xtr, ytr, Xte, yte, tipos_te, quadros_te, rng):
    """Ajuste na divisao de treino do corpus, teste no pool de avaliacao (o protocolo do detector)."""
    mu = Xtr.mean(0)
    Ztr, Zte = normaliza(Xtr, mu), normaliza(Xte, mu)
    C = centroides(Ztr, ytr)
    S = Zte @ C.T
    pred = {"centroide": S.argmax(1), "knn5": prediz_knn(Ztr, ytr, Zte)}
    for d in (2, 10):
        pmu, V, ve, _ = pca_ajusta(Ztr, d)
        pred[f"pca{d}_centroide"] = nc_euclid(pca_projeta(pmu, V, Ztr), ytr, pca_projeta(pmu, V, Zte))
    lmu, W = lda_ajusta(Ztr, ytr, 2)
    pred["lda2_centroide"] = nc_euclid((Ztr - lmu) @ W, ytr, (Zte - lmu) @ W)
    out = {m: resume_predicoes(yte, p, tipos_te, quadros_te,
                               S[:, 0] if m == "centroide" else None,
                               S[:, 0] - S[:, 2] if m == "centroide" else None, rng)
           for m, p in pred.items()}
    return out, pred


def tamanhos(meta):
    def est(v):
        v = np.array(v, float)
        return dict(mediana=round(float(np.median(v)), 1), p10=round(float(np.percentile(v, 10)), 1),
                    p90=round(float(np.percentile(v, 90)), 1), min=round(float(v.min()), 1),
                    max=round(float(v.max()), 1))
    out = {}
    for nome, sel in (("todas", meta), *[(CLASSES[c], [m for m in meta if m["cls"] == c]) for c in range(3)]):
        out[nome] = dict(n=len(sel), caixa_w_px=est([m["bw"] for m in sel]), caixa_h_px=est([m["bh"] for m in sel]),
                         recorte_w_px=est([m["cw"] for m in sel]), recorte_h_px=est([m["ch"] for m in sel]))
    return out


def carrega_detector(alt, pool):
    f = DETECTOR.get((alt, pool))
    if not f:
        return None, None
    d = json.load(open(os.path.join(RES, f), encoding="utf-8"))
    inst = {(i[0], i[1]): i[4] for i in d.get("instancias", [])}
    return d, inst


def analisa(d, cam, rng, completo=True):
    """Toda a analise de uma altitude numa camada. Devolve o bloco de resultados, as predicoes fora
    da dobra (cv_eval) e as do protocolo de referencia (ref_para_eval), ambas sobre o pool de
    avaliacao, mais os indices desse pool em `meta`."""
    X, y, tipos, quadros, pool = d["emb"][cam], d["y"], d["tipos"], d["quadros"], d["pool"]
    ev = pool != "train"
    ev_idx = np.where(ev)[0]
    Xe, ye, te, qe, pe = X[ev], y[ev], tipos[ev], quadros[ev], pool[ev]
    r = {}
    Ze = normaliza(Xe, Xe.mean(0))
    Zraw = Xe / np.maximum(np.linalg.norm(Xe, axis=1, keepdims=True), 1e-9)
    sil, sil_c = silhueta(Ze, ye)
    r["descritivo_eval"] = dict(
        n=int(len(ye)),
        cosim_pares_centralizado=np.round(cosim_pares(Ze, ye), 4).tolist(),
        cosim_centroides_centralizado=np.round(cosim_centroides(Ze, ye), 4).tolist(),
        cosim_pares_bruto=np.round(cosim_pares(Zraw, ye), 4).tolist(),
        cosim_centroides_bruto=np.round(cosim_centroides(Zraw, ye), 4).tolist(),
        silhueta=round(sil, 4), silhueta_por_classe={CLASSES[c]: round(sil_c[c], 4) for c in range(3)},
        ordem_das_classes=CLASSES)
    dob = dobras_estratificadas(ye, K_DOBRAS, np.random.default_rng(SEMENTE))
    r["cv_eval"], pred_cv, _ = roda_cv(Xe, ye, te, qe, dob, rng)
    r["cv_eval"]["por_pool"] = {}
    for pl in ("val", "novos"):
        m = pe == pl
        if m.any():
            r["cv_eval"]["por_pool"][pl] = {k: resume_predicoes(ye[m], pred_cv[k][m], te[m], qe[m], None, None, None)
                                            for k in ("centroide", "knn5")}
    if completo:
        dobq = dobras_por_quadro(qe, K_DOBRAS, np.random.default_rng(SEMENTE))
        r["cv_eval_quadro"], _, _ = roda_cv(Xe, ye, te, qe, dobq, None)
    tr = pool == "train"
    pred_ref = None
    if tr.any():
        r["ref_para_eval"], pred_ref = roda_ref(X[tr], y[tr], Xe, ye, te, qe, rng)
        r["ref_para_eval"]["por_pool"] = {}
        for pl in ("val", "novos"):
            m = pe == pl
            if m.any():
                r["ref_para_eval"]["por_pool"][pl] = {k: resume_predicoes(ye[m], pred_ref[k][m], te[m], qe[m], None, None, rng)
                                                      for k in ("centroide", "knn5")}
    if completo:
        dobt = dobras_por_quadro(quadros, K_DOBRAS, np.random.default_rng(SEMENTE))
        todos, _, _ = roda_cv(X, y, tipos, quadros, dobt, None)
        r["cv_todos"] = {k: todos[k] for k in ("centroide", "knn5", "pca2_centroide", "pca10_centroide",
                                               "lda2_centroide", "pca_variancia_explicada")}
    return r, pred_cv, pred_ref, ev_idx, pe, ye


def concordancia(alt, meta, ev_idx, pe, ye, pred_cv, pred_ref):
    """Por figura com objeto: o detector a chamou de armada? o classificador por similaridade tambem?
    Tabela 2 x 2, phi e kappa; `perdida` pelo detector conta como nao chamada de armada."""
    conc = {}
    for pl in ("val", "novos"):
        _, inst = carrega_detector(alt, pl)
        if not inst:
            continue
        idx = np.where((pe == pl) & (ye == 2))[0]
        for nome, predv in (("ref_para_eval_centroide", pred_ref["centroide"] if pred_ref is not None else None),
                            ("cv_eval_centroide", pred_cv["centroide"]), ("cv_eval_knn5", pred_cv["knn5"])):
            if predv is None:
                continue
            det, sim = [], []
            for i in idx:
                m = meta[ev_idx[i]]
                key = (m["quadro"], m["gi"])
                if key not in inst:
                    continue
                det.append(inst[key])
                sim.append(int(predv[i] == 0))
            det, sim = np.array(det), np.array(sim)
            if len(det) == 0:
                continue
            detectado = det != 3
            det_arm = (det == 0).astype(int)
            a = int(((det_arm == 1) & (sim == 1)).sum())
            b = int(((det_arm == 1) & (sim == 0)).sum())
            c = int(((det_arm == 0) & (sim == 1)).sum())
            dd = int(((det_arm == 0) & (sim == 0)).sum())
            den = math.sqrt(max((a + b) * (c + dd) * (a + c) * (b + dd), 1e-12))
            phi = (a * dd - b * c) / den
            po = (a + dd) / len(det)
            pe_ = ((a + b) * (a + c) + (c + dd) * (b + dd)) / len(det) ** 2
            kappa = (po - pe_) / (1 - pe_) if pe_ < 1 else float("nan")
            sub = dict(n_objetos=int(len(det)), n_detectados=int(detectado.sum()),
                       detector_chamou_armada=int(det_arm.sum()), similaridade_chamou_armada=int(sim.sum()),
                       ambos=a, so_detector=b, so_similaridade=c, nenhum=dd,
                       phi=round(phi, 3), kappa=round(kappa, 3),
                       p_sim_armada_dado_det_armada=round(float(sim[det_arm == 1].mean()), 4) if (det_arm == 1).any() else None,
                       p_sim_armada_dado_det_nao_armada=round(float(sim[det_arm == 0].mean()), 4) if (det_arm == 0).any() else None)
            if detectado.any():
                sub["entre_detectados"] = dict(
                    n=int(detectado.sum()),
                    detector_chamou_armada=round(float(det_arm[detectado].mean()), 4),
                    similaridade_chamou_armada=round(float(sim[detectado].mean()), 4),
                    ambos=int(((det_arm == 1) & (sim == 1) & detectado).sum()))
            conc.setdefault(pl, {})[nome] = sub
    return conc


def comparacao(alt, r):
    """Taxas do detector (arquivos de confusao_armado.py) ao lado das do classificador por
    similaridade, no val e nos quadros novos."""
    linhas = {}
    for pl in ("val", "novos"):
        djson, _ = carrega_detector(alt, pl)
        if djson is None:
            continue
        t = djson["taxa_por_classe_real"]
        obj, arm = t["objeto"], t["armada"]
        det = dict(objeto_chamado_de_armada=obj["armada"], n_objetos=obj["n"], perdida=obj["perdida"],
                   objeto_chamado_de_armada_entre_detectados=round(obj["armada"] / max(1 - obj["perdida"], 1e-9), 4),
                   recall_armada=arm["armada"], recall_armada_entre_detectados=round(arm["armada"] / max(1 - arm["perdida"], 1e-9), 4),
                   desarmada_chamada_de_armada=t["desarmada"]["armada"],
                   d_linha_armada_contra_objeto=round(d_linha(arm["armada"], obj["armada"]), 3),
                   pesos=os.path.basename(os.path.dirname(os.path.dirname(djson["pesos"]))), arquivo=DETECTOR[(alt, pl)])
        sim = {}
        if "ref_para_eval" in r and pl in r["ref_para_eval"]["por_pool"]:
            for k in ("centroide", "knn5"):
                s = r["ref_para_eval"]["por_pool"][pl][k]
                sim[f"ref_para_eval_{k}"] = dict(objeto_chamado_de_armada=s["objeto_chamado_de_armada"],
                                                 ic95=s.get("ic95_reamostragem_quadros", {}).get("objeto_chamado_de_armada"),
                                                 recall_armada=s["recall"]["armada"],
                                                 desarmada_chamada_de_armada=s["desarmada_chamada_de_armada"],
                                                 d_linha_armada_contra_objeto=s["d_linha_armada_contra_objeto"],
                                                 n_objetos=s["n_por_classe"]["objeto"])
        for k in ("centroide", "knn5"):
            s = r["cv_eval"]["por_pool"][pl][k]
            sim[f"cv_eval_{k}"] = dict(objeto_chamado_de_armada=s["objeto_chamado_de_armada"],
                                       recall_armada=s["recall"]["armada"],
                                       d_linha_armada_contra_objeto=s["d_linha_armada_contra_objeto"],
                                       n_objetos=s["n_por_classe"]["objeto"])
        linhas[pl] = dict(detector=det, similaridade=sim)
    return linhas


def etapa_analisar(args):
    rng = np.random.default_rng(SEMENTE)
    anterior = json.load(open(JSON_SAIDA, encoding="utf-8")) if os.path.exists(JSON_SAIDA) else {}
    saida = dict(gerado_em=dt.datetime.now().isoformat(timespec="minutes"),
                 extrator=dict(pesos=PESOS, descricao="tronco do YOLO11s pre-treinado no COCO (Ultralytics), "
                               "camadas 0 a 10 do DetectionModel, congelado; vetor = media espacial da saida da camada",
                               camadas=CAMADAS, camada_principal=CAMADA_PRINCIPAL, entrada_px=LADO,
                               reamostragem="bilinear (PIL), lado maior em 224, preenchimento cinza 114",
                               normalizacao="RGB / 255, sem media e desvio (como o Ultralytics)"),
                 recorte=dict(margem_por_lado=MARGEM, cortado_no_quadro=True),
                 protocolos=dict(
                     cv_eval="validacao cruzada de 5 dobras estratificada por classe (sorteio por recorte) no pool de "
                             "avaliacao: divisao de validacao mais quadros novos quando existem",
                     cv_eval_quadro="idem, mas as dobras sao sorteadas por quadro (recortes do mesmo quadro ficam na "
                                    "mesma dobra), para medir o vazamento entre recortes do mesmo quadro",
                     ref_para_eval="centroides, vizinhos e projecoes ajustados na divisao de TREINO do corpus e "
                                   "aplicados ao pool de avaliacao; e o protocolo do detector (val e quadros novos "
                                   "reportados em separado)",
                     cv_todos="validacao cruzada de 5 dobras por quadro em todos os recortes do corpus (treino, "
                              "validacao e quadros novos), so como leitura suplementar com mais dados"),
                 centralizacao="cada vetor e centralizado pela media do pool de ajuste e normalizado a norma 1; "
                               "similaridade = cosseno (produto interno)",
                 reamostragem=dict(n=N_BOOT, unidade="quadro", semente=SEMENTE),
                 pools={}, validacao_regra_tipos={}, tamanhos={}, camadas={k: {} for k in CAMADAS},
                 comparacao_detector={}, concordancia_detector={})
    if "extrator_treinado_na_tarefa" in anterior:
        saida["extrator_treinado_na_tarefa"] = anterior["extrator_treinado_na_tarefa"]

    dados = {alt: monta_dados(alt) for alt in POOLS}
    for alt, d in dados.items():
        p = POOLS[alt]
        saida["validacao_regra_tipos"].update(d["validacoes"])
        y, tipos, quadros, pool = d["y"], d["tipos"], d["quadros"], d["pool"]
        saida["pools"][alt] = dict(
            corpus=p["corpus"], quadros_novos=p["extra"], altitude_m=p["alt_m"], gsd_cm_px=p["gsd_cm"],
            recortes={k: int((pool == k).sum()) for k in ("train", "val", "novos")},
            quadros={k: int(len(np.unique(quadros[pool == k]))) for k in ("train", "val", "novos")},
            por_classe_eval={CLASSES[c]: int(((pool != "train") & (y == c)).sum()) for c in range(3)},
            por_classe_train={CLASSES[c]: int(((pool == "train") & (y == c)).sum()) for c in range(3)},
            tipos_eval={t: int(((pool != "train") & (tipos == t)).sum()) for t in sorted(set(tipos)) if t})
        saida["tamanhos"][alt] = dict(eval=tamanhos([m for m, pl in zip(d["meta"], pool) if pl != "train"]),
                                      todos=tamanhos(d["meta"]))

    for cam in CAMADAS:
        for alt, d in dados.items():
            r, pred_cv, pred_ref, ev_idx, pe, ye = analisa(d, cam, rng, completo=True)
            saida["camadas"][cam][alt] = r
            if cam == CAMADA_PRINCIPAL:
                conc = concordancia(alt, d["meta"], ev_idx, pe, ye, pred_cv, pred_ref)
                if conc:
                    saida["concordancia_detector"][alt] = conc
                saida["comparacao_detector"][alt] = comparacao(alt, r)
            print(f"[sim] analise {cam} {alt} pronta", flush=True)

    with open(JSON_SAIDA, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=1)
    print(f"[sim] gravado {JSON_SAIDA}")
    imprime_resumo(saida["camadas"][CAMADA_PRINCIPAL], CAMADA_PRINCIPAL)


def etapa_treinado(args):
    """Suplemento: o mesmo pipeline com o tronco do detector treinado em cada corpus."""
    saida = json.load(open(JSON_SAIDA, encoding="utf-8"))
    device = prepara_torch(args)
    rng = np.random.default_rng(SEMENTE + 1)
    bloco = dict(descricao="tronco (camadas 0 a 10) do detector de tres classes treinado em cada corpus, congelado; "
                           "mesmo recorte, mesma entrada e mesma analise, so na camada P5 e nos protocolos cv_eval e "
                           "ref_para_eval. Referencia superior, NAO livre de modelo: a divisao de treino foi vista no "
                           "treino e a de validacao selecionou o checkpoint; so os quadros novos sao inéditos.",
                 camada=CAMADA_PRINCIPAL, pesos={}, resultados={}, comparacao_detector={}, concordancia_detector={})
    for alt, p in POOLS.items():
        pesos = os.path.join(BL, "runs", "detect", p["detector"], "weights", "best.pt")
        sufixo = "__" + p["detector"]
        bloco["pesos"][alt] = pesos
        ext = None
        for ds in (p["corpus"], p["extra"]):
            if ds and (args.refazer or not os.path.exists(caminho_cache(ds, sufixo))):
                if ext is None:
                    ext = Extrator(pesos, device, CAMADAS)
                extrai_e_grava(ds, ext, args, sufixo)
        d = monta_dados(alt, sufixo)
        r, pred_cv, pred_ref, ev_idx, pe, ye = analisa(d, CAMADA_PRINCIPAL, rng, completo=False)
        bloco["resultados"][alt] = r
        conc = concordancia(alt, d["meta"], ev_idx, pe, ye, pred_cv, pred_ref)
        if conc:
            bloco["concordancia_detector"][alt] = conc
        bloco["comparacao_detector"][alt] = comparacao(alt, r)
        print(f"[sim] treinado {alt} pronto", flush=True)
    saida["extrator_treinado_na_tarefa"] = bloco
    with open(JSON_SAIDA, "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=1)
    print(f"[sim] gravado {JSON_SAIDA} (chave extrator_treinado_na_tarefa)")
    imprime_resumo(bloco["resultados"], "P5 do detector treinado")


def imprime_resumo(por_alt, titulo):
    print(f"\n=== resumo, {titulo} ===")
    for alt in POOLS:
        if alt not in por_alt:
            continue
        r = por_alt[alt]
        d = r["descritivo_eval"]
        cv = r["cv_eval"]
        print(f"\n[{alt}] n eval {d['n']}  silhueta {d['silhueta']:.3f}  cosim centralizado:")
        for a in range(3):
            print("   ", CLASSES[a][:9].ljust(10), " ".join(f"{v:6.3f}" for v in d["cosim_pares_centralizado"][a]))
        for m in ("centroide", "knn5", "pca2_centroide", "pca10_centroide", "lda2_centroide"):
            c = cv[m]
            print(f"  {m:16s} acc {c['acuracia']:.3f} bal {c['acuracia_balanceada']:.3f} "
                  f"recall {c['recall']['armada']:.3f}/{c['recall']['desarmada']:.3f}/{c['recall']['objeto']:.3f} "
                  f"obj->arm {c['objeto_chamado_de_armada']:.3f} des->arm {c['desarmada_chamada_de_armada']:.3f} "
                  f"d' {c['d_linha_armada_contra_objeto']:.2f}"
                  + (f" AUC {c['auc_armada_vs_objeto_sim_centroide_armada']:.3f}" if m == "centroide" else ""))
        print(f"  PCA var 2d {cv['pca_variancia_explicada']['2_dim']:.3f} 10d {cv['pca_variancia_explicada']['10_dim']:.3f}")
        if "ref_para_eval" in r:
            c = r["ref_para_eval"]["centroide"]
            print(f"  ref->eval centroide: obj->arm {c['objeto_chamado_de_armada']:.3f} recall arm {c['recall']['armada']:.3f} "
                  f"AUC {c['auc_armada_vs_objeto_sim_centroide_armada']:.3f}")
        ot = cv["centroide"]["objeto_por_tipo"]
        print("  por tipo (centroide, cv):", ", ".join(f"{t} {v['chamada_de_armada']:.2f} (n {v['n']})" for t, v in ot.items()))


# ----------------------------------------------------------------------------------------------
# etapa 3: figura
# ----------------------------------------------------------------------------------------------
def etapa_figura(args):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.lines import Line2D
    AZUL, LARANJA, AGUA, CINZA, TINTA = "#2a78d6", "#eb6834", "#1baf7a", "#8a8a86", "#0b0b0b"
    COR = {0: LARANJA, 1: AZUL, 2: AGUA}
    plt.rcParams.update({"font.family": "Arial", "font.size": 7.5, "axes.edgecolor": "#555",
                         "axes.linewidth": 0.6, "xtick.color": "#333", "ytick.color": "#333"})
    s = json.load(open(JSON_SAIDA, encoding="utf-8"))
    cam = s["extrator"]["camada_principal"]
    alts = ["35", "75g", "150g"]
    matrizes = {a: np.array(s["camadas"][cam][a]["descritivo_eval"]["cosim_pares_centralizado"]) for a in alts}
    vlim = max(float(np.abs(M).max()) for M in matrizes.values())
    vlim = math.ceil(vlim * 100) / 100          # escala comum, simetrica em zero
    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.7), dpi=300,
                             gridspec_kw=dict(height_ratios=[1.3, 1.0], hspace=0.32, wspace=0.28))
    rng = np.random.default_rng(1)
    for j, alt in enumerate(alts):
        p = POOLS[alt]
        d = monta_dados(alt)
        ev = d["pool"] != "train"
        X, y = d["emb"][cam][ev], d["y"][ev]
        Z = normaliza(X, X.mean(0))
        mu, V, ve, var = pca_ajusta(Z, 2)
        P = pca_projeta(mu, V, Z)
        for k in range(2):      # sinal dos eixos: centroide de armada a direita e acima
            if P[y == 0, k].mean() < P[y != 0, k].mean():
                P[:, k] *= -1
        ax = axes[0, j]
        ordem = rng.permutation(len(y))
        ax.scatter(P[ordem, 0], P[ordem, 1], c=[COR[c] for c in y[ordem]], s=3.0, alpha=0.45, lw=0, rasterized=True)
        for c in (1, 2, 0):
            cx, cy = P[y == c].mean(0)
            ax.plot(cx, cy, marker="o", ms=5, mfc=COR[c], mec="white", mew=1.0, zorder=5 + c)
        alcas = [Line2D([], [], marker="o", ls="none", ms=4.5, mfc=COR[c], mec="white", mew=0.6,
                        label=f"{CLASSES_EN[c]} (n = {(y == c).sum():,})") for c in range(3)]
        ax.legend(handles=alcas, loc="lower left", frameon=False, fontsize=6.8, handletextpad=0.25,
                  borderaxespad=0.35, labelspacing=0.25, labelcolor=TINTA)
        ax.set_xlabel(f"PC1 ({var[0] * 100:.0f}% of variance)")
        ax.set_ylabel(f"PC2 ({var[1] * 100:.0f}%)")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.02, 0.97, p["rotulo"], transform=ax.transAxes, ha="left", va="top", fontsize=7.5,
                fontweight="bold", color=TINTA)
        sil = s["camadas"][cam][alt]["descritivo_eval"]["silhueta"]
        ax.text(0.02, 0.905, f"silhouette {sil:.2f}", transform=ax.transAxes, ha="left", va="top", color="#444")
        # matriz de co-similaridade: divergente (laranja negativo, cinza zero, azul positivo), escala comum
        M = matrizes[alt]
        ax2 = axes[1, j]
        cmap = LinearSegmentedColormap.from_list("div", [LARANJA, "#f1f1ef", AZUL])
        ax2.imshow(M, cmap=cmap, vmin=-vlim, vmax=vlim, aspect="equal")
        for a in range(3):
            for b in range(3):
                ax2.text(b, a, f"{M[a, b]:+.3f}", ha="center", va="center", fontsize=7.2, color=TINTA)
        ax2.set_xticks(range(3))
        ax2.set_yticks(range(3))
        ax2.set_xticklabels(CLASSES_EN)
        ax2.set_yticklabels(CLASSES_EN if j == 0 else ["", "", ""])
        ax2.tick_params(length=0)
        for sp in ax2.spines.values():
            sp.set_visible(False)
        if j == 1:
            ax2.text(0.5, -0.27, f"mean pairwise cosine similarity of centred features; common scale, "
                                 f"orange {-vlim:+.2f} to blue {vlim:+.2f}", transform=ax2.transAxes,
                     ha="center", va="top", color="#444")
    fig.savefig(os.path.join(FIGS, "fig13_similaridade.png"), bbox_inches="tight", pad_inches=0.05)
    print(f"[sim] gravado {os.path.join(FIGS, 'fig13_similaridade.png')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--etapa", choices=["extrair", "analisar", "treinado", "figura", "tudo"], default="tudo")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--threads", type=int, default=6)
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--limite", type=int, default=0, help="teste de fumaca: so N quadros por corpus, sem gravar")
    a = ap.parse_args()
    if a.etapa in ("extrair", "tudo"):
        etapa_extrair(a)
    if a.etapa in ("analisar", "tudo"):
        etapa_analisar(a)
    if a.etapa in ("treinado", "tudo"):
        etapa_treinado(a)
    if a.etapa in ("figura", "tudo"):
        etapa_figura(a)
