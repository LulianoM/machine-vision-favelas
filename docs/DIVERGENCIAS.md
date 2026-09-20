# Divergências entre o Mac e o desktop

Aberto em 2026-09-18 [DESKTOP], na reconciliação. Cada item registra o que o repositório (lado Mac) afirmava, o que o desktop encontrou, a evidência e uma recomendação. Quem decide é o autor. Marcar `[x]` quando decidido e anotar a decisão e o commit.

Estados: ABERTA (depende do autor), CORRIGIDA (era fato desatualizado, já acertado nos arquivos), REGISTRADA (informação nova, sem conflito).

## A. Divergências que dependem do autor

### [x] 1. O experimento não é ARMA 3, é Blender (DECIDIDA em 2026-09-20 pelo autor)

**Decisão do autor (2026-09-20):** adotar o Blender como método do trabalho e do artigo. Razão dada: facilita a escrita e a criação dos scripts em Python, e é o caminho mais eficaz pelo que o levantamento mostrou. O ARMA 3 passa a constar como origem da ideia em 2022 (Fábio Guimarães, PCERJ) e como prior art via G-MAD, não como método executado. Falta aplicar no texto: `01-artigo/manuscrito/` (método e resultados) e `docs/CONTEXTO.md`.


- Mac afirma: o experimento é o "pipeline ARMA 3 -> bounding box -> YOLO" (`CLAUDE.md`, `03-arma3/`, `docs/CONTEXTO.md`), e o levantamento de 12/09 recomenda "ARMA 3 + código do G-MAD" para quem prioriza publicar rápido.
- Desktop encontrou: o ARMA 3 foi tentado em 2026-09-11 e abandonado no mesmo dia. A missão `dsFavela.Tanoa` chegou a existir, mas nenhuma imagem foi capturada. Motivo registrado na nota do desktop: o jogo não expõe controles, a automação dependia de OCR e de cliques em primeiro plano. Todo o resto (5 treinos, 8 datasets) foi feito no Blender 5.2.1 headless, com anotação por projeção de vértices e oclusão por ray cast.
- Evidência: 6 arquivos `.rpt` de 11/09 com zero linhas `DSIMG`/`DSLBL`; pasta `Documents\Arma 3\Screenshots` inexistente; `07-blender/README.md`; `docs/2026-09-12_nota-obsidian-desktop.md`.
- O que isso toca no artigo: a frase "dados sintéticos de motor de jogo", a Seção de resultados, o crédito ao Fábio e ao prof. Miceli (continua devido pela ideia de 2022, mas o método executado mudou), e a relação com o G-MAD (deixa de ser "mesmo método, publicado antes" e passa a ser "linhagem comum, método diferente").
- Recomendação: descrever o Blender como o método executado; o ARMA 3 entra como origem da ideia em 2022 e como prior art (G-MAD). Não reescrever nada no manuscrito antes de o autor e o orientador decidirem.

### [x] 2. Três dos quatro braços do experimento usam dado da PCERJ (DECIDIDA em 2026-09-20)

**Decisão do autor:** nenhuma imagem derivada do dado da PCERJ entra no artigo, e a utilização é
apenas citada de leve, sem desenvolvimento extenso. Não haverá consulta à PCERJ. Consequência
prática: as figuras saem todas do braço procedural, e o `dataset_cid150` aparece no texto apenas
como segunda amostra de estatística de rótulo, que é como a Seção 8 já o trata.

- Mac afirma: a base de geometria recomendada é a ortofoto pública do IPP de 2024 (mais o LiDAR, se vier), justamente por não ser dado sensível (`docs/CONTEXTO.md`, `PENDENCIAS.md` D3). Os ortomosaicos da PCERJ não trafegam.
- Desktop encontrou: as 567 fotos de drone da PCERJ (ago/2022) foram reprocessadas no OpenDroneMap e viraram a base de `dataset_odm`, `dataset_cid150`, `teste_angulos` e `teste_denso`, do mapa navegável e da quadra. Só o `dataset_v3` (OSM + Poly Haven) é livre de dado PCERJ. Nada disso saiu do desktop: a regra foi respeitada, mas o experimento depende do dado sensível.
- Evidência: `07-blender/scripts/gen_odm.py` (malha ODM), `segmenta_predios.py` (lê `dsm.tif` e `odm_orthophoto.tif`), `build_cidade.py` (laje com foto do ortomosaico); `06-resultados/ONDE-ESTAO-OS-DADOS.md`.
- Consequências: (a) as métricas podem ser citadas, as imagens não, então o artigo não pode ilustrar esses braços; (b) reprodutibilidade por terceiros é nula nesses braços; (c) é preciso confirmar com a PCERJ se publicar métrica derivada do dado é aceitável.
- Recomendação: tratar `blender_v3_tiles2` (OSM) como o braço publicável e ilustrável; tratar os braços PCERJ como resultado interno que mostra o ganho de usar geometria real; e, quando a ortofoto do IPP for baixada, refazer a "cidade de sólidos" sobre ela para ter um braço de geometria real que seja aberto.

### [ ] 3. As classes são armada e desarmada (ABERTA, e virou frente de trabalho em 2026-09-20)

**Direção do autor em 2026-09-20:** em vez de retirar a distinção do artigo, melhorá-la com
modelagem e teste novos. Ver `07-blender/PLANO-ARMADO.md`.

- Mac afirmava: "As classes atuais são pessoas vistas de cima (reproduz 2022)".
- Desktop encontrou: duas classes em todos os datasets, `pessoa_armada` e `pessoa_desarmada`, metade de cada.
- Evidência: `data.yaml` dos 8 datasets; contagens em `06-resultados/RESULTADOS.md`.
- Ponto para o autor: o próprio `RESULTADOS` do desktop avisa que a separação funciona no sintético porque a arma é sempre o mesmo modelo, na mesma posição e com o mesmo contraste, e que reportar isso como capacidade validada seria o salto que o artigo critica. O artigo trata de morfologia vertical e de uso dual; um detector de "pessoa armada" em favela é exatamente o uso policial. Decidir se esse resultado entra no artigo, e como.
- Recomendação: no artigo, reportar detecção de pessoa (classe única) como validação do método, e mencionar a distinção armado e desarmado só como ilustração do risco de uso dual, sem número de acurácia em destaque. O segundo experimento (edificação, pavimentos, adição em laje) continua sendo o que sustenta a tese.

### [x] 4. blender-mcp em uso no desktop apesar do alerta de segurança (DESCARTADA em 2026-09-20)

**Decisão do autor:** não perseguir. O pipeline de dataset não depende do MCP (tudo roda com
`blender -b --python`), então o risco fica contido ao uso interativo.

- Mac afirma (levantamento, parte 4): o `ahujasid/blender-mcp` teve a conta do mantenedor comprometida em agosto de 2026 e tem CVEs abertos; rodar em container ou em safe mode.
- Desktop encontrou: `blender-mcp 1.9.1` instalado em `C:\arma3-favela\mcp-venv`, registrado como servidor MCP do usuário, rodando fora de container. O addon no Blender é de 2026-09-11.
- Evidência: `pip list` do `mcp-venv`; processo `blender-mcp.exe` ativo em 2026-09-17.
- Recomendação: o pipeline de dataset não depende do MCP (tudo roda com `blender -b --python`). Desligar o servidor MCP quando não estiver em uso interativo, ou ativar o safe mode. Decisão do autor.

## B. Fatos desatualizados, já corrigidos

### [x] 5. Delighting: não foi feito, foi contornado (REGISTRADA como limitação)

- Mac afirmava: "Problema técnico a planejar se a fotogrametria de 2022 for usada: remover a iluminação assada da textura".
- Desktop fez: não removeu. No mapa e no `dataset_odm`, a cena é iluminada por ambiente neutro e o céu físico entra só por raio de câmera; o sol sintético fica preso perto da direção real do voo (elevação 45 a 54 graus, azimute dentro de 12 graus do norte, medido em `06-resultados/manifests/dataset_odm.jsonl`). Na "cidade de sólidos" (`cid150`), a saída foi a mitigação que o próprio levantamento sugere: geometria real do DSM, paredes com PBR autoral, cor do telhado amostrada do ortomosaico. Aí o sol varia livremente (28 a 72 graus, 0 a 360).
- Consequência: o braço `dataset_odm` não varia o sol, que é o eixo que em Liao et al. 2026 custa cerca de 10 pontos de mAP50. O braço `cid150` varia.

### [x] 6. Convenção de anotação: já fixada de fato

- Mac afirmava: definir modal ou amodal antes do primeiro lote.
- Desktop fez: amodal recortada no quadro, com visibilidade mínima de 0,35 em 14 raios (`people_mpfb.py`, funções `bbox_2d` e `visibility`). Compatível com o VisDrone.

### [x] 7. Estado do experimento no STATUS, C5 e D4 das pendências

- Mac afirmava: estado desconhecido; "No model has been trained" (texto do orientador).
- Desktop: 5 runs, métricas no sintético em `06-resultados/`. Nenhuma métrica em imagem real. `STATUS.md` e `PENDENCIAS.md` atualizados.

### [x] 8. A pesquisa a partir do e-mail de 12/09 não foi feita no desktop

- Mac afirmava (pelo relato do autor): há uma pesquisa feita no desktop a partir do e-mail.
- Desktop encontrou: nenhum arquivo e nenhuma menção a Liao, G-MAD, IPP ou LiDAR em `C:\arma3-favela\` nem na transcrição da sessão de 12 e 13/09. O e-mail (2026-09-12, 12h45) é posterior à prova de conceito da quadra (09h57 a 11h31 do mesmo dia), que nasceu de um pedido do autor por "recorte com fachadas reais" e usa dado PCERJ, não IPP. Ver `05-levantamento-3d/desktop/LEIA-ME.md`.
- Observação: o link do Gmail no prompt usa um identificador de interface que não é possível conferir por API. A busca por assunto, data e remetente devolve um único e-mail, e ele bate com a descrição.

### [x] 9. `train_yolo.py` original trava no Windows

- Corrigido: `03-arma3/scripts/train_yolo.py` foi sobrescrito com a versão do desktop (`train_yolo_win.py`, tudo dentro de `if __name__ == "__main__"`). A mesma versão está em `07-blender/scripts/` com o nome que os `.sh` chamam.

## C. Informação nova, sem conflito

### 10. Scripts do Google 3D Tiles ficaram de fora

`C:\arma3-favela\tools\fetch_google_3dtiles.py` e `import_google_tiles.py` foram escritos em 12/09 e o autor vetou o caminho na hora. O levantamento confirma que o uso é proibido contratualmente para detecção de objetos. Nenhum tile foi encontrado em disco. Os dois scripts não foram copiados para o repositório.

### 11. Altitude

`v3` e `odm` a cerca de 100 m, `cid150` a cerca de 150 m (a altura real do voo da PCERJ). O VisDrone voa bem mais baixo. O levantamento já apontava altitude como eixo severo de domain shift (SynDrone). Esperar zero-shot fraco no VisDrone por esse motivo, independentemente da qualidade do sintético.

### 12. Limite do dado PCERJ: só nadir

As 567 fotos são todas em nadir a 150 m. Não há textura de fachada: o mapa se sustenta de cima até cerca de 45 m de altura de câmera. Para a tese do artigo (morfologia vertical), isso significa que o levantamento de 2022 captura mal justamente o que o artigo quer medir. Vale uma frase em Limitations.

### 13. Caminhos absolutos embutidos nos scripts (não consertado, de propósito)

Os scripts foram copiados como estão. Ocorrências de `C:\arma3-favela` ou `/c/arma3-favela`:

| Arquivo em `07-blender/scripts/` | Ocorrências | O que aponta |
|---|---|---|
| `build_cidade.py` | 4 | assets Poly Haven, `odm\quadra`, saída `.blend` |
| `build_map.py`, `gen_odm.py`, `final_map.sh`, `run_batch_cidade.sh` | 3 cada | raiz do ODM, malha, `.blend`, venv |
| `gen_cidade.py`, `gen_jacarezinho.py`, `rebuild_map.sh`, `test_pessoas.py` | 2 cada | `quadra.blend`, assets, OSM |
| `build_dsm_mesh.py`, `build_quadra.py`, `export_dsm.py`, `render_quadra.py`, `segmenta_predios.py`, `dataset_real.sh`, `pos_mapa.sh`, `run_after_batch.sh`, `run_batch_odm.sh`, `run_batch_v3.sh` | 1 cada | raiz do ODM ou venv |

Também: os 8 `data.yaml` dos datasets (campo `path`), `03-arma3/scripts/windows/setup_mods.bat` e `start_favela.bat`, e `run_batch_v3.sh` e `run_batch_odm.sh` chamam `../projeto_contexto/.../train_yolo.py`.

Proposta de correção, para depois: um arquivo `07-blender/config.local.toml` (fora do git, com modelo `config.exemplo.toml` versionado) com três chaves, `DADOS` (hoje `C:\arma3-favela`), `BLENDER_EXE` e `PYTHON_EXE`; um módulo `caminhos.py` que lê esse arquivo, com a variável de ambiente `MVF_DADOS` como alternativa; e os `.sh` lendo as mesmas variáveis. Os `data.yaml` podem usar `path` relativo. Enquanto os dados morarem em `C:\arma3-favela`, os scripts funcionam como estão, de qualquer pasta.

### 14. Três versões do `capturaDataset.sqf`

(a) original de 11/09 (estava no repositório); (b) `missao\` do desktop: sem marcadores, usa a posição do jogador em vez de abortar, 500 imagens, 25 a 110 m (guardada em `03-arma3/missao/capturaDataset-500img-25a110m.sqf`); (c) a da pasta da missão do ARMA, que é (b) com 30 imagens, 95 a 105 m, pitch 60 a 90 (agora em `03-arma3/scripts/capturaDataset.sqf`, por ser a que estava em uso). Nenhuma chegou a gerar dado.
