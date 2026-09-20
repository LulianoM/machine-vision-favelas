## Methodology, continued: The Synthetic Data Generation Pipeline

> **Status note, 2026-09-20.** This subsection is additive. It extends Section 3 with the
> technical protocol and does not modify the research protocol, data collection, or positionality
> material written by the co-author. Every quantity reported here traces to a file under
> `06-resultados/` together with the command that produced it. Quantities not yet measured appear
> as `[X]` and are not to be filled by estimation.

The design-science component described above requires a concrete generative procedure. This
subsection specifies it. The account is deliberately detailed: the conference track to which this
work is addressed operates without discussants, so a methodological claim must be verifiable from
the text alone rather than defended in discussion.

### 3.1 Why synthesis, and what it does not solve

The ethical protocol stated above forecloses the conventional route to a training corpus. Aerial
imagery of an inhabited favela, at a resolution sufficient to resolve built form, necessarily
captures residents, rooftop activity, and address-level geometry. Synthesis is therefore not a
technical convenience. It is the only procedure we identified that yields a labelled corpus of the
required morphological specificity without collecting imagery of residents who have not consented
and who cannot meaningfully be asked under the conditions documented in Section 4.

Synthesis substitutes one problem for another. It removes the consent problem and introduces the
transfer problem: a detector trained on rendered imagery must operate on photographs. The
remainder of this subsection describes the generator. Sections 6 through 8 report what transfers
and what does not.

### 3.2 Scene construction

Scenes are generated procedurally in Blender 5.2 LTS, executed headless with a deterministic seed,
so that any reported image can be regenerated exactly from the seed recorded in its manifest
entry. No commercial asset packs are used: surface materials come from a public-domain library
(Poly Haven, CC0) and all geometry is authored by the generator. This matters twice over. It makes
the corpus redistributable, which the photogrammetric arms of this project are not, and it avoids
a documented failure mode, since Liao et al. (2026) measure a loss of 22.5 mAP50 points when a
photogrammetric base is replaced by generic assets.

Layout is produced in three stages, each addressing a specific way in which naive procedural
generation betrays itself when viewed from above.

**Parcelling.** The built core is subdivided by recursive binary partition. At each split the
boundary receives a gap drawn from a distribution whose modal value is zero: most party walls are
shared, as they are in consolidated self-built settlement. Non-zero gaps fall predominantly
between 0.5 and 1.2 metres, which is the alley, or beco, that defines the morphology. Wider
passages are rare by construction.

**Orientation.** A single binary partition, however deformed, leaves legible straight runs of ten
or twenty dwellings, and that is the strongest visual signature of procedural generation in a
nadir view. The generator therefore produces nine sub-districts, each with an independent
orientation, separated by a Voronoi diagram, reproducing the way consolidated settlement grows by
nuclei that meet at an angle. The result is verified rather than asserted: the fraction of edge
energy falling within 7.5 degrees of the cardinal axes is measured against the isotropic
expectation, and the generator is accepted only when that ratio approaches unity.

**Vertical accretion.** The dwelling is not a single prism. In the majority of cases with two or
more storeys the upper floor is smaller than the one below and offset toward one boundary, leaving
part of the lower slab exposed. Seen from above this produces the L-shaped footprint that
characterises the texture of the settlement, and it is the single geometric feature whose absence
most clearly reads as a grid of boxes rather than a favela. Storey count is drawn from a
low-frequency noise field rather than independently per dwelling, so that taller and shorter zones
form, as they do on a real hillside.

<!--FIG:06-resultados/figuras/fig1_nadir.jpg|A generated settlement seen from the virtual survey camera: nadir, 150 m above ground, rendered at 4K (4.88 cm/px). All geometry is authored by the generator and all materials are public domain. The three construction stages described above are visible: shared party walls with 0.5 to 1.2 m alleys, nine sub-districts meeting at an angle rather than a single orthogonal grid, and upper storeys offset from the floor below, which produces the L-shaped footprints that characterise the texture.-->

Roof surfaces carry the objects that occupy them in use: water tanks in three commercial volumes,
clotheslines, stair housings, satellite dishes, stacked roofing sheets, rubble, and exposed
reinforcement bar awaiting a further storey. Aerial cabling spans between rooftop anchor points.
These are not decoration. At the ground sampling distance of the target sensor they are the
dominant source of local clutter, and Section 6.3 shows that this clutter, rather than
illumination level, governs how hard a person is to detect.

<!--FIG:06-resultados/figuras/fig3_beco.jpg|The same generated scene at street level, inside an alley. The view is not used for training, which is conducted entirely from the aerial camera, and is shown because it is the check that the layout is three-dimensional built form rather than a texture painted to satisfy a top-down view.-->

### 3.3 Camera model

The virtual camera reproduces the sensor of the 2022 survey flight over the case study area: a
Zenmuse Z30 at 1920 by 1080, nadir, 150 metres above ground, corresponding to a 4.3 mm lens on a
5.37 mm sensor, or approximately 28.8 mm on a 36 mm equivalent. At that altitude the frame covers
approximately 187 by 105 metres of ground.

Rendering resolution is treated as a parameter distinct from sensor resolution, and the
distinction is consequential enough to state plainly. Ground sampling distance, not the nominal
resolution of the camera, determines whether a target survives to the network. Rendering the 150
metre nadir view at 1920 by 1080 yields 9.76 cm per pixel; rendering the same view at 3840 by 2160
yields 4.88 cm per pixel. Section 6.1 reports what this does to the target, and Section 9 states
the limitation it introduces.

### 3.4 Annotation

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
boxes. In a settlement this dense the discard rate is substantial and expected: a typical frame
retains roughly half the figures placed, the remainder being invisible in the alley from directly
above.

<!--FIG:06-resultados/figuras/fig5_anotacao.jpg|Automatically generated annotation. Green marks the armed class, blue the unarmed class; boxes are drawn with a four pixel outward offset so that they do not cover the target. The strip along the bottom shows individual targets magnified five times, with their true size in pixels printed beneath each one. At this ground sampling distance the target is a few pixels of low-contrast texture, which is the central difficulty characterised in Section 6.-->

### 3.5 Domain randomisation over illumination

Liao et al. (2026) measure that removing variation in sun position, weather, and viewing angle
costs approximately 10 mAP50 points, and approximately 20 on truncated objects. Illumination is
therefore randomised not as a stylistic choice but as the cheapest axis with a measured return.

Rather than jittering a single sun parameter, the generator defines six internally coherent
lighting budgets, each governing solar irradiance, the angular diameter of the solar disc, sky
fill, atmospheric scattering density, and aerosol content together: hard sun, low sun, overcast,
haze, heavy overcast, and rain. The angular diameter of the sun is what separates these
physically. At 0.6 degrees the shadow edge is hard; above roughly 20 degrees the cast shadow
effectively disappears, which is what a covered sky does. Mean frame luminance across the six
regimes spans 38 to 110 of 255.

<!--FIG:06-resultados/figuras/fig2_climas.jpg|The six illumination regimes over an identical scene and identical framing. Top row: hard sun, low sun, overcast. Bottom row: haze, heavy overcast, rain. Mean frame luminance runs from 110 (haze) to 38 (rain). Each regime is a coherent budget over solar irradiance, angular diameter of the solar disc, sky fill, scattering density and aerosol content, not a brightness adjustment.-->

The dataset sweeps the regimes in order rather than sampling them, so that a small corpus remains
balanced, and the regime of each image is written to its manifest entry. This permits the
per-regime analysis reported in Section 6.3 and the ablation in Section 8.

### 3.6 Training protocol

The scale at which a target reaches the network is the governing variable, and this project holds
a controlled measurement of it from an earlier arm. Holding the image set fixed at 120 images and
changing only the training scale, mAP50 moved from 0.116 to 0.561, a factor of 4.8, with no change
to the data itself (`06-resultados/RESULTADOS.md`). Downscaling a 4K frame to a 1536 pixel
training input reduces a target occupying 11 to 41 pixels to 4 to 16 pixels, and the smallest
stride of the detector is 8, so a 4 pixel target is close to invisible to the network by
construction.

Training therefore operates on tiles cut at native scale with 20 per cent overlap, never on
downscaled frames. The detector is YOLO11s (Ultralytics 8.4, PyTorch 2.14, CUDA 12.6) on a single
consumer GPU. Tile size, epoch count, batch size, and run identifiers are recorded alongside each
result in `06-resultados/`.

### 3.7 Evaluation protocol and the reference ceiling

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
minus mAP50(S-nadir) isolates the contribution of capture geometry, which Section 6.2 shows to be
the dominant mismatch between this corpus and the benchmark.
