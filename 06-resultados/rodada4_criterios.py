#!/usr/bin/env python3
"""
rodada4_criterios.py: aplica os criterios que 07-blender/PLANO-RODADA4.md fixou antes da rodada 4.

Le so arquivos de 06-resultados e grava rodada4_criterios.json. Cada item tem as medidas, a regra e o
veredito; item cujo arquivo ainda nao existe sai como "pendente". Nenhuma regra e escolhida aqui: elas
estao no plano, versionado antes do primeiro resultado, e este script so as executa.

  python rodada4_criterios.py
"""
import json
import math
import os
import random
import statistics as stt
from collections import defaultdict
from statistics import NormalDist

AQUI = os.path.dirname(os.path.abspath(__file__))
N = NormalDist()
R_PAREADO = "r_pareado"


def le(nome):
    p = os.path.join(AQUI, nome)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def map50(nome):
    d = le(f"sim2real_{nome}.json")
    if not d:
        return None
    return next((r.get("metrics/mAP50(B)") for r in d["resultados"] if r.get("conjunto") == "real"), None)


def binom_bilateral(b, c):
    """teste exato de McNemar: p bilateral de b discordantes num lado entre b + c"""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    cauda = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * cauda)


def duas_prop(k1, n1, k2, n2):
    p = (k1 + k2) / (n1 + n2)
    ep = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2)) or 1e-9
    z = (k2 / n2 - k1 / n1) / ep
    return round(z, 2), round(2 * (1 - N.cdf(abs(z))), 4)


def dlinha(hit_k, hit_n, fa_k, fa_n):
    """d' com correcao log-linear ((k + 0,5) / (n + 1)), definida mesmo com taxa 0 ou 1"""
    h = (hit_k + 0.5) / (hit_n + 1)
    f = (fa_k + 0.5) / (fa_n + 1)
    return N.inv_cdf(h) - N.inv_cdf(f)


def instancias(d):
    """quadro -> lista de (classe, coluna); coluna 0 = chamada de armada, 3 = perdida"""
    q = defaultdict(list)
    for base, gi, c, tipo, col in d.get("instancias", []):
        q[base].append((c, col, tipo, gi))
    return q


def taxas_quadros(q, quadros):
    k = defaultdict(int)
    n = defaultdict(int)
    for b in quadros:
        for c, col, _, _ in q[b]:
            n[c] += 1
            k[c] += col == 0
    return k, n


def perfil_altitude(nome_arq):
    """taxas, d' (armada contra objeto e contra desarmada) e IC por bootstrap de quadros"""
    d = le(nome_arq)
    if not d or "instancias" not in d:
        return None
    q = instancias(d)
    quadros = sorted(q)
    k, n = taxas_quadros(q, quadros)
    tot = sum(n.values())
    perdidas = sum(1 for b in quadros for c, col, _, _ in q[b] if col == 3)
    rnd = random.Random(0)
    bs_o, bs_d = [], []
    for _ in range(2000):
        amostra = [quadros[rnd.randrange(len(quadros))] for _ in quadros]
        kb, nb = taxas_quadros(q, amostra)
        if nb[0] and nb[2]:
            bs_o.append(dlinha(kb[0], nb[0], kb[2], nb[2]))
        if nb[0] and nb[1]:
            bs_d.append(dlinha(kb[0], nb[0], kb[1], nb[1]))
    bs_o.sort()
    bs_d.sort()

    def ic(v):
        return [round(v[int(0.025 * len(v))], 3), round(v[int(0.975 * len(v)) - 1], 3)] if v else None

    return {"quadros": len(quadros), "pessoas": tot,
            "recall_deteccao_qualquer_classe": round(1 - perdidas / max(1, tot), 4),
            "chamada_de_armada": {nome: {"k": k[c], "n": n[c], "taxa": round(k[c] / max(1, n[c]), 4)}
                                  for c, nome in ((0, "armada"), (1, "desarmada"), (2, "objeto"))},
            "dlinha_armada_contra_objeto": round(dlinha(k[0], n[0], k[2], n[2]), 3),
            "dlinha_armada_contra_objeto_ic95": ic(bs_o),
            "dlinha_armada_contra_desarmada": round(dlinha(k[0], n[0], k[1], n[1]), 3),
            "dlinha_armada_contra_desarmada_ic95": ic(bs_d)}


def item_iou():
    """10.6, convencao de anotacao: a ordem dos modelos muda com o limiar de IoU?"""
    d = le("visdrone_oficial_iou.json")
    if not d:
        return {"veredito": "pendente"}
    m = d["modelos"]
    pares = [("r_pareado", "s_oblvar"), ("s_oblvar", "s_obliquo"), ("s_obliquo", "s_nadir_4k"),
             ("s_variedade", "s_nadir_4k"), ("ft05_coco", "ft05_sint"), ("ft10_coco", "ft10_sint"),
             ("misto05", "ft05_coco"), ("misto10", "ft10_coco")]
    out = {"pares": {}, "eficacia": {}}
    muda = []
    for regra in ("padrao_ultralytics", "regra_oficial"):
        for a, b in pares:
            if a not in m or b not in m:
                continue
            sinais = {lim: m[a][regra][lim] - m[b][regra][lim] for lim in ("mAP50", "AP60", "AP75")}
            troca = len({v > 0 for v in sinais.values()}) > 1
            out["pares"][f"{regra}: {a} - {b}"] = {k: round(v, 4) for k, v in sinais.items()} | {"ordem_muda": troca}
            if troca:
                muda.append(f"{regra}: {a} x {b}")
        if R_PAREADO in m:
            for s in ("s_nadir_4k", "s_variedade", "s_obliquo", "s_oblvar", "s_oblvar_sd1", "s_oblvar_sd2"):
                if s in m:
                    out["eficacia"].setdefault(s, {})[regra] = {
                        lim: round(m[s][regra][lim] / m[R_PAREADO][regra][lim], 4) for lim in ("mAP50", "AP60", "AP75")}
    arm = {}
    for nome in ("armado_75", "armado_35", "armado_75g"):
        linha = {}
        for suf, lim in (("", "0.50"), ("_iou60", "0.60"), ("_iou75", "0.75")):
            c = le(f"confusao_{nome}{suf}.json")
            if c:
                linha[lim] = c["taxa_por_classe_real"]["objeto"]["armada"]
        arm[nome] = linha
    ordens = {}
    for lim in ("0.50", "0.60", "0.75"):
        v = {n: arm[n].get(lim) for n in arm if arm[n].get(lim) is not None}
        if len(v) == 3:
            ordens[lim] = sorted(v, key=v.get, reverse=True)
    out["objeto_chamado_de_armada_por_limiar"] = arm
    out["ordem_armados_por_limiar"] = ordens
    if len(set(tuple(o) for o in ordens.values())) > 1:
        muda.append("armados: ordem da taxa de objeto chamado de armada")
    out["ordens_que_mudam"] = muda
    out["regra"] = "se a ordem de um par muda entre 0,50, 0,60 e 0,75, esse par e artefato de anotacao e vai ao texto nos tres limiares"
    out["veredito"] = ("ordem estavel nos tres limiares" if not muda else "ordem muda em: " + "; ".join(muda))
    return out


def item_escala():
    e = le("escala_casada.json")
    prot, cas = map50("s_nadir_4k"), map50("s_nadir_4k_casada")
    rp, rc = map50("r_pareado"), map50("r_pareado_casada")
    if not e or cas is None:
        return {"veredito": "pendente"}
    rel = abs(cas - prot) / prot
    return {"imgsz_casado": e["imgsz_casado"], "no_protocolo": e["no_protocolo"], "no_casado": e["no_casado"],
            "s_nadir_4k_mAP50_protocolo": prot, "s_nadir_4k_mAP50_casado": cas, "diferenca_relativa": round(rel, 3),
            "r_pareado_mAP50_protocolo": rp, "r_pareado_mAP50_casado": rc,
            "eficacia_protocolo": round(prot / rp, 4) if rp else None,
            "eficacia_casada": round(cas / rc, 4) if rc else None,
            "regra": "diverge substancialmente se a diferenca relativa passar de 50%; ai a razao da 9.2 vai so na escala casada",
            "veredito": "diverge substancialmente: escala e confusor vivo" if rel > 0.5 else "nao diverge substancialmente"}


def item_porte(modelo):
    a, b = le(f"holdout_armas_{modelo}_inst.json"), le(f"porte_arma_{modelo}.json")
    g = le("porte_arma_gemeo.json")
    if not a or not b or not g:
        return {"veredito": "pendente"}
    qa, qb = instancias(a), instancias(b)
    diferentes = set(g.get("quadros_diferentes", []))
    pares = []
    for base in qa:
        if base + ".png" in diferentes or base not in qb or len(qa[base]) != len(qb[base]):
            continue
        for (c1, col1, t1, gi1), (c2, col2, t2, gi2) in zip(sorted(qa[base], key=lambda x: x[3]), sorted(qb[base], key=lambda x: x[3])):
            if c1 == c2 == 2 and t1 == t2:
                pares.append((t1, col1 == 0, col2 == 0))
    bcnt = sum(1 for _, x, y in pares if y and not x)
    ccnt = sum(1 for _, x, y in pares if x and not y)
    por_tipo = defaultdict(lambda: [0, 0, 0])
    for t, x, y in pares:
        por_tipo[t][0] += 1
        por_tipo[t][1] += x
        por_tipo[t][2] += y
    n = len(pares)
    ra = sum(x for _, x, _ in pares) / max(1, n)
    rb = sum(y for _, _, y in pares) / max(1, n)
    p = binom_bilateral(bcnt, ccnt)
    ta, tb = a["taxa_por_classe_real"]["objeto"], b["taxa_por_classe_real"]["objeto"]
    out = {"objetos_pareados": n, "taxa_porte_normal": round(ra, 4), "taxa_porte_de_arma": round(rb, 4),
           "discordantes_so_no_porte_de_arma": bcnt, "discordantes_so_no_normal": ccnt, "p_mcnemar_exato": round(p, 4),
           "por_tipo": {t: {"n": v[0], "normal": round(v[1] / v[0], 3), "porte_de_arma": round(v[2] / v[0], 3)}
                        for t, v in sorted(por_tipo.items())},
           "nao_pareado": {"normal": ta, "porte_de_arma": tb},
           "regra": "se a taxa sobe no porte de arma com McNemar p < 0,05, o texto passa a dar a taxa medida no porte de arma; senao a ressalva do angulo de porte sai"}
    out["veredito"] = ("sobe: reportar a taxa no porte de arma" if rb > ra and p < 0.05
                       else "nao sobe de forma resolvivel: retirar a ressalva do angulo")
    return out


def item_misto():
    m5, m10 = map50("misto05"), map50("misto10")
    c = [map50("ft05_coco"), map50("ft05_coco_sd1"), map50("ft05_coco_sd2")]
    if m5 is None:
        return {"veredito": "pendente"}
    c = [x for x in c if x is not None]
    dp = stt.stdev(c) if len(c) >= 2 else None
    out = {"misto05": m5, "misto10": m10, "ft05_coco": map50("ft05_coco"), "ft10_coco": map50("ft10_coco"),
           "ft05_sint": map50("ft05_sint"), "ft10_sint": map50("ft10_sint"),
           "dp_entre_sementes_ft05_coco": round(dp, 4) if dp is not None else None,
           "regra": "misto melhor que so real se a diferenca passar de 2 dp entre sementes do ft05_coco; pior se ficar abaixo de -2 dp (a 10% usa o mesmo dp, declarado como aproximacao)"}
    vered = {}
    for nome, mv, ref in (("5%", m5, map50("ft05_coco")), ("10%", m10, map50("ft10_coco"))):
        if mv is None or ref is None or dp is None:
            vered[nome] = "pendente"
            continue
        dif = mv - ref
        vered[nome] = (f"misto melhor ({dif:+.4f})" if dif > 2 * dp else f"misto pior ({dif:+.4f})" if dif < -2 * dp
                       else f"sem diferenca resolvivel ({dif:+.4f}, 2 dp = {2 * dp:.4f})")
    out["veredito"] = vered
    return out


def item_150():
    p150 = perfil_altitude("confusao_armado_150g.json")
    if not p150:
        return {"veredito": "pendente"}
    curva = {"35 m": perfil_altitude("confusao_armado_35_inst.json"),
             "75 m gemeo": perfil_altitude("confusao_armado_75g_inst.json"), "150 m gemeo": p150}
    valido = p150["recall_deteccao_qualquer_classe"] >= 0.5
    ic = p150["dlinha_armada_contra_objeto_ic95"]
    if not valido:
        v = "nao interpretavel: o modelo de 150 m nao aprendeu o proprio dominio (recall de deteccao < 0,5)"
    elif ic and ic[0] <= 0 <= ic[1]:
        v = "ausente, medida: o IC 95% de d' (armada contra objeto) inclui 0"
    else:
        v = "separacao acima do acaso no sintetico: o IC 95% de d' exclui 0 (a arma e argumentada irresolvivel a 150 m, entao a separacao usa outro indicio)"
    return {"curva_de_altitude": curva,
            "regra": "validade: recall de deteccao >= 0,5; ausencia medida se o IC 95% (bootstrap de quadros) de d' armada contra objeto incluir 0",
            "veredito": v}


def item_val_maior():
    a, b = perfil_altitude("extra_armado_35.json"), perfil_altitude("extra_armado_75g.json")
    if not a or not b:
        return {"veredito": "pendente"}
    oa, ob = a["chamada_de_armada"]["objeto"], b["chamada_de_armada"]["objeto"]
    z, p = duas_prop(ob["k"], ob["n"], oa["k"], oa["n"])
    out = {"35 m": a, "75 m gemeo": b, "objeto_35_menos_75g": round(oa["taxa"] - ob["taxa"], 4), "z": z, "p_bilateral": p}
    g35, g75 = le("gemeo_75_35.json") or {}, None
    if g35:
        t35 = g35["modelos"]["armado_35"]["taxas"]["objeto"]
        t75 = g35["modelos"]["armado_75g"]["taxas"]["objeto"]
        zc, pc = duas_prop(t75["chamada_armada"] + ob["k"], t75["n"] + ob["n"], t35["chamada_armada"] + oa["k"], t35["n"] + oa["n"])
        out["somado_ao_val_original"] = {"35 m": [t35["chamada_armada"] + oa["k"], t35["n"] + oa["n"]],
                                         "75 m gemeo": [t75["chamada_armada"] + ob["k"], t75["n"] + ob["n"]], "z": zc, "p_bilateral": pc}
    out["regra"] = ("so os quadros novos: 35 m acima do gemeo com p bilateral < 0,05 = estabelecida; direcao invertida = retirar "
                    "'a resolucao mais fina nao reduziu a confusao'; o resto = continua sugestiva")
    out["veredito"] = ("estabelecida" if oa["taxa"] > ob["taxa"] and p < 0.05 else
                       "invertida: retirar a frase" if oa["taxa"] < ob["taxa"] else "continua sugestiva")
    return out


def faixa(v):
    v = [x for x in v if x is not None]
    if not v:
        return None
    return {"valores": v, "media": round(stt.mean(v), 4), "dp": round(stt.stdev(v), 4) if len(v) > 1 else None,
            "min": min(v), "max": max(v)}


def separado(a, b):
    if not a or not b or len(a["valores"]) < 3 or len(b["valores"]) < 3:
        return "pendente"
    return "resolvivel (faixas nao se sobrepoem)" if a["max"] < b["min"] or b["max"] < a["min"] else "nao resolvivel (faixas se sobrepoem)"


def item_sementes():
    so = faixa([map50("s_oblvar"), map50("s_oblvar_sd1"), map50("s_oblvar_sd2")])
    fs = faixa([map50("ft05_sint"), map50("ft05_sint_sd1"), map50("ft05_sint_sd2")])
    fc = faixa([map50("ft05_coco"), map50("ft05_coco_sd1"), map50("ft05_coco_sd2")])

    def obj(arq):
        d = le(arq)
        return d["taxa_por_classe_real"]["objeto"]["armada"] if d else None

    a35 = faixa([obj("confusao_armado_35.json"), obj("confusao_armado_35_sd1.json"), obj("confusao_armado_35_sd2.json")])
    a75 = faixa([obj("confusao_armado_75g.json"), obj("confusao_armado_75g_sd1.json"), obj("confusao_armado_75g_sd2.json")])
    e35 = faixa([obj("extra_armado_35.json"), obj("extra_armado_35_sd1.json"), obj("extra_armado_35_sd2.json")])
    e75 = faixa([obj("extra_armado_75g.json"), obj("extra_armado_75g_sd1.json"), obj("extra_armado_75g_sd2.json")])
    r = map50("r_pareado")
    return {"s_oblvar_mAP50": so, "eficacia_s_oblvar": round(so["media"] / r, 4) if so and r else None,
            "ft05_sint": fs, "ft05_coco": fc, "ft05_sint_x_coco": separado(fs, fc),
            "objeto_armada_35_val": a35, "objeto_armada_75g_val": a75, "35_x_75g_val": separado(a35, a75),
            "objeto_armada_35_quadros_novos": e35, "objeto_armada_75g_quadros_novos": e75,
            "35_x_75g_quadros_novos": separado(e35, e75),
            "regra": "tres treinos por modelo (semente 0 original, 1 e 2); diferenca resolvivel se as faixas min-max nao se sobrepoem",
            "veredito": {"ft05": separado(fs, fc), "35_x_75g": separado(a35, a75)}}


def main():
    out = {"plano": "07-blender/PLANO-RODADA4.md",
           "10.6_iou_e_visdrone_oficial": item_iou(),
           "10.2_escala_casada": item_escala(),
           "9.5_objeto_no_porte_de_arma": {"armado_75": item_porte("armado_75"), "armado_75g": item_porte("armado_75g")},
           "9.4_misto": item_misto(),
           "11.5_150m": item_150(),
           "9.5_validacao_maior": item_val_maior(),
           "10.3_por_regime": (le("por_regime_s_nadir_4k.json") or {}).get("criterio_10_3", {"veredito": "pendente"}),
           "10.6_sementes": item_sementes()}
    json.dump(out, open(os.path.join(AQUI, "rodada4_criterios.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for k, v in out.items():
        if isinstance(v, dict):
            print(k, "->", v.get("veredito", {kk: vv.get("veredito") for kk, vv in v.items() if isinstance(vv, dict)}))


if __name__ == "__main__":
    main()
