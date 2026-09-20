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
