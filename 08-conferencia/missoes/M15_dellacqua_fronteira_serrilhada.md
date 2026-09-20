# M15 — Dell'Acqua et al.: desenho, pré-registro e a operacionalização da fronteira

Executada em 2026-08-21. **Versão publicada lida em texto integral**, obtida do repositório aberto da HBS.

---

## Referência verificada — com uma correção

DELL'ACQUA, Fabrizio; McFOWLAND III, Edward; MOLLICK, Ethan; LIFSHITZ, Hila; KELLOGG, Katherine C.; RAJENDRAN, Saran; KRAYER, Lisa; CANDELON, François; LAKHANI, Karim R. *Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of Artificial Intelligence on Knowledge Worker Productivity and Quality*. **Organization Science**, publicado on-line em *Articles in Advance*, **11 de março de 2026**, p. 1–21. DOI 10.1287/orsc.2025.21838. **Licença CC BY 4.0.**

Revisado em 23/01/2026, aceito em 27/01/2026.

> ⚠️ **Correção a registros anteriores do dossiê.** As missões M03 e M11 registraram "*Organization Science* 37(2), 2026, p. 403–423", com base em fonte secundária. O PDF publicado que li traz **"Articles in Advance, pp. 1–21"** — ou seja, à data daquele arquivo o artigo ainda não tinha sido alocado a fascículo. A paginação 37(2):403–423 pode ser a alocação final, mas **não a verifiquei**. Citar por DOI até confirmar.
>
> Registro também que o sobrenome da coautora aparece como **Lifshitz**, não "Lifshitz-Assaf" como consta em versões anteriores do working paper.

---

## Resumo do que esta missão muda

1. **A fronteira não é medida — é operacionalizada pelo método de avaliação.** Dentro da fronteira: tarefas intensivas em escrita, **sem resposta única correta**, avaliadas por rubrica subjetiva. Fora: um caso de estratégia com **recomendação objetivamente correta**, medido de forma dicotômica. Simples, replicável, e **muito melhor para o T3 do que qualquer métrica de capacidade de IA**.

2. **E isso é um presente para o T3.** As tarefas fora da fronteira são justamente aquelas em que o erro é **objetivamente verificável** — logo são as únicas em que retrabalho registrado no Argos Core significa erro de fato, e não mudança de gosto do cliente.

3. **Os autores declaram explicitamente o trabalho futuro que o T3 faz:** *"a need to understand the frontier's **shape and position** as well as **how it is perceived by knowledge workers**"*.

4. **⚠️ Correção importante a M04 e ao T4:** o paradoxo automação–augmentação não é de 2026. É **Raisch e Krakowski, *Academy of Management Review*, 46(1), p. 192–210, 2021**. Citação muito mais forte do que a que o dossiê vinha usando.

---

## 1. Desenho

**Experimento de campo pré-registrado**, em colaboração com o **Boston Consulting Group**. Os autores assessoraram desenho, desenvolvimento e execução; a empresa coletou os dados; o time de autores recebeu os dados e conduziu a análise.

**N = 758 trabalhadores do conhecimento.**

Sequência: primeiro estabelece-se uma **linha de base de desempenho em tarefas similares**; depois, atribuição aleatória a três condições.

| Condição | Acesso |
|---|---|
| Controle | Sem IA |
| Tratamento 1 | GPT-4 |
| Tratamento 2 | GPT-4 **mais** uma visão geral de engenharia de prompt |

**As tarefas:**

- **18 tarefas realistas dentro da fronteira**, cobrindo do criativo ao analítico.
- **1 tarefa gerencial complexa selecionada para estar fora da fronteira.**

---

## 2. A operacionalização da fronteira — a resposta que a missão pedia

Reprodução do trecho decisivo:

> *"Our design employs **different evaluation methods by task type**, directly mirroring how consulting work is assessed in practice. For **writing-intensive activities inside the frontier**, performance is evaluated through **subjective rubrics**, matching BCG's standard procedures because **no single correct answer exists**. Conversely, the **strategy case outside the frontier** features an **objectively correct recommendation** that is measured **dichotomously**."*

Formalizando:

| | Dentro da fronteira | Fora da fronteira |
|---|---|---|
| **Natureza** | Intensiva em escrita | Caso de estratégia |
| **Existe resposta certa?** | Não | **Sim, uma** |
| **Avaliação** | Rubrica subjetiva, padrão BCG | **Dicotômica**: acertou ou não |
| **Quantidade** | 18 tarefas | 1 tarefa |

**Não há medição de capacidade do modelo, nem benchmark, nem escala de dificuldade.** A distinção é feita pela **estrutura epistemológica da tarefa**: existe ou não existe uma resposta verificável.

Isso é metodologicamente elegante e tem uma consequência prática que os próprios autores registram como limitação: *"this design highlights a **single** outside-the-frontier task—an inherent limitation"*.

---

## 3. Resultados

**Dentro da fronteira**, consultores com IA, comparados aos sem IA:

- completaram **12,2% mais tarefas**;
- completaram-nas **25,1% mais rápido**;
- entregaram soluções de **qualidade significativamente melhor**.

**Fora da fronteira:**

- consultores com IA foram **19% menos propensos a produzir a solução correta**.

E a leitura que os autores extraem, que é a mais transferível:

> *"even a single complex challenge beyond AI's current capabilities can **disproportionately reduce overall performance** if users rely too heavily on AI's output."*

---

## 4. Limitações e ressalvas que os autores declaram

Três, e todas atingem o T3 diretamente.

**Uma única tarefa fora da fronteira.** Reconhecida como limitação inerente. O T3, com dezenas de tipos de tarefa registradas no Argos Core, pode ter **muitas** — o que é uma vantagem real, não retórica.

**Estrutura de incentivo específica.** O achado vale onde *"quality within allocated time frames is prioritized over speed optimization"*, como em BCG e serviços profissionais similares. Onde ganho de eficiência se traduz diretamente em recompensa, ou onde há troca explícita entre acurácia e velocidade — manufatura, atendimento com métrica de tempo de chamada, trabalho por peça —, os efeitos podem diferir substancialmente.

> **Um estúdio criativo pequeno está no primeiro grupo, não no segundo.** Isso favorece a transferência para o T3 e deve ser dito no paper.

**Autosseleção na adoção.** Quando o uso é discricionário — como no experimento e como num estúdio real —, *"early adopters are disproportionately male and more technologically confident, and the resulting performance gains can widen pre-existing gender- and skill-gaps rather than close them"*, citando Otis et al. (2024) e Humlum e Vestergaard (*PNAS*, 122(1), 2025).

> **Esta é a ameaça de endogeneidade do T3, nomeada por um paper de *Organization Science*.** Cita-se e trata-se explicitamente, em vez de esperar o revisor levantar.

---

## 5. O trabalho futuro que os autores pedem

> *"These results suggest a need to understand the **frontier's shape and position** as well as **how it is perceived by knowledge workers** to better determine AI's influence on work."*

Duas coisas, e o T3 pode entregar a primeira:

- **Forma e posição da fronteira** — exatamente o que um painel de tarefas com adoção escalonada permite mapear, tarefa a tarefa, em vez de com uma tarefa só.
- **Como ela é percebida pelos trabalhadores** — território da dissertação qualitativa, não do T3.

**A segunda metade é a ponte com o mestrado.** Um artigo de *Organization Science*, assinado por Kellogg — que já está na bibliografia crítica de Felipe —, pedindo investigação sobre **percepção** da fronteira pelos trabalhadores. É a justificativa do braço qualitativo, vinda de dentro da literatura quantitativa.

---

## 6. O que transfere para o T3

### A operacionalização, traduzida para entregas de agência

| | Dentro da fronteira | Fora da fronteira |
|---|---|---|
| **Exemplos** | Variações de copy, moodboard, alternativas de layout, naming, roteiro | Conformidade com guia de marca, requisitos de acessibilidade, cálculo de precificação, especificação técnica, exigência legal ou regulatória |
| **Resposta certa?** | Não | **Sim, verificável** |
| **Avaliação** | Aceite do cliente, rubrica | **Dicotômica**: conforme ou não conforme |

### Por que isso resolve um problema que o T3 tinha

O desfecho de retrabalho no Argos Core é ambíguo: um ciclo de revisão pode significar erro real **ou** mudança de opinião do cliente. Não se distingue.

**Mas nas tarefas fora da fronteira, a distinção some.** Se a peça viola o guia de marca, falha em contraste de acessibilidade ou erra a conta, o retrabalho é objetivamente atribuível a erro. **Logo o teste da predição contraintuitiva — retrabalho sobe nas tarefas logo fora da fronteira — deve ser rodado sobre o subconjunto de tarefas com verificabilidade objetiva**, e só sobre ele.

Isso estreita a amostra e fortalece a inferência. E dá ao T3 uma classificação de tarefas com critério publicado, em vez de julgamento próprio.

### O que não transfere

1. **Aleatorização.** Eles randomizam; o T3 tem adoção escalonada e discricionária. A ressalva de autosseleção deles é a ameaça central do T3.
2. **Linha de base individual prévia.** Eles medem desempenho de cada sujeito antes do tratamento. O T3 tem o análogo: histórico do Argos Core antes da adoção, por pessoa. **Usar, e dizer que é o análogo.**
3. **Tarefas padronizadas.** As 18 tarefas são iguais para todos. As entregas de agência não são — o que reforça a necessidade de estratificar por tipo, já registrada na M14.

---

## 7. Referências novas geradas

Todas citadas por Dell'Acqua et al. e relevantes:

| Referência | Por que importa |
|---|---|
| **Raisch e Krakowski (2021)**, *Artificial intelligence and management: The automation–augmentation paradox*, **Academy of Management Review** 46(1):192–210 | ⚠️ **Corrige o dossiê.** É a fonte canônica do paradoxo, não os artigos de 2026 que a M04 citou. Vai para o T4 |
| **Humlum e Vestergaard (2025)**, *The unequal adoption of ChatGPT exacerbates existing inequalities among workers*, **PNAS** 122(1):e2414972121 | Autosseleção na adoção — ameaça central do T3 |
| **Hui, Reshef e Zhou (2024)**, *The short-term effects of generative AI on employment: Evidence from an online labor market*, **Organization Science** 35(6):1977–1989 | Precedente de efeito de emprego em *Organization Science* |
| **Randazzo, Joshi, Kellogg, Lifshitz, Dell'Acqua e Lakhani (2025)**, *GenAI as a power persuader: How professionals get persuasion bombed when they attempt to validate LLMs*, HBS WP 26-021 | Mecanismo de por que profissionais falham em validar saídas de LLM — diretamente ligado ao retrabalho fora da fronteira |
| **Glaeser, Hillis, Kim, Kominers e Luca (2024)**, *Decision authority and the returns to algorithms*, **Strategic Management Journal** 45(4):619–648 | Autoridade decisória e retorno de algoritmos |
| **Gaessler e Piezunka (2023)**, *Training with AI: Evidence from chess computers*, **Strategic Management Journal** 44(11):2724–2750 | Aprendizado com IA |

---

## Pendências geradas

- [ ] Confirmar a paginação final em *Organization Science* (37(2):403–423 ou outra) e corrigir M03 e M11.
- [ ] **Corrigir a citação do paradoxo automação–augmentação** para Raisch e Krakowski (AMR, 2021) nos registros do T4 (M04) e no dossiê.
- [ ] Ler Randazzo et al. (2025), HBS WP 26-021 — o mecanismo de falha de validação é candidato a explicar o retrabalho fora da fronteira.
- [ ] Ler Humlum e Vestergaard (PNAS, 2025) para o tratamento formal da autosseleção na adoção. **Alta prioridade — é a ameaça central do T3.**
- [ ] Baixar o **apêndice on-line** do artigo (disponível no DOI) — contém o detalhamento das 18 tarefas e o Apêndice F com a análise de dados do Bureau of Labor Statistics.
- [ ] **M18 e M19 herdam:** restringir o teste da hipótese de retrabalho ao subconjunto de tarefas com verificabilidade objetiva, e usar o histórico pré-adoção por pessoa como linha de base individual.
- [ ] Localizar o pré-registro do experimento e verificar o que era confirmatório.
