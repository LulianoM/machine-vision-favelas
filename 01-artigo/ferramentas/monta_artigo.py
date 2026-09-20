#!/usr/bin/env python3
"""
monta_artigo.py: junta as seções do manuscrito num único PDF de leitura.

Não é diagramação final de submissão. É uma PRÉVIA fiel o bastante para julgar extensão,
ordem das seções, posição das figuras e se o texto fecha. A formatação segue o que os quatro
papers premiados de 2026 da AIM usam (`08-conferencia/modelos_2026/`): Times New Roman 12,
espaço duplo, uma coluna.

Por que não pandoc: não está instalado nesta máquina e não quero acrescentar dependência para
gerar uma prévia. O caminho é markdown para HTML e depois Edge em modo headless para PDF, que
já existe no Windows.

As notas de estado (blocos de citação que começam com `> **Status note`) são renderizadas em
destaque, de propósito: enquanto houver placeholder no texto, quem lê tem de ver onde está.

Uso:
  python monta_artigo.py --out C:\\Users\\marti\\Desktop\\artigo.pdf
  python monta_artigo.py --sem-notas          # esconde as notas de estado
"""
import argparse
import base64
import os
import re
import subprocess
import sys
import tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MAN = os.path.join(RAIZ, "01-artigo", "manuscrito")

# Ordem de leitura do artigo. Os arquivos "b" sao a parte tecnica, aditiva, e entram logo depois
# da secao do professor a que se acoplam.
ORDEM = [
    "01-introduction.md",                        # 1  professor
    "02-literature-review.md",                   # 2  professor
    "03-methodology.md",                         # 3  professor
    "03b-methodology-synthetic-pipeline.md",     # 4  tecnico
    "04-situating-the-study.md",                 # 5  professor
    "05-case-jacarezinho.md",                    # 6  professor
    "06-results-proposed-model.md",              # 7  professor
    "06b-model-free-evidence.md",                # 8  tecnico
    "07b-results-placeholder.md",                # 9  tecnico
    "08b-robustness.md",                         # 10 tecnico
    "09b-technical-limitations.md",              # 11 tecnico
    "07-conclusion.md",                          # 12 professor
    "08-references.md",                          # 13 professor
]

# As secoes do professor nao trazem numero no titulo, e as tecnicas trazem. O montador numera
# TODAS na ordem de leitura, para que numero de secao e remissao cruzada nunca possam divergir:
# foi exatamente esse tipo de deriva silenciosa que a revisao adversarial pegou.
RE_H2 = re.compile(r"^## (?:\d+\.\s*)?(.+)$", re.M)

# Figura declarada por marcador no texto: <!--FIG:arquivo|legenda-->
RE_FIG = re.compile(r"<!--\s*FIG:([^|]+)\|(.+?)\s*-->")

CSS = """
@page { size: A4; margin: 2.5cm 2.2cm; }
body { font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 2.0;
       color: #111; }
h1 { font-size: 16pt; line-height: 1.3; margin: 0 0 6pt 0; }
h2 { font-size: 13pt; line-height: 1.4; margin: 20pt 0 6pt 0; page-break-after: avoid; }
h3 { font-size: 12pt; line-height: 1.4; margin: 14pt 0 4pt 0; font-style: italic;
     page-break-after: avoid; }
p { margin: 0 0 8pt 0; text-align: justify; }
table { border-collapse: collapse; width: 100%; font-size: 10pt; line-height: 1.35;
        margin: 10pt 0 14pt 0; page-break-inside: avoid; }
th, td { border: 0.5pt solid #999; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #eee; font-weight: bold; }
blockquote { border-left: 3pt solid #c0392b; background: #fdf3f2; margin: 10pt 0;
             padding: 6pt 10pt; font-size: 10pt; line-height: 1.45; }
blockquote p { margin: 0 0 4pt 0; text-align: left; }
code { font-family: Consolas, monospace; font-size: 10pt; background: #f2f2f2;
       padding: 0 2pt; }
figure { margin: 14pt 0 16pt 0; page-break-inside: avoid; text-align: center; }
figure img { max-width: 100%; border: 0.5pt solid #bbb; }
figcaption { font-size: 10pt; line-height: 1.4; text-align: left; margin-top: 5pt;
             color: #222; }
em.src { font-size: 9.5pt; color: #444; }
.capa { text-align: center; margin-bottom: 26pt; }
.capa .sub { font-size: 11pt; line-height: 1.5; font-style: italic; }
.aviso { border: 1pt solid #c0392b; background: #fdf3f2; padding: 10pt 12pt;
         font-size: 10pt; line-height: 1.5; margin: 16pt 0; }
hr { border: none; border-top: 0.5pt solid #ccc; margin: 18pt 0; }
"""


def embute(caminho):
    """imagem em base64: o PDF sai de um HTML temporario, entao caminho relativo nao serve"""
    with open(caminho, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(caminho)[1].lstrip(".").lower()
    return f"data:image/{'jpeg' if ext in ('jpg', 'jpeg') else ext};base64,{b}"


def resolve_figuras(txt, n_fig):
    """troca <!--FIG:arquivo|legenda--> por <figure> com a imagem embutida"""
    def sub(m):
        nonlocal n_fig
        rel, leg = m.group(1).strip(), m.group(2).strip()
        p = os.path.join(RAIZ, rel)
        if not os.path.exists(p):
            return f'<p class="aviso">FIGURA AUSENTE: {rel}</p>'
        n_fig += 1
        return (f'<figure><img src="{embute(p)}" alt="{leg}">'
                f'<figcaption><b>Figure {n_fig}.</b> {leg}</figcaption></figure>')
    return RE_FIG.sub(sub, txt), n_fig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "machine-vision-favelas-previa.pdf"))
    ap.add_argument("--sem-notas", action="store_true")
    ap.add_argument("--html", default=None, help="grava tambem o HTML intermediario")
    args = ap.parse_args()

    import markdown

    partes, faltando, n_fig, n_ph, n_sec = [], [], 0, 0, 0
    for nome in ORDEM:
        p = os.path.join(MAN, nome)
        if not os.path.exists(p):
            faltando.append(nome)
            continue
        txt = open(p, encoding="utf-8").read()
        n_ph += txt.count("[X]")
        if args.sem_notas:
            txt = re.sub(r"^> \*\*Status note.*?(?=\n\n)", "", txt, flags=re.S | re.M)
        txt, n_fig = resolve_figuras(txt, n_fig)
        n_sec += 1
        txt = RE_H2.sub(lambda m: f"## {n_sec}. {m.group(1)}", txt, count=1)
        partes.append(txt)

    corpo = markdown.markdown("\n\n".join(partes),
                              extensions=["tables", "sane_lists", "md_in_html"])

    capa = """<div class="capa">
<h1>Machine Vision from the Global South:<br>Developing an AI Model for Vertical Favelas</h1>
</div>"""

    aviso = ""
    if n_ph:
        aviso = (f'<div class="aviso"><b>PRÉVIA, NÃO SUBMISSÃO.</b> Este documento contém '
                 f'<b>{n_ph} marcadores <code>[X]</code></b> de números ainda não medidos. '
                 f'Nenhum deles pode ser preenchido por estimativa. Os blocos em vermelho são '
                 f'notas de estado e não fazem parte do texto final.</div>')
    if faltando:
        aviso += ('<div class="aviso"><b>Seções ausentes:</b> ' + ", ".join(faltando) + "</div>")

    html = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS}</style></head><body>{capa}{aviso}{corpo}</body></html>")

    tmp = args.html or os.path.join(tempfile.gettempdir(), "artigo_previa.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge):
        edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    cmd = [edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={os.path.abspath(args.out)}",
           "file:///" + tmp.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, timeout=300)
    if not os.path.exists(args.out):
        print("falhou ao gerar PDF:", r.stderr.decode("utf-8", "ignore")[-500:], file=sys.stderr)
        sys.exit(1)

    palavras = len(re.sub(r"<[^>]+>", " ", corpo).split())
    print(f"secoes: {len(partes)} de {len(ORDEM)}")
    print(f"palavras: {palavras}")
    print(f"figuras: {n_fig}")
    print(f"placeholders [X]: {n_ph}")
    print(f"gravado: {args.out} ({os.path.getsize(args.out)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
