#!/usr/bin/env python3
"""
rodada4.py: a rodada iniciada em 27/09, em uma cadeia so, idempotente e retomavel (molde da rodada 3).

Desenho, criterios fixados antes de rodar e custo em 03-blender/PLANO-RODADA4.md. Cada etapa tem um
arquivo de prova; se ele existe, a etapa e pulada. Render retoma pelo manifest; treino retoma do
last.pt e so conta como feito com TREINO_OK. Uma trava impede duas instancias.

Grupos, na ordem (um grupo que falha nao impede os outros):
  K  avaliacoes rapidas: VisDrone pela regra oficial e a IoU 0,50/0,60/0,75 (10.6), confusao armada a
     IoU 0,60 e 0,75, escala casada pelo lado maior (10.2), instancias dos val para bootstrap
  H  objeto carregado como arma: gemeo do teste de arma inedita, com o objeto no porte da arma (9.5)
  F  sintetico e real no mesmo treino: S-oblique-six + 5% e + 10% do VisDrone, a partir do COCO
  E  150 m com objetos confundiveis: gemeo do corpus de 35 m a 150 m, 3 classes (11.5)
  I  validacao maior: 80 quadros novos a 35 m e os gemeos a 75 m (a diferenca de p 0,06)
  J  regime de luz: 120 quadros novos do corpus nadir, 20 por regime (10.3)
  G  sementes de treino 1 e 2: S-oblique-six, ajuste fino a 5%, armado 35 m e gemeo 75 m (10.6)
  Y  fechamento: VisDrone oficial dos modelos novos e os criterios (rodada4_criterios.json)

Uso:  python rodada4.py            (roda o que falta)
      python rodada4.py --listar   (mostra as etapas e o estado)
"""
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime

SCR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(SCR))
RES = os.path.join(REPO, "06-resultados")
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
FILA = os.path.join(RAIZ, "fila4")
LOG = os.path.join(RAIZ, "rodada4.log")
ESTADO = os.path.join(FILA, "estado.json")
TRAVA = os.path.join(FILA, "rodada4.trava")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
BLENDER = os.path.join("C:" + os.sep, "Program Files (x86)", "Steam", "steamapps", "common",
                       "Blender", "blender.exe")
VIS_YAML = os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "visdrone_yolo", "data.yaml")
FT = os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "ft")

# mesma receita de todos os bracos anteriores
MODELO, IMGSZ, EPOCAS, BATCH, WORKERS = "yolo11s.pt", 1280, 60, 6, 4
EPOCAS_FT = 30

# identico ao comando que gerou ds_armado_75 (etapa 16 da fila antiga), menos semente e armas: e o
# comando do teste de arma inedita da rodada 3 (ds_armado_75_inedita)
INEDITA = ["--samples", 96, "--res", 3840, 2160, "--people", 14, 30, "--pool", 6, "--seed", 47,
           "--climas", "todos", "--alt", 75, "--mistura", 0.34, 0.33, 0.33,
           "--armas", "mista_inedita"]
# identico ao comando que gerou ds_armado_35 (etapa 25 da fila antiga)
ARMADO35 = ["--samples", 64, "--res", 3840, 2160, "--people", 12, 24, "--pool", 6, "--seed", 43,
            "--climas", "todos", "--alt", 35, "--alt-jitter", 3, "--mistura", 0.34, 0.33, 0.33,
            "--porte-realista", "--fio-gsd", "--laje", 0.75, "--amostra-no-quadro"]


def gemeo(alt, jitter):
    """o comando do 35 m mudando so a altura e o jitter, proporcional (3 m a 35 m)"""
    c = list(ARMADO35)
    c[c.index("--alt") + 1] = alt
    c[c.index("--alt-jitter") + 1] = jitter
    return c


GEMEO75 = gemeo(75, 6)          # o da rodada 3
GEMEO150 = gemeo(150, 13)       # 3 x 150 / 35 = 12,9
# o comando do controle ds_morro_4k (sitio -1, semente 21), como no braco de variedade da fila antiga
NADIR4K = ["--samples", 96, "--res", 3840, 2160, "--people", 16, 34, "--pool", 6, "--seed", 21,
           "--climas", "todos", "--sitio", -1, "--mistura", 0.5, 0.5, 0.0, "--enquadro", "quadrado"]

VISDRONE_9 = ["r_pareado", "s_nadir_4k", "s_variedade", "s_obliquo", "s_oblvar",
              "ft05_sint", "ft05_coco", "ft10_sint", "ft10_coco"]
VISDRONE_NOVOS = ["misto05", "misto10", "s_oblvar_sd1", "s_oblvar_sd2", "ft05_sint_sd1", "ft05_sint_sd2",
                  "ft05_coco_sd1", "ft05_coco_sd2"]


def j(*p):
    return os.path.join(*[str(x) for x in p])


def log(m):
    linha = f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}"
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linha + "\n")
    print(linha, flush=True)


def carrega():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def grava(e):
    tmp = ESTADO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(e, f, indent=1, ensure_ascii=False)
    os.replace(tmp, ESTADO)


def marca(eid, **kw):
    e = carrega()
    e.setdefault(eid, {}).update(kw)
    grava(e)


def linhas(p):
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for ln in f if ln.strip())
    except OSError:
        return 0


def roda(cmd, nome_log):
    cmd = [str(c) for c in cmd]
    with open(j(FILA, nome_log), "a", encoding="utf-8", buffering=1) as f:
        f.write(f"\n# {datetime.now():%Y-%m-%d %H:%M:%S}\n# {' '.join(cmd)}\n\n")
        f.flush()
        return subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=RAIZ)


def ok_arq(p):
    return os.path.join(FILA, p + ".ok")


def marca_ok(eid):
    with open(ok_arq(eid), "w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat(timespec="seconds"))
    return 0


# ------------------------------------------------------------------ primitivas idempotentes
def render(nome_log, out, n, extra, inicio=0):
    """n quadros a partir do indice `inicio` do comando `extra`. Com inicio > 0 o gerador sorteia (sem
    renderizar) os quadros anteriores, entao os novos continuam a sequencia do corpus original."""
    feitos = linhas(j(out, "manifest.jsonl"))
    if os.path.exists(j(out, "data.yaml")) and feitos >= n:
        return 0
    cmd = [BLENDER, "-b", "--python-exit-code", 1, "--python", j(SCR, "gen_morro.py"), "--",
           "--out", out, "--dataset", inicio + n, *extra, "--start", inicio + feitos]
    log(f"  render {os.path.basename(out)}: de {feitos}/{n}" + (f" (indices {inicio} a {inicio + n - 1})" if inicio else ""))
    return roda(cmd, nome_log)


def ladrilha(ds, ds_t, nome_log):
    if os.path.exists(j(ds_t, "data.yaml")):
        return 0
    return roda([PY, j(SCR, "tile_dataset.py"), "--data", ds, "--out", ds_t,
                 "--tile", 1280, "--overlap", 0.2], nome_log)


def treina(nome, data, modelo, epocas, single, nome_log, semente=0):
    rd = j(RAIZ, "runs", "detect", nome)
    ok = j(rd, "TREINO_OK")
    if os.path.exists(ok):
        return 0
    last = j(rd, "weights", "last.pt")
    if os.path.exists(last):
        log(f"  treino {nome}: retomando de {last}")
        codigo = f"from ultralytics import YOLO\nYOLO(r'{last}').train(resume=True)\n"
        rc = roda([PY, "-c", codigo], nome_log)
        if rc != 0:
            with open(j(FILA, nome_log), encoding="utf-8", errors="replace") as f:
                cauda = f.read()[-4000:]
            if "nothing to resume" in cauda or "is finished" in cauda:
                rc = 0
    else:
        log(f"  treino {nome}: do zero, a partir de {os.path.basename(str(modelo))}, semente {semente}")
        cmd = [PY, j(SCR, "train_yolo_win.py"), "--data", data, "--model", modelo,
               "--imgsz", IMGSZ, "--epochs", epocas, "--batch", BATCH, "--workers", WORKERS,
               "--name", nome, "--seed", semente] + (["--single-cls"] if single else [])
        rc = roda(cmd, nome_log)
    if rc == 0 and os.path.exists(j(rd, "weights", "best.pt")):
        with open(ok, "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat())
    return rc


def pesos(nome):
    return j(RAIZ, "runs", "detect", nome, "weights", "best.pt")


def avalia(p, saida, nome_log, imgsz=IMGSZ):
    if os.path.exists(saida):
        return 0
    return roda([PY, j(SCR, "avalia_sim2real.py"), "--weights", p, "--real", VIS_YAML,
                 "--imgsz", imgsz, "--out", saida], nome_log)


def confusao(p, ds, split, saida, nome_log, iou=None, inst=False):
    if os.path.exists(saida):
        return 0
    cmd = [PY, j(RES, "confusao_armado.py"), "--pesos", p, "--ds", ds, "--split", split, "--out", saida]
    if iou is not None:
        cmd += ["--iou", iou]
    if inst:
        cmd += ["--instancias"]
    return roda(cmd, nome_log)


def varios(*chamadas):
    """roda uma lista de (funcao, args) em ordem e para no primeiro rc != 0"""
    for fn, *a in chamadas:
        rc = fn(*a)
        if rc != 0:
            return rc
    return 0


# ------------------------------------------------------------------ etapas compostas
def k1(L):
    rc = roda([PY, j(RES, "avalia_visdrone_oficial.py"), "--modelos", *VISDRONE_9,
               "--out", j(RES, "visdrone_oficial_iou.json")], L)
    d = json.load(open(j(RES, "visdrone_oficial_iou.json"), encoding="utf-8")) if os.path.exists(
        j(RES, "visdrone_oficial_iou.json")) else {}
    if rc == 0 and all(m in d.get("modelos", {}) for m in VISDRONE_9):
        return marca_ok("K1")
    return rc or 1


def k2(L):
    ch = []
    for nome, ds in (("armado_75", "ds_armado_75"), ("armado_35", "ds_armado_35"), ("armado_75g", "ds_armado_75g")):
        for iou in (0.6, 0.75):
            ch.append((confusao, pesos(nome), j(RAIZ, ds), "val",
                       j(RES, f"confusao_{nome}_iou{int(round(iou * 100))}.json"), L, iou))
    rc = varios(*ch)
    return marca_ok("K2") if rc == 0 else rc


def k4(L):
    rc = varios(*[(confusao, pesos(n), j(RAIZ, ds), "val", j(RES, f"confusao_{n}_inst.json"), L, None, True)
                  for n, ds in (("armado_75", "ds_armado_75"), ("armado_35", "ds_armado_35"),
                                ("armado_75g", "ds_armado_75g"))])
    return marca_ok("K4") if rc == 0 else rc


def h2(L):
    """os dois corpus de teste sao gemeos caixa a caixa? (mesma semente, mesmos sorteios)"""
    def carrega_mf(d):
        return {json.loads(x)["img"]: json.loads(x)["caixas"] for x in open(j(RAIZ, d, "manifest.jsonl"), encoding="utf-8") if x.strip()}
    a, b = carrega_mf("ds_armado_75_inedita"), carrega_mf("ds_armado_75_porte")
    iguais = [k for k in a if k in b and a[k] == b[k]]
    out = {"quadros_inedita": len(a), "quadros_porte": len(b), "quadros_com_caixas_identicas": len(iguais),
           "quadros_diferentes": sorted(k for k in a if k not in iguais),
           "nota": "caixas = [classe, tipo, laje] por linha de rotulo; quadro identico permite parear instancia a instancia"}
    json.dump(out, open(j(RES, "porte_arma_gemeo.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    log(f"  gemeo do porte: {len(iguais)}/{len(a)} quadros com caixas identicas")
    return 0


def monta_misto(fatia, L):
    """S-oblique-six (ladrilhos de treino) + a fatia real, num corpus so, por link fisico"""
    dst = j(RAIZ, f"ds_misto{fatia[2:]}")
    if os.path.exists(j(dst, "data.yaml")):
        return 0
    shutil.rmtree(dst, ignore_errors=True)
    for sub in ("images/train", "labels/train"):
        os.makedirs(j(dst, *sub.split("/")), exist_ok=True)
    n = {"sintetico": 0, "real": 0}
    fontes = [("sintetico", j(RAIZ, "ds_oblvar_tiles", "images", "train"), j(RAIZ, "ds_oblvar_tiles", "labels", "train")),
              ("real", j(FT, fatia, "images"), j(FT, fatia, "labels"))]
    for tipo, di, dl in fontes:
        for f in sorted(os.listdir(di)):
            base = os.path.splitext(f)[0]
            try:
                os.link(j(di, f), j(dst, "images", "train", f))
            except OSError:
                shutil.copy2(j(di, f), j(dst, "images", "train", f))
            lab = j(dl, base + ".txt")
            if os.path.exists(lab):
                shutil.copy2(lab, j(dst, "labels", "train", base + ".txt"))
            n[tipo] += 1
    # classe 1 = pessoa sintetica (o corpus obliquo so tem desarmadas); com single_cls vira uma classe so
    with open(j(dst, "data.yaml"), "w", encoding="utf-8") as f:
        f.write(f"path: {dst.replace(os.sep, '/')}\ntrain: images/train\nval: {j(FT, 'sel', 'images').replace(os.sep, '/')}\n"
                "names:\n  0: pessoa\n  1: pessoa_sintetica\n")
    json.dump(n, open(j(dst, "composicao.json"), "w", encoding="utf-8"))
    log(f"  ds_misto{fatia[2:]}: {n}")
    return 0


def f1(L):
    return varios((monta_misto, "ft05", L), (monta_misto, "ft10", L))


def g_ft(nome, init, semente, L):
    if init == "sint":
        base = f"s_oblvar_sd{semente}"
        if not os.path.exists(j(RAIZ, "runs", "detect", base, "TREINO_OK")):
            log(f"  {nome}: falta o peso de partida {base}")
            return 1
        return treina(nome, j(FT, "ft05.yaml"), pesos(base), EPOCAS_FT, True, L, semente)
    return treina(nome, j(FT, "ft05.yaml"), MODELO, EPOCAS_FT, True, L, semente)


def g_avalia(L):
    rc = varios(*[(avalia, pesos(n), j(RES, f"sim2real_{n}.json"), L)
                  for n in ("s_oblvar_sd1", "s_oblvar_sd2", "ft05_sint_sd1", "ft05_sint_sd2",
                            "ft05_coco_sd1", "ft05_coco_sd2")])
    return marca_ok("G7") if rc == 0 else rc


def g_confusao(L):
    ch = []
    for n, ds in (("armado_35", "ds_armado_35"), ("armado_75g", "ds_armado_75g")):
        for s in (1, 2):
            ch.append((confusao, pesos(f"{n}_sd{s}"), j(RAIZ, ds), "val", j(RES, f"confusao_{n}_sd{s}.json"), L, None, True))
            extra = j(RAIZ, f"{ds}_extra")
            if os.path.exists(j(extra, "data.yaml")):
                ch.append((confusao, pesos(f"{n}_sd{s}"), extra, "val", j(RES, f"extra_{n}_sd{s}.json"), L, None, True))
    rc = varios(*ch)
    return marca_ok("G12") if rc == 0 else rc


def y1(L):
    rc = roda([PY, j(RES, "avalia_visdrone_oficial.py"), "--modelos", *VISDRONE_NOVOS,
               "--out", j(RES, "visdrone_oficial_iou.json")], L)
    return marca_ok("Y1") if rc == 0 else rc


# (id, grupo, descricao, funcao(nome_log) -> rc, prova)
ETAPAS = [
    ("K1", "K", "VisDrone: regra oficial e IoU 0,5/0,6/0,75 (9 modelos)", k1, ok_arq("K1")),
    ("K2", "K", "confusao armada a IoU 0,60 e 0,75", k2, ok_arq("K2")),
    ("K3", "K", "10.2: escala casada pelo lado maior",
     lambda L: roda([PY, j(RES, "escala_casada.py")], L), j(RES, "sim2real_r_pareado_casada.json")),
    ("K4", "K", "instancias dos val armados (bootstrap)", k4, ok_arq("K4")),

    ("H1", "H", "render gemeo do teste inedito com objeto no porte de arma",
     lambda L: render(L, j(RAIZ, "ds_armado_75_porte"), 50, INEDITA + ["--objeto-porte-arma"]),
     j(RAIZ, "ds_armado_75_porte", "data.yaml")),
    ("H2", "H", "confere o gemeo caixa a caixa", h2, j(RES, "porte_arma_gemeo.json")),
    ("H3", "H", "armado_75: inedito (porte normal) com instancias",
     lambda L: confusao(pesos("armado_75"), j(RAIZ, "ds_armado_75_inedita"), "todos", j(RES, "holdout_armas_armado_75_inst.json"), L, None, True),
     j(RES, "holdout_armas_armado_75_inst.json")),
    ("H4", "H", "armado_75: objeto no porte de arma",
     lambda L: confusao(pesos("armado_75"), j(RAIZ, "ds_armado_75_porte"), "todos", j(RES, "porte_arma_armado_75.json"), L, None, True),
     j(RES, "porte_arma_armado_75.json")),
    ("H5", "H", "armado_75g: os dois corpus de teste",
     lambda L: varios((confusao, pesos("armado_75g"), j(RAIZ, "ds_armado_75_inedita"), "todos", j(RES, "holdout_armas_armado_75g_inst.json"), L, None, True),
                      (confusao, pesos("armado_75g"), j(RAIZ, "ds_armado_75_porte"), "todos", j(RES, "porte_arma_armado_75g.json"), L, None, True)),
     j(RES, "porte_arma_armado_75g.json")),

    ("F1", "F", "monta os corpus mistos (S-oblique-six + 5% e + 10%)", f1, j(RAIZ, "ds_misto10", "data.yaml")),
    ("F2", "F", "treino misto05 (a partir do COCO)",
     lambda L: treina("misto05", j(RAIZ, "ds_misto05", "data.yaml"), MODELO, EPOCAS_FT, True, L),
     j(RAIZ, "runs", "detect", "misto05", "TREINO_OK")),
    ("F3", "F", "treino misto10 (a partir do COCO)",
     lambda L: treina("misto10", j(RAIZ, "ds_misto10", "data.yaml"), MODELO, EPOCAS_FT, True, L),
     j(RAIZ, "runs", "detect", "misto10", "TREINO_OK")),
    ("F4", "F", "teste dos mistos no VisDrone val",
     lambda L: varios((avalia, pesos("misto05"), j(RES, "sim2real_misto05.json"), L),
                      (avalia, pesos("misto10"), j(RES, "sim2real_misto10.json"), L)),
     j(RES, "sim2real_misto10.json")),

    ("E1", "E", "render gemeo a 150 m do corpus de 35 m, 200 quadros",
     lambda L: render(L, j(RAIZ, "ds_armado_150g"), 200, GEMEO150), j(RAIZ, "ds_armado_150g", "data.yaml")),
    ("E2", "E", "ladrilhos do gemeo 150 m",
     lambda L: ladrilha(j(RAIZ, "ds_armado_150g"), j(RAIZ, "ds_armado_150g_tiles"), L), j(RAIZ, "ds_armado_150g_tiles", "data.yaml")),
    ("E3", "E", "treino armado_150g (3 classes)",
     lambda L: treina("armado_150g", j(RAIZ, "ds_armado_150g_tiles", "data.yaml"), MODELO, EPOCAS, False, L),
     j(RAIZ, "runs", "detect", "armado_150g", "TREINO_OK")),
    ("E4", "E", "confusao armado_150g com instancias",
     lambda L: confusao(pesos("armado_150g"), j(RAIZ, "ds_armado_150g"), "val", j(RES, "confusao_armado_150g.json"), L, None, True),
     j(RES, "confusao_armado_150g.json")),

    ("I1", "I", "render 80 quadros novos a 35 m (indices 200 a 279)",
     lambda L: render(L, j(RAIZ, "ds_armado_35_extra"), 80, ARMADO35 + ["--val", 1.0], inicio=200),
     j(RAIZ, "ds_armado_35_extra", "data.yaml")),
    ("I2", "I", "render os gemeos a 75 m dos 80 quadros",
     lambda L: render(L, j(RAIZ, "ds_armado_75g_extra"), 80, GEMEO75 + ["--val", 1.0], inicio=200),
     j(RAIZ, "ds_armado_75g_extra", "data.yaml")),
    ("I3", "I", "confusao armado_35 nos quadros novos",
     lambda L: confusao(pesos("armado_35"), j(RAIZ, "ds_armado_35_extra"), "val", j(RES, "extra_armado_35.json"), L, None, True),
     j(RES, "extra_armado_35.json")),
    ("I4", "I", "confusao armado_75g nos gemeos novos",
     lambda L: confusao(pesos("armado_75g"), j(RAIZ, "ds_armado_75g_extra"), "val", j(RES, "extra_armado_75g.json"), L, None, True),
     j(RES, "extra_armado_75g.json")),

    ("J1", "J", "render 120 quadros novos do nadir 4K (indices 180 a 299)",
     lambda L: render(L, j(RAIZ, "ds_regime_4k"), 120, NADIR4K + ["--val", 1.0], inicio=180),
     j(RAIZ, "ds_regime_4k", "data.yaml")),
    ("J2", "J", "ladrilhos do corpus por regime",
     lambda L: ladrilha(j(RAIZ, "ds_regime_4k"), j(RAIZ, "ds_regime_4k_tiles"), L), j(RAIZ, "ds_regime_4k_tiles", "data.yaml")),
    ("J3", "J", "desempenho do s_nadir_4k por regime (10.3)",
     lambda L: roda([PY, j(RES, "por_regime.py"), "--pesos", pesos("s_nadir_4k"), "--ds", j(RAIZ, "ds_regime_4k"),
                     "--tiles", j(RAIZ, "ds_regime_4k_tiles")], L),
     j(RES, "por_regime_s_nadir_4k.json")),

    ("G1", "G", "treino s_oblvar semente 1",
     lambda L: treina("s_oblvar_sd1", j(RAIZ, "ds_oblvar_tiles", "data.yaml"), MODELO, EPOCAS, True, L, 1),
     j(RAIZ, "runs", "detect", "s_oblvar_sd1", "TREINO_OK")),
    ("G2", "G", "treino s_oblvar semente 2",
     lambda L: treina("s_oblvar_sd2", j(RAIZ, "ds_oblvar_tiles", "data.yaml"), MODELO, EPOCAS, True, L, 2),
     j(RAIZ, "runs", "detect", "s_oblvar_sd2", "TREINO_OK")),
    ("G3", "G", "ajuste fino 5% do sintetico, semente 1", lambda L: g_ft("ft05_sint_sd1", "sint", 1, L),
     j(RAIZ, "runs", "detect", "ft05_sint_sd1", "TREINO_OK")),
    ("G4", "G", "ajuste fino 5% do sintetico, semente 2", lambda L: g_ft("ft05_sint_sd2", "sint", 2, L),
     j(RAIZ, "runs", "detect", "ft05_sint_sd2", "TREINO_OK")),
    ("G5", "G", "treino 5% do COCO, semente 1", lambda L: g_ft("ft05_coco_sd1", "coco", 1, L),
     j(RAIZ, "runs", "detect", "ft05_coco_sd1", "TREINO_OK")),
    ("G6", "G", "treino 5% do COCO, semente 2", lambda L: g_ft("ft05_coco_sd2", "coco", 2, L),
     j(RAIZ, "runs", "detect", "ft05_coco_sd2", "TREINO_OK")),
    ("G7", "G", "teste no VisDrone dos seis modelos de semente", g_avalia, ok_arq("G7")),
    ("G8", "G", "treino armado_35 semente 1",
     lambda L: treina("armado_35_sd1", j(RAIZ, "ds_armado_35_tiles", "data.yaml"), MODELO, EPOCAS, False, L, 1),
     j(RAIZ, "runs", "detect", "armado_35_sd1", "TREINO_OK")),
    ("G9", "G", "treino armado_35 semente 2",
     lambda L: treina("armado_35_sd2", j(RAIZ, "ds_armado_35_tiles", "data.yaml"), MODELO, EPOCAS, False, L, 2),
     j(RAIZ, "runs", "detect", "armado_35_sd2", "TREINO_OK")),
    ("G10", "G", "treino armado_75g semente 1",
     lambda L: treina("armado_75g_sd1", j(RAIZ, "ds_armado_75g_tiles", "data.yaml"), MODELO, EPOCAS, False, L, 1),
     j(RAIZ, "runs", "detect", "armado_75g_sd1", "TREINO_OK")),
    ("G11", "G", "treino armado_75g semente 2",
     lambda L: treina("armado_75g_sd2", j(RAIZ, "ds_armado_75g_tiles", "data.yaml"), MODELO, EPOCAS, False, L, 2),
     j(RAIZ, "runs", "detect", "armado_75g_sd2", "TREINO_OK")),
    ("G12", "G", "confusao dos quatro armados de semente (val e quadros novos)", g_confusao, ok_arq("G12")),

    ("Y1", "Y", "VisDrone oficial e IoU dos modelos novos", y1, ok_arq("Y1")),
    ("Y2", "Y", "criterios fixados no PLANO-RODADA4",
     lambda L: roda([PY, j(RES, "rodada4_criterios.py")], L), j(RES, "rodada4_criterios.json")),
]


def trava():
    """uma instancia so. psutil vem com o ultralytics."""
    import psutil
    if os.path.exists(TRAVA):
        try:
            pid = int(open(TRAVA).read().strip())
            if psutil.pid_exists(pid) and any(os.path.basename(a) == "rodada4.py"
                                              for a in psutil.Process(pid).cmdline()):
                return False
        except (ValueError, OSError, psutil.Error):
            pass
    with open(TRAVA, "w") as f:
        f.write(str(os.getpid()))
    return True


def main():
    os.makedirs(FILA, exist_ok=True)
    if "--listar" in sys.argv:
        e = carrega()
        for eid, g, desc, _, prova in ETAPAS:
            st = "feita" if os.path.exists(prova) else e.get(eid, {}).get("estado", "pendente")
            print(f"{eid:<4} {desc:<62} {st}")
        return 0
    if not trava():
        print("outra instancia da rodada4 ja esta rodando", flush=True)
        return 0
    log("rodada4: inicio (ou retomada)")
    e = carrega()
    e.pop("fim", None)
    e.pop("grupos_com_falha", None)
    grava(e)
    grupo_falhou = set()
    for eid, g, desc, fn, prova in ETAPAS:
        if os.path.exists(prova):
            if carrega().get(eid, {}).get("estado") != "ok":
                marca(eid, estado="ok", desc=desc)
            continue
        if g in grupo_falhou:
            marca(eid, estado="pulada", desc=desc)
            continue
        nome_log = f"{eid}_{desc.split()[0].strip(':,')}.log"
        log(f"[{eid}] {desc}")
        marca(eid, estado="rodando", desc=desc, inicio=datetime.now().isoformat(timespec="seconds"))
        t0 = time.time()
        rc = 1
        for tentativa in (1, 2):
            try:
                rc = fn(nome_log)
            except Exception as exc:          # erro do proprio orquestrador: registra e segue
                log(f"  excecao: {exc!r}")
                rc = 1
            if rc == 0 and os.path.exists(prova):
                break
            if rc == 0:
                rc = 1
                log("  terminou sem gerar a prova")
            log(f"  tentativa {tentativa} falhou (rc={rc})")
        dt = round(time.time() - t0)
        if rc == 0:
            marca(eid, estado="ok", segundos=dt, fim=datetime.now().isoformat(timespec="seconds"))
            log(f"[{eid}] ok em {dt / 60:.1f} min")
        else:
            marca(eid, estado=f"falhou_rc{rc}", segundos=dt)
            grupo_falhou.add(g)
            log(f"[{eid}] FALHOU; o resto do grupo {g} fica para a proxima retomada")
    e = carrega()
    e["fim"] = datetime.now().isoformat(timespec="seconds")
    e["grupos_com_falha"] = sorted(grupo_falhou)
    grava(e)
    log("rodada4: encerrada" + (f" com falha nos grupos {sorted(grupo_falhou)}" if grupo_falhou else ""))
    try:
        os.remove(TRAVA)
    except OSError:
        pass
    return 1 if grupo_falhou else 0


if __name__ == "__main__":
    sys.exit(main())
