"""Builds the Online Appendix PDF with the CSS of monta_artigo.py (Elsevier preview).
Usage: python monta_apendice.py <repo_root> <out.pdf>"""
import os, re, sys, tempfile, subprocess, time
raiz, out = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(raiz, "01-artigo", "ferramentas"))
import monta_artigo as M
import markdown

ROTULOS_FIG = {"fig10_ajuste_fino": "C2", "fig12_limiar_armado": "C3"}  # FIG markers moved from s5
src = open(os.path.join(raiz, "01-artigo", "manuscrito", "apendice-online.md"), encoding="utf-8").read()

def figura(caminho, rotulo, legenda):
    p = os.path.join(raiz, caminho)
    if not os.path.exists(p):
        sys.exit(f"figura ausente: {caminho}")
    return (f'\n<figure class="full"><img src="{M.embute(p)}" alt="">'
            f'<figcaption><b>Figure {rotulo}.</b> {legenda}</figcaption></figure>\n')

def sub_fig(m):
    chave = os.path.splitext(os.path.basename(m.group(1).strip()))[0]
    if chave not in ROTULOS_FIG:
        sys.exit(f"FIG sem rotulo no apendice: {chave}")
    return figura(m.group(1).strip(), ROTULOS_FIG[chave], m.group(2).strip())
src = M.RE_FIG.sub(sub_fig, src)
src = M.RE_TAB.sub("", src)  # the appendix carries its own "Table Cx." captions
src = re.sub(r"!\[Figure ([A-C]\d+)\. (.+?)\]\(([^)]+)\)", lambda m: figura(m.group(3), m.group(1), m.group(2)), src)

# caption paragraph ("Table X. ...") + table block span both columns, as wide pieces do in the article
linhas, saida, i = src.split("\n"), [], 0
while i < len(linhas):
    if linhas[i].startswith("|"):
        j = i
        while j < len(linhas) and linhas[j].startswith("|"):
            j += 1
        cap = []
        while saida and saida[-1].strip() == "":
            saida.pop()
        if saida and re.match(r"^Table [A-C]\d+[a-z]?(, panel [A-C])?\.", saida[-1]):
            cap = [saida.pop()]
        saida += ['<div class="full" markdown="1">', ""] + cap + [""] + linhas[i:j] + ["", "</div>", ""]
        i = j
    else:
        saida.append(linhas[i]); i += 1
src = "\n".join(saida)
src = re.sub(r"\A\s*# Online Appendix\s*\n", "", src)

corpo = markdown.markdown(src, extensions=["tables", "sane_lists", "md_in_html"])
capa = (f'<div class="capa full"><h1>Online Appendix</h1>'
        f'<div class="autores">{M.titulo()}</div></div>')
aviso = ('<div class="aviso full"><b>Preliminary version, not final.</b> Online Appendix to the working '
         'draft of 26 October 2026, shared among the authors for revision. <i>Versão prévia, ainda não '
         'finalizada.</i></div>')
html = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><style>{M.CSS_ELSEVIER}</style>"
        f"</head><body>{capa}{aviso}{corpo}</body></html>")
tmp = os.path.join(tempfile.gettempdir(), "apendice_previa.html")
open(tmp, "w", encoding="utf-8").write(html)
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge):
    edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
perfil = tempfile.mkdtemp(prefix="edge_perfil_")
if os.path.exists(out):
    os.remove(out)
subprocess.run([edge, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={perfil}",
                f"--print-to-pdf={os.path.abspath(out)}", "file:///" + tmp.replace("\\", "/")],
               capture_output=True, timeout=300)
fim, tam = time.time() + 120, -1
while time.time() < fim:
    if os.path.exists(out):
        t = os.path.getsize(out)
        if t > 0 and t == tam:
            break
        tam = t
    time.sleep(2)
print("gravado:", out, os.path.getsize(out))
