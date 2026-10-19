#!/usr/bin/env python3
"""
monta_resumo_leigo.py: gera o PDF do resumo simplificado (01-artigo/resumo-leigo-*.md) com o mesmo
caminho do montador do artigo: markdown -> HTML -> Edge headless -> PDF. Uma coluna, A4, sem
imagem, para o arquivo ficar pequeno o bastante para ir anexado em e-mail.

  python monta_resumo_leigo.py --md ../resumo-leigo-2026-09-30.md --out C:/Users/marti/Desktop/resumo-leigo.pdf
  python monta_resumo_leigo.py --md ../resumo-leigo-2026-10-18.md --out C:/Users/marti/Desktop/resumo-leigo-machine-vision-favelas-2026-10-18.pdf
"""
import argparse
import os
import subprocess
import sys
import tempfile
import time

CSS = """
@page { size: A4; margin: 1.4cm 1.9cm; }
body { font-family: "Times New Roman", Times, serif; font-size: 10.8pt; line-height: 1.33; color: #111; }
h1 { font-size: 16pt; line-height: 1.2; margin: 0 0 3pt 0; }
h2 { font-size: 11.5pt; margin: 8pt 0 2pt 0; page-break-after: avoid; }
p { margin: 0 0 5pt 0; text-align: justify; }
em { color: #444; }
table { border-collapse: collapse; width: 100%; font-size: 9.8pt; margin: 6pt 0 8pt 0; }
th, td { border-bottom: 0.5pt solid #999; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { border-top: 1pt solid #000; border-bottom: 1pt solid #000; }
ol { padding-left: 18pt; margin: 0 0 6pt 0; } li { margin-bottom: 4pt; }
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    import markdown
    corpo = markdown.markdown(open(args.md, encoding="utf-8").read(), extensions=["tables"])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{corpo}</body></html>"
    tmp = os.path.join(tempfile.gettempdir(), "resumo_leigo.html")
    open(tmp, "w", encoding="utf-8").write(html)
    if os.path.exists(args.out):
        os.remove(args.out)  # senao um PDF antigo passa pela checagem abaixo
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge):
        edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    # perfil novo a cada execucao: um perfil fixo fica travado se um Edge headless anterior nao fechou,
    # e o Edge sai sem erro e sem PDF
    perfil = tempfile.mkdtemp(prefix="edge_resumo_leigo_")
    r = subprocess.run([edge, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={perfil}",
                    f"--print-to-pdf={os.path.abspath(args.out)}", "file:///" + tmp.replace(chr(92), "/")],
                   capture_output=True, timeout=120)
    # o processo lancado pode sair antes de o Edge terminar de gravar: esperar o arquivo aparecer e estabilizar
    tam = -1
    for _ in range(90):
        if os.path.exists(args.out) and os.path.getsize(args.out) == tam > 0:
            break
        tam = os.path.getsize(args.out) if os.path.exists(args.out) else -1
        time.sleep(1)
    if not os.path.exists(args.out):
        sys.exit("falhou ao gerar o PDF: " + r.stderr.decode("utf-8", "ignore")[-500:])
    print(f"gravado {args.out} ({os.path.getsize(args.out) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
