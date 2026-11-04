#!/usr/bin/env python3
"""pagina.py: fecha os buracos de paginação movendo a figura ou tabela que pulou de página (ou de coluna)
para depois do parágrafo que vem logo após ela, ou para antes do parágrafo anterior. O texto não muda;
só a posição dos blocos. Rodar depois de qualquer edição de texto e antes de gera_pdf.sh.

Uso (Mac; no desktop o Edge é encontrado sozinho; precisa de pdfinfo, pdftotext e pdftoppm, do poppler, no PATH):
  python3 pagina.py versao-curta-aim2027.html                             # Carta, coluna única
  python3 pagina.py versao-curta-elsevier.html --colunas 2 --limiar 50    # A4 em duas colunas
  python3 pagina.py entrada.html saida.html

--primeira é a primeira página medida (1 por padrão; se o fonte tiver uma nota de trabalho nas primeiras
páginas, passar a primeira página do manuscrito). A última página nunca conta.
Com --colunas 1 (padrão), o branco de uma página é a distância da última linha de texto até --fundo, a borda
inferior da mancha em pt (Carta com margem de 1 pol.: 792 - 72 = 720). Buraco é mais de --limiar pt
(100 pt, cerca de quatro linhas em espaço duplo).
Com --colunas 2 a página é rasterizada (pdftoppm a 36 dpi, com fundo cinza nas figuras e tabelas só na
medição, para a imagem contar como tinta) e o branco é a soma, nas duas colunas, das faixas brancas de 24 pt
ou mais dentro da mancha: pé de coluna, topo de coluna e o vazio ao lado de uma figura antes de um bloco
largo. A geometria é a do CSS_ELSEVIER (A4, margens 1,9/1,6/2,2/1,6 cm, vão de 6 mm).

Blocos embrulhados em <div class="full"> (atravessam as duas colunas) ou <div class="flt"> (flutuam na
coluna: se não cabem, vão para o topo da coluna seguinte e o texto continua) são tratados como a figura ou
tabela que contêm. Uma tabela que não puder ser movida sem cruzar duas subseções pode receber
style="page-break-inside: auto;" com a primeira linha em <thead> (feito na Tabela 11) para quebrar
entre páginas com o cabeçalho repetido. Títulos consecutivos (h2 seguido de h3) contam como um só ao
limitar quantos títulos um bloco pode cruzar."""
import argparse, os, re, subprocess, sys, tempfile

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out", nargs="?")
ap.add_argument("--fundo", type=float, default=720.0)
ap.add_argument("--primeira", type=int, default=1)
ap.add_argument("--limiar", type=float, default=100.0)
ap.add_argument("--colunas", type=int, default=1, choices=(1, 2))
args = ap.parse_args()
SRC = args.src; OUT = args.out or SRC
AQUI = os.path.dirname(os.path.abspath(SRC))
FUNDO, PRIMEIRA, LIMIAR, COLUNAS = args.fundo, args.primeira, args.limiar, args.colunas
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
    if t.startswith('<div class="'):
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
    if COLUNAS == 2:  # só na medição: figura e tabela viram tinta sólida para o raster
        h = h.replace("</head>", "<style>figure, table { background: #d9d9d9; }</style></head>", 1)
    tmp_html = os.path.join(TMP, "pagina.html")
    open(tmp_html, "w", encoding="utf-8").write(h)
    subprocess.run([NAV, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={PDF}",
                    "file:///" + tmp_html.replace("\\", "/").lstrip("/")], capture_output=True, timeout=300)
    if COLUNAS == 2:
        for f in os.listdir(TMP):
            if f.endswith(".pgm"): os.remove(os.path.join(TMP, f))
        subprocess.run(["pdftoppm", "-r", str(DPI), "-gray", PDF, os.path.join(TMP, "pg")], check=True)

def paginas():
    return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", PDF], capture_output=True, text=True).stdout).group(1))

def branco(p):
    """uma coluna: distância da última linha de texto da página até a borda inferior da mancha"""
    t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-bbox-layout", PDF, "-"], capture_output=True, text=True).stdout
    ys = [float(y) for y in re.findall(r'<line xMin="[\d.]+" yMin="[\d.]+" xMax="[\d.]+" yMax="([\d.]+)"', t) if float(y) < FUNDO + 15]
    return FUNDO - max(ys) if ys else FUNDO

# geometria A4 do CSS_ELSEVIER em pixels a 36 dpi (1 px = 2 pt)
DPI = 36; PT = 72 / DPI; CM = DPI / 2.54
_x0, _x1 = 1.6 * CM, (21.0 - 1.6) * CM; _vao = 0.6 * CM; _larg = (_x1 - _x0 - _vao) / 2
COLS = [(int(_x0), int(_x0 + _larg)), (int(_x0 + _larg + _vao), int(_x1))]
TOPO_PX, FUNDO_PX = int(1.9 * CM), int((29.7 - 2.2) * CM)
FAIXA_MIN = 24  # pt; o maior vão legítimo (parágrafo + título de seção) fica abaixo disso

def branco_colunas(p):
    """duas colunas: soma das faixas brancas de FAIXA_MIN pt ou mais, em cada coluna, dentro da mancha"""
    arq = next(f for f in os.listdir(TMP) if f.startswith("pg-") and f.endswith(".pgm") and int(f[3:-4]) == p)
    raw = open(os.path.join(TMP, arq), "rb").read()
    partes = raw.split(b"\n", 3)
    w = int(partes[1].split()[0]); px = partes[3]
    total = 0.0
    for a, b in COLS:
        corrida = 0
        for y in range(TOPO_PX, FUNDO_PX):
            if min(px[y * w + a:y * w + b]) < 235:
                if corrida * PT >= FAIXA_MIN: total += corrida * PT
                corrida = 0
            else:
                corrida += 1
        if corrida * PT >= FAIXA_MIN: total += corrida * PT
    return total

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

def grupos_h(tokens, ate):
    """títulos antes do índice `ate`, contando títulos consecutivos (h2 seguido de h3) como um só"""
    n = 0; ant = None
    for t in tokens[:ate]:
        tt = tipo(t)
        if tt == "ws": continue
        if tt == "h" and ant != "h": n += 1
        ant = tt
    return n

def move_depois_do_proximo_p(tokens, i):
    """move o bloco i (e a nota da tabela) para depois do próximo parágrafo, cruzando no máximo um grupo de títulos"""
    j = i + 1; bloco = [i]
    while j < len(tokens) and tipo(tokens[j]) in ("ws", "tn"):
        if tipo(tokens[j]) == "tn": bloco.append(j)
        j += 1
    cruzados = 0; k = j; ant = None
    while k < len(tokens):
        td = tipo(tokens[k])
        if td == "p": break
        if td == "h" and ant != "h":
            cruzados += 1
            if cruzados > 1: return None
        if td == "outro": return None
        if td != "ws": ant = td
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

def bloco_que_pulou(tokens, p):
    """índice do bloco que abre a página p + 1 (legenda ou título seguido de figura ou tabela), ou None"""
    leg = primeira_legenda(p + 1)
    if isinstance(leg, tuple): return acha_bloco(tokens, *leg)
    if leg and re.match(r"\d+(\.\d+)* ", leg): return acha_bloco_apos_titulo(tokens, leg)
    return None

def blocos_largos_na_pagina(tokens, p):
    """índices dos blocos largos (<div class="full">) cuja legenda está na página p: em duas colunas,
    um bloco largo no meio da página parte a página em duas filas, e a fila de baixo, curta, é o que
    mais deixa buraco"""
    t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", PDF, "-"], capture_output=True, text=True).stdout
    idx = []
    for rot, num in re.findall(r"^\s*(Table|Figure) (\d+)\.", t, re.M):
        i = acha_bloco(tokens, rot, int(num))
        if i is not None and tokens[i].startswith('<div class="full">') and i not in idx: idx.append(i)
    return idx

def mede(tokens):
    """renderiza e devolve (páginas, buracos como (página, branco, blocos candidatos a culpados),
    branco por página). Candidatos: o bloco que abre a página seguinte e, em duas colunas, os blocos
    largos da própria página."""
    renderiza(tokens)
    n = paginas()
    medir = branco_colunas if COLUNAS == 2 else branco
    brancos = {p: medir(p) for p in range(PRIMEIRA, n)}
    buracos = []
    for p, b in brancos.items():
        if b <= LIMIAR: continue
        cands = [bloco_que_pulou(tokens, p)] + (blocos_largos_na_pagina(tokens, p) if COLUNAS == 2 else [])
        buracos.append((p, b, [i for k, i in enumerate(cands) if i is not None and i not in cands[:k]]))
    return n, buracos, brancos

def chave(n, buracos):
    """ordem de preferência entre layouts: menos páginas; depois o primeiro buraco acionável (com
    bloco identificado) o mais para o fim possível, porque a folga empurrada para a frente acaba
    absorvida pela última página; depois menos branco no total. Buracos sem bloco identificado (por
    exemplo, o vão ao lado do título na primeira página, que o raster vê como branco) não entram na
    segunda parte da chave, senão travariam a busca."""
    acionaveis = [p for p, _, c in buracos if c]
    return (n, -(acionaveis[0] if acionaveis else 10 ** 6), sum(b for _, b, _ in buracos))

def pontos_de_corte(tok):
    """posições (índice na lista de pedaços) em que um parágrafo pode ser partido: espaço fora de
    qualquer tag, com as tags em linha fechadas, com pelo menos uma palavra de cada lado"""
    m = re.match(r"(<p[^>]*>)(.*)</p>$", tok, re.S)
    pecas = re.split(r"(<[^>]+>|\s+)", m.group(2))
    pilha, palavras, cortes = [], 0, []
    for k, pc in enumerate(pecas):
        if not pc: continue
        if pc.startswith("<"):
            t = re.match(r"<(/?)(\w+)", pc)
            if not t or t.group(2) in ("br", "img"): continue
            if t.group(1): pilha and pilha.pop()
            else: pilha.append(t.group(2))
        elif pc.strip() == "":
            if not pilha and palavras > 0 and any(q.strip() and not q.startswith("<") for q in pecas[k + 1:]):
                cortes.append(k)
        else:
            palavras += 1
    return m.group(1), pecas, cortes

def estado_dividido(tokens, i, idx_p, corte):
    """o bloco i (e a nota da tabela) passa para dentro do parágrafo idx_p, cortado no ponto `corte`:
    a primeira parte fica antes do bloco e a segunda, sem recuo (class="cont"), depois dele. É o
    que faz um bloco largo cair exatamente no topo da página seguinte, com a anterior cheia."""
    abre, pecas, _ = pontos_de_corte(tokens[idx_p])
    parte1 = abre + "".join(pecas[:corte]) + "</p>"
    parte2 = '<p class="cont">' + "".join(pecas[corte + 1:]) + "</p>"
    j = i + 1; bloco = [i]
    while j < len(tokens) and tipo(tokens[j]) in ("ws", "tn"):
        if tipo(tokens[j]) == "tn": bloco.append(j)
        j += 1
    entre = tokens[j:idx_p]
    return tokens[:i] + entre + [parte1, "\n\n"] + [tokens[b] for b in bloco] + ["\n\n", parte2] + tokens[idx_p + 1:]

def proximo_paragrafo(tokens, i):
    """índice do primeiro parágrafo depois do bloco i, cruzando no máximo um grupo de títulos"""
    k = i + 1; cruzados = 0; ant = None
    while k < len(tokens):
        td = tipo(tokens[k])
        if td == "p": return k
        if td == "h" and ant != "h":
            cruzados += 1
            if cruzados > 1: return None
        if td == "outro": return None
        if td != "ws": ant = td
        k += 1
    return None

def divide_para_encher(tokens, i, p):
    """busca binária do ponto de corte do parágrafo seguinte que deixa a página p cheia (branco
    abaixo de ALVO) com o bloco i no topo da seguinte; devolve (estado, medição, descrição) ou None"""
    idx_p = proximo_paragrafo(tokens, i)
    if idx_p is None: return None
    _, _, cortes = pontos_de_corte(tokens[idx_p])
    if len(cortes) < 2: return None
    ALVO = min(LIMIAR, 30.0)
    lo, hi, memo = 0, len(cortes) - 1, {}
    def avalia(k):
        if k not in memo:
            est = estado_dividido(tokens, i, idx_p, cortes[k]); memo[k] = (est,) + mede(est)
        return memo[k]
    while lo < hi:
        mid = (lo + hi) // 2
        _, n2, _, br2 = avalia(mid)
        if br2.get(p, 0.0) <= ALVO: hi = mid
        else: lo = mid + 1
    est, n2, bur2, br2 = avalia(lo)
    return est, (n2, bur2, br2), f"parágrafo seguinte partido na palavra {lo + 1} de {len(cortes) + 1} (página {p} fica com {br2.get(p, 0):.0f} pt de branco)"

def cadeia(tokens, nome, fn, passos=6):
    """estados sucessivos movendo o mesmo bloco um parágrafo por vez, sem cruzar mais de um grupo de
    títulos no total: às vezes só o terceiro parágrafo fecha o buraco"""
    rot, num = nome.split(); num = int(num)
    i0 = acha_bloco(tokens, rot, num)
    h0 = grupos_h(tokens, i0)
    estados, atual = [], tokens
    for _ in range(passos):
        i = acha_bloco(atual, rot, num)
        prox = fn(atual, i) if i is not None else None
        if prox is None: break
        i1 = acha_bloco(prox, rot, num)
        if abs(grupos_h(prox, i1) - h0) > 1: break
        estados.append(prox); atual = prox
    return estados

# busca gulosa de cima para baixo: para o primeiro buraco, três famílias de candidatos (bloco avançado
# até seis parágrafos, recuado até seis, ou parágrafo seguinte partido no ponto que enche a página);
# fica o melhor pela chave (páginas, primeiro buraco mais ao fim, branco total). Como a chave só
# melhora, não há vaivém, e a folga empurrada para a frente acaba na última página.
rejeitados = set()
n, buracos, brancos = mede(toks)
for rodada in range(40):
    print(f"rodada {rodada}: {n} páginas, buracos:", [(p, round(b)) for p, b, _ in buracos], flush=True)
    if not buracos: break
    aceito = False
    for p, b, cands in buracos:
        if not cands:
            print(f"  página {p}: sem bloco a que atribuir o buraco; fica como está"); continue
        atual = chave(n, buracos)
        candidatos = []  # (chave, tokens, n, buracos, brancos, descrição)
        for i in cands:
            nome = re.search(r"<b>((?:Table|Figure) \d+)\.</b>", toks[i]).group(1)
            if (nome, i, p) in rejeitados: continue
            # primeiro o corte do parágrafo seguinte, que leva o bloco para o topo da página seguinte
            div = divide_para_encher(toks, i, p)
            if div:
                novo, (n2, bur2, br2), desc = div
                candidatos.append((chave(n2, bur2), novo, n2, bur2, br2, f"{nome}: {desc}"))
                if candidatos[-1][0] < atual: break
            for sentido, fn in (("para a frente", move_depois_do_proximo_p), ("para trás", move_antes_do_paragrafo_anterior)):
                for passo, novo in enumerate(cadeia(toks, nome, fn), 1):
                    n2, bur2, br2 = mede(novo)
                    candidatos.append((chave(n2, bur2), novo, n2, bur2, br2, f"{nome} movida {passo} parágrafo(s) {sentido}"))
            rejeitados.add((nome, i, p))
        if candidatos:
            melhor = min(candidatos, key=lambda c: c[0])
            if melhor[0] < atual:
                _, toks, n, buracos, brancos, desc = melhor; aceito = True
                print(f"  página {p}: {desc}", flush=True); break
        print(f"  página {p}: nenhum movimento dos blocos candidatos melhora; descartado", flush=True)
    if not aceito:
        print("  nenhum movimento melhora o layout; parando"); break
open(OUT, "w", encoding="utf-8").write(cabeca + "".join(toks) + cauda)
print("gravado", OUT, "com", n, "páginas e", len(buracos), "buraco(s) acima de", int(LIMIAR), "pt")
