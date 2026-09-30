#!/usr/bin/env python3
"""
monta_artigo.py: junta as seções do manuscrito num único PDF de leitura.

Não é diagramação final de submissão. É uma PRÉVIA fiel o bastante para julgar extensão,
ordem das seções, posição das figuras e se o texto fecha. O formato padrão (--formato elsevier) é
o de periódico em duas colunas; --formato aim reproduz o que os quatro papers premiados de 2026 da
AIM usam (`08-conferencia/modelos_2026/`): Times New Roman 12, espaço duplo, uma coluna.

Por que não pandoc: não está instalado nesta máquina e não quero acrescentar dependência para
gerar uma prévia. O caminho é markdown para HTML e depois Edge em modo headless para PDF, que
já existe no Windows.

As notas de proveniência e de estado (blocos de citação que começam com `> **Provenance note`,
`> **Nota de estado` ou `> **Status note`) são renderizadas em destaque, de propósito: enquanto
houver placeholder no texto, quem lê tem de ver onde está.

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

# Ordem de leitura do artigo. Os arquivos "b" sao a parte tecnica, escrita pelo mestrando; desde a
# reordenacao de 22/09 entram em bloco depois da secao 6.
ORDEM = [
    # Ordem revista em 2026-09-22. A anterior punha o pipeline tecnico entre a metodologia e o
    # contexto de campo, e o leitor saltava de "como geramos a cena" para "historia do
    # policiamento no Rio" e de volta. Pior: a propria metodologia declara que os componentes sao
    # "built one on the other", com o contexto de campo dando o chao que o modelo precisa para ser
    # plausivel, e a ordem antiga contradizia isso.
    #
    # A nova ordem segue problema -> territorio -> como estudamos -> o que propomos -> como
    # construimos -> o que medimos. As secoes 8 a 13 mantem o numero, entao nenhuma remissao
    # tecnica a 8, 9, 10 ou 11 precisou mudar.
    "01-introduction.md",                        # 1  professor
    "02-literature-review.md",                   # 2  professor
    "04-situating-the-study.md",                 # 3  delegado
    "05-case-jacarezinho.md",                    # 4  delegado
    "03-methodology.md",                         # 5  professor
    "06-results-proposed-model.md",              # 6  mestrando
    "03b-methodology-synthetic-pipeline.md",     # 7  tecnico
    "06b-model-free-evidence.md",                # 8  tecnico
    "07b-results-placeholder.md",                # 9  tecnico
    "08b-robustness.md",                         # 10 tecnico
    "09b-technical-limitations.md",              # 11 tecnico
    "07-conclusion.md",                          # 12 professor
    "08-references.md",                          # 13 professor
]

# QUADRO DE AUTORIA, so para esta fase de escrita. Sai do PDF final com --sem-autoria.
#
# Existe porque o artigo tem tres autores escrevendo partes diferentes ao mesmo tempo, e sem isso
# cada um precisa lembrar de cor o que e seu. Fica no montador, e nao dentro dos .md, por duas
# razoes: os arquivos que os coautores editam continuam limpos, e apagar os quadros e trocar uma
# opcao de linha de comando em vez de caçar bloco de citacao em treze arquivos.
#
# (autor, estado do texto, o que falta ou o que observar)
AUTORIA = {
    "01-introduction.md": (
        "Prof. Hélio Arthur Reis Irigaray",
        "v2 de 2026-09-10 com edições do mestrando (22 a 26/09)",
        "O abstract e as palavras-chave foram acrescentados em 20/09 pelo mestrando e atualizados "
        "até 30/09. O abstract tem hoje cerca de 510 palavras e os quatro premiados de 2026 têm de "
        "127 a 152, sem nenhuma citação: precisa encurtar para perto de 150. Na introdução, o "
        "mestrando reescreveu a pergunta de pesquisa e o objetivo, acrescentou o parágrafo de "
        "abertura, o das duas tarefas e o do Global South, e condensou o bloco de planejamento de "
        "trajetória; essas passagens precisam do aval do orientador."),
    "02-literature-review.md": (
        "Prof. Hélio Arthur Reis Irigaray",
        "v2 de 2026-09-10 com acréscimos do mestrando (22/09)",
        "O mestrando acrescentou o bloco sobre detecção aérea de pessoa e limite de resolução "
        "(Kiefer, Liao, VisDrone) e o parágrafo de fecho, e trocou por uma remissão à introdução "
        "a lista que a repetia (item A4 de PENDENCIAS.md); isso precisa do aval do orientador. "
        "Duas obras citadas neste texto, Horváth et al. (2023) e Watson e Elliott (2025), ainda "
        "não têm entrada na lista de referências (item B1); as outras cinco do B1 são citadas na "
        "introdução. Dependem de quem escreveu a frase dizer qual obra é."),
    "04-situating-the-study.md": (
        "Coautor delegado de polícia",
        "esboço de trabalho, não é a versão final",
        "A redação definitiva trará o enquadramento do problema de segurança pública com a "
        "profundidade que a posição do autor permite: conhecimento institucional das operações, "
        "da dinâmica territorial e das restrições operacionais reais. As seções técnicas dependem "
        "desta seção em um ponto e apenas nele: o veto ético à coleta de imagem real, que é a "
        "premissa de 7.1. Os resultados numéricos não derivam dela. O parágrafo final, que liga a "
        "seção à pergunta do artigo e às seções 8 a 11, e a frase que declara como séries "
        "diferentes os números de 2024 do Fórum e do JOTA foram acrescentados pelo mestrando "
        "(22 a 26/09) e precisam do aval do coautor."),
    "05-case-jacarezinho.md": (
        "Coautor delegado de polícia",
        "esboço de trabalho, não é a versão final",
        "É a menor seção do artigo, com cerca de 400 palavras. Três números de população divergem "
        "entre si no texto (35.458, ~37.000 e acima de 60.000) e a divergência é usada como "
        "argumento, o que funciona, mas precisa ficar explícito de onde vem cada um. A última "
        "frase, que entrega o leitor na pergunta do artigo, foi reescrita pelo mestrando em 22/09 "
        "e precisa do aval do coautor."),
    "03-methodology.md": (
        "Prof. Hélio Arthur Reis Irigaray",
        "v2 de 2026-09-10 com acréscimos do mestrando (22 a 26/09)",
        "O primeiro parágrafo foi reescrito pelo mestrando: quatro componentes em vez de três, "
        "com o componente computacional e a declaração de que o protocolo cresceu em etapas. "
        "Precisa do aval do orientador, além da conferência das remissões remapeadas em 22/09. "
        "O resto descreve o protocolo e trata a posicionalidade do coautor delegado de forma "
        "direta."),
    "06-results-proposed-model.md": (
        "Luciano Martins Figueira (mestrando)",
        "proposta conceitual, atualizada com o resultado da 9.4",
        "É a proposta que a seção 7 implementa. Continua a propor a classificação de altura de "
        "edificação, e o que foi construído e medido detecta pessoa; o último parágrafo e a seção "
        "11.4 já declaram essa diferença. O terceiro componente cita o resultado da 9.4, em que o "
        "início genérico supera o sintético com 5 e 10% do dado real; a rodada 4 acrescentou que "
        "misturar sintético e real no mesmo treino também fica abaixo do só real. Falta o autor "
        "decidir se esses resultados mudam a proposta."),
    "03b-methodology-synthetic-pipeline.md": (
        "Luciano Martins Figueira (mestrando)",
        "método executado, com versão e comando de origem",
        "Descreve o que rodou de fato: Blender 5.2.1 headless, não ARMA 3."),
    "06b-model-free-evidence.md": (
        "Luciano Martins Figueira (mestrando)",
        "medições fechadas, com arquivo de origem",
        "Segue o desenho de Dai et al., premiado em 2026, que põe a evidência sem modelo antes "
        "de qualquer regressão."),
    "07b-results-placeholder.md": (
        "Luciano Martins Figueira (mestrando)",
        "resultados medidos, cada número com arquivo de origem",
        "Cada modelo foi especificado antes de rodar, mas o protocolo cresceu em etapas, e o texto "
        "diz quais modelos entraram depois de resultados anteriores. A rodada 4 (27 a 30/09) "
        "acrescentou sementes, treino misto, objeto no porte de arma, quadros novos a 35 e 75 m e "
        "o gêmeo de 150 m, com critérios fixados antes em 07-blender/PLANO-RODADA4.md."),
    "08b-robustness.md": (
        "Luciano Martins Figueira (mestrando)",
        "ameaças e testes definidos antes dos resultados",
        "Cada ameaça traz o teste que a resolveria e o que aconteceria com a conclusão se o teste "
        "falhar. Na rodada 4 rodaram a 10.2 (escala casada), a 10.3 (por regime) e as duas da "
        "10.6 (limiar de IoU e sementes); ficam sem rodar a curva da 10.1 e a ablação só com sol "
        "duro da 10.3, marcadas como tal."),
    "09b-technical-limitations.md": (
        "Luciano Martins Figueira (mestrando)",
        "fechada",
        "Contém, em 11.5, a decisão de não reportar acurácia entre armado e desarmado a 150 m (o "
        "gêmeo treinado lá na rodada 4 ficou abaixo da condição de validade fixada antes) e o "
        "relato a 75 m e 35 m, com o teste de arma inédita e a condição de retirada fixada antes; "
        "é decisão de conteúdo e precisa do aval dos três autores."),
    "07-conclusion.md": (
        "Prof. Hélio Arthur Reis Irigaray",
        "v2 com edições do mestrando e o fecho acrescentado em 20/09",
        "O fecho (Closing) foi escrito pelo mestrando porque a v2 não concluía, só trazia "
        "Limitations, Delimitations e Future Research, e foi atualizado até 30/09 com os "
        "resultados das rodadas 2 a 4. O mestrando também reescreveu o primeiro parágrafo de "
        "Limitations, a delimitação da pergunta técnica e o parágrafo técnico de Future Research. "
        "Tudo isso precisa do aval do orientador."),
    "08-references.md": (
        "os três autores",
        "parcial",
        "Oito entradas conferidas no Crossref em 20/09. Sete citações acadêmicas do texto "
        "continuam sem entrada, de propósito: sobrenome e ano coincidindo não é evidência, e "
        "inserir DOI de obra errada é pior do que deixar a referência faltando. As citações da "
        "Wikipedia na seção 3 também não têm entrada e devem ser trocadas por fonte primária "
        "(item B3 de PENDENCIAS.md)."),
}


NL2 = chr(10) + chr(10)


def quadro_autoria(nome):
    if nome not in AUTORIA:
        return ""
    autor, estado, nota = AUTORIA[nome]
    return (f'<div class="autoria"><b>Autoria:</b> {autor} &nbsp;&middot;&nbsp; '
            f'<b>Estado:</b> {estado}<br><span>{nota}</span></div>')


# As secoes do professor nao trazem numero no titulo, e as tecnicas trazem. O montador numera
# TODAS na ordem de leitura, para que numero de secao e remissao cruzada nunca possam divergir:
# foi exatamente esse tipo de deriva silenciosa que a revisao adversarial pegou.
RE_H2 = re.compile(r"^## (?:\d+\.\s*)?(.+)$", re.M)

# Figura declarada por marcador no texto: <!--FIG:arquivo|legenda-->
RE_FIG = re.compile(r"<!--\s*FIG:([^|]+)\|(.+?)\s*-->")

CSS_AIM = """
.autoria { border: 0.6pt solid #b58900; border-left: 3pt solid #b58900; background: #fffceb;
           padding: 4pt 7pt; margin: 9pt 0 5pt 0; font-size: 9.5pt; line-height: 1.3;
           text-align: left; break-inside: avoid; }
.autoria span { color: #333; }

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
code { font-family: Consolas, monospace; font-size: 10pt; background: #f2f2f2; padding: 0 2pt; }
figure { margin: 14pt 0 16pt 0; page-break-inside: avoid; text-align: center; }
figure img { max-width: 100%; border: 0.5pt solid #bbb; }
figcaption { font-size: 10pt; line-height: 1.4; text-align: left; margin-top: 5pt; color: #222; }
.capa { text-align: center; margin-bottom: 26pt; }
.aviso { border: 1pt solid #c0392b; background: #fdf3f2; padding: 10pt 12pt;
         font-size: 10pt; line-height: 1.5; margin: 16pt 0; }
"""

# Duas colunas, no padrao de periodico da Elsevier: corpo em 9,5 pt com entrelinha apertada,
# titulo e avisos atravessando as duas colunas, e figura ou tabela larga promovida a largura
# total, que e como o periodico trata peca que nao cabe na coluna.
CSS_ELSEVIER = """
.autoria { border: 0.6pt solid #b58900; border-left: 3pt solid #b58900; background: #fffceb;
           padding: 4pt 7pt; margin: 9pt 0 5pt 0; font-size: 7.6pt; line-height: 1.3;
           text-align: left; break-inside: avoid; }
.autoria span { color: #333; }

@page { size: A4; margin: 1.9cm 1.6cm 2.2cm 1.6cm; }
body { font-family: "Times New Roman", Times, serif; font-size: 9.5pt; line-height: 1.30;
       color: #000; column-count: 2; column-gap: 6mm; column-fill: auto; text-align: justify;
       hyphens: auto; }
.full { column-span: all; }
h1 { font-size: 17pt; line-height: 1.22; margin: 0 0 8pt 0; font-weight: bold;
     text-align: left; }
h2 { font-size: 10.5pt; line-height: 1.3; margin: 11pt 0 4pt 0; font-weight: bold;
     page-break-after: avoid; text-align: left; }
h3 { font-size: 9.5pt; line-height: 1.3; margin: 8pt 0 3pt 0; font-weight: bold;
     font-style: italic; page-break-after: avoid; text-align: left; }
p { margin: 0 0 5pt 0; }
p + p { text-indent: 1.2em; margin-top: -3pt; }
table { border-collapse: collapse; width: 100%; font-size: 7.8pt; line-height: 1.18;
        margin: 6pt 0 9pt 0; break-inside: avoid; }
th, td { border: 0; border-bottom: 0.4pt solid #555; padding: 2pt 4pt; text-align: left;
         vertical-align: top; }
thead th { border-top: 0.8pt solid #000; border-bottom: 0.4pt solid #000; font-weight: bold;
           background: none; }
table tr:last-child td { border-bottom: 0.8pt solid #000; }
blockquote { border-left: 2pt solid #999; background: #f6f6f6; margin: 6pt 0; padding: 4pt 7pt;
             font-size: 8pt; line-height: 1.28; text-align: left; break-inside: avoid; }
blockquote p { margin: 0 0 3pt 0; text-indent: 0; }
code { font-family: "Courier New", monospace; font-size: 8pt; }
figure { margin: 8pt 0 10pt 0; break-inside: avoid; text-align: center; }
figure img { max-width: 100%; }
figcaption { font-size: 8pt; line-height: 1.25; text-align: justify; margin-top: 3pt; }
.capa { margin-bottom: 12pt; border-bottom: 1.2pt solid #000; padding-bottom: 8pt; }
.capa .autores { font-size: 10pt; margin-top: 6pt; }
.capa .afil { font-size: 8.5pt; font-style: italic; color: #333; }
.aviso { border: 0.6pt solid #b03a2e; background: #fbeeec; padding: 6pt 8pt; font-size: 8pt;
         line-height: 1.35; margin: 8pt 0 12pt 0; text-align: left; }
.resumo { font-size: 8.6pt; line-height: 1.34; border-top: 0.8pt solid #000;
          border-bottom: 0.8pt solid #000; padding: 7pt 0; margin: 0 0 12pt 0; text-align: justify; }
.resumo b { font-size: 9pt; }
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
        # peca larga atravessa as duas colunas, como faz o periodico
        try:
            from PIL import Image as _I
            larga = _I.open(p).width / max(_I.open(p).height, 1) > 1.9
        except Exception:
            larga = False
        cls = ' class="full"' if larga else ''
        return (f'<figure{cls}><img src="{embute(p)}" alt="{leg}">'
                f'<figcaption><b>Figure {n_fig}.</b> {leg}</figcaption></figure>')
    return RE_FIG.sub(sub, txt), n_fig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "machine-vision-favelas-previa.pdf"))
    ap.add_argument("--formato", choices=["aim", "elsevier"], default="elsevier",
                help="aim = uma coluna, Times 12, espaco duplo, que e o que os premiados de "
                     "2026 usam; elsevier = duas colunas de periodico")
    ap.add_argument("--sem-notas", action="store_true")
    ap.add_argument("--sem-autoria", action="store_true",
                help="tira os quadros de autoria. E o que se usa quando o artigo for "
                     "submetido: eles existem so enquanto os tres autores escrevem juntos")
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
        # a legenda "aparece como [X]" das notas de proveniencia (blocos de citacao) nao e marcador
        n_ph += sum(ln.count("[X]") for ln in txt.splitlines() if not ln.lstrip().startswith(">"))
        if args.sem_notas:
            txt = re.sub(r"^> \*\*(Status note|Provenance note|Nota de estado).*?(?=\n\n)", "", txt,
                         flags=re.S | re.M)
        txt, n_fig = resolve_figuras(txt, n_fig)
        n_sec += 1

        # O Abstract e as palavras-chave nao sao secao numerada, e o arquivo da introducao tem os
        # dois como H2 antes do titulo da propria introducao. Numerar o primeiro H2 sem checar
        # produzia "1. Abstract" e deixava a introducao sem numero, que foi o que o PDF mostrou.
        def _numera(m):
            return f"## {n_sec}. {m.group(1)}"

        alvos = [m for m in RE_H2.finditer(txt)
                 if not m.group(1).strip().lower().startswith(("abstract", "keywords"))]
        if alvos:
            m = alvos[0]
            txt = txt[:m.start()] + _numera(m) + txt[m.end():]
        if not args.sem_autoria:
            # o quadro entra ANTES do titulo, e em HTML cru para nao depender do markdown
            q = quadro_autoria(nome)
            if q:
                alvo = RE_H2.search(txt)
                if alvo:
                    txt = txt[:alvo.start()] + q + NL2 + txt[alvo.start():]
                else:
                    txt = q + NL2 + txt
        partes.append(txt)

    corpo = markdown.markdown("\n\n".join(partes),
                              extensions=["tables", "sane_lists", "md_in_html"])

    capa = """<div class="capa full">
<h1>Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Favelas</h1>
<div class="autores">Luciano Martins Figueira<sup>a</sup>, Helio Arthur Reis Irigaray<sup>a</sup>, <span style="color:#b58900">[coautor delegado, a incluir]</span></div>
<div class="afil"><sup>a</sup> Funda&ccedil;&atilde;o Get&uacute;lio Vargas, EBAPE, Rio de Janeiro, Brazil</div>
</div>"""

    aviso = ""
    if n_ph:
        aviso = (f'<div class="aviso full"><b>PRÉVIA, NÃO SUBMISSÃO.</b> Este documento contém '
                 f'<b>{n_ph} marcadores <code>[X]</code></b> de números ainda não medidos. '
                 f'Nenhum deles pode ser preenchido por estimativa. Os blocos de citação em destaque '
                 f'são notas de proveniência e de estado e não fazem parte do texto final.</div>')
    if faltando:
        aviso += ('<div class="aviso full"><b>Seções ausentes:</b> ' + ", ".join(faltando) + "</div>")

    html = (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<style>{CSS_ELSEVIER if args.formato == chr(101)+chr(108)+chr(115)+chr(101)+chr(118)+chr(105)+chr(101)+chr(114) else CSS_AIM}</style></head><body>{capa}{aviso}{corpo}</body></html>")

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
