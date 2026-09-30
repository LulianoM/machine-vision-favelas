# Dá para ver de cima se alguém está armado? O que o nosso artigo descobriu

*Resumo simplificado, para leitura sem conhecimento técnico. Versão de 30 de setembro de 2026.*

## A pergunta

Cada vez mais se fala em usar drones para vigiar territórios e, em particular, em sistemas que "reconhecem uma pessoa armada" a partir do ar. O que quase nunca se diz é a que altura, com que câmera e em que luz isso seria possível. O nosso artigo faz exatamente essa pergunta, tomando o Jacarezinho, no Rio, como o tipo de território em que ela importa: um lugar denso, construído em camadas, com becos estreitos e lajes ocupadas.

A resposta curta: na altura em que esses drones costumam voar, cerca de 150 metros, ninguém mostrou que a distinção é possível, e há uma razão simples para isso, explicada abaixo. Mais perto do chão a distinção passa a existir, mas com um erro alto: cerca de uma em cada quatro pessoas carregando uma vassoura ou um cano é marcada como armada.

## Por que não usamos fotos reais

Para ensinar um computador a reconhecer alguma coisa é preciso mostrar milhares de exemplos. Fotografar moradores do Jacarezinho de cima, sem consentimento, num território com histórico de violência policial, não é aceitável, e o artigo assume isso como regra, não como obstáculo. Em vez de fotos, construímos uma favela no computador, uma espécie de maquete digital: casas coladas umas nas outras, becos, lajes com caixas d'água e varais, fios, seis tipos de tempo (sol forte, sol baixo, nublado, neblina, céu fechado, chuva) e pessoas geradas por programa, algumas com armas, outras com objetos do dia a dia. A maquete não copia o Jacarezinho; imita o tipo de tecido urbano.

Com essa maquete, "fotografamos" milhares de cenas de cima, com uma câmera virtual igual à de um drone real, e treinamos o programa detector. Depois testamos o que ele aprendeu.

## O detalhe que decide tudo: quantos pontinhos uma pessoa ocupa

Uma foto é feita de pontinhos (pixels). A 150 metros de altura, com uma boa câmera de drone, uma pessoa vista de cima ocupa um quadrado de cerca de 17 por 17 pontinhos. Isso é mais ou menos o tamanho de um grão de arroz numa tela de computador. Dentro desse grão, um fuzil vira um risco de um ou dois pontinhos de largura. Não há como dizer se aquele risco é um fuzil, um cano ou o cabo de uma vassoura. Não é falta de um programa melhor: a informação simplesmente não chega à imagem.

Se o drone desce para 75 metros, a pessoa ocupa quatro vezes mais área na foto; a 35 metros, quase cinquenta vezes mais. Aí a pergunta deixa de ser impossível e vira uma pergunta que se pode medir.

| Altura do drone | Tamanho de uma pessoa na foto | Dá para ver a forma de uma arma? |
|---|---|---|
| 150 m (o padrão dos voos) | cerca de 17 por 17 pontinhos | não; o programa treinado nessa altura não achou nem metade das pessoas |
| 75 m | cerca de 48 por 42 pontinhos | em parte: uma em cada quatro pessoas com objeto comum é marcada como armada |
| 35 m | cerca de 122 por 103 pontinhos | em parte: o erro não diminui, continua em uma em cada quatro |

## O que fizemos para não nos enganar

Num mundo de computador é fácil "vencer" sem querer: se todas as armas fossem iguais e ninguém carregasse mais nada, o programa aprenderia a reconhecer o boneco da arma, não uma arma. Por isso a maquete tem cinco armas diferentes e nove objetos parecidos com armas quando vistos de cima (vassoura, rodo, cano, vergalhão, tábua, guarda-chuva fechado, enxada, tapete enrolado, mangueira), com as mesmas cores e carregados nas mesmas posições. O guarda-chuva fechado, com 88 centímetros e escuro, é o objeto que mais engana o programa.

Também fixamos, antes de rodar cada teste, o que contaria como resultado e o que faria a afirmação cair. E repetimos os treinos importantes três vezes, para ver se o resultado dependia do acaso.

## O que descobrimos, em cinco pontos

1. **Treinado só na maquete, o programa reconhece pessoas em fotos reais muito mal.** Comparado com um programa treinado com fotos reais de drone (de um conjunto público de outra cidade, não de uma favela), ele alcança 1,6% do desempenho quando a câmera aponta para baixo. Inclinando a câmera, como no conjunto público, chega a 15%. Ou seja, a posição da câmera pesa mais do que o realismo da maquete.

2. **Com algumas fotos reais, a maquete não ajuda; atrapalha um pouco.** Quando demos ao programa 5% ou 10% das fotos reais, começar do treino sintético foi pior do que começar do zero, e misturar as duas coisas também foi pior. Isso contraria o que parte da literatura promete, e o artigo diz isso claramente.

3. **Armado ou desarmado: o erro é alto e não melhora descendo.** A 75 metros, o programa chama de "armada" cerca de 24% das pessoas que carregam um objeto comum; a 35 metros, 27%. Testamos com um corpus idêntico em tudo menos a altura e o resultado se repetiu em 80 cenas novas e em três treinos: ver mais perto não reduziu a confusão.

4. **Sol forte é o pior tempo para essa tarefa.** Parece estranho, mas faz sentido: com sol a pino, cada caixa d'água, parapeito e varal projeta uma sombra dura no telhado, e a pessoa se perde no meio das sombras. Com céu coberto o fundo fica mais liso e a pessoa se destaca. As normas de levantamento aéreo pedem justamente céu limpo, para outro fim.

5. **A 150 metros, nem conseguimos medir.** O único programa treinado nessa altura para separar armados de desarmados não achou nem metade das pessoas, abaixo do limite que tínhamos fixado antes. Por isso o artigo não apresenta nenhum número de acerto nessa altura: a ausência da capacidade é argumentada pelo tamanho da pessoa na foto, não medida.

## O que isso significa

Quando alguém afirmar que um sistema de drone "identifica pessoas armadas" numa favela, essa afirmação pode ser checada antes de ser acreditada: basta perguntar a altura do voo, a câmera e a luz. Nas condições que testamos, a capacidade ou não existe ou vem junto com um erro que marcaria como armado um morador em cada quatro que carrega uma vassoura. Esse erro é a forma concreta do risco de uso indevido que o artigo discute.

O artigo não recomenda voar sobre o Jacarezinho nem construir esse sistema. Ele diz onde a capacidade foi medida, onde foi apenas argumentada e o que seria preciso para mostrá-la. Dizer em que condições uma capacidade não foi demonstrada é uma contribuição tão útil quanto demonstrar uma que existe, e, neste assunto, a mais útil das duas.

## Em uma frase

Ver de cima se uma pessoa está armada depende primeiro de quantos pontinhos ela ocupa na foto, e na altura em que os drones voam ela ocupa poucos demais; mais perto a distinção aparece, mas erra uma em cada quatro vezes, e nenhuma quantidade de realismo na maquete muda isso.
