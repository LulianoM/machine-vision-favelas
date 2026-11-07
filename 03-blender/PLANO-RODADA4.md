# Rodada 4: plano, critérios fixados antes e custo

Pedido do autor em 27/09: rodar o pacote recomendado para amarrar o artigo. Este arquivo foi
versionado antes do primeiro resultado da rodada. As regras abaixo são as que
`06-resultados/rodada4_criterios.py` executa. Qualquer mudança de regra depois disso tem de dizer
que veio depois.

Cadeia: `03-blender/scripts/rodada4.py`, com trava, retomada e supervisor, no molde da rodada 3.

- **Supervisor:** `supervisiona_rodada4.py`, aberto por `retoma_rodada4.cmd` e por um atalho na
  pasta Inicializar.
- **Pausa:** `pausa_rodada4.py pausa` e `pausa_rodada4.py retoma`.
- **Retrato:** `status_rodada4.py`.

Receita de treino igual à de todos os braços:

- YOLO11s, imgsz 1280, lote 6, AdamW automático, paciência de 15 épocas;
- 60 épocas nos braços sintéticos e 30 no ajuste fino;
- ladrilhos de 1280 px com sobreposição de 0,2.

## O que cada grupo fecha

| Grupo | O que roda | Seção que fecha |
|---|---|---|
| K | Avaliações sem treino. VisDrone pela regra oficial das regiões ignoradas e a IoU 0,50, 0,60 e 0,75 nos nove modelos do artigo; confusão armada a IoU 0,60 e 0,75; escala casada pelo lado maior; instâncias dos val armados | 10.6 (convenção de anotação), 10.2, comparação com Kiefer |
| H | Gêmeo do teste de arma inédita (50 quadros a 75 m, semente 47) com o objeto confundível carregado como arma | 9.5 (a taxa de objeto chamado de arma é limite inferior) |
| F | Sintético e real no mesmo treino: S-oblique-six mais 5% e mais 10% do VisDrone, a partir do COCO | 9.4 e proposta da seção 6 |
| E | Gêmeo do corpus de 35 m renderizado a 150 m (200 quadros, 3 classes), treino e confusão | 11.5 e 10.7 (a ausência a 150 m hoje é argumentada) |
| I | 80 quadros novos a 35 m (índices 200 a 279 da semente 43) e seus gêmeos a 75 m | 9.5 e 11.5 (27 contra 16%, p 0,06) |
| J | 120 quadros novos do corpus nadir (índices 180 a 299 da semente 21), 20 por regime de luz | 10.3 e 11.3 |
| G | Sementes de treino 1 e 2 para S-oblique-six, ajuste fino a 5% (das duas partidas), armado 35 m e gêmeo 75 m | 10.6 (dispersão entre treinos) |
| Y | VisDrone oficial dos modelos novos e aplicação dos critérios | todos |

## Critérios, fixados antes de rodar

### 10.6, convenção de anotação

Para cada par de modelos que o artigo compara, o critério olha o sinal da diferença a IoU 0,50, 0,60
e 0,75, nas duas regras de avaliação (a do Ultralytics e a oficial do VisDrone). Os pares são:

- R contra S-oblique-six;
- S-oblique-six contra oblíquo de um sítio;
- oblíquo contra nadir;
- variedade contra nadir;
- as partidas do ajuste fino a 5% e a 10%;
- os mistos contra o COCO.

Se o sinal muda em algum limiar, aquele par é artefato de anotação e vai ao texto nos três
limiares. Nos armados, o critério olha a ordem da taxa de objeto chamado de arma entre os três
modelos, nos três limiares.

### Regra oficial do VisDrone

Sai da avaliação toda caixa, verdadeira ou detectada, com metade ou mais da área em região
ignorada. É a regra de `dropObjectsInIgr.m` do VisDrone2018-DET-toolkit, conferida na fonte em
27/09.

O avaliador (`06-resultados/avalia_visdrone_oficial.py`) é o validador do Ultralytics com um filtro
antes do casamento. Sem regiões, ele reproduz o número padrão, e isso é conferido a cada modelo
(campo `confere_padrao`). Teste feito antes da rodada, no S-oblique-six: 0,1055 reproduzido.

O resultado não tem regra de derrubada. Ele dá a eficácia no protocolo oficial, que é o que torna
a comparação com Kiefer et al. mais limpa.

### 10.2, escala casada

O validador do Ultralytics redimensiona toda imagem para que o lado maior valha imgsz, para cima
ou para baixo (`ultralytics/data/base.py`, `load_image`). Reescalar os arquivos e avaliar com o
mesmo imgsz não muda a escala que a rede vê.

Consequência para o texto: a checagem do piloto (0,0055 contra 0,0061) comparou duas avaliações na
mesma escala de entrada. As duas foram feitas a imgsz 640, e o conjunto reescalado volta a 640 px
no lado maior. A frase da 10.2 que diz que casar a escala não recuperou o desempenho no piloto
precisa ser corrigida junto com o resultado desta rodada.

O casamento se faz pelo imgsz. O critério escolhe o múltiplo de 32 cuja mediana do lado maior das
caixas do VisDrone val, na entrada da rede, fique mais perto dos 20,55 px do corpus de treino. A
escolha é calculada só com rótulos e tamanhos de imagem, antes de qualquer avaliação:

- imgsz 1024 dá 20,27 px (1280 dá 25,33 px);
- a área mediana cai de 283 para 181 px², porque forma não se casa com escala uniforme.

O S-nadir-150 e o R são avaliados a 1024.

A regra é "diverge substancialmente" se o mAP50 casado diferir do de 1280 (0,0102) em mais de 50%
dele. Nesse caso, a razão da 9.2 passa a ser dada só na escala casada. Esta regra torna precisa,
antes de medir, a expressão "diverge substantially" do texto.

### 9.5, objeto carregado como arma

O corpus de teste (`ds_armado_75_porte`) é o comando do teste de arma inédita com
`--objeto-porte-arma`. A flag faz o objeto confundível usar a mesma distribuição de pose da arma,
e os de mais de 1,15 m deixam de ser reangulados. Os sorteios são os mesmos, então os quadros são
gêmeos dos da rodada 3, e isso é conferido caixa a caixa.

A comparação é pareada, objeto a objeto, com McNemar exato, no armado_75. O armado_75g entra como
secundário.

Regra: se a taxa sobe no porte de arma com p < 0,05, o texto passa a dar a taxa medida nesse porte.
Senão, sai a ressalva do ângulo de porte.

Limitação declarada: no porte de arma um objeto longo pode atravessar o chão ou a laje.

### 9.4, treino misto

O corpus misto junta os 890 ladrilhos de treino do S-oblique-six com as 324 (5%) ou 647 (10%)
imagens reais das mesmas fatias do ajuste fino. O treino parte do COCO, dura 30 épocas em classe
única e escolhe o peso em `sel`. O teste é no val inteiro.

Cada imagem real é vista 30 vezes, como no ft05_coco, mas há mais passos de gradiente, e isso vai
declarado.

Regra: o misto é melhor que só real se a diferença para o ft05_coco (ou o ft10_coco) passar de
2 desvios-padrão entre as três sementes do ft05_coco (grupo G). É pior se ficar abaixo de −2
desvios. No meio, não há diferença resolvível. A 10% usa o desvio de 5%, declarado como
aproximação.

### 11.5, 150 m

Validade: o modelo tem de detectar pelo menos metade das pessoas anotadas, em qualquer classe.
Abaixo disso, o resultado é não interpretável, como o do piloto.

A medida é d′ entre armada e objeto confundível: z(armada chamada de armada) − z(objeto chamado de
armada), com correção log-linear. O intervalo de 95% vem de um bootstrap de quadros (2.000
reamostragens, semente 0).

Regra:

- se o intervalo inclui 0, a ausência a 150 m passa a ser medida;
- se exclui, há separação acima do acaso no sintético. Como a arma é argumentada irresolvível a
  150 m, essa separação usa outro indício, e o texto o trata como atalho, não como capacidade.

A curva 35/75/150 m sai com a mesma medida nos três gêmeos.

### 9.5 e 11.5, validação maior

Regra, aplicada só nos quadros novos (replicação):

- 35 m acima do gêmeo de 75 m com p bilateral < 0,05: a diferença passa a estabelecida;
- direção invertida: sai a frase "a resolução mais fina não reduziu a confusão";
- qualquer outro caso: continua sugestiva.

A soma com o val original é secundária. Os quadros novos são renderizados pelo gerador atual nas
duas altitudes.

### 10.3, regime de luz

A regra já estava no artigo; aqui só se fixa a medida. A medida principal é o mAP50 do S-nadir-150
nos ladrilhos de cada regime. A secundária é o recall a conf 0,25 em imagem inteira, com intervalo
por bootstrap de quadros.

Regra: a implicação da 11.3 fica se o mAP50 sob "overcast" (nublado) for maior que sob "hard sun"
(sol_duro) e sob "rain" (chuva), e se hard sun estiver entre os dois regimes mais fracos. Senão, a
implicação sai.

O corpus é renderizado pelo gerador atual. A biblioteca de armas difere da do treino, o que não
pesa na detecção de pessoa em classe única e é igual para os seis regimes.

### 10.6, sementes

São três treinos por modelo: semente 0 (o original), 1 e 2. Varia só o treino; o corpus fica fixo.

Regra: uma diferença é resolvível se as faixas mínimo-máximo dos dois modelos não se sobrepõem.
Essa regra vale para:

- a eficácia do S-oblique-six (média e desvio);
- o ajuste fino a 5%, sintético contra COCO;
- o objeto chamado de arma a 35 m contra o gêmeo de 75 m, no val e nos quadros novos.

## Custo e previsão

Estimativa pelos tempos medidos na rodada 3:

- render de 120 a 190 s por quadro 4K;
- treino de 3 classes com cerca de 230 s por época;
- ajuste fino com cerca de 100 s por época;
- quadros pulados sorteados (sem render) a cerca de 8 s cada.

| Grupo | Horas |
|---|---|
| K | 1 |
| H | 3 |
| F | 5,5 |
| E | 12 |
| I | 6,5 |
| J | 7 |
| G | 25 |
| Y | 0,5 |

O total é de cerca de 60 h, com a parada antecipada podendo encurtar os treinos. A rodada foi
disparada em 27/09, perto do meio-dia, e a previsão de término é a noite de 29/09.

## O que não está na rodada

- **Opcionais:** a curva de aprendizado da 10.1, o corpus só com sol duro, o ajuste fino até
  convergir ou com camadas congeladas, e o armado com câmera oblíqua.
- **Sementes de corpus:** novo assentamento para cada semente não entrou, porque cada
  assentamento custa cerca de 8 h de render.
