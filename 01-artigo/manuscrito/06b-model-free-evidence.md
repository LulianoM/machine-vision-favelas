## 8. Model-Free Evidence

> **Provenance note.** Every figure in this section is a direct measurement over image and
> annotation files, computed before any detector was trained and independent of whether any
> detector succeeds. Each table names the corpus, the acquisition geometry recorded in its
> manifest, and the instance count. Section 9 reports detector performance and currently carries
> `[X]` where measurement is still running.

Before reporting detector performance we characterise the problem the detector is asked to solve.
The ordering follows the convention of this venue, in which model-free evidence precedes
estimation. It is also substantive here: aerial person detection in dense informal settlement is
usually discussed in terms of scene realism, and the implicit assumption is that a corpus which
looks more like a favela will transfer better. The measurements below identify two variables that
govern difficulty and that no appearance metric captures.

Three corpora are used, and their acquisition geometry differs in ways that matter, so the
parameters are stated rather than implied.

| Corpus | Geometry recorded in manifest | Render | Instances |
|---|---|---|---|
| `dataset_cid150` | pitch 50.0 to 89.9 deg (median 70.0), lens 30.1 to 50.0 mm, altitude 138 to 162 m | 3840 x 2160 | 4,856 (train split) |
| `dataset_cid150`, near-nadir subset | pitch at or above 88 deg, 29 images of the train split | 3840 x 2160 | 293 |
| `ds_morro_clima` | pitch 0.0 to 3.5 deg from nadir (generator setting, not recorded per image), 28.8 mm equivalent, altitude 150 m | 1920 x 1080 | 565 (train split) |
| VisDrone-DET validation | uncontrolled, real acquisition | mixed, mostly 1360 x 765 | 13,969 |

`dataset_cid150` is an earlier arm of this project built on photogrammetric terrain, and it is
used here only as a second independent sample of synthetic geometry. It is not the corpus
described in Section 7, which is `ds_morro_clima` and its 4K successor. Keeping the two separate
matters, because a measurement reported below changes sign depending on which is used, and an
earlier version of this analysis conflated them.

### 8.1 Ground sampling distance, not sensor resolution, sets the target size

A person viewed from directly above does not present their height. The vertical dimension, which
makes a person conspicuous in a ground level or oblique image, is exactly the dimension that does
not project in nadir. What the camera records is the plan of the figure, roughly 0.48 metres
shoulder to shoulder.

| Corpus | Render | GSD | Median long side | Below 8 px |
|---|---|---|---|---|
| `dataset_cid150` | 3840 x 2160 | 4.88 cm/px | 24.6 px | 0.0 per cent |
| `ds_morro_clima` | 1920 x 1080 | 9.76 cm/px | 10.1 px | 25 per cent |
| VisDrone-DET val | not applicable | not applicable | 25.0 px | 1.7 per cent |

*Measured over the label files named in the table above. The smallest stride of the detector is 8
pixels, so an instance below that size occupies less than one cell of the finest feature map.*

Two consequences follow, pointing in opposite directions.

The first is a caution about our own headline figure. The survey camera records at 1080p. A single
frame from that camera at 150 metres delivers a 10 pixel target, with a quarter of all instances
below one stride of the network. Rendering at 4K delivers a 20.6 pixel target on its long side. Synthetic imagery rendered
at 4K is therefore materially easier than a single real frame from the sensor it reproduces, and
any performance figure must declare the ground sampling distance to which it refers. The
photogrammetric orthomosaic built from the same flight falls between the two, at 6.4 to 7.4 cm per
pixel, because it is stitched from overlapping frames.

The second was initially mistaken for a problem. At 4K the median synthetic instance covers
301 square pixels and the median real benchmark instance covers 300, a ratio of 1.00. The long
side does not match as closely, 20.6 against 25.0 pixels, because the two differ in shape rather
than in size, which is the subject of Section 8.2. An earlier version of this analysis reported
a 2.49-fold scale gap between corpus and benchmark and attributed it to an altitude domain shift.
That gap was an artefact of rendering our own corpus at 1920 by 1080, not a property of either
corpus, and the claim is withdrawn.

We report medians rather than claiming distributional equivalence. Two medians agreeing does not
establish that two distributions agree, and the comparison below is where the distributions in
fact separate.

### 8.2 Apparent size is comparable; apparent shape is not, and it varies with pitch

Size is the wrong statistic. A detector learns a silhouette, not an area. Measuring the aspect
ratio of the same annotation sets, and separating the synthetic corpus by the camera pitch
recorded in its manifest, gives:

| Corpus and geometry | Median width | Median height | Median h/w | Instances |
|---|---|---|---|---|
| `dataset_cid150`, pitch at or above 88 deg | 20.8 px | 19.1 px | **0.93** | 293 |
| `ds_morro_clima`, pitch 0 to 3.5 deg from nadir | 8.3 px | 8.2 px | **0.98** | 565 |
| `dataset_cid150`, all pitches (median 70 deg) | 18.5 px | 22.9 px | 1.24 | 4,856 |
| `dataset_cid150`, pitch at or below 60 deg | 16.5 px | 25.5 px | 1.56 | 1,263 |
| VisDrone-DET val, real acquisition | 12.0 px | 25.0 px | **2.20** | 13,969 |

*For `dataset_cid150`, pitch is read from the manifest entry of each image. For `ds_morro_clima`
the manifest predates the field, so the value is the generator setting that produced the corpus,
which bounds pitch at 3.5 degrees from nadir but does not record it per image.*

Two synthetic corpora built by different generators, on different terrain, at different render
resolutions, agree to within 0.05 when both are restricted to true nadir: 0.93 and 0.98. The
quantity then rises monotonically as the camera is tilted, reaching 1.56 over the subset between
30 and 40 degrees off nadir, and the real benchmark sits at 2.20. This is an ordered relationship across five samples rather
than a contrast between two, which is what permits the interpretation.

A ratio near 1.0 is the plan of a head and shoulders recorded from above. A ratio of 2.20 is a
standing figure recorded obliquely. At comparable pixel area, these are different objects as far
as the detector is concerned.

This is the domain shift that matters here, and no appearance-based measure of realism detects it.
A generator could be made arbitrarily more photorealistic without moving this quantity. Unlike
photorealism it is also cheap to manipulate, being a property of where the camera is placed rather
than of how the scene is built. Section 9.3 reports the S-oblique model, in which the same generator
renders the same settlement from a tilted camera, and Section 10.4 treats the difference between
the arms as the isolated contribution of acquisition geometry.

One limit on the interpretation is stated here rather than in limitations. The monotonic series
above is measured within synthetic corpora, where pitch is known exactly. The benchmark value of
2.20 comes from real imagery whose acquisition geometry is not recorded, so it anchors the
direction of the relationship but not its slope.

### 8.3 Contrast against local clutter is lowest under hard sun and rain, not under low light

The six illumination regimes permit a measurement bearing on acquisition practice. For every
annotated instance we computed mean luminance inside the box, mean luminance of a six pixel ring
around it, and the standard deviation of that ring. The first difference is raw contrast; the
difference divided by the ring deviation is contrast against local clutter.

Instances within one image are not independent, so the statistic is aggregated per image and the
dispersion reported is between images.

| Regime | Mean frame luminance | Raw difference (DN) | Contrast over clutter, median per image | SD between images | Instances |
|---|---|---|---|---|---|
| Hard sun | 87.0 | 15.2 | **0.64** | 0.14 | 113 |
| Low sun | 56.0 | 9.0 | 0.70 | 0.20 | 117 |
| Overcast | 84.6 | **16.4** | **0.88** | 0.26 | 122 |
| Haze | 94.4 | 9.6 | 0.79 | 0.25 | 113 |
| Heavy overcast | 55.6 | 11.2 | 0.72 | 0.38 | 91 |
| Rain | 35.1 | 6.6 | **0.63** | 0.12 | 128 |

*684 instances across 48 images, eight per regime, corpus `ds_morro_clima`. Produced by
`06-resultados/mede_contraste_clima.py`; values in `06-resultados/contraste_clima.csv`.*

Overcast gives both the largest raw separation between figure and background and the largest
separation once local clutter is accounted for. Hard sun and rain are the two lowest on the latter
measure, and hard sun achieves that while sitting second on raw contrast. The proposed mechanism
follows from the scene description in Section 7.2: under a hard sun the background is itself
filled with sharp cast shadow from water tanks, parapets, clotheslines and cabling, the local
deviation of the background rises, and the figure stops standing out from the disorder. Under a
covered sky the background is smoother, so a comparable difference is easier to find.

What the sample supports and what it does not should be separated. With eight images per regime
and between-image dispersion of 0.12 to 0.38, only the gap between the extremes (rain and hard
sun at 0.63 and 0.64, against overcast at 0.88) approaches one standard deviation, and the
ordering of the four intermediate regimes is not resolvable at this sample size. The measurement
is therefore a hypothesis about detector difficulty, not a finding about it: a contrast statistic
is not a detection statistic. Section 11.3 states the test and the condition under which the
hypothesis is withdrawn.

### 8.4 What these measurements imply for the proposal

Taken together the measurements reframe the design problem stated in Section 5. The binding
constraint is not that a synthetic favela fails to look like a favela. At the scale at which this
task operates, the target is a few tens of pixels of low contrast texture; its silhouette in these
corpora tracks camera pitch rather than scene content; and the illumination condition that
maximises apparent contrast also maximises the background clutter competing with it.

Whether these constraints can be overcome by synthesis alone, and what fraction of the attainable
ceiling is reached, is the subject of Section 9.
