# Machine Vision from the Global South: pacote de contexto do projeto

Gerado em 2026-09-11 a partir do computador principal do Felipe (Luciano Martins Figueira). Este pacote existe para que um segundo computador, sem nenhum contexto prévio, consiga entender o projeto inteiro e executar o experimento de treinamento com bounding boxes gerados no ARMA 3.

Se você é o Claude Code rodando na outra máquina: leia este arquivo inteiro, depois `03-arma3/README-PIPELINE.md`, e só então comece a executar. O prompt de partida sugerido está em `PROMPT-PARA-CLAUDE-CODE.md`.

## 1. O que é o projeto, em uma frase

Artigo acadêmico em coautoria entre Felipe (mestrando, MEX FGV EBAPE 2026.2) e seu orientador, prof. Hélio Arthur Reis Irigaray (FGV EBAPE), propondo um modelo de visão computacional para mapear a morfologia vertical de favelas do Rio (caso: Jacarezinho), treinado com dados sintéticos gerados em motor de jogo, com discussão ética central sobre uso dual em segurança pública.

Título atual: **"Machine Vision from the Global South: Developing an AI Model for Vertical Favelas"**.

## 2. Linha do tempo

| Quando | O que |
|---|---|
| mar a ago/2022 | Projeto de pesquisa e extensão no BCMT-UFRJ com prof. Claudio Miceli (NCE-UFRJ) e Fábio H. P. Guimarães (perito da Polícia Civil do RJ, mestrando). Tema: detecção de ameaças (pessoas armadas) em imagens RGB-T de drone com CNN treinada em dados sintéticos do ARMA 3. Chegou ao estágio de dataset sintético com bounding box e ortomosaicos reais do Jacarezinho e Manguinhos. Ver `02-projeto-ufrj-2022/`. |
| 2026-09-09 | Levantamento de 15 artigos sobre CV + drones + segurança pública com ranking JIF. Ver `04-bibliografia/`. |
| 2026-09-09 e 10 | Orientador (Irigaray) escreve duas versões do artigo (v1 com 3.200 palavras, v2 com 7.000 palavras). A v2 está em `01-artigo/`, com resumo em `01-artigo/resumo-artigo-v2.md`. |
| 2026-09-11 | Este pacote. Próximo passo: rodar o experimento no ARMA 3 na outra máquina para testar a metodologia proposta na Seção 7 do artigo. |

## 3. O argumento do artigo (resumo de 10 linhas)

1. A literatura de planejamento de trajetória de UAV trata ambientes 3D complexos (montanha, cânion urbano), mas a literatura de policiamento aéreo modela tudo como problema horizontal (rede de ruas, caixeiro-viajante).
2. Favela verticalizada não é caso especial de montanha: encosta + construção sobreposta + lajes ocupadas + becos + GPS degradado + oclusão + pedestres.
3. Taxonomia proposta: terreno plano, terreno montanhoso, cidade formal 3D, ambiente informal verticalmente complexo (o quarto é o gap).
4. Duas literaturas que não se cruzam: UAV em policiamento/defesa e UAV em mapeamento de assentamentos informais.
5. Pergunta de pesquisa: como visão computacional terrain-aware melhora percepção, navegação e consciência situacional de UAV em ambientes informais verticalmente complexos?
6. Objetivo: propor e validar conceitualmente um modelo que mapeie a morfologia vertical do Jacarezinho, com dados sintéticos e observação de campo.
7. Metodologia: revisão de literatura + design science + contextualização qualitativa com material autoetnográfico (um dos autores é delegado da ativa com experiência no Jacarezinho).
8. Contexto: letalidade policial no RJ, Operação Exceptis (2021, Jacarezinho) e Operação Contenção (2025, Alemão e Penha, uso de drones pelo CV, expansão da COANT da Polícia Civil), ADPF 635.
9. Modelo proposto (Seção 7): backbone CNN de classificação estrutural (categorias de altura, adições em laje, transição de material) + pipeline sintético com structured domain randomization (Prakash et al. 2019) + fine-tuning limitado e consentido com dados reais.
10. Limitações declaradas: nada foi treinado nem validado. É exatamente isso que o experimento no ARMA 3 começa a atacar.

## 4. O que o experimento no ARMA 3 deve provar (e o que não prova)

**Prova:** que o pipeline "cena sintética em motor de jogo com anotação automática de bounding box, domain randomization, treino de detector, teste em imagem real" funciona de ponta a ponta e produz um número de mAP em imagem aérea real. Isso é a validação de método que o artigo diz não ter feito ("Whether a synthetic-training pipeline ... actually closes the sim-to-real gap ... is an empirical question this article does not answer").

**Não prova:** que o modelo mapeia morfologia vertical de favela. As classes do experimento de 2022 são pessoas (armadas ou não) vistas de cima. Para chegar às classes do artigo (altura de edificação, adição em laje, material) é preciso um segundo experimento com cenas de edificações empilhadas. O pipeline é o mesmo, só muda o que se anota. O `README-PIPELINE.md` explica como estender.

Recomendação: rodar primeiro o experimento de pessoas (reproduz 2022, valida o pipeline em 1 ou 2 dias), depois o de edificações.

## 5. Estrutura do pacote

```
00-LEIA-PRIMEIRO.md              este arquivo
PROMPT-PARA-CLAUDE-CODE.md       prompt de partida para a outra máquina
01-artigo/
  Machine Vision ... v2 (2026-09-10).docx   versão atual do orientador (7.020 palavras)
  Machine Vision ... v1 (2026-09-09).docx   versão anterior (3.205 palavras)
  artigo-v2-texto-extraido.txt              texto puro da v2
  resumo-artigo-v2.md                       resumo por seção + problemas encontrados
02-projeto-ufrj-2022/
  Projeto Drone PCERJ - UFRJ 2022.md        histórico, pessoas, cronograma, onde está o material
  Bibliografia - Projeto Drone PCERJ.md     19 papers do Fábio em 3 eixos
  decks-reunioes-2022.md                    transcrição dos decks e do cronograma do Drive
03-arma3/
  README-PIPELINE.md                        passo a passo: ARMA 3 -> bounding box -> YOLO -> teste real
  manifest-drive.md                         IDs e links do Drive (dataset 2022, ortomosaicos)
  amostra/412.PNG                           captura do editor Eden feita em 2022
  scripts/myScriptArmas3-original-2022.sqf  script original (3 linhas)
  scripts/capturaDataset.sqf                script novo: randomiza cena, câmera, clima; loga bboxes 2D
  scripts/rpt_to_yolo.py                    converte o log do ARMA (.rpt) + screenshots em dataset YOLO
  scripts/preview_boxes.py                  desenha as caixas para validar o alinhamento
  scripts/train_yolo.py                     treina e avalia com Ultralytics
  scripts/requirements.txt
04-bibliografia/
  papers-fabio-2022/                        18 PDFs + índice
  2026-09-09 - Computer Vision e Drones em Seguranca Publica - Bibliografia.md (+ PDF)
```

## 6. Pessoas e créditos

| Pessoa | Papel |
|---|---|
| Felipe / Luciano Martins Figueira | Autor, mestrando FGV EBAPE, eng. de software, cientista de dados, cofundador da Argos Estúdio |
| Prof. Hélio Arthur Reis Irigaray | Orientador no mestrado, autor do rascunho v1 e v2 do artigo |
| Prof. Claudio Miceli de Farias | Orientador do projeto de 2022 (NCE-UFRJ) |
| Fábio H. P. Guimarães | Perito PCERJ, autor da proposta de 2022 e da ideia de usar ARMA 3 |

Ao citar o pipeline ARMA 3, creditar Fábio pela proposta e Miceli pela orientação.

## 7. Cuidados

- Os ortomosaicos do Jacarezinho e Manguinhos (Drive, pasta Ortomosaico, ~390 MB em dois zips) são dados operacionais da PCERJ. Não incluí no pacote. Não redistribuir nem publicar recortes. Se forem usados como teste real, só internamente e sem coordenadas.
- O artigo assume três restrições éticas: nenhuma imagem identificando moradores, nenhuma coordenada em nível de endereço, coleta futura só com ética independente. O experimento sintético respeita isso por construção.
- Preferência de escrita do Felipe: nada de travessão em textos entregues; usar vírgula, dois-pontos ou parênteses.

## 8. Requisitos da outra máquina

- Windows 10/11 (ARMA 3 não roda nativamente em macOS; no Linux roda via Proton mas o `screenshot` e o RPT ficam em caminhos diferentes).
- ARMA 3 na Steam (base já basta; Apex/Tanoa ajuda pelas construções tipo "slum").
- GPU NVIDIA com 6 GB ou mais para treinar YOLO localmente; sem GPU, treinar no Colab ou Kaggle.
- Python 3.10 ou superior.
