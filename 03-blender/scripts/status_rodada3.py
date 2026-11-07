#!/usr/bin/env python3
"""
status_rodada3.py: retrato curto da rodada 3, para a checagem horaria.

Imprime: cadeia viva ou nao, etapa corrente com progresso e ritmo medido, idade do log mais novo,
erros recentes, previsao de termino (ritmo medido na etapa corrente, estimativa fixa nas outras),
e as etapas concluidas desde a ultima checagem, com o numero que cada uma produziu. As concluidas
sao marcadas como relatadas em fila3/relatadas.txt ao imprimir (o e-mail sai na mesma checagem).
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
import rodada3 as R  # noqa: E402

# segundos estimados por etapa (render: por quadro; treino: por epoca), medidos nas rodadas anteriores
EST = {"Z1": 120, "Z2": 120, "A2": 120, "A4": 90, "B2": 120, "C2": 120, "C4": 120, "D1": 60, "D6": 360}
QUADRO = {"A1": (180, 200), "B1": (50, 190), "C1": (200, 140)}
EPOCA = {"A3": ("s_oblvar", 60, 175), "C3": ("armado_75g", 60, 230), "D2": ("ft05_sint", 30, 180),
         "D3": ("ft05_coco", 30, 180), "D4": ("ft10_sint", 30, 330), "D5": ("ft10_coco", 30, 330)}
RENDER_DIR = {"A1": [f"_oblvar_s{k}" for k in R.SITIOS], "B1": ["ds_armado_75_inedita"], "C1": ["ds_armado_75g"]}


def vivo():
    try:
        import psutil
        for p in psutil.process_iter(["name", "cmdline"]):
            # por nome exato de argumento: "status_rodada3.py" tambem contem "rodada3.py"
            if any(os.path.basename(a) == "rodada3.py" for a in (p.info.get("cmdline") or [])):
                return True
    except Exception:
        pass
    return False


def quadros(eid):
    feitos, ts = 0, []
    for d in RENDER_DIR[eid]:
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
    rows = list(csv.DictReader(open(f, encoding="utf-8")))
    rows = [{k.strip(): v for k, v in r.items()} for r in rows]
    if not rows:
        return 0, None, None
    t = [float(r["time"]) for r in rows if r.get("time")]
    # "time" e acumulado e zera quando o treino e retomado de last.pt (pausa): o ritmo sai da mediana
    # das diferencas positivas entre epocas, nao de time/epocas
    d = [b - a for a, b in zip(t, t[1:]) if b > a]
    ritmo = sorted(d)[len(d) // 2] if d else ((t[-1] / len(t)) if t else None)
    m50 = rows[-1].get("metrics/mAP50(B)")
    return len(rows), ritmo, m50


def restante(eid, st):
    if st == "ok":
        return 0, ""
    if eid in QUADRO:
        tot, seg = QUADRO[eid]
        feitos, ts = quadros(eid)
        ritmo = (sum(ts) / len(ts) + 5) if ts else seg
        return (tot - feitos) * ritmo, f"{feitos}/{tot} quadros, {ritmo:.0f} s/quadro"
    if eid in EPOCA:
        nome, tot, seg = EPOCA[eid]
        n, ritmo, m50 = epocas(nome)
        r = ritmo or seg
        return (tot - n) * r, f"epoca {n}/{tot}, {r:.0f} s/epoca, mAP50 val {m50}"
    return EST.get(eid, 60), ""


def resultado(eid):
    """o numero que a etapa produziu, para o relato"""
    try:
        if eid == "A4":
            return f"s_oblvar VisDrone mAP50 {R.map50_real(os.path.join(R.RES, 'sim2real_s_oblvar.json'))}"
        if eid in ("Z1", "Z2", "B2", "C4"):
            arq = {"Z1": "confusao_armado_75", "Z2": "confusao_armado_35", "B2": "holdout_armas_armado_75",
                   "C4": "confusao_armado_75g"}[eid]
            d = json.load(open(os.path.join(R.RES, arq + ".json"), encoding="utf-8"))
            t = d["taxa_por_classe_real"]
            s = " ".join(f"{k}->armada {v['armada']:.2f}" for k, v in t.items())
            if d.get("por_tipo"):
                s += " | " + " ".join(f"{k} {v['chamada_de_armada']:.2f}" for k, v in d["por_tipo"].items())
            return s
        if eid == "D6":
            return json.dumps(json.load(open(os.path.join(R.RES, "ft_visdrone.json"), encoding="utf-8")))
        if eid in ("A1", "B1", "C1"):
            f, _ = quadros(eid)
            return f"{f} quadros"
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
        print(f"PAUSADA pelo autor desde {open(pausa).read().strip()} (pausa_rodada3.py retoma para voltar)")
    print(f"{agora:%d/%m %H:%M}  cadeia {'VIVA' if vivo() else 'PARADA'}"
          + (f"  | encerrada {e['fim']}" if e.get("fim") else "")
          + (f"  | FALHA nos grupos {e['grupos_com_falha']}" if e.get("grupos_com_falha") else ""))
    logs = sorted(glob.glob(os.path.join(R.FILA, "*.log")), key=os.path.getmtime)
    if logs:
        idade = (time.time() - os.path.getmtime(logs[-1])) / 60
        print(f"log mais novo: {os.path.basename(logs[-1])}, ha {idade:.0f} min"
              + ("  <<< PARADO" if idade > 45 else ""))
        cauda = open(logs[-1], encoding="utf-8", errors="replace").read()[-20000:]
        erros = [ln.strip() for ln in cauda.splitlines()
                 if re.search(r"Traceback|CUDA error|out of memory|Error:|FALHOU|nan", ln)]
        if erros:
            print("ERROS RECENTES:", " || ".join(erros[-4:])[:600])
    total = 0
    pend = []
    for eid, g, desc, _, prova in R.ETAPAS:
        st = "ok" if os.path.exists(prova) else e.get(eid, {}).get("estado", "pendente")
        seg, prog = restante(eid, st)
        total += seg
        if st == "rodando" or st.startswith("falhou"):
            print(f"  {eid} {desc[:50]:<50} {st:<10} {prog}")
        elif st != "ok":
            pend.append(eid)
    print("pendentes: " + (" ".join(pend) or "nenhuma"))
    fim = agora + timedelta(seconds=total)
    print(f"falta ~{total / 3600:.1f} h  ->  termino previsto {fim:%a %d/%m %H:%M}")
    rel_f = os.path.join(R.FILA, "relatadas.txt")
    rel = set(open(rel_f).read().split()) if os.path.exists(rel_f) else set()
    novas = [eid for eid, *_ , prova in R.ETAPAS if os.path.exists(prova) and eid not in rel]
    if novas:
        print("NOVAS CONCLUSOES:")
        for eid in novas:
            desc = next(d for i, _, d, *_ in R.ETAPAS if i == eid)
            print(f"  {eid} {desc}: {resultado(eid)}")
        with open(rel_f, "a") as f:
            f.write("\n".join(novas) + "\n")


if __name__ == "__main__":
    main()
