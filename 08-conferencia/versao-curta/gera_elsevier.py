#!/usr/bin/env python3
"""gera_elsevier.py: monta versao-curta-elsevier.html (A4, duas colunas, Times 9,5 pt, o CSS_ELSEVIER
de 01-artigo/ferramentas/monta_artigo.py) a partir de versao-curta-aim2027.html, sem a nota de
trabalho, e roda pagina.py nele (--fundo 779 --primeira 1) para fechar os buracos de paginação.
Depois, gera_pdf.sh renderiza os três HTMLs e deixa as cópias no Desktop.

Regras de diagramação: tabelas com cinco ou mais colunas e as figuras largas (nadir contra oblíquo,
desenho experimental, três GSDs, varredura de limiar) atravessam as duas colunas em <div class="full">;
o resto fica dentro da coluna. O texto é o mesmo da versão AIM, byte a byte: edite só lá."""
import os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, "../.."))
src = open(os.path.join(AQUI, "versao-curta-aim2027.html"), encoding="utf-8").read()
montador = open(os.path.join(REPO, "01-artigo/ferramentas/monta_artigo.py"), encoding="utf-8").read()
css = re.search(r'CSS_ELSEVIER\s*=\s*"""(.*?)"""', montador, re.S).group(1)
css += """
.new { background: #fff1a8; } .dec { background: #cfe4ff; }
.refs p, .refs p + p { text-indent: -1.2em; padding-left: 1.2em; margin: 0 0 3pt 0; font-size: 8.3pt; line-height: 1.22; overflow-wrap: anywhere; }
.decl p, .decl p + p { text-indent: 0; margin: 0 0 4pt 0; font-size: 8.6pt; }
table caption { caption-side: top; text-align: left; font-size: 8pt; line-height: 1.25; padding: 0 0 2pt 0; break-after: avoid; }
p.tn, p + p.tn { font-size: 7.6pt; line-height: 1.2; text-indent: 0; margin: -6pt 0 9pt 0; text-align: left; }
table.t td.num, table.t th.num { text-align: right; }
table.t .sub td { font-style: italic; }
table.t thead { display: table-header-group; }
.capa .autores, .capa .afil, .resumo p { text-indent: 0; }
"""
_, resto = src.split("<!-- MANUSCRITO", 1)
marca = "<!-- MANUSCRITO" + resto[:resto.index("-->") + 3]
corpo = resto[resto.index("-->") + 3:]
cauda = corpo[corpo.index("</body>"):]
corpo = corpo[:corpo.index("</body>")]

# capa e resumo nas classes do montador, atravessando as duas colunas
corpo = corpo.replace('<div class="front">', '<div class="capa full">', 1)
i = corpo.index('<div class="capa full">'); j = corpo.index("</div>", i)
capa = corpo[i:j]
capa = re.sub(r"<p>(Luciano[^<]*)</p>", r'<p class="autores">\1</p>', capa, count=1)
capa = re.sub(r"<p>(Fundação[^<]*)</p>", r'<p class="afil">\1</p>', capa, count=1)
corpo = corpo[:i] + capa + corpo[j:]
corpo = corpo.replace('<div class="abstract">', '<div class="resumo full">', 1)
corpo = corpo.replace('<p class="kw">', '<p class="kw" style="text-indent:0">')

LARGAS = ("fig7_", "fig8_", "fig9_", "fig12_")
def figura(m):
    blk = re.sub(r' style="max-width: \d+%;"', "", m.group(0))
    return f'<div class="full">{blk}</div>' if any(k in blk for k in LARGAS) else blk
corpo = re.sub(r"<figure>.*?</figure>", figura, corpo, flags=re.S)

def tabela(m):
    blk = m.group(0)
    cabecalho = re.search(r"<tr>.*?</tr>", blk, re.S).group(0)
    return f'<div class="full">{blk}</div>' if len(re.findall(r"<t[hd]", cabecalho)) >= 5 else blk
corpo = re.sub(r'<table class="t[^"]*"[^>]*>.*?</table>(\s*<p class="tn">.*?</p>)?', tabela, corpo, flags=re.S)

html = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Machine Vision from the Global South, short version, Elsevier preview</title>"
        f"<style>{css}</style></head><body>\n{marca}\n{corpo}{cauda}")
out = os.path.join(AQUI, "versao-curta-elsevier.html")
open(out, "w", encoding="utf-8").write(html)
print("montado", out)
subprocess.run([sys.executable, os.path.join(AQUI, "pagina.py"), out, "--fundo", "779", "--primeira", "1"], check=True)
