#!/usr/bin/env python3
"""
rodada6_criterios.py: aplica os criterios que 07-blender/PLANO-RODADA6.md fixou antes da rodada 6
(molde do rodada5_criterios.py). Le so arquivos de 06-resultados (inclusive revisao-2026-10-17/) e
grava rodada6_criterios.json (vereditos) e rodada6_eficacias.json/.md (eficacias com o R de selecao fora
do teste). Item cujo arquivo ainda nao existe sai como "pendente". Nenhuma regra e escolhida aqui.

Leituras de resolubilidade (secao 2.3 do PLANO-RODADA5, sem mudanca): (a) faixas de sementes que nao se
cruzam, (b) intervalo de 95% por reamostragem que exclui zero, (c) diferenca relativa de pelo menos 30%
do menor valor (descritiva); resolvivel = passa em (a) ou em (b).

  python rodada6_criterios.py --parte R|Q|L|E|G|V|H|C|tudo
"""
import argparse
import json
import os
import random
import sys
from datetime import datetime

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
REV = os.path.join(AQUI, "revisao-2026-10-17")
sys.path.insert(0, REV)
sys.path.insert(0, AQUI)
from bootstrap_visdrone import N_BOOT, SEMENTE, ap50, carrega, grupos_r5, ic  # noqa: E402
from rodada5_criterios import ic as ic_l, limpa, perfil  # noqa: E402

LIMIAR_REL = 30.0
SAIDA = os.path.join(AQUI, "rodada6_criterios.json")


def le(nome, pasta=AQUI):
    try:
        return json.load(open(os.path.join(pasta, nome), encoding="utf-8"))
    except (OSError, ValueError):
        return None


def existe(run, tag="visdrone"):
    return os.path.exists(os.path.join(REV, f"preds_{tag}_{run}.npz"))


def carrega_tag(tag, run):
    """o carrega() de bootstrap_visdrone, para os .npz de preds_nadir.py (mesmo formato)"""
    p = os.path.join(REV, f"preds_{tag}_{run}.npz")
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=False)
    conf, tp50, img_idx, n_gt = d["conf"], d["tp"][:, 0], d["img_idx"], d["n_gt"]
    o = np.argsort(-conf, kind="stable")
    return {"run": run, "conf": conf[o], "tp": tp50[o].astype(np.float64), "img": img_idx[o],
            "n_gt": n_gt.astype(np.float64), "n_img": len(n_gt)}


def boot_mapa(runs, tag="visdrone"):
    """mAP50 no conjunto inteiro e nas N_BOOT reamostras pareadas (semente 0) de cada run com preds"""
    m = {r: (carrega(r) if tag == "visdrone" else carrega_tag(tag, r)) for r in runs}
    m = {r: v for r, v in m.items() if v}
    if not m:
        return {}, {}
    n_img = next(iter(m.values()))["n_img"]
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, n_img, size=(N_BOOT, n_img))
    W = np.stack([np.bincount(i, minlength=n_img) for i in idx]).astype(np.float64)
    cheio = {r: ap50(m[r], np.ones(n_img)) for r in m}
    boot = {r: np.array([ap50(m[r], W[b]) for b in range(N_BOOT)]) for r in m}
    return cheio, boot


def rel(a, b):
    m = min(abs(a), abs(b))
    return round(100 * (a - b) / m, 1) if m > 0 else None


def faixas_nao_cruzam(va, vb):
    if len(va) < 2 or len(vb) < 2:
        return None
    return bool(min(va) > max(vb) or min(vb) > max(va))


def leitura(va, vb, boot_a, boot_b, pareado):
    """as tres leituras para 'a menos b': va, vb valores por semente; boot_a, boot_b reamostras (media das sementes)"""
    a0, b0 = float(np.mean(va)), float(np.mean(vb))
    if pareado:
        d = boot_a - boot_b
    else:
        d = boot_a - boot_b                    # reamostragens independentes (sementes distintas por lado)
    icd = ic(d)
    out = {"a_valores": [round(float(x), 4) for x in va], "b_valores": [round(float(x), 4) for x in vb],
           "a_media": round(a0, 4), "b_media": round(b0, 4), "dif": round(a0 - b0, 4), "dif_ic95": icd,
           "dif_relativa_pct_do_menor": rel(a0, b0), "razao_a_sobre_b": round(a0 / b0, 3) if b0 else None,
           "a_ok": faixas_nao_cruzam(va, vb), "b_ok": bool(icd[0] > 0 or icd[1] < 0),
           "c_ok": (rel(a0, b0) is not None and abs(rel(a0, b0)) >= LIMIAR_REL), "pareado": pareado}
    out["resolvivel"] = bool(out["a_ok"]) or out["b_ok"]
    out["passou_em"] = [k for k, v in (("a", out["a_ok"]), ("b", out["b_ok"]), ("c", out["c_ok"])) if v]
    return out


# ------------------------------------------------------------------ R (item 4): R com selecao fora do teste
def grupos_r6():
    g = grupos_r5()
    g.update({"R": ["r_pareado"], "R-sel": ["r_pareado_sel"], "R-full": ["r_cheio_sel"],
              "S-nadir-150 deg": ["s_nadir_4k_deg", "s_nadir_4k_deg_sd1", "s_nadir_4k_deg_sd2"],
              "S-oblique-six deg": ["s_oblvar_deg", "s_oblvar_deg_sd1", "s_oblvar_deg_sd2"]})
    return {k: [r for r in v if existe(r)] for k, v in g.items()}


def item_r():
    if not existe("r_pareado_sel"):
        return {"veredito": "pendente"}
    g = grupos_r6()
    runs = sorted({r for v in g.values() for r in v})
    cheio, boot = boot_mapa(runs)
    r0, r1 = cheio["r_pareado"], cheio["r_pareado_sel"]
    vies = boot["r_pareado"] - boot["r_pareado_sel"]
    out = {"R_mAP50": round(r0, 4), "R_sel_mAP50": round(r1, 4), "R_sel_mAP50_ic95": ic(boot["r_pareado_sel"]),
           "vies_de_selecao": {"dif": round(r0 - r1, 4), "ic95_pareado": ic(vies), "relativa_pct": rel(r0, r1)},
           "selecao": "r_pareado_sel: checkpoint escolhido em ft/sel_r.txt (265 imagens do VisDrone train fora da amostra "
                      "de treino e fora do val); r_pareado: escolhido no proprio VisDrone val",
           "regra": "PLANO-RODADA6 3.1: R-sel passa a ser o teto R do artigo (selecao fora do teste) e todas as eficacias "
                    "sao recalculadas com ele; a diferenca R menos R-sel e reportada como vies de selecao, com IC pareado"}
    ef = {}
    for k, v in g.items():
        if not v:
            continue
        mb = np.mean([boot[r] for r in v], 0)
        med = float(np.mean([cheio[r] for r in v]))
        ef[k] = {"runs": v, "valores": [round(cheio[r], 4) for r in v], "media": round(med, 4), "media_ic95": ic(mb),
                 "eficacia_R": round(med / r0, 4), "eficacia_R_sel": round(med / r1, 4),
                 "eficacia_R_sel_ic95": ic(mb / boot["r_pareado_sel"])}
        if "r_cheio_sel" in cheio:
            ef[k]["eficacia_R_full"] = round(med / cheio["r_cheio_sel"], 4)
    out["eficacias"] = ef
    with open(os.path.join(AQUI, "rodada6_eficacias.json"), "w", encoding="utf-8") as f:
        json.dump({"protocolo": "VisDrone-DET val, 548 imagens, classe unica, imgsz 1280; preds de visdrone_preds.py; "
                                f"{N_BOOT} reamostras pareadas, semente {SEMENTE}; eficacia = media das sementes / R",
                   "R": r0, "R_sel": r1, "vies": out["vies_de_selecao"], "grupos": ef,
                   "quando": datetime.now().isoformat(timespec="seconds")}, f, indent=1, ensure_ascii=False)
    L = ["# Eficacias com o R de selecao fora do teste (rodada 6, item 4)", "",
         f"R (selecao no val) {r0:.4f}; R-sel (selecao em sel_r) {r1:.4f}; vies R menos R-sel {r0 - r1:+.4f} "
         f"(IC 95% pareado {ic(vies)[0]:+.4f} a {ic(vies)[1]:+.4f}).", "",
         "| Grupo | runs | media mAP50 | IC 95% | eficacia / R | eficacia / R-sel (IC 95%) |", "|---|---|---|---|---|---|"]
    for k, v in ef.items():
        L.append(f"| {k} | {', '.join(v['runs'])} | {v['media']:.4f} | {v['media_ic95'][0]:.4f} a {v['media_ic95'][1]:.4f} | "
                 f"{100 * v['eficacia_R']:.1f}% | {100 * v['eficacia_R_sel']:.1f}% ({100 * v['eficacia_R_sel_ic95'][0]:.1f} a "
                 f"{100 * v['eficacia_R_sel_ic95'][1]:.1f}) |")
    with open(os.path.join(AQUI, "rodada6_eficacias.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    icv = out["vies_de_selecao"]["ic95_pareado"]
    out["veredito"] = (f"R-sel {r1:.4f} contra R {r0:.4f}: vies de selecao {r0 - r1:+.4f}"
                       + (" (IC exclui zero: vies real, pequeno)" if icv[0] > 0 or icv[1] < 0 else " (IC inclui zero: sem vies detectavel)")
                       + "; eficacias recalculadas em rodada6_eficacias.md")
    return out


# ------------------------------------------------------------------ Q (item 5): orcamento de treino e a forma em U
def perfis(prefixo, sementes=("", "_sd1", "_sd2")):
    ps = [perfil(f"{prefixo}{s}.json") for s in sementes]
    return [p for p in ps if p]


def compara_perfis(pa, pb, pareado):
    """a menos b em d' e em objeto chamado de armada, com as tres leituras (media das sementes de cada lado)"""
    out = {}
    for chave, k_val, k_boot in (("dlinha", "dlinha_armada_contra_objeto", "_boot_d"),
                                 ("objeto_chamado_armada", "objeto_chamado_armada", "_boot_o")):
        va = [p[k_val] for p in pa]
        vb = [p[k_val] for p in pb]
        n = min(len(p[k_boot]) for p in pa + pb)
        ba = np.mean([np.array(p[k_boot][:n]) for p in pa], 0)
        bb = np.mean([np.array(p[k_boot][:n]) for p in pb], 0)
        out[chave] = leitura(va, vb, ba, bb, pareado)
    return out


def item_q():
    e35, e75 = perfis("extra_armado_35_e120"), perfis("extra_armado_75g_e120")
    if not e35 or not e75:
        return {"veredito": "pendente"}
    b35, b75 = perfis("extra_armado_35"), perfis("extra_armado_75g")
    e150 = perfis("extra_armado_150g_e120", ("",))
    out = {"quadros_novos": {"35 m e120": [limpa(p) for p in e35], "75 m gemeo e120": [limpa(p) for p in e75],
                             "150 m gemeo e120": [limpa(p) for p in e150],
                             "35 m e60": [limpa(p) for p in b35], "75 m gemeo e60": [limpa(p) for p in b75]},
           "e120_contra_e60": {"35 m": compara_perfis(e35, b35, True), "75 m": compara_perfis(e75, b75, True)},
           "curva_e120": {"75 contra 35": compara_perfis(e75, e35, False),
                          "75 contra 150": compara_perfis(e75, e150, False) if e150 else None},
           "regra": "PLANO-RODADA6 3.2: nos 80 quadros novos; e120 contra e60 pareado (mesmos quadros); curva 75 contra 35 e "
                    "75 contra 150 independente. U confirmada com orcamento igual = a 120 epocas o gemeo de 75 m ainda tem "
                    "objeto chamado de armada abaixo de 35 e de 150 m pela leitura (b) nas duas; U era orcamento = pelo menos "
                    "uma das duas deixa de passar em (b) (intervalo inclui zero) ou inverte"}
    c = out["curva_e120"]
    o35 = c["75 contra 35"]["objeto_chamado_armada"]
    o150 = c["75 contra 150"]["objeto_chamado_armada"] if c["75 contra 150"] else None
    abaixo35 = o35["b_ok"] and o35["dif"] < 0
    abaixo150 = (o150["b_ok"] and o150["dif"] < 0) if o150 else None
    if abaixo150 is None:
        out["veredito"] = "pendente (sem o perfil de 150 m a 120 epocas)"
    elif abaixo35 and abaixo150:
        out["veredito"] = "U confirmada com orcamento igual: a 120 epocas o gemeo de 75 m continua com menos objeto chamado de armada que 35 e 150 m (b)"
    else:
        lados = [n for n, ok in (("35 m", abaixo35), ("150 m", abaixo150)) if not ok]
        out["veredito"] = f"U era (em parte) orcamento: com 120 epocas a vantagem de 75 m sobre {', '.join(lados)} nao passa em (b)"
    for alt in ("35 m", "75 m"):
        d = out["e120_contra_e60"][alt]["objeto_chamado_armada"]
        out["e120_contra_e60"][alt]["leitura"] = (f"objeto chamado de armada {d['dif']:+.4f} (IC {d['dif_ic95']}), "
                                                  + ("resolvivel" if d["resolvivel"] else "nao resolvivel"))
    return out


# ------------------------------------------------------------------ L (item 6): comprimento como atalho
def item_l():
    out = {"regra": "PLANO-RODADA6 3.3: modelo treinado com objetos no comprimento das armas, medido nos seus 80 quadros novos "
                    "(objetos no comprimento das armas). Se o IC de d' inclui 0: a separacao nessa altitude dependia do "
                    "comprimento; se exclui: a forma sobrevive sem o comprimento, e a queda contra o modelo original e dada "
                    "por (b) independente e (c). Cruzado: o modelo original nos quadros de comprimento igual mede quanto do seu "
                    "falso alarme vem do comprimento"}
    pend = True
    for alt, novo, orig, arq_cruz_orig, arq_cruz_novo in (
            ("75 m", "armado_75c", "armado_75g", "extra75c_armado_75g.json", "extra75g_armado_75c.json"),
            ("150 m", "armado_150c_e120", "armado_150g_e120", "extra150c_armado_150g_e120.json", "extra150g_armado_150c_e120.json")):
        pn = perfil(f"extra_{novo}.json")
        if not pn:
            continue
        pend = False
        po = perfil(f"extra_{orig}.json")
        pco, pcn = perfil(arq_cruz_orig), perfil(arq_cruz_novo)
        r = {"novo_nos_proprios_quadros_novos": limpa(pn), "original_nos_seus_quadros_novos": limpa(po) if po else None,
             "original_nos_quadros_de_comprimento_igual": limpa(pco) if pco else None,
             "novo_nos_quadros_originais": limpa(pcn) if pcn else None}
        icd = pn["dlinha_ic95"]
        if po:
            r["novo_contra_original"] = compara_perfis([pn], [po], False)
        if pco and po:
            r["original_comprimento_igual_contra_original"] = compara_perfis([pco], [po], False)
        if icd and icd[0] <= 0 <= icd[1]:
            r["veredito"] = f"{alt}: sem o comprimento o IC de d' inclui 0: a separacao dependia do comprimento (atalho confirmado)"
        else:
            q = r.get("novo_contra_original", {}).get("dlinha", {})
            r["veredito"] = (f"{alt}: a forma sobrevive sem o comprimento (d' {pn['dlinha_armada_contra_objeto']}, IC {icd}); "
                             f"queda contra o original {q.get('dif')} (IC {q.get('dif_ic95')}, {'resolvivel' if q.get('resolvivel') else 'nao resolvivel'})")
        out[alt] = r
    if pend:
        return {"veredito": "pendente"}
    out["veredito"] = " | ".join(out[a]["veredito"] for a in ("75 m", "150 m") if a in out)
    return out


# ------------------------------------------------------------------ E (item 7): sol duro sem "nulo por regra"
def regime_quadros(nome_arq, regime):
    d = le(nome_arq)
    if not d or "por_quadro" not in d.get("por_regime", {}).get(regime, {}):
        return None, None
    q = [(x["acertos"], x["caixas"]) for x in d["por_regime"][regime]["por_quadro"]]
    return q, d["por_regime"][regime]["mAP50"]


def boot_rec(qs, rnd, n=2000):
    bs = []
    for _ in range(n):
        s = [qs[rnd.randrange(len(qs))] for _ in qs]
        bs.append(sum(x for x, _ in s) / max(1, sum(y for _, y in s)))
    return np.array(bs)


def lado(runs, regime):
    """por semente: recall por quadro, mAP50; reamostras (semente 0) na media das sementes"""
    rec, m50, boots = [], [], []
    for r in runs:
        q, m = regime_quadros(f"por_regime_{r}.json", regime)
        if q is None:
            continue
        rec.append(sum(x for x, _ in q) / max(1, sum(y for _, y in q)))
        m50.append(m)
        boots.append(boot_rec(q, random.Random(0)))
    if not rec:
        return None
    return {"runs": runs, "recall": rec, "mAP50": m50, "boot": np.mean(boots, 0)}


def item_e():
    esp = lado(["s_soldur_4k", "s_soldur_4k_sd1", "s_soldur_4k_sd2"], "sol_duro")
    esp_runs = [r for r in ["s_soldur_4k", "s_soldur_4k_sd1", "s_soldur_4k_sd2"] if le(f"por_regime_{r}.json")]
    esp = lado(esp_runs, "sol_duro") if esp_runs else None
    esp_runs_m = [r for r in ["s_semsol_4k", "s_semsol_4k_sd1", "s_semsol_4k_sd2"] if le(f"por_regime_{r}.json")]
    esp_m = lado(esp_runs_m, "nublado") if esp_runs_m else None
    gen_runs = [r for r in ["s_nadir_4k_r5", "s_nadir_4k_sd1", "s_nadir_4k_sd2"] if le(f"por_regime_{r}.json")]
    gen = lado(gen_runs, "nublado") if gen_runs else None
    if esp is None or esp_m is None or len(esp["recall"]) < 2:
        return {"veredito": "pendente"}
    out = {"especialista_sol_duro": {"runs": esp["runs"], "recall": esp["recall"], "mAP50": esp["mAP50"]},
           "espelho_nublado": {"runs": esp_m["runs"], "recall": esp_m["recall"], "mAP50": esp_m["mAP50"]},
           "generalista_nublado": {"runs": gen["runs"], "recall": gen["recall"], "mAP50": gen["mAP50"]} if gen else None,
           "regra": "PLANO-RODADA6 3.4: E-iii decide: especialista de sol duro sob sol duro menos espelho (tudo menos sol duro) "
                    "sob nublado, recall a conf 0,25 em imagem inteira, 2.000 reamostras de quadros (semente 0) na media das "
                    "sementes, independente; (a) com as sementes dos dois lados; (c) no mAP50. Intervalo inteiro abaixo de zero e "
                    "(a) -> regime intrinsecamente mais dificil, resolvivel; intervalo que inclui zero -> nao resolvivel; "
                    "D-ii repetida com sementes"}
    out["E_iii"] = leitura(esp["recall"], esp_m["recall"], esp["boot"], esp_m["boot"], False)
    out["E_iii"]["mAP50_rel_pct"] = rel(float(np.mean(esp["mAP50"])), float(np.mean(esp_m["mAP50"])))
    if gen:
        out["D_ii_com_sementes"] = leitura(esp["recall"], gen["recall"], esp["boot"], gen["boot"], False)
    e = out["E_iii"]
    if e["dif_ic95"][1] < 0:
        out["veredito"] = ("regime intrinsecamente mais dificil: com participacao maxima nos dois lados o sol duro fica abaixo "
                           f"do nublado ({e['dif']:+.4f}, IC {e['dif_ic95']}, passou em {e['passou_em']})")
    elif e["dif_ic95"][0] > 0:
        out["veredito"] = f"sol duro acima do nublado com participacao maxima ({e['dif']:+.4f}, IC {e['dif_ic95']}): caso nao previsto, reportar"
    else:
        out["veredito"] = (f"nao resolvivel: com participacao maxima nos dois lados a diferenca ({e['dif']:+.4f}) tem IC que inclui "
                           f"zero ({e['dif_ic95']}); (a) {e['a_ok']}")
    return out


# ------------------------------------------------------------------ G (item 3): ruido, borrao e JPEG
def item_g():
    pares = {"S-nadir-150": (["s_nadir_4k", "s_nadir_4k_sd1", "s_nadir_4k_sd2"], ["s_nadir_4k_deg", "s_nadir_4k_deg_sd1", "s_nadir_4k_deg_sd2"]),
             "S-oblique-six": (["s_oblvar", "s_oblvar_sd1", "s_oblvar_sd2"], ["s_oblvar_deg", "s_oblvar_deg_sd1", "s_oblvar_deg_sd2"])}
    if not existe("s_nadir_4k_deg") and not existe("s_oblvar_deg"):
        return {"veredito": "pendente"}
    out = {"regra": "PLANO-RODADA6 3.5: degradado menos limpo, media das sementes, no VisDrone val (pareado, 1.000 reamostras) e na "
                    "HERIDAL a imgsz casado (idem); (a) com sementes dos dois lados; (c). Resolvivel para cima = a falta de "
                    "artefatos de sensor explica parte da lacuna; nao resolvivel = nao explica; para baixo = degradar prejudica"}
    vered = []
    for tag in ("visdrone", "heridal"):
        runs = [r for v in pares.values() for lado_ in v for r in lado_ if existe(r, tag)]
        if not runs:
            continue
        cheio, boot = boot_mapa(runs, tag)
        for nome, (limpo, deg) in pares.items():
            la = [r for r in deg if r in cheio]
            lb = [r for r in limpo if r in cheio]
            if not la or not lb:
                continue
            lt = leitura([cheio[r] for r in la], [cheio[r] for r in lb],
                         np.mean([boot[r] for r in la], 0), np.mean([boot[r] for r in lb], 0), True)
            lt.update({"a_runs": la, "b_runs": lb})
            out[f"{nome} {tag}"] = lt
            s = "sobe" if lt["dif"] > 0 else "cai"
            vered.append(f"{nome} no {tag}: degradado {s} {lt['dif']:+.4f} ({'resolvivel' if lt['resolvivel'] else 'nao resolvivel'}, {lt['passou_em']})")
    out["veredito"] = " | ".join(vered) if vered else "pendente"
    return out


# ------------------------------------------------------------------ H (item 8): arma na mao
def item_h():
    out = {"regra": "PLANO-RODADA6 3.7: para cada altitude, modelo treinado com a arma na mao, nos seus 80 quadros novos (arma na "
                    "mao), contra o e120 original nos seus 80 (mesmos indices, reamostragem independente): d' e objeto chamado de "
                    "armada, (b) e (c). Resolvivel = a cinematica das maos muda a medida nessa altitude; nao resolvivel = "
                    "sub-pixel, como esperado a 75 e 150 m. Cruzado, descritivo: cada modelo nos quadros do outro"}
    pend = True
    for alt, tag in (("35 m", "35"), ("75 m", "75g"), ("150 m", "150g")):
        pn = perfil(f"extra_armado_{tag}m_e120.json")
        if not pn:
            continue
        pend = False
        po = perfil(f"extra_armado_{tag}_e120.json")
        r = {"mao_nos_proprios_quadros_novos": limpa(pn), "original_nos_seus_quadros_novos": limpa(po) if po else None,
             "original_nos_quadros_com_mao": limpa(perfil(f"extra{tag}m_armado_{tag}_e120.json")),
             "mao_nos_quadros_originais": limpa(perfil(f"extra{tag}_armado_{tag}m_e120.json"))}
        if po:
            r["mao_contra_original"] = compara_perfis([pn], [po], False)
            d, o = r["mao_contra_original"]["dlinha"], r["mao_contra_original"]["objeto_chamado_armada"]
            r["veredito"] = (f"{alt}: d' {d['dif']:+.3f} (IC {d['dif_ic95']}), objeto chamado de armada {o['dif']:+.4f} "
                             f"(IC {o['dif_ic95']}): " + ("resolvivel" if d["resolvivel"] or o["resolvivel"] else "nao resolvivel"))
        else:
            r["veredito"] = f"{alt}: sem o e120 original para comparar"
        out[alt] = r
    if pend:
        return {"veredito": "pendente"}
    out["veredito"] = " | ".join(out[a]["veredito"] for a in ("35 m", "75 m", "150 m") if a in out)
    return out


# ------------------------------------------------------------------ C: transferencia de cor
CORPORA_C = {"S-nadir-150": "s_nadir_4k", "S-oblique-six": "s_oblvar"}


def sim2real_val(arq):
    d = le(arq)
    if not d:
        return None
    return next((r.get("metrics/mAP50(B)") for r in d["resultados"] if r.get("conjunto") == "real"), None)


def item_c():
    if not existe("s_nadir_4k_ct") and not existe("s_oblvar_ct"):
        return {"veredito": "pendente"}
    out = {"regra": "PLANO-RODADA6 3.10: transferido menos limpo, pareado por imagem, 1.000 reamostras, semente 0, no VisDrone val "
                    "(1280) e na HERIDAL (imgsz casado); leituras (b) e (c), (a) quando houver sementes dos dois lados. "
                    "Resolvivel para cima no VisDrone e nao na HERIDAL = a aparencia explica parte da lacuna, especifica do alvo; "
                    "para cima nos dois = aparencia generica; nulo = a lacuna e geometria. Sementes 1 e 2 so onde (b) passou",
           "sementes_indicadas": [], "corpora": {}}
    for nome, base in CORPORA_C.items():
        ct = [r for r in (f"{base}_ct", f"{base}_ct_sd1", f"{base}_ct_sd2") if existe(r)]
        if not ct:
            continue
        limpo = [base] + ([f"{base}_sd1", f"{base}_sd2"] if len(ct) > 1 else [])
        c = {"runs_transferido": ct, "runs_limpo": limpo}
        sobe = {}
        for tag in ("visdrone", "heridal"):
            la = [r for r in ct if existe(r, tag)]
            lb = [r for r in limpo if existe(r, tag)]
            if not la or not lb:
                continue
            cheio, boot = boot_mapa(la + lb, tag)
            lt = leitura([cheio[r] for r in la], [cheio[r] for r in lb],
                         np.mean([boot[r] for r in la], 0), np.mean([boot[r] for r in lb], 0), True)
            if len(la) < 2:
                lt["a_ok"] = None
            c[tag] = lt
            sobe[tag] = "cima" if (lt["b_ok"] and lt["dif"] > 0) else ("baixo" if (lt["b_ok"] and lt["dif"] < 0) else "nulo")
            if lt["b_ok"] and base not in out["sementes_indicadas"]:
                out["sementes_indicadas"].append(base)
        c["visdrone_1024"] = {"transferido": sim2real_val(f"sim2real_{base}_ct_1024.json"),
                              "limpo": sim2real_val(f"sim2real_{base}_1024.json")}
        comb = f"{base}_ctdeg"
        if existe(comb):
            cmb = {}
            for tag in ("visdrone", "heridal"):
                if existe(comb, tag) and existe(base, tag) and existe(f"{base}_ct", tag):
                    cheio, boot = boot_mapa([comb, base, f"{base}_ct"], tag)
                    cmb[tag] = {"contra_limpo": leitura([cheio[comb]], [cheio[base]], boot[comb], boot[base], True),
                                "contra_transferido": leitura([cheio[comb]], [cheio[f"{base}_ct"]], boot[comb], boot[f"{base}_ct"], True)}
            c["combinado_descritivo"] = cmb
        v, h = sobe.get("visdrone"), sobe.get("heridal")
        if v is None or h is None:
            c["veredito"] = f"{nome}: pendente (falta um benchmark)"
        elif v == "cima" and h != "cima":
            c["veredito"] = f"{nome}: a aparencia explica parte da lacuna, especifica do alvo (VisDrone sobe, HERIDAL {h})"
        elif v == "cima" and h == "cima":
            c["veredito"] = f"{nome}: aparencia generica (sobe nos dois benchmarks)"
        elif v == "nulo" and h == "nulo":
            c["veredito"] = f"{nome}: nulo nos dois: a lacuna e geometria, nao aparencia"
        else:
            c["veredito"] = f"{nome}: caso nao previsto pela regra (VisDrone {v}, HERIDAL {h}): reportar os dois"
        for tag in ("visdrone", "heridal"):
            if tag in c:
                c["veredito"] += f"; {tag} {c[tag]['dif']:+.4f} (IC {c[tag]['dif_ic95']}, passou em {c[tag]['passou_em']})"
        out["corpora"][nome] = c
    out["veredito"] = " | ".join(v["veredito"] for v in out["corpora"].values()) or "pendente"
    return out


# ------------------------------------------------------------------ V (item 9): teto com o treino completo
def item_v():
    if not existe("r_cheio_sel"):
        return {"veredito": "pendente"}
    cheio, boot = boot_mapa(["r_cheio_sel", "r_pareado_sel", "r_pareado"])
    d = boot["r_cheio_sel"] - boot["r_pareado_sel"]
    out = {"R_full_mAP50": round(cheio["r_cheio_sel"], 4), "R_full_ic95": ic(boot["r_cheio_sel"]),
           "R_sel_mAP50": round(cheio["r_pareado_sel"], 4), "dif": round(cheio["r_cheio_sel"] - cheio["r_pareado_sel"], 4),
           "dif_ic95_pareado": ic(d), "razao": round(cheio["r_cheio_sel"] / cheio["r_pareado_sel"], 3),
           "regra": "PLANO-RODADA6 3.6: descritivo; o texto declara R como teto do protocolo pareado (1.106 imagens) e cita o teto "
                    "com o treino completo (menos a fatia de selecao) como referencia, com as eficacias / R-full em rodada6_eficacias"}
    out["veredito"] = f"teto com o treino completo {cheio['r_cheio_sel']:.4f} contra R-sel {cheio['r_pareado_sel']:.4f} (razao {out['razao']})"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parte", default="tudo")
    a = ap.parse_args()
    partes = {"R": item_r, "Q": item_q, "L": item_l, "E": item_e, "G": item_g, "V": item_v, "H": item_h, "C": item_c}
    out = le("rodada6_criterios.json") or {}
    for k, fn in partes.items():
        if a.parte in ("tudo", k):
            out[k] = fn()
            print(f"{k}: {out[k].get('veredito')}", flush=True)
    out["quando"] = datetime.now().isoformat(timespec="seconds")
    with open(SAIDA, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=float)
    return 0


if __name__ == "__main__":
    sys.exit(main())
