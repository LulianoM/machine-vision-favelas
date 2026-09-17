---
title: Projeto Drone PCERJ, UFRJ 2022 (Miceli + Fábio Guimarães)
tags:
  - domain/pesquisa-academica
  - type/project-record
  - status/encerrado
  - topic/visao-computacional
  - topic/drones
  - topic/seguranca-publica
source: Gmail (thread "Dúvida Oficina Trab Pesquisa I BCMT"), Google Drive (pasta PROJETO DRONE), Google Calendar (evento "Projeto Drone")
created: 2026-09-10
periodo: 2022-03 a 2022-08
related:
  - "[[Bibliografia - Projeto Drone PCERJ]]"
  - "[[Socios]]"
  - "[[Sobre a Argos]]"
---

# Projeto Drone PCERJ, UFRJ 2022

> Caso citado no deck de apresentação do Luciano como "Polícia Civil RJ: treinamento de drones com visão computacional para reconhecimento de pessoas armadas".

## Resumo

Projeto de pesquisa e extensão do BCMT-UFRJ (Bacharelado em Ciências Matemáticas e da Terra), realizado entre março e agosto de 2022 para cumprir as disciplinas CMT003 (Oficina de Trabalho de Pesquisa I) e CMT006 (Oficina de Trabalho de Extensão I). Orientado pelo professor Claudio Miceli, em parceria com o mestrando Fábio Guimarães, perito da Polícia Civil do RJ.

## Pessoas

| Pessoa | Papel | Contato |
|---|---|---|
| Prof. Claudio Miceli de Farias | Orientador, NCE-UFRJ (PPGI) | cmicelifarias@gmail.com, claudiofarias@nce.ufrj.br |
| Fábio H. P. Guimarães | Mestrando UFRJ, Perito Criminal de Informática na PCERJ desde 2010, projeto de aeronaves não tripuladas na CORE. Tecnólogo em Processamento de Dados (Simonsen, 2004), pós em Perícia Criminal (Castelo Branco, 2014), professor da FAETEC desde 2011 | fabiocsirj@gmail.com |
| Luciano Martins Figueira | Aluno BCMT, engenheiro de software (na época na isaac) | martinslucianofigueira@gmail.com |
| Solange | Secretaria do BCMT | solange@ccmn.ufrj.br |
| Alexandre Vasconcelos | Colaborador, subiu ortomosaico de Manguinhos | alexanvasconcelos@gmail.com |

Nome completo do Fábio não aparece em nenhum documento (só "H. P."). Conferir no Lattes ou no repositório do PPGI-UFRJ se precisar citar.

## Como começou

- 14/03/2022: Luciano escreve ao Miceli propondo um Data Warehouse de dados de segurança pública (ISP, OTT, Fogo Cruzado).
- 16/03/2022: Miceli responde que há "muita sinergia com o trabalho do Fábio" e junta os três.
- 22/03/2022: primeira reunião. Cronograma e pasta no Drive criados em 24/03.
- 24/04/2022: pedido ao Miceli para abrir vaga em CMT006 (Oficina Trab Extensão I).

## Tema da pesquisa

**Título da proposta (19/04/2022, autoria do Fábio):**
"Fusão de Dados em imagens RGB-T obtidas por UAV para aumento da eficácia na detecção de ameaças usando CNN treinada com dados sintéticos"

**Ideia central:**
1. Drone com câmera RGB e térmica (RGB-T), fusão dos dois sensores.
2. Detecção de ameaças (pessoas armadas) por CNN com bounding box, no contexto de segurança pública.
3. Problema atacado: escassez de datasets aéreos anotados no domínio UAV.
4. Solução: gerar imagens sintéticas no videogame ARMA 3, com anotação automática de bounding box via script (comando boundingBoxReal da engine).

**Base anterior do Fábio:** artigo do ITA (SC-249 Simulação de Drones e Aplicações, jul/2021) "Detecção de Objetos em Tempo Real com Piloto Humano com Instabilidade", com YOLOv4 e filtro de Kalman treinados em simulação Matlab/Simulink (2.751 imagens sintéticas, 13,5 FPS no Colab com Tesla T4).

## Cronograma executado

| Data | Etapa | Entregável |
|---|---|---|
| 05/04/2022 | Revisão de papers (IEEE e ACM, 2018+) | Decks "Resumo Papers" (Fábio e Luciano) |
| 19/04/2022 | Proposta de solução | Deck "Reunião 19_04 Proposta" |
| 03/05/2022 | Protótipo (MVP) | Deck "Reunião 03_05 Protótipo": fusão RGB + térmico, código em Julia (VideoIO) |
| 17/05/2022 | Design de teste | Métricas de desempenho |
| 31/05/2022 | Documentação | Relatório |
| 05/2022 | Dataset sintético | Pasta DATASET com imagens do ARMA 3 e bounding boxes; script myScriptArmas3.txt |
| 08/2022 | Dados reais | Ortomosaicos do Jacarezinho (setores Sudoeste e Nordeste) e Manguinhos |

Reuniões quinzenais às terças, 14h (depois 16h), pelo Meet (qkt-bist-ofb).

## Onde está o material

- **Drive, pasta "PROJETO DRONE"** (id 1uljOHH2AyMCFj9Q1sTA5XYA70kvNqU0-): CronogramaDoProjeto, três decks de reunião, subpastas CÓDIGOS, DATASET, BIBLIOGRAFIA E PAPERS SELECIONADOS, Ortomosaico.
- **Gmail:** thread "Dúvida Oficina Trab Pesquisa I BCMT" (mar a abr/2022). Só agendamento, sem conteúdo técnico.
- **Papers:** [[Bibliografia - Projeto Drone PCERJ]], PDFs na subpasta `Papers/` desta nota e em `~/Desktop/PROJETO DRONE PCERJ/papers-fabio/`.

## Cuidados

- Os ortomosaicos do Jacarezinho e Manguinhos são dados operacionais da PCERJ. Não compartilhar nem citar sem autorização.
- Ao citar o projeto, creditar o Fábio pela proposta e o Miceli pela orientação.

## Possíveis reaproveitamentos

- Case de visão computacional e IA aplicada para o portfólio tech da Argos (ver [[2026-08-09 - Pivot Tech Software House - Validacao e Roadmap]]).
- Experiência prévia com pesquisa aplicada e dados sintéticos para o mestrado e submissões acadêmicas.
