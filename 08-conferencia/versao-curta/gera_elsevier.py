#!/usr/bin/env python3
"""gera_elsevier.py: monta versao-curta-elsevier.html (A4, duas colunas, Times 9,5 pt, o CSS_ELSEVIER
de 01-artigo/ferramentas/monta_artigo.py) a partir de versao-curta-aim2027.html e roda pagina.py nele
(--colunas 2 --limiar 50) para fechar os buracos de paginação. A nota de trabalho saiu dos HTMLs em
04/11 (registro em NOTA-DE-TRABALHO.md); se uma div.nota voltar ao fonte, ela entra na página 1. É o formato principal da submissão; gera_pdf.sh renderiza os três HTMLs e
deixa as cópias no Desktop.

Regras de diagramação: as quatro figuras largas (nadir contra oblíquo, desenho experimental, três
GSDs, varredura de limiar) e as tabelas com sete ou mais colunas ou quinze ou mais linhas atravessam
as duas colunas em <div class="full">; todo o resto flutua na coluna em <div class="flt"> (se não cabe
no pé da coluna, vai para o topo da seguinte e o texto sobe). O texto é o mesmo da versão AIM, byte a
byte: edite só lá."""
import os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, "../.."))
# uso: gera_elsevier.py [fonte.html [saida.html]]; o padrão é a versão em inglês
FONTE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, "versao-curta-aim2027.html")
SAIDA = sys.argv[2] if len(sys.argv) > 2 else os.path.join(AQUI, "versao-curta-elsevier.html")
src = open(FONTE, encoding="utf-8").read()
montador = open(os.path.join(REPO, "01-artigo/ferramentas/monta_artigo.py"), encoding="utf-8").read()
css = re.search(r'CSS_ELSEVIER\s*=\s*"""(.*?)"""', montador, re.S).group(1)
css += """
.new { background: #fff1a8; } .dec { background: #cfe4ff; }
.refs p, .refs p + p { text-indent: -1.2em; padding-left: 1.2em; margin: 0 0 2pt 0; font-size: 8pt; line-height: 1.15; overflow-wrap: anywhere; }
.decl p, .decl p + p { text-indent: 0; margin: 0 0 4pt 0; font-size: 8.6pt; }
table caption { caption-side: top; text-align: left; font-size: 8pt; line-height: 1.25; padding: 0 0 2pt 0; break-after: avoid; }
p.tn, p + p.tn { font-size: 7.6pt; line-height: 1.2; text-indent: 0; margin: -6pt 0 9pt 0; text-align: left; }
table.t td.num, table.t th.num { text-align: right; }
table.t .sub td { font-style: italic; }
table.t thead { display: table-header-group; }
.capa .autores, .capa .afil, .resumo p { text-indent: 0; }
/* bloco flutuante na coluna: se não cabe no pé da coluna vai para o topo da seguinte e o texto
   que o segue no fonte sobe para preencher a coluna (comportamento de figura de periódico) */
.flt { float: left; width: 100%; break-inside: avoid; margin: 0; }
.flt + p, .full + p { text-indent: 1.2em; margin-top: -3pt; }
.flt table { margin-top: 2pt; }
/* bloco largo que abre página (Figura 2): no meio da página ele partiria a leitura das duas colunas em
   duas filas; pagina.py enche a página anterior partindo o parágrafo seguinte */
.topo { break-before: page; }
.flt figure img { max-width: 100%; }
/* segunda parte de um parágrafo partido por pagina.py em volta de um bloco largo: continua sem recuo */
p.cont, .full + p.cont, .flt + p.cont, p + p.cont { text-indent: 0; margin-top: 0; }
/* nota de trabalho em português: uma coluna, página própria, apagar antes de submeter */
.nota { column-span: all; font-size: 8.6pt; line-height: 1.3; border: 1pt solid #444; padding: 8pt 10pt; background: #f6f6f6; break-after: page; text-align: left; }
.nota h1 { font-size: 10.5pt; line-height: 1.25; margin: 0 0 5pt 0; }
.nota p, .nota p + p, .nota li { text-indent: 0; margin: 0 0 4pt 0; }
.nota ol { margin: 2pt 0 4pt 16pt; padding: 0; }
.nota code { font-size: 7.8pt; }
"""
antes, resto = src.split("<!-- MANUSCRITO", 1)
m_nota = re.search(r'<div class="nota">.*?</div>', antes, re.S)
nota = m_nota.group(0).replace('<div class="nota">', '<div class="nota full">', 1) if m_nota else ""
marca = "<!-- MANUSCRITO" + resto[:resto.index("-->") + 3]
corpo = resto[resto.index("-->") + 3:]
cauda = corpo[corpo.index("</body>"):]
corpo = corpo[:corpo.index("</body>")]

# capa e resumo nas classes do montador, atravessando as duas colunas
corpo = corpo.replace('<div class="front">', '<div class="capa full">', 1)
i = corpo.index('<div class="capa full">'); j = corpo.index("</div>", i)
capa = corpo[i:j]
capa = re.sub(r"<p>(Luciano[^<]*)</p>", r'<p class="autores">\1</p>', capa, count=1)
capa = re.sub(r"<p>([¹²] [^<]*)</p>", r'<p class="afil">\1</p>', capa)
corpo = corpo[:i] + capa + corpo[j:]
corpo = corpo.replace('<div class="abstract">', '<div class="resumo full">', 1)
corpo = corpo.replace('<p class="kw">', '<p class="kw" style="text-indent:0">')

# figuras largas atravessam as duas colunas, com a largura que mantém o texto interno legível
# (84% de 504 pt deixa o rótulo da figura 9 em cerca de 7,4 pt e o eixo da 12 em cerca de 7 pt);
# as demais flutuam na coluna, na largura inteira da coluna
LARGAS = {"fig8_": "92%", "fig9_": "84%", "fig7_": "100%", "fig12_": "84%"}
def figura(m):
    blk = re.sub(r' style="max-width: \d+%;"', "", m.group(0))
    for chave, larg in LARGAS.items():
        if chave in blk:
            if larg != "100%": blk = blk.replace("<img ", f'<img style="max-width: {larg};" ', 1)
            return f'<div class="full{" topo" if chave == "fig9_" else ""}">{blk}</div>'
    return f'<div class="flt">{blk}</div>'
corpo = re.sub(r"<figure>.*?</figure>", figura, corpo, flags=re.S)

# tabelas com sete ou mais colunas ou quinze ou mais linhas atravessam as duas colunas (e podem
# quebrar entre páginas com o cabeçalho repetido); as demais flutuam na coluna, com a nota junto
def tabela(m):
    blk = m.group(0)
    cabecalho = re.search(r"<tr>.*?</tr>", blk, re.S).group(0)
    ncol = len(re.findall(r"<t[hd]", cabecalho)); nlin = len(re.findall(r"<tr", blk))
    return f'<div class="{"full" if ncol >= 7 or nlin >= 15 else "flt"}">{blk}</div>'
corpo = re.sub(r'<table class="t[^"]*"[^>]*>.*?</table>(\s*<p class="tn">.*?</p>)?', tabela, corpo, flags=re.S)

html = (f"<!doctype html><html lang='{'pt-BR' if 'ptbr' in FONTE else 'en'}'><head><meta charset='utf-8'>"
        f"<title>Machine Vision from the Global South, short version, {'cópia de leitura em português' if 'ptbr' in FONTE else 'Elsevier preview'}</title>"
        f"<style>{css}</style></head><body>\n{nota}\n{marca}\n{corpo}{cauda}")
out = SAIDA
open(out, "w", encoding="utf-8").write(html)
print("montado", out)
# se o fonte ainda tiver uma div.nota, ela ocupa a página 1 e a medição de buracos (por coluna, raster) começa na 2
subprocess.run([sys.executable, os.path.join(AQUI, "pagina.py"), out, "--colunas", "2", "--primeira", "2" if nota else "1", "--limiar", "50"], check=True)
