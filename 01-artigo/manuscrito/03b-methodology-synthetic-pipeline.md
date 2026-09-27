## 7. The Synthetic Data Generation Pipeline

> **Provenance note.** Every quantity in this section traces to a file under `06-resultados/`
> together with the command that produced it.

The design-science component declared in Section 5 and specified in Section 6 proposes a model of
vertical morphology and a synthetic-training strategy. This section specifies the generative
procedure that implements the second of those, and reports what happens when it is executed.

A distinction has to be drawn at the outset, because the two are easy to conflate. What is
implemented and evaluated below detects people: as a single class wherever transfer to the public
benchmark is measured, and at 75 m and 35 m in three classes, armed, unarmed, and unarmed carrying a
confusable elongated object, which no public benchmark annotates. Person detection is the task this
article measures, and it was chosen because it is the only one of the two with a public benchmark
against which transfer can be established. The conceptual model proposed in Section 6 classifies
built form instead: building height, rooftop addition, material transition. The same generator
already records the footprint, the storey count and the roof height of every structure it builds, so
the morphological task is a second experiment over the same infrastructure rather than a different
pipeline; what it lacks is an evaluation set, and Section 11.4 records that absence as a finding
rather than as an omission. Nothing below should be read as a validated capability over Jacarezinho,
and Section 11 restates the boundary.

### 7.1 Why synthesis, and what it does not solve

The ethical protocol of Section 5 forecloses the conventional route to a training corpus. Aerial
imagery of an inhabited favela, at a resolution sufficient to resolve built form, necessarily
captures residents, rooftop activity, and address-level geometry. Synthesis is therefore not a
technical convenience. It is the only procedure we identified that yields a labelled corpus of the
required morphological specificity without collecting imagery of residents who have not consented
and who cannot meaningfully be asked under the conditions documented in Section 3.

Synthesis substitutes one problem for another. It removes the consent problem and introduces the
transfer problem: a detector trained on rendered imagery must operate on photographs. The remainder
of this section describes the generator. Section 8 characterises the target independently of any
detector, and Sections 9 and 10 report what transfers and what does not.

### 7.2 Scene construction

Scenes are generated procedurally in Blender 5.2, executed headless with a deterministic seed, so
that the settlement, the camera and the illumination of any reported image can be regenerated
exactly from the seed recorded in its manifest entry, and the figures as well in every corpus but
the three that Section 11.6 names. No commercial asset packs are used: surface materials and the
four tree models of the vegetation come from a public-domain library (Poly Haven, CC0), the human
figures are built from the CC0 assets of MakeHuman through MPFB (Section 7.4), and all other
geometry is authored by the generator. That choice makes the corpus redistributable in full, and it
is paid for.

Liao et al. (2026) measure the cost directly. Replacing a photogrammetric reconstruction of the
target site with generic assets costs 27.0 mAP50 points on YOLOv11 (their name for YOLO11, the
family of the detector used here), and 22 to 23 points on average across the architectures they
test. In their taxonomy the corpus released with this article sits on the generic side, not the
photogrammetric one: it is procedural geometry with public-domain materials, and it is on the losing
side of that ablation by construction. Two qualifications bound how far the figure travels. Their
object class is vehicles rather than people, and their evaluation is on the same site they
reconstructed, so the result establishes that a digital twin of a place helps detection at that
place, not at another. This article reports the trade rather than claiming to have avoided it.
Measuring its size for this morphology would require a photogrammetric reconstruction of the target
site, which is precisely what the ethical protocol of Section 5 forecloses, so the cost is
quantified here from their result and not from ours.

Layout is produced in three stages, each addressing a specific way in which naive procedural
generation betrays itself when viewed from above.

**Parcelling.** The built core is subdivided by recursive binary partition. At each split the
boundary receives a gap drawn from a distribution whose modal value is zero, so that most dwellings
abut their neighbours, as they do in consolidated self-built settlement; because each lot is then
shrunk by 0.15 m towards its centroid and rotated about it (see Orientation below), a zero gap
leaves a narrow seam or a wedge between neighbours rather than an exactly shared wall. In the
released configuration the gap is zero with probability 0.82, falls between 0.5 and 1.2 m with
probability 0.12, between 1.3 and 2.0 m with probability 0.05, and above 2.0 m with probability
0.008. The second band is the alley, or *beco*, that defines the morphology.

**Orientation.** A single binary partition, however deformed, leaves legible straight runs of ten or
twenty dwellings, and that is the strongest visual signature of procedural generation in a nadir
view. The generator therefore divides the core into sub-districts, nine in the settlement of the
corpus of record and between 6 and 12 in the other five settlements of Section 9.2, each with an
independent orientation, separated by a Voronoi diagram, reproducing the way consolidated settlement
grows by nuclei that meet at an angle. Each lot is also rotated about its centroid by up to 0.17
radians and every corner passes through a smooth domain warp, so the statistic below measures the
three mechanisms together. The statistic is the fraction of edge energy falling within 7.5 degrees
of a cardinal axis, divided by the isotropic expectation. The measurement window covers 30 degrees
of 180, so the isotropic expectation is one sixth and unity means no preferred direction. In the
configuration of the corpus of record, rendered at 4K, the value is 0.94
(`06-resultados/teste_fidelidade.csv`, row v12, written by
`07-blender/scripts/teste_fidelidade.py`). The version of the generator that used a single partition
was never measured with the corrected script, so no value is reported for it.

An earlier draft of this article reported 1.62 for the configuration then released, an earlier
iteration of the generator. That figure came from a measurement script whose normaliser used 15
degrees of 180 rather than 30, inflating the whole column by a factor of two. The error mattered
beyond the digit: it placed the released configuration above the isotropic expectation when it is in
fact slightly below it. The script and the recorded values were corrected, and the correction is
noted here because the uncorrected figure appeared in circulated drafts.

**Vertical accretion.** The dwelling is not a single prism. In the majority of cases with two or
more storeys the upper floor is smaller than the one below and offset towards one boundary, leaving
part of the lower slab exposed. Seen from above this produces the L-shaped footprint that
characterises the texture of the settlement, and it is the single geometric feature whose absence
most clearly reads as a grid of boxes rather than a favela. Storey count is drawn around a
low-frequency noise field, with an independent per-dwelling scatter of 0.95 storeys (standard
deviation), so that taller and shorter zones form, as they do on a real hillside.

<!--FIG:06-resultados/figuras/fig1_nadir.jpg|A generated settlement seen from the virtual survey camera: nadir, 150 m above ground, rendered at 1920 by 1080, which gives 9.76 cm per pixel. The resolution is stated because Section 8.1 shows that ground sampling distance, not scene content, sets the size of the target; the corpus used for training is rendered at 3840 by 2160 and is twice as fine. All geometry except the CC0 tree models and human figures is authored by the generator, and all materials are public domain. The three construction stages described above are visible: dwellings abutting their neighbours with alleys mostly between 0.5 and 1.2 m, nine sub-districts meeting at an angle rather than a single orthogonal grid, and upper storeys offset from the floor below, which produces the L-shaped footprints that characterise the texture.-->

Roof surfaces carry the objects that occupy them in use: water tanks in three commercial volumes,
clotheslines, stair housings, satellite dishes, stacked roofing sheets, rubble, and exposed
reinforcement bar awaiting a further storey. Aerial cabling spans between rooftop anchor points.
These are not decoration. At the ground sampling distance of the target sensor they are intended as
a main source of local clutter, although no measurement here isolates their share, and Section 8.3
measures the contrast a person presents against that immediate background, which Section 10.3 treats
as a hypothesis about detector difficulty, with a test not yet run.

<!--FIG:06-resultados/figuras/fig3_beco.jpg|The same generated scene at street level, inside an alley. The view is not used for training, which is conducted entirely from the aerial camera, and is shown because it is the check that the layout is three-dimensional built form rather than a texture painted to satisfy a top-down view.-->

### 7.3 Camera model

The virtual camera reproduces a commercially available UAV payload in a configuration typical of
aerial survey over urban terrain: a Zenmuse Z30 at 1920 by 1080, corresponding to a 4.3 mm lens on a
5.37 mm sensor, or approximately 28.8 mm on a 36 mm equivalent, pointing down within 3.5 degrees of
vertical at a heading drawn per image, 150 m above ground with a per-image jitter of up to 6 m
either way (3 m in the 35 m corpus of Section 9.5). The parameters are stated in full so that the
acquisition conditions evaluated here can be reproduced or contested without reference to any
particular flight. At that altitude the frame covers approximately 187 by 105 m of ground.

Rendering resolution is treated as a parameter distinct from sensor resolution, and the distinction
is consequential enough to state plainly. Ground sampling distance, not the nominal resolution of
the camera, determines whether a target survives to the network. Rendering the 150 m nadir view at
1920 by 1080 yields 9.76 cm per pixel; rendering the same view at 3840 by 2160 yields 4.88 cm per
pixel. Section 8.1 reports what this does to the target and states the limitation it introduces:
imagery rendered at 4K is easier than a single real frame from the sensor it reproduces.

A second acquisition geometry is evaluated alongside the first, and the reason is arithmetic rather
than aesthetic. At 150 m a carried object is too thin for its form to be resolved, which this
article takes to foreclose the question rather than to answer it; no corpus of confusable objects
was rendered at that altitude to test that. The generator is therefore also run with the same sensor
at 75 m, where the frame covers approximately 94 by 53 m and the ground sampling distance halves to
2.44 cm per pixel at 3840 by 2160. Halving the distance doubles each linear dimension of the target
and quadruples its area before occlusion, and measured on the generated corpora the median instance
grows from 17.6 by 17.5 pixels to 47.6 by 41.7, a factor of 6.4 in area. That exceeds the four the
geometry alone gives, and part of the excess is composition: the corpus at 75 m adds a class
carrying elongated objects, whose boxes are the largest, and taken class by class the factor is 5.2
for armed and 5.7 for unarmed figures (`06-resultados/forma_corpora.json`).

The nadir altitudes are reported separately throughout, as S-nadir-150, S-nadir-75 and, in Section
9.5, S-nadir-35, because they answer different questions: the first is the altitude at which aerial
survey over urban terrain is conventionally flown with this payload, and the other two are the
geometries under which the distinction the article is named after was measured.

### 7.4 Annotation

Human figures are copies of a small pool of rigged, clothed meshes built for each rendering run
(MPFB, a MakeHuman derivative; `--pool`, six in the corpora rendered by the chains of Sections 9.2
to 9.5), each copy recoloured, rescaled and posed per instance, and placed both on rooftops and in
the alley network. Placement uses an occupancy map computed from the generated footprints, so that
ground placement is known to fall in open space rather than inferred by ray casting against
arbitrary geometry.

Bounding boxes are neither drawn by hand nor inferred from a segmentation pass. For each figure the
generator projects a subsample of the body and clothing vertices (every k-th vertex, about 500 per
figure) and every vertex of any carried object into image space, takes the axis-aligned extent, and
clips it to the frame. The convention is therefore amodal within the frame: the box covers the whole
figure, including parts hidden by intervening geometry, which is the convention used by the real
benchmark against which transfer is later measured. Occlusion is evaluated separately, by casting
fourteen rays from the camera to sample points on the figure, and instances whose visible fraction
falls below 0.35 are discarded from the label file rather than retained as degenerate boxes. In a
settlement this dense the discard rate is substantial and expected. Over the 180 frames of the
corpus of record, 4,582 figures were placed and 3,225 retained; the per-frame retained fraction has
a median of 0.71 (10th percentile 0.57, 90th percentile 0.83), so roughly three in ten figures
placed yield no label (`06-resultados/oclusao_ds_morro_4k.json`, produced by
`06-resultados/mede_oclusao.py`); the count does not separate the visibility threshold from the two
other reasons a placed figure is dropped, a box that falls outside the frame or a clipped box with a
side below 0.002 of the frame (`--min-lado`).

<!--FIG:06-resultados/figuras/fig5_anotacao.jpg|Automatically generated annotation. Green marks the armed class, blue the unarmed class; boxes are drawn with a four pixel outward offset so that they do not cover the target. The strip along the bottom shows individual targets magnified five times, with their true size in pixels printed beneath each one. At this ground sampling distance the target is a few pixels of low-contrast texture, which is the central difficulty characterised in Section 8.-->

**Carried objects and hard negatives.** At 75 m the corpus carries three classes rather than two:
armed, unarmed, and unarmed carrying an elongated object. The third exists because of an objection
that would otherwise be fatal to any figure reported for the first. If the weapon is always the same
asset, in the same pose, at the same contrast, a detector can separate the classes on properties of
the asset library rather than on anything visible in the world.

The corpus is built to remove that possibility. Five firearm models are generated procedurally, two
rifles, a carbine, a shotgun and a pistol, with recorded lengths of 0.20 to 1.05 m; the meshes of
the two rifles and of the shotgun are longer than the lengths recorded for them
(`07-blender/scripts/objetos_alongados.py`). Against them stand nine elongated objects that a person
carries in this territory, spanning 0.88 to 2.5 m: brooms, floor squeegees, plastic pipe,
reinforcement bar, planks, umbrellas, hoes, rolled mats and hose. Weapons and objects are drawn from
one palette of base colours and surface roughness, so that dark and metallic surfaces occur on both
and colour alone cannot separate the two, although light PVC and coloured plastic occur only on
objects. Both are carried through the same distribution of body poses, held forward, at the side,
slung on the back, or carried while walking, in the same proportions. However, an object whose
recorded length exceeds 1.15 m, which no weapon's recorded length does, is then re-angled in every
pose to rest on the shoulder or to point towards the ground (`07-blender/scripts/people_mpfb.py`,
`make_person`), so most confusable objects are carried at angles no weapon takes. A detector that
separates the classes on this corpus may therefore be using the length and silhouette of what is
carried, the light and coloured materials that only objects have, and the angle at which it is
carried, which is a rule of this generator rather than an observation of how residents carry things;
the rate at which it calls a broom a rifle is reported directly in Section 9.5. Two later corpora,
at 35 m and its twin at 75 m, depart from this in one respect, stated where they are reported: the
object is drawn in the firing pose with probability 0.08 rather than 0.42, the probability used for
the weapon (`07-blender/scripts/people_mpfb.py`, `make_person`), which is closer to how such objects
are carried.

### 7.5 Domain randomisation over illumination

Liao et al. (2026) measure that removing variation in sun position, weather and viewing angle costs
30.4 mAP50 points on YOLOv11, the detector used here, and 17.5 on average across the architectures
they test, with the largest penalty on truncated objects. The qualifications of Section 7.2 apply:
their object is vehicles and their test is on the reconstructed site. Illumination is randomised
here because it is the cheapest axis to vary and, for YOLOv11, the more costly of the two ablations
in that study (30.4 points against 27.0), though not on average across architectures (17.5 against
22 to 23).

Rather than jittering a single sun parameter, the generator defines six internally coherent lighting
budgets, each governing solar irradiance and colour, the angular diameter of the solar disc, a band
of solar elevation, sky fill and colour, atmospheric scattering density, aerosol content and a
camera exposure offset together: hard sun, low sun, overcast, haze, heavy overcast, and rain (the
mean frame luminances below include each regime's exposure offset). The angular diameter of the sun
is what separates these physically. At 0.6 degrees the shadow edge is hard; above roughly 20 degrees
the cast shadow effectively disappears, which is what a covered sky does. Mean frame luminance over
the 48 images of the pilot corpus `ds_morro_clima` (Section 8.3) runs 87.0 (hard sun), 56.0 (low
sun), 84.6 (overcast), 94.4 (haze), 55.6 (heavy overcast) and 35.1 (rain) of 255
(`06-resultados/contraste_clima.csv`, produced by `06-resultados/mede_contraste_clima.py`).

<!--FIG:06-resultados/figuras/fig2_climas.jpg|The six illumination regimes over an identical scene and identical framing. Top row: hard sun, low sun, overcast. Bottom row: haze, heavy overcast, rain. Over the 48 images of the corpus <code>ds_morro_clima</code>, not the six panels shown, mean frame luminance runs from 94.4 (haze) to 35.1 (rain) (<code>06-resultados/contraste_clima.csv</code>). Each regime is a coherent budget over solar irradiance, angular diameter of the solar disc, sky fill, scattering density and aerosol content, not a brightness adjustment.-->

The dataset sweeps the regimes in order rather than sampling them, so that a small corpus remains
balanced, and the regime of each image is written to its manifest entry. This permits the per-regime
analysis reported in Section 8.3 and the per-regime test that Section 10.3 specifies, which has not
been run.

### 7.6 Training protocol

The scale at which a target reaches the network is treated here as the governing variable, and the
reason is arithmetic before it is empirical. Downscaling a 4K frame to a 1536 pixel training input
divides every linear dimension by 2.5, so the median instance of the corpus of record, 17.6 by 17.5
pixels (Section 8.2), falls to about 7 by 7. The smallest stride of the detector is 8, so such an
instance occupies less than one cell of the finest feature map and is close to invisible to the
network by construction.

An earlier arm of this project recorded mAP50 moving from 0.116 to 0.561 between a run trained on
downscaled frames and a run trained on tiles at native scale
(`06-resultados/blender_v3/val_final.json` and `06-resultados/blender_v3_tiles2/val_final.json`,
written by `07-blender/scripts/train_yolo_win.py`, with the settings in the `args.yaml` beside each
run). That pair is reported here as consistent with the arithmetic and **not** as an isolated effect
of training scale, because the two runs differ in five further respects: detector size (YOLO11n
against YOLO11s), input size (1536 against 1280), epoch count (40 against 60), initialisation (COCO
weights against the checkpoint of a previous interrupted run) and the validation set on which each
score is computed (whole frames downscaled to 1536 px against native-scale tiles). No controlled
measurement of training scale alone exists in this project, and Section 11.1 states what would be
required to obtain one.

Synthetic training therefore operates on tiles cut at native scale with 20 per cent overlap, never
on downscaled frames, although the scale augmentation of the recipe rescales them at random; the
real-data models, R and the fine-tuning models of Section 9.4, train on whole VisDrone images
resized so that the long side is 1280 px, which downscales the most common training size, 1400 by
1050 (`06-resultados/alvo_por_split.json`).

| Parameter | Value |
|---|---|
| Detector | YOLO11s, Ultralytics 8.4.148, PyTorch 2.14.0, CUDA 12.6 |
| Hardware | Single NVIDIA RTX 2060, 6 GB |
| Initialisation | COCO pretrained weights for every model trained from scratch; the synthetic-start fine-tuning models of Section 9.4 start from S-oblique-six |
| Tile size, synthetic corpus at 4K | 1280 px at a stride of 1024 px (20 per cent overlap), with the last column and row aligned to the frame edge, so each 3840 by 2160 frame yields eight tiles and the edge tiles overlap their neighbours by more |
| Empty tiles retained as negatives | each tile without a box kept with probability 0.05 (`--keep-empty`, default of `07-blender/scripts/tile_dataset.py`); the realised share is printed in each tiling log and is not recorded under `06-resultados/` |
| Minimum retained fraction of a clipped box | 0.40 |
| Optimiser, learning rate | Ultralytics default (`optimizer=auto`), which ignores lr0 0.01 and at these training lengths selects AdamW, momentum 0.9, with an initial learning rate of 0.002 for the single-class models and 0.001429 for the three-class models (training logs), decaying linearly to 0.01 of that value after 3 warm-up epochs |
| Input size, batch | 1280 px, batch 6 |
| Augmentation | mosaic 1.0, switched off for the last 10 epochs; horizontal flip 0.5; rotation up to 10 degrees; scale gain 0.4; translation 0.1; HSV gains 0.015, 0.6 and 0.4 (`07-blender/scripts/train_yolo_win.py`; rotation, scale and saturation differ from the Ultralytics defaults of 0, 0.5 and 0.7) |
| Epochs | 60, stopping early after 15 epochs without improvement in validation mAP50-95, the Ultralytics fitness that also selects the reported checkpoint; 30 for the fine-tuning models of Section 9.4, selected the same way on their selection slice |
| Validation split | each rendered frame assigned to validation with probability 0.15 (`--val`, default of `07-blender/scripts/gen_morro.py`), realised as 24 to 35 frames per corpus; split by frame and not by tile, and within a corpus the validation frames show the same settlement as the training frames, from other camera positions, with other figures and light |
| Inference | conf 0.001, NMS IoU 0.7 (Ultralytics default, not tuned), reported at IoU 0.50 and 0.50 to 0.95; on VisDrone every model receives each image resized to 1280 px on its long side, as R is trained, so the 408 validation images of 1360 by 765 are slightly reduced and images of other sizes are enlarged or reduced accordingly |
| Seeds | training seed 0 with deterministic operations (Ultralytics defaults); the 1,106 images of R drawn with seed 21 (step 9 of `07-blender/scripts/fila_noite.py`); the fine-tuning and selection slices of Section 9.4 drawn with seed 2609 (`07-blender/scripts/prepara_ft.py`) |

Splitting the validation set by frame rather than by tile is necessary because overlapping tiles of
one frame are not independent; splitting by tile would place near-duplicates on both sides.
Precision and recall reported in Section 9, except in the table of Section 9.5, are those the
Ultralytics validator returns at the confidence that maximises F1, not at the 0.001 threshold used
to compute mAP.

### 7.7 Evaluation protocol and the reference ceiling

A detector evaluated on the world in which it was trained reports a ceiling, not evidence. A low
transfer score reported alone is equally uninterpretable, because nothing establishes the scale
against which to read it. The protocol therefore trains the models below. The single-class models
are evaluated on the same real test set, VisDrone-DET validation (548 images, 13,969 person
instances: the benchmark's pedestrian and people categories merged into one class, with its other
categories and its annotated ignored regions dropped by `03-arma3/scripts/visdrone_to_yolo.py`).
Every model is scored by the Ultralytics validator rather than the official VisDrone toolkit, so a
detection inside an ignored region, which that toolkit disregards, counts here as a false positive,
for R as for the synthetic models, though not necessarily to the same degree. Because no public
benchmark annotates a carried firearm, the three-class models are scored instead on the validation
split of their own corpus, whose tiles also served for early stopping and for selecting the
checkpoint, so that split is held out from training but not from model selection; Section 9.5
reports them separately: scored on the world in which they were trained, their figures are ceilings
rather than evidence of transfer, so the two groups cannot be read on one scale. Every synthetic
corpus holds the same number of images, 180 for the single-class models and 200 for the three-class
ones, so that no comparison below is a comparison of the number of frames, although instance counts
still differ (Section 8.2).

| Model | Training corpus | What it establishes |
|---|---|---|
| **R** | VisDrone-DET train, 1,106 images drawn at random, the number of training tiles in the synthetic corpus of record | The ceiling on the test set at matched volume |
| **S-nadir-150** | Synthetic, one settlement, camera straight down at 150 m, six illumination regimes | The method as proposed, at the acquisition geometry specified in Section 7.3 |
| **S-nadir-150-six** | The same, spread over six settlements | Whether variety of settlement is a term in the gap |
| **S-oblique** | The same settlement and generator settings, oblique camera (with the later weapon library, Section 9.3) | Whether failure is attributable to synthesis or to capture geometry |
| **S-oblique-six** | Six settlements, oblique camera at the calibrated pitch, figures carrying nothing | The best configuration of the generator: the synthetic model of this article |
| **S-nadir-75** | The same generator at 75 m, three classes with hard negatives | Whether the armed and unarmed distinction is resolvable |
| **S-nadir-35**, and its twin at 75 m | At 35 m with realistic carrying poses; the same corpus rendered at 75 m | Whether resolution or carrying pose drives the confusion |
| **F-synthetic, F-generic** | 5 or 10 per cent of VisDrone-DET train (324 or 647 images), starting from S-oblique-six or from COCO | What the synthetic pretraining is worth once some real data exists |

The reported efficacy of the synthetic method is mAP50(S) divided by mAP50(R): the fraction of the
ceiling reached without a single real training image. R is matched to the 1,106 training tiles of
the corpus of record; because tiling discards most empty tiles, the oblique models train on fewer
tiles, 968 for S-oblique and 890 for S-oblique-six (`06-resultados/RESULTADOS.md`), so for them the
match is by frame count rather than by training volume. The difference mAP50(S-oblique) minus
mAP50(S-nadir-150) estimates, from one training run per model, the contribution of capture geometry,
one effect of which Section 8.2 measures as a factor-of-two difference in target shape between this
corpus and the benchmark.
