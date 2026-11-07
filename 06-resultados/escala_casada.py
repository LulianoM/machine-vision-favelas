#!/usr/bin/env python3
"""
escala_casada.py: a metade da checagem 10.2 que faltava, no corpus corrigido (rodada 4).

O que a checagem pede: avaliar o modelo nadir no VisDrone com o alvo real na escala do alvo de treino,
casando o lado maior da caixa, como no piloto. O corpus de treino (ds_morro_4k) tem lado maior
mediano de 20,55 px, medido em resolucao nativa (alvo_por_split.json, "todos").

O detalhe que decide como casar. O validador do Ultralytics redimensiona TODA imagem para que o lado
maior valha imgsz, para cima ou para baixo (data/base.py, load_image). Entao reescalar os arquivos
do VisDrone e avaliar com o mesmo imgsz nao muda nada do que a rede ve: foi o que aconteceu no
piloto (visdrone_yolo_gsd a imgsz 640 contra visdrone_yolo a imgsz 640, a mesma escala na entrada da
rede). A escala da rede se escolhe pelo imgsz. Este script:

  1. calcula, so com os rotulos e o tamanho de cada imagem (nenhuma saida de modelo), o lado maior
     mediano das caixas de pessoa do VisDrone val NA ENTRADA DA REDE para cada imgsz multiplo de 32;
  2. escolhe o imgsz cuja mediana fica mais perto de 20,55 px (regra fixada antes de avaliar);
  3. avalia o s_nadir_4k e o r_pareado nesse imgsz (a razao de eficacia precisa dos dois no mesmo
     protocolo), com o avalia_sim2real.py de sempre.

  python escala_casada.py   ->  escala_casada.json, sim2real_s_nadir_4k_casada.json, sim2real_r_pareado_casada.json
"""
import glob
import json
import os
import statistics as st
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela")
VAL = os.path.join(RAIZ, "visdrone", "visdrone_yolo", "val")
VIS_YAML = os.path.join(RAIZ, "visdrone", "visdrone_yolo", "data.yaml")
DETECT = os.path.join(RAIZ, "blender", "runs", "detect")
AVALIA = os.path.join(os.path.dirname(AQUI), "03-blender", "scripts", "avalia_sim2real.py")
ALVO = json.load(open(os.path.join(AQUI, "alvo_por_split.json"), encoding="utf-8"))["ds_morro_4k"]["todos"]["lado_maior_med"]


def medidas():
    from PIL import Image
    L, A = [], []
    for p in sorted(glob.glob(os.path.join(VAL, "images", "*.jpg"))):
        W, H = Image.open(p).size
        lab = os.path.join(VAL, "labels", os.path.splitext(os.path.basename(p))[0] + ".txt")
        if not os.path.exists(lab):
            continue
        for ln in open(lab):
            _, _, _, w, h = map(float, ln.split())
            L.append((max(w * W, h * H), max(W, H)))
            A.append((w * W * h * H, max(W, H)))
    return L, A


def main():
    L, A = medidas()
    tab = {}
    for s in range(640, 1920 + 1, 32):
        tab[s] = {"lado_maior_med": round(st.median(l * s / m for l, m in L), 2),
                  "area_med": round(st.median(a * (s / m) ** 2 for a, m in A), 1)}
    escolhido = min(tab, key=lambda s: abs(tab[s]["lado_maior_med"] - ALVO))
    out = {"alvo_lado_maior_treino_px": ALVO, "caixas_visdrone_val": len(L),
           "imgsz_protocolo": 1280, "no_protocolo": tab[1280], "imgsz_casado": escolhido,
           "no_casado": tab[escolhido], "tabela": tab,
           "regra": "imgsz multiplo de 32 cuja mediana do lado maior na entrada da rede fica mais perto do alvo"}
    json.dump(out, open(os.path.join(AQUI, "escala_casada.json"), "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    print(f"alvo {ALVO} px; no protocolo (1280) {tab[1280]}; casado imgsz {escolhido} {tab[escolhido]}", flush=True)
    rc = 0
    for nome in ("s_nadir_4k", "r_pareado"):
        saida = os.path.join(AQUI, f"sim2real_{nome}_casada.json")
        if os.path.exists(saida):
            continue
        rc |= subprocess.call([sys.executable, AVALIA, "--weights", os.path.join(DETECT, nome, "weights", "best.pt"),
                               "--real", VIS_YAML, "--imgsz", str(escolhido), "--out", saida])
    return rc


if __name__ == "__main__":
    sys.exit(main())
