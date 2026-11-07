# 08-conferencia — dossiê AIM 2027

Estratégia de submissão e pesquisa sobre a conferência **AIM 2027** (7ª AI in Management, USC Marshall, Marina del Rey, 19 e 20/03/2027) e sobre os artigos premiados que servem de modelo de formato.

Pesquisa feita entre 21/08 e 09/09/2026. Movida para dentro deste repositório em 20/09/2026, antes vivia solta em `~/Documents/Mestrado/AIM2027/dossie-conferencia/` e só existia no Mac. Conteúdo movido em bloco, sem alteração: os links relativos entre os arquivos continuam válidos.

## Por que está neste repositório

Este é o único repositório compartilhado entre o Mac e o desktop, e o dossiê é o material de referência da conferência para onde o artigo *Machine Vision from the Global South* pode ser submetido. Atenção: os temas T1 a T5 descritos aqui são uma linha de trabalho distinta (GenAI e consumo), levantada quando ainda se avaliava o que submeter. O que vale para qualquer submissão, inclusive a do artigo de visão computacional, é o que está em **Datas e formato**, em **`modelos_2026/`** e no Bloco F do roteiro (ofício do paper).

## Datas e formato

| Item | Valor |
|---|---|
| Submissão | 19/11/2026 |
| Decisão | 19/12/2026 |
| Conferência | 19 e 20/03/2027, USC Marshall (Marina del Rey, Los Angeles) |
| Apresentação | 12 min + 3 de Q&A |
| Contato | AIM@marshall.usc.edu |
| Formato | inferido dos premiados de 2026: extended abstract de 8 a 12 páginas, Times New Roman 12, espaço duplo (ver `modelos_2026/` e M33 a M38) |
| Prêmios | 4 × até US$ 5.000, mestrando **não** é elegível. O retorno é aceite, apresentação e rede |

## Mapa

```
ESTRATEGIA_AIM2027.md   revisão 2 da estratégia: perfil real da conferência, sete arquétipos
                        que vencem, diagnóstico dos temas T1 a T5, plano de 90 dias,
                        pendências e referências com venue e ano conferidos
ROTEIRO.md              índice das 48 missões (48 feitas, 0 pendentes, 0 bloqueadas), com o
                        achado de cada uma resumido na própria tabela. É o índice de leitura
missoes/                MNN_slug.md, uma por missão, em seis blocos:
                          A (M01-M12) T2, o tema de submissão
                          B (M13-M20) T3, o programa de 12 meses
                          C (M21-M26) T1, coletor de longo curso
                          D (M27-M32) T4, a ponte com a dissertação
                          E (M33-M38) conferência e posicionamento (co-chairs, programa 2026,
                                      presença internacional, custos, coautoria, plano B)
                          F (M39-M48) ofício do paper (esqueleto, abstract, método, robustez,
                                      figuras, revisão adversarial, apresentação de 12 min)
eixos/                  EIXO_GENAI_CONSUMO.md, levantamento fora do roteiro (22/08) sobre
                        GenAI e opções de consumo
modelos_2026/           AIM2027_CFP.pdf e quatro papers premiados de 2026 (contigiani, dai,
                        ma, salas), usados como modelo de formato
```

## Versão curta do artigo (04/11/2026)

`versao-curta/`: `versao-curta-aim2027.html` é o texto fonte (corpo de 9,3 mil palavras, 12 tabelas e 5 figuras; em Carta, Times New Roman 12 e espaço duplo dá 44 páginas); `versao-curta-elsevier.html` é o formato principal da submissão (A4 em duas colunas, Times 9,5 pt, 18 páginas), montado por `gera_elsevier.py`, que também roda `pagina.py --colunas 2` para fechar os buracos (figuras e tabelas estreitas flutuam na coluna; blocos largos vão ao topo ou ao pé da página, cortando o parágrafo quando preciso); `esqueleto-aim2027.html` é o extended abstract de 4 mil palavras (18 páginas); `O-QUE-FALTA-NO-SERVIDOR.md` lista o que ainda precisa ser modelado e treinado no desktop, com custos e estado; `gera_pdf.sh` renderiza os três com o Chrome headless (Elsevier primeiro) e deixa cópias autocontidas em `~/Desktop/AIM 2027 - Versao Curta/`. A nota de trabalho em português que abria os PDFs saiu em 04/11, depois das decisões do autor; o texto dela está em `NOTA-DE-TRABALHO.md`. Os PDFs não entram no git.

## Regra de citação herdada

Nenhuma citação entrou sem venue e ano verificados. Fonte que não pôde ser verificada está marcada `[NÃO VERIFICADO]` no texto, e missão impossível está marcada `BLOQUEADA` com o motivo. Manter a regra ao editar.

## Exceção ao .gitignore

`CLAUDE.md` diz que PDF de paper fica fora do git. Os cinco PDFs de `modelos_2026/` são a exceção: somam 11 MB, são o CFP e os modelos de formato exigidos para escrever a submissão, e precisam existir nas duas máquinas. Nenhum outro PDF entra aqui.

## Pendências

- [ ] Confirmar o formato exigido com AIM@marshall.usc.edu (paper completo ou extended abstract, limite de páginas). O Google Form devolve 401 sem login.
- [ ] Award CFP separado, para confirmar elegibilidade.
- [ ] Custo total (inscrição via Eventbrite mais Los Angeles em março) e auxílio da FGV a evento internacional.

Dossiê online (artifact privado, mesmo conteúdo do `ESTRATEGIA_AIM2027.md`): https://claude.ai/code/artifact/311e9ba7-05d9-49ac-af53-7cdd1dcb5184
