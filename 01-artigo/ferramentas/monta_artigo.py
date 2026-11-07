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
# Rotulos por lingua (--lingua pt usa 01-artigo/manuscrito-pt, traducao de 2026-10-23)
ROT = {"Table": "Table", "Figure": "Figure"}

# Ordem de leitura do artigo. Os arquivos "b" sao a parte tecnica, escrita pelo mestrando; desde a
# reordenacao de 22/09 entram em bloco depois da secao 6.
ORDEM = [
    # Ordem revista em 2026-10-17, a partir do feedback de 14/10 (01-artigo/feedback-2026-10-14/):
    # estrutura de sete secoes (introducao, trabalhos relacionados, contexto, materiais e metodos,
    # resultados, discussao, conclusao). O montador numera o H2 de cada arquivo na ordem desta
    # lista; H3 e H4 levam numero explicito no texto. A ordem de 30/09 (treze arquivos, com as
    # secoes do orientador e as tecnicas "b") esta congelada em 01-artigo/manuscrito-2026-09-30/.
    "s1-introduction.md",         # 1 abstract e introducao
    "s2-related-work.md",         # 2
    "s3-study-context.md",        # 3
    "s4-materials-methods.md",    # 4
    "s5-results.md",              # 5
    "s6-discussion.md",           # 6
    "s7-conclusion.md",           # 7, seguida do bloco Declarations (H2 sem numero)
    "s8-references.md",           # referencias, sem numero
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
        "Em 30/09, com a busca bibliográfica, todas as obras citadas ganharam entrada conferida "
        "no Crossref; as frases sobre Barisic, Horváth, Gevaert e Watson e Elliott foram "
        "ajustadas ao que as obras dizem, e o parágrafo do sintético ganhou a ressalva de que o "
        "ganho do pré-treino sintético é condicional, com as citações."),
    "04-situating-the-study.md": (
        "Coautor delegado de polícia",
        "esboço de trabalho, não é a versão final",
        "A redação definitiva trará o enquadramento do problema de segurança pública com a "
        "profundidade que a posição do autor permite: conhecimento institucional das operações, "
        "da dinâmica territorial e das restrições operacionais reais. As seções técnicas dependem "
        "desta seção em um ponto e apenas nele: o veto ético à coleta de imagem real, que é a "
        "premissa de 7.1. Os resultados numéricos não derivam dela. O parágrafo final, que liga a "
        "seção à pergunta do artigo e às seções 8 a 11, e a frase sobre a diferença entre os "
        "números de 2024 do Fórum e do JOTA foram acrescentados pelo mestrando (22 a 26/09). Em "
        "30/09 a busca bibliográfica trocou a Wikipédia, a Vanguard Attaché e o Crime Brasil por "
        "fontes primárias, corrigiu autoria e datas e reescreveu as frases que as fontes não "
        "sustentavam; a falta de mapas das rotas passou a premissa do estudo. Tudo precisa do "
        "aval do coautor."),
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
        "o gêmeo de 150 m, com critérios fixados antes em 03-blender/PLANO-RODADA4.md."),
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
        "Refeita em 30/09 com a busca bibliográfica: as sete citações que faltavam entraram, "
        "cinco metadados foram corrigidos, as fontes jornalísticas frágeis deram lugar a fontes "
        "primárias e todos os DOIs foram conferidos no Crossref. Os dois blocos APA viraram uma "
        "ordem alfabética só. Ficam o bloco de marcadores herdado da v2 (item B8 de "
        "PENDENCIAS.md) e um travessão no título da entrada da Movisafe."),
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
# Tabela com legenda numerada: <!--TAB:chave|legenda--> na linha anterior a tabela; @tab{chave}
# no texto vira o numero. @fig{nome-do-arquivo-sem-extensao} faz o mesmo para figuras.
RE_TAB = re.compile(r"<!--\s*TAB:([^|]+)\|(.+?)\s*-->")


def resolve_tabelas(txt, num_tab):
    """troca <!--TAB:chave|legenda--> pela legenda numerada, em HTML cru acima da tabela"""
    def sub(m):
        chave, leg = m.group(1).strip(), m.group(2).strip()
        return f'<p class="tabcap"><b>{ROT["Table"]} {num_tab.get(chave, "?")}.</b> {leg}</p>'
    return RE_TAB.sub(sub, txt)

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
h4 { font-size: 12pt; line-height: 1.4; margin: 10pt 0 3pt 0; font-weight: normal;
     font-style: italic; page-break-after: avoid; }
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
.tabcap { font-size: 10pt; line-height: 1.4; margin: 10pt 0 2pt 0; page-break-after: avoid; }
caption.tabcap { caption-side: top; text-align: left; padding: 0 0 2pt 0; }
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
h4 { font-size: 9.5pt; line-height: 1.3; margin: 6pt 0 2pt 0; font-weight: normal;
     font-style: italic; page-break-after: avoid; text-align: left; }
h4 + p { text-indent: 0; }
p { margin: 0 0 5pt 0; }
p + p { text-indent: 1.2em; margin-top: -3pt; }
table { border-collapse: collapse; width: 100%; font-size: 7.8pt; line-height: 1.18;
        margin: 6pt 0 9pt 0; break-inside: avoid; }
div.full table, table.longa { break-inside: auto; }
thead, caption { break-after: avoid; }
tbody tr:first-child { break-before: avoid; }
tbody tr:nth-child(2) { break-before: avoid; }
/* tabela pode quebrar entre paginas (linha inteira, cabecalho repetido) em vez de pular
   inteira e deixar as duas colunas vazias embaixo, visto em 10 paginas da v9 */
tr { break-inside: avoid; }
thead { display: table-header-group; }
div.full { break-inside: auto !important; }
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
.tabcap { font-size: 8pt; line-height: 1.25; margin: 6pt 0 1pt 0; text-align: left; break-after: avoid; text-indent: 0; }
caption.tabcap { caption-side: top; padding: 0 0 2pt 0; break-after: avoid; }
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
            larga = _I.open(p).width / max(_I.open(p).height, 1) > 1.8
        except Exception:
            larga = False
        cls = ' class="full"' if larga else ''
        return (f'<figure{cls}><img src="{embute(p)}" alt="{leg}">'
                f'<figcaption><b>{ROT["Figure"]} {n_fig}.</b> {leg}</figcaption></figure>')
    return RE_FIG.sub(sub, txt), n_fig


# --- formato JMIS (Journal of Management Information Systems), pedido de 2026-10-20 -------------
# Regras de https://www.jmis-web.org/info-for-contributors: manuscrito anonimo, abstract de ate 150
# palavras sem citacao, Times 12, espaco duplo, alinhado a esquerda, paginas numeradas, ate 50
# paginas, figuras e tabelas no fim com a posicao indicada no texto, referencias em ordem
# alfabetica e numeradas, citadas no texto como [9]. Autoria, financiamento e agradecimentos vao
# para a carta de apresentacao, que sai num PDF a parte (--out com sufixo -title-page).

# Abstract da v de 18/10 tem ~260 palavras; este e o corte para o limite de 150. Em 26/10 a versao
# v3 (22/10) foi restaurada e so corrigida: taxas de objeto do trio pareado em quadros novos
# (24,5, 12,5 e 25,3 por cento a 150, 75 e 35 m, menor na resolucao do meio), sem a frase
# "finer resolution not reducing the confusion", que contradizia o resultado confirmatorio.
ABSTRACT_JMIS = (
    "Public security operations in the favelas of Rio de Janeiro are among the most lethal in "
    "Brazil and take place in dense, vertically built territory. Aerial systems already fly "
    "there, where lethal force turns on whether a person is armed. Training a detector for "
    "that judgement is hard: no imagery of residents can be collected with consent, no public "
    "benchmark annotates a carried firearm, and the altitude, camera angle and light of each "
    "flight decide what reaches the detector. On procedural corpora of a dense favela we "
    "characterised the target by ground sampling distance, camera pitch and illumination and "
    "scored synthetic-only detectors against a matched real-data ceiling. On an urban "
    "benchmark they reached 2.2 per cent of the ceiling for nadir imagery and 15.3 per cent "
    "for the best oblique configuration; on a nadir benchmark the order reversed. Added real "
    "images made the synthetic corpus a cost.")

# sigla usada no texto -> inicio da entrada na lista de referencias
SIGLAS = {"STF": "Supremo Tribunal Federal", "RICS": "Royal Institution of Chartered Surveyors",
          "DECEA": "Departamento de Controle do Espaço Aéreo",
          "ISP-RJ": "Instituto de Segurança Pública do Rio de Janeiro",
          # o regulamento da UE e citado pelo numero; a entrada comeca pelo titulo inteiro
          r"Regulation \(EU\) 2024/1689": "Regulation (EU) 2024/1689 of the European Parliament and "
          "of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence "
          "and amending Regulations (EC) No 300/2008"}
ANO = r"(?:\d{4}[a-z]?|n\.d\.(?:-[a-z])?)"


def le_referencias(refs_md):
    """[(autores, ano, linha)] na ordem do arquivo, que ja e alfabetica"""
    out = []
    for ln in refs_md.splitlines():
        m = re.match(r"^(.+?)\.? \((" + ANO + r")[,)]", ln.strip())
        if m and not ln.startswith("#"):
            out.append((m.group(1), m.group(2), ln.strip()))
    return out


def acha_ref(texto, ano, refs, ultimo=True):
    """indice da referencia cujo primeiro autor aparece em `texto` com o ano: o mais perto do fim
    (citacao narrativa, o nome vem logo antes do ano) ou, com ultimo=False, o primeiro (item entre
    parenteses, onde os coautores tambem aparecem: "Varga, Kiefer, ..." nao e Kiefer).
    Devolve (indice, posicao do nome no texto) ou (None, None)."""
    texto = re.sub(r"\s*\[[A-Z]+\]", "", texto)
    for sigla, nome in SIGLAS.items():
        texto = re.sub(rf"\b{sigla}\b", nome, texto)
    melhor = None
    for i, (aut, a, _) in enumerate(refs):
        if a != ano:
            continue
        lead = aut.split(",")[0].strip()
        ocorr = list(re.finditer(r"(?<!\w)" + re.escape(lead) + r"(?!\w)", texto))
        if not ocorr:
            continue
        pos = ocorr[-1 if ultimo else 0].start()
        # desempate: "Couto, 2025" e "Couto & Figueiredo, 2025"; cita com dois nomes pede o segundo
        cauda = texto[pos + len(lead):]
        n_cit = 3 if "et al" in cauda else 2 if re.search(r"&| and ", cauda) else 1
        # le_referencias corta o ponto final da ultima inicial ("Couto, C"); sem repor, "Couto, C."
        # e "Couto, C., & Figueiredo, C" contavam um autor cada e o desempate falhava
        n_ref = len(re.findall(r"(?:^|, |& )[^,&]+?, (?:[A-Z][a-zà-ü]?\.[ -]?)+", aut + ".")) or 1
        custo = (-pos if ultimo else pos, abs(min(n_ref, 3) - n_cit))
        if melhor is None or custo < melhor[0]:
            melhor = (custo, i, pos)
    return (melhor[1], melhor[2]) if melhor else (None, None)


def citacoes_numericas(txt, refs, perdidas):
    """(Autor, 2020; Outro et al., 2021) -> [3, 7]; Autor et al. (2020) -> Autor et al. [3]"""
    def grupo(m):
        itens, saida, achou = m.group(1).split("; "), [], False
        for it in itens:
            mi = re.match(r"^(?P<nomes>.+?), (?P<anos>" + ANO + r"(?:, " + ANO + r")*)(?P<pos>, .+)?$", it)
            if not mi:
                saida.append(("txt", it))
                continue
            nums = []
            for ano in mi.group("anos").split(", "):
                i, p = acha_ref(mi.group("nomes"), ano, refs, ultimo=False)
                if i is None:
                    nums = None
                    break
                nums.append(i + 1)
            if not nums:
                perdidas.append(it)
                saida.append(("txt", it))
                continue
            achou = True
            pre = mi.group("nomes")[:p].rstrip()
            pos_ = mi.group("pos") or ""
            # prefixo que nao e nome ("altitude range after Nguyen et al.") fica como texto
            if re.fullmatch(r"(?:[A-Z]\.\s*)+", pre):
                pre = ""  # inicial que desambigua o sobrenome (T. Li, Z. Li) cai com o nome
            if pre and pre not in ("e.g.,", "see", "cf."):
                saida.append(("txt", f"{mi.group('nomes')} [{', '.join(map(str, nums))}{pos_}]"))
            else:
                saida.append(("num", (pre, nums, pos_)))
        if not achou:
            return m.group(0)
        if all(k == "num" for k, _ in saida):
            pre = saida[0][1][0]
            corpo = ", ".join(f"{n}{p}" for n, p in sorted((n, p) for _, (_, ns, p) in saida
                                                        for n in ns))
            return f"{pre + ' ' if pre else ''}[{corpo}]"
        return "(" + "; ".join(v if k == "txt" else f"[{', '.join(map(str, v[1]))}{v[2]}]"
                               for k, v in saida) + ")"

    txt = re.sub(r"\(([^()]*?, " + ANO + r"(?:[,;)][^()]*)?)\)", grupo, txt)

    def narrativa(m):
        ano, resto = m.group(1), m.group(2) or ""
        janela = txt_atual[max(0, m.start() - 160):m.start()]
        i, _ = acha_ref(janela, ano, refs)
        if i is None:
            perdidas.append(janela[-50:] + m.group(0))
            return m.group(0)
        return f"[{i + 1}{resto}]"

    txt_atual = txt
    return re.sub(r"\((" + ANO + r")(, [^)]+)?\)", narrativa, txt)


CSS_JMIS = """
@page { size: letter; margin: 1in; @bottom-center { content: counter(page);
        font-family: "Times New Roman", Times, serif; font-size: 12pt; } }
body { font-family: "Times New Roman", Times, serif; font-size: 12pt; line-height: 2.0;
       color: #000; text-align: left; }
h1 { font-size: 14pt; line-height: 2.0; margin: 0 0 12pt 0; text-align: center; }
h2 { font-size: 12pt; line-height: 2.0; margin: 12pt 0 0 0; page-break-after: avoid; }
h3 { font-size: 12pt; line-height: 2.0; margin: 12pt 0 0 0; font-style: italic;
     page-break-after: avoid; }
h4 { font-size: 12pt; line-height: 2.0; margin: 0; font-weight: normal; font-style: italic;
     page-break-after: avoid; }
p { margin: 0; text-indent: 0.5in; }
h2 + p, h3 + p, h4 + p, .resumo p, .local + p { text-indent: 0; }
ol.refs { padding-left: 0.5in; } ol.refs li { margin: 0; }
.local { text-align: center; text-indent: 0; margin: 12pt 0; }
.capa { page-break-after: always; }
.resumo p { text-indent: 0; }
.fim { page-break-before: always; line-height: 1.3; }
.fim table { border-collapse: collapse; width: 100%; font-size: 10pt; line-height: 1.3;
             margin: 6pt 0 0 0; }
.fim th, .fim td { border: 0; border-bottom: 0.4pt solid #555; padding: 2pt 4pt;
                   text-align: left; vertical-align: top; }
.fim thead th { border-top: 0.8pt solid #000; border-bottom: 0.6pt solid #000; }
.fim tr:last-child td { border-bottom: 0.8pt solid #000; }
.fim figure { margin: 0; text-align: center; } .fim figure img { max-width: 100%; max-height: 7.2in; }
.fim .tabcap, .fim figcaption { font-size: 12pt; line-height: 1.5; text-align: left; margin: 0 0 6pt 0; }
code { font-family: "Courier New", monospace; font-size: 11pt; }
"""


def monta_jmis(partes, refs_md, args):
    """recebe as secoes ja numeradas (markdown, com FIG/TAB ja resolvidos em HTML) e devolve o HTML"""
    import markdown
    refs = le_referencias(refs_md)
    perdidas, tabelas, figuras = [], [], []
    corpo = "\n\n".join(partes)

    # abstract curto e palavras-chave; Funding e Acknowledgements identificam os autores
    corpo = re.sub(r"## Abstract\n\n.+?\n\n", "", corpo, count=1, flags=re.S)
    kw = re.search(r"\*\*Keywords:\*\*\s*(.+)", corpo)
    corpo = corpo.replace(kw.group(0), "") if kw else corpo
    extra = {}
    for rot in ("Funding", "Acknowledgements"):
        m = re.search(r"\*\*" + rot + r"\.\*\*.*?(?:\n\n|\Z)", corpo, re.S)
        if m:
            extra[rot] = m.group(0).strip()
            corpo = corpo.replace(m.group(0), "")

    corpo = citacoes_numericas(corpo, refs, perdidas)

    # tabelas (legenda + bloco |...|) e figuras saem do texto para o fim, com o lugar marcado
    def tira_tab(m):
        n = re.search(r"Table (\d+)", m.group(1)).group(1)
        tabelas.append(m.group(0))
        return f'\n<p class="local">[Insert Table {n} about here]</p>\n\n'
    corpo = re.sub(r'(<p class="tabcap">.*?</p>)\s*\n((?:\|.*\n?)+)', tira_tab, corpo)

    def tira_fig(m):
        n = re.search(r"Figure (\d+)", m.group(0)).group(1)
        figuras.append(m.group(0).replace(' class="full"', ""))
        return f'\n<p class="local">[Insert Figure {n} about here]</p>\n\n'
    corpo = re.sub(r"<figure.*?</figure>", tira_fig, corpo, flags=re.S)

    md = lambda s: markdown.markdown(s, extensions=["tables", "sane_lists", "md_in_html"])
    lista = "".join(f"<li>{md(l)[3:-4]}</li>" for _, _, l in refs)
    fim = "".join(f'<div class="fim">{md(t)}</div>' for t in tabelas + figuras)

    capa = (f'<div class="capa"><h1>{titulo()}</h1>'
            f'<div class="resumo"><h2>Abstract</h2><p>{ABSTRACT_JMIS}</p>'
            f'<p><b>Key words and phrases:</b> {kw.group(1).strip() if kw else ""}</p></div></div>')
    html = (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS_JMIS}</style></head>"
            f"<body>{capa}{md(corpo)}<h2 style='page-break-before:always'>References</h2>"
            f"<ol class='refs'>{lista}</ol>{fim}</body></html>")
    return html, perdidas, extra, len(tabelas), len(figuras)


def titulo():
    """titulo do artigo: o H1 da introducao (o montador tira esse H1 do corpo). Antes de 26/10 o
    titulo estava escrito a mao aqui em tres lugares e nao acompanhava a troca feita no s1."""
    p = os.path.join(MAN, ORDEM[0])
    if os.path.exists(p):
        m = re.match(r"\A\s*# ([^\n]+)", open(p, encoding="utf-8").read())
        if m:
            return m.group(1).strip()
    return "Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Favelas"


def folha_de_rosto(extra):
    """pagina de titulo da carta de apresentacao: o que o manuscrito anonimo nao pode levar"""
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS_JMIS}</style></head><body>"
            f"<h1>{titulo()}</h1>"
            "<p style='text-align:center;text-indent:0'>Luciano Martins Figueira (corresponding author)"
            "<br>H&eacute;lio Arthur Reis Irigaray<br><i>Funda&ccedil;&atilde;o Get&uacute;lio Vargas, "
            "Brazilian School of Public and Business Administration (FGV EBAPE), Rio de Janeiro, "
            "Brazil</i></p>"
            "<h2>Contact</h2><p style='text-indent:0'>[Full postal address, e-mail and telephone of "
            "each author]</p><h2>Author biographies</h2><p style='text-indent:0'>[Brief bio of each "
            "author]</p>"
            # concatenacao em vez de f-string: barra invertida dentro de {} so vale no Python 3.12+,
            # e o venv do desktop e 3.11
            + "".join("<p style='text-indent:0'>" + re.sub(r'[*][*](.+?)[*][*]', r'<b>\1</b>', v)
                      + "</p>" for v in extra.values())
            + "</body></html>")


def navegador():
    for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        if os.path.exists(p):
            return p
    sys.exit("nenhum Edge ou Chrome encontrado")


def imprime(html_path, pdf_path):
    os.makedirs(os.path.dirname(os.path.abspath(pdf_path)), exist_ok=True)
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/").lstrip("/")
    r = subprocess.run([navegador(), "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={os.path.abspath(pdf_path)}", url],
                       capture_output=True, timeout=300)
    if not os.path.exists(pdf_path):
        print("falhou ao gerar PDF:", r.stderr.decode("utf-8", "ignore")[-500:], file=sys.stderr)
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "machine-vision-favelas-previa.pdf"))
    ap.add_argument("--formato", choices=["aim", "elsevier", "jmis"], default="elsevier",
                help="aim = uma coluna, Times 12, espaco duplo, que e o que os premiados de "
                     "2026 usam; elsevier = duas colunas de periodico; jmis = submissao ao JMIS, "
                     "anonima, com a folha de rosto num PDF a parte")
    ap.add_argument("--sem-notas", action="store_true")
    ap.add_argument("--com-autoria", action="store_true",
                help="poe os quadros de autoria por secao. Desde 30/09 ficam fora por padrao "
                     "(pedido do autor); so o aviso unico de versao previa entra")
    ap.add_argument("--sem-previa", action="store_true",
                help="tira o aviso unico de versao previa do inicio. E o que se usa na submissao")
    ap.add_argument("--html", default=None, help="grava tambem o HTML intermediario")
    ap.add_argument("--lingua", choices=["en", "pt"], default="en",
                    help="pt: le 01-artigo/manuscrito-pt (traducao) e usa rotulos em portugues")
    args = ap.parse_args()
    global MAN
    if args.lingua == "pt":
        MAN = os.path.join(RAIZ, "01-artigo", "manuscrito-pt")
        ROT.update({"Table": "Tabela", "Figure": "Figura"})

    import markdown

    # Passo 1: numerar figuras e tabelas na ordem de leitura, para que @fig{nome} e @tab{chave}
    # no texto virem "Figure 3" e "Table 5" sem ninguem contar a mao (pedido de 30/09: figuras
    # e tabelas citadas no texto, tabelas com legenda numerada).
    num_fig, num_tab = {}, {}
    for nome in ORDEM:
        p = os.path.join(MAN, nome)
        if not os.path.exists(p):
            continue
        t0 = open(p, encoding="utf-8").read()
        for m in RE_FIG.finditer(t0):
            chave = os.path.splitext(os.path.basename(m.group(1).strip()))[0]
            num_fig.setdefault(chave, len(num_fig) + 1)
        for m in RE_TAB.finditer(t0):
            num_tab.setdefault(m.group(1).strip(), len(num_tab) + 1)

    partes, faltando, n_fig, n_ph, n_sec = [], [], 0, 0, 0
    for nome in ORDEM:
        p = os.path.join(MAN, nome)
        if not os.path.exists(p):
            faltando.append(nome)
            continue
        txt = open(p, encoding="utf-8").read()
        # o titulo ja vem na capa; o H1 que a introducao herdou do docx saia duas vezes no PDF
        txt = re.sub(r"\A\s*# [^\n]*\n+", "", txt)
        # a legenda "aparece como [X]" das notas de proveniencia (blocos de citacao) nao e marcador
        n_ph += sum(ln.count("[X]") for ln in txt.splitlines() if not ln.lstrip().startswith(">"))
        if args.sem_notas:
            txt = re.sub(r"^> \*\*(Status note|Provenance note|Nota de estado).*?(?=\n\n)", "", txt,
                         flags=re.S | re.M)
        txt = re.sub(r"@fig\{([^}]+)\}", lambda m: str(num_fig.get(m.group(1).strip(), "?")), txt)
        txt = re.sub(r"@tab\{([^}]+)\}", lambda m: str(num_tab.get(m.group(1).strip(), "?")), txt)
        txt = resolve_tabelas(txt, num_tab)
        txt, n_fig = resolve_figuras(txt, n_fig)
        n_sec += 1

        # O Abstract e as palavras-chave nao sao secao numerada, e o arquivo da introducao tem os
        # dois como H2 antes do titulo da propria introducao. Numerar o primeiro H2 sem checar
        # produzia "1. Abstract" e deixava a introducao sem numero, que foi o que o PDF mostrou.
        def _numera(m):
            return f"## {n_sec}. {m.group(1)}"

        alvos = [m for m in RE_H2.finditer(txt)
                 if not m.group(1).strip().lower().startswith(("abstract", "keywords", "references", "resumo", "palavras-chave", "referências"))]
        if alvos:
            m = alvos[0]
            txt = txt[:m.start()] + _numera(m) + txt[m.end():]
        if args.com_autoria:
            # o quadro entra ANTES do titulo, e em HTML cru para nao depender do markdown
            q = quadro_autoria(nome)
            if q:
                alvo = RE_H2.search(txt)
                if alvo:
                    txt = txt[:alvo.start()] + q + NL2 + txt[alvo.start():]
                else:
                    txt = q + NL2 + txt
        partes.append(txt)

    if args.formato == "jmis":
        refs_md = partes.pop() if ORDEM[-1] not in faltando else ""
        html, perdidas, extra, n_t, n_f = monta_jmis(partes, refs_md, args)
        tmp = args.html or os.path.join(tempfile.gettempdir(), "artigo_jmis.html")
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(html)
        imprime(tmp, args.out)
        rosto_html = os.path.splitext(tmp)[0] + "-title-page.html"
        with open(rosto_html, "w", encoding="utf-8") as f:
            f.write(folha_de_rosto(extra))
        rosto = os.path.splitext(args.out)[0] + "-title-page.pdf"
        imprime(rosto_html, rosto)
        print(f"tabelas: {n_t}  figuras: {n_f}  placeholders [X]: {n_ph}")
        print(f"abstract: {len(ABSTRACT_JMIS.split())} palavras")
        print(f"citacoes nao resolvidas: {len(perdidas)}")
        for c in perdidas:
            print("   ", c.replace(chr(10), " "))
        print(f"gravado: {args.out}\n         {rosto}")
        return

    corpo = markdown.markdown("\n\n".join(partes),
                              extensions=["tables", "sane_lists", "md_in_html"])
    # a legenda entra na propria tabela (<caption>), para nunca ficar orfa numa pagina quando a
    # tabela, mais alta que a pagina, e empurrada para a seguinte (visto na Tabela 27 da v8 e v9)
    corpo = re.sub(r'<p class="tabcap">(.*?)</p>' + chr(92) + r's*<table>',
                   r'<table><caption class="tabcap">' + chr(92) + r'1</caption>', corpo, flags=re.S)
    # tabela comprida (mais de 10 linhas) pode quebrar entre colunas ou paginas; a curta fica
    # inteira, porque o cabecalho nao se repete entre colunas
    corpo = re.sub(r'<table>(.*?)</table>',
                   lambda m: ('<table class="longa">' if m.group(1).count('<tr>') > 3 else '<table>') + m.group(1) + '</table>',
                   corpo, flags=re.S)

    capa = f"""<div class="capa full">
<h1>{titulo()}</h1>
<div class="autores">Luciano Martins Figueira<sup>a</sup>, H&eacute;lio Arthur Reis Irigaray<sup>a</sup></div>
<div class="afil"><sup>a</sup> Funda&ccedil;&atilde;o Get&uacute;lio Vargas, EBAPE, Rio de Janeiro, Brazil</div>
</div>"""

    aviso = ""
    if not args.sem_previa and args.lingua == "pt":
        aviso += ('<div class="aviso full"><b>Versão prévia, ainda não finalizada.</b> Rascunho de '
                  'trabalho de 27 de outubro de 2026, tradução para o português da versão em inglês, '
                  'compartilhada entre os autores para revisão; números, figuras e referências ainda '
                  'estão em revisão. Os rótulos dentro das figuras permanecem em inglês.</div>')
    elif not args.sem_previa:
        aviso += ('<div class="aviso full"><b>Preliminary version, not final.</b> Working draft of '
                  '27 October 2026, shared among the authors for revision; numbers, figures and '
                  'references are still under review and the text has not been approved by all '
                  'authors. <i>Versão prévia, ainda não finalizada.</i></div>')
    if n_ph:
        aviso = (f'<div class="aviso full"><b>PRÉVIA, NÃO SUBMISSÃO.</b> Este documento contém '
                 f'<b>{n_ph} marcadores <code>[X]</code></b> de números ainda não medidos. '
                 f'Nenhum deles pode ser preenchido por estimativa. Os blocos de citação em destaque '
                 f'são notas de proveniência e de estado e não fazem parte do texto final.</div>')
    if faltando:
        aviso += ('<div class="aviso full"><b>Seções ausentes:</b> ' + ", ".join(faltando) + "</div>")

    if args.lingua == "pt":
        capa = capa.replace("Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Favelas",
                            "Visão computacional a partir do Sul Global: dados sintéticos e os limites de aquisição para a detecção de pessoas armadas em favelas densas").replace("Brazil", "Brasil")
    html = (f"<!doctype html><html lang='{'pt-BR' if args.lingua == 'pt' else 'en'}'><head><meta charset='utf-8'>"
            f"<style>{CSS_ELSEVIER if args.formato == chr(101)+chr(108)+chr(115)+chr(101)+chr(118)+chr(105)+chr(101)+chr(114) else CSS_AIM}</style></head><body>{capa}{aviso}{corpo}</body></html>")

    tmp = args.html or os.path.join(tempfile.gettempdir(), "artigo_previa.html")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(html)

    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if not os.path.exists(edge):
        edge = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    # perfil novo a cada chamada e espera pelo arquivo: o Edge headless as vezes sai antes de gravar
    # o PDF, ou colide com outra instancia aberta (visto em 23/10 no montador do resumo e aqui)
    import time
    perfil = tempfile.mkdtemp(prefix="edge_perfil_")
    if os.path.exists(args.out):
        os.remove(args.out)
    cmd = [edge, "--headless", "--disable-gpu", "--no-pdf-header-footer",
           f"--user-data-dir={perfil}",
           f"--print-to-pdf={os.path.abspath(args.out)}",
           "file:///" + tmp.replace("\\", "/")]
    r = subprocess.run(cmd, capture_output=True, timeout=300)
    fim, tam = time.time() + 120, -1
    while time.time() < fim:
        if os.path.exists(args.out):
            t = os.path.getsize(args.out)
            if t > 0 and t == tam:
                break
            tam = t
        time.sleep(2)
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
