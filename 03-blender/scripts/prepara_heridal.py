#!/usr/bin/env python3
"""
prepara_heridal.py: converte a HERIDAL baixada (PASCAL VOC) para YOLO, classe unica (rodada 5, R5-6;
PLANO-RODADA5.md, secao 3.3). Roda com `python -I`, de fora da pasta baixada, e so le o que foi baixado.

Fonte combinada com o autor em 18/10: Zenodo 5662351 (Pyrro, "HERIDAL dataset in keras-retinanet PASCAL
VOC format", CC BY 3.0, heridal_keras_retinanet_voc.zip, 8,31 GB, md5 c2b625ae986898a870b9d8a907aefe45),
a versao modificada usada pelo detector AIR. O artigo da base reporta 1.546 imagens de treino e 101 de
teste.

O que faz, em ordem:
  1. acha o zip em --bruto (pasta ou arquivo; a pasta _bruto nao e alterada), confere o md5 se --md5 for
     dado, e extrai numa pasta IRMA (--extraido, padrao ...\\heridal\\_extraido), nunca dentro de _bruto,
     recusando membros com caminho absoluto ou com '..' (zip slip). Uma marca .extraido_ok evita extrair
     de novo; com uma pasta ja extraida dada em --bruto, pula esta etapa;
  2. acha o layout VOC: a pasta Annotations (*.xml), a pasta de imagens (JPEGImages ou a que tiver os
     arquivos citados nos xml) e ImageSets/Main/*.txt, se houver;
  3. escolhe as imagens: com --divisao teste (padrao), as listadas no arquivo de teste de ImageSets
     (test.txt; senao o que tiver 'test' no nome); sem ImageSets de teste, todas as anotadas, e isso fica
     registrado. Com --divisao todas, todas as anotadas (a leitura literal do plano de 18/10);
  4. guarda so a classe de pessoa (nome em --classes; padrao: person, human, people, pedestrian e, se a
     base tiver um nome de classe so, esse) e grava rotulos YOLO classe 0, caixa do VOC (xmin, ymin,
     xmax, ymax em pixel) recortada a imagem e normalizada pelo tamanho do <size> do xml (ou da imagem,
     se faltar). Imagem sem pessoa entra com rotulo vazio (negativo);
  5. liga as imagens em --out/images/val por link fisico (copia se o link falhar), grava
     --out/data.yaml (train e val = images/val, so avaliacao) e as contagens em
     06-resultados/heridal_contagens.json (contagem de treino e teste das listas, imagens, caixas,
     classes encontradas, tamanhos de imagem).

  C:/arma3-favela/venv/Scripts/python.exe -I prepara_heridal.py --bruto C:/arma3-favela/real_nadir/heridal/_bruto \\
      --out C:/arma3-favela/real_nadir/heridal/yolo --md5 c2b625ae986898a870b9d8a907aefe45
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from datetime import datetime

SCR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(SCR))
RES = os.path.join(REPO, "06-resultados")
BASE = os.path.join("C:" + os.sep, "arma3-favela", "real_nadir", "heridal")
PESSOA = {"person", "human", "people", "pedestrian", "pessoa"}
EXT_IMG = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 24), b""):
            h.update(bloco)
    return h.hexdigest()


def extrai(zp, dst):
    marca = os.path.join(dst, ".extraido_ok")
    if os.path.exists(marca):
        print(f"ja extraido em {dst}", flush=True)
        return
    os.makedirs(dst, exist_ok=True)
    raiz = os.path.realpath(dst)
    with zipfile.ZipFile(zp) as z:
        membros = z.infolist()
        for mi in membros:
            nome = mi.filename.replace("\\", "/")
            if nome.startswith("/") or ":" in nome.split("/")[0] or ".." in nome.split("/"):
                raise SystemExit(f"membro recusado (caminho perigoso): {mi.filename}")
            alvo = os.path.realpath(os.path.join(dst, nome))
            if not (alvo == raiz or alvo.startswith(raiz + os.sep)):
                raise SystemExit(f"membro recusado (fora da pasta): {mi.filename}")
        print(f"extraindo {len(membros)} membros de {zp} em {dst}", flush=True)
        for k, mi in enumerate(membros):
            z.extract(mi, dst)
            if k % 500 == 0:
                print(f"  {k}/{len(membros)}", flush=True)
    with open(marca, "w", encoding="utf-8") as f:
        f.write(datetime.now().isoformat(timespec="seconds"))


def acha_layout(raiz):
    anots = [d for d in glob.glob(os.path.join(raiz, "**", "Annotations"), recursive=True) if os.path.isdir(d)]
    anots = [d for d in anots if glob.glob(os.path.join(d, "*.xml"))]
    if not anots:
        # sem pasta Annotations: a pasta com mais xml
        cont = Counter(os.path.dirname(p) for p in glob.glob(os.path.join(raiz, "**", "*.xml"), recursive=True))
        if not cont:
            raise SystemExit(f"nenhum xml VOC em {raiz}")
        anots = [cont.most_common(1)[0][0]]
    anots.sort(key=lambda d: -len(glob.glob(os.path.join(d, "*.xml"))))
    ann = anots[0]
    voc = os.path.dirname(ann)
    sets = os.path.join(voc, "ImageSets", "Main")
    if not os.path.isdir(sets):
        achados = glob.glob(os.path.join(raiz, "**", "ImageSets", "Main"), recursive=True)
        sets = achados[0] if achados else None
    # indice de imagens por nome de base, em toda a arvore extraida
    imgs = {}
    for p in glob.glob(os.path.join(raiz, "**", "*"), recursive=True):
        if p.lower().endswith(EXT_IMG) and os.path.isfile(p):
            imgs.setdefault(os.path.splitext(os.path.basename(p))[0], p)
    return ann, sets, imgs


def le_lista(p):
    return [ln.split()[0] for ln in open(p, encoding="utf-8", errors="replace") if ln.strip()]


def listas(sets):
    """train e test das listas de ImageSets/Main (so as listas gerais, sem as por classe)"""
    out = {}
    if not sets:
        return out
    for p in sorted(glob.glob(os.path.join(sets, "*.txt"))):
        nome = os.path.splitext(os.path.basename(p))[0].lower()
        if "_" in nome:          # aeroplane_train.txt e afins: listas por classe, nao entram
            continue
        out[nome] = le_lista(p)
    return out


def le_xml(p):
    r = ET.parse(p).getroot()
    fn = (r.findtext("filename") or "").strip()
    sz = r.find("size")
    W = int(float(sz.findtext("width"))) if sz is not None and sz.findtext("width") else None
    H = int(float(sz.findtext("height"))) if sz is not None and sz.findtext("height") else None
    objs = []
    for o in r.findall("object"):
        bb = o.find("bndbox")
        if bb is None:
            continue
        objs.append(((o.findtext("name") or "").strip(),
                     *(float(bb.findtext(k)) for k in ("xmin", "ymin", "xmax", "ymax"))))
    return fn, W, H, objs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bruto", default=os.path.join(BASE, "_bruto"), help="pasta com o zip, o zip, ou pasta ja extraida")
    ap.add_argument("--extraido", default=os.path.join(BASE, "_extraido"))
    ap.add_argument("--out", default=os.path.join(BASE, "yolo"))
    ap.add_argument("--md5", default=None)
    ap.add_argument("--divisao", choices=["teste", "todas"], default="teste")
    ap.add_argument("--classes", nargs="*", default=None, help="nomes de classe que contam como pessoa")
    ap.add_argument("--contagens", default=os.path.join(RES, "heridal_contagens.json"))
    a = ap.parse_args()

    zips = ([a.bruto] if a.bruto.lower().endswith(".zip") else sorted(glob.glob(os.path.join(a.bruto, "*.zip"))))
    if zips:
        zp = zips[0]
        if a.md5:
            h = md5(zp)
            if h.lower() != a.md5.lower():
                raise SystemExit(f"md5 de {zp} e {h}, esperado {a.md5}: download incompleto ou outro arquivo")
            print(f"md5 confere: {h}", flush=True)
        raiz_ext = os.path.abspath(a.extraido)
        bruto_abs = os.path.abspath(os.path.dirname(zp) if zp.lower().endswith(".zip") else a.bruto)
        if raiz_ext == bruto_abs or raiz_ext.startswith(bruto_abs + os.sep):
            raise SystemExit("a pasta de extracao nao pode ficar dentro da pasta baixada")
        extrai(zp, raiz_ext)
    else:
        raiz_ext = os.path.abspath(a.bruto)
        print(f"sem zip em {a.bruto}: usando a pasta como ja extraida", flush=True)

    ann, sets, imgs = acha_layout(raiz_ext)
    ls = listas(sets)
    xmls = {os.path.splitext(os.path.basename(p))[0]: p for p in glob.glob(os.path.join(ann, "*.xml"))}
    print(f"Annotations: {ann} ({len(xmls)} xml); ImageSets: {sets} {({k: len(v) for k, v in ls.items()})}; "
          f"{len(imgs)} imagens na arvore", flush=True)

    teste_nome = "test" if "test" in ls else next((k for k in ls if "test" in k), None)
    if a.divisao == "teste" and teste_nome:
        escolhidas = [s for s in ls[teste_nome] if s in xmls]
        criterio = f"lista ImageSets/Main/{teste_nome}.txt"
    else:
        escolhidas = sorted(xmls)
        criterio = ("todas as anotadas (--divisao todas)" if a.divisao == "todas"
                    else "todas as anotadas: sem lista de teste em ImageSets")
    if not escolhidas:
        raise SystemExit("nenhuma imagem escolhida")

    # classes
    todas_cls = Counter()
    lidos = {}
    for s in escolhidas:
        lidos[s] = le_xml(xmls[s])
        todas_cls.update(n for n, *_ in lidos[s][3])
    if a.classes:
        aceitas = {c.lower() for c in a.classes}
    elif len(todas_cls) == 1:
        aceitas = {next(iter(todas_cls)).lower()}
    else:
        aceitas = PESSOA
    if not any(c.lower() in aceitas for c in todas_cls) and todas_cls:
        raise SystemExit(f"nenhuma classe de pessoa entre {dict(todas_cls)}; passe --classes")

    try:                        # data.yaml so reaparece no fim: a cadeia nunca ve uma conversao pela metade
        os.remove(os.path.join(a.out, "data.yaml"))
    except OSError:
        pass
    di, dl = os.path.join(a.out, "images", "val"), os.path.join(a.out, "labels", "val")
    for d in (di, dl):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)
    n_cx, sem_img, vazias, tam = 0, [], 0, Counter()
    lados = []
    for s in escolhidas:
        fn, W, H, objs = lidos[s]
        src = imgs.get(os.path.splitext(fn)[0]) if fn else None
        src = src or imgs.get(s)
        if src is None:
            sem_img.append(s)
            continue
        if not W or not H:
            from PIL import Image
            with Image.open(src) as im:
                W, H = im.size
        tam[f"{W}x{H}"] += 1
        ext = os.path.splitext(src)[1].lower()
        dst = os.path.join(di, s + ext)
        try:
            os.link(src, dst)
        except OSError:
            shutil.copy2(src, dst)
        linhas = []
        for nome, x1, y1, x2, y2 in objs:
            if nome.lower() not in aceitas:
                continue
            x1, x2 = max(0.0, min(x1, x2)), min(float(W), max(x1, x2))
            y1, y2 = max(0.0, min(y1, y2)), min(float(H), max(y1, y2))
            if x2 <= x1 or y2 <= y1:
                continue
            linhas.append(f"0 {(x1 + x2) / 2 / W:.6f} {(y1 + y2) / 2 / H:.6f} {(x2 - x1) / W:.6f} {(y2 - y1) / H:.6f}")
            lados.append(max(x2 - x1, y2 - y1))
        if not linhas:
            vazias += 1
        with open(os.path.join(dl, s + ".txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(linhas) + ("\n" if linhas else ""))
        n_cx += len(linhas)
    n_img = len(escolhidas) - len(sem_img)
    with open(os.path.join(a.out, "data.yaml"), "w", encoding="utf-8") as f:
        f.write(f"path: {os.path.abspath(a.out).replace(os.sep, '/')}\ntrain: images/val\nval: images/val\n"
                "names:\n  0: pessoa\n")
    lados.sort()
    cont = {"fonte": "Zenodo 5662351, heridal_keras_retinanet_voc.zip (CC BY 3.0), versao do AIR",
            "extraido_em": raiz_ext, "annotations": ann, "imagesets": sets,
            "listas_imagesets": {k: len(v) for k, v in ls.items()},
            "xml_total": len(xmls), "divisao": a.divisao, "criterio": criterio,
            "imagens_escolhidas": len(escolhidas), "imagens_convertidas": n_img, "imagens_sem_arquivo": sem_img[:50],
            "imagens_sem_pessoa": vazias, "caixas_pessoa": n_cx,
            "classes_encontradas": dict(todas_cls), "classes_aceitas_como_pessoa": sorted(aceitas),
            "tamanhos_de_imagem": dict(tam),
            "lado_maior_caixa_px_mediana": lados[len(lados) // 2] if lados else None,
            "data_yaml": os.path.join(os.path.abspath(a.out), "data.yaml"),
            "quando": datetime.now().isoformat(timespec="seconds")}
    os.makedirs(os.path.dirname(os.path.abspath(a.contagens)), exist_ok=True)
    with open(a.contagens, "w", encoding="utf-8") as f:
        json.dump(cont, f, indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in cont.items() if k != "imagens_sem_arquivo"}, ensure_ascii=False, indent=1))
    if sem_img:
        print(f"AVISO: {len(sem_img)} xml sem imagem correspondente", flush=True)
    return 0 if n_img else 1


if __name__ == "__main__":
    sys.exit(main())
