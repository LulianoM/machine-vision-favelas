#!/usr/bin/env python3
"""
train_yolo_win.py: treina e avalia um detector YOLO (Ultralytics) nos datasets gerados no Blender.

Igual ao train_yolo.py do pacote original, com duas diferencas necessarias no Windows:
  1. tudo dentro de `if __name__ == "__main__"`. Sem isso, o DataLoader com workers > 0 usa
     multiprocessing por spawn, reimporta o modulo e dispara o treino de novo em cada worker,
     o que trava o processo (foi exatamente o que aconteceu no primeiro lote).
  2. defaults ajustados para objeto pequeno em imagem aerea.

Exemplos:
  python train_yolo_win.py --data dataset_v3/data.yaml --name blender_v3
  python train_yolo_win.py --eval-only --weights runs/detect/blender_v3/weights/best.pt --real visdrone_yolo/data.yaml --single-cls

Flags da rodada 5 (18/10/2026), todas opcionais: sem elas os argumentos de train() sao exatamente os
de antes (cada uma so entra em train() quando e passada). --freeze, --optimizer, --lr0, --momentum e
--warmup-bias-lr servem ao ajuste fino com extrator congelado e taxa menor (R5-5): com optimizer=auto
o Ultralytics ignora lr0 e momentum, entao a taxa menor so vale com o otimizador explicito.
--patience muda a paciencia (padrao 15, a de todos os treinos). --dry-run imprime os argumentos de
train() e sai sem carregar modelo nem GPU; com --compara <args.yaml> lista tambem as chaves em que a
configuracao efetiva difere desse args.yaml (por exemplo o do ft05_coco).
"""
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="dataset_v3/data.yaml")
    ap.add_argument("--model", default="yolo11n.pt")
    ap.add_argument("--weights", default=None)
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--imgsz", type=int, default=1536)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--name", default="blender")
    ap.add_argument("--single-cls", action="store_true")
    ap.add_argument("--eval-only", action="store_true")
    ap.add_argument("--real", default=None, help="data.yaml de um dataset real para medir sim-to-real")
    ap.add_argument("--seed", type=int, default=0,
                    help="semente de treino do Ultralytics (0 e o padrao, usado em todos os treinos ate a rodada 3; a rodada 4 repete modelos com 1 e 2 para medir a dispersao entre treinos)")
    ap.add_argument("--freeze", type=int, default=None, help="camadas congeladas (0 a N-1); padrao: nenhuma")
    ap.add_argument("--optimizer", default=None, help="padrao: nao passa (auto do Ultralytics)")
    ap.add_argument("--lr0", type=float, default=None, help="padrao: o do Ultralytics")
    ap.add_argument("--momentum", type=float, default=None, help="padrao: o do Ultralytics")
    ap.add_argument("--warmup-bias-lr", type=float, default=None, help="padrao: o do Ultralytics")
    ap.add_argument("--patience", type=int, default=15)
    ap.add_argument("--dry-run", action="store_true", help="imprime os argumentos de train() e sai")
    ap.add_argument("--compara", default=None, help="com --dry-run: args.yaml de um treino antigo para comparar")
    args = ap.parse_args()

    kw = dict(data=args.data, epochs=args.epochs, imgsz=args.imgsz, batch=args.batch,
              workers=args.workers, name=args.name, single_cls=args.single_cls, exist_ok=True,
              hsv_h=0.015, hsv_s=0.6, hsv_v=0.4, degrees=10, scale=0.4, fliplr=0.5, mosaic=1.0,
              patience=args.patience, plots=True, seed=args.seed, deterministic=True)
    for chave in ("freeze", "optimizer", "lr0", "momentum", "warmup_bias_lr"):
        if getattr(args, chave) is not None:
            kw[chave] = getattr(args, chave)

    if args.dry_run:
        print("modelo:", args.weights or args.model)
        print("train(**" + json.dumps(kw, ensure_ascii=False, sort_keys=True) + ")")
        if args.compara:
            import yaml
            from ultralytics.cfg import get_cfg
            ef = vars(get_cfg(overrides=dict(kw, model=args.weights or args.model, mode="train", task="detect")))
            antigo = yaml.safe_load(open(args.compara, encoding="utf-8"))
            ignora = {"save_dir"}
            dif = {k: (antigo.get(k), ef.get(k)) for k in sorted(set(antigo) | set(ef))
                   if k not in ignora and str(antigo.get(k)) != str(ef.get(k))}
            print(f"diferencas para {args.compara} (antigo, agora):", json.dumps(dif, ensure_ascii=False, default=str))
        return

    from ultralytics import YOLO

    def resumo(m):
        r = m.results_dict if hasattr(m, "results_dict") else {}
        return {k: round(float(v), 4) for k, v in r.items()}

    modelo = YOLO(args.weights or args.model)
    saida = {}
    if not args.eval_only:
        modelo.train(**kw)
        best = Path(modelo.trainer.save_dir) / "weights" / "best.pt"
        modelo = YOLO(best)
        saida["pesos"] = str(best)
        saida["val_sintetico"] = resumo(modelo.val(data=args.data, imgsz=args.imgsz,
                                                  single_cls=args.single_cls, name=args.name + "_val", exist_ok=True))
    if args.real:
        saida["val_real"] = resumo(modelo.val(data=args.real, imgsz=args.imgsz,
                                              single_cls=args.single_cls, name=args.name + "_real", exist_ok=True))
    print(json.dumps(saida, indent=2, ensure_ascii=False))
    Path("resultados").mkdir(exist_ok=True)
    with open(Path("resultados") / f"{args.name}.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
