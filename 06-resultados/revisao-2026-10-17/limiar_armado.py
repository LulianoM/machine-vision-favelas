#!/usr/bin/env python3
"""
limiar_armado.py: varredura do limiar de confianca dos modelos de tres classes (armada, desarmada,
objeto), a partir das predicoes guardadas por armado_preds.py (imagem 4K inteira, imgsz 3840,
conf >= 0,05). Ponto S6 do feedback de 14/10 (limiares justificados) e A3 (diferencas pequenas).
Revisao de 17/10/2026, agente D2.

Protocolo de confusao_armado.py em cada limiar t de 0,05 a 0,95 (passo 0,05): ficam as predicoes com
conf >= t; casamento um para um por IoU >= 0,50 sem olhar a classe (pares ordenados por IoU, atribuicao
gulosa); cada pessoa anotada recebe a classe da predicao com que casou, ou "perdida". Medidas:
  recall de armada          = pessoas armadas chamadas de armada / pessoas armadas
  objeto chamado de armada  = pessoas com objeto chamadas de armada / pessoas com objeto
  desarmada chamada de armada
  precisao de armada        = pessoas armadas chamadas de armada / todas as predicoes de classe armada
                              (inclui as que nao casam com ninguem), como em compara_gemeo.py
  F1 de armada              = 2 P R / (P + R)
  d' (armada contra objeto e contra desarmada) com correcao log-linear (k + 0,5) / (n + 1),
                              como em rodada4_criterios.py
Tres pontos por modelo e conjunto: conf 0,25 (o padrao do artigo), o limiar que maximiza o F1 de
armada, e o menor limiar com objeto chamado de armada <= 0,10.

Reproducao: a conf 0,25 as taxas tem de bater com confusao_armado_*.json, extra_armado_*.json e
holdout_armas_armado_75.json (campo `reproducao`).

Bootstrap de quadros (1.000 reamostras, semente 0) das taxas a 0,25 e das diferencas 35 m menos gemeo
a 75 m, no val de cada corpus e nos 80 quadros novos (conjuntos nao pareados: reamostragem independente
de cada lado), para resolvivel.py.

  C:/arma3-favela/venv/Scripts/python.exe limiar_armado.py
Saidas: limiar_armado.json, limiar_armado.md, ../figuras/fig12_limiar_armado.png
"""
import json
import os
import sys
from collections import defaultdict
from datetime import datetime
from statistics import NormalDist

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(AQUI)
FIG = os.path.join(RES, "figuras")
sys.path.insert(0, AQUI)
from armado_preds import CONJUNTOS  # noqa: E402

LIMIARES = [round(0.05 * k, 2) for k in range(1, 20)]
N = NormalDist()
N_BOOT = 1000
SEMENTE = 0


def iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    i = ix * iy
    return i / ((a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - i + 1e-9)


def casa(gts, preds, lim_iou=0.5):
    """coluna de cada caixa verdadeira (0 armada, 1 desarmada, 2 objeto, 3 perdida) e indices das predicoes usadas"""
    pares = sorted(((iou(g[1:], p[:4]), gi, pi) for gi, g in enumerate(gts) for pi, p in enumerate(preds)), reverse=True)
    g_usado, p_usado, atrib = set(), set(), {}
    for v, gi, pi in pares:
        if v < lim_iou:
            break
        if gi in g_usado or pi in p_usado:
            continue
        g_usado.add(gi)
        p_usado.add(pi)
        atrib[gi] = preds[pi][5]
    return [atrib.get(gi, 3) for gi in range(len(gts))], p_usado


def contagens_por_quadro(registros, t):
    """por quadro: k[c] = caixas da classe c chamadas de armada, n[c] = caixas da classe c, n_pred_armada"""
    out = []
    for q in registros:
        preds = [p for p in q["preds"] if p[4] >= t]
        cols, _ = casa(q["gt"], preds)
        k, n = [0, 0, 0], [0, 0, 0]
        for g, col in zip(q["gt"], cols):
            n[g[0]] += 1
            k[g[0]] += col == 0
        out.append({"k": k, "n": n, "pred_armada": sum(1 for p in preds if p[5] == 0),
                    "perdidas": sum(1 for c in cols if c == 3)})
    return out


def dlinha(hk, hn, fk, fn):
    h = (hk + 0.5) / (hn + 1)
    f = (fk + 0.5) / (fn + 1)
    return N.inv_cdf(h) - N.inv_cdf(f)


def medidas(cq):
    k = [sum(q["k"][c] for q in cq) for c in range(3)]
    n = [sum(q["n"][c] for q in cq) for c in range(3)]
    npa = sum(q["pred_armada"] for q in cq)
    rec = k[0] / n[0] if n[0] else float("nan")
    prec = k[0] / npa if npa else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return {"recall_armada": round(rec, 4), "objeto_chamado_armada": round(k[2] / n[2], 4) if n[2] else None,
            "desarmada_chamada_armada": round(k[1] / n[1], 4) if n[1] else None,
            "precisao_armada": round(prec, 4), "f1_armada": round(f1, 4),
            "dlinha_armada_vs_objeto": round(dlinha(k[0], n[0], k[2], n[2]), 3),
            "dlinha_armada_vs_desarmada": round(dlinha(k[0], n[0], k[1], n[1]), 3),
            "k": k, "n": n, "predicoes_armada": npa,
            "recall_deteccao_qualquer_classe": round(1 - sum(q["perdidas"] for q in cq) / max(1, sum(n)), 4)}


def referencia(arq):
    p = os.path.join(RES, arq)
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    t = d["taxa_por_classe_real"]
    return {"armada": t["armada"]["armada"], "desarmada": t["desarmada"]["armada"], "objeto": t["objeto"]["armada"],
            "n": [t["armada"]["n"], t["desarmada"]["n"], t["objeto"]["n"]], "imagens": d.get("imagens")}


def boot_taxas(cq, rng):
    """reamostragem de quadros: taxas a conf 0,25 (objeto, desarmada, armada) e d' por reamostra"""
    K = np.array([q["k"] for q in cq], float)
    Nn = np.array([q["n"] for q in cq], float)
    m = len(cq)
    idx = rng.integers(0, m, size=(N_BOOT, m))
    out = {"objeto": [], "desarmada": [], "armada": [], "dlinha_obj": []}
    for i in idx:
        k, n = K[i].sum(0), Nn[i].sum(0)
        out["armada"].append(k[0] / n[0] if n[0] else np.nan)
        out["desarmada"].append(k[1] / n[1] if n[1] else np.nan)
        out["objeto"].append(k[2] / n[2] if n[2] else np.nan)
        out["dlinha_obj"].append(dlinha(k[0], n[0], k[2], n[2]) if (n[0] and n[2]) else np.nan)
    return {kk: np.array(v) for kk, v in out.items()}


def ic(v):
    v = np.asarray(v, float)
    v = v[~np.isnan(v)]
    return [round(float(np.percentile(v, 2.5)), 4), round(float(np.percentile(v, 97.5)), 4)]


def main():
    resultados = {}
    reproducao = []
    boots = {}
    faltando = []
    for nome, run, conjunto, ds, split, ref in CONJUNTOS:
        p = os.path.join(AQUI, f"preds_armado_{run}_{conjunto}.json")
        if not os.path.exists(p):
            faltando.append(f"{run} {conjunto} (sem preds)")
            continue
        d = json.load(open(p, encoding="utf-8"))
        if d.get("faltando"):
            faltando.append(f"{run} {conjunto} ({d.get('pesos') or d.get('ds')})")
            continue
        reg = d["registros"]
        curva = {}
        por_quadro_025 = None
        for t in LIMIARES:
            cq = contagens_por_quadro(reg, t)
            curva[f"{t:.2f}"] = medidas(cq)
            if abs(t - 0.25) < 1e-9:
                por_quadro_025 = cq
        m025 = curva["0.25"]
        r = referencia(ref)
        rep = {"arquivo": ref, "reportado": r, "obtido": {"armada": m025["recall_armada"], "desarmada": m025["desarmada_chamada_armada"],
                                                        "objeto": m025["objeto_chamado_armada"], "n": m025["n"]}}
        if r:
            rep["max_abs_dif"] = round(max(abs(r["armada"] - m025["recall_armada"]), abs(r["desarmada"] - m025["desarmada_chamada_armada"]),
                                          abs(r["objeto"] - m025["objeto_chamado_armada"])), 4)
            rep["n_igual"] = r["n"] == m025["n"]
            rep["ok_0002"] = rep["max_abs_dif"] <= 0.002
        reproducao.append({"modelo": nome, "run": run, "conjunto": conjunto} | rep)
        # tres pontos
        f1s = {t: v["f1_armada"] for t, v in curva.items()}
        t_f1 = max(f1s, key=f1s.get)
        t_obj10 = next((t for t in sorted(curva, key=float) if curva[t]["objeto_chamado_armada"] is not None
                        and curva[t]["objeto_chamado_armada"] <= 0.10), None)
        rng = np.random.default_rng(SEMENTE)
        b = boot_taxas(por_quadro_025, rng)
        boots[(nome, conjunto)] = b
        resultados[f"{nome} | {conjunto}"] = {
            "modelo": nome, "run": run, "conjunto": conjunto, "corpus": ds, "split": split, "quadros": len(reg),
            "caixas": d["caixas_verdadeiras"], "max_predicoes_num_quadro": d["max_predicoes_num_quadro"],
            "curva": curva,
            "pontos": {"conf_0.25": {"limiar": 0.25} | m025,
                       "max_f1_armada": {"limiar": float(t_f1)} | curva[t_f1],
                       "objeto_<=_0.10": ({"limiar": float(t_obj10)} | curva[t_obj10]) if t_obj10 else None},
            "bootstrap_quadros_conf_0.25": {"reamostras": N_BOOT, "semente": SEMENTE,
                                            "objeto_chamado_armada_ic95": ic(b["objeto"]),
                                            "desarmada_chamada_armada_ic95": ic(b["desarmada"]),
                                            "recall_armada_ic95": ic(b["armada"]),
                                            "dlinha_armada_vs_objeto_ic95": ic(b["dlinha_obj"])},
            "contagens_por_quadro_conf_0.25": [{"quadro": q["quadro"]} | c for q, c in zip(reg, por_quadro_025)],
        }
        print(f"{nome:<14} {conjunto:<6} quadros {len(reg):<3} conf0.25 rec {m025['recall_armada']:.3f} obj {m025['objeto_chamado_armada']:.3f} "
              f"des {m025['desarmada_chamada_armada']:.3f} P {m025['precisao_armada']:.3f} | maxF1 t={t_f1} | obj<=0.10 t={t_obj10} | "
              f"reproducao {'ok' if rep.get('ok_0002') else rep}", flush=True)

    # diferencas 35 m menos gemeo 75 m (objeto chamado de armada a 0,25), bootstrap independente de cada lado
    difs = []
    for conjunto in ("val", "novos"):
        for s in ("s0", "s1", "s2"):
            a, b = boots.get((f"S-nadir-35 {s}", conjunto)), boots.get((f"Twin-75 {s}", conjunto))
            if a is None or b is None:
                continue
            for medida in ("objeto", "desarmada", "armada"):
                d = a[medida] - b[medida]
                ra = resultados[f"S-nadir-35 {s} | {conjunto}"]["pontos"]["conf_0.25"]
                rb = resultados[f"Twin-75 {s} | {conjunto}"]["pontos"]["conf_0.25"]
                chave = {"objeto": "objeto_chamado_armada", "desarmada": "desarmada_chamada_armada", "armada": "recall_armada"}[medida]
                pa, pb = ra[chave], rb[chave]
                difs.append({"comparacao": f"S-nadir-35 {s} - Twin-75 {s}", "conjunto": conjunto, "medida": chave,
                             "a": pa, "b": pb, "dif": round(pa - pb, 4), "dif_ic95": ic(d), "ic_exclui_zero": bool(ic(d)[0] > 0 or ic(d)[1] < 0),
                             "fracao_positiva": round(float(np.nanmean(d > 0)), 3),
                             "dif_relativa_pct_do_menor": round(100 * (pa - pb) / min(pa, pb), 1) if min(pa, pb) > 0 else None})
        # media das tres sementes (bootstrap: media das reamostras das tres sementes, cada uma com a sua reamostragem)
        A = [boots[(f"S-nadir-35 s{k}", conjunto)] for k in range(3) if (f"S-nadir-35 s{k}", conjunto) in boots]
        B = [boots[(f"Twin-75 s{k}", conjunto)] for k in range(3) if (f"Twin-75 s{k}", conjunto) in boots]
        if len(A) == 3 and len(B) == 3:
            for medida in ("objeto", "desarmada", "armada"):
                chave = {"objeto": "objeto_chamado_armada", "desarmada": "desarmada_chamada_armada", "armada": "recall_armada"}[medida]
                pa = float(np.mean([resultados[f"S-nadir-35 s{k} | {conjunto}"]["pontos"]["conf_0.25"][chave] for k in range(3)]))
                pb = float(np.mean([resultados[f"Twin-75 s{k} | {conjunto}"]["pontos"]["conf_0.25"][chave] for k in range(3)]))
                d = np.mean([x[medida] for x in A], 0) - np.mean([x[medida] for x in B], 0)
                difs.append({"comparacao": "S-nadir-35 (media das sementes) - Twin-75 (media das sementes)", "conjunto": conjunto,
                             "medida": chave, "a": round(pa, 4), "b": round(pb, 4), "dif": round(pa - pb, 4), "dif_ic95": ic(d),
                             "ic_exclui_zero": bool(ic(d)[0] > 0 or ic(d)[1] < 0), "fracao_positiva": round(float(np.nanmean(d > 0)), 3),
                             "dif_relativa_pct_do_menor": round(100 * (pa - pb) / min(pa, pb), 1) if min(pa, pb) > 0 else None})
    # 35 m (s0) contra o 75 m original, so no val (os quadros novos nao sao comparaveis: corpora diferentes)
    a, b = boots.get(("S-nadir-35 s0", "val")), boots.get(("S-nadir-75", "val"))
    if a is not None and b is not None:
        for medida in ("objeto", "desarmada", "armada"):
            chave = {"objeto": "objeto_chamado_armada", "desarmada": "desarmada_chamada_armada", "armada": "recall_armada"}[medida]
            pa = resultados["S-nadir-35 s0 | val"]["pontos"]["conf_0.25"][chave]
            pb = resultados["S-nadir-75 | val"]["pontos"]["conf_0.25"][chave]
            d = a[medida] - b[medida]
            difs.append({"comparacao": "S-nadir-35 s0 - S-nadir-75 (original)", "conjunto": "val", "medida": chave,
                         "a": pa, "b": pb, "dif": round(pa - pb, 4), "dif_ic95": ic(d), "ic_exclui_zero": bool(ic(d)[0] > 0 or ic(d)[1] < 0),
                         "fracao_positiva": round(float(np.nanmean(d > 0)), 3),
                         "dif_relativa_pct_do_menor": round(100 * (pa - pb) / min(pa, pb), 1) if min(pa, pb) > 0 else None})

    out = {"protocolo": "imagem 4K inteira, imgsz 3840, casamento 1:1 IoU >= 0,50 sem classe, predicoes guardadas a conf >= 0,05 "
                        "(armado_preds.py, FP16) e filtradas por limiar; d' com correcao log-linear (k + 0,5) / (n + 1)",
           "limiares": LIMIARES, "faltando": faltando, "reproducao_conf_0.25": reproducao,
           "resultados": resultados, "diferencas_bootstrap_quadros": difs,
           "quando": datetime.now().isoformat(timespec="seconds")}
    with open(os.path.join(AQUI, "limiar_armado.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    escreve_md(out)
    figura(resultados)


def escreve_md(out):
    L = ["# Varredura de limiar dos modelos de tres classes (17/10/2026, agente D2)", "",
         "Protocolo: imagem 4K inteira na escala nativa, casamento um para um por IoU >= 0,50 sem olhar a classe; cada pessoa recebe a classe "
         "da predicao com que casou. Precisao de armada = armadas chamadas de armada / todas as predicoes de classe armada. "
         "d' com correcao log-linear. Conjuntos: val = divisao de validacao do proprio corpus; novos = quadros nunca vistos "
         "(80 quadros da semente 43 para o 35 m e o gemeo; os 50 quadros do teste de arma inedita para o 75 m original).", "",
         "## Reproducao a conf 0,25 contra os arquivos ja publicados", "",
         "| Modelo | Conjunto | Arquivo | armada (rep. / obtido) | desarmada | objeto | maior dif. | ok (<= 0,002) |", "|---|---|---|---|---|---|---|---|"]
    for r in out["reproducao_conf_0.25"]:
        rp, ob = r.get("reportado"), r["obtido"]
        if rp:
            L.append(f"| {r['modelo']} | {r['conjunto']} | `{r['arquivo']}` | {rp['armada']:.4f} / {ob['armada']:.4f} | "
                     f"{rp['desarmada']:.4f} / {ob['desarmada']:.4f} | {rp['objeto']:.4f} / {ob['objeto']:.4f} | {r['max_abs_dif']:.4f} | "
                     f"{'sim' if r['ok_0002'] else 'NAO'} |")
        else:
            L.append(f"| {r['modelo']} | {r['conjunto']} | `{r['arquivo']}` (nao encontrado) | {ob['armada']:.4f} | {ob['desarmada']:.4f} | {ob['objeto']:.4f} | | |")
    L += ["", "## Tres pontos de operacao por modelo e conjunto", "",
          "| Modelo | Conjunto | Quadros | Ponto | limiar | recall armada | objeto chamado armada | desarmada chamada armada | precisao armada | F1 armada | d' arm. vs obj. | d' arm. vs desarm. |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for chave, r in out["resultados"].items():
        for rot, nome in (("conf_0.25", "conf 0,25 (padrao)"), ("max_f1_armada", "max F1 de armada"), ("objeto_<=_0.10", "objeto <= 0,10")):
            p = r["pontos"][rot]
            if p is None:
                L.append(f"| {r['modelo']} | {r['conjunto']} | {r['quadros']} | {nome} | nenhum limiar ate 0,95 | | | | | | | |")
                continue
            L.append(f"| {r['modelo']} | {r['conjunto']} | {r['quadros']} | {nome} | {p['limiar']:.2f} | {p['recall_armada']:.3f} | "
                     f"{p['objeto_chamado_armada']:.3f} | {p['desarmada_chamada_armada']:.3f} | {p['precisao_armada']:.3f} | {p['f1_armada']:.3f} | "
                     f"{p['dlinha_armada_vs_objeto']:.2f} | {p['dlinha_armada_vs_desarmada']:.2f} |")
    L += ["", "## Intervalos por reamostragem de quadros a conf 0,25 (1.000 reamostras, semente 0)", "",
          "| Modelo | Conjunto | Quadros | objeto chamado armada | IC 95% | desarmada chamada armada | IC 95% | recall armada | IC 95% | d' arm. vs obj. | IC 95% |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for chave, r in out["resultados"].items():
        p, b = r["pontos"]["conf_0.25"], r["bootstrap_quadros_conf_0.25"]
        L.append(f"| {r['modelo']} | {r['conjunto']} | {r['quadros']} | {p['objeto_chamado_armada']:.3f} | {b['objeto_chamado_armada_ic95'][0]:.3f} a "
                 f"{b['objeto_chamado_armada_ic95'][1]:.3f} | {p['desarmada_chamada_armada']:.3f} | {b['desarmada_chamada_armada_ic95'][0]:.3f} a "
                 f"{b['desarmada_chamada_armada_ic95'][1]:.3f} | {p['recall_armada']:.3f} | {b['recall_armada_ic95'][0]:.3f} a {b['recall_armada_ic95'][1]:.3f} | "
                 f"{p['dlinha_armada_vs_objeto']:.2f} | {b['dlinha_armada_vs_objeto_ic95'][0]:.2f} a {b['dlinha_armada_vs_objeto_ic95'][1]:.2f} |")
    L += ["", "## Diferencas 35 m menos 75 m a conf 0,25 (reamostragem independente de quadros em cada lado)", "",
          "| Comparacao | Conjunto | Medida | a | b | dif. | IC 95% | exclui zero | reamostras com dif. > 0 | dif. relativa (% do menor) |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for d in out["diferencas_bootstrap_quadros"]:
        L.append(f"| {d['comparacao']} | {d['conjunto']} | {d['medida']} | {d['a']:.3f} | {d['b']:.3f} | {d['dif']:+.3f} | "
                 f"{d['dif_ic95'][0]:+.3f} a {d['dif_ic95'][1]:+.3f} | {'sim' if d['ic_exclui_zero'] else 'nao'} | {100 * d['fracao_positiva']:.1f}% | "
                 f"{d['dif_relativa_pct_do_menor']:+.1f}% |")
    if out["faltando"]:
        L += ["", "Faltando: " + "; ".join(out["faltando"])]
    with open(os.path.join(AQUI, "limiar_armado.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def figura(resultados):
    """objeto chamado de armada (x) contra recall de armada (y), uma curva por modelo, paineis val e novos"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    AZUL, LARANJA, AGUA, CINZA, TINTA = "#2a78d6", "#eb6834", "#1baf7a", "#8a8a86", "#0b0b0b"
    plt.rcParams.update({"font.family": "Arial", "font.size": 7.5, "axes.edgecolor": "#555", "axes.linewidth": 0.6,
                         "xtick.color": "#333", "ytick.color": "#333"})
    familias = {"S-nadir-35": (AZUL, "o", "S-nadir-35 (35 m)"), "Twin-75": (LARANJA, "^", "Twin of 35 m at 75 m"),
                "S-nadir-75": (AGUA, "s", "S-nadir-75 (original 75 m)")}
    estilo_semente = {"s0": "-", "s1": (0, (4, 2)), "s2": (0, (1, 1.5))}
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 4.2), dpi=300, sharey=True)
    titulos = {"val": "Validation split of each corpus", "novos": "New frames (80 at 35 m and at 75 m; 50 unseen-weapon frames for S-nadir-75)"}
    # deslocamento do rotulo direto (x, y) a partir do fim da curva (limiar 0,05), por painel e familia
    desloc = {("val", "S-nadir-35"): (0.012, 0.03), ("val", "S-nadir-75"): (0.012, -0.02), ("val", "Twin-75"): (0.012, -0.04),
              ("novos", "S-nadir-35"): (0.012, 0.0), ("novos", "S-nadir-75"): (0.012, -0.05), ("novos", "Twin-75"): ("abs", 0.005, 0.64)}
    for ax, conjunto in zip(axes, ("val", "novos")):
        rotulados = set()
        for chave, r in resultados.items():
            if r["conjunto"] != conjunto:
                continue
            fam = next(f for f in familias if r["modelo"].startswith(f))
            cor, marcador, rotulo = familias[fam]
            sem = r["modelo"].split()[-1] if r["modelo"].split()[-1].startswith("s") and len(r["modelo"].split()) > 1 else "s0"
            ls = estilo_semente.get(sem, "-")
            xs = [r["curva"][t]["objeto_chamado_armada"] for t in sorted(r["curva"], key=float)]
            ys = [r["curva"][t]["recall_armada"] for t in sorted(r["curva"], key=float)]
            ax.plot(xs, ys, color=cor, lw=1.4 if sem == "s0" else 1.0, ls=ls, zorder=3, alpha=1.0 if sem == "s0" else 0.85)
            p = r["pontos"]["conf_0.25"]
            ax.plot([p["objeto_chamado_armada"]], [p["recall_armada"]], marker=marcador, ms=6 if sem == "s0" else 5, color=cor,
                    mfc=cor if sem == "s0" else "white", mec="white" if sem == "s0" else cor, mew=0.8 if sem == "s0" else 1.0, zorder=5)
            if fam not in rotulados:
                rotulados.add(fam)
                d = desloc[(conjunto, fam)]
                if d[0] == "abs":
                    ax.text(d[1], d[2], rotulo, color=TINTA, ha="left", va="center", fontsize=7, zorder=6)
                else:
                    ax.text(xs[0] + d[0], ys[0] + d[1], rotulo, color=TINTA, ha="left" if d[0] > 0 else "right", va="center",
                            fontsize=7, zorder=6)
        ax.set_xlim(-0.005, 0.42)
        ax.set_ylim(0, 0.8)
        ax.set_xlabel("Person carrying a confusable object called armed (rate)")
        ax.grid(color="#e4e4e2", lw=0.5)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.text(0.0, 1.02, titulos[conjunto], transform=ax.transAxes, ha="left", va="bottom", fontsize=7, style="italic")
    axes[0].set_ylabel("Armed recall (armed person called armed)")
    axes[0].text(0.03, 0.97, "filled marker: confidence 0.25, seed 0\nhollow marker: confidence 0.25, seeds 1 and 2\n"
                 "each curve sweeps the threshold from 0.95\n(lower left) to 0.05 (upper right)",
                 transform=axes[0].transAxes, ha="left", va="top", fontsize=6.3, color="#444")
    fig.tight_layout(pad=0.5, w_pad=1.2)
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, "fig12_limiar_armado.png"))
    plt.close(fig)


if __name__ == "__main__":
    main()
