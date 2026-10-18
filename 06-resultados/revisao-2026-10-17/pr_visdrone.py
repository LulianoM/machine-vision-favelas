#!/usr/bin/env python3
"""
pr_visdrone.py: curvas precisao-recall a IoU 0,50 no VisDrone-DET val para R, S-oblique-six (semente 0),
F-generic 10% e F-synthetic 10%, a partir das predicoes guardadas por visdrone_preds.py (mesmo
protocolo de todos os numeros do artigo). Ponto S6 do feedback de 14/10. Revisao de 17/10/2026, D2.

A curva e a do validador do Ultralytics (ap_per_class): predicoes ordenadas por confianca, acertos e
erros acumulados, precisao com envelope (maior precisao em qualquer recall maior ou igual), amostrada
em 1.000 pontos de recall; a area sob ela e o AP50. O ponto de operacao e o da confianca que maximiza
o F1 da classe: como no validador, o F1 e calculado em 1.000 pontos de confianca e suavizado com
filtro de caixa de 10% antes do argmax (e assim que o Ultralytics escolhe o P e o R que reporta);
tambem se da o maximo sem suavizacao.

  C:/arma3-favela/venv/Scripts/python.exe pr_visdrone.py
Saidas: pr_visdrone.json, ../figuras/fig11_pr_visdrone.png
"""
import json
import os
import sys
from datetime import datetime

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(AQUI)
FIG = os.path.join(RES, "figuras")
sys.path.insert(0, AQUI)
from visdrone_preds import MODELOS, reportado  # noqa: E402

CURVAS = [("R", "R: 1,106 real images"), ("S-oblique-six s0", "S-oblique-six, zero-shot"),
          ("F-generic 10%", "F-generic 10%"), ("F-synthetic 10%", "F-synthetic 10%")]


def curva(run):
    from ultralytics.utils.metrics import ap_per_class
    d = np.load(os.path.join(AQUI, f"preds_visdrone_{run}.npz"), allow_pickle=False)
    tp = d["tp"][:, :1].astype(bool)
    conf = d["conf"].astype(np.float64)
    n_gt = int(d["n_gt"].sum())
    r = ap_per_class(tp, conf, np.zeros(len(conf)), np.zeros(n_gt))
    tp_f1, fp_f1, p, rc, f1, ap, _, p_curve, r_curve, f1_curve, x, prec_values = r
    # ponto de max F1 como o validador (suavizado) e sem suavizar
    from ultralytics.utils.metrics import smooth
    i_s = int(smooth(f1_curve.mean(0), 0.1).argmax())
    i_r = int(f1_curve.mean(0).argmax())
    # curva PR crua (sem envelope) para registro: precisao e recall acumulados na ordem de confianca
    o = np.argsort(-conf, kind="stable")
    tpc = np.cumsum(tp[o, 0])
    fpc = np.cumsum(~tp[o, 0])
    rec_crua = tpc / n_gt
    prec_crua = tpc / (tpc + fpc)
    return {"run": run, "AP50": round(float(ap[0, 0]), 4), "mAP50_reportado": reportado(run), "caixas_verdadeiras": n_gt,
            "predicoes": int(len(conf)),
            "max_f1_suavizado_como_validador": {"conf": round(float(x[i_s]), 4), "P": round(float(p_curve[0, i_s]), 4),
                                                "R": round(float(r_curve[0, i_s]), 4), "F1": round(float(f1_curve[0, i_s]), 4)},
            "max_f1_sem_suavizar": {"conf": round(float(x[i_r]), 4), "P": round(float(p_curve[0, i_r]), 4),
                                    "R": round(float(r_curve[0, i_r]), 4), "F1": round(float(f1_curve[0, i_r]), 4)},
            "em_conf_0.25": {"P": round(float(np.interp(0.25, x, p_curve[0])), 4), "R": round(float(np.interp(0.25, x, r_curve[0])), 4)},
            "_x_recall": x, "_prec_envelope": prec_values[0], "_rec_crua": rec_crua, "_prec_crua": prec_crua,
            "_p_curve": p_curve[0], "_r_curve": r_curve[0], "_i_s": i_s}


def figura(dados):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    AZUL, LARANJA, AGUA, CINZA, TINTA = "#2a78d6", "#eb6834", "#1baf7a", "#8a8a86", "#0b0b0b"
    plt.rcParams.update({"font.family": "Arial", "font.size": 7.5, "axes.edgecolor": "#555", "axes.linewidth": 0.6,
                         "xtick.color": "#333", "ytick.color": "#333"})
    estilo = {"R": (CINZA, "D"), "S-oblique-six s0": (LARANJA, "s"), "F-generic 10%": (AZUL, "o"), "F-synthetic 10%": (AGUA, "^")}
    # posicao do rotulo direto (recall, precisao), na area vazia a direita das curvas
    pos = {"R": (0.80, 0.78), "F-generic 10%": (0.80, 0.64), "F-synthetic 10%": (0.80, 0.50), "S-oblique-six s0": (0.21, 0.36)}
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)
    for nome, rotulo in CURVAS:
        if nome not in dados:
            continue
        c = dados[nome]
        cor, marcador = estilo[nome]
        x, y = c["_x_recall"], c["_prec_envelope"]
        ax.plot(x, y, color=cor, lw=1.6, zorder=3)
        m = c["max_f1_suavizado_como_validador"]
        ax.plot([m["R"]], [m["P"]], marker=marcador, ms=6, color=cor, mec="white", mew=0.8, zorder=5)
        ax.annotate(f"{rotulo}\nAP50 {c['AP50']:.3f}\nmax F1 at conf {m['conf']:.2f}: P {m['P']:.2f}, R {m['R']:.2f}",
                    xy=(m["R"], m["P"]), xytext=pos[nome], color=TINTA, fontsize=6.8, ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", color="#999", lw=0.6, shrinkA=0, shrinkB=4), zorder=6)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Recall (pedestrian and people merged, IoU 0.50)")
    ax.set_ylabel("Precision")
    ax.grid(color="#e4e4e2", lw=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.text(0.99, 0.97, "VisDrone-DET val, 548 images; marker = confidence that maximises F1", transform=ax.transAxes,
            ha="right", va="top", fontsize=6.5, color="#444")
    fig.tight_layout(pad=0.5)
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, "fig11_pr_visdrone.png"))
    plt.close(fig)


def main():
    dados = {}
    for nome, _ in CURVAS:
        run = MODELOS[nome]
        if os.path.exists(os.path.join(AQUI, f"preds_visdrone_{run}.npz")):
            dados[nome] = curva(run)
            c = dados[nome]
            print(f"{nome:<18} AP50 {c['AP50']:.4f} (reportado {c['mAP50_reportado']})  max F1: conf {c['max_f1_suavizado_como_validador']['conf']} "
                  f"P {c['max_f1_suavizado_como_validador']['P']} R {c['max_f1_suavizado_como_validador']['R']}")
    figura(dados)
    saida = {"protocolo": "VisDrone-DET val, 548 imagens, classe unica, imgsz 1280, conf 0,001, NMS IoU 0,7, max_det 300, IoU de acerto 0,50; "
                          "curva = envelope de precisao em 1.000 pontos de recall (ap_per_class do Ultralytics); ponto = conf que maximiza o F1 "
                          "(F1 em 1.000 pontos de conf, suavizado com filtro de caixa de 10%, como no validador)",
             "curvas": {n: {k: v for k, v in c.items() if not k.startswith("_")} |
                        {"curva_pr_envelope_101_pontos": {"recall": [round(float(r), 2) for r in np.linspace(0, 1, 101)],
                                                          "precisao": [round(float(np.interp(r, c["_x_recall"], c["_prec_envelope"])), 4)
                                                                       for r in np.linspace(0, 1, 101)]}}
                        for n, c in dados.items()},
             "figura": "06-resultados/figuras/fig11_pr_visdrone.png", "quando": datetime.now().isoformat(timespec="seconds")}
    with open(os.path.join(AQUI, "pr_visdrone.json"), "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
