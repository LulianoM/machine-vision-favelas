# Resumo do artigo (v2 do orientador, 2026-09-10, 7.020 palavras)

Arquivo: `Machine Vision from the Global South - v2 Irigaray 2026-09-10.docx`. Autor do documento: Hélio Arthur Reis Irigaray. É um rascunho quase completo: introdução, revisão, metodologia, contexto, caso, resultados, limitações, delimitações, pesquisas futuras e referências. Só a seção "Conclusion" está vazia.

## Introdução
- Parte da literatura de planejamento de trajetória de UAV em ambientes 3D (Rasoulie e Pashazadeh 2026; Xu 2025; Agrawal, Ratnoo e Ghose 2017; Jiang et al. 2026).
- Crítica: a literatura de policiamento aéreo (Wang e Qian 2026; Chen et al. 2025; Yan, Hsieh e Lai 2025) reduz tudo a formulações horizontais.
- Favela verticalizada não é caso especial de montanha; lista as fontes de complexidade que coocorrem no Rio.
- Taxonomia em 4 estágios: plano, montanhoso, urbano formal 3D, informal verticalmente complexo.
- Duas literaturas que não se cruzam: policiamento/defesa e mapeamento de assentamentos informais (Gevaert et al. 2016; Sithole e Mhangara 2025; da Silva et al. 2024).
- Pergunta: como visão computacional terrain-aware melhora percepção, navegação e consciência situacional de UAV em ambientes informais verticalmente complexos?
- Objetivo: propor e validar conceitualmente um modelo que mapeie a morfologia vertical do Jacarezinho com dados sintéticos e observação de campo.
- Relevância tripla: urbanismo e dados públicos; instituições policiais; comunidades (risco de uso dual tratado como central).

## Revisão de literatura
- CNNs para detecção de assentamentos informais (Gram-Hansen 2019; Du 2024; Hu 2025; Sithole e Mhangara 2025).
- Dimensão vertical pouco tratada (Gevaert 2016 em Kigali; Watson e Elliott 2025 em Nairobi, Kathmandu e Quito).
- Dados sintéticos e sim-to-real: Tobin 2017 (domain randomization), Prakash 2019 (structured DR), Barisic 2022 (dataset aéreo sintético, ganho de mAP), Horváth 2023 (mAP acima de 86% zero-shot e 97% one-shot).
- Posicionamento: o que muda técnica, ética e socialmente quando o fim é segurança pública.

## Metodologia
- Revisão + design science + contextualização qualitativa/autoetnográfica, encadeadas.
- Um dos autores é delegado da ativa com familiaridade operacional no Jacarezinho.
- Três vieses assumidos: olhar tático; acesso mediado pela instituição; impossibilidade de corrigir por completo (mitigação por triangulação, marcação das observações táticas, status de modelo conceitual).
- Três restrições: sem imagem identificando moradores; sem coordenadas em nível de endereço; coleta futura só com ética independente e engajamento comunitário fora da polícia.

## Contexto: violência e policiamento no Rio
- Homicídios em queda há duas décadas; letalidade policial alta e crescente em 2025 (798 mortes por intervenção, 20,5% das mortes violentas).
- Operação Exceptis (Jacarezinho, 06/05/2021, 28 mortos) e Operação Contenção (Alemão e Penha, 28/10/2025, 121 a 122 mortos).
- CV usou drones para lançar explosivos na Contenção; Polícia Civil expandiu a COANT.
- ADPF 635 ("ADPF das Favelas"): liminar de Fachin em 2020, julgamento final em 03/04/2025.
- Ambiente construído da favela como obstáculo estrutural ao policiamento.

## Caso Jacarezinho
- Zona Norte, ~40 ha, terceira maior favela do Rio. População: 35.458 (Censo 2022), ~37 mil (município), mais de 60 mil (fontes comunitárias).
- Origem no início do século 20; maior concentração de afro-brasileiros entre as favelas do Rio; controle do CV há décadas.
- Intervenções de 2021 e Cidade Integrada (jan/2023).

## Resultados (modelo conceitual, não implementado)
1. Backbone CNN de classificação estrutural: categorias de altura, adições em laje, transições de material.
2. Pipeline sintético com structured domain randomization: cenas 3D procedurais com alturas irregulares, vãos estreitos, telhados mistos, cabos, caixas d'água; texturas, luz e câmera randomizadas.
3. Fine-tuning limitado e consentido com dados reais.
- Explicita que não produz ferramenta de targeting operacional.

## Conclusão (só limitações, delimitações e futuro)
- Limitações: nada treinado nem validado; viés do olhar policial; dependência de fontes jornalísticas; caso único.
- Delimitações: sem coleta de campo; sem tratar implantação ou governança; revisão restrita a três literaturas.
- Futuro: desenhar o processo ético antes do refino técnico; benchmarking em datasets consentidos (Kigali, Slovo Park) antes de qualquer imagem do Jacarezinho; testar a taxonomia em outras favelas.

## Problemas encontrados no rascunho (para devolver ao orientador)
- "Conclusion" existe só como título.
- Referências faltando na lista: Chen 2025, Rasoulie e Pashazadeh 2026, Xu 2025, Agrawal 2017, Jiang 2026, Wang e Qian 2026, Yan 2025, Gevaert 2016, Du 2024, Barisic 2022, Horváth 2023, Watson e Elliott 2025, da Silva 2024. Entrada "[Slovo Park study]" sem autores.
- Wikipedia citada três vezes como fonte.
- XML vazado no início do último parágrafo de Delimitations e "eferences" sem o R.
- Usa travessão em vários trechos.
- Todos os DOIs precisam ser verificados no Crossref antes da submissão (regra do Felipe: nunca inventar DOI).
