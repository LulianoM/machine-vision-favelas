#!/usr/bin/env python3
"""Divide um rascunho .docx do artigo em um arquivo Markdown por seção.

Uso:
    python3 docx_para_secoes.py <rascunho.docx> <pasta_de_saida>

Só usa a biblioteca padrão (zipfile + xml), para rodar igual no Mac e no Windows.
O texto sai VERBATIM: nenhuma correção é aplicada aqui. Negrito e itálico de
trecho viram **...** e *...*. Títulos são detectados pelo estilo do Word
(Título 1/2/3) ou, na falta de estilo, por parágrafo curto todo em negrito.
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

# Títulos de nível 3 que merecem arquivo próprio (prefixo, sem diferenciar caixa).
PROMOVER_H3 = ("rio de janeiro's favelas and the case of",)

# Nome de arquivo por prefixo do título; o que não casar vira slug automático.
NOMES = [
    ("literature review", "literature-review"),
    ("methodology", "methodology"),
    ("situating the study", "situating-the-study"),
    ("rio de janeiro's favelas", "case-jacarezinho"),
    ("results", "results-proposed-model"),
    ("conclusion", "conclusion"),
    ("references", "references"),
    ("eferences", "references"),
]


def ligado(rpr, tag):
    if rpr is None:
        return False
    el = rpr.find(W + tag)
    return el is not None and el.get(W + "val") not in ("0", "false")


def runs_do_paragrafo(par):
    """Lista de (texto, negrito, italico), com runs vizinhos de mesmo formato unidos."""
    saida = []
    for r in par.iter(W + "r"):
        partes = []
        for el in r:
            if el.tag == W + "t":
                partes.append(el.text or "")
            elif el.tag == W + "tab":
                partes.append("\t")
            elif el.tag in (W + "br", W + "cr"):
                partes.append("\n")
        texto = "".join(partes)
        if not texto:
            continue
        rpr = r.find(W + "rPr")
        fmt = (ligado(rpr, "b"), ligado(rpr, "i"))
        if saida and saida[-1][1:] == fmt:
            saida[-1] = (saida[-1][0] + texto, *fmt)
        else:
            saida.append((texto, *fmt))
    return saida


def marcar(texto, negrito, italico):
    if not texto.strip() or not (negrito or italico):
        return texto
    m = re.match(r"^(\s*)(.*?)(\s*)$", texto, re.S)
    ini, miolo, fim = m.groups()
    marca = ("**" if negrito else "") + ("*" if italico else "")
    return f"{ini}{marca}{miolo}{marca[::-1]}{fim}"


def ler_paragrafos(caminho_docx):
    with zipfile.ZipFile(caminho_docx) as z:
        raiz = ET.fromstring(z.read("word/document.xml"))
    corpo = raiz.find(W + "body")
    itens = []
    for par in corpo.iter(W + "p"):
        runs = runs_do_paragrafo(par)
        puro = "".join(t for t, _, _ in runs)
        if not puro.strip():
            continue
        ppr = par.find(W + "pPr")
        estilo, lista = None, False
        if ppr is not None:
            ps = ppr.find(W + "pStyle")
            estilo = ps.get(W + "val") if ps is not None else None
            lista = ppr.find(W + "numPr") is not None
        todo_negrito = all(b for t, b, _ in runs if t.strip())
        nivel = None
        m = re.search(r"(?:t[ií]?tulo|heading)\s*(\d)", estilo or "", re.I)
        if m:
            nivel = int(m.group(1))
        elif estilo is None and todo_negrito and len(puro) < 150 and not lista:
            nivel = 1 if not itens else 2
        if nivel:
            itens.append({"tipo": "titulo", "nivel": nivel, "texto": puro.strip()})
        else:
            md = "".join(marcar(t, b, i) for t, b, i in runs).strip()
            itens.append({"tipo": "lista" if lista else "p", "texto": md, "puro": puro})
    return itens


def slug(texto):
    s = re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")
    return s[:50] or "secao"


def nome_para(titulo):
    t = titulo.lower()
    for prefixo, nome in NOMES:
        if t.startswith(prefixo):
            return nome
    return slug(titulo)


def dividir(itens):
    """Agrupa em seções. A primeira (título + parágrafos sem título) é a introdução."""
    secoes = [{"nome": "introduction", "titulo": "Introduction (sem título no original)", "itens": []}]
    for it in itens:
        if it["tipo"] == "titulo":
            promovido = it["nivel"] == 3 and it["texto"].lower().startswith(PROMOVER_H3)
            if it["nivel"] == 2 or promovido:
                secoes.append({"nome": nome_para(it["texto"]), "titulo": it["texto"], "itens": []})
        secoes[-1]["itens"].append(it)
    return secoes


def render(secao):
    linhas = []
    promovida = False
    for it in secao["itens"]:
        if it["tipo"] == "titulo":
            nivel = it["nivel"]
            if nivel == 3 and not promovida and it["texto"] == secao["titulo"]:
                nivel, promovida = 2, True  # H3 promovido a arquivo próprio
            linhas += ["#" * nivel + " " + it["texto"], ""]
        elif it["tipo"] == "lista":
            linhas.append("- " + it["texto"])
        else:
            if linhas and linhas[-1].startswith("- "):
                linhas.append("")
            linhas += [it["texto"], ""]
    return "\n".join(linhas).rstrip() + "\n"


def contar_palavras(secao):
    return sum(len(it.get("puro", it["texto"]).split()) for it in secao["itens"] if it["tipo"] != "titulo")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    origem, destino = Path(sys.argv[1]), Path(sys.argv[2])
    destino.mkdir(parents=True, exist_ok=True)
    secoes = dividir(ler_paragrafos(origem))
    total = 0
    print(f"{'arquivo':40} {'palavras':>8}  seção")
    for n, sec in enumerate(secoes, start=1):
        arquivo = f"{n:02d}-{sec['nome']}.md"
        (destino / arquivo).write_text(render(sec), encoding="utf-8")
        p = contar_palavras(sec)
        total += p
        print(f"{arquivo:40} {p:>8}  {sec['titulo']}")
    print(f"{'TOTAL':40} {total:>8}")


if __name__ == "__main__":
    main()
