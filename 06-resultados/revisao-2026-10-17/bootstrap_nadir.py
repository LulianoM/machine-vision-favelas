#!/usr/bin/env python3
"""
bootstrap_nadir.py: intervalos por reamostragem de imagens na base real nadir (rodada 5, R5-6;
PLANO-RODADA5.md, secao 3.3), a partir do que preds_nadir.py guardou por imagem.

Mesmo metodo de bootstrap_visdrone.py (de onde vem o calculo do mAP50 por multiplicidade): 1.000
reamostras das imagens com reposicao, numpy default_rng(0), as mesmas para todos os modelos, diferenca
na media das sementes de cada lado; intervalo pelos percentis 2,5 e 97,5. Para cada par grava as tres
leituras da secao 2.3 do plano: (a) faixas de sementes (funcoes de resolvivel.py), (b) intervalo
pareado que exclui zero, (c) diferenca relativa de pelo menos 30% do menor valor.

Pares, fixados no plano antes de rodar:
  principal    S-oblique (3 sementes) menos S-nadir-150 (3 sementes)
  secundario   S-oblique-six (3) menos S-nadir-150-six (1)
  validade     R (r_pareado) com mAP50 de pelo menos 0,05; abaixo disso o resultado e "nao interpretavel"
  razao        oblique/nadir aqui contra a do VisDrone (bootstrap_visdrone_r5.json, ou o de 17/10), descritiva
Tambem o mAP50 e a eficacia contra R de cada modelo, e o exploratorio armado_150g (classe unica).

  C:/arma3-favela/venv/Scripts/python.exe bootstrap_nadir.py --tag heridal
Saidas: bootstrap_<tag>.json, bootstrap_<tag>.md
"""
import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from bootstrap_visdrone import N_BOOT, SEMENTE, ap50, ic  # noqa: E402
from resolvivel import LIMIAR_REL, faixa, leitura_a  # noqa: E402

GRUPOS = {"R": ["r_pareado"],
          "S-nadir-150": ["s_nadir_4k", "s_nadir_4k_sd1", "s_nadir_4k_sd2"],
          "S-nadir-150-six": ["s_variedade"],
          "S-oblique": ["s_obliquo", "s_obliquo_sd1", "s_obliquo_sd2"],
          "S-oblique-six": ["s_oblvar", "s_oblvar_sd1", "s_oblvar_sd2"],
          "Armado-150 (exploratorio)": ["armado_150g"]}
PARES = [("S-oblique", "S-nadir-150", "principal: oblique vs nadir"),
         ("S-oblique-six", "S-nadir-150-six", "secundaria: six settlements, oblique vs nadir")]
LIMIAR_VALIDADE = 0.05


def carrega(tag, run):
    p = os.path.join(AQUI, f"preds_{tag}_{run}.npz")
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=False)
    conf, tp50, img_idx, n_gt = d["conf"], d["tp"][:, 0], d["img_idx"], d["n_gt"]
    o = np.argsort(-conf, kind="stable")
    return {"run": run, "conf": conf[o], "tp": tp50[o].astype(np.float64), "img": img_idx[o],
            "n_gt": n_gt.astype(np.float64), "n_img": len(n_gt), "names": d["names"]}


def razao_visdrone():
    for arq, comp in (("bootstrap_visdrone_r5.json", "R5-1 nadir vs oblique (principal)"),
                      ("bootstrap_visdrone.json", "nadir vs oblique")):
        p = os.path.join(AQUI, arq)
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        cand = [x for x in d["diferencas"] if x["comparacao"] == comp]
        if comp == "nadir vs oblique":
            cand = [x for x in cand if "media" in x["rotulo"]] or cand
        if cand:
            return {"fonte": arq, "razao": cand[0]["razao_a_sobre_b"], "razao_ic95": cand[0]["razao_ic95"]}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    a = ap.parse_args()
    runs = sorted({r for v in GRUPOS.values() for r in v})
    m = {r: carrega(a.tag, r) for r in runs}
    faltando = [r for r in runs if m[r] is None]
    m = {r: v for r, v in m.items() if v is not None}
    if "r_pareado" not in m:
        raise SystemExit(f"sem preds_{a.tag}_r_pareado.npz: rode preds_nadir.py antes")
    n_img = m["r_pareado"]["n_img"]
    for r, v in m.items():
        assert v["n_img"] == n_img and (v["names"] == m["r_pareado"]["names"]).all(), f"{r}: imagens diferentes de R"
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, n_img, size=(N_BOOT, n_img))
    W = np.stack([np.bincount(i, minlength=n_img) for i in idx]).astype(np.float64)
    cheio = {r: ap50(v, np.ones(n_img)) for r, v in m.items()}
    boot = {r: np.array([ap50(v, W[b]) for b in range(N_BOOT)]) for r, v in m.items()}
    r0 = cheio["r_pareado"]
    por_run = {r: {"mAP50": round(cheio[r], 4), "mAP50_ic95": ic(boot[r]),
                   "eficacia": round(cheio[r] / r0, 4) if r0 > 0 else None,
                   "eficacia_ic95": ic(boot[r] / boot["r_pareado"]) if r0 > 0 else None} for r in m}
    g = {k: [r for r in v if r in m] for k, v in GRUPOS.items()}
    por_grupo = {}
    for k, v in g.items():
        if v:
            med = float(np.mean([cheio[r] for r in v]))
            por_grupo[k] = {"runs": v, "valores": [round(cheio[r], 4) for r in v], "media": round(med, 4),
                            "media_ic95": ic(np.mean([boot[r] for r in v], 0)),
                            "eficacia_media": round(med / r0, 4) if r0 > 0 else None}
    difs = []
    for ga, gb, comp in PARES:
        ra, rb = g[ga], g[gb]
        if not ra or not rb:
            difs.append({"comparacao": comp, "faltando": True})
            continue
        A = np.mean([boot[x] for x in ra], 0)
        B = np.mean([boot[x] for x in rb], 0)
        a0 = float(np.mean([cheio[x] for x in ra]))
        b0 = float(np.mean([cheio[x] for x in rb]))
        d = A - B
        menor = min(a0, b0)
        with np.errstate(divide="ignore", invalid="ignore"):
            razao = A / B
        razao = razao[np.isfinite(razao)]
        fa, fb = faixa([round(cheio[x], 4) for x in ra]), faixa([round(cheio[x], 4) for x in rb])
        ra_txt, oka = leitura_a(fa, fb)
        rel = round(100 * (a0 - b0) / menor, 1) if menor > 0 else None
        okb = bool(ic(d)[0] > 0 or ic(d)[1] < 0)
        okc = rel is not None and abs(rel) >= LIMIAR_REL
        difs.append({"comparacao": comp, "a": ga, "b": gb, "a_runs": ra, "b_runs": rb, "a_mAP50": round(a0, 4),
                     "b_mAP50": round(b0, 4), "dif": round(a0 - b0, 4), "dif_ic95": ic(d),
                     "fracao_reamostras_positiva": round(float((d > 0).mean()), 3), "dif_relativa_pct_do_menor": rel,
                     "razao_a_sobre_b": round(a0 / b0, 3) if b0 > 0 else None,
                     "razao_ic95": ([round(float(np.percentile(razao, 2.5)), 3), round(float(np.percentile(razao, 97.5)), 3)]
                                    if len(razao) else None),
                     "a_faixas_de_sementes": ra_txt, "a_ok": oka, "b_ok": okb, "c_ok": okc,
                     "resolvivel": bool(oka is True or okb is True),
                     "sinal": "a acima" if a0 > b0 else "b acima"})
    out = {"tag": a.tag, "plano": "07-blender/PLANO-RODADA5.md, secao 3.3",
           "bootstrap": {"reamostras": N_BOOT, "semente": SEMENTE, "imagens": n_img, "unidade": "imagem, com reposicao",
                         "pareado": "as mesmas reamostras para todos os modelos"},
           "validade": {"R_mAP50": round(r0, 4), "limiar": LIMIAR_VALIDADE, "interpretavel": r0 >= LIMIAR_VALIDADE,
                        "regra": "R abaixo de 0,05 de mAP50 no imgsz casado: o protocolo falha, resultado nao interpretavel"},
           "runs": por_run, "grupos": por_grupo, "diferencas": difs, "razao_visdrone": razao_visdrone(),
           "faltando": faltando, "quando": datetime.now().isoformat(timespec="seconds")}
    with open(os.path.join(AQUI, f"bootstrap_{a.tag}.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    L = [f"# Base real nadir ({a.tag}): reamostragem de imagens ({datetime.now():%d/%m/%Y})", "",
         f"{N_BOOT} reamostras das {n_img} imagens, semente {SEMENTE}, pareadas. R = {r0:.4f} "
         f"({'interpretavel' if r0 >= LIMIAR_VALIDADE else 'NAO interpretavel: R abaixo de 0,05'}).", "",
         "| Grupo | runs | mAP50 (media) | IC 95% | eficacia |", "|---|---|---|---|---|"]
    for k, v in por_grupo.items():
        ef = "n/a" if v["eficacia_media"] is None else f"{100 * v['eficacia_media']:.1f}%"
        L.append(f"| {k} | {', '.join(v['runs'])} | {v['media']:.4f} | {v['media_ic95'][0]:.4f} a {v['media_ic95'][1]:.4f} | {ef} |")
    L += ["", "| Comparacao | a | b | dif. | IC 95% | (a) | (b) | (c) | razao a/b (IC 95%) |", "|---|---|---|---|---|---|---|---|---|"]
    for d in difs:
        if d.get("faltando"):
            L.append(f"| {d['comparacao']} | faltando | | | | | | | |")
            continue
        L.append(f"| {d['comparacao']} | {d['a_mAP50']:.4f} | {d['b_mAP50']:.4f} | {d['dif']:+.4f} | "
                 f"{d['dif_ic95'][0]:+.4f} a {d['dif_ic95'][1]:+.4f} | {d['a_faixas_de_sementes']} | "
                 f"{'sim' if d['b_ok'] else 'nao'} | {'sim' if d['c_ok'] else 'nao'} | {d['razao_a_sobre_b']} ({d['razao_ic95']}) |")
    if out["razao_visdrone"]:
        L += ["", f"Razao oblique/nadir no VisDrone: {out['razao_visdrone']['razao']} ({out['razao_visdrone']['razao_ic95']}), "
                  f"de {out['razao_visdrone']['fonte']}."]
    if faltando:
        L += ["", "Faltando: " + ", ".join(faltando)]
    with open(os.path.join(AQUI, f"bootstrap_{a.tag}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
