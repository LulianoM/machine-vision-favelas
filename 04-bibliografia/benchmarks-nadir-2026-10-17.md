# Benchmarks reais de pessoas vistas de cima: levantamento de 17/10/2026

Pedido do revisor: "Reassess whether the real-world benchmark adequately supports the evaluation of transfer across viewing geometries and, if possible, incorporate data with a more comparable perspective." Agente D4 da rodada de revisão. Levantamento só na web, sem baixar nenhum dataset. O que foi baixado para leitura: artigos em acesso aberto (arXiv, CVF, IEEE Access), READMEs do GitHub, registros da API do Zenodo, da DataCite e do Crossref, uma imagem de amostra do repositório do Unicamp-UAV e duas figuras do repositório do VTSaR, para decidir o ângulo da câmera. Nada do manuscrito foi alterado e nada foi commitado.

## 1. O que o artigo usa hoje e o que falta

- Aquisição de referência: nadir, 150 m, 3840 x 2160, 4,88 cm/px (seção 7.3 e tabela de GSD da 6b). Corpora de 75 m (2,44 cm/px) e 35 m (1,1 cm/px).
- Benchmark real usado: VisDrone-DET, split val. Resultado zero-shot dos modelos nadir: mAP50 0,0102 (uma favela) e 0,0190 (seis favelas); com câmera oblíqua de 45 a 56 graus: 0,0614 e 0,1055 (`07b-results-placeholder.md`). O próprio manuscrito estima o pitch do VisDrone pela razão altura/largura das caixas (mediana 1,95 no treino, contra 0,98 no corpus nadir).
- O que o levantamento acrescenta sobre o VisDrone (seção 5 abaixo): altitude estimada de 30 a 100 m (Nguyen et al., 2026, tabela 1) e, no split de treino, só cerca de 16% dos objetos estão em imagens de visada vertical ("bird view", 70 a 90 graus), contra 84% em imagens de ângulo agudo (Kiefer, Messmer e Zell, 2021, fig. 2, com faixas estimadas por inspeção visual). Ou seja, a avaliação zero-shot atual mede troca de geometria de visada tanto quanto troca de cena.

## 2. Método e limites

- Busca web (WebSearch, modo extended para altitude, pitch e licença), leitura das páginas oficiais e dos artigos originais. Todos os DOIs conferidos em `api.crossref.org/works/<doi>` (os de Zenodo e IEEE DataPort, em `api.datacite.org`). Nenhum e-mail do autor foi enviado em cabeçalho.
- Onde a fonte não dá GSD, calculei uma estimativa com a fórmula GSD = 2 H tan(HFOV/2) / largura em pixels, a partir da altitude declarada e do campo de visão nominal da câmera. Toda estimativa minha está marcada como "estimativa minha".
- Páginas que não responderam em 17/10: a página do HERIDAL na FESB (conexão recusada na porta 443 e sem resposta na 80), Springer e Nature (redirecionam para login), spj.science.org e ScienceDirect (403), a página do Semantic Drone Dataset (certificado expirado), o repositório GitHub do AU-AIR (404) e a página do UAV123 na KAUST (404). Nesses casos os dados vêm do artigo original em outra fonte ou de fonte secundária, indicada.
- O que não repeti: a busca de 30/09 sobre arma portada em benchmark público (`busca-2026-09-30-pontos-abertos.md`, seção 1). Novidade desde então: nenhuma. Nenhum dos conjuntos abaixo anota arma de fogo; o único conjunto aéreo novo de 2026 encontrado com caixas de pessoa (KIOS, Zenodo) não tem classe de arma.

## 3. Critério da nota de comparabilidade (1 a 5)

Referência: nadir, 150 m, 4,88 cm/px, pessoas em pé no chão, caixa por pessoa.

- 5: nadir, GSD entre 4 e 6 cm/px, pessoas no chão, caixas. Nenhum conjunto público chega a 5.
- 4: nadir com caixas de pessoa no chão e GSD a menos de um fator 2 da referência (ajustável por reamostragem).
- 3: nadir mas com GSD mais de 2x diferente, ou pessoa em contexto atípico (na água), ou anotação por ponto, ou pitch não declarado em altitude compatível.
- 2: oblíquo, ou altitude muito baixa (abaixo de 30 m), ou modalidade térmica.
- 1: outra tarefa ou outra perspectiva (rastreamento a 5 m, vídeo de internet).
- 0: sem classe de pessoa.

## 4. Quadro-resumo (ordenado por nota)

| # | Dataset | Year | Pitch | Altitude or GSD | Resolution | Images / person boxes | Licence, access | Size | Score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HERIDAL | 2019 | nadir | 40 a 65 m; 1,5 a 2,4 cm/px (estimativa minha) | 4000 x 3000 | 1.647 / 3.229 | não declarada; página da FESB (fora do ar em 17/10) | não declarado | 4 |
| 2 | SeaDronesSee (OD v2) | 2022 | 0 a 90 graus, com metadado por quadro | 5 a 260 m; a 150 m, 3,5 a 4,5 cm/px (estimativa minha) | 3840 x 2160 a 5456 x 3632 | 14.227 (v2) / v1: 5.630 imagens | registro no site; licença não declarada | não declarado | 3 |
| 3 | Stanford Drone Dataset | 2016 | nadir | cerca de 80 m; GSD grosseira (estimativa minha: 7 a 15 cm/px) | 1400 x 1904 (processado) | 60 vídeos, 8 cenas / cerca de 20.000 alvos | CC BY-NC-SA 3.0, download direto | 69 GB | 3 |
| 4 | MOBDrone | 2022 | nadir (90), poucas tomadas a 45 | 10 a 60 m; a 60 m, 4,7 cm/px (estimativa minha) | 1920 x 1080 | 126.170 / 113.408 | CC BY 4.0, Zenodo | 5,5 GB (vídeos) ou 243 GB (quadros) | 3 |
| 5 | DLR-ACD | 2019 | nadir e lateral (câmera tripla) | 500 a 1.600 m; 4,5 a 15 cm/px | média 3619 x 5226 | 33 / 226.291 pontos | GNU GPL, página do DLR | não declarado | 3 |
| 6 | WiSARD | 2022 | variado, não declarado | 20 a 120 m | 3840 x 2160 (RGB) | 33.786 RGB / total de caixas não declarado | não declarada; site da UW | não declarado | 3 |
| 7 | Aerial Dataset for Car and Person Detection (KIOS) | 2026 | não declarado | 40 e 60 m | não declarada | 13.755 / 221.186 | CC BY 4.0, Zenodo | 11,6 GB | 3 |
| 8 | NOMAD | 2024 | variável (câmera apontada ao ator) | 10, 30, 50, 70 e 90 m | 5472 x 3078 | 42.825 / 42.825 (um ator por quadro) | não declarada para os dados; Google Drive | não declarado | 3 |
| 9 | Okutama-Action | 2017 | 45 ou 90 graus | 10 a 45 m | 4K (vídeo); 1280 x 720 (quadros) | 77.365 / 524.649 | CC BY-NC-SA 3.0, download direto | 5,3 + 1,5 GB (720p); 14 + 4 GB (4K) | 3 |
| 10 | VTSaR (A-VTSaR) | 2025 | misto, com amostras verticais | "maior altitude", valor não verificado | 1920 x 1080 (RGB), 640 x 512 (IR) | 12.465 / 19.956 | não declarada; só Baidu Pan | não declarado | 3 |
| 11 | HIT-UAV (térmico) | 2023 | 30 a 90 graus, com metadado | 60 a 130 m; a 100 m, 6,9 cm/px (estimativa minha) | 640 x 512 | 2.898 / 12.312 | CC BY 4.0, GitHub | pequeno (não declarado) | 2 |
| 12 | VisDrone-DET (baseline) | 2018/2022 | majoritariamente oblíquo (84% dos objetos) | 30 a 100 m (fonte secundária) | até 2000 x 1500 | 10.209 / não recontado | uso em pesquisa, não reconferido | não conferido | 2 |
| 13 | AU-AIR | 2020 | 45 a 90 graus | 5 a 30 m (maioria a 10, 20 e 30) | 1920 x 1080 | 32.823 / 5.158 | CC BY (fonte secundária); GitHub 404 | não declarado | 2 |
| 14 | Manipal-UAV | 2023 | 45 a 90 graus (fonte secundária) | 10 a 50 m | 1280 x 720 | 13.462 / 153.112 | GPL-3.0 mais restrição acadêmica; pedido por formulário | não declarado | 2 |
| 15 | SARD | 2021 | 45 a 90 graus | 5 a 50 m | 1920 x 1080 | 1.981 / 6.532 | CC BY 4.0 (DataCite); IEEE DataPort com login | 4,43 GB | 2 |
| 16 | Archangel-Real | 2023 | 45 graus fixo (oblíquo) | 15 a 50 m, raio 15 a 50 m | 1304 x 978 | não declarado | site do ARL com login | não declarado | 2 |
| 17 | AFO | 2021 | "bird's-eye view" | não declarada | 1280 x 720 a 3840 x 2160 | 3.647 / 33.174 humanos | CC BY-NC-SA 3.0, Kaggle | 4,36 GB | 2 |
| 18 | Semantic Drone Dataset | 2017 | nadir | 5 a 30 m; estimativa minha: 0,2 a 1,2 cm/px | 6000 x 4000 | 400 públicas / caixas de pessoa, número não declarado | não comercial; pedido por formulário | não declarado | 2 |
| 19 | DroneCrowd | 2021 | não declarado | não declarada | 1920 x 1080 | 33.600 / 4,8 milhões de pontos (cabeças) | não declarada; GitHub | não declarado | 2 |
| 20 | AerialMPT | 2020 | nadir e lateral | 600 a 1.400 m; 8 a 13 cm/px | recortes de 425 x 358 em média | 307 / 44.740 pontos | GNU GPL, DLR | 75 MB | 2 |
| 21 | Unicamp-UAV (Brasil) | 2026 | oblíquo (horizonte no quadro) | cerca de 30 m | 3840 x 2160 | 6.500 / 58.555 | só pesquisa acadêmica; Google Drive | não declarado | 2 |
| 22 | LaDD (Lacmus) | 2023 | não declarado | 40 a 100 m (fontes divergem) | 4000 x 3000 (fonte secundária) | 1.365 / 4.733 | GPL (fonte secundária); links mortos | não declarado | 2 |
| 23 | BIRDSAI (térmico) | 2020 | não conferido | 60 a 120 m (fonte secundária) | não conferida | 162K / 84K | não conferida | não conferido | 1 |
| 24 | TinyPerson | 2020 | oblíquo, vídeos de internet | não há | variada | 1.610 / 72.651 | sem licença; restrições de uso | não declarado | 1 |
| 25 | UAV123 | 2016 | oblíquo | 5 a 25 m | 720p (padronizado) | 123 sequências, 112.578 quadros / rastreamento de um alvo | não declarada | 13,7 GB | 1 |
| 26 | P-DESTRE | 2021 | 45 a 90 graus | 5,5 a 6,7 m | 3840 x 2160 | 75 vídeos / 269 identidades | livre (sem licença formal) | não declarado | 1 |
| 27 | MAVREC | 2024 | não conferido | 25 a 45 m (fonte secundária) | não conferida | 14K / 60K | não conferida | não conferido | 1 |
| 28 | UAVDT | 2018 | oblíquo | 10 a mais de 70 m | 1080 x 540 | 80K / só veículos | pesquisa | não conferido | 0 |

Notas rápidas ao quadro: "fonte secundária" é a tabela 1 de Nguyen et al. (2026) ou a tabela 1 do ForestPersons (arXiv 2603.02541), ambas lidas hoje; os números de pessoas do VisDrone, do UAVDT e do MAVREC não foram recontados.

## 5. Fichas por dataset

Ordem do quadro. Em cada ficha: autores e veículo com estado do DOI; endereço dos dados; licença e acesso; plataforma e câmera; altitude ou GSD; pitch; resolução; imagens e instâncias; objetos portados; tamanho; nota com justificativa.

### 5.1 HERIDAL (2019). Nota 4

- Autores e veículo: Božić-Štulić, Marušić e Gotovac, International Journal of Computer Vision, 127(9), 1256-1278. DOI 10.1007/s11263-019-01177-1, conferido no Crossref.
- Dados: `ipsar.fesb.unist.hr/HERIDAL database.html` (FESB, Split). Página sem resposta em 17/10; confirmar antes de planejar. Há espelhos de usuário no Kaggle, sem garantia de licença.
- Licença e acesso: não declarada nas fontes lidas (o artigo da IJCV está atrás de login).
- Plataforma e câmera: vários drones e câmeras; Canon PowerShot S110 citada em fonte secundária.
- Altitude e GSD: 40 a 65 m. Pyrro, Naseri e Jung (2021, arXiv 2111.09406) resumem os requisitos embutidos no HERIDAL como "straight-down (nadir) image viewpoint" e "drone flying altitude (from 40 to 65 m)". GSD estimada minha com grande angular de 24 mm equivalentes: 1,5 cm/px a 40 m e 2,4 cm/px a 65 m, ou seja, a faixa do corpus de 75 m do artigo (2,44 cm/px); reamostrar por 2 leva à referência de 150 m.
- Pitch: nadir (Pyrro et al., 2021; tabela 1 do ForestPersons: "top-down"). Uma fonte secundária fala em 45 a 60 graus; a fonte primária lida diz nadir.
- Resolução: 4000 x 3000 na maioria; algumas 4000 x 2250.
- Imagens e instâncias: 1.647 imagens e 3.229 pessoas anotadas (Pyrro et al., 2021; o ForestPersons dá 1.600 e 3.194; a tabela de Nguyen dá "68K", que parece ser outra contagem e não bate com as demais).
- Objetos portados: não anotados. Pessoas em pé, sentadas ou deitadas em mato mediterrâneo (Croácia e Bósnia), muitas vezes em grupo.
- Tamanho: não declarado (1.647 JPEGs de 12 MP: alguns GB).
- Justificativa: único conjunto público com caixas de pessoa no chão, visada nadir declarada e GSD a menos de um fator 2 da referência; a cena é mato, não cidade.

### 5.2 SeaDronesSee, Object Detection v2 (2022). Nota 3

- Autores e veículo: Varga, Kiefer, Messmer e Zell, WACV 2022, pp. 3686-3696. DOI 10.1109/WACV51458.2022.00374, conferido no Crossref.
- Dados: `seadronessee.cs.uni-tuebingen.de/dataset`.
- Licença e acesso: registro no site (FAQ: "You need to register first"); licença não declarada na página nem no artigo; fontes secundárias (ResearchGate, Roboflow) dizem CC BY 4.0, não confirmado. Anotações do teste retidas (servidor de avaliação); para zero-shot servem treino e validação, já que não se treina neles.
- Plataforma e câmera: DJI Matrice 100 e 210, Mavic 2 Pro e Quantum Systems Trinity F90+; câmeras L1D-20c (5456 x 3632), UMC-R10C, Zenmuse X5 (3840 x 2160) e XT2.
- Altitude e GSD: 5 a 260 m. Cerca de 50% das imagens abaixo de 50 m; "there are many images facing downwards (90), because images taken at greater altitudes tend to face down" (artigo, seção 3). Estimativa minha a 150 m em nadir: 3,5 cm/px (L1D-20c) a 4,5 cm/px (X5), a faixa mais próxima dos 4,88 cm/px de todo o levantamento.
- Pitch: 0 a 90 graus, com pitch do gimbal, altitude, GPS e velocidade por quadro (metadado a 10 Hz). Na v2 (14.227 imagens), 2.830 imagens sem metadado e 686 só com pitch (relatório MaCVi 2023, arXiv 2211.13508). É isso que permite filtrar um subconjunto nadir entre 100 e 260 m.
- Resolução: 3840 x 2160 a 5456 x 3632.
- Imagens e instâncias: v1 5.630 imagens (2.975 treino, 859 val, 1.796 teste); v2 14.227 imagens; cerca de 60K caixas (tabela de Nguyen). Classes: swimmer, floater (com colete), life jacket, swimmer e floater em barco, boat.
- Objetos portados: colete salva-vidas como classe própria; nada alongado na mão.
- Tamanho: não declarado (imagens de 20 MP: dezenas de GB).
- Justificativa: a única fonte pública com caixas de pessoa, nadir e altitude declarada por quadro acima de 100 m; a pessoa está na água, de modo que a forma do alvo difere da de um pedestre.

### 5.3 Stanford Drone Dataset (2016). Nota 3

- Autores e veículo: Robicquet, Sadeghian, Alahi e Savarese, ECCV 2016, LNCS, pp. 549-565. DOI 10.1007/978-3-319-46484-8_33, conferido no Crossref.
- Dados: `cvgl.stanford.edu/projects/uav_data/` (um zip de 69 GB).
- Licença e acesso: CC BY-NC-SA 3.0, download direto.
- Plataforma e câmera: "a 4k camera mounted on a quadcopter platform (a 3DR solo) hovering above various intersections on a University campus at an altitude of approximately eighty meters" (artigo, seção 3).
- Altitude e GSD: cerca de 80 m. GSD não declarada; estimativa minha: grosseira, entre 7 e 15 cm/px, porque o vídeo 4K de grande angular foi reamostrado para 1400 x 1904; pessoa com cerca de 10 a 25 px de altura, o regime do corpus piloto do artigo (9,76 cm/px), não o do corpus de registro.
- Pitch: nadir ("top-view scenes").
- Resolução: 1400 x 1904, vídeo retificado e estabilizado.
- Imagens e instâncias: 8 cenas, 60 vídeos; cerca de 20.000 alvos (artigo), 6 classes (pedestre, ciclista, skatista, carrinho, carro, ônibus); pedestres são a maioria na maior parte das cenas. Caixa por quadro com marcas lost, occluded e generated (interpolada).
- Objetos portados: não; bicicleta e skate são classes próprias.
- Tamanho: 69 GB.
- Justificativa: único conjunto nadir acima de 50 m com pedestres em cena urbana (campus) e caixas, mas em resolução grosseira e com caixas interpoladas.

### 5.4 MOBDrone (2022). Nota 3

- Autores e veículo: Cafarelli, Ciampi, Vadicamo, Gennaro, Berton, Paterni, Benvenuti, Passera e Falchi, ICIAP 2022, LNCS, pp. 633-644. DOI 10.1007/978-3-031-06430-2_53, conferido no Crossref. Dados: DOI 10.5281/zenodo.5996890, conferido na DataCite.
- Dados: `zenodo.org/records/5996890`.
- Licença e acesso: CC BY 4.0, acesso aberto, sem registro.
- Plataforma e câmera: DJI Phantom 4 Pro V2, câmera FC6310.
- Altitude e GSD: 10 a 60 m acima do nível do mar; clipes por altitude: 10 m (1), 20 m (6), 30 m (15), 40 m (13), 50 m (16), 60 m (15). Estimativa minha em nadir, 1080p: 2,3 cm/px a 30 m, 3,9 a 50 m e 4,7 a 60 m.
- Pitch: "mostly 90 degrees (perpendicular to the water)"; um pequeno conjunto a 45 graus, sem contagem.
- Resolução: gravado em 4K, convertido para 1920 x 1080.
- Imagens e instâncias: 126.170 quadros; 181.689 caixas em 5 classes; 113.408 caixas de pessoa em 77.365 imagens. COCO JSON.
- Objetos portados: boia, prancha e madeira são classes próprias; pessoa na água, muitas vezes só parcialmente visível.
- Tamanho: 5,5 GB de vídeo (66 clipes) ou 243 GB de quadros.
- Justificativa: aberto, nadir e com GSD igual à referência nos clipes de 50 e 60 m, mas com pessoa flutuando no mar.

### 5.5 DLR-ACD (2019). Nota 3

- Autores e veículo: Bahmanyar, Vig e Reinartz, "MRCNet: Crowd counting and density map estimation in aerial and ground imagery", arXiv 1909.12743 (cópia em elib.dlr.de/128895). Sem DOI: a busca por título no Crossref não devolve o trabalho.
- Dados: `dlr.de/en/eoc/.../public-datasets/dlr-acd` (arquivo DLR_AerialCrowdDataset.zip).
- Licença e acesso: a página do DLR diz "Distributed under the GNU GPL license"; download direto.
- Plataforma e câmera: três DSLR (uma nadir e duas laterais) em helicóptero, campanhas de 2011 a 2017 em eventos de massa.
- Altitude e GSD: 500 a 1.600 m; GSD de 4,5 a 15 cm/px (tabela 1 do artigo: 7,0 a 14,0 nas 14 primeiras imagens).
- Pitch: nadir para a câmera central; as laterais são oblíquas, e a tabela não diz de qual câmera vem cada imagem.
- Resolução: média 3619 x 5226.
- Imagens e instâncias: 33 imagens; 226.291 pessoas marcadas por ponto (285 a 24.368 por imagem); 19 de treino e 14 de teste.
- Objetos portados: não.
- Tamanho: não declarado.
- Justificativa: GSD e visada nadir equivalentes às da referência, em cena urbana, mas anotação por ponto e multidão densa; serve a uma checagem de contagem ou de localização (ponto dentro da caixa), não a mAP.

### 5.6 WiSARD (2022). Nota 3

- Autores e veículo: Broyles, Hayner e Leung, IROS 2022, pp. 9467-9474. DOI 10.1109/IROS47612.2022.9981298, conferido no Crossref (já proposto na lista de 30/09).
- Dados: `sites.google.com/uw.edu/wisard`.
- Licença e acesso: não declarada.
- Plataforma e câmera: DJI Mavic 2 Enterprise Advanced (principal), Matrice 600 Pro com FLIR Duo Pro R, Inspire 1 com Zenmuse Z3, Mavic Mini, Phantom 4 Pro.
- Altitude e GSD: 20 a 120 m. Estimativa minha a 120 m em nadir, 4K: cerca de 4,6 cm/px.
- Pitch: "aspect angle" variado, não especificado.
- Resolução: 3840 x 2160 (maioria), 2720 x 1530 (Mini), 1920 x 1080 (parte); térmico 640 x 512.
- Imagens e instâncias: 33.786 RGB, 22.156 térmicas, 15.453 pares; total de caixas não declarado (a tabela do ForestPersons dá 44.588 imagens e 74.204 anotações). Formato YOLO, classe única.
- Objetos portados: não.
- Tamanho: não declarado.
- Justificativa: chega a 120 m com 4K, mas sem pitch por quadro e em mata, campo e neve.

### 5.7 Aerial Dataset for Car and Person Detection, KIOS (2026). Nota 3

- Autores e veículo: Vasileiadis, Savva e Kyrkou (KIOS, Universidade de Chipre), Zenodo, 06/07/2026. DOI 10.5281/zenodo.21216709, conferido na DataCite. Sem artigo associado.
- Dados: `zenodo.org/records/21216709`.
- Licença e acesso: CC BY 4.0, aberto.
- Plataforma e câmera: DJI Mavic 3M, lente RGB.
- Altitude e GSD: 40 e 60 m (trajetória por 5 waypoints) e 60 m parado (multidão). Estimativa minha se for nadir, em 4K: 1,6 cm/px a 40 m e 2,3 a 60 m.
- Pitch: não declarado. Confirmar com os autores antes de usar.
- Resolução: não declarada.
- Imagens e instâncias: 13.755 quadros de 11 vídeos; 221.186 caixas de pessoa e 1.074.474 de carro; PASCAL e YOLO.
- Objetos portados: não.
- Tamanho: 11,6 GB.
- Justificativa: aberto, recente e com muitas caixas em estacionamento, mas sem pitch declarado e com altitude abaixo da referência.

### 5.8 NOMAD (2024). Nota 3

- Autores e veículo: Russell Bernal, Scheirer e Cleland-Huang, WACV 2024, pp. 8569-8580 (Crossref; a página do arXiv diz 8584-8595). DOI 10.1109/WACV57701.2024.00839, conferido no Crossref.
- Dados: `github.com/ArtRuss/NOMAD` (Google Drive).
- Licença e acesso: licença dos dados não declarada (o CC BY 4.0 da página do arXiv é do artigo).
- Plataforma e câmera: sUAS não nomeado; vídeo 5.4K.
- Altitude e GSD: cinco distâncias, 10, 30, 50, 70 e 90 m de altitude; o suplemento (tabela S3) traz a GSD mínima por distância. Estimativa minha a 90 m, 5472 px: cerca de 2,4 cm/px.
- Pitch: não fixo; a câmera era apontada ao ator e deslocada para evitar não participantes ("creating a non-fixed pitch").
- Resolução: 5472 x 3078.
- Imagens e instâncias: 42.825 quadros, cada um com uma caixa e um rótulo de visibilidade em 10 níveis; 100 atores andando, deitados e escondidos.
- Objetos portados: não.
- Tamanho: não declarado (quadros de 17 MP: provavelmente centenas de GB).
- Justificativa: altitudes até 90 m com alta resolução, mas um ator por quadro, pitch variável e cena rural.

### 5.9 Okutama-Action (2017). Nota 3 para os modelos de 35 e 75 m, 2 para o de 150 m

- Autores e veículo: Barekatain, Marti, Shih, Murray, Nakayama, Matsuo e Prendinger, CVPR Workshops 2017, pp. 2153-2160. DOI 10.1109/CVPRW.2017.267, conferido no Crossref (já proposto na lista de 30/09).
- Dados: `okutama-action.org`.
- Licença e acesso: CC BY-NC-SA 3.0, download direto.
- Plataforma e câmera: dois DJI Phantom 4, campo de beisebol em Okutama, Japão.
- Altitude e GSD: 10 a 45 m. Estimativa minha a 45 m em 4K: cerca de 1,8 cm/px.
- Pitch: 45 ou 90 graus; o metadado por sequência (ângulo, velocidade, altitude) continua anunciado como "soon" no site.
- Resolução: vídeo 3840 x 2160; os conjuntos de treino e teste distribuídos como quadros 1280 x 720; vídeos 4K em pacotes separados.
- Imagens e instâncias: 43 sequências, 77.365 quadros, 524.649 caixas (tabela do ForestPersons).
- Objetos portados: sim, como rótulo de ação: entre as 12 ações estão Carrying, Pushing/Pulling, Reading e Drinking (artigo, seção 3).
- Tamanho: 5,3 GB (treino 720p) + 1,5 GB (teste 720p); 14 GB + 4 GB em 4K.
- Justificativa: o subconjunto a 90 graus é nadir com caixas e objetos na mão, mas abaixo de 45 m e numa única cena.

### 5.10 VTSaR, A-VTSaR (2025). Nota 3, geometria não verificada

- Autores e veículo: Zhang, Feng, Wang, Lu e Mei, "Aerial person detection for search and rescue: Survey and benchmarks", Journal of Remote Sensing, 5, 0474 (2025). DOI 10.34133/remotesensing.0474, conferido no Crossref. Artigo irmão: Zhang et al., IEEE JSTARS, 18, 5082-5099 (2025), DOI 10.1109/JSTARS.2025.3526995, conferido.
- Dados: `github.com/zxq309/VTSaR`, com link só no Baidu Pan (barreira prática a partir do Brasil).
- Licença e acesso: não declarada.
- Plataforma e câmera: pod óptico duplo em gimbal (visível 1080p com campo de 62 a 6,56 graus, zoom; infravermelho 640 x 512), aparentemente em plataforma tipo helicóptero (figura do README).
- Altitude e GSD: "higher capture altitudes"; o valor numérico (50 a 300 m num trecho de busca) não pôde ser verificado, porque o texto integral deu 403.
- Pitch: misto; as figuras do README mostram vista geral oblíqua e recortes verticais.
- Resolução: 1920 x 1080 e 640 x 512.
- Imagens e instâncias: 12.465 imagens, 19.956 instâncias reais; mais 54.749 sintéticas no AS-VTSaR.
- Objetos portados: não declarado.
- Tamanho: não declarado.
- Justificativa: promissor na geometria e pareado RGB-térmico, mas com altitude não verificada e acesso impraticável.

### 5.11 HIT-UAV (2023, térmico). Nota 2

- Autores e veículo: Suo, Wang, Zhang, Chen, Zhou e Shi, Scientific Data, 10, artigo 227. DOI 10.1038/s41597-023-02066-6, conferido no Crossref.
- Dados: `github.com/suojiashun/HIT-UAV-Infrared-Thermal-Dataset`.
- Licença e acesso: CC BY 4.0 (GitHub), download direto.
- Plataforma e câmera: DJI Matrice 210 V2 com Zenmuse XT2 (FLIR 640 x 512, lente de 25 mm).
- Altitude e GSD: 60 a 130 m, com altitude, ângulo, data e luz por imagem. Estimativa minha a 100 m: 6,9 cm/px.
- Pitch: 30 a 90 graus.
- Resolução: 640 x 512.
- Imagens e instâncias: 2.898 imagens; 12.312 pessoas, 7.311 carros, 4.980 bicicletas; caixas padrão e orientadas, XML e JSON.
- Objetos portados: não.
- Tamanho: pequeno, não declarado.
- Justificativa: é o único conjunto com altitude e ângulo por imagem na faixa de 60 a 130 m, mas térmico; serviria só como controle de geometria com troca de modalidade.

### 5.12 VisDrone-DET, o baseline (2018, artigo de 2022). Nota 2 como benchmark nadir

- Autores e veículo: Zhu, Wen, Du, Bian, Fan, Hu e Ling, IEEE TPAMI, 44(11), 7380-7399. DOI 10.1109/TPAMI.2021.3119563, conferido no Crossref (já proposto na lista de 30/09).
- Altitude: 30 a 100 m (Nguyen et al., 2026, tabela 1; o artigo do VisDrone não dá distribuição). Wu et al. (2019, ICCV) anotaram o VisDrone2018 com altitude (low, medium, high), vista (front, side, bird) e luz (daylight, night). Kiefer, Messmer e Zell (2021) estimaram por inspeção visual as faixas dessas etiquetas: low 0 a 30 m, medium 30 a 80 m, high 80 a 100 m; bird view 70 a 90 graus, acute 0 a 70 graus; e mostram (fig. 2) que no split de treino 84% dos objetos estão em imagens acute e 16% em bird view.
- Resolução: até 2000 x 1500. Imagens: 10.209 estáticas (288 clipes com 261.908 quadros no VID/MOT).
- Justificativa: oblíquo na maior parte e abaixo da altitude de referência; a avaliação atual do artigo confunde geometria e cena.

### 5.13 AU-AIR (2020). Nota 2

- Bozcan e Kayacan, ICRA 2020, pp. 8504-8510. DOI 10.1109/ICRA40945.2020.9196845, conferido. Parrot Bebop 2, 1920 x 1080, interseção em Aarhus. Altitude de 5 a 30 m, maioria a 10, 20 e 30 m (fig. 6 do artigo); ângulo de 45 a 90 graus; metadado de GPS, altitude, IMU e velocidade. 32.823 quadros, 132.034 caixas, das quais 5.158 de pessoa. Licença CC BY só em fonte secundária (Superb AI); o GitHub `bozcani/auairdataset` deu 404. Baixo e com poucas pessoas.

### 5.14 Manipal-UAV (2023). Nota 2

- Akshatha K. R. et al., ISPRS Journal of Photogrammetry and Remote Sensing, 195, 77-89. DOI 10.1016/j.isprsjprs.2022.11.008, conferido. DJI Mavic Pro e Phantom, 1280 x 720, 10 a 50 m (amostras a 10, 20, 30, 40 e 50 m), ângulo de 45 a 90 graus só em fonte secundária. 13.462 imagens, 153.112 instâncias, COCO e txt. GPL-3.0 no repositório, com cláusula de uso acadêmico; acesso por formulário e e-mail, com aviso de até 6 meses. Baixa resolução e altitude baixa.

### 5.15 SARD (2021). Nota 2

- Sambolek e Ivasić-Kos, IEEE Access, 9, 37905-37922. DOI 10.1109/ACCESS.2021.3063681, conferido (a página do DataPort traz esse DOI; o 3063421 que circulava está errado). Dados: IEEE DataPort, DOI 10.21227/ahxm-k331, DataCite, CC BY 4.0, mas a página exige assinatura ou login. DJI Phantom 4 Advanced, 1920 x 1080 a 50 fps, 5 a 50 m, ângulos de 45 a 90 graus, Moslavačka gora, Croácia; 1.981 imagens, 6.532 caixas (ForestPersons), VOC e YOLO; 4,43 GB. Oblíquo e baixo.

### 5.16 Archangel-Real (2023). Nota 2

- Shen et al., IEEE Access, 11, 80958-80972. DOI 10.1109/ACCESS.2023.3299235, conferido (já na lista de 30/09). Câmera ELP 1920 x 1080 com cerca de 120 graus de campo, "pitched forward by 45 degrees relative to level flight", apontada ao alvo enquanto o drone circula; altitude e raio de 15 a 50 m em passos de 5 m. Archangel-Real a 1304 x 978. Acesso em a2i2-archangel.vision com login. Oblíquo por construção.

### 5.17 AFO (2021). Nota 2

- Gąsienica-Józkowy, Knapik e Cyganek, Integrated Computer-Aided Engineering, 28(3), 221-235. DOI 10.3233/ICA-210649, conferido. Kaggle, CC BY-NC-SA 3.0, formato Darknet, 4,36 GB. 50 vídeos de 1280 x 720 a 3840 x 2160, "bird's-eye view", altitude não declarada; 3.647 imagens, 39.991 objetos, 33.174 humanos (contagem do Dataset Ninja). Pessoa na água e altitude desconhecida.

### 5.18 Semantic Drone Dataset, ICG TU Graz (2017). Nota 2

- Sem artigo com DOI. Nadir, 5 a 30 m, 6000 x 4000; 400 imagens públicas com máscaras semânticas e caixas de pessoa (LabelMe XML); uso não comercial, sem redistribuição, pedido por formulário Google. Estimativa minha de GSD: 0,2 a 1,2 cm/px; precisaria de reamostragem por 4 a 20 para chegar à referência.

### 5.19 DroneCrowd (2021). Nota 2

- Wen et al., CVPR 2021, pp. 7808-7817. DOI 10.1109/CVPR46437.2021.00772, conferido. 112 clipes, 33.600 quadros 1920 x 1080, 4,8 milhões de pontos de cabeça, 20.800 trajetórias; DJI Phantom 4, 4 Pro e Mavic; atributos de luz, escala e densidade, sem altitude no artigo final (a versão preliminar no arXiv 1912.01811 definia dois níveis de altitude com corte em 70 m). Pontos, não caixas.

### 5.20 AerialMPT (2020). Nota 2

- Kraus, Azimi, Ercelik, Bahmanyar, Reinartz e Knoll, ICPR 2020, pp. 2454-2461. DOI 10.1109/ICPR48806.2021.9413031, conferido. Sistema 3K do DLR em helicóptero (nadir mais duas laterais), 600 a 1.400 m, 8 a 13 cm/px; 14 sequências, 307 quadros (recortes de 425 x 358 em média), 2.528 pedestres com ponto e identidade; zip de 75 MB no DLR, GNU GPL. Nadir, mas pontos e recortes pequenos. O KIT AIS, único antecessor (189 quadros, 32.760 pedestres), é criticado por esse artigo e não foi localizado em distribuição ativa.

### 5.21 Unicamp-UAV (2026, Brasil). Nota 2

- Simões, Oliveira e Pereira, ISPRS Journal of Photogrammetry and Remote Sensing, 231, 119-136. DOI 10.1016/j.isprsjprs.2025.10.026, conferido. DJI Phantom 4, 3840 x 2160, cerca de 30 m, campus Barão Geraldo da Unicamp, de dia; 6.500 imagens, 58.555 instâncias, YOLO txt; só pesquisa acadêmica; Google Drive. A imagem de amostra do repositório (DJI_0083_2224.jpg) tem o horizonte no quadro: oblíquo. É o único conjunto aéreo brasileiro de pessoas encontrado; não é favela.

### 5.22 LaDD, Lacmus Drone Dataset (2023). Nota 2, não verificado

- Sem artigo. GitHub lacmus-foundation; 1.365 imagens, 4.733 pedestres, 4000 x 3000, 40 a 100 m (fontes secundárias divergem); GPL segundo o Dataset Ninja; os links públicos estão mortos e o acesso hoje depende de credenciais do projeto.

### 5.23 Outros, com nota 1 ou 0

- BIRDSAI (Bondi et al., WACV 2020, DOI 10.1109/WACV45572.2020.9093284, conferido): térmico, 60 a 120 m, animais e pessoas em savana, 162K imagens; não conferido em detalhe.
- TinyPerson (Yu, Gong, Jiang, Ye e Han, WACV 2020, DOI 10.1109/WACV45572.2020.9093394, conferido): 1.610 imagens de vídeos da internet, 72.651 pessoas em "sea person" e "earth person", vista oblíqua e distante à beira-mar; restrições de uso sem licença formal.
- UAV123 (Mueller, Smith e Ghanem, ECCV 2016, DOI 10.1007/978-3-319-46448-0_27, conferido): rastreamento de um alvo, 5 a 25 m, DJI S1000 com Panasonic GH4, 720p, 13,7 GB; licença não declarada.
- P-DESTRE (Kumar, Yaghoubi, Das, Harish e Proença, IEEE TIFS, 16, 1696-1708, DOI 10.1109/TIFS.2020.3040881, conferido): 5,5 a 6,7 m, 45 a 90 graus, 4K.
- MAVREC (Dutta, Das, Nielsen, Chakraborty e Shah, CVPR 2024, DOI 10.1109/CVPR52733.2024.02140, conferido): 25 a 45 m segundo a tabela de Nguyen; não conferido em detalhe.
- UAVDT (Du et al., ECCV 2018, DOI 10.1007/978-3-030-01249-6_23, conferido): só veículos (car, truck, bus). Não serve.
- Conjunto de pessoas do DLR usado no Drones4Good (Bahmanyar e Merkle, "Saving lives from above"): 311 imagens aéreas e de drone com 10.050 pessoas, GSD de 0,2 a 6 cm/px, na maior parte nadir; descrito como "our own training dataset", sem indicação de distribuição pública.
- Kiefer, Messmer e Zell (2021) também anunciam o PeopleOnGrass (POG): 2.900 imagens 3840 x 2160 com 13.713 objetos e altitude e pitch exatos (0 a 100 m, pitch de 0 a 90 graus). Não encontrei página de distribuição; fica como pista a verificar com os autores.

## 6. Favelas, Kigali, Slovo Park e arma portada

- Não encontrei conjunto público de imagem aérea com caixa de pessoa sobre assentamento informal (Rio, Kigali, Slovo Park ou outro). O que existe para essas áreas é mapeamento de edificação (OpenAerialMap, projetos HOT), sem pessoa anotada. O único conjunto brasileiro de pessoas vistas de drone é o Unicamp-UAV (campus, oblíquo, 30 m).
- Arma portada: nenhuma novidade em relação a 30/09. Nenhum dos 28 conjuntos acima tem classe de arma.

## 7. Ranking e recomendação (no máximo três)

1. HERIDAL (nota 4). Nadir declarado, caixas de pessoa no chão, 1.647 imagens de 12 MP a 40 a 65 m. Protocolo sugerido: avaliar o modelo de 75 m na resolução nativa (GSD estimada de 1,5 a 2,4 cm/px) e o modelo de 150 m com reamostragem por 2 (3 a 4,8 cm/px), ladrilhando em 1280 como no artigo. Restrições: a página da FESB estava fora do ar em 17/10, licença não declarada, anotação VOC, cena de mato (sem edificação). É o teste de geometria com pessoa em pé.
2. SeaDronesSee OD v2 (nota 3). Filtrar pelo metadado por quadro: pitch do gimbal entre 80 e 90 graus e altitude entre 120 e 180 m (ou 100 a 260 m para ter volume), o que dá GSD estimada de 3,5 a 4,5 cm/px, a mais próxima da referência. Restrições: registro no site, licença não declarada, teste sem anotação (usar treino e val), COCO JSON, dezenas de GB, pessoa na água (forma de alvo diferente). É o teste de geometria exata com troca de cena.
3. Stanford Drone Dataset (nota 3). Nadir a cerca de 80 m sobre campus, com pedestres em caixa; o único conjunto nadir urbano acima de 50 m. Protocolo: amostrar quadros dos 60 vídeos, usar só caixas não interpoladas (generated = 0) e não perdidas (lost = 0), classe pedestre; ler o resultado no regime do corpus piloto (pessoa de 10 a 25 px). Restrições: 69 GB, CC BY-NC-SA 3.0, GSD grosseira e não declarada, formato próprio de texto.

Alternativas, se alguma das três falhar: MOBDrone (CC BY 4.0, sem registro, nadir a 50 e 60 m com GSD estimada de 3,9 a 4,7 cm/px, pessoa na água; 5,5 GB de vídeo) substitui o SeaDronesSee; o conjunto do KIOS (CC BY 4.0, 40 e 60 m, 221 mil caixas em estacionamento) substitui o Stanford se os autores confirmarem câmera vertical; o DLR-ACD (nadir urbano a 4,5 a 15 cm/px, pontos) serve a uma checagem de contagem ou de "ponto dentro da caixa", não a mAP.

## O que entra no artigo

Frases em inglês, para as seções de limitações e trabalho futuro, com a citação de cada uma. Entram só com o OK do autor.

1. Limitações, sobre o benchmark usado: "The real benchmark used here, VisDrone-DET, was captured at an estimated 30 to 100 m with the camera mostly tilted: in its training split only about 16 per cent of the annotated objects lie in bird-view images, against 84 per cent in images with an acute viewing angle (Kiefer, Messmer, & Zell, 2021; altitude range after Nguyen et al., 2026). The near-zero zero-shot scores of the nadir models therefore measure a change of viewing geometry as much as a change of scene."
2. Limitações, sobre o que existe: "No public aerial benchmark with bounding boxes of people on land reproduces a nadir view at 150 m and about 5 cm per pixel. The closest are HERIDAL, nadir at 40 to 65 m and about 2 cm per pixel (Božić-Štulić, Marušić, & Gotovac, 2019; Pyrro, Naseri, & Jung, 2021), the Stanford Drone Dataset, nadir at about 80 m over a university campus (Robicquet, Sadeghian, Alahi, & Savarese, 2016), and SeaDronesSee, whose per-frame altitude and gimbal pitch allow nadir frames between 100 and 260 m to be selected, although its people are in the water (Varga, Kiefer, Messmer, & Zell, 2022)."
3. Trabalho futuro: "A zero-shot evaluation of the nadir models on HERIDAL resampled to the target ground sampling distance, on the nadir frames of SeaDronesSee and on the Stanford Drone Dataset would separate the effect of viewing geometry from that of scene content; the aerial crowd images of DLR-ACD, nadir at 4.5 to 15 cm per pixel but annotated with points, allow only a counting-style check (Bahmanyar, Vig, & Reinartz, 2019)."
4. Opcional, para a seção do Sul Global: "We found no public aerial dataset with person boxes over a dense informal settlement; the only Brazilian aerial person dataset we located, Unicamp-UAV, is oblique at about 30 m over a university campus (Simões, Oliveira, & Pereira, 2026)."

## Entradas para a lista de referências

Em APA 7, prontas para colar. Só as obras citadas nas frases acima ou nos três conjuntos recomendados. DOIs conferidos no Crossref em 17/10; as duas entradas do arXiv não têm DOI.

Bahmanyar, R., Vig, E., & Reinartz, P. (2019). MRCNet: Crowd counting and density map estimation in aerial and ground imagery. arXiv. https://arxiv.org/abs/1909.12743

Božić-Štulić, D., Marušić, Ž., & Gotovac, S. (2019). Deep learning approach in aerial imagery for supporting land search and rescue missions. International Journal of Computer Vision, 127(9), 1256-1278. https://doi.org/10.1007/s11263-019-01177-1

Kiefer, B., Messmer, M., & Zell, A. (2021). Diminishing domain bias by leveraging domain labels in object detection on UAVs. In 2021 20th International Conference on Advanced Robotics (ICAR) (pp. 523-530). IEEE. https://doi.org/10.1109/ICAR53236.2021.9659357

Nguyen, K., Liu, F., Fookes, C., Sridharan, S., Liu, X., & Ross, A. (2026). Person recognition in aerial surveillance: A decade survey. IEEE Transactions on Biometrics, Behavior, and Identity Science, 8(1), 3-19. https://doi.org/10.1109/TBIOM.2025.3617011

Pyrro, P., Naseri, H., & Jung, A. (2021). Rethinking drone-based search and rescue with aerial person detection. arXiv. https://arxiv.org/abs/2111.09406

Robicquet, A., Sadeghian, A., Alahi, A., & Savarese, S. (2016). Learning social etiquette: Human trajectory understanding in crowded scenes. In Computer Vision, ECCV 2016 (Lecture Notes in Computer Science, pp. 549-565). Springer. https://doi.org/10.1007/978-3-319-46484-8_33

Simões, D. P., Oliveira, H. C. de, & Pereira, D. R. (2026). Unicamp-UAV: An open dataset for human detection in UAV imagery. ISPRS Journal of Photogrammetry and Remote Sensing, 231, 119-136. https://doi.org/10.1016/j.isprsjprs.2025.10.026

Varga, L. A., Kiefer, B., Messmer, M., & Zell, A. (2022). SeaDronesSee: A maritime benchmark for detecting humans in open water. In 2022 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) (pp. 3686-3696). IEEE. https://doi.org/10.1109/WACV51458.2022.00374

Se as alternativas forem citadas:

Cafarelli, D., Ciampi, L., Vadicamo, L., Gennaro, C., Berton, A., Paterni, M., Benvenuti, C., Passera, M., & Falchi, F. (2022). MOBDrone: A drone video dataset for man overboard rescue. In Image Analysis and Processing, ICIAP 2022 (Lecture Notes in Computer Science, pp. 633-644). Springer. https://doi.org/10.1007/978-3-031-06430-2_53

Vasileiadis, A., Savva, A., & Kyrkou, C. (2026). Aerial dataset for car and person detection [Data set]. Zenodo. https://doi.org/10.5281/zenodo.21216709

Wu, Z., Suresh, K., Narayanan, P., Xu, H., Kwon, H., & Wang, Z. (2019). Delving into robust object detection from unmanned aerial vehicles: A deep nuisance disentanglement approach. In 2019 IEEE/CVF International Conference on Computer Vision (ICCV) (pp. 1201-1210). IEEE. https://doi.org/10.1109/ICCV.2019.00129

Já constam das listas propostas em 30/09 e não se repetem aqui: Zhu et al. (2022, VisDrone), Barekatain et al. (2017, Okutama-Action), Broyles et al. (2022, WiSARD), Shen et al. (2023, Archangel), Kiefer, Ott e Zell (2022).

## Notas de verificação

- Conferidos no Crossref (status ok, título e autores batem): HERIDAL, SARD (artigo), AFO, Okutama, Manipal, VisDrone, SeaDronesSee, HIT-UAV, NOMAD, TinyPerson, DroneCrowd, UAV123, AU-AIR, UAVDT, MOBDrone (capítulo), Kiefer-Messmer-Zell 2021, Kiefer-Ott-Zell 2022, Archangel, WiSARD, Nguyen 2026, Stanford Drone, P-DESTRE, Wu 2019, VTSaR (JSTARS, TGRS e Journal of Remote Sensing), Unicamp-UAV, AerialMPT, BIRDSAI, MAVREC.
- Conferidos na DataCite: SARD (DataPort, CC BY 4.0), MOBDrone (Zenodo, CC BY 4.0), KIOS (Zenodo, CC BY 4.0).
- Sem DOI (só arXiv): MRCNet/DLR-ACD, Pyrro et al. 2021. Sem artigo: Semantic Drone Dataset, LaDD, KIOS.
- Erro corrigido: o DOI do artigo do SARD é 10.1109/ACCESS.2021.3063681 (não 3063421).
- O Crossref devolveu 429 em metade das consultas feitas pela ferramenta web; as repetições saíram por script com pausa de 2 s e User-Agent genérico, sem e-mail.
- Nenhum dataset foi baixado. Arquivos obtidos para leitura: PDFs de artigos abertos, READMEs, uma imagem de amostra do Unicamp-UAV (3840 x 2160) e duas figuras do VTSaR, todos na pasta de rascunho da sessão, fora do repositório.
