#!/usr/bin/env python3
"""
figuras_mpl.py: duas figuras do artigo desenhadas com matplotlib (30/09, refino do artigo).

  fig9_desenho_experimental.png  o desenho do experimento: gerador -> corpora (por camera e
                                 altitude) -> modelos -> onde cada um e avaliado. Nao tem numero
                                 medido; so contagens de quadros que ja estao no texto.
  fig10_ajuste_fino.png          mAP50 no VisDrone-DET val contra o numero de imagens reais de
                                 treino, para o inicio generico (COCO), o inicio sintetico
                                 (S-oblique-six) e o treino conjunto; tres sementes onde existem;
                                 R (1.106 imagens, 60 epocas) como teto. Todo numero e lido dos
                                 JSON desta pasta (sim2real_*.json), nunca digitado aqui.

Paleta: os tres primeiros slots da paleta de referencia do skill dataviz, validados para todos os
pares (validate_palette.js, 30/09): azul #2a78d6, laranja #eb6834, verde-agua #1baf7a; cada serie
tem marcador proprio, e os valores vao escritos ao lado dos pontos, para que a identidade nao
dependa so da cor (o verde-agua fica abaixo de 3:1 de contraste no fundo claro).

  C:/arma3-favela/venv/Scripts/python.exe figuras_mpl.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "figuras")
AZUL, LARANJA, AGUA, CINZA, TINTA = "#2a78d6", "#eb6834", "#1baf7a", "#8a8a86", "#0b0b0b"
plt.rcParams.update({"font.family": "Arial", "font.size": 7.5, "axes.edgecolor": "#555",
                     "axes.linewidth": 0.6, "xtick.color": "#333", "ytick.color": "#333"})
NL = chr(10)


def map50(nome, conjunto="real"):
    d = json.load(open(os.path.join(AQUI, f"sim2real_{nome}.json"), encoding="utf-8"))
    for r in d["resultados"]:
        if r.get("conjunto", "real") == conjunto:
            return r["metrics/mAP50(B)"]
    raise KeyError(nome)


def fig_ajuste():
    x = {0: 0, 324: 1, 647: 2, 1106: 3}
    gen = {324: [map50("ft05_coco"), map50("ft05_coco_sd1"), map50("ft05_coco_sd2")], 647: [map50("ft10_coco")]}
    sin = {0: [map50("s_oblvar"), map50("s_oblvar_sd1"), map50("s_oblvar_sd2")],
           324: [map50("ft05_sint"), map50("ft05_sint_sd1"), map50("ft05_sint_sd2")], 647: [map50("ft10_sint")]}
    jun = {324: [map50("misto05")], 647: [map50("misto10")]}
    teto = map50("r_pareado")

    fig, ax = plt.subplots(figsize=(3.35, 2.8), dpi=300)
    ax.axhline(teto, color=CINZA, lw=0.8, ls=(0, (3, 2)), zorder=1)
    ax.text(x[0] - 0.22, teto + 0.018, f"R: 1,106 real images, 60 epochs, {teto:.3f}", ha="left",
            va="bottom", color="#444")
    ax.plot([x[1106]], [teto], marker="D", ms=4.5, color=CINZA, zorder=3)

    def serie(dados, cor, marcador, nome, pos):
        xs = sorted(dados)
        ax.plot([x[k] for k in xs], [dados[k][0] for k in xs], color=cor, lw=1.6, marker=marcador, ms=5,
                zorder=4, label=nome)
        for k in xs:
            for extra in dados[k][1:]:
                ax.plot([x[k]], [extra], marker=marcador, ms=4, mfc="white", mec=cor, mew=0.9, zorder=3)
            dx, dy, ha = pos[k]
            ax.text(x[k] + dx, dados[k][0] + dy, f"{dados[k][0]:.3f}", color=TINTA, ha=ha, va="center")

    serie(gen, AZUL, "o", "Generic start (COCO)", {324: (0, 0.045, "center"), 647: (0, 0.045, "center")})
    serie(jun, AGUA, "^", "Joint: synthetic tiles and real images together",
          {324: (-0.1, 0.012, "right"), 647: (0.1, 0.014, "left")})
    serie(sin, LARANJA, "s", "Synthetic start (S-oblique-six)",
          {0: (0.1, 0.0, "left"), 324: (0.1, -0.032, "left"), 647: (0.1, -0.028, "left")})
    ax.text(x[0] + 0.1, sin[0][0] - 0.05, "zero-shot", ha="left", va="center", color=TINTA)

    ax.set_xticks([0, 1, 2, 3])
    ax.set_xticklabels(["0", "324" + NL + "(5%)", "647" + NL + "(10%)", "1,106"])
    ax.set_xlim(-0.3, 3.35)
    ax.set_ylim(0, 0.72)
    ax.set_yticks([0, 0.2, 0.4, 0.6])
    ax.set_xlabel("Real training images from VisDrone-DET train")
    ax.set_ylabel("mAP50 on VisDrone-DET val")
    ax.grid(axis="y", color="#ddd", lw=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(loc="lower right", frameon=False, fontsize=6.6, handlelength=1.6, borderaxespad=0.2)
    fig.tight_layout(pad=0.4)
    fig.savefig(os.path.join(OUT, "fig10_ajuste_fino.png"))
    plt.close(fig)


def caixa(ax, x, y, w, h, titulo, corpo="", cor="#f4f4f2", borda="#555", tam=6.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.006,rounding_size=0.012",
                                fc=cor, ec=borda, lw=0.7, zorder=2))
    if corpo:
        n_tit = titulo.count(NL) + 1
        ax.text(x + w / 2, y + h - 0.022, titulo, ha="center", va="top", fontsize=tam, fontweight="bold",
                zorder=3, linespacing=1.15)
        ax.text(x + w / 2, y + h - 0.022 - 0.031 * n_tit - 0.014, corpo, ha="center", va="top",
                fontsize=tam - 0.7, zorder=3, linespacing=1.3)
    else:
        ax.text(x + w / 2, y + h / 2, titulo, ha="center", va="center", fontsize=tam, fontweight="bold",
                zorder=3, linespacing=1.25)


def seta(ax, x0, y0, x1, y1, cor="#444"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=cor, lw=0.7, shrinkA=0, shrinkB=0, mutation_scale=7))


def L(*linhas):
    return NL.join(linhas)


def fig_desenho():
    """Fluxo em quatro colunas com setas so horizontais (e um cotovelo pela calha entre colunas),
    para nenhuma seta cruzar texto; refeito em 30/09 depois de o autor apontar a versao anterior
    como mal formatada (setas diagonais sobre o texto e linhas saindo das caixas)."""
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    XA, WA = 0.01, 0.185    # gerador
    XB, WB = 0.245, 0.265   # corpora
    XC, WC = 0.56, 0.175    # detectores
    XD, WD = 0.785, 0.205   # avaliacao
    R1 = (0.79, 0.16)       # (base, altura) nadir
    R2 = (0.575, 0.19)      # obliquo
    R3 = (0.24, 0.31)       # tres classes
    R4 = (0.02, 0.15)       # dado real
    mid = lambda r: r[0] + r[1] / 2  # noqa: E731
    TIT, CORPO = 6.6, 5.9

    def bloco(x, y, w, h, titulo, corpo="", cor="#f7f7f5"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.004,rounding_size=0.012",
                                    fc=cor, ec="#555", lw=0.7, zorder=2))
        n_tit = titulo.count(NL) + 1
        if corpo:
            ax.text(x + w / 2, y + h - 0.02, titulo, ha="center", va="top", fontsize=TIT, fontweight="bold",
                    zorder=3, linespacing=1.15)
            ax.text(x + w / 2, y + h - 0.02 - 0.03 * n_tit - 0.016, corpo, ha="center", va="top",
                    fontsize=CORPO, zorder=3, linespacing=1.32)
        else:
            ax.text(x + w / 2, y + h / 2, titulo, ha="center", va="center", fontsize=TIT, fontweight="bold",
                    zorder=3, linespacing=1.25)

    def cabeca(x, w, txt):
        ax.text(x + w / 2, 0.978, txt, ha="center", va="center", fontsize=6.6, style="italic")

    def seta_h(x0, x1, y):
        seta(ax, x0, y, x1, y)

    cabeca(XA, WA, "Generator")
    bloco(XA, R3[0], WA, R1[0] + R1[1] - R3[0], "Procedural generator",
          L("Blender, deterministic seed", "", "settlement, alleys,", "stacked storeys", "rooftop clutter, cabling",
            "", "six illumination regimes", "", "MakeHuman figures", "five weapons,", "nine confusable objects", "",
            "boxes projected", "from geometry"), cor="#eef3fb")

    cabeca(XB, WB, "Synthetic corpora (tiles at native scale)")
    bloco(XB, R1[0], WB, R1[1], "Nadir, 150 m, one class",
          L("corpus of record: 180 frames,", "one settlement", "six settlements: 180 frames"))
    bloco(XB, R2[0], WB, R2[1], "Oblique, one class",
          L("S-oblique: 180 frames, one settlement,", "pitch 26 to 52 degrees",
            "S-oblique-six: 180 frames,", "six settlements, pitch 45 to 56"))
    bloco(XB, R3[0], WB, R3[1], L("Three classes: armed, unarmed,", "carrying a confusable object"),
          L("75 m: 200 frames", "35 m: 200 frames, realistic carrying", "twin of 35 m at 75 m: 200 frames",
            "twin of 35 m at 150 m: 200 frames", "new frames at 35 and 75 m: 80 each"), cor="#fbf1ec")
    bloco(XB, R4[0], WB, R4[1], "VisDrone-DET train (real)",
          L("1,106 images for R", "slices of 5% and 10% for fine-tuning"), cor="#eef8f3")
    for r in (R1, R2, R3):
        seta_h(XA + WA, XB, mid(r))

    cabeca(XC, WC, "Detectors (YOLO11s)")
    bloco(XC, R1[0], WC, R1[1], L("S-nadir-150", "S-nadir-150-six"))
    bloco(XC, R2[0], WC, R2[1], L("S-oblique", "S-oblique-six"))
    bloco(XC, R3[0], WC, R3[1], L("S-nadir-75", "S-nadir-35", "and its twins"), cor="#fbf1ec")
    bloco(XC, R4[0], WC, R4[1], L("R (ceiling)", "F-generic, F-synthetic,", "F-joint"), cor="#eef8f3")
    for r in (R1, R2, R3, R4):
        seta_h(XB + WB, XC, mid(r))

    cabeca(XD, WD, "Evaluation")
    bloco(XD, R2[0], WD, R1[0] + R1[1] - R2[0], "Real test set",
          L("VisDrone-DET val,", "548 images, one class", "", "efficacy =", "mAP50(S) / mAP50(R)"), cor="#eef8f3")
    bloco(XD, R3[0], WD, R3[1], L("Synthetic validation", "and new frames"),
          L("rate at which each class", "is called armed", "d-prime", "unseen-weapon test"), cor="#fbf1ec")
    seta_h(XC + WC, XD, mid(R1))
    seta_h(XC + WC, XD, mid(R2))
    seta_h(XC + WC, XD, mid(R3))
    # R e os modelos de ajuste fino vao ao mesmo conjunto de teste real: cotovelo pela calha
    xg = XC + WC + (XD - XC - WC) / 2
    ax.plot([XC + WC, xg, xg], [mid(R4), mid(R4), R2[0] + 0.035], color="#444", lw=0.7, zorder=1)
    seta_h(xg, XD, R2[0] + 0.035)

    fig.savefig(os.path.join(OUT, "fig9_desenho_experimental.png"), bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fig_ajuste()
    fig_desenho()
    for f in ("fig9_desenho_experimental.png", "fig10_ajuste_fino.png"):
        p = os.path.join(OUT, f)
        print(f, round(os.path.getsize(p) / 1024), "KB")
