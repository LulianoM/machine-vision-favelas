# Ordem de trabalho consolidada

Li os treze arquivos na ordem de `ORDEM` em `C:\projetos\machine-vision-favelas\01-artigo\ferramentas\monta_artigo.py`. Os 113 achados colapsam em **31 itens distintos**: 22 regressões e 9 problemas anteriores a esta rodada. Nenhum arquivo foi editado.

---

## 0. Antes de tudo: a ordem do PDF que você está lendo

**O manuscrito está certo, o PDF aberto no leitor é que está velho.** Verifiquei o arquivo em disco, `C:\Users\marti\Desktop\machine-vision-favelas-elsevier.pdf`, data 22/09 11h19, e extraí as rubricas numeradas:

```
1. Introduction          2. Literature Review
3. Situating the Study   4. Rio de Janeiro's Favelas and the Case of Jacarezinho
5. Methodology           6. Design
7. The Synthetic Data Generation Pipeline
8. Model-Free Evidence   9. Results  10. Robustness  11. Technical Scope
12. Conclusion           13. References
```

É exatamente o que você pediu: contexto (3 e 4) antes da parte técnica (7). A lista `ORDEM` (linhas 44 a 56 de `monta_artigo.py`) já põe `04-situating-the-study.md` na posição 3 e `03b-methodology-synthetic-pipeline.md` na posição 7. O commit que reordenou (`7865094`, 08h10) e o último commit do artigo (`235cb23`, 11h13) são ambos anteriores ao PDF.

O que você vê na tela é uma cópia carregada no leitor antes de 11h19. **Feche e reabra o PDF.** Não há nada a corrigir na estruturação. Dos dois achados que tratavam disso, um estava errado por não ter conferido o arquivo; o correto é este.

Sugestão para não repetir o susto: fazer `monta_artigo.py` imprimir a lista numerada das treze seções ao fim da execução, junto das linhas "secoes/palavras/figuras" que já imprime.

---

# PARTE A: REGRESSÕES

Estrago novo, introduzido por `abd0a7f`, `f68d1c5` e `235cb23`. Ordenado por impacto na leitura dividido por esforço.

---

## A1. Frase quebrada no abstract (esforço: 1 minuto)

**`01-introduction.md`, linhas 10 e 11.** Corrigir a segunda frase do abstract, hoje agramatical por colagem.

Hoje lê: *"At the sensor and altitude of the sensor and altitude specified in Section 7.3"*. O diff de `235cb23` mostra a causa: trocou-se `2022 police survey described in Section 5` por `sensor and altitude specified in Section 7.3` sem apagar o `of the` que regia o sintagma antigo.

Texto sugerido:

> At the sensor and altitude specified in Section 7.3, with the camera pointing straight down at 150 m and the corpus rendered at 4K, a person occupies 17.6 by 17.5 pixels and a firearm is not resolvable within that region.

O `and the corpus rendered at 4K` resolve de passagem o item A16 (os 17,6 x 17,5 px não vêm do sensor a 1080p, vêm do render em 4K).

---

## A2. Número vencido em dois lugares: "a quarter" virou 66,9 por cento (esforço: 2 minutos)

`235cb23` trocou a coluna da tabela 8.1 do lado MAIOR para o lado MENOR da caixa, e `ds_morro_clima` foi de 25 para 66,9 por cento. A prosa que lê a coluna não acompanhou, nos dois pontos em que ela é lida.

**`06b-model-free-evidence.md`, linha 48.** Trocar a leitura da coluna pelo valor da tabela dez linhas acima.

> A single frame from that camera at 150 metres delivers a 10 pixel target on its long side, with two thirds of all instances having a side below one stride of the network.

**`07b-results-placeholder.md`, linhas 23 e 24.** Mesma troca, agora com remissão explícita à 8.1, no parágrafo que explica o fracasso do piloto (onde um revisor confere a fonte).

> ...which doubles the ground sampling distance and places two thirds of all instances below one stride of the network (Section 8.1).

Conferir os dois contra `06-resultados/` antes de fechar. O número correto torna o argumento mais forte, não mais fraco.

---

## A3. Varredura de "the survey": oito ocorrências órfãs em cinco arquivos (esforço: 15 minutos)

Este é o maior aglomerado do lote, e o mais caro de deixar passar: a recusa de reportar acurácia a 150 m, que é a contribuição central do artigo, está ancorada num levantamento que o artigo não descreve mais. `235cb23` declara na mensagem ter tirado "as cinco remissões"; conferi por grep e **sobraram oito**. Faça numa varredura só.

| Arquivo, linha | Hoje | Trocar por |
|---|---|---|
| `03b`, 93 (legenda fig1) | `seen from the virtual survey camera` | `seen from the virtual camera specified in Section 7.3` |
| `03b`, 129 | `the first is the geometry a real flight over this territory used` | `the first is the geometry at which aerial survey over urban terrain is conventionally flown` |
| `03b`, 240 (tabela 7.7) | `at the survey geometry specified in Section 7.3` | `at the nadir 150 m geometry specified in Section 7.3` |
| `06b`, 47 | `The survey camera records at 1080p.` | `The sensor specified in Section 7.3 records at 1080p.` |
| `07b`, 44 e 45 | `with the camera geometry of Section 7.3, not the 2022 survey geometry` | apagar a oração negativa inteira (ver abaixo) |
| `09b`, 67 e 68 | `at the altitude of the survey that motivates this study` | `at 150 m, the nadir geometry specified in Section 7.3` |
| `09b`, 71 | `At nadir and 150 m with the survey sensor, the median annotated instance measures 17.6 by 17.5 pixels.` | `At nadir and 150 m, rendered at 4K, the median annotated instance measures 17.6 by 17.5 pixels; a single frame at the sensor's own 1920 by 1080 is smaller still (Section 8.1).` |
| `07-conclusion`, 39 e 40 | `At the ground sampling distance of the survey that motivates this study` | `At the ground sampling distance evaluated here` |

**A linha de `03b` 129 é a mais grave das técnicas**, porque contradiz a própria 7.3 vinte linhas acima (linha 110: os parâmetros valem *"without reference to any particular flight"*). É a única justificativa dada para os 150 m, altitude do braço principal inteiro.

**A de `07b` 44 e 45 é a mais visível**, porque é a ÚNICA menção a um levantamento de 2022 no corpo do artigo (conferido por grep nos treze arquivos; as outras ocorrências de "2022" são o censo na seção 4 e citações bibliográficas) e ela é uma negativa. O leitor encontra a negação de algo a que nunca foi apresentado. Texto sugerido para a abertura da 9.2:

> Model S-nadir-150, trained only on procedurally generated imagery with the camera geometry of Section 7.3, evaluated on the same real test set with no real training image of any kind.

A ocorrência de `04-situating` linha 22 está tratada em A4, porque ali o conserto é maior que uma substituição.

---

## A4. Fecho da seção 3: a ponte para a parte técnica promete o que as seções 8 a 11 não entregam (esforço: 10 minutos, **depende do coautor delegado**)

**`04-situating-the-study.md`, linhas 18 a 24.** Reescrever o fecho para que ele se sustente sem o voo retirado e sem afirmação empírica sobre prática operacional.

Você mandou manter esse vínculo entre o contexto de campo e o miolo técnico, e ele deve ficar: é a costura que faz o artigo ter uma espinha só. O problema é o conteúdo da frase, não a sua existência. Duas coisas que o artigo não tem:

1. `at the altitude of the survey flown over this territory`: nenhum levantamento sobre o território é apresentado em lugar nenhum do texto atual.
2. `it becomes resolvable only at an altitude no operation has flown`: afirmação factual sobre prática policial, sem fonte, e mais forte do que a 11.5, que diz apenas que a 75 m a arma ocupa região que a rede *can in principle resolve*, com todos os números da 9.5 ainda em `[X]`.

Texto sugerido para as linhas 21 a 24:

> Sections 8 to 11 report what that judgement demands of the acquisition: at 150 m, the altitude at which aerial survey over urban terrain is conventionally flown and the altitude this article evaluates, the distinction is not resolvable at all, and halving that altitude makes the question empirical rather than foreclosed.

Se o delegado quiser manter a afirmação sobre altitude de voo operacional, ela é do domínio dele e precisa de fonte na própria seção 3.

---

## A5. Fecho da seção 4 repete a pergunta com que a seção 3 acabou de fechar (esforço: 5 minutos, **depende do coautor delegado**)

**`05-case-jacarezinho.md`, linha 7.** Terminar a seção no que ela tem de próprio e não repetir a pergunta do fecho anterior.

O diff de `f68d1c5` mostra que os dois fechos foram escritos no mesmo commit, um em cada arquivo, sem que um soubesse do outro. O leitor lê a mesma promessa duas vezes em uma página.

Sugestão para a última frase:

> What this study engages is narrower, and prior to it: that morphology, dense, vertically stacked, and unmapped, is what the synthetic corpus of Section 7 reproduces.

---

## A6. A 8.2 se contradiz três vezes dentro de si (esforço: 15 minutos)

`235cb23` tirou as três linhas de `dataset_cid150` da tabela e deixou de pé tudo que dependia delas. São quatro consertos no mesmo arquivo, e convém fazer juntos porque se referem à mesma tabela.

**`06b`, linha 72, título.** O título ainda promete uma variação que nenhuma linha da tabela mede: as duas sintéticas têm a mesma geometria (0,98 e 0,98) e as duas do benchmark têm geometria não registrada.

> ### 8.2 Apparent size is comparable; apparent shape is not

Se quiser manter o gancho para a 9.3, acrescente ao corpo, não ao título, que a hipótese de atribuição à geometria de câmera é o que o braço S-oblique testa.

**`06b`, linhas 74 a 76, lead-in.** Promete separar o corpus `by the camera pitch recorded in its manifest`, o que a nota da própria tabela nega e o que não separa nada, já que as duas linhas sintéticas diferem em resolução, não em ângulo.

> Measuring the aspect ratio of the same annotation sets gives:

**`06b`, linhas 100 a 102, remissão à 10.4.** A 10.4 (conferida em `08b-robustness.md` linhas 73 a 88) compara dois braços de detector com pitch e altitude fixos e pontua por mAP; não varre ângulos nem recalcula a razão altura sobre largura. O leitor aceitou o rebaixamento da afirmação porque o artigo prometeu dizer como recuperá-la, e a contrapartida não está lá. Enuncie o teste ali mesmo:

> Establishing the intermediate ordering would require rendering the same settlement at several camera angles and measuring the same statistic, which this article does not do.

A outra remissão à 10.4 no mesmo arquivo (linha 112) está correta e deve ficar.

**`06b`, linhas 115 a 118, parágrafo órfão.** Diz *"The monotonic series above is measured within synthetic corpora, where pitch is known exactly"*. Não há série monotônica (a linha 95, vinte linhas acima, declara o contrário), e `pitch is known exactly` contradiz a nota da própria tabela três linhas acima (`does not record it per image`).

> One limit on the interpretation is stated here rather than in limitations. The generated value of 0.98 comes from a generator setting that bounds the camera within 3.5 degrees of vertical without recording pitch per image, and the benchmark value of 2.20 comes from real imagery whose acquisition geometry is not recorded at all. The contrast therefore anchors the direction of the relationship and neither its slope nor its intermediate points.

---

## A7. O preâmbulo da seção 8 conta dois corpora e a tabela tem três (esforço: 2 minutos)

**`06b`, linhas 16 e 17.**

> Three corpora are used, two generated and one real, and their acquisition geometry differs in ways that matter, so the parameters are stated rather than implied.

O parágrafo seguinte compara as duas geradas entre si, e a 8.2 linha 90 já fala em *"The two generated corpora"*.

---

## A8. A nota de proveniência da seção 8 promete a propriedade que a rodada acabou de reconhecer que não existe (esforço: 2 minutos)

**`06b`, linhas 3 a 7.** A coluna foi renomeada de "Geometry recorded in manifest" para "Geometry" justamente porque a geometria dos corpora gerados não está no manifesto, e a célula diz `generator setting, not recorded per image`. A nota continua prometendo *"the acquisition geometry recorded in its manifest"*.

> Each table names the corpus, the acquisition geometry that produced it, and the instance count, and says whether that geometry is recorded per image or fixed by a generator setting.

---

## A9. A 7.7 diz três modelos, a tabela tem quatro, e a frase é falsa para um deles (esforço: 5 minutos)

**`03b`, linhas 233 a 235.** Confirmado por `git log -S`: a frase é da criação do arquivo (`94d0e3c`) e a linha S-nadir-75 entrou em `f68d1c5`, sem que a frase fosse tocada. Trocar só o numeral não resolve: o S-nadir-75 tem três classes e a 9.5 o reporta sobre corpus sintético, não sobre o VisDrone reduzido a classe única.

> The protocol therefore trains four models. Three of them, R, S-nadir-150 and S-oblique, are evaluated on the same real test set, VisDrone-DET validation (548 images, 13,969 person instances, reduced to a single class). The fourth, S-nadir-75, carries three classes and is scored on a held-out synthetic split, because no public benchmark annotates a carried firearm; Section 9.5 reports it separately and Section 11.5 says why the two cannot be read on one scale.

Nomear `S-nadir-75` explicitamente em 9.5, que hoje só diz "At 75 m".

---

## A10. A abertura da seção 7 generaliza três classes para todo o pipeline (esforço: 3 minutos)

**`03b`, linhas 10 a 12.** A 7.4 (linha 154) diz que as três classes só existem a 75 m, o corpus de registro (`ds_morro_4k`, S-nadir-150) tem duas, e a legenda da fig5 fala de duas. O leitor entra na seção achando que os negativos difíceis existem em todo o material e descobre 140 linhas adiante que estão em metade dele, o que enfraquece justamente a defesa contra a objeção do asset invariante.

> What is implemented and evaluated below detects people: two classes at 150 m, armed and unarmed, and three at 75 m, where a class of unarmed people carrying a confusable elongated object is added for the reason given in Section 7.4.

---

## A11. A 11.6 descreve errado a tabela a que manda o leitor conferir, e o conectivo seguinte ficou órfão (esforço: 5 minutos)

**`09b`, linhas 99 a 104.** Dois defeitos no mesmo parágrafo, e o lugar é caro: é a subseção de reprodutibilidade, onde o leitor confere se o artigo sabe de onde vem cada número.

Primeiro, *"Section 8.2 reads pitch from the manifest for one corpus and from the generator setting for the other"* era verdade enquanto `dataset_cid150` estava na tabela; hoje a nota da 8.2 diz que AMBAS as linhas geradas carregam o ajuste do gerador. Segundo, *"The hyperparameter and inference tables in Section 7.6 are in the body of the article for the same reason"* perdeu o antecedente: o git mostra (`5cc6726`) que essa frase nasceu colada à frase sobre reprodutibilidade por semente, e a frase sobre pitch foi inserida depois entre as duas.

> Every generated image carries its seed, illumination regime and camera altitude in a manifest entry, and the generator reproduces any image exactly from that entry. Camera pitch is recorded per image only in corpora generated after the field was added, which the corpora reported in Section 8.2 predate, so the table there states that both generated rows carry the generator setting rather than a per-image value. The hyperparameter and inference tables are in the body of Section 7.6, rather than in an appendix, so that every parameter a reader would need to reproduce a run is in the article itself.

---

## A12. A 11.5 delega a condição de retirada para uma subseção que trata de outro assunto (esforço: 5 minutos)

**`09b`, linhas 93 a 95.** A 11.5 diz que *"Section 11.3 states the condition under which even the 75 m figure would be withdrawn"*. A 11.3 trata de iluminação: a condição que ela enuncia retira a recomendação de voar sob céu encoberto, e a própria 11.2 confirma o escopo ao chamá-la de *"the only acquisition recommendation this article makes"*. O leitor vai atrás da salvaguarda do número mais delicado do artigo e encontra meteorologia.

Atenção: **não basta repontar para a Seção 10**, porque a 10.8 declara explicitamente que a distinção armado/desarmado a 75 m não é ameaça que aquela seção possa checar. Enuncie a condição ali mesmo, apoiada na linha que já existe na 9.5:

> ...a claim that can be checked before it is believed. The 75 m figure is itself withdrawn if the rate at which a confusable object is called armed is of the same order as the recall on the armed class, since separability would then not be carried by the silhouette of what is carried. Nothing in this article recommends acquisition over the case study territory.

---

## A13. A 9.5 promete que a Seção 10 cobre cada resultado, e a 10.8 diz o contrário (esforço: 3 minutos)

**`07b`, linhas 145 e 146.** A promessa entrou em `abd0a7f`, nesta rodada. A Seção 10 não tem check algum sobre o resultado de 75 m nem sobre a taxa de falso positivo em hard negatives, e a 10.8 (linhas 141 a 143) declara: *"Neither is a threat this section can check, which is why neither carries a test above"*.

> Sections 10.1 to 10.7 state the overturning condition for the transfer results above; the 75 m result carries no check of its own, and Section 11.5 states the condition under which it is withdrawn.

Casa com o texto de A12. Alternativa mais cara: criar uma entrada própria em 10 para o braço de 75 m e ajustar a 10.8.

---

## A14. O bloco novo da revisão de literatura arma a lacuna e a desmonta uma frase depois (esforço: 10 minutos, **seção do orientador**)

**`02-literature-review.md`, linhas 26 a 29 e 33 a 35.** As linhas 26 a 28 dizem que duas variáveis operativas "follow" das ablações de Liao: GSD e proveniência da geometria. As ablações descritas duas linhas antes são outras duas: proveniência da geometria e variação de sol, clima e ângulo. O GSD não está entre elas, é achado próprio, medido na 8.1. E as linhas 33 a 35 declaram que a literatura não estabelece nada sobre escala, desmontando o que acabou de ser afirmado.

Correção mínima, nas linhas 33 a 35:

> What it does not establish is what that scale becomes for a person in a dense self-built settlement at survey altitude, or what follows when a machine vision system built for mapping is pointed at a territory under armed policing.

Correção completa, separando as duas origens nas linhas 26 a 28:

> One operative variable follows from their ablations, and it is not scene realism in the usual sense: the provenance of the scene geometry. A second, the ground sampling distance at which the target reaches the network, does not follow from their design and is measured directly in Section 8.1.

Na frase seguinte, *"They also qualify the transfer figures above"* atribui a Liao uma ressalva que é dos autores deste artigo. Trocar o sujeito: *"Those figures also require a qualification the cited work does not make: they were obtained..."*.

---

## A15. A seção 2 tem dois fechos, e emenda na seção 3 sem passagem (esforço: 10 minutos, **seção do orientador**)

**`02-literature-review.md`, linhas 13, 31 e 36 a 37.** O diff de `f68d1c5` mostra que o bloco "Aerial person detection and the resolution limit" (linhas 16 a 29) e o segundo fecho (linha 31) foram anexados DEPOIS do fecho que já existia (linha 13, "Positioning this study"). Os dois parágrafos de síntese começam com a mesma fórmula, "Taken together".

Duas opções: mover o bloco de detecção aérea para ANTES de "Positioning this study", de modo que a seção volte a ter um único fecho, ou fundir os dois parágrafos de síntese em um.

Na mesma passagem, resolver a travessia sem ponte para a seção 3. O fecho manda o leitor para "Sections 7 to 11" e a página seguinte abre, sem nenhuma frase de ligação, com *"Rio de Janeiro presents a paradoxical security landscape"* e um bloco de taxas por cem mil habitantes. É a primeira travessia entre autores do artigo. Sugestão para a linha 36 e 37:

> The first is the empirical subject of Sections 7 to 11; the second is the ethical argument this article treats as inseparable from it, and which the next two sections ground in the territory and in the policing that occurs there.

---

## A16. Os 17,6 x 17,5 px são atribuídos ao sensor, e vêm do render em 4K (esforço: 3 minutos)

A tabela da 8.2 dá 17,6 x 17,5 px só na linha `ds_morro_4k`; a 1080p a mesma tabela dá 8,3 x 8,2, e a 8.1 diz textualmente que um quadro do sensor a 150 m entrega alvo de 10 px. As duas seções se desmentem no número que sustenta a recusa.

**`01-introduction.md`, linhas 10 e 11:** resolvido pelo texto de A1 (`and the corpus rendered at 4K`).
**`09b`, linha 71:** resolvido pelo texto de A3.
**`07b`, 9.5 linha 123 e 124:** não tem o defeito, porque fala da altitude e não do sensor. Deixar como está.

---

## A17. O abstract reporta falso positivo "against altitude" e só existe uma altitude (esforço: 1 minuto)

**`01-introduction.md`, linhas 18 e 19.** Os negativos difíceis só existem a 75 m (7.4) e a 9.5 reporta a taxa numa tabela única, intitulada "Quantity at 75 m". Não há contraparte a 150 m para variar contra.

> False positives on those hard negatives are reported at the altitude at which the distinction is measurable at all.

---

## A18. Inserção cirúrgica quebrou a lógica do parágrafo da 10.2 (esforço: 3 minutos)

**`08b-robustness.md`, linhas 29 a 33.** O histórico mostra que `27a6cb0` inseriu *"and it does not extend to the long side, which is 20.6 against 25.0 pixels"* entre o antecedente e o `it` que o retomava. O parágrafo agora declara que a correspondência NÃO é exata e na frase seguinte raciocina sobre *"If it were not exact"*. O leitor não consegue extrair qual é a ameaça que a 10.2 checa.

> That match is a property of the rendering resolution we selected, and it does not extend to the long side, which is 20.6 against 25.0 pixels. Because the match is close in area but not in shape, a transfer failure attributable to scale could be mistaken for a failure attributable to synthesis, and the check below separates the two.

---

## A19. "arm" carrega dois sentidos e os dois convivem (esforço: 5 minutos)

O commit `f68d1c5` declarou aplicada a troca para `branch` no sentido histórico, mas só a 11.6 (linha 109) recebeu. O leitor não sabe se *"an earlier arm of this project reached 0.676"* é um dos quatro modelos da tabela 7.7 ou uma tentativa abandonada, e a ambiguidade recai sobre 0,116, 0,561 e 0,676, que são os únicos números fechados do artigo.

Trocar `arm` por `branch` nas quatro ocorrências de sentido histórico: `03b` linha 203, `07b` linha 20, `08b` linha 16, `09b` linha 13. Deixar `arm` exclusivamente para os braços experimentais nadir e oblíquo (`06b` 87; `07b` 77, 89, 90, 93; `08b` 77, 79, 82, 85; `09b` 33).

---

## A20. Fecho da seção 6 e abertura da seção 7 são parágrafos consecutivos que dizem a mesma frase (esforço: 5 minutos, **seção do orientador**)

**`06-results-proposed-model.md`, linha 11**, contra **`03b` linhas 10 a 14.** *"chosen because it is the only one of the two tasks with a public benchmark against which transfer can be measured"* contra *"it was chosen because it is the only one of the two with a public benchmark against which transfer can be established"*. A ressalva ainda aparece na introdução (linha 51) e na 11.4, ou seja, quatro vezes.

Deixar o enunciado completo na abertura da 7, que é onde o leitor precisa dele, e reduzir o fecho da 6:

> The **training strategy**, however, does not remain a proposal. Section 7 implements it on a different object class, the aerial detection of people, for the reason given at its opening, and Section 11.4 states why the two results must not be read as one.

Trocar `proxy object class` por `a different object class`: a 11.4 diz *"no performance figure reported here transfers from one to the other"*, e se nada transfere não é proxy.

---

## A21. Conclusão: "the previous section" aponta para a seção errada depois da reordenação (esforço: 1 minuto, **seção do orientador**)

**`07-conclusion.md`, linha 9.** Pela `ORDEM`, a seção anterior à Conclusão é a 11, Technical Scope, que não tem uma linha de material jornalístico. O material descrito (ISP-RJ, Fórum Brasileiro, Operação Exceptis, Operação Contenção, e as figuras de população) está nas seções 3 e 4.

> the contextual material assembled in Sections 3 and 4 relies heavily on...

Vale varrer a conclusão inteira atrás de outras remissões por posição (`above`, `earlier`, `described earlier`) que a reordenação possa ter invertido sem deixar rastro numérico.

---

## A22. Conclusão: "autoethnographic" não existe em nenhum outro ponto do artigo (esforço: 2 minutos, **seção do orientador**)

**`07-conclusion.md`, linha 7.** Conferido por grep sem distinção de caixa nos treze arquivos: a palavra aparece uma vez só. A metodologia hoje descreve o componente como *"a qualitative, field-informed contextualization"*. A segunda limitação do artigo se apresenta como retomada de algo que a metodologia não diz.

> The field material contributed by the police co-author, described in the Methodology section, is a second, unavoidable limitation.

Alternativa: reintroduzir o termo na metodologia, que é onde ele descrevia a natureza do dado.

---

# PARTE B: NÃO SÃO REGRESSÕES

Problemas anteriores a esta rodada, alguns amplificados por ela. Dois deles são mais graves que várias regressões acima.

---

## B1. A 10.3 tem premissa contradita pela tabela e condição de falseamento invertida (esforço: 15 minutos, alta prioridade)

Este é o item mais sério da Parte B: rodado como está escrito, o teste registrado de antemão **confirma a hipótese quando ela falha**, o que é exatamente o contrário do que a Seção 10 se propõe a fazer.

**`08b-robustness.md`, linhas 58 e 59.** Diz *"Section 8.3 measures that hard sunlight yields the largest raw figure-to-background difference"*. A tabela da 8.3 dá 16,4 ao encoberto e 15,2 ao sol forte, e a prosa da 8.3 (linha 144) diz literalmente *"hard sun achieves that while sitting second on raw contrast"*.

> Section 8.3 measures that hard sunlight sits second on raw figure-to-background difference while giving one of the two lowest ratios of contrast to local clutter, and raises the hypothesis that the detector performs better under overcast than under hard sun.

**`08b`, linha 68, condição de refutação.** *"If per-regime performance does not order inversely with raw contrast"*. O encoberto é o PRIMEIRO nas duas colunas (16,4 bruto e 0,88 sobre desordem). Ordenar inversamente ao contraste bruto preveria a chuva (6,6) como o melhor regime e o encoberto como o pior, o oposto da hipótese que a 10.3 defende.

> If per-regime performance orders with raw contrast rather than with contrast over local clutter, or if hard sun is not among the weakest regimes, the mechanism proposed in Section 8.3 is wrong and the operational implication in Section 11.3 is withdrawn.

**`09b-technical-limitations.md`, 11.3, linhas 49 a 51.** A mesma condição invertida se repete. A primeira frase da 11.3, essa sim, está correta.

> Section 10.3 specifies the test. If per-regime detector performance does not order with contrast over local clutter, this implication is withdrawn and the contrast measurement stands only as a description of the imagery.

---

## B2. "The illumination condition that maximises apparent contrast" lê a tabela 8.3 ao contrário, em dois lugares (esforço: 5 minutos)

Mesma família de B1. Quem maximiza o contraste aparente é o encoberto (16,4 bruto), e ele é também o melhor na coluna de contraste sobre desordem (0,88), ou seja o que MENOS sofre com a desordem. Quem enche o fundo de desordem é o sol forte (0,64 com 15,2 bruto, o que implica o maior desvio de anel da tabela).

**`06b`, linha 163 e 164, fecho da 8.4**, e **`07-conclusion.md`, linhas 42 e 43, primeiro dos três fechos.** A conclusão copia a frase da 8.4, então corrigir só uma criaria divergência. Sugestão para as duas:

> and the illumination condition conventionally preferred for flying, hard sun, is the one whose cast shadow fills the background with the clutter that competes with the figure.

Evitar a fórmula "maximises apparent contrast", que a coluna de contraste bruto atribui ao encoberto.

---

## B3. O artigo diz duas coisas incompatíveis sobre os números de Liao et al. (esforço: decisão sua, depois 5 minutos)

A 7.2 (`03b` linhas 44 a 55) trata 27,0 pontos e 22 a 23 pontos como medidas firmes e usa o número para uma concessão central sobre o próprio método (*"the cost is quantified here from their result"*). A 7.5 (`03b` linhas 174 a 176) declara: *"As above, we rely on the direction of that result rather than on the reported magnitudes, which we have not verified against the published text"*. O `As above` descreve errado o que a 7.2 fez. O bloco novo da revisão amplificou ao repetir a magnitude num terceiro lugar (`02` linha 24).

Decidir e uniformizar nos três pontos:
- Se a tabela de Liao foi conferida: cortar `which we have not verified against the published text` da 7.5 e dizer apenas que a magnitude da ablação de iluminação não é reportada de forma comparável.
- Se não foi: retirar o 27,0 da 7.2 e da revisão, manter só a direção nos três lugares, ou marcar a magnitude como pendente de conferência.

---

## B4. A 7.2 diz que o protocolo ético proíbe o que a 11.6 diz que o projeto fez (esforço: 3 minutos)

**`03b`, linhas 52 a 55**, contra **`09b` linhas 109 e 110.** As duas frases foram escritas no mesmo commit `235cb23` e, lidas juntas, dizem que o projeto fez o que o artigo declara que o protocolo ético proíbe. Além disso a Seção 5 não veda reconstrução a partir de imagem preexistente: ela veda coletar imagem nova de residentes, publicar coordenada em nível de endereço, e exige revisão ética para coleta futura.

Precisar o que o protocolo veda, na 7.2:

> ...would require a photogrammetric reconstruction of the target site released alongside the article, which the ethical protocol of Section 5 forecloses, so the cost is quantified here from their result and not from ours.

---

## B5. Ponteiro sem destino na 7.3 (esforço: 1 minuto)

**`03b`, linhas 117 e 118.** *"Section 8.1 reports what this does to the target, and Section 11 states the limitation it introduces"*. Nenhuma das seis subseções da Seção 11 trata da limitação de renderizar a 4K uma cena cujo sensor grava a 1080p (11.1 é escala de TREINO, 11.2 o benchmark, 11.3 iluminação, 11.4 as duas tarefas, 11.5 as altitudes, 11.6 reprodutibilidade). A ressalva existe, mas está na própria 8.1.

> Section 8.1 reports what this does to the target, and states the caution it introduces.

---

## B6. A 8.4 remete o problema de projeto para a metodologia (esforço: 1 minuto)

**`06b`, linha 160.** *"the measurements reframe the design problem stated in Section 5"*. A Seção 5 é Methodology (protocolo, coleta, posicionalidade). O problema de desenho (backbone, pipeline sintético, fine-tuning consentido) está na Seção 6, que esta rodada renomeou literalmente para "Design". Não é erro de remapeamento, a remissão sempre apontou para a metodologia; o que mudou é que agora existe uma seção chamada Design ao lado, o que torna o ponteiro visivelmente impreciso.

> Taken together the measurements reframe the design problem stated in Section 6.

---

## B7. O check da 10.7 promete um manifesto que a 11.6 diz não existir (esforço: 2 minutos)

**`08b`, linhas 129 e 130.** *"Every image carries its seed, illumination regime, camera altitude and pitch in a manifest entry"*, em presente e sem ressalva. A 11.6 diz o contrário para os corpora efetivamente reportados. Como a auditabilidade é um dos pilares da defesa do método, a divergência é cara.

> Every image carries its seed, illumination regime and camera altitude in a manifest entry, and camera pitch in corpora generated after that field was added.

---

## B8. A delimitação atribui à seção 2 um escopo que é da seção 1 (esforço: 2 minutos, **seção do orientador**)

**`07-conclusion.md`, linha 21.** Planejamento de trajetória e policiamento aéreo são revisados na introdução (Rasoulie e Pashazadeh, Xu, Agrawal, Jiang, Wang e Qian, Chen, Yan). A seção 2 trata de assentamento informal, dimensão vertical, dado sintético e limite de resolução, e a delimitação omite justamente os dois últimos.

> The comparative literature review in Sections 1 and 2 was restricted to UAV trajectory planning, aerial policing, machine vision applied to informal settlements, and the resolution limits of aerial person detection.

Tem o efeito colateral útil de reconhecer no texto que metade da revisão está na introdução.

---

## B9. O trecho das "two bodies of literature" aparece quase palavra por palavra em dois lugares (esforço: 5 minutos, **seção do orientador**)

**`01-introduction.md`, fim do parágrafo da linha 45**, e **`02-literature-review.md`, linha 13.** As duas versões listam a mesma série (surveillance, reconnaissance, patrol, target tracking, situational awareness, path planning), a mesma contraparte (mapping, photogrammetry, remote sensing, three-dimensional reconstruction, urban planning, building classification) e a mesma conclusão sobre a interseção. O leitor lê o mesmo parágrafo duas vezes e conclui que a revisão não acrescenta nada à introdução.

Deixar a formulação completa na revisão, que é onde ela pertence, e reduzir a da introdução a uma remissão:

> The intersection of these two literatures, characterised in Section 2, constitutes the gap this research addresses.

Preservar a frase do gap, que hoje só existe na versão da introdução.

---

# PARTE C: copidesque final, não é bloqueio de leitura

**C1. Registro e ortografia mudam na fronteira entre autores, e a fronteira mais visível está na primeira página.** Contagem por arquivo: `03b`, `06b`, `07b`, `08b` e `09b` são britânicos (21, 8, 10, 7 e 6 ocorrências de colour/artefact/metres/randomis/per cent) e usam primeira pessoa do plural (14 ocorrências de we/our); `01`, `02`, `04`, `06` e `07-conclusion` são americanos (8, 8, 8, 4 e 6 ocorrências de modeling/optimization/characterized/randomiz), e só o abstract, dentro do `01`, tem 4 britânicas e um `our`. As seções `05` e `03` não têm nenhuma das duas.

Escolher uma variante (a Elsevier aceita as duas, desde que consistente) e passar um normalizador antes da submissão: -ise/-ize, metre/meter, colour/color, artefact/artifact, per cent/percent, vírgula de série. Decidir também se o artigo usa primeira pessoa do plural, hoje presente só nas seções técnicas.

---

# Sequência sugerida

**Passada 1, quinze minutos, resolve o que um revisor veria primeiro:** A1, A2, A17 (abstract e os dois números vencidos), depois a varredura A3 inteira de uma vez.

**Passada 2, quarenta minutos, o miolo técnico:** A6 (os quatro consertos da 8.2), A7, A8, A9, A10, A11, A12, A13, A18, A19, e B1 com B2 juntos, porque leem a mesma tabela.

**Passada 3, vinte minutos, a moldura:** A14, A15, A20, A21, A22, B8, B9. São seções do orientador; se preferir devolver em bloco, isto vira uma entrada em `01-artigo/PENDENCIAS.md`.

**Passada 4, dez minutos, os ponteiros soltos:** B3 (exige sua decisão sobre Liao), B4, B5, B6, B7.

**Depende dos coautores:** A4 e A5 tocam texto do delegado; a reescrita sugerida em A4 mantém o vínculo com a parte técnica, que você pediu para manter, e tira só as duas afirmações sem lastro. A14, A15, A20, A21, A22, B8 e B9 tocam texto do orientador.

**Só depois de tudo isso, regerar o PDF:** `python 01-artigo/ferramentas/monta_artigo.py --formato elsevier --out <caminho>`. Mas para a leitura de hoje basta fechar e reabrir o arquivo que já está no Desktop: ele está correto.