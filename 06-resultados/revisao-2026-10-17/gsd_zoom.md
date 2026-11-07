# GSD, pegada no solo e a câmera de referência (revisão de 2026-10-17, agente D1)

Responde ao ponto M3 do revisor (GSD além de altitude; justificar a câmera e seu zoom). Valores numéricos em `gsd_zoom.json`; a aritmética foi feita em Python e está reproduzida aqui. Nada foi renderizado ou treinado.

## 1. O modelo de câmera do gerador

Origem: `03-blender/scripts/gen_morro.py`, linhas 1503 a 1508 e 1603.

```
Z30_LENS = 4.3 * 36 / 5.37      # 4.3 mm num sensor de 5.37 mm, ou seja ~28,8 mm equivalente
c.lens = lente; c.sensor_width = 36; c.sensor_fit = "HORIZONTAL"
CAMS["nadir"] = camera("CAM_NADIR_150m_Z30", Z30_LENS, ...)
```

Todo quadro de todo corpus sai de `cam_ds = CAMS["nadir"]` (linha 1690), inclusive os oblíquos: o preset `--obliqua` muda só altitude e inclinação (linhas 161 a 170), não a lente. Portanto:

| Parâmetro | Valor | Como se obtém |
|---|---|---|
| Sensor (Blender) | 36 mm de largura, ajuste horizontal | fixado no código |
| Distância focal | 28,83 mm equivalente | 4,3 × 36 / 5,37 |
| Campo de visão horizontal | 63,96 graus | 2 × atan(18 / 28,83) |
| Campo de visão vertical (16:9) | 38,71 graus | 2 × atan(10,125 / 28,83) |
| Largura no solo (nadir) | altitude × 1,2488 | altitude × 36 / 28,83 |
| Altura no solo | largura × 0,5625 | proporção 1080/1920 |
| GSD | largura / pixels de largura | metros por pixel × 100 = cm/px |

Seção 7.3 do manuscrito de 30/09: "a Zenmuse Z30 at 1920 by 1080, corresponding to a 4.3 mm lens on a 5.37 mm sensor, or approximately 28.8 mm on a 36 mm equivalent ... the frame covers approximately 187 by 105 m ... 9.76 cm per pixel ... 4.88 cm per pixel ... at 75 m ... 94 by 53 m ... 2.44 cm per pixel". **Código e manuscrito concordam.** O que a 7.3 não dá: a GSD de 35 m (a 9.5 diz "1,1 cm/px"; o valor é 1,14) e a altitude do preset oblíquo (120 m, com variação de 36 m, dita na 10.4).

A premissa "sensor de 5,37 mm" não vem da DJI (ver seção 3); vem do FOV publicado. O FOV horizontal resultante (63,96 graus) difere do publicado (63,7 graus) em 0,3 grau.

## 2. Altitude × render → GSD e pegada (câmera do gerador, nadir, altitude nominal)

Altitudes realizadas variam com `--alt-jitter` (6 m a 150 e a 75 m; 3 m a 35 m; 13 m no gêmeo de 150 m); a GSD média realizada de cada corpus está em `corpora.json` e difere da nominal em menos de 1 por cento.

| Altitude (m) | Pegada no solo (m × m) | Render | GSD (cm/px) | Pessoa em planta, 0,48 m (px) | Fuzil de 0,92 m deitado (px) |
|---|---|---|---|---|---|
| 35 | 43,7 × 24,6 | 1920 × 1080 | 2,28 | 21,1 | 40,4 |
| 35 | 43,7 × 24,6 | 3840 × 2160 | **1,14** | 42,2 | 80,8 |
| 75 | 93,7 × 52,7 | 1920 × 1080 | 4,88 | 9,8 | 18,9 |
| 75 | 93,7 × 52,7 | 3840 × 2160 | **2,44** | 19,7 | 37,7 |
| 120 (preset oblíquo) | 149,9 × 84,3 (nominal de nadir) | 3840 × 2160 | 3,90 (nominal) | 12,3 | 23,6 |
| 150 | 187,3 × 105,4 | 1920 × 1080 | **9,76** | 4,9 | 9,4 |
| 150 | 187,3 × 105,4 | 3840 × 2160 | **4,88** | 9,8 | 18,9 |

Aritmética de uma linha, para conferência: 150 × 36 / 28,83 = 187,33 m; 187,33 / 3840 = 0,04878 m = 4,88 cm/px; 187,33 × 0,5625 = 105,37 m. As larguras em pixels da pessoa e do fuzil são o objeto dividido pela GSD (0,48 / 0,0488 = 9,8), antes de qualquer oclusão; as medianas medidas nas anotações (17,6 × 17,5 px no corpus de referência) são maiores porque a caixa envolve corpo inteiro, braços e objeto carregado.

Para o corpus oblíquo a GSD no solo não é uma só: a câmera a 120 m inclinada 26 a 56 graus vê o solo a distâncias entre 120 m (no nadir) e cerca de 215 m (a 56 graus), então a GSD real varia ao longo do quadro; 3,90 cm/px é o número nominal de nadir usado em `RESULTADOS.md` ("GSD 3,9 cm/px").

## 3. A câmera real de referência: DJI Zenmuse Z30

Fonte primária: DJI, *Zenmuse Z30 User Manual* v1.2, PDF datado de 2019-09-06 (rodapé "© 2018 DJI"), seção *Specifications*, páginas 13 e 14. Obtido em https://dl.djicdn.com/downloads/Z30/20190906/Z30_User_Manual_EN.pdf, que é o arquivo listado em https://www.dji.com/downloads/products/zenmuse-z30 (lido em 2026-10-17; o PDF tem proteção de cópia, o texto foi extraído com PyMuPDF).

Citado do manual, verbatim:

| Campo | Texto do manual |
|---|---|
| Sensor | CMOS, 1/2.8" Effective Pixels: 2.13 M |
| Lens | 30× Optical Zoom F = 4.3 mm to 129 mm (29 mm to 872 mm equivalent) F1.6 to F4.7 |
| FOV | 63.7° to 2.3° |
| Digital Zoom | 6× |
| Video Resolution | FHD: 1920×1080 25/30p |
| Photo Resolution | 16:9, 1920×1080 |
| Gimbal, Angular Vibration Range | ±0.01° |
| Weight | 556 g |

O que a DJI **não publica**: a largura física do sensor em milímetros, o tamanho do pixel e se o FOV é horizontal ou diagonal. Daí:

- Largura de sensor implícita pelo FOV, tomado como horizontal: 2 × 4,3 × tan(63,7 / 2) = 5,34 mm. Pelo "29 mm equivalente": fator de corte 29 / 4,3 = 6,74, diagonal 43,27 / 6,74 = 6,42 mm, largura 16:9 de 5,59 mm. O 5,37 mm do gerador fica entre os dois e reproduz o FOV publicado dentro de 0,3 grau. A hipótese de FOV diagonal é descartada porque daria 34,8 mm equivalente, incompatível com os 29 mm que a própria DJI publica.
- A ficha do manual de 2022 do projeto (voo da PCERJ: 1920 × 1080, nadir, 150 m) é consistente com esta câmera em grande-angular.

### 3.1 O que a Z30 entrega a 150 m em nadir (computado; 1920 px de largura)

Método: largura no solo = 2 × 150 × tan(FOV / 2) com o FOV horizontal do manual; GSD = largura / 1920; altura = largura × 9 / 16.

| Ajuste | FOV (graus) | Pegada (m × m) | GSD (cm/px) | Pessoa em planta 0,48 m (px) |
|---|---|---|---|---|
| Grande-angular, 4,3 mm (1×) | 63,7 (manual) | 186,4 × 104,8 | **9,71** | 4,9 |
| Tele, 129 mm (30×) | 2,3 (manual) | 6,0 × 3,4 | **0,31** | 153 |

Contra o gerador em 1080p (187,3 m e 9,76 cm/px): diferença de 0,5 por cento, que vem só da premissa de 5,37 mm contra 5,34 mm. Escalar a largura grande-angular por 30 dá 6,21 m e FOV de 2,37 graus; o manual arredonda para 2,3.

### 3.2 Zoom necessário, a 150 m, para casar a GSD dos corpora sintéticos (computado)

Método: largura necessária = GSD alvo × 1920 px; zoom = 186,37 / largura necessária; distância focal = 4,3 mm × zoom; equivalente = focal × 29 / 4,3; FOV = 2 × atan(largura / 300).

| GSD alvo | De onde vem | Largura necessária (m × m) | Zoom óptico | Focal (mm) | Equivalente (mm) | FOV horizontal (graus) |
|---|---|---|---|---|---|---|
| 4,88 cm/px | render 4K a 150 m (corpus de referência) | 93,7 × 52,7 | **2,0×** | 8,6 | 58 | 34,7 |
| 2,44 cm/px | S-nadir-75 em 4K | 46,8 × 26,3 | **4,0×** | 17,1 | 115 | 17,7 |
| 1,14 cm/px | S-nadir-35 em 4K | 21,9 × 12,3 | **8,5×** | 36,7 | 247 | 8,3 |

Leitura para a 4.2.4 e a 6.2: a GSD de 35 m é alcançável de 150 m com 8,5× dos 30× ópticos, ao custo de a pegada cair de 186 × 105 m para 22 × 12 m, 73 vezes menos área por quadro (e 16 vezes menos a 2,44 cm/px, 47 × 26 m). O render 4K a 150 m já corresponde a 2× de zoom na câmera real, o que é a forma precisa de dizer que "o sintético em 4K é mais fácil que um quadro isolado da câmera" (8.1 do manuscrito de 30/09).

### 3.3 O que não está computado nem publicado

- Estabilidade com zoom: a única cifra publicada é a vibração angular do gimbal, ±0,01 grau; a 150 m isso desloca o quadro 2,6 cm (150 × tan 0,01 grau), 2,3 pixels na GSD de 1,14 cm/px e 0,3 pixel na de 9,7. Movimento do drone, vento e o tempo de exposição (1/30 a 1/6000 s no manual) não foram modelados: o gerador não simula borrão de movimento (ver `gerador-fatos.md`).
- Resolução óptica real da lente nas focais longas (MTF): não publicada; a GSD geométrica é um limite superior do detalhe.
- O manual lista FOV sem dizer se é horizontal ou diagonal; a leitura horizontal é a única compatível com o "29 mm equivalente" da mesma tabela.

Fontes consultadas e descartadas: a página de produto dji.com/zenmuse-z30/info é renderizada em JavaScript e não devolve texto; listagens de revendedores (Adorama, GetFPV, Full Compass) repetem a tabela do manual mas bloqueiam leitura automática ou não acrescentam a largura do sensor.
