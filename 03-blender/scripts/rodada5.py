#!/usr/bin/env python3
"""
rodada5.py: a rodada 5 (partida em 19/10/2026), em uma cadeia so, idempotente e retomavel.

Desenho, criterios fixados antes de rodar e custo em 03-blender/PLANO-RODADA5.md (secoes 2 a 6). Molde
das rodadas 3 e 4: cada etapa tem um arquivo de prova e, se ele existe, a etapa e pulada; render retoma
pelo numero de linhas do manifest (--start); treino retoma do last.pt e so conta como feito com
TREINO_OK (o best.pt existe desde a primeira epoca e nao serve de prova). Uma trava (fila5/rodada5.trava,
com o PID) impede duas instancias. Duas tentativas por etapa; se uma etapa falha, o resto do grupo e
pulado e os outros grupos seguem. Excecao: falha no grupo P grava `fim` com grupos_com_falha = ["P"] e
sai sem rodar nada (o supervisor sai junto). Com fila5/PAUSA presente a cadeia sai antes da proxima
etapa, sem gravar `fim`.

Estados novos: `aguardando_dado` (grupo N sem o data.yaml convertido da base nadir: nao e falha nem
prova; a cadeia segue, tenta de novo no fim e, se o dado ainda faltar, grava `fim` e o log diz para
rodar `python rodada5.py` depois da conversao) e `dispensada` (etapa condicional que a regra do plano
dispensou: M5 a M8 quando M4 passa, controles novos do ajuste fino quando F0 reproduz, sementes de F15
quando a celula escolhida e a original; grava a prova).

Grupos, na ordem pedida pelo autor (secao 1 do plano):
  P   checagem de partida: disco, GPU, caminhos, nomes livres, um quadro de teste com MPFB
  S   R5-1: sementes de treino 1 e 2 para S-nadir-150 e S-oblique
  F   R5-5: ajuste fino com extrator congelado e taxa menor (grade 2 x 2, dois inicios, 5 e 10%)
  N   R5-6: zero-shot numa base real nadir (HERIDAL), so se o data.yaml convertido existir
  Y1  criterios do bloco de validade (S, F, N)
  A   R5-3: curva de aprendizado sobre o numero de quadros (S-oblique-six)
  D   R5-4: ablacao so com sol duro
  M   R5-7: tres classes a 150 m que passe a condicao de validade (ramo caro condicional)
  C   R5-2: semente de cena para S-oblique-six (duas replicas)
  Y2  VisDrone oficial dos modelos novos, reamostragem, resolubilidade, todos os criterios

Uso:  python rodada5.py              (roda o que falta)
      python rodada5.py --listar     (mostra as etapas e o estado)
      python rodada5.py --dry-run    (imprime o comando de cada etapa pendente, sem executar nada)
      python rodada5.py --so P       (roda so os grupos dados, sem gravar `fim`; para testar a partida)
"""
import csv
import glob
import json
import os
import random
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
FILA = os.path.join(RAIZ, "fila5")
LOG = os.path.join(RAIZ, "rodada5.log")
ESTADO = os.path.join(FILA, "estado.json")
TRAVA = os.path.join(FILA, "rodada5.trava")
PAUSA = os.path.join(FILA, "PAUSA")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
BLENDER = os.path.join("C:" + os.sep, "Program Files (x86)", "Steam", "steamapps", "common",
                       "Blender", "blender.exe")
VIS_YAML = os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "visdrone_yolo", "data.yaml")
FT = os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "ft")
HERIDAL_YAML = os.path.join("C:" + os.sep, "arma3-favela", "real_nadir", "heridal", "yolo", "data.yaml")

# mesma receita de todos os bracos (secao 2.1 do plano)
MODELO, IMGSZ, EPOCAS, BATCH, WORKERS = "yolo11s.pt", 1280, 60, 6, 4
EPOCAS_FT = 30
DISCO_MIN_GB = 50
DRY = False

# listas de argumentos do gerador, identicas as dos corpora originais (secao 2.2)
NADIR4K = ["--samples", 96, "--res", 3840, 2160, "--people", 16, 34, "--pool", 6, "--seed", 21,
           "--climas", "todos", "--sitio", -1, "--mistura", 0.5, 0.5, 0.0, "--enquadro", "quadrado"]
SITIOS = [-1, 0, 1, 2, 3, 4]
POR_SITIO = 30


def oblvar(semente, sitio):
    """o comando de ds_oblvar (rodada 3) com a semente de cena e o sitio dados"""
    return ["--samples", 96, "--res", 3840, 2160, "--people", 16, 34, "--pool", 6, "--seed", semente,
            "--climas", "todos", "--obliqua", "--pitch-obl", 45, 56, "--camera-livre",
            "--mistura", 0, 1, 0, "--sitio", sitio]


# o comando de ds_armado_35, mudando so a altura e o jitter (3 x 150 / 35 = 12,9): o de ds_armado_150g
GEMEO150 = ["--samples", 64, "--res", 3840, 2160, "--people", 12, 24, "--pool", 6, "--seed", 43,
            "--climas", "todos", "--alt", 150, "--alt-jitter", 13, "--mistura", 0.34, 0.33, 0.33,
            "--porte-realista", "--fio-gsd", "--laje", 0.75, "--amostra-no-quadro"]


def climas(cmd, valor):
    c = list(cmd)
    c[c.index("--climas") + 1] = valor
    return c


# ajuste fino (secao 3.2): o otimizador explicito igual ao que o auto escolhia, e as celulas da grade
OPT = ["--optimizer", "AdamW", "--momentum", 0.9, "--warmup-bias-lr", 0.0]
CELULA = {"orig": ["--freeze", 0, "--lr0", 0.002], "fz": ["--freeze", 11, "--lr0", 0.002],
          "lr": ["--freeze", 0, "--lr0", 0.0002], "fzlr": ["--freeze", 11, "--lr0", 0.0002]}
NOVAS = ("fz", "lr", "fzlr")
INICIOS = ("sint", "coco")
REF_FT05_COCO = 0.5220            # mAP50 do ft05_coco (sim2real_ft05_coco.json)
TOL_REPRODUCAO = 0.0035           # desvio entre as tres sementes do ft05_coco

CURVA = (30, 60, 90, 120)
LISTA_N = ["s_nadir_4k", "s_nadir_4k_sd1", "s_nadir_4k_sd2", "s_variedade", "s_obliquo", "s_obliquo_sd1",
           "s_obliquo_sd2", "s_oblvar", "s_oblvar_sd1", "s_oblvar_sd2", "r_pareado", "armado_150g"]

# runs que esta rodada cria (o grupo P confere que nenhum existe antes da partida)
RUNS_NOVOS = (["s_nadir_4k_sd1", "s_nadir_4k_sd2", "s_obliquo_sd1", "s_obliquo_sd2", "ft05_coco_rep",
               "ft05_sint_rep", "ft10_coco_rep", "ft10_sint_rep"]
              + [f"ft{f}_{i}_{c}" for f in ("05", "10") for i in INICIOS for c in NOVAS]
              + [f"ft05_{i}_{c}_sd{s}" for i in INICIOS for c in NOVAS for s in (1, 2)]
              + [f"s_oblvar_c{n:03d}" for n in CURVA] + [f"s_oblvar_c{n:03d}_sd{s}" for n in (30, 120) for s in (1, 2)]
              + ["s_soldur_4k", "armado_150g_e120", "armado_150g_600", "s_oblvar_e22", "s_oblvar_e23"])


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
    """no dry-run, explica uma etapa interna ou condicional"""
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


DISPENSADA = -200                 # codigo de retorno: etapa condicional dispensada pela regra do plano


# ------------------------------------------------------------------ primitivas idempotentes
def render(nome_log, out, n, extra, inicio=0):
    """n quadros a partir do indice `inicio` do comando `extra` (com inicio > 0 o gerador sorteia sem
    renderizar os quadros anteriores, entao os novos continuam a sequencia do corpus original)"""
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
    return roda([PY, j(SCR, "tile_dataset.py"), "--data", ds, "--out", ds_t,
                 "--tile", 1280, "--overlap", 0.2], nome_log)


def pesos(nome):
    return j(RAIZ, "runs", "detect", nome, "weights", "best.pt")


def treinado(nome):
    return os.path.exists(j(RAIZ, "runs", "detect", nome, "TREINO_OK"))


def treina(nome, data, modelo, epocas, single, nome_log, semente=0, extra=(), paciencia=None):
    rd = j(RAIZ, "runs", "detect", nome)
    ok = j(rd, "TREINO_OK")
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
        log(f"  treino {nome}: do zero, a partir de {os.path.basename(str(modelo))}, semente {semente}")
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


def avalia(nome, nome_log, sint=None, imgsz=IMGSZ):
    """ZS: zero-shot no VisDrone val (secao 2.2)"""
    saida = j(RES, f"sim2real_{nome}.json")
    if os.path.exists(saida):
        return 0
    cmd = [PY, j(SCR, "avalia_sim2real.py"), "--weights", pesos(nome), "--real", VIS_YAML,
           "--imgsz", imgsz, "--out", saida] + (["--sintetico", sint] if sint else [])
    return roda(cmd, nome_log)


def preds(runs, nome_log):
    """PREDS: predicoes por imagem no VisDrone val, FP32, lote 4 (visdrone_preds.py, em REV)"""
    falta = [r for r in runs if not os.path.exists(j(REV, f"preds_visdrone_{r}.npz"))]
    if not falta:
        return 0
    rc = roda([PY, j(REV, "visdrone_preds.py"), "--modelos", *falta, "--batch", 4], nome_log)  # cwd RAIZ: as pastas val-N do validador caem em RAIZ/runs, como sempre
    if DRY:
        return rc
    sem = [r for r in falta if not os.path.exists(j(REV, f"preds_visdrone_{r}.npz"))]
    if sem:
        log(f"  preds sem saida para {sem}")
        return rc or 1
    return rc


def oficial(runs, nome_log):
    """OFICIAL: regra oficial do VisDrone e IoU 0,50/0,60/0,75, acrescentando ao JSON existente"""
    saida = j(RES, "visdrone_oficial_iou.json")
    d = le(saida) or {}
    falta = [r for r in runs if r not in d.get("modelos", {})]
    if not falta:
        return 0
    rc = roda([PY, j(RES, "avalia_visdrone_oficial.py"), "--modelos", *falta, "--out", saida], nome_log)
    if DRY:
        return rc
    d = le(saida) or {}
    sem = [r for r in falta if r not in d.get("modelos", {})]
    if sem:
        log(f"  oficial sem saida para {sem}")
        return rc or 1
    return rc


def confusao(nome, ds, split, saida, nome_log):
    """CONF: imagem inteira, imgsz 3840, conf 0,25, IoU 0,50, com instancias"""
    if os.path.exists(j(RES, saida)):
        return 0
    return roda([PY, j(RES, "confusao_armado.py"), "--pesos", pesos(nome), "--ds", ds, "--split", split,
                 "--instancias", "--out", j(RES, saida)], nome_log)


def varios(*chamadas):
    """roda uma lista de (funcao, args) em ordem e para no primeiro rc != 0"""
    for fn, *a in chamadas:
        rc = fn(*a)
        if rc != 0:
            return rc
    return 0


def zs_preds(runs, L, eid, sint=None):
    rc = varios(*[(avalia, r, L, sint) for r in runs], (preds, runs, L))
    return marca_ok(eid) if rc == 0 else rc


# ------------------------------------------------------------------ grupo P
def preflight(L):
    """P1: disco, GPU livre, venv, caminhos, pesos e corpora, nomes de run livres"""
    if DRY:
        nota(f"funcao interna: disco >= {DISCO_MIN_GB} GB em C:, nvidia-smi (memoria < 1 GB, utilizacao < 10%), "
             "venv (ultralytics 8.4.148, torch 2.14, CUDA), BL, PY, VIS, FT, yolo11s.pt, corpora, pesos, nomes livres")
        return 0
    prob, info = [], {}
    livre = shutil.disk_usage("C:" + os.sep).free / 1e9
    info["disco_livre_gb"] = round(livre, 1)
    if livre < DISCO_MIN_GB:
        prob.append(f"disco livre {livre:.0f} GB < {DISCO_MIN_GB}")
    try:
        amostras = []
        for _ in range(5):
            s = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used,utilization.gpu",
                                         "--format=csv,noheader,nounits"], text=True, timeout=30)
            mem, util = [float(x) for x in s.strip().splitlines()[0].split(",")]
            amostras.append((mem, util))
            time.sleep(1)
        mem = sorted(a for a, _ in amostras)[2]
        util = sorted(b for _, b in amostras)[2]
        info["gpu_memoria_mb_mediana"], info["gpu_utilizacao_mediana"] = mem, util
        if mem >= 1024:
            prob.append(f"GPU com {mem:.0f} MB em uso (>= 1 GB)")
        if util >= 10:
            prob.append(f"GPU com utilizacao {util:.0f}% (>= 10%)")
    except Exception as exc:
        prob.append(f"nvidia-smi falhou: {exc!r}")
    try:
        v = subprocess.check_output([PY, "-c", "import ultralytics, torch; print(ultralytics.__version__, "
                                     "torch.__version__, torch.cuda.is_available())"], text=True, timeout=300).split()
        info["venv"] = v
        if v[0] != "8.4.148" or not v[1].startswith("2.14") or v[2] != "True":
            prob.append(f"venv inesperado: {v}")
    except Exception as exc:
        prob.append(f"venv falhou: {exc!r}")
    caminhos = [BLENDER, PY, VIS_YAML, j(FT, "ft05.yaml"), j(FT, "ft10.yaml"), j(RAIZ, MODELO),
                j(SCR, "gen_morro.py"), j(SCR, "train_yolo_win.py"), j(SCR, "tile_dataset.py")]
    caminhos += [j(RAIZ, d, "data.yaml") for d in ("ds_morro_4k_tiles", "ds_morro_obl_tiles", "ds_oblvar",
                                                    "ds_oblvar_tiles", "ds_regime_4k", "ds_regime_4k_tiles",
                                                    "ds_armado_150g", "ds_armado_150g_tiles")]
    caminhos += [j(RAIZ, "ds_oblvar", "manifest.jsonl"), j(RAIZ, "ds_regime_4k", "manifest.jsonl")]
    caminhos += [pesos(r) for r in ("s_nadir_4k", "s_variedade", "s_obliquo", "s_oblvar", "s_oblvar_sd1",
                                    "s_oblvar_sd2", "r_pareado", "armado_150g", "armado_35", "armado_75g",
                                    "ft05_sint", "ft05_sint_sd1", "ft05_sint_sd2", "ft05_coco", "ft05_coco_sd1",
                                    "ft05_coco_sd2", "ft10_sint", "ft10_coco")]
    caminhos += [j(RES, f) for f in ("extra_armado_35.json", "extra_armado_75g.json", "sim2real_ft05_coco.json")]
    falta = [c for c in caminhos if not os.path.exists(c)]
    if falta:
        prob.append("faltando: " + "; ".join(falta))
    ocupados = [r for r in RUNS_NOVOS if os.path.exists(j(RAIZ, "runs", "detect", r))]
    if ocupados:
        prob.append("runs novos ja existem (o treino 'retomaria' um run alheio): " + ", ".join(ocupados))
    info["heridal_data_yaml"] = os.path.exists(HERIDAL_YAML)
    info["problemas"] = prob
    info["quando"] = datetime.now().isoformat(timespec="seconds")
    grava_json(j(FILA, "P1.json"), info)
    for p in prob:
        log(f"  P1: {p}")
    log(f"  P1: disco {info['disco_livre_gb']} GB, GPU {info.get('gpu_memoria_mb_mediana')} MB / "
        f"{info.get('gpu_utilizacao_mediana')}%, venv {info.get('venv')}, HERIDAL convertida: {info['heridal_data_yaml']}")
    return 1 if prob else marca_ok("P1")


def teste_mpfb(L):
    """P2: um quadro de NADIR4K num diretorio de teste, refeito do zero a cada partida"""
    out = j(RAIZ, "_teste_mpfb")
    if not DRY:
        shutil.rmtree(out, ignore_errors=True)
    rc = render(L, out, 1, NADIR4K)
    if DRY or rc != 0:
        return rc
    mf = [json.loads(x) for x in open(j(out, "manifest.jsonl"), encoding="utf-8") if x.strip()]
    rot = glob.glob(j(out, "labels", "*", "*.txt"))
    caixas = sum(linhas(r) for r in rot)
    cauda = open(j(FILA, L), encoding="utf-8", errors="replace").read()[-200000:]
    pool = [ln for ln in cauda.splitlines() if "pool MPFB:" in ln]
    pessoas = mf[0]["n_pessoas"] if mf else 0
    log(f"  P2: {pessoas} pessoas na cena, {caixas} caixas no rotulo, {pool[-1].strip() if pool else 'sem linha do pool MPFB'}")
    if pessoas < 16 or caixas == 0 or not pool or " 0 humanos" in pool[-1]:
        log("  P2: o Blender nao carregou o MPFB (ou o quadro saiu vazio)")
        return 1
    grava_json(j(FILA, "P2.json"), {"pessoas": pessoas, "caixas": caixas, "pool": pool[-1].strip(),
                                    "quando": datetime.now().isoformat(timespec="seconds")})
    return marca_ok("P2")


# ------------------------------------------------------------------ grupo F
def ft_inicio(ini, semente=0):
    if ini == "coco":
        return MODELO
    return pesos("s_oblvar" if semente == 0 else f"s_oblvar_sd{semente}")


def ft_treina(fatia, ini, cel, L, semente=0, nome=None):
    nome = nome or (f"ft{fatia}_{ini}_{cel}" + (f"_sd{semente}" if semente else ""))
    base = ft_inicio(ini, semente)
    if ini == "sint" and not DRY and not os.path.exists(base):
        log(f"  {nome}: falta o peso de partida {base}")
        return 1
    return treina(nome, j(FT, f"ft{fatia}.yaml"), base, EPOCAS_FT, True, L, semente, OPT + CELULA[cel])


def map50_real(nome):
    d = le(j(RES, f"sim2real_{nome}.json"))
    if not d:
        return None
    return next((r.get("metrics/mAP50(B)") for r in d["resultados"] if r.get("conjunto") == "real"), None)


def ft_reproducao(L):
    """F0 (checagem): ft05_coco_rep a ate 0,0035 dos 0,5220 do ft05_coco"""
    rc = avalia("ft05_coco_rep", L)
    if rc != 0:
        return rc
    if DRY:
        nota(f"funcao interna: |mAP50(ft05_coco_rep) - {REF_FT05_COCO}| <= {TOL_REPRODUCAO} -> rodada5_ft_reproducao.json")
        return 0
    ref = map50_real("ft05_coco") or REF_FT05_COCO
    v = map50_real("ft05_coco_rep")
    reproduz = v is not None and abs(v - ref) <= TOL_REPRODUCAO
    grava_json(j(RES, "rodada5_ft_reproducao.json"),
               {"ft05_coco": ref, "ft05_coco_rep": v, "dif": None if v is None else round(v - ref, 4),
                "tolerancia": TOL_REPRODUCAO, "reproduz": reproduz,
                "regra": "PLANO-RODADA5.md 3.2: com o otimizador explicito igual ao do auto, ft05_coco_rep tem de ficar a "
                         "ate 0,0035 do ft05_coco; senao a celula de controle passa a ser a _rep e entram controles novos "
                         "a 10% e para o inicio sintetico",
                "quando": datetime.now().isoformat(timespec="seconds")})
    log(f"  reproducao: ft05_coco_rep {v} contra {ref}: {'reproduz' if reproduz else 'NAO reproduz'}")
    return 0


def reproduz():
    d = le(j(RES, "rodada5_ft_reproducao.json"))
    return True if d is None else bool(d.get("reproduz"))


def ft_controles(L):
    """F12b: so se F0 nao reproduziu: controles novos (5% sintetico, 10% generico e sintetico)"""
    if DRY:
        nota("condicional: so se rodada5_ft_reproducao.json disser reproduz = false; senao 'dispensada'")
        return varios((ft_treina, "05", "sint", "orig", L, 0, "ft05_sint_rep"),
                      (ft_treina, "10", "coco", "orig", L, 0, "ft10_coco_rep"),
                      (ft_treina, "10", "sint", "orig", L, 0, "ft10_sint_rep"))
    if reproduz():
        return DISPENSADA
    rc = varios((ft_treina, "05", "sint", "orig", L, 0, "ft05_sint_rep"),
                (ft_treina, "10", "coco", "orig", L, 0, "ft10_coco_rep"),
                (ft_treina, "10", "sint", "orig", L, 0, "ft10_sint_rep"))
    return marca_ok("F12b") if rc == 0 else rc


def runs_ft_grade():
    runs = ["ft05_coco_rep"] + [f"ft{f}_{i}_{c}" for f in ("05", "10") for c in NOVAS for i in INICIOS]
    if not reproduz() or DRY:
        runs += ["ft05_sint_rep", "ft10_coco_rep", "ft10_sint_rep"]
    return runs


def ft_avalia(L):
    """F13: ZS e PREDS dos treze (e dos controles novos, se entraram)"""
    runs = runs_ft_grade()
    falta = [r for r in runs if not DRY and not treinado(r)]
    if falta:
        log(f"  F13: runs sem TREINO_OK: {falta}")
        return 1
    return zs_preds(runs, L, "F13")


def melhor_sel(run):
    """mAP50-95 em sel do best.pt = o maximo da coluna (fitness do Ultralytics 8.4 = mAP50-95)"""
    f = j(RAIZ, "runs", "detect", run, "results.csv")
    if not os.path.exists(f):
        return None
    v = []
    for r in csv.DictReader(open(f, encoding="utf-8")):
        r = {k.strip(): x for k, x in r.items()}
        try:
            v.append(float(r["metrics/mAP50-95(B)"]))
        except (KeyError, ValueError):
            pass
    return round(max(v), 4) if v else None


def selecao_ft(L):
    """F14: para cada inicio e fatia, a celula com maior mAP50-95 em sel; empate a 4 casas fica a original"""
    if DRY:
        nota("funcao interna: le results.csv das celulas (orig, fz, lr, fzlr) -> rodada5_ft_selecao.json")
        return 0
    rep = reproduz()
    out = {"regra": "PLANO-RODADA5.md 3.2: celula cujo best.pt tem maior mAP50-95 em sel; empate a quatro casas fica a "
                    "original; o teste nunca escolhe", "reproduz": rep, "celulas": {}, "runs": {}, "escolha": {}}
    for f in ("05", "10"):
        out["celulas"][f], out["runs"][f], out["escolha"][f] = {}, {}, {}
        for ini in INICIOS:
            runs = {"orig": f"ft{f}_{ini}" if rep else f"ft{f}_{ini}_rep"}
            runs.update({c: f"ft{f}_{ini}_{c}" for c in NOVAS})
            vals = {c: melhor_sel(r) for c, r in runs.items()}
            validos = {c: v for c, v in vals.items() if v is not None}
            if "orig" not in validos:
                log(f"  F14: falta o results.csv do controle {runs['orig']}")
                return 1
            topo = max(validos.values())
            esc = "orig" if validos["orig"] == topo else next(c for c in NOVAS if validos.get(c) == topo)
            out["celulas"][f][ini], out["runs"][f][ini], out["escolha"][f][ini] = vals, runs, esc
            log(f"  F14: {f}% {ini}: {vals} -> {esc}")
    out["quando"] = datetime.now().isoformat(timespec="seconds")
    grava_json(j(RES, "rodada5_ft_selecao.json"), out)
    return 0


def runs_f15():
    sel = le(j(RES, "rodada5_ft_selecao.json"))
    if not sel:
        return []
    return [(ini, sel["escolha"]["05"][ini], s) for ini in INICIOS if sel["escolha"]["05"][ini] != "orig" for s in (1, 2)]


def ft_sementes(L):
    """F15: sementes 1 e 2 da celula escolhida a 5%, para os dois inicios, se nao for a original"""
    if DRY:
        nota("condicional: para cada inicio cuja escolha a 5% nao e 'orig', ft05_<inicio>_<celula>_sd1 e _sd2 "
             "(o sintetico da semente s parte de s_oblvar_sd<s>); senao 'dispensada'. Exemplo com a celula fz:")
        return varios(*[(ft_treina, "05", ini, "fz", L, s) for ini in INICIOS for s in (1, 2)])
    if not le(j(RES, "rodada5_ft_selecao.json")):
        log("  F15: falta rodada5_ft_selecao.json")
        return 1
    alvo = runs_f15()
    if not alvo:
        return DISPENSADA
    rc = varios(*[(ft_treina, "05", ini, cel, L, s) for ini, cel, s in alvo])
    return marca_ok("F15") if rc == 0 else rc


def ft_avalia_sementes(L):
    if DRY:
        nota("condicional: ZS e PREDS dos runs de F15; 'dispensada' se F15 foi dispensada")
        return zs_preds([f"ft05_{ini}_fz_sd{s}" for ini in INICIOS for s in (1, 2)], L, "F16")
    runs = [f"ft05_{ini}_{cel}_sd{s}" for ini, cel, s in runs_f15()]
    if not runs:
        return DISPENSADA
    return zs_preds(runs, L, "F16")


# ------------------------------------------------------------------ grupo N
def n_escala(L):
    return roda([PY, "-I", j(RES, "escala_nadir.py"), "--data", HERIDAL_YAML, "--alvo", 20.55,
                 "--out", j(RES, "escala_heridal.json")], L)


def n_preds(L):
    e = le(j(RES, "escala_heridal.json"))
    casado = e["imgsz_casado"] if e else "<imgsz_casado de escala_heridal.json>"
    rc = varios((roda, [PY, j(REV, "preds_nadir.py"), "--data", HERIDAL_YAML, "--tag", "heridal", "--imgsz", casado,
                        "--modelos", *LISTA_N, "--batch", 4], L),
                (roda, [PY, j(REV, "preds_nadir.py"), "--data", HERIDAL_YAML, "--tag", "heridal_1280", "--imgsz", 1280,
                        "--modelos", *LISTA_N, "--batch", 4], L))
    return marca_ok("N2") if rc == 0 else rc


def n_bootstrap(L):
    rc = varios((roda, [PY, j(REV, "bootstrap_nadir.py"), "--tag", "heridal"], L),
                (roda, [PY, j(REV, "bootstrap_nadir.py"), "--tag", "heridal_1280"], L))
    return marca_ok("N3") if rc == 0 else rc


# ------------------------------------------------------------------ grupos Y
def bootstrap_r5(L):
    return varios((roda, [PY, j(REV, "bootstrap_visdrone.py"), "--sufixo", "r5"], L),
                  (roda, [PY, j(REV, "resolvivel.py"), "--sufixo", "r5"], L))


def criterios(parte, L):
    return roda([PY, j(RES, "rodada5_criterios.py"), "--parte", parte], L)


def y1(L):
    rc = varios((bootstrap_r5, L), (criterios, "prioridade", L))
    return marca_ok("Y1") if rc == 0 else rc


def runs_novos_unica():
    """modelos novos de classe unica que existem (para o VisDrone oficial)"""
    return [r for r in RUNS_NOVOS if r not in ("armado_150g_e120", "armado_150g_600") and (DRY or treinado(r))]


def y2(L):
    rc = oficial(runs_novos_unica(), L)
    return marca_ok("Y2") if rc == 0 else rc


def y3(L):
    rc = bootstrap_r5(L)
    return marca_ok("Y3") if rc == 0 else rc


def y4(L):
    rc = criterios("tudo", L)
    return marca_ok("Y4") if rc == 0 else rc


# ------------------------------------------------------------------ grupo A
def monta_curva(L):
    """A1: subconjuntos encaixados de 30, 60, 90 e 120 dos 152 quadros de treino de ds_oblvar, estratificados
    por sitio. De cada sitio, os quadros de treino em ordem de nome sorteada uma vez (random.Random(5), um
    gerador so, sitios em ordem); a ordem global intercala os sitios pela fracao (posicao + 0,5) / n do
    sitio, e o ponto N pega os N primeiros: encaixado por construcao e com a fracao N/152 de cada sitio
    (arredondada). Cada ponto leva todos os ladrilhos dos seus quadros, por link fisico; a validacao e a de
    ds_oblvar_tiles (os mesmos 144 ladrilhos em todos os pontos)."""
    if DRY:
        nota("funcao interna: ds_oblvar_c030_tiles ... c120_tiles por link fisico, val = ds_oblvar_tiles/images/val, "
             "RES/curva_subconjuntos.json")
        return 0
    src = j(RAIZ, "ds_oblvar")
    srct = j(RAIZ, "ds_oblvar_tiles")
    por_sitio = {k: [] for k in SITIOS}
    for ln in open(j(src, "manifest.jsonl"), encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            if r["split"] == "train":
                por_sitio[r["sitio"]].append(os.path.splitext(r["img"])[0])
    rnd = random.Random(5)
    chave = []
    for si, k in enumerate(SITIOS):
        q = sorted(por_sitio[k])
        rnd.shuffle(q)
        chave += [((p + 0.5) / len(q), si, nome, k) for p, nome in enumerate(q)]
    ordem = [(nome, k) for _, _, nome, k in sorted(chave)]
    total = len(ordem)
    ladrilhos = {}
    for f in os.listdir(j(srct, "images", "train")):
        ladrilhos.setdefault(os.path.splitext(f)[0].rsplit("_", 2)[0], []).append(f)
    out = {"regra": monta_curva.__doc__.strip(), "quadros_de_treino": total,
           "por_sitio_total": {str(k): len(v) for k, v in por_sitio.items()}, "pontos": {}}
    for n in CURVA:
        dst = j(RAIZ, f"ds_oblvar_c{n:03d}_tiles")
        escolhidos = ordem[:n]
        shutil.rmtree(dst, ignore_errors=True)
        os.makedirs(j(dst, "images", "train"))
        os.makedirs(j(dst, "labels", "train"))
        nl = 0
        for nome, _ in escolhidos:
            for f in ladrilhos.get(nome, []):
                try:
                    os.link(j(srct, "images", "train", f), j(dst, "images", "train", f))
                except OSError:
                    shutil.copy2(j(srct, "images", "train", f), j(dst, "images", "train", f))
                lab = os.path.splitext(f)[0] + ".txt"
                shutil.copy2(j(srct, "labels", "train", lab), j(dst, "labels", "train", lab))
                nl += 1
        with open(j(dst, "data.yaml"), "w", encoding="utf-8") as f:
            f.write(f"path: {dst.replace(os.sep, '/')}\ntrain: images/train\n"
                    f"val: {j(srct, 'images', 'val').replace(os.sep, '/')}\n"
                    "names:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
        out["pontos"][f"c{n:03d}"] = {"quadros": n, "ladrilhos_treino": nl,
                                      "por_sitio": {str(k): sum(1 for _, s in escolhidos if s == k) for k in SITIOS},
                                      "lista": [x for x, _ in escolhidos]}
        log(f"  curva c{n:03d}: {n} quadros, {nl} ladrilhos, por sitio {out['pontos'][f'c{n:03d}']['por_sitio']}")
    out["ladrilhos_treino_152"] = sum(len(v) for v in ladrilhos.values())
    out["quando"] = datetime.now().isoformat(timespec="seconds")
    grava_json(j(RES, "curva_subconjuntos.json"), out)
    return 0


def treina_curva(n, semente, L):
    nome = f"s_oblvar_c{n:03d}" + (f"_sd{semente}" if semente else "")
    return treina(nome, j(RAIZ, f"ds_oblvar_c{n:03d}_tiles", "data.yaml"), MODELO, EPOCAS, True, L, semente)


# ------------------------------------------------------------------ grupo D
def d_regime(L):
    rc = varios((roda, [PY, j(RES, "por_regime.py"), "--pesos", pesos("s_soldur_4k"), "--ds", j(RAIZ, "ds_regime_4k"),
                        "--tiles", j(RAIZ, "ds_regime_4k_tiles"), "--por-quadro",
                        "--out", j(RES, "por_regime_s_soldur_4k.json")], L),
                (roda, [PY, j(RES, "por_regime.py"), "--pesos", pesos("s_nadir_4k"), "--ds", j(RAIZ, "ds_regime_4k"),
                        "--tiles", j(RAIZ, "ds_regime_4k_tiles"), "--por-quadro",
                        "--out", j(RES, "por_regime_s_nadir_4k_r5.json")], L))
    return marca_ok("D4") if rc == 0 else rc


# ------------------------------------------------------------------ grupo M
def recall_qualquer(nome_arq):
    """fracao das pessoas anotadas encontradas em qualquer classe (coluna != perdida)"""
    d = le(j(RES, nome_arq))
    if not d or "instancias" not in d:
        return None, None
    n = len(d["instancias"])
    k = sum(1 for x in d["instancias"] if x[4] != 3)
    return (round(k / n, 4) if n else None), n


def validade_150(L):
    """M4: o armado_150g_e120 encontra pelo menos metade das pessoas no seu val E nos 80 quadros novos"""
    if DRY:
        nota("funcao interna: recall em qualquer classe >= 0,5 em confusao_armado_150g_e120.json e "
             "extra_armado_150g_e120.json -> RES/rodada5_validade_150.json")
        return 0
    rv, nv = recall_qualquer("confusao_armado_150g_e120.json")
    re_, ne = recall_qualquer("extra_armado_150g_e120.json")
    if rv is None or re_ is None:
        log("  M4: faltam as confusoes do armado_150g_e120")
        return 1
    valido = rv >= 0.5 and re_ >= 0.5
    grava_json(j(RES, "rodada5_validade_150.json"),
               {"modelo": "armado_150g_e120", "recall_qualquer_classe_val": rv, "pessoas_val": nv,
                "recall_qualquer_classe_quadros_novos": re_, "pessoas_quadros_novos": ne, "valido": valido,
                "regra": "PLANO-RODADA5.md 3.7: pelo menos metade das pessoas anotadas encontradas, em qualquer classe, "
                         "no val e nos 80 quadros independentes; se passa, M5 a M8 ficam dispensadas",
                "quando": datetime.now().isoformat(timespec="seconds")})
    log(f"  M4: recall val {rv} ({nv} pessoas), quadros novos {re_} ({ne}): {'VALIDO' if valido else 'nao valido'}")
    return 0


def m_valido():
    d = le(j(RES, "rodada5_validade_150.json"))
    return None if d is None else bool(d["valido"])


def condicional_m(eid, fn, L):
    """M5 a M8: so se M4 falhar a validade"""
    if DRY:
        nota("condicional: so se rodada5_validade_150.json disser valido = false; senao 'dispensada'")
        return fn(L)
    v = m_valido()
    if v is None:
        log(f"  {eid}: falta rodada5_validade_150.json")
        return 1
    if v:
        return DISPENSADA
    rc = fn(L)
    return marca_ok(eid) if rc == 0 else rc


def junta_150_600(L):
    """M6: ds_armado_150g (prefixo g_) + _armado_150g_mais (prefixo m_), por link fisico, e ladrilhos"""
    dst = j(RAIZ, "ds_armado_150g_600")
    if DRY:
        nota("funcao interna: junta ds_armado_150g e _armado_150g_mais em ds_armado_150g_600 (link fisico, prefixos g_ e m_)")
        return ladrilha(dst, dst + "_tiles", L)
    if not os.path.exists(j(dst, "data.yaml")):
        shutil.rmtree(dst, ignore_errors=True)
        for sub in ("images/train", "images/val", "labels/train", "labels/val"):
            os.makedirs(j(dst, *sub.split("/")), exist_ok=True)
        n = 0
        with open(j(dst, "manifest.jsonl"), "w", encoding="utf-8") as mf:
            for pre, par in (("g_", j(RAIZ, "ds_armado_150g")), ("m_", j(RAIZ, "_armado_150g_mais"))):
                for ln in open(j(par, "manifest.jsonl"), encoding="utf-8"):
                    if not ln.strip():
                        continue
                    r = json.loads(ln)
                    base = os.path.splitext(r["img"])[0]
                    src = j(par, "images", r["split"], r["img"])
                    d_img = j(dst, "images", r["split"], pre + base + ".png")
                    try:
                        os.link(src, d_img)
                    except OSError:
                        shutil.copy2(src, d_img)
                    shutil.copy2(j(par, "labels", r["split"], base + ".txt"), j(dst, "labels", r["split"], pre + base + ".txt"))
                    r["img"], r["origem"] = pre + base + ".png", os.path.basename(par)
                    mf.write(json.dumps(r) + "\n")
                    n += 1
        with open(j(RAIZ, "ds_armado_150g", "data.yaml"), encoding="utf-8") as f:
            nomes = f.read().split("names:", 1)[1]
        with open(j(dst, "data.yaml"), "w", encoding="utf-8") as f:
            f.write(f"path: {dst.replace(os.sep, '/')}\ntrain: images/train\nval: images/val\nnames:{nomes}")
        log(f"  ds_armado_150g_600: {n} quadros")
    return ladrilha(dst, dst + "_tiles", L)


# ------------------------------------------------------------------ grupo C
def junta_oblvar(semente, L):
    """C1/C5: seis sitios x 30 quadros com a semente de cena dada, juntados em ds_oblvar_e<semente>
    (a junta_oblvar da rodada 3 com a semente como parametro)"""
    dst = j(RAIZ, f"ds_oblvar_e{semente}")
    if os.path.exists(j(dst, "data.yaml")):
        return 0
    for k in SITIOS:
        rc = render(L, j(RAIZ, f"_oblvar_e{semente}_s{k}"), POR_SITIO, oblvar(semente, k))
        if rc != 0:
            log(f"  sitio {k} falhou rc={rc}")
            return rc
    if DRY:
        nota(f"funcao interna: junta os seis sitios em ds_oblvar_e{semente} (link fisico, prefixo s<sitio>_)")
        return 0
    shutil.rmtree(dst, ignore_errors=True)
    for sub in ("images/train", "images/val", "labels/train", "labels/val"):
        os.makedirs(j(dst, *sub.split("/")), exist_ok=True)
    n = 0
    with open(j(dst, "manifest.jsonl"), "w", encoding="utf-8") as mf:
        for k in SITIOS:
            par = j(RAIZ, f"_oblvar_e{semente}_s{k}")
            for ln in open(j(par, "manifest.jsonl"), encoding="utf-8"):
                if not ln.strip():
                    continue
                r = json.loads(ln)
                base = os.path.splitext(r["img"])[0]
                novo = f"s{str(k).replace('-', 'm')}_{base}"
                src = j(par, "images", r["split"], r["img"])
                d_img = j(dst, "images", r["split"], novo + ".png")
                try:
                    os.link(src, d_img)
                except OSError:
                    shutil.copy2(src, d_img)
                shutil.copy2(j(par, "labels", r["split"], base + ".txt"), j(dst, "labels", r["split"], novo + ".txt"))
                r["img"], r["sitio"] = novo + ".png", k
                mf.write(json.dumps(r) + "\n")
                n += 1
    with open(j(dst, "data.yaml"), "w", encoding="utf-8") as f:
        f.write("path: " + dst.replace(os.sep, "/") + "\ntrain: images/train\nval: images/val\n"
                "names:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
    log(f"  ds_oblvar_e{semente}: {n} imagens de {len(SITIOS)} sitios")
    return 0


def tr(nome):
    return j(RAIZ, "runs", "detect", nome, "TREINO_OK")


def grupo_c(semente, ids):
    i1, i2, i3, i4 = ids
    ds = j(RAIZ, f"ds_oblvar_e{semente}")
    run = f"s_oblvar_e{semente}"
    return [
        (i1, "C", f"render obliquo de seis sitios, semente de cena {semente}", lambda L: junta_oblvar(semente, L),
         j(ds, "data.yaml")),
        (i2, "C", f"ladrilhos de ds_oblvar_e{semente}", lambda L: ladrilha(ds, ds + "_tiles", L), j(ds + "_tiles", "data.yaml")),
        (i3, "C", f"treino {run}", lambda L: treina(run, j(ds + "_tiles", "data.yaml"), MODELO, EPOCAS, True, L), tr(run)),
        (i4, "C", f"ZS e PREDS de {run}", lambda L: zs_preds([run], L, i4), ok_arq(i4)),
    ]


# ------------------------------------------------------------------ etapas
def etapas():
    E = [
        ("P1", "P", "checagem: disco, GPU, venv, caminhos, nomes livres", preflight, ok_arq("P1")),
        ("P2", "P", "checagem: um quadro de teste com MPFB", teste_mpfb, ok_arq("P2")),
    ]
    # S (R5-1): intercaladas, para que uma pausa deixe uma semente de cada lado
    for eid, nome, ds, s in (("S1", "s_nadir_4k_sd1", "ds_morro_4k_tiles", 1), ("S2", "s_obliquo_sd1", "ds_morro_obl_tiles", 1),
                             ("S3", "s_nadir_4k_sd2", "ds_morro_4k_tiles", 2), ("S4", "s_obliquo_sd2", "ds_morro_obl_tiles", 2)):
        E.append((eid, "S", f"treino {nome}",
                  (lambda nome, ds, s: lambda L: treina(nome, j(RAIZ, ds, "data.yaml"), MODELO, EPOCAS, True, L, s))(nome, ds, s),
                  tr(nome)))
    S_RUNS = ["s_nadir_4k_sd1", "s_obliquo_sd1", "s_nadir_4k_sd2", "s_obliquo_sd2"]
    E += [
        ("S5", "S", "ZS dos quatro modelos de semente",
         lambda L: (varios(*[(avalia, r, L) for r in S_RUNS]) or marca_ok("S5")), ok_arq("S5")),
        ("S6", "S", "VisDrone oficial e IoU dos quatro", lambda L: (oficial(S_RUNS, L) or marca_ok("S6")), ok_arq("S6")),
        ("S7", "S", "PREDS dos quatro", lambda L: (preds(S_RUNS, L) or marca_ok("S7")), ok_arq("S7")),
    ]
    # F (R5-5)
    E += [
        ("F0", "F", "treino ft05_coco_rep (otimizador explicito, celula original)",
         lambda L: ft_treina("05", "coco", "orig", L, 0, "ft05_coco_rep"), tr("ft05_coco_rep")),
        ("F0b", "F", "checagem de reproducao do ft05_coco", ft_reproducao, j(RES, "rodada5_ft_reproducao.json")),
    ]
    k = 1
    for f in ("05", "10"):
        for c in NOVAS:
            for ini in INICIOS:
                nome = f"ft{f}_{ini}_{c}"
                E.append((f"F{k}", "F", f"treino {nome}", (lambda f, ini, c: lambda L: ft_treina(f, ini, c, L))(f, ini, c),
                          tr(nome)))
                k += 1
    E += [
        ("F12b", "F", "controles novos se F0 nao reproduziu (condicional)", ft_controles, ok_arq("F12b")),
        ("F13", "F", "ZS e PREDS da grade do ajuste fino", ft_avalia, ok_arq("F13")),
        ("F14", "F", "selecao do cronograma em sel", selecao_ft, j(RES, "rodada5_ft_selecao.json")),
        ("F15", "F", "sementes 1 e 2 da celula escolhida a 5% (condicional)", ft_sementes, ok_arq("F15")),
        ("F16", "F", "ZS e PREDS dos runs de F15 (condicional)", ft_avalia_sementes, ok_arq("F16")),
    ]
    # N (R5-6): so com o data.yaml convertido
    E += [
        ("N1", "N", "imgsz casado na base nadir (so rotulos)", n_escala, j(RES, "escala_heridal.json")),
        ("N2", "N", "preds na base nadir, imgsz casado e 1280", n_preds, ok_arq("N2")),
        ("N3", "N", "reamostragem na base nadir", n_bootstrap, ok_arq("N3")),
        ("Y1", "Y1", "criterios do bloco de validade (S, F, N)", y1, ok_arq("Y1")),
    ]
    # A (R5-3)
    E.append(("A1", "A", "monta os subconjuntos da curva", monta_curva, j(RES, "curva_subconjuntos.json")))
    k = 2
    for n, s in [(n, 0) for n in CURVA] + [(30, 1), (30, 2), (120, 1), (120, 2)]:
        nome = f"s_oblvar_c{n:03d}" + (f"_sd{s}" if s else "")
        E.append((f"A{k}", "A", f"treino {nome}", (lambda n, s: lambda L: treina_curva(n, s, L))(n, s), tr(nome)))
        k += 1
    A_RUNS = [f"s_oblvar_c{n:03d}" for n in CURVA] + [f"s_oblvar_c{n:03d}_sd{s}" for n in (30, 120) for s in (1, 2)]
    E.append(("A10", "A", "ZS (com teto sintetico) e PREDS da curva",
              lambda L: zs_preds(A_RUNS, L, "A10", j(RAIZ, "ds_oblvar_tiles", "data.yaml")), ok_arq("A10")))
    # D (R5-4)
    E += [
        ("D1", "D", "render 180 quadros nadir so com sol duro",
         lambda L: render(L, j(RAIZ, "ds_soldur_4k"), 180, climas(NADIR4K, "sol_duro")), j(RAIZ, "ds_soldur_4k", "data.yaml")),
        ("D2", "D", "ladrilhos de ds_soldur_4k",
         lambda L: ladrilha(j(RAIZ, "ds_soldur_4k"), j(RAIZ, "ds_soldur_4k_tiles"), L), j(RAIZ, "ds_soldur_4k_tiles", "data.yaml")),
        ("D3", "D", "treino s_soldur_4k",
         lambda L: treina("s_soldur_4k", j(RAIZ, "ds_soldur_4k_tiles", "data.yaml"), MODELO, EPOCAS, True, L), tr("s_soldur_4k")),
        ("D4", "D", "por regime, por quadro: especialista e generalista", d_regime, ok_arq("D4")),
        ("D5", "D", "ZS do s_soldur_4k (exploratorio)", lambda L: avalia("s_soldur_4k", L), j(RES, "sim2real_s_soldur_4k.json")),
    ]
    # M (R5-7)
    E += [
        ("M1", "M", "render 80 quadros novos a 150 m (indices 200 a 279)",
         lambda L: render(L, j(RAIZ, "ds_armado_150g_extra"), 80, GEMEO150 + ["--val", 1.0], inicio=200),
         j(RAIZ, "ds_armado_150g_extra", "data.yaml")),
        ("M2", "M", "treino armado_150g_e120 (120 epocas, paciencia 30, 3 classes)",
         lambda L: treina("armado_150g_e120", j(RAIZ, "ds_armado_150g_tiles", "data.yaml"), MODELO, 120, False, L, 0, (), 30),
         tr("armado_150g_e120")),
        ("M3", "M", "confusao do armado_150g_e120 (val e quadros novos) e do armado_150g",
         lambda L: (varios((confusao, "armado_150g_e120", j(RAIZ, "ds_armado_150g"), "val", "confusao_armado_150g_e120.json", L),
                           (confusao, "armado_150g_e120", j(RAIZ, "ds_armado_150g_extra"), "val", "extra_armado_150g_e120.json", L),
                           (confusao, "armado_150g", j(RAIZ, "ds_armado_150g_extra"), "val", "extra_armado_150g.json", L))
                    or marca_ok("M3")), ok_arq("M3")),
        ("M4", "M", "condicao de validade a 150 m", validade_150, j(RES, "rodada5_validade_150.json")),
        ("M5", "M", "render 400 quadros a 150 m, indices 280 a 679 (condicional)",
         lambda L: condicional_m("M5", lambda L2: render(L2, j(RAIZ, "_armado_150g_mais"), 400, GEMEO150, inicio=280), L),
         ok_arq("M5")),
        ("M6", "M", "junta o corpus de 600 quadros e ladrilha (condicional)",
         lambda L: condicional_m("M6", junta_150_600, L), ok_arq("M6")),
        ("M7", "M", "treino armado_150g_600 (condicional)",
         lambda L: condicional_m("M7", lambda L2: treina("armado_150g_600", j(RAIZ, "ds_armado_150g_600_tiles", "data.yaml"),
                                                         MODELO, EPOCAS, False, L2), L), ok_arq("M7")),
        ("M8", "M", "confusao do armado_150g_600 (condicional)",
         lambda L: condicional_m("M8", lambda L2: varios(
             (confusao, "armado_150g_600", j(RAIZ, "ds_armado_150g_600"), "val", "confusao_armado_150g_600.json", L2),
             (confusao, "armado_150g_600", j(RAIZ, "ds_armado_150g_extra"), "val", "extra_armado_150g_600.json", L2)), L),
         ok_arq("M8")),
    ]
    # C (R5-2): uma replica inteira antes da outra
    E += grupo_c(22, ("C1", "C2", "C3", "C4")) + grupo_c(23, ("C5", "C6", "C7", "C8"))
    # Y2
    E += [
        ("Y2", "Y2", "VisDrone oficial e IoU dos modelos novos", y2, ok_arq("Y2")),
        ("Y3", "Y2", "reamostragem e resolubilidade (sufixo r5)", y3, ok_arq("Y3")),
        ("Y4", "Y2", "todos os criterios do PLANO-RODADA5", y4, ok_arq("Y4")),
    ]
    return E


ETAPAS = etapas()


def trava():
    """uma instancia so. psutil vem com o ultralytics."""
    import psutil
    if os.path.exists(TRAVA):
        try:
            pid = int(open(TRAVA).read().strip())
            if pid != os.getpid() and psutil.pid_exists(pid) and any(
                    os.path.basename(a) == "rodada5.py" for a in psutil.Process(pid).cmdline()):
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
    """roda uma etapa com duas tentativas; devolve 0, DISPENSADA ou o rc da falha"""
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
        except Exception as exc:          # erro do proprio orquestrador: registra e segue
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
        log(f"[{eid}] dispensada pela regra do plano")
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
            st = e.get(eid, {}).get("estado") if e.get(eid, {}).get("estado") in ("dispensada", "aguardando_dado") else None
            st = st or ("feita" if os.path.exists(prova) else e.get(eid, {}).get("estado", "pendente"))
            print(f"{eid:<5} {g:<3} {desc:<66} {st}")
        return 0
    if DRY:
        print(f"DRY-RUN: nada e executado nem gravado; etapas com prova sao puladas. HERIDAL convertida: "
              f"{os.path.exists(HERIDAL_YAML)}", flush=True)
    elif not trava():
        print("outra instancia da rodada5 ja esta rodando", flush=True)
        return 0
    if not DRY:
        log("rodada5: inicio (ou retomada)" + (f", so os grupos {sorted(so)}" if so else ""))
        if so is None:
            e = carrega()
            e.pop("fim", None)
            e.pop("grupos_com_falha", None)
            grava(e)
    grupo_falhou, aguardando = set(), []
    n_cedo = n_tarde = False                 # o grupo N rodou no laco normal / na repescagem do fim
    y4_existia = os.path.exists(ok_arq("Y4"))
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
        if g == "N" and DRY and not os.path.exists(HERIDAL_YAML):
            print(f"      # [{eid}] sem {HERIDAL_YAML}: na cadeia real fica 'aguardando_dado' e roda no fim "
                  "se o dado aparecer. Comandos que rodariam:", flush=True)
        if g == "N" and not os.path.exists(HERIDAL_YAML) and not DRY:
            if carrega().get(eid, {}).get("estado") != "aguardando_dado":
                log(f"[{eid}] aguardando_dado: {HERIDAL_YAML} nao existe; o grupo N roda no fim se o dado aparecer")
            marca(eid, estado="aguardando_dado", desc=desc)
            aguardando.append((eid, g, desc, fn, prova))
            continue
        rc = executa(eid, g, desc, fn, prova)
        if g == "N" and rc in (0, DISPENSADA):
            n_cedo = True
        if rc not in (0, DISPENSADA) and not DRY:
            grupo_falhou.add(g)
            if g == "P" and not DRY:
                break
    if "P" in grupo_falhou and not DRY:
        log("rodada5: a checagem de partida (P) falhou; nada mais roda. Corrigir e relancar.")
    elif aguardando and not DRY:
        if os.path.exists(HERIDAL_YAML):
            log("rodada5: o dado da base nadir apareceu; rodando o grupo N agora")
            for eid, g, desc, fn, prova in aguardando:
                if os.path.exists(PAUSA):
                    log("PAUSA presente: a cadeia para antes da proxima etapa (sem gravar fim)")
                    solta()
                    return 0
                if os.path.exists(prova):
                    continue
                if g in grupo_falhou:
                    marca(eid, estado="pulada", desc=desc)
                    continue
                rc = executa(eid, g, desc, fn, prova)
                if rc in (0, DISPENSADA):
                    n_tarde = True
                else:
                    grupo_falhou.add(g)
        else:
            log(f"rodada5: grupo N aguardando_dado ({HERIDAL_YAML} nao existe). Depois do download e da conversao "
                "(prepara_heridal.py), rodar `python rodada5.py`: so o N e os criterios rodam.")
    if (n_tarde or (n_cedo and y4_existia)) and not DRY and "N" not in grupo_falhou and os.path.exists(ok_arq("Y4")):
        log("rodada5: o grupo N rodou depois dos criterios finais; refazendo reamostragem e criterios")
        rc = varios((bootstrap_r5, "Y4_criterios.log"), (criterios, "tudo", "Y4_criterios.log"))
        if rc != 0:
            grupo_falhou.add("Y2")
    if DRY:
        return 0
    if so is None:
        e = carrega()
        e["fim"] = datetime.now().isoformat(timespec="seconds")
        e["grupos_com_falha"] = sorted(grupo_falhou)
        e["aguardando_dado"] = [x[0] for x in aguardando if not os.path.exists(x[4])]
        grava(e)
    log("rodada5: encerrada" + (f" com falha nos grupos {sorted(grupo_falhou)}" if grupo_falhou else "")
        + (" (execucao parcial, sem fim)" if so is not None else ""))
    solta()
    return 1 if grupo_falhou else 0


if __name__ == "__main__":
    sys.exit(main())
