# M25 — Viabilidade do contrafactual: fontes brasileiras

Executada em 2026-08-21.

---

## Resumo do que esta missão muda

1. **O contrafactual deixa de ser um e passa a ser três canais** — e isso torna a pergunta do T1 muito melhor. Além de busca orgânica e resposta de IA, existe um terceiro canal público e brasileiro: **a lembrança espontânea humana**, medida pelo Top of Mind desde 1991.

2. **O paralelo conceitual é exato.** O Top of Mind pergunta *"qual a primeira marca que vem à cabeça quando penso em [categoria]?"*. Um prompt sem marca — "melhor tênis de corrida" — pede exatamente a mesma operação ao modelo. **Lembrança humana contra lembrança de máquina, mesma categoria, mesmo país.**

3. **⚠️ E isso desarma uma armadilha em que o T1 ia cair.** A lembrança humana **já é extremamente concentrada**. Concluir que "a IA concentra" sem comparar com quanto os humanos já concentram seria achado vazio. Com o terceiro canal, a pergunta vira: **a IA reproduz, amplifica ou atenua a concentração que já existe na cabeça das pessoas?** Três respostas possíveis, todas publicáveis.

4. **⚠️ Limite prático sério:** o Top of Mind publica rankings e percentuais das marcas do topo, não a distribuição completa. **Sem cauda, não há Gini nem Lorenz** — só índices de topo. Detalhado na seção 3.

---

## 1. O desenho de três canais

| Canal | O que mede | Fonte | Custo |
|---|---|---|---|
| **Memória humana** | Marcas lembradas espontaneamente por categoria | Top of Mind (Folha e Datafolha) | Publicado, parcial |
| **Busca orgânica** | Marcas que o buscador apresenta | API de SERP licenciada (M22) | **Pago** |
| **Resposta de IA** | Marcas que o modelo apresenta | Coletor próprio (M21) | API |

E a pergunta do T1 ganha uma segunda camada:

```
H1:  N_efet(IA) < N_efet(orgânico)          a IA concentra mais que a busca
H2:  a diferença é maior em pt-BR que em en-US
H3:  N_efet(IA) vs N_efet(memória humana)   ← nova, e a mais interessante
```

**H3 é a que muda o enquadramento.** Se a concentração da IA for parecida com a da memória humana, o achado é *"a IA herda o viés de saliência que já existe"*. Se for pior, é *"a IA amplifica"*. Se for melhor, é *"a IA expõe marcas que as pessoas não lembrariam"* — e nesse caso o T1 vira um paper sobre **descoberta**, não sobre desigualdade.

Nenhuma das três é derrota. **É a definição de uma pergunta empírica de verdade.**

---

## 2. Top of Mind — o que é e o que não é

**Fonte.** Pesquisa do Grupo Folha em parceria com o instituto **Datafolha**, criada em **1991**. Considerada a pesquisa mais abrangente de lembrança de marca no Brasil.

**Método verificado.** Pergunta aberta — *"qual a primeira marca que vem à cabeça quando penso em [categoria]?"* — formulada para obter **lembrança espontânea**. Entrevistas presenciais e por telefone, por amostragem **estratificada por sexo, faixa etária e região socioeconômica**, refletindo o perfil da população brasileira.

**Escala.** O Anuário Datafolha Top of Mind chegou à **19ª edição em 2026**. Categorias cobrem comunicação, saúde, educação, varejo, serviços, aplicativos e sustentabilidade, além de prêmios especiais.

> ⚠️ **Cuidado com números de edição regional.** Encontrei "501 entrevistas presenciais em fevereiro de 2026, público de 16 anos ou mais, com maior concentração de classe C e ensino médio completo, em 25 categorias" — mas esses números são de uma **edição regional (Ceará)**, não da nacional. **Não confundir.** A amostra e o número de categorias da edição nacional precisam ser confirmados na ficha técnica.

### Por que serve

- É **lembrança espontânea**, não reconhecimento assistido — a mesma operação do prompt sem marca.
- É **brasileira, urbana e estratificada**, o que casa com o recorte do T1.
- Tem **série desde 1991**, o que permitiria, em tese, verificar se a concentração humana mudou desde a chegada da IA.
- É **pública em nível de ranking**, sem custo.

### Por que não basta sozinho

| Limitação | Impacto |
|---|---|
| **Publica top-N, não a distribuição completa** | **Sem cauda, não há Gini nem curva de Lorenz.** Só C1, C3, talvez C5 |
| Anual | Não alinha com a cadência semanal do coletor |
| Capitais e áreas urbanas | Recorte mais estreito que o da POF |
| Categorias próprias | Podem não corresponder às categorias de prompt do T1 |
| Metodologia de amostra varia entre edições e regionais | Comparabilidade temporal exige checagem |

**Consequência de desenho:** o canal de memória humana entra com **índices de topo** (C1, C3), não com índices de distribuição completa. Os três canais são comparáveis em C1 e C3; **apenas orgânico e IA são comparáveis em Gini, Lorenz e cauda.**

Isso é aceitável e precisa estar declarado — não é falha, é o que o dado público permite.

---

## 3. O universo fixo de marcas — a decisão da M22

A M22 fixou que os índices só são comparáveis se o universo de marcas for definido a priori. Esta missão resolve a fonte.

**Recomendação: construir o universo por união de três fontes**, por categoria e mercado:

1. **Top of Mind** — marcas citadas na categoria (dá o núcleo saliente).
2. **Levantamento próprio de mercado** — marcas com presença comercial relevante na categoria, com critério declarado (por exemplo, disponibilidade nos três maiores varejistas do país).
3. **As marcas efetivamente mencionadas** por qualquer canal na rodada-piloto — garante que nada apareça "fora do universo".

A união das três, congelada antes da rodada 1, com fonte de entrada registrada por marca. **A terceira fonte é essencial**: sem ela, uma marca que a IA menciona e nenhuma lista prevê ficaria de fora, e o índice ficaria errado no sentido conveniente.

---

## 4. Google Trends — candidato com ressalva

**API oficial anunciada em 24 de julho de 2025**, em versão alfa.

A melhoria relevante: no site, os dados são normalizados de 0 a 100 **por consulta**, o que torna matematicamente inválido comparar o mesmo termo entre consultas diferentes. **A API usa escalonamento consistente entre requisições**, permitindo unir e comparar múltiplas consultas — que é exatamente o que uma série temporal exige.

⚠️ **Mas o acesso permanece limitado a um grupo pequeno de testadores selecionados por processo de inscrição.** Não é disponibilidade garantida.

Alternativas — `pytrends` e serviços de raspagem — têm **o mesmo problema jurídico** da coleta de SERP registrado na M22: violam termos de uso.

**Decisão:** inscrever-se no programa de acesso, mas **não desenhar o T1 dependendo do Google Trends**. Se sair, entra como camada de validação — interesse de busca por marca como controle de demanda. Se não sair, o desenho de três canais permanece intacto.

---

## 5. O que é pago e não vale a pena

| Fonte | Situação |
|---|---|
| Kantar BrandZ, Interbrand | Rankings de **valor de marca**, não de lembrança nem de participação. Publicam top-N. Conceito errado para o T1 |
| Nielsen, Kantar (participação de mercado) | Pago, caro, e participação de vendas ≠ visibilidade |
| Similarweb, Semrush | Pago. Tráfego de domínio, não menção de marca |
| Webshoppers, Neotrust | E-commerce agregado; útil para escolher categorias, não para o universo de marcas |

**Nenhuma é necessária.** O desenho de três canais dispensa dado de participação de mercado — e isso é bom, porque participação de vendas responde a preço e distribuição, não a visibilidade, e usá-la como contrafactual confundiria dois fenômenos.

---

## 6. Onde ficou o custo

Uma única linha, herdada da M22:

> **API de SERP licenciada, com cobertura de Brasil e Estados Unidos.**

É o que viabiliza o canal orgânico. Os outros dois canais — memória humana e resposta de IA — são, respectivamente, gratuito e barato.

---

## Pendências geradas

- [ ] **Obter a ficha técnica da edição nacional do Top of Mind**: amostra, número de categorias, praças, período. Os números que encontrei são de edição regional.
- [ ] Verificar **até que profundidade** o Top of Mind publica percentuais por categoria — é o que determina se dá para calcular algo além de C1 e C3.
- [ ] Verificar se há acesso acadêmico ao microdado do Datafolha; se houver, o canal de memória humana ganha distribuição completa e o desenho fica muito mais forte.
- [ ] Inscrever-se no acesso à API do Google Trends, sem depender dela.
- [ ] Mapear categorias do Top of Mind contra as categorias de prompt do T1 e escolher as que se sobrepõem.
- [ ] Verificar se o Top of Mind tem equivalente americano com metodologia comparável — sem isso, H3 só vale para o Brasil.
- [ ] **M26 herda:** o coletor precisa registrar a fonte de entrada de cada marca no universo fixo.
