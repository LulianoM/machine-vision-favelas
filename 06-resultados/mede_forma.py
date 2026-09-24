#!/usr/bin/env python3
"""
mede_forma.py: forma e tamanho do alvo (h/w e area em pixel, medianas) por corpus, por classe e,
quando o manifest traz o pitch da camera, por faixa de pitch; e as contagens de instancia.

E o comando por tras de tres numeros do artigo: a forma realizada pelo braco obliquo (secao 8.2),
a dependencia da forma com o pitch que calibrou o braco combinado (secao 9.3) e as contagens do
corpus armado (secao 9.5). Rotulos YOLO da imagem inteira, sem ladrilho (ladrilho com sobreposicao
conta a mesma pessoa mais de uma vez).

Uso: python mede_forma.py   ->  forma_corpora.json
"""
import glob
import json
import os
import statistics as st
from collections import defaultdict

RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
CORPORA = ["ds_morro_4k", "ds_variedade", "ds_morro_obl", "ds_oblvar", "ds_armado_75",
           "ds_armado_35", "ds_armado_75g", "ds_armado_75_inedita"]
NOMES = {0: "armada", 1: "desarmada", 2: "objeto"}


def resumo(rows):
    return {"n": len(rows), "h_w": round(st.median(r[1] for r in rows), 2),
            "area_px2": round(st.median(r[2] for r in rows)),
            "w_px": round(st.median(r[3] for r in rows), 1), "h_px": round(st.median(r[4] for r in rows), 1)}


def main():
    out = {}
    for ds in CORPORA:
        d = os.path.join(RAIZ, ds)
        if not os.path.exists(os.path.join(d, "manifest.jsonl")):
            continue
        man = {}
        for ln in open(os.path.join(d, "manifest.jsonl"), encoding="utf-8"):
            if ln.strip():
                r = json.loads(ln)
                man[os.path.splitext(r["img"])[0]] = r
        rows = []
        for f in glob.glob(os.path.join(d, "labels", "*", "*.txt")):
            b = os.path.splitext(os.path.basename(f))[0]
            r = man.get(b, {})
            W, H = r.get("w", 3840), r.get("h", 2160)
            for ln in open(f):
                c, cx, cy, w, h = map(float, ln.split())
                rows.append((int(c), (h * H) / (w * W), w * W * h * H, w * W, h * H, r.get("pitch")))
        if not rows:
            continue
        item = {"imagens": len(man), "todas": resumo(rows),
                "por_classe": {NOMES[c]: resumo([x for x in rows if x[0] == c])
                               for c in sorted({x[0] for x in rows})}}
        if any(x[5] is not None and x[5] > 10 for x in rows):
            faixas = defaultdict(list)
            for x in rows:
                faixas[int(x[5] // 5 * 5)].append(x)
            item["por_pitch"] = {f"{k}-{k + 5}": {"todas": resumo(v),
                                 "desarmada": resumo([x for x in v if x[0] == 1]) if any(x[0] == 1 for x in v) else None}
                                 for k, v in sorted(faixas.items())}
        out[ds] = item
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "forma_corpora.json"), "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    for ds, it in out.items():
        print(ds, it["imagens"], "imgs", it["todas"])


if __name__ == "__main__":
    main()
