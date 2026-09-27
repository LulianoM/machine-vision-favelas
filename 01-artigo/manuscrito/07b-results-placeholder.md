## 9. Results: Transfer to Real Imagery

> **Provenance note.** Every quantity below traces to a file under `06-resultados/` together with
> the command that produced it. Each model of the protocol in Section 7.7 was
> specified before that model was run, but the protocol grew in stages: S-nadir-150-six,
> S-oblique-six, S-nadir-35 and its twin, and the fine-tuning models of Section 9.4 were added after
> earlier results in this section were known. Section 10 declares in advance what would overturn the transfer results of Sections 9.1 to
> 9.3, as Section 11.5 does for the 75 m result of Section 9.5. Every model below was trained once,
> with a single seed, so no difference between models carries a measured run-to-run dispersion;
> Section 10.6 specifies the repetition that would supply one.

A pilot of the full protocol was run before the corpus reached its final size. Its results are
reported first, because they bound what follows and because withholding an unfavourable pilot
would make the rest of this section unreadable as evidence.

| Pilot run | Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| S-nadir-150, 40 training scenes at 1080p | synthetic validation | 0.109 | 0.148 | 0.077 | 0.019 |
| same model | VisDrone-DET val, zero-shot | 0.038 | 0.031 | 0.0055 | 0.0020 |
| same model | VisDrone-DET val, scale-matched | 0.041 | 0.037 | 0.0061 | 0.0009 |

*Source: `06-resultados/sim2real_morro_v1.json`.*

These are not results about transfer. The model failed on its own domain, reaching 0.077 where the
corpus of record, with 180 images at 4K, reaches 0.79 (Section 9.2), and transfer cannot be
measured from a model that did not learn. Sections 10.1 and 8.1 name two
candidate causes, properties of the pilot corpus rather than of the method if they hold, and
neither has been isolated (the test of the first, specified in Section 10.1, has not been run): it
contained 40 training scenes, and it was rendered at
1080p, which doubles the ground sampling distance and places two thirds of all instances below one
stride of the network (Section 8.1).

The pilot does establish one thing a favourable result could not. This pipeline is capable of
failing, and a candidate cause of the failure is legible in the corpus statistics before any training. It was also trained with a different
recipe (tiles and input of 640 pixels, 120 epochs). The rows below report the protocol re-run with
both defects corrected and with the recipe of Section 7.6.

### 9.1 Ceiling: what real training data achieves on this test set

Model R, trained on 1,106 images drawn at random from VisDrone-DET train (18,858 person
instances), the same number of training images as the tiled synthetic corpus of record, and
evaluated on VisDrone-DET validation. Holding the number of training images equal lets the ratio in
Section 9.2 speak to the data at a matched number of images, though not of instances: the images
of R hold 18,858 persons against 3,225 in the whole synthetic corpus of record. A run on the full training split
(6,471 images) was started and stopped before completion: at this hardware's pace it would have
taken two days to improve a denominator whose role is to be matched, not maximised.

| Model | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| R (1,106 real training images) | 0.7312 | 0.5729 | 0.6311 | 0.2538 |

*Source: `06-resultados/sim2real_r_pareado.json`.*

This figure is the denominator for everything that follows. It is not a claim about our method; it
establishes what the test set permits at this volume of data.

### 9.2 Transfer from synthetic training, nadir geometry

Model S-nadir-150, trained only on procedurally generated imagery with the camera geometry of Section 7.3,
evaluated on the same real test set with no real training image of any kind.

| Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Synthetic validation (ceiling of the corpus) | 0.8707 | 0.7413 | 0.7915 | 0.3656 |
| VisDrone-DET val (zero-shot) | 0.0856 | 0.0421 | 0.0102 | 0.0025 |

*Source: `06-resultados/sim2real_s_nadir_4k.json`.*

**Efficacy of the synthetic method** = mAP50(S-nadir-150) / mAP50(R) = 0.0102 / 0.6311 = 1.6 per cent.

**Variety of settlement at fixed volume.** The corpus of record renders one settlement. Model
S-nadir-150-six keeps every generator setting and the number of images fixed and spreads the 180
images over six settlements, 30 each, differing in relief, forest cover, a corridor through the
core (an avenue, a narrow street or a river) and the palette of roofs and facades
(`07-blender/scripts/sitios.py`, settlements -1 to 4).

| Model | Synthetic validation mAP50 | VisDrone-DET val mAP50 | mAP50-95 | Efficacy |
|---|---|---|---|---|
| S-nadir-150, one settlement | 0.7915 | 0.0102 | 0.0025 | 1.6% |
| S-nadir-150-six, six settlements | 0.6786 | 0.0190 | 0.0071 | 3.0% |

*Source: `06-resultados/sim2real_s_variedade.json`.*

Variety nearly doubles the transfer figure and lowers the score on the model's own validation
split, which is consistent with a model that has stopped memorising one scene, although the two
validation splits are different sets. From one training run per model it is a candidate term in
the gap, and in Section 9.3 it moves the transfer figure less than capture geometry does.

Kiefer, Ott and Zell (2022) report mAP@50 on VisDrone for three architectures trained purely on
synthetic data: 1.2 for EfficientDet-D0, 2.4 for Faster R-CNN and 10.2 for YOLO, against 24.6,
48.6 and 43.9 respectively for the same architectures trained on real data. The YOLO row is the
comparable one, since this article trains YOLO, and it gives a ratio of 23.2 per cent.

The two ratios are not directly comparable, and the reason matters more than the gap. Their
denominator is a detector trained on the full VisDrone training split and scored over ten object
classes; ours is trained on 1,106 images of that split, evaluated on its validation split and
scored on a single person class. Their synthetic corpus is also larger, 40,000 images rendered in
a game engine against 180 scenes here. These differences do not all act in the same direction,
so this design cannot say which of the two ratios is the harsher. What this article reports is the ratio to its own declared
ceiling, together with the comparison in Section 9.3.

### 9.3 Transfer from synthetic training, oblique geometry

Model S-oblique. Identical generator, identical settlement, identical illumination regimes; only
the camera is moved, together with the figure-placement filter that depends on it (Section 10.4).

Pitch is set from the height-to-width ratio of the VisDrone **training** split, not the validation
split on which every model in this article is scored. The distinction is load-bearing: the ratio
of 2.20 quoted in Section 8.2 is measured on the validation split, and calibrating a training
corpus on a statistic of the test set and then reporting the gain on that same test set would be
circular. The value used for calibration is 1.95, measured on the training split alone (Section 8.2).

This arm is therefore an adaptation of the corpus to the benchmark, and is reported as such rather
than as a discovery about acquisition geometry in general. What it tests is whether camera
geometry, which moves the mismatch identified in Section 8.2 together with the perspective of the
rest of the scene, is load-bearing on this benchmark.

| Model | mAP50 on VisDrone-DET val | Efficacy vs. ceiling |
|---|---|---|
| S-nadir-150 | 0.0102 | 1.6% |
| S-oblique | 0.0614 | 9.7% |
| S-oblique-six | 0.1055 | 16.7% |

*Source: `06-resultados/sim2real_s_obliquo.json` and `sim2real_s_oblvar.json`.*

**Difference attributable to acquisition geometry, on this benchmark** =
mAP50(S-oblique) - mAP50(S-nadir-150) = 0.0512, a factor of 6.0.

Two outcomes are possible and both are reportable. If the oblique arm substantially outperforms
the nadir arm, acquisition geometry is load-bearing relative to scene content on this benchmark.
That is consistent with the direction of Liao et al. (2026) without extending their claim, since
a single benchmark that is not the target domain cannot support a general statement about camera
position. If the two arms are comparable, the limitation lies in synthesis rather than viewpoint,
and the conclusion narrows accordingly.

The first outcome obtained. With the settlement, the generator and the training recipe held fixed,
the oblique model transfers 6 times better than the nadir model, against a factor of 1.9 for six
settlements instead of one. By the criteria fixed before the run (the two outcomes above and
Section 10.4), acquisition geometry is load-bearing on this benchmark. The comparison with variety
of settlement is not part of those criteria, since the variety arm was added after the nadir
result; on it, the change of camera moves the transfer figure more than six settlements do. The oblique
figure falls within the synthetic-only range reported by Kiefer, Ott and Zell (2022), although
their figures average ten VisDrone classes and ours scores a single person class.

The oblique corpus did not reach the shape it was calibrated for, 1.46 against 1.95, for the two
reasons measured in Section 8.2. Model S-oblique-six combines the two terms and corrects the
calibration: six settlements of 30 images; pitch between 45 and 56 degrees, chosen to centre
the median of figures carrying nothing on the benchmark's shape, which in the single-settlement
oblique corpus they reach only between 50 and 52 degrees; only such figures; and a camera placement
redrawn until the centre of the frame is not occluded by forest or hillside. It is not an ablation, since several
things change at once; it is the best configuration of this generator tried here and the model the rest
of this article calls the synthetic model. Result: mAP50 0.1055 on VisDrone-DET val (precision
0.2631, recall 0.1716, mAP50-95 0.0329), an efficacy of 16.7 per cent: 10.3 times the nadir model
and 1.7 times the single-settlement oblique model, against 0.7047 on its own synthetic validation.
The rendered figure approaches the calibration target without reaching it: a median
height-to-width ratio of 1.85 at 13.3 by 25.2 pixels, against 1.95 at 13.0 by 24.0 in the benchmark's training split (Section 8.2). In
absolute terms, 10.5 points of mAP50 sit just above the upper end of the synthetic-only range
reported by Kiefer, Ott and Zell (2022), although their figures average ten VisDrone classes and
ours scores a single person class, while the ratio to our own ceiling stays below theirs (Section
9.2).

The acquisition geometry this article reproduces points straight down. An oblique corpus that transfers better to
VisDrone is informative about the benchmark, not about the acquisition that would be flown over
Jacarezinho.

<!--FIG:06-resultados/figuras/fig4_dataset.jpg|One annotated frame from each of the six illumination regimes, with the generated boxes drawn. Green marks the armed class and blue the unarmed class. No accuracy figure for that distinction is reported at this altitude, for the reason given in Section 11.5; the 75 m result is reported in Section 9.5. The figure is included to show that annotation and occlusion handling behave identically across regimes, so that any per-regime performance difference found by the test specified in Section 10.3, not yet run, cannot be attributed to the labelling.-->

### 9.4 Limited real fine-tuning, on the public benchmark only

The proposal of Section 6 reserves a stage in which the synthetic pretraining is fine-tuned on a
modest volume of real imagery. It is run here on the public benchmark only, as a line separate from
the synthetic-only results above so that the two contributions stay distinguishable, and no imagery
of the case study territory is involved.

The protocol was fixed before the run. Two slices of the VisDrone-DET training split, 5 per cent
(324 images) and 10 per cent (647 images, containing the first), each train two models: one
initialised from the synthetic model of Section 9.3 and one from the same generic initialisation as
every other model in this article. The checkpoint is selected on a further 5 per cent of the
training split, disjoint from both, so that the validation split on which every figure here is
scored is not used for selection, which removes for this comparison the asymmetry declared in
Section 10.5. Thirty epochs, the same detector, input size and augmentation
(`07-blender/scripts/prepara_ft.py`).

| Real training data | F-synthetic (from S-oblique-six) | F-generic (from COCO) | Difference |
|---|---|---|---|
| 5 per cent (324 images) | 0.4424 | 0.5220 | -0.0796 |
| 10 per cent (647 images) | 0.5095 | 0.5709 | -0.0614 |

*mAP50 on VisDrone-DET val under the protocol of Section 9.1. Source: `06-resultados/ft_visdrone.json`;
precision, recall and mAP50-95 of each model in `sim2real_ft05_sint.json`, `sim2real_ft05_coco.json`,
`sim2real_ft10_sint.json` and `sim2real_ft10_coco.json`.*

The quantity of interest is the difference at each volume: what the synthetic pretraining is worth
when real data is scarce. The expectation, stated before the run, is that it is largest at the
smaller volume.

It is negative at both. Initialised from the synthetic model, the detector finishes 8.0 points of
mAP50 below the generic initialisation with 5 per cent of the real data and 6.1 points below with
10 per cent, and the synthetic start given 647 real images (0.5095) does not reach the generic start
given 324 (0.5220). The expectation stated before the run therefore fails: the difference
is not largest at the smaller volume but most negative there. Its magnitude narrows as real data
grows, but what narrows is a cost, not a benefit. On the selection slice the generic start overtakes the synthetic one by the fourth epoch at 5 per
cent and in the first epoch at 10 per cent, after which the synthetic start leads only
intermittently (`06-resultados/ft_curvas_selecao.json`). Fine-tuning does
transform the synthetic model itself, from 0.1055 to 0.4424 with 324 real images, which is the
effect the sim-to-real literature reports; what it does not do here is outperform a generic start
given the same real images. Relative to the ceiling of Section 9.1, trained on 1,106 real images for
twice as many epochs, the generic start recovers 82.7 and 90.5 per cent and the synthetic start 70.1
and 80.7 per cent. On this benchmark, at these volumes and in one training run per model, the
synthetic corpus does not substitute for real data; it costs some. One candidate explanation, not tested here, is that training on 890
tiles of generated figures overwrites part of what the generic initialisation encodes about real
people.

### 9.5 The armed and unarmed distinction, by altitude

No accuracy for the armed and unarmed distinction is reported at 150 m. At that altitude the
median instance measures 17.6 by 17.5 pixels and a firearm is not resolvable within it. The
distinction is nevertheless learnable in a corpus where the weapon is always the same asset in
the same pose at the same contrast, so that separability cannot be told apart from a property of
the generator, and reporting it would be the inferential leap this article criticises.

At 75 m the median instance measures 47.6 by 41.7 pixels, 6.4 times the area over all classes
(5.2 times for armed figures alone, Section 7.3), and the corpus is
built so that the artefact cannot account for the result: five firearm models against nine
elongated objects carried in the same territory, sharing the weapons' colour and roughness
palette and the same distribution of carrying poses. The corpus holds 2,887 instances in 200 images,
933 of them armed, 973 unarmed and 981 carrying a confusable object. A second corpus
at 35 m, 1.1 cm per pixel, holds 2,223 instances with a median of 121.8 by 103.1 pixels.

| Quantity | S-nadir-75 (75 m) | S-nadir-35 (35 m) | Twin of S-nadir-35 at 75 m |
|---|---|---|---|
| mAP50, three classes | 0.579 | 0.514 | 0.508 |
| Recall, armed | 0.547 | 0.569 | 0.471 |
| Precision, armed | 0.386 | 0.415 | 0.440 |
| Rate at which a confusable object is called armed | 0.237 | 0.273 | 0.165 |
| Rate at which an unarmed person with no object is called armed | 0.131 | 0.168 | 0.109 |

*Protocol: inference on the full 4K frame at native scale; confidence 0.25 and one-to-one matching
at an intersection-over-union of 0.50 for the rates; the validation split of each corpus
(27, 35 and 24 images). Source: `06-resultados/confusao_armado_75.json`,
`confusao_armado_35.json` and `confusao_armado_75g.json`, produced by `06-resultados/confusao_armado.py`;
precision from `compara_gemeo.py`. The third column is the matched corpus described below.*

The fourth row is the quantity of interest. It is the synthetic estimate, unmeasured on real
imagery, of the rate at which the system would mark a resident carrying a broom, a length of pipe or a rolled mat as armed, and it is the concrete form
of the dual-use harm this article discusses. It does not fall when the ground sampling distance is
halved again: at 35 m, where a rifle spans some 80 pixels, about one confusable object in four is
still called armed, and so is about one unarmed person in six.

The two corpora differ in more than altitude. The 35 m corpus also changed how confusable objects
are carried: at 75 m the object was held in the firing pose in 42 per cent of cases, as often as
the weapon, while at 35 m it is held that way in 8 per cent and otherwise over the shoulder, at the
side or in one hand. That removes a cue the 75 m model may have used, and it is the more realistic
distribution, but it confounds resolution with pose (and with render sampling, 64 against 96
samples per pixel). A third corpus separates them: identical to the 35 m corpus in every setting
except altitude, rendered at 75 m. Confusable objects called armed: 0.165; unarmed persons called
armed: 0.109 (third column above). Against 0.273 and 0.168 at 35 m with every other setting held,
halving the ground sampling distance did not reduce the confusion: the 35 m model calls every class
armed more often in point estimate, armed persons included (p = 0.15 and 0.22 for the armed and
unarmed rates in the same test), at the same mAP50, so the 35 m result does not appear to be an
artefact of the change of pose. The difference in the object rate is suggestive rather than established:
10.8 points, p = 0.06 in a two-proportion test that does not correct for clustering by frame
(`06-resultados/gemeo_75_35.json`, produced by `compara_gemeo.py`). At 75 m, moving from the original
75 m corpus to the generator settings of the 35 m corpus, realistic carrying poses among them,
is followed by an object rate of 0.165 against 0.237, a difference the same test does not
support (p = 0.19). Section 11.5 states the condition under which the 75 m figure would be withdrawn and reads
the altitudes together; Section 10.7 explains why Section 10 carries no test for this distinction.
