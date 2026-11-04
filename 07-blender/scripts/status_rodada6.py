#!/usr/bin/env python3
"""
status_rodada6.py: retrato curto da rodada 6, para a checagem horaria (molde do status_rodada5.py).

Imprime: pausa, cadeia e supervisor vivos ou nao, etapa corrente com progresso e ritmo, idade do log,
erros recentes, previsao de termino e as etapas concluidas desde a ultima checagem (marcadas em
fila6/relatadas.txt; --sem-marcar nao marca).
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
import rodada6 as R  # noqa: E402

# render: (pastas, quadros novos, s por quadro, s fixos do sorteio dos quadros pulados)
QUADRO = {"P2": (["_teste_comprimento"], 1, 128, 60), "L1": (["ds_armado_75c"], 200, 128, 0),
          "L4": (["ds_armado_150c"], 200, 128, 0),
          "L7": (["ds_armado_75c_extra", "ds_armado_150c_extra"], 160, 128, 3200),
          "E3": (["ds_semsol_4k"], 180, 183, 0), "P3": (["_teste_mao_quadro"], 1, 128, 60),
          "H1": (["ds_armado_35m"], 200, 128, 0), "H5": (["ds_armado_75gm"], 200, 128, 0), "H9": (["ds_armado_150gm"], 200, 128, 0),
          "H4": (["ds_armado_35m_extra"], 80, 128, 1600), "H8": (["ds_armado_75gm_extra"], 80, 128, 1600),
          "H12": (["ds_armado_150gm_extra"], 80, 128, 1600)}
# treino: (nome, epocas, s por epoca)
EPOCA = {"Q1": ("armado_35_e120", 120, 250), "Q2": ("armado_75g_e120", 120, 250), "L3": ("armado_75c", 60, 250),
         "L6": ("armado_150c_e120", 120, 261), "E1": ("s_soldur_4k_sd1", 60, 240), "E2": ("s_soldur_4k_sd2", 60, 240),
         "E5": ("s_semsol_4k", 60, 240), "G2": ("s_nadir_4k_deg", 60, 240), "G3": ("s_oblvar_deg", 60, 198),
         "T1": ("armado_35_e120_sd1", 120, 250), "T2": ("armado_75g_e120_sd1", 120, 250),
         "T3": ("armado_35_e120_sd2", 120, 250), "T4": ("armado_75g_e120_sd2", 120, 250),
         "T6": ("s_nadir_4k_deg_sd1", 60, 240), "T7": ("s_oblvar_deg_sd1", 60, 198),
         "T8": ("s_nadir_4k_deg_sd2", 60, 240), "T9": ("s_oblvar_deg_sd2", 60, 198),
         "T11": ("s_semsol_4k_sd1", 60, 240), "T12": ("s_semsol_4k_sd2", 60, 240),
         "V2": ("r_cheio_sel", 60, 1970), "R1": ("r_pareado_sel", 60, 400),
         "H3": ("armado_35m_e120", 120, 250), "H7": ("armado_75gm_e120", 120, 250), "H11": ("armado_150gm_e120", 120, 261)}
EST = {"P1": 60, "R2": 600, "Q3": 1200, "Q4": 60, "L2": 300, "L5": 300, "L8": 2400, "L9": 60, "E4": 300, "E6": 3000,
       "E7": 900, "E8": 60, "G1": 600, "G4": 3600, "G5": 300, "T5": 2400, "T10": 7200, "T13": 1200, "T14": 600,
       "V1": 60, "V3": 900, "Y1": 600, "H2": 300, "H6": 300, "H10": 300, "H13": 3600, "H14": 60}


def vivo(nome):
    try:
        import psutil
        for p in psutil.process_iter(["cmdline"]):
            if any(os.path.basename(a) == nome for a in (p.info.get("cmdline") or [])):
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
    if st in ("ok", "dispensada"):
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
        return (tot - n) * r * (0.75 if tot == 120 else 1.0), f"epoca {n}/{tot}, {r:.0f} s/epoca, mAP50 val {m50}"
    return EST.get(eid, 60), ""


def le(nome):
    p = os.path.join(R.RES, nome)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def map50(nome):
    d = le(f"sim2real_{nome}.json")
    if not d:
        return None
    return next((r.get("metrics/mAP50(B)") for r in d["resultados"] if r.get("conjunto") == "real"), None)


def taxas(nome):
    d = le(nome)
    if not d:
        return "(sem arquivo)"
    t = d["taxa_por_classe_real"]
    return " ".join(f"{k}->armada {v['armada']:.3f} perdida {v['perdida']:.3f} (n {v['n']})" for k, v in t.items())


def resultado(eid):
    try:
        c = le("rodada6_criterios.json") or {}
        if eid == "P1":
            d = json.load(open(os.path.join(R.FILA, "P1.json"), encoding="utf-8"))
            return f"disco {d['disco_livre_gb']} GB, venv {d.get('venv')}"
        if eid == "P2":
            d = json.load(open(os.path.join(R.FILA, "P2.json"), encoding="utf-8"))
            return f"{d['pessoas']} pessoas, {d['objetos']} objetos {d['comprimentos_objetos']}; {d['pool']}"
        if eid == "R1":
            return f"R-sel mAP50 {map50('r_pareado_sel')} (R 0,6311)"
        if eid in ("R2", "Q4", "L9", "E8", "G5", "T14", "Y1", "H14"):
            k = {"R2": "R", "Q4": "Q", "L9": "L", "E8": "E", "G5": "G", "H14": "H"}.get(eid)
            return c.get(k, {}).get("veredito") if k else json.dumps({x: c[x].get("veredito") for x in c if isinstance(c[x], dict)}, ensure_ascii=False)[:1500]
        if eid == "Q3":
            return " | ".join(f"{n} novos: {taxas(f'extra_{n}.json')}" for n in ("armado_35_e120", "armado_75g_e120"))
        if eid == "H13":
            return " | ".join(f"{n}: {taxas(f'extra_{n}.json')}" for n in ("armado_35m_e120", "armado_75gm_e120", "armado_150gm_e120"))
        if eid == "L8":
            return " | ".join(f"{n}: {taxas(f'extra_{n}.json')}" for n in ("armado_75c", "armado_150c_e120"))
        if eid == "E6":
            return " | ".join(f"{n}: " + " ".join(f"{v['regime_no_artigo']} {v['mAP50']}" for v in (le(f"por_regime_{n}.json") or {"por_regime": {}})["por_regime"].values())
                              for n in ("s_soldur_4k_sd1", "s_soldur_4k_sd2", "s_semsol_4k"))
        if eid == "E7":
            return "; ".join(f"{n}: {map50(n)}" for n in ("s_soldur_4k_sd1", "s_soldur_4k_sd2", "s_semsol_4k"))
        if eid in ("G4", "T10"):
            runs = ["s_nadir_4k_deg", "s_oblvar_deg"] if eid == "G4" else [f"{n}_sd{s}" for s in (1, 2) for n in ("s_nadir_4k_deg", "s_oblvar_deg")]
            return "; ".join(f"{n}: {map50(n)}" for n in runs)
        if eid == "V3":
            return f"R-full mAP50 {map50('r_cheio_sel')}"
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
    if os.path.exists(R.PAUSA):
        print(f"PAUSADA pelo autor desde {open(R.PAUSA).read().strip()} (pausa_rodada6.py retoma para voltar)")
    print(f"{agora:%d/%m %H:%M}  cadeia {'VIVA' if vivo('rodada6.py') else 'PARADA'}, "
          f"supervisor {'VIVO' if vivo('supervisiona_rodada6.py') else 'PARADO'}, r_sel {'VIVO' if vivo('r_sel.py') else 'parado'}"
          + (f"  | encerrada {e['fim']}" if e.get("fim") else "")
          + (f"  | FALHA nos grupos {e['grupos_com_falha']}" if e.get("grupos_com_falha") else ""))
    logs = sorted(glob.glob(os.path.join(R.FILA, "*.log")), key=os.path.getmtime)
    if logs:
        idade = (time.time() - os.path.getmtime(logs[-1])) / 60
        print(f"log mais novo: {os.path.basename(logs[-1])}, ha {idade:.0f} min" + ("  <<< PARADO" if idade > 60 else ""))
        cauda = open(logs[-1], encoding="utf-8", errors="replace").read()[-20000:]
        erros = [ln.strip() for ln in cauda.splitlines() if re.search(r"Traceback|CUDA error|out of memory|Error:|FALHOU|ABORTADO", ln)]
        if erros:
            print("ERROS RECENTES:", " || ".join(erros[-4:])[:600])
    total = 0
    pend = []
    for eid, g, desc, _, prova in R.ETAPAS:
        st = e.get(eid, {}).get("estado", "pendente")
        if os.path.exists(prova) and st != "dispensada":
            st = "ok"
        seg, prog = restante(eid, st)
        total += seg
        if st == "rodando" or st.startswith("falhou") or st == "pulada":
            print(f"  {eid} {desc[:70]:<70} {st:<10} {prog}")
        elif st not in ("ok", "dispensada"):
            pend.append(eid)
    print("pendentes: " + (" ".join(pend) or "nenhuma"))
    fim = agora + timedelta(seconds=total)
    print(f"falta ~{total / 3600:.1f} h  ->  termino previsto {fim:%a %d/%m %H:%M} (sem pausas)")
    rel_f = os.path.join(R.FILA, "relatadas.txt")
    rel = set(open(rel_f).read().split()) if os.path.exists(rel_f) else set()
    novas = [eid for eid, *_, prova in R.ETAPAS if os.path.exists(prova) and eid not in rel]
    if novas:
        print("NOVAS CONCLUSOES:")
        for eid in novas:
            desc = next(d for i, _, d, *_ in R.ETAPAS if i == eid)
            print(f"  {eid} {desc}: {resultado(eid)}")
        if "--sem-marcar" not in sys.argv:
            with open(rel_f, "a") as f:
                f.write("\n".join(novas) + "\n")


if __name__ == "__main__":
    main()
