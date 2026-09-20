# AIM 2027 — Estratégia de submissão (revisão 2)

Dossiê online: https://claude.ai/code/artifact/311e9ba7-05d9-49ac-af53-7cdd1dcb5184
Pesquisa 2026-08-21. Revisão 2: auditoria contra a literatura publicada.

## Dados da conferência
- 7ª AIM (AI in Management), USC Marshall — 19–20/03/2027, Los Angeles (Marina del Rey).
- Submissão: 19/11/2026 · Decisão: 19/12/2026 · Apresentação: 12 min + 3 de Q&A.
- Co-chairs: Gerard J. Tellis, Bowen Lou, Dan O'Leary, Nan Jia (USC Marshall); Hyo Kang (SNU); Atul Parvatiyar (Texas Tech Rawls).
- Contato: AIM@marshall.usc.edu · Submissão: https://forms.gle/W135GbRDdJMSbzZz8
- Escala: em 2023 foram 77 participantes e 35 apresentadores, 2 trilhas paralelas.
- Prêmios: 4 × até US$5.000 (Rao e Hanssens = PhD/pós-doc; Shugan e Tellis = junior faculty).
  **Mestrando não é elegível.** O retorno é aceite/apresentação/rede, não prêmio.

## Perfil real (indexação de 2023–2026)
Marketing science + IS + economia aplicada. Inferência causal, experimento de campo,
econometria de painel, ML aplicado. **Zero trabalhos de tradição interpretativa/crítica/
análise do discurso** em 4 anos de premiados, finalistas e nomeados.

### Sete arquétipos que vencem
A. GenAI e trabalho (efeito causal sobre produtividade/emprego/tarefas)
B. Humano+IA em criação (aumento vs. substituição, efeitos não-monotônicos)
C. LLM como instrumento (medidor, classificador, respondente sintético)
D. Auditoria de modelo (viés sistemático)
E. Conselho algorítmico (aceitação, explicabilidade)
F. Canal mediado por LLM (visibilidade de marca, GEO) — mais novo e mais aberto
G. Trabalho e sentido — única porta organizacional (Karunakaran/Stanford, Tellis 2025)

## Diagnóstico
"Entre o controle e o autocontrole" (Foucault + análise do discurso) é **não-submissível
como está**. Três pontes: (1) trocar método mantendo pergunta; (2) manter campo e medir
saída; (3) escrever algo independente do mestrado. Com 90 dias, só a (3) fecha.

## Temas, auditados (rev. 2)

- **T2 — O erro do respondente sintético tem forma. [SUBMETER]** Estimar o decaimento de
  fidelidade do consumidor simulado como *função contínua da distância socioeconômica ao
  centro de massa do corpus*. Virada de desenho: **variação identificadora INTRA-país** —
  o Brasil tem dispersão socioeconômica extrema dentro de uma só língua e nação, o que
  mantém língua e país fixos. Desfecho migra de opinião para **consumo/WTP** (ancorado em
  Brand, Israeli & Ngwe, HBS WP 23-062 rev. 2026), com benchmark POF/PNAD.
  Métricas: razão de variância, KS, Wasserstein, cobertura de intervalo — não só erro de média.
  Testar correções publicadas (verbalized sampling, semantic similarity rating) como baseline.
- **T3 — Melhor cada peça, mais parecido o portfólio. [MELHOR TEMA, 12 MESES]**
  Doshi & Hauser (Science Advances 2024): GenAI eleva criatividade individual e reduz
  diversidade coletiva. Ninguém testou **dentro de uma firma que atende muitos clientes**.
  Se real, o portfólio da agência converge entre marcas concorrentes — destrói o que o
  cliente compra. Medir por distância de embedding entre entregas de clientes distintos,
  antes/depois, com efeito fixo de estúdio e cliente. Segunda hipótese (fronteira serrilhada,
  Dell'Acqua et al., Organization Science 37(2) 2026, 403–423): retrabalho SOBE nas tarefas
  logo fora da fronteira.
- **T1 — A curva de Lorenz da citação. [FORA DE 2027, MIRAR 2028]**
  Perdeu o desenho causal: Agarwal & Sen (2026, ISB/CMU) já randomizaram ocultação de AI
  Overviews via extensão Chrome → +39,8% cliques orgânicos, −34,5% zero-click. E o eixo
  "como otimizar" está lotado desde Aggarwal et al. (KDD 2024). Resta a **forma da
  distribuição** (concentração da citação, Lorenz de domínios, cauda longa) + efeito de
  língua. Precisa de série temporal. **Ligar o coletor esta semana**, prompts congelados,
  versão de modelo registrada.
- **T4 — Autonomia prescrita.** Ficou mais defensável: o **paradoxo automação–augmentação**
  (2026) formaliza dois caminhos opostos — augmentação → autoeficácia; automação →
  insegurança. Permite manter Foucault na dissertação e ter modelo mediado testável na
  conferência. Exige braço de vinheta experimental.
- **T5 — De quem é o erro do agente.** Sólido, genérico, reserva.

## Plano de 90 dias
1. Semana 1 (até 28/08): e-mail para AIM@marshall.usc.edu pedindo o Award CFP e o formato
   exigido; abrir o Google Form logado; alinhar coautoria com o orientador.
2. Semanas 2–3 (set): construir o instrumento do T2 e **pré-registrar no OSF antes da coleta**
   (hipótese, estratos, métricas, regra de parada); ligar o coletor do T1 em paralelo.
3. Semanas 5–8 (out): coleta e análise; robustez (temperatura, ordem, versão, tradução).
4. Semanas 9–11 (out–nov): escrever em formato working paper de marketing science.
5. Até 19/11: submeter com uma semana de folga; preparar a versão de 12 minutos.

## Pendências de verificação
- [ ] Formato exigido (paper completo, extended abstract, limite de páginas) — form dá 401.
- [ ] Award CFP separado, para confirmar elegibilidade.
- [ ] Custo total (inscrição via Eventbrite + LA em março) e auxílio da FGV a evento internacional.

## Dez avaliações da revisão 2 (resumo)
1. Desenho causal do T1 já executado por Agarwal & Sen (2026) — T1 perde a camada de tráfego.
2. Eixo "como otimizar para LLM" lotado desde Aggarwal et al. (KDD 2024) — T1 vira estrutura de mercado.
3. "LLM é enviesado" não é mais contribuição (Bisbee 2024; Santurkar 2023; Atari) — T2 estava subespecificado.
4. **Variação identificadora do T2 tem que ser intra-país** — refinamento mais importante da rodada.
5. Desfecho do T2 migra de opinião política para consumo/WTP — terreno menos disputado e é onde a AIM olha.
6. Mecanismo é **colapso de variância**, não viés de média — muda as métricas exigidas.
7. T3 ganhou segundo desfecho (homogeneização de portfólio) e virou o tema mais original.
8. Fronteira serrilhada vira hipótese do T3 com predição de sinal contraintuitiva.
9. T4 ganhou enquadramento vivo — a Ponte 1 é mais barata do que estimei.
10. Faltava **pré-registro** e validação humana do classificador LLM — rigor mínimo da sala.

## Referências verificadas (venue e ano conferidos)
- Argyle et al. (2023), *Political Analysis* 31(3) — fidelidade algorítmica, silicon samples.
- Bisbee et al. (2024), *Political Analysis* — 48% dos coeficientes divergem; variância comprimida.
- Santurkar et al. (2023), ICML — OpinionQA, desalinhamento por grupo demográfico.
- Brand, Israeli & Ngwe, HBS WP 23-062 (rev. 2026) — WTP sintética às vezes com sinal trocado.
- Atari, Xue, Park, Blasi & Henrich, "Which Humans?" (Harvard) — alinhamento WEIRD.
- Horton, Filippas & Manning — *homo silicus* (working paper).
- Aggarwal et al. (2024), KDD, pp. 5–16, DOI 10.1145/3637528.3671900 — funda o GEO.
- Agarwal & Sen (2026), ISB/CMU — RCT AI Overviews. **CONFIRMAR referência formal antes de citar.**
- Doshi & Hauser (2024), *Science Advances*, DOI 10.1126/sciadv.adn5290 — dados abertos no Dryad.
- Dell'Acqua et al. (2026), *Organization Science* 37(2), 403–423 — fronteira serrilhada, pré-registrado, N=758.
- Kellogg, Valentine & Christin (2020), *AMA* 14(1), 366–410 — já na bibliografia dele.
- Kinowska & Sienkiewicz (2023), *ITP* 36(8), 21–42 — SEM, 21.869 orgs.
- Högemann et al. (2025), *Frontiers in AI* 8, DOI 10.3389/frai.2025.1728881 — já na pasta dele.
