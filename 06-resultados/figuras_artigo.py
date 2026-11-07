#!/usr/bin/env python3
"""
figuras_artigo.py: tres figuras do artigo, feitas so com corpora procedurais (gen_morro.py, sem dado
da PCERJ), a pedido do autor em 30/09.

  fig6_assentamentos.jpg  um quadro de cada um dos seis assentamentos do S-oblique-six (sitios -1 a
                          4 de sitios.py; o -1 e o assentamento do corpus de referencia)
  fig7_armados.jpg        pessoa com fuzil, com pistola, sem nada, com vassoura, com cano e com
                          guarda-chuva a 35, 75 e 150 m (corpus de 35 m, gemeos de 75 e 150 m e quadros
                          novos da rodada 4), cada recorte ampliado ao mesmo tamanho (vizinho mais
                          proximo), para mostrar quanto da arma chega ao sensor em cada altitude
  fig8_nadir_obliquo.jpg  o mesmo assentamento visto em nadir a 150 m (corpus de referencia) e com a
                          camera obliqua (S-oblique), com recortes de pessoas sem arma de cada um

Figuras 2 e 4 refeitas com rotulos em ingles a partir das mesmas imagens de 20/09. A figura 5 sai de
03-blender/scripts/previa_dataset.py --ds C:/arma3-favela/blender/ds_morro_clima --n 4 --cols 2
--larg 900 --zoom 5 --seed 1 --en --out figuras/fig5_anotacao.jpg (a semente 1 reproduz os quatro
quadros da versao de 20/09).

Escolha deterministica: para cada painel, o primeiro quadro (em ordem de nome) que atende ao filtro
declarado em cada funcao. Nenhum numero sai daqui; as legendas usam os do texto. Excecao: na figura 7
as pessoas com arma ou objeto foram escolhidas a olho (ver fig7).

  python figuras_artigo.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

B = os.path.join("C:" + os.sep, "arma3-favela", "blender")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figuras")
FONTE = ImageFont.truetype(os.path.join("C:" + os.sep, "Windows", "Fonts", "arialbd.ttf"), 34)
FONTE_P = ImageFont.truetype(os.path.join("C:" + os.sep, "Windows", "Fonts", "arialbd.ttf"), 28)
CLARO = ("sol_duro", "sol_baixo", "nublado")


def manifest(ds):
    return [json.loads(ln) for ln in open(os.path.join(B, ds, "manifest.jsonl"), encoding="utf-8") if ln.strip()]


def imagem(ds, r):
    return Image.open(os.path.join(B, ds, "images", r["split"], r["img"])).convert("RGB")


def caixas(ds, r):
    """[(classe, tipo, vis, cx, cy, w, h)] na ordem do arquivo de rotulo. Corpora antigos nao tem
    `caixas`; neles o tipo sai de `tipos`, que so lista as caixas com objeto (armada e objeto)."""
    base = os.path.splitext(r["img"])[0]
    linhas = [ln.split() for ln in open(os.path.join(B, ds, "labels", r["split"], base + ".txt")) if ln.strip()]
    vis = r.get("vis") or [1.0] * len(linhas)
    if "caixas" in r:
        tipos = [c[1] for c in r["caixas"]]
    else:
        fila = list(r.get("tipos") or [])
        tipos = [(fila.pop(0) if int(ln[0]) in (0, 2) and fila else "") for ln in linhas]
    return [(int(ln[0]), tipos[i] if i < len(tipos) else "", vis[i] if i < len(vis) else 1.0,
             *map(float, ln[1:5])) for i, ln in enumerate(linhas)]


def rotulo(img, texto, xy, fonte=FONTE):
    d = ImageDraw.Draw(img, "RGBA")
    x0, y0, x1, y1 = d.textbbox(xy, texto, font=fonte)
    d.rectangle((x0 - 10, y0 - 6, x1 + 10, y1 + 6), fill=(0, 0, 0, 170))
    d.text(xy, texto, font=fonte, fill=(255, 255, 255, 255))


def recorte(img, cx, cy, w, h, fator, lado_min, tam):
    W, H = img.size
    s = max(lado_min, int(max(w * W, h * H) * fator))
    x, y = int(cx * W - s / 2), int(cy * H - s / 2)
    x, y = min(max(0, x), W - s), min(max(0, y), H - s)
    return img.crop((x, y, x + s, y + s)).resize((tam, tam), Image.NEAREST)


def fig6():
    paineis = []
    for k in (-1, 0, 1, 2, 3, 4):
        ds = f"_oblvar_s{k}"
        rs = [r for r in manifest(ds) if r["clima"] == "sol_duro"]
        r = max(rs, key=lambda r: (r["n_caixas"], -int(r["img"][3:9])))
        paineis.append(imagem(ds, r).resize((1200, 675), Image.LANCZOS))
    grade = Image.new("RGB", (3 * 1200 + 2 * 12, 2 * 675 + 12), "white")
    for i, p in enumerate(paineis):
        x, y = (i % 3) * 1212, (i // 3) * 687
        grade.paste(p, (x, y))
        rotulo(grade, str(i + 1), (x + 22, y + 18))
    grade = grade.resize((2400, int(grade.height * 2400 / grade.width)), Image.LANCZOS)
    grade.save(os.path.join(OUT, "fig6_assentamentos.jpg"), quality=86)


def isolada(cxs, k, fator):
    """nenhuma outra caixa com centro dentro do recorte da caixa k"""
    _, _, _, cx, cy, w, h = cxs[k]
    meia = max(w, h) * fator / 2
    return all(abs(o[3] - cx) > meia or abs(o[4] - cy) > meia for i, o in enumerate(cxs) if i != k)


def fig7():
    """Escolha a olho, 30/09, depois de o autor apontar na versao anterior (maior caixa que passava nos
    filtros) um guarda-chuva que parecia pistola e armas soltas do corpo. Motivo, no gerador
    (people_mpfb.py): o objeto e preso no punho direito com orientacao fixada por pose no espaco do
    corpo, nao resolvida contra as maos, e na pose "ao lado" aponta quase na vertical, de modo que de
    cima o guarda-chuva encolhe a um toco escuro. Criterio da escolha, entre os recortes visiveis
    (visibilidade >= 0,85), sozinhos no recorte e em regime claro (folhas de candidatos com os 14 de
    maior caixa por tipo e altitude): o objeto dentro da mao e perto da horizontal, de modo que o
    comprimento inteiro aparece, e sem varal ou cabo da cena que se confunda com ele. A coluna sem
    arma segue o criterio automatico antigo. Os tipos conferem com as caixas: nos corpora com
    `caixas` a ordem de classe bate com o rotulo em todos os quadros, e no ds_armado_35, que so tem
    `tipos`, o numero de tipos bate com o de caixas armada e objeto nos 200 quadros."""
    linhas = [("35 m", "ds_armado_35_extra"), ("75 m", "ds_armado_75g_extra"), ("150 m", "ds_armado_150g")]
    colunas = [("Rifle", 0, ("fuzil_ak", "fuzil_ar", "carabina")), ("Pistol", 0, ("pistola",)),
               ("Unarmed", 1, ("",)), ("Broom", 2, ("vassoura",)), ("Pipe", 2, ("cano_pvc",)),
               ("Umbrella", 2, ("guarda_chuva",))]
    escolha = {  # (linha, coluna): (corpus, quadro, indice da caixa no rotulo)
        ("35 m", "Rifle"): ("ds_armado_35", "mr_000139.png", 7),
        ("35 m", "Pistol"): ("ds_armado_35", "mr_000042.png", 2),
        ("35 m", "Broom"): ("ds_armado_35", "mr_000156.png", 3),
        ("35 m", "Pipe"): ("ds_armado_35_extra", "mr_000277.png", 12),
        ("35 m", "Umbrella"): ("ds_armado_35", "mr_000090.png", 7),
        ("75 m", "Rifle"): ("ds_armado_75g", "mr_000186.png", 9),
        ("75 m", "Pistol"): ("ds_armado_75g_extra", "mr_000253.png", 3),
        ("75 m", "Broom"): ("ds_armado_75g_extra", "mr_000222.png", 6),
        ("75 m", "Pipe"): ("ds_armado_75g_extra", "mr_000234.png", 9),
        ("75 m", "Umbrella"): ("ds_armado_75g", "mr_000162.png", 4),
        ("150 m", "Rifle"): ("ds_armado_150g", "mr_000043.png", 2),
        ("150 m", "Pistol"): ("ds_armado_150g", "mr_000146.png", 7),
        ("150 m", "Broom"): ("ds_armado_150g", "mr_000098.png", 0),
        ("150 m", "Pipe"): ("ds_armado_150g", "mr_000038.png", 17),
        ("150 m", "Umbrella"): ("ds_armado_150g", "mr_000068.png", 11),
    }
    tam, ml, mt, g, fator = 300, 150, 70, 10, 1.7
    fig = Image.new("RGB", (ml + len(colunas) * (tam + g), mt + len(linhas) * (tam + g)), "white")
    d = ImageDraw.Draw(fig)
    for j, (nome, _, _) in enumerate(colunas):
        d.text((ml + j * (tam + g) + tam // 2, mt // 2), nome, font=FONTE_P, fill="black", anchor="mm")
    for i, (alt, ds_auto) in enumerate(linhas):
        d.text((ml // 2, mt + i * (tam + g) + tam // 2), alt, font=FONTE_P, fill="black", anchor="mm")
        for j, (nome, cls, tipos) in enumerate(colunas):
            if (alt, nome) in escolha:
                ds, img, k = escolha[(alt, nome)]
                r = next(x for x in manifest(ds) if x["img"] == img)
                c, tp, v, cx, cy, w, h = caixas(ds, r)[k]
                assert c == cls and tp in tipos, (alt, nome, c, tp)
            else:
                # sem arma: pessoa em laje, visivel, longe da borda, sozinha no recorte, em regime
                # claro; entre as que passam, a de maior caixa
                ds, cands = ds_auto, []
                for r in sorted(manifest(ds), key=lambda r: r["img"]):
                    if r["clima"] not in CLARO:
                        continue
                    cxs = caixas(ds, r)
                    lajes = [c[2] for c in r["caixas"]] if "caixas" in r else [1] * len(cxs)
                    for k, (c, tp, v, cx, cy, w, h) in enumerate(cxs):
                        if (c == cls and tp in tipos and v >= 0.95 and lajes[k] == 1 and 0.1 < cx < 0.9
                                and 0.1 < cy < 0.9 and isolada(cxs, k, fator)):
                            cands.append((w * h, r["img"], r, cx, cy, w, h))
                if not cands:
                    continue
                _, _, r, cx, cy, w, h = max(cands, key=lambda c: (c[0], c[1]))
            fig.paste(recorte(imagem(ds, r), cx, cy, w, h, fator, 24, tam), (ml + j * (tam + g), mt + i * (tam + g)))
    fig.save(os.path.join(OUT, "fig7_armados.jpg"), quality=88)


def fig8():
    lados = [("Nadir, 150 m", "ds_morro_4k"), ("Oblique, about 120 m", "ds_morro_obl")]
    quadro_w, quadro_h, tam, n = 1600, 900, 190, 4
    fig = Image.new("RGB", (2 * quadro_w + 20, quadro_h + tam + 40), "white")
    for i, (nome, ds) in enumerate(lados):
        rs = sorted([r for r in manifest(ds) if r["clima"] == "sol_duro"], key=lambda r: -r["n_caixas"])
        r = rs[0]
        img = imagem(ds, r)
        x0 = i * (quadro_w + 20)
        fig.paste(img.resize((quadro_w, quadro_h), Image.LANCZOS), (x0, 0))
        rotulo(fig, nome, (x0 + 24, 20))
        cxs = caixas(ds, r)
        pessoas = [cxs[k] for k in range(len(cxs)) if cxs[k][0] == 1 and cxs[k][2] >= 0.9
                   and 0.1 < cxs[k][3] < 0.9 and 0.1 < cxs[k][4] < 0.9 and isolada(cxs, k, 1.5)]
        # as quatro de recorte mais claro: a de beco sombreado nao mostra a silhueta
        luz = lambda c: sum(recorte(img, c[3], c[4], c[5], c[6], 1.5, 20, 32).convert("L").getdata())
        pessoas = sorted(pessoas, key=luz, reverse=True)
        largura = n * tam + (n - 1) * 12
        xs = x0 + (quadro_w - largura) // 2
        for k, (_, _, _, cx, cy, w, h) in enumerate(pessoas[:n]):
            fig.paste(recorte(img, cx, cy, w, h, 1.5, 20, tam), (xs + k * (tam + 12), quadro_h + 25))
    fig = fig.resize((2400, int(fig.height * 2400 / fig.width)), Image.LANCZOS)
    fig.save(os.path.join(OUT, "fig8_nadir_obliquo.jpg"), quality=86)



REGIMES = [("sol_duro", "Hard sun"), ("sol_baixo", "Low sun"), ("nublado", "Overcast"),
           ("neblina", "Haze"), ("encoberto", "Heavy overcast"), ("chuva", "Rain")]
FONTE_F = ImageFont.truetype(os.path.join("C:" + os.sep, "Windows", "Fonts", "arial.ttf"), 18)


def folha(celulas, larg=680, faixa=26):
    """grade 3 x 2 sobre fundo escuro, com a legenda em faixa abaixo de cada celula (o formato das
    figuras 2 e 4 de 20/09, agora com rotulo em ingles)"""
    ch = int(celulas[0][0].height * larg / celulas[0][0].width)
    f = Image.new("RGB", (3 * larg, 2 * (ch + faixa)), (18, 18, 20))
    d = ImageDraw.Draw(f)
    for k, (im, cap) in enumerate(celulas):
        x, y = (k % 3) * larg, (k // 3) * (ch + faixa)
        f.paste(im.resize((larg, ch), Image.LANCZOS), (x, y))
        d.text((x + 8, y + ch + 4), cap, font=FONTE_F, fill=(220, 220, 225))
    return f


def fig2():
    """os seis regimes sobre a mesma cena e o mesmo enquadramento (gen_morro.py --comparar-climas)"""
    cel = [(Image.open(os.path.join(B, "climas", f"clima_{k}.png")).convert("RGB"), nome) for k, nome in REGIMES]
    folha(cel).save(os.path.join(OUT, "fig2_climas.jpg"), quality=90)


def fig4():
    """um quadro anotado de cada regime, do corpus piloto de 1080p: os mesmos seis quadros da figura
    de 20/09 (identificados pelo regime, pelo numero de caixas e pela elevacao do sol)"""
    quadros = {"sol_duro": "mr_000036.png", "sol_baixo": "mr_000019.png", "nublado": "mr_000008.png",
               "neblina": "mr_000004.png", "encoberto": "mr_000045.png", "chuva": "mr_000047.png"}
    rs = {r["img"]: r for r in manifest("ds_morro_clima")}
    cores = {0: (60, 230, 90), 1: (80, 170, 255)}
    cel = []
    for k, nome in REGIMES:
        r = rs[quadros[k]]
        assert r["clima"] == k
        im = imagem("ds_morro_clima", r)
        W, H = im.size
        d = ImageDraw.Draw(im)
        cxs = caixas("ds_morro_clima", r)
        for c, _, _, cx, cy, w, h in cxs:
            x1, y1, x2, y2 = (cx - w / 2) * W, (cy - h / 2) * H, (cx + w / 2) * W, (cy + h / 2) * H
            d.rectangle([x1 - 4, y1 - 4, x2 + 4, y2 + 4], outline=cores.get(c, (255, 255, 255)), width=3)
        cel.append((im, f"{nome}, {len(cxs)} boxes"))
    folha(cel).save(os.path.join(OUT, "fig4_dataset.jpg"), quality=90)


if __name__ == "__main__":
    fig2()
    fig4()
    fig6()
    fig7()
    fig8()
    for f in ("fig2_climas.jpg", "fig4_dataset.jpg", "fig6_assentamentos.jpg", "fig7_armados.jpg",
              "fig8_nadir_obliquo.jpg"):
        p = os.path.join(OUT, f)
        print(f, Image.open(p).size, round(os.path.getsize(p) / 1024), "KB")
