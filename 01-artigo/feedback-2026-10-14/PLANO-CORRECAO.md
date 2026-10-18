# Plano de correção do artigo a partir do feedback de 14/10/2026

Escrito em 17/10/2026 [DESKTOP]. Fonte: `FEEDBACK-RECEBIDO.md` (texto e quatro áudios). Regra de ouro desta rodada, dada pelo revisor: **forma, leitura e estrutura primeiro; depois reenviar**. Nenhum experimento de treino novo nesta rodada; só análises por inferência sobre modelos e corpora que já existem, cada uma com comando e origem em `06-resultados/RESULTADOS.md`.

## 1. Decisões tomadas para esta rodada (o autor confirma ou desfaz)

| # | Decisão | Por quê |
|---|---|---|
| D1 | Adotar a "Final structure" de sete seções do `feedback.txt` como esqueleto, com as subseções exatamente como listadas | É a mais específica, foi construída sobre este artigo e corresponde ao esqueleto de seis seções do revisor (Resultados e Discussão podem ser fundidos no fim, e 6.4 e 6.5 podem subir a seção própria "Limitações e considerações éticas" se ele preferir) |
| D2 | Retirar a classificação "design science"; a seção de método descreve um estudo experimental computacional com caracterização do alvo independente de modelo | Recomendação do revisor (justificar com um quadro metodológico ou retirar); o artigo não segue nenhum ciclo de design science. O texto era do orientador: ver decisão A1 na seção 6 |
| D3 | A proposta do modelo de morfologia vertical (antiga seção 6) vira trabalho futuro (6.6), em um parágrafo | Nunca foi construída; a estrutura-alvo a põe em 6.6. Texto do orientador: decisão A2 |
| D4 | Seções 3 e 4 antigas (2 mil palavras de contexto policial) condensadas em 3.1 a 3.3, cerca de 1,2 mil palavras, com as mesmas fontes primárias | A estrutura-alvo diz "condensed"; o peso era crítica aberta desde 30/09 |
| D5 | Sem treino novo. Permitidas análises por inferência: intervalos de confiança por reamostragem, curvas por limiar, análise de similaridade de recortes, tabela de GSD, contagens de instâncias | O revisor pediu forma primeiro; treinos ficam listados na seção 5 com custo de GPU, para decisão |
| D6 | O texto mantém a decisão de 30/09 (só texto, sem corpus nem código); a seção 4.8 diz o que o leitor pode e não pode conferir | A liberação do gerador e dos corpora procedurais é a decisão A3, a mais cobrada por revisores |
| D7 | Meta de extensão: cerca de 16 mil palavras de corpo (hoje 26,5 mil), sem perder nenhum número | Redundância é a queixa central do áudio; periódicos pedem 8 a 12 mil |
| D8 | Estilo: grafia britânica em -ise, "per cent" na prosa e "%" nas tabelas, cada sigla definida uma vez, nenhuma frase-guardiã repetida, conectores variados, sem travessão | Áudio de 10h10 e harmonização pendente desde 30/09 |
| D9 | Numeração explícita nos títulos até o terceiro nível (4.2.1); o montador ganha estilo para h4 e o aviso de versão prévia passa a 17/10 | A estrutura-alvo tem três níveis |

## 2. Pontos do revisor e o que se faz com cada um

Legenda de origem: T = `feedback.txt`, A = áudio. Onde: subseção da estrutura nova. Quem: agente da seção 4.

| ID | Origem | Ponto | Ação nesta rodada | Onde | Quem |
|---|---|---|---|---|---|
| E1 | T, WhatsApp | Métodos explicados nos resultados; conclusões tiradas nos resultados | Reescrever na estrutura nova: protocolo, critérios e definições em 4; números em 5; interpretação em 6 | todas | W1 a W6, integrador |
| E2 | T | Repetição; cada seção deve responder às perguntas | Cada resultado aparece uma vez; remissão em vez de repetição; checagem automática de trechos repetidos | todas | integrador |
| E3 | A 10h10 | Siglas reexplicadas; conectores iguais | Definir sigla uma vez; varrer conectores | todas | integrador |
| M1 | T 1.1 | Objetivo e perguntas alinhados ao que foi medido; dizer que armado e desarmado foi só sintético | RQ1 a RQ3 em 1.3 com a variável medida de cada uma; abstract e conclusão repetem a restrição | 1.3, 5.4, 6.1, 7 | W1, W6 |
| M2 | T 1.2 | Separar validação (seleção) de teste independente | 4.7 define "selection split" e "held-out frames"; 5.4 reporta em linhas separadas; nenhum número de seleção entra sem rótulo | 4.5, 4.7, 5.4 | W4, W5, D1 |
| M3 | T 1.3 | GSD além de altitude; justificar a câmera e seu zoom | Tabela altitude × distância focal → GSD e pegada no solo; a câmera de referência (Zenmuse Z30, zoom óptico 30×) justificada e seu zoom discutido: GSD de 35 m é alcançável de 150 m ao custo de pegada e estabilidade | 4.2.4, 5.1, 6.2 | D1, W4, W6 |
| M4 | T 1.4 | Limites do realismo: resolução do sensor, ruído, borrão de movimento, compressão | Parágrafo factual: formato de gravação dos renders, ausência de modelo de ruído, borrão e compressão | 4.2.4, 6.5 | D1, W6 |
| M5 | T 1.5 | O benchmark real sustenta a avaliação entre geometrias? Dado com perspectiva comparável | Levantamento de bases reais nadir com pessoas anotadas (altitude, GSD, licença, tamanho); avaliação zero-shot fica proposta para a rodada 5 | 6.5, 6.6 | D4, W6 |
| S1 | T 2.1 | Mais repetições, sementes de cena, intervalos de confiança | Intervalos de 95% por reamostragem de imagens para todo mAP50 no VisDrone e para as diferenças pareadas; sementes existentes relatadas como estão; novas repetições na rodada 5 | 4.7, 5.2, 5.3, 5.6 | D2, W5 |
| S2 | T 2.2 | Confirmatório contra exploratório | 4.6 marca cada experimento como pré-especificado (com o critério) ou exploratório (acrescentado após resultado); 5.6 resume em tabela | 4.6, 5.6 | W4, W5 |
| S3 | T 2.3 | Comparabilidade das referências: imagens e instâncias; seleção de checkpoint | Tabela única de corpora com quadros, ladrilhos, instâncias por classe e divisão; procedimento de seleção dito uma vez | 4.3, 4.5 | D1, W4 |
| S4 | T 2.4 | Pistas alheias à arma: material, comprimento, modelo, configuração do gerador | 4.2.2 descreve paleta compartilhada e ângulos; 6.1 e 6.5 discutem comprimento como pista candidata; análise de similaridade (A2) mede separabilidade dos recortes sem detector | 4.2.2, 5.1, 6.1, 6.5 | D3, W4, W6 |
| S5 | T 2.5 | Conclusões sobre ajuste fino e treino conjunto dependem da configuração | 6.5 declara: um só cronograma, sem camadas congeladas nem busca de taxa de aprendizado; varredura proposta para a rodada 5 | 5.3, 6.5 | W5, W6 |
| S6 | T 2.6 | Curvas precisão-recall ou limiares justificados | Curvas PR no VisDrone (R, S-oblique-six, F-generic); varredura de limiar nos modelos de três classes (recall de armado × objeto chamado de arma), tabela no limiar padrão, no ótimo de F1 e no ponto de 10% de falso alarme | 4.7, 5.2, 5.4 | D2, W5 |
| S7 | T 2.7 | Diversidade das figuras; curva de aprendizado | Fatos do gerador (corpos, roupas, poses) em 4.2.2; curva de aprendizado na rodada 5 | 4.2.2, 6.5 | D1, W6 |
| S8 | T 2.8 | Luz: concluir só sobre o que foi feito | 5.5 reporta o teste por regime e a estatística de contraste; 6.3 fala em implicação condicional, sem recomendação de aquisição | 5.5, 6.3 | W5, W6 |
| C1 | T 3.1 | O que é "contextualização informada por campo" | 3.1 e 4.1 dizem: experiência profissional de um autor mais fontes públicas; é pano de fundo, não evidência empírica; nenhuma coleta de campo | 3.1, 4.1 | W3, W4 |
| C2 | T 3.2 | Declarações de ética, uso dual, conflito de interesse | 4.1 traz o enunciado; bloco "Declarations" antes das referências (ética, conflito de interesse, disponibilidade de dados, financiamento) | 4.1, Declarations | W4, integrador |
| C3 | T 3.3 | "Design science" | Retirada (D2) | 4.1 | W4 |
| C4 | T 3.4 | Reprodutibilidade | 4.8 reescrita; decisão A3 | 4.8 | W4 |
| A2 | A 10h15, 10h34 | Pré-algoritmo de similaridade (redução de ordem) antes da classificação | Análise de similaridade de recortes por altitude com extrator congelado: matriz de similaridade entre classes, vizinho mais próximo com validação cruzada, projeção em poucas dimensões; entra em 5.1 se separar e em 6.6 como caminho (detectar, depois classificar por similaridade) | 4.4, 5.1, 6.6 | D3, W5, W6 |
| A3 | A 10h34 | Diferenças pequenas entre modelos tratadas como resultado | 4.7 fixa o que conta como diferença resolvível (faixas de sementes que não se cruzam e intervalo da reamostragem); 5.6 e 6.1 dizem quais diferenças passam e quais não; diferenças relativas ao lado das absolutas | 4.7, 5.6, 6.1 | D2, W5, W6 |
| B1 | A 10h09 | "Coisas pequenas de bibliografia" | Aguardar o retorno escrito; nesta rodada só conferir que toda citação tem entrada e toda entrada é citada | 8 | validador |

## 3. Estrutura-alvo, arquivos e orçamento de palavras

Arquivos novos em `01-artigo/manuscrito/`; os antigos ficam congelados em `01-artigo/manuscrito-2026-09-30/` (com `ARTIGO-COMPLETO-2026-09-30.md`, o artigo inteiro com os números de seção que o PDF de 30/09 mostrava). O montador numera o H2 de cada arquivo na ordem de `ORDEM`; H3 e H4 levam número explícito.

| Arquivo | Seção | Subseções | De onde vem (artigo de 30/09) | Palavras |
|---|---|---|---|---|
| `s1-introduction.md` | Abstract; 1 Introduction | 1.1 problem; 1.2 gap; 1.3 objective and RQ1 to RQ3; 1.4 contributions and organisation | §1 | 250 + 1.200 |
| `s2-related-work.md` | 2 Related Work | 2.1 informal settlements and the vertical dimension; 2.2 synthetic data and sim-to-real; 2.3 small-object aerial detection, GSD, person and weapon detection; 2.4 synthesis | §2, §7.7 | 1.500 |
| `s3-study-context.md` | 3 Study Context | 3.1 policing, lethality, territorial control (ADPF 635, 2021, 2025); 3.2 Jacarezinho as morphological reference; 3.3 why the armed and unarmed judgement is the ethical core | §3 condensado, §4, fim de §3 | 1.200 |
| `s4-materials-methods.md` | 4 Materials and Methods | 4.1 design, ethics, positionality; 4.2 generator (4.2.1 layout, 4.2.2 figures, weapons, confusable objects, 4.2.3 illumination, 4.2.4 camera and GSD, 4.2.5 annotation); 4.3 corpora and real data (one table); 4.4 model-free indicators; 4.5 detector and training; 4.6 experiments A to D, confirmatory or exploratory; 4.7 metrics, statistics, criteria; 4.8 reproducibility | §5, §7.1 a §7.7, §8 (definições), §9.1 (protocolo), §10 (critérios), §11.5 | 5.000 |
| `s5-results.md` | 5 Results | 5.1 target characterisation; 5.2 experiment A; 5.3 experiment B; 5.4 experiment C; 5.5 experiment D; 5.6 robustness checks and hypothesis table | §8.1 a §8.3, §9.1 a §9.5, §10.1 a §10.6, §11.4 (números) | 4.500 |
| `s6-discussion.md` | 6 Discussion | 6.1 RQ1 to RQ3 against the literature; 6.2 GSD and viewpoint versus photorealism; 6.3 acquisition practice, illumination; 6.4 dual use, false-alarm rate as harm; 6.5 limitations in one place; 6.6 future work incl. vertical morphology | §8.4, §9.2, §9.4, §11.1 a §11.4, §12, §6 | 2.500 |
| `s7-conclusion.md` | 7 Conclusion; Declarations | answers to RQ1 to RQ3; final message | fecho de §12 | 500 |
| `s8-references.md` | References | | §13 | |

## 4. Agentes e ordem de execução

**Fase 1, em paralelo (análises e fatos; nenhum toca o manuscrito):**
- Z: lista de regras de Zobel (`zobel-checklist.md`).
- D1: fatos dos corpora e do gerador: tabela de corpora (quadros, divisão, ladrilhos, instâncias por classe), GSD e pegada por altitude e distância focal, especificação da câmera de referência com fonte, seleção de checkpoint por modelo, formato dos renders e ausência de ruído, borrão e compressão, diversidade das figuras, o que o experimento de luz mediu, custo de GPU dos experimentos da seção 5. Saída em `06-resultados/revisao-2026-10-17/` e entrada em `RESULTADOS.md`.
- D2: inferência no GPU: intervalos de confiança por reamostragem de imagens no VisDrone (todos os modelos de uma classe, diferenças pareadas), curvas PR, varredura de limiar dos modelos de três classes (divisão de validação e 80 quadros novos), figuras. Mesma saída.
- D3: similaridade de recortes por altitude com extrator congelado (resposta ao áudio). Mesma saída.
- D4: bases aéreas reais nadir com pessoas anotadas (`04-bibliografia/benchmarks-nadir-2026-10-17.md`).

**Fase 2, em paralelo (reescrita por seção, a partir de `ARTIGO-COMPLETO-2026-09-30.md`, desta tabela e da lista de Zobel):** W1 (s1), W2 (s2), W3 (s3), W4 (s4, espera D1), W5 (s5, espera D1), W6 (s6 e s7). Regras comuns: nenhum número novo que não esteja no artigo de 30/09 ou em `06-resultados/`; marcadores `<!--FIG:...-->`, `<!--TAB:chave|...-->`, `@fig{}` e `@tab{}` preservados e movidos para a seção certa; sem travessão; sem caminho, arquivo ou nome interno de corpus; inglês britânico; sigla definida uma vez.

**Fase 3, sequencial:** integrador (remissões cruzadas na numeração nova, duplicações, estilo, inclusão dos resultados de D2 e D3 em 4.7, 5.2, 5.4 e 5.1, abstract novo, bloco Declarations, referências sincronizadas, `ORDEM` do montador); validador (todo número conferido na origem, toda remissão resolve, sem travessão, sem `[X]`, citações e entradas em correspondência, lista de repetições); montagem do PDF, PENDENCIAS, STATUS, DIARIO, commit, página privada atualizada.

## 5. Experimentos propostos para a rodada 5 (decisão do autor; nada roda nesta rodada)

Custo estimado por D1 a partir de `07-blender/PLANO-EXPERIMENTAL.md` e dos tempos medidos em `RESULTADOS.md`.

| # | Experimento | Ponto do revisor | O que decide |
|---|---|---|---|
| R5-1 | Sementes de treino 1 e 2 para S-nadir-150 e S-oblique | S1, A3 | Se o fator nadir contra oblíquo (6,0) sobrevive à dispersão entre corridas |
| R5-2 | Variação da semente de cena (gerar e treinar) para S-oblique-six | S1 | Dispersão devida ao cenário, não só ao treino |
| R5-3 | Curva de aprendizado sobre o tamanho do corpus (antiga 10.1) | S7 | Se o corpus de 180 quadros está na parte plana ou inclinada da curva |
| R5-4 | Ablação só com sol duro (antiga 10.3) | S8 | Se o regime causa a queda ou só coincide com ela |
| R5-5 | Ajuste fino com extrator congelado e taxa menor | S5 | Se o custo do início sintético é artefato do cronograma |
| R5-6 | Zero-shot dos modelos nadir numa base real nadir (candidatas de D4; exige download) | M5 | Se a transferência em nadir é melhor num benchmark de geometria comparável |
| R5-7 | Modelo de três classes a 150 m que passe a condição de validade (corpus maior) | M1 | Medir, em vez de argumentar, a ausência a 150 m |

## 6. Decisões pendentes do autor (e do orientador)

| # | Decisão | Recomendação |
|---|---|---|
| A1 | Retirar "design science" (texto do orientador) | Aplicado em 18/10 com o OK do autor às mudanças sugeridas |
| A2 | Mover a proposta de morfologia vertical para trabalho futuro (seção do orientador) | Aplicado em 18/10 (6.6) com o OK do autor |
| A3 | Liberar gerador, configurações e corpora procedurais (sem dado PCERJ) | **Decidido pelo autor em 18/10: não liberar.** Declarado em 4.8 e em Data availability |
| A4 | Declaração de uso de IA generativa na escrita (política Elsevier) | **Decidido pelo autor em 18/10 e incluído nas Declarations:** Claude (Anthropic) usado para revisar o texto, conferir e corrigir informações e grafia, e auxiliar no monitoramento dos treinos |
| A5 | Nome, afiliação e conflito de interesse do coautor delegado | Obrigatório antes da submissão |
| A6 | Rodada 5: quais dos R5-1 a R5-7 rodar | R5-1, R5-5 e R5-6 primeiro (baratos e ligados à validade) |
| A7 | Fundir Resultados e Discussão (esqueleto de seis seções do revisor) ou manter sete | Mantidas sete (OK do autor em 18/10) até o revisor opinar |
