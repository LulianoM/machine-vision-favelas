#!/usr/bin/env python3
"""
rodada5_criterios.py: aplica os criterios que 03-blender/PLANO-RODADA5.md fixou antes da rodada 5
(molde do rodada4_criterios.py).

Le so arquivos de 06-resultados (inclusive revisao-2026-10-17/) e grava rodada5_criterios.json. Cada item
tem as medidas, a regra copiada do plano e o veredito; item cujo arquivo ainda nao existe sai como
"pendente". Nenhuma regra e escolhida aqui: elas estao no plano, versionado antes do primeiro resultado,
e este script so as executa. Leituras de resolubilidade (secao 2.3): (a) faixas de sementes que nao se
cruzam, (b) intervalo de 95% por reamostragem que exclui zero, (c) diferenca relativa de pelo menos 30%
do menor valor (descritiva); resolvivel = passa em (a) ou em (b).

  python rodada5_criterios.py --parte prioridade   (S, F, N: o bloco de validade, grupo Y1)
  python rodada5_criterios.py --parte tudo         (mais A, D, M, C e a regra de IoU, grupo Y2)

Fontes: revisao-2026-10-17/resolvivel_r5.json e bootstrap_visdrone_r5.json (VisDrone, pares da rodada 5),
rodada5_ft_reproducao.json e rodada5_ft_selecao.json (ajuste fino), revisao-2026-10-17/bootstrap_heridal*.json
e escala_heridal.json (base nadir), sim2real_*.json (curva e teto sintetico), por_regime_s_soldur_4k.json e
por_regime_s_nadir_4k_r5.json (sol duro), rodada5_validade_150.json, confusao_*/extra_* (150 m),
visdrone_oficial_iou.json (IoU).
"""
import argparse
import json
import math
import os
import random
import statistics as stt
from collections import defaultdict
from statistics import NormalDist

AQUI = os.path.dirname(os.path.abspath(__file__))
REV = os.path.join(AQUI, "revisao-2026-10-17")
N = NormalDist()
LIMIAR_REL = 30.0


def le(nome, pasta=AQUI):
    p = os.path.join(pasta, nome)
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sim2real(nome, conjunto="real"):
    d = le(f"sim2real_{nome}.json")
    if not d:
        return None
    return next((r.get("metrics/mAP50(B)") for r in d["resultados"] if r.get("conjunto") == conjunto), None)


def comparacao(prefixo):
    """linha de resolvivel_r5.json cuja comparacao comeca com o prefixo"""
    d = le("resolvivel_r5.json", REV)
    if not d:
        return None
    return next((x for x in d["comparacoes"] if x["comparacao"].startswith(prefixo)), None)


def grupo(nome):
    d = le("bootstrap_visdrone_r5.json", REV)
    return (d or {}).get("grupos", {}).get(nome)


def leituras(c):
    """resumo das tres leituras de uma linha de resolvivel_r5"""
    if c is None:
        return None
    return {"a_valor": c["a_valor"], "b_valor": c["b_valor"], "dif": c["dif_absoluta"],
            "dif_relativa_pct_do_menor": c["dif_relativa_pct_do_menor"], "razao_a_sobre_b": c["razao_a_sobre_b"],
            "razao_ic95": c["razao_ic95"], "a_runs": c["a_runs"], "b_runs": c["b_runs"],
            "a": c["a_faixas_de_sementes"], "a_ok": c["a_ok"], "b_ic95": c["b_ic95_dif"], "b_ok": c["b_ok"], "c_ok": c["c_ok"],
            "resolvivel": c["resolvivel"], "passou_em": c["veredito"]["passou_em"]}


# ------------------------------------------------------------------ S (R5-1)
def item_s():
    p = leituras(comparacao("R5-1 nadir vs oblique"))
    o = leituras(comparacao("R5-1 six settlements vs one, oblique"))
    n6 = leituras(comparacao("R5-1 six settlements vs one, nadir"))
    if p is None:
        return {"veredito": "pendente"}
    gn, go = grupo("S-nadir-150"), grupo("S-oblique")
    out = {"principal_S-oblique_menos_S-nadir-150": p, "six_vs_one_oblique": o, "six_vs_one_nadir": n6,
           "S-nadir-150": gn, "S-oblique": go,
           "regra": "PLANO 3.1: principal com 3 contra 3 sementes; passa em (a) e (b) -> 'passes all three readings' (ou as que "
                    "passar) e fator como razao das medias com faixa; so (b) -> resolvivel pelo intervalo e nao pelas faixas; "
                    "nenhuma -> sai 'Camera pitch moved the figure most'; seis contra um, obliquo, falhando (a) -> a 6.1 perde "
                    "'the single-settlement value lying outside the range of the three runs'"}
    if len(p["a_runs"]) < 3 or len(p["b_runs"]) < 3:
        out["aviso"] = f"principal sem as tres sementes dos dois lados: a {p['a_runs']}, b {p['b_runs']}"
    if p["a_ok"] is True and p["b_ok"]:
        v = "principal resolvivel em (a) e (b)" + (" e (c)" if p["c_ok"] else "")
    elif p["b_ok"]:
        v = ("principal resolvivel pelo intervalo (b) e nao pelas faixas (a): fator escrito com a faixa" if p["a_ok"] is False
             else f"principal resolvivel pelo intervalo (b); (a): {p['a']}")
    elif p["a_ok"] is True:
        v = "principal resolvivel so pelas faixas (a)"
    else:
        v = "principal NAO resolvivel: sai 'Camera pitch moved the figure most'; a ordem nadir-obliquo nao e resolvivel entre treinos"
    if p["dif"] < 0:
        v += " (sinal invertido: S-nadir-150 acima)"
    vs = {"principal": v}
    if o:
        vs["six_vs_one_oblique"] = ("passa (a)" if o["a_ok"] is True else
                                    "FALHA (a): a 6.1 perde 'the single-settlement value lying outside the range of the three runs'"
                                    if o["a_ok"] is False else f"(a) {o['a']}") + f"; resolvivel: {o['resolvivel']}, leituras {o['passou_em']}"
    if n6:
        vs["six_vs_one_nadir"] = f"{n6['a']}; leituras {n6['passou_em']}"
    out["veredito"] = vs
    return out


# ------------------------------------------------------------------ F (R5-5)
def item_f():
    rep = le("rodada5_ft_reproducao.json")
    sel = le("rodada5_ft_selecao.json")
    if rep is None:
        return {"veredito": "pendente"}
    out = {"reproducao_F0": rep}
    if sel is None:
        out["veredito"] = "pendente (selecao do cronograma)"
        return out
    out["selecao"] = sel
    cels = {}
    for f in ("5", "10"):
        for c in ("orig", "fz", "lr", "fzlr"):
            cels[f"{f}% {c}"] = leituras(comparacao(f"R5-5 generic vs synthetic start, {f}%, cell {c}"))
    out["doze_celulas_descritivo"] = cels
    esc = {f: leituras(comparacao(f"R5-5 generic vs synthetic start, {f}%, chosen")) for f in ("5", "10")}
    out["cronogramas_escolhidos"] = esc
    out["regra"] = ("PLANO 3.2: quantidade de interesse por fatia = F-generic menos F-synthetic, cada um no cronograma escolhido em "
                    "sel; custo robusto ao cronograma se nas duas fatias F-generic fica acima e resolvivel; senao custo do "
                    "cronograma (dizer fatia e cronograma); inversao resolvivel a favor do sintetico a 5% reabre a expectativa "
                    "fixada antes da rodada 3")
    if any(v is None for v in esc.values()):
        out["veredito"] = "pendente (falta a comparacao dos cronogramas escolhidos)"
        return out
    estado = {}
    for f, v in esc.items():
        if v["resolvivel"] and v["dif"] > 0:
            estado[f] = "generic acima, resolvivel"
        elif v["resolvivel"] and v["dif"] < 0:
            estado[f] = "synthetic acima, resolvivel (inversao)"
        else:
            estado[f] = "nao resolvivel (empate)"
    out["por_fatia"] = estado
    if all(s == "generic acima, resolvivel" for s in estado.values()):
        v = "custo robusto ao cronograma: o sinal se manteve sob os quatro cronogramas, cada inicio com o que sel preferiu"
    else:
        v = "custo do cronograma: " + "; ".join(f"{f}%: {s} (escolhas {sel['escolha']['05' if f == '5' else '10']})"
                                               for f, s in estado.items() if s != "generic acima, resolvivel")
    if estado.get("5") == "synthetic acima, resolvivel (inversao)":
        v += " | inversao resolvivel a favor do sintetico a 5%: reavaliar a expectativa da rodada 3 com a diferenca das duas fatias"
    if not rep.get("reproduz"):
        v += " | F0 nao reproduziu: controle = ft05_coco_rep (declarar)"
    out["veredito"] = v
    return out


# ------------------------------------------------------------------ N (R5-6)
def item_n():
    b = le("bootstrap_heridal.json", REV)
    if b is None:
        return {"veredito": "pendente (base nadir nao convertida ou nao avaliada)"}
    b1280 = le("bootstrap_heridal_1280.json", REV)
    out = {"escala": le("escala_heridal.json"), "contagens": le("heridal_contagens.json"), "imgsz_casado": b,
           "imgsz_1280": b1280,
           "regra": "PLANO 3.3: R abaixo de 0,05 no imgsz casado -> nao interpretavel; principal S-oblique (3) menos S-nadir-150 (3) "
                    "no casado, leituras (a), (b), (c); nadir resolvivelmente acima -> a ordem se inverte num benchmark nadir; obliquo "
                    "resolvivelmente acima com razao compativel com a do VisDrone -> qualificar a ressalva da 6.1; obliquo acima com "
                    "razao inteiramente abaixo da do VisDrone -> a geometria do benchmark explica parte do fator; nao resolvivel -> "
                    "as duas geometrias nao se separaram; ordem diferente entre casado e 1280 -> dependente de escala"}
    if not b["validade"]["interpretavel"]:
        out["veredito"] = f"nao interpretavel: R = {b['validade']['R_mAP50']} < 0,05 no imgsz casado"
        return out
    p = next((x for x in b["diferencas"] if x["comparacao"].startswith("principal")), None)
    if p is None or p.get("faltando"):
        out["veredito"] = "pendente (principal sem modelos)"
        return out
    rv = b.get("razao_visdrone") or {}
    ric = p.get("razao_ic95")
    vic = rv.get("razao_ic95")
    if p["resolvivel"] and p["dif"] < 0:
        v = "nadir resolvivelmente acima do obliquo: num benchmark nadir a ordem se inverte"
    elif p["resolvivel"] and p["dif"] > 0:
        if ric and vic and ric[1] < vic[0]:
            v = "obliquo acima, com razao inteiramente abaixo da do VisDrone: a geometria do benchmark explica parte do fator"
        elif ric and vic and ric[0] > vic[1]:
            v = "obliquo acima, com razao inteiramente acima da do VisDrone (caso nao previsto no plano: vai ao texto como medido)"
        else:
            v = "obliquo resolvivelmente acima tambem na base nadir, razao compativel com a do VisDrone: qualificar a ressalva da 6.1"
    else:
        v = "nao resolvivel: num benchmark nadir as duas geometrias nao se separaram"
    v += f" [leituras: (a) {p['a_ok']}, (b) {p['b_ok']}, (c) {p['c_ok']}]"
    if b1280:
        p2 = next((x for x in b1280["diferencas"] if x["comparacao"].startswith("principal")), None)
        if p2 and not p2.get("faltando") and (p2["dif"] > 0) != (p["dif"] > 0):
            v += " | ordem diferente a 1280: resultado dependente de escala, os dois vao ao texto"
    out["veredito"] = v
    return out


# ------------------------------------------------------------------ A (R5-3)
def item_a():
    c30 = leituras(comparacao("R5-3 152 vs 30 frames"))
    c120 = leituras(comparacao("R5-3 152 vs 120 frames"))
    if c30 is None and c120 is None:
        return {"veredito": "pendente"}
    pontos = {}
    for n, g in ((30, "S-oblique-six c030"), (60, "S-oblique-six c060"), (90, "S-oblique-six c090"),
                 (120, "S-oblique-six c120"), (152, "S-oblique-six")):
        gg = grupo(g)
        if gg:
            runs = gg["runs"]
            teto = [sim2real(r, "sintetico") for r in runs]
            teto = [t for t in teto if t is not None]
            pontos[n] = {"runs": runs, "mAP50_media": gg["media"], "faixa": [gg["min"], gg["max"]],
                         "teto_sintetico_media": round(stt.mean(teto), 4) if teto else None}
    ajuste = None
    if len(pontos) >= 3:
        xs = [math.log(n) for n in pontos]
        ys = [pontos[n]["mAP50_media"] for n in pontos]
        mx, my = stt.mean(xs), stt.mean(ys)
        a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        ajuste = {"a": round(a, 5), "b": round(my - a * mx, 5), "ganho_por_duplicacao_a_ln2": round(a * math.log(2), 5),
                  "pontos_usados": sorted(pontos)}
    out = {"pontos": pontos, "ajuste_log": ajuste, "152_vs_30": c30, "152_vs_120": c120,
           "regra": "PLANO 3.5: regra da antiga 10.1: o numero de quadros e operante se 152 fica acima de 30 em (a) e em (b); "
                    "senao a RQ1 vira propriedade do gerador. 152 contra 120: inclinado se (a) e (b); plano se nenhuma; 'subindo "
                    "dentro da dispersao de treino' se so (b). Descritivo: mAP50 = a ln(N) + b nas medias, ganho a ln 2"}
    v = {}
    if c30:
        v["regra_10_1"] = ("numero de quadros operante" if c30["a_ok"] is True and c30["b_ok"] and c30["dif"] > 0
                           else "numero de quadros nao operante: a resposta a RQ1 passa a ser propriedade do gerador")
    if c120:
        acima = c120["dif"] > 0
        if c120["a_ok"] is True and c120["b_ok"] and acima:
            v["fim_da_curva"] = "inclinado"
        elif c120["b_ok"] and acima and c120["a_ok"] is not True:
            v["fim_da_curva"] = "subindo dentro da dispersao de treino"
        elif not c120["b_ok"] and c120["a_ok"] is not True:
            v["fim_da_curva"] = "plano"
        else:
            v["fim_da_curva"] = f"caso nao previsto no plano (a {c120['a_ok']}, b {c120['b_ok']}, dif {c120['dif']}): reportar as leituras"
    out["veredito"] = v
    return out


# ------------------------------------------------------------------ D (R5-4)
def boot_recall(quadros, rnd, n=2000):
    bs = []
    for _ in range(n):
        s = [quadros[rnd.randrange(len(quadros))] for _ in quadros]
        bs.append(sum(x for x, _ in s) / max(1, sum(y for _, y in s)))
    return bs


def ic(v):
    v = sorted(v)
    return [round(v[int(0.025 * len(v))], 4), round(v[int(0.975 * len(v)) - 1], 4)] if v else None


def item_d():
    esp, gen = le("por_regime_s_soldur_4k.json"), le("por_regime_s_nadir_4k_r5.json")
    if not esp or not gen:
        return {"veredito": "pendente"}
    pe, pg = esp["por_regime"], gen["por_regime"]
    if "por_quadro" not in pe.get("sol_duro", {}) or "por_quadro" not in pg.get("nublado", {}):
        return {"veredito": "pendente (sem --por-quadro)"}
    e_sd = {q["quadro"]: (q["acertos"], q["caixas"]) for q in pe["sol_duro"]["por_quadro"]}
    g_sd = {q["quadro"]: (q["acertos"], q["caixas"]) for q in pg["sol_duro"]["por_quadro"]}
    g_nb = [(q["acertos"], q["caixas"]) for q in pg["nublado"]["por_quadro"]]
    comuns = sorted(set(e_sd) & set(g_sd))

    def rec(qs):
        return sum(x for x, _ in qs) / max(1, sum(y for _, y in qs))

    # D-i pareada: os mesmos quadros de sol duro
    rnd = random.Random(0)
    di = []
    for _ in range(2000):
        s = [comuns[rnd.randrange(len(comuns))] for _ in comuns]
        di.append(rec([e_sd[q] for q in s]) - rec([g_sd[q] for q in s]))
    # D-ii independente: especialista sob sol duro contra generalista sob nublado
    rnd = random.Random(0)
    be = boot_recall(list(e_sd.values()), rnd)
    bg = boot_recall(g_nb, rnd)
    dii = [a - b for a, b in zip(be, bg)]
    m_esp, m_gen_nb = pe["sol_duro"]["mAP50"], pg["nublado"]["mAP50"]
    rel = round(100 * (m_esp - m_gen_nb) / min(m_esp, m_gen_nb), 1) if min(m_esp, m_gen_nb) > 0 else None
    out = {"mAP50_especialista_sol_duro": m_esp, "mAP50_generalista_sol_duro": pg["sol_duro"]["mAP50"],
           "mAP50_generalista_nublado": m_gen_nb, "c_mAP50_rel_pct": rel,
           "recall_especialista_sol_duro": round(rec(list(e_sd.values())), 4),
           "recall_generalista_sol_duro": round(rec(list(g_sd.values())), 4),
           "recall_generalista_nublado": round(rec(g_nb), 4),
           "D_i_pareada_dif_recall": {"quadros": len(comuns), "dif": round(rec([e_sd[q] for q in comuns]) - rec([g_sd[q] for q in comuns]), 4),
                                      "ic95": ic(di)},
           "D_ii_independente_dif_recall": {"dif": round(rec(list(e_sd.values())) - rec(g_nb), 4), "ic95": ic(dii)},
           "bootstrap": "quadros, 2.000 reamostras, random.Random(0)",
           "regra": "PLANO 3.6: D-ii decide. Intervalo inteiro abaixo de zero e mAP50 do especialista sob sol duro abaixo do "
                    "generalista sob nublado -> regime intrinsecamente mais dificil; intervalo que inclui zero ou fica acima -> "
                    "queda de participacao no treino. (a) nao se aplica; (c) no mAP50"}
    icd = out["D_ii_independente_dif_recall"]["ic95"]
    if icd[1] < 0 and m_esp < m_gen_nb:
        v = "regime intrinsecamente mais dificil: o especialista nao fechou a diferenca"
    elif icd[1] < 0:
        v = "intervalo abaixo de zero mas mAP50 do especialista nao abaixo do generalista sob nublado (caso nao previsto: reportar as duas)"
    else:
        v = "queda de participacao no treino: a dificuldade sob sol duro some quando o treino ve sol duro bastante"
    out["veredito"] = v
    return out


# ------------------------------------------------------------------ M (R5-7)
def dlinha(hit_k, hit_n, fa_k, fa_n):
    """d' com correcao log-linear ((k + 0,5) / (n + 1)), definida mesmo com taxa 0 ou 1"""
    h = (hit_k + 0.5) / (hit_n + 1)
    f = (fa_k + 0.5) / (fa_n + 1)
    return N.inv_cdf(h) - N.inv_cdf(f)


def instancias(d):
    q = defaultdict(list)
    for base, gi, c, tipo, col in d.get("instancias", []):
        q[base].append((c, col))
    return q


def contagens(q, quadros):
    k, n = defaultdict(int), defaultdict(int)
    for b in quadros:
        for c, col in q[b]:
            n[c] += 1
            k[c] += col == 0
    return k, n


def perfil(nome_arq, reamostras=1000):
    d = le(nome_arq)
    if not d or "instancias" not in d:
        return None
    q = instancias(d)
    quadros = sorted(q)
    k, n = contagens(q, quadros)
    tot = sum(n.values())
    perdidas = sum(1 for b in quadros for c, col in q[b] if col == 3)
    rnd = random.Random(0)
    bd, bo = [], []
    for _ in range(reamostras):
        am = [quadros[rnd.randrange(len(quadros))] for _ in quadros]
        kb, nb = contagens(q, am)
        if nb[0] and nb[2]:
            bd.append(dlinha(kb[0], nb[0], kb[2], nb[2]))
            bo.append(kb[2] / nb[2])
    return {"arquivo": nome_arq, "quadros": len(quadros), "pessoas": tot,
            "recall_qualquer_classe": round(1 - perdidas / max(1, tot), 4),
            "objeto_chamado_armada": round(k[2] / max(1, n[2]), 4), "objeto_chamado_armada_ic95": ic(bo),
            "armada_chamada_armada": round(k[0] / max(1, n[0]), 4),
            "dlinha_armada_contra_objeto": round(dlinha(k[0], n[0], k[2], n[2]), 3), "dlinha_ic95": ic(bd),
            "_boot_d": bd, "_boot_o": bo}


def limpa(p):
    return {k: v for k, v in p.items() if not k.startswith("_")} if p else None


def item_m():
    val = le("rodada5_validade_150.json")
    if val is None:
        return {"veredito": "pendente"}
    modelo, pv, pe = None, None, None
    if val["valido"]:
        modelo = "armado_150g_e120"
        pv, pe = perfil("confusao_armado_150g_e120.json"), perfil("extra_armado_150g_e120.json")
    else:
        pv6, pe6 = perfil("confusao_armado_150g_600.json"), perfil("extra_armado_150g_600.json")
        if pv6 and pe6:
            modelo, pv, pe = "armado_150g_600", pv6, pe6
    out = {"validade_e120": val,
           "regra": "PLANO 3.7: validade = pelo menos metade das pessoas encontradas, em qualquer classe, no val e nos 80 quadros "
                    "independentes; d' armada contra objeto com IC por 1.000 reamostras de quadros (semente 0); IC inclui 0 -> "
                    "ausencia a 150 m medida; exclui -> separacao acima do acaso no sintetico, tratada como atalho; curva "
                    "35/75/150 m nos 80 quadros independentes, 150 contra 75 m pela leitura (b) (reamostragem independente) e (c)"}
    if modelo is None:
        out["veredito"] = "pendente (ramo de 600 quadros ainda nao medido)" if not val["valido"] else "pendente"
        return out
    valido = pv["recall_qualquer_classe"] >= 0.5 and pe["recall_qualquer_classe"] >= 0.5
    out.update({"modelo": modelo, "val": limpa(pv), "quadros_novos": limpa(pe), "valido": valido})
    curva = {"35 m": perfil("extra_armado_35.json"), "75 m gemeo": perfil("extra_armado_75g.json"), "150 m gemeo": pe}
    out["curva_quadros_novos"] = {k: limpa(v) for k, v in curva.items()}
    if curva["75 m gemeo"] and pe:
        a, b = pe, curva["75 m gemeo"]
        dd = [x - y for x, y in zip(a["_boot_d"], b["_boot_d"])]
        do = [x - y for x, y in zip(a["_boot_o"], b["_boot_o"])]
        icd, ico = ic(dd), ic(do)

        def rel(x, y):
            m = min(abs(x), abs(y))
            return round(100 * (x - y) / m, 1) if m > 0 else None
        out["150_contra_75"] = {
            "dlinha": {"dif": round(a["dlinha_armada_contra_objeto"] - b["dlinha_armada_contra_objeto"], 3), "ic95": icd,
                       "b_ok": bool(icd and (icd[0] > 0 or icd[1] < 0)),
                       "c_rel_pct": rel(a["dlinha_armada_contra_objeto"], b["dlinha_armada_contra_objeto"])},
            "objeto_chamado_armada": {"dif": round(a["objeto_chamado_armada"] - b["objeto_chamado_armada"], 4), "ic95": ico,
                                      "b_ok": bool(ico and (ico[0] > 0 or ico[1] < 0)),
                                      "c_rel_pct": rel(a["objeto_chamado_armada"], b["objeto_chamado_armada"])},
            "nota": "reamostragem independente de quadros nos dois corpora (os mesmos indices de quadro, sorteios separados)"}
    if not valido:
        out["veredito"] = (f"nao interpretavel: {modelo} nao passa a validade (recall val {pv['recall_qualquer_classe']}, "
                           f"novos {pe['recall_qualquer_classe']})" + ("; triplicar o corpus nao deu validade" if modelo.endswith("600") else ""))
        return out
    icd = pe["dlinha_ic95"]
    if icd and icd[0] <= 0 <= icd[1]:
        v = "ausencia a 150 m medida: o IC 95% de d' (armada contra objeto) inclui 0"
    else:
        v = "separacao acima do acaso no sintetico (IC de d' exclui 0): tratada como atalho, nao como capacidade"
    out["veredito"] = f"{modelo}: {v} (nos 80 quadros independentes)"
    return out


# ------------------------------------------------------------------ C (R5-2)
def item_c():
    cena, treino = grupo("S-oblique-six scenes"), grupo("S-oblique-six")
    c2 = leituras(comparacao("R5-2 C-ii"))
    if cena is None or c2 is None or len(cena["runs"]) < 3:
        return {"veredito": "pendente"}
    fc = cena["max"] - cena["min"]
    ft = treino["max"] - treino["min"]
    out = {"faixa_sementes_de_cena": cena, "faixa_sementes_de_treino": treino,
           "largura_cena": round(fc, 4), "largura_treino": round(ft, 4), "C_ii": c2,
           "regra": "PLANO 3.8: descritivo, faixa de cena (21, 22, 23) ao lado da de treino; C-ii: S-oblique-six nas tres sementes "
                    "de cena contra S-oblique nas tres de treino, (a), (b) pareada nas medias, (c); C-ii falha em (a) -> a frase "
                    "de seis sitios contra um diz que o valor de um sitio cai dentro da faixa de cena; faixa de cena mais que o "
                    "dobro da de treino -> o cenario domina a dispersao"}
    v = [f"C-ii leituras {c2['passou_em']}"]
    if c2["a_ok"] is False:
        v.append("C-ii falha em (a): o valor de um sitio cai dentro da faixa de cena")
    if ft > 0 and fc > 2 * ft:
        v.append("faixa de cena mais que o dobro da de treino: o cenario domina a dispersao; 15,3% lidos com essa faixa")
    out["veredito"] = "; ".join(v)
    return out


# ------------------------------------------------------------------ regra de IoU
def item_iou():
    d = le("visdrone_oficial_iou.json")
    sel = le("rodada5_ft_selecao.json")
    if not d:
        return {"veredito": "pendente"}
    m = d["modelos"]
    pares = [("S principal", ["s_obliquo", "s_obliquo_sd1", "s_obliquo_sd2"], ["s_nadir_4k", "s_nadir_4k_sd1", "s_nadir_4k_sd2"]),
             ("A 152 vs 30", ["s_oblvar", "s_oblvar_sd1", "s_oblvar_sd2"], ["s_oblvar_c030", "s_oblvar_c030_sd1", "s_oblvar_c030_sd2"]),
             ("C-ii", ["s_oblvar", "s_oblvar_e22", "s_oblvar_e23"], ["s_obliquo", "s_obliquo_sd1", "s_obliquo_sd2"])]
    if sel:
        for f in ("05", "10"):
            ga = sel["runs"][f]["coco"][sel["escolha"][f]["coco"]]
            gb = sel["runs"][f]["sint"][sel["escolha"][f]["sint"]]
            pares.append((f"F {f}% escolhidos", [ga], [gb]))
    out, muda = {}, []
    for regra in ("padrao_ultralytics", "regra_oficial"):
        for nome, a, b in pares:
            a = [x for x in a if x in m]
            b = [x for x in b if x in m]
            if not a or not b:
                continue
            dif = {lim: stt.mean(m[x][regra][lim] for x in a) - stt.mean(m[x][regra][lim] for x in b) for lim in ("mAP50", "AP60", "AP75")}
            troca = len({v > 0 for v in dif.values()}) > 1
            out[f"{regra}: {nome}"] = {k: round(v, 4) for k, v in dif.items()} | {"a": a, "b": b, "ordem_muda": troca}
            if troca:
                muda.append(f"{regra}: {nome}")
    return {"pares": out, "ordens_que_mudam": muda,
            "regra": "regra da rodada 4: par cuja ordem muda entre 0,50, 0,60 e 0,75 vai ao texto nos tres limiares",
            "veredito": "ordem estavel nos tres limiares" if not muda else "ordem muda em: " + "; ".join(muda)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parte", choices=["prioridade", "tudo"], default="tudo")
    a = ap.parse_args()
    anterior = le("rodada5_criterios.json") or {}
    out = {"plano": "03-blender/PLANO-RODADA5.md", "parte": a.parte,
           "R5-1_sementes_S": item_s(), "R5-5_ajuste_fino_F": item_f(), "R5-6_base_nadir_N": item_n()}
    if a.parte == "tudo":
        out.update({"R5-3_curva_A": item_a(), "R5-4_sol_duro_D": item_d(), "R5-7_150m_M": item_m(),
                    "R5-2_cena_C": item_c(), "iou_0.50_0.60_0.75": item_iou()})
    else:
        for k in ("R5-3_curva_A", "R5-4_sol_duro_D", "R5-7_150m_M", "R5-2_cena_C", "iou_0.50_0.60_0.75"):
            if k in anterior:
                out[k] = anterior[k]
    json.dump(out, open(os.path.join(AQUI, "rodada5_criterios.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for k, v in out.items():
        if isinstance(v, dict):
            print(k, "->", json.dumps(v.get("veredito"), ensure_ascii=False))


if __name__ == "__main__":
    main()
