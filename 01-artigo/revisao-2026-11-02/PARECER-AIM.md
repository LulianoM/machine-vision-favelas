# Parecer de revisão simulada para a AIM 2027, manuscrito v8

2026-11-02 [DESKTOP]. Leitura do manuscrito v8 (`01-artigo/manuscrito/s1` a `s8`, commit 9129ce3) por oito revisores em paralelo: um por capítulo e um transversal. Lente: revisor da AIM 2027 lendo um artigo de administração pública. Duas perguntas por capítulo: o que sobrou do parecer do Revisor 1 (Felipe I. Toledo, 14/10, pontos de `feedback-2026-10-14/PLANO-CORRECAO.md`) e que feedback construtivo um revisor da AIM daria. Nenhum arquivo do manuscrito foi alterado.

Conferido na fonte por quem consolidou: o par trocado no resumo, a ausência de "dual use" em 4.1 e nas Declarations, os dois valores de d′ e a extensão por seção.

## Quadro geral

| Capítulo | Veredito | Altos |
|---|---|---|
| Resumo e 1 Introdução | 6 pontos | 3 |
| 2 Related Work | 6 pontos | 2 |
| 3 Study Context | 6 pontos | 2 |
| 4 Materials and Methods | 8 pontos | 2 |
| 5 Results | 8 pontos | 2 |
| 6 Discussion | 8 pontos | 3 |
| 7 Conclusion e Declarations | 6 pontos | 2 |
| Referências | 8 pontos | 0 |

Resolvido do Revisor 1 em todo o texto: estrutura de sete seções, RQ1 a RQ3, "design science" retirado, travessão (zero), vazamento de repositório (zero), marcadores pendentes (zero), conectores que ele citou (zero "However" e "Moreover"), siglas definidas uma vez (três deslizes menores), seleção separada de teste, GSD, realismo do sensor, intervalos de confiança, confirmatório contra exploratório, curvas PR, citação e entrada em correspondência (214 pares, zero faltas).

Não resolvido do Revisor 1: extensão e repetição (E2). Corpo com 22.767 palavras contra a meta de 16 mil. No formato da AIM (Times 12, espaço duplo) o manuscrito dá 106 páginas, 91 de corpo. O premiado mais longo de 2026 tem cerca de 10 mil palavras. A seção 3 cresceu em vez de encolher (2.391 contra a meta de 1.200). Resultados reaparecem em detalhe na Discussão e na Conclusão.

Lacuna transversal: a pergunta de segurança pública é aberta na 1.2 e na 3.3 (o instrumento vê o que dizem que vê) e não é fechada em nenhuma seção. Falta dizer, no fim, o que um comando policial, o STF sob a ADPF 635 ou o Ministério Público pode exigir de uma alegação aérea de "pessoa armada" antes que ela entre numa decisão de força, e o que isso significa para o morador. O enquadramento do artigo é segurança pública; compras públicas e prestação de contas administrativa estão fora, por decisão do autor (v4 rejeitada em 26/10; resumo reescrito em 27/10).

## Resumo e 1 Introdução: 6 pontos (3 altos)

Rastros do Revisor 1:
- M1, resíduo: o objetivo (l.33) promete distinguir armado de desarmado por altitude, sensor, pitch e luz; o Experimento C variou só GSD, em nadir, em sintético.
- A3, resíduo: "on the nadir benchmark the order reversed" (l.7, l.47) é dado como firme, mas a inversão não passou a leitura por sementes.
- S1, resíduo: "replicated on held-out frames and across training runs" (l.47); o modelo de 150 m foi treinado uma vez.
- E2 e E3, resíduos leves: Kiefer et al. citado três vezes na 1.1 a 1.3; "the Civil Police flies UAVs" antes de definir UAV (l.15).

Feedback AIM:
1. Alta. Resumo, l.7: o par comparado muda de condição. No VisDrone, 15,3% é S-oblique-six; no HERIDAL, 42,1% é S-oblique de um assentamento (S-oblique-six dá 46,4%). Comparar a mesma condição nos dois benchmarks e dizer que as faixas de sementes se cruzam.
2. Alta. Objetivo (l.33) maior que o medido. Restringir a GSD em nadir, sintético, e à transferência da detecção de pessoa.
3. Alta. Nenhuma das cinco contribuições (l.47) fecha a lacuna de administração pública aberta na l.27. Uma frase: condição de aquisição e taxa de falso armado são o critério verificável que um comando policial e o órgão de controle podem exigir antes que uma alegação aérea entre numa decisão de força.
4. Média. A 1.2 declara como objeto empírico só a escala do objeto carregado (l.29), mas RQ1 e RQ2 testam transferência de pessoa. Nomear as duas aberturas.
5. Média. Afirmações além do medido na l.5 e l.15: o juízo visual sobre força letal tratado como fato (a 3.5 o chama de premissa); "no public benchmark annotates a carried firearm" contradiz a l.43; "claims that omit it are acted on" sem fonte.
6. Média. Resumo com 381 palavras e cerca de 17 números (premiados da AIM: cerca de 245). Introdução com 1.665 contra 1.200. Frase de abertura da 1.1 com 98 palavras.

## 2 Related Work: 6 pontos (2 altos)

Rastros do Revisor 1:
- E1, resíduo: justificativa do gerador na l.19 é método.
- E2, resíduo: "poucos metros do solo" quatro vezes (l.27, 31, 33 e s1 l.43); l.5 repete s1 l.23.
- M5, resíduo: "VisDrone-DET, is the one used here" (l.17); o HERIDAL, segundo benchmark, não aparece.

Feedback AIM:
1. Alta. Nenhuma citação de administração pública na seção; a 2.4 fecha em termos técnicos. Fechar a síntese dizendo que as três aberturas são a premissa perceptiva que a literatura de discricionariedade algorítmica dá como certa.
2. Alta. l.17 contradiz resumo e 4.3 (dois benchmarks). Apresentar o HERIDAL e a geometria majoritariamente oblíqua do VisDrone.
3. Média. A abertura 2 da síntese (l.33) não corresponde à RQ1, e a 2.1 não entra na síntese.
4. Média. l.19: levar a justificativa do gerador para a 4.2; a generalização sobre motores de jogo colide com Kim et al. (2026) na frase anterior.
5. Baixa. "rather than" oito vezes; seção 500 palavras acima do orçamento.
6. Baixa. Duas afirmações sem citação (l.23 "a domain shift in its own right"; l.31 "a modest volume of real data improves generalisation").

## 3 Study Context: 6 pontos (2 altos)

Rastros do Revisor 1:
- D4 (condensar), resíduo alto: 2.391 palavras contra meta de 1.200; a v5 tinha 1.428. Os cortes listados em `revisao-2026-10-26/PLANO-REVISAO.md` não foram aplicados.
- C1, resolvido (l.25 declara que é pano de fundo, não dado).
- E1, resíduo: descrição do gerador e de restrições do estudo (l.23, 43, 47) pertence à 4.1 e 4.2.
- E2, resíduo: a frase da vassoura e do cano duas vezes (l.45 e l.55); l.29 repete s1 l.27; o drone da Polícia Civil quatro vezes no artigo.
- E3, resíduo: STF e UAV escritos por extenso de novo (l.39, l.29).

Feedback AIM:
1. Alta. Aplicar os cortes de 26/10 na 3.1 e fundir a 3.4 com a 4.1, para cerca de 1.300 palavras.
2. Alta. A 3.4 duplica a 4.1 e a 3.5; "regenerated, audited and destroyed" (l.43) colide com a não liberação declarada na 4.8.
3. Média. A 3.3 é revisão de literatura (PAR), não contexto, e soa como enxerto. Levar para a seção 2.
4. Média. O contexto nomeia o instrumento e o controle (STF, ADPF 635), mas não quem decidiria adotar um detector nem a que regime de accountability um falso "armado" estaria sujeito.
5. Média. Afirmações a ajustar: "steep slopes" sem fonte (l.23); controle territorial e milícias sem citação (l.17); 798 óbitos são agregado estadual, não "operations" (l.39); "after 5 years of restricted incursions" conflita com a l.13.
6. Baixa. Ordem: a 3.3 remete à 3.5, que o leitor ainda não leu.

## 4 Materials and Methods: 8 pontos (2 altos)

Rastros do Revisor 1: M1 a M4, S2 a S6, C1, C3, C4 e A2 resolvidos. Resíduos:
- E1: números de resultado e leituras dentro de Métodos (l.65, 134, 151, 167, 173, 179, 181, 183, 194, 199, 210), por exemplo "below the 0.791 of the model of all regimes".
- E2: "held-out, used for neither training nor selection" quatro vezes; grade de cronogramas quatro vezes; sementes cinco vezes.
- S1: R, o denominador de toda eficácia, foi treinado uma vez; não tem faixa de sementes.
- S7: não diz quantos corpos distintos há por corpus.
- C2: risco de uso dual ausente na 4.1.
- C4: "which suffices to re-implement the generator" (l.218) é exagero sem as dimensões das armas, roupas e paleta.

Feedback AIM:
1. Alta. 6.191 palavras de corpo, 28 páginas no formato AIM. Levar para apêndice probabilidades de parcelamento e pose, paleta, orçamentos de luz, pipeline de similaridade, tabela de parâmetros, receita do piloto.
2. Alta. "Six settlements against one" (l.193, l.177) compara condições que também mudam faixa de pitch, classes e enquadramento. Nomear como pacote de fatores.
3. Média. Trocar cada número de resultado usado como critério por remissão à seção 5.
4. Média. Critério "established" de 35 contra 75 m usa teste de proporções sem correção por quadro, embora a l.128 admita dependência. Usar o bootstrap por quadro já usado para d′.
5. Média. Tabela de critérios (l.191 a 200) sem leitura para gestor. Acrescentar "o que muda na afirmação se falhar" e dizer que nenhuma taxa aceitável de falso alarme foi fixada por ser decisão do poder público.
6. Média. Uma frase de uso dual e mitigação na 4.1; fonte pública para "a payload flown at 150 m in nadir over territories of this kind" (l.65).
7. Baixa. Parágrafos de 449 e 360 palavras (l.177, l.37).
8. Baixa. "before any detector is trained" (l.122) é impreciso; "median instance of 17.6 pixels" é a largura mediana (l.134).

## 5 Results: 8 pontos (2 altos)

Rastros do Revisor 1: M2, S1, S2, S6, S8 resolvidos; cerca de 60 números conferidos contra `06-resultados/`, sem divergência de valor. Resíduos:
- E1: protocolo em Resultados (l.112, 121, 138, 151, 202, 229, 233, 248, 272, 354) e rótulos interpretativos na tabela de hipóteses ("shortcut", "caveat withdrawn").
- E2: 0,0102 em três tabelas; R 0,6311 quatro vezes; 0,253 seis vezes.
- A3: "AUC rose as resolution coarsened" (l.106) com intervalos que se cruzam; mAP50 por regime de luz sem intervalo e ordenado mesmo assim (l.348).

Feedback AIM:
1. Alta. A seção não abre com o resultado principal; a tabela de visão geral mistura semente 0, médias e cronogramas. Um parágrafo com um número por RQ.
2. Alta. 22 das 27 tabelas e 31 páginas no formato AIM. Levar ao apêndice piloto, teto, nadir, variedade, pitch, contraste, similaridade, cronograma, curva, PR e limiar.
3. Média. RQ3 em quatro tabelas; consolidar em uma.
4. Média. Mover o protocolo listado para 4.5 a 4.7.
5. Média. Tirar os rótulos interpretativos da tabela de hipóteses e levá-los à seção 6.
6. Média. O teto R teve checkpoint escolhido no próprio teste; dizer em 6.5 o sentido do viés sobre toda eficácia.
7. Baixa. "307.9%" sobre cerca de 4 pontos de mAP50 soa grande para o leitor de gestão; mostrar a diferença absoluta.
8. Baixa. d′ aparece como 0,78 e 0,90 na tabela de similaridade (sem correção) e 0,77 e 0,89 nas demais (com correção), sem dizer qual; legenda da tabela de cronograma fala em "zero-shot" para modelos ajustados; 152 e 180 quadros sem explicação; sinal em "+0.0637 below".

## 6 Discussion: 8 pontos (3 altos)

Rastros do Revisor 1: M4, M5, S5, S7, A2 resolvidos. Resíduos:
- E2, alto: a 6.1 (2.130 palavras) relista os resultados; a l.5 tem cerca de 30 números; o fator 4,08 aparece quatro vezes.
- E2, médio: limitações fora da 6.5 (l.7, 27, 35, 39, 17).
- S4: l.65 diz que arma e objeto compartilham a paleta; a 4.2.2 lista materiais exclusivos dos objetos.
- S8: l.33 e l.35 recomendam peso de treino e voo nublado sem condicional, a partir de um teste com intervalo que inclui zero.
- Falta um quadro de três linhas: demonstrado, hipótese, a validar.

Feedback AIM:
1. Alta. A seção não retoma Selten, Meijer, Gao e Riccucci, West e Bowman. Fechar a premissa "the instrument sees what it is said to see" com o achado.
2. Alta. A 6.4 não traduz o falso alarme em consequência de política: a precisão de 0,37 a 0,46 foi medida na proporção de armados do corpus; com a prevalência real, muito menor, a fração de alertas falsos sobe, e o custo recai sobre quem carrega ferramenta de trabalho.
3. Alta. Faltam implicações explícitas para a operação policial e para o controle externo (STF sob a ADPF 635, Ministério Público). Os testes do artigo viram o que se pode exigir de uma alegação aérea antes que ela entre numa decisão de força: GSD e ângulo declarados, taxa de objeto chamado de arma em imagem não vista, teste de arma não vista, ponto de operação.
4. Média. Afirmações além do medido: l.43 "a system flown at the reference acquisition would mark" projeta sintético em sistema real; l.27 "no appearance-based measure of realism detects it" não foi medido.
5. Média. Desequilíbrio: 2.130 palavras na 6.1, 335 na 6.4, onde está a contribuição para a segurança pública.
6. Média. A 6.3 trata só de luz; o trade-off que importa ao gestor (1,14 cm por pixel exige zoom de 8,5 vezes e cobre 73 vezes menos área) está na 6.2 sem leitura prática.
7. Média. Direitos dos moradores só como pergunta (l.75). Nomear instâncias candidatas e direitos em jogo como opções.
8. Baixa. Remissão da l.35 para a 6.4 errada; l.15 "trained for longer until it passed" sugere ajuste até passar; l.43 frase solta.

## 7 Conclusion e Declarations: 6 pontos (2 altos)

Rastros do Revisor 1:
- M1, resolvido.
- E2, resíduo: 892 palavras contra 500 e 49 numerais; jargão de método ("seed reading", "validity condition").
- C2, resíduo: "dual use" não aparece nas Declarations nem na 4.1.
- Respostas às RQ: só RQ1 é nomeada.

Feedback AIM:
1. Alta. Nenhuma frase diz ao comando policial ou ao órgão de controle o que exigir. Fechar com: nenhuma alegação aérea de "pessoa armada" deveria entrar numa decisão de força sem declarar GSD, geometria de visada e a taxa de desarmado chamado de armado em imagem real.
2. Alta. Uma frase por RQ com o número principal; o resto remete a 5 e 6.1.
3. Baixa. Nomear RQ2 e RQ3; "raise it at 152" sem unidade.
4. Média. Declaração explícita de uso dual, sem atribuir motivo à não liberação.
5. Média. "no personal data" convive com dois benchmarks com imagens de pessoas; dizer que foram usados só para avaliação, sob seus termos, e sem reprodução de imagem; licença do VisDrone não é dita.
6. Média. A declaração de IA cobre texto, checagem e monitoramento. Se a IA escreveu ou rodou código do gerador, do treino ou da análise, a política Elsevier pede isso no método. O autor decidiu manter como está; reabrir só se o fato for esse.

## Referências: 8 pontos (0 altos)

Correspondência OK: 113 entradas, zero citado sem entrada, zero entrada sem citação, zero ano divergente, ordem alfabética correta, 70 DOIs.

1. Média. Estilo misto no "et al.": 41 citações com três ou mais autores por extenso (Kiefer, Ott e Zell nove vezes), contra 15 obras abreviadas desde a primeira.
2. Média. 23 títulos em português sem tradução entre colchetes.
3. Média. Ferramentas sem referência: YOLO11/Ultralytics, pesos COCO, Blender/Cycles, MakeHuman/MPFB, Poly Haven, correção log-linear de d′.
4. Média. Seis entradas a conferir: AlJundi 2025 (volume), Kim 2026 (arXiv contra ACM MM 2026), JOTA via agregador, CBS com URL AMP, Couto e Falcão com título que não bate com a URL.
5. Baixa. "and" dentro de parêntese (s2 l.31); Du e Wang sem iniciais; Shen 2023a e 2023b com autores diferentes; STF não ligado à entrada.
6. Baixa. Anais IEEE em dois formatos; Kiefer 2022 sem "In" e "pp."; capítulos LNCS sem volume.
7. Baixa. "Article" ausente em Liao; Sithole sem volume.
8. Baixa. Movisafe com travessão no título citado; quebras `<wbr>` no DOI de Gevaert; itálico de páginas web inconsistente.

## Para a submissão de hoje

O que tem maior efeito por hora de trabalho, se só der para fazer pouco:
1. Corrigir o par trocado do resumo (Resumo, item 1).
2. Uma frase de implicação para a segurança pública (operação e controle externo) na 1.4, na 6.4 e na Conclusão (Resumo item 3, Discussão itens 2 e 3, Conclusão item 1).
3. Declaração de uso dual nas Declarations.
4. Submeter uma versão curta com o restante como material suplementar, se o formulário permitir, ou confirmar com AIM@marshall.usc.edu se há limite de páginas.
