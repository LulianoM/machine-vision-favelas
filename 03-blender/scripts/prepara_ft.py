#!/usr/bin/env python3
"""
prepara_ft.py: fatias do VisDrone para o ajuste fino com pouco dado real (secao 9.4 do artigo).

Desenho, fixado antes de rodar:
  - sel:  5% do treino do VisDrone (324 imagens), so para escolher o melhor peso durante o treino.
          O best.pt dos bracos reais anteriores foi escolhido na propria validacao do VisDrone,
          que e o conjunto de teste; aqui a escolha e feita fora dele.
  - ft05: outros 5% (324 imagens); ft10: 10% (647), contendo o ft05 inteiro, para a curva ser
          aninhada e a diferenca entre os dois pontos ser so o volume.
  - teste: a validacao do VisDrone inteira (548 imagens), a mesma de todos os outros numeros.
Sorteio com semente fixa, sobre a lista ordenada de nomes. Imagens por hardlink (sem copiar 1 GB).
"""
import json
import os
import random
import shutil

VIS = os.path.join("C:" + os.sep, "arma3-favela", "visdrone")
SRC = os.path.join(VIS, "visdrone_yolo", "train")
OUT = os.path.join(VIS, "ft")
SEMENTE = 2609


def liga(src, dst):
    if os.path.exists(dst):
        return
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def main():
    nomes = sorted(os.path.splitext(n)[0] for n in os.listdir(os.path.join(SRC, "images")))
    n = len(nomes)
    r = random.Random(SEMENTE)
    ordem = nomes[:]
    r.shuffle(ordem)
    k5, k10 = round(0.05 * n), round(0.10 * n)
    fatias = {"sel": ordem[:k5], "ft05": ordem[k5:2 * k5], "ft10": ordem[k5:k5 + k10]}
    ext = {os.path.splitext(x)[0]: os.path.splitext(x)[1] for x in os.listdir(os.path.join(SRC, "images"))}
    for nome, lista in fatias.items():
        for sub in ("images", "labels"):
            os.makedirs(os.path.join(OUT, nome, sub), exist_ok=True)
        for b in lista:
            liga(os.path.join(SRC, "images", b + ext[b]), os.path.join(OUT, nome, "images", b + ext[b]))
            lb = os.path.join(SRC, "labels", b + ".txt")
            if os.path.exists(lb):
                liga(lb, os.path.join(OUT, nome, "labels", b + ".txt"))
    for nome in ("ft05", "ft10"):
        with open(os.path.join(OUT, nome + ".yaml"), "w", encoding="utf-8") as f:
            f.write(f"path: {OUT.replace(os.sep, '/')}\ntrain: {nome}/images\nval: sel/images\n"
                    "names:\n  0: pessoa\n")
    resumo = {k: len(v) for k, v in fatias.items()} | {"treino_total": n, "semente": SEMENTE,
              "ft05_contido_em_ft10": set(fatias["ft05"]) <= set(fatias["ft10"]),
              "sel_disjunto": not (set(fatias["sel"]) & set(fatias["ft10"]))}
    with open(os.path.join(OUT, "fatias.json"), "w", encoding="utf-8") as f:
        json.dump(resumo, f, indent=1)
    print(resumo)


if __name__ == "__main__":
    main()
