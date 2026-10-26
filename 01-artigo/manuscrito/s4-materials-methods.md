## Materials and Methods

### 4.1 Research design, ethics and positionality

The study is a pre-deployment check of a capability claim: it asks under which acquisition conditions the claim that an aerial detector can tell an armed person from an unarmed one could hold, and fixes in advance the evidence that would count against it. It characterises the aerial target by GSD, camera pitch and illumination without a trained detector (Section 4.4), and scores detectors trained on synthetic imagery alone against a reference model trained on real images where a public benchmark exists and on held-out frames where none does (Sections 4.5 to 4.7). Only person detection is verified against reality, on two public benchmarks; the armed and unarmed distinction is not.

No imagery, geometry or address-level coordinate of Jacarezinho enters the generator, the corpora or any measurement, and no field data were collected. Synthesis yields a labelled corpus of the required morphology without imagery of residents who cannot meaningfully consent under the conditions of Section 3, trading the consent problem for the transfer problem; any future field data would require an independent ethics review and community engagement external to the police institution. The study is written from outside the territory, in a security framing that foregrounds what an aerial system would detect over daily life and how the community makes sense of its own space; the residents' perspective is absent. The question originates in a 2022 university research and extension proposal by a forensic expert of the Civil Police of the State of Rio de Janeiro (Acknowledgements), the institution that conducted the 2021 operation in Jacarezinho (Section 3.1). Exploratory work that preceded this study used a photogrammetric reconstruction from aerial survey imagery that the authors are not authorised to release; the reference acquisition of Section 4.2.4 reproduces the camera, pitch and altitude of that survey flight, and no image, geometry, corpus or result of that work enters this article.

### 4.2 Synthetic scene generator

Scenes are generated procedurally in Blender 5.2, headless with a deterministic seed, and rendered with its Cycles path tracer, from public-domain (CC0) assets of Poly Haven and of MPFB, the Blender implementation of MakeHuman, and from geometry authored by the generator; no commercial asset is used. The corpus contains no imagery or geometry of the territory, so it sits by construction on the generic side of the ablation of Liao et al. (2026).

#### 4.2.1 Settlement layout

Layout is generated in three stages, each removing a signature of procedural generation visible from above (Figure @fig{fig1_nadir}): a recursive partition whose gaps are mostly zero, so that dwellings abut across alleys (becos) of 0.5 to 1.2 m; sub-districts with independent orientations; and vertical accretion, with upper storeys smaller than and offset from the floor below. Six settlements differ in relief, cover, palette and density; settlement 1 is used in every single-settlement corpus (Online Appendix B3 and Figures B1 and B2).

<!--FIG:06-resultados/figuras/fig1_nadir.jpg|A generated settlement from the virtual survey camera: nadir, 150 m, rendered at 1920 by 1080 (9.76 cm per pixel); training corpora are rendered at 3840 by 2160. Abutting dwellings, alleys, nine sub-districts and offset upper storeys are visible.-->

#### 4.2.2 Figures, weapons and objects

Each run builds six rigged, clothed bodies with MPFB and places varied copies of them on rooftops and in alleys. Three classes are annotated: armed (carrying a firearm), unarmed (carrying nothing) and object (carrying an ordinary elongated object), the last answering the shortcut of Section 2.3. Five procedural firearms of 0.20 to 1.05 m stand against nine objects of 0.88 to 2.5 m, among them brooms, plastic (PVC) pipe and closed umbrellas (Online Appendix B3 and Table B3a). By construction a detector may separate the classes by length, by materials only objects have, by carrying angle (an object longer than 1.15 m, as no firearm is, rests on the shoulder or points to the ground) and, in the 35 m corpus and its twins, by carrying pose, since there objects are held forward with probability 0.08 and firearms with 0.42.

#### 4.2.3 Illumination regimes

The generator defines six coherent lighting budgets rather than jittering one sun parameter: hard sun (solar elevation 46 to 74 degrees), low sun (9 to 25), overcast, heavy overcast, haze and rain, the last with no raindrop or wet surface rendered. Each corpus sweeps the six in order and records the regime of every image (Online Appendix B6).

#### 4.2.4 Camera model and acquisition geometries

The virtual camera reproduces a commercially available UAV payload at its wide setting (horizontal field of view 63.96 degrees; Online Appendix, Table B1), so that the nadir ground width is 1.25 times the altitude. The nadir camera points within 3.5 degrees of vertical at a commanded altitude of 150, 75 or 35 m; the oblique camera flies at 120 m at a pitch drawn per image between 26 and 52 degrees from the vertical (S-oblique) or between 45 and 56 (S-oblique-six), as Figure @fig{fig8_nadir_obliquo} shows. Altitude jitter is given in Online Appendix B1.

The reference camera is the DJI Zenmuse Z30 (DJI, 2019), the payload of the survey flight of Section 4.1, which records 1920 by 1080 with a 30× optical zoom. The reference acquisition is nadir at 4.88 cm per pixel: a 3840 by 2160 render from 150 m, which the reference camera reaches from that altitude at 2× zoom (at its wide setting it gives 9.71 cm per pixel). The altitude labels 150, 75 and 35 m denote the GSDs the generator's camera reaches there at 3840 by 2160 (4.88, 2.44 and 1.14 cm per pixel), which a zoom also reaches from higher altitude at the cost of footprint (Table @tab{gsdzoom}). Stability under zoom, the lens's optical resolution at long focal lengths and the degradations of a real frame, among them sensor noise, motion blur and compression, are not modelled (Online Appendix B1), so the geometric GSD is an upper bound on detail.

<!--TAB:gsdzoom|GSD and footprint of the generator's camera, nadir, at the commanded altitude, and the zoom at which the reference camera reaches the same GSD from 150 m. The oblique row gives the nominal value at the frame centre. Bold: the GSDs the altitude labels denote.-->

| Altitude (m), render (px) | Footprint (m × m) | GSD (cm/px) | Reference camera from 150 m: zoom | Its footprint (m × m) |
|---|---|---|---|---|
| 150, 1920 × 1080 (pilot) | 187.3 × 105.4 | 9.76 | 1.0× (9.71 cm/px) | 186.4 × 104.8 |
| 150, 3840 × 2160 | 187.3 × 105.4 | **4.88** | 2.0× | 93.7 × 52.7 |
| 75, 3840 × 2160 | 93.7 × 52.7 | **2.44** | 4.0× | 46.8 × 26.3 |
| 35, 3840 × 2160 | 43.7 × 24.6 | **1.14** | 8.5× | 21.9 × 12.3 |
| 120 oblique, 3840 × 2160 | 149.9 × 84.3 (nominal) | 3.90 (nominal) | n.a. | n.a. |

<!--FIG:06-resultados/figuras/fig8_nadir_obliquo.jpg|The same settlement under the two camera geometries of Experiment A: nadir from 150 m, the reference acquisition, and oblique from about 120 m. Below each frame, four figures carrying nothing, enlarged without smoothing; Section 5.1 gives their shape ratios.-->

#### 4.2.5 Automatic annotation

Boxes come from geometry (Online Appendix, Figures B3 and B4): about 500 body and clothing vertices of each figure and every vertex of its carried item are projected into the image, and their axis-aligned extent is clipped to the frame. The convention is amodal within the frame, as in VisDrone: the box covers the whole figure, hidden parts and carried item included. Fourteen rays from the camera estimate the visible fraction; a figure below 0.35, outside the frame or with a clipped side under 0.002 of the frame is discarded (Online Appendix B2).

### 4.3 Synthetic corpora and real data

Training corpora are matched by frames (180 single-class, 200 three-class), not by instances (Online Appendix, Table B2 gives both by corpus). Table @tab{corpora} lists the training corpora, the model each trains and its role. S-nadir-150 (the corpus of record) renders settlement 1 at the reference acquisition under the six regimes; the other corpora depart from it in the settings their rows name.

The real data is VisDrone-DET (Section 2.2), with the pedestrian and people categories merged into one person class and the other categories and annotated ignored regions dropped. Its validation split of 548 images is the test set of every single-class model. R trains on 1,106 images drawn at random from the training split, as many as the training tiles of S-nadir-150, but on 18,858 persons against their 4,678 boxes, about four times as many. Three slices of the training split serve Experiment B: 5 per cent (324 images), 10 per cent (647, containing the first) and a selection split of 324 disjoint from both.

The second real test set is HERIDAL (Božić-Štulić et al., 2019; Pyrrö, 2021), people on the ground in Mediterranean scrub photographed straight down from 40 to 65 m (Pyrrö et al., 2021), at an estimated 1.5 to 2.4 cm per pixel, two to three times finer than the reference acquisition (Online Appendix B5). It is the only public set found with person boxes on land and a declared nadir view; its scene is wilderness, not a city. Every annotated image is used, for zero-shot evaluation only.

Held-out frames were rendered after the models they test had been trained and used for neither training nor selection: 80 continuing the seed of each of S-nadir-35, Twin-75 and Twin-150, at the same indices; 120 continuing that of S-nadir-150, 20 per regime; and 50 at 75 m in a new realisation of the settlement, with the two unseen firearms in half the armed figures, re-rendered with every object carried exactly as a weapon (Online Appendix B2).

<div class="full" markdown="1" style="break-inside: avoid">

<!--TAB:corpora|Training corpora and real training data, with the model each trains. Instances on whole frames (armed / unarmed / object). Held-out sets, tiles, test sets and derived corpora: Online Appendix, Table B2. n.a.: not applicable.-->

| Corpus | Camera and GSD (cm/px) | Frames or images, train / selection | Instances by class, train | Model and role |
|---|---|---|---|---|
| Pilot | nadir, 150 m, 9.76 | 40 / 8 | 292 / 273 / n.a. | pilot model; contrast statistic (Section 4.4) |
| S-nadir-150 | nadir, 150 m, 4.88 | 149 / 31 | 1,331 / 1,328 / n.a. | S-nadir-150: the reference acquisition (A, D) |
| S-nadir-150-six | nadir, 150 m, 4.88; six settlements | 156 / 24 | 1,424 / 1,368 / n.a. | S-nadir-150-six: settlement variety at nadir (A) |
| S-oblique | oblique, pitch 26 to 52°, 120 m, 3.90 nominal | 155 / 25 | 839 / 841 / n.a. | S-oblique: camera geometry (A) |
| S-oblique-six | oblique, pitch 45 to 56°, 120 m, 3.90 nominal; six settlements; figures carrying nothing | 152 / 28 | n.a. / 1,325 / n.a. | S-oblique-six: best of four configurations (A); start of F-synthetic, synthetic part of F-joint (B) |
| S-nadir-75 | nadir, 75 m, 2.44 | 173 / 27 | 816 / 820 / 846 | S-nadir-75: three classes at 2.44 (C) |
| S-nadir-35 | nadir, 35 m, 1.14; realistic object poses | 165 / 35 | 640 / 587 / 619 | S-nadir-35: three classes at 1.14 (C) |
| Twin-75 | S-nadir-35's corpus at 75 m, 2.44 | 176 / 24 | 650 / 638 / 701 | Twin-75: resolution with all else held (C) |
| Twin-150 | S-nadir-35's corpus at 150 m, 4.88 | 173 / 27 | 692 / 619 / 640 | Twin-150: the distinction at the reference acquisition (C) |
| R subset of VisDrone-DET train | real, mixed sizes | 1,106 / 548 (test split) | 18,858 persons | R: the reference model (A, B) |
| 5 per cent slice | real, as R | 324 / 324 | 5,883 persons | F-synthetic, F-generic, F-joint at 5 per cent (B) |
| 10 per cent slice (contains the 5 per cent slice) | real, as R | 647 / 324 | 11,091 persons | the same at 10 per cent (B) |

</div>

### 4.4 Characterisation of the target without a trained detector

Four properties of the target are measured before any detector is trained (Section 5.1). Size: on the pilot corpus, S-nadir-150 and the two oblique corpora, the median long side, width, height and area of the annotated box at native resolution, and the share of instances whose shorter side falls below 8 pixels, the stride of the finest feature map of the detector of Section 4.5. Shape: the height-to-width ratio of the box on the same sets, in S-oblique by pitch band of about 5 degrees, separately for figures carrying nothing, and on both VisDrone splits, because the pitch band of S-oblique-six was chosen on the training split. Contrast: on the pilot corpus (48 frames, 8 per regime), the difference between the mean luminance inside each box and in a 6 pixel ring around it, divided by the ring standard deviation and aggregated per image; it is measured at twice the GSD of the corpus Experiment D tests, so it motivates rather than predicts the per-regime ordering. Crop similarity: every annotated figure of the three-class corpora is embedded by the frozen backbone of the COCO-pretrained detector and classified by nearest centroid under five-fold cross-validation, scored by armed recall, object rate and the area under the receiver operating characteristic curve (AUC) for armed versus object (Online Appendix B4).

### 4.5 Detector and training protocol

The detector is YOLO11s, the small member of the Ultralytics YOLO11 family. Models start from weights pretrained on COCO (Lin et al., 2014), except F-synthetic, which starts from S-oblique-six. Synthetic training uses 1,280-pixel tiles cut at native scale, because downscaling a 3840 by 2160 frame to 1,536 pixels would take the median instance below one stride (Section 5.1); real images are resized to 1,280 pixels on the long side. Synthetic models train for 60 epochs and fine-tuning and joint models for 30, with AdamW at the learning rate the software sets from the number of classes (Online Appendix, Table B1).

After each epoch the fitness, mAP50-95 (Section 4.7), is computed on the selection split, the best checkpoint is kept and training stops after 15 epochs without improvement. Synthetic models select on the selection-split tiles of their own corpus, so VisDrone and HERIDAL never enter the selection of a single-class model, and three-class models are tested on that split and, separately, on held-out frames. Fine-tuning and joint models select on the real selection split, and R on the VisDrone test split, at epoch 58 of 60 without early stopping, on an untuned schedule; Section 6.5 states what this implies for each share of R.

### 4.6 Experimental design

Four experiments answer the research questions of Section 1.3; each check carries an identifier, H1 to H23, listed in Online Appendix C0. Online Appendix, Figure B6 shows how corpora, models and test sets connect; Table @tab{corpora} lists the models.

Experiment A (zero-shot transfer; RQ1) scores R and the four synthetic arms zero-shot on VisDrone and on HERIDAL under one single-class protocol, each as a share of R, with a check that R itself is not near chance and a scale-matched input size beside the protocol size (Online Appendix B1 and B5; H1 to H9).

A1, camera geometry. S-oblique keeps the settlement, materials, regimes and annotation of S-nadir-150 and moves the camera, which also changes the figure-placement filter, the GSD (about 4.3 to 6.3 cm per pixel at the frame centre, compared with 4.88) and the weapon library (Online Appendix B3); the difference between the two is the contribution of the camera with the settings that depend on it.

A2, settlement variety and scene dispersion. S-nadir-150-six spreads the same 180 frames over six settlements. S-oblique-six changes four settings at once (six settlements, a pitch band of 45 to 56 instead of 26 to 52 degrees chosen on the training split of VisDrone, figures carrying nothing only, and camera placement over the built core), so its difference from S-oblique is the gain of that bundle, not of settlement variety. It was configured after the score of S-oblique on VisDrone was known and was retained as the highest of the four configurations tried on that set (Section 5.2), a best-of-four on a reused test set for which HERIDAL, on which no configuration was chosen, is the independent check. Its two settlement-seed replicas measure the dispersion due to the scene.

A3, corpus size. S-oblique-six is retrained on its nested subsets of 30 to 120 frames, every point at the same 60 epochs, so that the smaller subsets take fewer gradient steps.

Experiment B (limited real data; RQ2). On the 5 and 10 per cent slices, F-synthetic starts from S-oblique-six and F-generic from COCO, first on the same untuned 30-epoch schedule and then on a grid that crosses a trainable or frozen backbone with a learning rate of 0.002 or 0.0002 at the same budget, each start taking per slice the cell whose best checkpoint scores highest in mAP50-95 on the selection split, never on the test set; a control run repeats the original generic model at 5 per cent. F-joint starts from COCO and trains for 30 epochs on the 890 training tiles of S-oblique-six with the same real images, about 2.7 synthetic inputs per real one at 5 per cent and 1.4 at 10 per cent, a ratio not varied; it is not rerun under the new schedules (H12 to H15).

Experiment C (the armed and unarmed distinction by GSD; RQ3). S-nadir-75 is scored on its selection split and on the two held-out sets at 75 m. The unseen-weapon test compares recall on the five training firearms with recall on two unseen ones in the same 50 frames, a 0.55 m submachine gun inside the length range of the training weapons and a 1.10 m rifle 0.05 m above it, so it bears on the asset more than on a new size. The carried-as-weapon test pairs the 227 objects matched box for box between the two renders and compares the rate at which they are called armed as normally carried and when carried in the weapons' poses and angles; it covers this 75 m model only.

Twin-75 and Twin-150 re-render the corpus of S-nadir-35 at 75 and 150 m on matched frame indices, changing only altitude and its jitter, and so separate resolution from the six settings that changed between the original 75 m corpus and the 35 m corpus, among them the carrying-pose distribution of objects (notes to Online Appendix Table B2). S-nadir-35 and the two twins are each scored on their selection split and on 80 held-out frames whose indices are shared across the three GSDs, so that d′ and the object rate can be read on matched frames, S-nadir-35 and Twin-75 across three training seeds. If Twin-150 failed its validity condition (at least half of the annotated figures found on both sets), two remedies were pre-specified before either ran: a longer budget (120 epochs, patience 30) and, only if that failed, a corpus three times larger.

The reading at 4.88 cm per pixel rests on a geometric premise. At that GSD the 0.92 m rifle spans about 19 pixels along its length and the 0.20 m pistol about 4, so the outline that distinguishes a firearm from a pipe or closed umbrella of similar length is not resolved; a separation there is therefore read as resting on a cue other than the firearm's form (H16 to H23).

Experiment D (illumination; secondary, synthetic only) scores S-nadir-150, trained on the six regimes in equal shares, per regime on its 120 held-out frames, and compares a specialist trained on hard sun alone, under hard sun, with that model under hard sun on the same 20 frames (D-i, descriptive) and under overcast (D-ii, which decides H11; Online Appendix C3).

Status of each check. Each check carries one of three labels: confirmatory, when hypothesis and criterion were fixed before any result on that test set; pre-specified follow-up, when the hypothesis was formed on earlier results on the same test set and the criterion was recorded before the run, a weaker test; and exploratory, for configurations added after earlier results without a criterion. HERIDAL and the frames rendered after training are the only data no hypothesis had seen. Criteria were recorded in a dated project log before each run; Online Appendix C0 lists H1 to H23 with status, criterion in full and outcome, and Section 5.6 tabulates the headline comparisons.

### 4.7 Metrics, statistical analysis and pre-specified criteria

Intersection over union (IoU) is the overlap of a predicted and an annotated box divided by their union; mAP50 counts a detection at IoU of at least 0.50, and mAP50-95 averages the same quantity over IoU thresholds from 0.50 to 0.95 and is the fitness on which every checkpoint is selected. The share of R is a synthetic model's mAP50 divided by that of R on the same test set; on VisDrone it is a share of the ceiling. Every difference is the model under test minus the reference. In plain terms, a share of R of one tenth means that a detector trained on synthetic imagery found persons in real images with a tenth of the accuracy of a detector trained on real ones. The quantity d′ measures how far apart the detector keeps armed people and people carrying an object, separately from how readily it flags anyone at all; zero means no separation.

The three-class models are scored on whole frames at native scale at confidence 0.25 (the default, not tuned). Predictions are matched one to one with annotated figures at IoU 0.50 without regard to class, each figure takes the class of its best-overlapping prediction, and an unmatched figure counts as not called armed. Four rates follow: armed recall, the object rate (the share of figures carrying an object that are called armed), the rate at which an unarmed figure is called armed, and the precision of the armed class. Each rate is a lower bound, since a second armed box on a figure matched to another class enters only the precision. The rates give d′, the difference between the normal quantiles of armed recall and of the rate at which the other class is called armed, each rate taking a log-linear correction before the quantile (Online Appendix B1). A sweep of the confidence threshold adds two operating points: the threshold that maximises the F1 (the harmonic mean of precision and recall) of the armed class and the lowest at which the object rate falls to 0.10 or below.

No threshold at which the capability to tell an armed person from one carrying an ordinary object would be read as present, in d′, object rate, armed recall or armed precision, was fixed before the results. Any statement about that capability therefore rests on the descriptive operating points of the threshold sweep (Section 5.4, where no model brought the object rate below 0.09 while keeping armed recall above 0.42) and, at 4.88 cm per pixel, where Twin-150 was not swept, also on the geometric premise of Section 4.6.

Ten models (Online Appendix B1) were trained with seeds 0, 1 and 2 on a fixed corpus, and the range over runs is reported; every other model was trained once. Intervals are 95 per cent percentile intervals from 1,000 resamples (2,000 for Experiment D): of test images on VisDrone and HERIDAL, identical for every model, so that shares of R and paired differences (between means over runs where a side has several) use the same resamples; and of frames for the three-class rates and d′. The frame-resampled interval is the primary measure; the two-proportion p-value, which ignores clustering by frame, is reported only where a criterion was pre-specified on it, and paired carried-as-weapon rates use an exact McNemar test.

What counts as a resolvable difference was fixed before any interval was computed: (a) the ranges of the two models over their three training seeds do not overlap (where one side was trained once, where its value falls in the other's range is recorded); (b) the 95 per cent interval of the paired difference excludes zero; and (c), descriptively, the relative difference, as a share of the smaller value, reaches 30 per cent. A difference that passes neither (a) nor (b) is reported as not resolvable; Section 5.6 applies the rule to the headline comparisons.

### 4.8 Reproducibility

Every generated image records its seed, illumination regime, commanded and realised altitude and, except in the pilot corpus and S-nadir-150, its camera pitch, so the authors can reproduce the settlement, camera and illumination of every reported image (Online Appendix B2). Training is deterministic under a fixed seed.

The scene generator, the corpora and the trained weights are not released, so a reader cannot check the corpora themselves. Each benchmark, the published specification of the reference camera and every parameter of Sections 4.2 to 4.7 and of the Online Appendix allow an independent replication of the protocol with a generator built to the same specification (Online Appendix B3), not a reproduction of the reported numbers; every asset is public domain.
