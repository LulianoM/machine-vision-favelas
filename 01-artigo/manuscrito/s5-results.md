## Results

Every check is recorded on its criterion in Online Appendix, Table C0a; interpretation is left to Section 6.

### 5.1 Characterisation of the target: size, shape, contrast and crop similarity

**Size.** Halving the GSD from 9.76 to 4.88 cm per pixel took the median long side of the annotated box from 10.1 to 20.6 pixels and the share of instances whose shorter side fell below one stride of the detector from 66.9 to 0.8 per cent, compared with 30.5 per cent on VisDrone val (Online Appendix, Table C2a); a pilot detector trained on 40 such frames failed on its own selection split (mAP50 0.077, two classes; Online Appendix, Table C4). At 4.88 cm per pixel the median synthetic instance covered 301 square pixels and the median VisDrone instance, both splits pooled, 300, though the long sides differed (20.6 and 24.0 pixels).

**Shape.** The two nadir corpora agreed on the median height-to-width ratio (0.98), compared with 1.95 and 2.20 on the two VisDrone splits (Online Appendix, Table C2a). In S-oblique the ratio rose with pitch from 1.28 to 1.70 and reached the 1.95 of VisDrone only for figures carrying nothing at the steepest band (Online Appendix, Table C2); as rendered, S-oblique realised 1.46, and S-oblique-six, calibrated to 1.95, realised 1.85.

**Contrast.** Contrast with local clutter, measured on the pilot corpus, was highest under overcast (0.88) and lowest under rain and hard sun (0.63 and 0.64); with eight frames per regime and a between-frame dispersion of 0.12 to 0.38, only that gap approached one standard deviation (Online Appendix, Tables C3 and C3a).

**Crop similarity.** Figure @fig{fig7_armados} shows the crops the detector receives at the three GSDs. Without a detector the three classes separated weakly, less than the detector did (Online Appendix, Table C12 and Figure C4), and the clearest structure opposed figures carrying nothing to figures carrying anything. The AUC separating armed figures from objects rose as resolution coarsened, from 0.525 to 0.654, its interval excluding 0.5 at 2.44 and 4.88 cm per pixel, and a nearest-centroid rule reached a d′ of 0.23 to 0.46, below that of the detector on the same selection splits, the detector at 4.88 cm per pixel being the first Twin-150 model, which failed its validity condition.

<!--FIG:06-resultados/figuras/fig7_armados.jpg|Figures carrying a rifle, a pistol, nothing, a broom, a length of pipe or a closed umbrella at 1.14, 2.44 and 4.88 cm per pixel, scaled without smoothing to show the pixels the detector receives; carrying figures chosen by eye (Section 4.2.2).-->

### 5.2 Experiment A: zero-shot transfer to real imagery

On VisDrone, as means of three training runs, synthetic-only training recovered 2.2 per cent of the ceiling at the reference acquisition, 8.8 per cent with the same settlement rendered obliquely and 15.3 per cent for S-oblique-six; on HERIDAL the order of the two geometries reversed (Table @tab{obliquo}).

**Ceiling and nadir.** R reached mAP50 0.6311 (0.6149 to 0.6471) on VisDrone, mAP50-95 0.2538. Over three runs S-nadir-150 scored 0.0102 to 0.0198, a mean of 0.0136 (0.0120 to 0.0160) and a share of R of 2.2 per cent (1.9 to 2.5). Spreading the same 180 frames over six settlements gave 0.0190, +0.0054 (+0.0009 to +0.0066) above the three-run mean, a ratio of 1.40 (1.07 to 1.50), inside the nadir range.

**Scale-matched check.** At the scale-matched input of 1,024 pixels (Online Appendix B5), the first run of S-nadir-150 scored 0.0128 and R 0.5849, a share of R of 2.2 rather than 1.6 per cent: a change of about a third of the protocol share, below the half pre-specified as the sign of a scale confound.

**Oblique.** Moving the camera to a pitch of 26 to 52 degrees, with every other setting of the geometry check held, raised the VisDrone score on every seed. On the means of three runs per side the difference was +0.0419 (+0.0368 to +0.0470), a ratio of 4.08 (3.44 to 4.64); seed by seed the ratio was 6.01, 2.79 and 4.64 (Online Appendix C6). S-oblique-six, which changed settlements, pitch band, figures and camera placement together, reached a mean of 0.0966, +0.0411 (+0.0367 to +0.0462) above S-oblique, a ratio of 1.74 (1.64 to 1.85).

**Settlement seed.** Over three settlement seeds S-oblique-six scored 0.0821 to 0.1055, a mean of 0.0937, a range 1.4 times that over training seeds, below the pre-specified factor of two, and stayed above S-oblique by +0.0381 (+0.0334 to +0.0437; Online Appendix C6).

**HERIDAL.** On HERIDAL R scored 0.3185 (0.2843 to 0.3543) at 1,152 pixels, and the order of the two geometries reversed: S-nadir-150 reached 62.7 per cent of R and S-oblique 42.1 per cent, a difference of -0.0656 (-0.0840 to -0.0471) and a ratio of 0.67 (0.61 to 0.74), with the nadir runs spreading from 0.0926 to 0.2672.

**Number of frames.** Trained on nested subsets of its 152 frames, S-oblique-six rose from 0.0618 at 30 frames to 0.0966 at 152, +0.0349 (+0.0310 to +0.0392), and from 120 to 152 frames by +0.0062 (+0.0033 to +0.0088), 0.0140 per doubling of frames (Online Appendix, Table C8).

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:obliquo|Experiment A: zero-shot single-class mAP50 on VisDrone-DET val and HERIDAL, as the mean over runs where a model was trained three times, with 95 per cent intervals by resampling images and share of R (Section 4.7).-->

| Model | Runs | mAP50, own selection split | VisDrone mAP50 (95% interval) | Range over runs | Share of R (95% interval) | HERIDAL mAP50 at 1,152 (95% interval); range | Share of R on HERIDAL | HERIDAL mAP50 at 1,280 |
|---|---|---|---|---|---|---|---|---|
| R | 1 | not applicable | 0.6311 (0.6149 to 0.6471) | one run | ceiling | 0.3185 (0.2843 to 0.3543) | 100% | 0.3353 |
| S-nadir-150 | 3 | 0.79 to 0.81 | 0.0136 (0.0120 to 0.0160) | 0.0102 to 0.0198 | 2.2% (1.9 to 2.5) | 0.1997 (0.1713 to 0.2306); 0.0926 to 0.2672 | 62.7% | 0.1682 |
| S-nadir-150-six | 1 | 0.6786 | 0.0190 (0.0142 to 0.0211) | one run | 3.0% (2.3 to 3.3) | 0.2488 (0.2116 to 0.2865) | 78.1% | 0.2208 |
| S-oblique | 3 | 0.74 to 0.76 | 0.0555 (0.0502 to 0.0614) | 0.0501 to 0.0614 | 8.8% (8.1 to 9.6) | 0.1341 (0.1149 to 0.1555); 0.1092 to 0.1476 | 42.1% | 0.1422 |
| S-oblique-six | 3 | 0.7047, first run | 0.0966 (0.0896 to 0.1048) | 0.0887 to 0.1055 | 15.3% (14.4 to 16.5) | 0.1477 (0.1265 to 0.1715); 0.1079 to 0.1847 | 46.4% | 0.1418 |
| S-oblique-six, three settlement seeds | 3 | not reported | 0.0937 (0.0868 to 0.1019) | 0.0821 to 0.1055 | 14.8% (13.9 to 16.0) | not reported | not reported | not reported |

</div>

### 5.3 Experiment B: synthetic pretraining and joint training compared with a generic start

Given 5 or 10 per cent of real images (Online Appendix, Figure C2; values per seed and per schedule in Tables C9 and C9a, precision-recall curves in Figure C1), the generic start finished above the synthetic start on the original schedule, at 5 per cent on every seed, by +0.0716 (+0.0658 to +0.0780) on the means, a ratio of 1.16 (1.14 to 1.17), and at 10 per cent by +0.0614 (+0.0553 to +0.0679). Contrary to the pre-specified expectation, the deficit was largest at the smaller volume. The joint models finished below the generic start by 0.0637 (0.0562 to 0.0700) at 5 per cent and 0.0281 (0.0214 to 0.0346) at 10, and above the synthetic start by 0.0078 (0.0025 to 0.0147), inside the synthetic seed range, and by 0.0333 (0.0276 to 0.0399).

Freezing the backbone, lowering the learning rate or both lowered the synthetic start in every cell (0.2028 to 0.3875), while the lower rate raised the generic start at both volumes. Each start on the schedule its selection slice preferred, the generic start finished above by +0.1369 (+0.1290 to +0.1465) at 5 per cent on three seeds each, and by +0.1129 (+0.1044 to +0.1230) at 10, one run per side; under every schedule and at both volumes the interval excluded zero.

### 5.4 Experiment C: the armed and unarmed distinction by GSD

**2.44 cm per pixel.** On the 50 held-out frames of the unseen-weapon test, in a new realisation of the settlement, S-nadir-75 called 0.434 (0.381 to 0.496) of armed figures, 0.152 (0.113 to 0.196) of objects and 0.068 (0.035 to 0.102) of unarmed persons armed, with an armed precision of 0.430 and a d′ (armed versus object) of 0.85 (0.64 to 1.09); every rate was lower than on its selection split. Recall was 0.400 on the five training firearms (50 of 125) and 0.466 on the two unseen ones (61 of 131), a ratio of 1.16 (approximate 95 per cent interval 0.88 to 1.54; Online Appendix, Table C13). The closed umbrella, 0.88 m, was the object most often called armed (0.38, 29 instances). In the carried-as-weapon re-render S-nadir-75 called 0.154 of the 227 paired objects armed as normally carried and 0.137 when carried in the poses and at the angles of the weapons (exact McNemar test, p = 0.56, unadjusted for clustering by frame); the umbrella, whose carriage did not change, stayed at 0.38.

**1.14 compared with 2.44 cm per pixel.** With every other setting held, S-nadir-35 called more objects armed than Twin-75 (Table @tab{armado}): by +0.108 (+0.015 to +0.211) on the selection split, and on the 80 held-out frames 0.253 compared with 0.125, +0.128 (+0.071 to +0.194; p = 0.0001, unadjusted for clustering by frame). Over three training seeds the means differed by +0.068 (+0.002 to +0.142) on the selection split, with overlapping ranges, and by +0.087 (+0.044 to +0.136) on the held-out frames, with separate ranges (Online Appendix, Table C10). The armed and unarmed rates were not resolvable on the means of three training seeds, the armed difference reversing in seed 2, and nor was the comparison with the original 75 m model (Online Appendix, Tables C0a and C10). On the held-out frames, where 31 to 36 per cent of annotated figures were armed by construction, between 0.37 and 0.43 of the detections that S-nadir-75, S-nadir-35 and Twin-75 labelled armed at the default threshold were armed figures.

**4.88 cm per pixel.** The first Twin-150 found 0.498 of the 297 annotated figures on its selection split, below the pre-specified half. Trained for longer as pre-specified (Section 4.6), it found 0.606 there and 0.663 of 916 on its 80 held-out frames. On the held-out frames its d′ (armed versus object) was 0.58 (0.38 to 0.78), an interval that excludes zero. On the same frame indices as Twin-75, d′ at 4.88 cm per pixel was lower by 0.394 (0.098 to 0.681) and the object rate higher by 0.120 (0.058 to 0.181). Figures carrying the 0.20 m pistol were called armed at 0.50 (17 of 34), within the range of the long arms (0.41 to 0.50).

**Threshold sweep.** Over the 14 combinations of model, training seed and set (Online Appendix, Table C11), the F1-maximising threshold lay between 0.30 and 0.50, raising armed precision from 0.37 to 0.46 to 0.47 to 0.66 at a cost of 0.01 to 0.08 of armed recall in 13 of them; no model exceeded an armed recall of 0.65 at any threshold, and at an object rate of 0.10 or below the highest armed recall was 0.420, for Twin-75 with training seed 2 on the held-out frames (armed precision 0.614), and 0.381 or below in every other combination (Online Appendix, Figure C3).

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:armado|Experiment C at confidence 0.25 (Section 4.7), first training run, on each selection split and on the 80 held-out frames of the matched corpora; 95 per cent intervals by resampling frames. Differences: model under test minus Twin-75.-->

| Model (GSD, cm/px) | Figures found | Armed called armed (95% interval) | Object called armed (95% interval) | Unarmed called armed (95% interval) | Armed precision | d′ vs object (95% interval) | mAP50, three classes |
|---|---|---|---|---|---|---|---|
| **Selection split** | | | | | | | |
| S-nadir-75 (2.44) | not reported | 0.547 (0.476 to 0.627) | 0.237 (0.183 to 0.289) | 0.131 (0.073 to 0.188) | 0.386 | 0.83 (0.54 to 1.13) | 0.579 |
| S-nadir-35 (1.14) | not reported | 0.569 (0.492 to 0.646) | 0.273 (0.202 to 0.353) | 0.168 (0.101 to 0.235) | 0.415 | 0.77 (0.46 to 1.10) | 0.514 |
| Twin-75 (2.44) | not reported | 0.471 (0.397 to 0.558) | 0.165 (0.100 to 0.230) | 0.109 (0.044 to 0.174) | 0.440 | 0.89 (0.58 to 1.32) | 0.508 |
| Twin-150 (4.88) | 0.606 | 0.435 | 0.178 (0.107 to 0.247) | 0.135 | not reported | 0.75 (0.33 to 1.26) | 0.388 |
| S-nadir-35 minus Twin-75 | | +0.099 (-0.022 to +0.217) | +0.108 (+0.015 to +0.211) | +0.059 (-0.038 to +0.154) | | | |
| **Held-out frames, matched indices** | | | | | | | |
| S-nadir-35 (1.14) | 0.684 | 0.543 | 0.253 (0.204 to 0.303) | 0.156 | 0.408 | 0.77 (0.57 to 0.99) | not reported |
| Twin-75 (2.44) | 0.766 | 0.432 | 0.125 (0.081 to 0.167) | 0.140 | 0.370 | 0.97 (0.77 to 1.20) | not reported |
| Twin-150 (4.88) | 0.663 | 0.457 | 0.245 (0.204 to 0.289) | 0.205 | not reported | 0.58 (0.38 to 0.78) | not reported |
| S-nadir-35 minus Twin-75 | | +0.112 (+0.031 to +0.192) | +0.128 (+0.071 to +0.194) | +0.015 (-0.040 to +0.073) | | | |
| Twin-150 minus Twin-75 | | | +0.120 (+0.058 to +0.181) | | | -0.394 (-0.681 to -0.098) | |

</div>

### 5.5 Experiment D: performance by illumination regime

Hard sun was the weakest regime for S-nadir-150 on synthetic frames, with an mAP50 of 0.675 and a recall of 0.657, compared with 0.791 and 0.796 under overcast. The specialist trained under hard sun alone gained recall there (D-i: +0.0818) and was no longer resolvably below the model of all regimes under overcast (D-ii: -0.0572, -0.1252 to +0.0067, an interval that includes zero), but fell below it in recall under the other five regimes, most under haze (0.569 compared with 0.726), while its mAP50 was level or higher under low sun, overcast and heavy overcast (Online Appendix, Tables C3 and C3a).

### 5.6 Robustness checks and headline comparisons

Neither the official toolkit rule for ignored regions nor stricter IoU thresholds (0.60 and 0.75) changed the order of any pair fixed for these checks; two other comparisons reversed at stricter thresholds (Online Appendix, Table C1). Table @tab{hipoteses} gives the outcome of the six headline comparisons and the readings of Section 4.7 each passes.

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:hipoteses|The six headline comparisons: research question, status (Section 4.6), outcome and the readings of Section 4.7 the difference passes, (a) seed ranges, (b) paired interval, (c) 30 per cent; n.a.: not applicable. Every hypothesis, H1 to H23: Online Appendix, Tables C0 and C0a.-->

| ID | RQ | Comparison | Status | Outcome | Resolvable (a / b / c) |
|---|---|---|---|---|---|
| H3 | RQ1 | Camera geometry: S-oblique against S-nadir-150 on VisDrone | Confirmatory | held: +0.0419, ratio 4.08 | yes / yes / yes, 307.9% |
| H4 | RQ1 | The same pair on HERIDAL | Confirmatory | held, order reversed: -0.0656, ratio 0.67; same order at 1,280 | no, ranges overlap / yes / yes, 48.9% |
| H13 | RQ2 | Cost of the synthetic start, each start on its chosen schedule | Pre-specified follow-up | held: F-synthetic lower by 0.1369 at 5% and 0.1129 at 10% | 5%: yes / yes / yes, 30.2%; 10%: n.a. / yes / no, 22.2% |
| H19 | RQ3 | Separation of armed figures and objects at 4.88 cm per pixel | Confirmatory | separation above chance, d′ 0.58 (0.38 to 0.78); read under its criterion in Section 6.1 | n.a. / yes, excludes zero / n.a. |
| H20 | RQ3 | 4.88 against 2.44 cm per pixel, matched held-out frames | Confirmatory | d′ lower by 0.394, object rate higher by 0.120 | n.a. / yes / yes, 68.0% and 96.2% |
| H21a | RQ3 | Object rate, 1.14 against 2.44 cm per pixel, held-out frames | Confirmatory | held: +0.128, p = 0.0001 (unadjusted for clustering by frame); +0.087 on seed means | yes / yes / yes, 64.9% |

</div>
