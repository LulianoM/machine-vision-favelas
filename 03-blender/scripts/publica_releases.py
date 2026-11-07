"""Empacota e sobe para releases do GitHub tudo o que mora so no desktop, menos o material PCERJ.

Uso:  python publica_releases.py [--so-listar]

Retomavel: antes de cada envio consulta os assets ja publicados e pula o que existir.
Releases:
  modelos-v1  um arquivo por peso:  <run>__best.pt, <run>__last.pt, mais os pre-treinos
  corpora-v1  um tar por corpus (sem compressao), cortado em partes de 1,9 GiB
  extras-v1   runs sem os pesos (metricas, graficos, args), resultados, cenas procedurais, assets CC0

Excluido sempre (dado operacional da PCERJ e o que reproduz a imagem ou a geometria dele):
  ortomosaicos, pasta odm/ inteira, datasets odm e cid150, teste_angulos, teste_denso,
  imagens dos runs treinados nesses datasets, logs com coordenada.
Excluido por licenca de terceiros (baixar da fonte, ver REPRODUZIR.md): VisDrone, HERIDAL,
  e as imagens VisDrone dos corpora mistos (ficam rotulos e composicao.json).
Remontar uma parte cortada:  cat NOME.tar.part* > NOME.tar && tar xf NOME.tar
"""
import hashlib, io, json, os, re, subprocess, sys, tarfile
from pathlib import Path

RAIZ = Path(r"C:\arma3-favela")
BL = RAIZ / "blender"
REPO = "LulianoM/machine-vision-favelas"
TMP = Path(os.environ.get("PUBLICA_TMP", r"C:\arma3-favela\_publica_tmp"))
PARTE = int(1.9 * 2**30)
MANIFESTO = Path(__file__).resolve().parents[2] / "06-resultados" / "releases-manifesto.jsonl"

PCERJ = re.compile(r"odm|cid150|ortomosaico|gen_cidade|build_cidade|jacarezinho\.blend|quadra\.blend|sudoeste|nordeste", re.I)
NEGA_PASTA = {"dataset_odm", "dataset_odm_tiles", "dataset_cid150", "dataset_cid150_tiles",
              "teste_angulos", "teste_denso", "aval_angulos", "aval_denso", "runs", "__pycache__",
              "fila", "fila3", "fila4", "fila5", "fila6"}
IMG = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp", ".mp4"}
TEXTO = {".jsonl", ".yaml", ".yml", ".json", ".log", ".txt", ".csv"}

NOTAS = {
    "modelos-v1": "Pesos YOLO (Ultralytics) de todos os runs do desktop. Nome: <run>__best.pt / <run>__last.pt. "
                  "Os runs blender_odm_tiles e cid150_s foram treinados em cenas com textura PCERJ; o peso vai, as imagens nao. "
                  "Ver REPRODUZIR.md e 06-resultados/RESULTADOS.md.",
    "corpora-v1": "Corpora sinteticos (Blender, Poly Haven CC0, OSM), formato YOLO. Um tar por corpus, sem compressao, "
                  "cortado em partes de 1,9 GiB. Remontar: cat NOME.tar.part* > NOME.tar && tar xf NOME.tar. "
                  "SHA256 de cada parte em 06-resultados/releases-manifesto.jsonl.",
    "extras-v1": "Runs sem os pesos (results.csv, args.yaml, graficos), resultados JSON, cenas procedurais .blend e assets CC0.",
}


def sh(*a, check=True):
    return subprocess.run(a, capture_output=True, text=True, encoding="utf-8", errors="replace", check=check)


def publicados(tag):
    r = sh("gh", "release", "view", tag, "-R", REPO, "--json", "assets", check=False)
    if r.returncode != 0:
        sh("gh", "release", "create", tag, "-R", REPO, "-t", tag, "-n", NOTAS[tag])
        return set()
    return {a["name"] for a in json.loads(r.stdout)["assets"]}


def sobe(tag, arq, ja, meta):
    if arq.name in ja:
        return
    h = hashlib.sha256()
    with open(arq, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    for tent in range(4):
        r = sh("gh", "release", "upload", tag, str(arq), "-R", REPO, "--clobber", check=False)
        if r.returncode == 0:
            break
        print(f"  falha ({tent+1}): {r.stderr.strip()[:200]}", flush=True)
    else:
        raise SystemExit(f"desisti de {arq.name}")
    ja.add(arq.name)
    with open(MANIFESTO, "a", encoding="utf-8") as m:
        m.write(json.dumps({"release": tag, "arquivo": arq.name, "bytes": arq.stat().st_size,
                            "sha256": h.hexdigest().upper(), **meta}, ensure_ascii=False) + "\n")
    print(f"  ok {tag}/{arq.name} ({arq.stat().st_size/2**20:.0f} MB)", flush=True)


def toca_pcerj(pasta):
    for p in pasta.rglob("*"):
        if p.suffix.lower() in TEXTO and p.stat().st_size < 50 * 2**20:
            try:
                if PCERJ.search(p.read_text(encoding="utf-8", errors="ignore")):
                    return p
            except OSError:
                pass
    return None


class Fatiador(io.RawIOBase):
    def __init__(self, base):
        self.base, self.n, self.usado, self.partes = base, 0, 0, []
        self._abre()

    def _abre(self):
        p = Path(f"{self.base}.part{self.n:03d}")
        self.partes.append(p)
        self.f = open(p, "wb")

    def writable(self):
        return True

    def write(self, b):
        b = memoryview(b)
        total = len(b)
        while len(b):
            cabe = PARTE - self.usado
            if cabe == 0:
                self.f.close(); self.n += 1; self.usado = 0; self._abre(); cabe = PARTE
            k = min(cabe, len(b))
            self.f.write(b[:k]); self.usado += k; b = b[k:]
        return total

    def close(self):
        self.f.close()
        super().close()


def tar_fatiado(nome, membros):
    """membros: lista de (caminho_no_disco, nome_no_tar). Devolve as partes."""
    TMP.mkdir(parents=True, exist_ok=True)
    fat = Fatiador(TMP / f"{nome}.tar")
    with tarfile.open(fileobj=fat, mode="w|", format=tarfile.PAX_FORMAT) as t:
        for disco, arc in membros:
            t.add(disco, arcname=arc, recursive=False)
    fat.close()
    if len(fat.partes) == 1:
        unico = TMP / f"{nome}.tar"
        fat.partes[0].replace(unico)
        return [unico]
    return fat.partes


def arquivos(pasta, filtro=lambda p: True):
    return [(p, p.relative_to(pasta.parent).as_posix()) for p in sorted(pasta.rglob("*")) if p.is_file() and filtro(p)]


def envia_tar(tag, nome, membros, ja, meta):
    if not membros:
        return
    if f"{nome}.tar" in ja or f"{nome}.tar.part000" in ja:
        print(f"  ja publicado: {nome}", flush=True)
        return
    partes = tar_fatiado(nome, membros)
    for p in partes:
        sobe(tag, p, ja, {**meta, "partes": len(partes)})
        p.unlink()


def main(so_listar=False):
    ex = []
    # 1. pesos
    pesos = []
    for pt in sorted((BL / "runs" / "detect").glob("*/weights/*.pt")):
        pesos.append((pt, f"{pt.parent.parent.name}__{pt.name}"))
    for pt in list(BL.glob("*.pt")) + list((BL / "weights").glob("*.pt")):
        pesos.append((pt, f"pretreino__{pt.name}"))
    # 2. corpora: toda pasta com data.yaml, ou ds_*/_dose/_oblvar
    corpora, outras = [], []
    for d in sorted(p for p in BL.iterdir() if p.is_dir()):
        if d.name in NEGA_PASTA or d.name.startswith(("test_odm", "test_cid")):
            ex.append((d.name, "lista fixa PCERJ / sem valor")); continue
        hit = toca_pcerj(d)
        if hit and not d.name.startswith("ds_misto"):
            ex.append((d.name, f"menciona PCERJ em {hit.name}")); continue
        (corpora if (d / "data.yaml").exists() or d.name.startswith(("ds_", "_dose", "_oblvar")) else outras).append(d)
    # 3. runs sem pesos
    runs = []
    for r in sorted((BL / "runs" / "detect").iterdir()):
        sens = r.name.startswith(("blender_odm", "cid150")) or r.name.startswith("val-") or r.name in ("train", "val")
        args = r / "args.yaml"
        if args.exists() and PCERJ.search(args.read_text(errors="ignore")):
            sens = True
        runs.append((r, sens))
    # 4. assets CC0
    assets = [a for a in (RAIZ / "assets").iterdir() if a.name != "ortomosaico"]

    print(f"pesos: {len(pesos)} | corpora: {len(corpora)} | outras pastas: {len(outras)} | runs: {len(runs)} | assets: {len(assets)}")
    print("excluidos:"); [print(f"  {n}: {m}") for n, m in ex]
    print("corpora:", " ".join(d.name for d in corpora))
    print("outras:", " ".join(d.name for d in outras))
    if so_listar:
        return

    ja = publicados("modelos-v1")
    for pt, nome in pesos:
        alvo = TMP / nome
        if nome in ja:
            continue
        TMP.mkdir(parents=True, exist_ok=True)
        if alvo.exists():
            alvo.unlink()
        os.link(pt, alvo)
        sobe("modelos-v1", alvo, ja, {"origem": str(pt.relative_to(RAIZ))})
        alvo.unlink()

    ja = publicados("extras-v1")
    membros = []
    for r, sens in runs:
        membros += arquivos(r, lambda p: p.suffix != ".pt" and not (sens and p.suffix.lower() in IMG))
    envia_tar("extras-v1", "runs_sem_pesos", membros, ja, {"conteudo": "runs/detect sem .pt"})
    envia_tar("extras-v1", "blender_resultados", arquivos(BL / "resultados", lambda p: not PCERJ.search(p.name)),
              ja, {"pasta": "resultados (sem os JSON dos runs odm e cid150)"})
    for d in outras:
        envia_tar("extras-v1", f"blender_{d.name}", arquivos(d), ja, {"pasta": d.name})
    for a in assets:
        if a.is_file():
            envia_tar("extras-v1", f"assets_{a.stem}", [(a, a.name)], ja, {"pasta": "assets"})
        else:
            envia_tar("extras-v1", f"assets_{a.name}", arquivos(a), ja, {"pasta": "assets"})

    ja = publicados("corpora-v1")
    for d in corpora:
        filtro = (lambda p: p.suffix.lower() not in IMG) if d.name.startswith("ds_misto") else (lambda p: True)
        envia_tar("corpora-v1", d.name, arquivos(d, filtro), ja, {"pasta": d.name})
    print("FIM", flush=True)


if __name__ == "__main__":
    main("--so-listar" in sys.argv)
