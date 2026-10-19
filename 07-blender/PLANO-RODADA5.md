# Rodada 5: plano, critérios fixados antes e custo

Escrito em 18/10/2026 [DESKTOP], antes de qualquer resultado da rodada, para a partida depois da
meia-noite (19/10). Responde à seção 5 de `01-artigo/feedback-2026-10-14/PLANO-CORRECAO.md`
(experimentos R5-1 a R5-7) e à decisão A6. As regras abaixo são as que
`06-resultados/rodada5_criterios.py` vai executar. Este arquivo tem de ser versionado (commit e push)
antes de a cadeia partir; qualquer mudança de regra depois disso tem de dizer que veio depois e por
quê. Nada foi lançado, treinado ou renderizado ao escrever este plano.

Fontes dos números: tempos unitários de `06-resultados/revisao-2026-10-17/custo-rodada5.md` e
`checkpoints.md`; leituras de resolubilidade de `resolvivel.md` e `bootstrap_visdrone.md`; bases
reais de `04-bibliografia/benchmarks-nadir-2026-10-17.md`; comandos de `06-resultados/RESULTADOS.md`
e de `07-blender/scripts/rodada3.py` e `rodada4.py`; protocolo do artigo nas seções 4.6 e 4.7 de
`01-artigo/manuscrito/s4-materials-methods.md`. Toda estimativa minha está marcada como estimativa.

## 1. Resumo: ordem, horas e o que cada grupo fecha

A ordem é a pedida pelo autor: primeiro o bloco de validade (R5-1, R5-5, R5-6), depois R5-3, R5-4,
R5-7 e R5-2. Um grupo que falha não impede os outros (molde das rodadas 3 e 4).

| Ordem | Grupo | Experimento | Ponto do revisor | Seção do artigo que fecha | Horas de máquina (estimativa) |
|---|---|---|---|---|---|
| 0 | P | Checagem de partida (disco, GPU, caminhos, um quadro de teste com MPFB) | | | 0,1 |
| 1 | S | R5-1: sementes de treino 1 e 2 para S-nadir-150 e S-oblique | S1, A3 | 5.2, 5.6, 6.1, 6.5 (item 4), 7 | 14 a 15,5 |
| 2 | F | R5-5: ajuste fino com extrator congelado e taxa menor, dois inícios, 5 e 10% | S5 | 4.6 (B), 5.3, 6.1 (RQ2), 6.5 (item 5), 6.6, 7 | 17 a 21,5 |
| 3 | N | R5-6: zero-shot dos modelos nadir e oblíquos numa base real nadir (exige download autorizado) | M5 | 5.2, 6.1, 6.2, 6.5 (item 1), 6.6 | 2 de GPU, mais download e conversão |
| 4 | Y1 | Critérios do bloco de validade (S, F, N) | todos | | 0,2 |
| 5 | A | R5-3: curva de aprendizado sobre o número de quadros (S-oblique-six) | S7 | 5.6, 6.5 (item 7), 6.6 | 11 a 14,5 |
| 6 | D | R5-4: ablação só com sol duro | S8 | 5.5, 6.3, 6.6 | 13,5 a 15,5 |
| 7 | M | R5-7: três classes a 150 m que passe a condição de validade | M1 | 5.4, 6.2, 6.6, 7 e resumo | 8 a 40 (condicional) |
| 8 | C | R5-2: semente de cena para S-oblique-six (duas réplicas) | S1 | 6.1, 6.5 (item 4) | 25,5 a 27 |
| 9 | Y2 | VisDrone oficial dos modelos novos, reamostragem, resolubilidade, todos os critérios | todos | 5.6 (tabela de hipóteses) | 2,5 |

**Total estimado: cerca de 94 a 139 h de máquina** (3,9 a 5,8 dias sem pausas). A faixa larga vem
quase toda do ramo condicional de R5-7 (corpus triplicado, 23 a 28 h, só se o teste barato falhar) e
das paradas antecipadas. O bloco de validade (P, S, F, N, Y1) custa **33 a 39 h**: partindo às 00:00
de 19/10, termina entre 09:20 e 15:20 de 20/10. Cronograma por grupo na seção 5.

Hora de GPU e hora de parede coincidem porque a cadeia roda uma etapa por vez (render e treino juntos
ficam mais lentos, `custo-rodada5.md`). As pausas do autor somam-se à parede: a rodada 4 teve quatro.

## 2. Convenções comuns a todos os grupos

### 2.1 Caminhos e receita

```
PY   = C:\arma3-favela\venv\Scripts\python.exe        (Ultralytics 8.4.148, PyTorch 2.14)
BL   = C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe
RAIZ = C:\arma3-favela\blender                       (diretório de trabalho de todo comando)
SCR  = C:\projetos\machine-vision-favelas\07-blender\scripts
RES  = C:\projetos\machine-vision-favelas\06-resultados
REV  = RES\revisao-2026-10-17
VIS  = C:\arma3-favela\visdrone\visdrone_yolo\data.yaml
FT   = C:\arma3-favela\visdrone\ft                    (ft05.yaml, ft10.yaml; val = sel)
FILA = RAIZ\fila5   (estado.json, logs por etapa, trava, PAUSA)
```

Receita de todos os braços, sem mudança: YOLO11s, imgsz 1280, lote 6, 4 workers, paciência 15,
`deterministic=True`, aumentos de `train_yolo_win.py`; 60 épocas nos sintéticos, 30 no ajuste fino;
ladrilhos de 1280 px com sobreposição de 0,2; seleção do `best.pt` pelo mAP50-95 na divisão `val`
do `data.yaml` do treino (`checkpoints.md`).

Fato conferido no código e nos logs em 18/10, que decide o desenho de R5-5: com `optimizer=auto` o
Ultralytics **ignora `lr0` e `momentum`** e escolhe AdamW com lr 0,002 e momento 0,9 em classe única
(log de `fila3/D2`: "AdamW(lr=0.002, momentum=0.9)"; `engine/trainer.py`, linha 1144: lr =
0,002 x 5 / (4 + nc)), e zera `warmup_bias_lr`. Todos os treinos do artigo rodaram assim. Uma taxa
menor só tem efeito com o otimizador explícito.

### 2.2 Moldes de comando (adaptados de `rodada4.py`)

```
TREINO(nome, data, modelo, ep, s, [--single-cls], extra):
  PY SCR\train_yolo_win.py --data <data> --model <modelo> --imgsz 1280 --epochs <ep> --batch 6
     --workers 4 --name <nome> --seed <s> [--single-cls] [extra]
  retomada:  PY -c "from ultralytics import YOLO; YOLO(r'RAIZ\runs\detect\<nome>\weights\last.pt').train(resume=True)"
  prova:     RAIZ\runs\detect\<nome>\TREINO_OK

ZS(nome):      PY SCR\avalia_sim2real.py --weights RAIZ\runs\detect\<nome>\weights\best.pt
                  --real VIS --imgsz 1280 --out RES\sim2real_<nome>.json
OFICIAL(runs): PY RES\avalia_visdrone_oficial.py --modelos <runs> --out RES\visdrone_oficial_iou.json
PREDS(runs):   (em REV) PY visdrone_preds.py --modelos <runs> --batch 4          (FP32, como em 17/10)
RENDER(ds, n, args, inicio=0):
  BL -b --python-exit-code 1 --python SCR\gen_morro.py -- --out RAIZ\<ds> --dataset <inicio+n>
     <args> --start <inicio+feitos>          (feitos = linhas do manifest.jsonl)
LADRILHA(ds):  PY SCR\tile_dataset.py --data RAIZ\<ds> --out RAIZ\<ds>_tiles --tile 1280 --overlap 0.2
CONF(run, ds, split, saida):
  PY RES\confusao_armado.py --pesos RAIZ\runs\detect\<run>\weights\best.pt --ds RAIZ\<ds>
     --split <split> --instancias --out RES\<saida>          (imgsz 3840, conf 0,25, IoU 0,50)
```

Listas de argumentos do gerador, idênticas às dos corpora originais:

```
NADIR4K      = --samples 96 --res 3840 2160 --people 16 34 --pool 6 --seed 21 --climas todos
               --sitio -1 --mistura 0.5 0.5 0.0 --enquadro quadrado          (ds_morro_4k)
OBLVAR(e, k) = --samples 96 --res 3840 2160 --people 16 34 --pool 6 --seed <e> --climas todos
               --obliqua --pitch-obl 45 56 --camera-livre --mistura 0 1 0 --sitio <k>
               (ds_oblvar com e = 21, k em -1, 0, 1, 2, 3, 4, 30 quadros por sítio)
GEMEO150     = --samples 64 --res 3840 2160 --people 12 24 --pool 6 --seed 43 --climas todos
               --alt 150 --alt-jitter 13 --mistura 0.34 0.33 0.33 --porte-realista --fio-gsd
               --laje 0.75 --amostra-no-quadro                               (ds_armado_150g)
```

### 2.3 As três leituras de resolubilidade (seção 4.7 do artigo, sem mudança)

- **(a) Faixas de sementes:** as faixas mínimo-máximo dos dois modelos sobre suas sementes de treino
  não se cruzam. Exige sementes dos dois lados; com um lado de treino único, registra-se onde o valor
  único cai em relação à faixa do outro.
- **(b) Intervalo pareado:** o intervalo de 95% da diferença pareada exclui zero. No VisDrone e na base
  nadir: 1.000 reamostras de imagens com reposição, semente 0, as mesmas para todos os modelos, a
  diferença calculada na média das sementes de cada lado. Nos corpora sintéticos: reamostragem de
  quadros, semente 0 (1.000 nos três-classes; 2.000 no teste por regime, como no Experimento D);
  pareada quando os dois modelos são medidos nos mesmos quadros, independente nos dois lados quando
  não.
- **(c) 30%:** diferença relativa de pelo menos 30% do menor valor. É descritiva.

Uma diferença é **resolvível** se passa em (a) ou em (b); se não passa em nenhuma, é "não
resolvível". Quando um resultado muda uma frase do artigo, a frase nova diz em quais leituras passou.
Todo experimento desta rodada é pré-especificado no sentido da tabela `rq` da 4.6: acrescentado depois
de resultados anteriores (pedido do revisor), com o critério fixado antes de rodar.

## 3. Experimentos, na ordem da cadeia

### 3.0 Grupo P: checagem de partida (0,1 h)

- P1: disco livre em C: de pelo menos 50 GB; memória de vídeo em uso abaixo de 1 GB e utilização
  abaixo de 10% (`nvidia-smi`); existem `BL`, `PY`, `VIS`, `FT\ft05.yaml`, `FT\ft10.yaml`,
  `RAIZ\yolo11s.pt` e os pesos e corpora listados no checklist (seção 6).
- P2: render de um quadro, `RENDER(_teste_mpfb, 1, NADIR4K)`, e conferência de que o manifest tem
  pelo menos 16 pessoas e o rótulo não está vazio. Prova que o processo nasceu num ambiente em que o
  Blender carrega o MPFB (a primeira etapa de render real só chega dois dias depois).
- Se P falha, a cadeia grava `fim` com `grupos_com_falha = ["P"]` e sai sem rodar nada; o supervisor
  sai junto. O autor corrige e relança.

### 3.1 Grupo S: R5-1, sementes de treino para S-nadir-150 e S-oblique

**Hipótese.** O fator de 6,0 entre S-oblique e S-nadir-150 no VisDrone (0,0614 contra 0,0102,
intervalo pareado +0,0447 a +0,0567) sobrevive à dispersão entre treinos. Hoje a leitura (a) é "não
avaliável": um treino de cada lado.

**Etapas e comandos** (corpus fixo, só a semente de treino muda; intercaladas para que uma pausa
deixe uma semente de cada lado):

| Etapa | Comando | Saída |
|---|---|---|
| S1 | `TREINO(s_nadir_4k_sd1, RAIZ\ds_morro_4k_tiles\data.yaml, yolo11s.pt, 60, 1, --single-cls)` | `runs\detect\s_nadir_4k_sd1` |
| S2 | `TREINO(s_obliquo_sd1, RAIZ\ds_morro_obl_tiles\data.yaml, yolo11s.pt, 60, 1, --single-cls)` | `runs\detect\s_obliquo_sd1` |
| S3 | idem S1 com `s_nadir_4k_sd2`, semente 2 | `runs\detect\s_nadir_4k_sd2` |
| S4 | idem S2 com `s_obliquo_sd2`, semente 2 | `runs\detect\s_obliquo_sd2` |
| S5 | `ZS` dos quatro | `RES\sim2real_s_nadir_4k_sd1.json` e análogos |
| S6 | `OFICIAL(s_nadir_4k_sd1 s_nadir_4k_sd2 s_obliquo_sd1 s_obliquo_sd2)` | acrescenta a `RES\visdrone_oficial_iou.json` |
| S7 | `PREDS` dos quatro | `REV\preds_visdrone_<run>.npz` |

**Tempo.** S-nadir-150 fez as 60 épocas em 3,99 h; S-oblique parou na 49 em 2,8 h (206 s por
época, até 3,4 h se for às 60). Total: 8,0 + 5,6 a 6,8 + 0,6 de avaliação = **14 a 15,5 h**.

**Critério, fixado antes.** Comparações e leituras:

| Comparação | Medida | Lados | (a) | (b) | (c) |
|---|---|---|---|---|---|
| S-oblique contra S-nadir-150 (principal) | mAP50 VisDrone val | 3 contra 3 sementes | avaliável | diferença das médias, pareada | sim |
| S-oblique-six contra S-oblique | idem | 3 contra 3 (passa a avaliável) | avaliável | idem | sim |
| S-nadir-150-six contra S-nadir-150 | idem | 1 contra 3 | onde o valor único cai | idem | sim |

Também se reportam, na média das sementes com faixa, o mAP50 e a eficácia contra R de S-nadir-150 e
de S-oblique, e a razão das médias com intervalo pela reamostragem.

**O que muda no artigo.**

- Comparação principal passa em (a) e (b): na 6.1 (RQ1), "the seed reading being inapplicable with
  one run per model" vira "passes all three readings" (ou as que passar), com o fator dado como razão
  das médias e faixa; na 6.5, item 4, sai a frase que diz que a comparação nadir-oblíquo "still
  rests on one training run per side"; na tabela de hipóteses da 5.6, a linha "Geometry
  load-bearing" troca "n.a." por "yes" em (a); no resumo, na 6.1 e na 7, 1,6% e 9,7% passam a média
  de três treinos com a melhor semente ao lado, como já se faz com os 15,3% de S-oblique-six.
- Passa em (b) e não em (a): os mesmos números, e o texto diz que a diferença é resolvível pelo
  intervalo e não pelas faixas de treino; o fator é escrito com a faixa.
- Não passa em (b) nem em (a): sai "Camera pitch moved the figure most" da 6.1 e o efeito de geometria
  deixa de ser manchete no resumo, na 6.2 e na 7, que passam a dizer que a ordem nadir-oblíquo não é
  resolvível entre treinos. (Improvável pelo intervalo atual, mas fixado.)
- Seis sítios contra um, oblíquo, falha em (a) com as sementes novas: a 6.1 perde "the
  single-settlement value lying outside the range of the three runs" e "Both pass every reading
  available to them" é reescrita com as leituras que passarem.

### 3.2 Grupo F: R5-5, ajuste fino com extrator congelado e taxa menor

**Hipótese.** O custo do início sintético (F-generic acima de F-synthetic por 0,0716 a 5% e 0,0614 a
10%) é propriedade do cronograma único e não ajustado (6.5, item 5): com um cronograma que preserva os
pesos de partida, o início sintético alcança ou passa o genérico.

**Desenho.** Grade 2 x 2 por início e por fatia: backbone treinável ou congelado (`--freeze 11`,
camadas 0 a 10 do YOLO11, isto é, todo o backbone até o C2PSA, conferido em `yolo11.yaml`) x taxa
0,002 (a que o `auto` escolheu) ou 0,0002 (dez vezes menor). Otimizador sempre explícito:
`OPT = --optimizer AdamW --momentum 0.9 --warmup-bias-lr 0.0`, que é o que o `auto` fazia. A célula
(treinável, 0,002) é a dos modelos existentes (`ft05_sint`, `ft05_coco`, `ft10_sint`, `ft10_coco`);
as outras três são novas. Início sintético: `s_oblvar` (semente 0); início genérico: `yolo11s.pt`
(COCO). 30 épocas, seleção em `sel`, teste no VisDrone val inteiro, como no Experimento B. O orçamento
fixo de 30 épocas é mantido e declarado.

Células e nomes: `_fz` = `--freeze 11 --lr0 0.002`; `_lr` = `--freeze 0 --lr0 0.0002`;
`_fzlr` = `--freeze 11 --lr0 0.0002`.

| Etapa | Comando | Saída |
|---|---|---|
| F0 | `TREINO(ft05_coco_rep, FT\ft05.yaml, yolo11s.pt, 30, 0, --single-cls, OPT --freeze 0 --lr0 0.002)` | checagem de reprodução do `ft05_coco` |
| F1 a F6 | `TREINO(ft05_{sint,coco}_{fz,lr,fzlr}, FT\ft05.yaml, <início>, 30, 0, --single-cls, OPT <célula>)` | seis runs a 5% |
| F7 a F12 | idem com `FT\ft10.yaml`, nomes `ft10_...` | seis runs a 10% |
| F13 | `ZS` e `PREDS` dos treze | `RES\sim2real_ft*_{fz,lr,fzlr,rep}.json`, `.npz` |
| F14 | seleção do cronograma (função da cadeia, só lê `results.csv`) | `RES\rodada5_ft_selecao.json` |
| F15 | sementes 1 e 2 da célula escolhida a 5%, para os dois inícios, se não for a original (o início sintético da semente s parte de `s_oblvar_sd<s>`, como na rodada 4) | até quatro runs `ft05_*_<célula>_sd1/sd2` |
| F16 | `ZS` e `PREDS` dos runs de F15 | idem |

**Checagem de reprodução (F0).** Com o otimizador explícito igual ao do `auto`, `ft05_coco_rep` tem
de ficar a até 0,0035 (o desvio entre as três sementes do `ft05_coco`) dos 0,5220 do `ft05_coco`. Se
ficar, as células novas se comparam com os modelos existentes. Se não, a célula de controle passa a
ser o `ft05_coco_rep` e um controle novo a 10% e para o início sintético entra na cadeia, o que é
declarado no texto.

**Seleção do cronograma, fixada antes.** Para cada início e cada fatia, o cronograma escolhido é a
célula cujo `best.pt` tem maior mAP50-95 em `sel` (o critério de seleção de checkpoint do artigo).
Empate a quatro casas: fica a célula original. O teste nunca escolhe o cronograma.

**Tempo.** Ajuste fino de 30 épocas: 0,82 h a 5% e 1,53 h a 10% (`checkpoints.md`; o backbone
congelado só encurta). 6 x 0,85 + 6 x 1,55 + 0,85 + 13 avaliações = **17 h**, mais até 4 h se F15
rodar: **17 a 21,5 h**.

**Critério, fixado antes.** Quantidade de interesse, por fatia: F-generic menos F-synthetic, cada um
no seu cronograma escolhido.

| Comparação | (a) | (b) | (c) |
|---|---|---|---|
| 5%, cronogramas escolhidos | avaliável com F15 (ou com as sementes existentes, se a escolhida for a original) | pareada no VisDrone, médias das sementes | sim |
| 10%, cronogramas escolhidos | um treino por lado | pareada | sim |
| as doze células, uma a uma | n.a. | pareada | sim (descritivo, tabela suplementar) |

Leituras para o texto:

- **Custo robusto ao cronograma:** nas duas fatias, F-generic acima de F-synthetic e resolvível. Na
  6.5, item 5, a frase "so the sign of Experiment B may be a property of the schedule" é trocada por
  uma que diz que o sinal se manteve sob quatro cronogramas (backbone treinável ou congelado, taxa
  0,002 ou 0,0002), cada início com o que a sua divisão de seleção preferiu; a 6.6 perde a frase do
  extrator congelado; a 7 mantém "does not add accuracy" e acrescenta "under four schedules"; a 4.6
  (Experimento B) troca "with no lower learning rate, frozen layers or longer budget for either" pela
  grade, mantendo o orçamento fixo.
- **Custo do cronograma:** em alguma fatia a diferença não é resolvível ou se inverte. A resposta à
  RQ2 muda na 6.1, na 7 e no resumo: "does not add accuracy" passa a valer só para o cronograma
  padrão, e o texto diz em que fatia e com que cronograma o início sintético empatou ou passou. A
  última frase do segundo parágrafo da RQ2 na 6.1 ("or the one schedule that was run ... this design
  cannot say") é substituída pelo resultado.
- **Inversão resolvível a favor do sintético a 5%:** além do anterior, a expectativa fixada antes da
  rodada 3 (valor do pré-treino maior no volume menor) é reavaliada com a diferença das duas fatias.

Fora do grupo, declarado: o treino conjunto (F-joint) não é repetido nos cronogramas novos.

### 3.3 Grupo N: R5-6, zero-shot numa base real nadir

**Exige download, que o autor tem de autorizar.** Nada desta etapa é baixado pela cadeia. A etapa só
roda se o `data.yaml` convertido existir; senão fica no estado `aguardando_dado`, não conta como falha
e é rodada depois com `python rodada5.py` (é só inferência, pode nascer de uma sessão do Claude).

**Base recomendada: HERIDAL** (nota 4 em `benchmarks-nadir-2026-10-17.md`, a única com visada nadir
declarada e caixa de pessoa no chão a menos de um fator 2 da GSD de referência).

| Item | HERIDAL |
|---|---|
| Fonte | página da FESB, Split (`ipsar.fesb.unist.hr/HERIDAL database.html`), fora do ar em 17/10: conferir antes. Espelhos de usuário no Kaggle sem garantia de licença: não usar sem decisão do autor |
| Licença | não declarada nas fontes lidas: o autor confere os termos antes de baixar; nada é redistribuído |
| Conteúdo | 1.647 imagens 4000 x 3000 (algumas 4000 x 2250), 3.229 pessoas, anotação VOC, mato mediterrâneo, nadir a 40 a 65 m |
| GSD | 1,5 a 2,4 cm/px (estimativa do levantamento) |
| Tamanho | não declarado; estimativa minha: 5 a 10 GB (1.647 JPEG de 12 MP a 3 a 6 MB cada) |

Alternativas, se a HERIDAL não estiver disponível (o autor escolhe; nenhuma entra sem autorização):
Stanford Drone Dataset (CC BY-NC-SA 3.0, download direto de um zip de 69 GB, nadir a cerca de 80 m
sobre campus, GSD grosseira); MOBDrone (CC BY 4.0, Zenodo sem registro, 5,5 GB de vídeo ou 243 GB de
quadros, pessoas na água); SeaDronesSee (exige registro no site, que o autor faz por conta própria,
dezenas de GB, filtrar pitch de 80 a 90 graus e altitude de 120 a 180 m). Trocar de base não muda o
critério; muda o conversor.

Manuseio do arquivo baixado: pasta própria e vazia `C:\arma3-favela\real_nadir\heridal\_bruto\`,
fora do git; conversor fora dela; todo Python que lê o baixado roda com `-I`. A base é pública e não é
dado da PCERJ.

**Hipótese.** O fator de 6,0 a favor do oblíquo no VisDrone reflete a geometria oblíqua do benchmark
(84% dos objetos do treino em visada aguda): num benchmark nadir, a vantagem do oblíquo encolhe ou se
inverte.

**Etapas e comandos.**

| Etapa | Comando | Saída |
|---|---|---|
| (manual) | download autorizado; `PY -I SCR\prepara_heridal.py --bruto ...\_bruto --out C:\arma3-favela\real_nadir\heridal\yolo` (VOC para YOLO, classe 0 pessoa, `val` = todas as imagens anotadas) | `...\heridal\yolo\data.yaml`, `RES\heridal_contagens.json` |
| N1 | `PY -I RES\escala_nadir.py --data ...\heridal\yolo\data.yaml --alvo 20.55 --out RES\escala_heridal.json` | imgsz casado, escolhido só com rótulos e tamanhos de imagem, antes de qualquer avaliação |
| N2 | (em REV) `PY preds_nadir.py --data ...\heridal\yolo\data.yaml --tag heridal --imgsz <casado> --modelos <lista>` e o mesmo com `--imgsz 1280` | `REV\preds_heridal_<run>.npz`, `REV\heridal_reproducao.json` (mAP50 do validador e recalculado) |
| N3 | (em REV) `PY bootstrap_nadir.py --tag heridal` | `REV\bootstrap_heridal.json` e `.md` |

Lista de modelos: `s_nadir_4k` e `_sd1`, `_sd2`; `s_variedade`; `s_obliquo` e `_sd1`, `_sd2`;
`s_oblvar` e `_sd1`, `_sd2`; `r_pareado` (referência treinada em real oblíquo, não teto); e, como
exploratório, `armado_150g` com `single_cls`. Protocolo do artigo: classe única, conf 0,001, NMS 0,7,
FP32, lote 4.

Regra do imgsz casado (a da 10.2 da rodada 4): o múltiplo de 32 cuja mediana do lado maior das caixas
da base, na entrada da rede, fique mais perto dos 20,55 px do corpus de registro. O protocolo de 1280
é a medida secundária.

**Tempo.** 12 modelos x 2 imgsz a cerca de 5 min (imagens de 12 MP): **cerca de 2 h de GPU**. Download
e conversão em horas de pessoa, fora da conta.

**Critério, fixado antes.**

- **Validade:** se R ficar abaixo de 0,05 de mAP50 no imgsz casado, o protocolo (convenção de caixa
  ou escala) é que falha, e o resultado é "não interpretável". Limiar convencional, fixado agora.
- **Principal:** S-oblique (3 sementes) menos S-nadir-150 (3 sementes), imgsz casado: (a), (b) e (c).
- **Secundárias:** S-oblique-six (3) menos S-nadir-150-six (1), com as mesmas leituras; a razão
  oblíquo/nadir na HERIDAL contra a do VisDrone (intervalos das duas razões), descritiva.
- Se a ordem principal for diferente entre o imgsz casado e 1280, os dois vão ao texto e o resultado
  é marcado como dependente de escala.

**O que muda no artigo.**

- **Nadir resolvivelmente acima do oblíquo:** a 6.1 deixa de ler o fator de 6,0 só como argumento
  ("We read the factor of 6.0 as the cost of that mismatch") e dá a medida: num benchmark nadir a
  ordem se inverte; na 6.5, item 1, "measure a change of viewing geometry as much as a change of
  scene" passa de afirmação a resultado; a frase da 6.6 sobre HERIDAL sai de trabalho futuro e o
  número entra na 5.2; a 6.2 ganha a medida.
- **Oblíquo resolvivelmente acima também na HERIDAL, com razão compatível com a do VisDrone:** a
  ressalva da 6.1 ("it says what the benchmark rewards and not how the settlement should be flown")
  tem de ser qualificada: o corpus oblíquo transfere melhor também para real nadir; o argumento de
  forma da 6.2 enfraquece e o texto diz isso.
- **Oblíquo acima, mas com razão inteiramente abaixo da do VisDrone:** a geometria do benchmark explica
  parte do fator; o texto dá as duas razões.
- **Não resolvível:** a 6.5, item 1, diz que num benchmark nadir as duas geometrias não se separaram.
- Em qualquer caso, a 6.5 diz que a HERIDAL é mato, não cidade, e que a GSD foi estimada.

### 3.4 Grupo Y1: critérios do bloco de validade (0,2 h)

`PY RES\rodada5_criterios.py --parte prioridade` aplica as regras de S, F e N (o que existir) e grava
`RES\rodada5_criterios.json`. Prova: `fila5\Y1.ok`. Existe para que o texto possa começar a ser
corrigido enquanto o resto da rodada roda.

### 3.5 Grupo A: R5-3, curva de aprendizado sobre o número de quadros

**Hipótese.** Com o resto fixo, o mAP50 zero-shot no VisDrone sobe com o número de quadros de treino;
a pergunta do revisor é se os 180 quadros (152 de treino) estão na parte plana ou na inclinada. É a
checagem da antiga 10.1, com a regra de derrubada que já estava no artigo de 30/09: se o desempenho no
teste real não sobe do menor ao maior corpus mais que a dispersão entre sementes, o número de cenas não
é a variável operante.

**Escolha declarada.** A curva é feita sobre S-oblique-six e não sobre S-nadir-150: o nadir está a
0,0102, perto do piso, onde a curva seria plana por efeito de piso, e S-oblique-six já tem três
sementes no ponto de 152 quadros. O piloto de 40 cenas (nadir, 640 px) continua sem as duas causas
separadas, e isso fica declarado.

**Desenho.** Subconjuntos encaixados dos 152 quadros de treino de `ds_oblvar`: 30, 60, 90 e 120
quadros, estratificados por sítio (de cada sítio, a fração N/152 dos seus quadros de treino, ordem
sorteada uma vez com `random.Random(5)`), cada um com todos os ladrilhos dos seus quadros (nomes
`<quadro>_<x>_<y>` do `tile_dataset.py`), por link físico. A validação é a mesma de `ds_oblvar_tiles`
(144 ladrilhos de 28 quadros) em todos os pontos. Épocas fixas em 60, como em todos os braços: os
pontos menores dão menos passos de gradiente, o que é declarado.

| Etapa | Comando | Saída |
|---|---|---|
| A1 | `monta_curva` (função da cadeia) | `RAIZ\ds_oblvar_c030_tiles` ... `c120_tiles`, `RES\curva_subconjuntos.json` (lista de quadros por ponto) |
| A2 a A5 | `TREINO(s_oblvar_c<N>, RAIZ\ds_oblvar_c<N>_tiles\data.yaml, yolo11s.pt, 60, 0, --single-cls)` para N = 030, 060, 090, 120 | quatro runs |
| A6 a A9 | sementes 1 e 2 para `c030` e `c120` | quatro runs `_sd1`, `_sd2` |
| A10 | `ZS` e `PREDS` dos oito | `RES\sim2real_s_oblvar_c*.json`, `.npz` |

**Tempo.** Proporcional aos ladrilhos (198 s por época nos 890 de `s_oblvar`), no teto de 60 épocas:
0,65 + 1,3 + 2,0 + 2,6 h, mais 2 x 0,65 e 2 x 2,6 h de sementes, mais 1,4 h de avaliação: **11 a
14,5 h** (a paciência encurta).

**Critério, fixado antes.**

- **Regra da antiga 10.1:** o número de quadros é operante se 152 quadros ficam acima de 30 quadros
  em (a) e em (b) (três sementes de cada lado). Senão, a conclusão da RQ1 passa a ser dita como
  propriedade do gerador, não do tamanho do corpus.
- **Plano ou inclinado no fim:** 152 contra 120 quadros (três sementes de cada lado). Inclinado se
  passa em (a) e (b); plano se não passa em nenhuma; "subindo dentro da dispersão de treino" se só
  passa em (b). (c) reportada.
- Descritivo: ajuste mAP50 = a ln(N) + b nas médias dos cinco pontos, com o ganho previsto por
  duplicação (a ln 2), e a curva do teto sintético (val próprio) ao lado.

**O que muda no artigo.** Na 6.5, item 7, "whether 180 frames sit on the flat or the rising part of
that curve is unknown" é trocada pelo resultado, e a frase sobre o piloto fica; na 5.6, "Every check
fixed in advance was run except the learning curve over corpus size and the hard-sun ablation" é
atualizada; a 6.6 perde "the learning curve". Se inclinado: a 6.1 (RQ1) diz que os 15,3% não são o
teto do método com este gerador e dá o ganho por duplicação. Se plano: a 6.1 e a 6.2 dizem que o
volume não é o gargalo neste tamanho, o que reforça o peso da geometria. Se a regra da 10.1 falhar:
a resposta à RQ1 é reescrita como propriedade do gerador.

### 3.6 Grupo D: R5-4, ablação só com sol duro

**Hipótese.** A queda sob sol duro (mAP50 0,675 contra 0,755 a 0,791 nos outros regimes, Experimento
D) é dificuldade do regime (sombra projetada enchendo o fundo), e não efeito de o regime ser um sexto
do treino. Se for do regime, um modelo treinado só com sol duro, com seis vezes mais quadros desse
regime, continua abaixo do modelo de todos os regimes sob nublado.

**Etapas e comandos.** Mesmo comando do corpus de registro, só com sol duro (mesma semente de cena e
sítio; os quadros diferem dos de teste, que são os índices 180 a 299 do comando com todos os regimes).

| Etapa | Comando | Saída |
|---|---|---|
| D1 | `RENDER(ds_soldur_4k, 180, NADIR4K com --climas sol_duro)` | `RAIZ\ds_soldur_4k` |
| D2 | `LADRILHA(ds_soldur_4k)` | `RAIZ\ds_soldur_4k_tiles` |
| D3 | `TREINO(s_soldur_4k, RAIZ\ds_soldur_4k_tiles\data.yaml, yolo11s.pt, 60, 0, --single-cls)` | `runs\detect\s_soldur_4k` |
| D4 | `PY RES\por_regime.py --pesos ...\s_soldur_4k\weights\best.pt --ds RAIZ\ds_regime_4k --tiles RAIZ\ds_regime_4k_tiles --por-quadro --out RES\por_regime_s_soldur_4k.json` e o mesmo para `s_nadir_4k` com `--out RES\por_regime_s_nadir_4k_r5.json` (o arquivo de outubro não é sobrescrito) | acertos e caixas por quadro, para o bootstrap pareado |
| D5 | `ZS(s_soldur_4k)` | `RES\sim2real_s_soldur_4k.json` (exploratório) |

**Tempo.** Render 180 quadros a 96 amostras: 8,7 a 11,1 h (`ds_morro_4k`); treino até 4,0 h; avaliações
0,5 h: **13,5 a 15,5 h**.

**Critério, fixado antes.** Medida principal: mAP50 nos ladrilhos de cada regime (ponto); inferência
pelo recall a conf 0,25 em imagem inteira, bootstrap de quadros (2.000, semente 0).

- D-i (pareada, os mesmos 20 quadros de sol duro): especialista menos generalista sob sol duro.
  Descritiva do ganho com mais dado do regime.
- D-ii (independente): especialista sob sol duro menos generalista sob nublado (0,791 de mAP50; recall
  0,796). É a que decide.
- (a) não se aplica (um treino de cada); (c) no mAP50.

Leituras:

- **Regime intrinsecamente mais difícil:** em D-ii o intervalo fica inteiro abaixo de zero e o mAP50
  do especialista sob sol duro fica abaixo de 0,791. Na 6.3, "and the hard-sun-only ablation was not
  run" vira a medida (o especialista não fechou a diferença), e o condicional da 6.3 fica; a 5.5 ganha
  o resultado e a 6.6 perde a ablação.
- **Queda de participação no treino:** em D-ii o intervalo inclui zero ou fica acima. O condicional da
  6.3 ("if the difficulty measured under hard sun holds on real imagery ... a covered sky is
  preferable") é reescrito: a dificuldade sob sol duro some quando o treino vê sol duro bastante, e a
  implicação passa de quando voar para com que luz treinar; o parágrafo de prática de aquisição da 6.3
  é ajustado.

Fora do grupo, declarado: o espelho "todos menos sol duro" (mais 15,5 h) não entra.

### 3.7 Grupo M: R5-7, três classes a 150 m que passe a condição de validade

**Hipótese.** O gêmeo de 150 m falhou a validade por pouco (148 de 297 pessoas encontradas, 0,498,
parada na época 36 com o melhor peso na 21). Treinar mais tempo, e só se isso não bastar, triplicar o
corpus, leva o modelo acima da metade; então a ausência de separação entre arma e objeto a 4,88 cm/px
pode ser medida em vez de argumentada.

**Etapas e comandos.** Primeiro o teste barato (sugerido em `custo-rodada5.md`), depois o ramo caro,
condicional.

| Etapa | Comando | Saída |
|---|---|---|
| M1 | `RENDER(ds_armado_150g_extra, 80, GEMEO150 --val 1.0, inicio=200)`: índices 200 a 279 da semente 43, gêmeos quadro a quadro dos 80 quadros novos de 35 m e de 75 m | `RAIZ\ds_armado_150g_extra` (teste independente) |
| M2 | `TREINO(armado_150g_e120, RAIZ\ds_armado_150g_tiles\data.yaml, yolo11s.pt, 120, 0, --patience 30)` (três classes) | `runs\detect\armado_150g_e120` |
| M3 | `CONF(armado_150g_e120, ds_armado_150g, val, confusao_armado_150g_e120.json)`, `CONF(armado_150g_e120, ds_armado_150g_extra, val, extra_armado_150g_e120.json)` e, descritivo, `CONF(armado_150g, ds_armado_150g_extra, val, extra_armado_150g.json)` | taxas, d′ e instâncias |
| M4 | validade (função da cadeia) | `RES\rodada5_validade_150.json` |
| M5 | só se M4 falhar: `RENDER(_armado_150g_mais, 400, GEMEO150, inicio=280)` (índices 280 a 679, divisão padrão de 15% em validação) | `RAIZ\_armado_150g_mais` |
| M6 | só se M4 falhar: junta `ds_armado_150g` e `_armado_150g_mais` em `ds_armado_150g_600` (link físico, prefixo no nome) e `LADRILHA` | `RAIZ\ds_armado_150g_600_tiles` |
| M7 | só se M4 falhar: `TREINO(armado_150g_600, ..._600_tiles\data.yaml, yolo11s.pt, 60, 0)` (receita padrão dos três-classes, para comparar com 35 e 75 m) | `runs\detect\armado_150g_600` |
| M8 | só se M4 falhar: `CONF` no val do `_600` e no `ds_armado_150g_extra` | `confusao_armado_150g_600.json`, `extra_armado_150g_600.json` |

Se M4 passa, M5 a M8 ficam no estado `dispensada` (prova gravada, nada roda).

**Tempo.** M1: 80 quadros a 128 s, 2,8 h. M2: 261 s por época, de 4,5 h (parada perto da época 60) a
8,7 h (as 120). M3: 0,3 h. Ramo condicional: render de 400 quadros a 128 s (14,2 h) mais o sorteio
sem render dos 280 anteriores a cerca de 8 s cada (0,6 h por partida), treino com cerca de 3.650
ladrilhos (8 a 13 h), 0,3 h de confusão: 23 a 28 h. Total: **8 a 12 h sem o ramo, até 40 h com ele**.

**Critério, fixado antes.**

- **Validade:** o modelo encontra pelo menos metade das pessoas anotadas, em qualquer classe, no seu
  val **e** nos 80 quadros independentes. Abaixo disso, não interpretável, como na rodada 4.
- **Medida:** d′ entre armada e objeto confundível, z(armada chamada de armada) menos z(objeto chamado
  de armada), com correção log-linear; intervalo de 95% por 1.000 reamostras de quadros, semente 0
  (4.7 do artigo; a rodada 4 usou 2.000 neste d′, o que é declarado). Taxa de objeto chamado de
  armada a 0,25, com intervalo.
- **Regra (a da 11.5 da rodada 4):** se o intervalo de d′ inclui 0, a ausência a 150 m passa a medida;
  se exclui, há separação acima do acaso no sintético, e como a arma é argumentada irresolvível a
  150 m (a pessoa em planta tem 9,8 px, `gsd_zoom.md`), essa separação usa outro indício (comprimento,
  silhueta) e o texto a trata como atalho, não como capacidade.
- **Curva 35/75/150 m** nos 80 quadros independentes dos três gêmeos (mesmos índices): d′ e taxa de
  objeto; 150 contra 75 m pela leitura (b), reamostragem independente, e (c). (a) não se aplica (uma
  semente a 150 m).

**O que muda no artigo.** Se o modelo passa a validade: na 7, "at 4.88 the absence remains argued
rather than measured, because the one model trained there failed its validity condition" é trocada
pelo resultado; na 5.4, o parágrafo de 4,88 cm/px deixa de dizer "not interpretable"; a linha de
validade da tabela de hipóteses muda; a 6.6 perde "a three-class measurement at 150 m"; o resumo
acompanha. Se falha também o ramo de 600 quadros: o texto diz que triplicar o corpus não deu validade
e que o limite é de detecção a 9,8 px, não de volume (6.2); a ausência continua argumentada.

### 3.8 Grupo C: R5-2, semente de cena para S-oblique-six

**Hipótese.** A dispersão devida ao cenário (assentamentos sorteados com outra semente nos mesmos seis
sítios) é da ordem da dispersão entre treinos (0,0887 a 0,1055), e a vantagem de seis sítios sobre um
no oblíquo sobrevive a ela.

**Etapas e comandos.** Duas réplicas, uma inteira antes da outra, com sementes de cena 22 e 23 (a 21 é
a do corpus existente; 43 e 47 estão em uso nos três-classes). Treino com semente 0.

| Etapa | Comando | Saída |
|---|---|---|
| C1 | para k em -1, 0, 1, 2, 3, 4: `RENDER(_oblvar_e22_s<k>, 30, OBLVAR(22, k))`; junta em `ds_oblvar_e22` (a `junta_oblvar` da rodada 3 com a semente como parâmetro) | `RAIZ\ds_oblvar_e22` |
| C2 | `LADRILHA(ds_oblvar_e22)` | `RAIZ\ds_oblvar_e22_tiles` |
| C3 | `TREINO(s_oblvar_e22, ..._e22_tiles\data.yaml, yolo11s.pt, 60, 0, --single-cls)` | `runs\detect\s_oblvar_e22` |
| C4 | `ZS` e `PREDS` | `RES\sim2real_s_oblvar_e22.json`, `.npz` |
| C5 a C8 | idem com a semente 23 | `s_oblvar_e23` |

**Tempo.** Por réplica: render de 180 quadros a 96 amostras em seis sítios, 10,0 h (medido em
`ds_oblvar`); treino 2,5 a 3,3 h; avaliação 0,2 h. Duas réplicas: **25,5 a 27 h**.

**Critério, fixado antes.**

- Descritivo: faixa sobre as três sementes de cena (21, 22, 23; treino 0) ao lado da faixa sobre as
  três sementes de treino (cena 21).
- C-ii: S-oblique-six nas três sementes de cena contra S-oblique nas três sementes de treino (grupo
  S): (a), (b) pareada nas médias, (c).
- A eficácia de S-oblique-six continua a da cena 21 (média de três treinos, 15,3%), com a faixa de cena
  dada ao lado.

**O que muda no artigo.** Na 6.5, item 4, "and the settlement seed was never varied" é trocada pela
medida (a faixa de cena contra a de treino). Se C-ii falha em (a) (faixas se cruzam), a frase da 6.1
sobre seis sítios contra um no oblíquo passa a dizer que o valor de um sítio cai dentro da faixa de
cena. Se a faixa de cena for mais que o dobro da de treino, a 6.1 diz que o cenário domina a dispersão
e que os 15,3% devem ser lidos com essa faixa.

### 3.9 Grupo Y2: fechamento (2,5 h)

| Etapa | Comando | Saída |
|---|---|---|
| Y2 | `OFICIAL` de todos os modelos novos de classe única (regra oficial e IoU 0,50, 0,60, 0,75) | `RES\visdrone_oficial_iou.json` |
| Y3 | (em REV) `PY bootstrap_visdrone.py --sufixo r5` e `PY resolvivel.py --sufixo r5`, com os pares novos | `REV\bootstrap_visdrone_r5.*`, `REV\resolvivel_r5.*` (os de 17/10 ficam como estão) |
| Y4 | `PY RES\rodada5_criterios.py --parte tudo` | `RES\rodada5_criterios.json` |

A regra da rodada 4 sobre IoU continua: um par cuja ordem muda entre 0,50, 0,60 e 0,75 vai ao texto
nos três limiares.

## 4. Desenho da cadeia

Molde da rodada 3, com as primitivas que a rodada 4 acrescentou (render com índice inicial, treino com
semente, `varios`, provas `.ok`):

- **Idempotente.** Cada etapa tem um arquivo de prova; se existe, a etapa é pulada. Render retoma pelo
  número de linhas do manifest (`--start`). Treino retoma do `last.pt` e só conta como feito com
  `TREINO_OK` (o `best.pt` existe desde a primeira época e não serve de prova).
- **Trava.** `fila5\rodada5.trava` com o PID; uma segunda instância sai.
- **Falha.** Duas tentativas por etapa; se falha, o resto do grupo é pulado e os outros grupos seguem.
  Exceção: falha em P encerra a cadeia (seção 3.0).
- **Estados novos.** `aguardando_dado` (N sem `data.yaml`: não é falha nem prova; a cadeia grava `fim`
  e o log diz para rodar `python rodada5.py` depois do download) e `dispensada` (M5 a M8 quando M4
  passa: grava a prova).
- **Supervisor.** `supervisiona_rodada5.py`, aberto por `retoma_rodada5.cmd` numa janela minimizada
  própria ("rodada5 - nao feche") e por um atalho `retoma_rodada5.lnk` na pasta Inicializar do
  Windows. Nunca pelo Agendador de Tarefas, WMI ou explorer por DCOM: aí o Blender nasce sem as
  extensões do usuário e o MPFB some (testado em 23 e 25/09). Também não pela sessão do Claude:
  processo nascido dela morre quando o app reinicia. A cada 5 min: se a cadeia não roda, lança; se
  nenhum log de `fila5` mudou em 60 min (45 na rodada 3; sobe porque o sorteio sem render dos 280
  quadros de M5 pode passar de 37 min calado), mata a árvore e relança. Sai quando o estado tem `fim`
  e apaga o próprio atalho. Com `fila5\PAUSA` presente, sai sem lançar nada.
- **Pausa.** `pausa_rodada5.py pausa` cria `PAUSA`, mata o supervisor primeiro e depois a cadeia, o
  Blender e o treino (perde-se só o quadro ou a época em curso). `pausa_rodada5.py retoma` apaga
  `PAUSA` e abre `retoma_rodada5.cmd`.
- **Retrato.** `status_rodada5.py`: cadeia viva ou não, etapa corrente com progresso e ritmo medido,
  idade do log, erros recentes, previsão de término, etapas concluídas desde a última checagem com o
  número de cada uma (marcadas em `fila5\relatadas.txt`). É a base da checagem horária e dos e-mails
  por etapa num fio só, como nas rodadas anteriores, e da previsão de término mandada na partida.

### 4.1 Scripts a criar (não criados ainda)

| Novo | Copiar de | O que muda |
|---|---|---|
| `07-blender/scripts/rodada5.py` | `rodada3.py` (estrutura, trava, laço, estado) com as primitivas de `rodada4.py` | `FILA = fila5`, `rodada5.log`, `rodada5.trava`; `ETAPAS` dos grupos P, S, F, N, Y1, A, D, M, C, Y2; `treina()` ganha `extra` (flags) e `paciencia`; funções `preflight`, `monta_curva`, `junta_oblvar(semente, dst)`, `junta_150_600`, `selecao_ft`, `validade_150`; estados `aguardando_dado` e `dispensada` |
| `07-blender/scripts/supervisiona_rodada5.py` | `supervisiona_rodada3.py` | 3 para 5 em nomes, fila, log (`vigia5.log`), atalho e título; `PARADO_S = 60 min`; `mata_cadeia` também mata `confusao_armado.py`, `por_regime.py`, `visdrone_preds.py`, `preds_nadir.py`, `avalia_sim2real.py` |
| `07-blender/scripts/pausa_rodada5.py` | `pausa_rodada3.py` | nomes; lista de processos com `por_regime.py`, `visdrone_preds.py`, `preds_nadir.py`, `avalia_visdrone_oficial.py`, `rodada5_criterios.py` |
| `07-blender/scripts/status_rodada5.py` | `status_rodada3.py` | `import rodada5 as R`; segundos por quadro: D1 183, M1 e M5 128, C1 e C5 200; segundos por época: S1 e S3 240, S2 e S4 206, F a 5% 98, F a 10% 184, A proporcional a 198, D3 240, M2 261, M7 780, C3 e C7 198; diretórios de render de D1, M1, M5, C1, C5 |
| `07-blender/scripts/retoma_rodada5.cmd` | `retoma_rodada3.cmd` | nomes e título da janela |
| atalho `retoma_rodada5.lnk` na pasta Inicializar | o da rodada 3 | é configuração persistente: só com o OK do autor; o supervisor o apaga no fim |
| `06-resultados/rodada5_criterios.py` | `rodada4_criterios.py` | as regras deste plano; `--parte prioridade` ou `tudo`; só lê arquivos de `06-resultados` |
| `06-resultados/revisao-2026-10-17/preds_nadir.py` | `visdrone_preds.py` | `--data`, `--tag`, `--imgsz`; saída `preds_<tag>_<run>.npz` e `<tag>_reproducao.json` |
| `06-resultados/revisao-2026-10-17/bootstrap_nadir.py` | `bootstrap_visdrone.py` | `--tag`; pares da seção 3.3; 1.000 reamostras, semente 0 |
| `06-resultados/escala_nadir.py` | `escala_casada.py` | `--data`, `--alvo 20.55`; só rótulos e tamanhos de imagem |
| `07-blender/scripts/prepara_heridal.py` | novo | VOC para YOLO, classe única; contagens de imagens e caixas; roda com `-I`, fora da pasta baixada |

### 4.2 Scripts a modificar (compatíveis para trás: o padrão é o comportamento de hoje)

- `train_yolo_win.py`: flags `--freeze` (padrão nenhum), `--optimizer` (padrão `auto`), `--lr0`,
  `--momentum`, `--warmup-bias-lr` (padrão os do Ultralytics), `--patience` (padrão 15) e `--dry-run`
  (imprime os argumentos de `train()` e sai, para conferir sem GPU que, sem flags novas, os argumentos
  são os do `args.yaml` do `ft05_coco`).
- `06-resultados/por_regime.py`: `--por-quadro` grava acertos e caixas por quadro e regime.
- `revisao-2026-10-17/visdrone_preds.py`: os runs novos entram em `MODELOS` (só acréscimo; os `.npz`
  existentes são pulados).
- `revisao-2026-10-17/bootstrap_visdrone.py` e `resolvivel.py`: `--sufixo` para gravar saídas novas sem
  sobrescrever as de 17/10, que o artigo cita; pares novos.

## 5. Cronograma previsto (partida 19/10 às 00:00, sem pausas)

| Grupo | Horas | Fim, limite inferior | Fim, limite superior |
|---|---|---|---|
| P | 0,1 | 19/10 00:06 | 19/10 00:06 |
| S (R5-1) | 14 a 15,5 | 19/10 14:06 | 19/10 15:36 |
| F (R5-5) | 17 a 21,5 | 20/10 07:06 | 20/10 13:06 |
| N (R5-6) | 2 | 20/10 09:06 | 20/10 15:06 |
| Y1 | 0,2 | 20/10 09:20 | 20/10 15:20 |
| A (R5-3) | 11 a 14,5 | 20/10 20:20 | 21/10 05:50 |
| D (R5-4) | 13,5 a 15,5 | 21/10 09:50 | 21/10 21:20 |
| M (R5-7) | 8 a 40 | 21/10 17:50 | 23/10 13:20 |
| C (R5-2) | 25,5 a 27 | 22/10 19:20 | 24/10 16:20 |
| Y2 | 2,5 | 22/10 21:50 | 24/10 18:50 |

Se o download da base nadir não estiver pronto quando F terminar, N fica `aguardando_dado` e o resto
do cronograma anda 2 h mais cedo.

## 6. Checklist da partida à meia-noite

Cada item com o estado conferido em 18/10, quando se conferiu.

1. **Repositório.** `git pull --rebase`; este plano e os scripts da seção 4 criados, revisados e
   versionados (commit e push) antes da partida; anotar o hash do commit no DIARIO, como na rodada 4.
2. **Disco.** Pelo menos 60 GB livres em C:. Em 18/10: 413 GB livres de 931. A rodada ocupa cerca de
   20 a 25 GB (estimativa: 180 quadros 4K ocupam 2,4 a 2,7 GB e seus ladrilhos 0,5 a 0,6 GB; até 1.020
   quadros novos; runs de cerca de 45 MB), mais 5 a 10 GB da HERIDAL.
3. **GPU livre.** `nvidia-smi` com memória em uso abaixo de 1 GB e utilização perto de 0%. Em 18/10, à
   tarde: 2,4 GB em uso e 34% de utilização, com League of Legends, Riot Client, Wallpaper Engine,
   Discord e o app do Xbox abertos: fechar todos. Conferir que o Ollama (na pasta Inicializar) não tem
   modelo carregado.
4. **Nada de rodada anterior vivo.** Nenhum `supervisiona_rodada3/4.py` nem `rodada3/4.py` rodando;
   `fila5\PAUSA` ausente. Pasta Inicializar em 18/10: só `Hermes_Gateway.vbs`, `Ollama.lnk` e
   `desktop.ini` (o atalho da rodada 4 já se apagou).
5. **venv.** `PY -c "import ultralytics, torch; print(ultralytics.__version__, torch.__version__, torch.cuda.is_available())"`
   deve dar 8.4.148, 2.14 e True.
6. **Caminhos.** Conferidos em 18/10: `BL`, `PY`, `VIS`, `FT\ft05.yaml` (val = `sel/images`),
   `FT\ft10.yaml`, `RAIZ\yolo11s.pt`, `RAIZ\ds_morro_4k_tiles`, `RAIZ\ds_morro_obl_tiles`,
   `RAIZ\ds_oblvar` e `_tiles`, `RAIZ\ds_regime_4k` e `_tiles`, `RAIZ\ds_armado_150g` e `_tiles`.
   Conferir também os `best.pt` de `s_nadir_4k`, `s_variedade`, `s_obliquo`, `s_oblvar`,
   `s_oblvar_sd1`, `s_oblvar_sd2`, `r_pareado`, `armado_150g`, `ft05_*` e `ft10_*`.
7. **Nomes livres.** `python rodada5.py --listar` mostra tudo pendente; nenhuma pasta
   `runs\detect\<run novo>` existe (senão o treino "retoma" um run alheio).
8. **Wrapper.** `train_yolo_win.py --dry-run` sem flags novas reproduz os argumentos do `ft05_coco`; com
   `OPT --lr0 0.0002 --freeze 11`, mostra `optimizer=AdamW`, `lr0=0.0002`, `momentum=0.9`,
   `warmup_bias_lr=0.0`, `freeze=11`.
9. **Download.** O autor decide se autoriza a HERIDAL (ou outra base da seção 3.3), confere a licença e
   faz o download e a conversão antes de o grupo N começar (cerca de 31 h depois da partida). Sem isso,
   N espera.
10. **Energia e reinício.** O PC não pode suspender. Se o Windows reiniciar, o atalho só relança a
    cadeia depois do login do usuário; o autor decide sobre as horas ativas do Windows Update.
11. **Partida.** O autor dá duplo clique em `retoma_rodada5.cmd` (ou o atalho na pasta Inicializar,
    criado com o seu OK), não pela sessão do Claude nem pelo Agendador. O grupo P confere o MPFB nos
    primeiros minutos; ver `fila5\P2_*.log` antes de ir dormir.
12. **Acompanhamento.** Fio de e-mail novo com este plano e a previsão de término; checagem horária com
    `status_rodada5.py`; pausa só por `pausa_rodada5.py`.

## 7. O que não está na rodada

- Sementes de treino para os pontos intermediários da curva (60 e 90 quadros), para a ablação de sol
  duro, para o modelo de 150 m e para as réplicas de cena.
- O espelho "todos menos sol duro" da ablação (mais 15,5 h).
- A curva de aprendizado sobre o corpus nadir e a separação das duas causas do piloto.
- Os cronogramas novos para o treino conjunto (F-joint) e um orçamento de ajuste fino maior que 30
  épocas.
- Mais de uma base real nadir, salvo se o autor autorizar outra além da HERIDAL.
