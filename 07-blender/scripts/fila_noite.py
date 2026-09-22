#!/usr/bin/env python3
"""
fila_noite.py: enfileira, em sequencia e sem supervisao, tudo que falta do pipeline.

Por que uma fila e nao varios comandos soltos: render e treino disputam a MESMA GPU (uma RTX 2060
de 6 GB). Rodar dois ao mesmo tempo nao acelera nada, derrama VRAM para a CPU e o custo explode
sem aviso no log. A fila resolve isso do jeito mais simples possivel, uma etapa de cada vez.

Ordem escolhida (pedido do autor em 2026-09-20): S-nadir primeiro, porque e ele que fecha o
numero que falta no artigo. O braco armado vem depois, porque exige render novo.

Cada etapa:
  - tem log proprio em <RAIZ_TRABALHO>/fila/<n>_<nome>.log
  - grava duracao e codigo de saida em <RAIZ_TRABALHO>/fila/estado.json
  - pode ser pulada se a saida ja existir (--retomar, que e o padrao)
  - se falhar, a fila PARA nas etapas que dependem dela e segue nas independentes

Uso:
  python fila_noite.py                  # roda tudo, esperando o render atual terminar
  python fila_noite.py --so 1,2,3       # so as etapas indicadas
  python fila_noite.py --listar         # imprime o plano e sai, sem executar
  python fila_noite.py --refazer        # ignora saida existente e refaz tudo
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime

RAIZ = r"C:\arma3-favela\blender"
VIS = r"C:\arma3-favela\visdrone"
SCR = os.path.dirname(os.path.abspath(__file__))
RES = os.path.abspath(os.path.join(SCR, "..", "..", "06-resultados"))
BLENDER = r"C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe"
FILA = os.path.join(RAIZ, "fila")
ESTADO = os.path.join(FILA, "estado.json")

# ---------------------------------------------------------------- parametros comuns
# Os MESMOS para o braco sintetico e para o braco real. Isso nao e detalhe de conveniencia: na
# rodada anterior o sintetico e o real diferiam em modelo, imgsz, epocas e inicializacao ao mesmo
# tempo, e por isso a comparacao nao isolava nada. Aqui muda o DADO e so o dado.
MODELO = "yolo11s.pt"
IMGSZ = 1280
EPOCAS = 60
BATCH = 6
WORKERS = 4

DS4K = os.path.join(RAIZ, "ds_morro_4k")
DS4K_T = os.path.join(RAIZ, "ds_morro_4k_tiles")
DS_OBL = os.path.join(RAIZ, "ds_morro_obl")
DS_OBL_T = os.path.join(RAIZ, "ds_morro_obl_tiles")
DS_ARM = os.path.join(RAIZ, "ds_armado_75")
DS_ARM_T = os.path.join(RAIZ, "ds_armado_75_tiles")
DS_VAR = os.path.join(RAIZ, "ds_variedade")
DS_VAR_T = os.path.join(RAIZ, "ds_variedade_tiles")
VIS_YAML = os.path.join(VIS, "visdrone_yolo", "data.yaml")
VIS_SUB = os.path.join(VIS, "visdrone_sub", "data.yaml")

# Interpretador pinado. `sys.executable` nao serve: o python do PATH desta maquina nao tem
# ultralytics, e a fila so descobriria isso horas depois, ao chegar no primeiro treino.
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = sys.executable


def sh(*a):
    return [str(x) for x in a]


def blender(script, *a):
    return sh(BLENDER, "-b", "--python", os.path.join(SCR, script), "--", *a)


def treino(data, nome, extra=()):
    return sh(PY, os.path.join(SCR, "train_yolo_win.py"), "--data", data, "--model", MODELO,
              "--imgsz", IMGSZ, "--epochs", EPOCAS, "--batch", BATCH, "--workers", WORKERS,
              "--name", nome, "--single-cls", *extra)


# NOTA sobre --real-gsd, que fica de fora de proposito.
#
# Aquele conjunto foi construido reescalando o VisDrone por 1/2,49 para casar a escala do alvo
# quando o nosso dataset ainda saia em 1080p. Medido agora no lote 4K com `06-resultados/
# mede_alvo.py`, em 3.225 caixas nossas contra 120.365 do VisDrone:
#
#            largura med   altura med   area med   h/w med
#   nosso        17,6 px      17,5 px     301 px2     0,98
#   VisDrone     13,0 px      24,0 px     300 px2     2,00
#
# A AREA bate em 1,00x. O que sobra de diferenca e FORMA, por um fator de 2,04, e nenhum
# reescalonamento uniforme conserta forma: encolher o VisDrone por 1/1,37 casaria a altura e
# pioraria a largura na mesma medida. Entao o braco reescalado nao isola nada aqui, e quem
# responde a pergunta da forma e a etapa 12, o preset obliquo.
#
# Correcao de registro: em 2026-09-20 eu escrevi que o alvo do lote 4K tinha "24,6 px contra
# 25,0 do VisDrone". 24,6 px e o percentil 90 da nossa largura, nao a mediana, que e 17,5 px.
# A conclusao (nao usar o conjunto reescalado) continua valendo; a razao que eu dei estava errada.
def aval(pesos, sint, saida):
    return sh(PY, os.path.join(SCR, "avalia_sim2real.py"), "--weights", pesos,
              "--sintetico", sint, "--real", VIS_YAML, "--imgsz", IMGSZ, "--out", saida)


def pesos(nome):
    return os.path.join(RAIZ, "runs", "detect", nome, "weights", "best.pt")


# ---------------------------------------------------------------- etapas
# (id, nome, o que faz, comando ou funcao, arquivo que prova que ja rodou, depende de)
def espera_render_4k(log):
    """bloqueia ate ds_morro_4k ter as 180 imagens. Nao mata nada, so espera."""
    alvo = 180
    while True:
        n = 0
        for sp in ("train", "val"):
            d = os.path.join(DS4K, "images", sp)
            if os.path.isdir(d):
                n += len([x for x in os.listdir(d) if x.endswith(".png")])
        log.write(f"{datetime.now():%H:%M:%S} {n}/{alvo} imagens\n")
        log.flush()
        if n >= alvo:
            return 0
        time.sleep(120)


def monta_subamostra(log):
    """cria um recorte do VisDrone com o MESMO numero de imagens de treino que o sintetico tem.

    Serve para separar duas perguntas que a rodada anterior misturou: o sintetico transfere mal,
    ou o sintetico so tem menos imagem? Com o mesmo N, a diferenca que sobrar e do dado, nao do
    tamanho do conjunto. O braco com o VisDrone inteiro tambem roda, mais adiante na fila."""
    import random
    import shutil
    n_sint = len([x for x in os.listdir(os.path.join(DS4K_T, "images", "train"))
                  if x.lower().endswith((".png", ".jpg"))])
    orig = os.path.join(VIS, "visdrone_yolo")
    dest = os.path.join(VIS, "visdrone_sub")
    todas = sorted(os.listdir(os.path.join(orig, "train", "images")))
    escolhidas = random.Random(21).sample(todas, min(n_sint, len(todas)))
    log.write(f"sintetico tem {n_sint} ladrilhos de treino; "
              f"sorteando {len(escolhidas)} imagens do VisDrone\n")
    for sp, itens in (("train", escolhidas), ("val", None)):
        for sub in ("images", "labels"):
            d = os.path.join(dest, sp, sub)
            os.makedirs(d, exist_ok=True)
            fonte = os.path.join(orig, sp, sub)
            nomes = (os.listdir(fonte) if itens is None else
                     [os.path.splitext(x)[0] + (".jpg" if sub == "images" else ".txt")
                      for x in itens])
            for nm in nomes:
                o = os.path.join(fonte, nm)
                if os.path.exists(o):
                    shutil.copy2(o, os.path.join(d, nm))
    with open(os.path.join(dest, "data.yaml"), "w", encoding="utf-8") as f:
        f.write(f"path: {dest.replace(os.sep, '/')}\n"
                "train: train/images\nval: val/images\nnames:\n  0: pessoa\n")
    log.write(f"gravado {dest}\n")
    return 0


def renomeia_nadir(log):
    """converte o nadir avulso para o nome que teste_fidelidade.py procura."""
    from PIL import Image
    o = os.path.join(RAIZ, "previa_4k", "nadir.png")
    d = os.path.join(RES, "morro_v12_nadir.jpg")
    Image.open(o).convert("RGB").save(d, quality=92)
    log.write(f"{o} -> {d}\n")
    return 0



# ---------------------------------------------------------------- teste de dose de variedade
# A pergunta: com o MESMO numero de imagens, 180, seis lugares diferentes transferem melhor que
# um lugar so? O controle ja existe e e o `ds_morro_4k`: 180 imagens de um unico sitio.
#
# Seis sitios x 30 imagens da 180, e 30 e divisivel por 6, entao cada sitio recebe exatamente
# cinco imagens de cada regime de tempo. Manter o clima balanceado DENTRO de cada sitio importa
# porque senao um sitio ficaria com mais sol duro que outro e a comparacao misturaria dois eixos.
#
# O sitio -1 entra na lista de proposito: ele e byte a byte o mesmo do controle (conferido em
# 2026-09-21, 4068 lotes e 208.396 faces com semente 21 nos dois). Assim a pergunta fica limpa:
# nao e "um lugar contra outros seis", e "180 imagens deste lugar contra 30 deste mais 150 de
# outros cinco".
SITIOS_DOSE = [-1, 0, 1, 2, 3, 4]
POR_SITIO = 30


def render_dose(log):
    import shutil
    import subprocess as sp
    destino = DS_VAR
    for sub in ("images/train", "images/val", "labels/train", "labels/val"):
        os.makedirs(os.path.join(destino, *sub.split("/")), exist_ok=True)
    total = 0
    for k in SITIOS_DOSE:
        parcial = os.path.join(RAIZ, f"_dose_s{k}")
        if not os.path.exists(os.path.join(parcial, "data.yaml")):
            cmd = blender("gen_morro.py", "--out", parcial, "--dataset", POR_SITIO,
                          "--samples", 96, "--res", 3840, 2160, "--people", 16, 34,
                          "--pool", 6, "--seed", 21, "--climas", "todos", "--sitio", k)
            log.write("\n# sitio %d\n# %s\n" % (k, " ".join(cmd)))
            log.flush()
            rc = sp.call(cmd, stdout=log, stderr=sp.STDOUT, cwd=RAIZ)
            if rc != 0:
                log.write("sitio %d falhou com rc=%d\n" % (k, rc))
                return rc
        # junta no dataset unico, prefixando o nome pelo sitio para nao colidir
        for split in ("train", "val"):
            for nome in sorted(os.listdir(os.path.join(parcial, "images", split))):
                base = os.path.splitext(nome)[0]
                novo = "s%s_%s" % (str(k).replace("-", "m"), base)
                shutil.copy2(os.path.join(parcial, "images", split, nome),
                             os.path.join(destino, "images", split, novo + ".png"))
                lb = os.path.join(parcial, "labels", split, base + ".txt")
                if os.path.exists(lb):
                    shutil.copy2(lb, os.path.join(destino, "labels", split, novo + ".txt"))
                    total += 1
    with open(os.path.join(destino, "data.yaml"), "w", encoding="utf-8") as f:
        f.write("path: " + destino.replace(os.sep, "/") + "\n"
                "train: images/train\nval: images/val\n"
                "names:\n  0: pessoa_armada\n  1: pessoa_desarmada\n")
    log.write("\n%d imagens juntadas de %d sitios em %s\n" % (total, len(SITIOS_DOSE), destino))
    return 0


ETAPAS = [
    (1, "espera_render_4k", "espera as 180 imagens de ds_morro_4k terminarem",
     espera_render_4k, None, []),

    (2, "nadir_avulso", "renderiza um nadir isolado com os mesmos parametros, para a fidelidade",
     blender("gen_morro.py", "--out", os.path.join(RAIZ, "previa_4k"), "--seed", 21,
             "--samples", 96, "--res", 3840, 2160, "--vistas", "nadir,beco"),
     os.path.join(RAIZ, "previa_4k", "nadir.png"), [1]),

    (3, "renomeia_nadir", "copia o nadir para 06-resultados com o nome que o teste espera",
     renomeia_nadir, os.path.join(RES, "morro_v12_nadir.jpg"), [2]),

    (4, "fidelidade", "dez metricas com faixa declarada, para nao treinar em cima de lote quebrado",
     sh(PY, os.path.join(SCR, "teste_fidelidade.py"), "--dir", RES,
        "--csv", os.path.join(RES, "teste_fidelidade.csv")), None, [3]),

    (5, "previa", "folha de contato com as caixas e recortes ampliados 5x",
     sh(PY, os.path.join(SCR, "previa_dataset.py"), "--ds", DS4K, "--n", 6, "--crops", 24,
        "--out", os.path.join(RES, "figuras", "previa_4k.jpg")),
     os.path.join(RES, "figuras", "previa_4k.jpg"), [1]),

    (6, "ladrilha_4k", "recorta o 4K em ladrilhos de 1280 px em escala nativa",
     sh(PY, os.path.join(SCR, "tile_dataset.py"), "--data", DS4K, "--out", DS4K_T,
        "--tile", 1280, "--overlap", 0.2),
     os.path.join(DS4K_T, "data.yaml"), [1]),

    (7, "treino_S_nadir", "o braco sintetico nadir, que e o numero que falta no artigo",
     treino(os.path.join(DS4K_T, "data.yaml"), "s_nadir_4k"),
     pesos("s_nadir_4k"), [6]),

    (8, "aval_S_nadir", "zero-shot no VisDrone com o peso sintetico",
     aval(pesos("s_nadir_4k"), os.path.join(DS4K_T, "data.yaml"),
          os.path.join(RES, "sim2real_s_nadir_4k.json")),
     os.path.join(RES, "sim2real_s_nadir_4k.json"), [7]),

    (9, "subamostra_visdrone", "recorte do VisDrone com o mesmo N do sintetico",
     monta_subamostra, VIS_SUB, [6]),

    (10, "treino_R_pareado", "braco real com N pareado e hiperparametros identicos ao sintetico",
     treino(VIS_SUB, "r_pareado"), pesos("r_pareado"), [9]),

    (12, "render_obliquo", "180 imagens no preset obliquo, para separar forma do alvo de sintese",
     blender("gen_morro.py", "--out", DS_OBL, "--dataset", 180, "--samples", 96,
             "--res", 1920, 1080, "--people", 16, 34, "--pool", 6, "--seed", 31,
             "--climas", "todos", "--obliqua"),
     os.path.join(DS_OBL, "data.yaml"), [7]),

    (13, "ladrilha_obliquo", "ladrilhos de 1280 px do braco obliquo",
     sh(PY, os.path.join(SCR, "tile_dataset.py"), "--data", DS_OBL, "--out", DS_OBL_T,
        "--tile", 1280, "--overlap", 0.2),
     os.path.join(DS_OBL_T, "data.yaml"), [12]),

    (14, "treino_S_obliquo", "braco sintetico obliquo, mesmos hiperparametros",
     treino(os.path.join(DS_OBL_T, "data.yaml"), "s_obliquo"),
     pesos("s_obliquo"), [13]),

    (15, "aval_S_obliquo", "zero-shot no VisDrone com o peso obliquo",
     aval(pesos("s_obliquo"), os.path.join(DS_OBL_T, "data.yaml"),
          os.path.join(RES, "sim2real_s_obliquo.json")),
     os.path.join(RES, "sim2real_s_obliquo.json"), [14]),

    (16, "render_armado_75", "tres classes com objetos confundiveis, a 75 m, onde a arma ainda "
                             "tem alguma chance de ser resolvida",
     blender("gen_morro.py", "--out", DS_ARM, "--dataset", 200, "--samples", 96,
             "--res", 3840, 2160, "--people", 14, 30, "--pool", 6, "--seed", 41,
             "--climas", "todos", "--alt", 75, "--mistura", 0.34, 0.33, 0.33),
     os.path.join(DS_ARM, "data.yaml"), [14]),

    (17, "ladrilha_armado", "ladrilhos do lote armado",
     sh(PY, os.path.join(SCR, "tile_dataset.py"), "--data", DS_ARM, "--out", DS_ARM_T,
        "--tile", 1280, "--overlap", 0.2),
     os.path.join(DS_ARM_T, "data.yaml"), [16]),

    (18, "treino_armado", "tres classes, SEM single_cls: e aqui que a pergunta armada se decide",
     sh(PY, os.path.join(SCR, "train_yolo_win.py"), "--data", os.path.join(DS_ARM_T, "data.yaml"),
        "--model", MODELO, "--imgsz", IMGSZ, "--epochs", EPOCAS, "--batch", BATCH,
        "--workers", WORKERS, "--name", "armado_75"),
     pesos("armado_75"), [17]),

    (19, "treino_R_cheio", "braco real com o VisDrone inteiro, 6.471 imagens. Fica por ultimo de "
                           "proposito: a razao de eficacia ja sai do pareado, e este aqui e o "
                           "mais caro da fila",
     treino(VIS_YAML, "r_cheio"), pesos("r_cheio"), []),

    (20, "render_dose_variedade", "seis sitios x 30 imagens, mesmo total do controle de 180",
     render_dose, os.path.join(DS_VAR, "data.yaml"), []),

    (21, "ladrilha_variedade", "ladrilhos de 1280 px do braco de variedade",
     sh(PY, os.path.join(SCR, "tile_dataset.py"), "--data", DS_VAR, "--out", DS_VAR_T,
        "--tile", 1280, "--overlap", 0.2),
     os.path.join(DS_VAR_T, "data.yaml"), [20]),

    (22, "treino_S_variedade", "mesmos hiperparametros do s_nadir_4k: muda o DADO e so o dado",
     treino(os.path.join(DS_VAR_T, "data.yaml"), "s_variedade"),
     pesos("s_variedade"), [21]),

    (23, "aval_S_variedade", "zero-shot no VisDrone, para comparar com sim2real_s_nadir_4k.json",
     aval(pesos("s_variedade"), os.path.join(DS_VAR_T, "data.yaml"),
          os.path.join(RES, "sim2real_s_variedade.json")),
     os.path.join(RES, "sim2real_s_variedade.json"), [22]),

    (24, "bench_otimizacao", "mede QUAL das tres otimizacoes de render paga, e se alguma estraga "
                             "a imagem. Fica no fim porque nao produz dado para o artigo, "
                             "produz a decisao de comprar ou nao placa nova",
     sh(PY, os.path.join(SCR, "bench_otimizacao.py"), "--quadros", 8),
     os.path.join(RES, "bench_otimizacao.json"), []),
]


def carrega():
    # Um kill no meio da escrita deixou este arquivo VAZIO em 22/09 e derrubou a fila inteira na
    # primeira linha. Arquivo ilegivel vale como fila nova, nao como erro fatal.
    if os.path.exists(ESTADO):
        try:
            return json.load(open(ESTADO, encoding="utf-8"))
        except (ValueError, OSError):
            print(f"[fila] {ESTADO} ilegivel, comecando estado vazio", flush=True)
    return {}


def grava(e):
    # escrita atomica: grava num temporario e renomeia, para um kill nunca deixar o arquivo pela metade
    tmp = ESTADO + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(e, f, indent=1, ensure_ascii=False)
    os.replace(tmp, ESTADO)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", default=None, help="ids separados por virgula")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--refazer", action="store_true")
    a = ap.parse_args()

    if a.listar:
        for i, nome, desc, _, prova, dep in ETAPAS:
            d = f" depende de {dep}" if dep else ""
            print(f"{i:>3}. {nome:<20} {desc}{d}")
        return

    os.makedirs(FILA, exist_ok=True)
    so = {int(x) for x in a.so.split(",")} if a.so else None
    est = carrega()
    falhou = set()

    for i, nome, desc, cmd, prova, dep in ETAPAS:
        if so and i not in so:
            continue
        if any(d in falhou for d in dep):
            print(f"[{i}] {nome}: PULADA, depende de etapa que falhou")
            est[str(i)] = dict(nome=nome, estado="pulada_por_dependencia")
            grava(est)
            falhou.add(i)
            continue
        if prova and os.path.exists(prova) and not a.refazer:
            print(f"[{i}] {nome}: ja existe {os.path.basename(prova)}, pulando")
            est[str(i)] = dict(nome=nome, estado="ja_existia")
            grava(est)
            continue

        lg = os.path.join(FILA, f"{i:02d}_{nome}.log")
        print(f"[{i}] {nome}: {desc}\n     log {lg}", flush=True)
        t0 = time.time()
        with open(lg, "w", encoding="utf-8", buffering=1) as f:
            f.write(f"# {datetime.now():%Y-%m-%d %H:%M:%S}  {nome}\n")
            if callable(cmd):
                try:
                    rc = cmd(f)
                except Exception as exc:
                    f.write(f"ERRO {exc!r}\n")
                    rc = 1
            else:
                f.write("# " + " ".join(cmd) + "\n\n")
                f.flush()
                rc = subprocess.call(cmd, stdout=f, stderr=subprocess.STDOUT, cwd=RAIZ)
        dt = time.time() - t0
        est[str(i)] = dict(nome=nome, estado="ok" if rc == 0 else f"falhou_rc{rc}",
                           segundos=round(dt), fim=f"{datetime.now():%Y-%m-%d %H:%M:%S}")
        grava(est)
        print(f"     {'ok' if rc == 0 else 'FALHOU rc=' + str(rc)} em {dt / 60:.1f} min",
              flush=True)
        if rc != 0:
            falhou.add(i)

    print("\nresumo em " + ESTADO)


if __name__ == "__main__":
    main()
