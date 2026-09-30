## 10. Robustness and Alternative Explanations

Each threat below is named, given a check, and given an explicit condition that would overturn the
result it protects; where the check has not been run, the text says so. Stating that condition in
advance is what distinguishes a check from a defence written after seeing the number. Each
overturning condition below was fixed before the corresponding measurement was run; the three made
more precise afterwards, in Sections 10.1, 10.2 and 10.3, were changed before their tests and say
so.

### 10.1 The corpus is small, and small corpora flatter themselves

**Threat.** The synthetic corpus is generated, so its size is a choice rather than a constraint, and
a detector trained on few scenes can memorise them. An earlier pilot of this pipeline used 40
training images and reached mAP50 of 0.077 on its own validation split, against 0.79 for the corpus
of record, trained on 149 of its 180 images at 4K (Section 9.2). The pilot is reported here because
it is instructive, not because it is a result: it establishes that this pipeline is capable of
failing, and points to scene count as one candidate cause, which the check below would test and
which has not been isolated.

**Check.** Learning curve over the number of distinct generated scenes, holding the illumination
regimes balanced and the tiling protocol fixed. A related comparison has been run at a fixed 180
images, one settlement against six (Section 9.2): 0.0102 against 0.0190 on the real test set. It
varies the variety of settlement at a fixed number of scenes, so it is not a point on this curve,
which was specified and has not been run.

**What would overturn the claim.** If performance on the real test set does not rise from the
smallest corpus to the largest by more than the between-seed dispersion of Section 10.6, scene count
is not the operative variable and the conclusion of Section 9 must be restated as a property of the
generator rather than of corpus size. This wording adds a direction and a margin to an earlier one
that asked only whether the two were separated, and is fixed here, before the curve has been run.

### 10.2 Apparent size, not synthesis, may explain the transfer gap

**Threat.** Section 8.1 reports that the synthetic target at 4K and the real benchmark target cover
near-identical median area, 301 and 300 square pixels, the second with the benchmark's training and
validation splits pooled. That match is a property of the rendering resolution we selected, and it
does not extend to the long side, which is 20.6 against 24.0 pixels over the same pooled splits.
Where it is not exact, as on the long side, a transfer failure attributable to scale could be
mistaken for a failure attributable to synthesis.

**Check.** The real test set is additionally evaluated at an input size chosen so that the median
long side of its person boxes, as they reach the network, matches that of the training corpus. The
scale has to be set through the input size, because the validator resizes every image so that its
long side equals the input size, enlarging as well as reducing, so rescaling the image files and
evaluating them at the same input size changes nothing the network sees. The input size is chosen
from the labels and image sizes alone, before any evaluation.

An earlier version of this check was run on the pilot reported in Section 9 and gave 0.0055 against
0.0061. It rescaled the benchmark's image files by 1/2.49 and evaluated both versions at the same
input size, 640 pixels, so, for the reason just given, both presented the network with the same
scale, and the difference between them is one of resampling, not of scale. Earlier drafts reported
it as a matched-scale result; that reading is withdrawn. On the corpus of record the check was run
as specified above. At the protocol's input size of 1,280 pixels the median long side of the
benchmark's person boxes reaches the network at 25.33 pixels; at 1,024 it reaches it at 20.27, the
closest a multiple of 32 comes to the 20.55 of the corpus of record, while the median area falls
from 283 to 181 square pixels, since no uniform rescaling matches shape. At 1,024 pixels S-nadir-150
reaches 0.0128 against 0.0102 at the protocol's size, and R 0.5849 against 0.6311, which would put
the efficacy of Section 9.2 at 2.2 rather than 1.6 per cent. What still differs at a matched long
side is shape, which Section 10.4 tests.

**What would overturn the claim.** If the two figures diverge substantially on the corpus of record,
scale is a live confound after all and the efficacy ratio in Section 9.2 must be reported at matched
scale only. "Substantially" was fixed before the matched run as a difference of more than half of
the protocol figure. The difference is a quarter of it, 0.0026 on 0.0102, so the condition is not
met and the ratio of Section 9.2 stands at the protocol's scale.

This subsection also records a correction. An earlier version of this analysis reported a 2.49-fold
scale gap between corpus and benchmark and treated it as an inherent altitude domain shift. It was
an artefact of rendering the corpus at 1920 by 1080 rather than at 4K. The claim is withdrawn, and
the check above exists so that the same error is detectable rather than assumed absent.

### 10.3 Illumination: the prediction that runs against intuition

**Threat.** Section 8.3 measures that overcast yields both the largest raw figure-to-background
difference and the largest ratio of contrast to local clutter, while hard sun sits second on raw
contrast and among the two lowest on the ratio. That raises the hypothesis that the detector
performs better under overcast than under hard sun. A contrast statistic is not a detection
statistic, the sample is eight images per regime, and between-image dispersion is of the same order
as several of the gaps.

**Check.** Per-regime performance on a held-out synthetic split, six regimes, balanced. It was run
on 120 new frames continuing the seed of the corpus of record, 20 per regime, none used in training,
and scored with S-nadir-150 as mAP50 on the tiles of each regime, the protocol of the synthetic
ceiling of Section 9.2, and, as a secondary measure fixed with it, as recall at confidence 0.25 on
whole frames with 95 per cent intervals by resampling frames. The mAP50 is 0.675 under hard sun,
0.755 under heavy overcast, 0.759 under rain, 0.780 under haze, 0.790 under low sun and 0.791 under
overcast; recall under hard sun is 0.657 (0.591 to 0.720), below every other regime, and under
overcast 0.796 (0.760 to 0.827), against 0.789 (0.748 to 0.827) under rain. An ablation against a
corpus generated under hard sun only, evaluated on the full six-regime split and on the real test
set, was specified and has not been run.

<!--FIG:06-resultados/figuras/fig4_dataset.jpg|One annotated frame of the pilot corpus (nadir, 150 m, 1920 by 1080) from each of the six illumination regimes, with the generated boxes drawn. Green marks the armed class and blue the unarmed class. No accuracy figure for that distinction is reported at this altitude, for the reason given in Section 11.5; the 75 m and 35 m results are reported in Section 9.5. Boxes are computed from the scene geometry, not from the rendered pixels (Section 7.4), so the labelling does not depend on the regime, and the per-regime differences found by the test of this section, run on new frames of the corpus of record, cannot come from it.-->

**What would overturn the claim.** If per-regime performance is not higher under overcast than under
both hard sun and rain, the only gap that Section 8.3 approaches resolving, or if hard sun is not
among the two weakest regimes, the mechanism proposed in Section 8.3 is wrong and the operational
implication in Section 11 is withdrawn. The image statistics would still stand, but they would be
describing something other than detector difficulty. The ablation in the check above carries no
overturning condition and would be reported descriptively. An earlier wording of this condition
referred to raw contrast, from a superseded measurement in which hard sun had the largest raw
difference, and a later one required performance to follow the ordering of contrast against local
clutter without saying over which regimes; both were corrected before the per-regime test was run.
Neither part of the condition is met: overcast scores above hard sun and above rain, and hard sun is
the weakest of the six regimes. What is robust is that hard sun is the weakest regime on mAP50,
eight points below the next, and that its recall interval lies wholly below those of overcast, rain
and low sun, though it overlaps those of haze and heavy overcast; the margin of overcast over rain
lies within the recall intervals. Low sun, which also casts sharp shadows, scores level with
overcast; the condition fixed in advance does not test this, and it limits the mechanism of Section
8.3 to a partial account.

### 10.4 Capture geometry against scene content

**Threat.** The central comparison of this article attributes a performance difference to camera
placement. It could instead reflect any of the incidental differences between the two synthetic
arms.

**Check.** The two models are trained on corpora generated with the same settings (though not with
the same version of the generator: the nadir corpus predates the five-model weapon library of
Section 7.4, so its armed figures carry one of three rifle patterns or a pistol and are held forward
with probability 0.46 rather than 0.42), the same settlement seed, the same material library, the
same illumination regimes, the same share of armed and unarmed figures and the same annotation
procedure, with the same training recipe and the same number of images, both at 4K. What differs is
the camera: pitch, drawn between 26 and 52 degrees and recorded per image, altitude (120 m for the
oblique camera, with a per-image jitter of up to 36 m either way) and its jitter. One further
setting differs because the camera does: the nadir corpus keeps figures within a square around the
camera axis whose side is 0.52 of the nadir frame width, the filter that produced it, while the
oblique corpus places them anywhere the projected frame covers, since an oblique frame is not a
square on the ground. At the centre of the frame and at the nominal 120 m, the oblique camera puts
the ground sampling distance between about 4.3 and 6.3 cm per pixel across the pitch range, a span
the altitude jitter widens, against 4.88 for the nadir corpus, so the change of camera moves the
shape of the target (h/w 1.46 against 0.98) and leaves its size in the same range, somewhat larger
in area (456 against 301 square pixels). Pitch is set from the VisDrone training split rather than
from the validation split on which both models are scored, so that the calibration does not consume
the test set. Result: 0.0614 for the oblique model against 0.0102 for the nadir model on the real
test set. The figure of 0.1055 for S-oblique-six (Section 9.3) is not a result of this check: that
corpus also changes the settlements, the pitch range, the figures, which carry nothing, and the
placement of the camera.

**What would overturn the claim.** If the oblique arm does not outperform the nadir arm, capture
geometry is not the dominant term, and Section 9.3 must conclude that the limitation lies in
synthesis rather than viewpoint. That outcome is reportable and is not treated here as a failure of
the study.

### 10.5 The ceiling may be low for reasons unrelated to us

**Threat.** A low transfer figure is uninterpretable without knowing what the test set permits.
Small-object aerial detection is difficult for real-data models too, and a reader has no way to
distinguish a weak synthetic method from a hard benchmark.

**Check.** Model R, trained on 1,106 images of the real training split of the same benchmark under
the same detector, the same input size, the same initialisation and the same schedule, reaches mAP50
0.6311 (Section 9.1). All synthetic figures are reported as a ratio to it.

One asymmetry is declared here rather than left for the reader to find. Model R selects its
checkpoint on the very split it is later scored on, the 548 validation images, while the synthetic
models select theirs on a synthetic validation split. This favours R, so the efficacy ratio reported
in Section 9.2 is conservative: it understates the synthetic method rather than flattering it.

**What would overturn the claim.** If R itself performs near chance under this protocol, the
protocol is inadequate to the benchmark and no conclusion about synthetic efficacy can be drawn from
it. In that case the appropriate report is the failure of the evaluation design, not a finding about
synthesis.

### 10.6 Two checks specified in advance

Two further threats had a check specified in advance; both have since been run, under criteria fixed before the runs.

**Annotation convention.** Synthetic boxes are amodal and projected from vertices; benchmark boxes
are human-drawn. A systematic difference in tightness would move overlap scores without any
difference in detection. The check is sensitivity of every reported figure to the
intersection-over-union threshold at 0.50, 0.60 and 0.75; if the ordering of the models changes with
the threshold, the comparison is an artefact of annotation and must be reported at several
thresholds. Under both the Ultralytics validator and the official rule of Section 7.7, no pair among
those fixed for this check changes order between 0.50, 0.60 and 0.75 on the benchmark. One further
comparison of Section 9.4 does: at 10 per cent, joint training scores above the synthetic start at
0.50 and 0.60 and below it at 0.75 (0.0983 against 0.1025). Among the three-class models of Section
9.5, scored on their own synthetic splits, the order also changes: the rate at which a confusable
object is called armed places the 35 m model above the original 75 m model at 0.50 and below it at
0.60 and 0.75, and the rate at which an unarmed person is called armed does the same at 0.75 (0.076
against 0.085); against its twin the 35 m model stays above at 0.50 and 0.60 and level at 0.75
(0.132 each). By the condition stated above, the comparison between the 35 m model and the original
75 m model is therefore an artefact of annotation, and those rates are reported at the three
thresholds (Section 9.5); the comparison with the matched twin, which does not reverse, is the one
that carries the argument.

**Seed dependence.** A single settlement seed, and a single training run per model, may be
favourable by chance. The check is repetition of the protocol across independent seeds with the
between-seed dispersion reported alongside the mean; if that dispersion is of the same order as the
differences reported in Section 9, those differences are not resolvable at this corpus size. Varying
the settlement seed would be a matter of compute rather than of design, since every image records
its seed and the generator reproduces the settlement exactly from it (Section 11.6 names the three
corpora whose figures it did not reproduce). What was run is narrower: five models, S-oblique-six,
the two fine-tuning models at 5 per cent, S-nadir-35 and its twin at 75 m, retrained with training
seeds 1 and 2 on a fixed corpus, and a difference was fixed in advance as resolvable when the ranges
of the two models over their three runs do not overlap. S-oblique-six reaches 0.1055, 0.0958 and
0.0887 on the benchmark, an efficacy of 15.3 per cent on average, between 14.1 and 16.7 (Section
9.3). The advantage of the generic start in fine-tuning at 5 per cent is resolvable, with means of
0.5244 against 0.4529 (Section 9.4). The difference between the 35 m model and its twin at 75 m in
the rate at which a confusable object is called armed is resolvable on the 80 new frames of Section
9.5, where the means are 0.222 against 0.134, but not on the smaller validation splits; their rates
for armed and unarmed persons are resolvable on neither. The central comparison of Section 10.4,
between S-nadir-150 and S-oblique, was not repeated, and its factor of 6.0 rests on one run per
model. The settlement seed was not varied: each repetition retrains on the same corpus, so the
dispersion measured is that of training, not of the realisation of the scene.

### 10.7 What this design cannot rule out

Two boundaries of this design are stated in Section 11 rather than argued here: the benchmark is not
a favela (Section 11.2), and the armed and unarmed distinction is reported at 75 m and 35 m but not
at 150 m, where the one three-class model trained for it did not pass the validity condition fixed
before it was run, and the two-class pilot did not learn its own domain (Section 11.5). The first is
structural; the second is a measurement that did not succeed, which leaves the absence argued rather
than shown.
