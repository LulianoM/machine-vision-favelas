#!/usr/bin/env python3
"""
visdrone_preds.py: roda o validador do Ultralytics no VisDrone-DET val (548 imagens) uma vez por modelo,
com o protocolo de todos os numeros do artigo (classe unica, imgsz 1280, conf 0,001, NMS IoU 0,7,
max_det 300), e GUARDA por imagem o que o validador usa para o mAP: a bandeira de acerto de cada
predicao nos 10 limiares de IoU (0,50 a 0,95), a confianca, e o numero de caixas verdadeiras.
Com isso o mAP50 pode ser recalculado para qualquer subconjunto de imagens (reamostragem) com
ultralytics.utils.metrics.ap_per_class, sem rodar a rede de novo.

Revisao de 17/10/2026 (agente D2, pontos S1, S6 e A3 do feedback de 14/10). So inferencia.

Para cada modelo grava preds_visdrone_<run>.npz (names, n_gt, img_idx, conf, tp, pred_cls) e
acrescenta a visdrone_reproducao.json o mAP50 do validador, o mAP50 recalculado dos dados
guardados e o valor reportado em 06-resultados (sim2real_<run>.json), com a diferenca.

  C:/arma3-favela/venv/Scripts/python.exe visdrone_preds.py --modelos r_pareado --batch 4 --fp16
  C:/arma3-favela/venv/Scripts/python.exe visdrone_preds.py --todos --batch 4 --fp16

Rodada 5 (18/10/2026): os runs novos entram em MODELOS_R5, so por acrescimo. MODELOS_1710 guarda os 17
de 17/10, que o bootstrap sem --sufixo continua usando (as saidas de 17/10, citadas no artigo, saem
iguais). Os .npz que ja existem sao pulados. Com --todos, um run novo ainda sem pesos e ignorado em
silencio (nao entra como "faltando" no visdrone_reproducao.json).
"""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(AQUI)                                   # 06-resultados
RAIZ = os.path.join("C:" + os.sep, "arma3-favela")
DETECT = os.path.join(RAIZ, "blender", "runs", "detect")
VIS_YAML = os.path.join(RAIZ, "visdrone", "visdrone_yolo", "data.yaml")

# nome no artigo -> run (um so lugar; os outros scripts importam daqui)
MODELOS_1710 = {
    "R": "r_pareado",
    "S-nadir-150": "s_nadir_4k",
    "S-nadir-150-six": "s_variedade",
    "S-oblique": "s_obliquo",
    "S-oblique-six s0": "s_oblvar",
    "S-oblique-six s1": "s_oblvar_sd1",
    "S-oblique-six s2": "s_oblvar_sd2",
    "F-synthetic 5% s0": "ft05_sint",
    "F-synthetic 5% s1": "ft05_sint_sd1",
    "F-synthetic 5% s2": "ft05_sint_sd2",
    "F-synthetic 10%": "ft10_sint",
    "F-generic 5% s0": "ft05_coco",
    "F-generic 5% s1": "ft05_coco_sd1",
    "F-generic 5% s2": "ft05_coco_sd2",
    "F-generic 10%": "ft10_coco",
    "F-joint 5%": "misto05",
    "F-joint 10%": "misto10",
}

# rodada 5 (03-blender/PLANO-RODADA5.md): R5-1 sementes, R5-5 cronogramas, R5-3 curva, R5-4 sol duro, R5-2 cena
MODELOS_R5 = {
    "S-nadir-150 s1": "s_nadir_4k_sd1",
    "S-nadir-150 s2": "s_nadir_4k_sd2",
    "S-oblique s1": "s_obliquo_sd1",
    "S-oblique s2": "s_obliquo_sd2",
    "F-generic 5% rep": "ft05_coco_rep",
    "F-synthetic 5% rep": "ft05_sint_rep",
    "F-generic 10% rep": "ft10_coco_rep",
    "F-synthetic 10% rep": "ft10_sint_rep",
}
for _f in ("05", "10"):
    for _cel in ("fz", "lr", "fzlr"):
        for _ini, _art in (("sint", "F-synthetic"), ("coco", "F-generic")):
            MODELOS_R5[f"{_art} {int(_f)}% {_cel}"] = f"ft{_f}_{_ini}_{_cel}"
            if _f == "05":
                for _s in (1, 2):
                    MODELOS_R5[f"{_art} 5% {_cel} s{_s}"] = f"ft05_{_ini}_{_cel}_sd{_s}"
for _n in ("030", "060", "090", "120"):
    MODELOS_R5[f"S-oblique-six c{_n} s0"] = f"s_oblvar_c{_n}"
    if _n in ("030", "120"):
        for _s in (1, 2):
            MODELOS_R5[f"S-oblique-six c{_n} s{_s}"] = f"s_oblvar_c{_n}_sd{_s}"
MODELOS_R5["S-nadir-150 hard-sun"] = "s_soldur_4k"
MODELOS_R5["S-oblique-six scene 22"] = "s_oblvar_e22"
MODELOS_R5["S-oblique-six scene 23"] = "s_oblvar_e23"

MODELOS = {**MODELOS_1710, **MODELOS_R5}


def reportado(run):
    """mAP50 no VisDrone val reportado em 06-resultados/sim2real_<run>.json (conjunto 'real')"""
    p = os.path.join(RES, f"sim2real_{run}.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    return next((r["metrics/mAP50(B)"] for r in d["resultados"] if r.get("conjunto") == "real"), None)


def validador_que_guarda():
    from ultralytics.models.yolo.detect import DetectionValidator

    class ValidadorGuarda(DetectionValidator):
        """o validador padrao, que alem de acumular as estatisticas as guarda por imagem"""

        def init_metrics(self, model):
            super().init_metrics(model)
            self.guarda = []

        def update_metrics(self, preds, batch):
            for si, pred in enumerate(preds):
                self.seen += 1
                pbatch = self._prepare_batch(si, batch)
                cls = pbatch["cls"].cpu().numpy()
                predn = self._prepare_pred(pred)
                sem = predn["cls"].shape[0] == 0
                stat = {
                    **self._process_batch(predn, pbatch),
                    "target_cls": cls,
                    "target_img": np.unique(cls),
                    "conf": np.zeros(0) if sem else predn["conf"].cpu().numpy(),
                    "pred_cls": np.zeros(0) if sem else predn["cls"].cpu().numpy(),
                    "im_name": Path(pbatch["im_file"]).name,
                }
                self.metrics.update_stats(stat)
                self.guarda.append((stat["im_name"], np.asarray(stat["tp"], dtype=bool),
                                    np.asarray(stat["conf"], dtype=np.float32),
                                    np.asarray(stat["pred_cls"], dtype=np.int16), cls.astype(np.int16)))

        def finalize_metrics(self):
            super().finalize_metrics()
            self.metrics.guarda = self.guarda      # o objeto que model.val() devolve

    return ValidadorGuarda


def recalcula_map50(tp, conf, pred_cls, target_cls):
    from ultralytics.utils.metrics import ap_per_class
    r = ap_per_class(tp, conf, pred_cls, target_cls)
    ap = r[5]                                  # (classes, limiares de IoU)
    return float(ap[:, 0].mean()), float(ap.mean())


def roda(run, batch, fp16, imgsz, refaz):
    from ultralytics import YOLO
    saida_npz = os.path.join(AQUI, f"preds_visdrone_{run}.npz")
    if os.path.exists(saida_npz) and not refaz:
        print(f"{run}: ja guardado em {os.path.basename(saida_npz)}")
        return None
    pesos = os.path.join(DETECT, run, "weights", "best.pt")
    if not os.path.exists(pesos):
        print(f"{run}: SEM PESOS em {pesos}")
        return {"run": run, "pesos": pesos, "faltando": True}
    kw = dict(data=VIS_YAML, imgsz=imgsz, conf=0.001, iou=0.7, max_det=300, single_cls=True, split="val",
              batch=batch, plots=False, verbose=False, validator=validador_que_guarda())
    if fp16:
        kw["quantize"] = 16
    r = YOLO(pesos).val(**kw)
    map50_val = float(r.box.map50)
    g = r.guarda
    nomes = np.array([x[0] for x in g])
    n_gt = np.array([len(x[4]) for x in g], dtype=np.int32)
    n_pred = np.array([len(x[2]) for x in g], dtype=np.int32)
    img_idx = np.repeat(np.arange(len(g), dtype=np.int32), n_pred)
    tp = np.concatenate([x[1].reshape(-1, 10) for x in g], 0).astype(bool)
    conf = np.concatenate([x[2] for x in g], 0).astype(np.float32)
    pred_cls = np.concatenate([x[3] for x in g], 0).astype(np.int16)
    target_cls = np.concatenate([x[4] for x in g], 0).astype(np.int16)
    assert len(g) == 548 and int(n_gt.sum()) == len(target_cls)
    assert not target_cls.any() and not pred_cls.any(), "classe unica: tudo deveria ser classe 0"
    m50, m5095 = recalcula_map50(tp, conf, pred_cls.astype(float), target_cls.astype(float))
    np.savez_compressed(saida_npz, names=nomes, n_gt=n_gt, img_idx=img_idx, conf=conf, tp=tp, pred_cls=pred_cls)
    rep = reportado(run)
    out = {"run": run, "pesos": pesos, "imagens": len(g), "caixas_verdadeiras": int(n_gt.sum()),
           "predicoes": int(n_pred.sum()), "batch": batch, "fp16": fp16, "imgsz": imgsz,
           "mAP50_validador": round(map50_val, 5), "mAP50_recalculado": round(m50, 5),
           "mAP50_95_validador": round(float(r.box.map), 5), "mAP50_95_recalculado": round(m5095, 5),
           "mAP50_reportado": rep,
           "dif_recalculado_validador": round(m50 - map50_val, 6),
           "dif_validador_reportado": None if rep is None else round(map50_val - rep, 5),
           "P_validador": round(float(r.box.mp), 4), "R_validador": round(float(r.box.mr), 4),
           "quando": datetime.now().isoformat(timespec="seconds")}
    print(f"{run}: validador {map50_val:.5f}  recalculado {m50:.5f}  reportado {rep}  "
          f"dif {out['dif_validador_reportado']}", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelos", nargs="*", default=[], help="runs em runs/detect")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--fp16", action="store_true")
    ap.add_argument("--imgsz", type=int, default=1280)
    ap.add_argument("--refaz", action="store_true")
    a = ap.parse_args()
    runs = ([r for r in MODELOS.values()
             if r in MODELOS_1710.values() or os.path.exists(os.path.join(DETECT, r, "weights", "best.pt"))]
            if a.todos else a.modelos)
    chk = os.path.join(AQUI, "visdrone_reproducao.json")
    saida = json.load(open(chk, encoding="utf-8")) if os.path.exists(chk) else {}
    saida.setdefault("protocolo", "VisDrone-DET val, 548 imagens, classe unica (pedestrian + people), imgsz 1280 "
                     "(lado maior), conf 0,001, NMS IoU 0,7, max_det 300, validador do Ultralytics 8.4.148; "
                     "casamento do validador (guloso por IoU, uma predicao por caixa) nos 10 limiares 0,50:0,95")
    saida.setdefault("modelos", {})
    for run in runs:
        r = roda(run, a.batch, a.fp16, a.imgsz, a.refaz)
        if r is not None:
            saida["modelos"][run] = r
            with open(chk, "w", encoding="utf-8") as f:
                json.dump(saida, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
