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
