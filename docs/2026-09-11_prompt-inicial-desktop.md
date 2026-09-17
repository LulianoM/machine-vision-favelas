# Prompt de partida para o Claude Code na outra máquina

Copie e cole no Claude Code aberto dentro da pasta descompactada:

---

Você está numa máquina nova, sem contexto. Este diretório é um pacote de contexto de um projeto de pesquisa acadêmica (artigo "Machine Vision from the Global South: Developing an AI Model for Vertical Favelas", FGV EBAPE). Faça o seguinte, nesta ordem:

1. Leia `00-LEIA-PRIMEIRO.md` por completo e depois `03-arma3/README-PIPELINE.md`. Leia `01-artigo/resumo-artigo-v2.md` para entender a metodologia que estamos testando (Seção 7 do artigo: dados sintéticos com domain randomization, treino de detector, fine-tuning e teste em imagem real).

2. Verifique o ambiente: Windows, ARMA 3 instalado via Steam (me diga o caminho), GPU disponível (`nvidia-smi`), Python 3.10+. Crie um venv e instale `03-arma3/scripts/requirements.txt`.

3. Prepare a missão no ARMA 3 conforme o README: crie a missão no editor Eden, coloque `capturaDataset.sqf` na pasta da missão e chame-o pelo `init.sqf`. Me guie passo a passo no que precisa ser feito dentro do jogo (eu opero o jogo, você opera o terminal).

4. Depois que o ARMA gerar as screenshots e o arquivo `.rpt` com as linhas `DSIMG` e `DSLBL`, rode `rpt_to_yolo.py`, depois `preview_boxes.py` em 10 imagens e me mostre. Se as caixas estiverem deslocadas, ajuste a normalização de safeZone conforme o README antes de treinar.

5. Treine com `train_yolo.py` (comece com yolo11n ou yolov8n, 50 épocas, imgsz 1280) e reporte mAP50 e mAP50-95 no conjunto de validação sintético.

6. Baixe o VisDrone-DET (val) e avalie o modelo sintético na classe pedestrian/people para ter um número de sim-to-real zero-shot. Depois faça fine-tuning com uma fração pequena (5% a 10%) do train do VisDrone e reavalie. Esses dois números (zero-shot e few-shot) são o resultado que vai para o artigo.

7. Registre tudo em `RESULTADOS.md` na raiz: comandos, hiperparâmetros, tabelas de métricas, caminhos dos pesos, o que deu errado. Escreva em português, sem travessão.

Regras: não invente números; se algo falhar, mostre o erro. Não baixe nem redistribua os ortomosaicos do Jacarezinho (dados sensíveis da PCERJ). Pergunte antes de qualquer ação destrutiva.
