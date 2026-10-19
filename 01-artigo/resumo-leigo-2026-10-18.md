# Dá para ver de cima se alguém está armado? O que o nosso artigo descobriu

*Resumo simplificado, para leitura sem conhecimento técnico. Versão de 18 de outubro de 2026, que substitui a de 30 de setembro.*

## A pergunta

Fala-se cada vez mais em drones que "reconhecem uma pessoa armada" do alto, mas quase nunca se diz a que altura, com que câmera e em que luz. O artigo as mede, tomando o Jacarezinho, no Rio, como o tipo de território em que importam: denso, em camadas, com becos estreitos e lajes ocupadas. A versão nova responde a três perguntas:

1. **Treinado só com imagens de computador, quanto um programa acha de pessoas em fotos reais?** E o que pesa mais: a inclinação da câmera, o tamanho da pessoa na foto ou a variedade das favelas simuladas?
2. **Quando já existem algumas fotos reais, as imagens de computador ainda ajudam?**
3. **Em que altura o programa separa quem carrega uma arma de quem carrega um objeto comum, e com que frequência confunde os dois?**

A resposta curta é a de setembro, medida com mais cuidado: a 150 metros, altura usual desses voos, ninguém mostrou que a distinção é possível; mais perto ela aparece, com erro alto, e descer não reduziu o erro.

## Por que não usamos fotos reais

Fotografar moradores do Jacarezinho sem consentimento, num território com histórico de violência policial, não é aceitável. Construímos então favelas no computador, uma maquete digital com seis tipos de tempo e pessoas geradas por programa, carregando uma de cinco armas, um de nove objetos do dia a dia (vassoura, cano, guarda-chuva fechado, entre outros) ou nada. Para as perguntas 1 e 2, o programa foi testado em fotos reais de um conjunto público de cenas urbanas densas, que não é favela. A pergunta 3 só pôde ser medida na maquete: não existe conjunto público de fotos aéreas com armas marcadas.

## Como ler os números: a faixa de confiança

Novidade desta versão: quase todo número vem com uma faixa, como "1,6% (de 1,4 a 2,1)". O teste usa 548 fotos reais; com outras fotos parecidas, o resultado mudaria um pouco. Refizemos a conta mil vezes, sorteando as fotos de novo, e a faixa mostra onde o resultado caiu em 95 de cada 100 sorteios. Se a faixa da diferença entre dois programas não inclui o zero, a diferença não vem do acaso das fotos. A faixa não mede o acaso do treino: para isso repetimos alguns treinos três vezes. E o artigo só chama de grande uma diferença acima de 30%.

## O detalhe que decide tudo: quantos pontinhos uma pessoa ocupa

Uma foto é feita de pontinhos (pixels). A 150 metros, com a câmera de referência, cada pontinho cobre 4,88 cm de chão e uma pessoa vista de cima ocupa 17,6 por 17,5 pontinhos, um grão de arroz na tela. Ali um fuzil vira um risco fino, igual a um cano: a informação não chega à imagem. A 75 metros a pessoa ocupa 6,4 vezes mais área. O que manda é quanto chão cabe em cada pontinho: a mesma câmera, a 150 metros com zoom de 4 vezes, chega à nitidez dos 75.

| Altura do drone | Pessoa na foto | Separa arma de objeto? |
|---|---|---|
| 150 m | 17,6 por 17,5 pontinhos | não medido: o único programa treinado ali achou 148 de 297 pessoas, menos da metade exigida antes do teste |
| 75 m | 47,6 por 41,7 pontinhos | em parte: marca como armados de 17% a 24% dos objetos comuns |
| 35 m | 121,8 por 103,1 pontinhos | em parte: marca 27%, e o erro não diminuiu |

## O que descobrimos, pergunta por pergunta

**1. Só com a maquete, o programa acha pessoas reais muito mal, e o que mais pesa é a inclinação da câmera.** A régua (o "teto") é um programa treinado com 1.106 fotos reais. Com a câmera apontada para baixo a 150 m, o programa da maquete alcança 1,6% do teto; com a câmera inclinada, 9,7%; na melhor configuração inclinada, com seis favelas simuladas, 15,3% na média de três treinos. Inclinar a câmera sobre a mesma favela multiplicou o resultado por 6,0 (faixa de 4,6 a 7,0), mas cada lado foi treinado uma vez só, então a faixa mede o acaso das fotos, não o do treino. Com o tamanho igualado (301 contra 300 pontinhos de área), o motivo provável é a forma: de cima, a pessoa é tão larga quanto comprida (proporção 0,98); nas fotos reais, cerca de duas vezes mais alta que larga (1,95 e 2,20). Seis favelas em vez de uma ajudaram menos: de 1,6% para 3,0% com a câmera vertical.

**2. Com algumas fotos reais, a maquete atrapalha um pouco: de forma consistente, mas modesta.** Com 324 ou 647 fotos reais (5% ou 10% do conjunto de treino), partir de um ponto genérico foi melhor que partir da maquete, por 15,8% e 12,1% em termos relativos, e melhor que misturar as duas fontes, por 13,8% e 5,2%. É consistente (com 5%, o pior dos três treinos genéricos superou o melhor dos três a partir da maquete), mas pequeno: entre 5 e 16%, longe dos 30%. Só se testou uma receita de ajuste, sem otimizá-la, e o sinal pode ser dela.

**3. Armado ou com objeto: o erro é alto, e chegar mais perto não o reduziu.** A 75 metros o programa marcou como armadas 24% das pessoas com objeto comum; a 35 metros, 27%. Para isolar a altura, a cena de 35 m foi refeita a 75 m, idêntica no resto (a "gêmea"). Em 80 cenas novas, o erro foi de 25% a 35 m contra 12,5% na gêmea, e essa direção se manteve em três treinos. Ajustar a exigência do alarme não resolve: nenhum ajuste levou o alarme falso abaixo de 9 em cada 100 objetos mantendo mais de 42 em cada 100 armados encontrados. O programa pode estar olhando o comprimento do que se carrega, não a forma da arma: as armas medem de 0,20 a 1,05 m, os objetos de 0,88 a 2,5 m, e o guarda-chuva fechado (0,88 m) é marcado como arma em 38% das vezes, contra 10% das vassouras e 11% dos canos. Também não é que o programa tenha decorado os modelos de arma: armas nunca vistas foram achadas tão bem quanto as conhecidas (46,6% contra 40,0%), e carregar objetos exatamente como armas não mudou o erro (13,7% contra 15,4%).

**Comparar por semelhança, sem detector, não separa arma de objeto.** Recortamos cada pessoa e a comparamos por semelhança com um programa genérico de imagens, sem treino. Numa escala em que 0,5 é cara ou coroa e 1 é separação perfeita, ficou entre 0,525 e 0,654 nas três alturas. Esse método só distingue quem carrega algo de quem não carrega nada.

**Luz e teto.** Na maquete, sol forte foi o pior tempo para achar pessoas e céu coberto o melhor, empatado com sol baixo; falta confirmar em foto real. E o teto é um pouco otimista: o programa de referência escolheu sua melhor versão olhando o próprio conjunto em que foi avaliado, como quem escolhe a prova olhando o gabarito.

## O que continua em aberto

Medir a 150 m com uma maquete grande o bastante; repetir o fator de 6,0 com mais treinos; testar outra receita de ajuste; testar em fotos públicas com câmera vertical; saber se o programa usa a forma da arma ou o comprimento do objeto. Nada sobre armas foi testado em foto real, e o modelo de morfologia vertical que motivou a escolha do Jacarezinho não foi construído. Qualquer imagem do território depende de revisão ética independente e de escuta dos moradores fora da polícia, que não aconteceram.

## O que isso significa

Dizer que um drone "identifica pessoas armadas" numa favela é algo que se checa antes de acreditar: basta perguntar altura, câmera e luz. Nas condições testadas, a capacidade ou não foi demonstrada ou marcaria como armado de um em seis a um em quatro moradores com um objeto comum. O artigo não recomenda voar sobre o Jacarezinho nem construir esse sistema: um sistema capaz da distinção e um sistema seguro de apontar para o Jacarezinho são coisas diferentes, e a segunda decisão cabe a um processo que inclua os moradores.
