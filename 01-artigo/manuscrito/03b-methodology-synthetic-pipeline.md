## 7. The Synthetic Data Generation Pipeline

> **Provenance note.** Every quantity in this section traces to a file under `06-resultados/`
> together with the command that produced it. Quantities not yet measured appear as `[X]`.

The design-science component of Section 5 proposes a model of vertical morphology and a
synthetic-training strategy. This section specifies the generative procedure that implements the
second of those, and reports what happens when it is executed.

A distinction has to be drawn at the outset, because the two are easy to conflate and the article
would contradict itself otherwise. The conceptual model proposed in Section 5 classifies built
form: building height, rooftop addition, material transition. What is implemented and evaluated
below detects people, which is a different task on the same imagery. The reason for implementing
the second rather than the first is that only it has a public benchmark against which transfer
can be measured, and the question at issue is whether synthesis transfers at all. The pipeline,
the annotation procedure, the randomisation and the scale analysis are shared; the object class is
not. Nothing below should be read as a validated capability over Jacarezinho, and Section 10
restates the boundary.

### 7.1 Why synthesis, and what it does not solve

The ethical protocol stated above forecloses the conventional route to a training corpus. Aerial
imagery of an inhabited favela, at a resolution sufficient to resolve built form, necessarily
captures residents, rooftop activity, and address-level geometry. Synthesis is therefore not a
technical convenience. It is the only procedure we identified that yields a labelled corpus of the
required morphological specificity without collecting imagery of residents who have not consented
and who cannot meaningfully be asked under the conditions documented in Section 3.

Synthesis substitutes one problem for another. It removes the consent problem and introduces the
transfer problem: a detector trained on rendered imagery must operate on photographs. The
remainder of this subsection describes the generator. Sections 8 through 10 report what transfers
and what does not.

### 7.2 Scene construction

Scenes are generated procedurally in Blender 5.2, executed headless with a deterministic seed,
so that any reported image can be regenerated exactly from the seed recorded in its manifest
entry. No commercial asset packs are used: surface materials come from a public-domain library
(Poly Haven, CC0) and all geometry is authored by the generator. This matters twice over. It makes
the corpus redistributable, which the photogrammetric arms of this project are not, and it avoids
a documented failure mode: Liao et al. (2026) report a substantial loss of accuracy when a
photogrammetric base is replaced by generic assets. We cite the direction of that result and not
its magnitude, because the specific figure has not been checked against the published text at the
time of writing, and because the object class in that study is vehicles rather than people.

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
dominant source of local clutter, and Section 8.3 shows that this clutter, rather than
illumination level, governs how hard a person is to detect.

<!--FIG:06-resultados/figuras/fig3_beco.jpg|The same generated scene at street level, inside an alley. The view is not used for training, which is conducted entirely from the aerial camera, and is shown because it is the check that the layout is three-dimensional built form rather than a texture painted to satisfy a top-down view.-->

### 7.3 Camera model

The virtual camera reproduces the sensor of the 2022 survey flight over the case study area: a
Zenmuse Z30 at 1920 by 1080, nadir, 150 metres above ground, corresponding to a 4.3 mm lens on a
5.37 mm sensor, or approximately 28.8 mm on a 36 mm equivalent. At that altitude the frame covers
approximately 187 by 105 metres of ground.

Rendering resolution is treated as a parameter distinct from sensor resolution, and the
distinction is consequential enough to state plainly. Ground sampling distance, not the nominal
resolution of the camera, determines whether a target survives to the network. Rendering the 150
metre nadir view at 1920 by 1080 yields 9.76 cm per pixel; rendering the same view at 3840 by 2160
yields 4.88 cm per pixel. Section 8.1 reports what this does to the target, and Section 11 states
the limitation it introduces.

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

### 7.5 Domain randomisation over illumination

Liao et al. (2026) report that removing variation in sun position, weather, and viewing angle
costs accuracy, with the largest penalty on truncated objects. As above, we rely on the direction
of that result rather than on the reported magnitudes, which we have not verified against the
published text. Illumination is randomised because it is the cheapest axis to vary and the one
the literature identifies as consequential, not because we can quote a figure for its value
here.

Rather than jittering a single sun parameter, the generator defines six internally coherent
lighting budgets, each governing solar irradiance, the angular diameter of the solar disc, sky
fill, atmospheric scattering density, and aerosol content together: hard sun, low sun, overcast,
haze, heavy overcast, and rain. The angular diameter of the sun is what separates these
physically. At 0.6 degrees the shadow edge is hard; above roughly 20 degrees the cast shadow
effectively disappears, which is what a covered sky does. Mean frame luminance over the training corpus runs
87.0 (hard sun), 56.0 (low sun), 84.6 (overcast), 94.4 (haze), 55.6 (heavy overcast) and 35.1
(rain) of 255 (`06-resultados/contraste_clima.csv`).

<!--FIG:06-resultados/figuras/fig2_climas.jpg|The six illumination regimes over an identical scene and identical framing. Top row: hard sun, low sun, overcast. Bottom row: haze, heavy overcast, rain. Mean frame luminance runs from 110 (haze) to 38 (rain). Each regime is a coherent budget over solar irradiance, angular diameter of the solar disc, sky fill, scattering density and aerosol content, not a brightness adjustment.-->

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
| Empty tiles retained as negatives | requested 6 per cent; realised 1.8 to 4.5 per cent depending on corpus density |
| Minimum retained fraction of a clipped box | 0.40 |
| Optimiser, learning rate | Ultralytics default, lr0 0.01 |
| Validation split | 15 per cent of generated scenes, split by scene and not by tile |
| Inference | conf 0.001, NMS IoU 0.7 (Ultralytics default, not tuned), reported at IoU 0.50 and 0.50 to 0.95 |

Splitting the validation set by scene rather than by tile is necessary because overlapping tiles
of one frame are not independent; splitting by tile would place near-duplicates on both sides.

### 7.7 Evaluation protocol and the reference ceiling

A detector evaluated on the world in which it was trained reports a ceiling, not evidence. A low
transfer score reported alone is equally uninterpretable, because nothing establishes the scale
against which to read it. The protocol therefore trains three models and evaluates all of them on
the same real test set, VisDrone-DET validation (548 images, 13,969 person instances, reduced to a
single class).

| Model | Training corpus | What it establishes |
|---|---|---|
| **R** | VisDrone-DET train, 6,471 images, 106,396 instances | The attainable ceiling on the test set |
| **S-nadir** | Synthetic, nadir at 150 m, six illumination regimes | The method as proposed, matching the 2022 survey geometry |
| **S-oblique** | Same generator, oblique and lower camera | Whether failure is attributable to synthesis or to capture geometry |

The reported efficacy of the synthetic method is mAP50(S) divided by mAP50(R): the fraction of the
attainable ceiling reached without a single real training image. The difference mAP50(S-oblique)
minus mAP50(S-nadir) isolates the contribution of capture geometry, which Section 8.2 shows to be
the dominant mismatch between this corpus and the benchmark.
