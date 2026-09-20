#!/usr/bin/env python3
"""
busca_crossref.py: procura no Crossref as obras citadas no texto que não têm entrada na lista.

Regra dura do projeto: DOI só entra depois de conferido, e nunca se inventa.

Lição que originou a versão 2 deste script. A versão 1 montava a consulta a partir do que EU
supunha ser o assunto de cada obra, e casava por sobrenome mais ano. Isso produziu uma
correspondência classificada como forte para "Xu (2025)" apontando para um artigo de
sensoriamento remoto, quando no texto Xu (2025) compara RRT, ACO e A* para planejamento de rota.
Sobrenome e ano batendo não é evidência de nada: existem muitos Xu publicando em 2025. Inserir
aquele DOI teria fabricado uma citação, que é pior do que deixar a referência faltando.

A versão 2 monta a consulta a partir do CONTEXTO REAL em que a obra é citada, extraído do próprio
manuscrito, e exige que o título devolvido tenha sobreposição de vocabulário com esse contexto.
Ainda assim não decide sozinha: a saída é uma lista de candidatos para conferência humana.

Uso:
  python busca_crossref.py --json candidatos.json
  python busca_crossref.py --ctx 260
"""
import argparse
import glob
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MAN = os.path.join(RAIZ, "01-artigo", "manuscrito")

# citacoes sem entrada, com o sobrenome do primeiro autor e o ano como aparecem no texto
ALVOS = [
    ("Chen", 2025), ("Rasoulie", 2026), ("Xu", 2025), ("Agrawal", 2017), ("Jiang", 2026),
    ("Wang", 2026), ("Yan", 2025), ("Gevaert", 2016), ("Du", 2024), ("Barisic", 2022),
    ("Horv", 2023), ("Watson", 2025), ("Silva", 2024), ("Sithole", 2025), ("Kiefer", 2022),
]

API = "https://api.crossref.org/works"
UA = "machine-vision-favelas/1.0 (mailto:martinslucianofigueira@gmail.com)"
VAZIAS = set("""the a an of and or in on for to with by from that this these those is are was were
be been as at it its their his her our we they which who whom whose than then so such not no nor
but if when while where how what why into over under between among during after before above
below up down out off again further once here there all any both each few more most other some
only own same too very can will just should now""".split())


def palavras(t):
    return {w for w in re.findall(r"[a-z]{4,}", t.lower()) if w not in VAZIAS}


def contexto(sobrenome, ano, n):
    """todo trecho do manuscrito em torno de uma citacao daquele autor e ano"""
    pedacos = []
    pat = re.compile(re.escape(sobrenome) + r"[^()]{0,90}?\(" + str(ano) + r"[a-z]?\)")
    pat2 = re.compile(r"\(" + re.escape(sobrenome) + r"[^()]{0,90}?" + str(ano) + r"[a-z]?\)")
    for p in sorted(glob.glob(os.path.join(MAN, "0[1-7]*.md"))):
        s = open(p, encoding="utf-8").read()
        for m in list(pat.finditer(s)) + list(pat2.finditer(s)):
            pedacos.append(s[max(0, m.start() - n): m.end() + n])
    return pedacos


def consulta(q, n=5):
    url = f"{API}?{urllib.parse.urlencode({'query.bibliographic': q, 'rows': n})}"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)["message"]["items"]


def ano_de(it):
    for k in ("published-print", "published-online", "issued", "created"):
        v = it.get(k, {}).get("date-parts", [[None]])[0][0]
        if v:
            return v
    return None


ap = argparse.ArgumentParser()
ap.add_argument("--json", default=None)
ap.add_argument("--ctx", type=int, default=240)
args = ap.parse_args()

saida = []
for sobrenome, ano in ALVOS:
    ctxs = contexto(sobrenome, ano, args.ctx)
    rotulo = f"{sobrenome} ({ano})"
    if not ctxs:
        print(f"\n### {rotulo}  [SEM CONTEXTO]  nao localizei a citacao no manuscrito")
        saida.append(dict(rotulo=rotulo, grau="SEM CONTEXTO"))
        continue
    ctx = " ".join(ctxs)[:900]
    vocab = palavras(ctx)
    q = f"{sobrenome} " + " ".join(sorted(vocab)[:16])
    try:
        itens = consulta(q)
    except Exception as e:
        print(f"[erro] {rotulo}: {e}", file=sys.stderr)
        itens = []

    cands = []
    for it in itens:
        t = (it.get("title") or [""])[0]
        aut = it.get("author") or []
        tem_autor = any(sobrenome.lower() in x.get("family", "").lower() for x in aut)
        y = ano_de(it)
        # sobreposicao de vocabulario entre o TITULO e o contexto da citacao
        sob = len(palavras(t) & vocab) / max(len(palavras(t)), 1)
        cands.append((sob, tem_autor, y, t, it))
    cands.sort(key=lambda c: (c[1], c[0]), reverse=True)

    print(f"\n### {rotulo}")
    print(f"  contexto: ...{ctxs[0][args.ctx - 90:args.ctx + 110].strip()}...")
    if not cands:
        print("  nenhum candidato")
        saida.append(dict(rotulo=rotulo, grau="NADA"))
        continue
    sob, tem_autor, y, t, it = cands[0]
    bate_ano = y is not None and abs(y - ano) <= 1
    grau = ("FORTE" if (tem_autor and bate_ano and sob >= 0.34) else
            "PLAUSIVEL" if (tem_autor and sob >= 0.22) else "FRACO")
    print(f"  [{grau}] sobreposicao de titulo {sob:.2f}, autor {'sim' if tem_autor else 'NAO'}, "
          f"ano {y} contra {ano}")
    print(f"  titulo : {t}")
    print(f"  veiculo: {(it.get('container-title') or [''])[0]}")
    print(f"  DOI    : {it.get('DOI')}")
    saida.append(dict(rotulo=rotulo, grau=grau, doi=it.get("DOI"), titulo=t, ano=y,
                      sobreposicao=round(sob, 2), tem_autor=tem_autor,
                      veiculo=(it.get("container-title") or [""])[0]))
    time.sleep(0.6)

print("\n" + "=" * 72)
for g in ("FORTE", "PLAUSIVEL", "FRACO", "NADA", "SEM CONTEXTO"):
    n = sum(1 for s in saida if s.get("grau") == g)
    if n:
        print(f"{g:<14}{n}")
print("\nNENHUM candidato entra na lista sem leitura humana do titulo contra o contexto.")
print("FORTE significa que o titulo compartilha vocabulario com a frase que cita a obra,")
print("nao que a obra esteja confirmada.")
if args.json:
    json.dump(saida, open(args.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"gravado {args.json}")
