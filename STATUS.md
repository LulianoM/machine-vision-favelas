# STATUS

Retrato atual do projeto. Reescrever a cada marco. Histórico fica em `DIARIO.md`.

Última atualização: 2026-11-04 (versão curta sem marcas, formato Elsevier como principal), [MAC]; rodada 6 lançada no mesmo dia, [DESKTOP]

## Rodada 6 (lançada 04/11 11:48): a lista do servidor inteira

Decisão do autor em 04/11: "o que manda é o PDF", GPU incluída. Plano e critérios fixados antes em `07-blender/PLANO-RODADA6.md` (commit 7a459ea); cadeia `07-blender/scripts/rodada6.py`, supervisor `supervisiona_rodada6.py` (janela própria, lançado por `retoma_rodada6.cmd`), pausa `pausa_rodada6.py pausa|retoma`, retrato `status_rodada6.py`; estado e logs em `C:rma3-favelalenderila6\`. Ordem: R (item 4, espera o `r_sel.py` das 11:28), P2, Q (item 5), L (item 6), E (item 7), G (item 3), T (sementes), V (item 9), Y (critérios por `06-resultados/rodada6_criterios.py`). Previsão 208 a 258 h com o grupo H (item 8, arma na mão, acrescentado às 12:10 depois da conferência visual de `testa_mao.py`), fim entre 13/11 e 15/11; uma semente de cada item até 08/11. Atalho `retoma_rodada6.lnk` na pasta Inicializar criado às 12:12 com o OK do autor (o supervisor o apaga quando a rodada termina): a rodada volta sozinha depois de reiniciar o PC. E-mail de abertura na thread "Rodada 6: iniciada em 04/11 às 11:48"; um e-mail por etapa concluída.

## O que faltava no servidor para a AIM 2027 (04/11, desktop)

Lista em `08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md`; números e comandos em `06-resultados/RESULTADOS.md`, entrada de 04/11.

| Item | Estado |
|---|---|
| 1, caixa das 5 malhas de arma | **Feito.** `06-resultados/mede_armas.py` (Blender headless), `armas_malhas.md`. Fuzil AK 1,071 × 0,050 × 0,227 m = 22,0 × 1,0 px a 150 m, 43,9 × 2,0 a 75, 94,0 × 4,4 a 35; pistola 0,195 × 0,030 m = 4,0 × 0,6 px a 150 m. Os dois fuzis medem 1,07 m, não 0,92 e 0,94 (nominal): os "19, 38, 81 px" do `[[NEW]]` da 5.1 são limite inferior. Largura de toda arma abaixo de 1 px a 150 m |
| 2, fração sub-stride dos oblíquos | **Feito.** `mede_alvo_split.py` com `ds_morro_obl` e `ds_oblvar`: lado menor < 8 px em 0,94% (S-oblique, 1.912 caixas) e 3,88% (S-oblique-six, 1.521). Já nas duas células da Tabela 5 da versão curta (0,9% e 3,9%); o PDF não foi regerado (fluxo do Mac) |
| 4, teto R com seleção fora do teste | **Rodando desde 11:28**, `07-blender/scripts/r_sel.py` via `lanca_r_sel.cmd`, run `r_pareado_sel`, log `C:rma3-favelalender
_sel.log`. Mesma receita de R; seleção em `ft/sel_r.txt` (265 imagens: a fatia `sel` de 324 menos 59 que estavam na amostra de treino de R). ETA do treino 17:25, cadeia (zero-shot e predições) 17:45. Depois: eficácias recalculadas e entrada própria no RESULTADOS |
| 3, 5, 6, 7, 8, 9 | Na rodada 6 (acima); o 8 é o grupo H, último |


## Versão curta para a AIM 2027 (04/11)

Corpo de 8.728 palavras (alvo do autor: 8 a 9 mil; a professora indicou cerca de 10 mil), 12 tabelas e 5 figuras do v9, sem nenhuma marca `[[NEW]]` (removidas em 04/11 à tarde a pedido do autor; os itens 1 e 2 do desktop entraram no texto: pegada das armas em pixels na 5.1 e sub-stride dos oblíquos na Tabela 5). **Formato principal: Elsevier** (A4, duas colunas, Times 9,5 pt), `08-conferencia/versao-curta/versao-curta-elsevier.html`, 17 páginas, montado por `gera_elsevier.py` a partir de `versao-curta-aim2027.html` (onde o texto se edita): figuras e tabelas estreitas flutuam na coluna, os quatro blocos de figura largos e as Tabelas 2, 4 e 5 atravessam as duas colunas, e `pagina.py --colunas 2` (medição por raster, corte de parágrafo) leva cada bloco largo ao topo ou ao pé de uma página; nenhum buraco acima de 50 pt, última página 166 pt antes do pé. Versão Carta/Times 12/espaço duplo: 41 páginas, 0 buracos. Extended abstract de 3 mil palavras: 17 páginas. A nota de trabalho que abria os PDFs saiu em 04/11 a pedido do autor (texto guardado em `08-conferencia/versao-curta/NOTA-DE-TRABALHO.md`). `gera_pdf.sh` renderiza os três (Elsevier primeiro) em `~/Desktop/AIM 2027 - Versao Curta/`. Lista do que falta no desktop: `08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md` (estado de 04/11 no topo). Decisões do autor em 04/11: título (A) mantido, as cinco figuras ficam, trilha do CFP "Applications of Natural Language Processing or Machine Vision". Pendente para o autor: ler e marcar o PDF Elsevier, revisão do orientador, entrada dos resultados da rodada 6 que terminarem até 19/11, submissão até 19/11.

## v9 (02/11): correções da revisão simulada da AIM aplicadas

Parecer em `01-artigo/revisao-2026-11-02/PARECER-AIM.md` (56 pontos, 16 altos). Aplicado em inglês e espelhado em português, sem perda de conteúdo: resumo com a mesma condição nos dois benchmarks, objetivo restrito ao medido, lacuna de segurança pública fechada (1.4, 2.4, 3.3, 6.4, 7), declaração de uso dual, resultados fora dos Métodos, d′ unificado, 119 referências. Enquadramento fixo: segurança pública, nunca compras públicas. PDFs em `v9_2026-11-02_revisao-aim/` na Área de Trabalho: `elsevier` sem aviso de prévia (41 p.), que é o de submissão, e `elsevier-PT` (44 p.). Leitura final feita e segunda rodada de vereditos por seção sobre o PDF final: pronto para submeter (41 p., 12 figuras, 27 tabelas). Figura da cena ao nível da rua removida a pedido do autor. Pendente para o autor: conferir as quatro citações acrescentadas por escopo na 3.1; decidir se corta extensão antes de submeter; confirmar com AIM@marshall.usc.edu limite de páginas e elegibilidade de mestrando.

## Rodada 4 (encerrada 30/09 10:25, sem grupo com falha)

Disparada em 27/09 11:31, com quatro pausas do autor. Plano e critérios fixados antes do primeiro resultado em `07-blender/PLANO-RODADA4.md` (commit 6ebbaa9); vereditos em `06-resultados/rodada4_criterios.json`; números e comandos em `06-resultados/RESULTADOS.md`, entrada de 30/09. O supervisor saiu sozinho e apagou o atalho de inicialização.

| Critério | Resultado | Veredito |
|---|---|---|
| 10.6, IoU 0,5/0,6/0,75 no VisDrone | nenhum par troca de ordem, nas duas regras | ordem estável |
| 10.6, IoU nos armados | objeto chamado de arma: 35 m acima de 75 m a 0,5, abaixo a 0,6 e 0,75; 35 m e gêmeo empatam a 0,75 (0,132) | ordem muda: taxas vão ao texto nos três limiares |
| Regra oficial do VisDrone (regiões ignoradas) | tudo sobe um pouco; eficácia do S-oblique-six 16,4% | sem regra de derrubada |
| 10.2, escala casada (imgsz 1024) | nadir 0,0128 contra 0,0102 (+25%) | não diverge; corrigir a frase do piloto |
| 9.5, objeto no porte de arma | 15,4% contra 13,7%, McNemar p 0,56 | não sobe: sai a ressalva do ângulo |
| 9.4, sintético e real juntos | 0,4607 contra 0,5220 (5%); 0,5428 contra 0,5709 (10%) | misto pior nas duas frações |
| 11.5, gêmeo a 150 m | detectou 148 de 297 pessoas (0,498 < 0,5) | não interpretável: ausência continua argumentada |
| 9.5, validação maior | quadros novos: 25,3% contra 12,5%, p 0,0001 | estabelecida |
| 10.3, regime de luz | hard sun 0,675 (o pior), overcast 0,791 (o melhor) | cumprido: a 11.3 fica |
| 10.6, sementes | S-oblique-six 15,3% (14,1 a 16,7%); ajuste fino COCO acima do sintético nas três; armados separam nos quadros novos, não no val original | ajuste fino resolvível; armados em parte |

Aplicado ao manuscrito em 30/09 (commit 35b09ca): abstract, 7.6, 7.7, 8.3, 9.3 a 9.5, 10.2, 10.3, 10.6, 10.7, 11.2, 11.3, 11.5, 11.6 e conclusão. Os 2 `[X]` que sobravam (curva da 10.1 e ablação só com sol duro da 10.3) viraram, na revisão geral de 30/09, a frase "specified and has not been run".

## Rodada 3 (encerrada 26/09 17:54, sem grupo com falha)

Disparada em 24/09 19:06. Ficou parada 9,5 h pela queda do PC (24/09 23:25) e mais 6 h em três pausas pedidas pelo autor. Cadeia `07-blender/scripts/rodada3.py`; o supervisor `supervisiona_rodada3.py` saiu sozinho e apagou o atalho de inicialização. Números e comandos em `06-resultados/RESULTADOS.md`, entradas de 25 e 26/09.

| Grupo | O que | Resultado |
|---|---|---|
| Z | Confusão dos modelos armados no protocolo de imagem inteira | objeto chamado de arma: 23,7% (75 m) e 27,3% (35 m) |
| A | S-oblique-six: 6 sítios × 30, pitch 45 a 56°, só pessoas sem arma, câmera livre de mata | VisDrone mAP50 0,1055, eficácia 16,7% (nadir 1,6%, oblíquo de um sítio 9,7%) |
| B | Teste de arma inédita (11.5): metade FAL e submetralhadora nunca vistos | recall 0,466 nas inéditas contra 0,400 nas vistas, razão 1,16 (limiar 0,8): afirmação mantida |
| C | Gêmeo a 75 m do corpus de 35 m (só a altitude muda) | objeto chamado de arma 16,5% a 75 m contra 27,3% a 35 m (p 0,06): o negativo de 35 m vem da altitude, não da pose |
| D | Ajuste fino com 5% e 10% do VisDrone, partindo do sintético e do COCO, teste no val inteiro | 5%: 0,4424 contra 0,5220; 10%: 0,5095 contra 0,5709. O pré-treino sintético custa 6 a 8 pontos de mAP50 |

Tudo entrou no manuscrito (9.3, 9.4, 9.5, 11.5, tabela da 8.2, abstract e conclusão) e os dois PDFs foram regerados na Área de Trabalho. Ficam `[X]` só nas checagens de robustez 10.1 e 10.3, que não estavam na rodada.

Para a próxima rodada longa neste PC: cadeia idempotente com trava e retomada; supervisor em janela própria aberto por atalho na pasta Inicializar (nunca pelo Agendador de Tarefas: o Blender sobe sem o MPFB); pausa e retomada com `pausa_rodada3.py`; retrato com `status_rodada3.py`. Os três servem de molde.

## Rodada 5 (encerrada 22/10 11:05, sem grupo com falha)

Plano e critérios em `07-blender/PLANO-RODADA5.md`; cadeia `07-blender/scripts/rodada5.py`, supervisor `supervisiona_rodada5.py` (atalho `retoma_rodada5.lnk` na pasta Inicializar, apagado pelo supervisor no fim), pausa `pausa_rodada5.py`, retrato `status_rodada5.py`. Ordem S, F, N, Y1, A, D, M, C, Y2; previsão da cadeia 24/10 19:07. HERIDAL (Zenodo 5662351, CC BY 3.0, 8,31 GB) baixando em `C:rma3-favela
eal_nadir\heridal\_bruto\`; o grupo N espera o dado sem travar a cadeia. Lançar sempre pela sessão com `cmd /c retoma_rodada5.cmd` ou por duplo clique; pelo Explorer a partir da sessão, o Blender sobe sem MPFB (visto em 18/10).

## Versões do artigo

Índice em `01-artigo/VERSOES.md`; PDFs em `Área de Trabalho/Artigo Machine Vision Favelas/vN_...`. Vigente: **v8 (27/10)**, com as subseções 3.3 e 3.4 (virada tecnológica na segurança pública; base ética do treino sintético), citações em toda a seção 1 e resumo centrado na segurança pública; antes v7, antes **v6 (27/10)**, a v5 com as decisões do autor sobre as declarações (ética sem comitê, conflito de interesse explícito, origem no projeto de 2022 removida). A v4 (26/10, reenquadrada para administração pública e cortada à metade) foi rejeitada pelo autor e fica só para comparação em `01-artigo/revisao-2026-10-26/`.

## Revisão de 17 e 18/10 (feedback de 14/10)

Feedback de Felipe I. Toledo (texto, quatro áudios transcritos, esqueleto de seções) em `01-artigo/feedback-2026-10-14/` (`FEEDBACK-RECEBIDO.md`, `PLANO-CORRECAO.md`, `zobel-checklist.md`). Pedido central: forma, leitura e estrutura primeiro; método só em Métodos, interpretação só na Discussão, menos repetição; depois reenviar.

| Item | Estado |
|---|---|
| Estrutura | Sete seções: 1 Introduction (RQ1 a RQ3 com escopo), 2 Related Work, 3 Study Context, 4 Materials and Methods, 5 Results, 6 Discussion (limitações todas em 6.5), 7 Conclusion e Declarations. Arquivos `01-artigo/manuscrito/s1` a `s8`; a versão de 30/09 congelada em `01-artigo/manuscrito-2026-09-30/` (com `ARTIGO-COMPLETO-2026-09-30.md`) |
| Análises novas, só inferência | Em `06-resultados/revisao-2026-10-17/` com entradas em `RESULTADOS.md`: fatos dos corpora, GSD e zoom da Z30, seleção de checkpoint (D1); intervalos de 95% por reamostragem, curvas PR, varredura de limiar, leituras de resolubilidade (D2); similaridade de recortes por altitude (D3). Bases reais nadir em `04-bibliografia/benchmarks-nadir-2026-10-17.md` (D4) |
| Achados que mudaram o texto | R selecionou o checkpoint no próprio VisDrone val (teto otimista por seleção, declarado); fator nadir/oblíquo 6,0 com intervalo 4,6 a 7,0 (ainda uma corrida por lado); diferenças do ajuste fino estáveis mas de 5 a 16% relativos; 35 m contra gêmeo resolvível só nos quadros novos; nenhum limiar leva o objeto chamado de arma abaixo de 0,09 com recall acima de 0,42; similaridade não separa arma de objeto em nenhuma altitude (AUC 0,53 a 0,65); renders sem ruído, borrão nem compressão |
| PDF | `C:/Users/marti/Desktop/machine-vision-favelas-elsevier-2026-10-17.pdf`: 34 páginas, cerca de 18,9 mil palavras de corpo, 13 figuras, 23 tabelas, 0 `[X]` |
| Decisões | 18/10: gerador não será liberado (A3); declaração de uso de IA incluída (A4); A1, A2 e A7 aplicados; sem financiamento (declarado); coautor delegado retirado por ora, com 4.1, 3.2, 6.5 e conflito de interesse reescritos sem ele (A5). Rodada 5 a partir da madrugada de 19/10, plano em `07-blender/PLANO-RODADA5.md` |
| Correções de 18/10 | G-MAD e Berwaldt et al. citados (2.2); origem no projeto UFRJ de 2022 e Acknowledgements a Fábio H. P. Guimarães e ao prof. Claudio Miceli; censo com fonte (29.766 na favela, 35.458 no subdistrito, IBGE); resumo para leigo novo (`01-artigo/resumo-leigo-2026-10-18.md`); inventário com 16 corpora e 26 runs; PENDENCIAS sem item aberto. PDF: 34 páginas |

## Artigo

| Item | Estado |
|---|---|
| Versão vigente do orientador | v2 de 2026-09-10 (`01-artigo/rascunhos-professor/2026-09-10_v2_Irigaray.docx`). O arquivo baixado em 17/09 é idêntico a ela: não há v3 |
| Manuscrito por seção | `01-artigo/manuscrito/s1` a `s8` desde 18/10 (estrutura de sete seções); a versão de 30/09 congelada em `01-artigo/manuscrito-2026-09-30/`; PDF por `01-artigo/ferramentas/monta_artigo.py` |
| Pendências do rascunho | `01-artigo/PENDENCIAS.md`: 12 resolvidas (A1, A2, A3, A5, B2, C1 a C5, E1, E2), 20 abertas |
| Resultados empíricos | Sintético e VisDrone (imagem real) com origem em arquivo (`06-resultados/`), todos no manuscrito. **Validado em 10 rodadas em 26 e 27/09** (`01-artigo/VALIDACAO-2026-09-26.md`): 287 achados conferidos e aplicados; todo número bate com a fonte, toda remissão resolve, o PDF sai limpo. Atualizado com a rodada 4 em 30/09 e revisado de novo no mesmo dia (três lentes: números, lógica, forma; 128 trocas, cada uma conferida na fonte; origem dos números conferidos em `06-resultados/RESULTADOS.md`, entrada de 30/09). Nenhum `[X]`: as duas checagens não rodadas estão descritas como especificadas e não executadas. Decidido em 30/09: sai só o texto, sem corpus nem código, e o manuscrito não cita arquivos do repositório. Decisões ainda do autor: lista na entrada do DIARIO de 30/09 (revisão geral) |
| Figuras | 8, todas do braço procedural, rótulos em inglês desde 30/09: nadir, beco, anotação, seis regimes de luz, seis assentamentos, nadir contra oblíquo, armados por altitude, quadros do piloto. Geradas por `06-resultados/figuras_artigo.py` e `07-blender/scripts/previa_dataset.py` |
| Refino de 30/09 | Análise geral e versão refinada: `01-artigo/ANALISE-2026-09-30.md` (diagnóstico, o que foi aplicado, dez críticas que ficam para os autores). Corpo de 28,0 mil para 26,5 mil palavras; abstract de 510 para 330; 11.1 e 10.7 removidas (11 renumerada); histórico de rascunho fora do texto; 17 tabelas numeradas com legenda; 10 figuras citadas no texto (duas novas: desenho experimental e curva do ajuste fino); quadros de autoria fora do PDF, só o aviso de versão prévia |
| Resumo para leigo | `01-artigo/resumo-leigo-2026-09-30.md`, 2 páginas em português para o orientador; PDF por `01-artigo/ferramentas/monta_resumo_leigo.py` |
| PDF | `monta_artigo.py`, formato Elsevier: 17 páginas, 28.621 palavras (com referências), 10 figuras, 17 tabelas, 0 `[X]`. Na Área de Trabalho do desktop. Enviado ao autor em 30/09 por link (página privada https://claude.ai/artifact/WPd1bZtKCVSo6XN56qMeuf, com o resumo para leigo), porque o anexo de 5 MB não cabe na ferramenta de e-mail |
| Rodada 5 no artigo (22/10) | Todos os vereditos da rodada 5 no manuscrito (resumo, 1, 4, 5, 6, 7, Declarations, s8), pelas regras do `PLANO-RODADA5.md`. PDF `C:/Users/marti/Desktop/machine-vision-favelas-elsevier-2026-10-22.pdf`: 39 páginas, 27 tabelas, 13 figuras, 0 `[X]`. Detalhe e conflitos de fonte no DIARIO de 22/10 |
| Busca bibliográfica de 30/09 | Concluída (8 agentes, cinco frentes; relatório em `04-bibliografia/busca-2026-09-30-pontos-abertos.md`) e aplicada no mesmo dia com o OK do autor: 33 trocas no texto, 65 referências novas com DOI reconferido no Crossref, 10 entradas substituídas ou retiradas, 5 corrigidas, lista numa ordem alfabética só |

## Experimento (desktop)

Detalhe em `06-resultados/RESULTADOS.md`.

| Item | Estado |
|---|---|
| Motor | **Blender 5.2.1 headless**, não ARMA 3. O ARMA 3 foi tentado em 11/09 e abandonado sem gerar imagem. **Decidido pelo autor em 20/09: o Blender é o método do trabalho e do artigo** (`docs/DIVERGENCIAS.md`, item 1) |
| Código | `07-blender/scripts/` (gerador `gen_morro.py`, sítios, pessoas MPFB, objetos, cadeias) e `06-resultados/` (avaliação e análise). Caminhos absolutos ainda embutidos (`docs/DIVERGENCIAS.md`, item 13) |
| Classes | Pessoa única nos braços de transferência; `pessoa_armada`, `pessoa_desarmada` e `pessoa_objeto` nos braços armados. Anotação amodal recortada no quadro, visibilidade mínima 0,35 |
| Receita de treino | YOLO11s, imgsz 1280, 60 épocas, batch 6, início COCO, ladrilhos de 1280 px com sobreposição 0,2; ajuste fino com 30 épocas. RTX 2060 6 GB |
| Sim-to-real | **Os três números medidos.** Teto real pareado (1.106 imagens): 0,6311. Zero-shot: nadir 0,0102 (1,6%), oblíquo 0,0614 (9,7%), S-oblique-six 0,1055 (16,7%). Ajuste fino, teste no val inteiro: 0,4424 e 0,5095 partindo do sintético, 0,5220 e 0,5709 partindo do COCO. Sintético e real no mesmo treino (rodada 4): 0,4607 (5%) e 0,5428 (10%), abaixo do só real. Três sementes: S-oblique-six 15,3% em média (14,1 a 16,7%); a vantagem do COCO a 5% é resolvível |
| Armado x desarmado | 75 m: objeto chamado de arma 23,7%, recall de armada 0,547; 35 m: 27,3% e 0,569; gêmeo a 75 m: 16,5% e 0,471. Arma inédita reconhecida como as vistas (razão 1,16). O guarda-chuva é o objeto mais chamado de arma (38 a 40%). Rodada 4: 80 quadros novos replicam 35 m contra gêmeo (25,3% contra 12,5%, p 0,0001); objeto no porte de arma não sobe a taxa; ordem muda com a IoU; gêmeo a 150 m não interpretável (148 de 297 pessoas) |
| Tamanho do alvo | Nadir 4K: 17,6 × 17,5 px, h/w 0,98. VisDrone treino: 13,0 × 24,0, h/w 1,95. `ds_oblvar`: 13,3 × 25,2, h/w 1,85. Ferramentas: `06-resultados/mede_forma.py` (corpora sintéticos) e `06-resultados/mede_alvo_split.py` (VisDrone e piloto, por split) |
| Comparação com a literatura | Kiefer et al. (YOLO): 10,2 sintético contra 43,9 real, razão 23,2%. O S-oblique-six faz 10,5 absoluto (logo acima da faixa deles) e razão 16,7%. Não é comparação direta: o real deles é o treino inteiro do VisDrone com 10 classes, o nosso são 1.106 imagens com uma classe, e o sintético deles tem 40.000 imagens |
| Achado de método | Ladrilhar em escala nativa levou o mAP50 de 0,116 para 0,561 nas mesmas 120 imagens (12/09); a escala de treino pesa mais que o volume |
| Plano experimental | `07-blender/PLANO-EXPERIMENTAL.md`, quatro frentes com custo de GPU declarado |
| Pesquisa a partir do e-mail de 12/09 | Liao et al. e Kiefer et al. lidos e conferidos na fonte em 21/09, com ficha própria em `04-bibliografia/`. G-MAD e IPP seguem por usar |
| Coleção de sítios | `07-blender/scripts/sitios.py`, sítios variando relevo, mata, corredor (avenida, rua, rio) e paleta. O sítio -1 reproduz o `ds_morro_4k` |
| Fila de execução | Rodada 6 rodando desde 04/11 11:48 (`status_rodada6.py`); dentro dela, `r_pareado_sel` (item 4) desde 11:28. Rodadas 2 a 5 encerradas |
| Dado sensível | Os braços com fotogrametria PCERJ (`odm`, `cid150`) não saíram do desktop. Todo o trabalho das rodadas 2 e 3 é procedural (`gen_morro.py`) e pode ser ilustrado |
| Onde estão os binários | `C:\arma3-favela\`. Inventário com SHA256 em `06-resultados/ONDE-ESTAO-OS-DADOS.md`, ainda sem os corpora e pesos das rodadas 2 e 3 |

## Infraestrutura entre as máquinas

| Item | Estado |
|---|---|
| Estrutura do repositório no Mac | Pronta em 17/09 |
| Repositório privado no GitHub | Criado em 17/09: https://github.com/LulianoM/machine-vision-favelas (primeiro commit marcado com a tag `v2-irigaray-verbatim`) |
| Desktop clonado e migrado para o repositório | **Feito em 17 e 18/09.** Clone em `C:\projetos\machine-vision-favelas`, `gh` instalado e autenticado. Ambiente em `docs/AMBIENTE-DESKTOP.md` |
| Base de trabalho do desktop | Em transição: o clone é a base de texto e código; dados, pesos e venv continuam em `C:\arma3-favela\` (proposta de mudança aguardando OK do autor) |
| Tailscale nas duas máquinas, SSH no desktop | Pendente |
| Acesso remoto à tela do desktop | Pendente. Deixou de ser urgente: o pipeline Blender roda sem interface gráfica |
| Painel web do projeto | Publicado em 17/09 (privado), atualizado pelo desktop em 18/09; não reflete as rodadas 2 e 3. Fonte em `painel/painel.html` |
| Dossiê da AIM 2027 (estratégia, 48 missões, modelos de formato) | Dentro do repositório desde 20/09, em `08-conferencia/` |

Painel: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH

## Próximos passos, em ordem

0. [AUTOR] Ler o PDF de 17/10 e reenviar ao revisor (Felipe I. Toledo), que pediu para revisar de novo depois da correção de forma e estrutura. Rodada 5 encerrada em 22/10 (vereditos em `06-resultados/rodada5_criterios.json`, resumo em `06-resultados/RESULTADOS.md`, entrada de 22/10); falta levar os resultados ao artigo. O formato da AIM 2027 não está no edital (só o prazo, 19/11/2026): confirmar com AIM@marshall.usc.edu antes de decidir o destino. Aguardar o retorno escrito do revisor sobre bibliografia.
0. [AUTOR] Ler o PDF revisado de 30/09 (Área de Trabalho do desktop) e decidir os itens que a revisão geral deixou para o autor (lista no DIARIO de 30/09).
0. [AUTOR] Ler `01-artigo/ANALISE-2026-09-30.md`, seção 4: dez decisões que o refino deixou para os autores (extensão e periódico-alvo, título da seção 6, proposta contra o resultado da 9.4, sementes do fator 6,0, nome do coautor delegado, liberação do gerador). Depois revisar as quatro escolhas da busca bibliográfica (DIARIO de 30/09): 51 e 100 mandados, mapas das rotas como premissa, sobrenome "Américo da Silva", dois-pontos na manchete do InSight Crime.
1. [AUTOR] Ler no PDF as passagens novas: abstract (16,7% e a frase do ajuste fino), 9.3, 9.4 (o pré-treino sintético perde para o COCO), 9.5 e 11.5 (gêmeo e arma inédita). Decidir se o resultado da 9.4 muda a proposta da seção 6, que conta com o pré-treino sintético.
2. [AUTOR] Ler no PDF as passagens mudadas pela rodada 4 (abstract, 9.3 a 9.5, 10.2, 10.3, 10.6, 10.7, 11.3, 11.5 e conclusão) e encurtar o abstract, que foi a ~510 palavras. Ficaram fora da rodada, como opcionais: curva de aprendizado da 10.1, corpus só com sol duro, ajuste fino até convergir ou congelado, armado com câmera oblíqua.
3. [AUTOR] Decidir as três divergências ainda abertas em `docs/DIVERGENCIAS.md`: o que fazer com os braços que usam dado PCERJ; como reportar armado x desarmado; blender-mcp. (O item 1, ARMA 3 ou Blender, foi decidido em 20/09: Blender.)
4. [DESKTOP] Pôr no inventário `06-resultados/ONDE-ESTAO-OS-DADOS.md` os corpora e pesos das rodadas 2 e 3, e atualizar o painel.
5. [DESKTOP] Tirar os caminhos absolutos dos scripts (item 13 de `docs/DIVERGENCIAS.md`).
6. [MAC ou DESKTOP] Resolver as 20 pendências abertas de `01-artigo/PENDENCIAS.md`. B1, B3, B6, B7, B9 e B10 foram fechados em 30/09 e o B8 em parte; seguem abertos B4, B5, o resto do B8 e as seções A, C e D.
7. [AUTOR] Devolver ao orientador a lista de pendências e combinar como ele quer receber as edições.
8. [AUTOR, quando quiser] Seguir `docs/SETUP-DESKTOP.md` para Tailscale e OpenSSH.
9. [AUTOR] E-mail para AIM@marshall.usc.edu confirmando o formato exigido na submissão de 19/11/2026 (pendências em `08-conferencia/README.md`).

**Descartado pelo autor em 2026-09-20:** o e-mail ao IPP pedindo LiDAR e MDS de 2024, e o braço
de "cidade de sólidos" sobre a ortofoto do IPP. Não perseguir de novo. Consequência a assumir no
texto: o único braço livre de dado PCERJ passa a ser o procedural (`gen_jacarezinho.py` sobre
OSM e `gen_morro.py`), e é dele que saem as figuras publicáveis.

## Bloqueios

- Os braços com dado PCERJ não podem ser ilustrados no artigo nem no painel.
