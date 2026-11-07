# Histórico do loop de fidelidade

Registro das iterações de `scripts/gen_morro.py` contra `RUBRICA-FIDELIDADE.md`.
Cada entrada diz o que mudou, por que, e o que o render revelou. Iniciado em 2026-09-20 [DESKTOP].

Câmera alvo em todas as iterações: `CAM_NADIR_150m_Z30`, que reproduz a Zenmuse Z30 do voo real
de 2022 (1920x1080, nadir, 150 m). Enquadra 187 x 105 m a 9,8 cm/px; pessoa de 1,7 m ocupa 17 px.

Nenhuma imagem desta linha de trabalho usa dado da PCERJ: geometria é procedural e os materiais
vêm do Poly Haven (CC0). Por isso, ao contrário dos braços `odm` e `cid150`, estas figuras podem
ilustrar o artigo.

## v0, primeira tentativa

Loteamento por subdivisão binária única, paleta de telhado lida da foto aérea de referência,
morro com mata em volta, céu Nishita como única fonte de luz.

O que o render revelou:
- Dominante azul em tudo. O céu Nishita limpo, usado como único ambiente, pinta toda a sombra de
  azul. A cena ficou com cara de maquete fria.
- Lote grande demais, cerca de 12 x 15 m. Leu como conjunto habitacional, não como favela.
- Paleta lavada: o tingimento fraco sobre textura cinza apagou as cores.

## v1, luz e escala

- Separado o que a câmera VÊ do que ILUMINA, com nó Light Path: céu para raio de câmera,
  ambiente neutro levemente quente para iluminação. Some a dominante azul.
- Cinzas de laje trocados para tons QUENTES (bege sujo). Cinza frio era o erro central de cor.
- Lote reduzido para 22 a 62 m², mínimo de 3,6 m de lado.
- Acrescentado telhado de duas águas, que a foto de referência mostra em boa parte das casas.

Resultado: cor e densidade muito melhores, mas ainda escuro e com caixa d'água em excesso.

## v2, bairros com orientação própria

Mudança estrutural. Uma subdivisão binária única, por mais deformada que seja, deixa fileiras
retas legíveis de 10 e 20 casas, e esse é o sinal mais forte de geração procedural numa vista de
cima. Passou a haver 9 bairros, cada um com ângulo próprio, separados por diagrama de Voronoi.
Favela consolidada cresce por núcleos que se encontram em ângulo, e é isso que está reproduzido.

Também nesta rodada:
- Telhado verde removido da paleta. Na referência, verde é vegetação, nunca cobertura.
- Número de pavimentos passou a vir de um campo de ruído de baixa frequência, para haver zonas
  altas e zonas baixas em vez de altura sorteada casa a casa.
- Objetos de laje ampliados: parabólica, telha empilhada, entulho, tanque de lavar.
- Chão escurecido para cimento sujo. Chão claro virava mancha branca vista de cima.

Primeira tentativa abriu vazios grandes na divisa entre bairros (só 31% construído). Corrigido
reduzindo a folga de descarte de 2,6 para 0,6 m e aumentando a proporção de parede geminada.

## v3, puxadinho

O ganho isolado mais forte até aqui. A casa de favela quase nunca é um prisma único: o pavimento
de cima é menor que o de baixo e fica deslocado, deixando um pedaço de laje descoberto ao lado.
Vista de cima isso vira o recorte em L que define a textura da favela. Sem ele a mancha fica com
cara de conjunto de caixas, que era o problema que sobrava em v2.

55% das casas com 2 ou mais pavimentos passaram a ter esse escalonamento, e tudo que vive na
cobertura (caixa d'água, varal, mureta, entulho) passou a ser colocado sobre a laje DE CIMA.

Estado: 430 edificações, 204 mil faces, 37% do recorte construído.

## Pendente

- Validação independente por agente, contra a rubrica, com medição numérica.
- Brilho médio ainda em 78 de 255, abaixo da faixa de 90 a 140 que a rubrica pede.
- Pessoas e anotação de bounding box: `people_mpfb.py` e a projeção de vértice com ray cast de
  oclusão ainda não estão plugados neste gerador.

## v4 a v7, dirigidas por validação independente

Dois agentes validadores avaliaram contra a rubrica com medição numérica, não com opinião.
Notas: **4,5** na linha de base (v0) e **6,3** em v3. A rubrica pede 7,0 para servir de figura.

### O erro de albedo, achado pelo validador

Diagnóstico que eu não tinha feito: a cadeia `tint MULTIPLY` sobre a difusa já colorida,
seguida de dois `_grime MULTIPLY`, multiplicava dois albedos e esmagava toda cor por um fator
de 3 a 5 vezes. Branco caiado pretendido em sRGB 226 saía em 112. A cena inteira lia marrom.

Correção: a textura passou a entrar só como MODULAÇÃO DE LUMINÂNCIA (0,78 a 1,18, via RGBToBW
mais Map Range) sobre a cor pretendida, e `_grime` passou de MULTIPLY para MIX fraco. Assim o
albedo final cai de fato na cor que a paleta pediu.

### O segundo erro, meu, ao corrigir o primeiro

Com o albedo certo, usei as cores lidas da FOTO como albedo. Cor de foto já é resultado
iluminado, não albedo de superfície: concreto reflete de 0,20 a 0,35, não 0,50. Todo telhado
estourou de branco. Entrou o fator `ALB`, e a luz foi recalibrada medindo em vez de chutar
(sol 3,3, ambiente quase neutro 1,0, exposição 0,0).

### Piso da sombra

O validador mediu sombra em RGB 10,3 / 4,7 / 1,9, ou seja B/R de 0,18: sombra cor de tijolo,
sem nenhuma componente de céu, e sem informação dentro dela. Nenhum sensor real entrega isso.
Subir o preenchimento ambiente e torná-lo quase neutro levou o B/R para 0,47 e a fração do
quadro abaixo de 25 de 20,5% para 12%.

### Medições atuais (v7)

| Métrica | Alvo da rubrica | v0 | v3 | v7 |
|---|---|---|---|---|
| Luminância média (8 bits) | 90 a 140 | 56,4 | 80,9 | 106,6 |
| Saturação média | acima de 0,25 | 0,52 | 0,47 | 0,27 |
| Fração abaixo de 25 | baixa | 29,4% | 20,5% | 12,1% |
| B/R na sombra profunda | perto de 1 | 0,18 | 0,18 | 0,47 |
| Telhado verde | zero | presente | 0,00% | 0,00% |

Outras mudanças de v4 a v7: caixa d'água virou cilindro com base de alvenaria e tampa; antena
parabólica virou disco inclinado; varal com número, posição e tamanho de peça aleatórios (o
motivo de 7 retângulos igualmente espaçados, repetido idêntico, foi apontado como sinal de
"kit de peças"); lote girado em ±0,17 rad em torno do centroide; warp de 9 m em comprimento de
onda de 38 m em vez de 3,2 m em 85 m; corte do BSP enviesado para lote estreito e profundo;
copa isolada dentro do miolo; borda de mata mais irregular.

## v8, o bug do branco escondido

Terceira validação deu **5,8**, ou seja, o saldo de v4 a v7 foi negativo: o ganho de 3 pontos em
"ausência de grade" (peso 2) foi anulado pela perda de 4,5 em "paleta" (peso 2). A rodada trocou
o problema da grade pelo problema da cor.

O validador achou um bug de código, não de parâmetro. Em `_grime`, o elemento 1 dos dois
ColorRamp recebe `.position` mas nunca recebe `.color`, então fica no branco padrão do Blender.
Herdado de `build_cidade.py`, onde era inofensivo porque o nó era MULTIPLY e branco é a
identidade da multiplicação. Ao trocar para MIX, o mesmo branco virou 30% de lavagem branca no
albedo de TODO material da cena. Era isso que deixava telhado terracota em rosa salmão, e era
isso que clareava o chão do beco, fazendo a fresta escura sumir.

Também foi refeito o orçamento de luz. Com sol 3,3 e ambiente branco 1,0, o ambiente respondia
por 51% da luz da laje e a razão sol/céu era 0,96 para 1, quando um dia claro do Rio a 66 graus
dá de 5 para 1 a 7 para 1. Sol foi para 6,5, ambiente para 0,54 e cor do ambiente para azul de
céu (0,72 / 0,80 / 1,00), que é o preenchimento fisicamente correto.

Acrescentada a quebra de nível na laje: uma metade da cobertura fica de 12 a 30 cm acima da
outra, com material diferente. Face de telhado lisa era o item pior avaliado (2,5 de 10), com
34% do quadro em manchas homogêneas acima de 25 m². Platibanda passou de 46% para 80% das lajes.

### Medições v8

| Métrica | Alvo | v0 | v3 | v7 | v8 |
|---|---|---|---|---|---|
| Luminância média | 90 a 140 | 56,4 | 80,9 | 106,6 | 99,6 |
| Contraste p90/p10 (paradas) | 3,5 a 4,5 | | | 2,5 | 4,11 |
| Fração abaixo de 25 | baixa | 29,4% | 20,5% | 12,1% | 17,4% |
| Edificações no quadro | acima de 500 | | 430 | 282 | 420 |
| Anisotropia de aresta em 0 e 90 graus | 1,0 | 4,35x | 1,37x | 0,90x | |

### Nota sobre um limite do tone mapper

A rubrica pede terracota com saturação acima de 0,45 em ao menos parte da cobertura. O material
sai do shader com saturação 0,97 no linear, e chega ao pixel abaixo de 0,45 porque o AgX
dessatura realce por construção. Trocar para o look "Punchy" recupera saturação (laranja de 9%
para 19%) ao custo de esmagar a média para 73 e levar 28% do quadro abaixo de 25. É um
compromisso real do tone mapper, não um defeito do gerador, e está registrado aqui para não ser
perseguido de novo nas próximas rodadas.

## v9, o segundo ramo morto e a névoa aérea

Quarta validação: **6,6** na régua do avaliador, que ele calibrou como **+0,5 real** sobre a
rodada anterior reavaliando v3 e v7 com o mesmo critério. Primeiro saldo positivo desde v3.

### Segundo bug de código achado pela validação

Ao subir a platibanda de 46% para 80% eu escrevi `if r_ < 0.80:` antes de `elif r_ < 0.70:`.
Como 0,70 é menor que 0,80, o ramo de telhado de duas águas ficou **inalcançável**: 0,0% de
telha inclinada medida, contra 24% em v7. É o plano inclinado que devolve laranja vivo em
nadir, então isso derrubou sozinho o item de paleta, que tem peso 2. Revertido para 0,44.

Lição que vale registrar: nas duas vezes em que o loop andou para trás, a causa foi um bug de
código que a inspeção visual não pega (ColorRamp sem cor, ramo inalcançável), não uma escolha
estética errada. Validação com medição numérica é o que encontra isso.

### Névoa aérea

Não havia nada nos 150 m de ar entre câmera e solo. Consequência medida: 6,8 paradas entre sol
e sombra, com 17% do quadro sem informação nenhuma dentro. Ar úmido do Rio põe de 2 a 4% de luz
espalhada dentro de toda sombra a essa distância.

Detalhe que custou uma tentativa: volume no World é ilimitado, então o raio do sol atravessa
distância infinita de meio, a transmitância vai a zero e a cena apaga por completo. O volume
tem de ir numa CAIXA que envolve o sítio.

### Outras correções da rodada

- Tampa da caixa d'água passou a ter a cor do corpo. Em nadir só a tampa aparece, então 100%
  das caixas viravam disco escuro idêntico e os 62% de caixa azul nunca eram vistos. Foi
  apontado como o sinal mais forte de cena sintética: 212 discos iguais, um a cada 93 m².
- Três volumes de caixa d'água (310 L, 500 L, 1000 L) em vez de um.
- Fiação: seção de 2,2 cm dava 0,45 px a 9,74 cm/px, ou seja sub-pixel, e a fiação simplesmente
  não aparecia (zero estruturas lineares detectadas). Passou para 16 cm, que é a seção real de
  um feixe, e passou a ser ancorada no telhado. Antes, 41% dos fios nasciam abaixo da laje
  vizinha e ficavam presos dentro do prédio.

### Medições v9

| Métrica | Alvo | v7 | v8 | v9 |
|---|---|---|---|---|
| Luminância média | 90 a 140 | 106,6 | 99,6 | 102,6 |
| Contraste p90/p10 (paradas) | 3,5 a 4,5 | 2,5 | 5,43 | **3,53** |
| B/R na sombra profunda | perto de 1 | 0,47 | 0,89 | **0,87** |
| Fração abaixo de 25 | baixa | 12,1% | 17,0% | 15,4% |
| Telhado de duas águas | presente | 24% | **0%** | 26% |
| Edificações no quadro | acima de 500 | 282 | 420 | 421 |

### Tensão irredutível registrada pela validação

Os dois subtestes do item 2 da rubrica são incompatíveis entre si: 500 casas de 50 m² dão
25.000 m² num quadro de 19.635 m². Não dá para perseguir os dois ao mesmo tempo. A rubrica
precisa ser corrigida numa próxima revisão.

## v10, o terceiro bug da mesma família

Quinta validação: **6,7**, ganho de apenas +0,1 sobre 6,6. O único ganho grande (tampa da caixa
d'água, +1,5) foi cancelado por uma perda igual em micro-relevo, porque destravar o telhado de
duas águas devolveu planos grandes e lisos.

### Terceiro bug de código

O laço da fiação sorteia um par de casas na elipse e filtra por distância entre 5 e 22 m. Esse
filtro aceita 7,4% das tentativas, então `range(260)` construía cerca de **19 fios, não 220**.
Área total de fio no quadro: 0,24%, contra 0,98% só das tampas de caixa d'água. Por isso o
detector de cume achava ZERO estruturas lineares: a fiação simplesmente não estava lá.

Agravante: o `print` de diagnóstico reportava edificações, caixas d'água, varais e faces, mas
não fio. O bug era invisível também no log. Agora reporta, e o número saiu de 19 para 231.

Esse é o terceiro caso, e os três têm a mesma forma: o parâmetro estava certo, o código não
fazia o que o parâmetro dizia. ColorRamp sem cor, ramo inalcançável, filtro que descarta 93%.
Nenhum dos três é pego por inspeção visual do render, e os três foram pegos por medição.

### Contraste, e por que névoa não é a resposta inteira

A névoa levanta a sombra mas dessatura o quadro por igual, e saturação é um teste da rubrica.
A 2,4e-4 o meio-tom foi a 42,9% e o escuro a 1,2%, mas a saturação caiu para 0,151. A solução
foi levantar a sombra pela RAZÃO SOL/CÉU (física da cena: sol de 6,5 para 5,0, ambiente de 0,54
para 0,78) e deixar a névoa em 0,9e-4 só para o airlight.

### Medições v10

| Métrica | Alvo | v8 | v9 | v10 |
|---|---|---|---|---|
| Luminância média | 90 a 140 | 99,6 | 102,6 | 92,7 |
| Contraste p90/p10 | 3,5 a 4,5 | 5,45 | 5,20 | 3,09 |
| B/R na sombra | perto de 1 | 0,89 | 1,02 | **0,98** |
| Meio-tom L 60 a 150 | 45 a 60% | 23,9% | 25,1% | **37,5%** |
| Fração abaixo de 25 | baixa | 17,0% | 15,4% | 13,6% |
| Fios construídos | centenas | 19 | 19 | **231** |
| Laranja S acima de 0,25 | alto | | | 16,7% |

### O que ainda reprova

Saturação média em 0,221, abaixo do piso de 0,25 da rubrica. É o item que resiste há três
rodadas. A causa não é a paleta (a cerâmica sai do shader com saturação 0,97 no linear) e não é
só o tone mapper: é a combinação de AgX com uma paleta cujo maior peso é cinza quente de laje,
que é de fato pouco saturado na referência. A próxima revisão da rubrica precisa decidir se
0,25 é o número certo para uma cena cuja cor dominante correta é cinza.

## Achado do primeiro dataset: o alvo em nadir é menor do que o projeto assumia

Medido em 621 caixas de 40 imagens a 1920x1080, câmera Z30 nadir a 150 m (9,76 cm/px):

| Dimensão da caixa | p5 | mediana | p95 | máximo |
|---|---|---|---|---|
| Largura | 5,0 px | 8,9 px | 13,4 px | 17,3 px |
| Altura | 4,9 px | 8,5 px | 12,6 px | 20,5 px |
| Maior lado | 6,1 px | **10,0 px** | 14,0 px | 20,5 px |

**19% das caixas têm o maior lado abaixo de 8 px, que é o menor stride do YOLO. 83% ficam
abaixo de 12 px. A área mediana da caixa é de 74 px².**

### Por que o número de 17 px estava errado

O gerador vinha imprimindo "pessoa de 1,7 m ocupa 17 px", e esse número é verdadeiro para
câmera OBLÍQUA e falso para nadir. Em nadir, a altura é justamente a dimensão que não se
projeta. O que a câmera vê de cima é a planta da pessoa:

| O que se mede | Extensão | Pixel a 150 m |
|---|---|---|
| Altura de pé | 1,70 m | 17,4 px (só em câmera oblíqua) |
| Ombro a ombro | 0,48 m | **4,9 px** |
| Planta cabeça e ombro | 0,62 m | **6,4 px** |

A mediana medida de 10 px fica acima da planta pura porque a anotação é amodal e inclui braço
estendido, pose sentada ou deitada, e a sombra própria não entra mas o membro fora do tronco
entra. Ainda assim, a ordem de grandeza é a da planta, não a da altura.

### O que isso significa para o artigo

1. **A câmera real de 2022 tem o mesmo limite.** O voo da PCERJ foi nadir a 150 m com a mesma
   Zenmuse Z30. Não é uma limitação do sintético, é uma limitação do dado real que o artigo
   pretende usar como alvo de sim-to-real.
2. **O ladrilhamento não resolve sozinho.** O ganho medido de mAP50 de 0,116 para 0,561 veio de
   parar de reduzir a imagem, preservando o tamanho nativo do alvo. Mas preservar 10 px continua
   sendo 10 px, e 19% do conjunto fica abaixo de um único passo da rede.
3. **Reforça a recomendação do item 3 de `docs/DIVERGENCIAS.md`.** Distinguir pessoa armada de
   desarmada exige resolver a arma dentro de uma caixa cuja mediana é de 10 px por 7 px. Isso
   não é plausível, e reportar acurácia de classe nesse regime seria exatamente o salto
   metodológico que o artigo critica.
4. **É argumento técnico para a câmera oblíqua**, que até aqui era defendida só pela fachada. A
   oblíqua é o único ângulo em que a dimensão de 1,70 m projeta em pixel.

Isso não estava em nenhum lugar do projeto e não aparece olhando para o render: só apareceu ao
medir a distribuição de tamanho de caixa do dataset gerado.

## Dataset com os seis regimes de tempo, e um resultado contraintuitivo

48 imagens, 8 por regime, 684 caixas, 1920x1080, Z30 nadir a 150 m.

| Clima | Imagens | Caixas | Caixas por imagem | Visibilidade média |
|---|---|---|---|---|
| sol_duro | 8 | 113 | 14,1 | 0,87 |
| sol_baixo | 8 | 117 | 14,6 | 0,86 |
| nublado | 8 | 122 | 15,2 | 0,88 |
| neblina | 8 | 113 | 14,1 | 0,86 |
| encoberto | 8 | 91 | 11,4 | 0,87 |
| chuva | 8 | 128 | 16,0 | 0,84 |

### O contraste entre pessoa e fundo, medido

Para cada caixa, a diferença entre a luminância média dentro da caixa e a de um anel de 6 px em
volta, e essa diferença dividida pelo desvio padrão do próprio anel (ou seja, contraste sobre
desordem local, que é o que o detector de fato enfrenta).

| Clima | Diferença absoluta (DN) | Contraste sobre ruído |
|---|---|---|
| sol_duro | **16,6** | **0,54** |
| nublado | 15,3 | **0,83** |
| neblina | 10,6 | 0,77 |
| encoberto | 9,8 | 0,71 |
| sol_baixo | 9,7 | 0,73 |
| chuva | **6,6** | 0,67 |

**O sol duro dá a maior diferença absoluta e o PIOR contraste sobre ruído de todos os regimes.**
A razão é que sob sol duro o próprio fundo fica cheio de sombra dura de caixa d'água, mureta,
varal e fiação, então o desvio local do fundo dispara e a pessoa deixa de se destacar da
desordem. Sob céu encoberto o fundo é liso, e uma diferença menor é mais detectável.

Isso gera uma previsão testável e contraintuitiva: **o detector deve ir melhor em nublado do que
em sol duro**, ao contrário do que a intuição sugere. Vale medir quando o treino rodar, e se
confirmar é resultado para o artigo, porque contraria a escolha usual de voar em dia claro.

A chuva é o pior caso em termos absolutos, com 6,6 DN, ou seja 2,5 vezes menos que o sol duro.

## Primeiro sim-to-real do projeto, e por que o número não vale ainda

Treino em `ds_morro_clima_tiles` (335 ladrilhos de 640 px, 1198 caixas, YOLO11s, 120 épocas) e
avaliação em três conjuntos. Resultado em `06-resultados/sim2real_morro_v1.json`:

| Conjunto | P | R | mAP50 | mAP50-95 |
|---|---|---|---|---|
| sintético | 0,109 | 0,148 | 0,0769 | 0,0189 |
| real (VisDrone val) | 0,038 | 0,031 | 0,0055 | 0,0020 |
| real_gsd (escala casada) | 0,041 | 0,037 | 0,0061 | 0,0009 |

**Estes não são números sobre sim-to-real.** O modelo falhou no próprio mundo (0,077 contra
0,676 do melhor run anterior), e não se mede transferência de um modelo que não aprendeu.

### A causa, medida

| Dataset | Resolução | Imagens de treino | GSD | Alvo mediana | Abaixo de 8 px |
|---|---|---|---|---|---|
| `dataset_cid150` | 3840x2160 | 473 | 4,88 cm/px | **24,6 px** | 0% |
| `dataset_v3` | 3840x2160 | 103 | 3,25 cm/px | 28,0 px | 0% |
| `ds_morro_clima` | 1920x1080 | 40 | 9,76 cm/px | **10,1 px** | **25%** |

Dois erros meus, somados:

1. **Renderizei em 1920x1080 e não em 4K.** A câmera Z30 real grava 1080p, então usar 1920x1080
   parecia o mais fiel. Mas o que decide se a rede enxerga o alvo é a GSD, e reduzir a resolução
   pela metade dobra a GSD e corta o alvo pela metade: de 24,6 px para 10,1 px, com 25% das
   caixas caindo abaixo do menor stride do YOLO. Os braços anteriores do projeto renderizavam em
   4K justamente por isso, e eu não verifiquei antes de escolher.
2. **40 imagens de treino contra 473.** Comparei por número de CAIXAS (684 contra 671 do `v3`) e
   concluí que era comparável. Não é: caixa em imagem repetida não traz a variação de cena que o
   treino precisa.

### Correção a uma afirmação anterior deste documento

Eu havia registrado que o VisDrone tem alvo 2,49 vezes maior que o nosso sintético, e tratei
isso como um domain shift inerente de altitude entre o projeto e o benchmark. **Está errado.** O
alvo mediano do `cid150` é de 24,6 px e o do VisDrone val é de 25,0 px: praticamente idênticos.
A diferença de 2,49 vezes era artefato da MINHA escolha de resolução, não propriedade do
projeto. O controle de escala em `avalia_sim2real.py` continua valendo como verificação, mas
deixa de ser necessário para o braço em 4K.
