# Validação do manuscrito em 10 rodadas (2026-09-26) [DESKTOP]

Pedido do autor depois da rodada 3: analisar o artigo, atualizar os resultados e validar em um loop
de 10 rodadas. Cada rodada é um revisor independente (subagente com contexto limpo, só leitura)
com uma lente diferente; ele cita o trecho, a evidência na fonte e a correção. Cada achado é
conferido antes de entrar no texto; os recusados ficam registrados com o motivo.

Antes do loop (passe próprio, commit 42319d2): resultados da rodada 3 propagados para as seções
6, 7.4, 7.6, 7.7, 10.4, 11.2 e a conclusão; dois erros de fato corrigidos (o FAL inédito tem
1,10 m e fica acima do maior dos cinco modelos, 1,05 m, não "dentro da faixa"; o rodo foi
traduzido como "rakes").

| Rodada | Lente |
|---|---|
| 1 | Números contra as fontes |
| 2 | Consistência interna e remissões |
| 3 | Critérios e expectativas declarados antes |
| 4 | Força das afirmações e linguagem estatística |
| 5 | Proveniência (arquivo e script de cada número) |
| 6 | Texto desatualizado |
| 7 | Método descrito contra o que o código executou |
| 8 | Revisor cético: confusões e ressalvas omitidas |
| 9 | Forma e estilo das seções técnicas |
| 10 | Passe final integrado |

## Rodada 1: números contra as fontes

Revisor com 83 consultas a arquivos, 25 min. 20 achados (5 erros, 10 inconsistências, 5 melhorias) e 5 observações fora da lente. Todos conferidos; todos aceitos, dois com redação ajustada.

- **Erros.** Gêmeo "17 por cento" era 16,48 (virou 16). mAP50 do S-oblique-six "10,6 pontos" é 10,5 (bruto entre 0,10545 e 0,1055) e fica logo *acima* da faixa de Kiefer, não no topo; e Kiefer mede 10 classes contra a nossa uma. **O denominador de Kiefer não é "real de outro domínio"**: é o treino inteiro do próprio VisDrone (ficha `04-bibliografia/kiefer-2022-numeros-conferidos.md`, Tabelas III e IV); o parágrafo da 9.2 que dizia que o nosso denominador era o mais duro foi reescrito (não dá para saber qual é o mais duro). "Reaches the calibration target" com 1,85 contra 1,95 virou "approaches ... without reaching it". A frase das curvas de seleção (sintético na frente só nas primeiras épocas) não batia com `ft_curvas_selecao.json`: o COCO passa na 4ª época com 5% e já na 1ª com 10%, e o sintético volta à frente de modo intermitente.
- **Inconsistências.** Os 300 px² do VisDrone são treino e validação juntos (8.1 e 10.2). "Reaches 1.97, the value of the training split" (o valor do treino é 1,95). O pitch de 45 a 56 graus não é "a faixa em que se atinge a forma": foi escolhido para centrar a mediana. A condição de refutação da 10.3 e da 11.3 falava em ordem inversa ao contraste bruto, herança de uma medição superada em que o sol duro tinha o maior contraste bruto; hoje o nublado tem o maior e a condição contradizia a própria hipótese. Foi corrigida para contraste contra o entorno, com nota de que a correção é anterior ao teste por regime. Contagem de corpora da 8 e notas da tabela da 8.2 desatualizadas (agora há quatro gerados). A 11.6 falava de "dois corpora da 8.2".
- **Melhorias.** "Every rate is lower" vale só para as taxas de chamada de armada. O contraste 75 m original contra gêmeo muda seis configurações, não só a pose. O fator 6,4 de área mistura composição de classes (o corpus a 75 m tem a classe com objeto, de caixas maiores): classe a classe é 5,2 (armada) e 5,7 (desarmada). O abstract passou a dizer "mais de cinco vezes", e a 7.3 perdeu a explicação por ângulo de visada, que não se sustenta: o campo de visão é o mesmo nas duas altitudes. A faixa de GSD do oblíquo vale só nos 120 m nominais. O oblíquo "dentro da faixa de Kiefer" ganhou a ressalva das 10 classes.
- **Fora da lente, também aplicadas.** As notas de proveniência da 8 e da 9 ainda falavam em `[X]` pendentes. A conclusão não listava a curva completa da 10.1 entre o que falta. O modelo R escolhe o checkpoint no próprio split em que é avaliado, as 548 imagens de validação (conferido: os 548 nomes coincidem), e não só "na mesma distribuição". Na 10.4 a câmera não é a única diferença: o corpus nadir restringe as figuras a uma faixa central de cerca de 3/5 do quadro (`--enquadro quadrado`), e o oblíquo usa o quadro projetado inteiro. A nota da 8 dizia "computado antes de qualquer detector", o que não vale para a tabela por pitch.
- Fora do manuscrito: STATUS (linha de Kiefer) e RESULTADOS (10,6 para 10,5) corrigidos.

## Rodada 2: consistência interna e remissões

Revisor com 65 consultas, 25 min. Montou o mapa de seções pelo `monta_artigo.py` e conferiu toda remissão "Section X.Y". 25 achados (1 erro, 13 inconsistências, 11 melhorias) e 3 observações fora da lente. Todos conferidos e aceitos. Seis deles já constavam de `01-artigo/COESAO-RODADA-2.md` (B5, B6, A8, A10, A11, A13) e nunca tinham sido aplicados.

- **Erro.** A 11.6 dizia que nenhum número do artigo vem dos braços fotogramétricos, mas o piloto (9) e a 10.1 comparavam o 0,077 com o 0,676 de 473 imagens do `cid150_s`, cuja geometria vem do DSM da PCERJ. A decisão do autor de 22/09 (commit 235cb23) tirou esse braço do artigo e o número ficou para trás. A comparação agora é com o próprio corpus de registro: 0,79 com 180 imagens em 4K (Seção 9.2).
- **Remissões erradas.** A 7.3 mandava para uma limitação na Seção 11 que não existe (está na 8.1). A 9 dizia que a 10.1 e a 10.2 identificam as duas causas do piloto (são a 10.1 e a 8.1). A 7.7 dizia que a 11.5 explica por que os dois grupos de modelos não se leem na mesma escala (não explica; agora o motivo está na própria 7.7). A 8.4 remetia à Seção 5 (é a 6). A 11.4 dizia que a implementação está nas 9 e 10 (está na 7). "Section 10 states, for each result above, the condition that would overturn it" era falso para 9.4 e 9.5: a condição do 75 m está na 11.5.
- **Afirmações que não batiam entre seções.** A 7.2 dizia que toda imagem se regenera exata pela semente (a 11.6 diz que as figuras não, nos corpora anteriores à correção). A 11.6 dizia "nos corpora relatados aqui", mas só três são anteriores à correção de 22/09 21:48: o piloto, o corpus de registro e o 75 m original (conferido pelas datas dos manifestos). A 7.2 e a 11.6 diziam que toda geometria é do gerador, mas as figuras humanas vêm dos ativos CC0 do MakeHuman via MPFB. A abertura da 7 dizia que o que se avalia é detecção em três classes e que é a tarefa com benchmark; as três classes existem só a 75 e 35 m, e são justamente a tarefa sem benchmark. "Corpus of record" era usado também para o 75 m original. "Na mais baixa das duas altitudes": são três. O abstract atribuía os 16,7% só aos seis sítios, mas o modelo também muda o pitch e mais duas coisas, e não é ablação. A 8 dizia que o `ds_morro_4k` treina "os modelos da Seção 9" (só o S-nadir-150). "A two-point version" da curva da 10.1 não é ponto da curva: muda a variedade de sítio com N fixo.
- **Anisotropia e 1,62.** A 7.2 dava 0,90 para a configuração publicada. O valor da configuração do corpus de registro, renderizada em 4K, é 0,94 (v12 de `teste_fidelidade.csv`, renderizada com os parâmetros do `ds_morro_4k`); 0,90 é da iteração anterior. O 1,62 da versão antiga corresponde a outra iteração (v10: 0,808 × 2). O 2,18 da partição única é o 4,35 da v0 no `HISTORICO-LOOP.md` dividido por 2; fica para a rodada 5 (proveniência).
- **Hipóteses apresentadas como achados.** A conclusão incluía, entre os achados, que o sol duro enche o fundo de desordem que compete com a figura; a 10.3 ainda não testou isso. A 7.2 e a legenda da figura 4 falavam da 10.3 como se o teste por regime existisse.
- **Nomes e piloto.** Os cabeçalhos das tabelas da 9.4 e da 9.5 passaram a usar os nomes da tabela de modelos da 7.7 (F-synthetic, F-generic, S-nadir-75, S-nadir-35 e o gêmeo). O piloto usou outra receita (ladrilhos e entrada de 640 px, 120 épocas), e o texto agora diz isso. Liao: a iluminação é a ablação mais cara só no YOLOv11 (30,4 contra 27,0); na média das arquiteturas é a geometria (22 a 23 contra 17,5).
