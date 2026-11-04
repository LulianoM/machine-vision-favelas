# Eficacias com o R de selecao fora do teste (rodada 6, item 4)

R (selecao no val) 0.6311; R-sel (selecao em sel_r) 0.6224; vies R menos R-sel +0.0087 (IC 95% pareado +0.0035 a +0.0136).

| Grupo | runs | media mAP50 | IC 95% | eficacia / R | eficacia / R-sel (IC 95%) |
|---|---|---|---|---|---|
| R | r_pareado | 0.6311 | 0.6149 a 0.6471 | 100.0% | 101.4% (100.6 a 102.2) |
| S-nadir-150 | s_nadir_4k, s_nadir_4k_sd1, s_nadir_4k_sd2 | 0.0136 | 0.0120 a 0.0160 | 2.2% | 2.2% (1.9 a 2.6) |
| S-oblique | s_obliquo, s_obliquo_sd1, s_obliquo_sd2 | 0.0555 | 0.0502 a 0.0614 | 8.8% | 8.9% (8.2 a 9.7) |
| S-oblique-six | s_oblvar, s_oblvar_sd1, s_oblvar_sd2 | 0.0966 | 0.0896 a 0.1048 | 15.3% | 15.5% (14.6 a 16.7) |
| S-nadir-150-six | s_variedade | 0.0190 | 0.0142 a 0.0211 | 3.0% | 3.1% (2.3 a 3.4) |
| S-oblique-six c030 | s_oblvar_c030, s_oblvar_c030_sd1, s_oblvar_c030_sd2 | 0.0618 | 0.0566 a 0.0679 | 9.8% | 9.9% (9.1 a 10.8) |
| S-oblique-six c060 | s_oblvar_c060 | 0.0806 | 0.0739 a 0.0885 | 12.8% | 13.0% (12.0 a 14.1) |
| S-oblique-six c090 | s_oblvar_c090 | 0.0810 | 0.0745 a 0.0886 | 12.8% | 13.0% (12.0 a 14.1) |
| S-oblique-six c120 | s_oblvar_c120, s_oblvar_c120_sd1, s_oblvar_c120_sd2 | 0.0904 | 0.0838 a 0.0986 | 14.3% | 14.5% (13.5 a 15.7) |
| S-oblique-six scenes | s_oblvar, s_oblvar_e22, s_oblvar_e23 | 0.0937 | 0.0868 a 0.1019 | 14.8% | 15.0% (14.1 a 16.2) |
| F-synthetic 5% orig | ft05_sint, ft05_sint_sd1, ft05_sint_sd2 | 0.4529 | 0.4373 a 0.4696 | 71.8% | 72.8% (71.2 a 74.0) |
| F-synthetic 5% fz | ft05_sint_fz | 0.2808 | 0.2664 a 0.2952 | 44.5% | 45.1% (43.4 a 46.8) |
| F-synthetic 5% lr | ft05_sint_lr | 0.3103 | 0.2961 a 0.3248 | 49.2% | 49.9% (48.2 a 51.5) |
| F-synthetic 5% fzlr | ft05_sint_fzlr | 0.2028 | 0.1917 a 0.2144 | 32.1% | 32.6% (31.1 a 34.1) |
| F-generic 5% orig | ft05_coco, ft05_coco_sd1, ft05_coco_sd2 | 0.5245 | 0.5075 a 0.5424 | 83.1% | 84.3% (83.1 a 85.3) |
| F-generic 5% fz | ft05_coco_fz | 0.5467 | 0.5298 a 0.5642 | 86.6% | 87.8% (86.4 a 89.2) |
| F-generic 5% lr | ft05_coco_lr, ft05_coco_lr_sd1, ft05_coco_lr_sd2 | 0.5897 | 0.5748 a 0.6073 | 93.4% | 94.8% (93.6 a 95.9) |
| F-generic 5% fzlr | ft05_coco_fzlr | 0.5410 | 0.5238 a 0.5594 | 85.7% | 86.9% (85.4 a 88.5) |
| F-synthetic 10% orig | ft10_sint | 0.5095 | 0.4935 a 0.5264 | 80.7% | 81.8% (80.6 a 83.0) |
| F-synthetic 10% fz | ft10_sint_fz | 0.3209 | 0.3054 a 0.3358 | 50.8% | 51.6% (49.9 a 53.2) |
| F-synthetic 10% lr | ft10_sint_lr | 0.3875 | 0.3724 a 0.4041 | 61.4% | 62.3% (60.7 a 64.0) |
| F-synthetic 10% fzlr | ft10_sint_fzlr | 0.2241 | 0.2119 a 0.2369 | 35.5% | 36.0% (34.5 a 37.7) |
| F-generic 10% orig | ft10_coco | 0.5709 | 0.5535 a 0.5883 | 90.5% | 91.7% (90.6 a 92.6) |
| F-generic 10% fz | ft10_coco_fz | 0.5772 | 0.5607 a 0.5942 | 91.5% | 92.7% (91.3 a 94.1) |
| F-generic 10% lr | ft10_coco_lr | 0.6224 | 0.6072 a 0.6396 | 98.6% | 100.0% (98.8 a 101.3) |
| F-generic 10% fzlr | ft10_coco_fzlr | 0.5644 | 0.5487 a 0.5815 | 89.4% | 90.7% (89.3 a 92.0) |
| F-synthetic 5% chosen | ft05_sint, ft05_sint_sd1, ft05_sint_sd2 | 0.4529 | 0.4373 a 0.4696 | 71.8% | 72.8% (71.2 a 74.0) |
| F-generic 5% chosen | ft05_coco_lr, ft05_coco_lr_sd1, ft05_coco_lr_sd2 | 0.5897 | 0.5748 a 0.6073 | 93.4% | 94.8% (93.6 a 95.9) |
| F-synthetic 10% chosen | ft10_sint | 0.5095 | 0.4935 a 0.5264 | 80.7% | 81.8% (80.6 a 83.0) |
| F-generic 10% chosen | ft10_coco_lr | 0.6224 | 0.6072 a 0.6396 | 98.6% | 100.0% (98.8 a 101.3) |
| R-sel | r_pareado_sel | 0.6224 | 0.6069 a 0.6397 | 98.6% | 100.0% (100.0 a 100.0) |
