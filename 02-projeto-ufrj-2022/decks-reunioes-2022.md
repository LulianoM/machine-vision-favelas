# Transcrição dos materiais do Drive "PROJETO DRONE" (2022)

Pasta do Drive: https://drive.google.com/drive/folders/1uljOHH2AyMCFj9Q1sTA5XYA70kvNqU0- (conta martinslucianofigueira@gmail.com).

## CronogramaDoProjeto (Google Doc, 24/03/2022)

Reuniões de 14h às 15h via Meet (qkt-bist-ofb).

- 05/04: apresentar papers do assunto (IEEE e ACM). Entregável: lista de papers 2018+ com resumos, o que existe e o que falta.
- 19/04: proposta de solução.
- 03/05: protótipo (MVP). Ferramentas necessárias para demonstrar que a solução funciona: algoritmo, simulação etc.
- 17/05: design de teste. Métricas de desempenho.
- 31/05: documentação. Relatório ou tese.

## Deck "Reunião 05_04 Resumo Papers" (Fábio)

1. Insight: trabalho de conclusão da disciplina Simulação de Drones e Aplicações do ITA (SC-249).
2. Nesse trabalho ("Detecção de Objetos em Tempo Real com Piloto Humano com Instabilidade"), seção II.A, cita Hu et al. 2021 (Monocular Quasi-Dense 3D Object Tracking) no contexto de datasets para CNN de bounding box.
3. Hu et al., seção 4, afirma que anotar bounding box é caro e recorre ao GTA V. Cita Richter et al. 2017 (Playing for Benchmarks) e Krähenbühl 2018 (Free Supervision from Video Games).
4. Muitos artigos citam o livro Synthetic Data for Deep Learning (Nikolenko) para validar dados artificiais.
5. No contexto de UAV: "extensos conjuntos de dados de imagens UAV anotados ainda são escassos" (Wu, Liebel e Körner, ICPR 2020).
6. Resumo traduzido de Narayanan et al. 2018: YOLO a bordo de hexacóptero, ME-RCNN na estação base, treino com mistura de imagens aéreas reais e sintéticas ar-solo geradas por motor de videogame; quantifica o ganho do sintético.

## Deck "Reunião 19_04 Proposta" (Fábio)

**Fusão de Dados em imagens RGB-T obtidas por UAV para aumento da eficácia na detecção de ameaças usando CNN treinada com dados sintéticos**

A fusão de dados de múltiplos sensores permite realizar inferências que não são viáveis a partir de um único sensor [1]. O rastreamento de objetos térmicos visíveis (RGB-T) visa obter um desempenho robusto com a orientação das informações de temperatura dos objetos [2]. No trabalho em tela utilizaremos sensores RGB-T embarcados em UAV para detectar ameaças no contexto da segurança pública. Tal detecção (bounding box) ocorrerá confrontando os dados (fundidos) dos sensores com um modelo gerado pelo treinamento de uma CNN. Embora haja alta demanda para o desenvolvimento de abordagens de aprendizado profundo, extensos conjuntos de dados de imagens aéreas anotadas, no domínio UAV, ainda são escassos [3]. Atacamos este problema utilizando dados sintéticos, ou seja, dados produzidos artificialmente com a finalidade de treinar modelos de aprendizado de máquina [4]. Para gerar imagens sintéticas de perspectivas aéreas, será utilizado o videogame ARMA 3, motor de jogo de mundo aberto com gráficos foto-realistas [5]. Neste jogo será possível gerar um ambiente urbano e simular as ameaças dentro do subdomínio "segurança pública".

[1] Farias e Pirmez 2017. [2] Zhang et al. 2022 (Visible-Thermal UAV Tracking). [3] Wu, Liebel e Körner 2021. [4] Nikolenko 2021. [5] Narayanan et al. 2018.

## Deck "Reunião 03_05 Protótipo de solução" (Fábio)

Slides: "Antes da Fusão: RGB, LBA (térmico), Converter"; "Fusão: + = "; e o código Julia abaixo (leitura de vídeo e escrita de frames com VideoIO).

```julia
using VideoIO
using Plots

function play_video(url)
    strm = VideoIO.openvideo(url)
    img = read(strm)
    fig = plot(img)
    while !eof(strm)
        read!(strm, img)
        plot!(fig, img)
        display(fig)
    end
end

play_video("rtsp://demo.stream.net/vod/mp4:test.mov")

using VideoIO
framestack = map(x->rand(UInt8, 100, 100), 1:100) # vector of 2D arrays
encoder_options = (crf=23, preset="medium")
framerate=24
open_video_out("video.mp4", framestack[1], framerate=framerate, encoder_options=encoder_options) do writer
    for frame in framestack
        write(writer, frame)
    end
end
```

## CÓDIGOS / "Docs sobre o Armas3" (Google Doc, 16/05/2022)

Como scriptar:
- https://forums.bohemia.net/forums/topic/183993-scripting-introduction-for-new-scripters/
- https://forums.bohemia.net/forums/topic/145056-arma-3-scripting-tutorial-for-noobs/

Comandos:
- https://community.bistudio.com/wiki/Category:Arma_3:_Editing
- https://community.bistudio.com/wiki/boundingBoxReal

## myScriptArmas3.txt (29/05/2022)

Script original de 3 linhas, salvo em `03-arma3/scripts/myScriptArmas3-original-2022.sqf`. Espera 3 s, pega o `boundingBoxReal` da unidade `man1`, mostra no hint e salva um screenshot com o nome igual ao box.

## DATASET (maio/2022)

- `ImagensExemplos/`: 28 capturas PNG (111 a 524, ~2 a 3,5 MB cada) feitas em 07/05/2022, vista de cima do editor Eden com unidades posicionadas. `411.PNG` e `412.PNG` são menores (~250 KB); a 412 está em `03-arma3/amostra/`.
- `ComBoundingBox/`: 7 PNGs (~7 MB cada) de 29/05/2022, nomeadas com a saída do script. Seis têm nome no formato `[x,y]` (saída de `worldToScreen`, posição 2D na tela) e uma tem `[[-0.8,-1.15,-0.1],[0.8,1.05,1.9],3.58852]` (saída de `boundingBoxReal`, caixa 3D no espaço do modelo).
- `imgboxScreen/`: 42 PNGs (~6 MB cada) de 30/05/2022, todas nomeadas `[x,y]`, com a unidade quase sempre perto do centro da tela (x≈0.476, y≈0.599).

Conclusão do estado de 2022: o pipeline chegou a extrair a posição 2D do centro da unidade na tela, mas não a caixa 2D completa. O script novo em `03-arma3/scripts/capturaDataset.sqf` fecha essa etapa.

## Ortomosaico (ago/2022)

Dados reais da PCERJ: `Jacarezinho_Sudoeste.zip` (145 MB), `Jacarezinho_Nordeste.zip` (248 MB), pastas de output e `Manguinhos` (Alexandre Vasconcelos). Sensíveis. Não incluídos.
