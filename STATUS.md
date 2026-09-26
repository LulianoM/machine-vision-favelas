# STATUS

Retrato atual do projeto. Reescrever a cada marco. Histórico fica em `DIARIO.md`.

Última atualização: 2026-09-25, 22h40, [DESKTOP]

## Rodada 3 (disparada 24/09 19:06; PAUSADA a pedido do autor desde 25/09 22:26, no C1 com 16/200 quadros; faltam ~19 h de máquina depois da retomada)

Cadeia única, idempotente e retomável: `07-blender/scripts/rodada3.py` (estado em `C:\arma3-favela\blender\fila3\estado.json`, log em `rodada3.log`). Supervisor `supervisiona_rodada3.py` numa janela própria minimizada ("rodada3 - nao feche", fora do app do Claude) relança se morrer ou travar, e um atalho na pasta Inicializar do Windows (`retoma_rodada3.lnk` → `C:\arma3-favela\blender\retoma_rodada3.cmd`) o reabre no login depois de um reinício; o atalho se apaga quando a rodada termina; análise do Claude de 1 em 1 h (`status_rodada3.py`) com e-mail ao autor a cada etapa. Pausa e retomada: `python 07-blender/scripts/pausa_rodada3.py pausa` (ou `retoma`); com `fila3\PAUSA` presente nada é lançado, nem pelo atalho.

| Grupo | O que | Estado |
|---|---|---|
| Z | Confusão dos modelos armados no protocolo de imagem inteira | feito: objeto→armada 23,7% (75 m), 27,3% (35 m) |
| A | Oblíquo combinado S-oblique-six: 6 sítios × 30, pitch 45 a 56°, só pessoas sem arma, câmera livre de mata; treino e VisDrone | feito: mAP50 VisDrone 0,1055, eficácia 16,7% (10x o nadir) |
| B | Teste de arma inédita (11.5): 50 quadros a 75 m, metade FAL e submetralhadora nunca vistos | feito: recall 0,466 nas inéditas contra 0,400 nas vistas, razão 1,16 (limiar 0,8): afirmação mantida |
| C | Gêmeo a 75 m do corpus de 35 m (separa resolução de pose) | em curso, pausado: render 16/200 (~6,4 h), depois treino (~3,8 h) |
| D | Ajuste fino 5% e 10% do VisDrone, do sintético e do COCO, seleção fora do teste | pendente (~8,6 h) |

A cadeia roda fora do app do Claude (supervisor em janela própria) e volta sozinha depois de um reinício do PC, pelo atalho de inicialização, salvo com PAUSA presente. O Agendador de Tarefas do Windows NÃO serve: o Blender sobe sem as extensões do usuário (MPFB).

## Artigo

| Item | Estado |
|---|---|
| Versão vigente do orientador | v2 de 2026-09-10 (`01-artigo/rascunhos-professor/2026-09-10_v2_Irigaray.docx`). O arquivo baixado em 17/09 é idêntico a ela: não há v3 |
| Manuscrito por seção | Feito em 17/09, 8 arquivos em `01-artigo/manuscrito/`, texto verbatim da v2 |
| Pendências do rascunho | Levantadas e verificadas em `01-artigo/PENDENCIAS.md`. Nenhuma resolvida ainda. Em 18/09 o desktop atualizou C5 e D4 e acrescentou D5 a D8 |
| Seção "Conclusion" | Só tem Limitations, Delimitations e Future Research. Falta o fecho |
| Resultados empíricos | Números do sintético e do VisDrone (imagem real), com origem em arquivo (`06-resultados/RESULTADOS.md`), já no manuscrito. Restam `[X]` da rodada 3 (S-oblique-six na 9.3, ajuste fino na 9.4, gêmeo a 75 m na 9.5 e na 11.5, recall do teste de arma inédita na 11.5), a preencher quando a rodada terminar, e os da seção de robustez, sem medida na fila |

## Experimento (desktop)

Estado real, levantado na reconciliação de 17 e 18/09. Detalhe em `06-resultados/RESULTADOS.md`.

| Item | Estado |
|---|---|
| Motor | **Blender 5.2.1 headless**, não ARMA 3. O ARMA 3 foi tentado em 11/09 e abandonado sem gerar imagem. **Decidido pelo autor em 20/09: o Blender é o método do trabalho e do artigo** (`docs/DIVERGENCIAS.md`, item 1). Falta aplicar no texto do manuscrito |
| Código | 19 scripts Python e 8 de batelada em `07-blender/scripts/`. Caminhos absolutos da pasta antiga ainda embutidos (`docs/DIVERGENCIAS.md`, item 13) |
| Classes | `pessoa_armada` e `pessoa_desarmada`. Anotação amodal recortada no quadro, visibilidade mínima 0,35 |
| Datasets | 3 de treino (cada um com versão em ladrilhos de 1280 px) e 2 de teste, todos sintéticos 4K. `dataset_v3` (OSM, 120 imagens), `dataset_odm` (malha real PCERJ, 120), `dataset_cid150` (cidade de sólidos sobre DSM PCERJ, 560), `teste_angulos` (60), `teste_denso` (40) |
| Treino | 5 runs YOLO11 numa RTX 2060. Melhor no sintético: `cid150_s`, mAP50 0,676, mAP50-95 0,327, 8 h 54 min |
| Achado principal | Ladrilhar em escala nativa levou o mAP50 de 0,116 para 0,561 nas mesmas 120 imagens |
| Teste em imagem inteira (sintético, semente nova) | F1 0,849 (ângulo e luz) e 0,787 (multidão); acurácia armado x desarmado 0,781 e 0,759 |
| Sim-to-real | **Um dos três medido em 21/09.** Zero-shot no VisDrone: mAP50 0,0102. Braço real pareado (1.106 imagens, hiperparâmetros idênticos): 0,6311. **Razão de eficácia 1,6%.** Faltam os dois números com dado real misturado. O VisDrone está no disco desde então (6.471 treino, 548 val) |
| Tamanho do alvo, medido | Nosso 4K: largura 17,6 px, altura 17,5, h/w 0,98. VisDrone: 13,0, 24,0, h/w 2,00. **A área bate em 1,00x e a forma difere em 2,04x.** 30,5% das caixas do VisDrone estão abaixo do stride 8. Ferramenta: `06-resultados/mede_alvo.py` |
| Comparação com a literatura | Kiefer et al. (YOLO): 10,2 sintético contra 43,9 real, razão 23,2%. Estamos catorze vezes abaixo. Ressalva: o denominador deles é real FORA do domínio, o nosso é real treinado no próprio VisDrone. Fichas em `04-bibliografia/` |
| Coleção de sítios | `07-blender/scripts/sitios.py`, 40 sítios variando relevo, avenida com carros, densidade, altura e mata. O sítio -1 reproduz byte a byte o `ds_morro_4k`, conferido |
| Fila de execução | `07-blender/scripts/fila_noite.py`, 22 etapas, uma GPU por vez, log e retomada por etapa. Em curso: lote armado a 75 m com objetos confundíveis, depois o teste de dose de variedade |
| Braço oblíquo | **Quebrado e corrigido, precisa refazer.** Saiu com 992 pessoas e zero caixas: o recuo da câmera tinha sinal trocado. É ele que decide se o 1,6% é síntese ou geometria de captura |
| Plano experimental | `07-blender/PLANO-EXPERIMENTAL.md`, quatro frentes com custo de GPU declarado |
| Dado sensível | 3 dos 4 braços usam fotogrametria das fotos da PCERJ. Nada saiu do desktop. Só o braço `v3` pode ser ilustrado (`docs/DIVERGENCIAS.md`, item 2) |
| Pesquisa a partir do e-mail de 12/09 | Liao et al. e Kiefer et al. lidos e conferidos na fonte em 21/09, com ficha própria em `04-bibliografia/`. G-MAD e IPP seguem por usar |
| Onde estão os binários | `C:\arma3-favela\` (44 GB, arquivo morto intacto). Inventário com SHA256 em `06-resultados/ONDE-ESTAO-OS-DADOS.md` |

## Infraestrutura entre as máquinas

| Item | Estado |
|---|---|
| Estrutura do repositório no Mac | Pronta em 17/09 |
| Repositório privado no GitHub | Criado em 17/09: https://github.com/LulianoM/machine-vision-favelas (primeiro commit marcado com a tag `v2-irigaray-verbatim`) |
| Desktop clonado e migrado para o repositório | **Feito em 17 e 18/09.** Clone em `C:\projetos\machine-vision-favelas`, `gh` instalado e autenticado. Ambiente em `docs/AMBIENTE-DESKTOP.md` |
| Base de trabalho do desktop | Em transição: o clone é a base de texto e código; dados, pesos e venv continuam em `C:\arma3-favela\` (proposta de mudança aguardando OK do autor) |
| Tailscale nas duas máquinas, SSH no desktop | Pendente |
| Acesso remoto à tela do desktop | Pendente. Deixou de ser urgente: o pipeline Blender roda sem interface gráfica |
| Painel web do projeto | Publicado em 17/09 (privado), atualizado pelo desktop em 18/09. Fonte em `painel/painel.html` |
| Dossiê da AIM 2027 (estratégia, 48 missões, modelos de formato) | Dentro do repositório desde 20/09, em `08-conferencia/`. Antes só existia no Mac |

Painel: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH

## Próximos passos, em ordem

1. [AUTOR] Decidir as três divergências ainda abertas em `docs/DIVERGENCIAS.md`: o que fazer com os braços que usam dado PCERJ; como reportar armado x desarmado; blender-mcp. (O item 1, ARMA 3 ou Blender, foi decidido em 20/09: Blender.)
2. [DESKTOP] Sim-to-real no VisDrone: baixar o VisDrone-DET, converter com `03-arma3/scripts/visdrone_to_yolo.py` para classe única de pessoa, rodar zero-shot com `blender_v3_tiles2` e `cid150_s`, depois ajuste fino com 5 a 10% de real, depois sintético mais real. São os três números do artigo.
3. [DESKTOP] Tirar os caminhos absolutos dos scripts (proposta no item 13 de `docs/DIVERGENCIAS.md`).
4. [MAC ou DESKTOP] Resolver `01-artigo/PENDENCIAS.md` começando pelas 13 referências ausentes (conferir cada DOI no Crossref).
5. [AUTOR] Devolver ao orientador a lista de pendências e combinar como ele quer receber as edições.
6. [AUTOR, quando quiser] Seguir `docs/SETUP-DESKTOP.md` para Tailscale e OpenSSH.
7. [AUTOR] E-mail para AIM@marshall.usc.edu confirmando o formato exigido na submissão de 19/11/2026 (pendências em `08-conferencia/README.md`).

**Descartado pelo autor em 2026-09-20:** o e-mail ao IPP pedindo LiDAR e MDS de 2024, e o braço
de "cidade de sólidos" sobre a ortofoto do IPP. Não perseguir de novo. Consequência a assumir no
texto: o único braço livre de dado PCERJ passa a ser o procedural (`gen_jacarezinho.py` sobre
OSM e `gen_morro.py`), e é dele que saem as figuras publicáveis.

## Bloqueios

- Nenhum número de sim-to-real existe. Causa conhecida: o teste em imagem real nunca foi rodado e o VisDrone não foi baixado. Não depende de ninguém além do desktop.
- O texto do artigo sobre o método não pode ser escrito antes da decisão do item 1 (ARMA 3 ou Blender, e o papel do dado PCERJ).
- Os braços com dado PCERJ não podem ser ilustrados no artigo nem no painel.

**[DESKTOP 2026-09-22 22:28] Cadeia da noite disparada** (`encadeia.py`, log em `C:\arma3-favela\blender\encadeia.log`), ordem: (1) teste de dose, 6 sitios x 30 imagens 4K, 2 classes, enquadro do controle, treino e VisDrone (~12,5 h); (2) armado a 35 m, 200 quadros, porte realista, fio fino, amostragem em quadro, 64 samples, treino (~7,5 h); (3) obliquo refeito em 4K a 120 m, treino, VisDrone (~10 h). R cheio (43 h) fora da fila. Logs por etapa em `C:\arma3-favela\blender\fila\NN_*.log`. A cadeia para sozinha se um grupo falhar (codigos de saida corrigidos).
