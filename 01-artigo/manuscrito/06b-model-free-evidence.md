## 8. Model-Free Evidence

> **Provenance note.** Every figure in this section is a direct measurement over image and
> annotation files, independent of whether any detector succeeds. The tables name each corpus, the
> acquisition geometry that produced it (recorded per image or fixed by a generator setting, as each
> table states), and the instance count. Section 9 reports detector performance.

Before reporting detector performance we characterise the problem the detector is asked to solve.
The ordering follows the convention of this venue, in which model-free evidence precedes estimation.
It is also substantive here: aerial person detection in dense informal settlement is usually
discussed in terms of scene realism, and the implicit assumption is that a corpus which looks more
like a favela will transfer better. The measurements below identify two variables that plausibly
govern difficulty and that no appearance metric captures.

Three corpora are used throughout, two generated and one real, and Section 8.2 adds two oblique
generated corpora; their acquisition geometry differs in ways that matter, so the parameters are
stated rather than implied.

| Corpus | Geometry | Render | Instances |
|---|---|---|---|
| `ds_morro_clima` | camera within 3.5 deg of straight down (generator setting, not recorded per image), 28.8 mm equivalent, altitude 150 m | 1920 x 1080 | 565 (train split) |
| `ds_morro_4k` | same generator and geometry, rendered at 4K | 3840 x 2160 | 3,225 |
| VisDrone-DET validation | uncontrolled, real acquisition | mixed, mostly 1360 x 765 | 13,969 |

*Instance counts and image sizes: `06-resultados/alvo_por_split.json`, produced by `06-resultados/mede_alvo_split.py` (408 of the 548 benchmark images are 1360 x 765).*

`ds_morro_4k` is the corpus of record: it renders the reference acquisition specified in Section 7.3
and is the training corpus of model S-nadir-150 in Section 9. `ds_morro_clima` is its 1080p
predecessor, retained here because the comparison between the two isolates the effect of render
resolution from every other variable.

### 8.1 Ground sampling distance, not sensor resolution, sets the target size

A person viewed from directly above does not present their height. The vertical dimension, which
makes a person conspicuous in a ground level or oblique image, is exactly the dimension that does
not project in nadir. What the camera records is the plan of the figure, roughly 0.48 metres
shoulder to shoulder.

| Corpus | Render | GSD | Median long side | Shorter side below 8 px |
|---|---|---|---|---|
| `ds_morro_clima` | 1920 x 1080 | 9.76 cm/px | 10.1 px | 66.9 per cent |
| `ds_morro_4k` | 3840 x 2160 | 4.88 cm/px | 20.6 px | 0.8 per cent |
| VisDrone-DET val | not applicable | not applicable | 25.0 px | 30.5 per cent |

*Measured over the label files named in the table above: `06-resultados/alvo_por_split.json`,
produced by `06-resultados/mede_alvo_split.py` (the `ds_morro_clima` row on its training split,
`ds_morro_4k` on both splits, the benchmark on its validation split). The smallest stride of the
detector is 8 pixels, so an instance below that size occupies less than one cell of the finest
feature map.*

Two consequences follow, pointing in opposite directions.

The first is a caution about our own headline figure. The survey camera records at 1080p. A single
frame from that camera at 150 metres delivers a 10 pixel target on its long side, with two thirds of
all instances below one stride on the short side. Rendering at 4K delivers a 20.6 pixel target on
its long side. Synthetic imagery rendered at 4K is therefore materially easier than a single real
frame from the sensor it reproduces, and any performance figure must declare the ground sampling
distance to which it refers.

The column that carries the argument is the last one, and it is measured on the shorter side of the
box rather than the longer, because it is the shorter side that has to survive one stride of the
network. Read that way the benchmark is not the easy case: 30.5 per cent of its instances have a
side below 8 pixels, against 0.8 per cent of ours at 4K. Part of what any transfer figure reported
later measures is that the real benchmark contains a third of its targets at a scale no detector of
this family resolves well.

The second was initially mistaken for a problem. At 4K the median synthetic instance covers 301
square pixels and the median instance of the real benchmark, its training and validation splits
pooled, covers 300, a ratio of 1.00 (`06-resultados/alvo_4k_vs_visdrone.csv`, produced by
`06-resultados/mede_alvo.py`; the values per split are in `alvo_por_split.json`). The long side does
not match as closely, 20.6 against 25.0 pixels, because the two differ in shape rather than in size,
which is the subject of Section 8.2. An earlier version of this analysis reported a 2.49-fold scale
gap between corpus and benchmark and attributed it to an altitude domain shift. That gap was an
artefact of rendering our own corpus at 1920 by 1080, not a property of either corpus, and the claim
is withdrawn.

We report medians rather than claiming distributional equivalence. Two medians agreeing does not
establish that two distributions agree, and the comparison below is where the distributions in fact
separate.

### 8.2 Apparent size is comparable; apparent shape is not, and it varies with pitch

Size is the wrong statistic. A detector learns a silhouette, not an area. Measuring the aspect ratio
of the same annotation sets, and separating the synthetic corpus by the camera pitch recorded in its
manifest, gives:

| Corpus and geometry | Median width | Median height | Median h/w | Instances |
|---|---|---|---|---|
| `ds_morro_clima`, within 3.5 deg of straight down | 8.3 px | 8.2 px | **0.98** | 565 |
| `ds_morro_4k`, same geometry at 4K | 17.6 px | 17.5 px | **0.98** | 3,225 |
| `ds_morro_obl`, same settlement, pitch 26 to 52 deg recorded per image | 17.9 px | 26.4 px | **1.46** | 1,912 |
| `ds_oblvar`, six settlements, pitch 45 to 56 deg, figures carrying nothing | 13.3 px | 25.2 px | **1.85** | 1,521 |
| VisDrone-DET train, real acquisition | 13.0 px | 24.0 px | 1.95 | 106,396 |
| VisDrone-DET val, real acquisition | 12.0 px | 25.0 px | **2.20** | 13,969 |

*The two nadir rows carry the generator setting that produced them, which bounds the camera within
3.5 degrees of vertical but does not record it per image; the two oblique rows record pitch per
image. The benchmark rows are measured directly. Both benchmark splits are shown because the two
differ, and because the oblique arm of Section 9.3 is calibrated on the training split so that the
validation split remains untouched. The `ds_morro_4k`, `ds_morro_obl` and `ds_oblvar` rows are in
`06-resultados/forma_corpora.json`, produced by `06-resultados/mede_forma.py`; the `ds_morro_clima`
row and the two benchmark rows are in `06-resultados/alvo_por_split.json`, produced by
`06-resultados/mede_alvo_split.py`.*

The two nadir corpora differ by a factor of two in render resolution and by a factor of six in
instance count, and agree on this quantity to the second decimal: 0.98 in both. The real benchmark
sits at 1.95 and 2.20 on its two splits. The separation is therefore a factor of two, and it is
stable under a change of resolution that moves apparent size by the same factor.

The oblique corpus records the pitch of every image, so the same measurement can be split by camera
angle. It gives the dose-response that a contrast of two geometries cannot:

| Pitch recorded in the manifest | Instances | Median h/w, all figures | Median h/w, figures carrying nothing |
|---|---|---|---|
| 26 to 30 deg | 482 | 1.28 | 1.35 |
| 30 to 35 deg | 512 | 1.41 | 1.50 |
| 35 to 40 deg | 231 | 1.49 | 1.58 |
| 40 to 45 deg | 359 | 1.64 | 1.82 |
| 45 to 50 deg | 222 | 1.64 | 1.78 |
| 50 to 52 deg | 106 | 1.70 | 1.97 |

*Source: `06-resultados/forma_corpora.json`, produced by `06-resultados/mede_forma.py` from the
full-frame labels.*

The ratio rises with pitch, from 0.98 at the vertical to 1.70 at the steepest angle in the corpus,
and for figures carrying nothing it reaches the value of the benchmark's training split, 1.95, only
between 50 and 52 degrees, where it measures 1.97 on 49 figures. Two consequences follow for Section
9.3. The oblique corpus as rendered, with pitch drawn uniformly between 26 and 52 degrees, realised
a median of 1.46 rather than the 1.95 it was calibrated for, because most of its images sit below
the angle at which the benchmark's shape is reached. And the annotated box of an armed figure
includes the weapon, which widens it: 1.38 against 1.58 for figures carrying nothing in the same
images. The benchmark contains no carried firearms, so for transfer to it the weapon is a source of
shape mismatch rather than of signal. The combined model of Section 9.3 is built from these two
measurements, and its corpus, `ds_oblvar`, realises a median of 1.85.

A ratio near 1.0 is the plan of a head and shoulders recorded from above. A ratio near 2.0 is a
standing figure recorded obliquely. At comparable pixel area, these are different objects as far as
the detector is concerned.

This is a domain shift that matters here, and no appearance-based measure of realism detects it. A
generator could be made arbitrarily more photorealistic without moving this quantity. Unlike
photorealism it is also cheap to manipulate, being a property of where the camera is placed rather
than of how the scene is built. Section 9.3 reports the S-oblique model, in which the same generator
renders the same settlement from a tilted camera, and Section 10.4 treats the difference between the
two models as the contribution of acquisition geometry, together with the settings that change with
it.

One limit on the interpretation is stated here rather than in limitations. The nadir corpora record
a generator setting rather than a per-image pitch, and the benchmark values come from real imagery
whose acquisition geometry is not recorded at all. The oblique corpus anchors the slope on the
synthetic side; on the benchmark side only the endpoint is known.

### 8.3 Contrast against local clutter is higher under overcast than under hard sun and rain

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
follows from the scene description in Section 7.2: under a hard sun the background is itself filled
with sharp cast shadow from water tanks, parapets, clotheslines and cabling, the local deviation of
the background rises, and the figure stops standing out from the disorder. Under a covered sky the
background is smoother, so a comparable difference is easier to find.

What the sample supports and what it does not should be separated. With eight images per regime and
between-image dispersion of 0.12 to 0.38, only the gap between the extremes (rain and hard sun at
0.63 and 0.64, against overcast at 0.88) approaches one standard deviation, and the ordering of the
four intermediate regimes is not resolvable at this sample size. The measurement is therefore a
hypothesis about detector difficulty, not a finding about it: a contrast statistic is not a
detection statistic. Section 10.3 states the test and the condition under which the hypothesis is
withdrawn, and Section 11.3 the implication that is withdrawn with it.

### 8.4 What these measurements imply for the proposal

Taken together the measurements reframe the design problem stated in Section 6. The binding
constraint is not only that a synthetic favela fails to look like a favela. At the scale at which
this task operates, the target is a few tens of pixels of low contrast texture; its silhouette in
these corpora tracks camera pitch rather than scene content; and under hard sun, the illumination
conventionally preferred for flying, the regime with the second largest raw contrast has the second
lowest point estimate once local clutter is accounted for, which Section 8.3 attributes, as a
proposed mechanism, to cast shadow in the background; whether that makes detection harder is the
test of Section 10.3, which has not been run.

Whether these constraints can be overcome by synthesis alone, and what fraction of the
matched-volume ceiling is reached, is the subject of Section 9.
