#!/usr/bin/env python3
"""
bootstrap_visdrone.py: intervalos de 95% por reamostragem de imagens (bootstrap) para o mAP50 de cada
modelo de classe unica no VisDrone-DET val, para a eficacia (mAP50 / mAP50 de R na MESMA reamostra) e
para as diferencas pareadas entre modelos, a partir do que visdrone_preds.py guardou por imagem.

Ponto S1 do feedback de 14/10 (intervalos de confianca) e A3 (diferencas pequenas tratadas como
resultado). Revisao de 17/10/2026, agente D2.

Metodo. 1.000 reamostras das 548 imagens com reposicao (numpy default_rng, semente 0), as mesmas para
todos os modelos (pareadas). Em cada reamostra o mAP50 e recalculado com a regra do validador do
Ultralytics (ap_per_class: ordenar por confianca, acumular acertos e erros, envelope de precisao,
integracao em 101 pontos). Para ir rapido, a reamostra entra como multiplicidade por imagem (peso 0, 1,
2...) nas somas acumuladas, o que da o mesmo resultado que repetir as predicoes; a equivalencia e
conferida contra ap_per_class com as predicoes repetidas de fato (campo `verificacao_equivalencia`).
Intervalo: percentis 2,5 e 97,5 da distribuicao de reamostras. Diferenca relativa: em % do menor dos
dois valores no conjunto inteiro.

  C:/arma3-favela/venv/Scripts/python.exe bootstrap_visdrone.py
Saidas: bootstrap_visdrone.json, bootstrap_visdrone.md

Rodada 5 (18/10/2026): com --sufixo r5 o script grava bootstrap_visdrone_r5.json e .md e NAO toca nos
de 17/10, que o artigo cita (sem --sufixo o calculo e o de antes, sobre os 17 modelos de 17/10). No
modo r5 as comparacoes sao entre GRUPOS de runs (as sementes de cada lado, PLANO-RODADA5.md, secao
2.3): a diferenca e calculada na media das sementes de cada lado, em cada reamostra; as mesmas 1.000
reamostras, semente 0. Os pares sao os das secoes 3.1, 3.2, 3.5 e 3.8 do plano; a celula de controle
do ajuste fino e os cronogramas escolhidos vem de ../rodada5_ft_reproducao.json e
../rodada5_ft_selecao.json (gravados pela cadeia). Par sem preds de um dos lados sai em "faltando".

  C:/arma3-favela/venv/Scripts/python.exe bootstrap_visdrone.py --sufixo r5
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from visdrone_preds import MODELOS, MODELOS_1710, reportado  # noqa: E402

N_BOOT = 1000
SEMENTE = 0
NOME = {v: k for k, v in MODELOS.items()}          # run -> nome no artigo
RES = os.path.dirname(AQUI)

# pares pedidos (a menos b), por nome no artigo; "seeds" expande s0/s1/s2 casados e a media das sementes
PARES = [
    ("S-oblique", "S-nadir-150", "nadir vs oblique"),
    ("S-oblique-six", "S-oblique", "six settlements vs one, oblique"),
    ("S-nadir-150-six", "S-nadir-150", "six settlements vs one, nadir"),
    ("F-generic 5%", "F-synthetic 5%", "generic vs synthetic start, 5%"),
    ("F-generic 10%", "F-synthetic 10%", "generic vs synthetic start, 10%"),
    ("F-generic 5%", "F-joint 5%", "generic vs joint, 5%"),
    ("F-generic 10%", "F-joint 10%", "generic vs joint, 10%"),
    ("F-joint 5%", "F-synthetic 5%", "joint vs synthetic start, 5%"),
    ("F-joint 10%", "F-synthetic 10%", "joint vs synthetic start, 10%"),
]


def carrega(run):
    p = os.path.join(AQUI, f"preds_visdrone_{run}.npz")
    if not os.path.exists(p):
        return None
    d = np.load(p, allow_pickle=False)
    conf, tp50, img_idx, n_gt = d["conf"], d["tp"][:, 0], d["img_idx"], d["n_gt"]
    o = np.argsort(-conf, kind="stable")             # ordem fixa: a mesma para todas as reamostras
    return {"run": run, "conf": conf[o], "tp": tp50[o].astype(np.float64), "img": img_idx[o], "n_gt": n_gt.astype(np.float64),
            "n_img": len(n_gt)}


def compute_ap(recall, precision):
    """copia literal de ultralytics.utils.metrics.compute_ap (metodo 'interp', 101 pontos)"""
    mrec = np.concatenate(([0.0], recall, [recall[-1] if len(recall) else 1.0], [1.0]))
    mpre = np.concatenate(([1.0], precision, [0.0], [0.0]))
    mpre = np.flip(np.maximum.accumulate(np.flip(mpre)))
    x = np.linspace(0, 1, 101)
    return float(np.trapezoid(np.interp(x, mrec, mpre), x))


def ap50(m, w):
    """mAP50 (classe unica) da reamostra com multiplicidade w por imagem (w = 1 em todas = conjunto inteiro)"""
    wp = w[m["img"]]
    n_l = float((m["n_gt"] * w).sum())
    if n_l == 0:
        return float("nan")
    fica = wp > 0                                     # predicao de imagem fora da reamostra nao existe
    if not fica.any():                                # sem predicao: AP 0, como no ap_per_class (rodada 5)
        return 0.0
    tp, wp = m["tp"][fica], wp[fica]
    tpc = np.cumsum(tp * wp)
    fpc = np.cumsum((1.0 - tp) * wp)
    recall = tpc / (n_l + 1e-16)
    precision = tpc / (tpc + fpc)
    return compute_ap(recall, precision)


def ap50_referencia(m, w):
    """o mesmo mAP50 pela funcao do Ultralytics, com as predicoes e caixas repetidas de fato"""
    from ultralytics.utils.metrics import ap_per_class
    wp = w[m["img"]].astype(int)
    tp = np.repeat(m["tp"].astype(bool), wp)[:, None]
    conf = np.repeat(m["conf"], wp)
    n_l = int((m["n_gt"] * w).sum())
    r = ap_per_class(tp, conf, np.zeros(len(conf)), np.zeros(n_l))
    return float(r[5][:, 0].mean())


def ic(v):
    v = np.asarray(v, dtype=float)
    return [round(float(np.percentile(v, 2.5)), 4), round(float(np.percentile(v, 97.5)), 4)]


def main():
    if "--sufixo" in sys.argv:
        return main_r5(sys.argv[sys.argv.index("--sufixo") + 1])
    modelos = {}
    faltando = []
    for nome, run in MODELOS_1710.items():
        m = carrega(run)
        if m is None:
            faltando.append(run)
        else:
            modelos[nome] = m
    if "R" not in modelos:
        raise SystemExit("sem R (r_pareado): rode visdrone_preds.py antes")
    n_img = modelos["R"]["n_img"]
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, n_img, size=(N_BOOT, n_img))
    W = np.stack([np.bincount(i, minlength=n_img) for i in idx]).astype(np.float64)   # (N_BOOT, 548)

    # equivalencia entre o calculo rapido (pesos) e o ap_per_class com repeticao, em 3 reamostras e no conjunto inteiro
    verif = []
    for nome in ("R", "S-oblique-six s0", "S-nadir-150"):
        if nome in modelos:
            for b in (None, 0, 1, 2):
                w = np.ones(n_img) if b is None else W[b]
                a, r = ap50(modelos[nome], w), ap50_referencia(modelos[nome], w)
                verif.append({"modelo": nome, "reamostra": b, "rapido": round(a, 6), "ap_per_class": round(r, 6),
                              "dif": round(a - r, 7)})
    max_dif = max(abs(v["dif"]) for v in verif)

    # mAP50 por modelo: conjunto inteiro e reamostras
    cheio = {n: ap50(m, np.ones(n_img)) for n, m in modelos.items()}
    boot = {n: np.array([ap50(m, W[b]) for b in range(N_BOOT)]) for n, m in modelos.items()}
    efic = {n: boot[n] / boot["R"] for n in boot}
    por_modelo = {}
    for n in modelos:
        por_modelo[n] = {"run": modelos[n]["run"], "mAP50_reportado": reportado(modelos[n]["run"]),
                         "mAP50_conjunto_inteiro": round(cheio[n], 4), "mAP50_boot_media": round(float(boot[n].mean()), 4),
                         "mAP50_ic95": ic(boot[n]), "eficacia_conjunto_inteiro": round(cheio[n] / cheio["R"], 4),
                         "eficacia_boot_media": round(float(efic[n].mean()), 4), "eficacia_ic95": ic(efic[n])}

    # diferencas pareadas (mesmas reamostras)
    def expande(base):
        """nomes concretos de um rotulo: 's0, s1, s2' quando ha sementes, senao o proprio"""
        if base in modelos:
            return [base]
        return [f"{base} s{k}" for k in range(3) if f"{base} s{k}" in modelos]

    def dif(a_nomes, b_nomes, rotulo, comparacao):
        """a menos b; com listas de sementes usa a media das sementes por reamostra"""
        A = np.mean([boot[x] for x in a_nomes], 0)
        B = np.mean([boot[x] for x in b_nomes], 0)
        a0 = float(np.mean([cheio[x] for x in a_nomes]))
        b0 = float(np.mean([cheio[x] for x in b_nomes]))
        d = A - B
        razao = A / B
        menor = min(a0, b0)
        return {"comparacao": comparacao, "a": a_nomes, "b": b_nomes, "rotulo": rotulo,
                "a_mAP50": round(a0, 4), "b_mAP50": round(b0, 4), "dif_conjunto_inteiro": round(a0 - b0, 4),
                "dif_boot_media": round(float(d.mean()), 4), "dif_ic95": ic(d),
                "fracao_reamostras_positiva": round(float((d > 0).mean()), 3),
                "dif_relativa_pct_do_menor": round(100 * (a0 - b0) / menor, 1) if menor > 0 else None,
                "razao_a_sobre_b": round(a0 / b0, 3) if b0 > 0 else None, "razao_ic95": [round(float(np.percentile(razao, 2.5)), 3),
                                                                                       round(float(np.percentile(razao, 97.5)), 3)],
                "ic_exclui_zero": bool(ic(d)[0] > 0 or ic(d)[1] < 0)}

    difs = []
    for a, b, comp in PARES:
        ea, eb = expande(a), expande(b)
        if not ea or not eb:
            continue
        if len(ea) > 1 or len(eb) > 1:
            # casadas por semente onde as duas tem sementes; senao cada semente contra o modelo unico
            if len(ea) > 1 and len(eb) > 1:
                for x, y in zip(ea, eb):
                    difs.append(dif([x], [y], f"{x} - {y}", comp))
            elif len(ea) > 1:
                for x in ea:
                    difs.append(dif([x], eb, f"{x} - {eb[0]}", comp))
            else:
                for y in eb:
                    difs.append(dif(ea, [y], f"{ea[0]} - {y}", comp))
            difs.append(dif(ea, eb, f"{a} (media das sementes) - {b}" + (" (media das sementes)" if len(eb) > 1 else ""), comp))
        else:
            difs.append(dif(ea, eb, f"{a} - {b}", comp))

    out = {"protocolo": "VisDrone-DET val, 548 imagens, classe unica, imgsz 1280, conf 0,001, NMS IoU 0,7, max_det 300; "
                        "predicoes guardadas por visdrone_preds.py (batch 4, FP16)",
           "bootstrap": {"reamostras": N_BOOT, "semente": SEMENTE, "gerador": "numpy default_rng(0).integers(0, 548, (1000, 548))",
                         "unidade": "imagem (548, com reposicao)", "pareado": "as mesmas reamostras para todos os modelos",
                         "intervalo": "percentis 2,5 e 97,5"},
           "verificacao_equivalencia": {"max_abs_dif": max_dif, "casos": verif},
           "faltando": faltando, "modelos": por_modelo, "diferencas": difs,
           "quando": datetime.now().isoformat(timespec="seconds")}
    with open(os.path.join(AQUI, "bootstrap_visdrone.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    # tabela
    L = ["# Intervalos por reamostragem de imagens no VisDrone-DET val (17/10/2026, agente D2)", "",
         f"Protocolo do artigo (classe unica, imgsz 1280, conf 0,001); {N_BOOT} reamostras das 548 imagens com reposicao, semente {SEMENTE}, "
         "as mesmas para todos os modelos. Intervalo = percentis 2,5 e 97,5. Eficacia = mAP50 do modelo / mAP50 de R na mesma reamostra. "
         f"Equivalencia do calculo com ap_per_class do Ultralytics conferida (maior diferenca absoluta {max_dif:.1e}).", "",
         "## mAP50 por modelo", "",
         "| Modelo | Run | mAP50 reportado | mAP50 (esta rodada) | media boot | IC 95% | Eficacia | IC 95% da eficacia |",
         "|---|---|---|---|---|---|---|---|"]
    for n, v in por_modelo.items():
        L.append(f"| {n} | `{v['run']}` | {v['mAP50_reportado']} | {v['mAP50_conjunto_inteiro']:.4f} | {v['mAP50_boot_media']:.4f} | "
                 f"{v['mAP50_ic95'][0]:.4f} a {v['mAP50_ic95'][1]:.4f} | {100 * v['eficacia_conjunto_inteiro']:.1f}% | "
                 f"{100 * v['eficacia_ic95'][0]:.1f} a {100 * v['eficacia_ic95'][1]:.1f}% |")
    L += ["", "## Diferencas pareadas (a menos b, mesmas reamostras)", "",
          "| Comparacao | a | b | dif. absoluta | IC 95% | reamostras com dif. > 0 | dif. relativa (% do menor) | razao a/b | IC 95% da razao |",
          "|---|---|---|---|---|---|---|---|---|"]
    for d in difs:
        L.append(f"| {d['comparacao']}: {d['rotulo']} | {d['a_mAP50']:.4f} | {d['b_mAP50']:.4f} | {d['dif_conjunto_inteiro']:+.4f} | "
                 f"{d['dif_ic95'][0]:+.4f} a {d['dif_ic95'][1]:+.4f} | {100 * d['fracao_reamostras_positiva']:.1f}% | "
                 f"{d['dif_relativa_pct_do_menor']:+.1f}% | {d['razao_a_sobre_b']} | {d['razao_ic95'][0]} a {d['razao_ic95'][1]} |")
    if faltando:
        L += ["", "Pesos faltando: " + ", ".join(faltando)]
    with open(os.path.join(AQUI, "bootstrap_visdrone.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


# ------------------------------------------------------------------ rodada 5 (--sufixo)
def le_res(nome):
    p = os.path.join(RES, nome)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def existe(run):
    return os.path.exists(os.path.join(AQUI, f"preds_visdrone_{run}.npz"))


def grupos_r5():
    """rotulo -> lista de runs (as sementes de um lado). So entra o que tem preds."""
    g = {"R": ["r_pareado"],
         "S-nadir-150": ["s_nadir_4k", "s_nadir_4k_sd1", "s_nadir_4k_sd2"],
         "S-oblique": ["s_obliquo", "s_obliquo_sd1", "s_obliquo_sd2"],
         "S-oblique-six": ["s_oblvar", "s_oblvar_sd1", "s_oblvar_sd2"],
         "S-nadir-150-six": ["s_variedade"],
         "S-oblique-six c030": ["s_oblvar_c030", "s_oblvar_c030_sd1", "s_oblvar_c030_sd2"],
         "S-oblique-six c060": ["s_oblvar_c060"],
         "S-oblique-six c090": ["s_oblvar_c090"],
         "S-oblique-six c120": ["s_oblvar_c120", "s_oblvar_c120_sd1", "s_oblvar_c120_sd2"],
         "S-oblique-six scenes": ["s_oblvar", "s_oblvar_e22", "s_oblvar_e23"],
         "S-nadir-150 hard-sun": ["s_soldur_4k"]}
    rep = le_res("rodada5_ft_reproducao.json") or {}
    reproduz = rep.get("reproduz", True)
    for f in ("05", "10"):
        for ini, art in (("sint", "F-synthetic"), ("coco", "F-generic")):
            if reproduz:
                orig = [f"ft{f}_{ini}"] + ([f"ft05_{ini}_sd1", f"ft05_{ini}_sd2"] if f == "05" else [])
            else:
                orig = [f"ft{f}_{ini}_rep"]
            g[f"{art} {int(f)}% orig"] = orig
            for cel in ("fz", "lr", "fzlr"):
                g[f"{art} {int(f)}% {cel}"] = [f"ft{f}_{ini}_{cel}"] + (
                    [f"ft05_{ini}_{cel}_sd1", f"ft05_{ini}_{cel}_sd2"] if f == "05" else [])
    sel = le_res("rodada5_ft_selecao.json")
    if sel:
        for f in ("05", "10"):
            for ini, art in (("sint", "F-synthetic"), ("coco", "F-generic")):
                cel = sel["escolha"][f][ini]
                g[f"{art} {int(f)}% chosen"] = g[f"{art} {int(f)}% {cel}"]
    return {k: [r for r in v if existe(r)] for k, v in g.items()}


PARES_R5 = [("S-oblique", "S-nadir-150", "R5-1 nadir vs oblique (principal)"),
            ("S-oblique-six", "S-oblique", "R5-1 six settlements vs one, oblique"),
            ("S-nadir-150-six", "S-nadir-150", "R5-1 six settlements vs one, nadir")]
for _f in ("5", "10"):
    for _cel in ("orig", "fz", "lr", "fzlr"):
        PARES_R5.append((f"F-generic {_f}% {_cel}", f"F-synthetic {_f}% {_cel}",
                         f"R5-5 generic vs synthetic start, {_f}%, cell {_cel}"))
    PARES_R5.append((f"F-generic {_f}% chosen", f"F-synthetic {_f}% chosen",
                     f"R5-5 generic vs synthetic start, {_f}%, chosen schedules"))
PARES_R5 += [("S-oblique-six", "S-oblique-six c030", "R5-3 152 vs 30 frames"),
             ("S-oblique-six", "S-oblique-six c120", "R5-3 152 vs 120 frames"),
             ("S-oblique-six scenes", "S-oblique", "R5-2 C-ii scene seeds vs S-oblique training seeds")]


def main_r5(sufixo):
    g = grupos_r5()
    runs = sorted({r for v in g.values() for r in v})
    if "r_pareado" not in runs:
        raise SystemExit("sem R (r_pareado): rode visdrone_preds.py antes")
    m = {r: carrega(r) for r in runs}
    n_img = m["r_pareado"]["n_img"]
    rng = np.random.default_rng(SEMENTE)
    idx = rng.integers(0, n_img, size=(N_BOOT, n_img))
    W = np.stack([np.bincount(i, minlength=n_img) for i in idx]).astype(np.float64)
    cheio = {r: ap50(m[r], np.ones(n_img)) for r in runs}
    boot = {r: np.array([ap50(m[r], W[b]) for b in range(N_BOOT)]) for r in runs}
    por_run = {r: {"nome": NOME.get(r), "mAP50_reportado": reportado(r), "mAP50_conjunto_inteiro": round(cheio[r], 4),
                   "mAP50_ic95": ic(boot[r]), "eficacia_conjunto_inteiro": round(cheio[r] / cheio["r_pareado"], 4),
                   "eficacia_ic95": ic(boot[r] / boot["r_pareado"])} for r in runs}
    por_grupo = {}
    for k, v in g.items():
        if not v:
            continue
        mb = np.mean([boot[r] for r in v], 0)
        vals = [round(cheio[r], 4) for r in v]
        med = float(np.mean([cheio[r] for r in v]))
        por_grupo[k] = {"runs": v, "valores": vals, "media": round(med, 4), "min": min(vals), "max": max(vals),
                        "n": len(v), "media_ic95": ic(mb), "eficacia_media": round(med / cheio["r_pareado"], 4),
                        "eficacia_ic95": ic(mb / boot["r_pareado"])}
    difs, faltando = [], []
    for a, b, comp in PARES_R5:
        ra, rb = g.get(a, []), g.get(b, [])
        if not ra or not rb:
            faltando.append(comp)
            continue
        A = np.mean([boot[x] for x in ra], 0)
        B = np.mean([boot[x] for x in rb], 0)
        a0 = float(np.mean([cheio[x] for x in ra]))
        b0 = float(np.mean([cheio[x] for x in rb]))
        d = A - B
        menor = min(a0, b0)
        razao = A / B
        difs.append({"comparacao": comp, "a": a, "b": b, "a_runs": ra, "b_runs": rb,
                     "a_valores": [round(cheio[x], 4) for x in ra], "b_valores": [round(cheio[x], 4) for x in rb],
                     "a_mAP50": round(a0, 4), "b_mAP50": round(b0, 4), "dif_conjunto_inteiro": round(a0 - b0, 4),
                     "dif_boot_media": round(float(d.mean()), 4), "dif_ic95": ic(d),
                     "fracao_reamostras_positiva": round(float((d > 0).mean()), 3),
                     "dif_relativa_pct_do_menor": round(100 * (a0 - b0) / menor, 1) if menor > 0 else None,
                     "razao_a_sobre_b": round(a0 / b0, 3) if b0 > 0 else None,
                     "razao_ic95": [round(float(np.percentile(razao, 2.5)), 3), round(float(np.percentile(razao, 97.5)), 3)],
                     "ic_exclui_zero": bool(ic(d)[0] > 0 or ic(d)[1] < 0)})
    out = {"plano": "07-blender/PLANO-RODADA5.md, secao 2.3 (b)",
           "protocolo": "VisDrone-DET val, 548 imagens, classe unica, imgsz 1280, conf 0,001, NMS IoU 0,7, max_det 300; "
                        "predicoes de visdrone_preds.py (FP32, lote 4)",
           "bootstrap": {"reamostras": N_BOOT, "semente": SEMENTE, "unidade": "imagem, com reposicao",
                         "pareado": "as mesmas reamostras para todos os modelos; diferenca na media das sementes de cada lado"},
           "runs": por_run, "grupos": por_grupo, "diferencas": difs, "faltando": faltando,
           "quando": datetime.now().isoformat(timespec="seconds")}
    with open(os.path.join(AQUI, f"bootstrap_visdrone_{sufixo}.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    L = [f"# Reamostragem no VisDrone-DET val, rodada 5 ({datetime.now():%d/%m/%Y})", "",
         f"{N_BOOT} reamostras das {n_img} imagens, semente {SEMENTE}, pareadas; diferenca na media das sementes de cada lado.", "",
         "| Grupo | runs | media mAP50 | faixa | IC 95% da media | eficacia |", "|---|---|---|---|---|---|"]
    for k, v in por_grupo.items():
        L.append(f"| {k} | {', '.join(v['runs'])} | {v['media']:.4f} | {v['min']:.4f} a {v['max']:.4f} | "
                 f"{v['media_ic95'][0]:.4f} a {v['media_ic95'][1]:.4f} | {100 * v['eficacia_media']:.1f}% |")
    L += ["", "| Comparacao | a | b | dif. | IC 95% | dif. relativa | razao a/b (IC 95%) |", "|---|---|---|---|---|---|---|"]
    for d in difs:
        rel = "n/a" if d["dif_relativa_pct_do_menor"] is None else f"{d['dif_relativa_pct_do_menor']:+.1f}%"
        L.append(f"| {d['comparacao']} | {d['a_mAP50']:.4f} | {d['b_mAP50']:.4f} | {d['dif_conjunto_inteiro']:+.4f} | "
                 f"{d['dif_ic95'][0]:+.4f} a {d['dif_ic95'][1]:+.4f} | {rel} | {d['razao_a_sobre_b']} "
                 f"({d['razao_ic95'][0]} a {d['razao_ic95'][1]}) |")
    if faltando:
        L += ["", "Faltando: " + "; ".join(faltando)]
    with open(os.path.join(AQUI, f"bootstrap_visdrone_{sufixo}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
