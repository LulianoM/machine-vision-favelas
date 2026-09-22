#!/usr/bin/env python3
"""
mede_oclusao.py: fracao de pessoas colocadas na cena que sobrevivem ao filtro de visibilidade.

A secao 7.4 do artigo afirmava a estatistica (mediana 0,65, p10 0,44, p90 0,75 sobre 48 quadros)
sem arquivo de origem, o que viola a nota de proveniencia do topo da propria secao. Este script
le o manifesto do corpus e grava o CSV que faltava.

Uso:
  python mede_oclusao.py C:/arma3-favela/blender/ds_morro_4k
"""
import json
import os
import statistics as st
import sys

raiz = sys.argv[1]
recs = [json.loads(l) for l in open(os.path.join(raiz, "manifest.jsonl"), encoding="utf-8")]
fr = [r["n_caixas"] / r["n_pessoas"] for r in recs if r["n_pessoas"]]
fr_s = sorted(fr)
saida = dict(corpus=os.path.basename(raiz), quadros=len(fr),
             pessoas=sum(r["n_pessoas"] for r in recs), caixas=sum(r["n_caixas"] for r in recs),
             mediana=round(st.median(fr), 3), p10=round(fr_s[len(fr_s) // 10], 3),
             p90=round(fr_s[9 * len(fr_s) // 10], 3))
print(saida)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oclusao_" + saida["corpus"] + ".json")
json.dump(saida, open(out, "w", encoding="utf-8"), indent=1)
print("gravado", out)
