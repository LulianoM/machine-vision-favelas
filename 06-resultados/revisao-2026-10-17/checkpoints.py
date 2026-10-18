#!/usr/bin/env python3
"""
checkpoints.py: para cada modelo reportado no artigo, le em runs/detect/<run>/ o args.yaml, o
results.csv e o best.pt, e devolve a epoca do checkpoint escolhido, a metrica de escolha, as epocas
pedidas e feitas, se houve parada antecipada e o tempo de treino.

Revisao de 2026-10-17 (agente D1). So le.

Uso:
  C:/arma3-favela/venv/Scripts/python.exe 06-resultados/revisao-2026-10-17/checkpoints.py
Saida: checkpoints.json e a tabela de checkpoints.md (so a tabela; o texto em volta e escrito a mao).

Regra de selecao do Ultralytics 8.4.148 (conferida no codigo instalado em C:/arma3-favela/venv):
  utils/metrics.py, DetMetrics.fitness: w = [0.0, 0.0, 0.0, 1.0] sobre [P, R, mAP50, mAP50-95],
  ou seja fitness = mAP50-95 na divisao de validacao do data.yaml do treino.
  engine/trainer.py: best_fitness so sobe com fitness estritamente maior (linha 907); best.pt e
  gravado em toda epoca em que fitness == best_fitness (linha 801), entao num empate exato o
  best.pt e o da epoca mais tardia. patience: para quando passam `patience` epocas sem subir.
  O best.pt gravado tem epoch = -1 (strip_optimizer) mas guarda em train_metrics as metricas da
  epoca escolhida; a epoca e recuperada casando essas metricas com as linhas do results.csv.
"""
import csv
import json
import os

RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
DETECT = os.path.join(RAIZ, "runs", "detect")
AQUI = os.path.dirname(os.path.abspath(__file__))

# (run, nome no artigo, grupo)
RUNS = [
    ("morro_clima_s", "Pilot model (1080p corpus, 640 px tiles)", "piloto"),
    ("r_pareado", "R", "classe unica, real"),
    ("s_nadir_4k", "S-nadir-150", "classe unica, sintetico"),
    ("s_variedade", "S-nadir-150-six", "classe unica, sintetico"),
    ("s_obliquo", "S-oblique", "classe unica, sintetico"),
    ("s_oblvar", "S-oblique-six (seed 0)", "classe unica, sintetico"),
    ("s_oblvar_sd1", "S-oblique-six (seed 1)", "classe unica, sintetico"),
    ("s_oblvar_sd2", "S-oblique-six (seed 2)", "classe unica, sintetico"),
    ("ft05_sint", "F-synthetic 5% (seed 0)", "ajuste fino"),
    ("ft05_sint_sd1", "F-synthetic 5% (seed 1)", "ajuste fino"),
    ("ft05_sint_sd2", "F-synthetic 5% (seed 2)", "ajuste fino"),
    ("ft05_coco", "F-generic 5% (seed 0)", "ajuste fino"),
    ("ft05_coco_sd1", "F-generic 5% (seed 1)", "ajuste fino"),
    ("ft05_coco_sd2", "F-generic 5% (seed 2)", "ajuste fino"),
    ("ft10_sint", "F-synthetic 10%", "ajuste fino"),
    ("ft10_coco", "F-generic 10%", "ajuste fino"),
    ("misto05", "F-joint 5%", "treino conjunto"),
    ("misto10", "F-joint 10%", "treino conjunto"),
    ("armado_75", "S-nadir-75 (three classes)", "tres classes"),
    ("armado_35", "S-nadir-35 (seed 0)", "tres classes"),
    ("armado_35_sd1", "S-nadir-35 (seed 1)", "tres classes"),
    ("armado_35_sd2", "S-nadir-35 (seed 2)", "tres classes"),
    ("armado_75g", "Twin at 75 m (seed 0)", "tres classes"),
    ("armado_75g_sd1", "Twin at 75 m (seed 1)", "tres classes"),
    ("armado_75g_sd2", "Twin at 75 m (seed 2)", "tres classes"),
    ("armado_150g", "Twin at 150 m", "tres classes"),
]


def le_args(run):
    import yaml
    with open(os.path.join(DETECT, run, "args.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def le_results(run):
    with open(os.path.join(DETECT, run, "results.csv"), encoding="utf-8") as f:
        rd = csv.DictReader(f)
        linhas = []
        for r in rd:
            linhas.append({k.strip(): (float(v) if v.strip() not in ("", "nan") else None) for k, v in r.items()})
    return linhas


def le_best(run):
    import torch
    ck = torch.load(os.path.join(DETECT, run, "weights", "best.pt"), map_location="cpu", weights_only=False)
    return dict(epoch_gravado=ck.get("epoch"), best_fitness_gravado=ck.get("best_fitness"),
                train_metrics=ck.get("train_metrics"), versao=ck.get("version"), data=str(ck.get("date")))


def val_split(data_yaml):
    """caminho absoluto da divisao de validacao (selecao) do data.yaml do treino"""
    try:
        import yaml
        p = str(data_yaml)
        if not os.path.isabs(p):
            p = os.path.join(RAIZ, p)      # os treinos rodaram a partir de C:/arma3-favela/blender
        with open(p, encoding="utf-8") as f:
            d = yaml.safe_load(f)
        v = str(d.get("val"))
        if not os.path.isabs(v):
            v = os.path.join(str(d.get("path") or os.path.dirname(p)), v)
        return v.replace("\\", "/")
    except Exception as e:
        return f"nao lido: {e}"


def selecao_txt(v):
    v = v.replace("\\", "/")
    if "/ft/sel/" in v or v.endswith("sel/images"):
        return "fatia sel (324 imagens do VisDrone train, disjunta do teste)"
    if "visdrone_sub/val" in v or "visdrone_yolo/val" in v:
        return "VisDrone val (o proprio conjunto de teste)"
    if "nao lido" in v:
        return v
    return "val proprio (ladrilhos dos quadros de validacao do corpus)"


# pesos iniciais reais dos treinos retomados de last.pt depois de pausa do autor (o args.yaml
# gravado na retomada mostra last.pt): rodada3.py e rodada4.py, MODELO = "yolo11s.pt"
INICIO_RETOMADOS = {"armado_75g": "yolo11s.pt", "armado_35_sd1": "yolo11s.pt", "misto10": "yolo11s.pt"}


def analisa(run, artigo, grupo):
    d = dict(run=run, nome_artigo=artigo, grupo=grupo, pasta=os.path.join(DETECT, run))
    if not os.path.isdir(d["pasta"]):
        d["nota"] = "pasta nao encontrada"
        return d
    a = le_args(run)
    d["args"] = dict(model=a.get("model"), data=a.get("data"), epochs=a.get("epochs"), patience=a.get("patience"),
                     imgsz=a.get("imgsz"), batch=a.get("batch"), seed=a.get("seed"), single_cls=a.get("single_cls"),
                     optimizer=a.get("optimizer"), lr0=a.get("lr0"), close_mosaic=a.get("close_mosaic"),
                     resume=a.get("resume"), deterministic=a.get("deterministic"))
    d["selecao_val"] = val_split(a.get("data"))
    rs = le_results(run)
    ep = [int(r["epoch"]) for r in rs]
    d["epocas_feitas"] = len(rs)
    d["epoca_primeira"] = min(ep) if ep else None
    d["epoca_ultima"] = max(ep) if ep else None
    d["epocas_repetidas_no_csv"] = sorted({e for e in ep if ep.count(e) > 1})
    d["tempo_treino_s"] = rs[-1].get("time") if rs else None
    # se houve retomada, o tempo pode ter recomecado: soma por trecho monotono
    tempo = 0.0
    prev = None
    for r in rs:
        t = r.get("time") or 0.0
        if prev is not None and t < prev:
            tempo += prev
        prev = t
    tempo += prev or 0.0
    d["tempo_treino_s_somado_trechos"] = round(tempo, 1)
    d["tempo_treino_h"] = round(tempo / 3600, 2)
    # retomadas: a coluna time recomeca do zero depois de cada pausa
    d["retomadas_apos_epoca"] = [int(rs[i - 1]["epoch"]) for i in range(1, len(rs))
                                 if (rs[i].get("time") or 0) < (rs[i - 1].get("time") or 0)]
    d["pesos_iniciais"] = INICIO_RETOMADOS.get(run, os.path.basename(str(a.get("model"))))
    if run in INICIO_RETOMADOS:
        d["pesos_iniciais"] += " (retomado de last.pt apos pausa)"
    m50, m5095 = "metrics/mAP50(B)", "metrics/mAP50-95(B)"
    # melhor por fitness = mAP50-95 (regra do 8.4.148), ultimo em caso de empate exato
    best_i = None
    best_v = -1.0
    for i, r in enumerate(rs):
        v = r.get(m5095) or 0.0
        if v > best_v:
            best_v, best_i = v, i
    d["melhor_por_csv"] = dict(epoca=int(rs[best_i]["epoch"]), mAP50_95=round(rs[best_i][m5095], 5),
                               mAP50=round(rs[best_i][m50], 5), P=round(rs[best_i]["metrics/precision(B)"], 5),
                               R=round(rs[best_i]["metrics/recall(B)"], 5)) if best_i is not None else None
    try:
        b = le_best(run)
        d["best_pt"] = dict(epoch_gravado=b["epoch_gravado"], best_fitness_gravado=b["best_fitness_gravado"],
                            versao=b["versao"], data=b["data"],
                            train_metrics={k: round(v, 5) for k, v in (b["train_metrics"] or {}).items()})
        tm = b["train_metrics"] or {}
        # casa as metricas gravadas no best.pt com as linhas do csv
        cas = [int(r["epoch"]) for r in rs
               if abs((r.get(m5095) or 0) - tm.get(m5095, -9)) < 1e-4 and abs((r.get(m50) or 0) - tm.get(m50, -9)) < 1e-4]
        d["epoca_best_pt_casada"] = cas[-1] if cas else None
        d["epocas_casadas"] = cas
        d["confere"] = (cas[-1] == d["melhor_por_csv"]["epoca"]) if cas else False
    except Exception as e:
        d["best_pt"] = f"nao lido: {e}"
    d["parada_antecipada"] = d["epocas_feitas"] < (a.get("epochs") or 0)
    if d["parada_antecipada"] and d.get("melhor_por_csv"):
        d["epocas_sem_melhora_no_fim"] = d["epoca_ultima"] - d["melhor_por_csv"]["epoca"]
    ok = os.path.join(DETECT, run, "TREINO_OK")
    d["treino_ok"] = os.path.exists(ok)
    return d


def main():
    out = dict(gerado_em="2026-10-17", script=os.path.abspath(__file__),
               comando="C:/arma3-favela/venv/Scripts/python.exe 06-resultados/revisao-2026-10-17/checkpoints.py",
               regra="fitness = mAP50-95 (DetMetrics.fitness, w = [0, 0, 0, 1], Ultralytics 8.4.148); best.pt = epoca de maior fitness na validacao do data.yaml (ultima em empate exato); patience = epocas sem subir antes de parar",
               runs=[])
    for r in RUNS:
        print("run", r[0], flush=True)
        out["runs"].append(analisa(*r))
    with open(os.path.join(AQUI, "checkpoints.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    L = ["| Modelo (artigo) | Run | Pesos iniciais | Dado de treino (`data`) | Seleção em | Épocas pedidas / feitas | Parada antecipada | Época do best.pt | mAP50-95 na seleção (critério) | mAP50 na seleção | Semente | Tempo de treino (h) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for d in out["runs"]:
        if "args" not in d:
            L.append(f"| {d['nome_artigo']} | `{d['run']}` | não apurado | | | | | | | | | |")
            continue
        a = d["args"]
        mb = d.get("melhor_por_csv") or {}
        pa = "sim" + (f" ({d.get('epocas_sem_melhora_no_fim')} sem melhora)" if d.get("epocas_sem_melhora_no_fim") is not None else "") if d["parada_antecipada"] else "não"
        ep_best = d.get("epoca_best_pt_casada") if d.get("epoca_best_pt_casada") is not None else mb.get("epoca")
        conf = "" if d.get("confere", True) else " (csv diverge do best.pt)"
        sel_txt = selecao_txt(str(d["selecao_val"]))
        model = d["pesos_iniciais"]
        if "s_oblvar" in str(a["model"]):
            model = "best.pt de " + str(a["model"]).replace("\\", "/").split("/detect/")[1].split("/")[0]
        if d["retomadas_apos_epoca"]:
            model += " (pausas apos as epocas " + ", ".join(str(x) for x in d["retomadas_apos_epoca"]) + ")"
        data = os.path.basename(os.path.dirname(str(a["data"]).replace("\\", "/"))) if "data.yaml" in str(a["data"]) else os.path.basename(str(a["data"]))
        L.append(f"| {d['nome_artigo']} | `{d['run']}` | {model} | `{data}` | {sel_txt} | {a['epochs']} / {d['epocas_feitas']} | {pa} | {ep_best}{conf} | {mb.get('mAP50_95')} | {mb.get('mAP50')} | {a['seed']} | {d['tempo_treino_h']} |")
    with open(os.path.join(AQUI, "checkpoints_tabela.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))
    print("gravado checkpoints.json e checkpoints_tabela.md em", AQUI)


if __name__ == "__main__":
    main()
