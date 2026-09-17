# Contexto acumulado do projeto

Conhecimento que estava só na memória do Claude do Mac e que o desktop também precisa. Atualizar aqui quando surgir algo que valha para as duas máquinas.

## Linha do tempo

| Quando | O que |
|---|---|
| mar a ago/2022 | Projeto de pesquisa e extensão BCMT-UFRJ com prof. Claudio Miceli (NCE-UFRJ) e Fábio H. P. Guimarães (perito PCERJ): detecção de pessoas armadas em imagens RGB-T de drone, CNN treinada com dados sintéticos do ARMA 3. Ver `02-projeto-ufrj-2022/`. |
| 2026-09-09 | Levantamento de 15 artigos sobre CV, drones e segurança pública. Ver `04-bibliografia/`. Orientador escreve a v1 do artigo (3.205 palavras). |
| 2026-09-10 | v2 do orientador: 6.304 palavras pela contagem do script de divisão (5.644 sem a lista de referências). É a versão vigente. |
| 2026-09-11 | Pacote `.rar` levado ao desktop com briefing, scripts do pipeline e prompt inicial (cópias em `docs/`). |
| 2026-09-12 | Levantamento técnico sobre como recriar a favela em 3D. Ver `05-levantamento-3d/`. |
| 2026-09-17 | O orientador não enviou versão nova: o arquivo baixado nesse dia é idêntico byte a byte à v2 de 10/09. Pasta reorganizada no Mac, artigo dividido por seção, estrutura de repositório único preparada. |

## O experimento e o que ele prova

O pipeline de `03-arma3/` valida o método da seção de resultados do artigo: cena sintética em motor de jogo, anotação automática de bounding box, domain randomization, treino de detector, teste em imagem aérea real (VisDrone). Números que vão para o artigo: mAP zero-shot, mAP com 5 a 10% de dado real, e sintético mais real. As classes atuais são pessoas vistas de cima (reproduz 2022). Classes do artigo (altura de edificação, adição em laje, transição de material) exigem um segundo experimento com cenas de edificações empilhadas; o pipeline é o mesmo.

## Achados do levantamento 3D que decidem o desenho

- O que decide o sim-to-real é a ORIGEM DA GEOMETRIA, não textura nem engine. Liao et al. 2026 (Remote Sensing 18(2):361, DOI 10.3390/rs18020361, dataset UAV-SynthScene, Colosseum + UE 5.1 + UltraDynamicSky, 4.659 imagens, uma RTX 4090) é o template do método. Duas ablações: tirar a variação de sol, clima e ângulo custa cerca de 10 pontos de mAP50 (cerca de 20 em objetos truncados); trocar a base fotogramétrica por assets genéricos custa 22,5 pontos.
- Consequência: comprar kit de favela é o braço perdedor. Assets servem para props sobre base real, nunca como base.
- O Instituto Pereira Passos serve publicamente uma ortofoto verdadeira do Rio de 2024, pixel de 15 cm, de um voo que incluiu LiDAR: `pgeo3.rio.rj.gov.br/arcgis/rest/services/Imagens/Mosaico_2024/ImageServer`, EPSG:31983, cobre o Jacarezinho. É dado municipal aberto, não sensível. A nuvem LiDAR não está publicada: pedir em cartografia.ipp@prefeitura.rio (disponibilidade, custo e termos não verificados).
- Google Photorealistic 3D Tiles é proibido contratualmente para detecção de objetos. Não usar como fonte de geometria nem como cena de captura.
- Prior art obrigatório: G-MAD (Kim et al., ACM MM 2026, arXiv 2607.19942), que usa ARMA 3 para dados aéreos RGB-T com bbox automático do engine. Também Berwaldt, Bettker e Pozzer, "Procedural Generation of Favela Layouts on Arbitrary Terrains", SBGames 2020, DOI 10.1109/SBGames51465.2020.00027.
- Expectativa calibrada: sintético puro em cena urbana densa pode colapsar (Kiefer, Ott e Zell, ICPR 2022: 1,2 a 2,4 mAP no VisDrone). Altitude é eixo de domain shift severo (SynDrone, ICCVW 2023). Com pré-treino sintético bom, 5 a 20% do dado real recupera 85 a 95% do desempenho. Não prometer substituição total.
- Convenção de anotação: definir e documentar modal (só a parte visível) versus amodal (objeto inteiro, como no VisDrone) antes de gerar o primeiro lote.
- Problema técnico a planejar se a fotogrametria de 2022 for usada: remover a iluminação assada da textura (delighting).

## Restrições de máquina

- O MacBook Air M1 de 8 GB está abaixo do mínimo para Unreal Engine 5 e não roda ARMA 3. Todo render e treino acontece no desktop.
- BlenderProc não usa GPU no macOS. Unity Perception foi descontinuado.

## Pessoas

| Pessoa | Papel |
|---|---|
| Luciano Martins Figueira (Felipe) | Autor, mestrando MEX FGV EBAPE 2026.2, engenheiro de software |
| Prof. Hélio Arthur Reis Irigaray | Orientador, autor dos rascunhos v1 e v2 |
| Prof. Claudio Miceli de Farias | Orientador do projeto de 2022 (NCE-UFRJ) |
| Fábio H. P. Guimarães | Perito PCERJ, autor da proposta de 2022 e da ideia de usar ARMA 3 |

## Onde estão os binários que não entram no git

- Pacote completo de 11/09 com os 18 PDFs: no Mac em `~/Documents/Mestrado/Projetos/PROJETO-MACHINE-VISION-FAVELAS-2026-09-11.rar`; no desktop, na pasta descompactada original.
- Dataset de 2022, ortomosaicos e decks: Google Drive, pasta "PROJETO DRONE". IDs em `03-arma3/manifest-drive.md`.
