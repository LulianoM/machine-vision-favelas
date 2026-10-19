#!/usr/bin/env python3
"""
status_rodada5.py: retrato curto da rodada 5, para a checagem horaria (molde do status_rodada4.py).

Imprime: pausa, cadeia viva ou nao, supervisor vivo ou nao, etapa corrente com progresso e ritmo medido,
idade do log mais novo, erros recentes, etapas aguardando dado ou dispensadas, previsao de termino
(ritmo medido na etapa corrente, estimativa fixa nas outras, tiradas de PLANO-RODADA5.md e
custo-rodada5.md) e as etapas concluidas desde a ultima checagem, com o numero que cada uma produziu.
As concluidas sao marcadas como relatadas em fila5/relatadas.txt ao imprimir (o e-mail sai na mesma
checagem). Com --sem-marcar nada e marcado (para olhar sem consumir as novidades).
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
import rodada5 as R  # noqa: E402

# render: (pastas, quadros novos, s por quadro, s fixos do sorteio dos quadros pulados)
QUADRO = {"P2": (["_teste_mpfb"], 1, 183, 120), "D1": (["ds_soldur_4k"], 180, 183, 0),
          "M1": (["ds_armado_150g_extra"], 80, 128, 1600), "M5": (["_armado_150g_mais"], 400, 128, 2240),
          "C1": ([f"_oblvar_e22_s{k}" for k in R.SITIOS], 180, 200, 0),
          "C5": ([f"_oblvar_e23_s{k}" for k in R.SITIOS], 180, 200, 0)}
# treino: (nome, epocas, s por epoca)
EPOCA = {"S1": ("s_nadir_4k_sd1", 60, 240), "S2": ("s_obliquo_sd1", 60, 206),
         "S3": ("s_nadir_4k_sd2", 60, 240), "S4": ("s_obliquo_sd2", 60, 206),
         "F0": ("ft05_coco_rep", 30, 98), "D3": ("s_soldur_4k", 60, 240),
         "M2": ("armado_150g_e120", 120, 261), "M7": ("armado_150g_600", 60, 780),
         "C3": ("s_oblvar_e22", 60, 198), "C7": ("s_oblvar_e23", 60, 198)}
for _eid, _g, _d, _f, _p in R.ETAPAS:
    if _g == "F" and _d.startswith("treino ft"):
        _n = _d.split()[1]
        EPOCA[_eid] = (_n, 30, 98 if _n.startswith("ft05") else 184)
    if _g == "A" and _d.startswith("treino s_oblvar_c"):
        _n = _d.split()[1]
        _q = int(_n[len("s_oblvar_c"):len("s_oblvar_c") + 3])
        EPOCA[_eid] = (_n, 60, round(198 * _q / 152))       # proporcional aos ladrilhos (198 s nos 152 quadros)
# etapas compostas: segundos estimados
EST = {"P1": 60, "S5": 900, "S6": 1800, "S7": 1200, "F0b": 240, "F12b": 3 * 30 * 140, "F13": 16 * 300, "F14": 5,
       "F15": 4 * 30 * 98, "F16": 4 * 300, "N1": 60, "N2": 7200, "N3": 300, "Y1": 600, "A1": 120, "A10": 8 * 400,
       "D2": 300, "D4": 1800, "D5": 240, "M3": 1100, "M4": 5, "M6": 600, "M8": 800, "C2": 300, "C4": 600,
       "C6": 300, "C8": 600, "Y2": 40 * 200, "Y3": 600, "Y4": 120}


def vivo(nome):
    try:
        import psutil
        for p in psutil.process_iter(["name", "cmdline"]):
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
    if st in ("ok", "dispensada", "aguardando_dado"):
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


def zs(runs):
    return "; ".join(f"{n}: {R.map50_real(n)}" for n in runs)


def taxas(nome):
    d = le(nome)
    if not d:
        return "(sem arquivo)"
    t = d["taxa_por_classe_real"]
    return " ".join(f"{k}->armada {v['armada']:.3f} perdida {v['perdida']:.3f} (n {v['n']})" for k, v in t.items())


def resultado(eid):
    """o numero que a etapa produziu, para o relato"""
    try:
        e = R.carrega().get(eid, {})
        if e.get("estado") == "dispensada":
            return "dispensada pela regra do plano"
        if eid == "P1":
            d = json.load(open(os.path.join(R.FILA, "P1.json"), encoding="utf-8"))
            return f"disco {d['disco_livre_gb']} GB, GPU {d.get('gpu_memoria_mb_mediana')} MB / {d.get('gpu_utilizacao_mediana')}%, venv {d.get('venv')}"
        if eid == "P2":
            d = json.load(open(os.path.join(R.FILA, "P2.json"), encoding="utf-8"))
            return f"{d['pessoas']} pessoas, {d['caixas']} caixas; {d['pool']}"
        if eid == "S5":
            return zs(["s_nadir_4k_sd1", "s_obliquo_sd1", "s_nadir_4k_sd2", "s_obliquo_sd2"])
        if eid in ("S6", "Y2"):
            d = le("visdrone_oficial_iou.json")
            runs = (["s_nadir_4k_sd1", "s_obliquo_sd1", "s_nadir_4k_sd2", "s_obliquo_sd2"] if eid == "S6"
                    else [r for r in R.RUNS_NOVOS if r in d["modelos"]])
            return "; ".join(f"{m}: {d['modelos'][m]['padrao_ultralytics']['mAP50']} -> oficial "
                             f"{d['modelos'][m]['regra_oficial']['mAP50']}" for m in runs if m in d["modelos"])
        if eid == "F0b":
            d = le("rodada5_ft_reproducao.json")
            return f"ft05_coco_rep {d['ft05_coco_rep']} contra {d['ft05_coco']}: {'reproduz' if d['reproduz'] else 'NAO reproduz'}"
        if eid == "F13":
            return zs(R.runs_ft_grade())
        if eid == "F14":
            return json.dumps(le("rodada5_ft_selecao.json")["escolha"])
        if eid == "F16":
            return zs([f"ft05_{i}_{c}_sd{s}" for i, c, s in R.runs_f15()])
        if eid == "N1":
            d = le("escala_heridal.json")
            return f"imgsz casado {d['imgsz_casado']} ({d['no_casado_lado_maior_med']} px); 1280 -> {d['no_protocolo_lado_maior_med']} px"
        if eid == "N3":
            d = json.load(open(os.path.join(R.REV, "bootstrap_heridal.json"), encoding="utf-8"))
            return (f"R {d['validade']['R_mAP50']} ({'interpretavel' if d['validade']['interpretavel'] else 'NAO interpretavel'}); "
                    + "; ".join(f"{x['comparacao']}: {x.get('dif')} {x.get('dif_ic95')}" for x in d["diferencas"]))
        if eid in ("Y1", "Y4"):
            d = le("rodada5_criterios.json")
            return json.dumps({k: (v.get("veredito") if isinstance(v, dict) else v) for k, v in d.items()
                               if isinstance(v, dict)}, ensure_ascii=False)[:1500]
        if eid == "Y3":
            d = json.load(open(os.path.join(R.REV, "resolvivel_r5.json"), encoding="utf-8"))
            return " | ".join(f"{x['comparacao']}: {x['veredito']['resumo']}" for x in d["comparacoes"])
        if eid == "A1":
            d = le("curva_subconjuntos.json")
            return "; ".join(f"{k}: {v['ladrilhos_treino']} ladrilhos" for k, v in d["pontos"].items())
        if eid == "A10":
            return zs([f"s_oblvar_c{n:03d}" for n in R.CURVA] + [f"s_oblvar_c{n:03d}_sd{s}" for n in (30, 120) for s in (1, 2)])
        if eid == "D4":
            d = le("por_regime_s_soldur_4k.json")
            return " ".join(f"{v['regime_no_artigo']} {v['mAP50']}" for v in d["por_regime"].values())
        if eid == "D5":
            return zs(["s_soldur_4k"])
        if eid == "M3":
            return "val: " + taxas("confusao_armado_150g_e120.json") + " | novos: " + taxas("extra_armado_150g_e120.json")
        if eid == "M4":
            d = le("rodada5_validade_150.json")
            return f"recall val {d['recall_qualquer_classe_val']}, novos {d['recall_qualquer_classe_quadros_novos']}: {'VALIDO' if d['valido'] else 'nao valido'}"
        if eid == "M8":
            return "val: " + taxas("confusao_armado_150g_600.json") + " | novos: " + taxas("extra_armado_150g_600.json")
        if eid in ("C4", "C8"):
            return zs(["s_oblvar_e22" if eid == "C4" else "s_oblvar_e23"])
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
        print(f"PAUSADA pelo autor desde {open(R.PAUSA).read().strip()} (pausa_rodada5.py retoma para voltar)")
    print(f"{agora:%d/%m %H:%M}  cadeia {'VIVA' if vivo('rodada5.py') else 'PARADA'}, "
          f"supervisor {'VIVO' if vivo('supervisiona_rodada5.py') else 'PARADO'}"
          + (f"  | encerrada {e['fim']}" if e.get("fim") else "")
          + (f"  | FALHA nos grupos {e['grupos_com_falha']}" if e.get("grupos_com_falha") else ""))
    logs = sorted(glob.glob(os.path.join(R.FILA, "*.log")), key=os.path.getmtime)
    if logs:
        idade = (time.time() - os.path.getmtime(logs[-1])) / 60
        print(f"log mais novo: {os.path.basename(logs[-1])}, ha {idade:.0f} min" + ("  <<< PARADO" if idade > 60 else ""))
        cauda = open(logs[-1], encoding="utf-8", errors="replace").read()[-20000:]
        erros = [ln.strip() for ln in cauda.splitlines()
                 if re.search(r"Traceback|CUDA error|out of memory|Error:|FALHOU|ABORTADO", ln)]
        if erros:
            print("ERROS RECENTES:", " || ".join(erros[-4:])[:600])
    total = 0
    pend, esperando, dispensadas = [], [], []
    for eid, g, desc, _, prova in R.ETAPAS:
        st = e.get(eid, {}).get("estado", "pendente")
        if os.path.exists(prova) and st not in ("dispensada",):
            st = "ok"
        if st == "aguardando_dado" and os.path.exists(prova):
            st = "ok"
        seg, prog = restante(eid, st)
        total += seg
        if st == "rodando" or st.startswith("falhou") or st == "pulada":
            print(f"  {eid} {desc[:60]:<60} {st:<10} {prog}")
        elif st == "aguardando_dado":
            esperando.append(eid)
        elif st == "dispensada":
            dispensadas.append(eid)
        elif st != "ok":
            pend.append(eid)
    print("pendentes: " + (" ".join(pend) or "nenhuma"))
    if esperando:
        print(f"aguardando dado (HERIDAL convertida: {os.path.exists(R.HERIDAL_YAML)}): " + " ".join(esperando))
    if dispensadas:
        print("dispensadas: " + " ".join(dispensadas))
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
