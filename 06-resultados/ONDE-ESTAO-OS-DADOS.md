# Onde estão os dados (desktop)

Levantado em 2026-09-17 e 18 [DESKTOP]. Nada desta lista está no git. Tudo mora em `C:\arma3-favela\` (44 GB), que fica intacta como arquivo morto. A coluna PCERJ marca o que deriva das fotos operacionais da PCERJ e por isso não sai do desktop por nenhum canal.

## Pesos

SHA256 calculado com `Get-FileHash -Algorithm SHA256`. Caminho base: `C:\arma3-favela\blender\`.

| Arquivo | MB | Data | PCERJ | SHA256 |
|---|---|---|---|---|
| `runs\detect\blender_v3\weights\best.pt` | 5,3 | 2026-09-12 02:04 | não | 42434FA00C61F0CDA7790C100296EAD5457A6D511CB040E8D5E9F348C8AD2F67 |
| `runs\detect\blender_v3\weights\last.pt` | 5,3 | 2026-09-12 02:04 | não | 0D12423532DD4822ECF5D820BD4037EA816F6E30A8522397D2C9678F523C08FB |
| `runs\detect\blender_v3_tiles\weights\best.pt` | 72,6 | 2026-09-12 03:05 | não | 502D3F7F4397F99A52A0971A34E7A5DD598E3D40D9007B9A1ADA9701B350AAE2 |
| `runs\detect\blender_v3_tiles\weights\last.pt` | 72,6 | 2026-09-12 03:24 | não | ECEB81A5968BBD7323D7E5BBFEC5B0E5709E2209BC552E7739312BE38682B793 |
| `runs\detect\blender_v3_tiles2\weights\best.pt` | 18,4 | 2026-09-12 04:44 | não | F8D00AFBE3DCF4E0C280247410D652496782C8EBC80622C8B4A7716F93EE8579 |
| `runs\detect\blender_v3_tiles2\weights\last.pt` | 18,4 | 2026-09-12 04:44 | não | 2D0EB454983712243E401DEF4CA85DC4C1CF45B3CE3781CF1C8013A9275F6F4E |
| `runs\detect\blender_odm_tiles\weights\best.pt` | 18,4 | 2026-09-12 07:02 | treinado em dado PCERJ | 6DDF75294A40D48E85393E76DBB1ACA94D3210F44C2758B8D3C9AAF984CA887F |
| `runs\detect\blender_odm_tiles\weights\last.pt` | 18,4 | 2026-09-12 07:02 | treinado em dado PCERJ | 51F27FF64A1EEFA14AA63B91E0BED48AD6C2C3DEF177386F9D9B00006E641B82 |
| `runs\detect\cid150_s\weights\best.pt` | 18,4 | 2026-09-13 05:23 | treinado em dado PCERJ | CEA30547EEB62589D1537F4E1B83C3FAA0A573AA9F965344E99DA88BDE9CDFD2 |
| `runs\detect\cid150_s\weights\last.pt` | 18,4 | 2026-09-13 05:23 | treinado em dado PCERJ | 33135A28E0EAC5EDD476404B3BF220CAC2FB5BE31FC86A7B859335747F203D94 |
| `yolo11n.pt` (COCO, Ultralytics) | 5,4 | 2026-09-12 01:31 | não | 0EBBC80D4A7680D14987A577CD21342B65ECFD94632BD9A8DA63AE6417644EE1 |
| `yolo11s.pt` (COCO, Ultralytics) | 18,4 | 2026-09-12 02:07 | não | 85A76FE86DD8AFE384648546B56A7A78580C7CB7B404FC595F97969322D502D5 |
| `weights\yolo26n.pt` (baixado, não usado em nenhum run) | 5,3 | 2026-09-12 01:31 | não | 9B09CC8BF347F0FC8A5F7657480587F25DB09B34BF33B0652110FB03A8AD4FEF |

Os `best.pt` do `blender_v3_tiles` têm 72,6 MB, o quádruplo dos outros yolo11s. Explicação provável (não verificada abrindo o arquivo): o treino foi interrompido antes de o Ultralytics remover o estado do otimizador, o que ele só faz ao fim do treino.

## Datasets

Caminho base: `C:\arma3-favela\blender\`. Estrutura YOLO (`images/{train,val}`, `labels/{train,val}`, `data.yaml`, `manifest.jsonl`). Os `data.yaml` têm o caminho absoluto antigo no campo `path`.

| Pasta | MB | Imagens train / val | Rótulos .txt | Caixas | Data | PCERJ |
|---|---|---|---|---|---|---|
| `dataset_v3` | 224 | 103 / 17 | 120 | 671 | 2026-09-11 e 12 | não |
| `dataset_v3_tiles` | 251 | 520 / 80 | 600 | 1.173 | 2026-09-12 | não |
| `dataset_odm` | 172 | 105 / 15 | 120 | 857 | 2026-09-12 | sim |
| `dataset_odm_tiles` | 217 | 595 / 87 | 682 | 1.551 | 2026-09-12 | sim |
| `dataset_cid150` (inclui `images_png` sem pós-processamento) | 7.621 | 473 / 87 | 560 | 5.745 | 2026-09-12 | sim |
| `dataset_cid150_tiles` | 1.169 | 2.377 / 437 | 2.814 | 10.239 | 2026-09-12 | sim |
| `teste_angulos` | 828 | 0 / 60 | 60 | 596 | 2026-09-12 | sim |
| `teste_denso` | 543 | 0 / 40 | 40 | 1.749 | 2026-09-12 | sim |

Pastas de ensaio (renders avulsos de calibração, sem valor de dataset): `amostra-4k`, `test_cid`, `test_now`, `test_odm`, `test_odm2`, `test_paint`, `test_pm`, `test_v3`, `test_v3b`, `test_v3c`, `test_z30`. Somam cerca de 2,4 GB.

## Runs completos

`C:\arma3-favela\blender\runs\detect\` (308 MB em 18/09): `blender_v3`, `blender_v3_tiles`, `blender_v3_tiles2`, `blender_odm_tiles`, `cid150_s`, cada um com a pasta irmã `<run>_val`. Os runs de 20 a 30/09 estão na seção seguinte. O que é leve e não sensível está copiado em `06-resultados/<run>/`. Ficaram só no desktop: pesos, e os mosaicos `train_batch*.jpg` e `val_batch*.jpg` dos runs `blender_odm_tiles` e `cid150_s` (mostram textura PCERJ).

Avaliações: `C:\arma3-favela\blender\aval_angulos\` e `aval_denso\` (`resultado.json` copiado, `previas.jpg` não).

Logs: 35 arquivos `.log` em `C:\arma3-favela\blender\` e 5 em `C:\arma3-favela\odm\`. Não copiados: têm caminhos locais e, em `build_map_final.log`, latitude e longitude do centro do voo.

## Corpora e runs do artigo (20 a 30/09/2026: cadeia inicial e rodadas 2, 3 e 4)

Acrescentado em 2026-10-18 [DESKTOP]. As tabelas abaixo são a saída de `06-resultados/inventario.py`, gerada com o comando `C:/arma3-favela/venv/Scripts/python.exe 06-resultados/inventario.py` (só lê; imprime as tabelas no stdout). Cobrem só os corpora procedurais do `gen_morro.py` (Poly Haven CC0, nenhum dado PCERJ), os dois corpora mistos com o VisDrone e os 26 runs listados em `revisao-2026-10-17/checkpoints.md`. A lista de pastas é fechada no script, e ele aborta se algum nome contiver `odm` ou `cid150`. Caminho base: `C:\arma3-favela\blender\`.

Convenções:

- MB em base binária (2^20 bytes), a mesma do `Get-Item` usado nas tabelas de cima; os pesos yolo11s dão 18,4 MB nas duas.
- Corpus: a imagem não é hasheada, uma a uma. Entram o SHA256 do `manifest.jsonl` do gerador, do `data.yaml` e do arquivo de rótulos. Esse arquivo não existe em disco: é um tar determinístico de todos os `labels/**/*.txt` montado em memória (ordem alfabética do caminho relativo, USTAR, mtime 0, uid e gid 0, modo 0644, sem os `.cache` do Ultralytics). Rodar o script de novo reproduz o hash enquanto nenhum rótulo mudar.
- As pastas `_tiles` não têm manifest: os ladrilhos herdam o do corpus de quadros. O `ds_variedade` também não tem: os quadros e os manifests por sítio estão nas seis pastas `_dose_s*`, cujas caixas somam as 3.228 do `ds_variedade` (cópia, não link físico). Os `ds_misto*` têm `composicao.json` no lugar do manifest; as imagens são links físicos para `ds_oblvar_tiles\images\train` e para `C:\arma3-favela\visdrone\ft\ft05` ou `ft10`, e a validação aponta para a fatia `sel` do VisDrone, fora da pasta.
- Caixas: linhas não vazias dos rótulos. Nos corpora de quadros batem com as "caixas retidas" de `revisao-2026-10-17/corpora.md`.
- Rodada: cadeia inicial de 20 a 22/09, rodada 2 de 22/09 22:28 a 24/09 16:54, rodada 3 até 26/09 17:54, rodada 4 de 27/09 11:31 a 30/09 10:25 (`DIARIO.md`). Os primeiros corpora e runs usados no artigo (piloto, S-nadir-150, R, S-nadir-75) são da cadeia anterior à rodada 2 e também faltavam aqui.
- Runs: a pasta irmã `<run>_val` entra no tamanho quando existe; `misto10`, `armado_35_sd1` e `armado_75g` não a têm. Os mosaicos `train_batch*.jpg` e `val_batch*.jpg` destes runs saem só de cena procedural ou do VisDrone (dedução pelo corpus de treino; não foram abertos).

Total: 16 corpora (14 sintéticos e 2 mistos) em 32 pastas (16 de quadros ou mistos, 10 de ladrilhos, 6 de sítio), mais 26 runs com 52 arquivos de pesos. Somam 33,1 GB aparentes, 32,2 GB em disco descontando links físicos. Os runs respondem por 1,2 GB; o resto é corpus. O total de 44 GB da primeira linha deste arquivo é de 18/09 e não inclui estas pastas.

### Corpora

| Pasta | MB | Arquivos | Imagens train / val | Rótulos .txt | Caixas | Data (arquivos mais antigo e mais novo) | Rodada | Nome no artigo |
|---|---|---|---|---|---|---|---|---|
| `ds_morro_clima` | 172 | 98 | 40 / 8 | 48 | 684 | 2026-09-20 a 2026-09-20 | cadeia 20 a 22/09 | Pilot corpus (1080p) |
| `ds_morro_clima_tiles` | 42,6 | 673 | 274 / 61 | 335 | 1198 | 2026-09-20 a 2026-09-20 | cadeia 20 a 22/09 | Pilot corpus, ladrilhos de 640 px |
| `ds_morro_4k` | 2.433 | 362 | 149 / 31 | 180 | 3225 | 2026-09-20 a 2026-09-20 | cadeia 20 a 22/09 | S-nadir-150 (corpus of record) |
| `ds_morro_4k_tiles` | 577 | 2665 | 1106 / 225 | 1331 | 5677 | 2026-09-20 a 2026-09-20 | cadeia 20 a 22/09 | S-nadir-150, ladrilhos |
| `ds_variedade` | 2.399 | 361 | 156 / 24 | 180 | 3228 | 2026-09-22 a 2026-09-23 | rodada 2 | S-nadir-150-six |
| `ds_variedade_tiles` | 542 | 2621 | 1135 / 174 | 1309 | 5665 | 2026-09-23 a 2026-09-23 | rodada 2 | S-nadir-150-six, ladrilhos |
| `_dose_s-1` | 404 | 62 | 24 / 6 | 30 | 529 | 2026-09-22 a 2026-09-23 | rodada 2 | S-nadir-150-six, sítio -1 (30 quadros; ds_variedade junta os seis) |
| `_dose_s0` | 400 | 62 | 26 / 4 | 30 | 542 | 2026-09-23 a 2026-09-23 | rodada 2 | S-nadir-150-six, sítio 0 |
| `_dose_s1` | 420 | 62 | 25 / 5 | 30 | 434 | 2026-09-23 a 2026-09-23 | rodada 2 | S-nadir-150-six, sítio 1 |
| `_dose_s2` | 359 | 62 | 28 / 2 | 30 | 663 | 2026-09-23 a 2026-09-23 | rodada 2 | S-nadir-150-six, sítio 2 |
| `_dose_s3` | 420 | 62 | 28 / 2 | 30 | 505 | 2026-09-23 a 2026-09-23 | rodada 2 | S-nadir-150-six, sítio 3 |
| `_dose_s4` | 397 | 62 | 25 / 5 | 30 | 555 | 2026-09-23 a 2026-09-23 | rodada 2 | S-nadir-150-six, sítio 4 |
| `ds_morro_obl` | 2.477 | 362 | 155 / 25 | 180 | 1912 | 2026-09-24 a 2026-09-24 | rodada 2 | S-oblique |
| `ds_morro_obl_tiles` | 500 | 2211 | 968 / 136 | 1104 | 3264 | 2026-09-24 a 2026-09-24 | rodada 2 | S-oblique, ladrilhos |
| `ds_oblvar` | 2.572 | 362 | 152 / 28 | 180 | 1521 | 2026-09-24 a 2026-09-25 | rodada 3 | S-oblique-six |
| `ds_oblvar_tiles` | 492 | 2071 | 890 / 144 | 1034 | 2746 | 2026-09-25 a 2026-09-25 | rodada 3 | S-oblique-six, ladrilhos |
| `ds_armado_75` | 2.485 | 403 | 173 / 27 | 200 | 2887 | 2026-09-21 a 2026-09-24 | cadeia 20 a 22/09 | S-nadir-75 (three classes) |
| `ds_armado_75_tiles` | 535 | 3039 | 1316 / 202 | 1518 | 4629 | 2026-09-22 a 2026-09-22 | cadeia 20 a 22/09 | S-nadir-75, ladrilhos |
| `ds_armado_35` | 2.259 | 403 | 165 / 35 | 200 | 2223 | 2026-09-23 a 2026-09-24 | rodada 2 | S-nadir-35 |
| `ds_armado_35_tiles` | 398 | 2819 | 1166 / 242 | 1408 | 3571 | 2026-09-24 a 2026-09-24 | rodada 2 | S-nadir-35, ladrilhos |
| `ds_armado_75g` | 2.456 | 403 | 176 / 24 | 200 | 2257 | 2026-09-25 a 2026-09-26 | rodada 3 | Twin of S-nadir-35 at 75 m |
| `ds_armado_75g_tiles` | 501 | 2929 | 1287 / 176 | 1463 | 3627 | 2026-09-26 a 2026-09-26 | rodada 3 | Twin at 75 m, ladrilhos |
| `ds_armado_150g` | 2.677 | 403 | 173 / 27 | 200 | 2248 | 2026-09-27 a 2026-09-28 | rodada 4 | Twin of S-nadir-35 at 150 m |
| `ds_armado_150g_tiles` | 596 | 2793 | 1215 / 180 | 1395 | 3789 | 2026-09-28 a 2026-09-28 | rodada 4 | Twin at 150 m, ladrilhos |
| `ds_armado_35_extra` | 907 | 163 | 0 / 80 | 80 | 953 | 2026-09-28 a 2026-09-28 | rodada 4 | New frames, 35 m (80, teste) |
| `ds_armado_75g_extra` | 986 | 163 | 0 / 80 | 80 | 837 | 2026-09-28 a 2026-09-28 | rodada 4 | New frames, twin at 75 m (80, teste) |
| `ds_armado_75_inedita` | 611 | 102 | 47 / 3 | 50 | 708 | 2026-09-25 a 2026-09-25 | rodada 3 | Unseen-weapon test frames (50) |
| `ds_armado_75_porte` | 611 | 102 | 47 / 3 | 50 | 709 | 2026-09-27 a 2026-09-27 | rodada 4 | Carried-as-weapon re-render (50) |
| `ds_regime_4k` | 1.617 | 242 | 0 / 120 | 120 | 2204 | 2026-09-28 a 2026-09-29 | rodada 4 | Per-regime test frames (120) |
| `ds_regime_4k_tiles` | 380 | 1784 | 0 / 885 | 885 | 3849 | 2026-09-29 a 2026-09-29 | rodada 4 | Per-regime test, ladrilhos |
| `ds_misto05` | 501; 425 MB já contados em outra pasta (link físico) | 2431 | 1214 / 0 (val = fatia `sel` do VisDrone) | 1214 | 8288 | 2026-09-20 a 2026-09-27 | rodada 4 | F-joint 5% (890 ladrilhos de ds_oblvar_tiles + 324 VisDrone, link fisico) |
| `ds_misto10` | 574; 501 MB já contados em outra pasta (link físico) | 3077 | 1537 / 0 (val = fatia `sel` do VisDrone) | 1537 | 13496 | 2026-09-20 a 2026-09-27 | rodada 4 | F-joint 10% (890 ladrilhos de ds_oblvar_tiles + 647 VisDrone, link fisico) |

### SHA256 dos corpora

| Pasta | `manifest.jsonl` | `data.yaml` | Arquivo de rótulos (tar determinístico de `labels/**/*.txt`) |
|---|---|---|---|
| `ds_morro_clima` | B94100394B66416E27FBAF48C85945B602BFD21CAFEA65D356ED712971EF1653 | B28F9B4C605E85E8C71C74881C8551FF2AD520473424AC0D392A69DF2DCF542B | 010B1DA585D86AD1A5978933EFF684E9FE0D5821B57BF88770F5FDDC7471CEEB |
| `ds_morro_clima_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | CAD83F8A2720910D0731D14DFD08683FC56DE045B79CAA9F81F87F6484338B63 | 6C7D4A719A1DE5988E6C29BAF7E58843E7ED17F91757AE86C4C088ECA37596AD |
| `ds_morro_4k` | CD2E196D8475D5F8DAA4E7C8783504F66D8054A0FEA281EF2452DA4C7D62F5BA | F7513E4DBB81BA1A734E7853C1E2C44C1FC2240F9236E517A25B2431988281AB | 341EE4492E74422DE2F0400B2CA99345666F2236905D8C406F74183A1B4AE998 |
| `ds_morro_4k_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 9D66D5065CEF15B8AE4CB0724309443836527B730D22F675874299D8F7F9B948 | 3E464AFE0EA0CE9F16CCF34DCB4AAF997166D3B8C6FE9553C0F8C5C05E25DE5E |
| `ds_variedade` | não existe (manifests por sítio nas pastas `_dose_s*`) | 62A895C9133924124AF5A58CE440BF3EBE8D82C7C2C53D962BC92845EC139573 | 8F458E18BFE654122FDEB002C2745EDB05AE6BA44F9C8D3E225E7408FC05F31D |
| `ds_variedade_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 18C0169B2E96E660F4244E855058BFE53E82B97933808799D2431456932B59C0 | 89728167DBA73956DA03FF674FDCB5D0870CA5FAC37575D41478EDA86265874F |
| `_dose_s-1` | 249564BE9BFCC6659764707FFAAF561C1F6DA7083C553C23BDBFAC4D3C082BED | 01841E8829032C7F961D63A49E6E45BD98252A00C9FA908FDCB3250002623091 | 6D3BB1BF6DA3CE76C835805D7515E3C6C813E1F048E1AC4D1BBA204BA3362419 |
| `_dose_s0` | CFE9FB316E299541965294BCAEC3AC183ABBAC342C8D46A7F1FF4AD1BBE1199E | F2F7B7644905C4CB7CE540BD2EEAA66107A583890C838AA91AA6F636FF8D71C1 | 671BF12E67E89636E73DD47073EB744B5E80EAACB2882B9C06B5455055D4A345 |
| `_dose_s1` | AA8AA905C3FA6F8DFACF50880CCF595B19EC7750FCF7F1C6B5B77FADFAD51F22 | BC7702D39C44E8FC9462D4BFE54B34C9DB2C9006B190E54322FDE19C30C37454 | FA8CC974A6089DBEEB62528B5EF469E1383E6F0AF24DBD16E8368876DF3F235C |
| `_dose_s2` | 20B3B24B162F09F201EE6661DEA42D83B6B209E02DBEFBDABF996AB3C94F645E | E00BBAAF9BF8A7ED9B0A996B8AC28FD08842B9A43BEAB173599525715F77961F | 394CDAC6E2814F5DCC1BB7035603D5EA496BBEFAC56736BDA187B7BAD39DC2D4 |
| `_dose_s3` | 4061FF620F2F7EC5C1265ABA9ECF92A564AD5F9C9FC2674235873E21A5F14ED0 | CAD092313457961ADE09FDE9E4C21EAF19A22C3385797AE3E0D33DFDD552164E | 693BBB185CF1758F24FC28B84F0DBDD71583B29D10F128E5212BF9841B0ED2EC |
| `_dose_s4` | 57DF46C1CDB039EB2D3C387D74B7DFB188259F20BC71D5CF7BA555DBEB64D573 | 8142F85B61BE433EACC3883CD56E5E1E4377C3524BAE24B4A244E2AA6C001116 | F2BEACA836B4CFB3CAA85D756A40267AF3DA4A5CEEC31BAAE2DB4A67507E48D7 |
| `ds_morro_obl` | A44B72F49F1FEF35FE80F0632AB204469CE9D3EF47BEDC5A283EFB54DB73D3E2 | B597C7B11D084050113868289558E7CB7F321138D673E56A9452C1C4951B3FC4 | 76C5555B3051ADEF815FCE95A4EC280A14E3B68EB156123F6D1E26B8CCA360A2 |
| `ds_morro_obl_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 40BE2A87570FE151262B5947AC42E3FAB8C4970CB4EDF2A7BB3ED6314C00A62C | C6881892BDF896D46CFE7A001B29E7F1C242A525AA43A6AD113D231DC2D4B982 |
| `ds_oblvar` | F44B3133D0A35C4A7CC6EF649A9DC4A70198F4BF91B4E5C8194D9DF74271B4E7 | D20045003473B0534A08130EF33613D02A8253E95F9F8DF956BBA2780763D510 | 7BABD1C492D1B2818BA1A3A76CDE1CBE43EDBDA22F5F1F809AE296BBA1B387BB |
| `ds_oblvar_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 48AAE1CD4EB9F49090F19E7F3ED5C7A5F189107964278F629748442CF735E328 | 69B41EAD5967B395F69899420FA9549E533928B297608A0E8DEFACC1A11C30E8 |
| `ds_armado_75` | F18E766363C75D3CB6801788851BDBF2D32E89B507F2EC7D9ED6A428AACC6705 | CC8A85760B97D8412F9D1C759E493E6887A87E478E13B86EEB462CEC196CD1F4 | B51C00C417AD996AE8185C40170E595B17B8871316F8B7BA9934FD585431EBB3 |
| `ds_armado_75_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 1E59AA09BD9F22B5EBDBBEF426CD690EE98A62CB7EF67F5AB70C18CC1ED1F3AD | 5739E4817EBAD36FD2558F4C5613EE837812E67570628AE7EA3B1681DE64B905 |
| `ds_armado_35` | DE9202D437F8EAF0B96BFCC4E9765E552B5280570DBE29CD102A32E8352F0919 | 1938942F2258210DA4A991856DB59284081A5220E34E883EFCAE06501F403B85 | E891D3DBBD6370D776BA7821CD78272924B39C50098247DA6F99B5ACE139A270 |
| `ds_armado_35_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | C6822DD392EA9D28413737B358D384C8FDD74E53A50D0C76D1EDD8E9BF674AB9 | 151E211BC5671E7830E7684699916BD02F5D7CB33BBB56A5FDB45395AC80676E |
| `ds_armado_75g` | 6112065F162E491100905270D175769682E6D152035A1E599DD18F893C5BB9B4 | 39A6DC26ED4E07C767C48B71CBCF83E79B1DA3EBB556768A1DF998F792949B0F | F29EBC603C537B360257175B680C62956FB6397E551398CC7FA934D0F89E04A5 |
| `ds_armado_75g_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 55D94ADFDDF5C0131C4D87DC9508A3CA5EDD8A8031EED8907480F3419CFAF9B1 | 3ADF5ECB343C01C74EDF0881B6518F9EC1885481CD716ADB88E30834A7D7D845 |
| `ds_armado_150g` | 87D4D00EE912A78ADFE5B82B6629AA4A322A068E19035A2943A53557D56B689B | B3CADFA2A1A2AB5753F9DD4A9C0A89790379CAB56BB139A66A42E6207ECAD933 | FEA670EE545530ECA279A6EC68E2CC90132AF49E49DD6E46D906BC98DE8B6DB1 |
| `ds_armado_150g_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 892F698069997A35871848424E953EB69D3B891195EA01B49C2DD9590BF5B04F | E0398BFBB5D2C53155838BE859288F77E5B7C928E1AE9161D617C3EACF350A9F |
| `ds_armado_35_extra` | 4088A9EE4D268456FF337F31671A503E7505EB029640EDEA349FC325EA12DE00 | 2329C7A256E77D180556AC8C725B1862B5D66CB2D082A6D4B0536EAE8AE3668F | 32F2FBA1E0823CF711A3C98A5A3BF6835973B5CCBF223125A6A29A5663BCEFD7 |
| `ds_armado_75g_extra` | 0F6DCD73141E4EF782CC9092487D2A247ED80430608E79488B9E0BF0576010B6 | 7566D23E1BC8E85F8A5B287A90C6ECD21A43D51DBC4DEC709C84ECDFD131BF97 | ED95FE481D776355BFC53973F16C3AE96EAB67D5DFBAF2A9E702BE24A2E886A9 |
| `ds_armado_75_inedita` | 927762C6AACC36319459DD7BF1B8EA62CC5595E2FDF9D43874F122738051B263 | 5906A4C164D160A8C714250A4BF6542C878C937F042C891BB6C79389C6CC39E9 | 5187FF9B4B629D7D9760043736BE29043F5A83184059E2754A3F06353BA9DB64 |
| `ds_armado_75_porte` | 264AD6DE1BBC3BB8A122DCF6C82F273FB2CDE2D47B06AED3A8B69F4B15BF75DA | 51ED9A9615AD62BA2A7203B459837304634C39B29380D4110D332746A42870F7 | B0B3AF5F2CC7D627B42FA9CD9A94B3B44A1D229522FBAD742F540D43BC2F9D2C |
| `ds_regime_4k` | 746300EDF6EA834C6A6A33D9AF96B5B0AAC77807B25A23E7D7AE7413D2BDB75C | E325F09CB9D218EA85783A386CD8DC74CC20F37C1A5EDC3728F25B6C89BF6022 | 99206A0EA5231223DB78102F431AAE5ECC0B515C92B3DCD7CB51496E865BB2B5 |
| `ds_regime_4k_tiles` | não existe (ladrilhos herdam o manifest do corpus de quadros) | 8C34F03D0DC1D125E38DCC207A3026F0A77BC3C51853EA071C0D7F1505BD4A0B | E5E9F65E84FB65AE01900BC19D91AC9DFDDC4FF133A400137C6CCAA17A3A8FCA |
| `ds_misto05` | não existe; `composicao.json` BE5FC5EB2072B6686D860B6C3CE42AFA65BA9F888BB58821E316847F1D9A92CB | 527D84D53E26ED5C91F0D4880F46A4EC10518304B788F990460DE0255C6DDE4F | 6D61B643CCE89A03FA920B70B8EBF5BCE63F1B53717393B228DC22A55B03045C |
| `ds_misto10` | não existe; `composicao.json` 26F4019E786ADC6E6CE768A89C6A9FE9594A7EF25DAF187FC01070A58F4D1234 | CDADD841CB411A57137FBA6CBED3F8D80FD20F836D06091D30D4831E11676AEA | FE044821D87206034B2E6BEB8D42C062F279D5933D4329DEFF472342D6BF80F2 |

### Pesos

| Arquivo | MB | Data | Rodada | Modelo no artigo | Corpus de treino | SHA256 |
|---|---|---|---|---|---|---|
| `runs\detect\morro_clima_s\weights\best.pt` | 18,3 | 2026-09-20 10:53 | cadeia 20 a 22/09 | Pilot model | ds_morro_clima_tiles | EC733067F9EEE093319BC7877A9177788E2206B0A4CCB5EEFD9238E952B13AD3 |
| `runs\detect\morro_clima_s\weights\last.pt` | 18,3 | 2026-09-20 10:53 | cadeia 20 a 22/09 | Pilot model | ds_morro_clima_tiles | 4C4417BDCED2111157A9E5EC667A36C54CE0A40F079C7E09BDBA1390022BC550 |
| `runs\detect\r_pareado\weights\best.pt` | 18,4 | 2026-09-21 08:55 | cadeia 20 a 22/09 | R | VisDrone, 1.106 imagens (visdrone_sub) | 8ED319E994B0E4B032F3CD4FA32F02C3E34F41B4853418B5A66EB377DC199665 |
| `runs\detect\r_pareado\weights\last.pt` | 18,4 | 2026-09-21 08:55 | cadeia 20 a 22/09 | R | VisDrone, 1.106 imagens (visdrone_sub) | AE901183850BC5F3043E136AC3C7125CD10AB88739E0EB36B2E0E5BEB190BE76 |
| `runs\detect\s_nadir_4k\weights\best.pt` | 18,4 | 2026-09-21 02:59 | cadeia 20 a 22/09 | S-nadir-150 | ds_morro_4k_tiles | 7C1CE94C66D816AC4A7D3DE1066CBAB851FF980B722230A3E3783425536EBA26 |
| `runs\detect\s_nadir_4k\weights\last.pt` | 18,4 | 2026-09-21 02:59 | cadeia 20 a 22/09 | S-nadir-150 | ds_morro_4k_tiles | AF546E255C4BC322A3107B53501F3CD2363836E6C7D4AAF404B264F4E463A469 |
| `runs\detect\s_variedade\weights\best.pt` | 18,4 | 2026-09-23 11:36 | rodada 2 | S-nadir-150-six | ds_variedade_tiles | A88231EAFE0E2097361E769B68B289D1351EFBAEFB39822D7E19DA41A276A313 |
| `runs\detect\s_variedade\weights\last.pt` | 18,4 | 2026-09-23 11:36 | rodada 2 | S-nadir-150-six | ds_variedade_tiles | 298546C22C4EE2EA3FF1C5D123FFFEB3F5316EE18817CDCEFDAEE562E2373444 |
| `runs\detect\s_obliquo\weights\best.pt` | 18,4 | 2026-09-24 16:53 | rodada 2 | S-oblique | ds_morro_obl_tiles | A0B60CF99BAB14451B1FB078E7042A7C8A603D1E06EDA3AC0C4F87C11105FB9F |
| `runs\detect\s_obliquo\weights\last.pt` | 18,4 | 2026-09-24 16:53 | rodada 2 | S-oblique | ds_morro_obl_tiles | 06FB7C09769951F77B8AA9C6817DE94C7727F00F31F9CF35E761C0554C831194 |
| `runs\detect\s_oblvar\weights\best.pt` | 18,4 | 2026-09-25 18:02 | rodada 3 | S-oblique-six (seed 0) | ds_oblvar_tiles | BB2BFF5524ED9E709CAFFFEA6C2676C8F978800C436B88C4C64A6C2E70A476A1 |
| `runs\detect\s_oblvar\weights\last.pt` | 18,4 | 2026-09-25 18:02 | rodada 3 | S-oblique-six (seed 0) | ds_oblvar_tiles | BA34651CC5284467AA6C7B056E5DAD43F110AD77C7658CF3611673A835E49EF9 |
| `runs\detect\s_oblvar_sd1\weights\best.pt` | 18,4 | 2026-09-29 03:48 | rodada 4 | S-oblique-six (seed 1) | ds_oblvar_tiles | DE116566C87E416EDD6D7B6BC72C0321104A4206CDADFC7999537F76D5F51290 |
| `runs\detect\s_oblvar_sd1\weights\last.pt` | 18,4 | 2026-09-29 03:48 | rodada 4 | S-oblique-six (seed 1) | ds_oblvar_tiles | CC4069E3A271BCF69D4FC12CAAF1B6B4A6C3705779011088BADA395B4E145FD4 |
| `runs\detect\s_oblvar_sd2\weights\best.pt` | 18,4 | 2026-09-29 06:28 | rodada 4 | S-oblique-six (seed 2) | ds_oblvar_tiles | 6E1D106CFA528D31C29E5813FB516C5AD10F44CBDF786FB7A168A36A03D07C61 |
| `runs\detect\s_oblvar_sd2\weights\last.pt` | 18,4 | 2026-09-29 06:28 | rodada 4 | S-oblique-six (seed 2) | ds_oblvar_tiles | 20F8001DE550B2B142299F8410135C9BB3441D73A41F6421F0F448ABF5AC7DBE |
| `runs\detect\ft05_sint\weights\best.pt` | 18,4 | 2026-09-26 13:54 | rodada 3 | F-synthetic 5% (seed 0) | fatia ft05 do VisDrone, a partir de s_oblvar | 8D0B60AA37FC2FC8F59FE93F05056B6829C6E4DA9D32FC26412EF23D3F2725DB |
| `runs\detect\ft05_sint\weights\last.pt` | 18,4 | 2026-09-26 13:54 | rodada 3 | F-synthetic 5% (seed 0) | fatia ft05 do VisDrone, a partir de s_oblvar | 141CFFAB47A5DE30EB576D650DC985EF97E81E9F3AF4D7A67CAC5A12D24DE4BF |
| `runs\detect\ft05_sint_sd1\weights\best.pt` | 18,4 | 2026-09-29 07:20 | rodada 4 | F-synthetic 5% (seed 1) | fatia ft05, a partir de s_oblvar_sd1 | ADA026352BA00C1543B36F52EE5FD1C588DE34659E09DCD89A1651B0903A31A7 |
| `runs\detect\ft05_sint_sd1\weights\last.pt` | 18,4 | 2026-09-29 07:20 | rodada 4 | F-synthetic 5% (seed 1) | fatia ft05, a partir de s_oblvar_sd1 | 407CCF62579E58A6066E3C074F8ECCFF3EB7E8C49BBAFE5DE3B25DF6DD0EC804 |
| `runs\detect\ft05_sint_sd2\weights\best.pt` | 18,4 | 2026-09-29 08:12 | rodada 4 | F-synthetic 5% (seed 2) | fatia ft05, a partir de s_oblvar_sd2 | 1016C8BF7BDBB49D2D7AE677475E11B2E1EC8C2C53F06CD0A503164755DCD92F |
| `runs\detect\ft05_sint_sd2\weights\last.pt` | 18,4 | 2026-09-29 08:12 | rodada 4 | F-synthetic 5% (seed 2) | fatia ft05, a partir de s_oblvar_sd2 | 9ED12674E6EE0975CF85FB94EF282D77B7DA91B544F92BD94AD0D5735994FF13 |
| `runs\detect\ft05_coco\weights\best.pt` | 18,4 | 2026-09-26 14:44 | rodada 3 | F-generic 5% (seed 0) | fatia ft05, a partir do COCO | 63106BE96532C5D78BDBE0BC602A75A0B9A2219B9364A491CDA504FD639459FB |
| `runs\detect\ft05_coco\weights\last.pt` | 18,4 | 2026-09-26 14:44 | rodada 3 | F-generic 5% (seed 0) | fatia ft05, a partir do COCO | 52DD4E4D2D139FA3118A44FD7B3BFB1A230C40AC992BA19D6B971CFF84CF1CFE |
| `runs\detect\ft05_coco_sd1\weights\best.pt` | 18,4 | 2026-09-29 09:03 | rodada 4 | F-generic 5% (seed 1) | fatia ft05, a partir do COCO | 340800B7B9FBE80E1B62D6D9CA62C65A5796CBDC8385838BF7C23396898957C2 |
| `runs\detect\ft05_coco_sd1\weights\last.pt` | 18,4 | 2026-09-29 09:03 | rodada 4 | F-generic 5% (seed 1) | fatia ft05, a partir do COCO | C16E340548E81AEB7EF87D8B93CD59A0ED5C98FA79CA075B5560D4D921D7220B |
| `runs\detect\ft05_coco_sd2\weights\best.pt` | 18,4 | 2026-09-29 09:56 | rodada 4 | F-generic 5% (seed 2) | fatia ft05, a partir do COCO | C69C2F0F73CB923B672AF0060C5C056FFB2FDD09B7D6C140FEE072ABFB7F8B2F |
| `runs\detect\ft05_coco_sd2\weights\last.pt` | 18,4 | 2026-09-29 09:56 | rodada 4 | F-generic 5% (seed 2) | fatia ft05, a partir do COCO | 28127B726782E6DDBE5D7EE865F64518CCC37CC2CDBCA9D5848CDA2B5E8340D6 |
| `runs\detect\ft10_sint\weights\best.pt` | 18,4 | 2026-09-26 16:17 | rodada 3 | F-synthetic 10% | fatia ft10, a partir de s_oblvar | 41FAAFFAECD732AE8FA9B48EC13186C05B678D0C652195DB34AE26B400B796BE |
| `runs\detect\ft10_sint\weights\last.pt` | 18,4 | 2026-09-26 16:17 | rodada 3 | F-synthetic 10% | fatia ft10, a partir de s_oblvar | 84533908800E5D2D87D1DA0DC3AAB366D1C0818EBE562CD5FBF9CA294AC74C0D |
| `runs\detect\ft10_coco\weights\best.pt` | 18,4 | 2026-09-26 17:51 | rodada 3 | F-generic 10% | fatia ft10, a partir do COCO | 7057E87F9C9E76C1CB073F4D21997D6A90DFBAF58F204D8CE9CD5F285F148DFD |
| `runs\detect\ft10_coco\weights\last.pt` | 18,4 | 2026-09-26 17:51 | rodada 3 | F-generic 10% | fatia ft10, a partir do COCO | 2D079E3D534333700C76180A90DC8033D0DC9A58BDB3DC3047B9BEF8E55A7467 |
| `runs\detect\misto05\weights\best.pt` | 18,4 | 2026-09-27 17:11 | rodada 4 | F-joint 5% | ds_misto05 | 4891C84251E23098544DD98372AFE8B5CBCF755E421E628D3AC7D5C74F56A347 |
| `runs\detect\misto05\weights\last.pt` | 18,4 | 2026-09-27 17:11 | rodada 4 | F-joint 5% | ds_misto05 | 85C4FF0775B02CB352680C864EF4AFDBC9F0574E16C5E7B1E7606F89F860DB9B |
| `runs\detect\misto10\weights\best.pt` | 18,4 | 2026-09-27 23:10 | rodada 4 | F-joint 10% | ds_misto10 | D8C04F8827797621067E2ADF938B38072AD29E09E3634448D530675735D79D2B |
| `runs\detect\misto10\weights\last.pt` | 18,4 | 2026-09-27 23:10 | rodada 4 | F-joint 10% | ds_misto10 | 821DA9149804F4CE8F3D6ED134C1A6DF5FBD719393C78145B7ED564E251395D4 |
| `runs\detect\armado_75\weights\best.pt` | 18,4 | 2026-09-22 10:18 | cadeia 20 a 22/09 | S-nadir-75 (three classes) | ds_armado_75_tiles | 6FE51FD9FAAAA14EAAA550B13E430CABAE5B8657898C8B4A587090CD100A14C6 |
| `runs\detect\armado_75\weights\last.pt` | 18,4 | 2026-09-22 10:18 | cadeia 20 a 22/09 | S-nadir-75 (three classes) | ds_armado_75_tiles | E1EB1423CEFD1675CA5571BDB6C0AF2FFA021FA248272E225632233822DDDC9A |
| `runs\detect\armado_35\weights\best.pt` | 18,4 | 2026-09-24 04:10 | rodada 2 | S-nadir-35 (seed 0) | ds_armado_35_tiles | 745E2791DCC6BF048B181D8EB346B542039E28D8679F146EF7DDDF9766286BA8 |
| `runs\detect\armado_35\weights\last.pt` | 18,4 | 2026-09-24 04:10 | rodada 2 | S-nadir-35 (seed 0) | ds_armado_35_tiles | 160893D15FCCCB2F43960EDB0A476563CDCB35CADD74C6A2E320C2D02E07D8EB |
| `runs\detect\armado_35_sd1\weights\best.pt` | 18,4 | 2026-09-29 21:07 | rodada 4 | S-nadir-35 (seed 1) | ds_armado_35_tiles | D4A6BC4A63BBA6D663C48BB93F595398705E1DF3260FE2B80D1856905A26CD3E |
| `runs\detect\armado_35_sd1\weights\last.pt` | 18,4 | 2026-09-29 21:07 | rodada 4 | S-nadir-35 (seed 1) | ds_armado_35_tiles | 3CE52CC03F667F8645FAF4E7BB98F382A1CFB443074DB76B27CEB9CF8079D621 |
| `runs\detect\armado_35_sd2\weights\best.pt` | 18,4 | 2026-09-30 01:18 | rodada 4 | S-nadir-35 (seed 2) | ds_armado_35_tiles | 7D394E91919EE32B675B9087A87F9A593593AE522797791C1EB93E49C6D72BF2 |
| `runs\detect\armado_35_sd2\weights\last.pt` | 18,4 | 2026-09-30 01:18 | rodada 4 | S-nadir-35 (seed 2) | ds_armado_35_tiles | 29A37079D8913133D3BB00BB2F95EAD285709590E88EB2B17C4AA09F26B71607 |
| `runs\detect\armado_75g\weights\best.pt` | 18,4 | 2026-09-26 13:04 | rodada 3 | Twin at 75 m (seed 0) | ds_armado_75g_tiles | 4E04B7984287B4E7A32D47D67BE65D005ED4E98116B3C83E85DF58651B9D07C2 |
| `runs\detect\armado_75g\weights\last.pt` | 18,4 | 2026-09-26 13:04 | rodada 3 | Twin at 75 m (seed 0) | ds_armado_75g_tiles | 6A8E54E1F58E90491299386DE34B3E39FF9E70BACCC30B9ED36E676827A21051 |
| `runs\detect\armado_75g_sd1\weights\best.pt` | 18,4 | 2026-09-30 05:37 | rodada 4 | Twin at 75 m (seed 1) | ds_armado_75g_tiles | EDE88EC6D193E48BB6A496D8B6866FAD12303BAA74F494800CD2DDBE7F29C1D1 |
| `runs\detect\armado_75g_sd1\weights\last.pt` | 18,4 | 2026-09-30 05:37 | rodada 4 | Twin at 75 m (seed 1) | ds_armado_75g_tiles | 546C8246EDCE26D04D7A50CA933D69A4103292ABAE0CF022AD399A036373A5E5 |
| `runs\detect\armado_75g_sd2\weights\best.pt` | 18,4 | 2026-09-30 10:06 | rodada 4 | Twin at 75 m (seed 2) | ds_armado_75g_tiles | B802CD86C8F9F2BD5CD7D289DB586B138F5FA03E13DA80C0EAC0DEBFD881F9D2 |
| `runs\detect\armado_75g_sd2\weights\last.pt` | 18,4 | 2026-09-30 10:06 | rodada 4 | Twin at 75 m (seed 2) | ds_armado_75g_tiles | 9828B7F222BC6BCEAF2034A25DC765F658BCDEBC796EA5B997DD7850F820717D |
| `runs\detect\armado_150g\weights\best.pt` | 18,4 | 2026-09-28 10:04 | rodada 4 | Twin at 150 m | ds_armado_150g_tiles | 95A9F0D3B76400B4EAC9CB84E4CCBC655B8F098B63BA304BFEF2C69B750FAB3C |
| `runs\detect\armado_150g\weights\last.pt` | 18,4 | 2026-09-28 10:04 | rodada 4 | Twin at 150 m | ds_armado_150g_tiles | 833ED302EAEDB7081217BFD55CCF40D3F3B7A5E966DA27B5B994E31053374D32 |

### Runs

| Run | Pasta `_val` | MB (run mais `_val`) | Arquivos | Rodada | Modelo no artigo |
|---|---|---|---|---|---|
| `morro_clima_s` | sim | 48,5 | 33 | cadeia 20 a 22/09 | Pilot model |
| `r_pareado` | sim | 45,8 | 36 | cadeia 20 a 22/09 | R |
| `s_nadir_4k` | sim | 48,4 | 36 | cadeia 20 a 22/09 | S-nadir-150 |
| `s_variedade` | sim | 49,1 | 36 | rodada 2 | S-nadir-150-six |
| `s_obliquo` | sim | 48,2 | 33 | rodada 2 | S-oblique |
| `s_oblvar` | sim | 47,5 | 34 | rodada 3 | S-oblique-six (seed 0) |
| `s_oblvar_sd1` | sim | 48,6 | 37 | rodada 4 | S-oblique-six (seed 1) |
| `s_oblvar_sd2` | sim | 48,8 | 37 | rodada 4 | S-oblique-six (seed 2) |
| `ft05_sint` | sim | 46,0 | 37 | rodada 3 | F-synthetic 5% (seed 0) |
| `ft05_sint_sd1` | sim | 46,1 | 37 | rodada 4 | F-synthetic 5% (seed 1) |
| `ft05_sint_sd2` | sim | 45,9 | 37 | rodada 4 | F-synthetic 5% (seed 2) |
| `ft05_coco` | sim | 46,0 | 37 | rodada 3 | F-generic 5% (seed 0) |
| `ft05_coco_sd1` | sim | 46,1 | 37 | rodada 4 | F-generic 5% (seed 1) |
| `ft05_coco_sd2` | sim | 45,9 | 37 | rodada 4 | F-generic 5% (seed 2) |
| `ft10_sint` | sim | 46,0 | 37 | rodada 3 | F-synthetic 10% |
| `ft10_coco` | sim | 46,0 | 37 | rodada 3 | F-generic 10% |
| `misto05` | sim | 46,0 | 37 | rodada 4 | F-joint 5% |
| `misto10` | não | 42,5 | 25 | rodada 4 | F-joint 10% |
| `armado_75` | sim | 49,5 | 36 | cadeia 20 a 22/09 | S-nadir-75 (three classes) |
| `armado_35` | sim | 46,9 | 36 | rodada 2 | S-nadir-35 (seed 0) |
| `armado_35_sd1` | não | 42,6 | 25 | rodada 4 | S-nadir-35 (seed 1) |
| `armado_35_sd2` | sim | 46,9 | 37 | rodada 4 | S-nadir-35 (seed 2) |
| `armado_75g` | não | 43,7 | 25 | rodada 3 | Twin at 75 m (seed 0) |
| `armado_75g_sd1` | sim | 49,0 | 37 | rodada 4 | Twin at 75 m (seed 1) |
| `armado_75g_sd2` | sim | 48,9 | 37 | rodada 4 | Twin at 75 m (seed 2) |
| `armado_150g` | sim | 49,2 | 34 | rodada 4 | Twin at 150 m |

### Fora do artigo (só tamanho)

| Pasta | MB | Arquivos |
|---|---|---|
| `ds_morro` | 166 | 82 |
| `ds_morro_teste` | 3,7 | 6 |
| `ds_obj_teste` | 7,6 | 6 |
| `ds_armado_75_descartado` | 1.838 | 297 |
| `ds_morro_obl_descartado_zero_caixas` | 629 | 362 |
| `runs\detect\r_cheio` | 146 | 8 |
| `runs\detect\s_obliquo_descartado_zero_caixas` | 40,1 | 19 |
| `runs\detect\s_obliquo_val_descartado_zero_caixas` | 0,9 | 8 |

## Fotogrametria e cenas 3D (tudo PCERJ, nada sai do desktop)

| Item | Caminho | Tamanho |
|---|---|---|
| Fotos brutas do drone, 217 + 350 (ago/2022, Zenmuse Z30) | `C:\arma3-favela\assets\ortomosaico\{sudoeste,nordeste}\` | 752 MB |
| Zip original baixado do Drive | `C:\Users\marti\Downloads\Ortomosaico-20260912T023827Z-1-001.zip` | 375 MB |
| Projeto ODM Sudoeste (ortomosaico, DSM, nuvem, malha) | `C:\arma3-favela\odm\sudoeste\` | 9,3 GB |
| Projeto ODM Nordeste | `C:\arma3-favela\odm\nordeste\` | 13,8 GB |
| Mapa navegável dos dois setores | `C:\arma3-favela\odm\jacarezinho.blend` (mais `.blend1`) | 314 MB |
| Quadra com paredes verticais e cidade de sólidos | `C:\arma3-favela\odm\quadra.blend` (mais `.blend1`), `odm\quadra\`, `odm\cidade\` | 386 MB |
| Vídeo do voo | `C:\arma3-favela\odm\voo_jacarezinho.mp4` | 8,6 MB |
| Figuras de comparação | `C:\arma3-favela\odm\*.png`, `odm\preview_mapa\`, `odm\mapa_hoje\`, `odm\pessoas\` | cerca de 55 MB |

## Insumos abertos (não sensíveis, fora do git por peso ou licença)

| Item | Caminho | Tamanho |
|---|---|---|
| Poly Haven CC0: 72 texturas PBR 1k, 15 HDRI 2k, 29 modelos glTF | `C:\arma3-favela\assets\polyhaven\` | 735 MB |
| OSM (footprints e vias de Jacarezinho e Rocinha) e SRTM | `C:\arma3-favela\assets\osm\` | 4,3 MB |
| MakeHuman e MPFB (pacotes de instalação) | `C:\arma3-favela\assets\makehuman\`, `assets\mpfb\` | 311 MB |
| Human Base Meshes v1.1.0 (Blender Studio, CC0) | `C:\arma3-favela\assets\human-base-meshes-bundle-v1.1.0\` | 48 MB |
| Instalador do ODM 3.6.2 | `C:\arma3-favela\tools\ODM_Setup_3.6.2.exe` | 239 MB |
| Pacote de contexto de 11/09 descompactado (com os 18 PDFs) | `C:\arma3-favela\projeto_contexto\` | 102 MB |

## ARMA 3

| Item | Caminho |
|---|---|
| Jogo | `C:\Program Files (x86)\Steam\steamapps\common\Arma 3\` |
| Missão em uso | `C:\Users\marti\Documents\Arma 3\missions\dsFavela.Tanoa\` (copiada para `02-projeto-ufrj-2022/arma3-2022/missao/`) |
| Logs `.rpt` | `C:\Users\marti\AppData\Local\Arma 3\`, 6 arquivos de 2026-09-11, nenhum com linha `DSIMG` ou `DSLBL` |
| Screenshots | A pasta `Documents\Arma 3\Screenshots\` não existe: nenhuma captura foi feita |
