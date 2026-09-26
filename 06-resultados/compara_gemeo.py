#!/usr/bin/env python3
"""
compara_gemeo.py: compara as matrizes de confusao de imagem inteira dos tres modelos armados
(saidas de confusao_armado.py no split val de cada corpus), para as secoes 9.5 e 11.5 do artigo.

  armado_75   75 m, gerador anterior a 22/09 (objeto em pose de tiro em 42% dos casos; sem --fio-gsd,
              --laje, --amostra-no-quadro; 96 samples)
  armado_35   35 m, --porte-realista --fio-gsd --laje 0.75 --amostra-no-quadro, 64 samples
  armado_75g  75 m, o comando do armado_35 mudando so a altura (gemeo, rodada 3)

Para cada taxa "chamada de armada" (pessoa armada, desarmada, com objeto): contagem, IC 95% de Wilson
e teste z de duas proporcoes em dois contrastes: gemeo contra 35 m (so a altitude muda) e 75 m
original contra gemeo (mudam as flags do gerador, a 75 m). Tambem d' = z(acerto) - z(alarme falso),
com "chamar de armada" como decisao, que separa discriminacao de vies. Os testes ignoram o
agrupamento das pessoas por quadro (24 a 35 quadros por val), entao sao otimistas.

  python compara_gemeo.py   ->  gemeo_75_35.json
"""
import json
import math
import os
from statistics import NormalDist

AQUI = os.path.dirname(os.path.abspath(__file__))
MODELOS = ["armado_75", "armado_35", "armado_75g"]
CONTRASTES = {"altitude: armado_75g -> armado_35": ("armado_75g", "armado_35"),
              "gerador a 75 m: armado_75 -> armado_75g": ("armado_75", "armado_75g")}
N = NormalDist()


def wilson(k, n, z=1.959964):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    m = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return [round(c - m, 4), round(c + m, 4)]


def carrega(nome):
    d = json.load(open(os.path.join(AQUI, f"confusao_{nome}.json"), encoding="utf-8"))
    taxas = {}
    for c, v in d["taxa_por_classe_real"].items():
        k = round(v["armada"] * v["n"])
        taxas[c] = dict(chamada_armada=k, n=v["n"], taxa=round(k / v["n"], 4), ic95=wilson(k, v["n"]))
    hit = taxas["armada"]["taxa"]
    dl = {c: round(N.inv_cdf(hit) - N.inv_cdf(taxas[c]["taxa"]), 3) for c in ("desarmada", "objeto")}
    vi = d.get("val_imagem_inteira") or {}
    # precisao de armada: acertos / todas as caixas chamadas de armada (inclui as que nao casam com
    # nenhuma pessoa anotada)
    chamadas = sum(t["chamada_armada"] for t in taxas.values()) + (d.get("predicoes_sem_par") or {}).get("armada", 0)
    return dict(imagens=d.get("imagens"), split=d.get("split"), taxas=taxas, d_linha_armada_contra=dl,
                precisao_armada=round(taxas["armada"]["chamada_armada"] / chamadas, 4),
                mAP50_imagem_inteira=vi.get("mAP50"))


def contraste(a, b):
    out = {}
    for c in ("armada", "desarmada", "objeto"):
        k1, n1 = a["taxas"][c]["chamada_armada"], a["taxas"][c]["n"]
        k2, n2 = b["taxas"][c]["chamada_armada"], b["taxas"][c]["n"]
        p = (k1 + k2) / (n1 + n2)
        ep = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
        z = (k2 / n2 - k1 / n1) / ep
        out[c] = dict(de=round(k1 / n1, 4), para=round(k2 / n2, 4), dif_pontos=round(100 * (k2 / n2 - k1 / n1), 1),
                      z=round(z, 2), p_bilateral=round(2 * (1 - N.cdf(abs(z))), 3))
    return out


def main():
    m = {n: carrega(n) for n in MODELOS}
    comp = {k: contraste(m[a], m[b]) for k, (a, b) in CONTRASTES.items()}
    out = dict(protocolo="imagem inteira, conf 0,25, casamento 1:1 IoU >= 0,5, split val de cada corpus",
               modelos=m, contrastes=comp,
               nota="z e IC ignoram o agrupamento por quadro; taxas = fracao chamada de pessoa_armada")
    with open(os.path.join(AQUI, "gemeo_75_35.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    for n, v in m.items():
        t = v["taxas"]
        print(f"{n:<11} armada {t['armada']['taxa']:.3f}  desarmada {t['desarmada']['taxa']:.3f}  "
              f"objeto {t['objeto']['taxa']:.3f}  d'(obj) {v['d_linha_armada_contra']['objeto']:.2f}  "
              f"d'(desarm) {v['d_linha_armada_contra']['desarmada']:.2f}  precisao {v['precisao_armada']:.3f}  "
              f"mAP50 {v['mAP50_imagem_inteira']}")
    for k, v in comp.items():
        print(k)
        for c, r in v.items():
            print(f"   {c:<10} {r['de']:.3f} -> {r['para']:.3f}  ({r['dif_pontos']:+.1f} pts, z {r['z']}, p {r['p_bilateral']})")


if __name__ == "__main__":
    main()
