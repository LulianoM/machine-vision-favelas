#!/usr/bin/env python3
"""
supervisiona_rodada3.py: mantem a rodada 3 rodando ate o fim, em janela propria, fora do app do Claude.

Por que existe (25/09). Na noite de 24 para 25 o PC caiu as 23:25 (queda de energia, pelo padrao dos
registros) e religou as 23:26, mas a fila so voltava se alguem abrisse uma sessao do Claude, e ficou
9,5 h parada. O vigia em bash morria junto com a sessao. Este supervisor:

  - e iniciado por um atalho na pasta Inicializar do Windows (retoma_rodada3.cmd), ou seja pelo shell
    do usuario no login, como um duplo clique: o Blender carrega as extensoes do usuario (MPFB), o que
    NAO acontece quando o processo nasce do Agendador de Tarefas, do WMI ou de um explorer lancado por
    DCOM (testado em 23 e 25/09);
  - roda numa janela minimizada propria ("rodada3 - nao feche"), entao nao depende do app do Claude;
  - a cada 5 min: se a cadeia nao esta rodando, lanca; se esta rodando mas nenhum log de fila3 foi
    escrito em 45 min, mata a arvore dela e relanca (a cadeia e idempotente e tem trava);
  - sai quando a rodada grava "fim" no estado, e ao sair apaga o proprio atalho de inicializacao.

Uma instancia so: se outro supervisor ja roda, sai.
"""
import glob
import json
import os
import subprocess
import sys
import time
from datetime import datetime

import psutil

SCR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
FILA = os.path.join(RAIZ, "fila3")
ESTADO = os.path.join(FILA, "estado.json")
LOGV = os.path.join(RAIZ, "vigia3.log")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
RODADA = os.path.join(SCR, "rodada3.py")
ATALHO = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs",
                      "Startup", "retoma_rodada3.lnk")
PARADO_S = 45 * 60
PASSO_S = 5 * 60


def log(m):
    linha = f"{datetime.now():%Y-%m-%d %H:%M:%S} [supervisor] {m}"
    with open(LOGV, "a", encoding="utf-8") as f:
        f.write(linha + "\n")
    print(linha, flush=True)


def tem_arg(p, nome):
    try:
        return any(os.path.basename(a) == nome for a in p.cmdline())
    except (psutil.Error, OSError):
        return False


def processos(nome):
    # O python.exe do venv e um lancador que abre o interpretador real como FILHO com a mesma linha
    # de comando: sem excluir os ancestrais, o supervisor ve o proprio lancador e acha que ha outro.
    eu = {os.getpid()} | {p.pid for p in psutil.Process().parents()}
    return [p for p in psutil.process_iter() if p.pid not in eu and tem_arg(p, nome)]


def fim():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return bool(json.load(f).get("fim"))
    except (OSError, ValueError):
        return False


def idade_log():
    logs = glob.glob(os.path.join(FILA, "*.log"))
    if not logs:
        return 0
    return time.time() - max(os.path.getmtime(x) for x in logs)


def mata_cadeia():
    alvos = []
    for p in processos("rodada3.py"):
        try:
            alvos += p.children(recursive=True) + [p]
        except psutil.Error:
            pass
    for p in psutil.process_iter():
        try:
            cmd = " ".join(p.cmdline())
        except (psutil.Error, OSError):
            continue
        if "gen_morro.py" in cmd or "train_yolo_win.py" in cmd or "resume=True" in cmd:
            alvos.append(p)
    for p in alvos:
        try:
            p.kill()
        except psutil.Error:
            pass
    psutil.wait_procs(alvos, timeout=30)
    try:
        os.remove(os.path.join(FILA, "rodada3.trava"))
    except OSError:
        pass


def lanca():
    # compartilha o console deste supervisor: fica visivel na mesma janela minimizada
    subprocess.Popen([PY, "-u", RODADA], cwd=RAIZ)


def main():
    if processos("supervisiona_rodada3.py"):
        print("outro supervisor ja esta rodando", flush=True)
        return 0
    log("iniciado")
    while True:
        if fim():
            log("rodada encerrada; apagando o atalho de inicializacao e saindo")
            try:
                os.remove(ATALHO)
            except OSError:
                pass
            return 0
        if not processos("rodada3.py"):
            log("cadeia nao esta rodando: lancando")
            try:
                os.remove(os.path.join(FILA, "rodada3.trava"))
            except OSError:
                pass
            lanca()
        elif idade_log() > PARADO_S:
            log(f"cadeia sem escrever log ha {idade_log() / 60:.0f} min: matando e relancando")
            mata_cadeia()
            time.sleep(10)
            lanca()
        time.sleep(PASSO_S)


if __name__ == "__main__":
    sys.exit(main())
