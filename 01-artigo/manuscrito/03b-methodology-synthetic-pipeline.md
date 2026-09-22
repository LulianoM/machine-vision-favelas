## 7. The Synthetic Data Generation Pipeline

> **Provenance note.** Every quantity in this section traces to a file under `06-resultados/`
> together with the command that produced it. Quantities not yet measured appear as `[X]`.

The design-science component declared in Section 5 and specified in Section 6 proposes a model
of vertical morphology and a synthetic-training strategy. This section specifies the generative procedure that implements the
second of those, and reports what happens when it is executed.

A distinction has to be drawn at the outset, because the two are easy to conflate. What is
implemented and evaluated below detects people, in three classes: armed, unarmed, and unarmed
carrying a confusable elongated object. That is the task this article measures, and it was
chosen because it is the only one of the two with a public benchmark against which transfer
can be established. The conceptual model proposed in Section 6 classifies built form instead:
building height, rooftop addition, material transition. The same generator already records the
footprint, the storey count and the roof height of every structure it builds, so the
morphological task is a second experiment over the same infrastructure rather than a different
pipeline; what it lacks is an evaluation set, and Section 11.4 records that absence as a
finding rather than as an omission. Nothing below should be read as a validated capability
over Jacarezinho, and Section 11 restates the boundary.

### 7.1 Why synthesis, and what it does not solve

The ethical protocol stated above forecloses the conventional route to a training corpus. Aerial
imagery of an inhabited favela, at a resolution sufficient to resolve built form, necessarily
captures residents, rooftop activity, and address-level geometry. Synthesis is therefore not a
technical convenience. It is the only procedure we identified that yields a labelled corpus of the
required morphological specificity without collecting imagery of residents who have not consented
and who cannot meaningfully be asked under the conditions documented in Section 3.

Synthesis substitutes one problem for another. It removes the consent problem and introduces the
transfer problem: a detector trained on rendered imagery must operate on photographs. The
remainder of this section describes the generator. Section 8 characterises the target before any
detector is trained, and Sections 9 and 10 report what transfers and what does not.

### 7.2 Scene construction

Scenes are generated procedurally in Blender 5.2, executed headless with a deterministic seed,
so that any reported image can be regenerated exactly from the seed recorded in its manifest
entry. No commercial asset packs are used: surface materials come from a public-domain library
(Poly Haven, CC0) and all geometry is authored by the generator. That choice makes the corpus
redistributable in full, and it is paid for.

Liao et al. (2026) measure the cost directly. Replacing a photogrammetric reconstruction of the
target site with generic assets costs 27.0 mAP50 points on YOLOv11, the detector used here, and
22 to 23 points on average across six architectures. In their taxonomy the corpus released with
this article sits on the generic side, not the photogrammetric one: it is procedural geometry
with public-domain materials, and it is on the losing side of that ablation by construction. Two
qualifications bound how far the figure travels. Their object class is vehicles rather than
people, and their evaluation is on the same site they reconstructed, so the result establishes
that a digital twin of a place helps detection at that place, not at another. This article
reports the trade rather than claiming to have avoided it. Measuring its size for this morphology
would require a photogrammetric reconstruction of the target site, which is precisely what the
ethical protocol of Section 5 forecloses, so the cost is quantified here from their result and
not from ours.

Layout is produced in three stages, each addressing a specific way in which naive procedural
generation betrays itself when viewed from above.

**Parcelling.** The built core is subdivided by recursive binary partition. At each split the
boundary receives a gap drawn from a distribution whose modal value is zero: most party walls are
shared, as they are in consolidated self-built settlement. In the released
configuration the gap is zero with probability 0.82, falls between 0.5 and 1.2 metres with
probability 0.12, between 1.3 and 2.0 metres with probability 0.05, and above 2.0 metres with
probability 0.008. The second band is the alley, or beco, that defines the morphology.

**Orientation.** A single binary partition, however deformed, leaves legible straight runs of ten
or twenty dwellings, and that is the strongest visual signature of procedural generation in a
nadir view. The generator therefore produces nine sub-districts, each with an independent
orientation, separated by a Voronoi diagram, reproducing the way consolidated settlement grows by
nuclei that meet at an angle. The result is measured. The statistic is the
fraction of edge energy falling within 7.5 degrees of a cardinal axis, divided by the isotropic
expectation. The measurement window covers 30 degrees of 180, so the isotropic expectation is one
sixth and unity means no preferred direction. In the released configuration the value is 0.90; in
the version of the generator that used a single partition it was 2.18
(`06-resultados/teste_fidelidade.csv`, `07-blender/HISTORICO-LOOP.md`).

An earlier draft of this article reported 1.62 for the same scene. That figure came from a
measurement script whose normaliser used 15 degrees of 180 rather than 30, inflating the whole
column by a factor of two. The error mattered beyond the digit: it placed the released
configuration above the isotropic expectation when it is in fact slightly below it. The script and
the recorded values were corrected, and the correction is noted here because the uncorrected
figure appeared in circulated drafts.

**Vertical accretion.** The dwelling is not a single prism. In the majority of cases with two or
more storeys the upper floor is smaller than the one below and offset toward one boundary, leaving
part of the lower slab exposed. Seen from above this produces the L-shaped footprint that
characterises the texture of the settlement, and it is the single geometric feature whose absence
most clearly reads as a grid of boxes rather than a favela. Storey count is drawn from a
low-frequency noise field rather than independently per dwelling, so that taller and shorter zones
form, as they do on a real hillside.

<!--FIG:06-resultados/figuras/fig1_nadir.jpg|A generated settlement seen from the virtual survey camera: nadir, 150 m above ground, rendered at 1920 by 1080, which gives 9.76 cm per pixel. The resolution is stated because Section 8.1 shows that ground sampling distance, not scene content, sets the size of the target; the corpus used for training is rendered at 3840 by 2160 and is twice as fine. All geometry is authored by the generator and all materials are public domain. The three construction stages described above are visible: shared party walls with alleys mostly between 0.5 and 1.2 m, nine sub-districts meeting at an angle rather than a single orthogonal grid, and upper storeys offset from the floor below, which produces the L-shaped footprints that characterise the texture.-->

Roof surfaces carry the objects that occupy them in use: water tanks in three commercial volumes,
clotheslines, stair housings, satellite dishes, stacked roofing sheets, rubble, and exposed
reinforcement bar awaiting a further storey. Aerial cabling spans between rooftop anchor points.
These are not decoration. At the ground sampling distance of the target sensor they are the
dominant source of local clutter, and Section 8.3 measures the contrast a person presents against
that immediate background, which Section 10.3 tests as a hypothesis about detector difficulty.

<!--FIG:06-resultados/figuras/fig3_beco.jpg|The same generated scene at street level, inside an alley. The view is not used for training, which is conducted entirely from the aerial camera, and is shown because it is the check that the layout is three-dimensional built form rather than a texture painted to satisfy a top-down view.-->

### 7.3 Camera model

The virtual camera reproduces a commercially available UAV payload in a configuration typical of
aerial survey over urban terrain: a Zenmuse Z30 at 1920 by 1080, pointing straight down, 150
metres above ground, corresponding to a 4.3 mm lens on a 5.37 mm sensor, or approximately 28.8 mm
on a 36 mm equivalent. The parameters are stated in full so that the acquisition conditions
evaluated here can be reproduced or contested without reference to any particular flight. At that altitude the frame covers
approximately 187 by 105 metres of ground.

Rendering resolution is treated as a parameter distinct from sensor resolution, and the
distinction is consequential enough to state plainly. Ground sampling distance, not the nominal
resolution of the camera, determines whether a target survives to the network. Rendering the 150
metre nadir view at 1920 by 1080 yields 9.76 cm per pixel; rendering the same view at 3840 by 2160
yields 4.88 cm per pixel. Section 8.1 reports what this does to the target, and Section 11 states
the limitation it introduces.

A second acquisition geometry is evaluated alongside the first, and the reason is arithmetic
rather than aesthetic. At 150 metres the target is too small for a carried object to be resolved
at all, which forecloses the question the article asks rather than answering it. The generator is
therefore also run with the same sensor at 75 metres, where the frame covers approximately 94 by
53 metres and the ground sampling distance halves to 2.44 cm per pixel at 3840 by 2160. Halving
the distance doubles each linear dimension of the target and quadruples its area before occlusion,
and measured on the generated corpora the median instance grows from 17.6 by 17.5 pixels to 47.6
by 41.7, a factor of 6.4 in area once the change in viewing angle within the frame is included.
The two altitudes are reported separately throughout, as `S-nadir-150` and `S-nadir-75`, because
they answer different questions: the first is the altitude at which aerial survey over urban
terrain is conventionally flown with this payload, and the second is the geometry under which the
distinction the article is named after becomes measurable at all.

### 7.4 Annotation

Human figures are instantiated from rigged, clothed meshes (MPFB, a MakeHuman derivative), posed
per instance, and placed both on rooftops and in the alley network. Placement uses an occupancy
map computed from the generated footprints, so that ground placement is known to fall in open
space rather than inferred by ray casting against arbitrary geometry.

Bounding boxes are neither drawn by hand nor inferred from a segmentation pass. For each figure
the generator projects the mesh vertices into image space, takes the axis-aligned extent, and
clips it to the frame. The convention is therefore amodal within the frame: the box covers the
whole figure, including parts hidden by intervening geometry, which is the convention used by the
real benchmark against which transfer is later measured. Occlusion is evaluated separately, by
casting fourteen rays from the camera to sample points on the figure, and instances whose visible
fraction falls below 0.35 are discarded from the label file rather than retained as degenerate
boxes. In a settlement this dense the discard rate is substantial and expected. Over 48 generated
frames the retained fraction has a median of 0.65 (10th percentile 0.44, 90th percentile 0.75):
about a third of the figures placed are invisible from directly above, most of them standing in
an alley.

<!--FIG:06-resultados/figuras/fig5_anotacao.jpg|Automatically generated annotation. Green marks the armed class, blue the unarmed class; boxes are drawn with a four pixel outward offset so that they do not cover the target. The strip along the bottom shows individual targets magnified five times, with their true size in pixels printed beneath each one. At this ground sampling distance the target is a few pixels of low-contrast texture, which is the central difficulty characterised in Section 8.-->

**Carried objects and hard negatives.** At 75 metres the corpus carries three classes rather than
two: armed, unarmed, and unarmed carrying an elongated object. The third exists because of an
objection that would otherwise be fatal to any figure reported for the first. If the weapon is
always the same asset, in the same pose, at the same contrast, a detector can separate the classes
on properties of the asset library rather than on anything visible in the world.

The corpus is built to remove that possibility. Five firearm models are generated
procedurally, spanning 0.20 to 1.05 metres in length: two rifles, a carbine, a shotgun and a
pistol. Against them stand nine elongated objects that a person carries in this territory, spanning
0.88 to 2.5 metres: brooms, rakes, plastic pipe, reinforcement bar, planks, umbrellas, hoes,
rolled mats and hose. Weapons and objects are drawn from the same palette of base colours and
surface roughness, so that no detector can separate the two by colour, and both are carried
through the same distribution of poses, held forward, at the side, slung on the back, or carried
while walking, in the same proportions. A detector that separates the classes on this corpus is
therefore doing so on the silhouette of what is carried, which is the only thing that could
transfer, and the rate at which it calls a broom a rifle is reported directly in Section 9.5.

### 7.5 Domain randomisation over illumination

Liao et al. (2026) measure that removing variation in sun position, weather and viewing angle
costs 30.4 mAP50 points on YOLOv11, the detector used here, and 17.5 on average across six
architectures, with the largest penalty on truncated objects. The qualifications of Section 7.2
apply: their object is vehicles and their test is on the reconstructed site. Illumination is
randomised here because it is the cheapest axis to vary and the one that result identifies as
the single most consequential.

Rather than jittering a single sun parameter, the generator defines six internally coherent
lighting budgets, each governing solar irradiance, the angular diameter of the solar disc, sky
fill, atmospheric scattering density, and aerosol content together: hard sun, low sun, overcast,
haze, heavy overcast, and rain. The angular diameter of the sun is what separates these
physically. At 0.6 degrees the shadow edge is hard; above roughly 20 degrees the cast shadow
effectively disappears, which is what a covered sky does. Mean frame luminance over the training corpus runs
87.0 (hard sun), 56.0 (low sun), 84.6 (overcast), 94.4 (haze), 55.6 (heavy overcast) and 35.1
(rain) of 255 (`06-resultados/contraste_clima.csv`).

<!--FIG:06-resultados/figuras/fig2_climas.jpg|The six illumination regimes over an identical scene and identical framing. Top row: hard sun, low sun, overcast. Bottom row: haze, heavy overcast, rain. Mean frame luminance runs from 94.4 (haze) to 35.1 (rain). Each regime is a coherent budget over solar irradiance, angular diameter of the solar disc, sky fill, scattering density and aerosol content, not a brightness adjustment.-->

The dataset sweeps the regimes in order rather than sampling them, so that a small corpus remains
balanced, and the regime of each image is written to its manifest entry. This permits the
per-regime analysis reported in Section 8.3 and the ablation in Section 10.

### 7.6 Training protocol

The scale at which a target reaches the network is treated here as the governing variable, and the
reason is arithmetic before it is empirical. Downscaling a 4K frame to a 1536 pixel training input
reduces a target occupying 11 to 41 pixels to 4 to 16 pixels. The smallest stride of the detector
is 8, so a 4 pixel instance occupies less than one cell of the finest feature map and is close to
invisible to the network by construction.

An earlier arm of this project recorded mAP50 moving from 0.116 to 0.561 between a run trained on
downscaled frames and a run trained on tiles at native scale. That pair is reported here as
consistent with the arithmetic and **not** as an isolated effect of training scale, because the
two runs differ in four further respects: detector size (YOLO11n against YOLO11s), input size
(1536 against 1280), epoch count (40 against 60) and initialisation (COCO weights against the
checkpoint of a previous interrupted run). No controlled measurement of training scale alone
exists in this project, and Section 11.1 states what would be required to obtain one.

Training therefore operates on tiles cut at native scale with 20 per cent overlap, never on
downscaled frames.

| Parameter | Value |
|---|---|
| Detector | YOLO11s, Ultralytics 8.4.148, PyTorch 2.14.0, CUDA 12.6 |
| Hardware | Single NVIDIA RTX 2060, 6 GB |
| Initialisation | COCO pretrained weights, identical for every model reported |
| Tile size, synthetic corpus at 4K | 1280 px, 20 per cent overlap |
| Empty tiles retained as negatives | requested 5 per cent; realised 0.8 to 4.5 per cent depending on corpus density, and 0.8 per cent in the corpus of record |
| Minimum retained fraction of a clipped box | 0.40 |
| Optimiser, learning rate | Ultralytics default, lr0 0.01 |
| Validation split | 15 per cent of generated scenes, split by scene and not by tile |
| Inference | conf 0.001, NMS IoU 0.7 (Ultralytics default, not tuned), reported at IoU 0.50 and 0.50 to 0.95 |

Splitting the validation set by scene rather than by tile is necessary because overlapping tiles
of one frame are not independent; splitting by tile would place near-duplicates on both sides.

### 7.7 Evaluation protocol and the reference ceiling

A detector evaluated on the world in which it was trained reports a ceiling, not evidence. A low
transfer score reported alone is equally uninterpretable, because nothing establishes the scale
against which to read it. The protocol therefore trains four models. Three of them, R,
S-nadir-150 and S-oblique, are evaluated on the same real test set, VisDrone-DET validation (548
images, 13,969 person instances, reduced to a single class). The fourth, S-nadir-75, carries three
classes and is scored on a held-out synthetic split instead, because no public benchmark annotates
a carried firearm; Section 9.5 reports it separately and Section 11.5 states why the two cannot be
read on one scale.

| Model | Training corpus | What it establishes |
|---|---|---|
| **R** | VisDrone-DET train, 6,471 images, 106,396 instances | The attainable ceiling on the test set |
| **S-nadir-150** | Synthetic, camera straight down at 150 m, six illumination regimes | The method as proposed, at the acquisition geometry specified in Section 7.3 |
| **S-nadir-75** | Same generator and sensor at 75 m, three classes with hard negatives | Whether the armed and unarmed distinction is resolvable at any altitude a drone flies |
| **S-oblique** | Same generator, oblique and lower camera | Whether failure is attributable to synthesis or to capture geometry |

The reported efficacy of the synthetic method is mAP50(S) divided by mAP50(R): the fraction of the
attainable ceiling reached without a single real training image. The difference mAP50(S-oblique)
minus mAP50(S-nadir-150) isolates the contribution of capture geometry, which Section 8.2 measures
as a factor-of-two difference in target shape between this corpus and the benchmark.
