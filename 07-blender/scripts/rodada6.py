#!/usr/bin/env python3
"""
rodada6.py: a rodada 6 (partida em 04/11/2026), em uma cadeia so, idempotente e retomavel: tudo o que
08-conferencia/versao-curta/O-QUE-FALTA-NO-SERVIDOR.md pede para o desktop, menos o item 8 (arma na mao),
que exige modelagem com verificacao visual e entra como grupo proprio quando estiver pronto.

Desenho, criterios fixados antes e custo em 07-blender/PLANO-RODADA6.md. Molde da rodada 5: cada etapa
tem um arquivo de prova e, se ele existe, a etapa e pulada; render retoma pelo manifest (--start); treino
retoma do last.pt e so conta como feito com TREINO_OK. Trava fila6/rodada6.trava; PAUSA em fila6/PAUSA.
Duas tentativas por etapa; se uma etapa falha, o resto do grupo e pulado e os outros grupos seguem.

Grupos, na ordem (secao 1 do plano):
  P   checagem de partida (disco, venv, caminhos, runs livres) e um quadro de teste com a flag nova
  R   item 4: espera o r_sel.py lancado as 11:28 terminar e completa o que faltar (idempotente)
  Q   item 5: S-nadir-35 e gemeo de 75 m com 120 epocas e paciencia 30; confusao no val e nos 80 quadros novos
  L   item 6: objetos confundiveis no comprimento das armas, 200 quadros a 75 e a 150 m, treinos, 80 quadros
      novos de cada, confusoes cruzadas
  E   item 7: especialista de sol duro com sementes 1 e 2 e o espelho "tudo menos sol duro"
  G   item 3: ruido, borrao e JPEG como aumento (ladrilhos degradados), S-nadir-150 e S-oblique-six
  T   sementes 1 e 2 de Q, G e do espelho de E
  V   item 9: teto R com a divisao de treino completa (menos a fatia de selecao)
  Y   criterios de tudo (06-resultados/rodada6_criterios.py)

Uso:  python rodada6.py              (roda o que falta)
      python rodada6.py --listar     (mostra as etapas e o estado)
      python rodada6.py --dry-run    (imprime o comando de cada etapa pendente, sem executar nada)
      python rodada6.py --so P,R     (roda so os grupos dados, sem gravar `fim`)
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime

SCR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(SCR))
RES = os.path.join(REPO, "06-resultados")
REV = os.path.join(RES, "revisao-2026-10-17")
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
FILA = os.path.join(RAIZ, "fila6")
LOG = os.path.join(RAIZ, "rodada6.log")
ESTADO = os.path.join(FILA, "estado.json")
TRAVA = os.path.join(FILA, "rodada6.trava")
PAUSA = os.path.join(FILA, "PAUSA")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
BLENDER = os.path.join("C:" + os.sep, "Program Files (x86)", "Steam", "steamapps", "common",
                       "Blender", "blender.exe")
VIS = os.path.join("C:" + os.sep, "arma3-favela", "visdrone")
VIS_YAML = os.path.join(VIS, "visdrone_yolo", "data.yaml")
FT = os.path.join(VIS, "ft")
HERIDAL_YAML = os.path.join("C:" + os.sep, "arma3-favela", "real_nadir", "heridal", "yolo", "data.yaml")
R_SEL_LOG = os.path.join(RAIZ, "r_sel.log")

MODELO, IMGSZ, EPOCAS, BATCH, WORKERS = "yolo11s.pt", 1280, 60, 6, 4
EPOCAS_LONGO, PACIENCIA_LONGO = 120, 30          # a receita do armado_150g_e120 (rodada 5, M2)
DISCO_MIN_GB = 60
DRY = False

# comandos dos corpora originais (rodada 3, 4 e 5), sem mudanca
NADIR4K = ["--samples", 96, "--res", 3840, 2160, "--people", 16, 34, "--pool", 6, "--seed", 21,
           "--climas", "todos", "--sitio", -1, "--mistura", 0.5, 0.5, 0.0, "--enquadro", "quadrado"]
ARMADO35 = ["--samples", 64, "--res", 3840, 2160, "--people", 12, 24, "--pool", 6, "--seed", 43,
            "--climas", "todos", "--alt", 35, "--alt-jitter", 3, "--mistura", 0.34, 0.33, 0.33,
            "--porte-realista", "--fio-gsd", "--laje", 0.75, "--amostra-no-quadro"]


def gemeo(alt, jitter):
    c = list(ARMADO35)
    c[c.index("--alt") + 1] = alt
    c[c.index("--alt-jitter") + 1] = jitter
    return c


GEMEO75 = gemeo(75, 6)
GEMEO150 = gemeo(150, 13)
COMPRIMENTO = ["--objetos-comprimento-arma"]
SEM_SOL_DURO = "sol_baixo,nublado,encoberto,neblina,chuva"


def climas(cmd, valor):
    c = list(cmd)
    c[c.index("--climas") + 1] = valor
    return c


RUNS_NOVOS = ["armado_35_e120", "armado_75g_e120", "armado_75c", "armado_150c_e120",
              "s_soldur_4k_sd1", "s_soldur_4k_sd2", "s_semsol_4k", "s_nadir_4k_deg", "s_oblvar_deg",
              "armado_35_e120_sd1", "armado_75g_e120_sd1", "armado_35_e120_sd2", "armado_75g_e120_sd2",
              "s_nadir_4k_deg_sd1", "s_oblvar_deg_sd1", "s_nadir_4k_deg_sd2", "s_oblvar_deg_sd2",
              "s_semsol_4k_sd1", "s_semsol_4k_sd2", "r_cheio_sel"]
DEG = [("ds_morro_4k_tiles", "ds_morro_4k_deg_tiles"), ("ds_oblvar_tiles", "ds_oblvar_deg_tiles")]


def j(*p):
    return os.path.join(*[str(x) for x in p])


def log(m):
    linha = f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}"
    if not DRY:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linha + "\n")
    print(linha, flush=True)


def carrega():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def grava(e):
    tmp = ESTADO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(e, f, indent=1, ensure_ascii=False)
    os.replace(tmp, ESTADO)


def marca(eid, **kw):
    if DRY:
        return
    e = carrega()
    e.setdefault(eid, {}).update(kw)
    grava(e)


def linhas(p):
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for ln in f if ln.strip())
    except OSError:
        return 0


def roda(cmd, nome_log, cwd=RAIZ):
    cmd = [str(c) for c in cmd]
    if DRY:
        print("      $ " + subprocess.list2cmdline(cmd), flush=True)
        return 0
    with open(j(FILA, nome_log), "a", encoding="utf-8", buffering=1) as f:
        f.write(f"\n# {datetime.now():%Y-%m-%d %H:%M:%S}\n# {' '.join(cmd)}\n\n")
        f.flush()
        return subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=cwd)


def nota(m):
    if DRY:
        print("      # " + m, flush=True)


def ok_arq(p):
    return os.path.join(FILA, p + ".ok")


def marca_ok(eid):
    if not DRY:
        with open(ok_arq(eid), "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat(timespec="seconds"))
    return 0


def le(p):
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def grava_json(p, d):
    if DRY:
        nota(f"grava {p}")
        return
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=1, ensure_ascii=False)


# ------------------------------------------------------------------ primitivas idempotentes
def render(nome_log, out, n, extra, inicio=0):
    feitos = linhas(j(out, "manifest.jsonl"))
    if os.path.exists(j(out, "data.yaml")) and feitos >= n:
        return 0
    cmd = [BLENDER, "-b", "--python-exit-code", 1, "--python", j(SCR, "gen_morro.py"), "--",
           "--out", out, "--dataset", inicio + n, *extra, "--start", inicio + feitos]
    log(f"  render {os.path.basename(out)}: de {feitos}/{n}" + (f" (indices {inicio} a {inicio + n - 1})" if inicio else ""))
    return roda(cmd, nome_log)


def ladrilha(ds, ds_t, nome_log):
    if os.path.exists(j(ds_t, "data.yaml")):
        return 0
    return roda([PY, j(SCR, "tile_dataset.py"), "--data", ds, "--out", ds_t, "--tile", 1280, "--overlap", 0.2], nome_log)


def pesos(nome):
    return j(RAIZ, "runs", "detect", nome, "weights", "best.pt")


def tr(nome):
    return j(RAIZ, "runs", "detect", nome, "TREINO_OK")


def treinado(nome):
    return os.path.exists(tr(nome))


def treina(nome, data, modelo, epocas, single, nome_log, semente=0, extra=(), paciencia=None):
    rd = j(RAIZ, "runs", "detect", nome)
    ok = tr(nome)
    if os.path.exists(ok):
        return 0
    last = j(rd, "weights", "last.pt")
    if os.path.exists(last):
        log(f"  treino {nome}: retomando de {last}")
        codigo = f"from ultralytics import YOLO\nYOLO(r'{last}').train(resume=True)\n"
        rc = roda([PY, "-c", codigo], nome_log)
        if rc != 0 and not DRY:
            with open(j(FILA, nome_log), encoding="utf-8", errors="replace") as f:
                cauda = f.read()[-4000:]
            if "nothing to resume" in cauda or "is finished" in cauda:
                rc = 0
    else:
        log(f"  treino {nome}: do zero, a partir de {os.path.basename(str(modelo))}, semente {semente}, {epocas} epocas")
        cmd = [PY, j(SCR, "train_yolo_win.py"), "--data", data, "--model", modelo,
               "--imgsz", IMGSZ, "--epochs", epocas, "--batch", BATCH, "--workers", WORKERS,
               "--name", nome, "--seed", semente] + (["--single-cls"] if single else []) + list(extra)
        if paciencia is not None:
            cmd += ["--patience", paciencia]
        rc = roda(cmd, nome_log)
    if rc == 0 and not DRY and os.path.exists(j(rd, "weights", "best.pt")):
        with open(ok, "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat())
    return rc


def treina_longo(nome, ds_tiles, L, semente=0):
    """tres classes, 120 epocas, paciencia 30: a receita do armado_150g_e120"""
    return treina(nome, j(RAIZ, ds_tiles, "data.yaml"), MODELO, EPOCAS_LONGO, False, L, semente, (), PACIENCIA_LONGO)


def avalia(nome, L, sint=None):
    saida = j(RES, f"sim2real_{nome}.json")
    if os.path.exists(saida):
        return 0
    cmd = [PY, j(SCR, "avalia_sim2real.py"), "--weights", pesos(nome), "--real", VIS_YAML,
           "--imgsz", IMGSZ, "--out", saida] + (["--sintetico", sint] if sint else [])
    return roda(cmd, L)


def preds(runs, L):
    falta = [r for r in runs if not os.path.exists(j(REV, f"preds_visdrone_{r}.npz"))]
    if not falta:
        return 0
    rc = roda([PY, j(REV, "visdrone_preds.py"), "--modelos", *falta, "--batch", 4], L)
    if rc != 0 or DRY:
        return rc
    sem = [r for r in falta if not os.path.exists(j(REV, f"preds_visdrone_{r}.npz"))]
    return 1 if sem else 0


def preds_heridal(runs, L):
    """preds na HERIDAL a imgsz casado (1152, escala_heridal.json) e a 1280; sem o dado, dispensada"""
    if not os.path.exists(HERIDAL_YAML):
        nota(f"sem {HERIDAL_YAML}: dispensada")
        return DISPENSADA if not DRY else 0
    e = le(j(RES, "escala_heridal.json"))
    casado = e["imgsz_casado"] if e else 1152
    rc = 0
    for tag, sz in (("heridal", casado), ("heridal_1280", 1280)):
        falta = [r for r in runs if not os.path.exists(j(REV, f"preds_{tag}_{r}.npz"))]
        if falta:
            rc = roda([PY, j(REV, "preds_nadir.py"), "--data", HERIDAL_YAML, "--tag", tag, "--imgsz", sz,
                       "--modelos", *falta, "--batch", 4], L) or rc
    return rc


def zs_preds(runs, L, eid, heridal=False):
    rc = varios(*[(avalia, r, L) for r in runs], (preds, runs, L))
    if rc == 0 and heridal:
        rc = preds_heridal(runs, L)
        if rc == DISPENSADA:
            rc = 0
    return marca_ok(eid) if rc == 0 else rc


def confusao(nome, ds, split, saida, L):
    if os.path.exists(j(RES, saida)):
        return 0
    return roda([PY, j(RES, "confusao_armado.py"), "--pesos", pesos(nome), "--ds", ds, "--split", split,
                 "--instancias", "--out", j(RES, saida)], L)


def por_regime(nome, L):
    saida = j(RES, f"por_regime_{nome}.json")
    if os.path.exists(saida):
        return 0
    return roda([PY, j(RES, "por_regime.py"), "--pesos", pesos(nome), "--ds", j(RAIZ, "ds_regime_4k"),
                 "--tiles", j(RAIZ, "ds_regime_4k_tiles"), "--por-quadro", "--out", saida], L)


def criterios(parte, L):
    return roda([PY, j(RES, "rodada6_criterios.py"), "--parte", parte], L)


def varios(*chamadas):
    for fn, *a in chamadas:
        rc = fn(*a)
        if rc != 0:
            return rc
    return 0


DISPENSADA = -200


# ------------------------------------------------------------------ grupo P
def preflight(L):
    if DRY:
        nota(f"funcao interna: disco >= {DISCO_MIN_GB} GB, venv (ultralytics 8.4.148, torch 2.14, CUDA), caminhos, "
             "corpora, pesos, runs novos livres")
        return 0
    prob, info = [], {}
    livre = shutil.disk_usage("C:" + os.sep).free / 1e9
    info["disco_livre_gb"] = round(livre, 1)
    if livre < DISCO_MIN_GB:
        prob.append(f"disco livre {livre:.0f} GB < {DISCO_MIN_GB}")
    try:
        v = subprocess.check_output([PY, "-c", "import ultralytics, torch; print(ultralytics.__version__, "
                                     "torch.__version__, torch.cuda.is_available())"], text=True, timeout=300).split()
        info["venv"] = v
        if v[0] != "8.4.148" or not v[1].startswith("2.14") or v[2] != "True":
            prob.append(f"venv inesperado: {v}")
    except Exception as exc:
        prob.append(f"venv falhou: {exc!r}")
    caminhos = [BLENDER, PY, VIS_YAML, j(FT, "sel_r.txt"), j(RAIZ, MODELO), j(SCR, "gen_morro.py"),
                j(SCR, "train_yolo_win.py"), j(SCR, "tile_dataset.py"), j(SCR, "degrada_ladrilhos.py"),
                j(SCR, "r_sel.py"), j(RES, "rodada6_criterios.py"), j(RES, "confusao_armado.py"), j(RES, "por_regime.py")]
    caminhos += [j(RAIZ, d, "data.yaml") for d in ("ds_armado_35_tiles", "ds_armado_75g_tiles", "ds_armado_35",
                                                    "ds_armado_75g", "ds_armado_35_extra", "ds_armado_75g_extra",
                                                    "ds_armado_150g_extra", "ds_morro_4k_tiles", "ds_oblvar_tiles",
                                                    "ds_soldur_4k_tiles", "ds_regime_4k", "ds_regime_4k_tiles")]
    caminhos += [pesos(r) for r in ("armado_35", "armado_75g", "armado_150g_e120", "s_soldur_4k", "s_nadir_4k",
                                    "s_oblvar", "r_pareado")]
    caminhos += [j(RES, f) for f in ("extra_armado_35.json", "extra_armado_75g.json", "extra_armado_150g_e120.json",
                                     "por_regime_s_soldur_4k.json", "por_regime_s_nadir_4k_r5.json")]
    falta = [c for c in caminhos if not os.path.exists(c)]
    if falta:
        prob.append("faltando: " + "; ".join(falta))
    ocupados = [r for r in RUNS_NOVOS if os.path.exists(j(RAIZ, "runs", "detect", r))]
    if ocupados:
        prob.append("runs novos ja existem: " + ", ".join(ocupados))
    info["heridal_data_yaml"] = os.path.exists(HERIDAL_YAML)
    info["problemas"] = prob
    info["quando"] = datetime.now().isoformat(timespec="seconds")
    grava_json(j(FILA, "P1.json"), info)
    for p in prob:
        log(f"  P1: {p}")
    log(f"  P1: disco {info['disco_livre_gb']} GB, venv {info.get('venv')}, HERIDAL convertida: {info['heridal_data_yaml']}")
    return 1 if prob else marca_ok("P1")


def teste_flag(L):
    """P2: um quadro a 75 m com --objetos-comprimento-arma; prova que o MPFB carregou e que todo objeto
    do manifest mede entre 0,62 e 1,05 m. Rodado depois do R (a GPU esta com o r_sel ate la)."""
    out = j(RAIZ, "_teste_comprimento")
    if not DRY:
        shutil.rmtree(out, ignore_errors=True)
    rc = render(L, out, 1, GEMEO75 + COMPRIMENTO)
    if DRY or rc != 0:
        return rc
    mf = [json.loads(x) for x in open(j(out, "manifest.jsonl"), encoding="utf-8") if x.strip()]
    if not mf:
        return 1
    m = mf[0]
    obj = [c for t, c in zip(m.get("tipos", []), m.get("comps", [])) if t and t in OBJETOS]
    cauda = open(j(FILA, L), encoding="utf-8", errors="replace").read()[-200000:]
    pool = [ln for ln in cauda.splitlines() if "pool MPFB:" in ln]
    info = {"pessoas": m.get("n_pessoas"), "caixas": m.get("n_caixas"), "objetos": len(obj),
            "comprimentos_objetos": obj, "pool": pool[-1].strip() if pool else "",
            "quando": datetime.now().isoformat(timespec="seconds")}
    log(f"  P2: {info}")
    if (m.get("n_pessoas", 0) < 12 or not pool or " 0 humanos" in pool[-1]
            or any(not (0.60 <= c <= 1.07) for c in obj)):
        log("  P2: MPFB ausente ou objeto fora da faixa 0,62 a 1,05 m")
        return 1
    grava_json(j(FILA, "P2.json"), info)
    return marca_ok("P2")


OBJETOS = {"vassoura", "rodo", "cano_pvc", "vergalhao", "tabua", "guarda_chuva", "enxada", "tapete", "mangueira"}


# ------------------------------------------------------------------ grupo R (item 4)
def r_sel_vivo():
    try:
        import psutil
        for p in psutil.process_iter(["cmdline"]):
            if any(os.path.basename(a) == "r_sel.py" for a in (p.info.get("cmdline") or [])):
                return True
    except Exception:
        pass
    return False


def espera_r_sel(L):
    """R1: espera o r_sel.py lancado fora da cadeia terminar (escrevendo no log a cada 15 min para o
    supervisor nao achar a cadeia parada) e depois completa o que faltar com o proprio r_sel.py"""
    if DRY:
        nota("espera o processo r_sel.py terminar, depois:")
        return roda([PY, j(SCR, "r_sel.py")], L)
    t0 = time.time()
    while r_sel_vivo():
        if time.time() - t0 > 16 * 3600:
            log("  R1: r_sel.py ainda vivo depois de 16 h; seguindo assim mesmo")
            break
        with open(j(FILA, L), "a", encoding="utf-8") as f:
            f.write(f"# {datetime.now():%H:%M} r_sel.py ainda rodando\n")
        time.sleep(15 * 60)
    return roda([PY, j(SCR, "r_sel.py")], L)


# ------------------------------------------------------------------ grupo V (item 9)
def lista_cheio(L):
    """V1: VisDrone train inteiro menos a fatia sel (324) -> train_sem_sel.txt e data_cheio_sel.yaml"""
    yaml = j(VIS, "visdrone_yolo", "data_cheio_sel.yaml")
    if os.path.exists(yaml):
        return 0
    if DRY:
        nota("funcao interna: lista das imagens de visdrone_yolo/train/images que nao estao em ft/sel/images; "
             "val = ft/sel/images")
        return 0
    sel = set(os.listdir(j(FT, "sel", "images")))
    todas = sorted(os.listdir(j(VIS, "visdrone_yolo", "train", "images")))
    fora = [f for f in todas if f not in sel]
    with open(j(VIS, "visdrone_yolo", "train_sem_sel.txt"), "w", encoding="utf-8") as f:
        for x in fora:
            f.write("C:/arma3-favela/visdrone/visdrone_yolo/train/images/" + x + "\n")
    with open(yaml, "w", encoding="utf-8") as f:
        f.write("path: C:/arma3-favela/visdrone/visdrone_yolo\ntrain: C:/arma3-favela/visdrone/visdrone_yolo/train_sem_sel.txt\n"
                "val: C:/arma3-favela/visdrone/ft/sel/images\nnames:\n  0: pessoa\n")
    grava_json(j(VIS, "visdrone_yolo", "train_sem_sel.json"),
               {"train_total": len(todas), "sel": len(sel), "em_comum": len(todas) - len(fora), "treino": len(fora),
                "quando": datetime.now().isoformat(timespec="seconds")})
    log(f"  V1: {len(fora)} imagens de treino ({len(todas)} menos {len(todas) - len(fora)} da fatia sel)")
    return 0


# ------------------------------------------------------------------ etapas
def conf_par(nome, ds, L):
    """confusao de um tres-classes no proprio val e nos 80 quadros novos do seu corpus de origem"""
    return varios((confusao, nome, j(RAIZ, ds), "val", f"confusao_{nome}.json", L),
                  (confusao, nome, j(RAIZ, ds + "_extra"), "val", f"extra_{nome}.json", L))


def etapas():
    E = [
        ("P1", "P", "checagem: disco, venv, caminhos, runs livres", preflight, ok_arq("P1")),
        ("R1", "R", "item 4: espera e completa o r_sel.py (treino, ZS, preds)", espera_r_sel,
         j(REV, "preds_visdrone_r_pareado_sel.npz")),
        ("R2", "R", "criterios do item 4 (eficacias com R-sel)", lambda L: criterios("R", L) or marca_ok("R2"), ok_arq("R2")),
        ("P2", "P", "checagem: um quadro de teste com --objetos-comprimento-arma", teste_flag, ok_arq("P2")),
        # Q (item 5)
        ("Q1", "Q", "treino armado_35_e120 (120 epocas, paciencia 30)",
         lambda L: treina_longo("armado_35_e120", "ds_armado_35_tiles", L), tr("armado_35_e120")),
        ("Q2", "Q", "treino armado_75g_e120 (120 epocas, paciencia 30)",
         lambda L: treina_longo("armado_75g_e120", "ds_armado_75g_tiles", L), tr("armado_75g_e120")),
        ("Q3", "Q", "confusao dos dois no val e nos 80 quadros novos",
         lambda L: varios((conf_par, "armado_35_e120", "ds_armado_35", L), (conf_par, "armado_75g_e120", "ds_armado_75g", L))
         or marca_ok("Q3"), ok_arq("Q3")),
        ("Q4", "Q", "criterios do item 5", lambda L: criterios("Q", L) or marca_ok("Q4"), ok_arq("Q4")),
        # L (item 6)
        ("L1", "L", "render ds_armado_75c: 200 quadros a 75 m, objetos no comprimento das armas",
         lambda L: (1 if not DRY and not os.path.exists(ok_arq("P2")) else render(L, j(RAIZ, "ds_armado_75c"), 200, GEMEO75 + COMPRIMENTO)),
         j(RAIZ, "ds_armado_75c", "data.yaml")),
        ("L2", "L", "ladrilhos de ds_armado_75c",
         lambda L: ladrilha(j(RAIZ, "ds_armado_75c"), j(RAIZ, "ds_armado_75c_tiles"), L), j(RAIZ, "ds_armado_75c_tiles", "data.yaml")),
        ("L3", "L", "treino armado_75c (60 epocas, a receita do armado_75g)",
         lambda L: treina("armado_75c", j(RAIZ, "ds_armado_75c_tiles", "data.yaml"), MODELO, EPOCAS, False, L), tr("armado_75c")),
        ("L4", "L", "render ds_armado_150c: 200 quadros a 150 m, objetos no comprimento das armas",
         lambda L: render(L, j(RAIZ, "ds_armado_150c"), 200, GEMEO150 + COMPRIMENTO), j(RAIZ, "ds_armado_150c", "data.yaml")),
        ("L5", "L", "ladrilhos de ds_armado_150c",
         lambda L: ladrilha(j(RAIZ, "ds_armado_150c"), j(RAIZ, "ds_armado_150c_tiles"), L), j(RAIZ, "ds_armado_150c_tiles", "data.yaml")),
        ("L6", "L", "treino armado_150c_e120 (120 epocas, paciencia 30, a receita do armado_150g_e120)",
         lambda L: treina_longo("armado_150c_e120", "ds_armado_150c_tiles", L), tr("armado_150c_e120")),
        ("L7", "L", "render 80 quadros novos de cada (indices 200 a 279)",
         lambda L: varios((render, L, j(RAIZ, "ds_armado_75c_extra"), 80, GEMEO75 + COMPRIMENTO + ["--val", 1.0], 200),
                          (render, L, j(RAIZ, "ds_armado_150c_extra"), 80, GEMEO150 + COMPRIMENTO + ["--val", 1.0], 200)),
         j(RAIZ, "ds_armado_150c_extra", "data.yaml")),
        ("L8", "L", "confusoes: proprios val e novos, novos originais, e os modelos originais nos novos de comprimento",
         lambda L: varios((conf_par, "armado_75c", "ds_armado_75c", L), (conf_par, "armado_150c_e120", "ds_armado_150c", L),
                          (confusao, "armado_75c", j(RAIZ, "ds_armado_75g_extra"), "val", "extra75g_armado_75c.json", L),
                          (confusao, "armado_150c_e120", j(RAIZ, "ds_armado_150g_extra"), "val", "extra150g_armado_150c_e120.json", L),
                          (confusao, "armado_75g", j(RAIZ, "ds_armado_75c_extra"), "val", "extra75c_armado_75g.json", L),
                          (confusao, "armado_150g_e120", j(RAIZ, "ds_armado_150c_extra"), "val", "extra150c_armado_150g_e120.json", L))
         or marca_ok("L8"), ok_arq("L8")),
        ("L9", "L", "criterios do item 6", lambda L: criterios("L", L) or marca_ok("L9"), ok_arq("L9")),
        # E (item 7)
        ("E1", "E", "treino s_soldur_4k_sd1",
         lambda L: treina("s_soldur_4k_sd1", j(RAIZ, "ds_soldur_4k_tiles", "data.yaml"), MODELO, EPOCAS, True, L, 1), tr("s_soldur_4k_sd1")),
        ("E2", "E", "treino s_soldur_4k_sd2",
         lambda L: treina("s_soldur_4k_sd2", j(RAIZ, "ds_soldur_4k_tiles", "data.yaml"), MODELO, EPOCAS, True, L, 2), tr("s_soldur_4k_sd2")),
        ("E3", "E", "render ds_semsol_4k: 180 quadros nadir com todos os regimes menos sol duro",
         lambda L: render(L, j(RAIZ, "ds_semsol_4k"), 180, climas(NADIR4K, SEM_SOL_DURO)), j(RAIZ, "ds_semsol_4k", "data.yaml")),
        ("E4", "E", "ladrilhos de ds_semsol_4k",
         lambda L: ladrilha(j(RAIZ, "ds_semsol_4k"), j(RAIZ, "ds_semsol_4k_tiles"), L), j(RAIZ, "ds_semsol_4k_tiles", "data.yaml")),
        ("E5", "E", "treino s_semsol_4k (espelho)",
         lambda L: treina("s_semsol_4k", j(RAIZ, "ds_semsol_4k_tiles", "data.yaml"), MODELO, EPOCAS, True, L), tr("s_semsol_4k")),
        ("E6", "E", "por regime, por quadro: sementes do especialista, espelho e sementes do generalista",
         lambda L: varios(*[(por_regime, r, L) for r in ("s_soldur_4k_sd1", "s_soldur_4k_sd2", "s_semsol_4k",
                                                           "s_nadir_4k_sd1", "s_nadir_4k_sd2")]) or marca_ok("E6"),
         ok_arq("E6")),
        ("E7", "E", "ZS dos tres (exploratorio)",
         lambda L: varios(*[(avalia, r, L) for r in ("s_soldur_4k_sd1", "s_soldur_4k_sd2", "s_semsol_4k")]) or marca_ok("E7"),
         ok_arq("E7")),
        ("E8", "E", "criterios do item 7", lambda L: criterios("E", L) or marca_ok("E8"), ok_arq("E8")),
        # G (item 3)
        ("G1", "G", "ladrilhos degradados (ruido, borrao, JPEG) dos corpora S-nadir-150 e S-oblique-six",
         lambda L: varios(*[(roda, [PY, j(SCR, "degrada_ladrilhos.py"), "--src", j(RAIZ, a), "--out", j(RAIZ, b)], L) for a, b in DEG]),
         j(RAIZ, DEG[1][1], "data.yaml")),
        ("G2", "G", "treino s_nadir_4k_deg",
         lambda L: treina("s_nadir_4k_deg", j(RAIZ, "ds_morro_4k_deg_tiles", "data.yaml"), MODELO, EPOCAS, True, L), tr("s_nadir_4k_deg")),
        ("G3", "G", "treino s_oblvar_deg",
         lambda L: treina("s_oblvar_deg", j(RAIZ, "ds_oblvar_deg_tiles", "data.yaml"), MODELO, EPOCAS, True, L), tr("s_oblvar_deg")),
        ("G4", "G", "ZS, PREDS no VisDrone e na HERIDAL dos dois",
         lambda L: zs_preds(["s_nadir_4k_deg", "s_oblvar_deg"], L, "G4", heridal=True), ok_arq("G4")),
        ("G5", "G", "criterios do item 3", lambda L: criterios("G", L) or marca_ok("G5"), ok_arq("G5")),
    ]
    # T: sementes 1 e 2
    k = 1
    for s in (1, 2):
        for nome, ds in (("armado_35_e120", "ds_armado_35_tiles"), ("armado_75g_e120", "ds_armado_75g_tiles")):
            E.append((f"T{k}", "T", f"treino {nome}_sd{s}", (lambda nome, ds, s: lambda L: treina_longo(f"{nome}_sd{s}", ds, L, s))(nome, ds, s),
                      tr(f"{nome}_sd{s}")))
            k += 1
    E.append(("T5", "T", "confusao das sementes de Q (val e novos)",
              lambda L: varios(*[(conf_par, f"{n}_sd{s}", d, L) for s in (1, 2)
                                 for n, d in (("armado_35_e120", "ds_armado_35"), ("armado_75g_e120", "ds_armado_75g"))])
              or marca_ok("T5"), ok_arq("T5")))
    k = 6
    for s in (1, 2):
        for nome, ds in (("s_nadir_4k_deg", "ds_morro_4k_deg_tiles"), ("s_oblvar_deg", "ds_oblvar_deg_tiles")):
            E.append((f"T{k}", "T", f"treino {nome}_sd{s}",
                      (lambda nome, ds, s: lambda L: treina(f"{nome}_sd{s}", j(RAIZ, ds, "data.yaml"), MODELO, EPOCAS, True, L, s))(nome, ds, s),
                      tr(f"{nome}_sd{s}")))
            k += 1
    E.append(("T10", "T", "ZS, PREDS VisDrone e HERIDAL das sementes de G",
              lambda L: zs_preds([f"{n}_sd{s}" for s in (1, 2) for n in ("s_nadir_4k_deg", "s_oblvar_deg")], L, "T10", heridal=True),
              ok_arq("T10")))
    for s in (1, 2):
        E.append((f"T{10 + s}", "T", f"treino s_semsol_4k_sd{s}",
                  (lambda s: lambda L: treina(f"s_semsol_4k_sd{s}", j(RAIZ, "ds_semsol_4k_tiles", "data.yaml"), MODELO, EPOCAS, True, L, s))(s),
                  tr(f"s_semsol_4k_sd{s}")))
    E += [
        ("T13", "T", "por regime das sementes do espelho",
         lambda L: varios((por_regime, "s_semsol_4k_sd1", L), (por_regime, "s_semsol_4k_sd2", L)) or marca_ok("T13"), ok_arq("T13")),
        ("T14", "T", "criterios com as sementes (Q, G, E)", lambda L: criterios("tudo", L) or marca_ok("T14"), ok_arq("T14")),
        # V (item 9)
        ("V1", "V", "lista do VisDrone train menos a fatia sel", lista_cheio, j(VIS, "visdrone_yolo", "data_cheio_sel.yaml")),
        ("V2", "V", "treino r_cheio_sel (6.147 imagens, selecao em sel)",
         lambda L: treina("r_cheio_sel", j(VIS, "visdrone_yolo", "data_cheio_sel.yaml"), MODELO, EPOCAS, True, L), tr("r_cheio_sel")),
        ("V3", "V", "ZS e PREDS do r_cheio_sel", lambda L: zs_preds(["r_cheio_sel"], L, "V3"), ok_arq("V3")),
        ("Y1", "Y", "todos os criterios do PLANO-RODADA6", lambda L: criterios("tudo", L) or marca_ok("Y1"), ok_arq("Y1")),
    ]
    return E


ETAPAS = etapas()


def trava():
    import psutil
    if os.path.exists(TRAVA):
        try:
            pid = int(open(TRAVA).read().strip())
            if pid != os.getpid() and psutil.pid_exists(pid) and any(
                    os.path.basename(a) == "rodada6.py" for a in psutil.Process(pid).cmdline()):
                return False
        except (ValueError, OSError, psutil.Error):
            pass
    with open(TRAVA, "w") as f:
        f.write(str(os.getpid()))
    return True


def solta():
    try:
        os.remove(TRAVA)
    except OSError:
        pass


def executa(eid, g, desc, fn, prova):
    nome_log = f"{eid}_{desc.split()[0].strip(':,')}.log"
    if DRY:
        print(f"[{eid}] ({g}) {desc}", flush=True)
        try:
            fn(nome_log)
        except Exception as exc:
            print(f"      ! excecao no dry-run: {exc!r}", flush=True)
            return 1
        return 0
    log(f"[{eid}] {desc}")
    marca(eid, estado="rodando", desc=desc, inicio=datetime.now().isoformat(timespec="seconds"))
    t0 = time.time()
    rc = 1
    for tentativa in (1, 2):
        try:
            rc = fn(nome_log)
        except Exception as exc:
            log(f"  excecao: {exc!r}")
            rc = 1
        if rc == DISPENSADA:
            marca_ok(eid)
            break
        if rc == 0 and os.path.exists(prova):
            break
        if rc == 0:
            rc = 1
            log("  terminou sem gerar a prova")
        log(f"  tentativa {tentativa} falhou (rc={rc})")
    dt = round(time.time() - t0)
    if rc == DISPENSADA:
        marca(eid, estado="dispensada", segundos=dt, fim=datetime.now().isoformat(timespec="seconds"))
        log(f"[{eid}] dispensada")
    elif rc == 0:
        marca(eid, estado="ok", segundos=dt, fim=datetime.now().isoformat(timespec="seconds"))
        log(f"[{eid}] ok em {dt / 60:.1f} min")
    else:
        marca(eid, estado=f"falhou_rc{rc}", segundos=dt)
        log(f"[{eid}] FALHOU; o resto do grupo {g} fica para a proxima retomada")
    return rc


def main():
    global DRY
    DRY = "--dry-run" in sys.argv
    so = None
    if "--so" in sys.argv:
        so = set(sys.argv[sys.argv.index("--so") + 1].split(","))
    if not DRY:
        os.makedirs(FILA, exist_ok=True)
    if "--listar" in sys.argv:
        e = carrega()
        for eid, g, desc, _, prova in ETAPAS:
            st = "feita" if os.path.exists(prova) else e.get(eid, {}).get("estado", "pendente")
            print(f"{eid:<5} {g:<3} {desc:<90} {st}")
        return 0
    if DRY:
        print("DRY-RUN: nada e executado nem gravado; etapas com prova sao puladas.", flush=True)
    elif not trava():
        print("outra instancia da rodada6 ja esta rodando", flush=True)
        return 0
    if not DRY:
        log("rodada6: inicio (ou retomada)" + (f", so os grupos {sorted(so)}" if so else ""))
        if so is None:
            e = carrega()
            e.pop("fim", None)
            e.pop("grupos_com_falha", None)
            grava(e)
    grupo_falhou = set()
    for eid, g, desc, fn, prova in ETAPAS:
        if so is not None and g not in so:
            continue
        if os.path.exists(PAUSA) and not DRY:
            log("PAUSA presente: a cadeia para antes da proxima etapa (sem gravar fim)")
            solta()
            return 0
        if os.path.exists(prova):
            if not DRY and carrega().get(eid, {}).get("estado") not in ("ok", "dispensada"):
                marca(eid, estado="ok", desc=desc)
            continue
        if g in grupo_falhou:
            marca(eid, estado="pulada", desc=desc)
            continue
        rc = executa(eid, g, desc, fn, prova)
        if rc not in (0, DISPENSADA) and not DRY:
            grupo_falhou.add(g)
            if g == "P" and eid == "P1":
                break
    if DRY:
        return 0
    if "P" in grupo_falhou and not os.path.exists(ok_arq("P1")):
        log("rodada6: a checagem de partida (P1) falhou; nada mais roda. Corrigir e relancar.")
    if so is None:
        e = carrega()
        e["fim"] = datetime.now().isoformat(timespec="seconds")
        e["grupos_com_falha"] = sorted(grupo_falhou)
        grava(e)
    log("rodada6: encerrada" + (f" com falha nos grupos {sorted(grupo_falhou)}" if grupo_falhou else "")
        + (" (execucao parcial, sem fim)" if so is not None else ""))
    solta()
    return 1 if grupo_falhou else 0


if __name__ == "__main__":
    sys.exit(main())
