#!/usr/bin/env python3
"""
Treina e avalia um detector YOLO (Ultralytics) no dataset sintético do ARMA 3
e, opcionalmente, mede sim-to-real num dataset real no formato YOLO.

Exemplos:
  # 1) treino sintético, 2 classes
  python train_yolo.py --data dataset_arma3/data.yaml --model yolo11n.pt --epochs 50 --imgsz 1280

  # 2) treino sintético em classe única (pessoa) para comparar com VisDrone
  python train_yolo.py --data dataset_arma3/data.yaml --single-cls --name arma3_single

  # 3) avaliação zero-shot em dado real (classe única) com pesos já treinados
  python train_yolo.py --eval-only --weights runs/detect/arma3_single/weights/best.pt --real visdrone_yolo/data.yaml --single-cls

  # 4) fine-tuning com fração pequena do real (few-shot), depois avaliação
  python train_yolo.py --weights runs/detect/arma3_single/weights/best.pt --data visdrone_yolo_5pct/data.yaml \
                       --single-cls --epochs 20 --name finetune_5pct --real visdrone_yolo/data.yaml
"""
import argparse, json
from pathlib import Path
from ultralytics import YOLO


def resumo(m):
    r = m.results_dict if hasattr(m, "results_dict") else {}
    return {k: round(float(v), 4) for k, v in r.items()}


ap = argparse.ArgumentParser()
ap.add_argument("--data", default="dataset_arma3/data.yaml")
ap.add_argument("--model", default="yolo11n.pt", help="modelo base (yolo11n.pt, yolov8s.pt, ...)")
ap.add_argument("--weights", default=None, help="pesos já treinados (substitui --model)")
ap.add_argument("--epochs", type=int, default=50)
ap.add_argument("--imgsz", type=int, default=1280)
ap.add_argument("--batch", type=int, default=-1, help="-1 = auto")
ap.add_argument("--name", default="arma3")
ap.add_argument("--single-cls", action="store_true", help="colapsa todas as classes em 'pessoa'")
ap.add_argument("--eval-only", action="store_true")
ap.add_argument("--real", default=None, help="data.yaml de um dataset real (ex.: VisDrone convertido) para avaliar")
args = ap.parse_args()

modelo = YOLO(args.weights or args.model)
saida = {}

if not args.eval_only:
    modelo.train(data=args.data, epochs=args.epochs, imgsz=args.imgsz, batch=args.batch,
                 name=args.name, single_cls=args.single_cls, exist_ok=True,
                 # augmentações moderadas; a randomização principal já veio do ARMA
                 hsv_h=0.015, hsv_s=0.6, hsv_v=0.4, degrees=10, scale=0.4, fliplr=0.5, mosaic=1.0)
    best = Path(modelo.trainer.save_dir) / "weights" / "best.pt"
    modelo = YOLO(best)
    saida["pesos"] = str(best)
    saida["val_sintetico"] = resumo(modelo.val(data=args.data, imgsz=args.imgsz, single_cls=args.single_cls, name=args.name + "_val", exist_ok=True))

if args.real:
    saida["val_real"] = resumo(modelo.val(data=args.real, imgsz=args.imgsz, single_cls=args.single_cls, name=args.name + "_real", exist_ok=True))

print(json.dumps(saida, indent=2, ensure_ascii=False))
Path("resultados").mkdir(exist_ok=True)
with open(Path("resultados") / f"{args.name}.json", "w") as f:
    json.dump(saida, f, indent=2, ensure_ascii=False)
