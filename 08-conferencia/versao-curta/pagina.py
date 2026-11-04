#!/usr/bin/env python3
"""pagina.py: fecha os buracos no pé das páginas movendo a figura ou tabela que pulou para a página
seguinte para depois do parágrafo que vem logo após ela. O texto não muda; só a posição dos blocos.
Rodar depois de qualquer edição de texto e antes de gera_pdf.sh.

Uso (Mac; no desktop o Edge é encontrado sozinho; precisa de pdfinfo e pdftotext, do poppler, no PATH):
  python3 pagina.py versao-curta-aim2027.html                       # Carta, nota nas páginas 1 e 2
  python3 pagina.py versao-curta-elsevier.html --fundo 779 --primeira 1   # A4 em duas colunas
  python3 pagina.py entrada.html saida.html

--fundo é a borda inferior do texto em pt (Carta com margem de 1 pol.: 792 - 72 = 720; A4 do formato
Elsevier com margem inferior de 2,2 cm: 842 - 62 = 779). --primeira é a primeira página medida (3 na
versão AIM, porque as duas primeiras são a nota de trabalho). Buraco é mais de --limiar pt em branco
(100 pt, cerca de quatro linhas em espaço duplo); a última página não conta.
Uma tabela que não puder ser movida sem cruzar duas subseções pode receber
style="page-break-inside: auto;" com a primeira linha em <thead> (feito na Tabela 11) para quebrar
entre páginas com o cabeçalho repetido. Blocos embrulhados em <div class="full"> (formato Elsevier,
atravessam as duas colunas) são tratados como a figura ou tabela que contêm."""
import argparse, os, re, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out", nargs="?")
ap.add_argument("--fundo", type=float, default=720.0)
ap.add_argument("--primeira", type=int, default=3)
ap.add_argument("--limiar", type=float, default=100.0)
args = ap.parse_args()
SRC = args.src; OUT = args.out or SRC
AQUI = os.path.dirname(os.path.abspath(SRC))
FUNDO, PRIMEIRA, LIMIAR = args.fundo, args.primeira, args.limiar
NAVEGADORES = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
               r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
               "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
NAV = next((p for p in NAVEGADORES if os.path.exists(p)), None) or sys.exit("nenhum Edge ou Chrome encontrado")

html = open(SRC, encoding="utf-8").read()
cabeca, resto = html.split("<!-- MANUSCRITO", 1)
fim_marca = resto.index("-->") + 3
cabeca += "<!-- MANUSCRITO" + resto[:fim_marca]
corpo = resto[fim_marca:]
i_fim = corpo.index("</body>")
corpo, cauda = corpo[:i_fim], corpo[i_fim:]

TOKEN = re.compile(r'<h[1-4]>.*?</h[1-4]>|<figure>.*?</figure>|<table class="t[^"]*"[^>]*>.*?</table>|'
                   r'<p[^>]*>.*?</p>|<div class="[^"]+">.*?</div>|<!--.*?-->|\s+', re.S)
toks = TOKEN.findall(corpo)
assert "".join(toks) == corpo, "o tokenizador não cobre o corpo: há marcação fora do padrão"

def tipo(t):
    if t.startswith('<div class="full">'):
        return "fig" if "<figure" in t else ("tab" if "<table" in t else "outro")
    if t.startswith("<figure"): return "fig"
    if t.startswith("<table"): return "tab"
    if t.startswith('<p class="tn"'): return "tn"
    if t.startswith("<p"): return "p"
    if t.startswith("<h"): return "h"
    if t.strip() == "": return "ws"
    return "outro"

TMP = tempfile.mkdtemp()
PDF = os.path.join(TMP, "pagina.pdf")

def renderiza(tokens):
    # as figuras são relativas à pasta do HTML de origem; o temporário fica em outra pasta
    raiz = os.path.abspath(os.path.join(AQUI, "../..")).replace("\\", "/")
    h = (cabeca + "".join(tokens) + cauda).replace('src="../../', 'src="file://' + raiz + "/")
    tmp_html = os.path.join(TMP, "pagina.html")
    open(tmp_html, "w", encoding="utf-8").write(h)
    subprocess.run([NAV, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={PDF}",
                    "file:///" + tmp_html.replace("\\", "/").lstrip("/")], capture_output=True, timeout=300)

def paginas():
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout).group(1))

def branco(p):
    t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-bbox-layout", PDF, "-"], capture_output=True, text=True).stdout
    ys = [float(y) for y in re.findall(r'<line xMin="[\d.]+" yMin="[\d.]+" xMax="[\d.]+" yMax="([\d.]+)"', t) if float(y) < FUNDO + 15]
    return FUNDO - max(ys) if ys else FUNDO

def primeira_legenda(p):
    t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", PDF, "-"], capture_output=True, text=True).stdout
    for ln in t.splitlines():
        if ln.strip():
            m = re.match(r"\s*(Table|Figure) (\d+)\.", ln)
            return (m.group(1), int(m.group(2))) if m else ln.strip()[:60]

def acha_bloco(tokens, rotulo, n):
    marca = "<b>%s %d.</b>" % (rotulo, n)
    return next((i for i, t in enumerate(tokens) if tipo(t) in ("fig", "tab") and marca in t), None)

def acha_bloco_apos_titulo(tokens, texto):
    """a página seguinte começa com um título: o título pulou junto com a figura ou tabela que vem
    logo depois dele (em duas colunas, a fila entre dois blocos largos sobe inteira). Devolve essa
    figura ou tabela, se existir antes do próximo título."""
    chave = re.sub(r"\s+", " ", texto)[:25]
    for i, t in enumerate(tokens):
        if tipo(t) == "h" and re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip().startswith(chave):
            for k in range(i + 1, len(tokens)):
                if tipo(tokens[k]) == "h": return None
                if tipo(tokens[k]) in ("fig", "tab"): return k
    return None

def move_depois_do_proximo_p(tokens, i):
    """move o bloco i (e a nota da tabela) para depois do próximo parágrafo, cruzando no máximo um título"""
    j = i + 1; bloco = [i]
    while j < len(tokens) and tipo(tokens[j]) in ("ws", "tn"):
        if tipo(tokens[j]) == "tn": bloco.append(j)
        j += 1
    cruzados = 0; k = j
    while k < len(tokens):
        td = tipo(tokens[k])
        if td == "p": break
        if td == "h":
            cruzados += 1
            if cruzados > 1: return None
        if td == "outro": return None
        k += 1
    if k >= len(tokens): return None
    movidos = [tokens[b] for b in bloco]
    novo = [t for idx, t in enumerate(tokens) if idx not in bloco]
    k2 = k - sum(1 for b in bloco if b < k)
    return novo[:k2 + 1] + ["\n\n"] + movidos + novo[k2 + 1:]

def move_antes_do_paragrafo_anterior(tokens, i):
    """plano B, quando não dá para avançar: recua o bloco para antes do parágrafo anterior (e do
    título colado a ele), desde que a primeira menção ao bloco continue antes dele"""
    j = i + 1; bloco = [i]
    while j < len(tokens) and tipo(tokens[j]) in ("ws", "tn"):
        if tipo(tokens[j]) == "tn": bloco.append(j)
        j += 1
    k = i - 1
    while k >= 0 and tipo(tokens[k]) != "p":
        if tipo(tokens[k]) in ("h", "outro"): return None
        k -= 1
    if k < 0: return None
    h = k - 1
    while h >= 0 and tipo(tokens[h]) == "ws": h -= 1
    if h >= 0 and tipo(tokens[h]) == "h": k = h
    m = re.search(r"<b>(Table|Figure) (\d+)\.</b>", tokens[i])
    antes = re.sub(r"<[^>]+>", " ", "".join(tokens[:k]))
    if not re.search(r"\b%ss? [^.;]*\b%s\b" % (m.group(1), m.group(2)), antes): return None
    movidos = [tokens[b] for b in bloco]
    novo = [t for idx, t in enumerate(tokens) if idx not in bloco]
    return novo[:k] + movidos + ["\n\n"] + novo[k:]

def mede(tokens):
    """renderiza e devolve (páginas, buracos, pontuação); a pontuação só cai quando o layout melhora"""
    renderiza(tokens)
    n = paginas()
    buracos = [(p, b) for p in range(PRIMEIRA, n) for b in [branco(p)] if b > LIMIAR]
    return n, buracos, n * 1000 + sum(b for _, b in buracos)

def cadeia(tokens, nome, fn, passos=4):
    """estados sucessivos movendo o mesmo bloco um parágrafo por vez, sem cruzar mais de um título
    no total: às vezes só o terceiro parágrafo fecha o buraco"""
    rot, num = nome.split(); num = int(num)
    i0 = acha_bloco(tokens, rot, num)
    h0 = sum(1 for t in tokens[:i0] if tipo(t) == "h")
    estados, atual = [], tokens
    for _ in range(passos):
        i = acha_bloco(atual, rot, num)
        prox = fn(atual, i) if i is not None else None
        if prox is None: break
        i1 = acha_bloco(prox, rot, num)
        if abs(sum(1 for t in prox[:i1] if tipo(t) == "h") - h0) > 1: break
        estados.append(prox); atual = prox
    return estados

# busca gulosa com até quatro passos de antevisão: um movimento só é aceito se baixar a pontuação
# (menos páginas ou menos branco), o que impede o vaivém de um bloco que não cabe em lugar nenhum
rejeitados = set()
n, buracos, pont = mede(toks)
for rodada in range(40):
    print(f"rodada {rodada}: {n} páginas, buracos:", [(p, round(b)) for p, b in buracos])
    if not buracos: break
    aceito = False
    for p, b in buracos:
        leg = primeira_legenda(p + 1)
        if isinstance(leg, tuple): i = acha_bloco(toks, *leg)
        elif leg and re.match(r"\d+(\.\d+)* ", leg): i = acha_bloco_apos_titulo(toks, leg)
        else: i = None
        if i is None:
            print(f"  página {p}: a seguinte começa com texto ({str(leg)[:40]!r}); fica como está"); continue
        nome = re.search(r"<b>((?:Table|Figure) \d+)\.</b>", toks[i]).group(1)
        for sentido, fn in (("depois do parágrafo seguinte", move_depois_do_proximo_p),
                            ("antes do parágrafo anterior", move_antes_do_paragrafo_anterior)):
            if (nome, sentido, i) in rejeitados: continue
            for passo, novo in enumerate(cadeia(toks, nome, fn), 1):
                n2, buracos2, pont2 = mede(novo)
                if pont2 < pont:
                    toks, n, buracos, pont = novo, n2, buracos2, pont2; aceito = True
                    print(f"  página {p}: {nome} movida {passo} parágrafo(s) para {sentido}"); break
            if aceito: break
            rejeitados.add((nome, sentido, i))
            print(f"  página {p}: {nome} para {sentido} não melhora; descartado")
        if aceito: break
    if not aceito:
        print("  nenhum movimento melhora o layout; parando"); break
open(OUT, "w", encoding="utf-8").write(cabeca + "".join(toks) + cauda)
print("gravado", OUT, "com", n, "páginas e", len(buracos), "buraco(s) acima de", int(LIMIAR), "pt")
