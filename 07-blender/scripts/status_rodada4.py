#!/usr/bin/env python3
"""
status_rodada4.py: retrato curto da rodada 4, para a checagem horaria (molde do status_rodada3.py).

Imprime: cadeia viva ou nao, etapa corrente com progresso e ritmo medido, idade do log mais novo,
erros recentes, previsao de termino (ritmo medido na etapa corrente, estimativa fixa nas outras), e
as etapas concluidas desde a ultima checagem, com o numero que cada uma produziu. As concluidas sao
marcadas como relatadas em fila4/relatadas.txt ao imprimir (o e-mail sai na mesma checagem).
"""
import csv
import glob
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rodada4 as R  # noqa: E402

# render: (pastas, quadros novos, s por quadro, s fixos do sorteio dos quadros pulados)
QUADRO = {"H1": (["ds_armado_75_porte"], 50, 170, 0), "E1": (["ds_armado_150g"], 200, 140, 0),
          "I1": (["ds_armado_35_extra"], 80, 125, 1500), "I2": (["ds_armado_75g_extra"], 80, 125, 1500),
          "J1": (["ds_regime_4k"], 120, 190, 1440)}
# treino: (nome, epocas, s por epoca)
EPOCA = {"F2": ("misto05", 30, 260), "F3": ("misto10", 30, 380), "E3": ("armado_150g", 60, 230),
         "G1": ("s_oblvar_sd1", 60, 175), "G2": ("s_oblvar_sd2", 60, 175),
         "G3": ("ft05_sint_sd1", 30, 100), "G4": ("ft05_sint_sd2", 30, 100),
         "G5": ("ft05_coco_sd1", 30, 100), "G6": ("ft05_coco_sd2", 30, 100),
         "G8": ("armado_35_sd1", 60, 230), "G9": ("armado_35_sd2", 60, 230),
         "G10": ("armado_75g_sd1", 60, 230), "G11": ("armado_75g_sd2", 60, 230)}
EST = {"K1": 1800, "K2": 900, "K3": 300, "K4": 600, "H2": 5, "H3": 300, "H4": 300, "H5": 600, "F1": 60,
       "F4": 240, "E2": 300, "E4": 300, "I3": 300, "I4": 300, "J2": 300, "J3": 900, "G7": 720, "G12": 1800,
       "Y1": 1600, "Y2": 60}


def vivo():
    try:
        import psutil
        for p in psutil.process_iter(["name", "cmdline"]):
            if any(os.path.basename(a) == "rodada4.py" for a in (p.info.get("cmdline") or [])):
                return True
    except Exception:
        pass
    return False


def quadros(eid):
    feitos, ts = 0, []
    for d in QUADRO[eid][0]:
        mf = os.path.join(R.RAIZ, d, "manifest.jsonl")
        if os.path.exists(mf):
            for ln in open(mf, encoding="utf-8"):
                if ln.strip():
                    feitos += 1
                    ts.append(json.loads(ln).get("render_s", 0))
    return feitos, ts[-10:]


def epocas(nome):
    f = os.path.join(R.RAIZ, "runs", "detect", nome, "results.csv")
    if not os.path.exists(f):
        return 0, None, None
    rows = [{k.strip(): v for k, v in r.items()} for r in csv.DictReader(open(f, encoding="utf-8"))]
    if not rows:
        return 0, None, None
    t = [float(r["time"]) for r in rows if r.get("time")]
    d = [b - a for a, b in zip(t, t[1:]) if b > a]
    ritmo = sorted(d)[len(d) // 2] if d else ((t[-1] / len(t)) if t else None)
    return len(rows), ritmo, rows[-1].get("metrics/mAP50(B)")


def restante(eid, st):
    if st == "ok":
        return 0, ""
    if eid in QUADRO:
        _, tot, seg, pulo = QUADRO[eid]
        feitos, ts = quadros(eid)
        ritmo = (sum(ts) / len(ts) + 5) if ts else seg
        return (tot - feitos) * ritmo + (pulo if feitos == 0 else 0), f"{feitos}/{tot} quadros, {ritmo:.0f} s/quadro"
    if eid in EPOCA:
        nome, tot, seg = EPOCA[eid]
        n, ritmo, m50 = epocas(nome)
        r = ritmo or seg
        return (tot - n) * r, f"epoca {n}/{tot}, {r:.0f} s/epoca, mAP50 val {m50}"
    return EST.get(eid, 60), ""


def le(nome):
    p = os.path.join(R.RES, nome)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def taxas(nome):
    d = le(nome)
    if not d:
        return "(sem arquivo)"
    t = d["taxa_por_classe_real"]
    return " ".join(f"{k}->armada {v['armada']:.3f} (n {v['n']})" for k, v in t.items())


def resultado(eid):
    """o numero que a etapa produziu, para o relato"""
    try:
        if eid in ("K1", "Y1"):
            d = le("visdrone_oficial_iou.json")
            return "; ".join(f"{m}: {v['padrao_ultralytics']['mAP50']} -> oficial {v['regra_oficial']['mAP50']} "
                             f"(AP60 {v['padrao_ultralytics']['AP60']}, AP75 {v['padrao_ultralytics']['AP75']})"
                             for m, v in d["modelos"].items())
        if eid == "K2":
            return " | ".join(f"{n} {s}: objeto->armada {le(f'confusao_{n}{s}.json')['taxa_por_classe_real']['objeto']['armada']}"
                              for n in ("armado_75", "armado_35", "armado_75g") for s in ("_iou60", "_iou75"))
        if eid == "K3":
            e = le("escala_casada.json")
            return (f"imgsz casado {e['imgsz_casado']} ({e['no_casado']}); s_nadir_4k "
                    f"{R.json.load(open(os.path.join(R.RES, 'sim2real_s_nadir_4k_casada.json')))['resultados'][0]}")
        if eid == "H2":
            g = le("porte_arma_gemeo.json")
            return f"{g['quadros_com_caixas_identicas']}/{g['quadros_inedita']} quadros gemeos caixa a caixa"
        if eid in ("H3", "H4", "E4", "I3", "I4"):
            arq = {"H3": "holdout_armas_armado_75_inst.json", "H4": "porte_arma_armado_75.json",
                   "E4": "confusao_armado_150g.json", "I3": "extra_armado_35.json", "I4": "extra_armado_75g.json"}[eid]
            return taxas(arq)
        if eid == "H5":
            return "normal: " + taxas("holdout_armas_armado_75g_inst.json") + " | porte de arma: " + taxas("porte_arma_armado_75g.json")
        if eid == "F4":
            return "; ".join(f"{n}: {R.json.load(open(os.path.join(R.RES, f'sim2real_{n}.json')))['resultados'][0].get('metrics/mAP50(B)')}"
                             for n in ("misto05", "misto10"))
        if eid == "J3":
            d = le("por_regime_s_nadir_4k.json")
            return (" ".join(f"{v['regime_no_artigo']} {v['mAP50']}" for v in d["por_regime"].values())
                    + f" | criterio {d['criterio_10_3']}")
        if eid == "G7":
            return "; ".join(f"{n}: {R.json.load(open(os.path.join(R.RES, f'sim2real_{n}.json')))['resultados'][0].get('metrics/mAP50(B)')}"
                             for n in ("s_oblvar_sd1", "s_oblvar_sd2", "ft05_sint_sd1", "ft05_sint_sd2", "ft05_coco_sd1", "ft05_coco_sd2"))
        if eid == "G12":
            return " | ".join(f"{n}: {taxas(f'confusao_{n}.json')}" for n in
                              ("armado_35_sd1", "armado_35_sd2", "armado_75g_sd1", "armado_75g_sd2"))
        if eid == "Y2":
            d = le("rodada4_criterios.json")
            return json.dumps({k: (v.get("veredito") if isinstance(v, dict) else v) for k, v in d.items()}, ensure_ascii=False)
        if eid in QUADRO:
            return f"{quadros(eid)[0]} quadros"
        if eid in EPOCA:
            n, _, m50 = epocas(EPOCA[eid][0])
            return f"{n} epocas, mAP50 val {m50}"
    except Exception as exc:
        return f"(sem numero: {exc!r})"
    return ""


def main():
    e = R.carrega()
    agora = datetime.now()
    pausa = os.path.join(R.FILA, "PAUSA")
    if os.path.exists(pausa):
        print(f"PAUSADA pelo autor desde {open(pausa).read().strip()} (pausa_rodada4.py retoma para voltar)")
    print(f"{agora:%d/%m %H:%M}  cadeia {'VIVA' if vivo() else 'PARADA'}"
          + (f"  | encerrada {e['fim']}" if e.get("fim") else "")
          + (f"  | FALHA nos grupos {e['grupos_com_falha']}" if e.get("grupos_com_falha") else ""))
    logs = sorted(glob.glob(os.path.join(R.FILA, "*.log")), key=os.path.getmtime)
    if logs:
        idade = (time.time() - os.path.getmtime(logs[-1])) / 60
        print(f"log mais novo: {os.path.basename(logs[-1])}, ha {idade:.0f} min" + ("  <<< PARADO" if idade > 45 else ""))
        cauda = open(logs[-1], encoding="utf-8", errors="replace").read()[-20000:]
        erros = [ln.strip() for ln in cauda.splitlines()
                 if re.search(r"Traceback|CUDA error|out of memory|Error:|FALHOU|ABORTADO", ln)]
        if erros:
            print("ERROS RECENTES:", " || ".join(erros[-4:])[:600])
    total = 0
    pend = []
    for eid, g, desc, _, prova in R.ETAPAS:
        st = "ok" if os.path.exists(prova) else e.get(eid, {}).get("estado", "pendente")
        seg, prog = restante(eid, st)
        total += seg
        if st == "rodando" or st.startswith("falhou"):
            print(f"  {eid} {desc[:55]:<55} {st:<10} {prog}")
        elif st != "ok":
            pend.append(eid)
    print("pendentes: " + (" ".join(pend) or "nenhuma"))
    fim = agora + timedelta(seconds=total)
    print(f"falta ~{total / 3600:.1f} h  ->  termino previsto {fim:%a %d/%m %H:%M}")
    rel_f = os.path.join(R.FILA, "relatadas.txt")
    rel = set(open(rel_f).read().split()) if os.path.exists(rel_f) else set()
    novas = [eid for eid, *_, prova in R.ETAPAS if os.path.exists(prova) and eid not in rel]
    if novas:
        print("NOVAS CONCLUSOES:")
        for eid in novas:
            desc = next(d for i, _, d, *_ in R.ETAPAS if i == eid)
            print(f"  {eid} {desc}: {resultado(eid)}")
        with open(rel_f, "a") as f:
            f.write("\n".join(novas) + "\n")


if __name__ == "__main__":
    main()
