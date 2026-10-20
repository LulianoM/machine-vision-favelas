# Reamostragem no VisDrone-DET val, rodada 5 (19/10/2026)

1000 reamostras das 548 imagens, semente 0, pareadas; diferenca na media das sementes de cada lado.

| Grupo | runs | media mAP50 | faixa | IC 95% da media | eficacia |
|---|---|---|---|---|---|
| R | r_pareado | 0.6311 | 0.6311 a 0.6311 | 0.6149 a 0.6471 | 100.0% |
| S-nadir-150 | s_nadir_4k, s_nadir_4k_sd1, s_nadir_4k_sd2 | 0.0136 | 0.0102 a 0.0198 | 0.0120 a 0.0160 | 2.2% |
| S-oblique | s_obliquo, s_obliquo_sd1, s_obliquo_sd2 | 0.0555 | 0.0501 a 0.0614 | 0.0502 a 0.0614 | 8.8% |
| S-oblique-six | s_oblvar, s_oblvar_sd1, s_oblvar_sd2 | 0.0966 | 0.0887 a 0.1055 | 0.0896 a 0.1048 | 15.3% |
| S-nadir-150-six | s_variedade | 0.0190 | 0.0190 a 0.0190 | 0.0142 a 0.0211 | 3.0% |
| S-oblique-six scenes | s_oblvar | 0.1055 | 0.1055 a 0.1055 | 0.0980 a 0.1148 | 16.7% |
| F-synthetic 5% orig | ft05_sint, ft05_sint_sd1, ft05_sint_sd2 | 0.4529 | 0.4424 a 0.4608 | 0.4373 a 0.4696 | 71.8% |
| F-synthetic 5% fz | ft05_sint_fz | 0.2808 | 0.2808 a 0.2808 | 0.2664 a 0.2952 | 44.5% |
| F-synthetic 5% lr | ft05_sint_lr | 0.3103 | 0.3103 a 0.3103 | 0.2961 a 0.3248 | 49.2% |
| F-synthetic 5% fzlr | ft05_sint_fzlr | 0.2028 | 0.2028 a 0.2028 | 0.1917 a 0.2144 | 32.1% |
| F-generic 5% orig | ft05_coco, ft05_coco_sd1, ft05_coco_sd2 | 0.5245 | 0.5220 a 0.5285 | 0.5075 a 0.5424 | 83.1% |
| F-generic 5% fz | ft05_coco_fz | 0.5467 | 0.5467 a 0.5467 | 0.5298 a 0.5642 | 86.6% |
| F-generic 5% lr | ft05_coco_lr, ft05_coco_lr_sd1, ft05_coco_lr_sd2 | 0.5897 | 0.5746 a 0.5982 | 0.5748 a 0.6073 | 93.4% |
| F-generic 5% fzlr | ft05_coco_fzlr | 0.5410 | 0.5410 a 0.5410 | 0.5238 a 0.5594 | 85.7% |
| F-synthetic 10% orig | ft10_sint | 0.5095 | 0.5095 a 0.5095 | 0.4935 a 0.5264 | 80.7% |
| F-synthetic 10% fz | ft10_sint_fz | 0.3209 | 0.3209 a 0.3209 | 0.3054 a 0.3358 | 50.8% |
| F-synthetic 10% lr | ft10_sint_lr | 0.3875 | 0.3875 a 0.3875 | 0.3724 a 0.4041 | 61.4% |
| F-synthetic 10% fzlr | ft10_sint_fzlr | 0.2241 | 0.2241 a 0.2241 | 0.2119 a 0.2369 | 35.5% |
| F-generic 10% orig | ft10_coco | 0.5709 | 0.5709 a 0.5709 | 0.5535 a 0.5883 | 90.5% |
| F-generic 10% fz | ft10_coco_fz | 0.5772 | 0.5772 a 0.5772 | 0.5607 a 0.5942 | 91.5% |
| F-generic 10% lr | ft10_coco_lr | 0.6224 | 0.6224 a 0.6224 | 0.6072 a 0.6396 | 98.6% |
| F-generic 10% fzlr | ft10_coco_fzlr | 0.5644 | 0.5644 a 0.5644 | 0.5487 a 0.5815 | 89.4% |
| F-synthetic 5% chosen | ft05_sint, ft05_sint_sd1, ft05_sint_sd2 | 0.4529 | 0.4424 a 0.4608 | 0.4373 a 0.4696 | 71.8% |
| F-generic 5% chosen | ft05_coco_lr, ft05_coco_lr_sd1, ft05_coco_lr_sd2 | 0.5897 | 0.5746 a 0.5982 | 0.5748 a 0.6073 | 93.4% |
| F-synthetic 10% chosen | ft10_sint | 0.5095 | 0.5095 a 0.5095 | 0.4935 a 0.5264 | 80.7% |
| F-generic 10% chosen | ft10_coco_lr | 0.6224 | 0.6224 a 0.6224 | 0.6072 a 0.6396 | 98.6% |

| Comparacao | a | b | dif. | IC 95% | dif. relativa | razao a/b (IC 95%) |
|---|---|---|---|---|---|---|
| R5-1 nadir vs oblique (principal) | 0.0555 | 0.0136 | +0.0419 | +0.0368 a +0.0470 | +307.9% | 4.079 (3.436 a 4.642) |
| R5-1 six settlements vs one, oblique | 0.0966 | 0.0555 | +0.0411 | +0.0367 a +0.0462 | +74.0% | 1.74 (1.641 a 1.85) |
| R5-1 six settlements vs one, nadir | 0.0190 | 0.0136 | +0.0054 | +0.0009 a +0.0066 | +39.9% | 1.399 (1.066 a 1.504) |
| R5-5 generic vs synthetic start, 5%, cell orig | 0.5245 | 0.4529 | +0.0716 | +0.0658 a +0.0780 | +15.8% | 1.158 (1.144 a 1.173) |
| R5-5 generic vs synthetic start, 5%, cell fz | 0.5467 | 0.2808 | +0.2659 | +0.2538 a +0.2791 | +94.7% | 1.947 (1.88 a 2.027) |
| R5-5 generic vs synthetic start, 5%, cell lr | 0.5897 | 0.3103 | +0.2794 | +0.2676 a +0.2920 | +90.1% | 1.901 (1.84 a 1.97) |
| R5-5 generic vs synthetic start, 5%, cell fzlr | 0.5410 | 0.2028 | +0.3382 | +0.3232 a +0.3533 | +166.7% | 2.667 (2.539 a 2.807) |
| R5-5 generic vs synthetic start, 5%, chosen schedules | 0.5897 | 0.4529 | +0.1369 | +0.1290 a +0.1465 | +30.2% | 1.302 (1.279 a 1.331) |
| R5-5 generic vs synthetic start, 10%, cell orig | 0.5709 | 0.5095 | +0.0614 | +0.0553 a +0.0679 | +12.1% | 1.121 (1.108 a 1.134) |
| R5-5 generic vs synthetic start, 10%, cell fz | 0.5772 | 0.3209 | +0.2562 | +0.2451 a +0.2678 | +79.8% | 1.798 (1.746 a 1.859) |
| R5-5 generic vs synthetic start, 10%, cell lr | 0.6224 | 0.3875 | +0.2348 | +0.2238 a +0.2458 | +60.6% | 1.606 (1.562 a 1.65) |
| R5-5 generic vs synthetic start, 10%, cell fzlr | 0.5644 | 0.2241 | +0.3402 | +0.3258 a +0.3539 | +151.8% | 2.518 (2.4 a 2.634) |
| R5-5 generic vs synthetic start, 10%, chosen schedules | 0.6224 | 0.5095 | +0.1129 | +0.1044 a +0.1230 | +22.2% | 1.222 (1.202 a 1.245) |
| R5-2 C-ii scene seeds vs S-oblique training seeds | 0.1055 | 0.0555 | +0.0499 | +0.0444 a +0.0563 | +89.9% | 1.899 (1.778 a 2.046) |

Faltando: R5-3 152 vs 30 frames; R5-3 152 vs 120 frames
