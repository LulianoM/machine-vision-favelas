---
title: Computer Vision e Drones em Segurança Pública, Bibliografia Comentada
tags:
  - domain/pesquisa
  - domain/tech
  - topic/computer-vision
  - topic/drones
  - topic/seguranca-publica
  - type/reference
  - status/active
source: Pesquisa web 2026-09-09 (Claude Code). Metadados dos 15 artigos verificados via API do Crossref; fatores de impacto lidos nas páginas oficiais das editoras em 09/09/2026 (JCR 2025, Clarivate, divulgado jun/2026)
created: 2026-09-09
related:
  - "[[2026-09-09 - Bibliografia CV Drones Seguranca Publica.pdf]]"
  - "[[Socios]]"
---

# Computer Vision e Drones em Segurança Pública

> Levantamento de 15 artigos (mais 3 complementares) sobre visão computacional embarcada ou aplicada a imagens de VANT (drone) em problemas de segurança pública: vigilância, detecção de crime e violência, policiamento de eventos, perícia, busca e salvamento, resposta a emergências e governança. Contexto: base para o projeto de detecção de ameaças em imagens RGB-T de UAV (UFRJ 2022, prof. Claudio Miceli e perito Fábio Guimarães, PCERJ) e para o mestrado. PDF completo: [[2026-09-09 - Bibliografia CV Drones Seguranca Publica.pdf]].

**Critério de seleção:** revisados por pares (periódico ou conferência de referência). Um preprint arXiv incluído por ser a revisão mais citada do tema. Resumos vieram dos abstracts e resultados de busca (texto completo bloqueado pelas editoras); conferir métricas no artigo antes de citar.

---

## Os 3 para ler primeiro

1. **Nguyen et al. (2022), The State of Aerial Surveillance: A Survey.** O mapa do território: detecção, rastreamento, reidentificação e ações de pessoas a partir de drones, comparação com câmeras fixas e datasets públicos. Revisão mais citada do tema, autores de referência (Fookes, Sridharan, Ross). https://arxiv.org/abs/2201.03080
2. **Royo et al. (2022), Enhancing Drones for Law Enforcement and Capacity Monitoring at Open Large Events.** Único da lista com deep learning validado em operação policial real (polícia de Castelldefels): contagem, lotação, latência, limites de altitude e câmera. https://doi.org/10.3390/drones6110359
3. **Zhang et al. (2025), Aerial Person Detection for Search and Rescue: Survey and Benchmarks.** Survey com benchmark RGB e térmico (RGBTDronePerson), JIF 11.0. Fala diretamente com alvo pequeno e fusão RGB-T do projeto PCERJ. https://doi.org/10.34133/remotesensing.0474

Quarto e quinto: Srivastava et al. (2022), o mais próximo de prevenção de crime; Ahmad et al. (2025) na ACM Computing Surveys, o mais forte em JIF, mas mais amplo (arquitetura do sistema inteiro).

---

## A. Revisões e surveys

| # | Referência | Periódico | Resumo |
|---|---|---|---|
| 1 | Nguyen, K.; Fookes, C.; Sridharan, S.; Tian, Y.; Liu, F.; Liu, X.; Ross, A. (2022). The State of Aerial Surveillance: A Survey. [arXiv 2201.03080](https://arxiv.org/abs/2201.03080) | arXiv (preprint) | Revisão centrada no humano da vigilância aérea: detecção, identificação, rastreamento e reidentificação a partir de drones. Mapeia datasets e lacunas. |
| 2 | Akbari, Y.; Almaadeed, N.; Al-maadeed, S.; Elharrouss, O. (2021). Applications, databases and open computer vision research from drone videos and images: a survey. 54(5). [DOI](https://doi.org/10.1007/s10462-020-09943-1) | Artificial Intelligence Review | Aplicações de CV em vídeo de drone com seção de vigilância, detecção de pessoas, reconhecimento facial e desastres. Inventário de bases de dados e problemas abertos. |
| 3 | Ramachandran, A.; Sangaiah, A. K. (2021). A review on object detection in unmanned aerial vehicle surveillance. 2. [DOI](https://doi.org/10.1016/j.ijcce.2021.11.005) | Int. J. of Cognitive Computing in Engineering | Detecção e rastreamento de objetos em vigilância por VANT: arquiteturas de DL, métricas e restrições embarcadas. Ponto de partida para implementar o pipeline. |
| 4 | Simões, D. P.; Oliveira, H. C.; Marsico, S.; Souza, J. R.; Barbosa, L. A. (2025). Human detection in UAV imagery using deep learning: a review. 37(22). [DOI](https://doi.org/10.1007/s00521-025-11446-5) | Neural Computing and Applications | Revisão de grupo brasileiro sobre detecção de pessoas em imagem de drone: alvos pequenos, altitude, ângulo e limites de hardware embarcado. |
| 5 | Ahmad, T.; Morel, A.; Cheng, N.; Palaniappan, K.; Calyam, P.; Sun, K.; Pan, J. (2025). Future UAV/Drone Systems for Intelligent Active Surveillance and Monitoring. 58(2). [DOI](https://doi.org/10.1145/3760389) | ACM Computing Surveys | Sistemas de vigilância ativa: percepção, autonomia, comunicação e edge computing integrados. Arquitetura completa drone, rede e nuvem. |

## B. Detecção de crime, violência e policiamento

| # | Referência | Periódico | Resumo |
|---|---|---|---|
| 6 | Srivastava, A.; Badal, T.; Saxena, P.; Vidyarthi, A.; Singh, R. (2022). UAV surveillance for violence detection and individual identification. 29(1). [DOI](https://doi.org/10.1007/s10515-022-00323-3) | Automated Software Engineering | Detecta comportamento violento em vídeo aéreo e identifica os envolvidos. Pose + classificação de ações com DL. |
| 7 | Vuyyuru, L. R.; Purimetla, N. R.; Reddy, K. Y.; Vellela, S. S.; Basha, S. K.; Vatambeti, R. (2024). Advancing automated street crime detection: a drone-based system integrating CNN models and enhanced feature selection techniques. 16(2). [DOI](https://doi.org/10.1007/s13042-024-02315-z) | Int. J. of Machine Learning and Cybernetics | Detecção de crimes de rua com CNN e seleção de características otimizada; ganhos de acurácia e discussão de latência. |
| 8 | Royo, P.; Asenjo, À.; Trujillo, J.; Çetin, E.; Barrado, C. (2022). Enhancing Drones for Law Enforcement and Capacity Monitoring at Open Large Events. 6(11), 359. [DOI](https://doi.org/10.3390/drones6110359) | Drones | Caso real com a polícia de Castelldefels (ES): contagem de pessoas e lotação em eventos abertos. |
| 9 | Georgiou, A.; Masters, P.; Johnson, S.; Feetham, L. (2022). UAV-assisted real-time evidence detection in outdoor crime scene investigations. 67(3). [DOI](https://doi.org/10.1111/1556-4029.15009) | Journal of Forensic Sciences | Detecção em tempo real de evidências em cenas de crime ao ar livre; taxas próximas de 100% em áreas amplas; uso pericial. |
| 10 | Abu-Khadrah, A.; Al-Qerem, A.; Hassan, M. R.; Ali, A. M.; Jarrah, M. (2025). Drone-assisted adaptive object detection and privacy-preserving surveillance in smart cities using whale-optimized deep reinforcement learning techniques. 15. [DOI](https://doi.org/10.1038/s41598-025-94796-3) | Scientific Reports | Detecção adaptativa em aglomerações urbanas com otimização + RL profundo e preservação de privacidade no mesmo desenho. |

## C. Busca, salvamento e resposta a emergências

| # | Referência | Periódico | Resumo |
|---|---|---|---|
| 11 | Zhang, X.; Feng, Y.; Wang, N.; Lu, G.; Mei, S. (2025). Aerial Person Detection for Search and Rescue: Survey and Benchmarks. 5. [DOI](https://doi.org/10.34133/remotesensing.0474) | Journal of Remote Sensing | Survey + benchmarks de detecção de pessoas para SAR, incluindo dataset RGB-T RGBTDronePerson. |
| 12 | Fraternali, P.; Morandini, L.; Motta, R. (2025). Enhancing Search and Rescue Missions with UAV Thermal Video Tracking. 17(17), 3032. [DOI](https://doi.org/10.3390/rs17173032) | Remote Sensing | Rastreamento de pessoas em vídeo térmico de drone, robusto a oclusão e baixo contraste. |
| 13 | Kyrkou, C.; Theocharides, T. (2019). Deep-Learning-Based Aerial Image Classification for Emergency Response Applications Using Unmanned Aerial Vehicles. [DOI](https://doi.org/10.1109/CVPRW.2019.00077) | IEEE/CVF CVPR Workshops | Dataset AIDER e CNN leve embarcada para classificar incêndio, enchente, colapso e acidente de trânsito. |

## D. Governança, ética e integração operacional

| # | Referência | Periódico | Resumo |
|---|---|---|---|
| 14 | Dolata, M.; Schwabe, G. (2023). Moving beyond privacy and airspace safety: Guidelines for just drones in policing. 40(4). [DOI](https://doi.org/10.1016/j.giq.2023.101874) | Government Information Quarterly | Aceitação pública de drones policiais depende da percepção de justiça, não só de privacidade. Diretrizes para programas. |
| 15 | Davies, A.; Krame, G. (2023). Integrating body-worn cameras, drones, and AI: A framework for enhancing police readiness and response. 17. [DOI](https://doi.org/10.1093/police/paad083) | Policing: A Journal of Policy and Practice | Framework sociotécnico: CV como parte de sistema com treinamento, protocolo e accountability. |

## Complementares (fora dos 15)

- Obaid, L. et al. (2025). State-of-the-art review of UAVs and AI for traffic and safety analyses. Transportation Research Interdisciplinary Perspectives, 33. https://doi.org/10.1016/j.trip.2025.101591
- Farhan, M. et al. (2025). Transforming Highway Safety With Autonomous Drones and AI: A Framework for Incident Detection and Emergency Response. IEEE Open Journal of Vehicular Technology, 6. https://doi.org/10.1109/ojvt.2025.3549387
- Jamil, S. et al. (2020). Malicious UAV Detection Using Integrated Audio and Visual Features for Public Safety Applications. Sensors, 20(14). https://doi.org/10.3390/s20143923 (o inverso do tema: CV para detectar drones hostis)

---

## Ranking dos periódicos por fator de impacto (JCR 2025)

| # | Periódico | Editora | JIF 2025 | JIF 5 anos | Artigos |
|---|---|---|---|---|---|
| 1 | ACM Computing Surveys | ACM | 30.4 | n/d | 5 |
| 2 | Artificial Intelligence Review | Springer | 18.8 | 19.1 | 2 |
| 3 | Journal of Remote Sensing | Science Partner Journals (AAAS) | 11.0 | n/d | 11 |
| 4 | Government Information Quarterly | Elsevier | 10.8 | n/d | 14 |
| 5 | Drones | MDPI | 5.2 | 5.3 | 8 |
| 6 | Scientific Reports | Springer Nature | 4.9 | 4.8 | 10 |
| 7 | Remote Sensing | MDPI | 4.3 | 5.0 | 12 |
| 8 | Automated Software Engineering | Springer | 3.9 | 3.4 | 6 |
| 9 | Int. J. of Machine Learning and Cybernetics | Springer | 2.9 | 3.4 | 7 |
| 10 | Journal of Forensic Sciences | Wiley | 1.9 | n/d | 9 |
| 11 | Policing: A Journal of Policy and Practice | Oxford UP | 1.8 | n/d | 15 |
| - | Neural Computing and Applications | Springer | não divulgado * | n/d | 4 |
| - | Int. J. of Cognitive Computing in Engineering | KeAi / Elsevier | sem JIF (CiteScore 18.0) | n/d | 3 |
| - | CVPR Workshops (conferência) | IEEE/CVF | não se aplica | | 13 |
| - | arXiv (preprint) | | não se aplica | | 1 |

\* A Springer não exibe JIF 2025 para a NCA, enquanto os outros três títulos da editora exibem. Compatível com supressão pela Clarivate no JCR 2025, sem comunicado oficial encontrado. Último JIF conhecido: 4.5 (JCR 2024). Tratar o artigo 4 com cautela se o critério for JIF.

Complementares: TRIP 4.8; Sensors 4.0; IEEE OJVT entre 6.4 e 6.6 (agregadores, página da IEEE bloqueou a verificação).

**Leitura:** os 4 primeiros são revistas de revisão ou de política pública, onde o JIF é naturalmente alto. Entre revistas de artigos empíricos aplicados, Drones e Scientific Reports lideram. Bloco forte para fundamentação com JIF de dois dígitos: artigos 5, 2, 11 e 14.

---

## Como este levantamento foi feito (para repetir)

1. Buscas web por eixo (survey, crime/violência, eventos/multidão, SAR/térmico, emergências/trânsito, ética/privacidade).
2. Verificação de autores, ano, periódico e volume via `https://api.crossref.org/works/{DOI}` (editoras bloqueiam fetch direto; DOIs errados foram corrigidos por `query.title`).
3. Fator de impacto lido nas páginas oficiais com o navegador (Playwright); agregadores como journalmetrics.org, resurchify e researcher.life divergem e alguns usam Scopus/OpenAlex, não JCR.
4. PDF gerado por HTML + Chrome headless em `~/Desktop/PESQUISA CV DRONES/`.
