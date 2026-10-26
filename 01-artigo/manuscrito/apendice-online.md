# Online Appendix

This appendix holds the material that supports the main text but is not needed to follow its argument: contextual detail on the study setting (Section A), the full parameters of the generator, the corpora and the training protocol (Section B), and supplementary results (Section C). Nothing here is a new analysis. Every table and figure comes from the same corpora, models and evaluations as the main text, and every number is the one the main text reports or reported before it was shortened. Terms follow the main text: S-nadir-150 is the corpus at the reference acquisition (nadir, 150 m, 4.88 cm per pixel); the selection split is the set on which a checkpoint is chosen; held-out frames are frames rendered after training and used for neither training nor selection; the share of R is the mAP50 of a model divided by that of R on the same test set; Twin-75 and Twin-150 are the S-nadir-35 corpus rendered at 75 and 150 m; the three classes are armed, unarmed and object.

## A. Study context: detail

### A1. Further figures on lethal force, territorial control and Jacarezinho

Section 3 of the main text draws on public sources only and is background, not data collected or analysed for the study. The figures below were part of that background in an earlier version and are kept here with their sources.

Intentional homicide in the state of Rio de Janeiro peaked in 1994 at 63.13 per 100,000 inhabitants in the series of the Instituto de Segurança Pública do Rio de Janeiro (ISP-RJ, n.d.-a) and stood at 17.1 in both 2024 and 2025 (Fórum Brasileiro de Segurança Pública, 2025, Table 3; 2026, Table 3).

The state homicide series of the Instituto de Segurança Pública do Rio de Janeiro begins in 1991 (ISP-RJ, n.d.-a), and the state rate of 17.1 per 100,000 inhabitants in 2024 was 10.8 per cent below that of 2023 (Fórum Brasileiro de Segurança Pública, 2025, Table 3). In the city of Rio de Janeiro, intentional homicides recorded by police district fell from 2,574 in 2003, the first year of that series, to 965 in 2025, a figure that from 2024 excludes femicides (ISP-RJ, n.d.-b). Over the two years of the police-intervention figures of Section 3.1 of the main text, police officers killed in the state rose from 28 to 51, an increase of 82.1 per cent, against a national fall from 144 to 139: the state accounted for 51 of the 139 police deaths in the country (Barros, 2026; Fórum Brasileiro de Segurança Pública, 2026, Table 6).

Operação Exceptis, carried out by the Civil Police in Jacarezinho on 6 May 2021, involved roughly 200 to 250 officers, armoured vehicles, helicopters and a sniper (Human Rights Watch, 2021; Sullivan et al., 2021).

After Operação Exceptis, human-rights organisations asked whether some of the dead had been executed (Human Rights Watch, 2021; Sullivan et al., 2021). In concluding ADPF 635 on 3 April 2025, the STF also required a plan to reoccupy areas held by criminal organisations (STF, 2025a, 2025b).

Under the restrictions of ADPF 635, lethality had already fallen by more than 60 per cent, from 1,814 deaths in 2019 to 699 in 2024 (JOTA, 2025). The figure for 2024 differs from the 703 of the Fórum Brasileiro de Segurança Pública (2026) for undocumented reasons. Critics found the ruling of 3 April 2025 either too weak or too intrusive (Causa Operária, 2025; Gazeta do Povo, 2025).

Operação Contenção was launched less than seven months after that ruling, against the Comando Vermelho criminal organisation (Agência Pública, 2025; Fichino, 2025). The official count was 121 dead, 117 of them civilians (Fichino, 2025), rising to 122 when a fifth officer died (Fórum Brasileiro de Segurança Pública, 2026); the state's Public Defender's Office counted 132 (Sullivan & da Cruz, 2025). Launched on 28 October 2025, it mobilised, besides about 2,500 officers, 32 armoured vehicles, 12 demolition vehicles and 2 helicopters (Couto, 2025; Fichino, 2025). Its judicial basis, by the state's report to the STF, was 51 arrest warrants of the 42nd Criminal Court of the capital, within a total of 100 the state sought to serve (Fichino, 2025). The President called it a massacre (CBS News, 2025), and the United Nations expressed grave concern (OPEB, 2025).

Criminal organisations hold durable, often decades-long control over particular favelas, financed by drug trafficking and contested by rival factions and by milícias (paramilitary groups often formed by security personnel). The principal one, the Comando Vermelho, emerged as a prison gang on Ilha Grande (Lessing, 2008), was first named in a prison director's report in 1979 (Misse, 2011) and in 2020 was estimated at around 30,000 members (InSight Crime, 2026). Narrow streets force special units to leave their armoured vehicles (Grillo, 2014), and incursions meet barricades, concrete at the entrance to Jacarezinho in 2021 and burning cars on access roads in 2025 (Sullivan et al., 2021; Sullivan & da Cruz, 2025).

Jacarezinho has the highest concentration of Afro-Brazilian residents among the city's favelas (RioOnWatch, 2019). The Comando Vermelho has long dominated it, and on 19 January 2022 more than 1,200 military police officers occupied it (Mistler-Ferguson, 2022).

The population of Jacarezinho is uncertain. Municipal figures put it at approximately 37,000 residents (RioOnWatch, 2019); the 2022 national census recorded 29,766 in the favela (Instituto Brasileiro de Geografia e Estatística, 2024, Table 5) and 35,458 in the administrative subdistrict of that name (Instituto Brasileiro de Geografia e Estatística, n.d.); community and journalistic sources commonly cite more than 60,000 (Caminhos Languages, 2025; Mistler-Ferguson, 2022), a discrepancy this article cannot resolve. It was already the largest favela of the city by 1960, with roughly 23,000 residents (RioOnWatch, 2019).

The original motivation of the study also rested on a premise that no source cited here establishes and that is stated as an assumption: that reliable, up-to-date maps of informal circulation routes do not exist, which leaves the planning of operations dependent on outdated or incomplete intelligence. No measurement in the article tests it.

## B. Methods: detail

### B1. Training and rendering parameters

Table B1. Training, inference and rendering settings, shared by every model unless stated.

| Parameter | Value |
|---|---|
| Detector, software, hardware | YOLO11s; Ultralytics 8.4.148, PyTorch 2.14.0, CUDA 12.6; one NVIDIA RTX 2060 with 6 GB |
| Initialisation | COCO pretrained weights; F-synthetic starts from S-oblique-six |
| Tiling of 3840 × 2160 frames | 1280 px tiles at a stride of 1024 px (20% overlap), 8 per frame; a tile without a box kept with probability 0.05; a clipped box kept if at least 0.40 of its area lies inside the tile; tiles cut at native scale, never from downscaled frames |
| Input size, batch | 1280 px, batch 6; real-data models train on whole VisDrone images resized to 1280 px on the long side, joint models on both kinds of input |
| Optimiser | AdamW, chosen automatically by the software together with its learning rate: momentum 0.9, initial learning rate 0.002 (single-class, fine-tuning and joint models) or 0.001429 (three-class models), linear decay to 0.01 of that value, 3 warm-up epochs; in the schedule grid of Experiment B the same optimiser set explicitly, with a learning rate of 0.002 or 0.0002 and the backbone (layers 0 to 10) trainable or frozen |
| Augmentation | mosaic 1.0, off for the last 10 epochs; horizontal flip 0.5; rotation up to 10 degrees; scale gain 0.4; translation 0.1; hue, saturation and value gains 0.015, 0.6 and 0.4 |
| Epochs | 60 for the synthetic models, 30 for the fine-tuning and joint models, 120 for the pilot; patience 15; 120 with patience 30 for Twin-150 when trained for longer |
| Selection split of a synthetic corpus | each frame assigned to the selection split with probability 0.15 (24 to 35 frames per corpus); split by frame, never by tile, since overlapping tiles are not independent |
| Checkpoint selection | fitness mAP50-95 at the validator's default thresholds, computed at the end of each epoch; checkpoint saved whenever the fitness strictly exceeds its previous best; training stops after 15 epochs without improvement; the fine-tuning and joint models of the original schedule ran their 30 epochs, best weights at epochs 27 to 30 |
| Selection split by family | synthetic models: tiles of the selection frames of their own corpus; fine-tuning and joint models: the selection slice of VisDrone train; R: VisDrone val, which is also its test set, at epoch 58 of 60 without early stopping |
| Inference | confidence 0.001 and non-maximum suppression at IoU 0.7 (defaults, not tuned) for mAP; VisDrone images resized to 1280 px on the long side; three-class rates at confidence 0.25 on whole frames at native scale |
| Rendering | Blender 5.2, headless, deterministic seed; Cycles path tracer on the GPU; 96 or 64 samples per pixel with denoising on; lossless PNG; training tiles re-encoded once as JPEG at quality 92 without chroma subsampling; every whole-frame evaluation reads the lossless frames |
| Camera implementation | a 4.3 mm lens on a 5.37 mm sensor, implemented as 28.8 mm on a 36 mm sensor with horizontal fit; horizontal field of view 63.96 degrees at 16:9; ground width 1.2488 times the altitude in nadir; the 5.37 mm sensor width, which the manual of the reference camera does not give, reproduces its published field of view within 0.3 degrees |
| Seeds | training seed 0 with deterministic operations; seeds 1 and 2 for the 10 repeated models; settlement seed 21 for S-oblique-six, 22 and 23 for its replicas; the 1,106 images of R drawn with seed 21; the 3 VisDrone slices with seed 2609 |

Three runs (Twin-75 with seed 0, S-nadir-35 with seed 1 and F-joint at 10 per cent) were paused and resumed from the last saved state, which restarts the draw of augmentations, so they are not bit-identical to continuous runs. The pilot used an earlier recipe: 2 classes, tiles and input of 640 pixels, batch 8 and a budget of 120 epochs cut short at 24.

Log-linear correction of d′. Each rate that enters d′ (Section 4.7 of the main text) is computed as (k + 0.5) / (n + 1), where k is the count called armed and n the class total, before the normal quantile is taken.

Altitude jitter. The commanded altitude of the nadir camera is jittered per image by up to 6 m (3 m at 35 m, 13 m for Twin-150); the oblique camera flies at 120 m with a jitter of up to 36 m.

Effects not simulated. Sensor noise, motion blur, depth of field, rolling shutter, chromatic aberration, vignetting, lens distortion and video compression, all present in a real frame from the reference camera, are not simulated.

Precision and recall of the single-class models. Precision and recall are those the validator returns at the confidence that maximises F1, the harmonic mean of precision and recall, not at the 0.001 threshold used for mAP.

Models trained three times. Ten models were trained with seeds 0, 1 and 2 on a fixed corpus: S-nadir-150, S-oblique, S-oblique-six, its subsets of 30 and 120 frames, both fine-tuning models at 5 per cent on the original schedule, F-generic at 5 per cent on the lower learning rate, S-nadir-35 and Twin-75. The per-regime recall of Experiment D uses 2,000 resamples of frames, paired for D-i.

Checks of Experiment A. The ceiling check asks whether R itself performs near chance, in which case the protocol, not synthesis, would be at fault. A scale-matched input size, fixed from labels before any evaluation, accompanies the protocol size of 1,280, so that the median person box reaches the network at about the size it has in S-nadir-150 (B5). HERIDAL is scored under the single-class protocol of VisDrone (H1 to H9, Table C0).

### B2. Corpora, held-out sets and real data

Table B2. Every corpus and test set of the study. Synthetic rows: camera, commanded altitude and nominal GSD, render size, frames by split, tiles by split, and annotated instances by class on whole frames (armed / unarmed / object). Real rows: images and person instances. The last column gives the model trained on the corpus and what it establishes, or the role of a test set. n.a.: not applicable.

| Corpus or set | Camera, altitude, GSD (cm/px) | Render (px) | Frames or images, train / selection or test | Tiles, train / selection | Instances, train | Instances, selection or test | Model and what it establishes, or role |
|---|---|---|---|---|---|---|---|
| Pilot corpus | nadir, 150 m, 9.76 | 1920 × 1080 | 40 / 8 | 274 / 61 | 292 / 273 / n.a. | 55 / 64 / n.a. | pilot model, two classes, earlier recipe: the pilot of the protocol (Table C4) |
| S-nadir-150 | nadir, 150 m, 4.88 | 3840 × 2160 | 149 / 31 | 1,106 / 225 | 1,331 / 1,328 / n.a. | 278 / 288 / n.a. | S-nadir-150: the method at the reference acquisition |
| S-nadir-150-six | nadir, 150 m, 4.88; 6 settlements | 3840 × 2160 | 156 / 24 | 1,135 / 174 | 1,424 / 1,368 / n.a. | 203 / 233 / n.a. | whether variety of settlement is a term in the gap |
| S-oblique | oblique 26 to 52°, 120 m, 3.90 nominal | 3840 × 2160 | 155 / 25 | 968 / 136 | 839 / 841 / n.a. | 113 / 119 / n.a. | whether failure is attributable to synthesis or to capture geometry |
| S-oblique-six | oblique 45 to 56°, 120 m, 3.90 nominal; 6 settlements | 3840 × 2160 | 152 / 28 | 890 / 144 | n.a. / 1,325 / n.a. | n.a. / 196 / n.a. | the best configuration tried, the synthetic model of the article; starting weights of F-synthetic; its 890 training tiles enter F-joint |
| S-oblique-six, settlement seeds 22 and 23 | as S-oblique-six, the six settlements drawn anew at the same sites | 3840 × 2160 | 180 frames each; split not reported | not reported | not reported | not reported | the dispersion due to the scene |
| S-oblique-six, nested subsets | as S-oblique-six, stratified by settlement | 3840 × 2160 | 30, 60, 90 or 120 / 28 | 182, 341, 503 or 696 / 144 | not reported | as S-oblique-six | whether the number of frames is operant, and where the curve stands at 152 |
| Hard-sun-only corpus | nadir, 150 m, 4.88; settlement and scene seed of S-nadir-150; hard sun alone | 3840 × 2160 | 180 frames; split not reported | not reported | not reported | not reported | hard-sun-only model: whether the hard-sun deficit belongs to the regime or to its share of training |
| S-nadir-75 | nadir, 75 m, 2.44 | 3840 × 2160 | 173 / 27 | 1,316 / 202 | 816 / 820 / 846 | 117 / 153 / 135 | whether the armed and unarmed distinction is resolvable |
| S-nadir-35 | nadir, 35 m, 1.14; realistic carrying poses for objects | 3840 × 2160 | 165 / 35 | 1,166 / 242 | 640 / 587 / 619 | 137 / 119 / 121 | with Twin-75: whether resolution or carrying pose drives the confusion |
| Twin-75 | nadir, 75 m, 2.44; the S-nadir-35 corpus rendered at 75 m | 3840 × 2160 | 176 / 24 | 1,287 / 176 | 650 / 638 / 701 | 85 / 92 / 91 | the comparison partner of S-nadir-35, every other setting held |
| Twin-150 | nadir, 150 m, 4.88; the S-nadir-35 corpus rendered at 150 m | 3840 × 2160 | 173 / 27 | 1,215 / 180 | 692 / 619 / 640 | 92 / 104 / 101 | whether the distinction is measurable at 4.88 cm per pixel |
| Held-out frames, 35 m | nadir, 35 m, 1.14 | 3840 × 2160 | 0 / 80 | not tiled | n.a. | 346 / 315 / 292 | test of S-nadir-35; frame indices shared with the two twins |
| Held-out frames, Twin-75 | nadir, 75 m, 2.44 | 3840 × 2160 | 0 / 80 | not tiled | n.a. | 257 / 292 / 288 | test of Twin-75 |
| Held-out frames, Twin-150 | nadir, 150 m, 4.88 | 3840 × 2160 | 0 / 80 | not tiled | n.a. | 324 / 278 / 314 | test of Twin-150 |
| Unseen-weapon test | nadir, 75 m, 2.44; new realisation of the settlement | 3840 × 2160 | 0 / 50 | not tiled | n.a. | 256 / 222 / 230 | test of S-nadir-75; the 2 unseen firearms in half the firearms |
| Carried-as-weapon re-render | nadir, 75 m, 2.44; the same 50 frames | 3840 × 2160 | 0 / 50 | not tiled | n.a. | 256 / 222 / 231 | test of S-nadir-75; every object carried exactly as a weapon, every other draw unchanged |
| Per-regime test | nadir, 150 m, 4.88 | 3840 × 2160 | 0 / 120 | 0 / 885 | n.a. | 1,085 / 1,119 / n.a. | Experiment D: S-nadir-150 and the hard-sun-only model, 20 frames per regime |
| VisDrone-DET train, full | real | mixed; 1400 × 1050 most common | 6,471 / n.a. | n.a. | 106,396 persons | n.a. | source of the R subset and of the three slices |
| VisDrone val | real | mixed; 408 of 548 at 1360 × 765 | n.a. / 548 | n.a. | n.a. | 13,969 persons | test set of every single-class model; also the selection split of R |
| R subset of train | real | as train | 1,106 / n.a. | n.a. | 18,858 persons | n.a. | R: the ceiling on VisDrone val, matched to the training tiles of S-nadir-150 by images, not by instances |
| 5 per cent slice of train | real | as train | 324 / n.a. | n.a. | 5,883 persons | n.a. | F-synthetic, F-generic and F-joint at 5 per cent; the schedule grid: whether the cost of the synthetic start belongs to the schedule |
| 10 per cent slice (contains the 5 per cent slice) | real | as train | 647 / n.a. | n.a. | 11,091 persons | n.a. | the same at 10 per cent |
| Selection slice (disjoint from both) | real | as train | n.a. / 324 | n.a. | n.a. | 5,886 persons | checkpoint and schedule selection for the fine-tuning and joint models |
| HERIDAL, every annotated image | real, nadir, 40 to 65 m, 1.5 to 2.4 estimated | 4000 × 3000 | n.a. / 1,647 | n.a. | n.a. | 3,229 persons | zero-shot test of R and of the four synthetic single-class arms; no image enters training or selection |

Notes to Table B2. In VisDrone the pedestrian and people categories are merged into one person class, and the other categories and the annotated ignored regions are dropped from the labels. Of the 1,647 HERIDAL images, 561 contain no person; 3 of the 1,650 annotation files have no image. Figures drawn per frame vary by corpus: 16 to 34 at 150 m and in the oblique corpora, 14 to 30 in S-nadir-75 and its test frames, 12 to 24 in S-nadir-35, its twins and their held-out frames, and 10 to 26 in the pilot. The share of placed figures that survive the visibility filter of Section 4.2.5 of the main text is about 0.70 in the nadir corpora at 150 m, 0.62 to 0.66 at 75 and 35 m, and 0.34 to 0.41 in the oblique corpora, where a tilted frame covers less of the ground over which figures are drawn. S-oblique-six carries only figures carrying nothing. In the tiles the detector sees, counts differ again (4,678 boxes in the 1,106 training tiles of S-nadir-150 against 2,659 in its 149 training frames), because the 20 per cent overlap duplicates boxes along seams and a box with under 40 per cent of its area inside a tile is dropped. R is matched to S-nadir-150 by images, not by instances: 18,858 persons in its 1,106 images against 4,678 boxes in the 1,106 training tiles. The held-out frames at 35 m, at 75 m (Twin-75) and at 150 m (Twin-150) continue the seed of their corpus at the same indices; the 120 per-regime frames continue the seed of S-nadir-150. Three derived training corpora change one setting each. The hard-sun-only corpus repeats the command of S-nadir-150 for 180 frames under hard sun alone, six times its hard-sun frames, and its frames differ from the per-regime test frames. Two replicas of S-oblique-six redraw its six settlements at the same sites with settlement seeds 22 and 23 instead of 21. The learning-curve subsets nest 30, 60, 90 and 120 of the 152 training frames of S-oblique-six, stratified by settlement, with the selection tiles of the full corpus. Besides altitude, six settings changed between the original 75 m corpus and the 35 m corpus that Twin-75 and Twin-150 re-render: the carrying-pose distribution of objects (Table B3a), the share of figures on rooftops (45, then 75 per cent), the figures per frame (14 to 30, then 12 to 24), the render samples (96, then 64 per pixel), the radius of cables and clotheslines (fixed, then scaled to the GSD) and the sampling of figure positions (over the whole ground, then only among rooftops and alley cells inside the frame).

Annotation. A discarded figure (Section 4.2.5 of the main text) remains rendered and therefore counts as background in training, a departure from VisDrone, which annotates occluded persons. Labelling does not depend on the regime (Figure B4), and the three-class corpora record the type of the carried item per instance.

Test sets and derived corpora. The VisDrone test set holds 548 images with 13,969 persons and HERIDAL 1,647 images with 3,229 persons. Three derived training corpora, each changing one setting (a hard-sun-only corpus, two settlement-seed replicas of S-oblique-six and its learning-curve subsets), are described above.

Reproducibility. The figures cannot be regenerated exactly in the three corpora rendered before the figure generator drew from a seeded stream (the pilot corpus, S-nadir-150 and the original 75 m corpus).

### B3. Generator parameters

Layout is produced in three stages.

Parcelling. The built core is subdivided by recursive binary partition. Each split receives a gap drawn as in Table B3; the second band is the alley, or beco, that defines the morphology. Each lot is shrunk by 0.15 m and rotated about its centroid, so a zero gap leaves a seam rather than a shared wall.

Table B3. Gap between lots at each split of the partition.

| Gap | Probability |
|---|---|
| zero (dwellings abut) | 0.82 |
| 0.5 to 1.2 m (alley) | 0.12 |
| 1.3 to 2.0 m | 0.052 |
| 2.3 to 3.1 m | 0.008 |

Orientation. A single partition leaves straight runs of 10 or 20 dwellings. The core is therefore divided by a Voronoi diagram into sub-districts with independent orientations (9 in the settlement of S-nadir-150, 6 to 12 in the other 5), each lot is rotated by up to 0.17 radians, and every corner passes through a smooth domain warp.

Vertical accretion. In most dwellings of 2 or more storeys the upper floor is smaller than the one below and offset to one boundary. Storey count is drawn around a low-frequency noise field with a per-dwelling scatter of 0.95 storeys (SD), so that taller and shorter zones form. Roofs carry water tanks, clotheslines, stair housings, satellite dishes, roofing sheets, rubble and exposed reinforcement bar, and cabling spans between rooftop anchors; these fixtures are the intended main source of local clutter, although no measurement isolates their share of it. Trees come from 4 public-domain models. The six settlements (Figure B2) differ in relief, forest cover, a corridor through the core, the palette of roofs and facades, the extent of the core, the storey distribution and the share of vacant lots; settlement 1 is the one of every single-settlement corpus.

Figure pool. Each rendering run builds a pool of 6 rigged, clothed meshes with MPFB, a MakeHuman derivative. For each body MPFB draws sex, continuous age, musculature, weight, height, proportions, one of 23 skin textures and one of 10 hairstyles; each body receives one of 12 complete outfits. Per instance the generator varies the hue, saturation and value of the outfit and draws a scale between 0.92 and 1.08, a heading and a pose, with noise per bone. Unarmed figures stand (0.36), walk (0.38), sit (0.14) or cross their arms (0.12), and 35 per cent of male instances are shirtless. Figures are placed one at a time, 45 per cent on rooftop slabs (75 per cent in S-nadir-35, its twins and their held-out frames) and the rest in alley cells left free by an occupancy map computed from the footprints; 10 to 34 are drawn per frame, by corpus (Notes to Table B2).

Firearms and objects. Five firearms are built procedurally from boxes and cylinders: 2 rifles (recorded lengths 0.92 and 0.94 m), a carbine (0.62 m), a shotgun (1.05 m) and a pistol (0.20 m). The recorded length of a firearm or object is the length stored with each instance. Against them stand 9 objects spanning 0.88 to 2.5 m: brooms, floor squeegees, plastic pipe, reinforcement bar, planks, closed umbrellas, hoes, rolled mats and hose. Two further firearms, a rifle of 1.10 m and a compact submachine gun of 0.55 m, enter no training corpus and serve only the unseen-weapon test.

Materials. Firearms and objects draw from one palette of 11 materials with fixed colour and roughness. Metal, worn metal, wood, light wood and polymer occur on both kinds, so that dark and metallic surfaces alone cannot separate the classes; PVC, grey PVC, rust, dark cloth, bristle and coloured plastic occur only on objects.

Carrying poses. The item is attached at the right wrist (at the spine when slung) with an orientation fixed per pose rather than solved against the hands, so it does not always sit in the grip. An object whose recorded length exceeds 1.15 m, which no firearm's does, is re-angled in every pose to rest on the shoulder or point to the ground.

Table B3a. Carrying-pose probabilities by corpus family and class.

| Corpus family | Class | Held forward | At the side | Slung on the back | While walking |
|---|---|---|---|---|---|
| Corpora with the five-firearm library (S-oblique and later), except the S-nadir-35 family | armed and object alike | 0.42 | 0.26 | 0.16 | 0.16 |
| S-nadir-35, Twin-75, Twin-150 and their held-out frames | armed | 0.42 | 0.26 | 0.16 | 0.16 |
| S-nadir-35, Twin-75, Twin-150 and their held-out frames | object | 0.08 | 0.34 | 0.28 | 0.30 |

In the S-nadir-35 family the pose distribution therefore differs by class. A detector may separate the classes by length, by the materials only objects have, by carrying angle and, in that family, by pose; these are rules of the generator, not observations of how residents carry things. The carried-as-weapon test, which neutralises carrying angle, was run on S-nadir-75 only.

Earlier weapon library. The pilot corpus and S-nadir-150 carry an earlier library: a rifle in 3 silhouettes, a pistol in 15 per cent of armed figures, every weapon recorded at 0.9 m, and the forward pose drawn with probability 0.46. Every later corpus, S-oblique included, carries the five firearms above.

### B4. Crop-similarity protocol

The crop-similarity measurement asks whether crops of the three classes separate at each GSD without any trained detector. Every annotated figure of the selection split and, where they exist, of the 80 held-out frames is cropped with a margin of 25 per cent of the box on each side and fitted into 224 by 224 pixels. Each crop is embedded by the frozen backbone (layers 0 to 10) of the COCO-pretrained YOLO11s, as the spatial mean of its last feature map (512 dimensions). Vectors are centred by the pool mean and normalised, and similarity is the cosine. Separation is read from the mean cosine between and within classes, the cosine between class centroids, the silhouette, and nearest-centroid and 5-nearest-neighbour classification under 5-fold stratified cross-validation, scored by accuracy, object rate, armed recall, d′ and the AUC for armed against object. The classification is repeated after PCA to 2 and 10 dimensions, after a supervised Fisher projection to 2 dimensions (LDA), with folds drawn by frame, on the two shallower feature maps, and fitted on the training split and applied to the evaluation pool. Intervals are 95 per cent by resampling frames. A supplement, not model-free, repeats the pipeline with the backbone of each trained three-class detector. Here d′ is computed without the log-linear correction of Section 4.7 of the main text, and the detector's d′ quoted beside it is recomputed the same way.

### B5. Scale-matched input sizes, the GSD of HERIDAL and the benchmarks searched

The scale checks match the apparent size of persons as they reach the network to the training corpus. The target is the median long side of the person boxes of S-nadir-150, 20.55 pixels. The input size is the multiple of 32 at which the median long side of the test set's person boxes, after resizing, comes closest to that target, chosen from labels and image sizes alone before any evaluation. For VisDrone val this gives 1,024 pixels (Table C5 reports the result). For HERIDAL, whose median person box has a long side of 71.0 pixels at native resolution, it gives 1,152 pixels, at which the median reaches the network at 20.45 pixels; the protocol size of 1,280 pixels, at which it reaches 22.72, is the secondary measure.

HERIDAL declares a nadir view from 40 to 65 m (Pyrrö et al., 2021) but no camera. Its GSD of 1.5 to 2.4 cm per pixel is an estimate from the declared altitudes, assuming a wide-angle lens of 24 mm equivalent focal length: about 1.5 cm per pixel at 40 m and 2.4 at 65 m, two to three times finer than the 4.88 cm per pixel of the reference acquisition. HERIDAL shows people in Mediterranean scrub, not a city.

Nadir sets found and why none suffices. Zero-shot evaluation on nadir imagery of people would test whether the reversal on HERIDAL holds over built ground and at the target GSD. None of the sets found allows it: the frames of SeaDronesSee from 100 to 260 m show people in the water (Varga et al., 2022); the Stanford Drone Dataset, at about 80 m, shows a university campus (Robicquet et al., 2016); and DLR-ACD, nadir at 4.5 to 15 cm per pixel, is annotated with points, which allows only a counting-style check (Bahmanyar et al., 2019). No public benchmark with person boxes over a city at a nadir view near 5 cm per pixel was found.

Search for weapon benchmarks. The search for aerial weapon benchmarks reported in Section 2.3 of the main text was made in September 2026 in Crossref, arXiv and public dataset repositories, and did not include full-text search of IEEE Xplore, Scopus or Google Scholar.

### B6. Illumination regimes

Each regime fixes together solar irradiance and colour, the angular diameter of the solar disc, a band of solar elevation, sky fill, scattering, aerosols and an exposure offset. Each corpus sweeps the six regimes in order rather than sampling them, so that a small corpus stays balanced, and the regime of every image is recorded.

Table B6. The six illumination regimes: band of solar elevation and angular diameter of the solar disc, the two parameters that separate them physically. Irradiance, colour, sky fill, scattering, aerosols and exposure offset are set jointly per regime and are not tabulated here.

| Regime | Solar elevation (degrees) | Solar disc (degrees) | Character |
|---|---|---|---|
| Hard sun | 46 to 74 | 0.6 | hard shadow edge |
| Low sun | 9 to 25 | 0.9 | sharp shadows |
| Overcast | 30 to 70 | 24 | cast shadow effectively absent |
| Heavy overcast | 28 to 66 | 38 | cast shadow effectively absent |
| Haze | 22 to 52 | 7 | disc between those of the sun regimes and of the overcast regimes |
| Rain | 24 to 60 | 32 | dark, diffuse budget with dense haze; no raindrop or wet surface rendered |

At a disc of 0.6 degrees the shadow edge is hard; above roughly 20 degrees the cast shadow effectively disappears, as under a covered sky. The six regimes over an identical scene are shown in Figure B5.

### Figures B1 to B6

![Figure B1. A generated scene at street level, inside an alley. The view is not used for training; it checks that the layout is three-dimensional built form rather than a texture painted to satisfy a top-down view.](06-resultados/figuras/fig3_beco.jpg)

![Figure B2. The six settlements over which S-nadir-150-six and S-oblique-six spread their 180 frames, one frame of each from S-oblique-six, all under hard sun. Settlement 1 is the one rendered in S-nadir-150.](06-resultados/figuras/fig6_assentamentos.jpg)

![Figure B3. Automatic annotation on four frames of the pilot corpus (1920 by 1080, 9.76 cm per pixel at 150 m). Green marks the armed class, blue the unarmed class; boxes are offset four pixels outward so as not to cover the target. The bottom strip magnifies individual targets five times, with their true size in pixels.](06-resultados/figuras/fig5_anotacao.jpg)

![Figure B4. One annotated frame of the pilot corpus (nadir, 150 m, 1920 by 1080, 9.76 cm per pixel) under each of the six illumination regimes, with the generated boxes: green for armed, blue for unarmed. The labelling does not depend on the regime.](06-resultados/figuras/fig4_dataset.jpg)

![Figure B5. The six illumination regimes over an identical scene and identical framing. Top row: hard sun, low sun, overcast. Bottom row: haze, heavy overcast, rain.](06-resultados/figuras/fig2_climas.jpg)

![Figure B6. The design of the experiments. One generator produces every synthetic corpus. Single-class models are scored on VisDrone against R; three-class models on their selection split and on held-out frames; fine-tuning and joint models on VisDrone. HERIDAL is not drawn.](06-resultados/figuras/fig9_desenho_experimental.png)

## C. Supplementary results

Intervals are 95 per cent: by resampling images on VisDrone val and HERIDAL, by resampling frames on synthetic sets (Section 4.7 of the main text). Differences are the model under test minus the reference. Readings (a), (b) and (c) are those of Section 4.7 of the main text.

### C0. Hypotheses and pre-specified criteria in full

The protocol grew in three stages, so each check carries one of three labels (Section 4.6 of the main text): confirmatory, pre-specified follow-up or exploratory.

Table C0. Hypotheses H1 to H23, numbered as in Table C0a, with measure, models and data, status (Section 4.6 of the main text) and pre-specified criterion in full. Readings (a), (b) and (c) are those of Section 4.7 of the main text.

<!--TAB:rq|Hypotheses H1 to H23, numbered as in Table C0a, with measure, models and data, status (Section 4.6) and pre-specified criterion. Readings (a), (b) and (c) are those of Section 4.7.-->

| ID | RQ | Hypothesis | Measure | Models and data | Status | Criterion |
|---|---|---|---|---|---|---|
| H1 | RQ1 | The reference model R is valid | mAP50 | R; VisDrone | Confirmatory | Valid unless R is near chance |
| H2 | RQ1 | Synthetic-only training recovers a fraction of the ceiling, not an artefact of scale | share of R at 1,280 and at the scale-matched size | S-nadir-150; VisDrone | Confirmatory | Scale a confound if the scale-matched share differs from the protocol share by more than half of it |
| H3 | RQ1 | Camera geometry moves the share: S-oblique above S-nadir-150 | mAP50; share of R | S-nadir-150 and S-oblique, three seeds each; VisDrone | Confirmatory | Geometry load-bearing if S-oblique is above S-nadir-150 by the readings of Section 4.7; otherwise the limitation lies in synthesis |
| H4 | RQ1 | The oblique advantage reflects the oblique geometry of VisDrone and shrinks or reverses on a nadir set | mAP50; share of R | R; S-nadir-150 and S-oblique, three seeds each; HERIDAL | Confirmatory | Not interpretable if R falls below 0.05; S-oblique against S-nadir-150 at the matched input size by the readings of Section 4.7; scale-dependent if the order differs at 1,280 pixels |
| H5 | RQ1 | Settlement variety at nadir raises the share | mAP50 | S-nadir-150-six; S-nadir-150, three seeds; VisDrone | Pre-specified follow-up | Readings of Section 4.7 against the three seeds of S-nadir-150 |
| H6 | RQ1 | The oblique bundle of four settings raises the share | mAP50 | S-oblique-six and S-oblique, three seeds each; VisDrone | Pre-specified follow-up | Readings of Section 4.7 on three seeds per side; S-oblique-six is a best of four on this set |
| H7 | RQ1 | Six settlements stay above one across settlement seeds | mAP50; range over settlement seeds compared with range over training seeds | S-oblique-six, settlement seeds 21 to 23; S-oblique; VisDrone | Pre-specified follow-up | Readings of Section 4.7; the scene dominates the dispersion if its range exceeds twice that of the training seeds |
| H8 | RQ1 | The number of training frames is operant | mAP50 at 152 and at 30 frames | S-oblique-six and its 30-frame subset, three seeds each; VisDrone | Pre-specified follow-up | Operant if 152 frames lie above 30 in readings (a) and (b); otherwise the answer to RQ1 is a property of the generator |
| H9 | RQ1 | The curve still rises at 152 frames | mAP50 at 152 and at 120 frames | S-oblique-six and its 120-frame subset, three seeds each; VisDrone | Pre-specified follow-up | Rising if (a) and (b); flat if neither; rising within training dispersion if (b) only |
| H10 | Secondary: illumination (synthetic only) | A model trained on all regimes does better under overcast than under hard sun, because cast shadow clutters the background | mAP50 per regime; recall at confidence 0.25 | S-nadir-150; 120 held-out frames | Confirmatory | Mechanism withdrawn if overcast is not above both hard sun and rain, or hard sun is not among the two weakest regimes (on point estimates; intervals reported descriptively) |
| H11 | Secondary: illumination (synthetic only) | The hard-sun deficit belongs to the regime, not to its share of training | recall at confidence 0.25 (D-i, D-ii); mAP50 | hard-sun-only model and S-nadir-150; held-out frames under hard sun and overcast | Pre-specified follow-up | The deficit belongs to the regime if the interval of D-ii (Section 4.6 of the main text) lies wholly below zero and the specialist's mAP50 under hard sun stays below the 0.791 of the model of all regimes under overcast; otherwise it belongs to the share of hard sun in training. An interval that includes zero means that the regime explanation is not supported, not that the share explanation is demonstrated |
| H12 | RQ2 | Synthetic pretraining adds accuracy, most at 5 per cent | difference in mAP50 | F-synthetic against F-generic, original schedule; VisDrone | Pre-specified follow-up | F-synthetic above F-generic, the difference largest at 5 per cent (expectation recorded before the runs) |
| H13 | RQ2 | The cost of the synthetic start does not belong to the schedule | difference in mAP50 | F-synthetic and F-generic on the schedule grid; VisDrone | Pre-specified follow-up | Robust if F-generic stays above F-synthetic at both volumes by the readings of Section 4.7, each start on the schedule chosen on the selection split; the control run must reproduce the original F-generic at 5 per cent within 0.0035, the SD of its three seeds |
| H14 | RQ2 | Joint training adds accuracy | difference in mAP50 | F-joint against F-generic; VisDrone | Pre-specified follow-up | F-joint above F-generic by more than twice the SD of the three F-generic runs at 5 per cent (margin borrowed at 10 per cent) |
| H15 | RQ2 | Joint training differs from the synthetic start | difference in mAP50 | F-joint against F-synthetic; VisDrone | Exploratory | None |
| H16 | RQ3 | At 2.44 cm per pixel the distinction does not rest on the asset library | armed recall on unseen compared with seen firearms | S-nadir-75; 50 held-out frames | Confirmatory | Claim at 2.44 withdrawn if recall on unseen firearms falls below four fifths of recall on seen ones |
| H17 | RQ3 | Objects carried as weapons are called armed more often | paired object rate | S-nadir-75; 50 held-out frames in two renders | Confirmatory | Carrying-angle caveat withdrawn if the paired rate does not rise (exact McNemar test) |
| H18 | RQ3 | A three-class model at 4.88 cm per pixel is valid | share of annotated figures found | Twin-150; selection split and 80 held-out frames | Confirmatory | At least half of the annotated figures found on both sets; remedies pre-specified (Section 4.6 of the main text) |
| H19 | RQ3 | Armed figures and objects separate at 4.88 cm per pixel | d′ | Twin-150; 80 held-out frames | Confirmatory | Interval of d′ includes zero: absence measured; excludes zero: separation read as resting on a cue other than the firearm's form (Section 4.6 of the main text) |
| H20 | RQ3 | Separation differs between 4.88 and 2.44 cm per pixel | d′; object rate | Twin-150 against Twin-75; 80 matched held-out frames | Confirmatory | Readings (b) and (c) |
| H21a | RQ3 | With every other setting held, the object rate differs between 1.14 and 2.44 cm per pixel, on held-out frames | object rate | S-nadir-35 against Twin-75, three seeds each; 80 held-out frames per corpus | Confirmatory | Established if the S-nadir-35 rate exceeds that of Twin-75 on the held-out frames at two-sided p below 0.05, unadjusted for clustering by frame; withdrawn if reversed; suggestive otherwise |
| H21b | RQ3 | The same comparison on the selection splits | object rate | S-nadir-35 against Twin-75, three seeds each; selection splits | Exploratory | None (reported without p-value) |
| H22 | RQ3 | Armed and unarmed rates differ between 1.14 and 2.44 cm per pixel | armed recall; rate at which unarmed figures are called armed | S-nadir-35 against Twin-75; selection splits and held-out frames | Exploratory | None |
| H23 | RQ3 | S-nadir-35 differs from the original S-nadir-75 | object rate | S-nadir-35 against S-nadir-75; selection splits | Exploratory | None |

Table C0a. Hypotheses H1 to H23: research question, status (Section 4.6 of the main text), pre-specified criterion in short (in full: Table C0), outcome and the readings of Section 4.7 of the main text its headline difference passes, (a) seed ranges, (b) paired interval, (c) 30 per cent; n.a.: not applicable. The six headline comparisons (H3, H4, H13, H19, H20, H21a) are repeated in Section 5.6 of the main text.

| ID | RQ | Hypothesis (short label) | Status | Criterion (short) | Outcome | Resolvable (a / b / c) |
|---|---|---|---|---|---|---|
| H1 | RQ1 | R is a valid ceiling | Confirmatory | Valid unless R scores near chance | held: 0.6311 | n.a. |
| H2 | RQ1 | Synthetic-only training recovers a fraction of R; scale check | Confirmatory | Scale confound if the scale-matched share differs from the protocol share by over half | held: 2.2% of R on three runs; scale-matched share differed by about a third (2.19 against 1.62 per cent) | n.a. |
| H3 | RQ1 | Camera geometry: S-oblique above S-nadir-150 | Confirmatory | Geometry load-bearing if S-oblique exceeds S-nadir-150 by the readings; otherwise synthesis limits | held: +0.0419, ratio 4.08 | yes / yes / yes, 307.9% |
| H4 | RQ1 | The oblique advantage shrinks or reverses on HERIDAL | Confirmatory | Uninterpretable if R falls below 0.05; S-oblique against S-nadir-150 at matched size | held, order reversed: -0.0656, ratio 0.67; same order at 1,280 | no, ranges overlap / yes / yes, 48.9% |
| H5 | RQ1 | Settlement variety at nadir: S-nadir-150-six against S-nadir-150 | Pre-specified follow-up | Readings against the three seeds of S-nadir-150 | +0.0054 on three nadir runs | inside the three-run range / yes / yes, 39.9% |
| H6 | RQ1 | S-oblique-six against S-oblique (four settings changed) | Pre-specified follow-up | Readings on three seeds per side; S-oblique-six is a best of four | +0.0411 on three runs per side | yes / yes / yes, 74.0% |
| H7 | RQ1 | Bundle gain across settlement seeds | Pre-specified follow-up | Readings; scene dominates if its range exceeds twice the training-seed range | held: +0.0381; settlement-seed range 1.4 times the training-seed range | yes / yes / yes, 68.7% |
| H8 | RQ1 | 152 frames above 30 | Pre-specified follow-up | Operant if 152 frames exceed 30 in readings (a) and (b) | held: +0.0349 | yes / yes / yes, 56.5% |
| H9 | RQ1 | End of the curve: 152 against 120 frames | Pre-specified follow-up | Rising if (a) and (b); flat if neither; within dispersion if (b) only | +0.0062, interval reading only; 0.0140 per doubling | no, ranges overlap / yes / no, 6.9% |
| H10 | Secondary | Illumination: overcast above hard sun and rain; hard sun among the two weakest | Confirmatory | Withdrawn unless overcast exceeds hard sun and rain, and hard sun ranks among two weakest (on point estimates; intervals reported descriptively) | held on point estimates; overcast above hard sun resolvable on recall, overcast above rain not; no interval on mAP50 by regime | n.a. / hard sun yes, rain no / n.a. |
| H11 | Secondary | The hard-sun deficit is intrinsic to the regime | Pre-specified follow-up | Regime explanation if the D-ii interval lies below zero and specialist mAP50 below 0.791 | failed: regime explanation not supported, -0.0572 (-0.1252 to +0.0067); D-i: specialist +0.0818 on the same frames | n.a. / no / no, 6.5% on mAP50 |
| H12 | RQ2 | Synthetic pretraining adds accuracy, most at 5% | Pre-specified follow-up | F-synthetic above F-generic, largest at 5 per cent (expectation recorded before the runs) | failed: F-synthetic lower by 0.0716 at 5% and 0.0614 at 10% | 5%: yes / yes / no, 15.8%; 10%: n.a. / yes / no, 12.1% |
| H13 | RQ2 | The cost of the synthetic start is robust to the schedule | Pre-specified follow-up | Robust if F-generic stays above at both volumes; control run within 0.0035 | held: F-synthetic lower by 0.1369 at 5% and 0.1129 at 10% | 5%: yes / yes / yes, 30.2%; 10%: n.a. / yes / no, 22.2% |
| H14 | RQ2 | Joint training adds accuracy | Pre-specified follow-up | F-joint above F-generic by more than twice the SD of F-generic at 5 per cent | failed: F-joint lower by 0.0637 at 5% and 0.0281 at 10%, beyond the margin | 5%: joint outside the generic range / yes / no, 13.8%; 10%: n.a. / yes / no, 5.2% |
| H15 | RQ2 | F-joint against F-synthetic | Exploratory | None | F-joint higher by 0.0078 at 5% and 0.0333 at 10% | 5%: joint inside the synthetic range / yes on the mean, no on two of three seeds / no, 1.7%; 10%: n.a. / yes / no, 6.5% |
| H16 | RQ3 | At 75 m the armed call does not depend on the firearm asset | Confirmatory | Withdrawn if unseen-firearm recall falls below four fifths of seen-firearm recall | held: ratio 1.16 (0.88 to 1.54), above 0.80 | n.a. |
| H17 | RQ3 | Objects carried as weapons are called armed more often | Confirmatory | Angle caveat withdrawn if the paired rate does not rise (exact McNemar test) | failed: paired rate did not rise (0.154 as normally carried, 0.137 as weapons), p = 0.56 (unadjusted for clustering by frame) | n.a. |
| H18 | RQ3 | Validity of the three-class model at 4.88 cm per pixel | Confirmatory | At least half of annotated figures found on both sets; remedies pre-specified | first model 0.498, not interpretable; trained for longer as pre-specified, held: 0.606 and 0.663 | n.a. |
| H19 | RQ3 | Separation at 4.88 cm per pixel | Confirmatory | Interval includes zero: absence measured; excludes zero: separation rests on a non-form cue | separation above chance, d′ 0.58 (0.38 to 0.78); read under its criterion in Section 6.1 of the main text | n.a. / yes, excludes zero / n.a. |
| H20 | RQ3 | 4.88 against 2.44 cm per pixel, matched held-out frames | Confirmatory | Readings (b) and (c) | d′ lower by 0.394, object rate higher by 0.120 | n.a. / yes / yes, 68.0% and 96.2% |
| H21a | RQ3 | Object rate, 1.14 against 2.44 cm per pixel, held-out frames | Confirmatory | Established if S-nadir-35 exceeds Twin-75 at two-sided p below 0.05; withdrawn if reversed | held: +0.128, p = 0.0001 (unadjusted for clustering by frame); +0.087 on seed means | yes / yes / yes, 64.9% |
| H21b | RQ3 | Object rate, 1.14 against 2.44 cm per pixel, selection split | Exploratory | None (reported without p-value) | +0.108; +0.068 on seed means | no, ranges overlap / yes / yes, 38.1% |
| H22 | RQ3 | Armed and unarmed rates, S-nadir-35 against Twin-75 | Exploratory | None | not resolvable: the held-out armed difference reverses in seed 2 and the unarmed difference excludes zero in no seed | no / no / n.a. |
| H23 | RQ3 | S-nadir-35 against the original S-nadir-75 | Exploratory | None | not resolvable: +0.036 (-0.059 to +0.124); order reverses at IoU 0.60 and 0.75 | n.a. / no / no, 15.1% |

### C1. Single-class and three-class models at a glance

Table C1. Every model with its test set and headline figure. VisDrone val: mAP50 with its interval and the share of R on the same resamples; where a model was trained three times, the mean of the three runs with its interval, and the best run. HERIDAL rows at the matched input size of 1,152 pixels. Three-class models: three-class mAP50 on the selection split and the object rate at confidence 0.25 on the selection split and on held-out frames.

| Model | Training data (real images) | Test set | mAP50 (95% interval) | Share of R (95% interval) |
|---|---|---|---|---|
| R | 1,106 images of VisDrone-DET train (1,106) | VisDrone val | 0.6311 (0.6149 to 0.6471) | ceiling |
| S-nadir-150, mean of 3 seeds (best run) | 180 frames, 1 settlement, nadir, 4.88 cm/px (0) | VisDrone val | 0.0136 (0.0120 to 0.0160); best 0.0198 | 2.2% (1.9 to 2.5); best 3.1% |
| S-nadir-150-six | 180 frames, 6 settlements, nadir, 4.88 cm/px (0) | VisDrone val | 0.0190 (0.0142 to 0.0211) | 3.0% (2.3 to 3.3) |
| S-oblique, mean of 3 seeds (best run) | 180 frames, 1 settlement, oblique, 3.90 cm/px nominal (0) | VisDrone val | 0.0555 (0.0502 to 0.0614); best 0.0614 | 8.8% (8.1 to 9.6); best 9.7% |
| S-oblique-six, mean of 3 seeds (best run) | 180 frames, 6 settlements, pitch 45 to 56 degrees (0) | VisDrone val | 0.0966 (0.0896 to 0.1048); best 0.1055 | 15.3% (14.4 to 16.5); best 16.7% |
| F-synthetic, original schedule; 5%: mean of 3 seeds (best run); 10%: one run | from S-oblique-six (324 and 647) | VisDrone val | 5%: 0.4529 (0.4373 to 0.4696), best 0.4608; 10%: 0.5095 (0.4935 to 0.5264) | 5%: 71.8%; 10%: 80.7% (79.3 to 82.1) |
| F-generic, original schedule; 5%: mean of 3 seeds (best run); 10%: one run | from COCO weights (324 and 647) | VisDrone val | 5%: 0.5245 (0.5075 to 0.5424), best 0.5285; 10%: 0.5709 (0.5535 to 0.5883) | 5%: 83.1%; 10%: 90.5% (89.2 to 91.6) |
| F-generic, lower learning rate (chosen on the selection slice); 5%: mean of 3 seeds; 10%: one run | from COCO weights (324 and 647) | VisDrone val | 5%: 0.5897 (0.5748 to 0.6073); 10%: 0.6224 (0.6072 to 0.6396) | 5%: 93.4% (92.3 to 94.8); 10%: 98.6% (97.4 to 100.1) |
| F-joint, one run at each volume | COCO weights, 890 synthetic tiles and the real images (324 and 647) | VisDrone val | 5%: 0.4607 (0.4444 to 0.4789); 10%: 0.5428 (0.5259 to 0.5610) | 5%: 73.0% (71.6 to 74.6); 10%: 86.0% (84.8 to 87.4) |
| R on HERIDAL | as above (1,106) | HERIDAL, 1,647 images | 0.3185 (0.2843 to 0.3543) | reference model (100%) |
| S-nadir-150 on HERIDAL, mean of 3 seeds | as above (0) | HERIDAL | 0.1997 (0.1713 to 0.2306) | 62.7% |
| S-oblique on HERIDAL, mean of 3 seeds | as above (0) | HERIDAL | 0.1341 (0.1149 to 0.1555) | 42.1% |
| S-nadir-75 | 200 frames, 3 classes, 2.44 cm/px (0) | selection split, 27 frames; held-out, 50 | 0.579; object rate 0.237; held-out 0.152 | not applicable |
| S-nadir-35 | 200 frames, 3 classes, 1.14 cm/px (0) | selection split, 35; held-out, 80 | 0.514; object rate 0.273; held-out 0.253 | not applicable |
| Twin-75 | the S-nadir-35 corpus at 2.44 cm/px (0) | selection split, 24; held-out, 80 | 0.508; object rate 0.165; held-out 0.125 | not applicable |
| Twin-150, trained for longer | the S-nadir-35 corpus at 4.88 cm/px (0) | selection split, 27; held-out, 80 | 0.388; object rate 0.178; held-out 0.245 | not applicable |

Notes to Table C1. The 5 per cent cells of F-synthetic and F-generic are means over three training seeds; the share of R of a mean is given without an interval. The first training run alone scored 0.4424 for F-synthetic at 5 per cent, a share of R of 70.1% (68.4 to 71.8), and 0.5220 for F-generic, 82.7% (81.4 to 84.1). On HERIDAL R is a reference model trained on VisDrone, not a ceiling. Two robustness checks apply to every single-class score (Section 5.6 of the main text reports them). Each score is recomputed under the rule of the official VisDrone toolkit, which drops a detection with half or more of its area inside an ignored region (the validator counts it as a false positive), and at IoU 0.60 and 0.75; an ordering that reverses with the IoU threshold is treated as an artefact of annotation and reported at all three.

These are the figures displaced from Section 5.6 of the main text. Under the official toolkit rule for ignored regions every single-class mAP50 rose slightly (R to 0.6548, the first run of S-oblique-six to 0.1074) and every share of R fell slightly (S-oblique-six from 16.7 to 16.4 per cent). No pair fixed for the IoU check changed order between 0.50, 0.60 and 0.75 under either rule. Two other comparisons reversed: at 10 per cent F-joint fell below F-synthetic at 0.75 (0.0983 against 0.1025), and S-nadir-35 fell below the original S-nadir-75 at 0.60 and 0.75 (object rates 0.223 and 0.132 against 0.230 and 0.141).

### C2. Target size and apparent shape

Table C2. Height-to-width ratio of the annotated box by camera pitch in S-oblique (120 m, 3.90 cm per pixel nominal), from the full-frame labels.

| Pitch recorded per image | Instances | Median h/w, all figures | Median h/w, figures carrying nothing |
|---|---|---|---|
| 26 to 30 degrees | 482 | 1.28 | 1.35 |
| 30 to 35 degrees | 512 | 1.41 | 1.50 |
| 35 to 40 degrees | 231 | 1.49 | 1.58 |
| 40 to 45 degrees | 359 | 1.64 | 1.82 |
| 45 to 50 degrees | 222 | 1.64 | 1.78 |
| 50 to 52 degrees | 106 | 1.70 | 1.97 |

The ratio rose with pitch from 1.28 to 1.70, not strictly between 40 and 50 degrees. For figures carrying nothing it reached the 1.95 of VisDrone's training split only between 50 and 52 degrees, where it measured 1.97 on 49 figures. S-oblique as rendered realised 1.46 rather than the 1.95 it was calibrated for, its armed figures measuring 1.38 against 1.58 for figures carrying nothing; S-oblique-six realised 1.85 at 13.3 by 25.2 pixels. The two nadir corpora, which differ by a factor of 2 in render resolution and of 6 in instance count, agreed on the ratio to the second decimal (0.98).

Table C2a. Target size and shape by corpus, from full-frame labels at native resolution; the last numeric column is the share of instances whose shorter side falls below one detector stride (8 pixels). Pilot row: training split.

| Corpus and geometry | GSD (cm/px) | Median width x height (px) | Median long side | Median area (px²) | Median h/w | Shorter side below 8 px | Instances |
|---|---|---|---|---|---|---|---|
| Pilot corpus, nadir, 1920 by 1080 | 9.76 | 8.3 x 8.2 | 10.1 px | 69 | **0.98** | 66.9% | 565 |
| S-nadir-150, nadir | 4.88 | 17.6 x 17.5 | 20.6 px | 301 | **0.98** | 0.8% | 3,225 |
| S-oblique, pitch 26 to 52 degrees | 3.90 nominal | 17.9 x 26.4 | not measured | 456 | **1.46** | not measured | 1,912 |
| S-oblique-six, pitch 45 to 56 degrees, figures carrying nothing | 3.90 nominal | 13.3 x 25.2 | not measured | 324 | **1.85** | not measured | 1,521 |
| S-nadir-75, nadir | 2.44 | 47.6 x 41.7 | not measured | 1,917 | **0.88** | not measured | 2,887 |
| S-nadir-35, nadir | 1.14 | 121.8 x 103.1 | not measured | 12,160 | **0.84** | not measured | 2,223 |
| Twin-75, nadir | 2.44 | 48.4 x 41.5 | not measured | 1,964 | **0.87** | not measured | 2,257 |
| VisDrone-DET train, real acquisition | not recorded | 13.0 x 24.0 | 24.0 px | 304 | **1.95** | 26.5% | 106,396 |
| VisDrone-DET val, real acquisition | not recorded | 12.0 x 25.0 | 25.0 px | 288 | **2.20** | 30.5% | 13,969 |

On the matched twins the median box measured 48 by 41 pixels at 2.44 and 21 by 20 at 4.88 cm per pixel, about 4.7 times the area. At 4.88 cm per pixel the median VisDrone instance, training and validation splits pooled, covered 300 square pixels, with a long side of 24.0 pixels. All sizes in Tables C2 and C2a are at native resolution, before the resizing of Section 4.5 of the main text.

### C3. Contrast and detection by illumination regime

Table C3. Figure-to-background contrast by regime in the pilot corpus (nadir, 150 m, 9.76 cm per pixel): mean frame luminance, raw luminance difference in digital numbers (DN), contrast against local clutter aggregated per frame, and its dispersion between frames; 684 instances over 48 frames, 8 per regime.

| Regime | Mean frame luminance | Raw difference (DN) | Contrast over clutter, median per frame | SD between frames | Instances |
|---|---|---|---|---|---|
| Hard sun | 87.0 | 15.2 | **0.64** | 0.14 | 113 |
| Low sun | 56.0 | 9.0 | 0.70 | 0.20 | 117 |
| Overcast | 84.6 | **16.4** | **0.88** | 0.26 | 122 |
| Haze | 94.4 | 9.6 | 0.79 | 0.25 | 113 |
| Heavy overcast | 55.6 | 11.2 | 0.72 | 0.38 | 91 |
| Rain | 35.1 | 6.6 | **0.63** | 0.12 | 128 |

Contrast is the mean luminance inside the box minus the mean of a 6 pixel ring around it, divided by the SD of that ring; instances within one image are not independent, so the statistic is aggregated per image. Overcast gave both the largest raw difference and the largest contrast over clutter; hard sun and rain were the two lowest on the latter, hard sun while sitting second on raw contrast. With 8 frames per regime and a between-frame dispersion of 0.12 to 0.38, only the gap between the extremes approached one SD; the order of the four intermediate regimes was not resolvable at this sample size. The measurement was made on the pilot corpus at 9.76 cm per pixel, not on S-nadir-150.

Exploratory reading. Zero-shot on VisDrone val, the hard-sun-only model scored 0.0072 against 0.0102 for the first run of S-nadir-150.

Table C3a. Experiment D: per-regime mAP50 and recall at 0.25 on 120 held-out frames of S-nadir-150 (20 per regime), for S-nadir-150 and the hard-sun specialist, 95 per cent intervals by resampling frames; contrast measured on the pilot corpus.

<!--TAB:regimes|Experiment D: per-regime mAP50 and recall at 0.25 on 120 held-out frames of S-nadir-150 (20 per regime), for S-nadir-150 and the hard-sun specialist, 95 per cent intervals by resampling frames; contrast measured on the pilot corpus.-->

| Regime | mAP50, all regimes | Recall at 0.25, all regimes (95% interval) | mAP50, hard sun only | Recall at 0.25, hard sun only | Contrast over clutter, pilot corpus (median per frame) | SD between frames |
|---|---|---|---|---|---|---|
| Hard sun | 0.675 | 0.657 (0.591 to 0.720) | 0.742 | 0.739 | **0.64** | 0.14 |
| Heavy overcast | 0.755 | 0.768 (0.714 to 0.816) | 0.754 | 0.749 | 0.72 | 0.38 |
| Rain | 0.759 | 0.789 (0.748 to 0.827) | 0.728 | 0.747 | **0.63** | 0.12 |
| Haze | 0.780 | 0.726 (0.697 to 0.757) | 0.652 | 0.569 | 0.79 | 0.25 |
| Low sun | 0.790 | 0.814 (0.768 to 0.854) | 0.794 | 0.776 | 0.70 | 0.20 |
| Overcast | 0.791 | 0.796 (0.760 to 0.827) | 0.796 | 0.759 | **0.88** | 0.26 |

Experiment D in detail. Overcast was the strongest regime on mAP50, level with low sun (0.791 and 0.790), though its margin over rain lay within the recall intervals. The mAP50 of hard sun lay 0.080 below the next regime, and its recall interval lay wholly below those of overcast, rain and low sun while overlapping those of haze and heavy overcast. Low sun scored highest on recall. The ordering by detection matched the ordering by contrast over clutter at the two extremes, overcast and hard sun, and not among the intermediate regimes. The hard-sun specialist, although no longer resolvably below the model of all regimes under overcast in recall (D-ii), kept an mAP50 6.5 per cent lower. The specialist gained +0.0818 (+0.0377 to +0.1243) of recall under hard sun over the model of all regimes on the same 20 frames (D-i); against the model of all regimes under overcast (D-ii) the difference was -0.0572 (-0.1252 to +0.0067). The recall intervals by regime are those of Table C3a: 0.657 (0.591 to 0.720) under hard sun and 0.796 (0.760 to 0.827) under overcast for the model of all regimes. An interval of D-ii that includes zero means that the regime explanation is not supported, not that the share explanation is demonstrated.

### C4. The pilot

Table C4. The pilot of the protocol: a two-class model trained on 40 frames rendered at 1920 by 1080 (9.76 cm per pixel), scored on its own selection split and zero-shot on VisDrone val.

| Pilot run | Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| Pilot model (nadir, 150 m), 40 training frames at 1920 × 1080 | synthetic selection split | 0.109 | 0.148 | 0.077 | 0.019 |
| same model | VisDrone val, zero-shot | 0.038 | 0.031 | 0.0055 | 0.0020 |

The pilot, an exploratory run on 40 training frames at 9.76 cm per pixel with the earlier recipe of Table B1, failed on its own domain: 0.077 on its own selection split, a two-class mean not on the single-class scale of the other models, against 0.7915 for S-nadir-150. At 9.76 cm per pixel the median long side of the box was 10.1 pixels and 66.9 per cent of instances had a shorter side below 8 pixels.

### C5. The ceiling and the nadir arm in detail

Table C5. R, S-nadir-150 (first training seed) and S-nadir-150-six on their own selection split and on VisDrone val. Precision and recall at the F1-maximising confidence.

| Model | Evaluation set | Precision | Recall | mAP50 (95% interval) | mAP50-95 | Share of R (95% interval) |
|---|---|---|---|---|---|---|
| R (1,106 real training images; checkpoint selected on the test split) | VisDrone val | 0.7312 | 0.5729 | 0.6311 (0.6149 to 0.6471) | 0.2538 | ceiling |
| S-nadir-150, seed 0 | synthetic selection split | 0.8707 | 0.7413 | 0.7915 | 0.3656 | n.a. |
| S-nadir-150, seed 0 | VisDrone val, zero-shot | 0.0856 | 0.0421 | 0.0102 (0.0087 to 0.0133) | 0.0025 | 1.6% (1.4 to 2.1) |
| S-nadir-150-six | synthetic selection split | not reported | not reported | 0.6786 | not reported | n.a. |
| S-nadir-150-six | VisDrone val, zero-shot | not reported | not reported | 0.0190 (0.0142 to 0.0211) | 0.0071 | 3.0% (2.3 to 3.3) |

Further runs on the selection split. S-nadir-150 with seeds 1 and 2 scored 0.794 and 0.810 on its selection split (0.0198 and 0.0108 on VisDrone val); S-oblique with seeds 1 and 2 scored 0.764 and 0.736 (0.0552 and 0.0501); the first run of S-oblique-six scored 0.7047 on its selection split and, on VisDrone val, precision 0.2631, recall 0.1716 and mAP50-95 0.0329.

Scale check. The median long side of VisDrone's person boxes reached the network at 25.33 pixels at the protocol's input size of 1,280 and at 20.27 pixels at 1,024, while the median area fell from 283 to 181 square pixels. At 1,024 pixels the first run of S-nadir-150 scored 0.0128 and R 0.5849, a share of R of 2.2 rather than 1.6 per cent: the model's mAP50 rose by a quarter (0.0026 on 0.0102) and its share of R by about a third (2.19 against 1.62 per cent), against the pre-specified half.

Ignored regions. Under the official VisDrone toolkit rule (a box with half or more of its area inside an ignored region is dropped), R rose to 0.6548 and the first run of S-oblique-six to 0.1074, whose share of R fell from 16.7 to 16.4 per cent.

A run of R on the full VisDrone training split was started and stopped before completion; no result of it is reported.

### C6. Experiment A per seed and first-run comparisons

Table C6, panel A. Zero-shot mAP50 on VisDrone val for each training seed and the mean of three, and for S-oblique-six also two further settlement seeds (training seed 0).

| Model | mAP50 on VisDrone val (95% interval) | Share of R (95% interval) |
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

Settlement seed. The range over the three settlement seeds, 0.0821 to 0.1055, was 0.0234 wide, 1.4 times the range over training seeds (0.0168), below the pre-specified factor of two.

Comparisons between first runs. The main text compares means over three training seeds; the comparisons between first runs, made before the further seeds existed, are these. S-nadir-150-six against the first run of S-nadir-150: +0.0088 (+0.0038 to +0.0102), a ratio of 1.87 (1.31 to 2.07) and a relative difference of 86.6 per cent of the smaller value. S-oblique against S-nadir-150, first run of each: +0.0511 (+0.0447 to +0.0567), a ratio of 6.01 (4.57 to 7.01). S-oblique-six against S-oblique, first run of each: +0.0441 (+0.0383 to +0.0514). For seeds 1 and 2 alone, the ratio of S-oblique to S-nadir-150 was 2.79 and 4.64. In the comparison of S-oblique with S-nadir-150 the median height-to-width ratio moved from 0.98 to 1.46 and the median area from 301 to 456 square pixels.

Table C6, panel B. Zero-shot person detection on HERIDAL (1,647 images, 3,229 persons, nadir from 40 to 65 m) at the matched input size of 1,152 pixels and at the protocol size of 1,280: mAP50 on the mean of the training runs where a model was trained three times, the range over those runs, and the share of R, which was trained on VisDrone.

| Model | Runs | mAP50 at 1,152 (95% interval) | Range over runs | Share of R | mAP50 at 1,280 |
|---|---|---|---|---|---|
| R (1,106 real images of VisDrone-DET train) | 1 | 0.3185 (0.2843 to 0.3543) | one run | 100% | 0.3353 |
| S-nadir-150 | 3 | 0.1997 (0.1713 to 0.2306) | 0.0926 to 0.2672 | 62.7% | 0.1682 |
| S-nadir-150-six | 1 | 0.2488 (0.2116 to 0.2865) | one run | 78.1% | 0.2208 |
| S-oblique | 3 | 0.1341 (0.1149 to 0.1555) | 0.1092 to 0.1476 | 42.1% | 0.1422 |
| S-oblique-six | 3 | 0.1477 (0.1265 to 0.1715) | 0.1079 to 0.1847 | 46.4% | 0.1418 |

On HERIDAL, S-oblique against S-nadir-150 on the means of three runs was -0.0656 (-0.0840 to -0.0471), a ratio of 0.67 (0.61 to 0.74), passing readings (b) and (c) and not (a), since the runs overlap. S-oblique-six against S-nadir-150-six was -0.1012 (-0.1216 to -0.0786), passing (b) and (c). At the secondary size of 1,280 pixels the order was the same, -0.0260 (-0.0414 to -0.0097) between the single-settlement arms, passing reading (b) only.

### C7. Precision-recall operating points

Table C7. Operating points on VisDrone val for the four models of Figure C1: confidence, precision, recall and F1 at the F1 maximum (smoothed as the validator does), and precision and recall at the default prediction confidence of 0.25.

| Model | Confidence at max F1 | Precision | Recall | F1 | Precision at 0.25 | Recall at 0.25 |
|---|---|---|---|---|---|---|
| R | 0.2963 | 0.7312 | 0.5729 | 0.6424 | 0.6731 | 0.6036 |
| F-generic 10% | 0.3193 | 0.6823 | 0.5160 | 0.5876 | 0.5698 | 0.5757 |
| F-synthetic 10% | 0.2983 | 0.6372 | 0.4579 | 0.5328 | 0.5535 | 0.4986 |
| S-oblique-six, seed 0 | 0.2152 | 0.2631 | 0.1716 | 0.2077 | 0.2804 | 0.1625 |

Figure C1 draws the precision-recall curves of R, the first run of S-oblique-six, and F-generic and F-synthetic at 10 per cent. The three curves with real training data kept the same order over the whole range of recall; the zero-shot curve of S-oblique-six fell below a precision of 0.6 at 1 per cent recall and ended at a recall of 0.39.

![Figure C1. Precision-recall curves at IoU 0.50 on VisDrone-DET val for R, S-oblique-six (first run, zero-shot), and F-generic and F-synthetic at 10 per cent; the marker is the F1-maximising confidence (Section 4.7 of the main text).](06-resultados/figuras/fig11_pr_visdrone.png)

### C8. Learning curve

Table C8. Learning curve of S-oblique-six over the number of training frames: nested subsets stratified by settlement, the same selection tiles, 60 epochs, zero-shot mAP50 on VisDrone val by training seed, with the mean over seeds, its interval and the share of R of the mean. Means and differences are computed before rounding.

| Training frames (tiles) | mAP50 by training seed | Mean (95% interval) | Range | Share of R of the mean |
|---|---|---|---|---|
| 30 (182) | 0.0499, 0.0674, 0.0679 | 0.0618 (0.0566 to 0.0679) | 0.0499 to 0.0679 | 9.8% |
| 60 (341) | 0.0806 | 0.0806 (0.0739 to 0.0885) | one run | 12.8% |
| 90 (503) | 0.0810 | 0.0810 (0.0745 to 0.0886) | one run | 12.8% |
| 120 (696) | 0.0915, 0.0878, 0.0918 | 0.0904 (0.0838 to 0.0986) | 0.0878 to 0.0918 | 14.3% |
| 152 (890), the full corpus | 0.1055, 0.0958, 0.0887 | 0.0966 (0.0896 to 0.1048) | 0.0887 to 0.1055 | 15.3% |

Every point is trained for the same 60 epochs, so the smaller points take fewer gradient steps. From 30 to 152 frames the difference was +0.0349 (+0.0310 to +0.0392), 56.5 per cent, passing all three readings. From 120 to 152 frames it was +0.0062 (+0.0033 to +0.0088), 6.9 per cent, passing the interval reading only. A fit of mAP50 on the logarithm of the number of frames over the five means gave a gain of 0.0140 per doubling.

### C9. Fine-tuning per seed

Table C9. Fine-tuning on 5 and 10 per cent of VisDrone's training split from S-oblique-six (F-synthetic) and from COCO weights (F-generic), and joint training from COCO weights on the same real images with the 890 synthetic tiles (F-joint): mAP50 on VisDrone val with intervals by resampling images, by training seed where repeated. Original schedule except the column for the learning rate of 0.0002, the schedule F-generic preferred on the selection slice.

| Real training data, seed | F-synthetic, original schedule | F-generic, original schedule | F-generic, learning rate 0.0002 | F-joint |
|---|---|---|---|---|
| 5 per cent (324 images), seed 0 | 0.4424 (0.4260 to 0.4587) | 0.5220 (0.5045 to 0.5403) | 0.5746 | 0.4607 (0.4444 to 0.4789) |
| 5 per cent, seed 1 | 0.4608 (0.4441 to 0.4784) | 0.5228 (0.5056 to 0.5410) | 0.5963 | trained once |
| 5 per cent, seed 2 | 0.4554 (0.4400 to 0.4721) | 0.5285 (0.5114 to 0.5474) | 0.5982 | trained once |
| 5 per cent, mean of 3 seeds | 0.4529 (0.4373 to 0.4696) | 0.5245 (0.5075 to 0.5424) | 0.5897 (0.5748 to 0.6073) | n.a. |
| 10 per cent (647 images), seed 0 | 0.5095 (0.4935 to 0.5264) | 0.5709 (0.5535 to 0.5883) | 0.6224 (0.6072 to 0.6396) | 0.5428 (0.5259 to 0.5610) |

Per seed at 5 per cent on the original schedule, F-generic finished above F-synthetic by +0.0796 (+0.0721 to +0.0873), +0.0620 (+0.0548 to +0.0706) and +0.0731 (+0.0654 to +0.0810), and the lowest generic run lay above the highest synthetic one. As ratios of F-generic to the other model on the same resamples, F-generic stood at 1.158 (1.144 to 1.173) times F-synthetic at 5 per cent and 1.121 (1.108 to 1.134) at 10 per cent on the original schedule, at 1.302 (1.279 to 1.331) and 1.222 (1.202 to 1.245) with each start on its chosen schedule, and at 1.138 (1.121 to 1.154) and 1.052 (1.039 to 1.064) times F-joint. The sign was the same in mAP50-95, the metric on which every checkpoint was selected: -0.0368 for the synthetic start at 5 per cent and -0.0232 at 10. Fine-tuning moved the synthetic model itself from 0.1055 to 0.4424 with 324 real images, and the synthetic start given 647 real images (0.5095) did not reach the generic start given 324 (0.5220). At 10 per cent F-joint lay above F-synthetic at IoU 0.50 and 0.60 and below it at 0.75 (0.0983 against 0.1025). On the selection slice the synthetic start led in the first three epochs at 5 per cent and was overtaken by the fourth; at 10 per cent the generic start led from the first epoch; afterwards the synthetic start led only intermittently, and the generic start's lead did not narrow between epoch 20 and epoch 30.

Table C9a. Fine-tuning under four schedules: mAP50 on VisDrone val, first seed, with the selection-slice mAP50-95 that chose each schedule in parentheses (chosen cell bold); last column, three-seed mean where run, and share of R.

| Slice, start | Original | Frozen backbone | Learning rate 0.0002 | Both | Mean of three seeds where run (95% interval); share of R |
|---|---|---|---|---|---|
| 5 per cent, synthetic | **0.4424 (0.1480)** | 0.2808 (0.0901) | 0.3103 (0.1019) | 0.2028 (0.0585) | original: 0.4529 (0.4373 to 0.4696); 71.8% |
| 5 per cent, generic | 0.5220 (0.1802) | 0.5467 (0.1886) | **0.5746 (0.2230)** | 0.5410 (0.1915) | original: 0.5245 (0.5075 to 0.5424); 83.1%. Learning rate 0.0002: 0.5897 (0.5748 to 0.6073); 93.4% |
| 5 per cent, joint | 0.4607 | not run | not run | not run | one run; 73.0% |
| 10 per cent, synthetic | **0.5095 (0.1743)** | 0.3209 (0.1053) | 0.3875 (0.1258) | 0.2241 (0.0681) | one run; 80.7% |
| 10 per cent, generic | 0.5709 (0.1951) | 0.5772 (0.2030) | **0.6224 (0.2451)** | 0.5644 (0.2001) | one run; original 90.5%, learning rate 0.0002 98.6% |
| 10 per cent, joint | 0.5428 | not run | not run | not run | one run; 86.0% |

The control run reproduced the original generic model exactly (0.5220).

### C10. The matched twins in detail

Table C10, panel A. The three-class models at 1.14, 2.44 and 4.88 cm per pixel on the 80 held-out frames of each corpus, which share their frame indices: share of annotated figures found in any class, the rates at which each class is called armed at confidence 0.25, and d′ against objects (log-linear correction), first training run of each model, Twin-150 being the model trained for longer. Interval at 150 m by 1,000 resamples of frames; intervals at the two finer GSDs in panel B.

| Model (GSD, cm/px) | Figures found | Armed called armed | Object called armed | Unarmed called armed | d′ vs object |
|---|---|---|---|---|---|
| S-nadir-35 (1.14) | 0.684 | 0.543 | 0.253 | 0.156 | 0.77 |
| Twin-75 (2.44) | 0.766 | 0.432 | 0.125 | 0.140 | 0.97 |
| Twin-150 (4.88) | 0.663 | 0.457 | 0.245 (0.204 to 0.289) | 0.205 | 0.58 (0.38 to 0.78) |

Table C10, panel B. S-nadir-35 against Twin-75, every other setting held: rates at which each class is called armed at confidence 0.25 on the selection splits (35 and 24 frames) and on the 80 held-out frames of each corpus, with differences, intervals by resampling frames independently on each side and p from a two-sided two-proportion test, unadjusted for clustering by frame. Further rows: ranges and means over three training seeds, the object rate at stricter IoU thresholds and d′.

| Quantity | S-nadir-35 (1.14 cm/px) | Twin-75 (2.44 cm/px) | Difference (95% interval) |
|---|---|---|---|
| Object called armed, selection split | 0.273 | 0.165 | +0.108 (+0.015 to +0.211), p = 0.06 |
| Object called armed, 80 held-out frames | 0.253 (74 of 292) | 0.125 (36 of 288) | +0.128 (+0.071 to +0.194), p = 0.0001 |
| Armed called armed, selection split | 0.569 | 0.471 | +0.099 (-0.022 to +0.217), p = 0.15 |
| Armed called armed, 80 held-out frames | 0.543 | 0.432 | +0.112 (+0.031 to +0.192) |
| Unarmed called armed, selection split | 0.168 | 0.109 | +0.059 (-0.038 to +0.154), p = 0.22 |
| Unarmed called armed, 80 held-out frames | 0.156 | 0.140 | +0.015 (-0.040 to +0.073) |
| d′ against objects, selection split | 0.77 (0.46 to 1.10) | 0.89 (0.58 to 1.32) | |
| d′ against objects, 80 held-out frames | 0.77 (0.57 to 0.99) | 0.97 (0.77 to 1.20) | |
| Object rate over three training seeds, selection split (range; mean) | 0.231 to 0.273; 0.248 | 0.132 to 0.242; 0.179 | ranges overlap; +0.068 (+0.002 to +0.142), 38.1% |
| Object rate over three training seeds, 80 held-out frames (range; mean) | 0.202 to 0.253; 0.222 | 0.097 to 0.181; 0.134 | ranges separate; +0.087 (+0.044 to +0.136), 64.9% |
| Object rate, selection split, at IoU 0.60 and 0.75 | 0.223 and 0.132 | 0.165 and 0.132 | level at 0.75 |

Without the log-linear correction, d′ on the selection splits of S-nadir-75, S-nadir-35 and Twin-75 is 0.83, 0.78 and 0.90 against objects and 1.24, 1.14 and 1.16 against unarmed figures.

Seed by seed. The object-rate difference between S-nadir-35 and Twin-75 excluded zero in seeds 0 and 1 and not in seed 2, on both sets. The armed recall of S-nadir-35 exceeded that of Twin-75 on the held-out frames in seeds 0 and 1 and fell below it in seed 2, and the unarmed rate differed in no seed. On the held-out frames S-nadir-35 called 0.253 of objects armed and Twin-75 0.125 in the first run, about twice as many, and 0.222 and 0.134 on the means of three training runs, 1.7 times as many.

Against the original 75 m model. The object rate of S-nadir-35 on its selection split differed from that of S-nadir-75 by +0.036 (-0.059 to +0.124) at IoU 0.50 and fell below it at 0.60 and 0.75, where S-nadir-75 called 0.230 and 0.141 of objects armed; the unarmed rate did the same at 0.75 (0.076 against 0.085). Between S-nadir-75 and Twin-75, which changed the carrying poses and the other settings listed in Section 4.6 of the main text at the same GSD, the object rate moved from 0.237 to 0.165 with an interval that includes zero (p = 0.19, unadjusted for clustering by frame).

Twin-150. Trained with the standard recipe, Twin-150 found 148 of 297 annotated figures (0.498) on its selection split, where the median annotated box measures 21 by 20 pixels, below the pre-specified half. Trained again for longer (it stopped at epoch 80), it found 0.606 of the 297 figures in any class on its selection split and 0.663 of 916 on its 80 held-out frames, and passed the condition. On its selection split it called 0.435 of armed figures and 0.178 (0.107 to 0.247) of objects armed, a d′ of 0.75 (0.33 to 1.26), with a three-class mAP50 of 0.388. On the held-out frames, against Twin-75, its d′ was lower by 0.394 (-0.681 to -0.098) and its object rate higher by 0.120 (+0.058 to +0.181), relative differences of 68.0 and 96.2 per cent, both passing readings (b) and (c). Figures carrying the 0.20 m pistol were called armed at 0.50 (17 of 34), within the range of the long arms (0.41 to 0.50).

### C11. Threshold sweep

Table C11. The three operating points of Section 4.7 of the main text (default confidence 0.25, maximum armed F1, object rate at or below 0.10) for each of the 14 combinations of three-class model, training seed and set. Selection: the selection split of the corpus; held-out: 80 new frames for S-nadir-35 and Twin-75, the 50 unseen-weapon frames for S-nadir-75. Where two operating points coincide they share one row. d′ with the log-linear correction.

| Model, seed | Set (frames) | Operating point | Threshold | Armed recall | Object called armed | Unarmed called armed | Armed precision | Armed F1 | d′ vs object | d′ vs unarmed |
|---|---|---|---|---|---|---|---|---|---|---|
| S-nadir-75, 0 | selection (27) | default | 0.25 | 0.547 | 0.237 | 0.131 | 0.386 | 0.452 | 0.83 | 1.23 |
| S-nadir-75, 0 | selection (27) | max armed F1 | 0.40 | 0.564 | 0.200 | 0.118 | 0.516 | 0.539 | 0.99 | 1.33 |
| S-nadir-75, 0 | selection (27) | object rate 0.10 | 0.70 | 0.333 | 0.096 | 0.033 | 0.661 | 0.443 | 0.86 | 1.38 |
| S-nadir-75, 0 | held-out (50) | default | 0.25 | 0.434 | 0.152 | 0.068 | 0.430 | 0.432 | 0.85 | 1.31 |
| S-nadir-75, 0 | held-out (50) | max armed F1 | 0.45 | 0.391 | 0.126 | 0.059 | 0.578 | 0.466 | 0.86 | 1.27 |
| S-nadir-75, 0 | held-out (50) | object rate 0.10 | 0.55 | 0.340 | 0.100 | 0.027 | 0.669 | 0.451 | 0.86 | 1.48 |
| S-nadir-35, 0 | selection (35) | default | 0.25 | 0.569 | 0.273 | 0.168 | 0.415 | 0.480 | 0.77 | 1.12 |
| S-nadir-35, 0 | selection (35) | max armed F1 | 0.30 | 0.555 | 0.256 | 0.126 | 0.469 | 0.508 | 0.79 | 1.27 |
| S-nadir-35, 0 | selection (35) | object rate 0.10 | 0.60 | 0.285 | 0.099 | 0.017 | 0.722 | 0.408 | 0.70 | 1.47 |
| S-nadir-35, 0 | held-out (80) | default | 0.25 | 0.543 | 0.253 | 0.156 | 0.408 | 0.466 | 0.77 | 1.12 |
| S-nadir-35, 0 | held-out (80) | max armed F1 | 0.35 | 0.497 | 0.226 | 0.121 | 0.484 | 0.491 | 0.74 | 1.16 |
| S-nadir-35, 0 | held-out (80) | object rate 0.10 | 0.65 | 0.211 | 0.099 | 0.035 | 0.603 | 0.313 | 0.48 | 0.99 |
| S-nadir-35, 1 | selection (35) | default | 0.25 | 0.547 | 0.231 | 0.101 | 0.455 | 0.497 | 0.84 | 1.38 |
| S-nadir-35, 1 | selection (35) | max armed F1 | 0.35 | 0.504 | 0.223 | 0.067 | 0.507 | 0.505 | 0.76 | 1.48 |
| S-nadir-35, 1 | selection (35) | object rate 0.10 | 0.65 | 0.314 | 0.083 | 0.017 | 0.741 | 0.441 | 0.88 | 1.56 |
| S-nadir-35, 1 | held-out (80) | default | 0.25 | 0.471 | 0.202 | 0.124 | 0.424 | 0.447 | 0.76 | 1.08 |
| S-nadir-35, 1 | held-out (80) | max armed F1 | 0.40 | 0.451 | 0.178 | 0.102 | 0.534 | 0.489 | 0.80 | 1.14 |
| S-nadir-35, 1 | held-out (80) | object rate 0.10 | 0.65 | 0.275 | 0.096 | 0.044 | 0.651 | 0.386 | 0.70 | 1.09 |
| S-nadir-35, 2 | selection (35) | default | 0.25 | 0.511 | 0.240 | 0.092 | 0.407 | 0.453 | 0.73 | 1.33 |
| S-nadir-35, 2 | selection (35) | max armed F1 | 0.45 | 0.460 | 0.132 | 0.042 | 0.656 | 0.541 | 1.00 | 1.59 |
| S-nadir-35, 2 | selection (35) | object rate 0.10 | 0.55 | 0.358 | 0.099 | 0.017 | 0.721 | 0.478 | 0.91 | 1.68 |
| S-nadir-35, 2 | held-out (80) | default | 0.25 | 0.477 | 0.209 | 0.130 | 0.439 | 0.457 | 0.75 | 1.06 |
| S-nadir-35, 2 | held-out (80) | max armed F1 | 0.45 | 0.396 | 0.164 | 0.083 | 0.598 | 0.476 | 0.71 | 1.12 |
| S-nadir-35, 2 | held-out (80) | object rate 0.10 | 0.55 | 0.292 | 0.099 | 0.057 | 0.656 | 0.404 | 0.73 | 1.02 |
| Twin-75, 0 | selection (24) | default | 0.25 | 0.471 | 0.165 | 0.109 | 0.440 | 0.455 | 0.89 | 1.14 |
| Twin-75, 0 | selection (24) | max armed F1 | 0.40 | 0.423 | 0.154 | 0.054 | 0.522 | 0.468 | 0.81 | 1.37 |
| Twin-75, 0 | selection (24) | object rate 0.10 | 0.55 | 0.341 | 0.099 | 0.043 | 0.630 | 0.443 | 0.86 | 1.26 |
| Twin-75, 0 | held-out (80) | default | 0.25 | 0.432 | 0.125 | 0.140 | 0.370 | 0.399 | 0.97 | 0.90 |
| Twin-75, 0 | held-out (80) | max armed F1 and object rate 0.10 | 0.40 | 0.381 | 0.090 | 0.120 | 0.480 | 0.425 | 1.03 | 0.87 |
| Twin-75, 1 | selection (24) | default | 0.25 | 0.353 | 0.132 | 0.098 | 0.417 | 0.382 | 0.73 | 0.90 |
| Twin-75, 1 | selection (24) | max armed F1 | 0.40 | 0.341 | 0.110 | 0.076 | 0.580 | 0.430 | 0.80 | 1.00 |
| Twin-75, 1 | selection (24) | object rate 0.10 | 0.45 | 0.282 | 0.099 | 0.043 | 0.600 | 0.384 | 0.69 | 1.09 |
| Twin-75, 1 | held-out (80) | default and object rate 0.10 | 0.25 | 0.354 | 0.097 | 0.127 | 0.396 | 0.374 | 0.92 | 0.76 |
| Twin-75, 1 | held-out (80) | max armed F1 | 0.40 | 0.284 | 0.062 | 0.089 | 0.549 | 0.374 | 0.95 | 0.77 |
| Twin-75, 2 | selection (24) | default | 0.25 | 0.588 | 0.242 | 0.141 | 0.391 | 0.469 | 0.91 | 1.28 |
| Twin-75, 2 | selection (24) | max armed F1 | 0.40 | 0.541 | 0.209 | 0.076 | 0.511 | 0.526 | 0.90 | 1.50 |
| Twin-75, 2 | selection (24) | object rate 0.10 | 0.65 | 0.271 | 0.099 | 0.022 | 0.622 | 0.377 | 0.66 | 1.33 |
| Twin-75, 2 | held-out (80) | default | 0.25 | 0.556 | 0.181 | 0.195 | 0.390 | 0.458 | 1.05 | 1.00 |
| Twin-75, 2 | held-out (80) | max armed F1 | 0.50 | 0.479 | 0.118 | 0.127 | 0.583 | 0.526 | 1.12 | 1.08 |
| Twin-75, 2 | held-out (80) | object rate 0.10 | 0.55 | 0.420 | 0.097 | 0.106 | 0.614 | 0.499 | 1.09 | 1.04 |

Over the 14 combinations, the threshold that maximised the F1 of the armed class lay between 0.30 and 0.50 (0.40 in 7 of them) and raised the armed precision from 0.37 to 0.46 at the default to 0.47 to 0.66, at a cost of 1 to 8 points of armed recall in 13 of them and a gain of 2 in S-nadir-75 on its selection split. Bringing the object rate to 0.10 required a threshold of 0.55 to 0.70 for S-nadir-35 and S-nadir-75, where armed recall then lay between 0.21 and 0.36; Twin-75 reached 0.10 at thresholds between 0.25 and 0.65. At no threshold did any model exceed an armed recall of 0.65, and none brought the object rate below 0.09 while keeping armed recall above 0.42. On the held-out frames the curve of S-nadir-35 ran to the right of that of Twin-75, at a higher object rate for the same armed recall.

### C12. Crop similarity in full

<!--TAB:similaridade|Separation of the three classes without a trained detector, by GSD (Section 4.4): nearest-centroid classification under 5-fold cross-validation, detector d′ in parentheses, and AUC of armed versus object; 95 per cent intervals by resampling frames. Chance: 0.33 accuracy, 0.50 AUC.-->

Table C12, panel A. Separation of the three classes in the frozen generic feature space by GSD (protocol in Section B4). Median annotated box in the evaluation pool; nearest-centroid classification under 5-fold cross-validation, with the detector's d′ on the corpus's selection split in parentheses (both without the log-linear correction) and intervals by resampling frames; AUC of armed against object; accuracy after PCA to 2 and 10 dimensions and after LDA to 2 dimensions. Chance: 0.33 for accuracy, 0.50 for AUC.

| Corpus (GSD, cm/px) | Crops: armed / unarmed / object | Median box (px) | Accuracy, 3 classes | Object called armed (95% interval) | Armed recall | d′ (detector) | AUC armed vs object (95% interval) | Accuracy, PCA 2 / PCA 10 / LDA 2 |
|---|---|---|---|---|---|---|---|---|
| S-nadir-35 (1.14) | 483 / 434 / 413 | 124 by 105 | 0.507 | 0.332 (0.285 to 0.375) | 0.420 | 0.23 (0.78) | 0.525 (0.483 to 0.561) | 0.384 / 0.495 / 0.547 |
| Twin-75 (2.44) | 342 / 384 / 379 | 48 by 41 | 0.531 | 0.253 (0.207 to 0.297) | 0.377 | 0.35 (0.90) | 0.576 (0.531 to 0.622) | 0.399 / 0.525 / 0.586 |
| Twin-150 (4.88) | 92 / 104 / 101 | 21 by 20 | 0.492 | 0.208 (0.131 to 0.287) | 0.359 | 0.45 (0.67*) | 0.654 (0.574 to 0.730) | 0.428 / 0.471 / 0.502 |
| S-nadir-75, original (2.44) | 117 / 153 / 135 | 45 by 41 | 0.558 | 0.267 (0.187 to 0.360) | 0.436 | 0.46 (0.83) | 0.534 (0.459 to 0.615) | 0.348 / 0.526 / 0.514 |

\* From the first Twin-150 model, trained with the standard recipe, which failed its validity condition (Table C10).

Table C12, panel B. Structure of the centred feature space and the supplement with trained backbones, in the order of panel A.

| Corpus (GSD, cm/px) | Largest centred co-similarity entry | Silhouette, 3 classes | Centroid cosine, unarmed vs object | Centroid cosine, armed vs object | AUC armed vs object, trained backbone (not model-free) |
|---|---|---|---|---|---|
| S-nadir-35 (1.14) | 0.025 | 0.002 | -0.75 | +0.15 | 0.547 |
| Twin-75 (2.44) | 0.026 | 0.007 | -0.85 | -0.03 | 0.502 |
| Twin-150 (4.88) | 0.032 | 0.002 | -0.86 | -0.55 | 0.574* |
| S-nadir-75, original (2.44) | 0.020 | 0.006 | -0.69 | +0.13 | 0.494 |

\* Backbone of the first Twin-150 model, which failed its validity condition.

Table C12, panel C. The nearest-centroid rule fitted on the training split and applied to the detector's own evaluation pools, against the detector's object rate at confidence 0.25.

| Pool | Object called armed by the rule (95% interval) | Object called armed by the detector |
|---|---|---|
| S-nadir-35, selection split | 0.331 (0.254 to 0.408) | 0.273 |
| S-nadir-35, held-out frames | 0.288 (0.237 to 0.343) | 0.253 |
| Twin-75, selection split | 0.231 (0.151 to 0.316) | 0.165 |
| Twin-75, held-out frames | 0.292 (0.234 to 0.351) | 0.125 |

After centring, every entry of the co-similarity matrices lay between -0.030 and +0.032 (between 0.71 and 0.79 before centring). The one structure present opposed the unarmed class to the two carrying classes: the largest negative entries sat on the unarmed-against-object pair at every GSD (-0.017 to -0.030), and the silhouette of the armed class was negative at all four GSDs. The AUC of armed against object rose as resolution coarsened; its interval excludes 0.50 at 2.44 cm per pixel (Twin-75) and at 4.88 (Twin-150), the latter resting on 92 against 101 crops with the widest interval. The crops thus separated weakly, less than the detector: the nearest-centroid rule gave a d′ of 0.23 to 0.46 against 0.67 to 0.90 for the detector. Applied to the four pools of panel C, the fitted rule recognised 0.39 to 0.50 of armed figures against the detector's 0.43 to 0.57. Two principal components kept 0.18 to 0.20 of the variance and lowered accuracy to 0.348 to 0.428; 10 components kept 0.50 to 0.55 and matched the full space; the Fisher projection gave the highest accuracy without a detector, 0.502 to 0.586, with a d′ of 0.18 to 0.53. The 5-nearest-neighbour rule, the two shallower feature maps (AUC 0.485 to 0.572 under the nearest-centroid rule) and folds drawn by frame gave the same picture.

Note to Table C12. A two-stage alternative to the three-class head, detecting the person and then classifying the crop by its distance to class prototypes, would make the decision inspectable. It would need local features from the detector's own map, since the pooled vector of a crop, generic or from the trained backbone, separates armed figures from figures carrying an object less well than the detector at every GSD (Section 5.1 of the main text); it has not been tested.

![Figure C2. Crop similarity without a trained detector at 1.14, 2.44 and 4.88 cm per pixel. Top: each evaluation pool on its first two principal components, class centroids marked. Bottom: mean pairwise cosine similarity of centred features between and within classes (Section B4).](06-resultados/figuras/fig13_similaridade.png)

### C13. Rates by firearm and by object in the unseen-weapon test

Table C13. Rate at which S-nadir-75 called figures armed on the 50 held-out frames of the unseen-weapon test (75 m, 2.44 cm per pixel), by carried item, at confidence 0.25. Each firearm rests on 15 to 69 instances; the rates are descriptive and carry no intervals.

| Carried item | Seen in training | Called armed | Instances |
|---|---|---|---|
| Rifle, 1.10 m | no | 0.50 | not reported |
| Submachine gun, 0.55 m | no | 0.43 | not reported |
| Pistol, 0.20 m | yes | 0.20 | 20 |
| Long arms seen in training (two rifles, carbine, shotgun) | yes | 0.34 to 0.52 | not reported |
| Closed umbrella, 0.88 m | n.a. (object) | 0.38 | 29 |
| Brooms | n.a. (object) | 0.10 | 41 |
| Lengths of pipe | n.a. (object) | 0.11 | 28 |

Recall was 0.400 on the five training firearms (50 of 125) and 0.466 on the two unseen ones (61 of 131), a ratio of 1.16 (approximate 95 per cent interval 0.88 to 1.54, ignoring the clustering of boxes within frames); with the pistol set aside the ratio stayed above the pre-specified 0.80. In the carried-as-weapon re-render the 227 paired objects were matched box for box in 49 of 50 frames. In the carried-as-weapon re-render the umbrella, whose carriage did not change, stayed at 0.38.

## References for the Online Appendix

Sources cited only in this appendix. Sources also cited in the main text are listed in its reference list.

Bahmanyar, R., Vig, E., & Reinartz, P. (2019). MRCNet: Crowd counting and density map estimation in aerial and ground imagery. arXiv. https://arxiv.org/abs/1909.12743

Barros, M. (2026, July 30). Anuário aponta avanço da violência contra policiais no Rio de Janeiro. Defesa em Foco. https://www.defesaemfoco.com.br/<wbr>anuario-aponta-avanco-da-violencia-contra-policiais-no-rio-de-janeiro/<wbr>

Caminhos Languages. (2025). The largest favelas in Rio de Janeiro. https://caminhoslanguages.com/<wbr>blog/<wbr>favelas-in-rio-de-janeiro/<wbr>

Causa Operária. (2025, April). STF julga ADPF 635 autorizando o terror policial contra favelas. https://causaoperaria.org.br/<wbr>2025/<wbr>stf-julga-adpf-635-autorizando-o-terror-policial-contra-favelas/<wbr>

CBS News. (2025, November 4). Brazil's president calls for investigation after 121 killed in police operation against gang: "There was a massacre." https://www.cbsnews.com/<wbr>amp/<wbr>miami/<wbr>news/<wbr>brazil-president-lula-probe-police-operation-gang-massacre

Couto, C. (2025, October 28). Megaoperação tenta prender 100 membros do CV no Alemão e Penha (RJ). CNN Brasil. https://www.cnnbrasil.com.br/<wbr>nacional/<wbr>sudeste/<wbr>rj/<wbr>rj-megaoperacao-com-mais-de-2-mil-policiais-toma-alemao-e-penha/<wbr>

Fórum Brasileiro de Segurança Pública. (2025). *19º Anuário Brasileiro de Segurança Pública: 2025*. https://publicacoes.forumseguranca.org.br/<wbr>handle/<wbr>fbsp/<wbr>279

Gazeta do Povo. (2025, April 10). "ADPF das Favelas": decisão final do STF vai melhorar ou piorar de vez a segurança do Rio? https://www.gazetadopovo.com.br/<wbr>vida-e-cidadania/<wbr>adpf-635-decisao-final-stf-vai-melhorar-ou-piorar-rio/<wbr>

Grillo, I. (2014, September 10). Brazil's Red Command and the police who fight them. InSight Crime. https://insightcrime.org/<wbr>news/<wbr>analysis/<wbr>brazils-red-command-rio-police-favelas-slums/<wbr>

InSight Crime. (2026, September 11). Red Command (Comando Vermelho). https://insightcrime.org/<wbr>brazil-organized-crime-news/<wbr>red-command-profile/<wbr>

Instituto Brasileiro de Geografia e Estatística. (2024). *Censo Demográfico 2022: Favelas e comunidades urbanas: Resultados do universo*. IBGE. https://censo2022.ibge.gov.br/<wbr>apps/<wbr>pgi/<wbr>pdf/<wbr>Censo%20Demogr%C3%A1fico%202022%20-%20Favelas%20e%20Comunidades%20Urbanas%20-%20Resultados%20do%20universo%20-%202024%2011%2006.pdf

Instituto Brasileiro de Geografia e Estatística. (n.d.). *Censo Demográfico 2022: Tabela 9923, população residente, por situação do domicílio* [Data set]. SIDRA. Retrieved October 18, 2026, from https://sidra.ibge.gov.br/<wbr>tabela/<wbr>9923

Instituto de Segurança Pública do Rio de Janeiro. (n.d.-a). *Estatísticas de segurança: Série histórica anual no estado desde 1991 (taxas por 100 mil habitantes)* [Data set]. Retrieved September 30, 2026, from https://www.ispdados.rj.gov.br/<wbr>Arquivos/<wbr>BaseEstadoTaxaAno.csv

Instituto de Segurança Pública do Rio de Janeiro. (n.d.-b). *Estatísticas de segurança: Série histórica mensal por área de delegacia desde 01/2003* [Data set]. Retrieved September 30, 2026, from https://www.ispdados.rj.gov.br/<wbr>Arquivos/<wbr>BaseDPEvolucaoMensalCisp.csv

JOTA. (2025, April 13). O julgamento da ADPF das Favelas: avanços, alertas e inovações. https://tagteam.harvard.edu/<wbr>hub_<wbr>feeds/<wbr>3884/<wbr>feed_<wbr>items/<wbr>13579751/<wbr>content

Lessing, B. (2008). As facções cariocas em perspectiva comparativa. *Novos Estudos CEBRAP*, (80), 43-62. https://doi.org/10.1590/S0101-33002008000100004

Misse, M. (2011). Crime organizado e crime comum no Rio de Janeiro: Diferenças e afinidades. *Revista de Sociologia e Política, 19*(40), 13-25. https://doi.org/10.1590/S0104-44782011000300003

Mistler-Ferguson, S. (2022, January 27). Brazil tries to reclaim Rio's favelas: Ad infinitum. InSight Crime. https://insightcrime.org/<wbr>news/<wbr>brazil-tries-reclaim-rio-favelas-ad-infinitum/<wbr>

OPEB. (2025, November 12). Crise, calamidade e exceção: os limites dos direitos humanos na megaoperação nos complexos do Alemão e da Penha. https://opeb.org/<wbr>2025/<wbr>11/<wbr>12/<wbr>crise-calamidade-e-excecao-os-limites-dos-direitos-humanos-na-megaoperacao-nos-complexos-do-alemao-e-da-penha/<wbr>

Robicquet, A., Sadeghian, A., Alahi, A., & Savarese, S. (2016). Learning social etiquette: Human trajectory understanding in crowded scenes. In *Computer Vision, ECCV 2016* (Lecture Notes in Computer Science, pp. 549-565). Springer. https://doi.org/10.1007/978-3-319-46484-8_33

Varga, L. A., Kiefer, B., Messmer, M., & Zell, A. (2022). SeaDronesSee: A maritime benchmark for detecting humans in open water. In *2022 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)* (pp. 3686-3696). IEEE. https://doi.org/10.1109/WACV51458.2022.00374

## Where the main text cites each item

| Appendix item | Cited from |
|---|---|
| A1 | Sections 3.1 and 3.2 |
| B1 and Table B1 | Sections 4.2.4, 4.5, 4.6 and 4.7 |
| Table B2 and its notes | Sections 4.2.5, 4.3, 4.6 and 4.8 |
| B3, Tables B3 and B3a | Sections 4.2.1, 4.2.2, 4.6 and 4.8 |
| B4 | Section 4.4 |
| B5 | Sections 2.3, 4.3, 4.6, 5.2 and 6.6 |
| B6, Table B6 and Figure B5 | Section 4.2.3 |
| Figures B1 and B2 | Section 4.2.1 |
| Figures B3 and B4 | Section 4.2.5 |
| Figure B6 | Section 4.6 |
| Table C0 | Sections 4.6, 5.6 and 6.4 |
| Table C0a | the opening of Section 5 and Sections 5.2, 5.4 and 5.6 |
| Notes to Table C1 | Sections 4.7 and 5.6 |
| Tables C2, C4, C12 and Figure C2 | Section 5.1 |
| Table C2a | Sections 5.1, 6.1 and 6.2 |
| Tables C3 and C3a | Sections 4.6, 5.1 and 5.5 |
| Table C7 and Figure C1 | Section 5.3 |
| Table C8 | Section 5.2 |
| Tables C9 and C9a | Sections 5.3 and 6.1 |
| Tables C11, C13 | Section 5.4 |
| Tables C6 and C10 | Sections 5.2 and 5.4 |
| Tables C1 (body) and C5 | not cited in the main text |
