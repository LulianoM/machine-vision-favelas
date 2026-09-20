# M24 — Varredura da literatura de GEO: catálogo e mapa do espaço vazio

Executada em 2026-08-21. Nove trabalhos catalogados; seis baixados e lidos.

---

## Resumo do que esta missão muda

1. **O eixo de otimização não está só lotado — está em contradição interna não resolvida.** Aggarwal et al. (KDD 2024) fundaram o campo mostrando que otimização funciona; **C-SEO Bench (NeurIPS 2025) mostra que a maioria dos métodos não funciona e vários pioram o ranqueamento**. Nenhum dos dois lados reconciliou. E os trabalhos de 2026 seguem propondo métodos novos como se a contradição não existisse.

2. **C-SEO Bench transforma o T1 de descritivo em relevante para política pública.** Se a otimização comprovadamente não funciona **e** a visibilidade é concentrada, então **a marca pequena não tem remédio disponível**. Concentração deixa de ser fato de mercado e vira falha estrutural.

3. **O espaço vazio confirmou-se e ficou mais preciso.** Nove trabalhos, nenhum mede a **forma da distribuição**, e **nenhum sai do inglês**.

---

## 1. O catálogo

### Cluster A — Fundação e métodos de otimização

| Trabalho | Venue e data | O que faz |
|---|---|---|
| **Aggarwal, Murahari, Rajpurohit, Kalyan, Narasimhan e Deshpande** — *GEO: Generative Engine Optimization* | **KDD 2024**, p. 5–16, DOI 10.1145/3637528.3671900 | Cunha o termo. Estatísticas verificáveis, citações e fontes confiáveis dão **30–40%** de ganho em visibilidade ajustada por posição |
| **Zhou, Chen, Chen, Bao, Chen e Liao** — *IF-GEO: Conflict-Aware Instruction Fusion for Multi-Query GEO* | arXiv:2601.13938v1, 20/01/2026 · USTC | Otimização para **múltiplas consultas simultâneas**, tratando conflito entre instruções |
| **Wu, Mao, Lin, Yang, Lu, Guo, Zhang, Wu, Huang e Li** — *From Experience to Skill: Multi-Agent GEO via Reusable Strategy Learning* | arXiv:2604.19516v1, 21/04/2026 · Hangzhou Dianzi e outras | GEO multiagente com aprendizado de estratégia reutilizável. Observa que a página virou **camada probatória, não ponto final de interação** |
| **Liu e Xu** — *Think Before Writing: Feature-Level Multi-Objective Optimization for Generative Citation Visibility* | arXiv:2604.19113v1, 21/04/2026 · NUIST | Otimização multiobjetivo em nível de atributo para visibilidade de citação |

### Cluster B — Ceticismo e benchmark ⭐

| Trabalho | Venue e data | O que acha |
|---|---|---|
| **Puerto, Gubri, Green, Oh e Yun** — *C-SEO Bench: Does Conversational SEO Work?* | **NeurIPS 2025, Datasets and Benchmarks Track** · arXiv:2506.11097 · código em `github.com/parameterlab/c-seo-bench` | **Primeiro benchmark** de métodos de SEO conversacional. **9 métodos, 6 domínios**, duas tarefas — resposta a perguntas e recomendação de produto, três domínios cada |

Achados, e são duros:

- *"most current C-SEO methods are not only largely ineffective but also frequently have a negative impact on document ranking, opposite to what is expected."*
- Uma linha de base tradicional de recuperação e ranqueamento — **mover a fonte para a posição 1 do contexto** — é cerca de **7,6× mais eficaz** no domínio de varejo que o melhor método de GEO testado.
- **Adoção crescente leva a retornos decrescentes.**

### Cluster C — Testbeds e datasets

| Trabalho | Venue e data | O que traz |
|---|---|---|
| **Bagga, Farias, Korkotashvili, Peng e Wu** — *E-GEO: A Testbed for Generative Engine Optimization in E-Commerce* | arXiv:2511.20867v2, 14/07/2026 · MIT e Columbia | **Primeiro dataset construído especificamente para GEO em e-commerce.** Declaram que as práticas atuais de GEO são *"largely ad hoc"* e os impactos *"poorly understood"*. Site, código e dados públicos |

### Cluster D — Medição de visibilidade em escala

| Trabalho | Venue e data | O que acha |
|---|---|---|
| **Kumar** — *GEO at Scale: Measuring Brand Visibility Across AI Search Engines* | arXiv:2606.20065v1, 18/06/2026 · Ranqo (comercial) | Escada de três degraus: **73% / 44% / 11%** por estatura de marca. Ver M21 |

### Cluster E — Efeito de canal e economia

| Trabalho | Venue e data | O que acha |
|---|---|---|
| **Agarwal e Sen** — *The Impact of Google AI Overviews on Publisher Traffic and User Experience* | SSRN, DOI 10.2139/ssrn.6513059, abr/2026 rev. jun/2026 · ISB e CMU | RCT com extensão de Chrome: **−39,8%** em cliques orgânicos, **+34,5%** sem clique, citações geram só **~8%** dos cliques. Ver M23 |

### Cluster F — Adversarial e integridade

| Trabalho | Venue e data | O que faz |
|---|---|---|
| **Luo e Chen** — *One Polluted Page Is Enough: Evaluating Web Content Pollution in Generative Recommenders* | arXiv:2606.13610v1, 11/06/2026 · Chinese University of Hong Kong | Até que ponto LLMs com busca viram **promotores involuntários** de conteúdo poluído — avaliações falsas, páginas promocionais feitas para enganar recomendação |

---

## 2. A contradição não resolvida

> **Aggarwal et al. (2024): otimização funciona, 30–40% de ganho.**
> **Puerto et al. (2025): a maioria dos métodos não funciona, e vários pioram.**

E os quatro trabalhos de 2026 do Cluster A seguem propondo métodos novos sem enfrentar o benchmark.

**A reconciliação provável é metodológica, e ninguém a escreveu:** os dois lados **medem coisas diferentes**. Aggarwal mede uma métrica de visibilidade ajustada por posição, dentro da resposta gerada. C-SEO Bench mede **ranqueamento de documento** — se a fonte sobe ou desce na recuperação. Uma tática pode inflar a proeminência do trecho citado e ao mesmo tempo prejudicar a chance de ser recuperado.

**Não é o paper do T1**, mas é um parágrafo obrigatório na revisão de literatura — e é o tipo de observação que um discussant valoriza.

---

## 3. O que C-SEO Bench faz pelo T1

Este é o achado mais consequente da missão.

Se a otimização funcionasse, a concentração medida pelo T1 seria um estado transitório: marcas pequenas investiriam em GEO e a distribuição se abriria. A conclusão seria *"invista em GEO"*, que é conselho de consultoria, não achado de pesquisa.

**Com C-SEO Bench, isso muda.** Se os métodos de GEO são majoritariamente ineficazes, às vezes prejudiciais, e com retornos decrescentes na adoção — então a marca de cauda **não tem instrumento** para reverter a própria invisibilidade.

| Sem C-SEO Bench | Com C-SEO Bench |
|---|---|
| "A IA concentra visibilidade" | "A IA concentra visibilidade **e não há tática conhecida que reverta isso**" |
| Implicação: invista em otimização | Implicação: **é falha estrutural de canal, não deficiência de esforço** |
| Público: gerentes de marketing | Público: **gerentes, reguladores e a agenda de economia da IA da AIM** |

E note que o resultado de retornos decrescentes na adoção é, ele próprio, um resultado de equilíbrio: **se todos otimizam, ninguém ganha.** Isso conversa diretamente com o dilema social que Doshi e Hauser descrevem no T3 — mesma estrutura, outro mercado. Vale a nota cruzada no paper.

---

## 4. O mapa do espaço vazio

| Dimensão | Coberto por | Vazio? |
|---|---|---|
| Como otimizar | Cluster A, 4 trabalhos | ❌ Lotado |
| Otimização funciona? | C-SEO Bench | ❌ Respondido, e negativamente |
| Dataset e testbed | E-GEO | ❌ Coberto, e por time forte |
| Nível de visibilidade por marca | Kumar | ❌ Coberto |
| Quanto tráfego se perde | Agarwal e Sen | ❌ Coberto, com RCT |
| Manipulação adversarial | Luo e Chen | ❌ Coberto |
| **Forma da distribuição de visibilidade** | — | ✅ **VAZIO** |
| **Contrafactual orgânico pareado por prompt** | — | ✅ **VAZIO** |
| **Qualquer língua que não o inglês** | — | ✅ **VAZIO** |
| Bem-estar do consumidor | — | ✅ Vazio, mas fora do alcance do T1 |
| Equilíbrio quando todos otimizam | Tangenciado por C-SEO Bench | 🟡 Parcial |

**Três vazios, e o T1 ocupa os três primeiros ao mesmo tempo.** Não por sorte: são justamente os que exigem coleta pareada em dois canais e em duas línguas, que é trabalho de engenharia sustentado — a barreira que separa o T1 de quem publica método.

### E uma observação sobre a geografia da literatura

Dos nove trabalhos: quatro da China, dois dos Estados Unidos, um da Coreia com Alemanha, um da Índia com Estados Unidos, um comercial. **Nenhum da América Latina, nenhum sobre mercado não-anglófono.**

Isso não é só oportunidade — é **argumento de contribuição**, do mesmo tipo que o T2 usa com a POF. O ativo é o mercado, não o método.

---

## Pendências geradas

- [ ] Ler C-SEO Bench integral e verificar se o benchmark cobre alguma língua além do inglês — se cobrir, o argumento de vazio linguístico enfraquece.
- [ ] Verificar se o dataset E-GEO é reutilizável para o T1 ou se é específico demais para e-commerce.
- [ ] Investigar se alguém já reconciliou Aggarwal com C-SEO Bench — se não, é parágrafo de revisão; se sim, citar.
- [ ] Checar se Luo e Chen (poluição de conteúdo) tocam concentração — poluição pode ser mecanismo de concentração, não só de engano.
- [ ] **M25 herda:** o argumento de contribuição do T1 passa a ter três pernas — forma da distribuição, contrafactual pareado e língua —, e não só a última.
- [ ] Confirmar a página exata e o DOI de C-SEO Bench nos anais do NeurIPS 2025.
