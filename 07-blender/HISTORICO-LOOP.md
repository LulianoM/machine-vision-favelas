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
