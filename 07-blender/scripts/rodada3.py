#!/usr/bin/env python3
"""
rodada3.py: a rodada iniciada em 24/09, em uma cadeia so, idempotente e retomavel.

Cada etapa tem um arquivo de prova; se ele existe, a etapa e pulada. Render retoma pelo numero de
linhas do manifest (--start, deterministico desde 38bb01f). Treino retoma do last.pt, e so conta
como feito quando TREINO_OK existe: a fila antiga usava o best.pt como prova, que o Ultralytics
grava ja na primeira epoca, entao uma queda no meio do treino faria a fila avaliar um modelo pela
metade achando que estava pronto. Pode ser relancada a qualquer momento (vigia_rodada3.sh faz
isso sozinho) e uma trava impede duas instancias ao mesmo tempo.

Grupos, na ordem, cada um independente dos outros exceto D, que usa o peso de A:
  Z  confusao dos dois modelos armados que ja existem, no protocolo novo (imagem inteira)
  A  braco obliquo combinado: 6 sitios x 30, camera inclinada 45 a 56 graus, camera livre de
     mata, so pessoas sem arma; treino e zero-shot no VisDrone          (o modelo do artigo)
  B  teste de arma inedita (secao 11.5): 50 quadros a 75 m, metade das armas de dois modelos que
     o armado_75 nunca viu; recall por modelo
  C  gemeo a 75 m do corpus de 35 m: tudo igual ao de 35 m menos a altura; treino e confusao
  D  ajuste fino com 5% e 10% do VisDrone real, a partir do peso de A e a partir do COCO

Uso:  python rodada3.py            (roda o que falta)
      python rodada3.py --listar   (mostra as etapas e o estado)
"""
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
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
FILA = os.path.join(RAIZ, "fila3")
LOG = os.path.join(RAIZ, "rodada3.log")
ESTADO = os.path.join(FILA, "estado.json")
TRAVA = os.path.join(FILA, "rodada3.trava")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
BLENDER = os.path.join("C:" + os.sep, "Program Files (x86)", "Steam", "steamapps", "common",
                       "Blender", "blender.exe")
VIS_YAML = os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "visdrone_yolo", "data.yaml")
FT = os.path.join("C:" + os.sep, "arma3-favela", "visdrone", "ft")

# mesma receita de todos os bracos anteriores
MODELO, IMGSZ, EPOCAS, BATCH, WORKERS = "yolo11s.pt", 1280, 60, 6, 4
EPOCAS_FT = 30

SITIOS = [-1, 0, 1, 2, 3, 4]
POR_SITIO = 30
OBLVAR = ["--samples", 96, "--res", 3840, 2160, "--people", 16, 34, "--pool", 6, "--seed", 21,
          "--climas", "todos", "--obliqua", "--pitch-obl", 45, 56, "--camera-livre",
          "--mistura", 0, 1, 0]
# identico ao comando que gerou ds_armado_75 (etapa 16 da fila antiga), menos semente e armas
INEDITA = ["--samples", 96, "--res", 3840, 2160, "--people", 14, 30, "--pool", 6, "--seed", 47,
           "--climas", "todos", "--alt", 75, "--mistura", 0.34, 0.33, 0.33,
           "--armas", "mista_inedita"]
# identico ao comando que gerou ds_armado_35 (etapa 25), menos a altura (e o jitter, proporcional)
GEMEO75 = ["--samples", 64, "--res", 3840, 2160, "--people", 12, 24, "--pool", 6, "--seed", 43,
           "--climas", "todos", "--alt", 75, "--alt-jitter", 6, "--mistura", 0.34, 0.33, 0.33,
           "--porte-realista", "--fio-gsd", "--laje", 0.75, "--amostra-no-quadro"]


def j(*p):
    return os.path.join(*[str(x) for x in p])


def log(m):
    linha = f"{datetime.now():%Y-%m-%d %H:%M:%S} {m}"
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
    e = carrega()
    e.setdefault(eid, {}).update(kw)
    grava(e)


def linhas(p):
    try:
        with open(p, encoding="utf-8") as f:
            return sum(1 for ln in f if ln.strip())
    except OSError:
        return 0


def roda(cmd, nome_log):
    cmd = [str(c) for c in cmd]
    with open(j(FILA, nome_log), "a", encoding="utf-8", buffering=1) as f:
        f.write(f"\n# {datetime.now():%Y-%m-%d %H:%M:%S}\n# {' '.join(cmd)}\n\n")
        f.flush()
        return subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=RAIZ)


# ------------------------------------------------------------------ primitivas idempotentes
def render(nome_log, out, total, extra):
    feitos = linhas(j(out, "manifest.jsonl"))
    if os.path.exists(j(out, "data.yaml")) and feitos >= total:
        return 0
    cmd = [BLENDER, "-b", "--python-exit-code", 1, "--python", j(SCR, "gen_morro.py"), "--",
           "--out", out, "--dataset", total, *extra, "--start", feitos]
    log(f"  render {os.path.basename(out)}: de {feitos}/{total}")
    return roda(cmd, nome_log)


def ladrilha(ds, ds_t, nome_log):
    if os.path.exists(j(ds_t, "data.yaml")):
        return 0
    return roda([PY, j(SCR, "tile_dataset.py"), "--data", ds, "--out", ds_t,
                 "--tile", 1280, "--overlap", 0.2], nome_log)


def treina(nome, data, modelo, epocas, single, nome_log):
    rd = j(RAIZ, "runs", "detect", nome)
    ok = j(rd, "TREINO_OK")
    if os.path.exists(ok):
        return 0
    last = j(rd, "weights", "last.pt")
    if os.path.exists(last):
        log(f"  treino {nome}: retomando de {last}")
        codigo = f"from ultralytics import YOLO\nYOLO(r'{last}').train(resume=True)\n"
        rc = roda([PY, "-c", codigo], nome_log)
        if rc != 0:
            with open(j(FILA, nome_log), encoding="utf-8", errors="replace") as f:
                cauda = f.read()[-4000:]
            if "nothing to resume" in cauda or "is finished" in cauda:
                rc = 0
    else:
        log(f"  treino {nome}: do zero, a partir de {os.path.basename(str(modelo))}")
        cmd = [PY, j(SCR, "train_yolo_win.py"), "--data", data, "--model", modelo,
               "--imgsz", IMGSZ, "--epochs", epocas, "--batch", BATCH, "--workers", WORKERS,
               "--name", nome] + (["--single-cls"] if single else [])
        rc = roda(cmd, nome_log)
    if rc == 0 and os.path.exists(j(rd, "weights", "best.pt")):
        with open(ok, "w", encoding="utf-8") as f:
            f.write(datetime.now().isoformat())
    return rc


def pesos(nome):
    return j(RAIZ, "runs", "detect", nome, "weights", "best.pt")


def avalia(p, sint, saida, nome_log):
    if os.path.exists(saida):
        return 0
    cmd = [PY, j(SCR, "avalia_sim2real.py"), "--weights", p, "--real", VIS_YAML,
           "--imgsz", IMGSZ, "--out", saida] + (["--sintetico", sint] if sint else [])
    return roda(cmd, nome_log)


def confusao(p, ds, split, saida, nome_log):
    if os.path.exists(saida):
        return 0
    return roda([PY, j(RES, "confusao_armado.py"), "--pesos", p, "--ds", ds, "--split", split,
                 "--out", saida], nome_log)


def map50_real(saida):
    try:
        with open(saida, encoding="utf-8") as f:
            d = json.load(f)
        for r in d.get("resultados", []):
            if r.get("conjunto") == "real":
                return r.get("metrics/mAP50(B)")
    except (OSError, ValueError):
        pass
    return None


# ------------------------------------------------------------------ etapas compostas
def junta_oblvar(nome_log):
    dst = j(RAIZ, "ds_oblvar")
    if os.path.exists(j(dst, "data.yaml")):
        return 0
    for k in SITIOS:
        rc = render(nome_log, j(RAIZ, f"_oblvar_s{k}"), POR_SITIO, OBLVAR + ["--sitio", k])
        if rc != 0:
            log(f"  sitio {k} falhou rc={rc}")
            return rc
    shutil.rmtree(dst, ignore_errors=True)
    for sub in ("images/train", "images/val", "labels/train", "labels/val"):
        os.makedirs(j(dst, *sub.split("/")), exist_ok=True)
    n = 0
    with open(j(dst, "manifest.jsonl"), "w", encoding="utf-8") as mf:
        for k in SITIOS:
            par = j(RAIZ, f"_oblvar_s{k}")
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
                shutil.copy2(j(par, "labels", r["split"], base + ".txt"),
                             j(dst, "labels", r["split"], novo + ".txt"))
                r["img"], r["sitio"] = novo + ".png", k
                mf.write(json.dumps(r) + "\n")
                n += 1
    with open(j(dst, "data.yaml"), "w", encoding="utf-8") as f:
        f.write("path: " + dst.replace(os.sep, "/") + "\ntrain: images/train\nval: images/val\n"
                "names:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
    log(f"  ds_oblvar: {n} imagens de {len(SITIOS)} sitios")
    return 0


def base_ft():
    """peso de partida do ajuste fino: o braco combinado (A), fixado antes de rodar; se A falhou,
    o obliquo de um sitio, e isso fica registrado no estado."""
    if os.path.exists(j(RAIZ, "runs", "detect", "s_oblvar", "TREINO_OK")):
        return "s_oblvar", pesos("s_oblvar")
    return "s_obliquo", pesos("s_obliquo")


def ft_treino(nome, fatia, init, nome_log):
    if init == "sint":
        rot, p = base_ft()
        marca(nome, base=rot)
        modelo = p
    else:
        modelo = MODELO
    return treina(nome, j(FT, fatia + ".yaml"), modelo, EPOCAS_FT, True, nome_log)


def ft_resumo(nome_log):
    saida = j(RES, "ft_visdrone.json")
    tab = {}
    for n in ("ft05_sint", "ft05_coco", "ft10_sint", "ft10_coco"):
        f = j(RES, f"sim2real_{n}.json")
        if avalia(pesos(n), None, f, nome_log) != 0:
            return 1
        tab[n] = map50_real(f)
    tab["base_sintetica"] = carrega().get("ft05_sint", {}).get("base")
    tab["protocolo"] = ("treino em 5% ou 10% do treino do VisDrone, escolha do peso em outros 5% "
                        f"do treino, teste na validacao inteira; {EPOCAS_FT} epocas, mesma receita")
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(tab, f, indent=1, ensure_ascii=False)
    return 0


# (id, grupo, descricao, funcao(nome_log) -> rc, prova)
ETAPAS = [
    ("Z1", "Z", "confusao armado_75 (protocolo novo)",
     lambda L: confusao(pesos("armado_75"), j(RAIZ, "ds_armado_75"), "val", j(RES, "confusao_armado_75.json"), L),
     j(RES, "confusao_armado_75.json")),
    ("Z2", "Z", "confusao armado_35 (protocolo novo)",
     lambda L: confusao(pesos("armado_35"), j(RAIZ, "ds_armado_35"), "val", j(RES, "confusao_armado_35.json"), L),
     j(RES, "confusao_armado_35.json")),

    ("A1", "A", "render obliquo combinado, 6 sitios x 30", junta_oblvar, j(RAIZ, "ds_oblvar", "data.yaml")),
    ("A2", "A", "ladrilhos do obliquo combinado",
     lambda L: ladrilha(j(RAIZ, "ds_oblvar"), j(RAIZ, "ds_oblvar_tiles"), L), j(RAIZ, "ds_oblvar_tiles", "data.yaml")),
    ("A3", "A", "treino s_oblvar",
     lambda L: treina("s_oblvar", j(RAIZ, "ds_oblvar_tiles", "data.yaml"), MODELO, EPOCAS, True, L),
     j(RAIZ, "runs", "detect", "s_oblvar", "TREINO_OK")),
    ("A4", "A", "zero-shot no VisDrone do s_oblvar",
     lambda L: avalia(pesos("s_oblvar"), j(RAIZ, "ds_oblvar_tiles", "data.yaml"), j(RES, "sim2real_s_oblvar.json"), L),
     j(RES, "sim2real_s_oblvar.json")),

    ("B1", "B", "render teste de arma inedita, 50 quadros a 75 m",
     lambda L: render(L, j(RAIZ, "ds_armado_75_inedita"), 50, INEDITA), j(RAIZ, "ds_armado_75_inedita", "data.yaml")),
    ("B2", "B", "recall por modelo de arma do armado_75 no teste inedito",
     lambda L: confusao(pesos("armado_75"), j(RAIZ, "ds_armado_75_inedita"), "todos", j(RES, "holdout_armas_armado_75.json"), L),
     j(RES, "holdout_armas_armado_75.json")),

    ("C1", "C", "render gemeo a 75 m do corpus de 35 m, 200 quadros",
     lambda L: render(L, j(RAIZ, "ds_armado_75g"), 200, GEMEO75), j(RAIZ, "ds_armado_75g", "data.yaml")),
    ("C2", "C", "ladrilhos do gemeo 75 m",
     lambda L: ladrilha(j(RAIZ, "ds_armado_75g"), j(RAIZ, "ds_armado_75g_tiles"), L), j(RAIZ, "ds_armado_75g_tiles", "data.yaml")),
    ("C3", "C", "treino armado_75g (3 classes)",
     lambda L: treina("armado_75g", j(RAIZ, "ds_armado_75g_tiles", "data.yaml"), MODELO, EPOCAS, False, L),
     j(RAIZ, "runs", "detect", "armado_75g", "TREINO_OK")),
    ("C4", "C", "confusao armado_75g",
     lambda L: confusao(pesos("armado_75g"), j(RAIZ, "ds_armado_75g"), "val", j(RES, "confusao_armado_75g.json"), L),
     j(RES, "confusao_armado_75g.json")),

    ("D1", "D", "fatias do VisDrone para ajuste fino",
     lambda L: roda([PY, j(SCR, "prepara_ft.py")], L), j(FT, "fatias.json")),
    ("D2", "D", "ajuste fino 5% a partir do sintetico",
     lambda L: ft_treino("ft05_sint", "ft05", "sint", L), j(RAIZ, "runs", "detect", "ft05_sint", "TREINO_OK")),
    ("D3", "D", "treino 5% a partir do COCO",
     lambda L: ft_treino("ft05_coco", "ft05", "coco", L), j(RAIZ, "runs", "detect", "ft05_coco", "TREINO_OK")),
    ("D4", "D", "ajuste fino 10% a partir do sintetico",
     lambda L: ft_treino("ft10_sint", "ft10", "sint", L), j(RAIZ, "runs", "detect", "ft10_sint", "TREINO_OK")),
    ("D5", "D", "treino 10% a partir do COCO",
     lambda L: ft_treino("ft10_coco", "ft10", "coco", L), j(RAIZ, "runs", "detect", "ft10_coco", "TREINO_OK")),
    ("D6", "D", "teste dos quatro no VisDrone", ft_resumo, j(RES, "ft_visdrone.json")),
]


def trava():
    """uma instancia so. psutil vem com o ultralytics."""
    import psutil
    if os.path.exists(TRAVA):
        try:
            pid = int(open(TRAVA).read().strip())
            if psutil.pid_exists(pid) and "rodada3" in " ".join(psutil.Process(pid).cmdline()):
                return False
        except (ValueError, OSError, psutil.Error):
            pass
    with open(TRAVA, "w") as f:
        f.write(str(os.getpid()))
    return True


def main():
    os.makedirs(FILA, exist_ok=True)
    if "--listar" in sys.argv:
        e = carrega()
        for eid, g, desc, _, prova in ETAPAS:
            st = "feita" if os.path.exists(prova) else e.get(eid, {}).get("estado", "pendente")
            print(f"{eid:<3} {desc:<58} {st}")
        return 0
    if not trava():
        print("outra instancia da rodada3 ja esta rodando", flush=True)
        return 0
    log("rodada3: inicio (ou retomada)")
    e = carrega()
    e.pop("fim", None)
    e.pop("grupos_com_falha", None)
    grava(e)
    grupo_falhou = set()
    for eid, g, desc, fn, prova in ETAPAS:
        if os.path.exists(prova):
            if carrega().get(eid, {}).get("estado") != "ok":
                marca(eid, estado="ok", desc=desc)
            continue
        if g in grupo_falhou:
            marca(eid, estado="pulada", desc=desc)
            continue
        nome_log = f"{eid}_{desc.split()[0]}.log"
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
            if rc == 0 and os.path.exists(prova):
                break
            if rc == 0:
                rc = 1
                log("  terminou sem gerar a prova")
            log(f"  tentativa {tentativa} falhou (rc={rc})")
        dt = round(time.time() - t0)
        if rc == 0:
            marca(eid, estado="ok", segundos=dt, fim=datetime.now().isoformat(timespec="seconds"))
            log(f"[{eid}] ok em {dt / 60:.1f} min")
        else:
            marca(eid, estado=f"falhou_rc{rc}", segundos=dt)
            grupo_falhou.add(g)
            log(f"[{eid}] FALHOU; o resto do grupo {g} fica para a proxima retomada")
    e = carrega()
    e["fim"] = datetime.now().isoformat(timespec="seconds")
    e["grupos_com_falha"] = sorted(grupo_falhou)
    grava(e)
    log("rodada3: encerrada" + (f" com falha nos grupos {sorted(grupo_falhou)}" if grupo_falhou else ""))
    try:
        os.remove(TRAVA)
    except OSError:
        pass
    return 1 if grupo_falhou else 0


if __name__ == "__main__":
    sys.exit(main())
