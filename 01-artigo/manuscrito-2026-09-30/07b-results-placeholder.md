## 9. Results: Transfer to Real Imagery and the Armed and Unarmed Distinction

Each model of the protocol in Section 7.7 was specified before that model was run, but the protocol
grew in stages: S-nadir-150-six, S-oblique-six, S-nadir-35 and its twins at 75 m and 150 m, and the
fine-tuning and joint models of Section 9.4 were added after earlier results in this section were
known. Section 10 declares in advance what would overturn the transfer results of Sections 9.1 to
9.3, as Section 11.4 does for the 75 m result of Section 9.5. Five models (S-oblique-six, the two
fine-tuning models at 5 per cent, S-nadir-35 and its twin at 75 m) were trained three times, with
training seeds 0, 1 and 2 on a fixed corpus (Section 10.6); every other model was trained once, so a
difference involving it carries no measured run-to-run dispersion. Nor does any VisDrone figure
carry an interval over the 548 test images, whose persons are clustered within images, so the
smaller differences between zero-shot figures, such as 0.0102 against 0.0190, rest on point
estimates alone.

Table @tab{visao} collects every model with its test set and headline figure; the sections below
give the protocol and the qualifications behind each number.

<!--TAB:visao|Results at a glance. Efficacy is mAP50 divided by that of R on the same real test set. Three-class models are scored on their own synthetic validation split, so their figures are ceilings rather than evidence of transfer.-->

| Model | Training data | Real training images | Test set | mAP50 | Efficacy |
|---|---|---|---|---|---|
| R | 1,106 images of VisDrone-DET train | 1,106 | VisDrone-DET val | 0.6311 | ceiling |
| S-nadir-150 | 180 frames, one settlement, nadir at 150 m | 0 | VisDrone-DET val | 0.0102 | 1.6 per cent |
| S-nadir-150-six | 180 frames, six settlements, nadir at 150 m | 0 | VisDrone-DET val | 0.0190 | 3.0 per cent |
| S-oblique | 180 frames, one settlement, oblique camera | 0 | VisDrone-DET val | 0.0614 | 9.7 per cent |
| S-oblique-six | 180 frames, six settlements, pitch 45 to 56 degrees | 0 | VisDrone-DET val | 0.1055 (mean of three runs 0.0967) | 16.7 per cent (15.3) |
| F-synthetic, 5 and 10 per cent | fine-tuned from S-oblique-six | 324 and 647 | VisDrone-DET val | 0.4424 and 0.5095 | 70.1 and 80.7 per cent |
| F-generic, 5 and 10 per cent | fine-tuned from COCO weights | 324 and 647 | VisDrone-DET val | 0.5220 and 0.5709 | 82.7 and 90.5 per cent |
| F-joint, 5 and 10 per cent | COCO weights, 890 synthetic tiles and the real images together | 324 and 647 | VisDrone-DET val | 0.4607 and 0.5428 | 73.0 and 86.0 per cent |
| S-nadir-75 | 200 frames, three classes, 75 m | 0 | synthetic validation | 0.579; calls 0.237 of confusable objects armed | not applicable |
| S-nadir-35 | 200 frames, three classes, 35 m | 0 | synthetic validation | 0.514; 0.273 (0.253 on new frames) | not applicable |
| Twin of S-nadir-35 at 75 m | the 35 m corpus rendered at 75 m | 0 | synthetic validation | 0.508; 0.165 (0.125 on new frames) | not applicable |
| Twin of S-nadir-35 at 150 m | the 35 m corpus rendered at 150 m | 0 | synthetic validation | did not pass its validity condition (148 of 297 figures found) | not applicable |

A pilot of the full protocol was run first, on a smaller corpus from another realisation of the
settlement rendered at 1080p. Its results are reported first, because they bound what follows and
because withholding an unfavourable pilot would make the rest of this section unreadable as
evidence.

<!--TAB:piloto|The pilot of the protocol: a two-class model trained on 40 scenes rendered at 1080p.-->

| Pilot run | Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| Pilot model (nadir, 150 m), 40 training scenes at 1080p | synthetic validation | 0.109 | 0.148 | 0.077 | 0.019 |
| same model | VisDrone-DET val, zero-shot | 0.038 | 0.031 | 0.0055 | 0.0020 |


These are not results about transfer: the model failed on its own domain, reaching 0.077 where the
corpus of record reaches 0.79 (Section 9.2), and transfer cannot be measured from a model that did
not learn. Two candidate causes are legible in the corpus statistics before any training, 40
training scenes (Section 10.1) and a render resolution at which two thirds of all instances fall
below one stride of the network (Section 8.1); neither has been isolated. The pilot also used a
different recipe (tiles and input of 640 pixels, batch 8, a budget of 120 epochs cut short by early
stopping) and two classes, armed and unarmed, so its synthetic validation figure is a mean over two
classes and is not on the single-class scale of the 0.79. What the pilot establishes is that this
pipeline is capable of failing. The rows below report the protocol re-run with both defects of the
pilot corpus corrected and with the recipe of Section 7.6.

### 9.1 Ceiling: what real training data achieves on this test set

Model R is trained on 1,106 images drawn at random from VisDrone-DET train (18,858 person
instances), the same number of training images as the tiled synthetic corpus of record, and
evaluated on VisDrone-DET validation. Holding the number of training images equal lets the ratio in
Section 9.2 speak to the data at a matched number of images, though not of instances: the images of
R hold 18,858 persons against 2,659 in the 149 training frames of the synthetic corpus of record
(3,225 in all 180). A run on the full training split (6,471 images) was started and stopped before
completion: with roughly six times as many images per epoch, it would have cost far more machine
time than the matched run to improve a denominator whose role is to be matched, not maximised.

<!--TAB:teto|The ceiling: R, trained on 1,106 real images, on VisDrone-DET val.-->

| Model | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| R (1,106 real training images) | 0.7312 | 0.5729 | 0.6311 | 0.2538 |

This figure is the denominator for everything that follows. It is not a claim about our method; it
establishes what the test set permits at this volume of data.

### 9.2 Transfer from synthetic training, nadir geometry

Model S-nadir-150 is trained only on procedurally generated imagery with the camera geometry of
Section 7.3 and evaluated on the same real test set with no real training image of any kind.

<!--TAB:nadir|S-nadir-150 on its own validation split and on the real test set, zero-shot.-->

| Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Synthetic validation (ceiling of the corpus) | 0.8707 | 0.7413 | 0.7915 | 0.3656 |
| VisDrone-DET val (zero-shot) | 0.0856 | 0.0421 | 0.0102 | 0.0025 |

**Efficacy of the synthetic method** = mAP50(S-nadir-150) / mAP50(R) = 0.0102 / 0.6311 = 1.6 per cent.

**Variety of settlement at fixed volume.** The corpus of record renders one settlement. Model
S-nadir-150-six keeps every setting of the generator other than those that define the settlement,
and the number of images, fixed and spreads the 180 images over six settlements, 30 each (Figure
@fig{fig6_assentamentos}), differing in relief, forest cover, a corridor through the core (an
avenue, a narrow street or a river) and the palette of roofs and facades, and also in the extent of
the built core, the number of sub-districts, the distribution of storey counts and the share of
vacant lots. It was rendered with the later generator, so its armed figures carry the five weapon
models of Section 7.4, which the corpus of record predates.

<!--TAB:variedade|One settlement against six at a fixed number of frames, nadir at 150 m.-->

| Model | Synthetic validation mAP50 | VisDrone-DET val mAP50 | mAP50-95 | Efficacy |
|---|---|---|---|---|
| S-nadir-150, one settlement | 0.7915 | 0.0102 | 0.0025 | 1.6 per cent |
| S-nadir-150-six, six settlements | 0.6786 | 0.0190 | 0.0071 | 3.0 per cent |

Variety nearly doubles the transfer figure and lowers the score on the model's own validation split,
which is consistent with a model that has stopped memorising one scene, although the two validation
splits are different sets. From one training run per model it is a candidate term in the gap, and in
Section 9.3 it moves the transfer figure less than capture geometry does.

<!--FIG:06-resultados/figuras/fig6_assentamentos.jpg|The six settlements over which S-nadir-150-six and S-oblique-six spread their 180 images, one frame of each from the S-oblique-six corpus, all under the hard-sun regime. They differ in relief, forest cover, a corridor through the core (an avenue, a narrow street or a river) and the palette of roofs and facades. Settlement 1 is the one rendered in the corpus of record.-->

Kiefer, Ott and Zell (2022) report mAP50 on VisDrone of 1.2, 2.4 and 10.2 points for three
architectures trained purely on synthetic data, against 24.6, 48.6 and 43.9 for the same
architectures trained on real data; the YOLO row, the comparable one, gives a ratio of 23.2 per
cent. The two ratios are not directly comparable: their denominator is trained on the full training
split and scored over ten classes, ours on 1,106 images and a single person class, and their
synthetic corpus holds 40,000 game-engine images against 180 scenes here. These differences do not
all act in the same direction, so this design cannot say which ratio is the harsher.

### 9.3 Transfer from synthetic training, oblique geometry

Model S-oblique keeps the settlement, the illumination regimes and the generator settings identical;
the camera is moved (Figure @fig{fig8_nadir_obliquo}), together with the figure-placement filter
that depends on it (Section 10.4). One further difference comes from the generator's history rather
than from the camera: the nadir corpus was rendered before the five-model weapon library of Section
7.4 existed, so its armed figures carry one of three rifle patterns or a pistol and are held forward
with probability 0.46 rather than 0.42, while those of the oblique corpus carry the five models; the
share of armed figures is the same in both.

Pitch is set from the height-to-width ratio of the VisDrone **training** split, not the validation
split on which every model in this article is scored. The distinction is load-bearing: the ratio of
2.20 quoted in Section 8.2 is measured on the validation split, and calibrating a training corpus on
a statistic of the test set and then reporting the gain on that same test set would be circular. The
value used for calibration is 1.95, measured on the training split alone (Section 8.2).

This arm is therefore an adaptation of the corpus to the benchmark, and is reported as such rather
than as a discovery about acquisition geometry in general. What it tests is whether camera geometry,
which moves the mismatch identified in Section 8.2 together with the perspective of the rest of the
scene, is load-bearing on this benchmark.

<!--TAB:obliquo|Nadir against oblique acquisition on the real test set.-->

| Model | mAP50 on VisDrone-DET val | Efficacy vs. ceiling |
|---|---|---|
| S-nadir-150 | 0.0102 | 1.6 per cent |
| S-oblique | 0.0614 | 9.7 per cent |
| S-oblique-six | 0.1055 (mean of three runs 0.0967) | 16.7 per cent (15.3) |

**Difference attributable to acquisition geometry, on this benchmark** = mAP50(S-oblique) -
mAP50(S-nadir-150) = 0.0512, a factor of 6.0.

<!--FIG:06-resultados/figuras/fig8_nadir_obliquo.jpg|The same settlement under the two camera geometries compared in this section: straight down from 150 m, the reference acquisition of this study, and oblique from about 120 m, closer to the benchmark's. Below each frame, four figures carrying nothing, enlarged to the same size without smoothing. Seen from above, a person is the plan of the whole figure, about as wide as it is long, with a median height-to-width ratio of 0.98 over all figures in the nadir corpus; seen obliquely, a standing figure with its limbs, with a median of 1.58 for figures carrying nothing in the oblique corpus (1.46 over all figures), against 1.95 in the benchmark's training split (Section 8.2). Trained on each, the detector reaches 1.6 and 9.7 per cent of the real-data ceiling on the benchmark.-->

Two outcomes were reportable, and both were fixed before the run: if the oblique arm substantially
outperforms the nadir arm, acquisition geometry is load-bearing on this benchmark, consistent with
the direction of Liao et al. (2026) without extending their claim, since a single benchmark that is
not the target domain cannot support a general statement about camera position; if the two arms are
comparable, the limitation lies in synthesis rather than viewpoint. The first obtained. With the
settlement and the training recipe held fixed, the oblique model transfers 6 times better than the
nadir model, against a factor of 1.9 for six settlements instead of one, so on this benchmark the
change of camera moves the transfer figure more than variety of settlement does (that comparison was
not among the criteria, since the variety arm was added after the nadir result). The oblique figure
falls within the synthetic-only range reported by Kiefer, Ott and Zell (2022), although their
figures average ten VisDrone classes.

The oblique corpus did not reach the shape it was calibrated for, 1.46 against 1.95, for the two
reasons measured in Section 8.2. Model S-oblique-six combines the two terms and corrects the
calibration: six settlements of 30 images; pitch between 45 and 56 degrees, chosen to centre the
median of figures carrying nothing on the benchmark's shape, which in the single-settlement oblique
corpus they reach only between 50 and 52 degrees; and only such figures. Its camera placement is
also redrawn, target, pitch and heading together and at most 30 times, until the camera stands at
least 45 m above the ground beneath it and the ray through the centre of the frame first strikes the
scene within 30 m of the target rather than on forest or hillside. It is not an ablation, since
several things change at once; it is the best configuration of this generator tried here and the
model the rest of this article calls the synthetic model. Result: mAP50 0.1055 on VisDrone-DET val
(precision 0.2631, recall 0.1716, mAP50-95 0.0329), an efficacy of 16.7 per cent: 10.3 times the
nadir model and 1.7 times the single-settlement oblique model, against 0.7047 on its own synthetic
validation. Trained twice more on the same corpus with other training seeds, it reaches 0.0958 and
0.0887, so its efficacy averages 15.3 per cent over three runs, between 14.1 and 16.7; the first
run, reported above and in the table, was the best of the three. Under the official VisDrone rule
for ignored regions (Section 7.7) every mAP50 in this section rises slightly, R to 0.6548 and the
first run of S-oblique-six to 0.1074, while every efficacy falls slightly, that of S-oblique-six
from 16.7 to 16.4 per cent, and no comparison between the models of Sections 9.1 to 9.3 changes
order at an intersection-over-union of 0.50, 0.60 or 0.75. The rendered figure approaches the
calibration target without reaching it: a median height-to-width ratio of 1.85 at 13.3 by 25.2
pixels, against 1.95 at 13.0 by 24.0 in the benchmark's training split (Section 8.2). In absolute
terms, the 10.5 points of mAP50 of the first run sit just above the upper end of that synthetic-only
range and the 9.7 of the mean of three runs just inside it, under the same difference in classes,
while the ratio to our own ceiling stays below theirs (Section 9.2).

The acquisition geometry this article reproduces points straight down. An oblique corpus that
transfers better to VisDrone is informative about the benchmark, not about the acquisition that
would be flown over Jacarezinho.

### 9.4 Limited real fine-tuning, on the public benchmark only

The proposal of Section 6 reserves a stage in which the synthetic pretraining is fine-tuned on a
modest volume of real imagery. It is run here on the public benchmark only, as a line separate from
the synthetic-only results above so that the two contributions stay distinguishable, and no imagery
of the case study territory is involved.

The protocol was fixed before the run. Two slices of the VisDrone-DET training split, 5 per cent
(324 images) and 10 per cent (647 images, containing the first), each train two models: one
initialised from the synthetic model of Section 9.3 and one from the same generic initialisation as
every other model in this article. The synthetic start carries over every weight, including a
detection head already trained for one person class, whereas the generic start re-initialises the
last classification layer of the COCO head, which has eighty classes; the synthetic start therefore
begins as a working person detector, consistent with its lead in the first three epochs at 5 per
cent, although at 10 per cent the generic start leads from the first epoch, and the result below
holds despite that head start. The checkpoint is selected on a further 5 per cent of the training
split, disjoint from both, so that the validation split on which every figure here is scored is not
used for selection, which removes for this comparison the asymmetry declared in Section 10.5. All
four models train for thirty epochs with the same detector, input size and augmentation. Both starts
receive the same untuned schedule of Section 7.6, AdamW at 0.002 with three warm-up epochs, although
one of them is already a person detector, and no lower learning rate, frozen layers or longer budget
was tried for either. On the selection slice all four models reach their best mAP50 and mAP50-95
between epochs 27 and 30 of 30, so the comparison is at a fixed budget rather than at convergence,
although the generic start's lead on that slice does not narrow between epoch 20 and epoch 30.

<!--TAB:ajuste|Fine-tuning on 5 and 10 per cent of the benchmark's training split from the synthetic model and from generic weights.-->

| Real training data | F-synthetic (from S-oblique-six) | F-generic (from COCO) | Difference |
|---|---|---|---|
| 5 per cent (324 images) | 0.4424 | 0.5220 | -0.0796 |
| 10 per cent (647 images) | 0.5095 | 0.5709 | -0.0614 |

*mAP50 on VisDrone-DET val under the protocol of Section 9.1.*

<!--FIG:06-resultados/figuras/fig10_ajuste_fino.png|mAP50 on VisDrone-DET val against the number of real training images, for the three ways of using the synthetic corpus once real images exist: as the starting weights (synthetic start), mixed into the training set (joint), or not at all (generic start). Filled markers are the first training run, reported in the table; open markers are the two further runs where they exist. The dashed line is R, trained on 1,106 real images for twice as many epochs. At both volumes the generic start ends highest and the synthetic start lowest.-->

The quantity of interest is the difference at each volume: what the synthetic pretraining is worth
when real data is scarce (Figure @fig{fig10_ajuste_fino}). The expectation, stated before the run,
was that it would be largest at the smaller volume.

It is negative at both. Initialised from the synthetic model, the detector finishes 8.0 points of
mAP50 below the generic initialisation with 5 per cent of the real data and 6.1 points below with 10
per cent, and the synthetic start given 647 real images (0.5095) does not reach the generic start
given 324 (0.5220). The sign is the same in mAP50-95, the metric on which every checkpoint was
selected: -0.0368 at 5 per cent and -0.0232 at 10 per cent. The expectation stated before the run
therefore fails: the difference is not largest at the smaller volume but most negative there. Its
magnitude narrows as real data grows, but what narrows is a cost, not a benefit. On the selection
slice the generic start overtakes the synthetic one by the fourth epoch at 5 per cent and in the
first epoch at 10 per cent, after which the synthetic start leads only intermittently. Fine-tuning
does transform the synthetic model itself, from 0.1055 to 0.4424 with 324 real images, which is the
effect the sim-to-real literature reports; what it does not do here is outperform a generic start
given the same real images. Relative to the ceiling of Section 9.1, trained on 1,106 real images for
twice as many epochs, the generic start recovers 82.7 and 90.5 per cent and the synthetic start 70.1
and 80.7 per cent. Repeated at 5 per cent with training seeds 1 and 2, each synthetic start from the
S-oblique-six model of the same seed, the synthetic start reaches 0.4608 and 0.4554 and the generic
start 0.5228 and 0.5285: the lowest of the three generic runs lies above the highest synthetic one,
so the difference exceeds the spread between runs by the criterion fixed in advance (Section 10.6).
On this benchmark and at these volumes the synthetic corpus does not substitute for real data; it
costs some. One candidate explanation, not tested here, is that training on 890 tiles of generated
figures overwrites part of what the generic initialisation encodes about real people; the joint
models below, which keep that initialisation and see the real images throughout, bear on it.

**Joint training.** Pretraining is one way to use the synthetic corpus; training on synthetic and
real imagery together is the other, and it was specified with its criterion before it was run. Two
models (F-joint) start from COCO and train for 30 epochs on the 890 synthetic tiles of S-oblique-six
together with the same 324 or 647 real images, selected on the same slice. Each real image is seen
as often as in the generic start, but every epoch also carries the synthetic tiles, so these models
take more gradient steps. They reach 0.4607 at 5 per cent and 0.5428 at 10 per cent, 0.0613 and
0.0281 below the generic start given only the real images, beyond the margin fixed in advance, twice
the standard deviation of the three generic runs at 5 per cent (0.0035), a standard deviation that
at 10 per cent is borrowed from the 5 per cent runs. Mixed in, the synthetic corpus costs less than
as pretraining at an intersection-over-union of 0.50 and 0.60, though at 10 per cent not at 0.75,
but it still costs: on this benchmark neither way of adding it to real data helped. That keeping the
generic initialisation and showing the real images from the first epoch reduces the cost without
removing it suggests that the explanation offered above is at most part of the account.

This result departs from the closest precedent only in part. Kiefer, Ott and Zell (2022) pretrained
a COCO-initialised YOLO on up to 40,000 game-engine images generated to match VisDrone's traffic
scenes and found the gain on VisDrone largest with the smallest real set. Their figure 2 also shows,
however, that pretraining on only 10,000 synthetic images scored below no synthetic pretraining at
every real-data size on their maritime benchmark, and gave no consistent gain on VisDrone beyond the
smallest real set. Our corpus holds 890 tiles of six generated settlements. Negative transfer (Wang
et al., 2019) recurs in aerial person detection. On the full VisDrone training split, pretraining on
either of two public synthetic corpora scored below training from scratch at most detector sizes. A
corpus designed for diverse human motion scored above it and, combined with COCO in pretraining,
above COCO alone on the one detector size tested (Yim et al., 2026). Mixing synthetic with real
images fell below the real-only baseline in low-shot VisDrone training (Shen et al., 2023b). It
harmed the larger COCO-pretrained detectors most when real images were fewest, and much less once
the two shares were balanced (Shen et al., 2023a). With unbalanced batches, it biased a drone
detector of people at sea towards the more numerous synthetic images (Martinez-Esteso et al., 2025).
These findings are consistent with our joint-training cost, which narrows as the real share grows.
The candidate mechanism has only indirect support, from training on renders alone: retraining a
feature extractor pretrained on real images degraded detection, whereas freezing it came close to
training on real images (Hinterstoisser et al., 2019), although freezing hurt with highly randomised
scenes (Tremblay et al., 2018). At these volumes the starting weights weigh most (He et al., 2019),
and this design cannot tell which property of the corpus decides the sign: its size, its variety or
its image domain, the factor that most determines positive transfer (Mensink et al., 2022).

### 9.5 The armed and unarmed distinction, by altitude

No accuracy for the armed and unarmed distinction is reported at 150 m. At that altitude the median
instance measures 17.6 by 17.5 pixels, and a firearm is argued from resolution, not shown by
measurement, to be unresolvable within it. No model was trained to separate the classes on the
corpus of record, and a detector that did so there could be relying on the weapon being the only
elongated object any figure carries, so its separability could not be told apart from a property of
the generator. A three-class model was later trained at 150 m on a twin of the 35 m corpus described
below, identical to it in every setting except altitude and its jitter, and so with the confusable
objects the corpus of record lacks. A validity condition was fixed before it was run: the model had
to find at least half of the annotated figures, in any class. It found 148 of 297 (0.498), so its
rates are not interpretable and are not reported as a result; descriptively, it calls 0.34 of armed
figures and 0.14 of confusable objects armed, which taken at face value would separate the classes
rather than support the absence, plausibly by the length of what is carried rather than the form of
a firearm. The absence at 150 m therefore remains argued, not measured.

At 75 m the median instance measures 47.6 by 41.7 pixels, 6.4 times the area over all classes (5.2
times for armed figures alone, Section 7.3), and the corpus is built so that the artefact cannot
account for the result: five firearm models against nine elongated objects carried in the same
territory, sharing the weapons' colour and roughness palette and the same distribution of body
poses, though objects longer than any weapon are held at other angles (Section 7.4). The corpus
holds 2,887 instances in 200 images, 933 of them armed, 973 unarmed and 981 carrying a confusable
object. A second corpus at 35 m, 1.1 cm per pixel, holds 2,223 instances with a median of 121.8 by
103.1 pixels (Figure @fig{fig7_armados}).

<!--FIG:06-resultados/figuras/fig7_armados.jpg|Figures carrying a rifle, a pistol, nothing, a broom, a length of pipe or a closed umbrella at the three altitudes of this section, each cropped from a rendered frame and scaled to the same size without smoothing, so that every crop shows the pixels the detector receives. The carrying figures were chosen by eye, among isolated figures under clear light, as ones whose item sits in the hand and close to the horizontal, so that its full length shows; in many frames the item points steeply downward and appears foreshortened, or does not sit in the grip, because of how the generator places it (Section 7.4). At 35 m the weapons and the objects are distinct shapes; at 75 m they survive as lines of different length and tone; at 150 m, the reference altitude, the whole figure is a few tens of pixels, the rifle and the pistol cannot be told from the body, and a long object such as the pipe, the broom or the umbrella still shows as a line. The crops at 35 m and 75 m come from the corpus at 35 m, its twin at 75 m and the new frames rendered with their settings; those at 150 m from the twin corpus whose model did not pass its validity condition.-->

<!--TAB:armado|The armed and unarmed distinction on the validation split of each three-class corpus.-->

| Quantity | S-nadir-75 (75 m) | S-nadir-35 (35 m) | Twin of S-nadir-35 at 75 m |
|---|---|---|---|
| mAP50, three classes | 0.579 | 0.514 | 0.508 |
| Recall, armed | 0.547 | 0.569 | 0.471 |
| Precision, armed | 0.386 | 0.415 | 0.440 |
| Rate at which a confusable object is called armed | 0.237 | 0.273 | 0.165 |
| Rate at which an unarmed person with no object is called armed | 0.131 | 0.168 | 0.109 |

*Protocol: inference on the full 4K frame at native scale; for the rates, confidence 0.25 and
one-to-one matching at an intersection-over-union of 0.50 that ignores the predicted class, each
person taking the class of its best-overlapping prediction, so that a second box of another class on
the same person counts only against precision; the validation split of each corpus (27, 35 and 24
images). The threshold of 0.25 is the Ultralytics default for prediction and was not tuned; every
rate depends on it and varies with the realisation of the settlement: in the new realisation of
Section 11.4 the S-nadir-75 model calls 0.15 of confusable objects and 0.43 of armed persons armed,
against 0.237 and 0.547 here. The rates also give d′, the difference between the normal quantiles of
the armed recall and of the rate at which the other class is called armed, which under the usual
equal-variance assumption separates how well a model distinguishes two classes from how readily it
calls a figure armed: against confusable objects 0.83, 0.78 and 0.90 in the three columns, against
unarmed persons 1.24, 1.14 and 1.16; the replication below uses a log-linear correction for rates
near zero or one, under which the validation-split values against confusable objects are 0.77 and
0.89 for S-nadir-35 and its twin. The third column is the matched corpus described below.*

The fourth row is the quantity of interest. It is the synthetic estimate, unmeasured on real
imagery, of the rate at which the system would mark a resident carrying a broom, a length of pipe or
a rolled mat as armed, and it is the concrete form of the dual-use harm this article discusses.
Because each person takes only the class of the prediction matched to it, an armed box on a person
matched to a box of another class does not enter this rate, although an operator would see it as an
alert, so the rate is a lower bound on how often such a person receives an armed detection at this
threshold; the precision row counts those boxes, together with alarms on background, without
separating them. The rate is not an artefact of how the generator carries objects, although that was
a live possibility, since every object longer than 1.15 m is re-angled in every pose (Section 7.4).
In the unseen-weapon test of Section 11.4 the closed umbrella, which at 0.88 m falls below that
length and so is carried in the weapons' poses, is the object most often called armed (0.38, on 29
instances), against 0.10 for brooms (41) and 0.11 for lengths of pipe (28). The frames of that test
were rendered again with every confusable object carried exactly as a weapon is, in the weapons'
distribution of poses and at their angles, with every random draw unchanged, so that the two
versions match box for box in 49 of 50 frames. Paired object by object over 227 objects, the
S-nadir-75 model calls 0.154 of them armed as normally carried and 0.137 when carried as a weapon
(exact McNemar test, p = 0.56), and the umbrella, whose carriage did not change, stays at 0.38. By
the criterion fixed before the test the rate does not rise, and the caveat that objects carried as
weapons would be called armed more often is withdrawn.

Nor does the rate fall when the ground sampling distance is halved again, although the two corpora
differ in more than altitude. The 35 m corpus also changed how confusable objects are carried: at 75
m the object was drawn in the firing pose with probability 0.42, as the weapon is, while at 35 m it
is drawn that way with probability 0.08 and otherwise over the shoulder, at the side or in one hand,
the more realistic distribution, which confounds resolution with pose and with every other setting
that changed between the two corpora (render sampling, the share of figures placed on rooftops,
figures per frame, the radius of wires and clotheslines, the placement of candidate positions and
the settlement seed). A third corpus separates them: identical to the 35 m corpus in every setting
except altitude and its jitter, rendered at 75 m. A replication was also fixed before it was run,
with its criterion: on 80 new frames continuing the seed of the 35 m corpus, and their twins at 75
m, none used in training, the difference would count as established if the 35 m rate exceeded the
twin's at a two-sided p below 0.05, would be withdrawn if the direction reversed, and would remain
suggestive otherwise. Table @tab{gemeo} gives the two models on both sets, across three training
runs and at three overlap thresholds.

<!--TAB:gemeo|The 35 m model against its twin rendered at 75 m with every other setting held: rates at which each class is called armed on the validation splits (35 and 24 images) and on the 80 new frames of each corpus; ranges over three training runs; and the object rate on the validation split at stricter overlap thresholds. Intervals for d′ are 95 per cent by resampling frames; p from two-proportion tests without correction for clustering by frame.-->

| Quantity | S-nadir-35 (35 m) | Twin at 75 m | Difference |
|---|---|---|---|
| Confusable object called armed, validation split | 0.273 | 0.165 | 10.8 points, p = 0.06 |
| Confusable object called armed, 80 new frames | 0.253 (74 of 292) | 0.125 (36 of 288) | 12.8 points, p = 0.0001 |
| Armed person called armed, validation split | 0.569 | 0.471 | p = 0.15 |
| Armed person called armed, 80 new frames | 0.543 | 0.432 | |
| Unarmed person called armed, validation split | 0.168 | 0.109 | p = 0.22 |
| d′ against confusable objects, validation split | 0.77 | 0.89 | |
| d′ against confusable objects, 80 new frames | 0.77 (0.57 to 0.99) | 0.97 (0.77 to 1.20) | |
| Object rate over three training runs, validation split | 0.231 to 0.273 | 0.132 to 0.242 | ranges overlap |
| Object rate over three training runs, 80 new frames | 0.202 to 0.253 | 0.097 to 0.181 | ranges separate |
| Object rate, validation split, at IoU 0.60 and 0.75 | 0.223 and 0.132 | 0.165 and 0.132 | level at 0.75 |

*The two models reach the same mAP50 on their validation splits (0.514 and 0.508) and a precision of
0.415 against 0.440 on the armed class (Table @tab{armado}).*

With every other setting held, halving the ground sampling distance did not reduce the confusion: in
the first training run the 35 m model calls every class armed more often in point estimate, at the
same mAP50 and with a d′ no larger than the twin's, so the 35 m result does not appear to be an
artefact of the change of pose. On the new frames the difference in the object rate is established
by the criterion fixed in advance, and its direction holds across the three training runs there but
not on the smaller validation splits, where the ranges overlap; the rates for armed and unarmed
persons, and with them the observation that the 35 m model calls every class armed more often, do
not hold across the runs on either set. The rate also depends on the overlap required to score a
detection: at an intersection-over-union of 0.75 the 35 m model and its twin coincide on the
validation split, and against the original 75 m model, which calls 0.230 and 0.141 of objects armed
at 0.60 and 0.75, the 35 m model changes order, so by the criterion of Section 10.6 that second
comparison is an artefact of annotation and the argument rests on the matched twin. At 75 m, moving
from the original corpus to the settings of the 35 m corpus, realistic carrying poses among them, is
followed by an object rate of 0.165 against 0.237, a difference the two-proportion test does not
support (p = 0.19). Section 11.4 states the condition under which the 75 m figure would be withdrawn
and reads the altitudes together.
