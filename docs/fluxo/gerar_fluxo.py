#!/usr/bin/env python3
"""Gera docs/fluxo/fluxo-do-trabalho.svg: os blocos do trabalho e a ordem de construção.

Para mudar o diagrama, edite a lista FASES abaixo e rode de novo:
    python3 gerar_fluxo.py
Só biblioteca padrão. O PNG é tirado do SVG com o Chrome em modo headless (ver LEIA-ME).
"""
from html import escape
from pathlib import Path

# tipo do bloco -> (cor do traço, cor de fundo, rótulo)
TIPOS = {
    "escrita": ("#1C69AD", "#EDF4FB", "ESCRITA"),
    "conhecimento": ("#B45E2A", "#FCF2EA", "CONHECIMENTO"),
    "experimento": ("#2B7A52", "#EAF6EF", "EXPERIMENTO"),
}
INK, GREY, LINE, GROUND = "#17212A", "#4C5A67", "#8E9BA8", "#F4F6F8"

# (título em 1 ou 2 linhas, tipo, linhas do corpo, situação ou None)
FASES = [
    ("FASE 1 · FUNDAMENTAÇÃO", "Por que o problema existe", None, [
        (["Introdução"], "escrita",
         ["O policiamento aéreo pensa plano; a favela", "vertical é um quarto tipo de ambiente.", "Lacuna, pergunta e objetivo."],
         "existe na v2"),
        (["Revisão de literatura"], "escrita",
         ["Três frentes: UAV em trajetória e policiamento;", "visão computacional em assentamentos", "informais; dados sintéticos e sim-to-real."],
         "existe na v2, faltam 13 referências"),
        (["Contexto: segurança", "pública no Rio"], "escrita",
         ["Letalidade policial, Exceptis, Contenção,", "ADPF 635, drones do crime, expansão da COANT."],
         "existe na v2, trocar fontes frágeis"),
        (["O campo: Jacarezinho"], "escrita",
         ["Território, morfologia vertical (lajes, becos,", "encosta) e histórico de operações."],
         "existe na v2"),
    ]),
    ("FASE 2 · DESENHO DA PESQUISA", "Como vamos responder", None, [
        (["Metodologia e", "posicionalidade"], "escrita",
         ["Design science mais campo. Coautor delegado:", "vieses assumidos e como são contornados."],
         "existe na v2"),
        (["Ética e uso dual"], "escrita",
         ["Sem imagem de morador, sem coordenada,", "dado sensível da PCERJ fora do pipeline."],
         "existe na v2, espalhada em duas seções"),
        (["Especificação do", "campo sintético"], "conhecimento",
         ["O que a cena precisa ter para valer como", "favela vertical: alturas irregulares, lajes,", "becos, oclusão, caixas d'água, encosta."],
         "a construir"),
        (["Origem da geometria"], "conhecimento",
         ["Cena do ARMA 3, ortofoto IPP 2024 (aberta),", "LiDAR a pedir. A geometria pesa mais", "que a textura."],
         "levantamento de 12/09 feito, falta virar texto"),
    ]),
    ("FASE 3 · EXPERIMENTO", "Roda no desktop", "estado real: aguardando a reconciliação do desktop", [
        (["Construção do campo"], "experimento",
         ["Missão no ARMA 3. Randomização estruturada:", "sol, clima, altitude, ângulo, posição."], None),
        (["Captura dos dados"], "experimento",
         ["Screenshots em lote e log do motor", "com as caixas de cada objeto."], None),
        (["Anotação automática"], "experimento",
         ["O log vira rótulo YOLO. Conferência visual", "das caixas antes de treinar."], None),
        (["Treinamento"], "experimento",
         ["Detector YOLO treinado só no sintético."], None),
        (["Validação no sintético"], "experimento",
         ["mAP no conjunto de validação gerado."], None),
        (["Teste em imagem real"], "experimento",
         ["VisDrone: zero-shot; com 5 a 10% de real;", "sintético mais real. São os três números", "que vão para o artigo."], None),
    ]),
    ("FASE 4 · FECHAMENTO", "O que achamos e o que significa", None, [
        (["Resultados"], "escrita",
         ["Os três números, o que o pipeline prova e o", "que ainda não prova (classes de edificação)."],
         "a v2 é conceitual: reescrever com os números"),
        (["Discussão e limitações"], "escrita",
         ["Limites do sintético, viés do olhar policial,", "caso único. A ética volta ao centro."],
         "existe na v2, ajustar ao resultado"),
        (["Conclusão e agenda futura"], "escrita",
         ["Fecho do argumento, taxonomia dos quatro", "ambientes, próximos passos com consentimento."],
         "falta o fecho"),
        (["Resumo, referências", "e formato"], "escrita",
         ["Abstract e palavras-chave. Introdução", "reenquadrada: de conceitual a empírico."],
         "a construir"),
        (["Revisão com o orientador", "e submissão"], "escrita",
         ["Devolutiva ao prof. Irigaray e versão final", "em .docx ou PDF."],
         "futuro"),
    ]),
]

M, COL_W, GUT = 50, 390, 70
TOP_BOX = 262
GAP = 30
FONT = "'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "Menlo,Consolas,monospace"


def altura(bloco):
    titulo, _tipo, corpo, situacao = bloco
    return 16 + 24 * len(titulo) + 6 + 19 * len(corpo) + (36 if situacao else 0) + 14


def main():
    out = []
    caixas = {}  # número -> (x, y, w, h)
    n = 0
    fundo_max = 0
    for c, (_nome, _sub, _nota, blocos) in enumerate(FASES):
        x = M + c * (COL_W + GUT)
        y = TOP_BOX
        for bloco in blocos:
            n += 1
            h = altura(bloco)
            caixas[n] = (x, y, COL_W, h)
            y += h + GAP
        fundo_max = max(fundo_max, y - GAP)
    W = 2 * M + 4 * COL_W + 3 * GUT
    H = fundo_max + 190

    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
    out.append(f'''<defs>
  <marker id="seta" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GREY}"/></marker>
  <marker id="setaA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#B45E2A"/></marker>
  <marker id="setaB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#2B7A52"/></marker>
</defs>''')
    out.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')
    out.append(f'<text x="{M}" y="72" font-size="34" font-weight="700" fill="{INK}">Fluxo de construção do trabalho</text>')
    out.append(f'<text x="{M}" y="104" font-size="17" fill="{GREY}">Machine Vision from the Global South: blocos de escrita, de conhecimento e de experimento, na ordem em que se apoiam</text>')

    # cabeçalhos das fases, em forma de seta para a direita
    hy, hh = 140, 66
    for c, (nome, sub, nota, _b) in enumerate(FASES):
        x = M + c * (COL_W + GUT)
        ponta = 26
        esq = f"{x},{hy} " if c == 0 else f"{x},{hy} {x + ponta},{hy + hh / 2} {x},{hy + hh} "
        if c == 0:
            pts = f"{x},{hy} {x + COL_W},{hy} {x + COL_W + ponta},{hy + hh / 2} {x + COL_W},{hy + hh} {x},{hy + hh}"
        else:
            pts = f"{x},{hy} {x + COL_W},{hy} {x + COL_W + ponta},{hy + hh / 2} {x + COL_W},{hy + hh} {x},{hy + hh} {x + ponta},{hy + hh / 2}"
        out.append(f'<polygon points="{pts}" fill="{INK}"/>')
        tx = x + (20 if c == 0 else 44)
        out.append(f'<text x="{tx}" y="{hy + 28}" font-size="17" font-weight="700" fill="#FFFFFF" letter-spacing="0.6">{escape(nome)}</text>')
        out.append(f'<text x="{tx}" y="{hy + 50}" font-size="14.5" fill="#C9D3DC">{escape(sub)}</text>')
        if nota:
            out.append(f'<text x="{x + COL_W / 2}" y="{hy + hh + 30}" font-size="13" font-style="italic" fill="{GREY}" text-anchor="middle">{escape(nota)}</text>')

    # blocos e setas verticais
    n = 0
    for c, (_nome, _sub, _nota, blocos) in enumerate(FASES):
        for i, (titulo, tipo, corpo, situacao) in enumerate(blocos):
            n += 1
            x, y, w, h = caixas[n]
            cor, fundo, rotulo = TIPOS[tipo]
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fundo}" stroke="{cor}" stroke-width="2"/>')
            out.append(f'<circle cx="{x + 28}" cy="{y + 30}" r="15" fill="{cor}"/>')
            out.append(f'<text x="{x + 28}" y="{y + 35.5}" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">{n}</text>')
            out.append(f'<text x="{x + w - 14}" y="{y + 20}" font-size="10.5" font-family="{MONO}" fill="{cor}" text-anchor="end" letter-spacing="0.8">{rotulo}</text>')
            ty = y + 16 + 20
            for linha in titulo:
                out.append(f'<text x="{x + 54}" y="{ty}" font-size="19" font-weight="700" fill="{INK}">{escape(linha)}</text>')
                ty += 24
            ty += 2
            for linha in corpo:
                out.append(f'<text x="{x + 18}" y="{ty + 4}" font-size="14.5" fill="{GREY}">{escape(linha)}</text>')
                ty += 19
            if situacao:
                out.append(f'<line x1="{x + 18}" y1="{ty + 5}" x2="{x + w - 18}" y2="{ty + 5}" stroke="{cor}" stroke-opacity="0.35" stroke-dasharray="2 3"/>')
                out.append(f'<text x="{x + 18}" y="{ty + 24}" font-size="12.5" font-family="{MONO}" fill="{cor}">{escape(situacao)}</text>')
            if i < len(blocos) - 1:
                ax = x + w / 2
                out.append(f'<line x1="{ax}" y1="{y + h + 3}" x2="{ax}" y2="{y + h + GAP - 3}" stroke="{GREY}" stroke-width="2" marker-end="url(#seta)"/>')
            elif c < len(FASES) - 1:
                out.append(f'<text x="{x + w}" y="{y + h + 24}" font-size="13.5" font-style="italic" fill="{GREY}" text-anchor="end">continua na Fase {c + 2}  →</text>')

    # ligação A: o campo observado alimenta a especificação da cena (4 -> 7)
    x4, y4, w4, h4 = caixas[4]
    x7, y7, _w7, h7 = caixas[7]
    ax1, ay1, ax2, ay2 = x4 + w4 + 2, y4 + h4 / 2, x7 - 3, y7 + h7 / 2
    out.append(f'<path d="M{ax1},{ay1} C{ax1 + 58},{ay1} {ax2 - 58},{ay2} {ax2},{ay2}" fill="none" stroke="#B45E2A" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#setaA)"/>')
    mx, my = (ax1 + ax2) / 2, (ay1 + ay2) / 2
    out.append(f'<circle cx="{mx}" cy="{my}" r="11" fill="{GROUND}" stroke="#B45E2A" stroke-width="1.5"/><text x="{mx}" y="{my + 4.5}" font-size="13" font-weight="700" fill="#B45E2A" text-anchor="middle">A</text>')

    # ligação B: laço de iteração do experimento (14 -> 9)
    x9, y9, w9, h9 = caixas[9]
    x14, y14, _w14, h14 = caixas[14]
    lx = x9 + w9 + 36
    out.append(f'<path d="M{x9 + w9 + 2},{y14 + h14 / 2} H{lx} V{y9 + h9 / 2} H{x9 + w9 + 4}" fill="none" stroke="#2B7A52" stroke-width="2" stroke-dasharray="7 5" stroke-linejoin="round" marker-end="url(#setaB)"/>')
    by = (y9 + h9 / 2 + y14 + h14 / 2) / 2
    out.append(f'<circle cx="{lx}" cy="{by}" r="11" fill="{GROUND}" stroke="#2B7A52" stroke-width="1.5"/><text x="{lx}" y="{by + 4.5}" font-size="13" font-weight="700" fill="#2B7A52" text-anchor="middle">B</text>')

    # legenda
    ly = fundo_max + 62
    out.append(f'<line x1="{M}" y1="{ly - 26}" x2="{W - M}" y2="{ly - 26}" stroke="{LINE}" stroke-opacity="0.6"/>')
    lx0 = M
    for tipo, desc in (("escrita", "seção do artigo"), ("conhecimento", "pesquisa e decisão de desenho"), ("experimento", "roda no desktop")):
        cor, fundo, rotulo = TIPOS[tipo]
        out.append(f'<rect x="{lx0}" y="{ly - 14}" width="26" height="18" rx="3" fill="{fundo}" stroke="{cor}" stroke-width="2"/>')
        out.append(f'<text x="{lx0 + 36}" y="{ly}" font-size="14.5" fill="{INK}"><tspan font-weight="700">{rotulo.capitalize()}</tspan>: {desc}</text>')
        lx0 += {"escrita": 290, "conhecimento": 410, "experimento": 330}[tipo]
    out.append(f'<line x1="{lx0}" y1="{ly - 5}" x2="{lx0 + 40}" y2="{ly - 5}" stroke="{GREY}" stroke-width="2" marker-end="url(#seta)"/>')
    out.append(f'<text x="{lx0 + 52}" y="{ly}" font-size="14.5" fill="{INK}">sequência</text>')
    out.append(f'<line x1="{lx0 + 160}" y1="{ly - 5}" x2="{lx0 + 200}" y2="{ly - 5}" stroke="{GREY}" stroke-width="2" stroke-dasharray="7 5"/>')
    out.append(f'<text x="{lx0 + 212}" y="{ly}" font-size="14.5" fill="{INK}">alimenta ou retroalimenta</text>')
    out.append(f'<text x="{M}" y="{ly + 36}" font-size="14.5" fill="{INK}"><tspan font-weight="700" fill="#B45E2A">A</tspan>  O que se observa no campo (4) vira o que se modela na cena (7).</text>')
    out.append(f'<text x="{M}" y="{ly + 60}" font-size="14.5" fill="{INK}"><tspan font-weight="700" fill="#2B7A52">B</tspan>  Se a distância entre sintético e real for grande no teste (14), volta-se à construção do campo (9) e varia-se mais a cena.</text>')
    out.append(f'<text x="{M}" y="{ly + 94}" font-size="13.5" font-style="italic" fill="{GREY}">Ordem de construção do trabalho, não necessariamente a ordem final das seções. A linha em fonte fixa dentro de cada bloco é a situação em 17/09/2026.</text>')
    out.append("</svg>")

    destino = Path(__file__).with_name("fluxo-do-trabalho.svg")
    destino.write_text("\n".join(out), encoding="utf-8")
    print(destino, W, H)


if __name__ == "__main__":
    main()
