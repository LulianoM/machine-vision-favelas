---
title: Bibliografia do Projeto Drone PCERJ (papers do Fábio Guimarães)
tags:
  - domain/pesquisa-academica
  - type/bibliography
  - topic/visao-computacional
  - topic/dados-sinteticos
  - topic/fusao-rgb-termico
source: Drive > PROJETO DRONE > BIBLIOGRAFIA E PAPERS SELECIONADOS (subidos por fabiocsirj@gmail.com em abr/2022)
created: 2026-09-10
related:
  - "[[Projeto Drone PCERJ - UFRJ 2022]]"
---

# Bibliografia do Projeto Drone PCERJ

19 arquivos na pasta do Drive. 18 PDFs copiados para `Papers/` (17 originais + 1 preprint do arXiv em vez do livro). Dois ficaram só no Drive por passarem do limite do conector.

## Trabalho base do Fábio

- Guimarães, F. H. P.; Freitas, R. D.; Cunha, M. L. O. **Detecção de Objetos em Tempo Real com Piloto Humano com Instabilidade.** Trabalho final SC-249, ITA, jul/2021. [[Papers/Projeto_Boxing_ITA.pdf]]
  YOLOv4 + filtro de Kalman, dataset sintético gerado em Matlab/Simulink (vr octavia + drone 6DoF), anotação automática por câmera pinhole.

## Eixo 1: Treinamento com dados sintéticos

Eixo central da proposta. Ordem por proximidade com o projeto.

- Narayanan, P.; Borel-Donohue, C.; Lee, H.; Kwon, H.; Rao, R. **A real-time object detection framework for aerial imagery using deep neural networks and synthetic training images.** Proc. SPIE 10646, 2018. [[Papers/A real-time object detection framework for aerial imagery using deep neural networks and synthetic training images.pdf]]
  O mais próximo do caso: YOLO a bordo de hexacóptero, treinado com mistura de imagens aéreas reais e sintéticas ar-solo de motor de videogame. Quantifica o ganho do sintético. Ref. 5 da proposta.
- Nikolenko, S. I. **Synthetic Data for Deep Learning.** Springer Optimization and Its Applications 174, 2021. Preprint arXiv:1909.11512. [[Papers/Synthetic Data for Deep Learning - Nikolenko (arXiv 1909.11512).pdf]]
  Fundamento teórico da técnica. Ref. 4 da proposta.
- Wu, S.; Liebel, L.; Körner, M. **Derivation of Geometrically and Semantically Annotated UAV Datasets at Large Scales from 3D City Models.** ICPR 2020. **Só no Drive:** https://drive.google.com/file/d/1CtHcPns5VFUOe5Vk1wN5a82znDHzflAP/view
  Origem da frase de abertura da proposta sobre escassez de datasets UAV anotados. Ref. 3 da proposta.
- Richter, S. R.; Vineet, V.; Roth, S.; Koltun, V. **Playing for Data: Ground Truth from Computer Games.** ECCV 2016. [[Papers/Playing for Data Ground Truth from Computer Games.pdf]]
  Rótulos pixel a pixel extraídos do GTA V interceptando a comunicação com a GPU. Modelo com dados do jogo + 1/3 do CamVid supera o CamVid inteiro.
- Krähenbühl, P. **Free Supervision from Video Games.** CVPR 2018. [[Papers/Free Supervision From Video Games.pdf]]
  Injeção no DirectX para gerar ground truth em tempo real (segmentação, profundidade, fluxo óptico, tracking). 220 mil imagens em 3 jogos.
- Hu, H.-N. et al. **Monocular Quasi-Dense 3D Object Tracking.** arXiv:2103.07351, 2021. [[Papers/Monocular Quasi-Dense 3D Object Tracking (arXiv 2103.07351).pdf]]
  Usa GTA V para dataset de tracking. Foi por este paper que o Fábio chegou em Richter e Krähenbühl.
- Kniaz, V.; Gorbatsevich, V. S.; Mizginov, V. **ThermalNet: A Deep Convolutional Network for Synthetic Thermal Image Generation.** ISPRS Archives XLII-2/W4, 2017. [[Papers/THERMALNET_A_DEEP_CONVOLUTIONAL_NETWORK_FOR_SYNTHE.pdf]]
  Gera imagens térmicas sintéticas a partir de RGB. Ponte entre o eixo sintético e o eixo RGB-T.

## Eixo 2: Fusão RGB + térmico

- Zhang, P.; Zhao, J.; Wang, D.; Lu, H.; Ruan, X. **Visible-Thermal UAV Tracking: A Large-Scale Benchmark and New Baseline.** CVPR 2022, arXiv:2204.04120. [[Papers/Visible-Thermal UAV Tracking (arXiv 2204.04120).pdf]] Ref. 2 da proposta.
- Sun, Y.; Zuo, W.; Liu, M. **RTFNet: RGB-Thermal Fusion Network for Semantic Segmentation of Urban Scenes.** IEEE RA-L 4(3), 2019. [[Papers/RTFNet RGB-Thermal Fusion Network for Semantic Segmentation of Urban Scenes.pdf]]
- Sun, Y.; Zuo, W.; Yun, P.; Wang, H.; Liu, M. **FuseSeg: Semantic Segmentation of Urban Scenes Based on RGB and Thermal Data Fusion.** IEEE T-ASE, 2020. [[Papers/FuseSeg Semantic Segmentation of Urban Scenes Based on RGB and Thermal Data Fusion.pdf]]
- Yogamani, S.; Dahyot, R. et al. **CNN based Color and Thermal Image Fusion for Object Detection in Automated Driving.** IMVIP 2020. [[Papers/CNN_based_Color_and_Thermal_Image_Fusion_for_Object_Detection_in_Automated_Driving.pdf]]
- Lee, Y.; Bui, T. D.; Shin, J. **Pedestrian Detection based on Deep Fusion Network using Feature Correlation.** APSIPA ASC 2018. [[Papers/Pedestrian Detection based on Deep Fusion Networkusing Feature Correlation.pdf]]
- Rocco Spremolla, I.; Antunes, M.; Aouada, D.; Ottersten, B. **RGB-D and Thermal Sensor Fusion: Application in Person Tracking.** VISAPP 2016. [[Papers/RGB-D and Thermal Sensor FusionApplication in Person Tracking.pdf]]
- Kim, J.; Cho, J. **Exploring a Multimodal Mixture-Of-YOLOs Framework for Advanced Real-Time Object Detection.** Applied Sciences 10(2), 2020. [[Papers/Exploring a Multimodal Mixture-Of-YOLOs Framework for Advanced Real-Time Object Detection.pdf]]
- Li, S.; Li, Y.; Li, Y.; Li, M.; Xu, X. **YOLO-FIRI: Improved YOLOv5 for Infrared Image Object Detection.** IEEE Access 9, 2021. DOI 10.1109/ACCESS.2021.3120870. [[Papers/YOLO-FIRI_Improved_YOLOv5_for_Infrared_Image_Object_Detection.pdf]]
- Sharma, M. et al. **YOLOrs: Object Detection in Multimodal Remote Sensing Imagery.** IEEE JSTARS 14, 2021. DOI 10.1109/JSTARS.2020.3041316. **Só no Drive:** https://drive.google.com/file/d/1DLe51G9rpiSqEjCzpR2xmxyMCB0SAa_b/view

## Eixo 3: Fusão de dados em geral

- Farias, C. M. de; Pirmez, L. **A Multisensor Data Fusion Technique for Multiapplication Wireless Sensor Networks Based on Overlapping Intervals.** IEEE DASC/PiCom/DataCom/CyberSciTech, 2017. [[Papers/a-multisensor-data-fusion-technique-for-multiapplication-wireles-2017.pdf]] Paper do orientador. Ref. 1 da proposta.
- Meng, T.; Jing, X.; Yan, Z.; Pedrycz, W. **A Survey on Machine Learning for Data Fusion.** Information Fusion 57, 2020. DOI 10.1016/j.inffus.2019.12.001. [[Papers/A Survey on Machine Learning for Data Fusion.pdf]]
- Rosero, L. A. R. **Detecção de obstáculos usando fusão de dados de percepção 3D e radar em veículos automotivos.** Dissertação de mestrado, ICMC-USP, 2017. [[Papers/LuisAlbertoRoseroRosero_revisadapdf.pdf]] PDF escaneado, sem texto pesquisável.

## Referências do artigo do ITA sem PDF na pasta

- Sobral, P. V. N. C.; Santos, A. T. A Inserção dos Drones (RPAS) na Segurança Pública Brasileira. Revista Em Tempo 18(1), 2019.
- Delibasoglu, I. UAV Images Dataset for Moving Object Detection from Moving Cameras. arXiv:2103.11460, 2021.
- Benjdira, B. et al. Car Detection using UAVs: Comparison between Faster R-CNN and YOLOv3. UVS Oman, 2019.
- Silano, G.; Iannelli, L. MAT-Fly: an educational platform for simulating UAVs aimed to detect and track moving objects. IEEE Access 9, 2021.
- Bochkovskiy, A.; Wang, C.-Y.; Liao, H.-Y. M. YOLOv4: Optimal Speed and Accuracy of Object Detection. arXiv:2004.10934, 2020.
- Li, J.-M.; Chen, C. W.; Cheng, T.-H. Estimation and tracking of a moving target by UAVs. ACC 2019.
