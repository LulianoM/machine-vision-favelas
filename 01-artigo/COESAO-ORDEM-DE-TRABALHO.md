# ORDEM DE TRABALHO: COESÃO E FLUXO
## Artigo Machine Vision from the Global South, manuscrito de 2026-09-22

Li os treze arquivos na ordem de `ORDEM` em `monta_artigo.py` e conferi por busca os pontos em que as sete lentes divergiam entre si. Consolidei 99 achados em 24 itens, fundindo os duplicados e agrupando por arquivo quando as edições se tocam.

---

## DIAGNÓSTICO EM TRÊS LINHAS

O artigo não são três textos grampeados. É **um** texto com **três costuras**, e todas as três são do mesmo tipo: a reescrita de título e abstract de 22/09 avançou nas pontas (abstract, 9.5, 11.5) e não atravessou o miolo. O resultado é que (1) o leitor recebe três declarações diferentes do que o artigo tenta fazer, em três lugares onde ele naturalmente procura por isso (abstract, pergunta de pesquisa, fecho); (2) a conclusão diz duas vezes, com quarenta linhas de distância, que o pipeline foi construído e que o pipeline precisa ser construído; (3) seis remissões internas apontam uma seção adiante do alvo, sequela da reordenação.

Nada disso é problema de conteúdo. É problema de sincronia. Os itens da Faixa 1 abaixo são cerca de duas horas de edição e consertam a maior parte do tropeço.

---

# FAIXA 1: MUITO CONSERTO, POUCO ESFORÇO

Doze edições pontuais. Nenhuma depende de medição nova, nenhuma depende de decisão de conteúdo dos coautores, exceto onde marcado.

### 1. `06b-model-free-evidence.md`, `03b-methodology-synthetic-pipeline.md`, `09b-technical-limitations.md`: corrigir as seis remissões internas que apontam para a seção errada

Seis lentes acharam isto por caminhos diferentes. É o conserto de maior retorno do artigo: hoje o leitor que segue um ponteiro cai em lugar nenhum seis vezes.

| arquivo:linha | está | fica |
|---|---|---|
| 06b:6 | "Section 10 reports detector performance" | "Section 9 reports detector performance" |
| 06b:101 | "Section 10.3 reports the S-oblique arm" | "Section 9.3 reports the S-oblique model" |
| 06b:102 | "Section 11.4 treats the difference between the arms" | "Section 10.4 treats the difference between the models" |
| 06b:157 | "is the subject of Section 10" | "is the subject of Section 9" |
| 03b:11 | "The conceptual model proposed in Section 5" | "The conceptual model proposed in Section 6" |
| 09b:55 | "The model proposed in Section 5 and Section 6" | "The model proposed in Section 6" |

**Atenção, aqui duas lentes erraram e uma acertou:** para 06b:102 o alvo certo é **10.4**, não 11.2. Conferi. A 10.4 chama-se "Capture geometry against scene content" e é exatamente a atribuição isolada da diferença à posição da câmera; a 11.2 diz o quase oposto (que um corpus oblíquo que transfere melhor informa sobre o VisDrone e não recomenda geometria); a 11.4 trata de duas tarefas que compartilham pipeline. Use 10.4.

Mais duas na mesma família, de ambiguidade e não de erro:
- **03b:6**, "The design-science component of Section 5", vira "The design-science component declared in Section 5 and specified in Section 6". A seção 5 nomeia o componente, ela não propõe o modelo.
- **03b:17**, "Section 10 restates the boundary", vira "Section 11 restates the boundary". Obrigatório se o item 2 abaixo for aplicado.
- **06b:150**, "the design problem stated in Section 5": defensável como está (a seção 5 de fato enuncia a restrição ética que cria o problema de desenho). Se quiser padronizar, "stated in Sections 5 and 6". Baixa prioridade.

Depois de aplicar, vale rodar uma conferência mecânica de todas as remissões contra a lista `ORDEM`. Conferi as demais uma a uma e estão corretas (as de 03b para 8.1, 8.2, 8.3 e 11.1; as de 07b para 10.1, 10.2 e 8.1; as de 08b e 09b inteiras), mas a deriva pode voltar na próxima reordenação.

### 2. `08b-robustness.md`: apagar a subseção 10.8 inteira

Ela faz três coisas ruins de uma vez. O primeiro parágrafo é quase verbatim a 11.2, que vem duas páginas adiante (comparei frase a frase: "no claim of the latter is made anywhere in this article" contra "no claim of that kind is made anywhere in this article"). O segundo parágrafo, "The class distinction between armed and unarmed figures is not evaluated at all", **contradiz frontalmente** a 9.5, que avalia a distinção a 75 m com tabela de cinco linhas, e contradiz o abstract, o título e a 11.5. E ela é a única subseção da seção 10 sem teste, quebrando o padrão ameaça/teste/condição de refutação que define a seção.

Se preferir manter um marcador no lugar em vez de deletar, este é o texto mínimo:

> ### 10.8 What this design cannot rule out
> Two boundaries of this design are structural rather than testable, and are stated in Section 11 rather than here: the benchmark is not a favela (Section 11.2), and the armed and unarmed distinction is reported at 75 m and deliberately withheld at 150 m (Section 11.5).

Aplicando isto, ajustar 03b:17 como diz o item 1.

### 3. `07b-results-placeholder.md` linha 100: corrigir a legenda da figura 4, que nega a tabela impressa quarenta linhas abaixo dela

Hoje diz "no accuracy figure for that distinction is reported anywhere in this article". A tabela de 9.5 reporta exatamente isso. Texto sugerido:

> Green marks the armed class and blue the unarmed class. No accuracy figure for that distinction is reported at this altitude, for the reason given in Section 11.5; the 75 m result is reported in Section 9.5.

### 4. `07b-results-placeholder.md` linha 144 e `09b-technical-limitations.md` linha 95: tirar os dois ponteiros que mandam o leitor à 11.3 atrás de coisa que não está lá

Conferi as sete subseções da 10 e as seis da 11: **não existe em lugar nenhum do artigo uma condição de retirada para os números de 75 m**. A 11.3 trata da implicação de iluminação, e a condição que ela enuncia é sobre ordenação por regime de clima.

Fecho sugerido para a seção 9 (07b:143-144), que também resolve a colisão de vocabulário do item 16:

> The fourth row is the quantity of interest. It is the rate at which the system would mark a resident carrying a broom, a length of pipe or a rolled mat as armed, and it is the concrete form of the dual-use harm this article discusses. Section 10 states, for each result above, the condition that would overturn it, and Section 11.5 reads the two altitudes together.

Em 09b:95, o mínimo é cortar a oração. O correto é escrever a condição que falta (ver item 21, que fica na faixa de depender do que for implementado depois).

### 5. `06-results-proposed-model.md` linha 1: renomear a seção 6, porque hoje há duas seções chamadas Results e a que não tem número nenhum vem primeiro

O montador numera as duas na ordem de leitura, então o PDF traz "6. Results: A Proposed Machine Vision Model..." sem um único número dentro, e "9. Results: Transfer to Real Imagery" com todos eles. O leitor passa a desconfiar da numeração. Nenhuma remissão interna cita a seção 6 pelo título, então a troca não quebra nada.

> `## Design: A Machine Vision Model of Vertical Morphology`

(alternativa mais neutra: `## The Proposed Model and Its Training Strategy`.)

### 6. `07-conclusion.md` linha 35: trocar a frase de abertura do Closing, que contradiz os três parágrafos que ela mesma introduz

Os três pontos que vêm depois (GSD, silhueta por pitch e clutter; o que a síntese compra; a capacidade que aparece e desaparece com a altitude) já servem o enquadramento novo. Só a frase de abertura ficou no antigo.

> This article set out to ask under what acquisition conditions an aerial system can tell an armed person from an unarmed one over a dense self-built settlement, and what it costs to answer that question responsibly. Three things follow from the work reported above.

### 7. `07-conclusion.md` linhas 60 a 63: realinhar a última frase do artigo

> What remains open is not primarily technical. A system that can tell an armed person from an unarmed one and a system that is safe to point at Jacarezinho are different objects, and nothing in the engineering reported here decides the second. That decision belongs to a process that includes the residents of the territory, and it has not taken place.

### 8. `07-conclusion.md` linha 27: a frase que diz que nada foi construído, vinte e duas linhas depois da frase que diz que tudo foi

É a contradição mais visível do artigo, e está dentro da mesma seção. Linha 5: "a synthetic corpus has been generated and detectors have been trained on it". Linha 27: "the domain-randomization strategy proposed here needs to be built and tested before any of its claims can be taken as more than plausible", sem qualificador nenhum, depois de cinco seções que a construíram e testaram.

> On the technical side, the domain-randomization strategy proposed here has been built and partially tested: the generator, the corpus and the three-model evaluation protocol are reported in Sections 7 to 10, against a public aerial benchmark. What remains untested is specific rather than general: the controlled measurement of training scale described in Section 11.1, the per-regime illumination test specified in Section 10.3, and repetition across independent settlement seeds (Section 10.7). Beyond those lies the half of the work that has no evaluation infrastructure at all, the morphological task of Section 11.4, and, separately from any of it, validation against real imagery of the territory, which is the stage the ethics process described above would have to precede.

No mesmo parágrafo, a proposta de "benchmarking against publicly available, already-consented imagery (Kigali, Slovo Park)" como **primeiro** estágio futuro ignora que a 7.7 já fixou um protocolo contra o VisDrone. Reescrever como alternativa ao VisDrone, com a razão dita, e não como estreia.

### 9. `06-results-proposed-model.md` linha 9: reescrever o último parágrafo da seção 6, que é a junção mais visível do artigo

Hoje a seção 6 fecha com "At this stage, the study's result is the conceptual architecture... together with an explicit account of what would be required to move from this proposal to a validated, field-tested system", e a linha seguinte do artigo montado é a seção 7 especificando Blender 5.2 headless, YOLO11s e RTX 2060. É o ponto onde o texto do orientador encontra o do mestrando, e o leitor cai no vazio.

> At this stage, the study's contribution under this heading is the conceptual architecture described above, not a deployed system: moving from one to the other would require independent ethical review, meaningful community consultation, and a governance framework for use limitation that falls outside the scope of a single research article. The training strategy, however, does not remain a proposal. Section 7 implements it, and Sections 8 to 11 report what it achieves on a proxy object class, the aerial detection of people, chosen because it is the only one of the two tasks with a public benchmark. Section 11.4 states why the two results must not be read as one.

### 10. `03b-methodology-synthetic-pipeline.md` linha 209: baixar "dominant mismatch" ao que a seção 8 de fato sustenta

A 8.2 diz explicitamente que o valor do benchmark "anchors the direction of the relationship but not its slope"; a 10.4 trata a geometria como ameaça com resultado por medir; a 9.3 diz que os dois desfechos são possíveis. Dominância nunca foi comparada contra outro termo.

> The difference mAP50(S-oblique) minus mAP50(S-nadir) isolates the contribution of capture geometry, which Section 8.2 measures as the largest mismatch between this corpus and the benchmark, and which Section 10.4 treats as an open question rather than a settled one.

### 11. `03b-methodology-synthetic-pipeline.md` linhas 95 e 96: a mesma correção, na direção oposta

Hoje: "Section 8.3 shows that this clutter, rather than illumination level, governs how hard a person is to detect". A própria 8.3 recusa isso na linha 144 ("a contrast statistic is not a detection statistic") e a 11.3 repete a ressalva.

> ...and Section 8.3 measures the contrast a person presents against that immediate background, which Section 10.3 tests as a hypothesis about detector difficulty.

### 12. `07b-results-placeholder.md` linhas 113 a 117: duas orações que o artigo desmente em outro lugar

A tabela logo acima ajusta com 5 e 10 por cento do VisDrone-DET train, que é imagem pública de cena urbana densa, não imagem consentida do território. O artigo é rigoroso com essa distinção em 11.2 e a abandona aqui. E o intervalo "5 to 20 per cent... 85 to 95 per cent" é atribuído à seção 2, que não o contém (li a seção 2 inteira: traz Horváth, Barisic e a fórmula genérica "a modest volume of real, fine-tuning data", nenhum número de fração).

> This is the quantity with the clearest practical meaning for the proposal in Section 6: how much real aerial imagery the synthetic pretraining removes the need for, measured on a public benchmark. Whether the same fraction holds for consent-bounded imagery of the case study territory is not established here, for the reason given in Section 11.2. The sim-to-real literature surveyed in Section 2 establishes that a modest volume of real data substantially improves generalisation from synthetic pretraining, but not how much is needed at this ground sampling distance or in this scene type, which is what these rows answer.

---

# FAIXA 2: CONSERTO GRANDE, ESFORÇO MÉDIO

Reescrita de parágrafos. É aqui que o artigo passa a ter uma espinha só.

### 13. `01-introduction.md` linhas 45 e 47: reescrever a pergunta de pesquisa e o objetivo, mais uma declaração de escopo de três linhas

Este é o item de maior impacto do artigo inteiro, e é o que exige decisão dos coautores (ver o fim desta ordem). Hoje o leitor recebe três objetos: o título e o abstract prometem condição de aquisição para reconhecimento de pessoa armada; a pergunta (linha 45) promete "UAV perception, navigation, and situational awareness"; o objetivo (linha 47) promete "mapping the vertical morphology of a favela". Conferi por busca: `navigat`, `GNSS`, `trajectory`, `line of sight` e `situational awareness` aparecem **zero** vezes nas seções 7 a 11. `terrain-aware` aparece uma vez no artigo inteiro, dentro da própria pergunta.

Pergunta (linha 45):
> This article accordingly poses the following research question: **Under what acquisition conditions, and at what cost in transfer, does synthetic imagery of a dense self-built settlement support the aerial recognition of an armed person?**

Objetivo (linha 47):
> Our objective, correspondingly, is to establish the acquisition conditions (altitude, sensor, camera geometry, and illumination) under which a person observed from the air can be distinguished as armed or unarmed, and to measure what a detector trained on synthetic imagery alone recovers of that capability, using Jacarezinho, in Rio de Janeiro, as the morphology the synthetic corpus reproduces and as the site whose vertical complexity motivates the choice.

Declaração de escopo, três linhas novas logo após o objetivo. Ela antecipa para a introdução o aviso que hoje só chega na linha 11 da seção 7, doze páginas adiante:
> Two object classes are in play, and they should be separated at the outset. The vertical morphology of the settlement is what the model proposed in Section 6 is designed to classify, and it is the reason this site was chosen. The instrument evaluated in Sections 7 to 11 detects people, and at the lower of the two altitudes, armed people. Only the second has a public benchmark against which transfer can be measured, which is why it, and not the first, carries the empirical claims of this article.

### 14. `01-introduction.md` linhas 33 a 41: parágrafo de abertura novo, e encolher o bloco de planejamento de trajetória

Entre o abstract (arma, pixel, altitude, GSD) e a primeira página da introdução (TAMOPSO, RRT, ACO, A*, fluxo óptico, multipath de GNSS, cerca de 900 palavras) há dois textos de assuntos diferentes encostados. Nenhuma dessas obras é retomada em lugar nenhum do artigo.

Abertura nova, antes da linha 33:
> Aerial systems are already being bought and flown on the premise that a camera above a city can tell an armed person from an unarmed one. What is rarely stated alongside that premise is the altitude and the sensor at which the distinction is visible at all. Answering that requires a reading of policed urban space that the aerial literature has largely not offered, and the reason it has not is the subject of what follows.

E o bloco de trajetória encolhe de três parágrafos para um, cumprindo a única função argumentativa que hoje cumpre (mostrar que a literatura de UAV policial herda a cidade como rede de ruas e ignora a dimensão vertical), fechando com a ponte que devolve o leitor ao assunto:
> The same planar inheritance reappears one level down, at the level of perception, in the assumption that an aerial view of a person is a view of a standing figure. Section 8.2 measures what nadir acquisition does to that assumption.

A ponte funciona porque a 8.2 mede exatamente a razão altura sobre largura que separa figura em pé de planta de cabeça e ombros.

### 15. `03b-methodology-synthetic-pipeline.md` linhas 10 a 18: inverter o preâmbulo da seção 7, que hoje apresenta a tarefa do título como substituta

Sob o título novo, detecção de pessoa armada **é** o assunto do artigo, e o parágrafo está com o sinal trocado ("The reason for implementing the second rather than the first is that only it has a public benchmark"). Invertendo, a 11.4 deixa de ser confissão e vira achado. Este parágrafo também é o único lugar razoável para declarar as três classes, que hoje entram no artigo pela legenda da figura 5 (conferi: `armed` ocorre **uma vez** em toda a seção 7, e é dentro da legenda).

> A distinction has to be drawn at the outset, because the two are easy to conflate. What is implemented and evaluated below detects people, in three classes: armed, unarmed, and unarmed carrying a confusable elongated object. That is the task this article measures, and it was chosen because it is the only one of the two with a public benchmark against which transfer can be established. The conceptual model proposed in Section 6 classifies built form instead: building height, rooftop addition, material transition. The same generator already records the footprint, the storey count and the roof height of every structure it builds, so the morphological task is a second experiment over the same infrastructure rather than a different pipeline; what it lacks is an evaluation set, and Section 11.4 records that absence as a finding rather than as an omission. Nothing below should be read as a validated capability over Jacarezinho, and Section 11 restates the boundary.

### 16. `03b-methodology-synthetic-pipeline.md`: descrever o corpus de 75 m na seção de método, de onde ele hoje está inteiramente ausente

Conferi por busca: `75 m`, `firearm`, `weapon` e `confusable` têm **zero** ocorrências em 03b. A 7.3 fixa uma única câmera (Zenmuse Z30, nadir, 150 m) e a tabela de 7.7 declara exatamente três modelos. Em 9.5 o leitor encontra um quarto aparato experimental completo, com corpus próprio, cinco modelos de arma, nove objetos confundíveis e três classes, nada disso construído diante dele. É o único ponto do artigo em que um experimento inteiro surge sem procedimento, num texto que abre cada seção técnica com nota de proveniência.

Três edições:
- **7.3**, parágrafo novo com a segunda geometria de câmera a 75 m, a GSD resultante e a razão aritmética (6,4 vezes a área).
- **7.4**, parágrafo novo sobre objetos carregados e negativos duros: os cinco modelos de arma, os nove objetos alongados (vassouras, rastelos, cano plástico, vergalhão, tábuas, guarda-chuvas, enxadas, esteiras enroladas, mangueira), o critério de paleta de cor e rugosidade compartilhada, a distribuição de poses de porte, e a contagem por classe.
- **7.7**, quarta linha na tabela de modelos, com nome no mesmo padrão: `S-nadir-75`. Passando a usar `S-nadir-150` onde a altitude precisar ficar explícita.

**Isto é movimentação, não redação nova.** O material descritivo já está escrito em 11.5, linhas 80 a 88. Depois da mudança, a 11.5 cita a 7.4 em vez de descrever pela primeira vez, e o item 22 (de-duplicação) fica resolvido de graça.

Feito isso, **não** é preciso criar a 9.1 de dois regimes que uma das lentes propôs: o leitor já chega na seção 9 sabendo das duas altitudes, e deslocar o teto da 9.1 custaria mais do que rende. Basta uma frase no preâmbulo da seção 9 dizendo em que subseção cada altitude é reportada.

### 17. `03-methodology.md` linha 3: declarar o quarto componente, porque a metodologia não anuncia o experimento que ocupa cinco seções

Hoje a seção 5 declara três componentes e o verbo do técnico é "proposes". Quatro páginas depois aparecem Blender headless, YOLO11s, RTX 2060, protocolo de ladrilhamento, split por cena e três modelos avaliados no VisDrone, nada disso anunciado como método.

> The study combines four components: a structured literature review; a qualitative, field-informed contextualization (Sections 3 and 4); a design-science component that proposes a technical model architecture and training strategy (Section 6); and a computational component that implements that strategy, generates a synthetic corpus, measures its properties before any detector is trained, and evaluates transfer to a public aerial benchmark against a ceiling trained on real data (Sections 7 to 10). The evaluation protocol of the fourth component was fixed before any model was trained; it is specified in Section 7.7 rather than here because it is long. That component instantiates the proposal of Section 6 on a different object class, the aerial detection of people, for the reason given at the opening of Section 7.

"O protocolo foi fixado antes de qualquer treino" hoje é um ponto forte escondido numa nota de proveniência da seção 9. O lugar dele é aqui.

### 18. Apresentar o voo de levantamento de 2022 uma vez, em lugar nenhum ele é apresentado

O abstract (linha 11) diz "the 2022 police survey that motivates this study" com artigo definido, para algo que o leitor nunca viu. Busquei: o voo reaparece em 03b:89, 03b:102, 03b:204, 06b:50, 07b:45, 07b:96, 09b:34, 09b:68 e 07-conclusion:40, em **seis formulações diferentes**, e nenhuma das seções 1 a 6 menciona que existe um voo policial sobre o território do caso. Agrava que a seção 5 declara que o estudo não coleta imagem em favela por impedimento ético, o que faz a menção repetida a um levantamento policial sobre o mesmo território levantar uma pergunta que o texto nunca responde.

Parágrafo novo, em `03-methodology.md` (a proveniência do dado é matéria de método):
> The study's acquisition parameters are not hypothetical. A police photogrammetric survey of the case study area was flown in August 2022, before and independently of this research, with a Zenmuse Z30 recording at 1920 by 1080, nadir, 150 metres above ground. No image from that survey, and no product derived from it, is published in this article or in any material accompanying it. What the survey supplies is a sensor and an altitude: the virtual camera of Section 7.3 reproduces both, so that the acquisition conditions evaluated here are the ones a real flight over this territory actually used.

Depois, padronizar em uma forma só, "the 2022 survey flight", e trocar 03b:102 por "the sensor of the 2022 survey flight described in Section 5". No abstract, "the 2022 police survey that motivates this study" vira "the 2022 police survey described in Section 5".

(Uma lente propôs pôr este parágrafo no fim da seção 4, na voz do delegado. Funciona também e ancora melhor o território; é escolha de autoria. O que não pode é continuar sem apresentação.)

### 19. `02-literature-review.md`: acrescentar o bloco que prepara a metade empírica, hoje inteiramente ausente

Conferi por busca: **`Liao` e `Kiefer` têm zero ocorrências na seção 2**. `VisDrone` também. O leitor conhece Gram-Hansen, Du, Hu e Watson & Elliott, que sustentam a tarefa que o artigo **não** implementou, e não conhece nenhuma das três coisas que sustentam a que implementou. Pior: a seção 2 fecha instalando Horváth et al. com "above 86% in zero-shot transfer", e a seção 9 compara-se a uma razão de 23,2 por cento. Ninguém reconcilia 86 com 23, e a 03b:45 ainda invoca "In their taxonomy" para uma taxonomia nunca apresentada.

Bloco novo ao fim de "Synthetic data and the sim-to-real gap":
> Aerial person detection and the resolution limit. The evidence above concerns objects that occupy a substantial share of the frame. The task this article evaluates does not. Kiefer, Ott and Zell (2022) trained three detectors purely on synthetic data and evaluated them on VisDrone, the standard public benchmark for aerial detection in dense urban scenes, reporting mAP50 of 1.2, 2.4 and 10.2 against 24.6, 48.6 and 43.9 for the same architectures trained on real imagery. In a top-down view of a crowded street, purely synthetic training recovers a fraction of what real data achieves. Liao et al. (2026) identify where that fraction is won or lost: in an aerial synthetic corpus built in Unreal Engine they ablate two factors, and replacing a photogrammetric reconstruction of the target site with generic assets costs 27.0 mAP50 points on YOLOv11, while removing variation in sun position, weather and viewing angle costs accuracy again, with the largest penalty on truncated objects. Two operative variables follow, and neither is scene realism in the usual sense: the ground sampling distance at which the target reaches the network, and the provenance of the scene geometry. They also qualify the figures above: transfer beyond 86 per cent was obtained on large objects in a controlled scene, not on a person seen from 150 metres.

Isto resolve quatro coisas de uma vez: a revisão passa a apontar para o achado em vez de contra ele; `ground sampling distance`, que é o eixo da tese nova, ganha primeira aparição no corpo; a taxonomia da 03b:45 ganha referente; e o VisDrone deixa de estrear numa célula de tabela de protocolo.

Faltará ainda um bloco sobre uso dual e vigilância de território. A introdução declara o uso dual "a central, rather than peripheral, concern" e o Closing o promove ao terceiro ponto, e a seção 2 não tem uma linha sobre ele (a seção 12, linha 21, confirma por escrito ao delimitar a revisão para fora de vigilância urbana e policiamento preditivo). Ou entram quatro ou cinco obras, ou a palavra "central" sai da introdução.

### 20. `01-introduction.md` linha 43 e `02-literature-review.md` linha 13: desfazer a duplicação quase verbatim entre introdução e revisão

O fecho da seção 2 repete o penúltimo parágrafo da introdução palavra por palavra, com as mesmas duas listas de seis e de sete itens ("surveillance, reconnaissance, patrol, target tracking, situational awareness, and path planning" e "mapping, photogrammetry, remote sensing, three-dimensional reconstruction, urban planning, and building classification"). Gevaert et al. (2016), Sithole e Mhangara (2025) e da Silva et al. (2024) também são descritos duas vezes cada um, com a mesma função argumentativa e quase a mesma redação.

Recomendo: **formulação completa das duas literaturas fica na introdução**, que é onde a lacuna é anunciada e de onde nasce a pergunta. O fecho da seção 2 passa a fazer o que só ele pode fazer, dizer o que a literatura revista estabelece e o que ela não estabelece:

> Taken together, the literature reviewed here establishes two things and leaves a third untouched. It establishes that domain-randomized synthesis transfers to aerial detection tasks, and that the vertical dimension of informality has been repeatedly recognized without being integrated. What it does not establish is anything about the scale at which an aerial target reaches a detector, or about what follows when a machine vision system built for mapping is pointed at a territory under armed policing. The first is the empirical subject of Sections 7 to 11; the second is the ethical argument this article treats as inseparable from it.

Nas três obras duplicadas: descrição completa na revisão, menção de uma linha na introdução.

### 21. `04-situating-the-study.md` e `05-case-jacarezinho.md`: fechar as duas seções de campo em direção ao miolo técnico

Hoje as duas terminam olhando para trás, e a ligação só é feita no sentido contrário, quando a 7.1 cita a seção 3 para justificar a impossibilidade de consentimento. A seção 4 é **órfã em sentido literal**: busquei `Section 4` nos treze arquivos e há **zero** ocorrências. Nenhuma outra seção remete a ela.

Fecho da seção 3 (após 04:15):
> One consequence of this record bears directly on what follows. The legal and operational category on which the use of lethal force turns, in each of the episodes above and in the contestation that followed them, is whether the person engaged was armed. That is a visual judgement made at speed, and it is increasingly proposed as one an aerial system could assist. Sections 8 to 11 report what that judgement actually demands of the acquisition: at the altitude of the survey flown over this territory, the distinction is not resolvable at all, and it becomes resolvable only at an altitude no operation has flown.

Última frase da seção 4 (05:7), substituindo as três coisas nomeadas que o artigo não engaja:
> ...remains contested. What this study engages is narrower, and prior to it: whether an aerial system flown over this morphology can resolve the distinction on which the use of lethal force is justified, and under what acquisition conditions.

Acrescentar também à seção 4 um parágrafo de morfologia mensurável (faixa típica de largura de beco, proporção de paredes geminadas, número típico de pavimentos, frequência de laje ocupada e de recuo do pavimento superior, declive), para que a 7.2 passe a abrir cada um dos três estágios citando-o ("The gap distribution is set from the alley widths reported in Section 4"). Hoje a 7.2 calibra tudo isso e justifica por "as they are in consolidated self-built settlement", genérico, nunca por Jacarezinho, enquanto 10.8 e 11.2 dizem duas vezes que nada se afirma sobre Jacarezinho. Onde o número vier do ortomosaico da PCERJ, citar como faixa, sem coordenada.

**Topografia:** a seção 4 nunca menciona relevo, e três seções técnicas afirmam que a morfologia reproduzida é de encosta (03b:87 "as they do on a real hillside", 08b:145, 09b:26), e a conclusão (linha 31) afirma "Jacarezinho's specific combination of steep topography" como estabelecido. Ou a seção 4 estabelece a topografia, ou as técnicas passam a dizer "consolidated self-built settlement with irregular terrain". As duas não podem coexistir sem explicação.

### 22. Cinco argumentos que o artigo faz duas vezes: regra de lugar único

Cada afirmação é argumentada onde nasce e depois apenas citada. Conferi as cinco:

| o quê | onde está hoje | fica onde | vira o quê no outro lugar |
|---|---|---|---|
| piloto que falhou (0,077 contra 0,676, 40 contra 473) | abertura da 9 (07b:7-28) **e** 10.1 (08b:13-18) | abertura da 9 | 10.1 mantém só ameaça, teste e condição: "The pilot reported at the opening of Section 9 reached mAP50 of 0.077 on its own validation split, and scene count is one of the two causes identified there." |
| retirada do fator 2,49 | 8.1 (06b:61-64) **e** 10.2 (08b:50-54) | 10.2, onde a checagem vive | 8.1 vira oração: "(an earlier 2.49-fold figure was an artefact of 1080p rendering and is withdrawn; see Section 10.2)" |
| o oblíquo informa sobre o benchmark, não sobre a aquisição | 8.2, 9.3 (07b:96-98) **e** 11.2 (09b:33-36) | 11.2, argumento completo | 8.2 e 9.3 reduzem a uma frase com ponteiro |
| artefato do ativo único (17,6 por 17,5; 47,6 por 41,7; 6,4 vezes; lista de distratores) | 9.5 **e** 11.5, por inteiro nas duas | 9.5 fica com o resultado e a tabela; 11.5 fica com o argumento | 11.5 cita a tabela em vez de reintroduzir os números |
| separação das duas tarefas, com a enumeração do que é compartilhado | preâmbulo da 7 **e** 11.4 | preâmbulo da 7 (distinção operacional) | 11.4 fica só com o que é dela: a infraestrutura de avaliação da tarefa morfológica não existe |

Somando com o item 2, a ressalva "o benchmark não é favela", que hoje chega ao leitor **três** vezes (10.8, 11.2 e primeiro parágrafo das Limitations), passa a chegar uma.

### 23. `07-conclusion.md`, primeiro parágrafo de Limitations e Delimitations: encolher e realinhar

O primeiro parágrafo repete o argumento de 11.2 logo depois de a 11.2 tê-lo enunciado, e carrega "rather than a system whose performance has been measured on the specific problem this article defines", que só se salva se o leitor ler "the specific problem" como a tarefa de morfologia, que não é mais o que o título promete.

> Section 11 states the limitations that are properties of the measurement itself, and one of them bears repeating because the rest of this section depends on it: the transfer figures reported above are obtained on a public aerial benchmark that is not a favela, and no output of this work has been validated against imagery of the case study territory (Section 11.2). The limitations that follow are of a different kind. They concern the vantage point from which the study was conducted and the single territory it addresses.

Em Delimitations (linha 19), "delimited to the technical and conceptual question of whether machine vision can represent vertical informal structure" passa a incluir a questão que o artigo de fato responde: "...delimited to the technical question of what acquisition conditions the armed and unarmed distinction requires and what synthetic training recovers of it, and to the conceptual question of whether machine vision can represent vertical informal structure; it does not extend to how such a model would be operationally deployed..."

### 24. Duas colisões de vocabulário que fazem o leitor tropeçar em frase certa

**"arm" tem dois sentidos no artigo.** Histórico (ramo anterior do projeto): 03b:40, 03b:50, 03b:167, 06b:26, 07b:20, 08b:16, 09b:13, 09b:107-110. Experimental (os modelos do protocolo de 7.7): 06b:101, 06b:103, 07b:77-93, 08b:77-85, 09b:33. O dano concreto está em **11.6, a seção de reprodutibilidade**: "The procedurally generated arms are redistributable... but the photogrammetric arms of this project are derived from operational imagery that cannot be released". Lida no sentido experimental a frase é falsa, porque S-nadir e S-oblique são os dois procedurais, e o leitor sai sem saber se o dado dos resultados pode ou não ser liberado.

Reservar `arm` (ou melhor, `model`) para R, S-nadir, S-oblique e S-nadir-75, e usar `branch` para o sentido histórico. Correção de 09b:107-110:
> What a reader cannot check from this article is the corpus itself. The corpora behind the models reported here are redistributable by construction, since all geometry is authored and all materials are public domain. Two earlier branches of this project, built on photogrammetric reconstruction of operational imagery, cannot be released; where a measurement in Section 8 uses one of them, the table says so.

**"regime" tem dois sentidos.** Aparece cerca de 22 vezes significando condição de iluminação, inclusive dentro do próprio 09b (11.3: "eight images per regime", "the four intermediate regimes"), e quarenta linhas adiante muda para altitude sem aviso: 09b:90 "The distinction between the two regimes is the contribution" e 07b:143 "what the two regimes mean together". Reservar `regime` para iluminação e escrever `altitudes` nos dois lugares (o item 4 já aplica isso em 07b:143).

**O corpus de registro não tem nome.** Ele é chamado de "its 4K successor" (06b:28), "the corpus of record" (03b:184, dentro de uma célula de tabela, nunca definido antes nem depois), "the corrected corpus" (08b:44) e "the corpus at that altitude" (09b:83). Os dois únicos corpora com nome são declarados explicitamente como **não** sendo ele. Batizar uma vez, no início de 7.2, com o identificador real de disco, e usar só ele nos quatro lugares. **Não** usar "473 scenes" como o tamanho dele: 08b:16 atribui os 473 ao ramo anterior, e 07b:22 ("it contained 40 training scenes against 473") fica ambíguo entre os dois. O tamanho do corpus corrigido não está declarado em lugar nenhum e pode entrar depois.

---

# FAIXA 3: BARATO E VISÍVEL

### 25. Todos os treze arquivos: uma passada de ortografia e de voz

A costura entre autores é visível linha a linha. Medi: os arquivos técnicos somam 19 (03b), 12 (07b), 9 (06b), 8 (08b) e 6 (09b) ocorrências britânicas e quase nenhuma americana; os do orientador e do delegado somam 8 (02), 8 (04), 4 (06) americanas e zero britânicas. Depois da reescrita de 22/09 a fronteira passou para **dentro** de dois arquivos: `01-introduction` tem 4 britânicas (todas no abstract: `artefact`, `colour`, `per cent`) contra 12 americanas na introdução logo abaixo; `07-conclusion` tem 2 britânicas (`maximises`, no Closing) contra 9 americanas (Limitations e Implications). Voz: `we/our` aparece 0 vezes nas seções 2 a 6 e 15 vezes nas 7 a 11 (mais um "Our ultimate objective" isolado na linha 47 da introdução).

A direção é decisão do autor. O defeito é a mistura, não a escolha. Começar pelo abstract e pela conclusão, que são onde as duas se encostam.

### 26. `01-introduction.md` linhas 10 e 11: glosar nadir e ground sampling distance no primeiro uso

Custa poucas palavras e o abstract é onde o leitor decide se continua. `nadir` só ganha explicação em 8.1 ("A person viewed from directly above does not present their height"), vinte páginas adiante; `ground sampling distance` nunca é definido, só exemplificado em cm por pixel em 03b. Sugestão: "Ground sampling distance, the ground area a single pixel covers, not scene realism, fixes the target" e "nadir (the camera pointing straight down) at 150 m". Fazer o mesmo com `oblique` no primeiro uso do corpo. (A observação de uma das lentes sobre `stride` no abstract não procede: `stride` não aparece lá, e onde aparece já vem explicado.)

### 27. `01-introduction.md` linha 43 e `07-conclusion.md` linha 31: fixar os quatro rótulos da taxonomia e rebaixar a sua promoção

Introdução: "from a flat urban environment, to mountainous terrain, to a formal three-dimensional urban environment, and finally to a vertically complex informal urban environment". Conclusão: "(flat terrain, mountainous terrain, formal three-dimensional urban space, and vertically complex informal urban space)". Três dos quatro rótulos mudam, e a primeira mudança é semântica, não cosmética. Fixar os quatro na introdução, de preferência numerados para serem citáveis, e repeti-los idênticos.

Na conclusão, tirar "proposed in this article": a taxonomia aparece exatamente duas vezes no manuscrito, na introdução como observação sobre o que a literatura traçou, e na conclusão já promovida a contribuição. Entre as duas ela não organiza a revisão, não estrutura nenhuma seção e não interpreta nenhuma medida.

### 28. `04-situating-the-study.md` linhas 5 e 13: dois números para 2024 na mesma seção

"703 deaths the year before" (Fórum Brasileiro, linha 5) e "2024 (699 deaths)" (JOTA, linha 13). Fontes diferentes, séries diferentes, e o texto não diz. Unificar pelo Anuário, ou declarar a divergência numa oração e amarrá-la ao argumento que a própria seção 4 já faz sobre a precariedade do dado oficial, que converte o tropeço no argumento do artigo.

### 29. `01-artigo/ferramentas/monta_artigo.py` linhas 84 e 85: o quadro de autoria nega, em caixa amarela, a dependência que o artigo declara

A entrada `04-situating-the-study.md` diz "As secoes tecnicas, 6 a 11, nao dependem do conteudo desta secao e nao devem ser lidas como derivadas dela". Mas a 7.1 depende dela de forma explícita: a síntese existe porque o consentimento não pode ser obtido "under the conditions documented in Section 3", e a seção 5 diz que "the field contextualization supplies the empirical and situational grounding the model needs to be plausible".

> As seções técnicas dependem desta seção em um ponto e apenas nele: o veto ético à coleta de imagem real, que é a premissa de 7.1. Os resultados numéricos não derivam dela.

---

# ITENS QUE DEPENDEM DE DECISÃO DOS COAUTORES, NÃO APLICAR SOZINHO

1. **Itens 13 e 14** (pergunta de pesquisa, objetivo, corte do bloco de trajetória). A introdução é v2 do orientador, verbatim. Cortar cerca de 700 palavras dele e reescrever a pergunta de pesquisa é matéria de coautoria, não de edição. O que se pode levar ao orientador é o dado: `navigation`, `GNSS`, `trajectory` e `situational awareness` têm zero ocorrências nas seções 7 a 11, e `terrain-aware` tem uma em todo o manuscrito, dentro da própria pergunta.

2. **Item 19 e a palavra "central"**. Acrescentar bloco à revisão do orientador, e decidir se entra literatura de uso dual ou se "a central, rather than peripheral, concern" sai da introdução.

3. **Itens 8 e 23** (Limitations, Delimitations, Implications). Texto do orientador, e o parágrafo de fecho do Closing já foi escrito pelo mestrando e aguarda aval, segundo o próprio quadro de autoria.

4. **Item 21** (fechos das seções 3 e 4, parâmetros de morfologia, topografia). São as seções do delegado, em esboço declarado. Os números de morfologia dependem do ortomosaico da PCERJ e precisam sair como faixa, sem coordenada, pela regra de dado sensível.

5. **Título.** Duas correções separadas, e ambas precisam dos três. (a) `Recognition` não aparece mais nenhuma vez nos treze arquivos fora do nome do ICPR nas referências; o corpo usa `detection` em onze dos treze, e as palavras-chave do próprio abstract, quinze linhas abaixo do título, dizem "aerial object detection". (b) `over Vertical Favelas` usa a mesma preposição que o corpo emprega para negar, três vezes, qualquer medição no local ("it does not establish performance over Jacarezinho"), e o abstract reescrito já fez a escolha contrária, "a dense self-built settlement". Sugestão: `Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Self-Built Settlements`.

6. **"Global South" no título.** Aparece **uma** vez no corpo inteiro, de passagem, em 02:9, dentro de uma oração sobre Watson e Elliott. Ou entra um parágrafo curto na introdução nomeando o que a expressão significa aqui (o material já existe disperso: não há benchmark público para a tarefa proposta nesta morfologia, 11.4; o benchmark disponível é de cena urbana que não é favela, 11.2; e não há imagem consentida do território, 7.1, e as três coisas não apareceriam num estudo do mesmo problema numa cidade mapeada, consentida e com benchmark), ou a expressão sai do título.

7. **Item 4, parte final, e a condição de retirada dos 75 m.** Escrever a condição exige decidir se o teste de hold-out por modelo de arma vai ser rodado. Se vai, ela vira uma 10.9 no padrão ameaça/teste/refutação e as duas remissões passam a apontar para lá. Se não vai (ou se fica para depois), a condição tem de ser enunciada em 11.5 sem teste associado, ou os ponteiros simplesmente saem. **O que não pode ficar é o estado atual**, em que duas frases mandam o leitor à 11.3 atrás de algo que não está lá.

8. **`03-methodology.md` linhas 3 e 13, o material autoetnográfico.** A seção 5 declara que as seções 3 e 4 são "grounded partly in autoethnographic material" e promete "marking tactically framed observations as such in the data record". As seções 3 e 4 são integralmente crônica de fonte secundária (ISP-RJ, Fórum Brasileiro, HRW, CNN, Agência Pública, RioOnWatch), sem uma observação marcada em lugar nenhum. Se o material do delegado entra depois, a declaração precisa de marcador visível de que o registro ainda não está no texto. Se não entra, corta-se as duas orações e reescreve-se o segundo parágrafo de Limitations para falar de acesso institucional e enquadramento de fontes, que é o que o artigo de fato faz.

---

# O QUE FICOU DE FORA, E POR QUÊ

**Corrigi um achado que três lentes erraram:** 06b:102 deve apontar para **10.4**, não para 11.2 nem para 11.4. Ver item 1.

**Descartei** a parte do achado sobre glosar `stride` no abstract (a palavra não está no abstract e já vem explicada onde surge), e a leitura de que "reduced to a single class" em 03b:199 significa que o artigo inteiro é de uma classe (a frase é sobre o conjunto de teste VisDrone).

**Deixei na faixa de "depois"**, por caírem no que o autor mandou ignorar: a reconciliação de 17,6 por 17,5 com os 20,6 px de 8.1 e a linha do corpus de registro na tabela de 8.1 (item de medição, embora o conserto barato seja entrar com `[X]` e a nota de procedência, que é o que o artigo já faz em outros lugares); a criação da 10.9; e qualquer item de referência bibliográfica, DOI, marcador `[X]` ou extensão.