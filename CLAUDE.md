# Machine Vision from the Global South

Artigo em coautoria (mestrando FGV EBAPE + orientador prof. Hélio Arthur Reis Irigaray) propondo um modelo de visão computacional para mapear a morfologia vertical de favelas do Rio (caso: Jacarezinho), treinado com dados sintéticos de motor de jogo, com a ética do uso dual como tema central. Este repositório é a fonte única de verdade do projeto e é compartilhado entre duas máquinas.

## Duas máquinas, um repositório

| Máquina | Papel | O que só existe nela |
|---|---|---|
| DESKTOP (Windows, GPU, sempre ligado) | Central. Blender headless (o ARMA 3 foi abandonado em 11/09), OpenDroneMap, geração de dataset, treino YOLO, avaliação | Datasets, fotogrametria e cenas `.blend`, pesos `.pt`, `runs/` completos. Tudo em `C:\arma3-favela\`, inventariado em `06-resultados/ONDE-ESTAO-OS-DADOS.md` |
| MAC (MacBook Air M1 8 GB) | Cliente leve. Acesso remoto ao desktop e escrita do artigo quando offline | Conectores locais (Obsidian), memórias antigas do Claude |

A memória automática do Claude Code é local por máquina e NÃO é compartilhada. Tudo que o outro lado precisa saber vai para arquivo versionado aqui, nunca só para a memória.

## Protocolo de sessão (vale para qualquer Claude, em qualquer máquina)

1. Ao começar: `git pull --rebase`, depois ler `STATUS.md` e as últimas entradas de `DIARIO.md`.
2. Ao terminar (ou a cada marco): atualizar `STATUS.md`, acrescentar uma entrada em `DIARIO.md` com a etiqueta da máquina (`[DESKTOP]` ou `[MAC]`) e data, fazer commit e `git push`.
3. `STATUS.md` é o retrato atual (reescreve-se). `DIARIO.md` é histórico (só se acrescenta no topo, nunca se apaga).
4. Conflito de merge em `STATUS.md` ou `DIARIO.md`: manter as duas versões, ordenar por data, nunca descartar a entrada do outro lado.
5. Commits pequenos e descritivos, em português. Pedir confirmação antes de qualquer ação destrutiva ou de reescrever histórico.

## Mapa do repositório

```
CLAUDE.md                 este arquivo (instruções comuns)
STATUS.md                 retrato atual: o que está feito, em curso, bloqueado, próximos passos
DIARIO.md                 diário de bordo das duas máquinas
01-artigo/
  rascunhos-professor/    .docx originais do orientador, congelados, nome = data_versão_autor
  manuscrito/             o artigo dividido em um .md por seção (cópia de trabalho; é aqui que se edita)
  PENDENCIAS.md           problemas verificados do rascunho, para resolver e devolver ao orientador
  resumo-artigo-v2.md     resumo por seção
  ferramentas/            docx_para_secoes.py (rodar de novo quando chegar v3)
02-projeto-ufrj-2022/     histórico do projeto drone PCERJ/UFRJ (Miceli, Fábio Guimarães)
03-arma3/                 pipeline ARMA 3 -> bounding box -> YOLO (README-PIPELINE.md + scripts). Tentado em 11/09, sem dado gerado
04-bibliografia/          índices e notas versionados; PDFs ficam fora do git
05-levantamento-3d/       levantamento técnico de 12/09: de onde vem a geometria da favela
06-resultados/            o que o desktop produz: RESULTADOS.md, métricas, figuras leves
07-blender/               pipeline que de fato rodou: Blender headless -> bounding box -> YOLO (README.md + scripts)
08-conferencia/           dossiê da AIM 2027: estratégia, roteiro de 48 missões, eixos e os
                          papers premiados de 2026 que servem de modelo de formato
painel/                   fonte HTML do painel web (artifact) do projeto
docs/                     guias de setup, briefing do pacote de 11/09, contexto acumulado, DIVERGENCIAS.md, AMBIENTE-DESKTOP.md
```

## Regras duras

- Nunca inventar número, métrica, citação ou DOI. Métrica só entra no artigo se estiver em `06-resultados/` com o comando que a gerou. DOI só depois de conferido no Crossref.
- Dados sensíveis: os ortomosaicos do Jacarezinho e de Manguinhos são dados operacionais da PCERJ. Não entram no git, em artifact, em pacote, nem em serviço externo. Nenhuma coordenada em nível de endereço, nenhuma imagem que identifique morador. Vale também para tudo que DERIVA deles: malhas e DSM do OpenDroneMap, cenas `.blend`, renders dos datasets `odm` e `cid150`, mosaicos `train_batch` e `val_batch` desses treinos, e logs com coordenada. Só o braço `v3` (OSM + Poly Haven) pode ser ilustrado.
- Fora do git (ver `.gitignore`): datasets, screenshots do ARMA, pesos, `runs/`, PDFs de papers, zips. Única exceção: os cinco PDFs de `08-conferencia/modelos_2026/` (CFP e modelos de formato da AIM 2027, 11 MB). Binário grande trafega por cópia direta entre as máquinas (scp/rsync via Tailscale), não pelo GitHub.
- Texto entregue ao autor ou ao orientador: sem travessão. Usar vírgula, dois-pontos ou parênteses. O manuscrito herdado do orientador ainda tem travessões; removê-los é item de `PENDENCIAS.md`.
- Documento acadêmico para leitura sai em PDF ou .docx, não como página estilizada. O painel web é só para estado do projeto.
- Ao citar o pipeline ARMA 3, creditar Fábio H. P. Guimarães (proposta, 2022) e prof. Claudio Miceli de Farias (orientação).

## Painel web

Endereço: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH (artifact privado, ligado à conta claude.ai, não à máquina).
Para atualizar de qualquer máquina: editar os blocos marcados com `ESTADO` em `painel/painel.html` a partir de `STATUS.md` e `DIARIO.md`, e republicar com a ferramenta Artifact passando esse endereço em `url` (ler o artifact antes, a ferramenta exige). Sem `url` nasce um painel novo em outro endereço, o que não queremos. Nada sensível no painel.

## Contexto acumulado

@docs/CONTEXTO.md
