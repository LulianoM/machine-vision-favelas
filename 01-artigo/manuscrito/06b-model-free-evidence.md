## Model-Free Evidence

> **Status note, 2026-09-20.** Every figure in this section is a direct measurement over image
> and annotation files, computed before any detector was trained and independent of whether any
> detector succeeds. Sources are given per table. Section 7 reports detector performance and
> currently carries `[X]` placeholders where measurement is still running.

Before reporting any detector performance, we characterise the problem the detector is being
asked to solve. This ordering is deliberate. Aerial person detection in dense informal settlement
is frequently discussed in terms of scene realism, and the implicit assumption is that a corpus
which looks more like a favela will transfer better. The three measurements below show that the
variables which actually govern difficulty are not the ones that realism addresses, and two of
them are invisible in any appearance metric.

### 6.1 The target is smaller than the sensor specification suggests

A person viewed from directly above does not present their height. The vertical dimension, which
is the one that makes a person conspicuous in a ground-level or oblique image, is precisely the
dimension that does not project in nadir. What the camera records is the plan of the figure:
roughly 0.48 metres shoulder to shoulder.

At 150 metres with the survey sensor this produces the following, measured over the annotation
files of three corpora:

| Corpus | Render resolution | GSD | Median target, long side | Below 8 px |
|---|---|---|---|---|
| Synthetic, 4K | 3840 x 2160 | 4.88 cm/px | 24.6 px | 0 per cent |
| Synthetic, 1080p | 1920 x 1080 | 9.76 cm/px | 10.1 px | 25 per cent |
| VisDrone-DET val (real) | mixed, mostly 1360 x 765 | not applicable | 25.0 px | 2 per cent |

*Sources: label files of `dataset_cid150` (4,856 instances), `ds_morro_clima` (565 instances) and
the converted VisDrone validation split (13,969 instances). The smallest stride of the detector is
8 pixels.*

Two consequences follow, and they point in opposite directions.

The first is a caution about our own headline figure. The survey camera records at 1080p. A single
frame from that camera at 150 metres therefore delivers a 10 pixel target, with a quarter of all
instances falling below one stride of the network. Rendering at 4K delivers a 24.6 pixel target.
Synthetic imagery rendered at 4K is thus materially easier than a single real frame from the
sensor it claims to reproduce, and any performance figure must declare the ground sampling
distance to which it refers. The photogrammetric orthomosaic produced from the same flight falls
between the two, at 6.4 to 7.4 cm per pixel, because it is stitched from overlapping frames.

The second is favourable and was initially mistaken for a problem. Measured at 4K, the median
synthetic target is 24.6 pixels and the median real benchmark target is 25.0 pixels. In apparent
size, the corpus and the benchmark are matched almost exactly. An earlier version of this analysis
reported a 2.49-fold scale gap between the two and attributed it to an altitude domain shift; that
gap was an artefact of a rendering resolution choice on our side, not a property of either corpus,
and is withdrawn.

### 6.2 Apparent size is matched; apparent shape is not

Size, however, is the wrong statistic. A detector learns a silhouette, not an area. Measuring the
aspect ratio of the same annotation sets gives:

| Corpus | Median width | Median height | Median h/w | h/w at 90th pct |
|---|---|---|---|---|
| VisDrone-DET val (real) | 12.0 px | 25.0 px | **2.20** | 3.17 |
| Synthetic, nadir at 150 m | 18.5 px | 22.9 px | **1.24** | 2.07 |

*Sources: as above, 13,969 and 4,856 instances respectively.*

The two corpora contain targets of comparable pixel area and incompatible shape. A height-to-width
ratio of 2.20 is a standing human figure recorded from an oblique viewpoint. A ratio of 1.24 is
the plan of a head and shoulders recorded from above. These are not two samples of one appearance
distribution; they are two different objects as far as the detector is concerned.

This is the domain shift that matters here, and it is invisible to every appearance-based measure
of realism. A generator could be made arbitrarily more photorealistic without moving this number
at all. It is also, unlike photorealism, cheap to manipulate: it is a property of where the camera
is placed, not of how the scene is built. Section 7 reports the S-oblique arm, in which the same
generator renders the same settlement from a camera calibrated to this measured ratio, and
Section 8.2 treats the difference between the two arms as the isolated cost of capture geometry.

### 6.3 Hard sunlight is the worst illumination regime for this task

The six illumination regimes permit a measurement that bears directly on operational practice.
For every annotated instance we computed the mean luminance inside the box, the mean luminance of
a six-pixel ring surrounding it, and the standard deviation of that ring. The first difference is
raw contrast; the difference divided by the ring deviation is contrast against local clutter,
which is what the detector actually faces.

| Regime | Absolute difference (DN) | Contrast over local clutter |
|---|---|---|
| Hard sun | **16.6** | **0.54** |
| Overcast | 15.3 | **0.83** |
| Haze | 10.6 | 0.77 |
| Heavy overcast | 9.8 | 0.71 |
| Low sun | 9.7 | 0.73 |
| Rain | **6.6** | 0.67 |

*Source: 684 instances across 48 images, eight per regime, corpus `ds_morro_clima`.*

Hard sunlight produces the largest raw separation between figure and background and the worst
separation once local clutter is accounted for. The mechanism is visible in the images and follows
from the scene description in Section 3.2: under a hard sun the background is itself filled with
sharp cast shadow from water tanks, parapets, clotheslines and cabling, the local deviation of the
background rises, and the figure ceases to stand out from the disorder. Under a covered sky the
background is smooth, and a smaller difference is more detectable.

This yields a prediction that runs against intuition and against the conventional preference for
flying in clear weather: **the detector should perform better under overcast than under hard
sun.** Section 8.3 tests it. If it holds, the operational implication is direct, and it is the
kind of implication that does not depend on the detector being good, only on it being measured.

### 6.4 What these three measurements imply for the proposal

Taken together, the measurements reframe the design problem stated in Section 3. The constraint is
not that a synthetic favela fails to look like a favela. At the scale at which this task operates,
the constraint is that the target is approximately 25 pixels of low-contrast texture, that its
silhouette is determined by camera placement rather than by scene content, and that the
illumination condition which maximises apparent contrast simultaneously maximises the background
clutter competing with it.

Whether these constraints can be overcome by synthesis alone, and by how much of the attainable
ceiling, is the subject of Section 7.
