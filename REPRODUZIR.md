# Como reproduzir

Guia para quem quer validar o trabalho de fora: baixar os modelos e rodar o próprio benchmark, ou refazer a cadeia inteira (cena sintética no Blender, anotação automática, ladrilhamento, treino YOLO e teste em imagem aérea real).

Os números do artigo e o comando que gerou cada um estão em [`06-resultados/RESULTADOS.md`](06-resultados/RESULTADOS.md). Este arquivo diz como chegar neles.

## 1. O que está publicado e onde

| O quê | Onde | Observação |
|---|---|---|
| Código | este repositório, [`03-blender/scripts/`](03-blender/scripts/) | gerador de cena, anotação, ladrilhamento, treino, avaliação |
| Pesos de todos os runs | release [`modelos-v1`](https://github.com/LulianoM/machine-vision-favelas/releases/tag/modelos-v1) | um arquivo por peso, nome `<run>__best.pt` e `<run>__last.pt` |
| Corpora sintéticos (formato YOLO) | release [`corpora-v1`](https://github.com/LulianoM/machine-vision-favelas/releases/tag/corpora-v1) | um `.tar` por corpus, sem compressão; acima de 1,9 GiB sai em partes |
| Runs sem os pesos, cenas `.blend` procedurais, assets CC0 | release [`extras-v1`](https://github.com/LulianoM/machine-vision-favelas/releases/tag/extras-v1) | `results.csv`, `args.yaml` e gráficos de cada treino |
| SHA256 de cada arquivo publicado | [`06-resultados/releases-manifesto.jsonl`](06-resultados/releases-manifesto.jsonl) | gerado pelo próprio script de envio |
| Inventário com tamanho, data e SHA256 dos corpora e pesos | [`06-resultados/ONDE-ESTAO-OS-DADOS.md`](06-resultados/ONDE-ESTAO-OS-DADOS.md) | |

Remontar um corpus cortado em partes:

```bash
cat ds_morro_4k.tar.part* > ds_morro_4k.tar && tar xf ds_morro_4k.tar
```

O envio foi feito por [`03-blender/scripts/publica_releases.py`](03-blender/scripts/publica_releases.py). Se alguma peça não estiver na release, ainda está subindo, ou foi para o Google Drive com link em [`06-resultados/RELEASES.md`](06-resultados/RELEASES.md).

### O que não está publicado, e por quê

- **Dado operacional da PCERJ** (fotos do voo de 2022 sobre o Jacarezinho e Manguinhos, os ortomosaicos e tudo que carrega a imagem ou a geometria deles): malhas e DSM do OpenDroneMap, cenas `jacarezinho.blend` e `quadra.blend`, datasets `dataset_odm*` e `dataset_cid150*`, testes `teste_angulos` e `teste_denso`, mosaicos de treino desses runs e logs com coordenada. Os pesos `blender_odm_tiles` e `cid150_s` estão publicados, mas as imagens que os treinaram não.
- **VisDrone e HERIDAL**: são bases públicas com licença própria. Baixe da fonte (seção 4). Dos corpora mistos `ds_misto05` e `ds_misto10` vão só rótulos e `composicao.json`; as imagens se remontam com o VisDrone e `ds_oblvar_tiles`.

Os resultados do artigo vêm do braço procedural (`gen_morro.py`, Poly Haven CC0), que está publicado inteiro.

## 2. Ambiente

Testado num Windows 10 com RTX 2060 de 6 GB e 32 GB de RAM (detalhes em [`docs/AMBIENTE-DESKTOP.md`](docs/AMBIENTE-DESKTOP.md)). Nada é específico de Windows, além dos caminhos `C:\arma3-favela\...` hardcoded em alguns scripts de fila. O nome da pasta vem de 2022, quando o plano era o ARMA 3. Ajuste os caminhos para os seus.

| Item | Versão usada |
|---|---|
| Blender | 5.2.1 LTS |
| Extensão MPFB (MakeHuman para Blender) | 2.0.17 |
| Python | 3.11 |
| PyTorch | 2.14.0 + CUDA 12.6 |
| Ultralytics | 8.4.148 |
| Outros | numpy, opencv-python, pyyaml, pillow, tqdm, rasterio (só para o braço ODM) |

```bash
python -m venv venv
venv/Scripts/pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
venv/Scripts/pip install "ultralytics==8.4.148" numpy opencv-python pyyaml pillow tqdm
```

Assets da cena (todos CC0, também na release `extras-v1`): texturas, HDRIs e modelos do Poly Haven (baixador `fetch_ph.py`, índice `index.json`), Human Base Meshes v1.1.0 da Blender Studio e MPFB instalada como extensão do Blender.

## 3. Caminho curto: testar os modelos publicados

O run de referência do artigo é `s_nadir_4k` (corpus `ds_morro_4k`, câmera nadir a 150 m). A tabela que liga cada run e corpus ao nome usado no artigo está em [`06-resultados/revisao-2026-10-17/checkpoints.md`](06-resultados/revisao-2026-10-17/checkpoints.md) e [`corpora.md`](06-resultados/revisao-2026-10-17/corpora.md).

```bash
# baixa o peso de referência e os ladrilhos do corpus
gh release download modelos-v1 -R LulianoM/machine-vision-favelas -p "s_nadir_4k__best.pt"
gh release download corpora-v1 -R LulianoM/machine-vision-favelas -p "ds_morro_4k_tiles.tar*"

# validação no próprio sintético (teto, não evidência)
yolo val model=s_nadir_4k__best.pt data=ds_morro_4k_tiles/data.yaml imgsz=1280 single_cls=True
```

O `data.yaml` de cada corpus tem `path:` absoluto do desktop. Troque pela pasta onde extraiu.

Para o seu benchmark em imagem real, o protocolo do artigo é zero-shot com `single_cls` (o modelo tem duas classes, `pessoa_armada` e `pessoa_desarmada`; as bases reais têm uma, `pessoa`), `imgsz` 1280:

```bash
python 03-blender/scripts/avalia_sim2real.py --weights s_nadir_4k__best.pt \
    --sintetico ds_morro_4k_tiles/data.yaml \
    --real <visdrone_yolo>/data.yaml --real-gsd <visdrone_yolo_gsd>/data.yaml \
    --out sim2real_s_nadir_4k.json
```

Teste por imagem com intervalo de confiança: `06-resultados/revisao-2026-10-17/bootstrap_visdrone.py` e `bootstrap_nadir.py` (1.000 reamostras pareadas por imagem, semente 0).

## 4. Bases reais

| Base | Fonte | Preparo |
|---|---|---|
| VisDrone2019-DET (treino e val) | <https://github.com/VisDrone/VisDrone-Dataset> (task 1, object detection in images) | `visdrone_to_yolo.py` (em `02-projeto-ufrj-2022/arma3-2022/scripts/`), depois `03-blender/scripts/prepara_ft.py` para as fatias `sel`, `ft05` e `ft10` (semente 2609) |
| HERIDAL (busca e resgate, nadir) | <https://zenodo.org/records/5662351>, `heridal_keras_retinanet_voc.zip`, CC BY 3.0 | `python -I 03-blender/scripts/prepara_heridal.py --bruto <pasta do zip>` |

## 5. Caminho longo: refazer tudo

Ordem da cadeia, com os comandos de verdade em [`03-blender/scripts/fila_noite.py`](03-blender/scripts/fila_noite.py) e nos `rodada*.py`:

1. **Gerar o corpus** no Blender, headless, com semente fixa. A anotação sai exata: projeção dos vértices deformados do corpo e da arma, mais ray cast de oclusão (14 pontos, visibilidade mínima de 0,35):

   ```bash
   blender -b --python-exit-code 1 --python 03-blender/scripts/gen_morro.py -- \
       --out ds_morro_4k --dataset 180 --samples 96 --res 3840 2160 \
       --people 16 34 --pool 6 --seed 21 --climas todos
   ```

   `--help` lista todas as opções (câmera oblíqua, altitude, armas inéditas, objetos confundíveis, sítio). O `manifest.jsonl` de cada corpus publicado guarda, por quadro, altitude, regime de tempo, sol, névoa, exposição e visibilidade de cada caixa.

2. **Ladrilhar** em escala nativa. É o passo que mais pesa: reduzir o 4K inteiro joga a pessoa abaixo do menor stride do YOLO.

   ```bash
   python 03-blender/scripts/tile_dataset.py --data ds_morro_4k --out ds_morro_4k_tiles --tile 1280 --overlap 0.2
   ```

3. **Treinar.** A receita comum do artigo é yolo11s, 60 épocas, batch 6, imgsz 1280, paciência 15, semente 0 e classe única. O `args.yaml` de cada run na release `extras-v1` tem a configuração efetiva completa.

   ```bash
   python 03-blender/scripts/train_yolo_win.py --data ds_morro_4k_tiles/data.yaml --model yolo11s.pt \
       --epochs 60 --batch 6 --imgsz 1280 --workers 4 --single-cls --name s_nadir_4k
   ```

4. **Avaliar** como na seção 3, e rodar os critérios de cada rodada (`06-resultados/rodada4_criterios.py`, `rodada5_criterios.py`, `rodada6_criterios.py`).

Limite honesto da regeneração: o render é determinístico pela semente, mas o gerador mudou entre rodadas. Os corpora mais antigos (`ds_morro_clima`, `ds_morro_4k`) usaram a biblioteca de armas antiga de `people_mpfb.py` e o filtro de enquadramento quadrado, e versões diferentes do Blender ou do driver mudam o ruído do Cycles. Para conferir os números do artigo, use os corpora publicados. Regenerar serve para validar o método, não para bater pixel a pixel.

## 6. Histórico

O plano de 2022 (Fábio H. P. Guimarães, com orientação do prof. Claudio Miceli de Farias) era gerar os dados no ARMA 3. A tentativa de 11/09/2026 não gerou nenhuma imagem e foi abandonada na mesma noite, em favor do Blender. Esse material fica em [`02-projeto-ufrj-2022/arma3-2022/`](02-projeto-ufrj-2022/arma3-2022/), só como registro.
