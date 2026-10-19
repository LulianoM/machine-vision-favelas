#!/usr/bin/env python3
"""
resolvivel.py: para cada comparacao de manchete do artigo, a diferenca relativa e se ela e resolvivel sob
tres leituras (ponto A3 do feedback de 14/10: diferencas pequenas entre modelos tratadas como resultado):
  (a) faixas min-max das sementes de treino que nao se cruzam (so onde ha sementes dos dois lados;
      com um lado de treino unico, diz-se onde o valor unico cai em relacao a faixa do outro lado);
  (b) intervalo de 95% por reamostragem da diferenca pareada que exclui zero
      (VisDrone: reamostragem de imagens, pareada, bootstrap_visdrone.json; armados: reamostragem de
      quadros, independente em cada lado, limiar_armado.json);
  (c) diferenca relativa de pelo menos 30% do menor valor.
Onde ha sementes, a diferenca e a das medias das sementes (as diferencas semente a semente ficam no JSON).

  C:/arma3-favela/venv/Scripts/python.exe resolvivel.py
Saidas: resolvivel.json, resolvivel.md

Rodada 5 (18/10/2026): com --sufixo r5 le bootstrap_visdrone_r5.json (pares da rodada 5, entre grupos de
sementes) e grava resolvivel_r5.json e .md, sem tocar nos de 17/10. Cada diferenca do bootstrap r5
recebe as tres leituras, com as mesmas funcoes de faixa e de leitura (a) daqui.

  C:/arma3-favela/venv/Scripts/python.exe resolvivel.py --sufixo r5
"""
import json
import os
import sys
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
LIMIAR_REL = 30.0


def le(nome):
    p = os.path.join(AQUI, nome)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def faixa(vals):
    vals = [v for v in vals if v is not None]
    return {"valores": vals, "min": min(vals), "max": max(vals), "n": len(vals)} if vals else None


def leitura_a(fa, fb):
    """fa = lado maior esperado (a), fb = lado b"""
    if fa is None or fb is None:
        return "sem dado", None
    if fa["n"] >= 2 and fb["n"] >= 2:
        sep = fa["min"] > fb["max"] or fb["min"] > fa["max"]
        return ("resolvivel: faixas nao se cruzam" if sep else "nao resolvivel: faixas se cruzam"), sep
    # um lado com treino unico
    if fa["n"] == 1 and fb["n"] >= 2:
        fora = fa["min"] > fb["max"] or fa["min"] < fb["min"]
        return (f"treino unico em a; o valor de a fica {'fora' if fora else 'dentro'} da faixa de b"), None
    if fb["n"] == 1 and fa["n"] >= 2:
        fora = fb["min"] > fa["max"] or fb["min"] < fa["min"]
        return (f"treino unico em b; o valor de b fica {'fora' if fora else 'dentro'} da faixa de a"), None
    return "treino unico dos dois lados: nao avaliavel", None


def main():
    if "--sufixo" in sys.argv:
        return main_sufixo(sys.argv[sys.argv.index("--sufixo") + 1])
    bv = le("bootstrap_visdrone.json")
    la = le("limiar_armado.json")
    if bv is None or la is None:
        raise SystemExit("rode bootstrap_visdrone.py e limiar_armado.py antes")
    mod = bv["modelos"]
    difs = bv["diferencas"]

    def val(nome):
        return mod[nome]["mAP50_conjunto_inteiro"] if nome in mod else None

    def sementes(base):
        if base in mod:
            return faixa([val(base)])
        return faixa([val(f"{base} s{k}") for k in range(3)])

    def dif_media(comp):
        """a entrada de diferenca pareada que usa as medias das sementes (ou a unica, se nao ha sementes)"""
        cands = [d for d in difs if d["comparacao"] == comp]
        if not cands:
            return None
        med = [d for d in cands if "media das sementes" in d["rotulo"]]
        return med[0] if med else cands[0]

    linhas = []

    def linha_visdrone(titulo, comp, a, b, unidade="mAP50 no VisDrone-DET val"):
        d = dif_media(comp)
        if d is None:
            linhas.append({"comparacao": titulo, "faltando": True})
            return
        fa, fb = sementes(a), sementes(b)
        ra, oka = leitura_a(fa, fb)
        okb = d["ic_exclui_zero"]
        rel = d["dif_relativa_pct_do_menor"]
        okc = rel is not None and abs(rel) >= LIMIAR_REL
        linhas.append({"comparacao": titulo, "medida": unidade, "a": a, "b": b, "a_valor": d["a_mAP50"], "b_valor": d["b_mAP50"],
                       "dif_absoluta": d["dif_conjunto_inteiro"], "dif_relativa_pct_do_menor": rel, "razao_a_sobre_b": d["razao_a_sobre_b"],
                       "razao_ic95": d["razao_ic95"], "sementes_a": fa, "sementes_b": fb,
                       "a_faixas_de_sementes": ra, "a_ok": oka, "b_ic95_dif": d["dif_ic95"], "b_fracao_positiva": d["fracao_reamostras_positiva"],
                       "b_ok": okb, "c_ok": okc, "bootstrap": "imagens do VisDrone val (pareado)",
                       "semente_a_semente": [{"rotulo": x["rotulo"], "dif": x["dif_conjunto_inteiro"], "ic95": x["dif_ic95"], "exclui_zero": x["ic_exclui_zero"]}
                                             for x in difs if x["comparacao"] == comp and "media das sementes" not in x["rotulo"]]})

    linha_visdrone("Nadir vs oblique (S-oblique vs S-nadir-150)", "nadir vs oblique", "S-oblique", "S-nadir-150")
    linha_visdrone("Six settlements vs one, nadir (S-nadir-150-six vs S-nadir-150)", "six settlements vs one, nadir", "S-nadir-150-six", "S-nadir-150")
    linha_visdrone("Six settlements vs one, oblique (S-oblique-six vs S-oblique)", "six settlements vs one, oblique", "S-oblique-six", "S-oblique")
    linha_visdrone("Generic vs synthetic start, 5%", "generic vs synthetic start, 5%", "F-generic 5%", "F-synthetic 5%")
    linha_visdrone("Generic vs synthetic start, 10%", "generic vs synthetic start, 10%", "F-generic 10%", "F-synthetic 10%")
    linha_visdrone("Generic vs joint, 5%", "generic vs joint, 5%", "F-generic 5%", "F-joint 5%")
    linha_visdrone("Generic vs joint, 10%", "generic vs joint, 10%", "F-generic 10%", "F-joint 10%")
    linha_visdrone("Joint vs synthetic start, 5%", "joint vs synthetic start, 5%", "F-joint 5%", "F-synthetic 5%")
    linha_visdrone("Joint vs synthetic start, 10%", "joint vs synthetic start, 10%", "F-joint 10%", "F-synthetic 10%")

    # armados: objeto chamado de armada a conf 0,25
    res = la["resultados"]
    dq = la["diferencas_bootstrap_quadros"]

    def obj(chave):
        return res[chave]["pontos"]["conf_0.25"]["objeto_chamado_armada"] if chave in res else None

    for conjunto, rot in (("val", "validation split"), ("novos", "new frames, 80 each")):
        fa = faixa([obj(f"S-nadir-35 s{k} | {conjunto}") for k in range(3)])
        fb = faixa([obj(f"Twin-75 s{k} | {conjunto}") for k in range(3)])
        d = next((x for x in dq if x["conjunto"] == conjunto and x["medida"] == "objeto_chamado_armada" and "media das sementes" in x["comparacao"]), None)
        if d is None or fa is None or fb is None:
            linhas.append({"comparacao": f"35 m vs twin at 75 m, object called armed, {rot}", "faltando": True})
            continue
        ra, oka = leitura_a(fa, fb)
        rel = d["dif_relativa_pct_do_menor"]
        linhas.append({"comparacao": f"35 m vs twin at 75 m, object called armed, {rot}", "medida": "objeto chamado de armada a conf 0,25",
                       "a": "S-nadir-35 (media das sementes)", "b": "Twin-75 (media das sementes)", "a_valor": d["a"], "b_valor": d["b"],
                       "dif_absoluta": d["dif"], "dif_relativa_pct_do_menor": rel, "razao_a_sobre_b": round(d["a"] / d["b"], 3) if d["b"] else None,
                       "razao_ic95": None, "sementes_a": fa, "sementes_b": fb, "a_faixas_de_sementes": ra, "a_ok": oka,
                       "b_ic95_dif": d["dif_ic95"], "b_fracao_positiva": d["fracao_positiva"], "b_ok": d["ic_exclui_zero"],
                       "c_ok": rel is not None and abs(rel) >= LIMIAR_REL, "bootstrap": "quadros, independente em cada lado (conjuntos nao pareados)",
                       "semente_a_semente": [{"rotulo": x["comparacao"], "dif": x["dif"], "ic95": x["dif_ic95"], "exclui_zero": x["ic_exclui_zero"]}
                                             for x in dq if x["conjunto"] == conjunto and x["medida"] == "objeto_chamado_armada" and "media" not in x["comparacao"]]})
    d = next((x for x in dq if x["comparacao"].startswith("S-nadir-35 s0 - S-nadir-75") and x["medida"] == "objeto_chamado_armada"), None)
    if d is not None:
        fa, fb = faixa([obj("S-nadir-35 s0 | val")]), faixa([obj("S-nadir-75 | val")])
        ra, oka = leitura_a(fa, fb)
        rel = d["dif_relativa_pct_do_menor"]
        linhas.append({"comparacao": "35 m vs original 75 m, object called armed, validation split", "medida": "objeto chamado de armada a conf 0,25",
                       "a": "S-nadir-35 s0", "b": "S-nadir-75", "a_valor": d["a"], "b_valor": d["b"], "dif_absoluta": d["dif"],
                       "dif_relativa_pct_do_menor": rel, "razao_a_sobre_b": round(d["a"] / d["b"], 3) if d["b"] else None, "razao_ic95": None,
                       "sementes_a": fa, "sementes_b": fb, "a_faixas_de_sementes": ra, "a_ok": oka, "b_ic95_dif": d["dif_ic95"],
                       "b_fracao_positiva": d["fracao_positiva"], "b_ok": d["ic_exclui_zero"], "c_ok": rel is not None and abs(rel) >= LIMIAR_REL,
                       "bootstrap": "quadros, independente em cada lado (vals de corpora diferentes)", "semente_a_semente": []})

    for l in linhas:
        if l.get("faltando"):
            continue
        passa = [l["a_ok"], l["b_ok"], l["c_ok"]]
        l["veredito"] = {"leituras_passadas": sum(1 for x in passa if x is True), "leituras_avaliaveis": sum(1 for x in passa if x is not None),
                         "resumo": ("resolvivel nas " + ("tres" if sum(1 for x in passa if x is True) == 3 else str(sum(1 for x in passa if x is True)) + " de " + str(sum(1 for x in passa if x is not None)))
                                    + " leituras") if sum(1 for x in passa if x is True) else "nao resolvivel em nenhuma leitura"}

    out = {"leituras": {"a": "faixas min-max das sementes de treino nao se cruzam (exige sementes dos dois lados)",
                        "b": "IC 95% por reamostragem da diferenca pareada exclui zero",
                        "c": f"diferenca relativa >= {LIMIAR_REL:.0f}% do menor valor"},
           "fontes": ["bootstrap_visdrone.json", "limiar_armado.json"], "comparacoes": linhas,
           "quando": datetime.now().isoformat(timespec="seconds")}
    with open(os.path.join(AQUI, "resolvivel.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)

    def sim(x):
        return "sim" if x is True else ("nao" if x is False else "n/a")

    def fx(f):
        return "treino unico" if f["n"] == 1 else f"{f['min']:.4f} a {f['max']:.4f}" if f["max"] < 1 and f["min"] < 0.2 else f"{f['min']:.3f} a {f['max']:.3f}"

    L = ["# Diferencas de manchete: resolviveis sob tres leituras (17/10/2026, agente D2)", "",
         "Leituras: (a) faixas min-max das sementes de treino nao se cruzam; (b) intervalo de 95% por reamostragem da diferenca pareada exclui zero "
         "(VisDrone: reamostragem de imagens, pareada; armados: reamostragem de quadros, independente em cada lado); (c) diferenca relativa de pelo menos "
         "30% do menor valor. Onde ha sementes dos dois lados, a diferenca e a das medias das sementes; a leitura (a) exige sementes dos dois lados, e "
         "com um lado de treino unico fica registrado onde o valor unico cai em relacao a faixa do outro.", "",
         "| Comparacao | medida | a | b | dif. absoluta | dif. relativa (% do menor) | razao a/b (IC 95%) | sementes a | sementes b | (a) faixas | (b) IC 95% da dif. | (b) | (c) >= 30% | veredito |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for l in linhas:
        if l.get("faltando"):
            L.append(f"| {l['comparacao']} | faltando | | | | | | | | | | | | |")
            continue
        razao = f"{l['razao_a_sobre_b']}" + (f" ({l['razao_ic95'][0]} a {l['razao_ic95'][1]})" if l.get("razao_ic95") else "")
        L.append(f"| {l['comparacao']} | {l['medida']} | {l['a_valor']:.4f} | {l['b_valor']:.4f} | {l['dif_absoluta']:+.4f} | {l['dif_relativa_pct_do_menor']:+.1f}% | {razao} | "
                 f"{fx(l['sementes_a'])} | {fx(l['sementes_b'])} | {l['a_faixas_de_sementes']} | {l['b_ic95_dif'][0]:+.4f} a {l['b_ic95_dif'][1]:+.4f} | {sim(l['b_ok'])} | "
                 f"{sim(l['c_ok'])} | {l['veredito']['resumo']} |")
    L += ["", "Diferencas semente a semente (onde ha sementes):", ""]
    for l in linhas:
        for s in l.get("semente_a_semente", []):
            L.append(f"- {l['comparacao']}: {s['rotulo']}: {s['dif']:+.4f}, IC 95% {s['ic95'][0]:+.4f} a {s['ic95'][1]:+.4f}, exclui zero: {'sim' if s['exclui_zero'] else 'nao'}")
    with open(os.path.join(AQUI, "resolvivel.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


def main_sufixo(sufixo):
    bv = le(f"bootstrap_visdrone_{sufixo}.json")
    if bv is None:
        raise SystemExit(f"rode bootstrap_visdrone.py --sufixo {sufixo} antes")
    linhas = []
    for d in bv["diferencas"]:
        fa, fb = faixa(d["a_valores"]), faixa(d["b_valores"])
        ra, oka = leitura_a(fa, fb)
        rel = d["dif_relativa_pct_do_menor"]
        okc = rel is not None and abs(rel) >= LIMIAR_REL
        okb = d["ic_exclui_zero"]
        passa = [oka, okb, okc]
        n_ok = sum(1 for x in passa if x is True)
        n_av = sum(1 for x in passa if x is not None)
        linhas.append({"comparacao": d["comparacao"], "medida": "mAP50 no VisDrone-DET val", "a": d["a"], "b": d["b"],
                       "a_runs": d["a_runs"], "b_runs": d["b_runs"], "a_valor": d["a_mAP50"], "b_valor": d["b_mAP50"],
                       "dif_absoluta": d["dif_conjunto_inteiro"], "dif_relativa_pct_do_menor": rel,
                       "razao_a_sobre_b": d["razao_a_sobre_b"], "razao_ic95": d["razao_ic95"],
                       "sementes_a": fa, "sementes_b": fb, "a_faixas_de_sementes": ra, "a_ok": oka,
                       "b_ic95_dif": d["dif_ic95"], "b_fracao_positiva": d["fracao_reamostras_positiva"], "b_ok": okb, "c_ok": okc,
                       "resolvivel": bool(oka is True or okb is True),
                       "veredito": {"leituras_passadas": n_ok, "leituras_avaliaveis": n_av,
                                    "passou_em": [k for k, x in zip("abc", passa) if x is True],
                                    "resumo": (f"resolvivel ({', '.join(k for k, x in zip('abc', passa) if x is True)})"
                                               if (oka is True or okb is True) else "nao resolvivel em (a) nem em (b)")}})
    out = {"leituras": {"a": "faixas min-max das sementes de treino nao se cruzam (exige sementes dos dois lados)",
                        "b": "IC 95% por reamostragem pareada de imagens da diferenca das medias exclui zero",
                        "c": f"diferenca relativa >= {LIMIAR_REL:.0f}% do menor valor (descritiva)",
                        "resolvivel": "passa em (a) ou em (b) (PLANO-RODADA5.md, secao 2.3)"},
           "fontes": [f"bootstrap_visdrone_{sufixo}.json"], "comparacoes": linhas, "faltando": bv.get("faltando", []),
           "quando": datetime.now().isoformat(timespec="seconds")}
    with open(os.path.join(AQUI, f"resolvivel_{sufixo}.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    L = [f"# Resolubilidade, rodada 5 ({datetime.now():%d/%m/%Y})", "",
         "| Comparacao | a | b | dif. | dif. relativa | (a) faixas | (b) IC 95% | (c) | veredito |",
         "|---|---|---|---|---|---|---|---|---|"]
    for l in linhas:
        rel = "n/a" if l["dif_relativa_pct_do_menor"] is None else f"{l['dif_relativa_pct_do_menor']:+.1f}%"
        L.append(f"| {l['comparacao']} | {l['a_valor']:.4f} | {l['b_valor']:.4f} | {l['dif_absoluta']:+.4f} | {rel} | "
                 f"{l['a_faixas_de_sementes']} | {l['b_ic95_dif'][0]:+.4f} a {l['b_ic95_dif'][1]:+.4f} | "
                 f"{'sim' if l['c_ok'] else 'nao'} | {l['veredito']['resumo']} |")
    with open(os.path.join(AQUI, f"resolvivel_{sufixo}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
