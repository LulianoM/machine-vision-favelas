#!/usr/bin/env python3
"""
holdout_criterio.py: aplica o criterio pre-declarado do teste de arma inedita (secao 11.5 do artigo)
a saida de confusao_armado.py no corpus ds_armado_75_inedita (etapa B2 da rodada 3).

Criterio (declarado antes da rodada 3): se o recall de armada nos dois modelos ineditos ficar abaixo
de 4/5 do recall nos cinco modelos de treino, a afirmacao de que o detector reconhece "arma", e nao
os cinco modelos que viu, e retirada. Recall aqui = caixas do grupo chamadas de armada / caixas do
grupo, somadas no grupo (nao media das taxas por modelo). Os grupos saem das tabelas ARMAS e
ARMAS_INEDITAS de objetos_alongados.py, lidas por ast porque o modulo importa bpy.

  python holdout_criterio.py [--entrada holdout_armas_armado_75.json] [--saida holdout_armas_criterio.json]

Intervalos de 95%: Wilson por grupo e Katz (log) para a razao. Ignoram o agrupamento das caixas
por quadro (50 quadros), entao sao otimistas.
"""
import argparse
import ast
import json
import math
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(AQUI, "..", "07-blender", "scripts", "objetos_alongados.py")
LIMIAR = 0.8
Z = 1.959964


def tabela(nome):
    for no in ast.parse(open(OBJ, encoding="utf-8").read()).body:
        if isinstance(no, ast.Assign) and any(getattr(t, "id", None) == nome for t in no.targets):
            return [el.elts[0].value for el in no.value.elts]
    raise KeyError(nome)


def wilson(k, n):
    p = k / n
    c = (p + Z * Z / (2 * n)) / (1 + Z * Z / n)
    m = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / (1 + Z * Z / n)
    return [round(c - m, 4), round(c + m, 4)]


def grupo(por_tipo, modelos):
    k = sum(por_tipo[t]["armada"] for t in modelos if t in por_tipo)
    n = sum(por_tipo[t]["n"] for t in modelos if t in por_tipo)
    return dict(modelos=modelos, armada=k, n=n, recall=round(k / n, 4), ic95=wilson(k, n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", default=os.path.join(AQUI, "holdout_armas_armado_75.json"))
    ap.add_argument("--saida", default=os.path.join(AQUI, "holdout_armas_criterio.json"))
    a = ap.parse_args()
    d = json.load(open(a.entrada, encoding="utf-8"))
    pt = d["por_tipo"]
    v, i = grupo(pt, tabela("ARMAS")), grupo(pt, tabela("ARMAS_INEDITAS"))
    razao = (i["armada"] / i["n"]) / (v["armada"] / v["n"])
    # Katz: ep(ln razao) = raiz(1/k1 - 1/n1 + 1/k2 - 1/n2)
    ep = math.sqrt(1 / i["armada"] - 1 / i["n"] + 1 / v["armada"] - 1 / v["n"])
    out = dict(entrada=os.path.basename(a.entrada), pesos=d.get("pesos"), protocolo=d.get("protocolo"),
               imagens=d.get("imagens"), conf=d.get("conf"),
               criterio=f"retirar se recall_ineditas < {LIMIAR} x recall_vistas",
               vistas=v, ineditas=i, razao=round(razao, 4),
               razao_ic95=[round(razao * math.exp(-Z * ep), 4), round(razao * math.exp(Z * ep), 4)],
               limiar=LIMIAR, retirar=razao < LIMIAR,
               por_modelo={t: pt[t]["chamada_de_armada"] for t in v["modelos"] + i["modelos"] if t in pt},
               nota="IC ignora o agrupamento das caixas por quadro")
    with open(a.saida, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f"vistas   {v['armada']}/{v['n']} = {v['recall']:.3f}  IC95 {v['ic95']}")
    print(f"ineditas {i['armada']}/{i['n']} = {i['recall']:.3f}  IC95 {i['ic95']}")
    print(f"razao {razao:.3f}  IC95 {out['razao_ic95']}  limiar {LIMIAR}  -> "
          + ("RETIRAR a afirmacao" if out["retirar"] else "afirmacao mantida"))


if __name__ == "__main__":
    main()
