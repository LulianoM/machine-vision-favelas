#!/usr/bin/env python3
"""
bench_otimizacao.py: mede QUAL das otimizacoes de render paga, e se alguma delas estraga a imagem.

`07-blender/PLANO-OTIMIZACAO.md` lista tres suspeitas para os 176 s por imagem, ordenadas por
palpite e nenhuma medida em separado. Este script faz o A contra B que falta.

Duas coisas sao medidas em cada variante, e as duas importam:

  tempo      mediana de `render_s` no manifesto, descartando o primeiro quadro, que carrega a
             construcao da cena e nao e representativo.
  fidelidade as dez metricas de `teste_fidelidade.py` sobre um nadir isolado da mesma semente.
             Duas das otimizacoes mexem em coisa que aparece na imagem: encolher a caixa de ar
             muda contraste, meio-tom e B/R da sombra, e a poda de arvore muda a moldura de mata.
             Ganhar 30% de tempo e sair da faixa de fidelidade nao e ganho, e troca.

Por que nao confiar no palpite: o mesmo raciocinio de "isto aqui deve ser o caro" ja produziu
neste projeto um normalizador com fator 2 errado, um ramo de telhado inalcancavel e um filtro que
descartava 93% dos fios. Medicao com alvo declarado e o que pegou os tres.

Uso:
  python bench_otimizacao.py                      # todas as variantes, 8 quadros cada
  python bench_otimizacao.py --quadros 4          # mais barato, com mais ruido
  python bench_otimizacao.py --so base,otimizado
"""
import argparse
import json
import os
import statistics as st
import subprocess
import sys
import time

SCR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
RES = os.path.abspath(os.path.join(SCR, "..", "..", "06-resultados"))
BLENDER = os.path.join("C:" + os.sep, "Program Files (x86)", "Steam", "steamapps",
                       "common", "Blender", "blender.exe")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
BENCH = os.path.join(RAIZ, "bench_otim")

# (nome, argumentos extras). `base` e o estado atual, e e contra ele que todo o resto e comparado.
VARIANTES = [
    ("base", []),
    ("persistente", ["--persistente"]),
    ("nevoa40", ["--nevoa-folga", "40"]),
    ("podar", ["--podar-arvores"]),
    ("otimizado", ["--otimizado"]),
]


def roda(nome, extra, quadros, samples, res, log):
    out = os.path.join(BENCH, nome)
    man = os.path.join(out, "manifest.jsonl")
    if not os.path.exists(man):
        cmd = [BLENDER, "-b", "--python", os.path.join(SCR, "gen_morro.py"), "--",
               "--out", out, "--dataset", str(quadros), "--samples", str(samples),
               "--res", str(res[0]), str(res[1]), "--people", "16", "34", "--pool", "6",
               "--seed", "21", "--climas", "todos"] + extra
        log.write("\n# " + " ".join(cmd) + "\n")
        log.flush()
        t0 = time.time()
        rc = subprocess.call(cmd, stdout=log, stderr=subprocess.STDOUT, cwd=RAIZ)
        log.write(f"# rc={rc} em {time.time() - t0:.0f} s\n")
        if rc != 0:
            return None
    recs = [json.loads(l) for l in open(man, encoding="utf-8")]
    # o primeiro quadro carrega a construcao da cena: fora da conta
    ts = [r["render_s"] for r in recs][1:]
    if not ts:
        return None
    return dict(nome=nome, quadros=len(recs), mediana=st.median(ts),
                minimo=min(ts), maximo=max(ts),
                caixas=sum(r["n_caixas"] for r in recs),
                nadir=os.path.join(out, "images", "train",
                                   recs[0]["img"].replace(".png", "")) )


ap = argparse.ArgumentParser()
ap.add_argument("--quadros", type=int, default=8)
ap.add_argument("--samples", type=int, default=96)
ap.add_argument("--res", type=int, nargs=2, default=[3840, 2160])
ap.add_argument("--so", default=None, help="nomes de variante separados por virgula")
a = ap.parse_args()

os.makedirs(BENCH, exist_ok=True)
alvos = [v for v in VARIANTES if not a.so or v[0] in a.so.split(",")]
saida = []
with open(os.path.join(BENCH, "bench.log"), "a", encoding="utf-8", buffering=1) as log:
    for nome, extra in alvos:
        print(f"[bench] {nome} {' '.join(extra) or '(sem flag)'}", flush=True)
        r = roda(nome, extra, a.quadros, a.samples, a.res, log)
        if r is None:
            print(f"[bench] {nome} FALHOU, ver {os.path.join(BENCH, 'bench.log')}")
            continue
        saida.append(r)
        print(f"[bench]   mediana {r['mediana']:.1f} s ({r['minimo']:.0f} a {r['maximo']:.0f}), "
              f"{r['caixas']} caixas", flush=True)

if not saida:
    sys.exit("nenhuma variante concluiu")

base = next((r for r in saida if r["nome"] == "base"), None)
print(f"\n{'variante':<14}{'mediana s':>11}{'faixa':>16}{'ganho':>9}{'caixas':>9}")
print("-" * 60)
for r in saida:
    g = ""
    if base and r["nome"] != "base":
        g = f"{100 * (base['mediana'] - r['mediana']) / base['mediana']:+.0f}%"
    print(f"{r['nome']:<14}{r['mediana']:>11.1f}"
          f"{str(round(r['minimo'])) + ' a ' + str(round(r['maximo'])):>16}{g:>9}"
          f"{r['caixas']:>9}")

print("\nA contagem de caixas tem de ficar PARECIDA entre as variantes. Se a poda de arvore ou a")
print("caixa de ar mudarem o numero de alvos anotados, elas mexeram na cena e nao so no custo,")
print("e ai o ganho de tempo nao e comparavel.")
print("\nFalta a fidelidade: rodar teste_fidelidade.py --img sobre um nadir de cada variante.")
print("Encolher a nevoa mexe em contraste, meio-tom e B/R da sombra, que sao tres das dez.")

json.dump(saida, open(os.path.join(RES, "bench_otimizacao.json"), "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print(f"\ngravado {os.path.join(RES, 'bench_otimizacao.json')}")
