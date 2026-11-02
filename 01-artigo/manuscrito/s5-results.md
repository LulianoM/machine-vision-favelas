## Results

Section 5.1 reports the model-free characterisation of the target, Sections 5.2 to 5.5 report Experiments A to D in the order of the research questions, and Section 5.6 applies the criteria of Sections 4.6 and 4.7 to every pre-specified check. Table @tab{visao} collects every model with its test set and headline figure; what the observations mean for RQ1 to RQ3 is left to Section 6.

One result per question. For RQ1, trained on synthetic imagery alone, the detector recovered 2.2, 8.8 and 15.3 per cent of the ceiling on the urban benchmark, as means of three training runs, at the nadir geometry, at the oblique geometry of the same settlement and in the best oblique configuration; on the nadir benchmark the order reversed, 62.7 per cent of the ceiling for the nadir model against 42.1 and 46.4 for the two oblique models, with ranges over training runs that overlap (Section 5.2). For RQ2, the synthetic start brought no gain once 5 or 10 per cent of the real training images were available: 0.4424 against 0.5220 for the generic start at 5 per cent and 0.5095 against 0.5709 at 10, on the original schedule (Section 5.3). For RQ3, the three-class detectors called a confusable object armed in 25.3, 12.5 and 24.5 per cent of cases at 1.14, 2.44 and 4.88 cm per pixel on the held-out frames, from the first training run of each model, so that the rate was lowest at the middle GSD (Section 5.4).

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:visao|Results at a glance: mAP50 on VisDrone-DET val with 95 per cent intervals by resampling the 548 test images, and efficacy against R on the same resamples; where a model was trained three times, the mean of the three runs with its interval, and the best run. The last single-class rows give the nadir benchmark, HERIDAL, at the matched input size. Three-class models carry their three-class mAP50 and the object rate at confidence 0.25 on their selection split and on held-out frames rendered after training.-->

| Model | Training data (real images) | Test set | mAP50 (95% interval) | Efficacy (95% interval) |
|---|---|---|---|---|
| R | 1,106 images of VisDrone-DET train (1,106) | VisDrone-DET val | 0.6311 (0.6149 to 0.6471) | ceiling |
| S-nadir-150, mean of 3 seeds (best run) | 180 frames, 1 settlement, nadir, 4.88 cm/px (0) | VisDrone-DET val | 0.0136 (0.0120 to 0.0160); best 0.0198 | 2.2% (1.9 to 2.5); best 3.1% |
| S-nadir-150-six | 180 frames, 6 settlements, nadir, 4.88 cm/px (0) | VisDrone-DET val | 0.0190 (0.0142 to 0.0211) | 3.0% (2.3 to 3.3) |
| S-oblique, mean of 3 seeds (best run) | 180 frames, 1 settlement, oblique, 3.90 cm/px nominal (0) | VisDrone-DET val | 0.0555 (0.0502 to 0.0614); best 0.0614 | 8.8% (8.1 to 9.6); best 9.7% |
| S-oblique-six, mean of 3 seeds (best run) | 180 frames, 6 settlements, pitch 45 to 56 degrees (0) | VisDrone-DET val | 0.0966 (0.0896 to 0.1048); best 0.1055 | 15.3% (14.4 to 16.5); best 16.7% |
| F-synthetic, 5 and 10%, first training seed (the three seeds at 5% are in Table @tab{ajuste}) | from S-oblique-six (324 and 647) | VisDrone-DET val | 0.4424 (0.4260 to 0.4587); 0.5095 (0.4935 to 0.5264) | 70.1% (68.4 to 71.8); 80.7% (79.3 to 82.1) |
| F-generic, 5 and 10%, first training seed (the three seeds at 5% are in Table @tab{ajuste}) | from COCO weights (324 and 647) | VisDrone-DET val | 0.5220 (0.5045 to 0.5403); 0.5709 (0.5535 to 0.5883) | 82.7% (81.4 to 84.1); 90.5% (89.2 to 91.6) |
| F-generic, lower learning rate (chosen on the selection slice), 5 and 10% | from COCO weights (324 and 647) | VisDrone-DET val | 0.5897 (0.5748 to 0.6073), mean of 3 seeds; 0.6224 (0.6072 to 0.6396) | 93.4% (92.3 to 94.8); 98.6% (97.4 to 100.1) |
| F-joint, 5 and 10% | COCO weights, 890 synthetic tiles and the real images (324 and 647) | VisDrone-DET val | 0.4607 (0.4444 to 0.4789); 0.5428 (0.5259 to 0.5610) | 73.0% (71.6 to 74.6); 86.0% (84.8 to 87.4) |
| R on the nadir benchmark | as above (1,106) | HERIDAL, 1,647 images | 0.3185 (0.2843 to 0.3543) | ceiling |
| S-nadir-150 on the nadir benchmark, mean of 3 seeds | as above (0) | HERIDAL | 0.1997 (0.1713 to 0.2306) | 62.7% |
| S-oblique on the nadir benchmark, mean of 3 seeds | as above (0) | HERIDAL | 0.1341 (0.1149 to 0.1555) | 42.1% |
| S-nadir-75 | 200 frames, 3 classes, 2.44 cm/px (0) | selection split, 27 frames; held-out, 50 | 0.579; object rate 0.237; held-out 0.152 | not applicable |
| S-nadir-35 | 200 frames, 3 classes, 1.14 cm/px (0) | selection split, 35; held-out, 80 | 0.514; object rate 0.273; held-out 0.253 | not applicable |
| Twin of S-nadir-35 at 75 m | the 35 m corpus at 2.44 cm/px (0) | selection split, 24; held-out, 80 | 0.508; object rate 0.165; held-out 0.125 | not applicable |
| Twin of S-nadir-35 at 150 m, trained for longer | the 35 m corpus at 4.88 cm/px (0) | selection split, 27; held-out, 80 | 0.388; object rate 0.178; held-out 0.245 | not applicable |

</div>

### 5.1 Characterisation of the target: size, shape and contrast

Measured on the annotations and the rendered pixels alone, GSD set the size of the target, camera pitch set its shape, the illumination regime moved its contrast against local clutter, and the crops of the three classes separated only weakly under a frozen generic extractor at each of the three GSDs, less than under the detector.

**Size.** Table @tab{gsd} gives the size of the annotated box by GSD.

<!--TAB:gsd|Target size by GSD: median long side of the annotated box and the share of instances whose shorter side falls below one stride of the detector (8 pixels), at native resolution, on the training split of the pilot corpus, both splits of the corpus of record and the validation split of the benchmark.-->

| Corpus | Altitude, GSD (cm/px) | Render | Median long side | Shorter side below 8 px |
|---|---|---|---|---|
| Pilot corpus | nadir 150 m, 9.76 | 1920 by 1080 | 10.1 px | 66.9% |
| Corpus of record | nadir 150 m, 4.88 | 3840 by 2160 | 20.6 px | 0.8% |
| VisDrone-DET val | not recorded | mixed, 408 of 548 at 1360 by 765 | 25.0 px | 30.5% |

Halving the GSD from 9.76 to 4.88 cm per pixel took the median long side from 10.1 to 20.6 pixels and the share of instances below one stride on the shorter side from 66.9 to 0.8 per cent, against 30.5 per cent in the benchmark. In area the median synthetic instance at 4.88 cm per pixel covered 301 square pixels and the median benchmark instance, training and validation splits pooled, 300, a ratio of 1.00; on the long side the two differed, 20.6 against 24.0 pixels over the pooled splits and 25.0 on the validation split. At 2.44 cm per pixel (75 m) the median instance measured 47.6 by 41.7 pixels, 6.4 times the area at 4.88 over all classes and 5.2 times for armed figures; at 1.14 (35 m) it measured 121.8 by 103.1 pixels. These sizes are at native resolution, before the resizing of Section 4.5.

**Shape.** Table @tab{forma} gives the height-to-width ratio of the same annotation sets, and Table @tab{pitch} splits the S-oblique corpus by the pitch recorded per image.

<!--TAB:forma|Apparent shape of the target: median box dimensions and height-to-width ratio by corpus and camera geometry, from the full-frame labels. The nadir rows carry the generator setting (within 3.5 degrees of vertical); the oblique rows record pitch per image; the benchmark records no acquisition geometry.-->

| Corpus and geometry | Altitude, GSD (cm/px) | Median width | Median height | Median h/w | Instances |
|---|---|---|---|---|---|
| Pilot corpus, nadir | 150 m, 9.76 | 8.3 px | 8.2 px | **0.98** | 565 |
| Corpus of record, nadir | 150 m, 4.88 | 17.6 px | 17.5 px | **0.98** | 3,225 |
| S-oblique, pitch 26 to 52 degrees, one settlement | 120 m, 3.90 nominal | 17.9 px | 26.4 px | **1.46** | 1,912 |
| S-oblique-six, pitch 45 to 56 degrees, six settlements, figures carrying nothing | 120 m, 3.90 nominal | 13.3 px | 25.2 px | **1.85** | 1,521 |
| VisDrone-DET train, real acquisition | not recorded | 13.0 px | 24.0 px | **1.95** | 106,396 |
| VisDrone-DET val, real acquisition | not recorded | 12.0 px | 25.0 px | **2.20** | 13,969 |

<!--TAB:pitch|Height-to-width ratio of the annotated box by camera pitch in the S-oblique corpus (120 m, 3.90 cm per pixel nominal), from the full-frame labels.-->

| Pitch recorded per image | Instances | Median h/w, all figures | Median h/w, figures carrying nothing |
|---|---|---|---|
| 26 to 30 degrees | 482 | 1.28 | 1.35 |
| 30 to 35 degrees | 512 | 1.41 | 1.50 |
| 35 to 40 degrees | 231 | 1.49 | 1.58 |
| 40 to 45 degrees | 359 | 1.64 | 1.82 |
| 45 to 50 degrees | 222 | 1.64 | 1.78 |
| 50 to 52 degrees | 106 | 1.70 | 1.97 |

The two nadir corpora, which differ by a factor of 2 in render resolution and of 6 in instance count, agreed on the ratio to the second decimal, against 1.95 and 2.20 on the two benchmark splits. In the oblique corpus the ratio rose with pitch from 1.28 to 1.70, not strictly between 40 and 50 degrees, and for figures carrying nothing it reached the 1.95 of the benchmark's training split only between 50 and 52 degrees, where it measured 1.97 on 49 figures. S-oblique as rendered realised 1.46 rather than the 1.95 it was calibrated for, its armed figures measuring 1.38 against 1.58 for figures carrying nothing; S-oblique-six realised 1.85 at 13.3 by 25.2 pixels.

**Contrast.** Table @tab{contraste} gives figure-to-background contrast by illumination regime.

<!--TAB:contraste|Figure-to-background contrast by illumination regime in the pilot corpus (nadir, 150 m, 9.76 cm per pixel): mean frame luminance, raw luminance difference in digital numbers (DN), contrast against local clutter aggregated per frame, and its dispersion between frames (standard deviation, SD); 684 instances over 48 frames, 8 per regime.-->

| Regime | Mean frame luminance | Raw difference (DN) | Contrast over clutter, median per frame | SD between frames | Instances |
|---|---|---|---|---|---|
| Hard sun | 87.0 | 15.2 | **0.64** | 0.14 | 113 |
| Low sun | 56.0 | 9.0 | 0.70 | 0.20 | 117 |
| Overcast | 84.6 | **16.4** | **0.88** | 0.26 | 122 |
| Haze | 94.4 | 9.6 | 0.79 | 0.25 | 113 |
| Heavy overcast | 55.6 | 11.2 | 0.72 | 0.38 | 91 |
| Rain | 35.1 | 6.6 | **0.63** | 0.12 | 128 |

Overcast gave both the largest raw difference and the largest contrast over clutter; hard sun and rain were the two lowest on the latter, and hard sun reached that while sitting second on raw contrast. With 8 frames per regime and a between-frame dispersion of 0.12 to 0.38, only the gap between the extremes, rain and hard sun at 0.63 and 0.64 against overcast at 0.88, approached one standard deviation; the ordering of the four intermediate regimes was not resolvable at this sample size. Figure @fig{fig7_armados} shows what the detector receives at the three GSDs of Experiment C.

<!--FIG:06-resultados/figuras/fig7_armados.jpg|Figures carrying a rifle, a pistol, nothing, a broom, a length of pipe or a closed umbrella at 1.14, 2.44 and 4.88 cm per pixel (35, 75 and 150 m). Each is cropped from a rendered frame of the 35 m corpus, its twins or their held-out frames and scaled to the same size without smoothing, so that every crop shows the pixels the detector receives. The carrying figures were chosen by eye, under clear light, as ones whose item sits in the hand close to the horizontal; in many frames the item points steeply downward or does not sit in the grip (Section 4.2.2).-->

**Crop similarity.** Under the protocol of Section 4.4, the co-similarity matrices of the three classes were flat at every GSD (Figure @fig{fig13_similaridade}, Table @tab{similaridade}). After centring, every entry lay between -0.030 and +0.032 (between 0.71 and 0.79 before centring); the largest entry was 0.025, 0.026, 0.032 and 0.020 at 35 m, the twin at 75 m, the twin at 150 m and the original 75 m corpus, and the silhouette of the three classes was 0.002, 0.007, 0.002 and 0.006. The one structure present opposed the unarmed class to the two carrying classes. The largest negative entries sat on the unarmed-against-object pair at every GSD (-0.017 to -0.030), and the centroid cosines were -0.75, -0.85, -0.86 and -0.69 for that pair against +0.15, -0.03, -0.55 and +0.13 for armed against object. The silhouette of the armed class was negative at all four GSDs.

<!--FIG:06-resultados/figuras/fig13_similaridade.png|Crop similarity without a detector at 1.14, 2.44 and 4.88 cm per pixel (35 m, the twin at 75 m, the twin at 150 m). Top: the evaluation pool of each corpus on its first two principal components (18 to 20 per cent of the variance), class centroids as large markers, silhouette of the three classes printed. Bottom: mean pairwise cosine similarity of the centred features between and within classes, common scale from -0.04 to +0.04.-->

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:similaridade|Separation of the three classes in the frozen generic feature space by GSD (Section 4.4). Columns: median annotated box in the evaluation pool; nearest-centroid classification under 5-fold cross-validation, with the detector's d′ on the corpus's selection split in parentheses (at 4.88 cm per pixel, that of the first model at 150 m, which failed its validity condition; Section 5.4) and 95 per cent intervals by resampling frames; every d′ in this table is without the log-linear correction of Section 4.7, as Section 4.4 specifies, and with it the detector's values at 1.14 and 2.44 cm per pixel are 0.77 and 0.89 rather than 0.78 and 0.90 (Table @tab{armado}); AUC of armed against object; accuracy after PCA to 2 and 10 dimensions and after LDA to 2 dimensions. Chance: 0.33 for accuracy, 0.50 for AUC.-->

| Corpus (GSD, cm/px) | Crops: armed / unarmed / object | Median box (px) | Accuracy, 3 classes | Object called armed (95% interval) | Armed recall | d′ (detector), uncorrected | AUC armed vs object (95% interval) | Accuracy, PCA 2 / PCA 10 / LDA 2 |
|---|---|---|---|---|---|---|---|---|
| S-nadir-35 (1.14) | 483 / 434 / 413 | 124 by 105 | 0.507 | 0.332 (0.285 to 0.375) | 0.420 | 0.23 (0.78; 0.77 corrected) | 0.525 (0.483 to 0.561) | 0.384 / 0.495 / 0.547 |
| Twin at 75 m (2.44) | 342 / 384 / 379 | 48 by 41 | 0.531 | 0.253 (0.207 to 0.297) | 0.377 | 0.35 (0.90; 0.89 corrected) | 0.576 (0.531 to 0.622) | 0.399 / 0.525 / 0.586 |
| Twin at 150 m (4.88) | 92 / 104 / 101 | 21 by 20 | 0.492 | 0.208 (0.131 to 0.287) | 0.359 | 0.45 (0.67) | 0.654 (0.574 to 0.730) | 0.428 / 0.471 / 0.502 |
| S-nadir-75, original (2.44) | 117 / 153 / 135 | 45 by 41 | 0.558 | 0.267 (0.187 to 0.360) | 0.436 | 0.46 (0.83) | 0.534 (0.459 to 0.615) | 0.348 / 0.526 / 0.514 |

</div>

The AUC of armed against object was higher at the coarser GSDs on point estimates, with intervals that overlap between neighbouring GSDs, the highest value, at 4.88 cm per pixel, resting on 92 against 101 crops with the widest interval. A nearest-centroid rule called 0.208 to 0.332 of objects armed and recognised 0.359 to 0.436 of armed figures, a d′ of 0.23 to 0.46 against 0.67 to 0.90 for the detector on the selection splits (the 0.67 at 4.88 cm per pixel being that of the first model at 150 m, which failed its validity condition), both computed without the log-linear correction, as in Section 4.4; with the correction the detector's values at 1.14 and 2.44 cm per pixel are 0.77 and 0.89 rather than 0.78 and 0.90 (Table @tab{armado}). The 5-nearest-neighbour rule, the two shallower feature maps (AUC 0.485 to 0.572 under the nearest-centroid rule) and folds drawn by frame gave the same picture. Fitted on the training split and applied to the detector's own pools, the rule called 0.331 (0.254 to 0.408) of objects armed on the 35 m selection split against the detector's 0.273, and 0.288 (0.237 to 0.343) on the 35 m held-out frames against 0.253. On the twin it called 0.231 (0.151 to 0.316) on the selection split against 0.165 and 0.292 (0.234 to 0.351) on the held-out frames against 0.125, with armed recall of 0.39 to 0.50 across the four pools against the detector's 0.43 to 0.57. Two principal components kept 0.18 to 0.20 of the variance and lowered accuracy to 0.348 to 0.428; 10 components kept 0.50 to 0.55 and matched the full space; the Fisher projection gave the highest accuracy without a detector, 0.502 to 0.586, with a d′ of 0.18 to 0.53. The supplement with the backbone of each trained detector, which is not model-free, gave AUC of 0.547, 0.502, 0.574 and 0.494.

### 5.2 Experiment A: zero-shot transfer to real imagery

Trained on synthetic imagery alone, the detector recovered on the urban benchmark, as means of three training runs, 2.2 per cent of the ceiling at the nadir geometry of the reference acquisition, 8.8 per cent when the same settlement was rendered obliquely and 15.3 per cent for the best oblique configuration; on the nadir benchmark the order of the two geometries reversed.

**Pilot.** The pilot of the protocol, an exploratory run on 40 training frames at 9.76 cm per pixel with the earlier recipe of Section 4.5, failed on its own domain (Table @tab{piloto}): 0.077 on its own validation split, a two-class mean not on the single-class scale of the rows that follow, against 0.7915 for the corpus of record.

<!--TAB:piloto|The pilot of the protocol: a two-class model trained on 40 frames rendered at 1920 by 1080 (9.76 cm per pixel), scored on its own validation split and zero-shot on the benchmark.-->

| Pilot run | Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| Pilot model (nadir, 150 m), 40 training frames at 1080p | synthetic validation split | 0.109 | 0.148 | 0.077 | 0.019 |
| same model | VisDrone-DET val, zero-shot | 0.038 | 0.031 | 0.0055 | 0.0020 |

**Ceiling.** R reached mAP50 0.6311 on the test set (Table @tab{teto}); its checkpoint was selected on that same split (Section 4.5), at epoch 58 of 60, without early stopping. A run on the full training split was started and stopped before completion.

<!--TAB:teto|The ceiling: R, trained on 1,106 real images of VisDrone-DET train, on VisDrone-DET val, with the 95 per cent interval by resampling images. Precision and recall at the F1-maximising confidence.-->

| Model | Precision | Recall | mAP50 (95% interval) | mAP50-95 |
|---|---|---|---|---|
| R (1,106 real training images; checkpoint selected on the test split) | 0.7312 | 0.5729 | 0.6311 (0.6149 to 0.6471) | 0.2538 |

**Nadir.** S-nadir-150 scored 0.7915 on its own validation split (its selection split, Section 4.5) and 0.0102 on the benchmark with its first training seed (Table @tab{nadir}), an efficacy of 1.6 per cent (1.4 to 2.1). Its two further seeds scored 0.0198 and 0.0108 (0.794 and 0.810 on the validation split), a mean over three runs of 0.0136 (0.0120 to 0.0160) and an efficacy of 2.2 per cent (1.9 to 2.5), 3.1 per cent for the best run.

<!--TAB:nadir|S-nadir-150 (nadir, 150 m, 4.88 cm per pixel), first training seed, on its own validation split and zero-shot on the real test set, with the 95 per cent interval by resampling images.-->

| Evaluation set | Precision | Recall | mAP50 (95% interval) | mAP50-95 |
|---|---|---|---|---|
| Synthetic validation split (ceiling of the corpus) | 0.8707 | 0.7413 | 0.7915 | 0.3656 |
| VisDrone-DET val, zero-shot | 0.0856 | 0.0421 | 0.0102 (0.0087 to 0.0133) | 0.0025 |

In the scale-matched check (Section 4.6), the median long side of the benchmark's person boxes reached the network at 25.33 pixels at the protocol's input size of 1,280 and at 20.27 pixels at 1,024, the closest a multiple of 32 comes to the 20.55 of the corpus of record, while the median area fell from 283 to 181 square pixels. At 1,024 pixels the first run of S-nadir-150 scored 0.0128 and R 0.5849, an efficacy of 2.2 rather than 1.6 per cent; the difference, 0.0026 on 0.0102, is a quarter of the protocol figure, against the half fixed in advance.

**Settlement variety.** Spreading the same 180 frames over six settlements raised the benchmark score from 0.0102 to 0.0190 and lowered the score on the model's own validation split (Table @tab{variedade}). Against the first nadir run the paired difference was +0.0088 (+0.0038 to +0.0102), a ratio of 1.866 (1.308 to 2.071) and a relative difference of 86.6 per cent of the smaller value. Against the mean of the three nadir runs it was +0.0054 (+0.0009 to +0.0066), a ratio of 1.40 (1.07 to 1.50) and 39.9 per cent, and the six-settlement value, from one run, lay inside the range of the three nadir runs (0.0102 to 0.0198).

<!--TAB:variedade|One settlement against six at a fixed 180 frames, nadir at 150 m (4.88 cm per pixel), on the synthetic validation split and on the real test set.-->

| Model | Synthetic validation mAP50 | VisDrone-DET val mAP50 (95% interval) | mAP50-95 | Efficacy (95% interval) |
|---|---|---|---|---|
| S-nadir-150, one settlement | 0.7915 | 0.0102 (0.0087 to 0.0133) | 0.0025 | 1.6% (1.4 to 2.1) |
| S-nadir-150-six, six settlements | 0.6786 | 0.0190 (0.0142 to 0.0211) | 0.0071 | 3.0% (2.3 to 3.3) |

**Oblique.** With every setting of the geometry check of Section 4.6 held and the camera moved to a pitch of 26 to 52 degrees, the benchmark score rose from 0.0102 to 0.0614 on the first training seed of each model (Table @tab{obliquo}), a paired difference of +0.0511 (+0.0447 to +0.0567) and a ratio of 6.011 (4.571 to 7.011). The two further seeds of S-oblique scored 0.0552 and 0.0501 (0.764 and 0.736 on its validation split), a mean of 0.0555 (0.0502 to 0.0614) and an efficacy of 8.8 per cent (8.1 to 9.6). On the means of three runs per side the paired difference was +0.0419 (+0.0368 to +0.0470), a ratio of 4.08 (3.44 to 4.64) and a relative difference of 307.9 per cent, and the ranges of the two models, 0.0501 to 0.0614 and 0.0102 to 0.0198, did not overlap; for seeds 1 and 2 alone the ratio was 2.79 and 4.64. In the same comparison the median height-to-width ratio moved from 0.98 to 1.46 and the median area from 301 to 456 square pixels, with the oblique GSD at the centre of the frame between about 4.3 and 6.3 cm per pixel across the pitch range. S-oblique-six, which changed the settlements, the pitch band, the figures and the camera placement together, scored 0.1055 on its first run (precision 0.2631, recall 0.1716, mAP50-95 0.0329; 0.7047 on its own validation split), 0.0958 and 0.0887 on two further training seeds, a mean of 0.0966 and an efficacy of 15.3 per cent over the three runs. Against S-oblique the paired difference was +0.0441 (+0.0383 to +0.0514) between first runs and, on the means of three runs per side, +0.0411 (+0.0367 to +0.0462), a ratio of 1.74 (1.64 to 1.85) and 74.0 per cent, with ranges that did not overlap. Under the official toolkit rule for ignored regions (Section 4.7) every mAP50 of this experiment rose slightly, R to 0.6548 and the first run of S-oblique-six to 0.1074, every efficacy fell slightly, that of S-oblique-six from 16.7 to 16.4 per cent, and no comparison between these models, the further seeds included, changed order at IoU 0.50, 0.60 or 0.75.

**Settlement seed.** Rendered with settlement seeds 22 and 23 instead of 21 and trained with seed 0, S-oblique-six scored 0.0935 and 0.0821 against 0.1055 (Table @tab{obliquo}), a mean of 0.0937 (0.0868 to 0.1019) and an efficacy of 14.8 per cent. The range over settlement seeds, 0.0234 wide, was 1.4 times the range over training seeds (0.0887 to 0.1055, 0.0168 wide), below the factor of 2 fixed in advance (Section 4.6) as the sign that the scene dominates the dispersion. Over the three settlement seeds six settlements stayed above one settlement over its three training seeds by +0.0381 (+0.0334 to +0.0437), 68.7 per cent, with ranges that did not overlap.

<!--TAB:obliquo|Nadir against oblique acquisition on the real test set, each model for each of its three training seeds and as the mean of the three, S-oblique-six also for two further settlement seeds (training seed 0), with 95 per cent intervals by resampling images.-->

| Model | mAP50 on VisDrone-DET val (95% interval) | Efficacy (95% interval) |
|---|---|---|
| S-nadir-150 (4.88 cm/px), seed 0 | 0.0102 (0.0087 to 0.0133) | 1.6% (1.4 to 2.1) |
| S-nadir-150, seed 1 | 0.0198 (0.0172 to 0.0232) | 3.1% (2.7 to 3.7) |
| S-nadir-150, seed 2 | 0.0108 (0.0090 to 0.0128) | 1.7% (1.4 to 2.0) |
| S-nadir-150, mean of 3 seeds | 0.0136 (0.0120 to 0.0160) | 2.2% (1.9 to 2.5) |
| S-oblique (3.90 cm/px nominal), seed 0 | 0.0614 (0.0554 to 0.0673) | 9.7% (8.9 to 10.6) |
| S-oblique, seed 1 | 0.0552 (0.0493 to 0.0607) | 8.7% (7.9 to 9.6) |
| S-oblique, seed 2 | 0.0501 (0.0448 to 0.0569) | 7.9% (7.1 to 8.9) |
| S-oblique, mean of 3 seeds | 0.0555 (0.0502 to 0.0614) | 8.8% (8.1 to 9.6) |
| S-oblique-six, seed 0 (settlement seed 21) | 0.1055 (0.0980 to 0.1148) | 16.7% (15.7 to 18.1) |
| S-oblique-six, seed 1 | 0.0958 (0.0884 to 0.1048) | 15.2% (14.1 to 16.5) |
| S-oblique-six, seed 2 | 0.0887 (0.0813 to 0.0968) | 14.1% (13.1 to 15.2) |
| S-oblique-six, mean of 3 seeds | 0.0966 (0.0896 to 0.1048) | 15.3% (14.4 to 16.5) |
| S-oblique-six, settlement seed 22 | 0.0935 (0.0866 to 0.1023) | 14.8% (13.8 to 16.1) |
| S-oblique-six, settlement seed 23 | 0.0821 (0.0746 to 0.0901) | 13.0% (11.9 to 14.1) |
| S-oblique-six, mean of 3 settlement seeds | 0.0937 (0.0868 to 0.1019) | 14.8% (13.9 to 16.0) |

**Precision and recall.** Figure @fig{fig11_pr_visdrone} draws the precision-recall curves of R, the first run of S-oblique-six and the two fine-tuning models at 10 per cent (Section 5.3), and Table @tab{pr} gives their operating points. The three curves with real training data kept the same order over the whole range of recall; the zero-shot curve fell below a precision of 0.6 at 1 per cent recall and ended at a recall of 0.39.

<!--FIG:06-resultados/figuras/fig11_pr_visdrone.png|Precision-recall curves at IoU 0.50 on VisDrone-DET val (548 images, pedestrian and people merged) for R, S-oblique-six (seed 0, zero-shot), F-generic and F-synthetic at 10 per cent, from the validator's precision envelope at 1,000 recall points. The marker on each curve is the confidence that maximises F1.-->

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:pr|Operating points on VisDrone-DET val for the four models of the precision-recall figure: confidence, precision, recall and F1 at the F1 maximum (smoothed as the validator does), and precision and recall at the default prediction confidence of 0.25.-->

| Model | Confidence at max F1 | Precision | Recall | F1 | Precision at 0.25 | Recall at 0.25 |
|---|---|---|---|---|---|---|
| R | 0.2963 | 0.7312 | 0.5729 | 0.6424 | 0.6731 | 0.6036 |
| F-generic 10% | 0.3193 | 0.6823 | 0.5160 | 0.5876 | 0.5698 | 0.5757 |
| F-synthetic 10% | 0.2983 | 0.6372 | 0.4579 | 0.5328 | 0.5535 | 0.4986 |
| S-oblique-six, seed 0 | 0.2152 | 0.2631 | 0.1716 | 0.2077 | 0.2804 | 0.1625 |

</div>

**Number of frames.** Trained on nested subsets of its training frames (152 training frames of its 180), S-oblique-six rose on the benchmark from 0.0618 at 30 frames to 0.0966 at 152 (Table @tab{curva}). The difference of +0.0349 (+0.0310 to +0.0392), 56.5 per cent, passed all three readings, the ranges over three seeds not overlapping. Between 120 and 152 frames it was +0.0062 (+0.0033 to +0.0088), 6.9 per cent, which passed the interval reading only, the ranges overlapping. A fit of mAP50 on the logarithm of the number of frames over the five means gave a gain of 0.0140 per doubling.

<!--TAB:curva|Learning curve of S-oblique-six over the number of training frames: nested subsets stratified by settlement, the same validation tiles, 60 epochs, zero-shot mAP50 on VisDrone-DET val by training seed, with the mean over seeds, its 95 per cent interval by resampling images and the efficacy of the mean. Means and differences are computed before rounding.-->

| Training frames (tiles) | mAP50 by training seed | Mean (95% interval) | Range | Efficacy of the mean |
|---|---|---|---|---|
| 30 (182) | 0.0499, 0.0674, 0.0679 | 0.0618 (0.0566 to 0.0679) | 0.0499 to 0.0679 | 9.8% |
| 60 (341) | 0.0806 | 0.0806 (0.0739 to 0.0885) | one run | 12.8% |
| 90 (503) | 0.0810 | 0.0810 (0.0745 to 0.0886) | one run | 12.8% |
| 120 (696) | 0.0915, 0.0878, 0.0918 | 0.0904 (0.0838 to 0.0986) | 0.0878 to 0.0918 | 14.3% |
| 152 (890), the full corpus | 0.1055, 0.0958, 0.0887 | 0.0966 (0.0896 to 0.1048) | 0.0887 to 0.1055 | 15.3% |

**Nadir benchmark.** On HERIDAL, at the matched input size of 1,152 pixels (Section 4.6), R scored 0.3185 (0.2843 to 0.3543), above the 0.05 fixed as the limit of interpretability. The order of the two geometries reversed with respect to the urban benchmark (Table @tab{heridal}). S-nadir-150 reached 0.1997 on the mean of its three runs, 62.7 per cent of R, and S-oblique 0.1341, 42.1 per cent. The difference, -0.0656 (-0.0840 to -0.0471), a ratio of 0.671 (0.61 to 0.74) against 4.08 on the urban benchmark, passed the interval and relative readings and not the seed reading: the nadir runs spread from 0.0926 to 0.2672 and overlapped the oblique runs, 0.1092 to 0.1476. With six settlements the nadir model, from one run, reached 0.2488, 78.1 per cent of R, against 0.1477 for S-oblique-six on three runs, a difference of -0.1012 (-0.1216 to -0.0786) that passed the interval and relative readings. At the protocol size of 1,280 pixels the order was the same, -0.0260 (-0.0414 to -0.0097) between the single-settlement arms, which passed the interval reading only.

<!--TAB:heridal|Zero-shot person detection on the nadir benchmark, HERIDAL (1,647 images, 3,229 persons, nadir from 40 to 65 m), at the matched input size of 1,152 pixels and at the protocol size of 1,280: mAP50 with the 95 per cent interval by resampling images, on the mean of the training runs where a model was trained three times, the range over those runs and the share of R, which was trained on the urban benchmark.-->

| Model | Runs | mAP50 at 1,152 (95% interval) | Range over runs | Share of R | mAP50 at 1,280 |
|---|---|---|---|---|---|
| R (1,106 real images of VisDrone-DET train) | 1 | 0.3185 (0.2843 to 0.3543) | one run | 100% | 0.3353 |
| S-nadir-150 | 3 | 0.1997 (0.1713 to 0.2306) | 0.0926 to 0.2672 | 62.7% | 0.1682 |
| S-nadir-150-six | 1 | 0.2488 (0.2116 to 0.2865) | one run | 78.1% | 0.2208 |
| S-oblique | 3 | 0.1341 (0.1149 to 0.1555) | 0.1092 to 0.1476 | 42.1% | 0.1422 |
| S-oblique-six | 3 | 0.1477 (0.1265 to 0.1715) | 0.1079 to 0.1847 | 46.4% | 0.1418 |

### 5.3 Experiment B: synthetic pretraining and joint training against a generic start

Given the 5 or 10 per cent slice of real images, the model that started from the synthetic weights finished below the generic start at both volumes, under the original schedule and under each of three others, and so did the model trained on synthetic and real images together (Table @tab{ajuste}, Figure @fig{fig10_ajuste_fino}).

<!--TAB:ajuste|Fine-tuning on 5 and 10 per cent of the benchmark's training split from the synthetic model and from generic weights, and joint training from generic weights on the same real images with the 890 synthetic tiles: mAP50 on VisDrone-DET val with 95 per cent intervals by resampling images, by training seed where repeated.-->

| Real training data, seed | F-synthetic (from S-oblique-six) | F-generic (from COCO) | F-joint |
|---|---|---|---|
| 5 per cent (324 images), seed 0 | 0.4424 (0.4260 to 0.4587) | 0.5220 (0.5045 to 0.5403) | 0.4607 (0.4444 to 0.4789) |
| 5 per cent, seed 1 | 0.4608 (0.4441 to 0.4784) | 0.5228 (0.5056 to 0.5410) | trained once |
| 5 per cent, seed 2 | 0.4554 (0.4400 to 0.4721) | 0.5285 (0.5114 to 0.5474) | trained once |
| 10 per cent (647 images), seed 0 | 0.5095 (0.4935 to 0.5264) | 0.5709 (0.5535 to 0.5883) | 0.5428 (0.5259 to 0.5610) |

<!--FIG:06-resultados/figuras/fig10_ajuste_fino.png|mAP50 on VisDrone-DET val against the number of real training images for the three ways of using the synthetic corpus once real images exist: as starting weights (synthetic start), mixed into the training set (joint) or not at all (generic start). Filled markers: the first training run; open markers: the two further runs where they exist. Dashed line: R, trained on 1,106 real images for twice as many epochs.-->

At 5 per cent the generic start finished above the synthetic start by +0.0796 (+0.0721 to +0.0873), +0.0620 (+0.0548 to +0.0706) and +0.0731 (+0.0654 to +0.0810) on the three seeds, +0.0716 (+0.0658 to +0.0780) on the means, a ratio of 1.158 (1.144 to 1.173) and a relative difference of 15.8 per cent. The lowest generic run lay above the highest synthetic one. At 10 per cent the difference was +0.0614 (+0.0553 to +0.0679), a ratio of 1.121 (1.108 to 1.134) and 12.1 per cent. The sign was the same in mAP50-95, the selection metric (Section 4.7): -0.0368 for the synthetic start at 5 per cent and -0.0232 at 10. The best weights of every fine-tuned and joint model under the original schedule fell at epochs 27 to 30 of their 30. The synthetic start given 647 real images (0.5095) did not reach the generic start given 324 (0.5220), and the expectation fixed before the run (Section 4.6), that the difference would be largest at the smaller volume, failed in sign: the difference was most negative there and narrowed as real data grew. Fine-tuning did move the synthetic model itself, from 0.1055 to 0.4424 with 324 real images.

The joint models finished 0.0637 (0.0562 to 0.0700) below the generic start on the mean of its three seeds at 5 per cent (ratio 1.138, 1.121 to 1.154; 13.8 per cent) and 0.0281 (0.0214 to 0.0346) below at 10 per cent (ratio 1.052, 1.039 to 1.064; 5.2 per cent). Both margins exceeded twice the standard deviation of the three generic runs at 5 per cent (a standard deviation of 0.0035), the margin fixed in advance and borrowed at 10 per cent. Against the synthetic start the joint model scored +0.0078 (+0.0025 to +0.0147) higher on the mean of the synthetic seeds at 5 per cent (1.7 per cent), with the interval crossing zero against two of the three synthetic seeds and the joint value falling inside their range. At 10 per cent it scored +0.0333 (+0.0276 to +0.0399) higher (6.5 per cent), above the synthetic start at IoU 0.50 and 0.60 and below it at 0.75 (0.0983 against 0.1025). On the selection slice the synthetic start led in the first three epochs at 5 per cent and was overtaken by the fourth; at 10 per cent the generic start led from the first epoch; afterwards the synthetic start led only intermittently, and the generic start's lead did not narrow between epoch 20 and epoch 30.

**Fine-tuning schedule.** With the optimiser set explicitly, the control run reproduced the generic model at 5 per cent exactly, 0.5220 against 0.5220 (tolerance 0.0035, Section 4.6), so the new cells compare with the existing models. Table @tab{cronograma} gives the twelve cells. Freezing the backbone, lowering the learning rate or both lowered the synthetic start in every cell, to between 0.2028 and 0.3875, while the lower learning rate raised the generic start at both volumes. On the selection slice the synthetic start preferred the original schedule at both volumes and the generic start the learning rate of 0.0002; its two further seeds at 5 per cent scored 0.5963 and 0.5982. With each start on the schedule it preferred, the generic start finished above the synthetic one by +0.1369 (+0.1290 to +0.1465) at 5 per cent, 0.5897 against 0.4529 on the means of three seeds, a ratio of 1.302 (1.279 to 1.331) and 30.2 per cent, with ranges that did not overlap; at 10 per cent by +0.1129 (+0.1044 to +0.1230), 0.6224 against 0.5095, a ratio of 1.222 (1.202 to 1.245) and 22.2 per cent, from one run per side. Under each of the four schedules, at both volumes, the generic start lay above the synthetic one with an interval excluding zero, and neither ordering changed at IoU 0.60 or 0.75. The joint models were not trained under the new schedules (Section 4.6).

<!--TAB:cronograma|Fine-tuning under four schedules, by real-data slice and start: mAP50 of the fine-tuned model on VisDrone-DET val, the test set (first training seed), and, in parentheses, the mAP50-95 of its best checkpoint on the selection slice, on which the schedule of each start was chosen; the chosen cell is in bold. The schedules are those of the grid of Section 4.6: the original trains the whole network at a learning rate of 0.002, the others freeze the backbone, lower the rate to 0.0002, or both, at the same budget of 30 epochs.-->

| Slice, start | Original | Frozen backbone | Learning rate 0.0002 | Both |
|---|---|---|---|---|
| 5 per cent, synthetic | **0.4424 (0.1480)** | 0.2808 (0.0901) | 0.3103 (0.1019) | 0.2028 (0.0585) |
| 5 per cent, generic | 0.5220 (0.1802) | 0.5467 (0.1886) | **0.5746 (0.2230)** | 0.5410 (0.1915) |
| 10 per cent, synthetic | **0.5095 (0.1743)** | 0.3209 (0.1053) | 0.3875 (0.1258) | 0.2241 (0.0681) |
| 10 per cent, generic | 0.5709 (0.1951) | 0.5772 (0.2030) | **0.6224 (0.2451)** | 0.5644 (0.2001) |

### 5.4 Experiment C: the armed and unarmed distinction by GSD

At 2.44 and 1.14 cm per pixel the three-class detectors called between 0.165 and 0.273 of confusable objects armed on their selection splits, and halving the GSD from 2.44 to 1.14 cm per pixel did not reduce that rate on matched corpora (0.253 against 0.125 on held-out frames); at 4.88 cm per pixel a separation above chance remained, weaker than at 2.44 on the same held-out frames, where the object rate was 0.245, so that the rate was lowest at the middle GSD.

**4.88 cm per pixel.** The twin at 150 m, where the median annotated box of its selection split measures 21 by 20 pixels, first found 148 of 297 annotated figures (0.498) on its selection split, below the half fixed before its run. Trained again for longer (Section 4.6; it stopped at epoch 80), it found 0.606 of the 297 figures in any class on its selection split and 0.663 of 916 on its 80 held-out frames, and passed the condition. On the selection split it called 0.435 of armed figures and 0.178 (0.107 to 0.247) of confusable objects armed, a d′ of 0.75 (0.33 to 1.26), with a three-class mAP50 of 0.388. On the held-out frames (Table @tab{gsd150}) it called 0.457 of armed figures, 0.245 (0.204 to 0.289) of confusable objects and 0.205 of unarmed persons armed, a d′ against objects of 0.58 (0.38 to 0.78), whose interval excludes zero. On the same frame indices the d′ was 0.97 for the twin at 75 m and 0.77 for the 35 m model. Against the twin at 75 m, d′ at 150 m was lower by 0.394 (-0.681 to -0.098) and the object rate higher by 0.120 (+0.058 to +0.181), both passing the interval and relative readings. Figures carrying the 0.20 m pistol were called armed at 0.50 (17 of 34), within the range of the long arms (0.41 to 0.50).

<!--TAB:gsd150|The three-class models at 1.14, 2.44 and 4.88 cm per pixel on the 80 held-out frames of each corpus, which share their frame indices: share of annotated figures found in any class, the rates at which each class is called armed at confidence 0.25, and d′ against confusable objects (log-linear correction), from the first training run of each model, the model at 150 m being the one trained for longer. The interval at 150 m is by 1,000 resamples of frames; the intervals of the two finer GSDs are in Table @tab{gemeo}.-->

| Model (GSD, cm/px) | Figures found | Armed called armed | Object called armed | Unarmed called armed | d′ vs object |
|---|---|---|---|---|---|
| S-nadir-35 (1.14) | 0.684 | 0.543 | 0.253 | 0.156 | 0.77 |
| Twin at 75 m (2.44) | 0.766 | 0.432 | 0.125 | 0.140 | 0.97 |
| Twin at 150 m (4.88) | 0.663 | 0.457 | 0.245 (0.204 to 0.289) | 0.205 | 0.58 (0.38 to 0.78) |

**2.44 and 1.14 cm per pixel, selection split.** Table @tab{armado} gives the three models on their selection splits (instance counts in Table @tab{corpora}).

<!--TAB:armado|The armed and unarmed distinction on the selection split of each three-class corpus (27, 35 and 24 frames), under the protocol of Section 4.7, at confidence 0.25, with 95 per cent intervals by resampling frames. d′ with the log-linear correction; without it the values against objects are 0.83, 0.78 and 0.90 and against unarmed persons 1.24, 1.14 and 1.16. The three-class mAP50 is on whole frames.-->

| Quantity | S-nadir-75 (75 m, 2.44 cm/px) | S-nadir-35 (35 m, 1.14 cm/px) | Twin of S-nadir-35 at 75 m (2.44 cm/px) |
|---|---|---|---|
| mAP50, three classes | 0.579 | 0.514 | 0.508 |
| Recall, armed | 0.547 (0.476 to 0.627) | 0.569 (0.492 to 0.646) | 0.471 (0.397 to 0.558) |
| Precision, armed | 0.386 | 0.415 | 0.440 |
| Confusable object called armed | 0.237 (0.183 to 0.289) | 0.273 (0.202 to 0.353) | 0.165 (0.100 to 0.230) |
| Unarmed person carrying nothing called armed | 0.131 (0.073 to 0.188) | 0.168 (0.101 to 0.235) | 0.109 (0.044 to 0.174) |
| d′ against confusable objects | 0.83 (0.54 to 1.13) | 0.77 (0.46 to 1.10) | 0.89 (0.58 to 1.32) |
| d′ against unarmed persons | 1.23 | 1.12 | 1.14 |

**Held-out frames at 2.44 cm per pixel.** On the 50 held-out frames of the unseen-weapon test (Section 4.3), S-nadir-75 called 0.434 (0.381 to 0.496) of armed figures, 0.152 (0.113 to 0.196) of confusable objects and 0.068 (0.035 to 0.102) of unarmed persons armed. Its armed precision was 0.430 and its d′ against objects 0.85 (0.64 to 1.09). Every rate was lower than on the selection split. Recall was 0.400 on the five training firearms (50 of 125) and 0.466 on the two unseen ones (61 of 131), a ratio of 1.16 (approximate 95 per cent interval 0.88 to 1.54) against the threshold of 0.80 (Section 4.6). The seen group includes the pistol, 20 of its 125 instances, and with the pistol set aside the ratio stayed above the threshold. Per model, from 15 to 69 instances each and without intervals, the unseen 1.10 m rifle was called armed at 0.50, within the range of the seen long arms (0.34 to 0.52), the unseen 0.55 m submachine gun at 0.43 and the pistol at 0.20. Among objects, the closed umbrella, 0.88 m long, was called armed at 0.38 (29 instances), brooms at 0.10 (41) and lengths of pipe at 0.11 (28). In the carried-as-weapon re-render, matched box for box in 49 of 50 frames, S-nadir-75 called 0.154 of the 227 paired objects armed as normally carried and 0.137 when carried in the weapons' poses and at their angles (exact McNemar test, p = 0.56), and the umbrella, whose carriage did not change, stayed at 0.38.

**35 m against its twin at 75 m.** Table @tab{gemeo} gives the two matched models on their selection splits and on the 80 held-out frames of each corpus, over three training seeds and at three IoU thresholds.

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:gemeo|S-nadir-35 against its twin at 75 m, every other setting held. Rates at which each class is called armed at confidence 0.25 on the selection splits (35 and 24 frames) and on the 80 held-out frames of each corpus, with differences, 95 per cent intervals by resampling frames independently on each side and p from a two-proportion test. Further rows give ranges and means over three training seeds, the object rate at stricter IoU thresholds and d′ (log-linear correction) with intervals by resampling frames.-->

| Quantity | S-nadir-35 (1.14 cm/px) | Twin at 75 m (2.44 cm/px) | Difference (95% interval) |
|---|---|---|---|
| Confusable object called armed, selection split | 0.273 | 0.165 | +0.108 (+0.015 to +0.211), p = 0.06 |
| Confusable object called armed, 80 held-out frames | 0.253 (74 of 292) | 0.125 (36 of 288) | +0.128 (+0.071 to +0.194), p = 0.0001 |
| Armed person called armed, selection split | 0.569 | 0.471 | +0.099 (-0.022 to +0.217), p = 0.15 |
| Armed person called armed, 80 held-out frames | 0.543 | 0.432 | +0.112 (+0.031 to +0.192) |
| Unarmed person called armed, selection split | 0.168 | 0.109 | +0.059 (-0.038 to +0.154), p = 0.22 |
| Unarmed person called armed, 80 held-out frames | 0.156 | 0.140 | +0.015 (-0.040 to +0.073) |
| d′ against confusable objects, selection split | 0.77 (0.46 to 1.10) | 0.89 (0.58 to 1.32) | |
| d′ against confusable objects, 80 held-out frames | 0.77 (0.57 to 0.99) | 0.97 (0.77 to 1.20) | |
| Object rate over three training seeds, selection split (range; mean) | 0.231 to 0.273; 0.248 | 0.132 to 0.242; 0.179 | ranges overlap; +0.068 (+0.002 to +0.142), 38.1% |
| Object rate over three training seeds, 80 held-out frames (range; mean) | 0.202 to 0.253; 0.222 | 0.097 to 0.181; 0.134 | ranges separate; +0.087 (+0.044 to +0.136), 64.9% |
| Object rate, selection split, at IoU 0.60 and 0.75 | 0.223 and 0.132 | 0.165 and 0.132 | level at 0.75 |

</div>

Seed by seed, the object-rate difference excluded zero in seeds 0 and 1 and not in seed 2 on both sets; the armed recall of the 35 m model exceeded the twin's on the held-out frames in seeds 0 and 1 and fell below it in seed 2, and the unarmed rate differed in no seed. On the means of the three seeds the armed difference was +0.072 (-0.023 to +0.163) on the selection splits and +0.050 (-0.017 to +0.111) on the held-out frames, and the unarmed difference +0.004 (-0.053 to +0.062) and -0.018 (-0.063 to +0.031), every interval crossing zero. Against the original 75 m model, the 35 m model's object rate on the selection split differed by +0.036 (-0.059 to +0.124) at IoU 0.50 and fell below it at 0.60 and 0.75, where the original model called 0.230 and 0.141 of objects armed; the unarmed rate did the same at 0.75 (0.076 against 0.085). Between the original 75 m corpus and the twin, which changed the carrying poses and the other settings of Section 4.6 at the same GSD, the object rate moved from 0.237 to 0.165 (p = 0.19).

**Threshold sweep.** Figure @fig{fig12_limiar_armado} sweeps the confidence threshold of the seven three-class models on both sets, and Table @tab{limiar} gives the three operating points of Section 4.7 for the first run of each model.

<!--FIG:06-resultados/figuras/fig12_limiar_armado.png|Armed recall against the object rate as the confidence threshold runs from 0.95 (lower left) to 0.05 (upper right), for S-nadir-75, S-nadir-35 and the twin at 75 m. Left: selection split of each corpus. Right: held-out frames (80 at 35 m and at 75 m; the 50 unseen-weapon frames for S-nadir-75). Filled markers: confidence 0.25, seed 0; hollow markers: confidence 0.25, seeds 1 and 2 (dashed and dotted curves).-->

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:limiar|The three operating points of Section 4.7 (default confidence 0.25, maximum armed F1, object rate at or below 0.10) for each three-class model (seed 0) on its selection split and its held-out frames; d′ against confusable objects, log-linear correction.-->

| Model | Set (frames) | Operating point | Threshold | Armed recall | Object called armed | Armed precision | d′ vs object |
|---|---|---|---|---|---|---|---|
| S-nadir-75 | selection (27) | default | 0.25 | 0.547 | 0.237 | 0.386 | 0.83 |
| S-nadir-75 | selection (27) | max armed F1 | 0.40 | 0.564 | 0.200 | 0.516 | 0.99 |
| S-nadir-75 | selection (27) | object rate 0.10 | 0.70 | 0.333 | 0.096 | 0.661 | 0.86 |
| S-nadir-75 | held-out (50) | default | 0.25 | 0.434 | 0.152 | 0.430 | 0.85 |
| S-nadir-75 | held-out (50) | max armed F1 | 0.45 | 0.391 | 0.126 | 0.578 | 0.86 |
| S-nadir-75 | held-out (50) | object rate 0.10 | 0.55 | 0.340 | 0.100 | 0.669 | 0.86 |
| S-nadir-35 | selection (35) | default | 0.25 | 0.569 | 0.273 | 0.415 | 0.77 |
| S-nadir-35 | selection (35) | max armed F1 | 0.30 | 0.555 | 0.256 | 0.469 | 0.79 |
| S-nadir-35 | selection (35) | object rate 0.10 | 0.60 | 0.285 | 0.099 | 0.722 | 0.70 |
| S-nadir-35 | held-out (80) | default | 0.25 | 0.543 | 0.253 | 0.408 | 0.77 |
| S-nadir-35 | held-out (80) | max armed F1 | 0.35 | 0.497 | 0.226 | 0.484 | 0.74 |
| S-nadir-35 | held-out (80) | object rate 0.10 | 0.65 | 0.211 | 0.099 | 0.603 | 0.48 |
| Twin at 75 m | selection (24) | default | 0.25 | 0.471 | 0.165 | 0.440 | 0.89 |
| Twin at 75 m | selection (24) | max armed F1 | 0.40 | 0.423 | 0.154 | 0.522 | 0.81 |
| Twin at 75 m | selection (24) | object rate 0.10 | 0.55 | 0.341 | 0.099 | 0.630 | 0.86 |
| Twin at 75 m | held-out (80) | default | 0.25 | 0.432 | 0.125 | 0.370 | 0.97 |
| Twin at 75 m | held-out (80) | max armed F1 | 0.40 | 0.381 | 0.090 | 0.480 | 1.03 |
| Twin at 75 m | held-out (80) | object rate 0.10 | 0.40 | 0.381 | 0.090 | 0.480 | 1.03 |

</div>

Over the 14 combinations of model, seed and set, the threshold that maximised the F1 of the armed class lay between 0.30 and 0.50 (0.40 in 7 of them) and raised the armed precision from 0.37 to 0.46 at the default to 0.47 to 0.66, at a cost of 1 to 8 points of armed recall in 13 of them and a gain of 2 in S-nadir-75 on its selection split. Bringing the object rate to 0.10 required a threshold of 0.55 to 0.70 for S-nadir-35 and S-nadir-75, where armed recall then lay between 0.21 and 0.36; the twin reached 0.10 at thresholds between 0.25 and 0.65. At no threshold did any model exceed an armed recall of 0.65, and at an object rate of 0.10 or below the highest armed recall was 0.42, for the twin at 75 m on its third training seed on the held-out frames (armed precision 0.61), and 0.38 or below in every other combination. On the held-out frames the curve of the 35 m model ran to the right of the twin's, at a higher object rate for the same armed recall.

### 5.5 Experiment D: performance by illumination regime

Measured on synthetic frames, hard sun was the weakest of the six regimes for S-nadir-150 on both measures, and overcast the strongest on mAP50, level with low sun (Table @tab{regimes}, Figure @fig{fig4_dataset}); a model trained under hard sun alone was not resolvably below the model of all regimes under overcast in recall.

<!--TAB:regimes|Per-regime performance on the 120 held-out frames of the corpus of record (nadir, 150 m, 4.88 cm per pixel), 20 per regime: mAP50 on the tiles of each regime and recall at confidence 0.25 on whole frames, for S-nadir-150, trained on all six regimes, with 95 per cent intervals by resampling frames, and for the model trained under hard sun alone.-->

| Regime | mAP50, all regimes | Recall at 0.25, all regimes | 95% interval | mAP50, hard sun only | Recall at 0.25, hard sun only |
|---|---|---|---|---|---|
| Hard sun | 0.675 | 0.657 | 0.591 to 0.720 | 0.742 | 0.739 |
| Heavy overcast | 0.755 | 0.768 | 0.714 to 0.816 | 0.754 | 0.749 |
| Rain | 0.759 | 0.789 | 0.748 to 0.827 | 0.728 | 0.747 |
| Haze | 0.780 | 0.726 | 0.697 to 0.757 | 0.652 | 0.569 |
| Low sun | 0.790 | 0.814 | 0.768 to 0.854 | 0.794 | 0.776 |
| Overcast | 0.791 | 0.796 | 0.760 to 0.827 | 0.796 | 0.759 |

<!--FIG:06-resultados/figuras/fig4_dataset.jpg|One annotated frame of the pilot corpus (nadir, 150 m, 1920 by 1080, 9.76 cm per pixel) from each of the six illumination regimes, with the generated boxes drawn: green for the armed class, blue for the unarmed class. The labelling does not depend on the regime (Section 4.2.5).-->

On point estimates, without intervals, hard sun scored 8 points of mAP50 below the next regime; on recall, which carries an interval, its interval lay wholly below those of overcast, rain and low sun while overlapping those of haze and heavy overcast. Overcast scored above both hard sun and rain on both measures, and the margin of overcast over rain lay within the recall intervals. Low sun, which also casts sharp shadows, scored level with overcast on mAP50 (0.790 against 0.791) and highest on recall. The ordering by detection, measured on the corpus of record at 4.88 cm per pixel, matched the ordering by contrast over clutter of Section 5.1, measured on the pilot corpus at 9.76 cm per pixel, at the two extremes, overcast and hard sun, and not among the intermediate regimes.

**Hard-sun-only ablation.** Trained on 180 frames under hard sun alone, the specialist scored 0.7422 of mAP50 and 0.739 of recall under hard sun. On the same 20 hard-sun frames its recall exceeded that of the model of all regimes by +0.0818 (+0.0377 to +0.1243). Against the model of all regimes under overcast, the comparison fixed as decisive, its recall under hard sun differed by -0.0572 (-0.1252 to +0.0067), an interval that includes zero; its mAP50 under hard sun stayed below the 0.7906 of that model under overcast, by 6.5 per cent. Under the other five regimes the specialist fell below the model of all regimes in recall, most under haze (0.569 against 0.726), while its mAP50 was level under heavy overcast and higher under low sun and overcast. Zero-shot on the urban benchmark, as an exploratory reading, it scored 0.0072 against 0.0102 for the first run of S-nadir-150.

### 5.6 Robustness checks and summary of hypotheses

Every check fixed in advance was run, those of the last stage of Section 4.6 included; Table @tab{hipoteses} records each outcome against its criterion, with the three readings of resolvability of Section 4.7 for every headline comparison. Under both the validator and the official toolkit rule, no pair among those fixed for the IoU check changed order between 0.50, 0.60 and 0.75 on the benchmark, including the pairs of the last stage (the geometry comparison on three seeds per side, 152 against 30 frames, the settlement seeds against S-oblique and the fine-tuning starts on their chosen schedules); the two comparisons that did reverse are reported at all three thresholds in Sections 5.3 and 5.4.

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:hipoteses|Each hypothesis and pre-specified check against its criterion, with its status (Section 4.6) and the readings of Section 4.7 that its headline difference passes: (a) seed ranges, (b) paired interval, (c) 30 per cent; n.a. where a side was trained once or no difference is at issue.-->

| Hypothesis or check | Pre-specified criterion | Status | Data | Outcome | Resolvable (a / b / c) |
|---|---|---|---|---|---|
| Ceiling R valid | R not near chance | confirmatory | real; R selected on the test split | held: 0.6311 | n.a. |
| Synthetic-only training recovers a fraction of the ceiling | ratio to R; scale a confound if the scale-matched figure differs by more than half | confirmatory | real | held: 2.2% on 3 seeds (1.6% on seed 0); scale check differed by a quarter | n.a. |
| Geometry load-bearing: S-oblique above S-nadir-150 | oblique arm outperforms nadir arm; last stage: readings of Section 4.7 on 3 seeds per side | confirmatory | real | held: +0.0419 on 3 seeds per side, ratio 4.08 (seed 0 alone: +0.0511, ratio 6.011) | yes / yes / yes, 307.9% |
| Oblique advantage shrinks or reverses on a nadir benchmark | R not below 0.05; S-oblique against S-nadir-150 at the matched input size, readings of Section 4.7; scale-dependent if the order differs at 1,280 | confirmatory | real nadir | held, reversed: -0.0656, ratio 0.671; R 0.3185; same order at 1,280 | no, ranges overlap / yes / yes, 48.9% |
| Six settlements against one, nadir | none; last stage: readings of Section 4.7 | exploratory, criterion fixed | real | observed: +0.0054 on 3 nadir seeds (+0.0088 on seed 0) | six-settlement value inside the 3-seed range / yes / yes, 39.9% |
| Six settlements against one, oblique | none; last stage: readings of Section 4.7 on 3 seeds per side | exploratory, criterion fixed | real | observed: +0.0411 on 3 seeds per side | yes / yes / yes, 74.0% |
| Six settlements above one across settlement seeds | readings of Section 4.7; scene dominates if its range exceeds twice the training range | confirmatory | real | held: +0.0381; scene range 1.4 times the training range | yes / yes / yes, 68.7% |
| Number of frames operant: 152 against 30 | 152 above 30 in (a) and (b) | confirmatory | real | held: +0.0349 | yes / yes / yes, 56.5% |
| End of the curve: 152 against 120 | rising if (a) and (b); flat if neither; rising within training dispersion if (b) only | confirmatory | real | rising within training dispersion: +0.0062; 0.0140 per doubling | no, ranges overlap / yes / no, 6.9% |
| Illumination: overcast above hard sun and rain; hard sun among the 2 weakest | as stated | confirmatory | synthetic held-out | held on point estimates; the margin of overcast over rain lies within the recall intervals | n.a. |
| Hard-sun deficit belongs to the regime | specialist under hard sun below the model of all regimes under overcast, D-ii interval wholly below zero | confirmatory | synthetic held-out | D-ii interval includes zero: -0.0572 (-0.1252 to +0.0067); condition not met | n.a. / no / no, 6.5% on mAP50 |
| Synthetic pretraining adds accuracy, most at 5% | expectation fixed before the run | exploratory, criterion fixed | real | failed: -0.0716 at 5%, -0.0614 at 10% | 5%: yes / yes / no, 15.8%; 10%: n.a. / yes / no, 12.1% |
| Cost of the synthetic start robust to the schedule | F-generic resolvably above F-synthetic at both volumes, each on the schedule chosen on the selection slice; control reproduced within 0.0035 | confirmatory | real | held: +0.1369 at 5%, +0.1129 at 10%; control 0.5220 against 0.5220 | 5%: yes / yes / yes, 30.2%; 10%: n.a. / yes / no, 22.2% |
| Joint training adds accuracy | margin of twice the SD of the 3 generic runs (SD 0.0035) | exploratory, criterion fixed | real | failed: -0.0637 and -0.0281, beyond the margin | 5%: joint outside the generic range / yes / no, 13.8%; 10%: n.a. / yes / no, 5.2% |
| Joint training against the synthetic start | none | exploratory | real | observed: +0.0078 at 5%, +0.0333 at 10% | 5%: joint inside the synthetic range / yes on the mean, no on 2 of 3 seeds / no, 1.7%; 10%: n.a. / yes / no, 6.5% |
| Unseen-firearm recall at 75 m against seen-firearm recall | 75 m figure withdrawn if the ratio falls below 0.80 | confirmatory | synthetic held-out | withdrawal condition not met: ratio 1.16 | n.a. |
| Objects carried as weapons are called armed more often | paired rate rises (exact McNemar test); carrying caveat withdrawn if it does not | confirmatory | synthetic held-out | paired rate did not rise: 0.154 against 0.137, p = 0.56; withdrawal condition of the caveat met | n.a. |
| Validity of the three-class model at 4.88 cm per pixel | at least half of annotated figures found, on the selection split and on 80 held-out frames | confirmatory | synthetic selection split and held-out | first model not interpretable: 0.498; trained for longer, held: 0.606 and 0.663 | n.a. |
| Separation at 4.88 cm per pixel | interval of d′ includes zero: absence measured; excludes zero: separation above chance, read as a shortcut | confirmatory | synthetic held-out | interval excludes zero: d′ 0.58 (0.38 to 0.78); read as a shortcut by the rule of Section 4.6 | n.a. / yes, excludes zero / n.a. |
| 4.88 against 2.44 cm per pixel, matched held-out frames | readings (b) and (c) | confirmatory | synthetic held-out | d′ lower by 0.394, object rate higher by 0.120 | n.a. / yes / yes, 68.0% and 96.2% |
| Object rate differs between 1.14 and 2.44 cm per pixel, all else held | 35 m rate above the twin's on held-out frames at p below 0.05; withdrawn if reversed | exploratory, criterion fixed | synthetic held-out; selection split | held: +0.128, p = 0.0001; +0.087 on seed means (selection split: +0.108; +0.068 on seed means) | held-out: yes / yes / yes, 64.9%; selection: no, ranges overlap / yes / yes, 38.1% |
| Armed and unarmed rates differ between the 35 m model and its twin | none | exploratory | synthetic, both splits | not resolvable: seed-mean intervals cross zero on both sets; the held-out armed difference reverses in seed 2 | no / no / n.a. |
| 35 m model against the original 75 m model | ordering holds at IoU 0.50, 0.60 and 0.75 | exploratory | synthetic selection split | not resolvable: +0.036 (-0.059 to +0.124); order reverses at 0.60 | n.a. / no / no, 15.1% |

</div>
