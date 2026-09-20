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
**Teste:** nenhum telhado verde; laranja e terracota entre 12 e 30% da area de cobertura;
o cinza de laje tem matiz entre 30 e 60 graus (quente), nunca azulado; area de azul forte
(S acima de 0,35) abaixo de 1,2% do quadro.

> **Correcao de 2026-09-20.** O piso de 25% de laranja tambem estava acima da referencia: a
> fotogrametria real da 12,4%. Faixa corrigida para 12 a 30%. O limite de azul e novo, e veio da
> medicao: o render tinha 3,57% de azul forte contra 0,80% da referencia, 4,5 vezes demais.

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
finas. **Teste:** Hough sobre mascara de limiar LOCAL restrita a estrutura fina, contando segmentos
acima de 4 m e acima de 8 m; e nenhuma laje com mais de 3 fios convergentes no mesmo ponto.

> **Correcao de 2026-09-20.** O teste anterior usava detector de cume com limiar GLOBAL, que e
> dominado pelas sombras de beco e reportava zero segmentos mesmo quando a fiacao existia. Nao
> era medida de ausencia de fio, era piso de falso-negativo: ele deu praticamente o mesmo
> resultado em v9 (19 fios construidos) e v10 (231 fios).

### 8. Luz e cor
Sol alto de dia claro do Rio. Sombra dura, beco em sombra profunda, laje estourando de claro.
Branco de balanco correto, nao azulado. **Teste:** media do quadro entre 90 e 140 em 8 bits;
contraste entre 3,5 e 4,5 paradas MEDIDO EM CENA LINEAR sobre o construido (ver nota de régua
abaixo); B/R na sombra profunda entre 0,95 e 1,05; saturacao media do quadro entre 0,14 e 0,24;
saturacao da cobertura ao sol entre 0,09 e 0,18; fracao acromatica (S abaixo de 0,12) da
cobertura entre 55 e 75%.

> **Correcao de 2026-09-20.** A versao anterior deste teste exigia saturacao media ACIMA de
> 0,25. Isso estava errado. Medindo o proprio material de referencia do projeto com o mesmo
> calculo, a fotogrametria de favela real da saturacao de 0,098 (mapa obliquo) a 0,168 (recortes
> de voo), e na foto aerea real so 7,3% dos pixels de cobertura passam de S = 0,25. O piso de
> 0,25 foi calibrado contra as versoes v0 e v3 do gerador, que eram justamente as que sofriam do
> bug de albedo duplicado corrigido em v4: a regua foi escrita olhando para uma imagem quebrada.
> Perseguir 0,25 empurrava o gerador para LONGE da referencia. Uma cena cuja cobertura e de 70 a
> 76% cinza de laje nao pode ter saturacao media de 0,25.

### 9. Mata
Vegetacao densa cercando o nucleo, encosta ingreme, copa fechada. Nao pode parecer gramado nem
anel regular de arvores. **Teste:** a mata ocupa borda do quadro sem formar anel de raio
constante.

### 10. Micro-relevo da edificacao
Aresta com quebra (nunca 90 graus perfeito), mureta de laje, caixa de escada, agua furtada,
beiral, platibanda. Vista de cima o telhado nao e um retangulo liso.
**Teste:** nenhuma face de telhado maior que 25 m2 totalmente lisa.

## Nota de régua: em que espaço medir

Contraste tem de ser medido em CENA LINEAR (passando o pixel por sRGB inverso) e restrito ao
construído. Medir `log2(p90/p10)` direto em DN de tela da um numero sistematicamente menor e
NAO comparavel ao alvo: na mesma imagem, 3,09 em DN corresponde a 4,87 em cena linear. Errar
isso faz um item que reprova parecer que passa.

## Como pontuar

Nota final e a media ponderada, com peso 2 nos itens 1, 4 e 5 e peso 1 nos demais.
Abaixo de 7,0 o render ainda nao serve de figura para o artigo.

## Historico do loop

Ver `HISTORICO-LOOP.md`.
