# DIÁRIO DE BORDO

Entradas novas no topo. Formato: `## AAAA-MM-DD [MÁQUINA] título`, depois o que foi feito, o que foi decidido e o que ficou para o outro lado. Nunca apagar entrada antiga.

## 2026-09-21 [DESKTOP] Os primeiros números de sim-to-real, e três defeitos que eles revelaram

Primeira vez que o projeto tem a razão de eficácia que o artigo precisa. Também a primeira vez que
três defeitos de geração aparecem no mesmo dia, todos da mesma família: código que roda sem erro e
produz dado errado.

### Os números

| | mAP50 | arquivo |
|---|---|---|
| S-nadir no próprio sintético | 0,7915 | `resultados/s_nadir_4k.json` |
| S-nadir zero-shot no VisDrone | 0,0102 | `06-resultados/sim2real_s_nadir_4k.json` |
| R pareado, 1.106 imagens reais, hiperparâmetros idênticos | 0,6311 | `resultados/r_pareado.json` |
| razão de eficácia | **1,6%** | |

O braço real usa os MESMOS hiperparâmetros e o MESMO N do sintético (yolo11s, 1280 px, 60 épocas,
batch 6, init COCO). Na rodada anterior os dois diferiam em modelo, imgsz, épocas e inicialização
ao mesmo tempo, e por isso a comparação não isolava nada.

### Três defeitos

1. **Braço oblíquo: 180 imagens, 992 pessoas, zero caixas.** O recuo da câmera tinha o sinal
   trocado, e o filtro de enquadramento usava um raio derivado da largura do quadro NADIR, que não
   vale com a câmera inclinada. Corrigido apontando a câmera com `to_track_quat` e trocando o
   filtro por projeção. 2,6 h de render perdidas.
2. **Lote armado com 7,4 pessoas por imagem em vez de 14 a 30.** Mesma causa: o raio de aceitação
   encolhe junto com a altura, e a 75 m caía de 49 m para 24 m. Refeito depois da correção.
3. **`data.yaml` com duas classes tendo três nos rótulos.** O gerador passou a emitir
   `pessoa_objeto` mas o writer do yaml continuou declarando duas. Quebraria o treino horas depois
   do render. Agora conta as classes que foram de fato escritas.

Freio novo no gerador: se cinco quadros renderizarem sem nenhuma caixa, aborta. Foi o que faltou
no item 1, e é o tipo de coisa que só se descobre pagando.

### Correções de número que mudam argumento

- **O alvo mediano é 17,5 px, não 24,6.** 24,6 é o percentil 90 da largura. A área do nosso alvo
  bate com a do VisDrone em 1,00x (301 contra 300 px²) e o que difere é FORMA, por 2,04x (h/w 0,98
  contra 2,00). Ferramenta em `06-resultados/mede_alvo.py`.
- **Kiefer et al. conferido na fonte.** A métrica é mAP@50, como as notas diziam. O intervalo
  "1,2 a 2,4" omitia a linha do YOLO, que é o nosso detector e marca 10,2 sintético contra 43,9
  real, ou 23,2% de razão. Estamos catorze vezes abaixo da referência que se aplica, não "na mesma
  ordem de grandeza" como eu havia dito.
- **Liao et al. conferido na fonte.** Tirar variação de luz, clima e ângulo custa 30,4 pontos no
  YOLOv11. Trocar base fotogramétrica por assets genéricos custa 27,0. O artigo é inconsistente
  consigo mesmo entre 22,5 e 23,3 na média. O objeto deles é VEÍCULO, não pessoa.
- **O denominador da literatura é outro.** Liao compara contra um real treinado FORA do domínio de
  teste (36,4 no VisDrone); nós comparamos contra um real treinado no PRÓPRIO VisDrone (63,1). Por
  isso eles dão 94% e nós 1,6%. O artigo precisa reportar os dois.

Fichas em `04-bibliografia/kiefer-2022-numeros-conferidos.md` e `liao-2026-numeros-conferidos.md`.

### O que entrou no código

- `07-blender/scripts/sitios.py`: coleção de 40 sítios variando relevo (plano, morro, dois morros,
  encosta), avenida com asfalto e carros, densidade, altura média e regime de mata. O índice -1 é o
  sítio histórico, e foi conferido que reproduz byte a byte o `ds_morro_4k` (4.068 lotes, 439
  edificações, 208.396 faces com semente 21).
- `07-blender/scripts/fila_noite.py`: fila de 22 etapas, uma GPU de cada vez, com log por etapa e
  retomada pelo arquivo de saída.
- `07-blender/PLANO-EXPERIMENTAL.md`: quatro frentes com custo de GPU declarado.

### Decidido pelo autor

- Nenhuma imagem real de pessoa armada entra. O braço armado é 100% sintético.
- O teste de dose de variedade (6 sítios x 30 imagens contra 1 sítio x 180, mesmo total) roda antes
  do treino no VisDrone inteiro, que passa a ser o último da fila.
- A escala futura vai por número de SÍTIOS, não por número de imagens do mesmo sítio.

### Para o outro lado

Os três números de sim-to-real do artigo ainda não existem todos: há o zero-shot, falta o com 5 a
10% de dado real e o sintético mais real. São as frentes C do plano. E o braço oblíquo precisa ser
refeito: é ele que decide se o 1,6% é problema de síntese ou de geometria de captura.

## 2026-09-20 [MAC] Dossiê da AIM 2027 entra no repositório

A pesquisa sobre a conferência e sobre os artigos do congresso só existia no Mac, na pasta irmã `~/Documents/Mestrado/AIM2027/dossie-conferencia/`. Movida em bloco para `08-conferencia/`, sem alteração de conteúdo, para que o desktop consiga puxar: `ESTRATEGIA_AIM2027.md` (revisão 2), `ROTEIRO.md` (48 missões, todas feitas), `missoes/` (48 arquivos, blocos A a F), `eixos/EIXO_GENAI_CONSUMO.md` e `modelos_2026/` (CFP mais os quatro papers premiados de 2026). Um `README.md` novo explica o conjunto, as datas da conferência e o formato da submissão.

Numeração: a pasta nasceu como `07-conferencia` no Mac e virou `08-conferencia` no rebase, porque o desktop já havia publicado `07-blender/`.

Decidido:
- Os cinco PDFs de `modelos_2026/` (11 MB) são a única exceção à regra de não versionar PDF de paper: são o CFP e o modelo de formato da submissão, e precisam existir nas duas máquinas. Registrado em `CLAUDE.md` e no `.gitignore`.
- Os temas T1 a T5 do dossiê são linha de pesquisa distinta (GenAI e consumo), levantada quando ainda se avaliava o que submeter. O que serve ao artigo de visão computacional é o calendário, o formato exigido, os modelos de 2026 e o Bloco F (ofício do paper).

Para o desktop: depois do `git pull`, o dossiê está em `08-conferencia/`. A pasta `dossie-conferencia/` do Mac não existe mais.

## 2026-09-20 [DESKTOP] Decisão: o método é o Blender

O autor decidiu adotar o Blender como método do trabalho e do artigo, por facilitar a escrita e a criação dos scripts em Python e por ser o caminho mais eficaz pelo que o levantamento mostrou. Isso fecha o item 1 de `docs/DIVERGENCIAS.md`. O ARMA 3 passa a constar como origem da ideia em 2022 e como prior art via G-MAD, não como método executado.

Também foi feito o levantamento de qual é a melhor modelagem disponível hoje. É a "cidade de sólidos" do braço `cid150`: sólidos por edificação segmentados do DSM da PCERJ, paredes e lajes com PBR autoral do Poly Haven, sol livre. Renders de referência em `C:\arma3-favela\odm\cidade\` (5 câmeras, 1920x1080) e cena em `C:\arma3-favela\odm\quadra.blend`. É também o braço com o melhor mAP50 no sintético (0,676). Nada disso entra no git nem no painel, porque a geometria vem do dado da PCERJ (item 2 das divergências, ainda aberto).

Fica para o autor: aplicar a decisão no texto do manuscrito, e decidir os itens 2, 3 e 4 das divergências.

## 2026-09-18 [DESKTOP] Reconciliação com o repositório

Feito (17 e 18/09):
- `gh` instalado e autenticado, repositório clonado em `C:\projetos\machine-vision-favelas`, identidade git configurada só no clone.
- Inventário completo, só leitura, da pasta real de trabalho, que é `C:\arma3-favela\` (44 GB, não era repositório git, então não havia histórico a preservar). Nenhum processo de treino ou render estava rodando.
- Código do desktop copiado: pasta nova `07-blender/` (19 scripts Python, 8 de batelada, README), missão e automação do ARMA 3 em `03-arma3/missao/` e `03-arma3/scripts/windows/`, `capturaDataset.sqf` e `train_yolo.py` sobrescritos pelas versões do desktop.
- `06-resultados/`: `RESULTADOS.md` com a ficha do experimento no topo (cada número com arquivo e comando de origem), 5 runs com `args.yaml`, `results.csv`, curvas, matrizes, `val_final.json` e `val_por_classe.txt`, manifests de randomização dos 5 datasets, `ONDE-ESTAO-OS-DADOS.md` com SHA256 de 13 arquivos de pesos. Previews com caixas só do braço OSM.
- `docs/DIVERGENCIAS.md` (14 itens), `docs/AMBIENTE-DESKTOP.md`, seção "Vindo do desktop" e linha do tempo corrigida em `docs/CONTEXTO.md`, cópia da nota do Obsidian, `05-levantamento-3d/desktop/LEIA-ME.md`.
- Três citações conferidas em 18/09: Liao et al. 2026 e Berwaldt et al. 2020 no Crossref, G-MAD no arXiv.
- `STATUS.md`, `PENDENCIAS.md` (C5, D4 e novos D5 a D8), `CLAUDE.md` (mapa e tabela de máquinas) e painel atualizados.

Descoberto:
- O experimento não rodou no ARMA 3. Foi tentado em 11/09 e abandonado na mesma noite sem nenhuma captura. Tudo foi feito no Blender 5.2.1 headless.
- Três dos quatro braços usam fotogrametria das fotos da PCERJ, refeita no OpenDroneMap porque o processamento de 2022 se perdeu. Nada saiu do desktop.
- As classes são `pessoa_armada` e `pessoa_desarmada`.
- Nenhum número de sim-to-real existe. O VisDrone nunca foi baixado.
- A pesquisa "a partir do e-mail de 12/09" não foi feita no desktop. A prova de conceito da quadra é anterior ao e-mail e independente dele.

Decidido (pelo desktop, dentro das regras de precedência, com OK geral do autor em 18/09):
- Código Blender em pasta própria `07-blender/`, não dentro de `03-arma3/`.
- Nenhuma imagem com textura ou geometria PCERJ entra no git: dos runs `blender_odm_tiles` e `cid150_s` só entraram números e gráficos. Nenhum `.log` entrou (um deles tem latitude e longitude do voo).
- Scripts do Google 3D Tiles ficaram de fora.
- Caminhos absolutos nos scripts não foram consertados agora; proposta registrada.

Fica para o autor: as quatro divergências abertas (itens 1 a 4 de `docs/DIVERGENCIAS.md`) e o OK para a mudança de base de trabalho.

Fica para o Mac: ler `docs/DIVERGENCIAS.md` e `05-levantamento-3d/desktop/LEIA-ME.md` antes de tocar em `06-results-proposed-model.md` e em Limitations; o que o Mac sabia sobre "pipeline ARMA 3" está superado. Os itens D1 a D3 de `PENDENCIAS.md` continuam valendo e agora têm as citações conferidas.

## 2026-09-17 [MAC] Prompt de reconciliação para o desktop

O autor informou que o desktop avançou muito (modelo já treinado) e que há uma pesquisa feita lá a partir do e-mail de 12/09 ("Levantamento técnico: recriar quarteirão de favela em 3D com alta fidelidade", enviado de si para si). Esse e-mail é o resumo do levantamento cujo PDF completo só existia no Mac e agora está em `05-levantamento-3d/`. `docs/PROMPT-MIGRACAO-DESKTOP.md` foi reescrito (versão 2) para esse cenário: fases com parada para aprovação, regras de precedência (desktop prevalece em experimento e código, repositório prevalece em estrutura e manuscrito, pesquisa é união), divergências registradas em `docs/DIVERGENCIAS.md`. O prompt também está no painel, com botão de copiar.

Para o desktop: tudo que este lado afirma sobre o experimento está desatualizado. Corrigir sem cerimônia, com arquivo de origem para cada número.

## 2026-09-17 [MAC] Reorganização da pasta e repositório único

Feito:
- Pasta `~/Documents/Mestrado/AIM2027/` separada em duas áreas: `dossie-conferencia/` (estratégia AIM 2027, roteiro, 48 missões, eixos, modelos de formato; movidos em bloco, links relativos preservados) e `machine-vision-favelas/` (este projeto).
- As três pastas soltas (PROJETO MACHINE VISION FAVELAS, PROJETO DRONE PCERJ, PESQUISA CV DRONES) foram fundidas aqui, na mesma estrutura numerada do pacote de 11/09 que o desktop recebeu.
- Rascunhos do orientador copiados de `~/Downloads` para `01-artigo/rascunhos-professor/`. Achado: `Machine Vision from the Global South(2).docx`, baixado em 17/09, tem o mesmo MD5 do `(1)` de 10/09. Não existe v3.
- v2 dividida em 8 arquivos Markdown por seção com `01-artigo/ferramentas/docx_para_secoes.py` (só biblioteca padrão, roda igual no Windows). Texto verbatim.
- Auditoria do rascunho refeita e ampliada em `01-artigo/PENDENCIAS.md`.
- Criados `CLAUDE.md`, `STATUS.md`, este diário, `docs/CONTEXTO.md` (conhecimento que estava só na memória do Claude do Mac) e os guias de setup do desktop.

- Repositório privado criado e publicado: https://github.com/LulianoM/machine-vision-favelas. O primeiro commit tem a tag `v2-irigaray-verbatim` (texto do orientador sem nenhuma alteração). Painel web publicado: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH

Decidido:
- Um repositório git é a fonte única de verdade. O desktop é a máquina central. A memória automática do Claude não é canal de comunicação entre máquinas.
- Scripts em `03-arma3/scripts/` aqui são os ORIGINAIS de 11/09. As versões do desktop, se evoluíram, prevalecem: o desktop sobrescreve e o git mostra a diferença.

Para o desktop:
- Seguir `docs/PROMPT-MIGRACAO-DESKTOP.md`. O mais urgente é `06-resultados/RESULTADOS.md` e a atualização do `STATUS.md` com o estado real do treino.
