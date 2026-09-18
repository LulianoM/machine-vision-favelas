# STATUS

Retrato atual do projeto. Reescrever a cada marco. Histórico fica em `DIARIO.md`.

Última atualização: 2026-09-18, [DESKTOP]

## Artigo

| Item | Estado |
|---|---|
| Versão vigente do orientador | v2 de 2026-09-10 (`01-artigo/rascunhos-professor/2026-09-10_v2_Irigaray.docx`). O arquivo baixado em 17/09 é idêntico a ela: não há v3 |
| Manuscrito por seção | Feito em 17/09, 8 arquivos em `01-artigo/manuscrito/`, texto verbatim da v2 |
| Pendências do rascunho | Levantadas e verificadas em `01-artigo/PENDENCIAS.md`. Nenhuma resolvida ainda. Em 18/09 o desktop atualizou C5 e D4 e acrescentou D5 a D8 |
| Seção "Conclusion" | Só tem Limitations, Delimitations e Future Research. Falta o fecho |
| Resultados empíricos | Há números no sintético, com origem em arquivo (`06-resultados/RESULTADOS.md`). Nenhum número em imagem real. Nada entrou no texto do artigo ainda |

## Experimento (desktop)

Estado real, levantado na reconciliação de 17 e 18/09. Detalhe em `06-resultados/RESULTADOS.md`.

| Item | Estado |
|---|---|
| Motor | **Blender 5.2.1 headless**, não ARMA 3. O ARMA 3 foi tentado em 11/09 e abandonado sem gerar imagem. Decisão sobre como o artigo trata isso: aberta (`docs/DIVERGENCIAS.md`, item 1) |
| Código | 19 scripts Python e 8 de batelada em `07-blender/scripts/`. Caminhos absolutos da pasta antiga ainda embutidos (`docs/DIVERGENCIAS.md`, item 13) |
| Classes | `pessoa_armada` e `pessoa_desarmada`. Anotação amodal recortada no quadro, visibilidade mínima 0,35 |
| Datasets | 3 de treino (cada um com versão em ladrilhos de 1280 px) e 2 de teste, todos sintéticos 4K. `dataset_v3` (OSM, 120 imagens), `dataset_odm` (malha real PCERJ, 120), `dataset_cid150` (cidade de sólidos sobre DSM PCERJ, 560), `teste_angulos` (60), `teste_denso` (40) |
| Treino | 5 runs YOLO11 numa RTX 2060. Melhor no sintético: `cid150_s`, mAP50 0,676, mAP50-95 0,327, 8 h 54 min |
| Achado principal | Ladrilhar em escala nativa levou o mAP50 de 0,116 para 0,561 nas mesmas 120 imagens |
| Teste em imagem inteira (sintético, semente nova) | F1 0,849 (ângulo e luz) e 0,787 (multidão); acurácia armado x desarmado 0,781 e 0,759 |
| Sim-to-real (os três números do artigo) | **Não medido.** VisDrone não está no disco. Nenhuma imagem real anotada |
| Dado sensível | 3 dos 4 braços usam fotogrametria das fotos da PCERJ. Nada saiu do desktop. Só o braço `v3` pode ser ilustrado (`docs/DIVERGENCIAS.md`, item 2) |
| Pesquisa a partir do e-mail de 12/09 | Não foi feita no desktop. IPP, Liao et al. e G-MAD seguem por ler e por usar (`05-levantamento-3d/desktop/LEIA-ME.md`) |
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

Painel: https://claude.ai/artifact/3XtSXZvhkzovA1ixGZ4rFH

## Próximos passos, em ordem

1. [AUTOR] Decidir as quatro divergências abertas em `docs/DIVERGENCIAS.md`: ARMA 3 ou Blender no texto do artigo; o que fazer com os braços que usam dado PCERJ; como reportar armado x desarmado; blender-mcp.
2. [DESKTOP] Sim-to-real no VisDrone: baixar o VisDrone-DET, converter com `03-arma3/scripts/visdrone_to_yolo.py` para classe única de pessoa, rodar zero-shot com `blender_v3_tiles2` e `cid150_s`, depois ajuste fino com 5 a 10% de real, depois sintético mais real. São os três números do artigo.
3. [AUTOR] E-mail para cartografia.ipp@prefeitura.rio pedindo a nuvem LiDAR e o MDS de 2024 do recorte do Jacarezinho. Continua sendo a ação de maior alavancagem.
4. [DESKTOP] Baixar recorte da ortofoto do IPP de 2024 e refazer a "cidade de sólidos" sobre ela, para ter um braço de geometria real sem dado sensível.
5. [DESKTOP] Tirar os caminhos absolutos dos scripts (proposta no item 13 de `docs/DIVERGENCIAS.md`).
6. [MAC ou DESKTOP] Resolver `01-artigo/PENDENCIAS.md` começando pelas 13 referências ausentes (conferir cada DOI no Crossref).
7. [AUTOR] Devolver ao orientador a lista de pendências e combinar como ele quer receber as edições.
8. [AUTOR, quando quiser] Seguir `docs/SETUP-DESKTOP.md` para Tailscale e OpenSSH.

## Bloqueios

- Nenhum número de sim-to-real existe. Causa conhecida: o teste em imagem real nunca foi rodado e o VisDrone não foi baixado. Não depende de ninguém além do desktop.
- O texto do artigo sobre o método não pode ser escrito antes da decisão do item 1 (ARMA 3 ou Blender, e o papel do dado PCERJ).
- Os braços com dado PCERJ não podem ser ilustrados no artigo nem no painel.
