# DIÁRIO DE BORDO

Entradas novas no topo. Formato: `## AAAA-MM-DD [MÁQUINA] título`, depois o que foi feito, o que foi decidido e o que ficou para o outro lado. Nunca apagar entrada antiga.

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
