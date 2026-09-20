#!/usr/bin/env python3
"""
avalia_sim2real.py: mede os números de sim-to-real de um detector treinado só em sintético.

Roda TRÊS avaliações com o mesmo peso, e a terceira é a que o projeto acrescenta à prática usual:

  1. `sintetico`   validação no próprio conjunto sintético. É o modelo se avaliando no mundo em
                   que nasceu. Serve de teto, não de evidência.
  2. `real`        zero-shot no VisDrone-DET como ele é. É o número que a literatura reporta.
  3. `real_gsd`    zero-shot no VisDrone reescalado para casar a distância de amostragem no solo.

Por que a terceira existe: medido em 2026-09-20, o alvo mediano do VisDrone tem 25 px e o do
nosso sintético tem 10 px, ou seja 2,49 vezes. Testar direto mistura DOIS domain shifts, o de
sintético para real e o de 150 m para dezenas de metros, e o resultado não diz qual dos dois
causou o quê. Reescalar o real por 1/2,49 iguala a escala do alvo e isola o primeiro.

O rótulo YOLO é normalizado, então reescalar a imagem não altera o rótulo.

O modelo tem duas classes (`pessoa_armada`, `pessoa_desarmada`) e o VisDrone tem uma (`pessoa`),
então as avaliações em real usam `single_cls`, que funde as duas na hora de comparar.

Uso:
  python avalia_sim2real.py --weights runs/detect/morro_clima_s/weights/best.pt \
      --sintetico ds_morro_clima_tiles/data.yaml \
      --real C:/arma3-favela/visdrone/visdrone_yolo/data.yaml \
      --real-gsd C:/arma3-favela/visdrone/visdrone_yolo_gsd/data.yaml \
      --out 06-resultados/sim2real_morro.json
"""
import argparse
import json
import os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--sintetico", default=None)
    ap.add_argument("--real", default=None)
    ap.add_argument("--real-gsd", default=None)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--conf", type=float, default=0.001)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    from ultralytics import YOLO
    m = YOLO(args.weights)

    def roda(nome, data, single):
        if not data:
            return None
        r = m.val(data=data, imgsz=args.imgsz, conf=args.conf, single_cls=single,
                  split="val", verbose=False, plots=False)
        d = {k: round(float(v), 4) for k, v in (r.results_dict or {}).items()}
        d["conjunto"] = nome
        d["data"] = data
        d["single_cls"] = single
        return d

    res = [x for x in (roda("sintetico", args.sintetico, False),
                       roda("real", args.real, True),
                       roda("real_gsd", args.real_gsd, True)) if x]

    ch = ["metrics/precision(B)", "metrics/recall(B)", "metrics/mAP50(B)", "metrics/mAP50-95(B)"]
    print(f"\n{'conjunto':<12}{'P':>9}{'R':>9}{'mAP50':>9}{'mAP50-95':>11}")
    print("-" * 50)
    for d in res:
        print(f"{d['conjunto']:<12}" + "".join(f"{d.get(k, float('nan')):>9.4f}" if k != ch[-1]
                                               else f"{d.get(k, float('nan')):>11.4f}" for k in ch))
    print("\nO numero de 'sintetico' e teto, nao evidencia: o modelo esta sendo avaliado no")
    print("mesmo mundo em que foi treinado. Os dois de baixo sao os que valem para o artigo.")

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        json.dump(dict(weights=os.path.abspath(args.weights), imgsz=args.imgsz,
                       conf=args.conf, resultados=res),
                  open(args.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print(f"\ngravado {args.out}")


if __name__ == "__main__":
    main()
