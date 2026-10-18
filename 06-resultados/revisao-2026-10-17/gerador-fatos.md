# Fatos do gerador: realismo, diversidade das figuras, biblioteca de objetos, luz (revisão de 2026-10-17, agente D1)

Responde aos pontos M4 (limites do realismo), S4 e S7 (diversidade das figuras e pistas alheias à arma) e S8 (o que o experimento de luz mediu). Cada fato traz arquivo e linha no estado do repositório em 2026-10-17 (`07-blender/scripts/`, salvo indicação). Nada foi renderizado ou treinado.

## 1. Formato dos renders, motor e o que NÃO é simulado

| Fato | Valor | Origem |
|---|---|---|
| Motor | Cycles, GPU (OptiX, senão CUDA) | `gen_morro.py` 1623, 1627 a 1639 |
| Amostras por pixel | `--samples`: 96 nos corpora de 150 m, oblíquos, 75 m original, arma inédita, porte e regime; 64 no 35 m, nos dois gêmeos e nos 80 quadros novos; piloto não apurado | `gen_morro.py` 58 e 1640; comandos em `fila_noite.py` 209 a 212, 280 a 287, 306 a 308, 347 a 350; `rodada3.py` 52 a 62; `rodada4.py` 51 a 72 |
| Denoising | ligado (`scene.cycles.use_denoising = True`), denoiser padrão do Blender 5.2 | `gen_morro.py` 1641 |
| Saltos de luz | max 10, difusos 8, transmissão 4, volume 1 | `gen_morro.py` 1642 a 1645 |
| Transformação de visualização | AgX, look "Medium High Contrast" se disponível, exposição base 0,20 e deslocamento por regime (seção 4) | `gen_morro.py` 1432 a 1439, 1488 |
| Formato gravado pelo gerador | PNG (`file_format = "PNG"`), 3840 × 2160 (1920 × 1080 no piloto), sem perda | `gen_morro.py` 1626; arquivos `images/train/*.png` em todos os corpora |
| Compressão antes do treino | ladrilhos de 1280 px gravados em JPEG, qualidade 92, subamostragem de croma desligada (4:4:4), uma única codificação | `tile_dataset.py` 78 |
| Compressão nos testes de imagem inteira | nenhuma: `confusao_armado.py` e `por_regime.py` leem os PNG dos quadros | pastas `images/val/*.png`; `por_regime.py` cabeçalho (imgsz 3840) |
| Pós-processamento de câmera (`post_process.py`: ruído de sensor dependente do sinal, desfoque gaussiano de 0,25 a 0,8 px, aberração cromática de até 1,5 px, vinheta, névoa, JPEG de qualidade 82 a 95) | **existe mas não foi aplicado a nenhum corpus do `gen_morro`**: os quadros continuam PNG, não há pasta `images_png/`, e nenhuma das cadeias (`fila_noite.py`, `rodada3.py`, `rodada4.py`) chama o script. Foi usado só nos braços de 12 e 13/09 (`dataset_v3`, `dataset_odm`, `dataset_cid150`), que não estão no artigo | `post_process.py` 1 a 68; `RESULTADOS.md`, seção 1 da ficha |
| Ruído de sensor | não simulado (o denoiser remove o ruído de Monte Carlo; nenhum ruído é somado depois) | ausência de qualquer chamada no código do gerador |
| Borrão de movimento | não simulado (`use_motion_blur` não aparece em `gen_morro.py`) | idem |
| Desfoque de lente, profundidade de campo | não simulado (`dof` não aparece; câmera nova do Blender nasce com DOF desligado) | `gen_morro.py` 1505 a 1515 |
| Obturador rolante, aberração cromática, vinheta, distorção de lente | não simulados | idem |
| Resolução do sensor real | não simulada: o sensor de 2,13 MP (1080p) da Z30 é representado por um render sem perda em 4K, o que equivale a 2× de zoom na câmera real (`gsd_zoom.md`, 3.2) | |
| Textura de solo, fachada e laje | materiais PBR Poly Haven (CC0) e procedurais; quatro modelos de árvore CC0; nenhum pacote comercial e nenhum dado PCERJ | `gen_morro.py` 50 (`ASSETS`), 7.2 do manuscrito |

Consequência para a 4.2.4 e a 6.5: os renders são imagens sem ruído, sem borrão, sem compressão com perda nos quadros, e com um único JPEG de qualidade 92 nos ladrilhos de treino. Um quadro real da Z30 a 150 m traz ruído de sensor de 1/2,8", compressão H.264 do vídeo FHD e borrão proporcional ao tempo de exposição e ao deslocamento do drone; nenhum destes efeitos entrou no corpus, e o artigo deve dizê-lo em vez de descrever o `post_process.py` como se tivesse sido usado.

## 2. As figuras humanas

Origem: `people_mpfb.py` (MPFB 2, build 20260722, assets CC0 do MakeHuman instalados em `%APPDATA%\Blender Foundation\Blender\5.2\extensions\.user\user_default\mpfb\data\`).

| Fato | Valor | Origem |
|---|---|---|
| Corpos base por corpus | `--pool 6`: seis humanos criados por `bpy.ops.mpfb.create_random_human()` no início de cada execução do gerador, guardados fora da cena e duplicados (cópia ligada) por instância | `gen_morro.py` 68, 1687; `people_mpfb.py` 66 a 121, 407 a 412 |
| Semente dos corpos | derivada da semente do lote desde 22/09 (`random.seed(0x5EED ^ ...)`); os corpora renderizados antes da correção tiveram corpos não reprodutíveis: `ds_morro_clima`, `ds_morro_4k` e também o 75 m original (`ds_armado_75`, render terminado em 22/09 às 05:10, antes do commit da semeadura às 21:48; correção do integrador em 18/10) | `people_mpfb.py` 71 a 78; `DIARIO.md`, 2026-09-22 |
| O que o MPFB sorteia em cada corpo (configuração padrão do addon, nenhuma propriedade alterada pelo gerador) | sexo discreto (mulher ou homem); idade contínua (distribuição em sino em torno do valor neutro); músculo, peso, altura e proporções contínuos; pesos de "raça" (african, asian, caucasian) contínuos e normalizados; alvos de detalhe; pele sorteada entre as 23 instaladas (young, middleage, old × african, asian, caucasian × female, male, mais duas variantes); cabelo sorteado entre 10 estilos; íris sorteada | `randomizationservice.py` 374 a 440 e `ui/new_human/randomize/properties/*.json` do MPFB (`discrete_gender` True, `discrete_age` False, `discrete_race` False, `randomize_skin` True, `hair_randomize` True) |
| Tom de pele | varia entre os seis corpos (pele sorteada pelo MPFB), não por instância | `people_mpfb.py` 83 (só `create_random_human`) |
| Idade | contínua no MPFB; não foi verificado se corpos de criança ocorrem no pool | `randomizationservice.py` 416 a 427 |
| Roupa | um traje completo (`*suit*.mhclo`) por corpo, sorteado entre os 12 instalados (8 masculinos: casualsuit01 a 06, elegantsuit01, worksuit01; 4 femininos: casualsuit01, 02, elegantsuit01, sportsuit01), **sem filtro de sexo**, com material MakeSkin; sapatos vêm do MPFB; dentes, língua, sobrancelhas e cílios removidos | `people_mpfb.py` 43 a 48, 96 a 104; pasta `mpfb/data/clothes` |
| Variação da roupa por instância | matiz uniforme em 0 a 1, saturação 0,4 a 1,4, valor 0,5 a 1,15 (nó Hue/Saturation sobre a cor base), rugosidade 0,85 | `people_mpfb.py` 143 a 166 |
| Sem camisa | 35 por cento das instâncias masculinas, com bermuda pintada no corpo entre 0,42 e 0,58 da altura numa de seis cores | `people_mpfb.py` 169 a 200, 418 a 437 |
| Escala (altura) | fator uniforme 0,92 a 1,08 por instância sobre o corpo do MPFB (cerca de 1,75 m no espaço local), ou seja altura de cerca de 1,61 a 1,89 m; o objeto carregado recebe escala inversa para manter o tamanho real | `people_mpfb.py` 441, 463 a 465, 513 |
| Orientação | yaw uniforme 0 a 360 graus | `people_mpfb.py` 440 |
| Poses, desarmada | parado 0,36, andando 0,38, sentado 0,14, braços cruzados 0,12; cada pose com ruído por osso (`pose_rig`) | `people_mpfb.py` 307 a 383, 460 |
| Poses, armada e com objeto | empunhando 0,42, ao lado 0,26, nas costas 0,16, andando 0,16, a mesma distribuição para arma e objeto; com `--porte-realista` (35 m, gêmeos e quadros novos) o objeto passa a empunhando 0,08, lado 0,34, costas 0,28, andando 0,30, e a arma mantém a primeira | `people_mpfb.py` 442 a 458; `gen_morro.py` 91 a 93 |
| Pose "agachado" | existe em `pose_rig` mas não é sorteada por `make_person` (só por argumento explícito); não ocorre nos corpora | `people_mpfb.py` 353, 442 a 460 |
| Grupos | `place_group` existe mas não é chamado por `gen_morro.py`: as pessoas são colocadas uma a uma, 45 por cento sobre laje (`--laje 0.45`; 75 por cento a 35 m e nos gêmeos) e o resto em célula livre de beco | `people_mpfb.py` 522 a 538; `gen_morro.py` 75 a 78, 1786 a 1805 |
| Pessoas por quadro (sorteadas) | 16 a 34 nos corpora de 150 m e oblíquos; 14 a 30 no 75 m original, arma inédita e porte; 12 a 24 no 35 m, gêmeos e quadros novos; 10 a 26 no piloto (padrão) | `gen_morro.py` 67; comandos citados na seção 1 |

O que isso limita: a diversidade de corpo, pele e cabelo de um corpus é a de seis indivíduos; a diversidade de aparência vem da cor da roupa, da escala, da pose e da orientação por instância. Não há crianças verificadas, não há mochilas, bonés, guarda-chuvas abertos nem roupas além de trajes inteiros do MakeHuman; não há figuras parcialmente dentro de edificação além da oclusão natural de becos.

## 3. Armas e objetos confundíveis

Origem: `objetos_alongados.py` (entrou no repositório em 2026-09-20 18:01, commit 8a8070e). **Os dois corpora mais antigos usaram outra biblioteca**: `ds_morro_clima` (render terminado em 2026-09-20 04:07) e `ds_morro_4k` (iniciado antes do commit e terminado às 22:52 do mesmo dia; o manifest não tem os campos `tipos`, `comps`, `n_objeto` e `pitch` que o gerador passou a gravar com a terceira classe) usaram o fuzil e a pistola de `people_mpfb.py` (`make_rifle`, três silhuetas: padrão AK 55 por cento, padrão AR 30 por cento, carabina 15 por cento; `make_pistol`; pistola em 15 por cento das armadas; comprimento registrado 0,9 m para todas), linhas 253 a 297. Todos os corpora posteriores (de `ds_variedade` em diante, inclusive S-oblique) usaram a biblioteca abaixo, como a 7.7 do manuscrito já diz para S-oblique.

| Item | Peso de sorteio | Comprimento registrado (m) | Materiais | Origem (linha) |
|---|---|---|---|---|
| fuzil padrão AK | 26 | 0,92 | metal, madeira | 120 a 131 |
| fuzil padrão AR | 24 | 0,94 | polímero, metal | 134 a 146 |
| carabina (coronha recolhida) | 20 | 0,62 | polímero, metal | 149 a 159 |
| espingarda | 18 | 1,05 | madeira, metal | 162 a 171 |
| pistola | 12 | 0,20 | metal, polímero | 174 a 181 |
| fuzil FAL (inédito, só teste) | 50 dos 50 por cento inéditos | 1,10 | metal ou metal gasto; polímero ou madeira | 293 a 306 |
| submetralhadora (inédita, só teste) | 50 dos 50 por cento inéditos | 0,55 | | 309 a 320 |
| vassoura | 20 | 1,28 | cabo madeira clara ou PVC cinza, cerda | 196 a 205 |
| rodo | 12 | 1,22 | madeira clara, plástico colorido | 208 a 212 |
| cano de PVC | 14 | 1,5 a 2,5 (uniforme) | PVC | 215 a 221 |
| vergalhão | 16 | 1,0 a 2,0 | ferrugem ou metal gasto | 224 a 231 |
| tábua | 12 | 0,9 a 2,0 | madeira clara (60 por cento) ou madeira | 234 a 239 |
| guarda-chuva fechado | 12 | 0,88 | madeira, pano escuro, metal | 242 a 249 |
| enxada | 8 | 1,24 | madeira, metal gasto | 252 a 256 |
| tapete enrolado | 8 | 1,1 a 1,8 | plástico colorido (40 por cento) ou pano escuro | 259 a 265 |
| mangueira enrolada | 6 | registrado 1,0 (malha de 0,7 a 1,3) | plástico colorido | 268 a 271 |

- Paleta compartilhada (`mats()`, linhas 46 a 62): onze materiais; metal, metal gasto, madeira, madeira clara e polímero ocorrem em armas e em objetos; PVC, PVC cinza, ferrugem, pano escuro, cerda e plástico colorido só em objetos. Cor e rugosidade são fixas por material (sem variação por instância).
- Geometria: caixas e cilindros no eixo +X com origem na empunhadura (`Construtor`, 65 a 112); nenhum modelo externo. A extensão real das malhas não foi conferida contra o comprimento registrado (a 7.4 do manuscrito diz que fuzis e espingarda são mais longos do que o registrado).
- Fixação: objeto parentado ao rig; posição na ponta do osso `wrist.R` (ou `spine03` mais 0,16 m à frente, na pose "costas"); orientação fixada por pose no referencial do corpo com ruído de 6 a 10 graus (`people_mpfb.py` 484 a 503); pistola com ângulos próprios (501); objeto com mais de 1,15 m reangulado para o ombro ou para o chão (508 a 510), salvo com `--objeto-porte-arma` (porte de arma: mesmos sorteios, ângulo de arma). A tabela `PORTES` e `sorteia_porte` em `objetos_alongados.py` (366 a 390) não são chamadas por nenhum script: código morto, não descreve os corpora.
- Mistura de classes: `--mistura 0.34 0.33 0.33` nos corpora de três classes; `0.5 0.5 0` nos de 150 m nadir e no oblíquo de um sítio; `0 1 0` no oblíquo de seis sítios (só desarmadas). Modo `--armas mista_inedita`: metade das armas sai dos cinco modelos, metade dos dois inéditos (`faz_arma`, 344 a 352; `MODO_ARMAS`, 330).

Pistas alheias à arma que o código permite (para a 4.2.2 e a 6.5): comprimento (armas 0,20 a 1,05 m, objetos 0,88 a 2,5 m), materiais exclusivos de objeto (PVC, plástico colorido, cerda, ferrugem), ângulo de porte dos objetos longos, e a frequência da pose de tiro (0,42 contra 0,08 para objeto com `--porte-realista`). O teste de porte (`ds_armado_75_porte`) neutraliza o ângulo; nenhum teste neutraliza comprimento nem material.

## 4. Regimes de iluminação

Origem: `gen_morro.py`, dicionário `CLIMAS` (1456 a 1473) e `aplica_clima` (1476 a 1498); céu Nishita com `sun_elevation`, `sun_rotation`, `air_density` e `dust_density`.

| Regime (nome no artigo) | Elevação do sol (graus, uniforme) | Energia do sol | Diâmetro angular do sol (graus) | Preenchimento do céu | Densidade de névoa (×1e-4) | Deslocamento de exposição | Ar / poeira (Nishita) |
|---|---|---|---|---|---|---|---|
| sol_duro (hard sun) | 46 a 74 | 5,0 | 0,6 | 0,92 | 0,9 | +0,20 | 1,1 / 2,2 |
| sol_baixo (low sun) | 9 a 25 | 3,6 | 0,9 | 0,85 | 2,8 | +0,40 | 1,6 / 8,0 |
| nublado (overcast) | 30 a 70 | 0,55 | 24 | 2,45 | 2,6 | -0,10 | 1,9 / 6,0 |
| encoberto (heavy overcast) | 28 a 66 | 0,12 | 38 | 1,70 | 3,8 | -0,55 | 2,2 / 9,5 |
| neblina (haze) | 22 a 52 | 2,0 | 7 | 1,60 | 9,0 | +0,05 | 2,4 / 10,0 |
| chuva (rain) | 24 a 60 | 0,22 | 32 | 1,10 | 5,2 | -0,90 | 2,3 / 10,0 |

Por quadro: azimute do sol uniforme 0 a 360 graus; energia do sol × U(0,85; 1,15); preenchimento × U(0,9; 1,1); névoa × U(0,8; 1,25); exposição + U(-0,12; +0,12); cor do sol e do céu fixas por regime. Os regimes são percorridos em ordem (`CLIMAS_USO[i % 6]`, linha 1704), não sorteados, por isso cada corpus tem 30, 33 a 34 ou 20 quadros por regime (`corpora.md`, tabela 4). Não há chuva renderizada (gotas, molhado): "chuva" é um orçamento de luz escura e difusa com névoa densa. Elevações realizadas nos manifests: 9,1 a 74,0 graus no conjunto (`corpora.json`).

## 5. O que o experimento de luz mediu, e só isso

Duas medidas distintas, que o texto deve manter separadas:

**(a) Estatística de contraste (modelo-livre), seção 8.3 do manuscrito.** `06-resultados/mede_contraste_clima.py` sobre o **piloto** `ds_morro_clima` (48 quadros de 1920 × 1080, 8 por regime, 684 caixas), saída `06-resultados/contraste_clima.csv` (2026-09-20 17:24). Por caixa: luminância média dentro da caixa menos a média de um anel de 6 px em volta (`bruto_dn`, em níveis de 0 a 255), e essa diferença dividida pelo desvio padrão do anel (`razao_mediana`, mediana por regime; `razao_dp_entre_img`, dispersão entre quadros). Valores do CSV: sol_duro 15,2 DN e 0,64; sol_baixo 9,0 e 0,70; nublado 16,4 e 0,88; neblina 9,6 e 0,79; encoberto 11,2 e 0,72; chuva 6,6 e 0,63; luminância média do quadro 87,0; 56,0; 84,6; 94,4; 55,6; 35,1. (A entrada de `07-blender/HISTORICO-LOOP.md` cita uma versão anterior da medida, 16,6 e 0,54 para sol duro; vale o CSV.) É uma medida sobre renders de 1080p, a GSD do piloto, não sobre o corpus de referência.

**(b) Teste por regime, seção 10.3 do manuscrito (rodada 4, etapa J).** Um único modelo, `s_nadir_4k` (S-nadir-150, treinado nos quadros 0 a 179 com os seis regimes), avaliado em `ds_regime_4k`: 120 quadros novos (índices 180 a 299 da mesma semente 21 e do mesmo comando, renderizados depois do treino, 20 por regime, 2.204 caixas). Comando: `python por_regime.py --pesos runs/detect/s_nadir_4k/weights/best.pt --ds ds_regime_4k --tiles ds_regime_4k_tiles` (saída `por_regime_s_nadir_4k.json`). Medidas: mAP50 nos ladrilhos de cada regime (validador Ultralytics, classe única, conf 0,001) e recall a conf 0,25 em imagem inteira (imgsz 3840, casamento 1:1 a IoU 0,5) com IC 95 por cento por bootstrap de quadros (2.000 reamostragens). Critério pré-fixado: nublado acima de sol_duro e de chuva, e sol_duro entre os dois mais fracos. Resultado: cumprido (mAP50 0,675 sol_duro; 0,755 encoberto; 0,759 chuva; 0,780 neblina; 0,790 sol_baixo; 0,791 nublado), com intervalos de recall que se sobrepõem entre nublado e chuva.

O que (b) **não** é: não há modelo treinado só em sol duro nem só em nublado (a ablação é o R5-4 proposto); não há imagem real envolvida; os 120 quadros são do mesmo sítio e da mesma semente do treino, então medem dificuldade por regime dentro do mundo sintético, para um modelo que viu todos os regimes em proporções iguais. A frase do artigo pode ser: "um detector treinado com os seis regimes detecta pior sob sol duro, em quadros novos do mesmo cenário sintético"; não pode ser "voar em dia nublado melhora a detecção", que exige ablação e dado real.
