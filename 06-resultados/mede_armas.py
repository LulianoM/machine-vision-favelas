#!/usr/bin/env python3
"""
mede_armas.py: caixa envolvente de cada malha de arma do gerador (comprimento, largura e altura
em metros, no referencial local da arma: +X e o cano, Y a largura, Z a altura) e a pegada em
pixels nos tres GSDs do artigo (4,88, 2,44 e 1,14 cm/px, isto e, 150, 75 e 35 m em 4K).

E o item 1 de 08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md: a 5.1 do artigo so tinha o
comprimento registrado (0,92 m etc.), e a largura e a altura das malhas nao estavam em lugar nenhum.
A geometria de cada arma e deterministica (o sorteio em objetos_alongados.py so escolhe material);
o script constroi cada malha com varias sementes e confere que a caixa nao muda.

Roda DENTRO do Blender headless, porque objetos_alongados.py constroi as malhas com bpy:

  "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Blender\\blender.exe" -b --python 06-resultados/mede_armas.py

Grava armas_malhas.json e armas_malhas.md ao lado deste script. Mede tambem as duas armas ineditas
(so teste) e, para contraste, os nove objetos confundiveis, com a mesma convencao.
"""
import json
import os
import random
import statistics as st
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(AQUI, "..", "07-blender", "scripts")))

import bpy  # noqa: E402
import objetos_alongados as OA  # noqa: E402

GSD = [("150 m", 4.88), ("75 m", 2.44), ("35 m", 1.14)]  # cm/px, gsd_zoom.md
SEMENTES = 12


def extensao(o):
    xs = [v.co.x for v in o.data.vertices]
    ys = [v.co.y for v in o.data.vertices]
    zs = [v.co.z for v in o.data.vertices]
    return dict(x_min=min(xs), x_max=max(xs), comprimento=max(xs) - min(xs),
                largura=max(ys) - min(ys), altura=max(zs) - min(zs), vertices=len(xs))


def mede(nome, fn, M, deterministico=True):
    """deterministico=True exige que as SEMENTES deem a mesma caixa (armas: o sorteio so escolhe material).
    Os objetos confundiveis sorteiam o comprimento, entao para eles a caixa sai como mediana e faixa."""
    caixas, registrados = [], []
    for s in range(SEMENTES):
        rng = random.Random(1000 + s)
        o, comp = fn(f"_med_{nome}_{s}", rng, M)
        registrados.append(round(comp, 3))
        caixas.append(extensao(o))
        bpy.data.objects.remove(o, do_unlink=True)
    varia = {k: max(c[k] for c in caixas) - min(c[k] for c in caixas) for k in ("comprimento", "largura", "altura")}
    if deterministico:
        assert len(set(registrados)) == 1, (nome, registrados)
        assert max(varia.values()) < 1e-9, (nome, varia)
    c = {k: st.median(x[k] for x in caixas) for k in ("comprimento", "largura", "altura", "x_min", "x_max")}
    comp_reg = st.median(registrados)
    px = {}
    for alt, gsd in GSD:
        m_por_px = gsd / 100.0
        px[alt] = dict(gsd_cm_px=gsd,
                       comprimento_px=round(c["comprimento"] / m_por_px, 1),
                       largura_px=round(c["largura"] / m_por_px, 1),
                       altura_px=round(c["altura"] / m_por_px, 1),
                       comprimento_registrado_px=round(comp_reg / m_por_px, 1))
    return dict(comprimento_registrado_m=round(comp_reg, 3),
                comprimento_registrado_faixa_m=[min(registrados), max(registrados)],
                comprimento_m=round(c["comprimento"], 4), largura_m=round(c["largura"], 4),
                altura_m=round(c["altura"], 4), x_min_m=round(c["x_min"], 4), x_max_m=round(c["x_max"], 4),
                comprimento_faixa_m=[round(min(x["comprimento"] for x in caixas), 4),
                                     round(max(x["comprimento"] for x in caixas), 4)],
                vertices=caixas[0]["vertices"],
                geometria_varia_com_semente=max(varia.values()) >= 1e-9, pixels=px)


def main():
    M = OA.mats()
    out = {"metodo": "vertices da malha construida por objetos_alongados.py, no referencial local da arma "
                     "(+X cano, Y largura, Z altura); caixa = max menos min por eixo; pixels = metros / GSD; "
                     f"{SEMENTES} sementes por malha, caixa identica em todas (o sorteio so escolhe material)",
           "gsd_cm_px": dict(GSD), "armas": {}, "armas_ineditas": {}, "objetos": {}}
    for nome, fn, peso in OA.ARMAS:
        out["armas"][nome] = dict(peso_sorteio=peso, **mede(nome, fn, M))
    for nome, fn, peso in OA.ARMAS_INEDITAS:
        out["armas_ineditas"][nome] = dict(peso_sorteio=peso, **mede(nome, fn, M))
    for nome, fn, peso in getattr(OA, "OBJETOS", []):
        out["objetos"][nome] = dict(peso_sorteio=peso, **mede(nome, fn, M, deterministico=False))

    # pegada mediana e faixa das cinco armas de treino, ponderadas pelo peso de sorteio
    pesos = {n: d["peso_sorteio"] for n, d in out["armas"].items()}
    tot = sum(pesos.values())
    out["armas_resumo"] = {}
    for alt, gsd in GSD:
        comp = [d["pixels"][alt]["comprimento_px"] for d in out["armas"].values()]
        larg = [d["pixels"][alt]["largura_px"] for d in out["armas"].values()]
        out["armas_resumo"][alt] = dict(
            comprimento_px_min=min(comp), comprimento_px_max=max(comp),
            largura_px_min=min(larg), largura_px_max=max(larg),
            comprimento_px_medio_ponderado=round(sum(d["pixels"][alt]["comprimento_px"] * pesos[n]
                                                      for n, d in out["armas"].items()) / tot, 1),
            largura_px_media_ponderada=round(sum(d["pixels"][alt]["largura_px"] * pesos[n]
                                                 for n, d in out["armas"].items()) / tot, 2))

    with open(os.path.join(AQUI, "armas_malhas.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    L = ["# Caixa envolvente das malhas de arma e pegada em pixels", "",
         "Gerado por `mede_armas.py` (dentro do Blender headless; ver docstring). Metros no referencial local "
         "da arma: comprimento no eixo do cano, largura de lado a lado, altura do carregador ao topo. Pixels = metros "
         "dividido pelo GSD (4,88, 2,44 e 1,14 cm/px a 150, 75 e 35 m em 4K). A caixa e deterministica: "
         f"{SEMENTES} sementes por malha deram a mesma caixa (o sorteio so escolhe material). "
         "\"Registrado\" e o comprimento nominal que a funcao devolve e que o manuscrito cita; a malha pode ser "
         "mais comprida (coronha e carregador fora do nominal). Os objetos confundiveis sorteiam o comprimento: "
         "para eles a tabela traz a mediana das sementes e, entre colchetes, a faixa.", ""]
    for grupo, titulo in (("armas", "Armas de treino (as cinco)"), ("armas_ineditas", "Armas ineditas (so teste)"),
                          ("objetos", "Objetos confundiveis (contraste)")):
        if not out[grupo]:
            continue
        L += [f"## {titulo}", "",
              "| Malha | Peso | Registrado (m) | Comprimento (m) | Largura (m) | Altura (m) | "
              "150 m: C x L (px) | 75 m: C x L (px) | 35 m: C x L (px) | Altura a 150 / 75 / 35 (px) |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for n, d in out[grupo].items():
            p = d["pixels"]
            faixa = (f" [{d['comprimento_faixa_m'][0]:.2f} a {d['comprimento_faixa_m'][1]:.2f}]"
                     if d["geometria_varia_com_semente"] else "")
            L.append(f"| {n} | {d['peso_sorteio']} | {d['comprimento_registrado_m']:.2f} | {d['comprimento_m']:.3f}{faixa} | "
                     f"{d['largura_m']:.3f} | {d['altura_m']:.3f} | "
                     f"{p['150 m']['comprimento_px']:.1f} x {p['150 m']['largura_px']:.1f} | "
                     f"{p['75 m']['comprimento_px']:.1f} x {p['75 m']['largura_px']:.1f} | "
                     f"{p['35 m']['comprimento_px']:.1f} x {p['35 m']['largura_px']:.1f} | "
                     f"{p['150 m']['altura_px']:.1f} / {p['75 m']['altura_px']:.1f} / {p['35 m']['altura_px']:.1f} |")
        L.append("")
    L += ["## Resumo das cinco armas de treino", "",
          "| GSD | Comprimento (px), min a max | Largura (px), min a max | Comprimento medio ponderado pelo sorteio (px) | Largura media ponderada (px) |",
          "|---|---|---|---|---|"]
    for alt, gsd in GSD:
        r = out["armas_resumo"][alt]
        L.append(f"| {alt}, {gsd} cm/px | {r['comprimento_px_min']} a {r['comprimento_px_max']} | "
                 f"{r['largura_px_min']} a {r['largura_px_max']} | {r['comprimento_px_medio_ponderado']} | "
                 f"{r['largura_px_media_ponderada']} |")
    with open(os.path.join(AQUI, "armas_malhas.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
