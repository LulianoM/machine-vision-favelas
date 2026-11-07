#!/usr/bin/env python3
"""
contagens.py: contagens dos corpora sinteticos procedurais (gen_morro) e das fatias do VisDrone,
lidas dos arquivos em disco (rotulos YOLO, manifests do gerador, pastas de ladrilhos).

Revisao de 2026-10-17 (agente D1). So le; nao gera nem treina nada. Nao toca em pasta odm, cid150
nem em nada derivado do ortomosaico da PCERJ.

Uso (a partir de qualquer pasta):
  C:/arma3-favela/venv/Scripts/python.exe 06-resultados/revisao-2026-10-17/contagens.py
Saida: corpora.json e corpora.md ao lado deste script.

O que cada numero e:
  quadros           imagens inteiras (PNG do gerador), por divisao train/val
  caixas            linhas dos rotulos YOLO dos quadros, por classe e por divisao
  ladrilhos         imagens JPEG de 1280 px produzidas por tile_dataset.py (--tile 1280 --overlap 0.2,
                    --keep-empty 0.05 e --min-vis 0.4 por padrao), por divisao
  caixas_ladrilhos  linhas dos rotulos dos ladrilhos (uma caixa de quadro pode cair em mais de um
                    ladrilho por causa da sobreposicao, e caixas com menos de 40% da area no ladrilho
                    sao descartadas)
  manifest          faixas realizadas (altitude, pitch, elevacao do sol), semente, regime, sitio,
                    pessoas colocadas contra caixas retidas, soma de render_s
  gsd_cm_px         (alt_media * 36 / 28.82) / largura_px * 100: sensor 36 mm, lente 28,82 mm
                    (gen_morro.py, Z30_LENS = 4.3 * 36 / 5.37); para corpus obliquo e a GSD nominal
                    de nadir na altitude media da camera, nao a GSD real no solo
"""
import glob
import json
import os
import statistics
from collections import Counter, defaultdict

RAIZ = os.path.join("C:" + os.sep, "arma3-favela", "blender")
VIS = os.path.join("C:" + os.sep, "arma3-favela", "visdrone")
AQUI = os.path.dirname(os.path.abspath(__file__))
SENSOR_MM = 36.0
LENTE_MM = 4.3 * 36 / 5.37          # 28,82 mm equivalente (gen_morro.py, Z30_LENS)
NOMES = {0: "pessoa_armada", 1: "pessoa_desarmada", 2: "pessoa_objeto"}

# (nome interno, nome no artigo, pasta de ladrilhos ou None, manifests alternativos ou None, papel)
CORPORA = [
    ("ds_morro_clima", "Pilot corpus (1080p)", "ds_morro_clima_tiles", None,
     "piloto; treino morro_clima_s (ladrilhos de 640 px)"),
    ("ds_morro_4k", "S-nadir-150 (corpus of record)", "ds_morro_4k_tiles", None,
     "treino s_nadir_4k; define N = 1.106 ladrilhos para R"),
    ("ds_variedade", "S-nadir-150-six", "ds_variedade_tiles",
     ["_dose_s-1", "_dose_s0", "_dose_s1", "_dose_s2", "_dose_s3", "_dose_s4"],
     "treino s_variedade; 6 sitios x 30 quadros, manifests por sitio em _dose_s*"),
    ("ds_morro_obl", "S-oblique", "ds_morro_obl_tiles", None,
     "treino s_obliquo; preset --obliqua (120 m, pitch 26 a 52)"),
    ("ds_oblvar", "S-oblique-six", "ds_oblvar_tiles", None,
     "treino s_oblvar (+ sd1, sd2); 6 sitios, --pitch-obl 45 56 --camera-livre, so desarmadas"),
    ("ds_armado_75", "S-nadir-75 (original)", "ds_armado_75_tiles", None,
     "treino armado_75; 3 classes, antes de --porte-realista"),
    ("ds_armado_35", "S-nadir-35", "ds_armado_35_tiles", None,
     "treino armado_35 (+ sd1, sd2); 3 classes, --porte-realista"),
    ("ds_armado_75g", "Twin of S-nadir-35 at 75 m", "ds_armado_75g_tiles", None,
     "treino armado_75g (+ sd1, sd2); comando do 35 m com --alt 75 --alt-jitter 6"),
    ("ds_armado_150g", "Twin of S-nadir-35 at 150 m", "ds_armado_150g_tiles", None,
     "treino armado_150g; comando do 35 m com --alt 150 --alt-jitter 13"),
    ("ds_armado_35_extra", "New frames, 35 m (80)", None, None,
     "indices 200 a 279 da semente 43, so validacao; teste de armado_35 e sementes"),
    ("ds_armado_75g_extra", "New frames, twin at 75 m (80)", None, None,
     "indices 200 a 279, gemeo a 75 m, so validacao; teste de armado_75g e sementes"),
    ("ds_armado_75_inedita", "Unseen-weapon test frames (50)", None, None,
     "comando do ds_armado_75 com semente 47 e --armas mista_inedita; teste de armado_75 e 75g"),
    ("ds_armado_75_porte", "Carried-as-weapon re-render (50)", None, None,
     "mesmo comando do inedita com --objeto-porte-arma; gemeo caixa a caixa"),
    ("ds_regime_4k", "Per-regime test frames (120)", "ds_regime_4k_tiles", None,
     "indices 180 a 299 da semente 21 com o comando do ds_morro_4k, so validacao; teste de s_nadir_4k"),
]

VISDRONE = [
    ("visdrone_yolo/train", "VisDrone-DET train (full, 6,471)", os.path.join(VIS, "visdrone_yolo", "train")),
    ("visdrone_yolo/val", "VisDrone-DET val (test set, 548)", os.path.join(VIS, "visdrone_yolo", "val")),
    ("visdrone_sub/train", "R (1,106 images, seed 21)", os.path.join(VIS, "visdrone_sub", "train")),
    ("ft/ft05", "5 per cent slice (324)", os.path.join(VIS, "ft", "ft05")),
    ("ft/ft10", "10 per cent slice (647)", os.path.join(VIS, "ft", "ft10")),
    ("ft/sel", "5 per cent selection slice (324)", os.path.join(VIS, "ft", "sel")),
]


def conta_rotulos(pasta_labels):
    """(n_arquivos, Counter classe -> caixas) a partir dos .txt YOLO"""
    arqs = sorted(glob.glob(os.path.join(pasta_labels, "*.txt")))
    c = Counter()
    for a in arqs:
        for ln in open(a, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                c[int(ln.split()[0])] += 1
    return len(arqs), c


def conta_imagens(pasta):
    if not os.path.isdir(pasta):
        return 0
    return len([f for f in os.listdir(pasta) if f.lower().endswith((".png", ".jpg", ".jpeg"))])


def le_manifests(caminhos):
    regs = []
    for c in caminhos:
        if not os.path.exists(c):
            continue
        for ln in open(c, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                regs.append(json.loads(ln))
    return regs


def faixa(vals, nd=1):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return dict(min=round(min(vals), nd), max=round(max(vals), nd),
                media=round(statistics.mean(vals), nd))


def resumo_manifest(regs, nome):
    if not regs:
        return dict(nota="sem manifest")
    r = {}
    r["linhas"] = len(regs)
    r["resolucao"] = sorted({f"{x['w']}x{x['h']}" for x in regs})
    r["sementes"] = sorted({x.get("seed") for x in regs})
    r["alt_m"] = faixa([x.get("alt") for x in regs])
    r["pitch_graus"] = faixa([x.get("pitch") for x in regs]) if any("pitch" in x for x in regs) else "nao gravado (corpus anterior ao campo pitch; faixa nominal --pitch 0 3.5)"
    r["elev_sol_graus"] = faixa([x.get("elev") for x in regs])
    r["regimes"] = dict(Counter(x.get("clima") for x in regs))
    r["split_manifest"] = dict(Counter(x.get("split") for x in regs))
    if any("sitio" in x for x in regs):
        r["quadros_por_sitio"] = dict(sorted(Counter(x["sitio"] for x in regs).items()))
    r["pessoas_colocadas"] = sum(x.get("n_pessoas", 0) for x in regs)
    r["caixas_retidas"] = sum(x.get("n_caixas", 0) for x in regs)
    r["fracao_retida"] = round(r["caixas_retidas"] / r["pessoas_colocadas"], 3) if r["pessoas_colocadas"] else None
    rs = [x.get("render_s") for x in regs if x.get("render_s") is not None]
    r["render_s_total"] = round(sum(rs), 1)
    r["render_s_mediana"] = round(statistics.median(rs), 1) if rs else None
    r["render_h_total"] = round(sum(rs) / 3600, 2)
    tipos = Counter()
    for x in regs:
        for t in x.get("tipos", []) or []:
            tipos[t] += 1
    if tipos:
        r["tipos_carregados"] = dict(sorted(tipos.items()))
    w = regs[0]["w"]
    alt = r["alt_m"]["media"]
    larg = alt * SENSOR_MM / LENTE_MM
    r["pegada_nominal_m"] = [round(larg, 1), round(larg * regs[0]["h"] / w, 1)]
    r["gsd_cm_px"] = round(larg / w * 100, 2)
    return r


def corpus(nome, artigo, tiles, manifests_alt, papel):
    base = os.path.join(RAIZ, nome)
    d = dict(nome_interno=nome, nome_artigo=artigo, papel=papel, pasta=base)
    if not os.path.isdir(base):
        d["nota"] = "pasta nao encontrada"
        return d
    # classes declaradas
    yml = os.path.join(base, "data.yaml")
    d["classes_data_yaml"] = [ln.strip() for ln in open(yml, encoding="utf-8") if ln.strip()[:1].isdigit()] if os.path.exists(yml) else None
    d["quadros"] = {}
    d["caixas"] = {}
    tot = Counter()
    for sp in ("train", "val"):
        n_img = conta_imagens(os.path.join(base, "images", sp))
        n_lab, c = conta_rotulos(os.path.join(base, "labels", sp))
        d["quadros"][sp] = n_img
        d["caixas"][sp] = {NOMES.get(k, str(k)): v for k, v in sorted(c.items())} | {"total": sum(c.values()), "rotulos": n_lab}
        tot.update(c)
    d["quadros"]["total"] = d["quadros"]["train"] + d["quadros"]["val"]
    d["caixas"]["total"] = {NOMES.get(k, str(k)): v for k, v in sorted(tot.items())} | {"total": sum(tot.values())}
    # manifest
    if manifests_alt:
        regs = le_manifests([os.path.join(RAIZ, m, "manifest.jsonl") for m in manifests_alt])
        d["manifest_origem"] = manifests_alt
        # quadros por sitio pelo prefixo do nome no corpus juntado
        pref = Counter()
        for sp in ("train", "val"):
            for f in os.listdir(os.path.join(base, "images", sp)):
                pref[f.split("_")[0]] += 1
        d["quadros_por_sitio_prefixo"] = dict(sorted(pref.items()))
    else:
        regs = le_manifests([os.path.join(base, "manifest.jsonl")])
        d["manifest_origem"] = [nome]
    d["manifest"] = resumo_manifest(regs, nome)
    # ladrilhos
    if tiles:
        tb = os.path.join(RAIZ, tiles)
        d["ladrilhos_pasta"] = tb
        d["ladrilhos"] = {}
        d["caixas_ladrilhos"] = {}
        for sp in ("train", "val"):
            n_img = conta_imagens(os.path.join(tb, "images", sp))
            n_lab, c = conta_rotulos(os.path.join(tb, "labels", sp))
            vazios = 0
            for a in glob.glob(os.path.join(tb, "labels", sp, "*.txt")):
                if os.path.getsize(a) == 0:
                    vazios += 1
            d["ladrilhos"][sp] = n_img
            d["caixas_ladrilhos"][sp] = {NOMES.get(k, str(k)): v for k, v in sorted(c.items())} | {"total": sum(c.values()), "ladrilhos_vazios": vazios}
        # tamanho do ladrilho pelo primeiro arquivo
        try:
            from PIL import Image
            f0 = sorted(os.listdir(os.path.join(tb, "images", "train")))
            f0 = f0 or sorted(os.listdir(os.path.join(tb, "images", "val")))
            sp0 = "train" if os.path.isdir(os.path.join(tb, "images", "train")) and os.listdir(os.path.join(tb, "images", "train")) else "val"
            with Image.open(os.path.join(tb, "images", sp0, f0[0])) as im:
                d["ladrilho_px"] = list(im.size)
        except Exception as e:
            d["ladrilho_px"] = f"nao lido: {e}"
    return d


def visdrone_sub(nome, artigo, pasta):
    d = dict(nome_interno=nome, nome_artigo=artigo, pasta=pasta)
    d["imagens"] = conta_imagens(os.path.join(pasta, "images"))
    n_lab, c = conta_rotulos(os.path.join(pasta, "labels"))
    d["rotulos"] = n_lab
    d["instancias_pessoa"] = sum(c.values())
    d["classes_presentes"] = sorted(c.keys())
    d["imagens_sem_caixa"] = sum(1 for a in glob.glob(os.path.join(pasta, "labels", "*.txt")) if os.path.getsize(a) == 0)
    return d


def visdrone_val_original():
    """conta no formato original do VisDrone-DET val: categorias 1 (pedestrian) e 2 (people) com
    score != 0, mais as regioes ignoradas (categoria 0)"""
    anot = os.path.join(VIS, "VisDrone2019-DET-val", "annotations")
    arqs = sorted(glob.glob(os.path.join(anot, "*.txt")))
    ped = peo = ign = score0_outras = 0
    img_ign = 0
    for a in arqs:
        tem_ign = False
        for ln in open(a, encoding="utf-8"):
            v = [x for x in ln.strip().split(",") if x != ""]
            if len(v) < 6:
                continue
            score, cat = int(v[4]), int(v[5])
            if cat == 0:                      # regiao ignorada (categoria 0), como no kit oficial
                ign += 1
                tem_ign = True
                continue
            if score == 0:                    # score 0 em outra categoria: tambem descartado pelo conversor
                score0_outras += 1
                continue
            if cat == 1:
                ped += 1
            elif cat == 2:
                peo += 1
        img_ign += tem_ign
    return dict(imagens=len(arqs), pedestrian=ped, people=peo, pessoa_total=ped + peo,
                regioes_ignoradas_cat0=ign, imagens_com_regiao_ignorada=img_ign,
                linhas_score0_outras_categorias=score0_outras,
                regra="categoria 1 ou 2 e score != 0 (visdrone_to_yolo.py descarta score 0 = regiao ignorada)")


def main():
    saida = dict(gerado_em="2026-10-17", script=os.path.abspath(__file__),
                 comando="C:/arma3-favela/venv/Scripts/python.exe 06-resultados/revisao-2026-10-17/contagens.py",
                 camera=dict(sensor_mm=SENSOR_MM, lente_mm=round(LENTE_MM, 2),
                             nota="gen_morro.py: c.sensor_width = 36, sensor_fit HORIZONTAL, c.lens = Z30_LENS = 4.3 * 36 / 5.37"),
                 corpora=[], visdrone=[])
    for args in CORPORA:
        print("corpus", args[0], flush=True)
        saida["corpora"].append(corpus(*args))
    for args in VISDRONE:
        print("visdrone", args[0], flush=True)
        saida["visdrone"].append(visdrone_sub(*args))
    saida["visdrone_val_formato_original"] = visdrone_val_original()
    fat = os.path.join(VIS, "ft", "fatias.json")
    if os.path.exists(fat):
        saida["fatias_json"] = json.load(open(fat, encoding="utf-8"))
    with open(os.path.join(AQUI, "corpora.json"), "w", encoding="utf-8") as f:
        json.dump(saida, f, indent=1, ensure_ascii=False)
    escreve_md(saida)
    print("gravado corpora.json e corpora.md em", AQUI)


def _c(d, k):
    return d.get(k, 0)


def escreve_md(s):
    L = []
    L.append("# Corpora do artigo: contagens lidas do disco (revisão de 2026-10-17, agente D1)\n")
    L.append("Gerado por `contagens.py` com o comando `" + s["comando"] + "`. Cada número vem dos rótulos YOLO, dos manifests do gerador e das pastas de ladrilhos em `C:\\arma3-favela\\blender\\` e `C:\\arma3-favela\\visdrone\\`. Nenhum corpus derivado do ortomosaico da PCERJ foi lido. Detalhe por corpus em `corpora.json`.\n")
    L.append("Câmera de todos os corpora sintéticos: sensor de 36 mm (ajuste horizontal) e lente de 28,82 mm (`Z30_LENS = 4.3 * 36 / 5.37` em `gen_morro.py`). A GSD da tabela é (altitude média × 36 / 28,82) / largura em px; para os corpora oblíquos é a GSD nominal de nadir na altitude média da câmera, não a GSD real no solo, que varia ao longo do quadro.\n")
    L.append("## 1. Corpora sintéticos\n")
    L.append("| Nome interno | Nome no artigo | Render | Altitude realizada (m) | Pitch realizado (graus a partir do nadir) | GSD (cm/px) | Quadros train / val | Ladrilhos train / val | Semente | Sítios (quadros) |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for c in s["corpora"]:
        m = c.get("manifest", {})
        alt = m.get("alt_m") or {}
        p = m.get("pitch_graus")
        if isinstance(p, dict):
            ptxt = f"{p['min']} a {p['max']} (média {p['media']})"
        else:
            ptxt = p or "não apurado"
        lad = c.get("ladrilhos")
        ladtxt = f"{lad['train']} / {lad['val']}" if lad else "não ladrilhado"
        if "quadros_por_sitio" in m:
            sit = ", ".join(f"{k}: {v}" for k, v in m["quadros_por_sitio"].items())
        elif "quadros_por_sitio_prefixo" in c:
            sit = ", ".join(f"{k}: {v}" for k, v in c["quadros_por_sitio_prefixo"].items())
        else:
            sit = "sítio -1 (histórico): " + str(c["quadros"]["total"])
        L.append(f"| `{c['nome_interno']}` | {c['nome_artigo']} | {', '.join(m.get('resolucao', ['?']))} | "
                 f"{alt.get('min')} a {alt.get('max')} (média {alt.get('media')}) | {ptxt} | {m.get('gsd_cm_px')} | "
                 f"{c['quadros']['train']} / {c['quadros']['val']} | {ladtxt} | {', '.join(str(x) for x in m.get('sementes', []))} | {sit} |")
    L.append("")
    L.append("## 2. Instâncias anotadas por classe (rótulos dos quadros inteiros)\n")
    L.append("| Nome interno | Classes | Train: armada / desarmada / objeto / total | Val: armada / desarmada / objeto / total | Pessoas colocadas | Caixas retidas | Fração retida | Caixas por quadro |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c in s["corpora"]:
        tr, va = c["caixas"]["train"], c["caixas"]["val"]
        m = c.get("manifest", {})
        ncls = len(c.get("classes_data_yaml") or [])
        L.append(f"| `{c['nome_interno']}` | {ncls} | {_c(tr,'pessoa_armada')} / {_c(tr,'pessoa_desarmada')} / {_c(tr,'pessoa_objeto')} / {tr['total']} | "
                 f"{_c(va,'pessoa_armada')} / {_c(va,'pessoa_desarmada')} / {_c(va,'pessoa_objeto')} / {va['total']} | "
                 f"{m.get('pessoas_colocadas')} | {m.get('caixas_retidas')} | {m.get('fracao_retida')} | {round(c['caixas']['total']['total'] / max(1, c['quadros']['total']), 1)} |")
    L.append("")
    L.append("## 3. Instâncias por classe nos ladrilhos de treino (o que o detector vê)\n")
    L.append("| Nome interno | Ladrilhos train / val | Train: armada / desarmada / objeto / total | Val: armada / desarmada / objeto / total | Ladrilhos vazios mantidos train / val |")
    L.append("|---|---|---|---|---|")
    for c in s["corpora"]:
        if "caixas_ladrilhos" not in c:
            continue
        tr, va = c["caixas_ladrilhos"]["train"], c["caixas_ladrilhos"]["val"]
        L.append(f"| `{c['nome_interno']}` | {c['ladrilhos']['train']} / {c['ladrilhos']['val']} | "
                 f"{_c(tr,'pessoa_armada')} / {_c(tr,'pessoa_desarmada')} / {_c(tr,'pessoa_objeto')} / {tr['total']} | "
                 f"{_c(va,'pessoa_armada')} / {_c(va,'pessoa_desarmada')} / {_c(va,'pessoa_objeto')} / {va['total']} | "
                 f"{tr['ladrilhos_vazios']} / {va['ladrilhos_vazios']} |")
    L.append("")
    L.append("## 4. Regimes de luz, elevação do sol e tempo de render\n")
    L.append("| Nome interno | Quadros por regime | Elevação do sol realizada (graus) | Render mediano por quadro (s) | Render total (h) |")
    L.append("|---|---|---|---|---|")
    for c in s["corpora"]:
        m = c.get("manifest", {})
        e = m.get("elev_sol_graus") or {}
        reg = ", ".join(f"{k} {v}" for k, v in (m.get("regimes") or {}).items())
        L.append(f"| `{c['nome_interno']}` | {reg} | {e.get('min')} a {e.get('max')} | {m.get('render_s_mediana')} | {m.get('render_h_total')} |")
    L.append("")
    L.append("## 5. VisDrone: imagens e instâncias de pessoa (pedestrian + people fundidas na classe única `pessoa`)\n")
    L.append("| Conjunto | Nome no artigo | Imagens | Instâncias de pessoa | Imagens sem caixa |")
    L.append("|---|---|---|---|---|")
    for v in s["visdrone"]:
        L.append(f"| `{v['nome_interno']}` | {v['nome_artigo']} | {v['imagens']} | {v['instancias_pessoa']} | {v['imagens_sem_caixa']} |")
    o = s["visdrone_val_formato_original"]
    L.append("")
    L.append(f"Conferência no formato original do VisDrone-DET val (`VisDrone2019-DET-val/annotations`): {o['imagens']} imagens, {o['pedestrian']} pedestrian + {o['people']} people = {o['pessoa_total']} instâncias de pessoa; {o['regioes_ignoradas_cat0']} regiões ignoradas (categoria 0) em {o['imagens_com_regiao_ignorada']} imagens, mais {o['linhas_score0_outras_categorias']} linhas de outras categorias com score 0, também descartadas. Regra do conversor: {o['regra']}.")
    if "fatias_json" in s:
        f = s["fatias_json"]
        L.append(f"\nFatias (`visdrone/ft/fatias.json`, `prepara_ft.py`): sel {f['sel']}, ft05 {f['ft05']}, ft10 {f['ft10']} de {f['treino_total']} imagens de treino; semente {f['semente']}; ft05 contido em ft10: {f['ft05_contido_em_ft10']}; sel disjunta de ft10: {f['sel_disjunto']}. A fatia `sel` é a validação (seleção de checkpoint) dos modelos de ajuste fino e dos conjuntos; o teste é o val inteiro.")
    L.append("")
    L.append("## 6. Notas de leitura\n")
    L.append("- Nomes do artigo contra nomes internos: Pilot corpus = `ds_morro_clima` (treino `morro_clima_s`); S-nadir-150 = `ds_morro_4k` (`s_nadir_4k`); S-nadir-150-six = `ds_variedade` (`s_variedade`); S-oblique = `ds_morro_obl` (`s_obliquo`); S-oblique-six = `ds_oblvar` (`s_oblvar`, `_sd1`, `_sd2`); S-nadir-75 = `ds_armado_75` (`armado_75`); S-nadir-35 = `ds_armado_35` (`armado_35`, `_sd1`, `_sd2`); gêmeo a 75 m = `ds_armado_75g` (`armado_75g`, `_sd1`, `_sd2`); gêmeo a 150 m = `ds_armado_150g` (`armado_150g`); quadros novos = `ds_armado_35_extra` e `ds_armado_75g_extra`; arma inédita = `ds_armado_75_inedita`; porte de arma = `ds_armado_75_porte`; teste por regime = `ds_regime_4k`; R = `visdrone_sub/train` (`r_pareado`); F = `ft/ft05`, `ft/ft10` com seleção em `ft/sel`; F-joint = `ds_misto05`, `ds_misto10` (890 ladrilhos de `ds_oblvar_tiles/train` mais a fatia real).")
    L.append("- A GSD da tabela 1 é a realizada (altitude média do manifest); a nominal na altitude de comando está em `gsd_zoom.md` (150 m: 9,76 em 1080p e 4,88 em 4K; 75 m: 2,44; 35 m: 1,14).")
    L.append("- `pitch` não foi gravado no manifest dos dois corpora mais antigos (`ds_morro_clima`, `ds_morro_4k`); a faixa de comando era o padrão `--pitch 0 3.5` (graus a partir do nadir), a mesma realizada nos corpora posteriores de nadir (0,0 a 3,5).")
    L.append("- Amostras do Cycles por quadro (não ficam no manifest; lidas dos comandos em `03-blender/scripts/fila_noite.py`, `rodada3.py` e `rodada4.py`): 96 em `ds_morro_4k`, `ds_variedade`, `ds_morro_obl`, `ds_oblvar`, `ds_armado_75`, `ds_armado_75_inedita`, `ds_armado_75_porte` e `ds_regime_4k`; 64 em `ds_armado_35`, `ds_armado_75g`, `ds_armado_150g` e nos dois `_extra`. Para `ds_morro_clima` o comando não ficou registrado: não apurado.")
    L.append("- Pessoas colocadas contra caixas retidas: a diferença soma três causas que o manifest não separa (visibilidade abaixo de 0,35 em 14 raios, caixa fora do quadro, lado abaixo de 0,2 por cento do quadro). Nos corpora oblíquos a fração retida cai a 0,34 a 0,41 porque a câmera inclinada enquadra uma faixa menor do terreno sorteado.")
    L.append("- As divisões train/val são por quadro (sorteio com probabilidade `--val 0.15` por quadro); os ladrilhos herdam a divisão do quadro. `ds_armado_75_inedita` e `ds_armado_75_porte` têm 47 quadros em train e 3 em val só por herança do sorteio: nenhum dos dois foi usado em treino; os testes usaram `--split todos` (50 quadros).")
    L.append("- As instâncias dos ladrilhos (tabela 3) não somam às dos quadros (tabela 2): a sobreposição de 20 por cento duplica caixas na emenda e caixas com menos de 40 por cento da área dentro do ladrilho são descartadas.")
    L.append("- VisDrone: os rótulos YOLO em disco (`visdrone_yolo`, conversor `02-projeto-ufrj-2022/arma3-2022/scripts/visdrone_to_yolo.py`) fundem pedestrian (8.844 no val) e people (5.125) na classe única `pessoa` e descartam linhas com score 0; as 1.378 regiões ignoradas (categoria 0, 340 imagens) não viram caixa, e é por isso que o validador padrão conta detecção dentro delas como falso positivo (ver `avalia_visdrone_oficial.py`).")
    with open(os.path.join(AQUI, "corpora.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
