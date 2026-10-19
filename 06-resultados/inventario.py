#!/usr/bin/env python3
"""
inventario.py: inventario dos corpora procedurais (gen_morro) e dos runs de treino usados no
artigo, para 06-resultados/ONDE-ESTAO-OS-DADOS.md. So le; nada e gravado em C:/arma3-favela.

Para cada corpus de C:/arma3-favela/blender/ds_* (mais as seis pastas _dose_s*, que guardam os
quadros e os manifests por sitio de ds_variedade): tamanho, numero de arquivos, imagens train/val,
rotulos .txt, caixas, datas, SHA256 do manifest.jsonl (quando existe), do data.yaml e do
"arquivo de rotulos". O arquivo de rotulos nao existe em disco: e um tar deterministico montado
em memoria com todos os labels/**/*.txt do corpus (ordem alfabetica do caminho relativo, formato
USTAR, mtime 0, uid e gid 0, modo 0644, sem os .cache do Ultralytics). Quem quiser conferir roda
o script de novo; o hash so muda se algum rotulo mudar.

Para cada run de C:/arma3-favela/blender/runs/detect/<run> (mais a pasta irma <run>_val, quando
existe): tamanho, numero de arquivos e SHA256 de weights/best.pt e weights/last.pt.

Regra dura: a lista e fechada (CORPORA, RUNS, FORA_DO_ARTIGO). Nenhum caminho com odm ou cid150 e
aberto; o script aborta se algum nome da lista contiver um dos dois.

Uso (revisao de 2026-10-18):
  C:/arma3-favela/venv/Scripts/python.exe 06-resultados/inventario.py
Saida: tabelas em Markdown no stdout.
"""
import hashlib
import io
import os
import sys
import tarfile
from datetime import datetime

RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
DETECT = os.path.join(RAIZ, "runs", "detect")
PROIBIDO = ("odm", "cid150")

# (pasta, nome no artigo, papel)
CORPORA = [
    ("ds_morro_clima", "Pilot corpus (1080p)", "quadros"),
    ("ds_morro_clima_tiles", "Pilot corpus, ladrilhos de 640 px", "ladrilhos"),
    ("ds_morro_4k", "S-nadir-150 (corpus of record)", "quadros"),
    ("ds_morro_4k_tiles", "S-nadir-150, ladrilhos", "ladrilhos"),
    ("ds_variedade", "S-nadir-150-six", "quadros"),
    ("ds_variedade_tiles", "S-nadir-150-six, ladrilhos", "ladrilhos"),
    ("_dose_s-1", "S-nadir-150-six, sítio -1 (30 quadros; ds_variedade junta os seis)", "sitio"),
    ("_dose_s0", "S-nadir-150-six, sítio 0", "sitio"),
    ("_dose_s1", "S-nadir-150-six, sítio 1", "sitio"),
    ("_dose_s2", "S-nadir-150-six, sítio 2", "sitio"),
    ("_dose_s3", "S-nadir-150-six, sítio 3", "sitio"),
    ("_dose_s4", "S-nadir-150-six, sítio 4", "sitio"),
    ("ds_morro_obl", "S-oblique", "quadros"),
    ("ds_morro_obl_tiles", "S-oblique, ladrilhos", "ladrilhos"),
    ("ds_oblvar", "S-oblique-six", "quadros"),
    ("ds_oblvar_tiles", "S-oblique-six, ladrilhos", "ladrilhos"),
    ("ds_armado_75", "S-nadir-75 (three classes)", "quadros"),
    ("ds_armado_75_tiles", "S-nadir-75, ladrilhos", "ladrilhos"),
    ("ds_armado_35", "S-nadir-35", "quadros"),
    ("ds_armado_35_tiles", "S-nadir-35, ladrilhos", "ladrilhos"),
    ("ds_armado_75g", "Twin of S-nadir-35 at 75 m", "quadros"),
    ("ds_armado_75g_tiles", "Twin at 75 m, ladrilhos", "ladrilhos"),
    ("ds_armado_150g", "Twin of S-nadir-35 at 150 m", "quadros"),
    ("ds_armado_150g_tiles", "Twin at 150 m, ladrilhos", "ladrilhos"),
    ("ds_armado_35_extra", "New frames, 35 m (80, teste)", "quadros"),
    ("ds_armado_75g_extra", "New frames, twin at 75 m (80, teste)", "quadros"),
    ("ds_armado_75_inedita", "Unseen-weapon test frames (50)", "quadros"),
    ("ds_armado_75_porte", "Carried-as-weapon re-render (50)", "quadros"),
    ("ds_regime_4k", "Per-regime test frames (120)", "quadros"),
    ("ds_regime_4k_tiles", "Per-regime test, ladrilhos", "ladrilhos"),
    ("ds_misto05", "F-joint 5% (890 ladrilhos de ds_oblvar_tiles + 324 VisDrone, link fisico)", "misto"),
    ("ds_misto10", "F-joint 10% (890 ladrilhos de ds_oblvar_tiles + 647 VisDrone, link fisico)", "misto"),
]

# (run, modelo no artigo, corpus de treino)
RUNS = [
    ("morro_clima_s", "Pilot model", "ds_morro_clima_tiles"),
    ("r_pareado", "R", "VisDrone, 1.106 imagens (visdrone_sub)"),
    ("s_nadir_4k", "S-nadir-150", "ds_morro_4k_tiles"),
    ("s_variedade", "S-nadir-150-six", "ds_variedade_tiles"),
    ("s_obliquo", "S-oblique", "ds_morro_obl_tiles"),
    ("s_oblvar", "S-oblique-six (seed 0)", "ds_oblvar_tiles"),
    ("s_oblvar_sd1", "S-oblique-six (seed 1)", "ds_oblvar_tiles"),
    ("s_oblvar_sd2", "S-oblique-six (seed 2)", "ds_oblvar_tiles"),
    ("ft05_sint", "F-synthetic 5% (seed 0)", "fatia ft05 do VisDrone, a partir de s_oblvar"),
    ("ft05_sint_sd1", "F-synthetic 5% (seed 1)", "fatia ft05, a partir de s_oblvar_sd1"),
    ("ft05_sint_sd2", "F-synthetic 5% (seed 2)", "fatia ft05, a partir de s_oblvar_sd2"),
    ("ft05_coco", "F-generic 5% (seed 0)", "fatia ft05, a partir do COCO"),
    ("ft05_coco_sd1", "F-generic 5% (seed 1)", "fatia ft05, a partir do COCO"),
    ("ft05_coco_sd2", "F-generic 5% (seed 2)", "fatia ft05, a partir do COCO"),
    ("ft10_sint", "F-synthetic 10%", "fatia ft10, a partir de s_oblvar"),
    ("ft10_coco", "F-generic 10%", "fatia ft10, a partir do COCO"),
    ("misto05", "F-joint 5%", "ds_misto05"),
    ("misto10", "F-joint 10%", "ds_misto10"),
    ("armado_75", "S-nadir-75 (three classes)", "ds_armado_75_tiles"),
    ("armado_35", "S-nadir-35 (seed 0)", "ds_armado_35_tiles"),
    ("armado_35_sd1", "S-nadir-35 (seed 1)", "ds_armado_35_tiles"),
    ("armado_35_sd2", "S-nadir-35 (seed 2)", "ds_armado_35_tiles"),
    ("armado_75g", "Twin at 75 m (seed 0)", "ds_armado_75g_tiles"),
    ("armado_75g_sd1", "Twin at 75 m (seed 1)", "ds_armado_75g_tiles"),
    ("armado_75g_sd2", "Twin at 75 m (seed 2)", "ds_armado_75g_tiles"),
    ("armado_150g", "Twin at 150 m", "ds_armado_150g_tiles"),
]

# rodada que produziu cada pasta (DIARIO.md: cadeia de 20 a 22/09; rodada 2 de 22/09 22:28 a
# 24/09 16:54; rodada 3 de 24/09 a 26/09 17:54; rodada 4 de 27/09 11:31 a 30/09 10:25)
C0, R2, R3, R4 = "cadeia 20 a 22/09", "rodada 2", "rodada 3", "rodada 4"
RODADA = {
    "ds_morro_clima": C0, "ds_morro_clima_tiles": C0, "ds_morro_4k": C0, "ds_morro_4k_tiles": C0,
    "ds_armado_75": C0, "ds_armado_75_tiles": C0,
    "ds_variedade": R2, "ds_variedade_tiles": R2, "ds_morro_obl": R2, "ds_morro_obl_tiles": R2,
    "ds_armado_35": R2, "ds_armado_35_tiles": R2,
    "ds_oblvar": R3, "ds_oblvar_tiles": R3, "ds_armado_75g": R3, "ds_armado_75g_tiles": R3,
    "ds_armado_75_inedita": R3,
    "ds_armado_75_porte": R4, "ds_armado_150g": R4, "ds_armado_150g_tiles": R4, "ds_armado_35_extra": R4,
    "ds_armado_75g_extra": R4, "ds_regime_4k": R4, "ds_regime_4k_tiles": R4, "ds_misto05": R4, "ds_misto10": R4,
    "morro_clima_s": C0, "s_nadir_4k": C0, "r_pareado": C0, "armado_75": C0,
    "s_variedade": R2, "s_obliquo": R2, "armado_35": R2,
    "s_oblvar": R3, "armado_75g": R3, "ft05_sint": R3, "ft05_coco": R3, "ft10_sint": R3, "ft10_coco": R3,
}
for _s in ("-1", "0", "1", "2", "3", "4"):
    RODADA["_dose_s" + _s] = R2


def rodada(nome):
    return RODADA.get(nome, R4)   # o que sobra (misto*, armado_150g, sementes sd1 e sd2) e da rodada 4


# pastas procedurais fora do artigo: so tamanho e contagem
FORA_DO_ARTIGO = [
    os.path.join(RAIZ, "ds_morro"),
    os.path.join(RAIZ, "ds_morro_teste"),
    os.path.join(RAIZ, "ds_obj_teste"),
    os.path.join(RAIZ, "ds_armado_75_descartado"),
    os.path.join(RAIZ, "ds_morro_obl_descartado_zero_caixas"),
    os.path.join(DETECT, "r_cheio"),
    os.path.join(DETECT, "s_obliquo_descartado_zero_caixas"),
    os.path.join(DETECT, "s_obliquo_val_descartado_zero_caixas"),
]


def confere_nome(p):
    low = p.lower()
    for x in PROIBIDO:
        if x in low:
            sys.exit(f"abortado: caminho proibido na lista: {p}")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest().upper()


def varre(pasta, vistos=None):
    """tamanho aparente, tamanho unico (descontando links fisicos ja vistos), arquivos, mtime min e max"""
    tam = unico = n = 0
    tmin = tmax = None
    for raiz, _, arqs in os.walk(pasta):
        for a in arqs:
            st = os.stat(os.path.join(raiz, a))
            tam += st.st_size
            n += 1
            chave = (st.st_dev, st.st_ino)
            if vistos is None or chave not in vistos:
                unico += st.st_size
                if vistos is not None:
                    vistos.add(chave)
            tmin = st.st_mtime if tmin is None else min(tmin, st.st_mtime)
            tmax = st.st_mtime if tmax is None else max(tmax, st.st_mtime)
    return tam, unico, n, tmin, tmax


def conta(p):
    return len(os.listdir(p)) if os.path.isdir(p) else 0


def tar_rotulos(pasta):
    """SHA256 do tar deterministico dos labels/**/*.txt; devolve (hash, n_txt, n_caixas)"""
    base = os.path.join(pasta, "labels")
    arqs = []
    for raiz, _, nomes in os.walk(base):
        for a in nomes:
            if a.endswith(".txt"):
                arqs.append(os.path.relpath(os.path.join(raiz, a), pasta).replace(os.sep, "/"))
    arqs.sort()
    buf = io.BytesIO()
    caixas = 0
    with tarfile.open(fileobj=buf, mode="w", format=tarfile.USTAR_FORMAT) as tf:
        for rel in arqs:
            with open(os.path.join(pasta, rel), "rb") as f:
                dado = f.read()
            caixas += sum(1 for ln in dado.splitlines() if ln.strip())
            ti = tarfile.TarInfo(rel)
            ti.size = len(dado)
            ti.mtime = 0
            ti.mode = 0o644
            ti.uid = ti.gid = 0
            ti.uname = ti.gname = ""
            tf.addfile(ti, io.BytesIO(dado))
    return hashlib.sha256(buf.getvalue()).hexdigest().upper(), len(arqs), caixas


def mb(x):
    """MB binario (2^20 bytes), como o Get-Item do PowerShell usado na primeira parte do inventario"""
    v = x / 2 ** 20
    return f"{v:,.0f}".replace(",", ".") if v >= 100 else f"{v:.1f}".replace(".", ",")


def gb(x):
    return f"{x / 2 ** 30:.1f}".replace(".", ",")


def data(t):
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M")


def dia(t):
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    for nome, _, _ in CORPORA:
        confere_nome(nome)
    for nome, _, _ in RUNS:
        confere_nome(nome)
    for p in FORA_DO_ARTIGO:
        confere_nome(p)

    vistos = set()
    total_ap = total_un = 0

    print("### Corpora\n")
    print("| Pasta | MB | Arquivos | Imagens train / val | Rótulos .txt | Caixas | Data (arquivos mais antigo e mais novo) | Rodada | Nome no artigo |")
    print("|---|---|---|---|---|---|---|---|---|")
    hashes = []
    for nome, artigo, papel in CORPORA:
        p = os.path.join(RAIZ, nome)
        tam, un, n, t0, t1 = varre(p, vistos)
        total_ap += tam
        total_un += un
        it = conta(os.path.join(p, "images", "train"))
        iv = conta(os.path.join(p, "images", "val"))
        if papel == "misto":
            # a validacao do misto aponta para a fatia sel do VisDrone, fora desta pasta
            iv_txt = "0 (val = fatia `sel` do VisDrone)"
        else:
            iv_txt = str(iv)
        h_lab, n_txt, cx = tar_rotulos(p)
        extra = f"; {mb(tam - un)} MB já contados em outra pasta (link físico)" if tam != un else ""
        print(f"| `{nome}` | {mb(tam)}{extra} | {n} | {it} / {iv_txt} | {n_txt} | {cx} | {dia(t0)} a {dia(t1)} | {rodada(nome)} | {artigo} |")
        man = os.path.join(p, "manifest.jsonl")
        dy = os.path.join(p, "data.yaml")
        comp = os.path.join(p, "composicao.json")
        if os.path.exists(man):
            h_man = sha256(man)
        elif papel == "ladrilhos":
            h_man = "não existe (ladrilhos herdam o manifest do corpus de quadros)"
        else:
            h_man = "não existe (manifests por sítio nas pastas `_dose_s*`)"
        hashes.append((nome, h_man,
                       sha256(dy) if os.path.exists(dy) else "não existe",
                       h_lab,
                       sha256(comp) if os.path.exists(comp) else None))

    print("\n### SHA256 dos corpora\n")
    print("| Pasta | `manifest.jsonl` | `data.yaml` | Arquivo de rótulos (tar determinístico de `labels/**/*.txt`) |")
    print("|---|---|---|---|")
    for nome, hm, hd, hl, hc in hashes:
        if hc:
            hm = f"não existe; `composicao.json` {hc}"
        print(f"| `{nome}` | {hm} | {hd} | {hl} |")

    print("\n### Pesos\n")
    print("| Arquivo | MB | Data | Rodada | Modelo no artigo | Corpus de treino | SHA256 |")
    print("|---|---|---|---|---|---|---|")
    runs_tab = []
    for run, artigo, corpus in RUNS:
        for w in ("best.pt", "last.pt"):
            p = os.path.join(DETECT, run, "weights", w)
            st = os.stat(p)
            print(f"| `runs\\detect\\{run}\\weights\\{w}` | {mb(st.st_size)} | {data(st.st_mtime)} | {rodada(run)} | {artigo} | {corpus} | {sha256(p)} |")
        tam, un, n, _, _ = varre(os.path.join(DETECT, run), vistos)
        pv = os.path.join(DETECT, run + "_val")
        if os.path.isdir(pv):
            tv, uv, nv, _, _ = varre(pv, vistos)
            tam += tv; un += uv; n += nv
        total_ap += tam
        total_un += un
        runs_tab.append((run, artigo, tam, n, os.path.isdir(pv)))

    print("\n### Runs\n")
    print("| Run | Pasta `_val` | MB (run mais `_val`) | Arquivos | Rodada | Modelo no artigo |")
    print("|---|---|---|---|---|---|")
    for run, artigo, tam, n, tem_val in runs_tab:
        print(f"| `{run}` | {'sim' if tem_val else 'não'} | {mb(tam)} | {n} | {rodada(run)} | {artigo} |")

    print("\n### Fora do artigo (só tamanho)\n")
    print("| Pasta | MB | Arquivos |")
    print("|---|---|---|")
    for p in FORA_DO_ARTIGO:
        tam, _, n, _, _ = varre(p)
        print(f"| `{os.path.relpath(p, RAIZ)}` | {mb(tam)} | {n} |")

    print(f"\nTotal do artigo (corpora mais runs): {gb(total_ap)} GB aparentes, {gb(total_un)} GB em disco "
          f"descontando links físicos; {len(CORPORA)} pastas de corpus, {len(RUNS)} runs.")


if __name__ == "__main__":
    main()
