# Machine Vision from the Global South

Detecção de pessoas, e de pessoas armadas, em imagem aérea de drone sobre favela, com um detector YOLO treinado só com dados sintéticos gerados no **Blender**. A cena da favela é procedural: becos estreitos, lajes, mosaico de coberturas e morro com mata. A anotação de bounding box sai automática e exata do próprio motor de render. O modelo é testado em imagem aérea real (VisDrone, HERIDAL). A ética do uso dual é tema central do artigo.

Artigo em coautoria: Luciano Martins Figueira (mestrado, FGV EBAPE), prof. Hélio Arthur Reis Irigaray (FGV EBAPE) e Felipe I. M. Toledo (COPPE/UFRJ).

- **Reproduzir ou validar:** [`REPRODUZIR.md`](REPRODUZIR.md)
- **Modelos, corpora e runs:** [releases](https://github.com/LulianoM/machine-vision-favelas/releases)
- **Números e o comando que gerou cada um:** [`06-resultados/RESULTADOS.md`](06-resultados/RESULTADOS.md)

## Estrutura

| Pasta | Conteúdo |
|---|---|
| [`01-artigo/`](01-artigo/) | manuscrito por seção, pendências, versões |
| [`02-projeto-ufrj-2022/`](02-projeto-ufrj-2022/) | projeto de 2022 (PCERJ e NCE-UFRJ) que deu origem ao trabalho, incluindo o plano original com ARMA 3, que não foi usado |
| [`03-blender/`](03-blender/) | **pipeline usado**: geradores de cena, anotação, ladrilhamento, treino e avaliação |
| [`04-bibliografia/`](04-bibliografia/) | índices e notas de leitura |
| [`05-levantamento-3d/`](05-levantamento-3d/) | levantamento de fontes de geometria para a cena |
| [`06-resultados/`](06-resultados/) | métricas, critérios por rodada, inventário de dados e de pesos |
| [`08-conferencia/`](08-conferencia/) | versão curta para a conferência |
| [`docs/`](docs/) | ambiente da máquina, contexto e divergências registradas |

## Dados que não estão aqui

As fotos de drone de 2022 sobre o Jacarezinho são dado operacional da Polícia Civil do Rio de Janeiro. Elas e tudo que reproduz a imagem ou a geometria delas não são publicados. Os resultados do artigo vêm do braço procedural, que está publicado inteiro.

## Créditos

A ideia de treinar com dado sintético de motor de jogo vem da proposta de Fábio H. P. Guimarães (2022), com orientação do prof. Claudio Miceli de Farias (NCE-UFRJ).
