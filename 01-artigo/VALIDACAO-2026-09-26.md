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

## Rodada 3: critérios e expectativas declarados antes

Revisor com 70 consultas, 26 min, cruzando o histórico do git com as datas do RESULTADOS e do DIARIO para ver quando cada critério entrou no texto e quando o resultado saiu. 16 achados (2 erros, 7 inconsistências, 7 melhorias). Todos conferidos e aceitos.

- **Erro: a expectativa da 9.4 falhou e o texto dizia "as expected".** A expectativa declarada em 24/09, antes das corridas, era que o valor do pré-treino sintético fosse maior no volume menor. Ele saiu mais negativo no volume menor (-0,0796 contra -0,0614). O texto agora diz que a expectativa falhou. A mesma frase no RESULTADOS ("como declarado antes da rodada") foi corrigida.
- **Erro: "o protocolo da 7.7 foi fixado antes de qualquer corrida".** Pelo git, a 7.7 tinha quatro modelos até 22/09. S-nadir-150-six, S-oblique-six, o de 35 m e seu gêmeo e os de ajuste fino entraram depois que resultados anteriores eram conhecidos. Agora o texto diz que cada modelo foi especificado antes da própria corrida, mas o protocolo cresceu em etapas. A caixa de estado do PDF (`monta_artigo.py`) repetia a afirmação antiga e também foi corrigida.
- **A metade em escala casada da 10.2 nunca rodou no corpus corrigido.** O texto afirmava que o 0,0102 "também é o número em escala casada" por argumento. E o argumento troca a estatística: o piloto casou pelo lado maior da caixa, e o corpus corrigido casa em área, mas não no lado maior (20,6 contra 25,0 px). Agora o texto diz que só a metade nativa rodou, que a outra foi abandonada antes do resultado e que a condição de refutação não foi avaliada. Também saiu a leitura do piloto como "evidência contra a escala": um modelo que não aprendeu o próprio domínio não informa sobre isso.
- **Causalidade além do teste.** A 11.5 afirmava o efeito da altitude sobre as três taxas como estabelecido; nenhum contraste passa de p 0,05, e agora a 11.5 diz "sugestivo", como a 9.5. A 11.2 estendia ao S-oblique-six (que não é ablação) a atribuição à geometria de captura. A 10.4 trazia o 0,1055 como resultado de um teste em que só a câmera muda. A 9.3 creditava ao critério da 10.4 a comparação com a variedade de sítio, que é posterior a ele. A 10.1 e a 9 davam a contagem de cenas como causa "identificada" do fracasso do piloto, mas nada a isolou.
- **Condições que não decidiam nada.** A condição da 10.3 ("ordenar com o contraste") não dizia sobre quais regimes. Passou a comparar o nublado com o sol duro e a chuva, a única diferença que a 8.3 chega perto de resolver, e a exigir o sol duro entre os dois piores; a ablação ficou descritiva. A 11.3 ganhou a mesma condição, que antes omitia a cláusula do sol duro. A condição da 10.1 não tinha direção nem margem: agora exige subir do menor corpus para o maior mais do que a dispersão entre sementes. As duas redações novas declaram que foram fixadas antes dos testes, que continuam sem rodar. A 11.5 dizia que a distinção "existe" a 75 m sem limiar fixado; agora diz em que sentido (acima do acaso) e que não houve limiar prévio.
- **Pequenas.** A abertura da 10 dizia que toda ameaça foi "testada". A lista do que falta na conclusão ganhou a metade casada da 10.2. A 8.4 ganhou a ressalva do sol duro. A remissão da 8.3 agora aponta para a 10.3 (teste e condição) e para a 11.3 (a implicação).

## Rodada 4: força das afirmações e linguagem estatística

Revisor com 56 consultas, 29 min. 36 achados (1 erro, 16 inconsistências, 19 melhorias). Todos conferidos e aceitos, alguns com redação ajustada. **É a rodada que mais mexe no tom do artigo, e o autor deve ler as passagens abaixo.**

- **Treino único nunca declarado.** Toda comparação entre modelos vem de uma corrida de treino por modelo, com uma semente, sem dispersão medida. Isso vale para 0,0102 contra 0,0190, para os 6 a 8 pontos do ajuste fino e para as taxas do gêmeo. Nada no texto dizia isso. Agora a nota de proveniência da 9 diz; o abstract, a 9.4 e a conclusão dizem "em uma corrida por modelo"; e a 10.6 inclui a corrida única entre as fontes de acaso.
- **A 150 m a ausência é argumentada, não medida.** Nenhum corpus com objetos confundíveis foi renderizado a 150 m. O próprio gerador (`objetos_alongados.py`) calcula que ali um fuzil chega como uma linha de 18 por 1 px que quebra a silhueta, e a caixa da pessoa armada a 150 m já é maior que a da desarmada (20,1 × 19,6 contra 15,5 × 15,0 px). O abstract, a 4, a 7.3 e a 11.5 passaram de "a capacidade não existe" para "o objeto chega como linha fina cuja forma não se resolve, ausência argumentada pela resolução e não medida". A tese continua de pé, mas como argumento declarado.
- **Cor.** "Nenhum detector separa as classes pela cor" era forte demais: os objetos têm cores que nenhuma arma tem (PVC claro, plástico azul, pano escuro). Agora o texto diz que a cor sozinha não separa, e a 7.4 diz quais cores só aparecem em objetos.
- **Abstract.** Passou a dizer que o benchmark real é urbano público e não é favela.
- **Estatística do gêmeo e do teste inédito.** As taxas de armada e desarmada do gêmeo têm p de 0,15 e 0,22, e o texto agora cita os dois. "Lowers the object rate (p = 0,19)" virou "diferença que o teste não sustenta". O intervalo de Katz ignora o agrupamento nos 50 quadros e é otimista, e o critério se aplica à razão pontual. A leitura "o detector generaliza para comprimento e silhueta" virou "consistente com", com as contagens (15 a 69) e a submetralhadora inédita (0,55 m, chamada de armada em 0,43), que a leitura por comprimento não prevê.
- **Escopo e causalidade.** "Bounds generalisation to dense aerial urban scenes" virou "mede a generalização para as cenas que esse benchmark registra". A taxa de objeto chamado de arma é uma estimativa sintética, não a taxa sobre moradores reais. "The binding constraint(s)" (8.4 e conclusão) virou "not only" e "os medidos aqui": o realismo nunca foi variado. O mecanismo do sol duro virou hipótese em todo lugar. O título da 8.3 afirmava uma ordem que a própria 8.3 diz não resolver. A diferença oblíquo menos nadir "estima", não "isola". "Best configuration this generator supports" virou "tried here". "Attainable ceiling" virou "matched-volume ceiling". O R tem o mesmo número de imagens, mas não de pessoas (18.858 contra 3.225).
- **Pequenas.** A seção 5 ainda dizia que o protocolo foi fixado antes de qualquer treino (a rodada 3 esqueceu esse arquivo). "Invisíveis de cima, a maioria num beco" não foi medido. "Fonte dominante de desordem" também não. O 1,97 da 8.2 vem de 49 figuras. Na 9.2, "assinatura esperada" de menos memorização compara splits de validação diferentes.

## Rodada 5: proveniência

Revisor com 87 consultas, 24 min; recontou nos rótulos do desktop, só leitura, os valores que não estavam em arquivo. 17 achados (5 erros, 3 inconsistências, 9 melhorias). Todos conferidos e aceitos. Para os números corretos sem arquivo, a correção foi **criar a fonte**, não ressalvar o texto.

- **Script novo, `06-resultados/mede_alvo_split.py` → `alvo_por_split.json`.** Mede tamanho e forma por corpus e por split, com o lado maior. Reproduz exatamente os números que estavam no texto sem arquivo: a tabela da 8.1 (lado maior 10,1 / 20,6 / 25,0 px; 66,9 / 0,8 / 30,5% abaixo do stride); as linhas do `ds_morro_clima` e do VisDrone na 8.2, incluindo o alvo de calibração 1,95; 408 das 548 imagens de teste em 1360 × 765; as 1.106 imagens e 18.858 pessoas do R. O `mede_alvo.py` antigo junta treino e validação e não mede o lado maior; é daí que vinham os 300 px² misturados.
- **Erro: 2,18 sem fonte.** A anisotropia da "versão de partição única" era o 4,35 da v0 dividido por 2, supondo o mesmo erro de normalização. Mas o 4,35 foi medido pelo validador externo antes de o `teste_fidelidade.py` existir, na escala já correta (os valores dele para v3 e v7 batem com o CSV corrigido). Não há render da v0 para remedir, então o número saiu, e o texto diz que ela nunca foi medida com o script corrigido. O 0,94 ganhou a fonte (linha v12, `teste_fidelidade.py`).
- **Erro: negativos vazios.** O "realizado 0,8 a 4,5%" não está em arquivo e os logs de ladrilhamento o contradizem (0,7 a 2,9%). E o 5% não é uma fração pedida: é a probabilidade de manter cada ladrilho vazio. A tabela da 7.6 agora diz isso.
- **Luminância.** A 7.5 atribuía ao corpus de treino as médias do corpus piloto (48 imagens do `ds_morro_clima`), e a legenda da figura 2 as atribuía aos seis painéis mostrados, que são outro render.
- **Citações que faltavam.** O par 0,116 / 0,561 (`val_final.json` dos dois runs). As taxas por modelo e as duas revocações da 11.5. As contagens do corpus de 35 m. A precisão da tabela da 9.5 (`gemeo_75_35.json`: não é o P dos arquivos de confusão). O `sim2real_s_nadir_4k.json` nas legendas da 9.2 e da 9.3. O R, que agora cita o `avalia_sim2real.py` e os passos 9 e 10 do `fila_noite.py`.
- **Sem fonte, reescritos.** "Alvo de 11 a 41 px" (do braço antigo a 100 m, sem comando) virou a conta com a mediana do corpus de registro (17,6 / 2,5 ≈ 7 px). "Dois dias" do R cheio virou "seis vezes mais imagens por época". "Faixa central de três quintos" virou o parâmetro do filtro (quadrado de 0,52 da largura). "Seis arquiteturas" de Liao não está na ficha conferida e virou "as arquiteturas que eles testam". "8% e 42% dos casos" de pose de tiro são probabilidades de sorteio do gerador, não frequências medidas, e agora o texto diz assim.

## Rodada 6: texto desatualizado

Revisor com 91 consultas, 29 min. 45 achados (3 erros, 17 inconsistências, 25 melhorias) e 1 observação fora da lente. Todos conferidos e aceitos.

- **Erros: caixas de estado do PDF.** As caixas de estado (`monta_artigo.py`) chamavam de "v2 verbatim" a introdução, a revisão e a metodologia do orientador, mas o mestrando reescreveu partes das três: a pergunta de pesquisa, o objetivo, os quatro componentes, o bloco de detecção aérea. A conclusão aparecia como "v2 mais o fecho", embora o primeiro parágrafo de Limitations, a delimitação técnica e o Future Research técnico também tenham sido reescritos. As caixas agora dizem o que mudou e que precisa do aval do orientador (ou do coautor, nas seções 3 e 4). O abstract tem hoje cerca de 370 palavras, e a caixa registra isso contra a meta de 150.
- **Texto velho no manuscrito.**
  - A 7.3 falava em "duas altitudes"; hoje são três.
  - A 7.5 citava como existente a ablação da 10.
  - A 11.1 ainda falava da "instância de 4 pixels", aritmética que a rodada 5 trocou.
  - A 10.2 mantinha "If it were not exact", da redação de 20/09.
  - A 10.6 falava em "corpora of record".
  - A 6 chamava a detecção de pessoa de "proxy", enquadramento anterior a 22/09.
  - A conclusão dizia "a synthetic corpus" e "at the time of writing".
  - A seção 5 descrevia um único corpus e parava na seção 10.
  - A 11.4 falava da "tarefa que o artigo de fato propõe".
  - A expectativa da 9.4 estava no presente, três linhas antes do veredito.
  - A ressalva de Kiefer aparecia duas vezes seguidas na 9.3.
  - A remissão 17,6 × 17,5 apontava para a 8.1 (é a 8.2).
  - A frase "Nada neste artigo recomenda aquisição" ficou órfã depois de uma divisão de parágrafo.
  - A conclusão restringia a revisão de literatura a temas que hoje estão na introdução, e não listava a ablação da 10.3 entre o que falta.
- **PENDENCIAS.** A4, D1, D4, D6, D7 e E4 resolvidos ou superados pelo texto e fechados. D5 e D8 ganharam a situação atual. B8 descrevia a lista de referências antiga.
- **Ferramenta.** O `--sem-notas` procurava "Status note", nome abandonado em 20/09. A contagem de `[X]` do aviso do PDF contava também a legenda das notas; agora dá 3, os reais. A docstring e o aviso ainda descreviam o formato AIM e "blocos em vermelho".
- **Quebras de linha.** As edições automáticas deixaram linhas longas e fragmentos no meio de frases, e numa linha da 11.5 o texto começava com "9. ", que o markdown poderia ler como item de lista. `reflui.py` (scratchpad) refluiu os parágrafos quebrados a mão para cerca de 100 colunas, com verificação de que nenhuma palavra mudou. Os parágrafos de linha única do orientador ficaram intactos.
- **Fora da lente, aplicada.** A 11.6 dizia que todo corpus por trás de todo número é redistribuível por construção. O par 0,116 / 0,561 vem do braço anterior, com plantas do OpenStreetMap, e o R e o ajuste fino usam o VisDrone, distribuído pelos próprios autores. O texto agora diz isso.

## Rodada 7: método descrito contra o que o código executou

Revisor com 87 consultas, 30 min. Conferiu cada modelo da tabela 7.7 e cada corpus contra o `gen_morro.py` (na versão que de fato renderizou cada corpus), `people_mpfb.py`, `objetos_alongados.py`, `sitios.py`, as cadeias, o `tile_dataset.py`, todos os `args.yaml`, os logs de treino e render, os manifestos e o venv. 31 achados (8 erros, 15 inconsistências, 8 melhorias). Todos conferidos e aceitos. Correções aplicadas com casamento tolerante a quebra de linha e parágrafos refluídos depois.

- **Erro: taxa de aprendizado.** A tabela da 7.6 dizia "lr0 0,01". Todos os logs mostram que o Ultralytics, com `optimizer=auto`, ignora o lr0 e escolhe AdamW com 0,002 nos modelos de uma classe e 0,001429 nos de três.
- **Erro: a arma a 150 m.** A 9.5 e a 11.5 diziam que no corpus de 150 m a arma é "sempre o mesmo modelo, na mesma pose". O código que renderizou o `ds_morro_4k` (anterior à biblioteca de cinco armas) sorteava três padrões de fuzil ou uma pistola, em quatro poses. O que torna a acurácia a 150 m ininterpretável é outra coisa: a arma é o único objeto alongado que qualquer figura carrega.
- **Erro: S-oblique não é "o mesmo gerador".** O corpus de registro é anterior à biblioteca de cinco armas que o oblíquo e o de seis sítios usam, e também a pose de tiro muda (0,46 contra 0,42). A 9.3 dizia "Identical generator" e a 10.4 "the same code".
- **Erro: piloto 0,077.** É média de duas classes (armada e desarmada), e o 0,79 com que é comparado é de uma classe. O texto diz isso agora. O piloto também não era "o mesmo corpus antes do tamanho final": é outra realização do assentamento (semente 11 contra 21), e a 8 já não diz que a comparação "isola" a resolução.
- **Carregamento dos objetos.** Todo objeto com mais de 1,15 m (nenhuma arma chega a isso) é reinclinado no ombro ou apontado para o chão em qualquer pose. Portanto a maioria dos objetos confundíveis é carregada em ângulos que nenhuma arma assume, e a "mesma distribuição de poses" vale para o corpo, não para o ângulo. Isso foi corrigido na 7.4, na 9.5 e na 11.5.
- **Comprimentos das armas.** Os comprimentos registrados (0,20 a 1,05 m) não são os das malhas: os dois fuzis e a espingarda são mais longos modelados. Com isso o FAL inédito (1,10 m) fica dentro da faixa das armas vistas como modeladas, e a 11.5 agora diz isso.
- **Validação e seleção.** O split de validação não é 15% fixo: cada quadro vai para validação com probabilidade 0,15 (24 a 35 quadros por corpus), e os quadros de validação mostram o mesmo assentamento. Os modelos de três classes são avaliados no mesmo split que serviu para parada antecipada e escolha do checkpoint, a mesma assimetria que a 10.5 declara para o R. A parada e o checkpoint seguem o mAP50-95, não o mAP50 que o artigo relata.
- **Protocolo que faltava.** A tabela da 7.6 ganhou a linha de aumento de dados (três valores diferem do padrão do Ultralytics) e o passo real dos ladrilhos (1.024 px, oito por quadro). O R e o ajuste fino treinam em imagens inteiras do VisDrone reduzidas a 1.280 px no lado maior. A câmera não é exatamente nadir nem de altura fixa: inclinação até 3,5 graus, rumo sorteado e ±6 m. Os orçamentos de iluminação também fixam elevação, cor e um deslocamento de exposição. A 7.2 agora diz que são 9 sub-bairros só no sítio do corpus de registro (6 a 12 nos outros), que lotes giram e deformam, que a folga zero deixa uma fresta (não parede compartilhada) e que o número de andares tem dispersão por casa. A anotação projeta uma subamostra de uns 500 vértices por figura. As figuras vêm de um conjunto de 6 corpos MPFB por render. As árvores são 4 modelos CC0 do Poly Haven, não geometria do gerador (7.2 e 11.6). O par 0,116 / 0,561 difere em cinco aspectos, não quatro: também no conjunto de validação. O casamento da matriz de confusão ignora a classe prevista. O refazimento da câmera livre tem duas condições e limite de 30 tentativas. O R casa com os ladrilhos do corpus de registro, mas os oblíquos têm menos ladrilhos (968 e 890).

## Rodada 8: revisor cético

Revisor com 76 consultas, 27 min. Fez recontagens só de leitura nas anotações brutas do VisDrone, nos tamanhos das imagens, nos logs e no código do Ultralytics. 17 objeções (1 erro, 4 inconsistências, 12 melhorias). Todas conferidas e aceitas. Números recontados que não estão em arquivo de `06-resultados` (tamanhos na entrada da rede, razão sem a pistola ≈ 1,06, d' na nova realização ≈ 0,86) ficaram fora do texto.

- **Erro: reprodutibilidade.** A 11.6 diz que todo parâmetro para reproduzir uma corrida está no artigo, mas faltavam as sementes (treino 0 determinístico; as 1.106 imagens do R com semente 21; as fatias do ajuste fino com semente 2609). A tabela da 7.6 ganhou a linha. Também faltavam o mapeamento de rótulos do VisDrone e o tamanho de entrada na avaliação.
- **O que estava só em nota.** Que o protocolo cresceu em etapas (o S-oblique-six, número principal do abstract, foi desenhado depois de resultados conhecidos) e que cada modelo treinou uma vez só estava na nota de proveniência da 9, que o `--sem-notas` apaga na versão de submissão. Foi para o corpo do texto, junto com a ressalva de que nenhum número do VisDrone tem intervalo sobre as 548 imagens de teste. O mesmo valeu para a frase da 10 sobre condições fixadas antes.
- **VisDrone.** Pedestre e "people" foram fundidos numa classe e as regiões ignoradas foram descartadas. O validador do Ultralytics, ao contrário do kit oficial, conta como falso positivo uma detecção dentro de região ignorada (1.378 regiões em 340 das 548 imagens). As imagens são avaliadas redimensionadas a 1.280 px no lado maior, e os tamanhos da 8.1 são em resolução nativa. P e R da seção 9 vêm do limiar de F1 máximo, não de 0,001.
- **Taxa de objeto chamado de arma.** Pelo casamento que ignora a classe, uma caixa de armada sobre uma pessoa já casada com outra caixa não entra na taxa, então ela é um limite inferior do alerta que um operador veria. A taxa também depende da regra do gerador que reinclina os objetos longos: o guarda-chuva, curto o bastante para ser carregado como arma, é o mais chamado de arma (0,38 contra 0,10 da vassoura). E depende do limiar de 0,25, não ajustado, e da realização do assentamento; o d' do `gemeo_75_35.json` separa discriminação de viés e confirma a leitura de que a 35 m o modelo não separa melhor. Na 7.4, "o detector separa pela silhueta, a única coisa que poderia transferir" não se seguia mais: ele pode usar comprimento, cor e ângulo de carregamento, e o ângulo é regra do gerador.
- **Ajuste fino.** O cronograma não foi ajustado e é o mesmo para as duas partidas. Os quatro modelos atingem o melhor valor entre as épocas 27 e 30 de 30, ou seja, a comparação é a orçamento fixo, não a convergência (a vantagem do COCO não diminui da época 20 para a 30). O início sintético herda a cabeça de detecção já treinada para pessoa, enquanto o COCO reinicia a camada de classes; a vantagem do COCO vale mesmo contra essa largada. O sinal é o mesmo em mAP50-95, a métrica de seleção.
- **Outras.** A 9.3 ainda dizia "gerador mantido fixo" logo depois de a rodada 7 declarar a diferença. No teste inédito, o grupo das armas vistas inclui a pistola, e parte da razão acima de 1 é composição (sem a pistola, a razão continua acima do limiar). O abstract agora diz que o denominador é o mesmo detector com número casado de imagens reais e que os falsos positivos são medidos só em imagem sintética.

## Rodada 9: forma e estilo

Revisor com 88 consultas, 31 min. Renderizou os arquivos com as próprias funções do montador, fora do repositório. 37 achados (1 erro, 16 inconsistências, 20 melhorias). Todos aceitos. Das 7 observações fora da lente, 5 foram aplicadas e 2 ficam para o autor.

- **Erro.** A legenda da figura 4 saía no PDF com crases literais, porque o montador cola a legenda como HTML cru. Trocado por `<code>`.
- **Mistura de formas.** A grafia técnica é britânica e ficou consistente:
  - "metres" virou "m" depois de numeral (13 ocorrências);
  - "%" virou "per cent" nas tabelas da 9.2 e da 9.3;
  - "toward" virou "towards";
  - "deg" virou "degrees" e "x" virou "by" nas tabelas da 8;
  - "low contrast" ganhou hífen;
  - "mAP@50" virou "mAP50";
  - "YOLOv11" (nome de Liao) ganhou a glosa;
  - *beco* foi para itálico;
  - os nomes de modelo saíram do formato de código;
  - o caminho do `holdout_criterio.py` ficou completo;
  - o 1,95 da tabela da 8.2 passou a negrito como os outros.
- **Estragos das rodadas anteriores.**
  - "The result is measured." ficou solto depois de uma inserção.
  - Na 7.3, a lente passou a se ligar ao corpus de 35 m.
  - Na 7.5, a lista dos seis regimes passou a ler como parte de um parêntese.
  - O parêntese de fonte do par 0,116 / 0,561 separava o verbo do complemento.
  - "Both defects" do piloto e "the same test" da 9.5 ficaram sem antecedente.
  - Na 10.4, "that puts" e "the change" passaram a se referir ao filtro de posicionamento.
  - A 10.2 repetia os números de 15 linhas antes.
  - A 11.5 repetia a remissão à 7.4.
  - A 11.6 dizia duas vezes que o defeito foi achado depois.
  - Cinco frases com mais de 90 palavras foram divididas sem perder fato: 7.4, S-oblique-six, teste inédito, 8.4 e conclusão.
- **Fora da lente, aplicadas.**
  - A legenda da figura 1 e a 11.2 ainda diziam "parede compartilhada" e "toda geometria é do gerador".
  - A 8.2 dizia "o mesmo gerador" para o S-oblique.
  - A 9.2 dizia "mantém toda configuração do gerador" duas linhas antes de dizer que era outra versão; agora diz "toda configuração de linha de comando".
  - O abstract definia GSD como área; é distância.
  - "The corpus" do abstract não tinha antecedente.
  - "domain-randomization" estava no parágrafo reescrito da conclusão.
  - A contagem do abstract na caixa de estado passou a cerca de 390 palavras.
- **Para o autor.**
  - As figuras 2, 4 e 5 têm rótulos em português dentro da imagem ("sol_duro", "caixas", "verde = armada").
  - O texto nunca cita figura por número.
  - A introdução do orientador mistura grafia britânica e americana.
  - O abstract tem 386 palavras, contra a meta de cerca de 150.

## Rodada 10: passe final integrado

Revisor com 74 consultas, 27 min. Leu o artigo inteiro, em ordem, como um argumento só, e conferiu por amostragem pelo menos três correções de cada rodada anterior (todas presentes e íntegras). 29 achados (2 erros, 8 inconsistências, 19 melhorias). Todos aceitos, menos um: o travessão dentro do título de uma referência fica, porque é citação literal de título publicado.

- **Erros que sobreviveram às nove rodadas.** A 9.5 e a 11.5 diziam que a distinção armado/desarmado é "aprendível" a 150 m, mas nenhum modelo do artigo sustenta isso: o S-nadir-150 é de classe única, e o piloto de duas classes não aprendeu o próprio domínio. A frase é resto do braço fotogramétrico retirado em 22/09 (o único modelo de duas classes a 150 m era o `cid150_s`). Agora o texto diz que um detector ali *poderia* separar as classes pelo motivo errado, e que nenhum foi treinado para isso.
- **Abstract e conclusão.** O abstract não trazia nenhum resultado armado/desarmado, justamente o assunto do título. Agora traz as taxas de 75 m, de 35 m e do gêmeo, com a ressalva de que são só em imagem sintética e de que a diferença é sugestiva. Também passou a dizer que a transferência medida é de detecção de pessoa em classe única e que cada modelo treinou uma vez. A conclusão reformulava a pergunta de pesquisa de outro jeito; agora a repete. E ganhou uma frase que diz quais das quatro condições de aquisição do objetivo foram de fato variadas: só a altitude, para a distinção, e só em imagem sintética.
- **Resíduos.**
  - A 7.2 dizia que o corpus é "liberado com o artigo", contra a 11.6.
  - A tabela 7.7 não tinha o "tried here" da rodada 4.
  - A 10.4 omitia a diferença de pose 0,46 contra 0,42.
  - A 3 ainda afirmava a ausência a 150 m sem ressalva.
  - A frase de abertura do artigo afirmava sem fonte que sistemas "são comprados" com essa promessa; agora remete à seção 3.
  - "Convencionalmente voado a 150 m" não tinha fonte; virou "a altitude de referência deste estudo".
  - O piloto não treinou 120 épocas: a parada antecipada o cortou.
  - A frase de Liao na seção 2 subestimava a ablação de iluminação.
- **Texto herdado.** Duas frases sem verbo principal na introdução do orientador. Três vírgulas soltas deixadas pela retirada dos travessões (seções 3 e 4). Os títulos embutidos da seção 2 foram para negrito. Na lista de referências, Liao ganhou a lista de autores conferida na ficha e perdeu a nota em português, e os intervalos de página passaram a usar hífen.

## Resultado do loop

- **287 achados em 10 rodadas, todos conferidos antes de entrar no texto.** Nenhum foi recusado por estar errado; um foi mantido por ser citação literal. Houve ainda o passe próprio anterior ao loop.
- **Arquivos novos em `06-resultados/`:** `mede_alvo_split.py` e `alvo_por_split.json` (a fonte dos números da 8.1, da 8.2 e do R), `ft_curvas.py` e `ft_curvas_selecao.json`, e a precisão de armada no `compara_gemeo.py`.
- **Veredito da rodada 10:**
  - Todo número conferido bate com a fonte, toda remissão resolve, e o PDF sai limpo, com 3 `[X]`, todos das checagens de robustez não rodadas.
  - Resta um travessão, dentro de um título de referência.

**Para o autor decidir antes de mandar ao orientador:**
1. Encurtar o abstract, hoje com cerca de 450 palavras contra a meta de cerca de 150, sem perder as ressalvas de 150 m, do ajuste fino, de 75/35 m e do treino único.
2. Decidir se o corpus e o código serão liberados; hoje o repositório é privado, e a 11.6 diz que o leitor não confere o corpus.
3. Confirmar o periódico ou evento, porque a seção 8 fala em "this venue" e o montador usa o formato Elsevier.
4. Dar fonte à "preferência convencional por voar com céu limpo" (11.3).
5. Aprovar as passagens reescritas nas seções do orientador e do coautor; as caixas de estado do PDF dizem quais são.
6. Decidir se o resultado da 9.4 muda a proposta da seção 6.
7. Trocar os rótulos em português dentro das figuras 2, 4 e 5, e decidir se o texto deve citar figuras por número.
8. Resolver as pendências B1 a B10 das referências.
