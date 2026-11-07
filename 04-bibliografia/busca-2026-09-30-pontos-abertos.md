# Busca bibliográfica de 30/09/2026: pontos abertos do artigo

Pedido do autor em 30/09. Oito agentes em cinco frentes: busca e verificação cética para cada um dos três temas de conteúdo (arma portada em benchmark público, convenção de voar com céu limpo, sintético que atrapalha) e uma conferência para cada lista de referências pendentes (B1 e fontes jornalísticas de `01-artigo/PENDENCIAS.md`). Cada fonte foi aberta; os DOIs foram conferidos no Crossref (os do Zenodo e do Mendeley, no DataCite).

**Nada no manuscrito foi alterado. As mudanças abaixo esperam o OK do autor.** Os textos propostos em inglês estão prontos para colar. Os números de linha citados pelos agentes são de antes da revisão geral de 30/09: localizar pela frase. O resultado bruto completo está em `busca-2026-09-30-pontos-abertos.json`, ao lado.

## O que muda no artigo, se aprovado

1. **Arma portada em benchmark público** (abstract, abertura da seção 7, 7.7 e conclusão; opcionais na introdução, 7.4, 7.6 e 8.2). A frase "no public benchmark annotates a carried firearm" está errada por ser ampla demais. Existem benchmarks públicos com arma portada, todos de vigilância (CCTV-Gun, Mock Attack, UCLM, Monash Guns, Sohas, YouTube-GDD). Do ar, o que é público fica a 2 a 8 m e rotula por ação ou por gravação, não por caixa (UAV-Human; Dual-UAV, do CEFET-RJ, com réplica de fuzil contra guarda-chuva). Os conjuntos de drone com caixa de arma descritos em artigo não são públicos. Nas altitudes do artigo não há nada. Proposta: "we found no public aerial benchmark that annotates a carried firearm at these altitudes", um parágrafo novo na 7.7 e de 9 a 11 referências novas. A justificativa da 7.7 (pontuar os modelos de três classes na validação sintética) continua de pé.
2. **"Clear weather" como convenção de voo** (8.4, 11.3 e fecho da conclusão; opcionais na 8.3 e 10.3). Só o aerolevantamento tem convenção escrita de céu limpo (NGS, 2002; RICS, 2021), e ela controla a sombra pela elevação do sol: o hard sun do gerador (46 a 74 graus) cabe nela, o low sun fica abaixo. A orientação para mapeamento com drone é dividida por produto (modelo 3D prefere encoberto; ortomosaico prefere sol). As regras de voo (FAA, EASA, ANAC, DECEA) pedem visibilidade, não sol, e no Brasil vedam voo sob chuva. Não há estudo em imagem real que isole sol duro contra encoberto para pessoas vistas do ar. Proposta: reescrever uma frase da 8.4, o primeiro parágrafo da 11.3 (vira quatro, mais duas ressalvas) e o fecho; cerca de 20 referências, entre elas Zhu et al. (2022), o artigo do VisDrone, que falta hoje na lista embora o benchmark seja usado no artigo todo.
3. **Sintético que atrapalha** (9.4 e seção 2). A 9.4 não é anômala. Em Kiefer, Ott e Zell (2022, fig. 2), com só 10 mil imagens sintéticas o pré-treino ficou abaixo de não ter pré-treino sintético no SeaDronesSee e só ajudou no VisDrone com o menor volume real. No SynPlay (Yim et al., 2026), corpora sintéticos públicos ficaram abaixo até do treino do zero, e um corpus grande e variado ajudou. Treino misto sem balanceamento pende para o sintético (Shen et al., 2023a; Martinez-Esteso et al., 2025). O mecanismo candidato (os pesos de partida) tem só apoio indireto. Proposta: um parágrafo novo que fecha a 9.4 e, na seção 2, citações para a ressalva que a revisão geral já pôs ("reports" no lugar de "confirms"); 11 referências.
4. **Referências B1** (13 obras da introdução e da revisão de literatura). As 13 foram encontradas e conferidas no Crossref. Há erro em cinco entradas já inseridas em `08-references.md`: Agrawal (inicial P.), Rasoulie (inicial F. e número de artigo 24356), da Silva (volume 147), Du (páginas 13169-13187) e Gevaert (DOI exibido pelo editor). Há ajuste de conteúdo em quatro: Barisic (o objeto detectado é o próprio UAV), Horváth (objetos industriais, mAP50, e nove palavras seguidas copiadas do resumo sem aspas), Watson e Elliott (oito palavras copiadas; "essential" não está no resumo) e Gevaert ("substantially" exagera o resumo). Nove das 13 candidatas de `01-artigo/candidatos_crossref.json` estão erradas: não reutilizar esse arquivo.
5. **Fontes jornalísticas** (B3, B6, B7, B9 e B10, seções 3 e 4 do texto do coautor). A Wikipédia tem substituto nos três usos (CNN Brasil, Justiça Global, Lessing, 2008, Misse, 2011, InSight Crime). "CNN Brasil (2026a)" é matéria da Defesa em Foco. "Maior alta do país" não está no Anuário e é falso em termos relativos (Rio Grande do Norte, +100%). B7 é de Scott Mistler-Ferguson, 27/01/2022; sustenta os 60.000 moradores, os mais de 1.200 policiais militares e o Cidade Integrada, mas não as frases sobre ambiente construído. 132 mortos é contagem da Defensoria que só aparece na imprensa; 121 é o número oficial e 122 inclui o quinto policial. O pico da série estadual do ISP é 1994, não o início dos anos 2000. A base atual do ISP também dá 703 mortes por intervenção em 2024, o que enfraquece a explicação da diferença com o 699 da JOTA na seção 3.

## Decisões que ficam com o autor

- Aprovar, por frente, os textos propostos abaixo (ou pedir outra redação).
- Seção 3: como citar 51 ou 100 mandados; achar fonte para a falta de mapas atualizados das rotas ou tratá-la como argumento próprio; dois-pontos no lugar do traço na manchete do InSight Crime; Penglase (2008) não foi lido (texto pago).
- Frente 2: a URL oficial da EASA contém um travessão codificado; se a regra do travessão pesar, citar a decisão sem a URL.

## Nota de processo

Dois agentes de busca (arma e clima) mandaram o e-mail do autor no cabeçalho das primeiras consultas à API do Crossref, no campo de contato que o Crossref recomenda. O projeto não autoriza enviar o e-mail a serviço de terceiros; as consultas seguintes saíram sem ele e nenhum outro dado do autor foi enviado. Onde o ScienceDirect ou o Roboflow recusaram a leitura automática, os agentes leram a página pelo navegador embutido, só leitura, sem contornar verificação anti-robô.


## 1. Arma portada em benchmark público

### Veredito da verificação

VEREDITO: como está escrita, a frase é ampla demais e está errada. Com uma qualificação ela se sustenta, e a justificativa da 7.7 (pontuar os modelos de três classes na validação sintética) continua válida.

CONFERÊNCIA DAS 18 FONTES
Todas existem e os metadados batem: 12 DOIs conferidos no Crossref, 2 DOIs DataCite (Dual-UAV e Mendeley), 2 só com arXiv (G-MAD e YouTube-GDD) e 2 páginas sem DOI (Kaggle e Roboflow). Todas dizem, no essencial, o que o resumo afirma, e os 18 trechos existem. Ajustes:
(a) Duas lacunas resolvidas. O Sohas está sob CC BY-SA 4.0, segundo o README. O Archangel é distribuído pelo site do ARL, com login.
(b) Nuances que faltavam. O conjunto Mendeley se chama de 'useful benchmark'. A licença do Faheem aparece como CC BY 4.0 na página e 3.0 no Crossref. O AlJundi fala em 'model weapons'. Chamar o smartphone do conjunto de Sevilha de objeto confundível é inferência.
(c) Correção de fundo no item 3 da busca. Há coleções públicas de usuário no Roboflow com imagem de drone e caixa de arma, por exemplo Drone-Weapon-Our-drone (2.610 imagens, person e weapon, CC BY 4.0). Nenhuma tem descrição, altitude ou protocolo. 'Os conjuntos de drone com caixa de arma não são públicos' só vale para conjuntos descritos em artigo. Por isso a frase do artigo precisa dizer 'benchmark', não 'dataset'.

QUADRO REVISADO
1. Benchmarks públicos que anotam arma portada existem, todos de vigilância ou vídeo:
- CCTV-Gun, com as classes Person e Handgun.
- Mock Attack, chamado de 'public benchmark dataset' por Hnoohom et al. (2022).
- O conjunto da UCLM, com Handgun e Machine_Gun e as ações carry e aim.
- Monash Guns, Sohas e YouTube-GDD.
Na vigilância existe até o desenho de objeto confundível do artigo: o Sohas e uma amostra sintética comercial de fuzil contra guarda-chuva (Simuletic, sem revisão por pares).
2. Do ar, o material público descrito em artigo ou repositório fica a 2-8 m e marca a arma por rótulo de ação ou por gravação, não por caixa:
- UAV-Human, de 2 a 8 m, com a ação A131.
- Dual-UAV, a 2 e 5 m, réplica de fuzil contra guarda-chuva, com rótulo no nome do arquivo e a palavra-chave 'benchmark dataset'.
- AVI, de 2 a 8 m, mas não declara disponibilidade.
3. Os conjuntos de drone com caixa de arma descritos em artigo não são públicos:
- AlJundi: 20 m, sem declaração de dados.
- Faheem: dados só para órgãos policiais.
- A vitrine do Kaggle não distribui o conjunto.
- Ma e Yakimenko (2023) tratam de arma largada no chão, não de arma portada.
4. Nas altitudes do artigo (35, 75 e 150 m) não achei benchmark público, real ou sintético, com arma portada anotada:
- AMOD (120 m): não tem classe de pessoa.
- Archangel (15-50 m real): pessoas, sem arma.
- VisDrone (30-100 m): nenhuma categoria de arma.
- Mendeley 2026 (sintético de GTA5) e KIIT-MiTA (Kaggle): classe 'soldier', que marca o papel militar e não a arma, sem altitude informada.
Um revisor pode apontar 'soldier' como análogo de 'armado'. A redação com 'annotates a carried firearm' resiste a essa objeção.
5. Os conjuntos de 2-8 m não serviriam de teste para os modelos de 35 e 75 m, por causa da escala. É esse o argumento que a 7.7 pode usar.

REDAÇÃO RECOMENDADA
Trocar a frase por 'we found no public aerial benchmark that annotates a carried firearm at these altitudes'.
Ocorrências, com as linhas conferidas hoje (a busca indicou números antigos):
- Abstract: 01-introduction.md, linhas 19-20.
- Variante: 03b, linhas 9-10 (não a 13).
- 7.7: 03b, linhas 283-284 (não 298-300).
- 07-conclusion.md, linha 5.
Opcionais:
- 01-introduction.md, linha 60.
- 06b, linha 123: 'contains no carried firearms', dito do VisDrone, fica melhor como 'has no firearm category'.

Mudanças em relação à redação da busca:
(i) 'public aerial collections' virou 'documented public aerial datasets ... that label a person as armed', por causa do Roboflow e dos conjuntos com 'soldier'.
(ii) Para o AlJundi, 'not public' virou 'not released with the article'.
(iii) Tirei 'drawn from online video' da frase da 7.7: as quatro obras citadas ali são de vigilância.
(iv) As citações com o sobrenome Li levam iniciais (T. Li; Z. Li), para distinguir os dois primeiros autores.
(v) O Faheem entra como 'Haq, Q. E. U.', como está no Crossref.
(vi) O Dual-UAV é citado como 'Torkst et al.'.

LACUNAS
- Roboflow: a busca devolve 300 projetos e inspecionei 3.
- Dual-UAV: não baixei o samples.rar, então não posso excluir que haja caixas lá dentro.
- Ma e Yakimenko: sem texto integral. Houve CAPTCHA e não contornei.
- O link de dados do ACF dá 404.
- Não houve busca em texto integral no IEEE Xplore, na Scopus ou no Scholar.
Nenhum arquivo do repositório foi editado.

NOTA OPERACIONAL: nas 12 primeiras consultas à API do Crossref pus por engano o e-mail do usuário no cabeçalho User-Agent. Todas as consultas seguintes saíram sem ele.

### Texto proposto, já revisado pela verificação

```text
[1] Abstract, 01-introduction.md, lines 19 to 20. Replace the clause "since no public benchmark annotates a carried firearm":
On synthetic validation imagery only, since we found no public aerial benchmark that annotates a carried firearm at such altitudes, the detector trained at that altitude calls 24 per cent of those objects armed; [rest of the sentence unchanged]

[2] Section 7, opening, 03b-methodology-synthetic-pipeline.md, lines 9 to 10:
... and at 75 m and 35 m in three classes, armed, unarmed, and unarmed carrying a confusable elongated object, a distinction for which we found no public aerial benchmark at these altitudes.

[3] Section 7.7, 03b-methodology-synthetic-pipeline.md, lines 283 to 284. Replace the sentence that begins "Because no public benchmark annotates a carried firearm":
Public benchmarks that annotate a carried firearm do exist, but they are recorded from surveillance viewpoints, not from the air (Salazar González et al., 2020; Lim et al., 2021; Ruiz-Santaquiteria et al., 2024; Z. Li et al., 2025). The documented public aerial datasets we found that label a person as armed were captured between 2 and 8 m above the ground, and they attach that label to an action class or to a whole recording rather than to an annotated box (T. Li et al., 2021; Torkst et al., 2026). The drone datasets we found with annotated firearms are either restricted to law-enforcement agencies (Faheem et al., 2025) or were not released with the article that describes them (AlJundi et al., 2025). Because we found no public aerial benchmark that annotates a carried firearm at the altitudes studied here, the three-class models are scored instead on the validation split of their own corpus, [rest of the sentence unchanged]

[4] Conclusion, 07-conclusion.md, line 5, last sentence:
The transfer measured is that of person detection, since we found no public aerial benchmark that annotates a carried firearm at the altitudes studied here.

[5] Optional, 01-introduction.md, line 60:
Only the second has a public benchmark against which transfer can be measured, and only for people: we found no public aerial benchmark for the armed class. That is why it, and not the first, carries the empirical claims of this article.

[6] Optional, 06b-model-free-evidence.md, line 123:
The benchmark has no firearm category, so for transfer to it the weapon is a source of shape mismatch rather than of signal.

[7] Optional, Section 7.4, after the paragraph on carried objects and hard negatives (03b, around line 180):
Setting weapons against objects handled in the same way has precedents: in surveillance imagery, a pistol and a knife are set against a smartphone, a banknote, a purse and a card (Pérez-Hernández et al., 2020), and from drones hovering at 2 and 5 m, a rifle replica is set against a visually similar umbrella (Torkst et al., 2026).

[8] Optional, Section 7.6, next to the argument for native-scale tiles (03b, around line 241):
Tiling has been adopted for the same reason in surveillance footage of armed pedestrians, where downsampling erases small weapons (Hnoohom et al., 2022).

[References to add; every DOI checked in Crossref, the Zenodo one in DataCite. Add Hnoohom and Pérez-Hernández only if items 7 and 8 are used]
AlJundi, Z., Alsubaie, S., Faheem, M. H., Almarashi, R. M., Qazi, E.-u.-H., & Kim, J. H. (2025). Dangerous objects detection using deep learning and first responder drone. International Journal of Digital Crime and Forensics, 16(1), 1-18. https://doi.org/10.4018/ijdcf.367034
Faheem, M. H., Haq, Q. E. U., Khan, T. M., & Kim, J. H. (2025). Deep-learning-based weapon detection using drones equipped with infrared and color cameras. International Journal of Digital Crime and Forensics, 17(1), 1-16. https://doi.org/10.4018/ijdcf.393088
Hnoohom, N., Chotivatunyu, P., & Jitpattanakul, A. (2022). ACF: An armed CCTV footage dataset for enhancing weapon detection. Sensors, 22(19), 7158. https://doi.org/10.3390/s22197158
Li, T., Liu, J., Zhang, W., Ni, Y., Wang, W., & Li, Z. (2021). UAV-Human: A large benchmark for human behavior understanding with unmanned aerial vehicles. In 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (pp. 16261-16270). https://doi.org/10.1109/cvpr46437.2021.01600
Li, Z., Yellapragada, S., Bhadresh Doshi, K., Mhasakar, P. M., Fan, H., Wei, J., Blasch, E., Zhang, B., & Ling, H. (2025). CCTV-Gun: Benchmarking handgun detection in CCTV images. In Dynamic Data Driven Applications Systems (Lecture Notes in Computer Science, pp. 171-181). Springer Nature Switzerland. https://doi.org/10.1007/978-3-031-94895-4_18
Lim, J., Al Jobayer, M. I., Baskaran, V. M., Lim, J. M., See, J., & Wong, K. (2021). Deep multi-level feature pyramids: Application for non-canonical firearm detection in video surveillance. Engineering Applications of Artificial Intelligence, 97, 104094. https://doi.org/10.1016/j.engappai.2020.104094
Pérez-Hernández, F., Tabik, S., Lamas, A., Olmos, R., Fujita, H., & Herrera, F. (2020). Object detection binary classifiers methodology based on deep learning to identify small objects handled similarly: Application in video surveillance. Knowledge-Based Systems, 194, 105590. https://doi.org/10.1016/j.knosys.2020.105590
Ruiz-Santaquiteria, J., Muñoz, J. D., Maigler, F. J., Deniz, O., & Bueno, G. (2024). Firearm-related action recognition and object detection dataset for video surveillance systems. Data in Brief, 52, 110030. https://doi.org/10.1016/j.dib.2024.110030
Salazar González, J. L., Zaccaro, C., Álvarez-García, J. A., Soria Morillo, L. M., & Sancho Caparrini, F. (2020). Real-time gun detection in CCTV: An open problem. Neural Networks, 132, 297-308. https://doi.org/10.1016/j.neunet.2020.09.013
Torkst, C., Rangel, P., & Efigenio, J. (2026). Dual-UAV dataset for detection and localization of armed individuals [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18746168

[Note for the author] "We found no" can become "to our knowledge, no" if the house style prefers it. Keep "benchmark" and do not replace it with "dataset": undocumented user collections of drone imagery with weapon boxes do exist on Roboflow.
```

### Fontes da busca, com a conferência

- **Muhammad Hamza Faheem, Qazi Emad Ul Haq, Tariq M. Khan, Jong Hyuk Kim (2025)**. Deep-Learning-Based Weapon Detection Using Drones Equipped With Infrared and Color Cameras. International Journal of Digital Crime and Forensics, 17(1), 1-16. DOI: 10.4018/ijdcf.393088. Crossref: sim; aberta pelo agente: sim.
  O que diz: Artigo revisado por pares, em acesso aberto (CC BY 3.0). Drone quadrirrotor com câmera colorida e infravermelha, gravando em laboratório, estacionamento e deserto, com armas metálicas reais em cena, algumas junto a carros ou dentro de veículos (nem sempre portadas por pessoa). Caixas para arma longa, pistola e faca. Não informa altitude. Afirma que não há conjunto público de arma de fogo coletado por drone. Os dados não são públicos: a seção de disponibilidade diz que podem ser cedidos a órgãos policiais aprovados, mediante pedido. Real, drone.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref (10.4018/ijdcf.393088): título, 4 autores, IJDCF 17(1), 1-16, 2025. Li o texto integral na IGI pelo navegador (o WebFetch levou 429). A frase 'there are no publicly available firearm datasets collected from drones' está lá. Confirmei também: quadricóptero com câmera RGB e IR; laboratório, estacionamento e deserto; armas metálicas reais usadas perto de carros, dentro de veículos e em área aberta; classes guns, pistols e knives, em polígono; nenhuma altitude; 9.204 imagens. Disponibilidade: só para órgãos policiais aprovados, mediante pedido. Divergência pequena: a página diz CC BY com link para a 4.0 e o Crossref registra CC BY 3.0.

- **Zeyad AlJundi, Saad Alsubaie, Muhammad H. Faheem, Raha Mosleh Almarashi, Emad-ul-Haq Qazi, Jong Hyuk Kim (2025)**. Dangerous Objects Detection Using Deep Learning and First Responder Drone. International Journal of Digital Crime and Forensics, 16(1), 1-18. DOI: 10.4018/ijdcf.367034. Crossref: sim; aberta pelo agente: sim.
  O que diz: Trabalho anterior do mesmo grupo. Drone a 20 m do solo, à noite, sem zoom, em trajetória circular. Vídeo colorido 1920x1080 e infravermelho 640x480, com caixas para faca, pistola e arma longa. Real, drone a baixa altitude. O texto não tem declaração de disponibilidade e não encontrei o conjunto publicado.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref (10.4018/ijdcf.367034): título, 6 autores, IJDCF 16(1), 1-18, publicado em 10/01/2025 (o artigo de Faheem o cita como 2024). No texto integral: tabela com 20 m e sem zoom, vídeo colorido 1920x1080 e IR 640x480, gravação noturna com iluminação, trajetória circular, classes knife, pistol e gun. O trecho citado existe literalmente. O texto fala em 'six different model weapons', o que sugere réplicas. Não há seção de disponibilidade de dados nem link.

- **Caio Torkst, Pablo Rangel, Jonathan Efigenio (2026)**. Dual-UAV Dataset for Detection and Localization of Armed Individuals. Zenodo (DOI DataCite, conferido em api.datacite.org; o Crossref devolve 404). DOI: 10.5281/zenodo.18746168. Crossref: não; aberta pelo agente: sim.
  O que diz: Público, acesso aberto, CC BY 4.0 (código sob MIT). Autores do CEFET-RJ e do Instituto de Pesquisas da Marinha; as palavras-chave incluem 'benchmark dataset' e 'weapon detection'. Real: dois drones Autel EVO II Dual 640T V2, RGB 1920x1080 a 60 fps, altitude de 2 m e 5 m, distância de 5 m e 10 m. Uma pessoa de balaclava segura réplica de fuzil ('real') ou guarda-chuva parecido ('falso'). O rótulo armado ou desarmado vem do nome do arquivo de cada gravação; nem a descrição nem os dois repositórios de código documentam caixa anotada da arma. É o precedente mais próximo do desenho do artigo (arma contra guarda-chuva), mas muito abaixo das altitudes dele. Os artigos associados (FUSION 2026 e LAFUSION 2025) não estão no Crossref.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. API do Zenodo e DataCite conferem título, autores (CEFET-RJ e Instituto de Pesquisas da Marinha), data 23/02/2026 e licenças CC BY 4.0 e MIT. O Crossref devolve 404, o que é esperado para DOI DataCite. A descrição confirma: altitude de 2 e 5 m, distância de 5 e 10 m, réplica de fuzil ('real') contra guarda-chuva ('falso'), rótulo no nome do arquivo e a palavra-chave 'benchmark dataset'. Os READMEs dos dois repositórios (Dual-UAV-Fusion-Detection-Localization e drone_yolo_detection) avaliam por amostra, com ou sem arma, e não documentam caixa anotada da arma. A busca por título no Crossref não achou os artigos FUSION 2026 e LAFUSION 2025.

- **Tianjiao Li, Jun Liu, Wei Zhang, Yun Ni, Wenqian Wang, Zhiheng Li (2021)**. UAV-Human: A Large Benchmark for Human Behavior Understanding with Unmanned Aerial Vehicles. 2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 16261-16270. DOI: 10.1109/cvpr46437.2021.01600. Crossref: sim; aberta pelo agente: sim.
  O que diz: Benchmark público de comportamento humano visto de drone, real, com RGB, profundidade, infravermelho e esqueleto. Altura de voo de 2 a 8 m. Entre as classes de ação há 'threat someone with a gun': a arma entra como rótulo de ação do vídeo, não como caixa. O README diz que o download está liberado e que houve termo de consentimento dos filmados; os termos de uso não foram conferidos.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 6 autores, CVPR 2021, pp. 16261-16270. O PDF do arXiv diz 'hovering height (varying from 2 to 8 meters)'. O README do GitHub traz 'A131: threat someone with a gun', download liberado e termo de consentimento de todos os filmados. A arma aparece como rótulo de ação, não como caixa.

- **Amarjot Singh, Devendra Patil, S. N. Omkar (2018)**. Eye in the Sky: Real-Time Drone Surveillance System (DSS) for Violent Individuals Identification Using ScatterNet Hybrid Deep Learning Network. 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), pp. 1710-17108. DOI: 10.1109/cvprw.2018.00214. Crossref: sim; aberta pelo agente: sim.
  O que diz: Apresenta o conjunto AVI: 2.000 imagens de drone Parrot AR a 2, 4, 6 e 8 m, com 10.863 pessoas anotadas com 14 pontos do corpo e rótulo de ação violenta, entre elas 'Shooting'. Não há caixa de arma: 'shooting' é pose. O artigo não tem declaração de disponibilidade nem link para os dados.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 3 autores, CVPRW 2018. A paginação '1710-17108' é erro do próprio registro no Crossref. No PDF do arXiv: 2.000 imagens, 10.863 pessoas com 14 pontos do corpo, cinco ações violentas (entre elas Shooting), drone Parrot AR a 2, 4, 6 e 8 m. O trecho existe. Não há declaração de disponibilidade nem link para os dados.

- **Yechan Kim, JongHyun Park, Dongho Yoon, Namhoon Jung, Moongu Jeon (2026)**. G-MAD: A Game-Based Data Generation Framework for Multi-View RGB-T Aerial Object Detection. arXiv:2607.19942 (ACM Multimedia 2026). DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Sintético (ARMA 3), RGB e térmico, multivista, com câmera a 120 m e GSD nominal de 0,1 m/pixel. O benchmark gerado (AMOD) anota 12 classes de equipamento militar (blindado, artilharia, helicóptero, tanque, radar, entre outras) e nenhuma classe de pessoa, soldado ou arma portátil. Portanto não contradiz a frase do artigo. O framework foi liberado só para pesquisa acadêmica não comercial.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. A API do arXiv (2607.19942) confere o título, os 5 autores e o comentário 'ACM Multimedia 2026'. Não há DOI: busquei o título no Crossref e não apareceu nada. No PDF, o AMOD tem 12 classes de equipamento (Armored, Artillery, Helicopter, LCU, MLRS, Plane, RADAR, SAM, Self-propelled Artillery, Support Vehicle, Tank, TEL), nenhuma de pessoa ou de arma portátil. Câmera a 120 m, GSD nominal de 0,1 m/pixel. O framework foi liberado só para pesquisa acadêmica não comercial ou protótipo. As colunas Person e Car do PDF vêm do HIT-UAV, que é real e só entra no fine-tuning. O trecho existe.

- **Mohammad Quraan, Ahmed Shatnawi, Basheer Al-Duwairi (2026)**. A Multi-Class UAV Military Object Detection Dataset: Tank, Drone, Soldier, and People Images from Aerial Perspectives with Synthetic Data Augmentation. Mendeley Data (DOI DataCite, conferido em api.datacite.org). DOI: 10.17632/9z7yrcrpjk.1. Crossref: não; aberta pelo agente: sim.
  O que diz: Público (CC BY 4.0). 7.985 imagens de vista aérea ou de cima com quatro classes: tanque, drone, pessoa e soldado. As imagens reais vêm de coleções do Roboflow e do Kaggle; a classe soldado é inteira sintética, gerada no GTA5, e os autores justificam pela escassez de imagem aberta de soldado vista por drone. Anota a pessoa pelo papel (soldado ou civil), não a arma portada. Altitude não informada.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. DataCite e a página do Mendeley conferem título, autores, a data 09/06/2026 e a licença CC BY 4.0. O DOI é DataCite, não Crossref. São 7.985 imagens nas classes tank, drone, people e soldier, com imagens reais tiradas do Roboflow e do Kaggle. Os passos 10 e 11 da página confirmam que o subconjunto soldier foi gerado no GTA5 (982 imagens base), então 'inteira sintética' está certo. O conjunto anota o papel da pessoa, não a arma. Nuance que faltou no resumo: a descrição cita 'altitude variations' sem dar números e chama o conjunto de 'useful benchmark'.

- **Zhenghong Li, Srikar Yellapragada, Kevin Bhadresh Doshi, Purva Makarand Mhasakar, Heng Fan, Jie Wei, Erik Blasch, Bin Zhang, Haibin Ling (2025)**. CCTV-Gun: Benchmarking Handgun Detection in CCTV Images. Dynamic Data Driven Applications Systems, Lecture Notes in Computer Science, pp. 171-181. DOI: 10.1007/978-3-031-94895-4_18. Crossref: sim; aberta pelo agente: sim.
  O que diz: Benchmark público (código Apache-2.0) com imagens reais de CCTV de três conjuntos (Monash Guns, US Real-time Gun Detection e UCF Crime), em que a pistola e a pessoa que a segura foram anotadas à mão (classes Person e Handgun). É benchmark público com arma portada anotada, o que contradiz a frase na forma atual. Ponto de vista de CCTV, não aéreo. Saiu em 2025 nos anais DDDAS (LNCS) com Zhenghong Li como primeiro autor; a versão arXiv põe Yellapragada primeiro.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 9 autores com Zhenghong Li em primeiro, LNCS 'Dynamic Data Driven Applications Systems', pp. 171-181, 2025, Springer. No arXiv o primeiro autor é Yellapragada, e o resumo traz 'manually annotate handguns and their holders'. O README confirma as três fontes (Monash Guns, US Real-time e UCF Crime) e as duas classes, Person e Handgun. Repositório sob Apache-2.0. É benchmark público com arma portada anotada, com imagem de CCTV.

- **JunYi Lim, Md Istiaque Al Jobayer, Vishnu Monn Baskaran, Joanne MunYee Lim, John See, KokSheik Wong (2021)**. Deep multi-level feature pyramids: Application for non-canonical firearm detection in video surveillance. Engineering Applications of Artificial Intelligence, 97, 104094. DOI: 10.1016/j.engappai.2020.104094. Crossref: sim; aberta pelo agente: sim.
  O que diz: Introduz o Monash Guns Dataset: pistolas em ambiente não controlado, vistas por vigilância, a partir de 250 vídeos gravados, com anotação PASCAL VOC. Público (Google Drive; licença MIT no repositório). Real, CCTV, não aéreo. O CCTV-Gun reanota nessas imagens também a pessoa que segura a arma.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 6 autores, EAAI 97, 104094, janeiro de 2021. O resumo na ScienceDirect diz 'constructed from a set of 250 recorded videos', com mais de 2.500 quadros vistos de CCTV. Repositório sob MIT, dados no Google Drive, formato PASCAL VOC. O conjunto anota a pistola; quem a segura só foi anotado depois, pelo CCTV-Gun.

- **Jose L. Salazar González, Carlos Zaccaro, Juan A. Álvarez-García, Luis M. Soria Morillo, Fernando Sancho Caparrini (2020)**. Real-time gun detection in CCTV: An open problem. Neural Networks, 132, 297-308. DOI: 10.1016/j.neunet.2020.09.013. Crossref: sim; aberta pelo agente: sim.
  O que diz: Libera dois conjuntos (CC BY-NC 4.0, no Hugging Face). O Mock Attack são gravações reais de três câmeras de vigilância (dois corredores e uma entrada) durante um ataque simulado numa universidade, anotadas à mão. O outro é sintético, em Unity, com personagens e 11 objetos: 4 tipos de pistola, 5 de fuzil, faca e smartphone, este último como objeto confundível. Real e sintético, CCTV, não aéreo. É precedente de dado sintético de motor de jogo para detecção de arma.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 5 autores, Neural Networks 132, 297-308, 2020. A página do conjunto confirma: Mock Attack gravado por três câmeras de vigilância (dois corredores e uma entrada) e anotado à mão; parte sintética em Unity com 11 objetos (4 pistolas, 5 fuzis, faca e smartphone); CC BY-NC 4.0, no Hugging Face. O trecho existe. A página não chama o smartphone de objeto confundível: isso é inferência do resumo, plausível. Hnoohom et al. (2022) e Faheem et al. (2025) chamam o Mock Attack de 'public benchmark dataset'.

- **Jesus Ruiz-Santaquiteria, Juan D. Muñoz, Francisco J. Maigler, Oscar Deniz, Gloria Bueno (2024)**. Firearm-related action recognition and object detection dataset for video surveillance systems. Data in Brief, 52, 110030. DOI: 10.1016/j.dib.2024.110030. Crossref: sim; aberta pelo agente: sim.
  O que diz: Artigo de dados com conjunto público (Mendeley Data, DOI 10.17632/bbzpxhd22j.2, CC BY-NC 3.0). São 398 vídeos de uma pessoa fazendo ações, com caixas COCO das classes Handgun, Machine_Gun e No_Gun e ações positivas de portar (carry) e apontar (aim). Câmera IP ou smartphone, em cinco posições na Universidade de Castilla-La Mancha; a altura da câmera não é informada. Real, vigilância, arma portada anotada.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 5 autores, Data in Brief 52, 110030, 2024. No PMC: 398 vídeos, anotação COCO, classes Handgun, Machine_Gun e No_Gun, ações Carry e Aim, câmera IP (C1) ou de smartphone (C2), cinco posições na UCLM. A altura da câmera não é informada. O trecho existe. O DataCite do conjunto (10.17632/bbzpxhd22j.2) confirma CC BY-NC 3.0.

- **Francisco Pérez-Hernández, Siham Tabik, Alberto Lamas, Roberto Olmos, Hamido Fujita, Francisco Herrera (2020)**. Object Detection Binary Classifiers methodology based on deep learning to identify small objects handled similarly: Application in video surveillance. Knowledge-Based Systems, 194, 105590. DOI: 10.1016/j.knosys.2020.105590. Crossref: sim; aberta pelo agente: sim.
  O que diz: Universidade de Granada. Cria o Sohas_weapon: seis objetos manuseados de modo parecido (pistola, faca, smartphone, cédula, carteira, cartão), fotografados com câmeras comuns e de vigilância, com 10% das imagens baixadas da internet, anotados para detecção. Distribuído pelo repositório ari-dasci/OD-WeaponDetection (licença não conferida). Ponto de vista de solo ou vigilância, com o objeto na mão. É precedente, em CCTV, do desenho de objeto confundível do artigo.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 6 autores, KBS 194, 105590, 2020. Os destaques na ScienceDirect confirmam os seis objetos (pistola, faca, smartphone, cédula, carteira e cartão), fotos de câmeras comuns e de vigilância, 10% das imagens tiradas da internet e anotação para detecção. O trecho existe. A licença, que a busca deixou em aberto, está no README do ari-dasci/OD-WeaponDetection: CC BY-SA 4.0 (os metadados do GitHub dizem CC-BY-4.0).

- **Roberto Olmos, Siham Tabik, Francisco Herrera (2018)**. Automatic handgun detection alarm in videos using deep learning. Neurocomputing, 275, 66-72. DOI: 10.1016/j.neucom.2017.05.012. Crossref: sim; aberta pelo agente: sim.
  O que diz: Universidade de Granada. Detector de pistola em vídeo, com base de treino nova (fontes não conferidas aqui) e teste em vídeos do YouTube de baixa qualidade. Ponto de vista de solo, não aéreo. Entra só como contraste de ponto de vista.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 3 autores, Neurocomputing 275, 66-72, 2018. O resumo contém o trecho sobre vídeos de baixa qualidade do YouTube. A introdução fala numa base própria de 3.000 imagens de armas em contextos variados. Ponto de vista de solo, útil só como contraste.

- **Yongxiang Gu, Xingbin Liao, Xiaolin Qin (2022)**. YouTube-GDD: A challenging gun detection dataset with rich contextual information. arXiv:2203.04129. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Preprint do arXiv, sem DOI no Crossref. 5.000 imagens de 343 vídeos do YouTube, com armas e pessoas anotadas; repositório sob Apache-2.0. Ponto de vista de vídeo de internet, não aéreo.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. A API do arXiv confere título, 3 autores e a data 08/03/2022. Não há DOI. O resumo traz 343 vídeos, 5.000 imagens e o trecho literal sobre 16.064 armas e 9.046 pessoas. O repositório UCAS-GYX/YouTube-GDD está sob Apache-2.0.

- **Yi-Ting Shen, Yaesop Lee, Heesung Kwon, Damon M. Conover, Shuvra S. Bhattacharyya, Nikolas Vale, Joshua D. Gray, G. Jeremy Leong, Kenneth Evensen, Frank Skirlo (2023)**. Archangel: A Hybrid UAV-Based Human Detection Benchmark With Position and Pose Metadata. IEEE Access, 11, 80958-80972. DOI: 10.1109/access.2023.3299235. Crossref: sim; aberta pelo agente: sim.
  O que diz: Benchmark de detecção de pessoa por drone com metadado de posição e pose. A parte real foi voada de 15 a 50 m; há uma parte com manequins e outra sintética de 5 a 80 m. Poses: em pé, agachado e deitado. O texto não menciona arma nem fuzil. Mostra que existe benchmark aéreo de pessoa nas altitudes do artigo, mas sem arma. Disponibilidade não conferida.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 10 autores, IEEE Access 11, 80958-80972, 2023. No PDF do arXiv: parte real voada de 15 a 50 m em passos de 5 m, com pessoas de roupa civil; manequins de 15 a 50 m; parte sintética de 5 a 80 m; poses em pé, ajoelhado e deitado. As únicas ocorrências de 'armed' falam em armar o drone. A disponibilidade, que a busca não conferiu, está no artigo: o conjunto fica em a2i2-archangel.vision, site do ARL que o declara aprovado para divulgação pública e exige login e aceite de termo.

- **Kien Nguyen, Feng Liu, Clinton Fookes, Sridha Sridharan, Xiaoming Liu, Arun Ross (2026)**. Person Recognition in Aerial Surveillance: A Decade Survey. IEEE Transactions on Biometrics, Behavior, and Identity Science, 8, 3-19. DOI: 10.1109/tbiom.2025.3617011. Crossref: sim; aberta pelo agente: sim.
  O que diz: Survey de dez anos sobre reconhecimento de pessoa em vigilância aérea, com tabela de conjuntos públicos de detecção de pessoa e suas altitudes (VisDrone de 30 a 100 m, UAV-Human de 2 a 8 m, entre outros). No texto integral da versão arXiv não aparece weapon, firearm, gun, rifle nem armed. É evidência indireta de que o campo não tem benchmark aéreo com arma anotada.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref: título, 6 autores, IEEE T-BIOM 8(1), 3-19, janeiro de 2026. No PDF do arXiv, a Tabela 1 põe o VisDrone entre 30 e 100 m e o UAV-Human entre 2 e 8 m. Nenhuma ocorrência de weapon, firearm, gun, rifle, pistol, handgun ou armed. É evidência indireta.

- **perfil 'hann_ah' no Kaggle (2026)**. Drone-Weapon-Detection-Showcase (Drone Weapon Detection Dataset Showcase 2026). Kaggle. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Vitrine no Kaggle (CC BY-NC-SA 4.0) de um conjunto aéreo híbrido com classes Person e Weapon. Mistura imagem aérea pública, quadros de helicóptero, cenas reais editadas por IA para inserir pessoa armada e cenas geradas inteiramente por IA. Só amostras e estatísticas estão publicadas; o conjunto completo não é distribuído. Sem altitude e sem revisão por pares.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Abri a página pelo navegador (o curl recebeu reCAPTCHA e não insisti). Perfil HANN_AH. Classes Person e Weapon; 5.220 imagens, com 1.040 anotações de arma. Fontes: imagem aérea pública, quadros de helicóptero, edição por IA (Gemini) e cenas geradas por IA. Licença CC BY-NC-SA 4.0, nenhuma altitude, e a frase 'The complete dataset is not publicly distributed.' está lá. Sem DOI e sem revisão por pares.

- **GOP (workspace do Roboflow Universe) (2024 (segundo o BibTeX da página))**. object_detetcion_v2 (Roboflow Universe, workspace GOP). Roboflow Universe. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Coleção de usuário, pública (CC BY 4.0), com 1.530 imagens e 14 classes: ações de pessoa ('armed', 'aiming', 'carrying_something', 'hands_up' e outras), veículo e animal. As miniaturas vistas no navegador são tomadas oblíquas de drone a baixa altura, com 'armed' na caixa da pessoa; não há classe própria de arma. Sem descrição, altitude, protocolo ou artigo: não é benchmark. Representa um tipo de coleção do Roboflow, onde a busca por 'armed' devolve 300 projetos, não inspecionados um a um.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. A página confere: 1.530 imagens, 14 classes (armed e aiming entre elas, nenhuma de arma), CC BY 4.0, sem descrição, BibTeX de 2024. As miniaturas mostram tomadas oblíquas de drone, aparentemente em baixa altura. Não é benchmark. Na busca do Roboflow achei outra coleção de usuário, com caixa de arma em imagem de drone (ver fontes esquecidas). Por isso o item 3 da busca só vale para conjuntos descritos em artigo.


### Fontes que a verificação acrescentou

- **Narit Hnoohom, Pitchaya Chotivatunyu, Anuchit Jitpattanakul (2022)**. ACF: An Armed CCTV Footage Dataset for Enhancing Weapon Detection. Sensors, 22(19), 7158. DOI: 10.3390/s22197158.
  CCTV encenado, com pedestres armados de pistola e de faca. Duas câmeras em suportes de 2,8 m, inclinadas cerca de 30 a 35 graus para baixo (câmera alta, não aérea). Usa ladrilhamento (tiling) contra a perda da arma pequena na redução da imagem, o mesmo argumento de escala da seção 7.6 do artigo. Chama o Mock Attack de 'public benchmark dataset', o que reforça que já existe benchmark público com arma portada. A declaração de disponibilidade aponta para github.com/iCUBE-Laboratory/The-Armed-CCTV-Footage, que hoje dá 404 pela API do GitHub.

- **Sudip Chakrabarty, Rajdeep Chatterjee, Sorup Chakraborty, Sourov Roy Shuvo, Rajesh Chowdhury (2025)**. KIIT-MiTA: High-Resolution Drone Imagery for Military Object Detection and Recognition (conjunto); artigo associado: Drones in Defense: Real-Time Vision-Based Military Target Surveillance and Tracking. Kaggle (conjunto); 2025 3rd International Conference on Intelligent Systems, Advanced Computing and Communication (ISACC), pp. 508-513 (artigo). DOI: 10.1109/ISACC65211.2025.10969335.
  Conjunto público no Kaggle, sob CC BY-NC 4.0 (uso comercial proibido). São 1.700 imagens de drone em 7 classes: Artillery, Missile, Radar, M. Rocket Launcher, Soldier, Tank e Vehicle. Tem classe soldado, nenhuma de arma, e a altitude não é informada, o que confirmei também no PDF de Shuvo et al. (arXiv 2605.21157), que usa o conjunto. É mais um conjunto aéreo que marca o papel militar da pessoa, não a arma portada. O artigo indicado na página confere no Crossref, mas não o abri.

- **Jungmok Ma, Oleg A. Yakimenko (2023)**. The concept of sUAS/DL-based system for detecting and classifying abandoned small firearms. Defence Technology, 30, 23-31. DOI: 10.1016/j.dt.2023.04.017.
  Drone pequeno com sensor eletro-óptico e YOLOv2 para localizar e classificar armas deixadas no chão, em estande de tiro ou campo de batalha: pistolas e fuzis parcialmente ocultos. A arma de fogo é anotada em imagem aérea, mas não está com ninguém. Li só o resumo: o PDF pediu CAPTCHA e parei ali. Altitude e disponibilidade dos dados ficaram sem conferência.

- **Lingren Kong, Jianzhong Wang, Peng Zhao (2022)**. YOLO-G: A Lightweight Network Model for Improving the Performance of Military Targets Detection. IEEE Access, 10, 55546-55564. DOI: 10.1109/ACCESS.2022.3177628.
  5.000 imagens de homens armados colhidas no Google e no Bing, com 10.157 caixas. As duas classes são de pessoa, definidas pela arma: Soldier_R (fuzil) e Soldier_RPG (lança-rojão). As fotos não são aéreas e o conjunto não é público; os autores dizem que não havia conjunto público utilizável. Serve de precedente para anotar a pessoa armada como classe de pessoa, que é o desenho do artigo. O Faheem et al. (2025) o cita.

- **Simuletic (2026)**. Synthetic Weapon Detection: Rifles vs. Umbrellas (CCTV). Hugging Face Datasets. DOI: sem DOI.
  Amostra pública e sintética da empresa Simuletic, publicada em 10/01/2026. Classes person, rifle e umbrella, metade fuzil e metade guarda-chuva, em vista alta de CCTV; a imagem de exemplo mostra o alto de um prédio, perto da pessoa. Tem cerca de 120 imagens (243 arquivos na pasta, contando os rótulos). É o mesmo desenho de objeto confundível do artigo, fuzil contra guarda-chuva, mas em CCTV. Não tem artigo nem revisão por pares, e a licença é inconsistente: os metadados dizem CC BY-NC 4.0 e o README diz CC BY 4.0. A mesma empresa publica outra amostra de CCTV, com person e weapon (Simuletic/cctv-weapon-dataset, CC BY 4.0, 2025). Serve para o autor saber que existe; não recomendo citar como referência acadêmica.

- **VisionTechDroneProject (workspace do Roboflow Universe) (2026 (segundo o BibTeX da página))**. Drone-Weapon-Our-drone (Roboflow Universe, workspace VisionTechDroneProject). Roboflow Universe. DOI: sem DOI.
  Coleção de usuário pública, sob CC BY 4.0, com 2.610 imagens e classes person, weapon e 'd'. As miniaturas são de drone, aparentemente em baixa altura. É o exemplo mais direto de imagem de drone com caixa de arma em acesso aberto. Não tem descrição, altitude, protocolo nem artigo, então não é benchmark. O mesmo workspace tem 'Drone-Weapon-Detection', com 258 imagens. É ela que obriga a dizer 'benchmark' na frase, e não 'dataset'.

- **Brandi Vincent (2026)**. Data from 'half a million hours of Ukraine conflict drone footage' now available to train AI. DefenseScoop. DOI: sem DOI.
  Notícia de 16/06/2026. A empresa Enabled Intelligence oferece mais de meio milhão de horas de vídeo de drone da guerra na Ucrânia, rotulado para detecção aérea, classificação de veículo e atividade em solo. O acesso é só de usuários aprovados nos EUA, na Ucrânia e em países da OTAN. Não é público nem benchmark, e a notícia não fala em rótulo de arma. Mostra que existe dado aéreo de combate rotulado em grande escala, mas restrito, o que conversa com o argumento do Sul Global no artigo.


### Lacunas declaradas pela busca

1) Roboflow Universe: a busca "armed" devolve 300 projetos de usuário e inspecionei poucos. Foram eles: GOP object_detetcion_v2 (drone oblíquo, rótulo "armed" na pessoa), MilitaryVehicleModel (fotos de solo) e o "tracking militar" da Escola Naval (vistas mistas, classe "soldier"). Não dá para excluir que alguma coleção de usuário tenha drone de 35 a 150 m com arma anotada. Nenhuma se apresenta como benchmark com protocolo, e por isso a redação proposta usa "benchmark" e "we found".

2) Dual-UAV: não baixei o samples.rar (2,9 GB), então não posso excluir que haja caixas dentro dele. A descrição do Zenodo e os dois repositórios de código indicam rótulo por nome de arquivo. Os artigos FUSION 2026 e LAFUSION 2025 não estão no Crossref e não foram conferidos.

3) Não conferidos: os termos de acesso do UAV-Human; a disponibilidade do AVI (o artigo não declara) e a do Archangel.

4) Repositórios:
- Papers with Code saiu do ar (redireciona para o Hugging Face Papers), então não consultei o índice de conjuntos dele.
- Na API de conjuntos do Hugging Face, nenhum nome combina arma com aéreo.
- No Kaggle só apareceu a vitrine citada.
- Não fiz busca em texto integral no IEEE Xplore, Scopus ou Google Scholar.
- ScienceDirect e Roboflow bloquearam o WebFetch (403 e 429). Li essas páginas pelo navegador embutido, só leitura, sem contornar verificação.

5) DOIs: os do Zenodo e do Mendeley são DataCite, conferidos em api.datacite.org (por isso crossref_conferido=false). G-MAD e YouTube-GDD só têm arXiv; não procurei o DOI da ACM para o G-MAD.

6) Não reconferi as classes do VisDrone. A frase da 06b, linha 136 ("The benchmark contains no carried firearms"), refere-se a ele e depende do script de conversão do próprio projeto.

7) Dados restritos de polícia ou defesa, como os do próprio projeto, ficam fora por definição; por isso a frase precisa dizer "public".

8) Ocorrências no manuscrito: a mesma frase está no Abstract (linha 20), na 7.7 (linhas 298 a 300) e na Conclusão (07-conclusion.md, linha 5). Há uma variante na 03b, linha 13. A introdução (linha 60) fica correta se ganhar "aerial".

9) Sugestão fora do pedido: citar Sohas e Dual-UAV como precedentes do objeto confundível na 7.4. O Dual-UAV é do Rio (CEFET-RJ e Instituto de Pesquisas da Marinha) e usa justamente guarda-chuva.

10) Nenhum arquivo do repositório foi editado. PDFs e JSON de apoio ficaram só no scratchpad.


## 2. "Clear weather" como convenção de voo

### Veredito da verificação

Veredito: reformular. A frase da 11.3 ('conventional preference for flying in clear weather') e o aposto da 8.4 e do fecho ('the illumination conventionally preferred for flying') juntam três práticas diferentes. Só uma delas tem convenção escrita de céu limpo, e ela é de aerolevantamento, não de 'voar' em geral.

(a) Especificações de aerolevantamento: aqui a frase se sustenta.
Essa tradição é tripulada e foi transposta para contratos de drone.
- NGS (2002): nenhuma nuvem nem sombra de nuvem; encoberto alto só se não reduzir a luz nem as sombras dos objetos; sol nunca abaixo de 30°, ideal de 40 a 60° pelas sombras intermediárias.
- RICS, norma vigente, 6ª edição (2021, reemitida em 2023): sol de pelo menos 15°, imagem substancialmente livre de nuvem e sombra densa.
- Boas práticas do NAIP (2007): excluem encoberto alto que reduza a iluminação e pedem sol de 30° ou mais.
- Anexo baiano de VANT: 45°.
Essas normas controlam a sombra pela elevação do sol, não evitando o sol direto.
- O hard sun do gerador (46 a 74°, disco de 0,6°, conferido em gen_morro.py) é essa condição.
- O low sun (9 a 25°) fica abaixo do mínimo de 30°.
- Os regimes cobertos violam a cláusula de nuvem.
O resultado contraria essa convenção: ela escolhe o pior regime do teste (0,675) e exclui o low sun (0,790).

(a') Mapeamento com drone. Aqui corrijo a busca, que dizia ser 'o contrário': a orientação está dividida por produto.
- Modelo 3D: o encoberto é preferível pela ausência de sombra escura, embora o sol dê bons resultados na maioria dos estudos (Maes, 2025, revisão). A Pix4D recomenda dia encoberto. Leitão et al. (2016), em área urbana, preferiram o encoberto, mas com um único voo nessa condição e efeito muito menor que o da altitude.
- Ortomosaico RGB: Maes recomenda sol ininterrupto, que permite obturador rápido e evita borrão.
- Multiespectral e térmica: sol.
- Fornecedor de sensores para drone: a GeoCue (2025) pede sol acima de 30°.
- Evidência sobre reconstrução: mista. Dandois (2015) teve céu limpo melhor em floresta; Slade (2025) achou efeito fraco e não significativo.
O achado estende à detecção uma preferência que a orientação já tem para reconstrução 3D, contraria a preferência por sol no ortomosaico e herda um custo: menos luz, logo obturador mais lento ou ganho maior. O teste por regime não mede isso.

(b) Polícia, SAR e ISR: a frase não se sustenta. Nenhum manual encontrado prefere sol.
- O POP 101.6.5 da PMSC (em Machado, 2025) pede só condição meteorológica favorável.
- SAR ocorre a qualquer hora e lugar (Broyles et al., 2022).
- O FM 34-81-1 (1992) restringe teto baixo; não confirmei se foi revogado.
- Não consegui ler doutrina recente (ATP): a busca web atingiu o limite de sessão.

(c) Regras de voo: aqui há erro de categoria. VMC é visibilidade e afastamento de nuvem, não sol.
- FAA 107.51.
- EASA AMC (2019).
- ANAC RBAC 100 (VLOS e EVLOS são operação em VMC; em vigor desde 16/06/2026, substitui o RBAC-E 94).
- DECEA ICA 100-40 (art. 27: sem precipitação, vento ou nevoeiro; em vigor desde 01/07/2026).
Encoberto com base alta cabe em todas elas; a chuva é vedada no Brasil. Fora do escopo: os 150 m de referência passam dos 120 m e, pela ICA 100-40 (art. 25), exigem segregação do espaço aéreo.

Detecção. Não há estudo em imagem real que isole sol duro contra encoberto para pessoas vistas do ar.
Indícios a favor, todos com confusão de variáveis:
- UAVDT: detecção pior de dia, mas rastreamento melhor de dia.
- DroneCrowd: o método proposto e os três melhores baselines erram mais em Sunny, mas as cenas diferem e a tarefa é contagem.
- Dare (2005): sombra de prédio obscurece informação em área urbana densa.
Contrapesos:
- Reilly et al. (2010): a sombra da própria pessoa serve de pista.
- Maes (2025): na detecção agrícola, sol, encoberto e variável não afetaram o desempenho de forma significativa.
O Okutama-Action, gravado num só local sob sol e nublado, é o candidato para um teste real.

Correções à busca:
1. O mapeamento com drone é dividido, não 'o contrário'.
2. Citar a RICS 6ª edição (2021), não a de 2010.
3. A ICA 100-40 revoga as Portarias 928, 929 e 930/2023; a 'MCA 56-5' não foi confirmada.
4. O HazyDet tem versão publicada (TGRS 2026).
5. Slade et al.: citar 2025, ano do fascículo.
6. O artigo usa o VisDrone e não o cita nas referências.
7. Bahia, Miller e DJI saem do texto.

As 27 fontes existem e os 17 DOIs Crossref batem. O de HazyDet é DataCite, e Liasis e Stavrou ficaram só no título. Processo: a busca anterior usou o e-mail do usuário no mailto do Crossref; eu não usei e-mail em nenhuma consulta. Nenhum arquivo do repositório foi alterado.

### Texto proposto, já revisado pela verificação

```text
SEÇÃO 8.4, terceira frase (substitui 'hard sun, the illumination conventionally preferred for flying,'):

At the scale at which this task operates, the target is a few tens of pixels of low-contrast texture; its silhouette in these corpora tracks camera pitch rather than scene content; and hard sun, which matches the cloud-free sky and minimum solar elevation that aerial survey specifications have conventionally required (National Geodetic Survey, 2002; RICS, 2021), is the regime with the second largest raw contrast and the second lowest point estimate once local clutter is accounted for.

SEÇÃO 11.3, o primeiro parágrafo vira os quatro abaixo (o parágrafo 'The implication was stated conditionally...' fica como está, logo depois deles):

Section 8.3 measures contrast against local clutter lower under hard sun and rain than under overcast, and proposes as the mechanism that the background under a hard sun is itself filled with cast shadow from rooftop objects. A detector evaluated per regime behaves as that mechanism predicts (Section 10.3). The practical implication is that, for detecting people over a roofscape of this kind, an overcast sky is preferable to hard sun, provided that the cloud base leaves the flight in visual meteorological conditions.

Which practice this runs against should be stated, because three are easily conflated. It runs against the specifications of aerial survey photography, which ask for imagery free of cloud and cloud shadow and set a minimum elevation for the sun. One of them admits a high, thin overcast only if it reduces neither the light nor the shadows of ground objects, and requires the sun never to be lower than 30 degrees and ideally between 40 and 60 degrees, because of the intermediate-size shadows produced (National Geodetic Survey, 2002); another asks for at least 15 degrees and warns that lower sun angles may produce deep shadows in urban areas (RICS, 2021). Both control shadow through the elevation of the sun, not by avoiding direct sunlight. Hard sun falls within what they ask for, and over this roofscape the shadow they tolerate, and in one case seek, is the clutter measured in Section 8.3.

Guidance for mapping with drones is divided, and the division follows the product. For three-dimensional reconstruction, a recent review of mapping practice finds overcast conditions preferable because dark shadows are absent, while noting that sunny conditions still give good results in most studies (Maes, 2025); a photogrammetry software vendor recommends an overcast day for its diffuse light and advises against direct sunlight because of the harsh shadows it creates (Pix4D, 2022; Pix4D, n.d.); and a drone survey of an urban area judged overcast preferable for its elevation models, although only one of its flights was overcast and the effect was much weaker than that of altitude (Leitão et al., 2016). For orthomosaics, by contrast, the same review recommends uninterrupted sun, which permits fast shutter speeds and so avoids motion blur (Maes, 2025), and at least one vendor of drone mapping sensors recommends a solar elevation above 30 degrees (GeoCue, 2025). The empirical record on reconstruction is itself mixed (Dandois et al., 2015; Slade et al., 2025). The measurement therefore extends to the detection of people a preference that part of this guidance already states for reconstruction, rather than overturning a settled practice; and it carries the cost that the other part names, since under a covered sky less light reaches the sensor and a slower shutter or a higher gain is needed, a trade-off that the per-regime test was not designed to measure.

Nor is the question one of flight rules. These set minima for visibility and for distance from cloud (14 C.F.R. § 107.51), define operation within visual line of sight as operation in visual meteorological conditions (ANAC, 2026), ask that the weather be verified as compatible with the manufacturer's manual (EASA, 2019), or prohibit operation under precipitation, wind or fog (DECEA, 2026). None of them asks for sunshine, and an overcast sky whose base lies well above the flight is compatible with all of them.

SEÇÃO 11.3, depois do parágrafo 'The implication was stated conditionally...':

Two qualifications follow. The favourable regime is overcast, not rain, and in Brazil operation under precipitation is excluded in any case (DECEA, 2026). And operations that answer to events rather than to a schedule, such as search and rescue, which can occur anywhere and at any time (Broyles et al., 2022), cannot choose their light; for them the finding bears on the robustness a detector needs, not on when to fly.

[Opcional, só depois de a seção 7.5 declarar a faixa de elevação solar de cada regime:] Low sun, the other regime lit directly by the sun, scores level with overcast, and its solar elevation lies below the minimum of the first specification and partly below that of the second. The survey convention therefore selects the weakest of the six regimes and excludes one of the strongest. The same result qualifies the mechanism of Section 8.3, since a low sun casts longer shadows than a high one.

FECHO, segundo parágrafo (substitui de 'and under the illumination condition conventionally preferred for flying' até 'cast shadow in the background.'):

...rather than by how faithfully the scene is built, and under hard sun, the cloud-free condition that aerial survey specifications have conventionally required (National Geodetic Survey, 2002; RICS, 2021), the figure shows among the lowest point estimates of contrast against local clutter of the six regimes, and a detector trained on all six finds it hardest to detect under that regime (Section 10.3). Section 8.3 attributes this, as a hypothesis, to cast shadow in the background, which is also the reason that guidance for three-dimensional reconstruction from drones gives for preferring an overcast sky (Section 11.3).

OPCIONAL, SEÇÃO 8.3 (depois de 'so a comparable difference is easier to find.'):

The mechanism agrees with what remote sensing reports for dense urban scenes, where shadow cast by buildings obscures much of the information in the image and can corrupt classification (Dare, 2005), and with a drone benchmark whose vehicle detectors performed worse in daylight than at night, which its authors attribute to more objects and a more cluttered background, having noted that daylight brings interference from shadows; its trackers, by contrast, performed better in daylight (Du et al., 2018). It has a counterpart that this statistic does not capture: under a direct sun a person also casts a shadow of their own, which detectors for aerial imagery have used as a cue (Reilly et al., 2010).

OPCIONAL, SEÇÃO 10.3 (depois do 'Check', antes de 'What would overturn the claim'):

No public aerial benchmark isolates this contrast on real imagery. VisDrone covers various weather and lighting conditions, but for detection it records occlusion and truncation for each box and no illumination label (Zhu et al., 2022). DroneCrowd labels its sequences as cloudy, sunny or night and, for its proposed method and its three strongest baselines, reports larger counting errors on sunny than on cloudy sequences, but across different scenes and crowd sizes, and for counting rather than detection (Wen et al., 2021). Okutama-Action was captured at a single site under sunny and cloudy conditions without results reported by condition (Barekatain et al., 2017), which makes it the nearest candidate for a real test that holds the scene constant. In agricultural detection from drones, a recent review reports that sunny, overcast and variable conditions did not significantly affect model performance (Maes, 2025). The per-regime result therefore has no counterpart on real imagery yet, and it may be specific to small targets over cluttered backgrounds.

REFERÊNCIAS A ACRESCENTAR (no formato de 08-references.md; Zhu et al. falta hoje embora o VisDrone seja usado no artigo todo):

Agência Nacional de Aviação Civil. (2026). *RBAC nº 100, Emenda nº 00: Requisitos gerais para aeronaves não tripuladas de uso civil* (Resolução nº 805, de 15 de junho de 2026). https://pergamum.anac.gov.br/pergamum/vinculos/RBAC100EMD00.pdf

Barekatain, M., Marti, M., Shih, H.-F., Murray, S., Nakayama, K., Matsuo, Y., & Prendinger, H. (2017). Okutama-Action: An aerial view video dataset for concurrent human action detection. *2017 IEEE Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, 2153-2160. https://doi.org/10.1109/CVPRW.2017.267

Broyles, D., Hayner, C. R., & Leung, K. (2022). WiSARD: A labeled visual and thermal image dataset for wilderness search and rescue. *2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, 9467-9474. https://doi.org/10.1109/IROS47612.2022.9981298

Dandois, J. P., Olano, M., & Ellis, E. C. (2015). Optimal altitude, overlap, and weather conditions for computer vision UAV estimates of forest structure. *Remote Sensing, 7*(10), 13895-13920. https://doi.org/10.3390/rs71013895

Dare, P. M. (2005). Shadow analysis in high-resolution satellite imagery of urban areas. *Photogrammetric Engineering & Remote Sensing, 71*(2), 169-177. https://doi.org/10.14358/PERS.71.2.169

Departamento de Controle do Espaço Aéreo. (2026). *ICA 100-40: Aeronaves não tripuladas e o acesso ao espaço aéreo brasileiro* (Portaria DECEA nº 2.094/DNOR8, de 18 de março de 2026). Comando da Aeronáutica. https://www.gov.br/defesa/pt-br/assuntos/aerolevantamento/arquivos/2026/ica-100-40-publicada-port-2094-dnor8-18-03-2026-bca-058-30-03-2026.pdf

Du, D., Qi, Y., Yu, H., Yang, Y., Duan, K., Li, G., Zhang, W., Huang, Q., & Tian, Q. (2018). The unmanned aerial vehicle benchmark: Object detection and tracking. In *Computer Vision, ECCV 2018* (Lecture Notes in Computer Science, pp. 375-391). Springer. https://doi.org/10.1007/978-3-030-01249-6_23

European Union Aviation Safety Agency. (2019). *Acceptable Means of Compliance (AMC) and Guidance Material (GM) to Part-UAS: UAS operations in the 'open' and 'specific' categories* (Issue 1, ED Decision 2019/021/R). https://www.easa.europa.eu/sites/default/files/dfu/AMC%20&%20GM%20to%20Part-UAS%20%E2%80%94%20Issue%201.pdf

GeoCue. (2025, November 27). *Flight planning: Sun angle*. GeoCue Support Knowledge Base. https://support.geocue.com/flight-planning-sun-angle/

Leitão, J. P., Moy de Vitry, M., Scheidegger, A., & Rieckermann, J. (2016). Assessing the quality of digital elevation models obtained from mini unmanned aerial vehicles for overland flow modelling in urban areas. *Hydrology and Earth System Sciences, 20*(4), 1637-1653. https://doi.org/10.5194/hess-20-1637-2016

Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot sensors. *Remote Sensing, 17*(4), 606. https://doi.org/10.3390/rs17040606

National Geodetic Survey. (2002). *General specifications for aeronautical surveys, Volume II: Airport aerial photography* (Version 14). National Oceanic and Atmospheric Administration. https://www.ngs.noaa.gov/AERO/GenSpecVol_II_v14.pdf

Operating limitations for small unmanned aircraft, 14 C.F.R. § 107.51. Retrieved 30 September 2026, from https://www.law.cornell.edu/cfr/text/14/107.51

Pix4D. (2022, April 20). *5 key things we wish we knew before flying a drone*. Pix4D Blog. https://www.pix4d.com/blog/tips-for-successful-drone-flights

Pix4D. (n.d.). *Best practices for image acquisition and photogrammetry*. PIX4D Documentation. Retrieved 30 September 2026, from https://support.pix4d.com/hc/best-practices-for-image-acquisition-and-photogrammetry

Reilly, V., Solmaz, B., & Shah, M. (2010). Geometric constraints for human detection in aerial imagery. In *Computer Vision, ECCV 2010* (Lecture Notes in Computer Science, pp. 252-265). Springer. https://doi.org/10.1007/978-3-642-15567-3_19

Royal Institution of Chartered Surveyors. (2021). *Earth observation and aerial surveys* (6th ed.; RICS professional standard, global, reissued January 2023). RICS. https://www.rics.org/content/dam/ricsglobal/documents/standards/Earth%20observation%20and%20aerial%20surveys_reissue%20Jan%202023.pdf

Slade, G., Anderson, K., Graham, H. A., & Cunliffe, A. M. (2025). Repeated drone photogrammetry surveys demonstrate that reconstructed canopy heights are sensitive to wind speed but relatively insensitive to illumination conditions. *International Journal of Remote Sensing, 46*(1), 24-41. https://doi.org/10.1080/01431161.2024.2377832

Wen, L., Du, D., Zhu, P., Hu, Q., Wang, Q., Bo, L., & Lyu, S. (2021). Detection, tracking, and counting meets drones in crowds: A benchmark. *2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 7808-7817. https://doi.org/10.1109/CVPR46437.2021.00772

Zhu, P., Wen, L., Du, D., Bian, X., Fan, H., Hu, Q., & Ling, H. (2022). Detection and tracking meet drones challenge. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 44*(11), 7380-7399. https://doi.org/10.1109/TPAMI.2021.3119563

Notas:
- Na primeira citação, escrever 'Royal Institution of Chartered Surveyors [RICS], 2021'.
- Slade et al. saiu online em 2024 e no fascículo em 2025; o APA usa o ano do fascículo.
- A URL da EASA contém um travessão codificado (%E2%80%94) que faz parte do endereço oficial; se a regra do travessão pesar, citar a decisão sem a URL.
```

### Fontes da busca, com a conferência

- **National Geodetic Survey (NOAA, National Ocean Service) (2002)**. General Specifications for Aeronautical Surveys, Volume II: Airport Aerial Photography (Version 14). NOAA National Geodetic Survey, especificação técnica. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Especificação de aerofotografia tripulada para levantamento aeronáutico. Item 6.1: nenhuma nuvem ou sombra de nuvem nas fotos; encoberto alto e fino só é tolerado se não reduzir a luz nem as sombras dos objetos, e filme pancromático P&B nunca sob céu totalmente encoberto. Itens 6.3 e 6.4: imagem bem definida, sem neblina, fumaça ou chuva, visibilidade de 10 milhas. Item 6.5: sol nunca abaixo de 30°, idealmente entre 40 e 60° 'because of the intermediate-size shadows produced'; remete ao Manual of Photogrammetry da ASPRS (4ª ed., seção 5.8.3). É a convenção 'céu limpo e sol alto' em forma de norma.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Abri o PDF da NGS. A capa confirma Version 14, de 22/07/2002 (NGS/NOS/NOAA). Os itens 6.1, 6.3, 6.4 e 6.5 dizem o que o resumo afirma: sem nuvem nem sombra de nuvem; encoberto alto e fino só se não reduzir a luz nem as sombras dos objetos; sol nunca abaixo de 30°, ideal de 40 a 60° pelas sombras de tamanho intermediário; remissão ao Manual of Photogrammetry, 4ª ed., seção 5.8.3. Ressalva: é especificação de aerofotografia de aeroporto com filme, e ali a sombra é desejada, porque serve para interpretar alturas. A norma controla a sombra pelo ângulo do sol, não a evita.

- **Royal Institution of Chartered Surveyors (RICS) (2010)**. Vertical aerial photography and digital imagery, 5th edition (Guidance Note GN 61/2010). RICS Practice Standards, UK. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Guia britânico para contratar aerofotografia vertical. Seção 3.4 (Flying conditions): altitude solar acima de 15°; a foto deve ser 'substantially free of cloud, dense shadow or smoke'; a temporada normal de voo, de abril a outubro, é escolhida por 'optimal lighting and weather conditions'; contratos podem exigir sol mínimo de 15 ou 20°, porque sol baixo gera sombras profundas em área urbana. Controle de qualidade: sombras de prédios não podem obscurecer detalhes. Foi substituído pela 6ª edição (2023, 'Earth observation and aerial surveys'); o rascunho de consulta dessa edição mantém sol acima de 15° e a mesma cláusula de nuvem e sombra.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. PDF aberto. A capa confirma 5ª edição, GN 61/2010. A seção 3.4 e o controle de qualidade dizem o que o resumo afirma. Correção à busca: a sucessora, 'Earth observation and aerial surveys' (6ª edição), é de setembro de 2021, vale desde 04/01/2022 e foi reemitida como professional standard em janeiro de 2023. A busca a datou de 2023 e só leu o rascunho. Conferi a versão final: mantém sol de pelo menos 15° e imagem substancialmente livre de nuvem e sombra densa, e acrescenta que levantamentos com VANT dependem menos do ângulo solar. No artigo, citar a 6ª edição (ver fontes esquecidas).

- **Pix4D (s.d. (consultado em 30/09/2026))**. Best practices for image acquisition and photogrammetry. Pix4D Support. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Guia do fabricante de software de fotogrametria, também para drone. A melhor luz é suave e constante, obtida com céu nublado, o que reduz sombras. Deve-se evitar sol direto, que cria sombras duras e superexposição e esconde detalhes. Redação conferida no HTML da página.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. HTML conferido. A página recomenda luz suave e constante, obtida com luz artificial ou céu nublado, e manda evitar sol direto por causa das sombras duras e da superexposição. Não tem data (copyright 2026) e trata de fotogrametria em geral, aérea e terrestre. É orientação de fabricante.

- **Pix4D (equipe de treinamento) (2022)**. 5 key things we wish we knew before flying a drone. Pix4D Blog, 20/04/2022. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: O suporte da Pix4D recomenda dia encoberto, pela luz difusa. Nuvem constante é o ideal, porque sombras que se movem durante o voo distorcem o processamento. Poucos drones voam na chuva sem dano. Redação conferida no HTML da página.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Post de 20/04/2022 no blog da Pix4D, escrito a partir da equipe de treinamento. Confirma que o suporte recomenda dia encoberto, pela luz difusa. Nuvem constante é o ideal, porque sombra que se move distorce o processamento. Cita também o risco de chuva para o drone.

- **Jarrod Miller (University of Delaware Cooperative Extension) (2025)**. Mapping With Drones: Optimal Times for Delaware. University of Delaware Cooperative Extension, fact sheet, março de 2025. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Ficha agronômica de extensão. A prática usual é evitar nuvem variável, voando em dias limpos ou encobertos. O ângulo solar também importa: sol baixo gera sombras longas. A recomendação comum é voar até duas horas do meio-dia solar. Não há preferência por sol duro.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Ficha de março de 2025, de Jarrod Miller, conferida. Nuance: ela registra que a discussão costuma focar em evitar nuvem variável, voando em dia limpo ou encoberto. A recomendação própria é voar a até duas horas do meio-dia solar, o que pressupõe sol, e o assunto é reflectância de cultivos. Não serve como apoio a céu encoberto. Retirei do texto proposto, onde entra Maes (2025), que é mais forte.

- **Aparajithan Sampath, Mahesh Shrestha, Michelle While, Victoria Mary Scholl (2023)**. Guidelines for calibration of uncrewed aircraft systems imagery (Open-File Report 2023-1033). U.S. Geological Survey, Open-File Report. DOI: 10.3133/ofr20231033. Crossref: sim; aberta pelo agente: sim.
  O que diz: Guia da USGS para calibração de imagens de UAS. Lista como vantagem do UAS poder voar em dia nublado quando a nuvem está acima da rota, o que não acontece com satélite. Observa que a iluminação varia durante o voo com o ângulo solar e pede registrar o tempo e a cobertura de nuvens. Não recomenda sol.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. No Crossref (10.3133/ofr20231033), título, os quatro autores e o ano de 2023 conferem. No texto completo: o UAS pode voar em dia nublado se a nuvem estiver acima da rota; a iluminação muda durante o voo com o ângulo solar; pede registrar tempo, cobertura de nuvens e estado do céu. Não recomenda sol.

- **DJI (2024)**. DJI Terra User Manual v4.2 (2024.07). DJI, manual do software de mapeamento. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Não recomenda condição de céu para a missão. Trata a luz forte como fonte de artefato: reflexo especular, brilho de um lado, sombra do outro e listras no mapa. Oferece a correção 'Light Uniformity' no processamento e presets de exposição Sunny, Cloudy e Low light.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. PDF de julho de 2024 conferido. Traz a função Light Uniformity (luz forte, reflexo especular, brilho de um lado e sombra do outro, listras no mapa) e os presets de exposição Sunny, Cloudy e Low light. Nuance: a Light Uniformity é descrita para cenas de campo (solo e dossel agrícola), não para área urbana. O manual não recomenda condição de céu. Peso fraco.

- **Jonathan P. Dandois, Marc Olano, Erle C. Ellis (2015)**. Optimal Altitude, Overlap, and Weather Conditions for Computer Vision UAV Estimates of Forest Structure. Remote Sensing 7(10):13895-13920. DOI: 10.3390/rs71013895. Crossref: sim; aberta pelo agente: sim.
  O que diz: UAV-SfM em floresta temperada, variando altitude, sobreposição e tempo. Depois de corrigido o alinhamento, não houve diferença significativa no erro de altura entre níveis de iluminação. As melhores estimativas saíram com 'clear lighting' e sobreposição alta. É contraponto: na reconstrução de dossel, o céu limpo não foi pior. Resumo lido no Crossref.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (Remote Sensing 7(10):13895-13920, 2015), e li o PDF no site do laboratório. A nuance reforça o contraponto. Nos dias limpos o erro de posicionamento absoluto foi quase a metade do dos dias nublados, e o contraste no dossel foi menor com nuvem. A densidade mediana de pontos não diferiu. Depois de corrigido o alinhamento, o erro de altura não diferiu entre níveis de iluminação.

- **Glenn Slade, Karen Anderson, Hugh A. Graham, Andrew M. Cunliffe (2024 (online; impresso em 2025))**. Repeated drone photogrammetry surveys demonstrate that reconstructed canopy heights are sensitive to wind speed but relatively insensitive to illumination conditions. International Journal of Remote Sensing 46(1):24-41. DOI: 10.1080/01431161.2024.2377832. Crossref: sim; aberta pelo agente: sim.
  O que diz: 61 levantamentos UAV-SfM no mesmo local ao longo de 24 dias. A altura do dossel é sensível ao vento e pouco sensível à elevação solar. Nuvem contra sol direto teve efeito fraco e não significativo; o sol, com sombras, reduziu a altura de forma marginal. Resumo lido no Semantic Scholar.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere, com saída online em 26/07/2024 e fascículo 46(1):24-41 em 2025. Li o resumo no Semantic Scholar: 61 levantamentos; efeito fraco e não significativo de nuvem contra sol direto; com sol, redução marginal da altura. Como o APA usa o ano do fascículo, a proposta cita 2025.

- **Mike R. James, Jim H. Chandler, Anette Eltner, Clive Fraser, Pauline E. Miller, Jon P. Mills, Tom Noble, Stuart Robson, Stuart N. Lane (2019)**. Guidelines on the use of structure-from-motion photogrammetry in geomorphic research. Earth Surface Processes and Landforms 44(10):2081-2084. DOI: 10.1002/esp.4637. Crossref: sim; aberta pelo agente: sim.
  O que diz: Diretrizes de SfM em geomorfologia. Não prescrevem iluminação; pedem que as condições de campo, inclusive tempo e iluminação, sejam documentadas. Lido na versão final submetida, depositada na UNIL.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (ESPL 44(10):2081-2084, 2019, nove autores). Li a versão aceita no repositório de Lancaster. O item 5 pede documentar as condições de campo, inclusive tempo e iluminação. O texto não prescreve iluminação.

- **Governo do Estado da Bahia (órgão provável: SIHS; não confirmado) (2024 (inferido do código da licitação; não confirmado))**. Anexo E-III: Cobertura aerofotogramétrica com a utilização de VANT (especificação técnica SIHS01). Portal Compras.BA, anexo de licitação 23001CE0032024. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Especificação brasileira para aerofotogrametria com VANT em projetos de saneamento. Para minimizar sombras, o voo deve ocorrer em horário com altura solar mínima de 45°, em condições atmosféricas e de visibilidade favoráveis, sem nuvens nem fumaça nas imagens. Mostra que a convenção do aerolevantamento tripulado foi transposta para contratos de drone no Brasil. É literatura cinzenta.
  Verificação: existe sim; metadados não; diz o que o resumo afirma sim. PDF aberto. O conteúdo confere: altura solar mínima de 45° para minimizar sombras, e nenhuma nuvem ou fumaça nas imagens. A data de criação do PDF, 29/10/2024, apoia o ano de 2024. O órgão (SIHS) só aparece no nome do arquivo e não foi confirmado. É literatura cinzenta e fica fora do texto. Serve ao veredito como indício de que a convenção de sol alto chegou aos contratos de drone no Brasil.

- **Federal Aviation Administration (EUA) (vigente (texto conferido na edição de 2018 do CFR e no LII em 30/09/2026))**. 14 CFR § 107.51 Operating limitations for small unmanned aircraft. Code of Federal Regulations, Title 14, Part 107. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Regra americana para drones pequenos: visibilidade mínima de 3 milhas terrestres a partir da estação de controle; o drone fica 500 pés abaixo e 2.000 pés na horizontal de nuvens; teto de 400 pés AGL. É mínimo de visibilidade e afastamento de nuvem, de tipo VMC, e não exige sol.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Conferido no LII. Exige visibilidade mínima de 3 milhas terrestres, distância mínima de 500 pés abaixo e 2.000 pés na horizontal de nuvem, e teto de 400 pés AGL. Não exige sol.

- **European Union Aviation Safety Agency (EASA) (2019)**. Acceptable Means of Compliance (AMC) and Guidance Material (GM) to Part-UAS, Issue 1 (Annex II to ED Decision 2019/021/R). EASA, ED Decision 2019/021/R. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Categoria aberta, AMC1 UAS.OPEN.060(1)(c): o piloto verifica se o tempo no início e durante toda a operação é compatível com o manual do fabricante, e deve conhecer as condições de luz. Não exige VMC nem sol; os limites são os do equipamento (vento, temperatura, visibilidade). Há revisões posteriores do AMC que não conferi.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. PDF aberto (Issue 1, 09/10/2019). O AMC1 UAS.OPEN.060(1)(c) confere: tempo compatível com o manual do fabricante; o piloto deve conhecer as condições de luz. O cabeçalho do PDF alterna entre 'Annex I' e 'Annex II', por isso convém citar só o número da decisão. Emendas posteriores não foram conferidas.

- **Agência Nacional de Aviação Civil (ANAC) (2026)**. RBAC nº 100, Emenda nº 00: Requisitos gerais para aeronaves não tripuladas de uso civil. ANAC, Resolução nº 805, de 15/06/2026 (DOU de 16/06/2026). DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Substitui integralmente o RBAC-E nº 94 e está em vigor desde a publicação (Resolução 805, art. 10). Item 100.3: define VLOS e EVLOS como operação em VMC. Item 100.25: só se inicia o voo com autonomia suficiente, considerando vento e demais condições meteorológicas. Não menciona sol nem céu encoberto.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. PDF da ANAC aberto. O item 100.3 define VLOS e EVLOS como operação em VMC, e o 100.25 trata de autonomia 'considerando vento e demais condições meteorológicas'. Não menciona sol nem nuvem. Li também a Resolução nº 805: o art. 1º traz a substituição integral do RBAC-E nº 94 e o art. 10 a vigência na publicação, DOU de 16/06/2026.

- **Agência Nacional de Aviação Civil (ANAC) (2026 (atualizado em 19/03/2026))**. Nevoeiro (Condições meteorológicas adversas para o voo). Portal gov.br/ANAC. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Reproduz a ICA 100-12 (Regras do Ar): o voo VFR exige visibilidade e distância de nuvens iguais ou superiores às especificadas, além de teto e visibilidade mínimos para pouso e decolagem. Mostra que VMC se define por visibilidade, nuvem e teto, não por sol.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. A página existe e reproduz a ICA 100-12, item 5.1.1 (VFR com mínimos de visibilidade e de distância de nuvens). Foi publicada em 20/11/2018 e atualizada em 19/03/2026. A URL informada redireciona para .../seguranca-operacional/biblioteca-safety/meteorologia-aeronautica/condicoes-meteorologicas-adversas-para-o-voo/nevoeiro.

- **Departamento de Controle do Espaço Aéreo (DECEA) (2026)**. ICA 100-40: Aeronaves Não Tripuladas e o Acesso ao Espaço Aéreo Brasileiro. Portaria DECEA nº 2.094/DNOR8, de 18/03/2026 (BCA nº 58, de 30/03/2026), em vigor desde 01/07/2026. DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Vale para todos os operadores de UA (art. 2º), inclusive órgãos de segurança pública, e revogou a MCA 56-5. Art. 27, nas regras gerais: não operar sob precipitação, vento, nevoeiro ou condição que ponha a operação em risco. Art. 73: o planejamento avalia informes e previsões meteorológicas. Art. 25: operação acima de 400 pés (120 m) AGL exige segregação do espaço aéreo. Não fala de sol nem de céu encoberto e não usa o termo VMC.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. PDF aberto: Portaria DECEA nº 2.094/DNOR8, de 18/03/2026, BCA nº 58 de 30/03/2026, em vigor desde 01/07/2026. Conferem o art. 2º (aplica-se a todos os envolvidos), o art. 27 (precipitação, vento, nevoeiro), o art. 73 (planejamento meteorológico) e o art. 25 (acima de 400 pés exige segregação). O texto não usa VMC nem fala de nuvem, sol ou visibilidade. Correção: a portaria revoga as Portarias DECEA 928, 929 e 930/DNOR8, de 2023, e não nomeia a 'MCA 56-5'. Essa parte do resumo não foi confirmada.

- **Juarez Saldanha Machado (2025)**. A utilização de aeronaves remotamente pilotas pela Polícia Militar do Paraná: estabelecimento de procedimento operacional padrão. Revista Ibero-Americana de Humanidades, Ciências e Educação (REASE) 11(10):5325-5343. DOI: 10.51891/rease.v11i10.21838. Crossref: sim; aberta pelo agente: sim.
  O que diz: Propõe um POP para a PMPR e reproduz o POP 101.6.5 da PM de Santa Catarina. O POP manda 'certificar-se de condição meteorológica favorável', lista como erro 'operar em condições meteorológicas adversas', e o checklist de mínimos pergunta pela meteorologia. Não menciona sol, sombra ou céu encoberto. É evidência de prática policial brasileira, mas o veículo é de baixo impacto.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (REASE 11(10):5325-5343, 2025, Machado). No PDF, o POP 101.6.5 da PMSC pede condição meteorológica favorável, lista como erro operar em condições adversas, e o checklist pergunta pela meteorologia. Não fala de sol, sombra ou nuvem.

- **Headquarters, Department of the Army (EUA) (1992)**. FM 34-81-1 Battlefield Weather Effects. U.S. Army Field Manual, 23/12/1992 (superado). DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Doutrina militar de efeitos do tempo, já superada. Apêndice I (inteligência): céu encoberto com base baixa reduz a eficácia de sistemas fotográficos e infravermelhos e pode restringir o uso de UAV; precipitação e baixa visibilidade degradam a coleta. Cobertura de nuvens e sombras do terreno afetam a luz disponível para sistemas eletro-ópticos. A restrição é de teto baixo, não preferência por sol.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Texto do archive.org conferido, com data de 23/12/1992. O manual diz que céu encoberto de base baixa reduz a eficácia dos sistemas fotográficos e infravermelhos e pode restringir o uso de UAV, e que nuvem e sombra do terreno afetam a luz disponível. Não confirmei que o manual tenha sido superado ou revogado; o resumo afirma isso sem fonte.

- **Daniel Broyles, Christopher R. Hayner, Karen Leung (2022)**. WiSARD: A Labeled Visual and Thermal Image Dataset for Wilderness Search and Rescue. IEEE/RSJ IROS 2022, p. 9467-9474. DOI: 10.1109/IROS47612.2022.9981298. Crossref: sim; aberta pelo agente: sim.
  O que diz: Conjunto visual e térmico para busca e salvamento, construído com socorristas. As operações de SAR ocorrem em qualquer lugar e a qualquer hora, por isso se pede robustez a tempo e luz. Lista folhagem e sombras como fonte de oclusão na detecção de pessoas por UAV; câmeras visuais falham com pouca luz. Lido na versão arXiv.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (IROS 2022, p. 9467-9474). No arXiv: as operações ocorrem em qualquer lugar e hora; a oclusão por folhagem e sombra é um desafio (C2); a câmera visual falha com pouca luz. Os autores trabalharam com socorristas.

- **Dawei Du, Yuankai Qi, Hongyang Yu, Yifan Yang, Kaiwen Duan, Guorong Li, Weigang Zhang, Qingming Huang, Qi Tian (2018)**. The Unmanned Aerial Vehicle Benchmark: Object Detection and Tracking. ECCV 2018, Lecture Notes in Computer Science, p. 375-391. DOI: 10.1007/978-3-030-01249-6_23. Crossref: sim; aberta pelo agente: sim.
  O que diz: Benchmark de detecção de veículos por drone, com atributo de condição (dia, noite, neblina). Registra que vídeos diurnos trazem interferência de sombras. Na avaliação por atributo, os detectores vão pior de dia do que à noite, e os autores atribuem isso a mais objetos e fundo mais poluído. Apoia o mecanismo de clutter, mas está confundido com a densidade de objetos e trata de veículos. Lido na versão arXiv (1804.00518).
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (ECCV 2018, LNCS, p. 375-391). Conferi o arXiv e a versão open access da CVF, com as mesmas frases: o daylight traz interferência de sombras, e a detecção é pior de dia que à noite, o que os autores atribuem a mais objetos e fundo mais poluído. Nuance omitida pela busca: no rastreamento (MOT), a maioria dos métodos vai melhor de dia.

- **Longyin Wen, Dawei Du, Pengfei Zhu, Qinghua Hu, Qilong Wang, Liefeng Bo, Siwei Lyu (2021)**. Detection, Tracking, and Counting Meets Drones in Crowds: A Benchmark. CVPR 2021, p. 7808-7817. DOI: 10.1109/CVPR46437.2021.00772. Crossref: sim; aberta pelo agente: sim.
  O que diz: Multidões vistas de drone, com atributo de iluminação Cloudy, Sunny ou Night (18.300, 12.300 e 3.000 quadros). Na Tabela 3 (contagem por mapa de densidade), os cinco métodos de menor erro global têm MAE maior em Sunny do que em Cloudy (STNNet 19,9 contra 14,1; CSRNet 19,1 contra 12,8; DM-Count 12,6 contra 11,4). Vários métodos mais fracos mostram o contrário. Os subconjuntos diferem em cena e densidade média, e a tarefa é contagem, não detecção. Lido na versão arXiv (2105.02440).
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (CVPR 2021, p. 7808-7817). A Tabela 3 é igual no arXiv e na CVF. STNNet tem MAE 14,1 em Cloudy e 19,9 em Sunny; CSRNet, 12,8 e 19,1; DM-Count, 11,4 e 12,6; CAN, 11,2 e 14,8. Vários métodos fracos mostram o contrário. Os quadros somam 18.300 em Cloudy e 12.300 em Sunny, com contagem média de 144,9 e 153,3. Os subconjuntos são vídeos diferentes.

- **Mohammadamin Barekatain, Miquel Marti, Hsueh-Fu Shih, Samuel Murray, Kotaro Nakayama, Yutaka Matsuo, Helmut Prendinger (2017)**. Okutama-Action: An Aerial View Video Dataset for Concurrent Human Action Detection. CVPR Workshops 2017, p. 2153-2160. DOI: 10.1109/CVPRW.2017.267. Crossref: sim; aberta pelo agente: sim.
  O que diz: Pessoas vistas de drone, gravadas em duas condições de luz (sol e nublado), sem resultado separado por condição. Mostra que o rótulo existe mas não é analisado. Lido na versão arXiv (1706.03038).
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (CVPRW 2017, p. 2153-2160). O arXiv confirma as duas condições de luz, sol e nublado, gravadas num único local, um campo de beisebol, e nenhum resultado por condição. Por ter um só local, é o melhor candidato a um teste real com a cena constante.

- **Pengfei Zhu, Longyin Wen, Dawei Du, Xiao Bian, Heng Fan, Qinghua Hu, Haibin Ling (2022)**. Detection and Tracking Meet Drones Challenge. IEEE Transactions on Pattern Analysis and Machine Intelligence 44(11):7380-7399. DOI: 10.1109/TPAMI.2021.3119563. Crossref: sim; aberta pelo agente: sim.
  O que diz: Artigo do VisDrone, o benchmark usado no artigo. O conjunto cobre várias condições de tempo e luz, mas na detecção só anota oclusão e truncamento por caixa; iluminação só aparece como atributo de sequência no rastreamento de objeto único. Sem novo rótulo, não dá para testar sol duro contra encoberto em imagem real. Lido na versão arXiv (2001.06303v3).
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (TPAMI 44(11):7380-7399, 2022). O arXiv v3 confirma que o conjunto cobre vários tempos e luzes e que, na detecção, só a oclusão e o truncamento são rotulados por caixa. 'Illumination variation' aparece como atributo de sequência no SOT. Atenção: o artigo usa o VisDrone em todo o texto, mas 08-references.md não traz Zhu et al. É preciso acrescentar.

- **Vladimir Reilly, Berkan Solmaz, Mubarak Shah (2010)**. Geometric Constraints for Human Detection in Aerial Imagery. ECCV 2010, Lecture Notes in Computer Science, p. 252-265. DOI: 10.1007/978-3-642-15567-3_19. Crossref: sim; aberta pelo agente: sim.
  O que diz: Detecta pessoas em imagem de UAV usando como pista a sombra projetada pela própria pessoa, com orientação e comprimento previstos pela posição do sol. Afirma que poucos pixels no alvo dificultam separar pessoa de clutter. É contrapeso ao mecanismo do artigo: o sol direto também dá à figura uma sombra discriminativa. Resumo lido no ML Anthology.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (ECCV 2010, p. 252-265). Li o PDF aberto na Springer. O método usa a sombra projetada pela pessoa, com orientação e relação altura-sombra, e observa que poucos pixels no alvo dificultam separar a pessoa do clutter. Nota adicional: as sombras atrapalham os métodos baseados em movimento.

- **Paul M. Dare (2005)**. Shadow Analysis in High-Resolution Satellite Imagery of Urban Areas. Photogrammetric Engineering & Remote Sensing 71(2):169-177. DOI: 10.14358/PERS.71.2.169. Crossref: sim; aberta pelo agente: sim.
  O que diz: Em imagem de alta resolução de áreas urbanas densas, sombras de prédios obscurecem boa parte da informação e podem corromper a classificação ou gerar erros de interpretação. Propõe detectar e remover a sombra. Apoia, em termos gerais, a ideia de sombra como fonte de erro em cena urbana densa. Resumo lido via OpenAlex.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Crossref confere (PE&RS 71(2):169-177, 2005). No resumo, pelo OpenAlex: a sombra de prédios em área urbana densa obscurece a informação e pode corromper a classificação; o artigo propõe detectar e remover sombra.

- **Changfeng Feng, Zhenyuan Chen, Xiang Li, Chunping Wang, Jian Yang, Ming-Ming Cheng, Yimian Dai, Qiang Fu (2024 (v2 de 2025))**. HazyDet: Open-Source Benchmark for Drone-View Object Detection with Depth-Cues in Hazy Scenes. arXiv:2409.19833 (sem versão publicada conferida). DOI: 10.48550/arXiv.2409.19833. Crossref: não; aberta pelo agente: sim.
  O que diz: Benchmark de detecção vista de drone sob névoa, com 383 mil instâncias reais e sintéticas. Afirma que detecção aérea sob condições atmosféricas adversas é pouco explorada, por falta de benchmark. Mostra que a pesquisa de robustez ao tempo em drone se concentra em névoa, noite e chuva, não em sol duro contra encoberto. O DOI é DataCite, não Crossref.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O arXiv confere (v1 de 30/09/2024, v2 de 26/05/2025, 383 mil instâncias, 'underexplored'). O DOI 10.48550 é DataCite e o Crossref devolve 404. Correção: há versão publicada, que a busca não achou, conferida no Crossref: IEEE TGRS 64 (2026), artigo 5006414, DOI 10.1109/TGRS.2026.3701819, com ordem de autores diferente. Não entra no texto.

- **Gregoris Liasis, Stavros Stavrou (2016)**. Satellite images analysis for shadow detection and building height estimation. ISPRS Journal of Photogrammetry and Remote Sensing 119:437-450. DOI: 10.1016/j.isprsjprs.2016.07.006. Crossref: sim; aberta pelo agente: não.
  O que diz: Só título e metadados (Crossref); o resumo não estava disponível e o texto não foi lido. Usa sombras para estimar a altura de edificações. Serve para uma ressalva: a tarefa morfológica da seção 6 (altura de edificação) pode se beneficiar da mesma sombra que atrapalha a detecção de pessoas.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma não. Os metadados conferem no Crossref (ISPRS J. 119:437-450, 2016). O resumo não está no OpenAlex nem no Semantic Scholar (só o TLDR sobre delinear sombras), e a ScienceDirect devolve 403. Que a altura venha da sombra é inferência do título; o conteúdo não foi conferido. Fica fora do texto.


### Fontes que a verificação acrescentou

- **Wouter H. Maes (2025)**. Practical Guidelines for Performing UAV Mapping Flights with Snapshot Sensors. Remote Sensing 17(4):606. DOI: 10.3390/rs17040606.
  Revisão com diretrizes para voos de mapeamento com VANT. Na iluminação, a preferência depende do produto. Para modelo 3D, o céu encoberto é preferível pela ausência de sombras escuras, embora o sol dê bons resultados na maioria dos estudos. Para ortomosaico RGB, o melhor é sol ininterrupto, pelo obturador rápido que evita borrão, com encoberto leve também adequado. Multiespectral e térmica pedem sol. Na hora do voo, o meio-dia solar é preferido; sol abaixo de 30° dá sombra excessiva. Em detecção agrícola por deep learning, sol, encoberto e variável não afetaram o desempenho de forma significativa, e a revisão recomenda variar as condições no treino. É a fonte que corrige a leitura da busca, de que a orientação de drone seria o contrário da frase.

- **João P. Leitão, Matthew Moy de Vitry, Andreas Scheidegger, Jörg Rieckermann (2016)**. Assessing the quality of digital elevation models obtained from mini unmanned aerial vehicles for overland flow modelling in urban areas. Hydrology and Earth System Sciences 20(4):1637-1653. DOI: 10.5194/hess-20-1637-2016.
  DEMs de VANT em área urbana. O encoberto foi preferível, provavelmente por iluminação mais uniforme e ausência de sombras duras e móveis, mas pesou bem menos que a altitude. Ressalvas dos próprios autores: só um voo foi feito sob céu encoberto, e numa métrica quantitativa (elevação do terreno) o erro foi maior no encoberto. É o único estudo urbano achado sobre o tema, e com evidência fraca.

- **Royal Institution of Chartered Surveyors (RICS) (2021 (reemitida em janeiro de 2023))**. Earth observation and aerial surveys (RICS professional standard, global, 6th edition). RICS, 6ª edição, setembro de 2021, em vigor desde 04/01/2022. DOI: sem DOI.
  Sucessora da GN 61/2010 e versão a citar no lugar dela. Recomenda sol de pelo menos 15°; abaixo disso pode haver sombra profunda, sobretudo em área urbana. A fotografia deve ser substancialmente livre de nuvem, sombra densa e fumaça. Observa que os levantamentos com VANT dependem menos do ângulo solar.

- **ITT Space Systems, LLC, para o USDA Farm Service Agency, Aerial Photography Field Office (2007)**. Aerial Photography Field Office, National Agriculture Imagery Program (NAIP) Suggested Best Practices, Final Report (CDRL A006). USDA FSA APFO, relatório de 01/02/2007. DOI: sem DOI.
  Boas práticas para o programa federal de ortoimagem agrícola dos EUA. Imagem só com o solo livre de nuvem, sombra de nuvem e encoberto alto que reduza a iluminação. Sol de 30° ou mais, com 40 a 60° preferidos, apresentado como forma de eliminar sombras; janela das 10h às 14h. Reforça que a convenção de aerolevantamento exclui o encoberto e controla a sombra pela altura do sol. É de 2007, não foi usada no texto e fica como apoio opcional.

- **GeoCue Support (2025)**. Flight Planning: Sun Angle. GeoCue Support Knowledge Base, 27/11/2025. DOI: sem DOI.
  Orientação de fornecedor de sensores de mapeamento para drone (TrueView). Pede sol acima de 30°, tolera até 20° e manda evitar menos de 15°. O sol alto dá luz uniforme e reduz artefatos de sombra, e a nuvem reduz a iluminação. Mostra que a regra do ângulo solar da tradição tripulada persiste no mapeamento com drone.

- **Agisoft LLC (2026)**. Agisoft Metashape User Manual, Professional Edition, Version 2.3. Manual do software de fotogrametria. DOI: sem DOI.
  Nos requisitos de objeto e cena: se não der para evitar objetos brilhantes, esperar um dia nublado. O sol direto cria manchas de luz que se movem durante a captura e atrapalham a reconstrução. É orientação de fabricante, restrita a superfícies brilhantes, e só dá apoio lateral à preferência por encoberto na reconstrução.

- **Agência Nacional de Aviação Civil (ANAC) (2026)**. Resolução nº 805, de 15 de junho de 2026 (aprova o RBAC nº 100). DOU de 16/06/2026, Seção 1, p. 85-90. DOI: sem DOI.
  Aprova o RBAC nº 100 em substituição integral ao RBAC-E nº 94 (art. 1º) e entra em vigor na publicação (art. 10). Confirma a vigência do regulamento citado na 11.3.


### Lacunas declaradas pela busca

1) Doutrina recente de polícia e ISR. Não abri o ATP 3-04.64 (UAS do Exército dos EUA), o ATP 2-01.3, nem manuais de SAR como IAMSAR e NASAR. Os sites militares e o da FAA devolveram 403 ou um desafio antirrobô, que não tentei contornar. A única doutrina militar lida, o FM 34-81-1, é de 1992 e está superada. Não achei manual policial, brasileiro ou estrangeiro, que fale de sol ou de sombra; o de Albuquerque (SOP 2-15) recusou a conexão.

2) Normas vigentes de aerolevantamento.
- A NGS (2002) remete ao Manual of Photogrammetry da ASPRS (4ª ed., seção 5.8.3), que não abri.
- A FAA AC 150/5300-17C (2011), sucessora dessa linha para aeroportos, deu 403. A especificação NAIP do USDA não abriu (timeout).
- A RICS 2010 foi substituída pela 6ª edição (2023, 'Earth observation and aerial surveys'). Só li o rascunho de consulta, que mantém sol acima de 15° e a cláusula de nuvem e sombra. Para citar a norma vigente, conferir a versão final.

3) Fontes não lidas por inteiro.
- O'Connor, Smith e James (2017), 'Cameras and settings for aerial surveys in the geosciences', Progress in Physical Geography 41(3):325-344, DOI 10.1177/0309133317703092: conferido no Crossref, mas o texto não abriu (servidor recusou). Não sei o que diz sobre iluminação, por isso ficou fora.
- MicaSense: página com 403.
- Burke et al. (2019), SAR térmico: só o resumo, sem nada sobre tempo.
- Liasis e Stavrou (2016): só os metadados.
- Várias fontes foram lidas na versão arXiv, e a versão publicada foi conferida só nos metadados: UAVDT, DroneCrowd, Okutama, VisDrone e WiSARD.

4) Especificação da Bahia. É anexo de licitação, literatura cinzenta. O órgão (provável SIHS) e o ano (2024) foram inferidos do nome do arquivo e não estão confirmados. Por isso ficou fora do texto proposto.

5) Detecção em imagem real. Não encontrei estudo que isole sol duro contra encoberto para pessoas vistas do ar; os indícios (UAVDT, DroneCrowd) estão confundidos com cena, densidade, tarefa ou classe. Um teste real possível: usar os rótulos Sunny e Cloudy do DroneCrowd, com a ressalva de cena, ou rotular a iluminação de parte do VisDrone test-dev.

6) Faixa de elevação solar. A faixa de cada regime não está no artigo. Pelo 03-blender/scripts/gen_morro.py: sol_duro de 46 a 74° com disco de 0,6°; sol_baixo de 9 a 25° com disco de 0,9°.
- Se a seção 7.5 declarar essas faixas, o texto pode dizer que o hard sun cai na faixa exigida e perto da 'ideal' da NGS (40 a 60°).
- Pode dizer também que o low sun, que empatou com o encoberto (0,790 contra 0,791), fica abaixo do mínimo da NGS (30°) e em parte abaixo do da RICS (15°). É a frase opcional marcada na 11.3.
- O empate do low sun também pesa sobre o mecanismo: um sol direto baixo, com sombra longa, não prejudicou. Há duas hipóteses a testar: com o sol alto, a sombra do fundo fica fragmentada; com o sol baixo, a sombra longa da própria pessoa ajuda, como em Reilly et al. (2010).

7) Tarefa morfológica. A proposta da seção 6 (altura de edificação) pode se beneficiar da sombra (Liasis e Stavrou, 2016). A preferência por céu encoberto não se transfere para ela sem teste próprio, o que é coerente com a 11.4.

8) Fora do escopo, mas ligado ao 'how to fly' da 11.3. A altitude de referência de 150 m passa dos 400 pés (120 m) acima dos quais a ICA 100-40/2026 (art. 25) exige segregação do espaço aéreo, e passa do teto de 400 pés da FAA (107.51).

9) Anos a acertar conforme o estilo do periódico. Slade et al. saiu online em 2024 e impresso em 2025 (v. 46, n. 1). O AMC da EASA citado é a Issue 1 (2019), e há revisões posteriores que não conferi. Verificar também se o VisDrone já é citado de outra forma na lista de referências.

10) Nota de processo. Em duas consultas à API do Crossref usei, indevidamente, o e-mail do usuário no parâmetro mailto. Não repeti nas consultas seguintes. Nenhum arquivo do repositório foi alterado; os arquivos temporários ficaram só no scratchpad.


## 3. Sintético que atrapalha

### Veredito da verificação

CONFERÊNCIA
As 17 fontes existem. Título, autores e ano batem na API do arXiv para as 16 que têm preprint (a exceção é McCormac 2017, conferido no PDF da CVF). Para as 14 com DOI, batem também no registro aberto em api.crossref.org/works/<DOI>. Nowruzi 2019, Li 2020 e G-MAD não têm DOI (a busca por título no Crossref não achou nada) e continuam fora do texto. Abri o texto de todas, nos PDFs do arXiv e da CVF, e conferi os números e trechos citados; em Mensink, Wang e Li, conferi o resumo e as seções de dados. O conteúdo confere em 16 fichas, com ressalvas. A ficha do SynPlay tem um erro material.

O QUE MUDA
1. Kiefer, Ott e Zell 2022: a omissão que mais pesa. A fig. 2 usa o mesmo desenho da 9.4 (YOLOv5m6 COCO, pré-treino sintético, depois real). Li os valores nos vetores do PDF e os calibrei contra as tabelas III e V. Com só 10 mil imagens sintéticas, o pré-treino ficou abaixo de não ter pré-treino sintético em todos os volumes reais do SeaDronesSee (cerca de 46,9 contra 48,6; 50,5 contra 54,6; 54,5 contra 55,8). No VisDrone, esse pré-treino só ajudou com 1 mil imagens reais; com 40 mil a 90 mil imagens, o ganho aparece. Logo, o precedente mais próximo não contradiz a 9.4 por inteiro: os 890 ladrilhos da 9.4 se comportam como o corpus pequeno deles.
Correções no texto da busca:
- Na 9.4 só o SINAL se inverte. Nos dois estudos, a magnitude do efeito encolhe quando o dado real cresce; 'o sinal e a tendência se invertem' está errado.
- Os autores chamam a tabela V de inconclusiva, então o 44,7 contra 43,9 sai da argumentação.
- A frase do ganho desproporcional vale para o VisDrone. No SeaDronesSee com 90 mil imagens, o ganho é maior no maior volume real.
- O menor volume real testado (1 mil) supera os 324 e 647 imagens da 9.4.
- No Cattle, o YOLO com pré-treino sintético ficou abaixo do só real (86,9 contra 88,8).

2. SynPlay (Yim et al. 2026). O modelo 'real' é treinado do zero, e o artigo declara isso. O Archangel e o SynDrone ficaram abaixo até do treino do zero. A tabela 3 (YOLOv8m, só pessoa, VisDrone completo) dá, em AP50: COCO+real 51,73 contra 49,52 do zero; SynPlay+real 52,13; COCO+SynPlay+real 53,01. Com um corpus grande e diverso (73.892 imagens), somar o sintético ao COCO ajudou. Isso cria um segundo conflito direto com a 9.4, então 'o único conflito direto é Kiefer' está errado. E reforça a mesma leitura: o corpus decide o sinal.

3. Treino misto.
- Archangel: o balanceamento reduziu muito o dano, mas não o eliminou. O dado real do ajuste é de manequins.
- Fonte independente nova (Martinez-Esteso et al. 2025, Alicante): sem lotes balanceados, o modelo pende para o conjunto mais numeroso, o sintético. Com 5% do real, somar sintético às vezes piorou os detectores de referência.
- Isso responde em parte à lacuna 'um só grupo'. Também casa com a 9.4, que junta 890 ladrilhos a 324 ou 647 imagens reais sem balanceamento declarado e cujo custo cai quando a parte real dobra.

4. Mecanismo.
- Hinterstoisser, Tremblay e Ljungqvist tratam de treino SÓ sintético, sem ajuste em real depois. Hinterstoisser, além disso, é detecção de instância de 10 objetos. O apoio à explicação candidata é indireto: 'consistente com', não 'apoio parcial'.
- No Ljungqvist o head parte do zero, então ligá-lo ao head COCO é inferência.
- O PTL chama de 'catastrophic forgetting' o esquecimento em sequência, na direção inversa à da 9.4.

5. Inferências que não devem aparecer como achado:
- He et al. comparam ImageNet contra inicialização aleatória.
- Mensink não diz que o COCO é favorecido.
- Li 2020 trata de classificação.
- Lee 2024 mede outra coisa, acha o sintético útil em todos os casos e não se opõe a Kiefer.

6. Cronograma. O ajuste positivo de Tremblay dividiu a taxa por dez. PTL e SynPlay usaram a mesma taxa nos dois estágios, como a 9.4. É observação, não causa demonstrada.

7. Confiabilidade. Shen et al. 2025 (tabela 1) e SynPlay (tabela 4) trazem os mesmos números com a terceira coluna rotulada de outro jeito (ICG num, Semantic Drone no outro). São do mesmo grupo.

FONTES ESQUECIDAS
- Martinez-Esteso et al. 2025.
- Lima et al. 2025: pré-treino sintético mais 10% do real superou o treino do zero. É mais um positivo medido contra o treino do zero; li só o resumo.
- Fabbri et al. 2021 (MOTSynth): pedestre em solo. Treinar no sintético superou o COCO, e a diversidade decidiu. Fica fora do texto por não ser aéreo.

SÍNTESE
A frase 'confirms' da seção 2 é forte demais: trocar por 'suggests' e acrescentar a ressalva. O fecho da seção ('It establishes...') pede o mesmo abrandamento.
A 9.4 não é anômala. Em detecção aérea, os dois estudos que comparam contra uma partida COCO só acham ganho com corpora de dezenas de milhares de imagens. Em Kiefer, o menor corpus deu perda.
Corpora de pouca variedade ficam abaixo até do treino do zero. A mistura pesa quando o sintético domina e o real é escasso.
O mecanismo candidato é consistente com a literatura, mas não está demonstrado. Tamanho e variedade do corpus são os primeiros suspeitos, mas nada os separa do domínio de imagem nem do cronograma não ajustado.
Nenhum arquivo do repositório foi alterado; os arquivos de trabalho ficaram no scratchpad.

### Texto proposto, já revisado pela verificação

```text
[Section 9.4: paragraph to close the discussion of the fine-tuning and joint-training results]

This result departs from the closest precedent only in part. Kiefer, Ott and Zell (2022) pretrained a COCO-initialised YOLO on up to 40,000 game-engine images generated to match VisDrone's traffic scenes and found the gain on VisDrone largest with the smallest real set. Their figure 2 also shows, however, that pretraining on only 10,000 synthetic images scored below no synthetic pretraining at every real-data size on their maritime benchmark, and gave no consistent gain on VisDrone beyond the smallest real set. Our corpus holds 890 tiles of six generated settlements. Negative transfer (Wang et al., 2019) recurs in aerial person detection. On the full VisDrone training split, pretraining on either of two public synthetic corpora scored below training from scratch at most detector sizes. A corpus designed for diverse human motion scored above it and, combined with COCO in pretraining, above COCO alone on the one detector size tested (Yim et al., 2026). Mixing synthetic with real images fell below the real-only baseline in low-shot VisDrone training (Shen et al., 2023b). It harmed the larger COCO-pretrained detectors most when real images were fewest, and much less once the two shares were balanced (Shen et al., 2023a). With unbalanced batches, it biased a drone detector of people at sea towards the more numerous synthetic images (Martinez-Esteso et al., 2025). These findings are consistent with our joint-training cost, which narrows as the real share grows. The candidate mechanism has only indirect support, from training on renders alone: retraining a feature extractor pretrained on real images degraded detection, whereas freezing it came close to training on real images (Hinterstoisser et al., 2019), although freezing hurt with highly randomised scenes (Tremblay et al., 2018). At these volumes the starting weights weigh most (He et al., 2019), and this design cannot tell which property of the corpus decides the sign: its size, its variety or its image domain, the factor that most determines positive transfer (Mensink et al., 2022).

[Section 2, paragraph 'Synthetic data and the sim-to-real gap': in the sentence beginning 'Together, this body of work', replace 'confirms' with 'suggests', and add after it:]

That benefit is conditional rather than general. Gains from synthetic pretraining have often been measured against ImageNet or random initialisation rather than against a detector already trained on real images of the target class (McCormac et al., 2017; Tremblay et al., 2018; Lima et al., 2025). In aerial person detection, both pretraining on some synthetic corpora and mixing synthetic with real images have scored below training on the real images alone (Shen et al., 2023a, 2023b; Yim et al., 2026; Martinez-Esteso et al., 2025).

[Optional, closing paragraph of Section 2: replace 'It establishes that domain-randomized synthesis transfers to aerial detection tasks' with:]

It suggests that domain-randomised synthesis can transfer to aerial detection tasks, under conditions of corpus size, variety and starting point that it does not settle

[References to add. Kiefer, Ott and Zell (2022) is already listed. Every DOI below was opened at api.crossref.org, and title, authors and year match.]

He, K., Girshick, R., & Dollár, P. (2019). Rethinking ImageNet pre-training. In 2019 IEEE/CVF International Conference on Computer Vision (ICCV) (pp. 4917-4926). https://doi.org/10.1109/ICCV.2019.00502

Hinterstoisser, S., Lepetit, V., Wohlhart, P., & Konolige, K. (2019). On pre-trained image features and synthetic images for deep learning. In Computer Vision, ECCV 2018 Workshops (Lecture Notes in Computer Science, pp. 682-697). Springer. https://doi.org/10.1007/978-3-030-11009-3_42

Lima, L., Andrade, F., Djenouri, Y., Pfeiffer, C., & Moura, M. (2025). Optimizing object detection for maritime search and rescue: Progressive fine-tuning of YOLOv9 with real and synthetic data. In Proceedings of the 17th International Conference on Agents and Artificial Intelligence (pp. 209-216). SCITEPRESS. https://doi.org/10.5220/0013112700003890

Martinez-Esteso, J. P., Castellanos, F. J., Rosello, A., Calvo-Zaragoza, J., & Gallego, A. J. (2025). On the use of synthetic data for body detection in maritime search and rescue operations. Engineering Applications of Artificial Intelligence, 139, 109586. https://doi.org/10.1016/j.engappai.2024.109586

McCormac, J., Handa, A., Leutenegger, S., & Davison, A. J. (2017). SceneNet RGB-D: Can 5M synthetic images beat generic ImageNet pre-training on indoor segmentation? In 2017 IEEE International Conference on Computer Vision (ICCV) (pp. 2697-2706). https://doi.org/10.1109/ICCV.2017.292

Mensink, T., Uijlings, J., Kuznetsova, A., Gygli, M., & Ferrari, V. (2022). Factors of influence for transfer learning across diverse appearance domains and task types. IEEE Transactions on Pattern Analysis and Machine Intelligence, 44(12), 9298-9314. https://doi.org/10.1109/TPAMI.2021.3129870

Shen, Y.-T., Lee, Y., Kwon, H., Conover, D. M., Bhattacharyya, S. S., Vale, N., Gray, J. D., Leong, G. J., Evensen, K., & Skirlo, F. (2023a). Archangel: A hybrid UAV-based human detection benchmark with position and pose metadata. IEEE Access, 11, 80958-80972. https://doi.org/10.1109/ACCESS.2023.3299235

Shen, Y.-T., Lee, H., Kwon, H., & Bhattacharyya, S. S. (2023b). Progressive transformation learning for leveraging virtual images in training. In 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (pp. 835-844). https://doi.org/10.1109/CVPR52729.2023.00087

Tremblay, J., Prakash, A., Acuna, D., Brophy, M., Jampani, V., Anil, C., To, T., Cameracci, E., Boochoon, S., & Birchfield, S. (2018). Training deep networks with synthetic data: Bridging the reality gap by domain randomization. In 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW). https://doi.org/10.1109/CVPRW.2018.00143

Wang, Z., Dai, Z., Póczos, B., & Carbonell, J. (2019). Characterizing and avoiding negative transfer. In 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) (pp. 11285-11294). https://doi.org/10.1109/CVPR.2019.01155

Yim, J., Lee, H., Eum, S., Shen, Y.-T., Zhang, Y., Kwon, H., & Bhattacharyya, S. S. (2026). SynPlay: Large-scale synthetic human data with real-world diversity for aerial-view perception. In 2026 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV) (pp. 938-947). https://doi.org/10.1109/WACV61042.2026.00098

[Notes: page numbers for Tremblay et al. are omitted because the Crossref record is malformed. The Crossref container title for Hinterstoisser et al. contains a dash, replaced here by a comma. The labels 2023a and 2023b follow the list's convention; strict APA 7 would distinguish the two works in the text by author names instead.]
```

### Fontes da busca, com a conferência

- **Kiefer, B.; Ott, D.; Zell, A. (2022)**. Leveraging Synthetic Data in Object Detection on Unmanned Aerial Vehicles. 2022 26th International Conference on Pattern Recognition (ICPR), pp. 3564-3571. DOI: 10.1109/ICPR56361.2022.9956710. Crossref: sim; aberta pelo agente: sim.
  O que diz: É o precedente mais próximo e o que mais contradiz a 9.4. Usa YOLOv5m6 com pesos COCO, o DGTA-VisDrone (até 40 mil imagens GTA V geradas para o cenário de tráfego do VisDrone) e 10 classes. O pré-treino sintético seguido de treino no real superou o só real nos três detectores (YOLO: 45,0 contra 43,9 mAP50 com o VisDrone completo). O ganho foi desproporcionalmente maior com conjuntos reais menores (fig. 2). Partindo de pesos aleatórios, o pré-treino sintético (44,7) ainda superou COCO seguido de real (43,9) (tabela V). Em experimentos preliminares não tabelados, pré-treinar foi melhor que o treino combinado. Diferenças para o artigo: volume, domínio da cena e número de classes.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Abri o registro do Crossref (10.1109/ICPR56361.2022.9956710): título, os três autores, ICPR 2022 e pp. 3564-3571 conferem. Li o PDF do arXiv 2112.12252. Conferem: YOLOv5m6 com pesos COCO; DGTA-VisDrone com 40 mil imagens de treino, com spawn ajustado à distribuição de classes do VisDrone; tabela III (YOLO 45,0 contra 43,9, e os três detectores ganham no VisDrone); a frase do ganho desproporcional; e os 'experimentos preliminares' contra o treino combinado. Ressalvas: (1) os autores chamam a tabela V de inconclusiva por efeitos pequenos, então a comparação 44,7 contra 43,9 não serve de evidência. (2) OMISSÃO IMPORTANTE, com o mesmo YOLO COCO e o mesmo desenho da 9.4. Valores lidos nos vetores da fig. 2 e calibrados contra as tabelas III e V: com só 10 mil imagens sintéticas, o pré-treino ficou abaixo de não ter pré-treino sintético em todos os volumes reais do SeaDronesSee (cerca de 46,9 contra 48,6; 50,5 contra 54,6; 54,5 contra 55,8). No VisDrone, esse pré-treino só ajudou com 1 mil imagens reais. (3) No SeaDronesSee, com 90 mil imagens, o ganho é maior no MAIOR volume real, então a frase dos autores vale para o VisDrone e não para os dois conjuntos. (4) O menor volume real testado (1 mil) supera os 324 e 647 imagens da 9.4. (5) No Cattle, o YOLO com pré-treino sintético ficou abaixo do só real (86,9 contra 88,8).

- **Shen, Y.-T.; Lee, H.; Kwon, H.; Bhattacharyya, S. S. (2023)**. Progressive Transformation Learning for Leveraging Virtual Images in Training. 2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 835-844. DOI: 10.1109/CVPR52729.2023.00087. Crossref: sim; aberta pelo agente: sim.
  O que diz: Usa RetinaNet com backbone ResNet50 pré-treinado no ImageNet, 20 ou 50 imagens reais do VisDrone e imagens virtuais do Archangel-Synthetic. Na tabela 1 (AP50/AP), a base só real fez 3,74/1,09 (20 imagens) e 6,42/1,86 (50). A mistura ingênua fez 3,41/1,02 e 5,18/1,65, abaixo da base. O pretrain-finetune fez 4,99/1,46 e 6,25/1,99: abaixo da base em AP50 com 50 imagens, acima em AP. Misturar imagens transformadas foi ainda pior. É transferência negativa por mistura em pessoa aérea, mas com base ImageNet, e a ordem pré-treino acima da mistura é a inversa da 9.4. Tabela lida na renderização ar5iv (a CVF deu 403).
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: CVPR 2023, pp. 835-844, e os quatro autores. Li direto o PDF do arXiv 2211.01778, não só a renderização ar5iv. A tabela 1 confere número a número (AP50/AP). Base só real: 3,74/1,09 e 6,42/1,86. Pretrain-finetune: 4,99/1,46 e 6,25/1,99. Mistura ingênua: 3,41/1,02 e 5,18/1,65. O virtual é o Archangel-Synthetic (17,3 mil imagens). O detector é RetinaNet com ResNet50 ImageNet, e a mesma taxa (0,001) foi usada nos dois estágios. O trecho confere; na frase completa lê-se 'in some cases'. Não observado pela busca: os autores atribuem o ganho marginal do pré-treino a 'catastrophic forgetting'. É esquecimento em sequência, mas na direção inversa à da explicação candidata da 9.4.

- **Shen, Y.-T.; Lee, Y.; Kwon, H.; Conover, D. M.; Bhattacharyya, S. S.; Vale, N.; Gray, J. D.; Leong, G. J.; Evensen, K.; Skirlo, F. (2023)**. Archangel: A Hybrid UAV-Based Human Detection Benchmark With Position and Pose Metadata. IEEE Access, 11, pp. 80958-80972. DOI: 10.1109/ACCESS.2023.3299235. Crossref: sim; aberta pelo agente: sim.
  O que diz: Usa YOLOv5 (n6, s6, m6) pré-treinado no COCO, com ajuste fino de 20 épocas e backbone congelado (freeze=10). O dado real são subconjuntos de manequins; o sintético, Unity (Arch-Syn-FT, 4,6 mil imagens, um personagem, um fundo). Misturar o sintético degradou significativamente os modelos maiores (s6, m6) nas poses em pé e ajoelhado, sobretudo com menos dado real. Os autores atribuem isso a um sintético simples demais, que causa sobreajuste. Balancear real e sintético reduziu muito ou eliminou o efeito: a proporção decide. O sintético ajudou na pose rara (deitado). Casa com o custo do treino misto da 9.4 diminuir quando a parte real dobra. Lido no PDF v1 e confirmado na renderização ar5iv da versão atual.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: IEEE Access 11, 80958-80972, 2023, e os dez autores. Li os PDFs do arXiv v1 e v3. Conferem: YOLOv5n6, s6 e m6 pré-treinados no COCO; 20 épocas com freeze=10; Arch-Syn-FT com 4,6 mil imagens, um personagem e um fundo; queda significativa em s6 e m6 nas poses em pé e ajoelhado, maior quando havia menos dado real; atribuição a sobreajuste; ganho na pose deitada; e o trecho literal. Ressalvas: (1) segundo o texto, o balanceamento 'largely decreases or even diminishes' o dano; 'eliminou' e 'quase eliminou' exageram, e o correto é 'reduziu muito'. (2) O dado real do ajuste é de manequins; a avaliação é em pessoas reais (Arch-Real-Eval).

- **Yim, J.; Lee, H.; Eum, S.; Shen, Y.-T.; Zhang, Y.; Kwon, H.; Bhattacharyya, S. S. (2026)**. SynPlay: Large-Scale Synthetic Human Data with Real-World Diversity for Aerial-View Perception. 2026 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), pp. 938-947. DOI: 10.1109/WACV61042.2026.00098. Crossref: sim; aberta pelo agente: sim.
  O que diz: Pessoa em vista aérea, YOLOv8 s/m/l, pré-treino no sintético e ajuste no treino completo do VisDrone; a inicialização não é declarada. AP50 no VisDrone: só real 47,43/49,52/51,10; Archangel+real 45,39/48,52/49,51, abaixo nos três tamanhos (também em AP); SynDrone+real 45,79/49,44/51,51, abaixo em s e m; SynPlay+real 49,31/52,12/52,93, acima nos três. É a evidência mais próxima da 9.4 (YOLO, VisDrone, pessoa) de que o sinal do pré-treino depende de como o corpus sintético foi construído.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma não. O registro do Crossref confere: WACV 2026, pp. 938-947, e os sete autores. Li o PDF do arXiv 2408.11814v2. Os números da tabela 1 conferem. ERRO MATERIAL: o resumo diz que a inicialização não é declarada, mas o artigo declara que o modelo 'real' é 'trained-from-scratch'. Portanto, o Archangel e o SynDrone ficaram abaixo do treino DO ZERO, e não de uma partida COCO. OMISSÃO: a tabela 3 (YOLOv8m, só pessoa, VisDrone com treino real completo) dá, em AP50: COCO+real 51,73; do zero 49,52; SynPlay+real 52,13; COCO+SynPlay+real 53,01. Somar ao COCO um corpus grande e desenhado para diversidade (73.892 imagens) superou o COCO sozinho: é um segundo conflito direto com a 9.4. Sem ajuste fino, o COCO (16,46) supera o SynPlay (9,12). O pré-treino e o ajuste usaram as mesmas épocas e a mesma taxa. Nota de confiabilidade: a tabela 4 traz os mesmos números da tabela 1 de Shen et al. 2025, mas a terceira coluna tem outro rótulo (Semantic Drone aqui, ICG lá).

- **Hinterstoisser, S.; Lepetit, V.; Wohlhart, P.; Konolige, K. (2019)**. On Pre-trained Image Features and Synthetic Images for Deep Learning. Computer Vision, ECCV 2018 Workshops (Lecture Notes in Computer Science), pp. 682-697. DOI: 10.1007/978-3-030-11009-3_42. Crossref: sim; aberta pelo agente: sim.
  O que diz: Detectores (Faster R-CNN, R-FCN, Mask R-CNN) treinados só com render OpenGL. Congelar o extrator de features pré-treinado em imagem real chega a até 95% do desempenho do treino real. Retreiná-lo no sintético vai mal, e descongelá-lo depois degrada. As features de pares real/sintético se afastam quando o extrator é ajustado no sintético. Apoia a explicação candidata da 9.4 (o estágio sintético sobrescreve o que foi aprendido em imagem real). O Crossref dá 2019 (anais dos workshops do ECCV 2018); o preprint é de 2017.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: LNCS, ECCV 2018 Workshops, pp. 682-697, 2019, e os quatro autores. Li o PDF do arXiv 1710.10710. Conferem: Faster R-CNN, R-FCN e Mask R-CNN treinados só com render OpenGL; com o extrator ImageNet congelado, chega-se a 'up to 95%' do treino real; retreinado no sintético, o extrator vai mal; descongelado depois de 1,2 milhão de passos, degrada; e as features de pares real/sintético se afastam quando o extrator é ajustado no sintético. Ressalvas: é detecção de instância de 10 objetos com modelo CAD, sem ajuste em real depois do sintético. O apoio à 9.4 é por analogia, e 'preserva' deve virar 'aproxima-se de'.

- **Tremblay, J.; Prakash, A.; Acuna, D.; Brophy, M.; Jampani, V.; Anil, C.; To, T.; Cameracci, E.; Boochoon, S.; Birchfield, S. (2018)**. Training Deep Networks with Synthetic Data: Bridging the Reality Gap by Domain Randomization. 2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW). DOI: 10.1109/CVPRW.2018.00143. Crossref: sim; aberta pelo agente: sim.
  O que diz: Domain randomization para carros no KITTI, com Faster R-CNN e extrator pré-treinado no ImageNet; a base só real também parte do ImageNet. Ajustar no real depois do DR supera o só real: com 6 mil imagens reais, AP 98,5, 2,1% acima. No ajuste, a taxa de aprendizado foi dividida por dez. Congelar os pesos do ImageNet piorou (até 13,5%), o contrário de Hinterstoisser, o que os autores atribuem à grande variedade do DR. Pesos COCO sozinhos dão 56,1 AP no KITTI; DR partindo do COCO, 83,7. Contradiz a 9.4 no sinal, mas com base ImageNet e sintético muito variado.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: CVPRW 2018 e os dez autores. As páginas estão malformadas ('1082-10828') e devem ser omitidas. Li o PDF do arXiv 1804.06516. Conferem: carros no KITTI; Faster R-CNN com extrator ImageNet; com 6 mil imagens reais, AP 98,5, 2,1% acima do só real; taxa dividida por dez no ajuste; congelar piorou 'as much as 13.5%'; COCO sozinho dá 56,1 e COCO+DR, 83,7. Ressalva: os 83,7 vêm sem nenhum ajuste em real, e o congelamento foi testado em treino só sintético.

- **He, K.; Girshick, R.; Dollár, P. (2019)**. Rethinking ImageNet Pre-Training. 2019 IEEE/CVF International Conference on Computer Vision (ICCV), pp. 4917-4926. DOI: 10.1109/ICCV.2019.00502. Crossref: sim; aberta pelo agente: sim.
  O que diz: O pré-treino no ImageNet acelera a convergência, mas não melhora necessariamente a acurácia final no COCO, exceto com pouco dado. Com 1 mil imagens, 9,9 contra 3,5 AP; com 3,5 mil, 16,0 contra 9,3. O ponto de quebra fica entre 3,5 mil e 10 mil imagens, e com pouco dado os hiperparâmetros precisam ser reescolhidos. Implica que, a 324 e 647 imagens, a inicialização domina, e que a diferença entre partidas tende a ser maior no menor volume e a encolher com mais dado, como na 9.4.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: ICCV 2019, pp. 4917-4926. Li o PDF do arXiv 1811.08883. Conferem: 9,9 contra 3,5 AP com 1 mil imagens; 16,0 contra 9,3 com 3,5 mil; ponto de quebra entre 3,5 mil e 10 mil; necessidade de reescolher hiperparâmetros com pouco dado; e o trecho. Ressalva: o artigo compara ImageNet contra inicialização aleatória. Dizer que a diferença entre DUAS partidas pré-treinadas encolhe com o volume é inferência.

- **McCormac, J.; Handa, A.; Leutenegger, S.; Davison, A. J. (2017)**. SceneNet RGB-D: Can 5M Synthetic Images Beat Generic ImageNet Pre-training on Indoor Segmentation?. 2017 IEEE International Conference on Computer Vision (ICCV), pp. 2697-2706. DOI: 10.1109/ICCV.2017.292. Crossref: sim; aberta pelo agente: sim.
  O que diz: Segmentação, não detecção. Pré-treinar em 5 milhões de imagens sintéticas RGB superou os pesos VGG-16 do ImageNet depois do ajuste em NYUv2 e SUN RGB-D. Mostra que vencer um pré-treino genérico real exigiu milhões de imagens sintéticas específicas da tarefa, e que a comparação foi contra ImageNet. Li só o resumo.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: ICCV 2017, pp. 2697-2706. Abri o PDF da CVF, além do resumo. Conferem: 5 milhões de imagens RGB sintéticas; U-Net em 13 classes; após o ajuste no NYUv2 e no SUN RGB-D, o pré-treino sintético supera os pesos VGG-16 ImageNet; e o trecho. É segmentação, não detecção, e a base é ImageNet, não COCO.

- **Mensink, T.; Uijlings, J.; Kuznetsova, A.; Gygli, M.; Ferrari, V. (2022)**. Factors of Influence for Transfer Learning Across Diverse Appearance Domains and Task Types. IEEE Transactions on Pattern Analysis and Machine Intelligence, 44(12), pp. 9298-9314. DOI: 10.1109/TPAMI.2021.3129870. Crossref: sim; aberta pelo agente: sim.
  O que diz: Mais de 2 mil experimentos de transferência, entre domínios (inclusive sintético e aéreo) e tarefas (inclusive detecção). O domínio de imagem é o fator mais importante para a transferência positiva, e a fonte deve incluir o domínio da imagem-alvo; os efeitos negativos são pequenos quando a fonte é mais ampla que o alvo. Explica por que uma partida COCO (foto real) pode vencer uma partida em render. Li só o resumo.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: TPAMI 44(12), 9298-9314, 2022. Li o resumo e a introdução no PDF do arXiv 2103.13318. As cinco conclusões e o trecho conferem. Ressalvas: na detecção, as bases são COCO, BDD, VOC e Underwater Trash, e o domínio aéreo só entra na segmentação. 'Favorece o COCO contra render' é inferência da busca: nem o COCO nem o corpus sintético são imagem aérea real. O que a fonte sustenta é que o domínio de imagem pesa mais e que uma fonte ampla traz pouco efeito negativo.

- **Wang, Z.; Dai, Z.; Póczos, B.; Carbonell, J. (2019)**. Characterizing and Avoiding Negative Transfer. 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 11285-11294. DOI: 10.1109/CVPR.2019.01155. Crossref: sim; aberta pelo agente: sim.
  O que diz: Define transferência negativa: o conhecimento de uma fonte menos relacionada pode piorar o desempenho no alvo. Propõe uma definição formal e um método para evitá-la. Serve para nomear o resultado da 9.4. Li só o resumo.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: CVPR 2019, pp. 11285-11294. Li o resumo e a seção de dados no PDF do arXiv 1811.09751. O trecho literal confere. Serve para nomear o fenômeno; os experimentos são de adaptação de domínio em classificação (Digits, Office-31, Office-Home, VisDA).

- **Lee, H.; Zhang, Y.; Kwon, H.; Bhattacharyya, S. S. (2024)**. Exploring the Potential of Synthetic Data to Replace Real Data. 2024 IEEE International Conference on Image Processing (ICIP), pp. 1005-1011. DOI: 10.1109/ICIP51287.2024.10647508. Crossref: sim; aberta pelo agente: sim.
  O que diz: Detecção de pessoa em UAV entre domínios: treino com 20 a 200 imagens do VisDrone mais Archangel-Synthetic (via PTL, RetinaNet) e teste em Okutama-Action, ICG, HERIDAL e SARD. O valor do sintético varia com o número de imagens reais e com o conjunto de teste, e a capacidade de substituir dado real cresce com mais imagens reais, tendência oposta à de Kiefer. Mostra que o efeito do volume real não é universal. O desenho, entre domínios, difere da 9.4.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: ICIP 2024, pp. 1005-1011, e os quatro autores. Li o PDF do arXiv 2408.14559. Conferem: treino entre domínios com 20, 50, 100 e 200 imagens do VisDrone mais Archangel-Synthetic via PTL (RetinaNet); teste no Okutama-Action, ICG, HERIDAL e SARD; e o trecho. Ressalvas: (1) a métrica é quantas imagens do mesmo domínio o treino entre domínios substitui, não o ganho sobre a base. Por isso 'tendência oposta à de Kiefer' não se sustenta. (2) O artigo diz que o sintético melhora 'in all cross-domain cases', o que a ficha omite. Não é caso de transferência negativa.

- **Shen, Y.-T.; Lee, H.; Kwon, H.; Bhattacharyya, S. S. (2025)**. Diversifying Human Pose In Synthetic Data For Aerial-View Human Detection. 2025 IEEE International Conference on Image Processing (ICIP), pp. 1648-1653. DOI: 10.1109/ICIP55913.2025.11084750. Crossref: sim; aberta pelo agente: sim.
  O que diz: RetinaNet (implementação do PTL), com 20 e 50 imagens do VisDrone. Com o Archangel-Synthetic original, o PT-FT ficou abaixo do só real no teste entre domínios Okutama-Action com 50 imagens (AP/AP50 5,32/20,96 contra 7,82/28,66). Nos demais casos o sintético ajudou, e diversificar as poses aumentou o ganho. Outra instância de transferência negativa condicionada ao corpus.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: ICIP 2025, pp. 1648-1653. Li o PDF do arXiv 2405.15939. Conferem: RetinaNet nas condições do PTL, com 20 e 50 imagens do VisDrone e média de três execuções; o pré-treino com o Archangel original ficou abaixo do só real no Okutama com 50 imagens (5,32/20,96 contra 7,82/28,66, AP/AP50); e o trecho. Nota: a tabela 4 do SynPlay repete esses números, mas rotula a terceira coluna como Semantic Drone, onde aqui está ICG. Os valores do Okutama batem nos dois artigos.

- **Rizzoli, G.; Barbato, F.; Caligiuri, M.; Zanuttigh, P. (2023)**. SynDrone - Multi-modal UAV Dataset for Urban Scenarios. 2023 IEEE/CVF International Conference on Computer Vision Workshops (ICCVW), pp. 2202-2212. DOI: 10.1109/ICCVW60793.2023.00235. Crossref: sim; aberta pelo agente: sim.
  O que diz: 72 mil imagens sintéticas (CARLA) a 20, 50 e 80 m. A detecção só é avaliada no próprio sintético (Faster R-CNN, RetinaNet, 8 classes com pedestres); o teste sintético-real é só de segmentação. Na segmentação, a generalização cai com a diferença de altitude entre treino e teste (treino a 20 m, teste a 80 m: 28,1% mIoU) e em cidades não vistas. Não testa pré-treino seguido de ajuste real em detecção. O teste de terceiros (Yim et al. 2026) achou o pré-treino no SynDrone abaixo do só real em dois de três tamanhos no VisDrone.

- **Ljungqvist, M. G.; Nordander, O.; Skans, M.; Mildner, A.; Liu, T.; Nugues, P. (2023)**. Object Detector Differences when Using Synthetic and Real Training Data. SN Computer Science, 4(3), 302. DOI: 10.1007/s42979-023-01704-5. Crossref: sim; aberta pelo agente: sim.
  O que diz: YOLOv3 com backbone ImageNet treinado em BDD (real) ou GTAV (sintético), com análise CKA por camada. As camadas iniciais ficam parecidas e a maior diferença está no head. Congelar ou não o backbone durante o treino sintético não mudou o mAP (cerca de 0,12 no BDD, contra 0,43 do treino real) nem a similaridade. Sugere que o estrago do treino sintético se concentra no head, a parte que o COCO treinou com pessoas reais, e relativiza a ideia de que congelar o backbone resolveria.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. O registro do Crossref confere: SN Computer Science 4(3), artigo 302, 2023, e os seis autores. Existe também uma versão do VISAPP 2022. Li o PDF do arXiv 2312.00694. Conferem: YOLOv3 com Darknet-53 ImageNet; BDD contra GTAV; cerca de 0,43 contra 0,12 de mAP no BDD; CKA mais baixa no head; nenhuma diferença entre congelar ou não; e o trecho. Ressalvas: o head parte de pesos aleatórios e não há ajuste em real depois do sintético. Ligar o resultado ao head COCO 'treinado com pessoas reais' é inferência.

- **Nowruzi, F. E.; Kapoor, P.; Kolhatkar, D.; Al Hassanat, F.; Laganiere, R.; Rebut, J. (2019)**. How much real data do we actually need: Analyzing object detection performance using synthetic and real data. ICML 2019 Workshop on AI for Autonomous Driving (arXiv:1907.07061). DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: SSD-MobileNet treinado do zero, classes carro e pessoa, vários sintéticos (entre eles P4B e Synscapes) com 2,5 a 10% do real. Ajustar no real um modelo treinado no sintético foi melhor que o treino misto com o mesmo volume real, e a diversidade pesou mais que o fotorrealismo. Como a base parte do zero, sem um detector real a preservar, isso explica por que a ordem difere da 9.4. Artigo de workshop, sem DOI; fica fora do texto proposto.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Não tem DOI: a busca por título no Crossref não achou nada. É workshop do ICML 2019, segundo o arXiv 1907.07061, cujo PDF li. Conferem: SSD-MobileNet treinado do zero; classes carro e pessoa; P4B, Synscapes (7D) e CARLA com 2,5% a 10% do real; o ajuste fino superou o treino misto; a diversidade pesou mais que o fotorrealismo; e o trecho literal da conclusão. Fica fora do texto.

- **Li, H.; Chaudhari, P.; Yang, H.; Lam, M.; Ravichandran, A.; Bhotika, R.; Soatto, S. (2020)**. Rethinking the Hyperparameters for Fine-tuning. ICLR 2020 (arXiv:2002.11770). DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Os hiperparâmetros ótimos de ajuste fino (sobretudo a taxa de aprendizado efetiva e o momento) dependem do conjunto e da similaridade entre os domínios fonte e alvo; regularizar em direção aos pesos pré-treinados não vale para domínios dissimilares. Relevante porque a 9.4 usa um cronograma único, não ajustado, para duas partidas com fontes diferentes. ICLR não emite DOI; fica fora do texto proposto.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Não tem DOI: o ICLR não emite e a busca por título no Crossref não achou nada. Li o resumo e a seção de dados no PDF do arXiv 2002.11770. O resumo e o trecho conferem. Ressalva: são sete conjuntos de classificação de imagem, não detecção. Fica fora do texto.

- **Kim, Y.; Park, J.; Yoon, D.; Jung, N.; Jeon, M. (2026)**. G-MAD: A Game-Based Data Generation Framework for Multi-View RGB-T Aerial Object Detection. arXiv:2607.19942 (ACM Multimedia 2026, segundo o arXiv). DOI: sem DOI. Crossref: não; aberta pelo agente: sim.
  O que diz: Arcabouço sobre ARMA 3 (dataset AMOD, alvos militares, RGB-T). O pré-treino no AMOD, feito depois de transferir o estilo para o domínio-alvo e transferindo só o backbone, superou a inicialização ImageNet no DIOR-R (63,14 para 69,83 mAP50) e no HIT-UAV térmico (74,57 para 77,08; pessoa 85,30 para 87,68). É mais um caso positivo medido contra ImageNet, não COCO. Preprint (aceito no ACM MM 2026, segundo o arXiv) sem DOI no Crossref; fica fora do texto proposto.
  Verificação: existe sim; metadados sim; diz o que o resumo afirma sim. Não tem DOI no Crossref: a busca por título não achou nada. O arXiv 2607.19942 (v3, 15/08/2026) indica o ACM Multimedia 2026. Li o PDF. Conferem: ARMA 3; AMOD; Oriented R-CNN com Swin-S partindo do ImageNet; só o backbone é transferido, depois de uma transferência de estilo para o domínio-alvo; DIOR-R de 63,14 para 69,83; HIT-UAV de 74,57 para 77,08; pessoa de 85,30 para 87,68. É um caso positivo medido contra ImageNet. Fica fora do texto.


### Fontes que a verificação acrescentou

- **Martinez-Esteso, J. P.; Castellanos, F. J.; Rosello, A.; Calvo-Zaragoza, J.; Gallego, A. J. (2025)**. On the use of synthetic data for body detection in maritime search and rescue operations. Engineering Applications of Artificial Intelligence, 139, 109586. DOI: 10.1016/j.engappai.2024.109586.
  Estudo de grupo independente (Universidade de Alicante) sobre detecção de pessoas no mar a partir de UAV. Usa o SeaDronesSee, com 5% a 100% do treino real, mais um corpus sintético em Unreal Engine 4 (SynBASe) e um YOLO modificado. Sem lotes balanceados, o modelo pende para o conjunto mais numeroso, o sintético, e aprende duas distribuições separadas (apêndice B, t-SNE): o resultado piora e o sintético fica subaproveitado, sobretudo com pouco dado real. Nos detectores de referência (YOLO, Faster R-CNN, U-Net), somar sintético a 5% do real não bastou e às vezes piorou. O sintético sem variação de clima deu ganho modesto e às vezes queda em domínios adversos. É evidência, fora do grupo ARL/Maryland, de que a mistura desbalanceada prejudica, o que casa com o treino misto da 9.4. Não achei declaração da inicialização dos pesos.

- **Lima, L.; Andrade, F.; Djenouri, Y.; Pfeiffer, C.; Moura, M. (2025)**. Optimizing Object Detection for Maritime Search and Rescue: Progressive Fine-Tuning of YOLOv9 with Real and Synthetic Data. Proceedings of the 17th International Conference on Agents and Artificial Intelligence (ICAART), pp. 209-216. DOI: 10.5220/0013112700003890.
  YOLOv9t em busca e salvamento marítimo por UAV, com dados reais e sintéticos (Unreal Engine 4). Um modelo pré-treinado no sintético e ajustado com 10% do real superou em 13,7% o modelo treinado só com dado real, e esse modelo só real parte do zero. O melhor resultado veio com 70% do real, não com 100%. É mais um resultado positivo em pessoa vista de UAV medido contra treino do zero, não contra um detector COCO; por isso entra na frase proposta para a seção 2. Li só o resumo, porque o PDF exige captcha; a métrica e a base dos 13,7% não estão definidas nele.

- **Fabbri, M.; Braso, G.; Maugeri, G.; Cetintas, O.; Gasparini, R.; Osep, A.; Calderara, S.; Leal-Taixe, L.; Cucchiara, R. (2021)**. MOTSynth: How Can Synthetic Data Help Pedestrian Detection and Tracking?. 2021 IEEE/CVF International Conference on Computer Vision (ICCV), pp. 10829-10839. DOI: 10.1109/ICCV48922.2021.01067.
  Pedestres em vídeo de vigilância (MOT17 e MOT20), não em imagem aérea. O corpus sintético, feito no GTA V, tem mais de 1,3 milhão de quadros e 40 milhões de instâncias. Treinar só nele superou treinar no COCO em quatro detectores, de +1,87 a +3,48 AP no MOT17. Com o número de imagens fixo, a amostra mais diversa igualou o COCO e a menos diversa ficou abaixo; o texto se contradiz ao dizer qual taxa de amostragem é a mais densa. Mostra que, para a classe pessoa, um corpus sintético grande e diverso pode superar o COCO, o que reforça tamanho e variedade como suspeitos na 9.4. Fica fora do texto proposto por não ser aéreo.


### Lacunas declaradas pela busca

1) Não achei estudo que reproduza exatamente o desenho da 9.4: COCO seguido de sintético e depois real, contra COCO seguido de real, com 5% e 10% do VisDrone, só pessoa, YOLO11. Os mais próximos são Kiefer 2022 (10 classes, até 40 mil imagens sintéticas, YOLOv5m6, sem resultado por classe) e Yim et al. 2026 (pessoa, YOLOv8, mas só com o treino real completo e sem declarar a inicialização nem o cronograma).

2) As evidências de transferência negativa em pessoa aérea vêm quase todas de um só grupo (DEVCOM ARL e Universidade de Maryland: Archangel, PTL, Lee 2024, SynPoseDiv, SynPlay), com datasets e código compartilhados. Não são replicações independentes.

3) Formas de leitura:
- PTL e a versão atual do Archangel foram lidos pela renderização ar5iv do arXiv: o PDF da CVF deu 403 e os PDFs do arXiv passam de 10 MB. O Archangel também foi lido no PDF do arXiv v1. Não abri as versões do IEEE Xplore.
- SynPlay foi lido no HTML do arXiv v2 (título igual ao do WACV).
- McCormac 2017, Mensink 2022 e Wang 2019: li só o resumo. Os DOIs estão conferidos.

4) Sem conferência no Crossref, e por isso fora do texto proposto:
- Nowruzi 2019 (workshop do ICML, sem DOI);
- Li 2020 (ICLR, sem DOI);
- G-MAD (arXiv, ACM MM 2026, DOI ainda não registrado).

5) Detalhes de referência:
- O registro Crossref de Tremblay 2018 traz a página '1082-10828', aparentemente malformada; omiti as páginas.
- Para Hinterstoisser, o Crossref dá 2019 (LNCS dos workshops do ECCV 2018). Troquei o traço do título do volume por vírgula por causa da regra do travessão, e não conferi os editores.
- Usei Shen et al. 2023a (Archangel) e 2023b (PTL). O APA 7 estrito pediria desambiguar pelos coautores; ajustar à convenção da lista.

6) Em Kiefer, a superioridade do pré-treino sobre o treino combinado vem de 'experimentos preliminares' não tabelados.

7) Vistos e descartados:
- PeopleSansPeople (arXiv 2112.09290): preprint, compara com ImageNet e não com COCO;
- Burdorf et al. 2022 (arXiv 2202.00632): sem registro no Crossref, trata de proporção de mistura em carros;
- MOTSynth (ICCV 2021): só resumo, DOI não conferido;
- Lee et al., arXiv 2405.15203: preprint;
- Varol et al. 2017, citado por Kiefer como precedente de pré-treino acima da mistura: não aberto.

8) A literatura não decide se congelar camadas ou baixar a taxa de aprendizado mudaria o sinal na 9.4. Hinterstoisser e Tremblay divergem, Ljungqvist não viu efeito do congelamento, e no Archangel o backbone estava congelado e ainda houve dano. É experimento em aberto, não afirmação.

9) Fora do escopo desta busca: Horváth et al. 2023, citado na seção 2, continua sem entrada (PENDENCIAS B1). As afirmações sobre Barisic 2022 e Horváth 2023 na seção 2 não foram reconferidas aqui.

10) Nenhum arquivo do repositório foi alterado. As extrações de texto ficaram só no scratchpad da sessão.


## 4. Referências B1

### Resumo do agente

Encontrei as 13 obras. Abri o registro de cada uma em api.crossref.org/works/<DOI>, e título, autores, ano e veículo conferem nas 13. As 13 também correspondem ao que a frase do manuscrito diz, mas em quatro o texto precisa de ajuste (ver abaixo). As 7 que a rodada de 20/09 deixou abertas foram identificadas sem ambiguidade graças à redação original da v2 do orientador (git show 0a0fcdb:01-artigo/manuscrito/01-introduction.md). Essa versão trazia detalhes que só uma obra tem: Denver e 6 anos de dados (Chen), RRT/ACO/A* com Bézier (Xu), título da seção 5.2 (Jiang), UPPF e PSO (Wang e Qian), rede tempo-espaço (Yan), 86%/97% (Horváth) e Mukuru (Watson e Elliott).

Das 13 candidatas de 01-artigo/candidatos_crossref.json, 9 estão erradas: Chen, Xu, Agrawal, Jiang, Wang, Yan, Gevaert, Horváth e Watson. Não reutilizar esse arquivo.

Erros nas entradas já inseridas em 08-references.md:
- Agrawal: a inicial é P. (Pooja), não K.
- Rasoulie: a inicial é F. (Fariborz), não M., e falta o número do artigo, 24356.
- da Silva et al.: o volume é 147, não 150. O Crossref registra o sobrenome como "Américo da Silva" e a segunda autora como I. F.
- Du et al.: as páginas são 13169-13187, não 14074-14090.
- Gevaert: há dois DOIs válidos. A página do editor exibe 10.5194/isprs-annals-III-3-317-2016.

Ajustes de conteúdo:
- Barisic: o objeto detectado é o próprio UAV.
- Horváth: são objetos industriais, a métrica é mAP50, e o manuscrito copia do resumo nove palavras seguidas sem aspas.
- Watson e Elliott: o Mukuru só é omitido no conjunto da Microsoft. O resumo diz "creates new opportunities", não "essential", e o manuscrito copia oito palavras seguidas.
- Gevaert: "substantially" exagera o resumo.

Formato das entradas: APA 7, com "Article" antes do número do artigo e hífen nos intervalos de página, como na lista atual (sem meia-risca nem travessão). O APA 7 também pede "et al." desde a primeira citação para 3 ou mais autores, e o manuscrito lista todos.

Limites:
- Agrawal: o resumo só foi visto por trechos de busca, porque ADS e ScienceDirect recusaram a leitura direta.
- Yan et al.: o ScienceDirect pediu verificação anti-robô, que não contornei. O resumo foi lido no IDEAS/RePEc.

Nada foi editado no repositório. Os arquivos temporários ficaram no scratchpad (cr.py, jiang.html, yan.html, wang.txt). O WebFetch salvou sozinho o PDF de Jiang et al. em C:\Users\marti\.claude\projects\C--projetos-machine-vision-favelas\ea433fd4-511a-436d-85fd-af6679b6d36c\tool-results\webfetch-1790779716051-kbacga.pdf.

### Item por item

- **Chen, Liu, Hu, Zhang e Pan (2025)**. Onde: 01-introduction.md, 2o parágrafo: 'patrol as optimisation over a street network (Chen, Liu, Hu, Zhang, & Pan, 2025)'. Na v2 (commit 0a0fcdb): modelo de patrulha por UAV policial calibrado com seis anos de dados de crime de Denver, com alocação de estações e rotas de patrulha.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.3390/drones9060449.
  Referência: Chen, Z., Liu, Y., Hu, S., Zhang, X., & Pan, Y. (2025). Deterring street crimes using aerial police: Data-driven joint station deployment and patrol path planning for policing UAVs. Drones, 9(6), Article 449. https://doi.org/10.3390/drones9060449
  Observação: No Crossref conferem o título, os cinco autores na ordem citada (Zuyu Chen, Yan Liu, Shengze Hu, Xin Zhang, Yan Pan), Drones 9(6) 449 e a data de 19/06/2025. O resumo depositado no Crossref descreve UAVs patrulhando ruas de alto risco para dissuadir crimes, com um módulo de planejamento de rota e outro de localização de estações, avaliados com uma base de crimes de 6 anos de Denver. Bate com a frase atual e com a descrição da v2. A candidata antiga (10.3390/rs18183179, detecção de pluma de gás) estava errada.

- **Rasoulie e Pashazadeh (2026)**. Onde: 01-introduction.md, 2o parágrafo: 'route planning over terrain with peaks and no-fly zones (Rasoulie & Pashazadeh, 2026)'. Na v2: algoritmo TAMOPSO para rota 3D de UAV, validado em terrenos sintéticos com picos, variação de altitude, obstáculos e zonas de exclusão aérea.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1038/s41598-026-42372-8.
  Referência: Rasoulie, F., & Pashazadeh, S. (2026). 3D UAV path optimization using a task-allocation and archive-guided mutation particle swarm optimization algorithm. Scientific Reports, 16(1), Article 24356. https://doi.org/10.1038/s41598-026-42372-8
  Observação: No Crossref: Fariborz Rasoulie e Saeid Pashazadeh, Scientific Reports 16(1), artigo 24356, 27/05/2026. Li o texto completo no Europe PMC (PMC13448216): TAMOPSO com waypoints 3D, avaliado em terrenos de referência com sete e dez picos, aglomerados de obstáculos e espaço aéreo restrito. Confere. ERRO na entrada atual de 08-references.md: a inicial 'M.' deve ser 'F.', e falta o número do artigo (24356).

- **Xu (2025)**. Onde: 01-introduction.md, 2o parágrafo: 'through gridded urban space with high-rise obstacles (Xu, 2025)'. Na v2: compara RRT, ACO e A*, com otimização por curva de Bézier, em ambiente urbano 3D em grade pensado para operações policiais, com prédios altos e obstáculos dinâmicos.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1371/journal.pone.0326633.
  Referência: Xu, G. (2025). A comparative study of drones path planning and bezier curve optimization based on multi-strategy search algorithm. PLOS One, 20(7), Article e0326633. https://doi.org/10.1371/journal.pone.0326633
  Observação: No Crossref: autor único Ganbin Xu, PLOS One 20(7), e0326633, 09/07/2025. O resumo depositado trata de planejamento de rota em ambiente urbano tridimensional em grade, com prédios altos e obstáculos dinâmicos, em operações de aplicação da lei, comparando RRT, ACO e A* com curva de Bézier. Coincide ponto por ponto com a v2. É a obra que a rodada de 20/09 não achou. A candidata de sensoriamento remoto (10.3390/rs17213581) era mesmo errada.

- **Agrawal, Ratnoo e Ghose (2017)**. Onde: 01-introduction.md, 2o parágrafo: 'along urban canyons by optical flow (Agrawal, Ratnoo, & Ghose, 2017)'. Na v2: câmera frontal única, comando de guinada inversamente proporcional à diferença de fluxo óptico entre os dois lados da imagem, cânions retos, em L e em T.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1016/j.ast.2017.05.012.
  Referência: Agrawal, P., Ratnoo, A., & Ghose, D. (2017). Inverse optical flow based guidance for UAV navigation through urban canyons. Aerospace Science and Technology, 68, 163-178. https://doi.org/10.1016/j.ast.2017.05.012
  Observação: No Crossref e no OpenAlex: Pooja Agrawal, Ashwini Ratnoo e Debasish Ghose, Aerospace Science and Technology 68, 163-178, 2017. O título já sustenta a frase atual. O resumo (câmera frontal única, comando inversamente proporcional à diferença de fluxo óptico, simulações em cânions retos, em L e em T) só foi visto em trechos de busca das páginas do ADS e do ScienceDirect, que recusaram a leitura direta (405 e 403). Bate com a v2. ERRO na entrada atual: a inicial 'K.' deve ser 'P.' (Pooja).

- **Jiang et al. (2026)**. Onde: 01-introduction.md, 2o parágrafo: 'with GNSS degradation in exactly those canyons documented as a reason to fuse visual sensing (Jiang et al., 2026)'. Na v2: revisão sobre posicionamento GNSS de UAV, com uma seção 'Urban Canyons and Low-Altitude Electromagnetically Complex Environments'.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.3390/drones10020091.
  Referência: Jiang, C., Zhou, X., Chen, H., & Liu, T. (2026). UAV positioning using GNSS: A review of the current status. Drones, 10(2), Article 91. https://doi.org/10.3390/drones10020091
  Observação: No Crossref: Chaopei Jiang, Xingyu Zhou, Hua Chen e Tianjun Liu, Drones 10(2), 91, 28/01/2026. Li o PDF do editor via WebFetch. A seção 5.2 tem exatamente o título citado na v2. Ela diz que prédios altos e ruas estreitas bloqueiam a linha de visada, geram multicaminho severo e reduzem a visibilidade de satélites, e que ali a navegação só por GNSS raramente basta, pedindo fusão GNSS/INS/visão (VO ou VIO). Confere com a frase atual e com a v2. A candidata antiga (preprint SSRN sobre YOLO) era errada.

- **Wang e Qian (2026)**. Onde: 01-introduction.md, 2o parágrafo: 'multi-target search as a travelling-salesman variant with no treatment of altitude or vertical obstacles (Wang & Qian, 2026)'. Na v2: UAV policial em ambiente urbano complexo, com o problema modelado (UPPF) como variante discreta do caixeiro-viajante e otimizado por PSO.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1038/s41598-026-40670-9.
  Referência: Wang, D., & Qian, X. (2026). Police UAV path planning method based on improved PSO using AFS and HJS. Scientific Reports, 16(1), Article 12417. https://doi.org/10.1038/s41598-026-40670-9
  Observação: No Crossref: Dongxing Wang e Xiaoxiao Qian, Scientific Reports 16(1), artigo 12417, 06/03/2026. Li o texto completo no Europe PMC (PMC13083867). A introdução diz que o UAV policial tem vantagem em ambiente urbano complexo e dificuldade para planejar a busca de múltiplos alvos. A UPPF devolve a distância total de uma ordem de visita aos alvos: é um problema discreto em que cada partícula é uma permutação. Não há ocorrência de altitude, obstáculo ou 3D no método. Confere. Duas ressalvas: o artigo não usa a expressão caixeiro-viajante (é leitura nossa, correta), e a UPPF é a função de aptidão, não o problema (PU3P), caso a redação da v2 volte.

- **Yan, Hsieh e Lai (2025)**. Onde: 01-introduction.md, 2o parágrafo: 'routing over patrol points to maximise coverage (Yan, Hsieh, & Lai, 2025)'. Na v2: modelo de roteirização e programação que integra UAVs e viaturas por rede tempo-espaço, com pontos de patrulha e maximização da cobertura de crimes.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1016/j.seps.2025.102334.
  Referência: Yan, S., Hsieh, T.-H., & Lai, Y.-C. (2025). Enhancing public safety through integrated UAV and police patrols. Socio-Economic Planning Sciences, 102, Article 102334. https://doi.org/10.1016/j.seps.2025.102334
  Observação: No Crossref: Shangyao Yan, Tsung-Hsun Hsieh e Yu-Chien Lai, Socio-Economic Planning Sciences 102, 102334, volume de dezembro de 2025 (online em setembro). O ScienceDirect exigiu verificação anti-robô, que não contornei. Li o resumo no IDEAS/RePEc: rede tempo-espaço, roteirização e programação de patrulha combinada de UAV e viatura, objetivo de maximizar a cobertura de crimes, dados de um departamento de polícia de Taiwan com pontos de patrulha. Confere com a frase atual e com a v2.

- **Gevaert, Persello, Sliuzas e Vosselman (2016)**. Onde: 01-introduction.md ('Gevaert, Persello, Sliuzas, and Vosselman (2016) in Kigali') e 02-literature-review.md: prédios densos e terreno íngreme desafiam os classificadores, e integrar atributos 2D radiométricos, 2.5D topográficos e 3D geométricos extraídos de UAV 'substantially improves classification accuracy'.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.5194/isprs-annals-III-3-317-2016.
  Referência: Gevaert, C. M., Persello, C., Sliuzas, R., & Vosselman, G. (2016). Classification of informal settlements through the integration of 2D and 3D features extracted from UAV data. ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, III-3, 317-324. https://doi.org/10.5194/isprs-annals-III-3-317-2016
  Observação: No Crossref conferem autores, título, 2016, III-3 e 317-324. O resumo no Crossref cobre assentamento não planejado em Kigali, prédios densos e terreno íngreme que dificultam identificar objetos elevados, e integração 2D, 2.5D e 3D que leva a acurácias maiores. Confere. Há dois DOIs registrados no Crossref para o mesmo artigo, e os dois resolvem: 10.5194/isprsannals-III-3-317-2016 (o da lista atual, que leva ao PDF antigo) e 10.5194/isprs-annals-III-3-317-2016 (o exibido na página do editor). Sugiro o segundo. O resumo diz só que a acurácia fica maior: trocar 'substantially improves' por 'improves' na 02. A candidata antiga (Rwanda Journal, 2017) era outra obra.

- **Du, Xing, Wang, Wei e Zhang (2024)**. Onde: 02-literature-review.md: 'proposed a scene-classification-assisted, texture-feature-enhanced multiscale network for large-scale informal-settlement extraction from remote sensing imagery'.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1109/JSTARS.2024.3432200.
  Referência: Du, S., Xing, J., Wang, S., Wei, L., & Zhang, Y. (2024). STMNet: Scene classification-assisted and texture feature-enhanced multiscale network for large-scale urban informal settlement extraction from remote sensing images. IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 17, 13169-13187. https://doi.org/10.1109/JSTARS.2024.3432200
  Observação: No Crossref e no OpenAlex conferem autores, título, 2024, volume 17 e páginas 13169-13187. O resumo (OpenAlex) confere com a frase: STMNet sobre imagem de alta resolução, testado num conjunto próprio e no UIS-Shenzhen. ERRO na entrada atual: as páginas '14074-14090' não existem em nenhuma das duas fontes; o correto é 13169-13187.

- **Barisic, Petric e Bogdan (2022)**. Onde: 02-literature-review.md: gerou um dataset aéreo sintético com randomização de textura e relatou ganhos de mAP 'for UAV object detectors evaluated on real imagery, particularly under difficult illumination and small-object conditions'.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1109/LRA.2022.3147337.
  Referência: Barisic, A., Petric, F., & Bogdan, S. (2022). Sim2Air: Synthetic aerial dataset for UAV monitoring. IEEE Robotics and Automation Letters, 7(2), 3757-3764. https://doi.org/10.1109/LRA.2022.3147337
  Observação: Crossref confere, e li o resumo no arXiv 2110.05145: dataset feito no Blender (a mesma ferramenta do nosso pipeline) com texturas randomizadas, voltado a iluminação difícil e a objetos pequenos no quadro, com ganho de mAP para YOLO e Faster R-CNN em dois conjuntos reais. Confere, com uma ressalva de conteúdo: o objeto detectado é o próprio UAV (imagens UAV-para-UAV), não pessoa nem edificação, e 'UAV object detectors' é ambíguo. Os ganhos vão de 1,1 a 20 pontos, então 'consistent' só vale para o sinal. Texto proposto: 'Barisic, Petric, and Bogdan (2022), publishing in IEEE Robotics and Automation Letters, rendered a synthetic aerial dataset in Blender with randomised object textures and reported mean-average-precision gains for detectors of UAVs, evaluated on two real test sets of UAV-to-UAV imagery; the conditions targeted were challenging illumination and objects that occupy a small part of the frame.'

- **Horváth, Erdős, Istenes, Horváth e Földi (2023)**. Onde: 02-literature-review.md: 'in IEEE Transactions on Robotics, demonstrated that a sim-to-real domain-randomization pipeline for object detection could shrink the reality gap to a satisfactory level, achieving mean-average-precision scores above 86% in zero-shot transfer and above 97% in one-shot transfer'.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1109/TRO.2022.3207619.
  Referência: Horváth, D., Erdős, G., Istenes, Z., Horváth, T., & Földi, S. (2023). Object detection using Sim2Real domain randomization for robotic applications. IEEE Transactions on Robotics, 39(2), 1225-1243. https://doi.org/10.1109/TRO.2022.3207619
  Observação: No Crossref: os cinco autores, T-RO 39(2), 1225-1243, abril de 2023. No resumo do arXiv 2208.04171: YOLOv4, objetos industriais, mAP50 de 86,32% zero-shot e 97,38% one-shot em 190 imagens reais anotadas. Os números da frase conferem. Três ressalvas: (a) não é tarefa aérea, e o parágrafo abre falando em transferência para tarefas aéreas; (b) a métrica é mAP50; (c) 'could shrink the reality gap to a satisfactory level' repete nove palavras seguidas do resumo, sem aspas. Texto proposto: 'In a related vein, though for industrial objects in a robotic setting rather than for aerial imagery, Horváth, Erdős, Istenes, Horváth, and Földi (2023), in IEEE Transactions on Robotics, trained a YOLOv4 detector on domain-randomised synthetic images and reported mAP50 of 86.32% in zero-shot and 97.38% in one-shot transfer, measured on 190 manually annotated real images.' A candidata de 20/09 (Kiefer et al., ICPR) era outra obra.

- **Watson e Elliott (2025)**. Onde: 02-literature-review.md: em Scientific Reports, 'used high-resolution digital elevation models and deep-learning-based height prediction' para Nairobi, Kathmandu e Quito, 'explicitly flagging the omission of Nairobi's Mukuru informal settlement from existing open building datasets', e dimensão vertical 'essential' para população e exposição a riscos.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1038/s41598-025-15929-2.
  Referência: Watson, C. S., & Elliott, J. R. (2025). Narrowing the gap for city building height predictions. Scientific Reports, 15(1), Article 29913. https://doi.org/10.1038/s41598-025-15929-2
  Observação: No Crossref: C. Scott Watson e John R. Elliott, Scientific Reports 15(1), 29913, 15/08/2025. O resumo e o texto completo (Europe PMC, PMC12354800) conferem: DEMs de 1,5 m, altura por deep learning, três cidades do Sul Global. É a obra certa, mas a frase pede duas correções. (a) O Mukuru só é omitido no conjunto da Microsoft (GMLBF); o Google Open Buildings o detecta e o OSM o mapeia em parte, então 'from existing open building datasets' generaliza demais. (b) O artigo diz que a dimensão vertical cria novas oportunidades, não que seja 'essential', e a oração do manuscrito repete oito palavras seguidas do resumo. Texto proposto: '... explicitly noting that Nairobi's Mukuru informal settlement is omitted from one of the open building-footprint datasets they compared and only partially mapped in OpenStreetMap, and arguing that building-scale height estimates open new possibilities for estimating population distribution and exposure to natural hazards.'

- **da Silva, Kormann da Silva e Westerholt (2024)**. Onde: 01-introduction.md: 'the mapping literature surveyed by da Silva, Kormann da Silva, and Westerholt (2024), all oriented to planning rather than to security'. 02-literature-review.md: 'the broader literature on digital mapping and community participation in informal areas'.
  Encontrado: sim; confere com a frase: sim; Crossref: sim; DOI: 10.1016/j.habitatint.2024.103040.
  Referência: Américo da Silva, A., Kormann da Silva, I. F., & Westerholt, R. (2024). Mapping the margins: A systematic scoping review of the impact of digital mapping on public participation in informal settlements. Habitat International, 147, Article 103040. https://doi.org/10.1016/j.habitatint.2024.103040
  Observação: No Crossref e no OpenAlex conferem título, 2024, Habitat International e artigo 103040. ERRO na entrada atual: o volume é 147, não 150. O Crossref registra o primeiro autor com sobrenome 'Américo da Silva' (prenome Alan) e a segunda autora como Iasmin Fernanda Kormann da Silva; a lista atual traz 'da Silva, A. A.' e 'I.'. Seguindo o registro do editor, a citação no texto passa a Américo da Silva et al. (2024), o que fica para o autor decidir. O resumo (OpenAlex) confere com as duas frases: revisão de escopo sobre mapeamento digital e participação em áreas informais do Sul Global, que achou pouca participação direta adicional dos moradores.


## 5. Fontes jornalísticas

### Resumo do agente

Consegui resolver os cinco itens com fontes abertas. Não alterei nada no repositório. As bases do ISP e do FBSP que o WebFetch salvou na pasta de resultados da sessão foram lidas com Python no scratchpad. Pela regra de direitos autorais, reproduzi um único trecho literal (InSight Crime, B7 uso 4); o resto está parafraseado, com página ou tabela.

B3: os três usos da Wikipédia têm substituto.
(1) Dados da operação: CNN Brasil (Couto, 28/10/2025) e relatório da Justiça Global (Fichino, nov/2025), que resume o documento do Estado ao STF. Os números: 2.500 agentes, 32 blindados, 12 veículos de demolição e 2 helicópteros. São 51 mandados da 42ª Vara dentro de um total de 100, e os dois complexos reúnem 26 comunidades.
(2) Mortos: 121 (117 civis e 4 policiais), número da Polícia Civil de 30/10/2025. Passa a 122 com o quinto policial morto em novembro (Reuters, 22/11/2025; Anuário 2026, p. 33 e 70).
(3) Comando Vermelho: Lessing (2008) e Misse (2011), com DOIs conferidos no Crossref, e o perfil do InSight Crime (cerca de 30.000 membros em 2020). Nessa frase, 'fundado em 1979' e 'hoje até 30.000' precisam de ajuste.

B6: 'CNN Brasil (2026a)' não é matéria da CNN. Título e URL são da Defesa em Foco (Marcelo Barros, 30/07/2026). Os números conferem no 20º Anuário: 703 para 798 na Tabela 08; 28 para 51 (+82,1%) na Tabela 06, contra 144 para 139 no país. Já 'maior alta do país' não está no Anuário e é falso em termos relativos (Rio Grande do Norte +100%).

B7: o autor é Scott Mistler-Ferguson, e o texto é de 27/01/2022. A ocupação do Jacarezinho foi em 19/01/2022, não em janeiro de 2023. O texto sustenta os 60.000 moradores, os 1.200 PMs e o Cidade Integrada. Não sustenta as frases sobre ambiente construído (04 linha 15 e 05 linha 5). Para elas servem Grillo (InSight Crime, 2014) e as duas notas do SWJ. A falta de mapas atualizados das rotas continua sem fonte.

B9: cada número tem origem diferente.
- 132: contagem da Defensoria Pública em 29/10/2025 (128 civis e 4 policiais), só em imprensa (CNN Brasil, Exame). A nota da própria Defensoria diz apenas mais de cem.
- 121: número oficial de 30/10/2025, que também está no documento ao STF.
- 122: inclui o quinto policial.
As entradas do SWJ precisam dos autores: Sullivan e da Cruz (2025); Sullivan, Bunker e da Cruz (2021).

B10: o 17,1 por 100 mil em 2024 e a queda de 10,8% vêm do 19º Anuário do FBSP (Tabela 03: homicídio doloso com feminicídio, dados do ISP, população do IBGE). A página da Vanguard foi reescrita e não traz mais o número. O 20º Anuário dá 17,1 também em 2025. O pico da série estadual do ISP é 1994 (63,13 por 100 mil), não o início dos anos 2000. A série da cidade (2.574 em 2003, 965 em 2025) confere nos microdados do ISP por delegacia, com duas ressalvas: 2003 é o primeiro ano da série, não o pico, e desde 2024 o feminicídio sai da coluna de homicídio doloso.

Decisões que ficam com o autor:
- como citar 51 ou 100 mandados;
- achar fonte para a falta de mapas atualizados das rotas, ou tratá-la como argumento próprio;
- os dois-pontos no lugar do traço na manchete do InSight Crime;
- Penglase (2008) não foi lido (texto pago).

Achado lateral: a base atual do ISP também dá 703 mortes por intervenção em 2024, igual ao FBSP. Isso enfraquece a explicação da linha 13 para a diferença com o 699 da JOTA.

### Item por item

- **B3**. Onde: Uso 1 de 3, 04-situating-the-study.md linha 11: (Agência Pública, 2025; Wikipedia, 2026). A frase diz: operação conjunta das polícias civil e militar lançada em 28/10/2025 contra o CV no Alemão e na Penha, cerca de 2.500 agentes, blindados, veículos de demolição e helicópteros, para cumprir 51 mandados de prisão em 26 comunidades.
  Encontrado: sim; confere com a frase: sim; Crossref: não; DOI: sem DOI.
  Referência: Couto, C. (2025, October 28). Megaoperação tenta prender 100 membros do CV no Alemão e Penha (RJ). CNN Brasil. https://www.cnnbrasil.com.br/nacional/sudeste/rj/rj-megaoperacao-com-mais-de-2-mil-policiais-toma-alemao-e-penha/ | Fichino, D. (2025). Operação Contenção: Análise da operação policial mais letal da história do estado do Rio de Janeiro à luz dos padrões internacionais de uso da força e de investigações [Report]. Justiça Global. https://www.global.org.br/wp/wp-content/uploads/2025/11/2025-11-07-JG-RELATORIO-OPERACAO-CONTENCAO_VF-compactado.pdf
  Observação: Fontes originais (a Wikipédia en e pt cita Reuters, G1, Estadão e O São Gonçalo para estes dados). (1) CNN Brasil, Camille Couto, 28/10/2025 06:51, atualizada 12:52: cerca de 2.500 agentes das forças estaduais; 100 mandados de prisão contra integrantes do CV; os complexos do Alemão e da Penha reúnem 26 comunidades; drones, 2 helicópteros, 32 blindados e 12 veículos de demolição do Núcleo de Apoio às Operações Especiais. (2) Relatório da Justiça Global, autoria Daniela Fichino, novembro de 2025, que resume o documento enviado pelo Estado ao STF na ADPF 635: planejamento por SEPOL, PMERJ e GAECO/MPRJ; cerca de 2.500 agentes (650 da Polícia Civil e 1.800 da PM); 2 helicópteros, 32 blindados e 12 veículos de demolição (p. 8 impressa); objetivo principal de cumprir 51 mandados de prisão e 145 de busca expedidos pela 42ª Vara Criminal da Capital, mais 19 de foragidos e 30 do Pará, total de 100 (p. 7 e 8); o relatório discute a divergência 51 contra 100 (p. 16). (3) Agência Pública, byline Catarina Duarte, Paulo Batistella e Ponte Jornalismo, 29/10/2025 10:56: 51 mandados, 2,5 mil policiais, 2 helicópteros, 32 blindados e 12 veículos; não menciona 26 comunidades. A frase confere, mas o 51 é só a base judicial; o governo anunciou 100, e a Wikipédia usa 100. Correção da lista: acrescentar Couto (2025) e Fichino (2025); a entrada 'Global.org.br (2025, November 7)' deve virar Fichino (2025); opcionalmente trocar 'Agência Pública (2025)' por Duarte e Batistella (2025). Frase proposta: On 28 October 2025, a joint operation of the civil and military police (Operação Contenção) was launched against the Comando Vermelho in the Complexo do Alemão and the Complexo da Penha, which together comprise 26 communities. It mobilised about 2,500 officers, 32 armoured vehicles, 12 demolition vehicles and two helicopters (Couto, 2025; Fichino, 2025). Its judicial basis, according to the state's report to the Supreme Federal Court, was 51 arrest warrants issued by the 42nd Criminal Court of the capital, within a total of 100 that the state said it sought to serve (Fichino, 2025).

- **B3**. Onde: Uso 2 de 3, 04-situating-the-study.md linha 11: (CNN Brasil, 2026b; Global.org.br, 2025; Wikipedia, 2026). A frase diz: números oficiais de 121 a 122 mortos, com 4 a 5 policiais, a operação policial mais letal da história do Brasil.
  Encontrado: sim; confere com a frase: sim; Crossref: não; DOI: sem DOI.
  Referência: Couto, C., & Figueiredo, C. (2025, October 30). Polícia atualiza para 121 o número de mortos em megaoperação no Rio. CNN Brasil. https://www.cnnbrasil.com.br/nacional/sudeste/rj/policia-atualiza-numero-de-mortos-em-megaoperacao-no-rio/ | Reuters. (2025, November 22). Fifth police officer dies after Brazil's deadliest anti-drug raid. Investing.com. https://www.investing.com/news/world-news/fifth-police-officer-dies-after-brazils-deadliest-antidrug-raid-4374110 | Fórum Brasileiro de Segurança Pública. (2026). Anuário Brasileiro de Segurança Pública 2026 (Ano 20). https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf
  Observação: (1) CNN Brasil, Camille Couto e Carolina Figueiredo, 30/10/2025 06:07: a Polícia Civil atualizou o total para 121, sendo 117 civis e 4 policiais, a partir dos registros do IML. (2) Justiça Global (Fichino, 2025, p. 5 e 10 impressas): o Estado informa 117 mortos, classificados no documento oficial como opositores neutralizados, e 4 policiais; o relatório qualifica a ação como a operação policial mais letal da história do Brasil. (3) Reuters, 22/11/2025, lida no Investing.com: a Polícia Civil confirmou a morte de um quinto policial ferido na operação, total de 122. (4) 20º Anuário do FBSP: p. 33 (Raquel Sousa) dá 122 mortos, 5 deles agentes de segurança; p. 70 (Leonardo de Carvalho Silva) repete 122 com 5 policiais e diz que pesquisadores a apontam como a mais letal já registrada no Brasil, acima do Carandiru. (5) A CNN Brasil 2026b já citada (Beto Souza, 23/07/2026) também dá 122. A frase confere; basta trocar Wikipedia por estas fontes. A reescrita desta frase, com a cronologia de cada número, está no registro B9 (121 a 122).

- **B3**. Onde: Uso 3 de 3, 04-situating-the-study.md linha 15: (principally the Comando Vermelho, founded in 1979 within the Cândido Mendes prison and now estimated to have up to 30,000 members with territorial reach well beyond Rio de Janeiro; Wikipedia, 2025a).
  Encontrado: sim; confere com a frase: não; Crossref: sim; DOI: 10.1590/S0101-33002008000100004; 10.1590/S0104-44782011000300003.
  Referência: Lessing, B. (2008). As facções cariocas em perspectiva comparativa. Novos Estudos CEBRAP, (80), 43-62. https://doi.org/10.1590/S0101-33002008000100004 | Misse, M. (2011). Crime organizado e crime comum no Rio de Janeiro: Diferenças e afinidades. Revista de Sociologia e Política, 19(40), 13-25. https://doi.org/10.1590/S0104-44782011000300003 | InSight Crime. (2026, September 11). Red Command (Comando Vermelho). https://insightcrime.org/brazil-organized-crime-news/red-command-profile/
  Observação: No verbete da Wikipédia o número de membros remete ao perfil do InSight Crime. Fontes abertas: (1) InSight Crime, perfil Red Command, sem autor individual, publicado 13/08/2026 e atualizado 11/09/2026: o grupo surgiu nos anos 1970 como autoproteção de presos no presídio Cândido Mendes, na Ilha Grande, e em 1979 já tinha passado da prisão às ruas; estimativa de cerca de 30.000 membros no Brasil em 2020; redutos secundários no Amazonas e no Mato Grosso, presença na Bolívia e no Paraguai. (2) Lessing (2008), lido no SciELO: o CV nasceu como gangue de prisão na Cândido Mendes da Ilha Grande; não dá ano. Crossref confere título, autor, número 80, p. 43-62, 2008. (3) Misse (2011), lido no SciELO: o primeiro relatório de um diretor de presídio sobre a organização foi entregue ao governo em 1979, e o nome passou de Falange Vermelha a Comando Vermelho pela imprensa; não cita a Ilha Grande. Crossref confere título, autor, 19(40), p. 13-25, 2011. Penglase (2008, Luso-Brazilian Review 45(1), DOI 10.1353/lbr.0.0001) confere no Crossref, mas o texto é pago e não foi lido; não usar. Problemas da frase: 'founded in 1979' é impreciso (origem nos anos 1970, primeiro registro oficial em 1979) e 'now estimated ... up to 30,000' não bate (estimativa de 2020, cerca de 30.000). O parêntese aninhado também convém desfazer; o resto da frase (tráfico, milícias) não foi conferido aqui. Frase proposta: Rio's security forces operate against criminal organisations that maintain durable, often decades-long territorial control over specific favelas. The principal one, the Comando Vermelho, emerged as a prison gang in the Cândido Mendes penitentiary on Ilha Grande (Lessing, 2008) and was first mentioned in a prison director's report to the government in 1979 (Misse, 2011); in 2020 it was estimated to have around 30,000 members across Brazil, with secondary strongholds in Amazonas and Mato Grosso (InSight Crime, 2026).

- **B6**. Onde: 04-situating-the-study.md linha 5: (CNN Brasil, 2026a; Defesa em Foco, 2026). A frase diz: 798 mortes por intervenção policial no RJ em 2025 contra 703 em 2024; mortes violentas de policiais +82,1%, a maior alta do país; o estado concentra mais de um terço dessas mortes no Brasil.
  Encontrado: sim; confere com a frase: não; Crossref: não; DOI: sem DOI.
  Referência: Fórum Brasileiro de Segurança Pública. (2026). Anuário Brasileiro de Segurança Pública 2026 (Ano 20). https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf | Barros, M. (2026, July 30). Anuário aponta avanço da violência contra policiais no Rio de Janeiro. Defesa em Foco. https://www.defesaemfoco.com.br/anuario-aponta-avanco-da-violencia-contra-policiais-no-rio-de-janeiro/
  Observação: A entrada 'CNN Brasil (2026a)' não é matéria da CNN Brasil: título e URL são da matéria do site Defesa em Foco, assinada por Marcelo Barros, 30/07/2026 10:05, que não menciona a CNN em nenhum ponto (a foto é da Agência Brasil). A busca no domínio cnnbrasil.com.br não achou matéria com esse título nem com o 82,1%; a matéria da CNN Brasil sobre o Anuário (Beto Souza, 23/07/2026, a atual 'CNN Brasil 2026b') não traz o dado dos policiais. Fonte primária aberta: 20º Anuário do FBSP (ISSN 1983-7364). Tabela 08 (p. 67-68): mortes decorrentes de intervenção policial no RJ, 703 em 2024 e 798 em 2025, taxa 4,1 e 4,6 por 100 mil, variação 13,5%. Tabela 06 (p. 51-52): policiais civis e militares vítimas de CVLI no RJ, 28 em 2024 e 51 em 2025, +82,1%; Brasil 144 e 139 (-3,5%); nota da tabela: em 2025 foram 42 PMs e 9 policiais civis. No texto da p. 58 o Anuário trata o Rio como o caso mais saliente, na contramão da tendência nacional. Dois ajustes: 'the sharpest increase recorded nationally' não está no Anuário e não vale em termos relativos (Rio Grande do Norte foi de 1 para 2, +100,0%; Maranhão +75,0%); 'more than a third' vem da Defesa em Foco e se sustenta como 51 de 139. A Tabela 09 (p. 69) confirma o 20,5% do parágrafo seguinte. Correção das entradas: apagar 'CNN Brasil (2026a)'; trocar 'Defesa em Foco (2026)' por Barros (2026) ou retirá-la; renomear 'CNN Brasil (2026b)' para Souza, B. (2026, July 23). Letalidade policial cresce 5,4% no Brasil em 2025, diz Anuário da Segurança. CNN Brasil. https://www.cnnbrasil.com.br/nacional/brasil/letalidade-policial-cresce-54-no-brasil-em-2025-diz-anuario-da-seguranca/; na entrada do FBSP (2026), trocar a URL da página inicial pela do PDF. Frase proposta: The Fórum Brasileiro de Segurança Pública's 20th Anuário Brasileiro de Segurança Pública recorded 798 deaths from police intervention in Rio de Janeiro state in 2025, up from 703 the year before (Fórum Brasileiro de Segurança Pública, 2026, Table 8). Against a national fall from 144 to 139, the number of police officers killed in the state, on or off duty, rose from 28 to 51, an increase of 82.1%, so that Rio de Janeiro accounted for 51 of the 139 police deaths recorded in Brazil (Fórum Brasileiro de Segurança Pública, 2026, Table 6).

- **B7**. Onde: Uso 1 de 4, 04-situating-the-study.md linha 15: (InSight Crime, as cited in Ad Infinitum, 2023; Small Wars Journal, 2021, 2025). A frase atribui ao ambiente construído (construção densa e empilhada que bloqueia a visada, becos e barricadas que detêm blindados, falta de mapas atualizados das rotas) o papel de obstáculo ao policiamento.
  Encontrado: sim; confere com a frase: não; Crossref: não; DOI: sem DOI.
  Referência: Mistler-Ferguson, S. (2022, January 27). Brazil tries to reclaim Rio's favelas: Ad infinitum. InSight Crime. https://insightcrime.org/news/brazil-tries-reclaim-rio-favelas-ad-infinitum/ | Grillo, I. (2014, September 10). Brazil's Red Command and the police who fight them. InSight Crime. https://insightcrime.org/news/analysis/brazils-red-command-rio-police-favelas-slums/ | Sullivan, J. P., Bunker, R., & da Cruz, J. de A. (2021, May 26). Third generation gangs strategic note no. 36: High casualty civil police raid in Rio de Janeiro's Jacarezinho favela raises human rights concerns. Small Wars Journal. https://smallwarsjournal.com/2021/05/26/third-generation-gangs-strategic-note-no-36-high-casualty-civil-police-raid-rio-de/
  Observação: 'Ad Infinitum' não é autor: é o fim da manchete. O texto é de Scott Mistler-Ferguson, publicado no InSight Crime em 27/01/2022 (não 2023). A manchete original usa um traço antes de 'Ad Infinitum'; na entrada proposta ele virou dois-pontos para seguir a regra de não usar travessão (se preferir fidelidade literal, manter a pontuação original na referência). Esse texto NÃO trata de becos, barricadas, relevo, visada nem mapas, então não apoia esta frase, e não há 'InSight Crime citado por' ninguém. Alternativas lidas: Grillo (InSight Crime, publicado 10/09/2014, atualizado 24/04/2023) diz que as ruas estreitas muitas vezes obrigam a CORE a deixar os blindados, que os policiais planejam rotas pelas favelas em labirinto e que ficar acima dos atiradores é um desafio constante; não fala de barricadas nem de mapas. Sullivan, Bunker e da Cruz (SWJ, 26/05/2021, byline John P. Sullivan, Robert Bunker e José de Arimatéia da Cruz) descrevem combate em becos estreitos e em lajes no Jacarezinho e barricadas de concreto na entrada da favela. Sullivan e da Cruz (SWJ, 02/11/2025) registram blindados rompendo barricadas e ruas bloqueadas com carros em chamas. Nenhum dos quatro textos apoia a ausência de mapas confiáveis e atualizados das rotas nem a construção vertical que bloqueia a visada; esse trecho, que motiva o estudo, precisa de fonte própria ou deve aparecer como argumento dos autores. Frase proposta: This territorial permanence, combined with the built environment of the favelas themselves, has repeatedly been described as an obstacle to policing: narrow streets often force special police units to leave their armoured vehicles and to plan routes through maze-like favelas (Grillo, 2014), and incursions have met barricades, concrete ones at the entrance to Jacarezinho in 2021 and burning cars on access roads in 2025 (Sullivan et al., 2021; Sullivan & da Cruz, 2025).

- **B7**. Onde: Uso 2 de 4, 05-case-jacarezinho.md linha 3: (Ad Infinitum, 2023; Caminhos Languages, 2025). A frase diz que fontes comunitárias e jornalísticas citam mais de 60.000 moradores no Jacarezinho.
  Encontrado: sim; confere com a frase: sim; Crossref: não; DOI: sem DOI.
  Referência: Mistler-Ferguson, S. (2022, January 27). Brazil tries to reclaim Rio's favelas: Ad infinitum. InSight Crime. https://insightcrime.org/news/brazil-tries-reclaim-rio-favelas-ad-infinitum/
  Observação: Confere: o texto de Mistler-Ferguson (27/01/2022) descreve o Jacarezinho como favela de mais de 60.000 moradores na Zona Norte. Só a citação muda. Frase proposta: ... while community and journalistic sources commonly cite figures above 60,000 (Caminhos Languages, 2025; Mistler-Ferguson, 2022), ...

- **B7**. Onde: Uso 3 de 4, 05-case-jacarezinho.md linha 5: (Ad Infinitum, 2023). A frase diz que o CV controla o Jacarezinho há décadas e usa o ambiente construído (becos, passarelas elevadas, traçado orgânico) para o tráfico e para limitar o alcance das forças de segurança.
  Encontrado: sim; confere com a frase: não; Crossref: não; DOI: sem DOI.
  Referência: Mistler-Ferguson, S. (2022, January 27). Brazil tries to reclaim Rio's favelas: Ad infinitum. InSight Crime. https://insightcrime.org/news/brazil-tries-reclaim-rio-favelas-ad-infinitum/ | Sullivan, J. P., Bunker, R., & da Cruz, J. de A. (2021, May 26). Third generation gangs strategic note no. 36: High casualty civil police raid in Rio de Janeiro's Jacarezinho favela raises human rights concerns. Small Wars Journal. https://smallwarsjournal.com/2021/05/26/third-generation-gangs-strategic-note-no-36-high-casualty-civil-police-raid-rio-de/
  Observação: Confere só em parte: Mistler-Ferguson (2022) diz que o Comando Vermelho domina o Jacarezinho há muito tempo, mas não fala de becos, passarelas, traçado nem do uso do ambiente para o tráfico ou para conter a polícia. A nota do SWJ de 2021, sobre a operação no próprio Jacarezinho, registra combate em becos estreitos e em lajes e barricadas de concreto na entrada. 'Elevated walkways', 'grown organically' e o uso deliberado do ambiente pelo CV ficam sem fonte: tirar ou buscar fonte. Frase proposta: Like many of Rio's favelas, it has long been dominated by the Comando Vermelho (Mistler-Ferguson, 2022). During the police raid of May 2021, fighting took place in narrow alleys and on rooftops, and concrete barricades stood at the favela's entrance (Sullivan et al., 2021).

- **B7**. Onde: Uso 4 de 4, 05-case-jacarezinho.md linha 7: (Ad Infinitum, 2023). A frase diz que em janeiro de 2023 mais de 1.200 PMs ocuparam a comunidade no programa Cidade Integrada, que combina segurança com investimento social e de infraestrutura.
  Encontrado: sim; confere com a frase: não; Crossref: não; DOI: sem DOI.
  Referência: Mistler-Ferguson, S. (2022, January 27). Brazil tries to reclaim Rio's favelas: Ad infinitum. InSight Crime. https://insightcrime.org/news/brazil-tries-reclaim-rio-favelas-ad-infinitum/
  Observação: Erro de data no manuscrito: a ocupação foi em 19 de janeiro de 2022, não em janeiro de 2023. O texto, datado de 27/01/2022, diz: "On January 19, over 1,200 military police officers marched into Jacarezinho". O mesmo texto confirma que o Cidade Integrada pretende combinar intervenções de segurança com programas sociais e de infraestrutura (com cerca de 91 milhões de dólares do governo estadual, segundo a matéria) e que no mesmo dia a PM entrou na Muzema, dominada por milícia. Frase proposta: This dynamic culminated in the May 2021 Operação Exceptis, discussed above, and again on 19 January 2022, when more than 1,200 military police officers occupied the community as part of the state's "Cidade Integrada" (Integrated City) programme, an initiative meant to pair security interventions with social and infrastructure programmes (Mistler-Ferguson, 2022).

- **B9**. Onde: Entrada 'Small Wars Journal. (2025, November 2)', cujo título diz 132 mortos; citada como (Small Wars Journal, 2025) em 04-situating-the-study.md linhas 11 e 15, enquanto a linha 11 usa 121 a 122.
  Encontrado: sim; confere com a frase: não; Crossref: não; DOI: sem DOI.
  Referência: Sullivan, J. P., & da Cruz, J. de A. (2025, November 2). Third generation gangs strategic note no. 59: Police raid "Megaoperação Contenção" on Comando Vermelho leads to 132 killed. Small Wars Journal. https://smallwarsjournal.com/2025/11/02/third-generation-gangs-strategic-note-no-59-police-raid-megaoperacao-contencao-on-comando-vermelho-leads-to-132-killed/ | Falcão, T., & Couto, C. (2025, October 29). Número de mortes em megaoperação no Rio passa de 130, diz defensoria. CNN Brasil. https://www.cnnbrasil.com.br/nacional/sudeste/rj/numero-de-mortes-em-megaoperacao-no-rio-passa-de-120-diz-defensoria/
  Observação: Origem do 132: Defensoria Pública do Estado do Rio de Janeiro, contagem de quarta-feira, 29/10/2025, depois que moradores retiraram dezenas de corpos da mata. A nota do SWJ (John P. Sullivan e José de Arimatéia da Cruz, 02/11/2025) atribui o 132 à Defensoria e registra também 119 (polícia estadual, 29/10), 58 (governador, primeiro dia) e um trecho do Guardian com 121. CNN Brasil (Tainá Falcão e Camille Couto, 29/10/2025 10:21, atualizada 12:16): 128 civis e 4 policiais, total 132, quando o governo ainda falava em 64. Exame (Estela Marconi, 29/10/2025 13h05) dá o mesmo 132. A nota pública da própria Defensoria (29/10/2025) fala só em mais de cem mortos, sem número exato, então o 132 tem apenas fonte de imprensa. Correção das entradas: o autor não é 'Small Wars Journal'. Usar Sullivan e da Cruz (2025) e, para a nota de 2021, Sullivan, Bunker e da Cruz (2021), byline conferida (John P. Sullivan, Robert Bunker e José de Arimatéia da Cruz, 26/05/2021). No texto: (Sullivan & da Cruz, 2025) e (Sullivan et al., 2021). Frase proposta: ver o registro B9 seguinte (121 a 122), que explicita a origem de cada número.

- **B9**. Onde: 04-situating-the-study.md linha 11: 'Official figures put the death toll at 121 to 122, including four to five police officers' (CNN Brasil, 2026b; Global.org.br, 2025; Wikipedia, 2026).
  Encontrado: sim; confere com a frase: sim; Crossref: não; DOI: sem DOI.
  Referência: Couto, C., & Figueiredo, C. (2025, October 30). Polícia atualiza para 121 o número de mortos em megaoperação no Rio. CNN Brasil. https://www.cnnbrasil.com.br/nacional/sudeste/rj/policia-atualiza-numero-de-mortos-em-megaoperacao-no-rio/ | Fichino, D. (2025). Operação Contenção: Análise da operação policial mais letal da história do estado do Rio de Janeiro à luz dos padrões internacionais de uso da força e de investigações [Report]. Justiça Global. https://www.global.org.br/wp/wp-content/uploads/2025/11/2025-11-07-JG-RELATORIO-OPERACAO-CONTENCAO_VF-compactado.pdf | Reuters. (2025, November 22). Fifth police officer dies after Brazil's deadliest anti-drug raid. Investing.com. https://www.investing.com/news/world-news/fifth-police-officer-dies-after-brazils-deadliest-antidrug-raid-4374110 | Fórum Brasileiro de Segurança Pública. (2026). Anuário Brasileiro de Segurança Pública 2026 (Ano 20). https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf
  Observação: 121: número oficial da Polícia Civil, atualizado na manhã de 30/10/2025 (117 civis e 4 policiais), CNN Brasil (Camille Couto e Carolina Figueiredo, 30/10/2025 06:07). O documento do Estado ao STF, resumido pela Justiça Global (Fichino, 2025, p. 10 impressa), traz os mesmos 117 mais 4 policiais; a Agência Brasil (Mariana Tokarnia, 31/10/2025) repete 121 com 4 policiais, segundo os secretários de Polícia Civil e de Segurança Pública. 122: Reuters, 22/11/2025 (lida no Investing.com), a Polícia Civil confirmou a morte de um quinto policial ferido na operação; o 20º Anuário do FBSP adota 122 com 5 agentes (p. 33 e p. 70). As páginas do governo em rj.gov.br devolveram 403 e não puderam ser abertas; o número oficial fica citado pela Polícia Civil na imprensa e pelo documento ao STF. Frase proposta (substitui a da linha 11 e resolve também o uso 2 de B3): The official count, updated by the Civil Police on 30 October 2025, was 121 dead: 117 civilians and four police officers (Couto & Figueiredo, 2025; Fichino, 2025). It rose to 122 when a fifth officer wounded in the operation died in November (Fórum Brasileiro de Segurança Pública, 2026; Reuters, 2025). On 29 October the Public Defender's Office of the State of Rio de Janeiro had counted 132 dead, 128 civilians and four officers (Falcão & Couto, 2025), the figure in the title of Sullivan and da Cruz (2025). By either count it was the deadliest police operation on record in Brazil (Fichino, 2025; Fórum Brasileiro de Segurança Pública, 2026).

- **B10**. Onde: 04-situating-the-study.md linha 5: (Instituto de Segurança Pública [ISP-RJ], as cited in Vanguard Attaché, 2026). A frase diz que a taxa de homicídio doloso do estado caiu de um pico no início dos anos 2000 para 17,1 por 100 mil em 2024, queda de 10,8% sobre 2023.
  Encontrado: sim; confere com a frase: não; Crossref: não; DOI: sem DOI.
  Referência: Fórum Brasileiro de Segurança Pública. (2025). 19º Anuário Brasileiro de Segurança Pública: 2025. https://publicacoes.forumseguranca.org.br/handle/fbsp/279 | Fórum Brasileiro de Segurança Pública. (2026). Anuário Brasileiro de Segurança Pública 2026 (Ano 20). https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf | Instituto de Segurança Pública do Rio de Janeiro. (n.d.-a). Estatísticas de segurança: Série histórica anual no estado desde 1991 (taxas por 100 mil habitantes) [Data set]. Retrieved September 30, 2026, from https://www.ispdados.rj.gov.br/Arquivos/BaseEstadoTaxaAno.csv
  Observação: A página da Vanguard Attaché aberta hoje (Arthur Harris, atualizada 14/09/2026, título mudou para 'Is Rio safe for tourists? How to assess your trip') não traz nenhuma taxa; o web.archive.org não é acessível daqui, então a versão de março não pôde ser vista. Origem real dos números: 19º Anuário do FBSP (2025), Tabela 03, lida na planilha oficial do item do repositório do FBSP (o PDF de 15,57 MB passa do limite do WebFetch): RJ, homicídio doloso incluindo feminicídio, 3.293 vítimas em 2023 e 2.938 em 2024, taxa 19,1 e 17,1 por 100 mil, variação -10,8%; dados do ISP, população do IBGE. Na mesma edição a MVI do RJ também cai 10,8% (24,8 para 22,1). O 20º Anuário (2026), Tabela 03 (p. 47), mantém 17,1 em 2024 e dá 17,1 em 2025 (2.949 vítimas, +0,4%); a Tabela 02 (p. 29-30) tem a série de MVI do RJ de 2012 a 2025 (máximo 39,5 em 2017; 22,6 em 2025). ISP direto: o arquivo anual de taxas do estado vai de 1991 a 2023, com máximo de homicídio doloso em 1994, 63,13 por 100 mil (2002: 46,85; 2003: 44,62; 2023: 18,75), sem 2024. A série mensal absoluta do estado, somada por mim, dá 3.293 em 2023, 2.908 em 2024 e 2.844 em 2025; somando a coluna de feminicídio, separada a partir de 2024 (30 e 105), chega-se exatamente aos 2.938 e 2.949 do Anuário. Problemas da frase: (a) o pico é 1994, não o início dos anos 2000; (b) 17,1 e 10,8% são do FBSP, com população do IBGE, e não taxa publicada pelo ISP (a do ISP para 2023 é 18,75, contra 19,1 do FBSP, pela diferença de denominador); (c) antes de 1998 a série do ISP não tem coluna de morte por intervenção policial. Correção: apagar a entrada Vanguard Attaché (2026) e acrescentar FBSP (2025) e ISP (n.d.-a). Frase proposta: Homicide figures have fallen substantially since the mid-1990s. In the state series of the Instituto de Segurança Pública (ISP-RJ), which begins in 1991, the intentional homicide rate was highest in 1994, at 63.13 per 100,000 inhabitants (Instituto de Segurança Pública [ISP-RJ], n.d.-a). The Fórum Brasileiro de Segurança Pública puts the rate at 17.1 per 100,000 in 2024, 10.8% below 2023 (Fórum Brasileiro de Segurança Pública, 2025, Table 3), and at 17.1 again in 2025 (Fórum Brasileiro de Segurança Pública, 2026, Table 3). Achado lateral: nos arquivos atuais do ISP, as mortes por intervenção de agente do Estado somam 1.814 em 2019, 703 em 2024 e 800 em 2025 (o Anuário dá 798). O 703 é igual no ISP e no FBSP, então a explicação da linha 13 para a diferença com o 699 da JOTA (as duas séries contam de modo diferente) não se sustenta; a causa provável é a data de extração.

- **B10**. Onde: 04-situating-the-study.md linha 5: (Crime Brasil, 2026). A frase diz que os homicídios na cidade caíram de 2.574 em 2003 para 965 em 2025, redução de 63%.
  Encontrado: sim; confere com a frase: sim; Crossref: não; DOI: sem DOI.
  Referência: Instituto de Segurança Pública do Rio de Janeiro. (n.d.-b). Estatísticas de segurança: Série histórica mensal por área de delegacia desde 01/2003 [Data set]. Retrieved September 30, 2026, from https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv | Instituto de Segurança Pública do Rio de Janeiro. (2021). Séries históricas anuais de taxa de letalidade violenta no estado do Rio de Janeiro e grandes regiões. https://www.ispdados.rj.gov.br/Arquivos/SeriesHistoricasLetalidadeViolenta.pdf
  Observação: Crime Brasil: autor Valdo Stonehart, 17/04/2026; dá 965 homicídios dolosos na capital em 2025, 63% abaixo do que chama de pico de 2003 (2.574), com dados do ISP. Conferido direto no ISP: a série mensal por delegacia (desde 01/2003), somada por mim para as delegacias do município do Rio, dá exatamente 2.574 em 2003 e 965 em 2025 (946 em 2024; 1.492 em 2017). Ressalvas: (a) 2003 é o primeiro ano dessa série, não o pico, pois 2004 soma 2.653; (b) para a capital o ISP tem série de letalidade violenta desde 1991 (PDF da Coordenadoria de Estatística, março de 2021), com máximo em 1994: 4.192 mortes, 75,9 por 100 mil; (c) a partir de 2024 o feminicídio fica em coluna própria (47 na capital em 2025, soma minha), então o 965 não inclui feminicídios e o de 2003 provavelmente sim; conferir a nota metodológica do ISP antes de comparar os dois anos; (d) o 63% é arredondamento do Crime Brasil e pode sair. Correção da entrada: citar ISP (n.d.-b) no lugar de Crime Brasil; se mantiver, completar como Stonehart, V. (2026, April 17). Criminalidade no Rio de Janeiro cidade: 20 anos de dados e o que mudou. Crime Brasil. https://crimebrasil.com.br/analises/criminalidade-rio-de-janeiro-cidade-2025. Frase proposta: In the city of Rio de Janeiro, ISP-RJ records by police district show intentional homicides falling from 2,574 in 2003, the first year of that series, to 965 in 2025 (ISP-RJ, n.d.-b).
