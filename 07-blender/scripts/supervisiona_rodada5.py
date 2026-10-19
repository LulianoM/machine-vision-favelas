#!/usr/bin/env python3
"""
supervisiona_rodada5.py: mantem a rodada 5 rodando ate o fim, em janela propria, fora do app do Claude.

Copia do supervisor das rodadas 3 e 4 (25/09), que funcionou. Por que existe. Na noite de 24 para 25/09
o PC caiu e religou, mas a fila so voltava se alguem abrisse uma sessao do Claude, e ficou 9,5 h parada;
processo nascido de uma sessao do Claude morre quando o app reinicia. Este supervisor:

  - e aberto por retoma_rodada5.cmd (duplo clique, ou um atalho retoma_rodada5.lnk na pasta Inicializar,
    criado so com o OK do autor), ou seja pelo shell do usuario: o Blender carrega as extensoes do
    usuario (MPFB), o que NAO acontece quando o processo nasce do Agendador de Tarefas, do WMI ou de um
    explorer lancado por DCOM (testado em 23 e 25/09);
  - roda numa janela minimizada propria ("rodada5 - nao feche"), entao nao depende do app do Claude;
  - a cada 5 min: se a cadeia nao esta rodando, lanca; se esta rodando mas nenhum log de fila5 foi
    escrito em 60 min (45 na rodada 3; sobe porque o sorteio sem render dos 280 quadros de M5 pode
    passar de 37 min calado), mata a arvore dela e relanca (a cadeia e idempotente e tem trava);
  - sai quando a rodada grava "fim" no estado, e ao sair apaga o proprio atalho de inicializacao;
  - com fila5/PAUSA presente, sai sem lancar nada.

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
FILA = os.path.join(RAIZ, "fila5")
ESTADO = os.path.join(FILA, "estado.json")
LOGV = os.path.join(RAIZ, "vigia5.log")
PY = os.path.join("C:" + os.sep, "arma3-favela", "venv", "Scripts", "python.exe")
RODADA = os.path.join(SCR, "rodada5.py")
ATALHO = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs",
                      "Startup", "retoma_rodada5.lnk")
PARADO_S = 60 * 60
PASSO_S = 5 * 60
FILHOS = ("gen_morro.py", "train_yolo_win.py", "resume=True", "confusao_armado.py", "por_regime.py",
          "visdrone_preds.py", "preds_nadir.py", "avalia_sim2real.py")


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


def falhas():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f).get("grupos_com_falha") or []
    except (OSError, ValueError):
        return []


def idade_log():
    logs = glob.glob(os.path.join(FILA, "*.log"))
    if not logs:
        return 0
    return time.time() - max(os.path.getmtime(x) for x in logs)


def mata_cadeia():
    alvos = []
    for p in processos("rodada5.py"):
        try:
            alvos += p.children(recursive=True) + [p]
        except psutil.Error:
            pass
    for p in psutil.process_iter():
        try:
            cmd = " ".join(p.cmdline())
        except (psutil.Error, OSError):
            continue
        if any(k in cmd for k in FILHOS):
            alvos.append(p)
    for p in alvos:
        try:
            p.kill()
        except psutil.Error:
            pass
    psutil.wait_procs(alvos, timeout=30)
    try:
        os.remove(os.path.join(FILA, "rodada5.trava"))
    except OSError:
        pass


def lanca():
    # compartilha o console deste supervisor: fica visivel na mesma janela minimizada
    subprocess.Popen([PY, "-u", RODADA], cwd=RAIZ)


def main():
    if processos("supervisiona_rodada5.py"):
        print("outro supervisor ja esta rodando", flush=True)
        return 0
    os.makedirs(FILA, exist_ok=True)
    log("iniciado")
    primeira = True
    while True:
        # PAUSA: o autor pediu para usar o PC. Nada e lancado enquanto o arquivo existir,
        # inclusive quando o atalho de inicializacao abre o supervisor depois de um reinicio.
        if os.path.exists(os.path.join(FILA, "PAUSA")):
            log("PAUSA presente: supervisor sai sem lancar nada")
            return 0
        # Um `fim` com grupo em falha (por exemplo P, que encerra a cadeia) nao impede a relancada
        # pedida pelo autor: na primeira volta o supervisor lanca a cadeia, que tira o `fim` e tenta de
        # novo o que falhou. Um `fim` sem falha e rodada concluida.
        if primeira and fim() and falhas() and not processos("rodada5.py"):
            log(f"estado com fim e falha nos grupos {falhas()}: relancando a cadeia para tentar de novo")
            lanca()
            primeira = False
            time.sleep(PASSO_S)
            continue
        primeira = False
        if fim() and not processos("rodada5.py"):
            log("rodada encerrada; apagando o atalho de inicializacao e saindo")
            try:
                os.remove(ATALHO)
            except OSError:
                pass
            return 0
        if not processos("rodada5.py"):
            log("cadeia nao esta rodando: lancando")
            try:
                os.remove(os.path.join(FILA, "rodada5.trava"))
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
