# Rubrica de fidelidade: favela vista de drone em nadir a 150 m

Criada em 2026-09-20 [DESKTOP] para dirigir o loop de melhoria de `scripts/gen_morro.py`.
Serve de criterio unico tanto para a autocritica quanto para o agente validador. Cada item vale
de 0 a 10 e tem um teste objetivo, para que a nota nao dependa de gosto.

Referencia declarada: fotografia aerea obliqua de favela carioca consolidada (tipologia
Alemao, Penha, Jacarezinho), mais fotografia de beco ao nivel do solo. As duas foram fornecidas
pelo autor em 2026-09-20 e NAO estao versionadas aqui (material de terceiros). O que esta
versionado e a descricao abaixo, que e o que o loop persegue.

## O que a referencia mostra, item a item

### 1. Densidade e vazio (peso alto)
Praticamente nao existe solo visivel entre edificacoes. O vazio aparece so como fresta de beco,
com 0,6 a 2,5 m, e raramente como travessa de 3 a 4 m. Nao ha recuo frontal, nao ha quintal,
nao ha estacionamento. **Teste:** fracao de pixel de solo exposto no quadro nadir abaixo de 8%.

### 2. Tamanho da edificacao
Lote tipico de 4 x 7 a 9 x 12 m. Num quadro de 187 x 105 m a contagem esperada passa de 500
edificacoes. **Teste:** area mediana da projecao de telhado entre 35 e 90 m2.

### 3. Altura e escalonamento
De 1 a 5 pavimentos, com vizinhos quase sempre de alturas diferentes, o que produz degrau de
laje constante. Casas na encosta acompanham o terreno, entao a cumeeira desenha a topografia.
**Teste:** desvio padrao da altura entre vizinhos imediatos acima de 2,5 m.

### 4. Paleta de cobertura (peso alto)
Na referencia dominam, nesta ordem: laje de concreto em cinza QUENTE (bege sujo), telha
ceramica laranja e terracota, branco caiado e azul forte (caixa d'agua, lona, laje pintada).
Verde e raro e, quando aparece, e vegetacao, nao telhado. Amarelo e rosa sao acentos pontuais.
**Teste:** nenhum telhado verde; laranja e terracota somam ao menos 25% da area de cobertura;
o cinza de laje tem matiz entre 30 e 60 graus (quente), nunca azulado.

### 5. Ausencia de grade
Nao existe alinhamento ortogonal legivel. As divisas mudam de angulo a cada poucas casas e os
becos serpenteiam. **Teste:** na FFT do mapa de ocupacao nao deve haver pico dominante em 0 e
90 graus; visualmente, nenhuma fileira reta com mais de 5 casas.

### 6. Cobertura habitada
Laje e area de uso: caixa d'agua (azul e preta), varal com roupa, casinha de escada, antena
parabolica, ferragem de espera, entulho, telha empilhada, cadeira, tanque. **Teste:** ao menos
70% das lajes com algum objeto; ao menos 3 tipos distintos visiveis no quadro.

### 7. Fiacao
Emaranhado aereo atravessando becos, com postes e catenarias visiveis em nadir como linhas
finas. **Teste:** presente, sem virar malha regular.

### 8. Luz e cor
Sol alto de dia claro do Rio. Sombra dura, beco em sombra profunda, laje estourando de claro.
Cor saturada, nao lavada, e branco de balanco correto, nao azulado. **Teste:** media do quadro
entre 90 e 140 em 8 bits; saturacao media acima de 0,25; sem dominante azul na sombra.

### 9. Mata
Vegetacao densa cercando o nucleo, encosta ingreme, copa fechada. Nao pode parecer gramado nem
anel regular de arvores. **Teste:** a mata ocupa borda do quadro sem formar anel de raio
constante.

### 10. Micro-relevo da edificacao
Aresta com quebra (nunca 90 graus perfeito), mureta de laje, caixa de escada, agua furtada,
beiral, platibanda. Vista de cima o telhado nao e um retangulo liso.
**Teste:** nenhuma face de telhado maior que 25 m2 totalmente lisa.

## Como pontuar

Nota final e a media ponderada, com peso 2 nos itens 1, 4 e 5 e peso 1 nos demais.
Abaixo de 7,0 o render ainda nao serve de figura para o artigo.

## Historico do loop

Ver `HISTORICO-LOOP.md`.
