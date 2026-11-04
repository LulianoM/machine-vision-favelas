#!/usr/bin/env python3
"""pagina.py: fecha os buracos no pé das páginas da versão curta movendo a figura ou tabela que
pulou para a página seguinte para depois do parágrafo que vem logo após ela. O texto não muda;
só a posição dos blocos. Rodar depois de qualquer edição de texto e antes de gera_pdf.sh.

Uso (Mac; no desktop trocar o navegador abaixo e ter o poppler no PATH):
  python3 pagina.py versao-curta-aim2027.html            # reescreve o próprio arquivo
  python3 pagina.py entrada.html saida.html

Precisa de pdfinfo e pdftotext (poppler). Critério: buraco é mais de 100 pt em branco acima da
margem inferior (cerca de quatro linhas em espaço duplo); a última página e a nota não contam.
Uma tabela que não puder ser movida sem cruzar duas subseções pode receber
style="page-break-inside: auto;" com a primeira linha em <thead> (feito na Tabela 11) para quebrar
entre páginas com o cabeçalho repetido."""
import os, re, subprocess, sys, tempfile

SRC = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else SRC
AQUI = os.path.dirname(os.path.abspath(SRC))
LIMIAR = 100.0   # pt de branco no pé da página que conta como buraco
FUNDO = 720.0    # borda inferior do texto em Carta com margem de 1 pol. (792 - 72)
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
    h = (cabeca + "".join(tokens) + cauda).replace('src="../../', 'src="file://' + os.path.abspath(os.path.join(AQUI, "../..")).replace("\\", "/") + "/")
    tmp_html = os.path.join(TMP, "pagina.html")
    open(tmp_html, "w", encoding="utf-8").write(h)
    subprocess.run([NAV, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={PDF}",
                    "file:///" + tmp_html.replace("\\", "/").lstrip("/")], capture_output=True, timeout=300)

def paginas():
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout).group(1))

def branco(p):
    t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-bbox-layout", PDF, "-"], capture_output=True, text=True).stdout
    ys = [float(y) for y in re.findall(r'<line xMin="[\d.]+" yMin="[\d.]+" xMax="[\d.]+" yMax="([\d.]+)"', t) if float(y) < 735]
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

for rodada in range(20):
    renderiza(toks)
    n = paginas()
    buracos = [(p, branco(p)) for p in range(3, n)]
    buracos = [(p, b) for p, b in buracos if b > LIMIAR]
    print(f"rodada {rodada}: {n} páginas, buracos:", [(p, round(b)) for p, b in buracos])
    if not buracos: break
    moveu = False
    for p, b in buracos:
        leg = primeira_legenda(p + 1)
        if not isinstance(leg, tuple):
            print(f"  página {p}: a seguinte começa com texto ({leg!r}); fica como está"); continue
        i = acha_bloco(toks, *leg)
        novo = move_depois_do_proximo_p(toks, i) if i is not None else None
        if novo is None:
            print(f"  página {p}: não dá para mover {leg[0]} {leg[1]} sem cruzar duas seções"); continue
        toks = novo; moveu = True
        print(f"  página {p}: {leg[0]} {leg[1]} movida para depois do parágrafo seguinte"); break
    if not moveu: break
open(OUT, "w", encoding="utf-8").write(cabeca + "".join(toks) + cauda)
print("gravado", OUT, "com", paginas(), "páginas")
