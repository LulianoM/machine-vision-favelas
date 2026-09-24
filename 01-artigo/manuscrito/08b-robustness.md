## 10. Robustness and Alternative Explanations

> **Provenance note.** Each overturning condition below was fixed before the corresponding
> measurement was run. Quantities appear as `[X]` until measured, and each check is reported
> whether or not its outcome is favourable.

Each threat below is named, tested, and given an explicit condition that would overturn the result
it protects. Stating that condition in advance is what distinguishes a check from a defence
written after seeing the number.

### 10.1 The corpus is small, and small corpora flatter themselves

**Threat.** The synthetic corpus is generated, so its size is a choice rather than a constraint,
and a detector trained on few scenes can memorise them. An earlier pilot of this pipeline used 40
training images and reached mAP50 of 0.077 on its own validation split, against 0.676 obtained by
a previous arm of this project with 473 images. The pilot is reported here because it is
instructive, not because it is a result: it establishes that this pipeline is capable of failing,
and identifies scene count as one of two causes.

**Check.** Learning curve over the number of distinct generated scenes, holding the illumination
regimes balanced and the tiling protocol fixed. A two-point version has been run at a fixed 180
images, one settlement against six (Section 9.2): 0.0102 against 0.0190 on the real test set. The full
curve: `[X]`.

**What would overturn the claim.** If performance on the real test set does not separate the
largest corpus from the smallest, scene count is not the operative variable and the conclusion of
Section 9 must be restated as a property of the generator rather than of corpus size.

### 10.2 Apparent size, not synthesis, may explain the transfer gap

**Threat.** Section 8.1 reports that the synthetic target at 4K and the real benchmark target
cover near-identical median area, 301 and 300 square pixels. That match is a property of the
rendering resolution we selected, and it does not extend to the long side, which is 20.6 against
25.0 pixels. If it were not exact, a transfer failure attributable to scale could be
mistaken for a failure attributable to synthesis.

**Check.** The real test set is additionally evaluated after rescaling so that its target size
distribution matches the training corpus by construction. The label format is normalised, so
rescaling the image leaves the annotation unchanged and the control is clean.

This check has already been run once, on the pilot reported in Section 9, and its outcome is given
here rather than withheld: mAP50 of 0.0055 at native scale against 0.0061 at matched scale, a
difference of 0.0006 (`06-resultados/sim2real_morro_v1.json`). On that pilot, matching the scale
did not recover performance. That is evidence against scale as the operative confound, and
therefore against the explanation most favourable to us. On the corrected corpus the check
reduces to its native-scale half: the synthetic and benchmark targets already match in median area
(301 against 300 square pixels, Section 8.1), so rescaling the benchmark to the corpus leaves it
where it is, and the native-scale figure of Section 9.2, 0.0102, is also the matched-scale figure. What
still differs at matched area is shape, which Section 10.4 tests.

**What would overturn the claim.** If the two figures diverge substantially on the corrected
corpus, scale is a live confound after all and the efficacy ratio in Section 9.2 must be reported
at matched scale only.

This subsection also records a correction. An earlier version of this analysis reported a
2.49-fold scale gap between corpus and benchmark and treated it as an inherent altitude domain
shift. It was an artefact of rendering the corpus at 1920 by 1080 rather than at 4K. The claim is
withdrawn, and the check above exists so that the same error is detectable rather than assumed
absent.

### 10.3 Illumination: the prediction that runs against intuition

**Threat.** Section 8.3 measures that overcast yields both the largest raw figure-to-background
difference and the largest ratio of contrast to local clutter, while hard sun sits second on raw
contrast and among the two lowest on the ratio. That raises the hypothesis that the detector
performs better under overcast than under hard sun. A contrast
statistic is not a detection statistic, the sample is eight images per regime, and between-image
dispersion is of the same order as several of the gaps.

**Check.** Per-regime performance on a held-out synthetic split, six regimes, balanced: `[X]`.
Ablation against a corpus generated under hard sun only, evaluated on the full six-regime split
and on the real test set: `[X]`.

**What would overturn the claim.** If per-regime performance does not order inversely with raw
contrast, or if hard sun is not among the weakest regimes, the mechanism proposed in Section 8.3
is wrong and the operational implication in Section 11 is withdrawn. The image statistics would
still stand, but they would be describing something other than detector difficulty.

### 10.4 Capture geometry against scene content

**Threat.** The central comparison of this article attributes a performance difference to camera
placement. It could instead reflect any of the incidental differences between the two synthetic
arms.

**Check.** The two models are trained on corpora generated from the same code, the same
settlement seed, the same material library, the same illumination regimes, the same share of armed
and unarmed figures and the same annotation procedure, with the same training recipe and the same
number of images, both at 4K. What differs is the camera: pitch, drawn between 26 and 52 degrees
and recorded per image, altitude (120 m for the oblique camera) and its jitter. At the centre of the
frame that puts the ground sampling distance between about 4.3 and 6.3 cm per pixel across the pitch
range, against 4.88 for the nadir corpus, so the change moves the shape of the target (h/w 1.46
against 0.98) and leaves its size in the same range, somewhat larger in area (456 against 301
square pixels). Pitch is set from the VisDrone training split rather than from the validation
split on which both models are scored, so that the calibration does not consume the test set.
Result: 0.0614 for the oblique model against 0.0102 for the nadir model on the real test set (Section 9.3).

**What would overturn the claim.** If the oblique arm does not outperform the nadir arm, capture
geometry is not the dominant term, and Section 9.3 must conclude that the limitation lies in
synthesis rather than viewpoint. That outcome is reportable and is not treated here as a failure
of the study.

### 10.5 The ceiling may be low for reasons unrelated to us

**Threat.** A low transfer figure is uninterpretable without knowing what the test set permits.
Small-object aerial detection is difficult for real-data models too, and a reader has no way to
distinguish a weak synthetic method from a hard benchmark.

**Check.** Model R, trained on 1,106 images of the real training split of the same benchmark under
the same detector, the same input size, the same initialisation and the same schedule, reaches
mAP50 0.6311 (Section 9.1). All synthetic figures are reported as a ratio to it.

One asymmetry is declared here rather than left for the reader to find. Model R selects its
checkpoint on the same distribution it is later scored on, while the synthetic models select
theirs on a synthetic validation split. This favours R, so the efficacy ratio reported in
Section 9.2 is conservative: it understates the synthetic method rather than flattering it.

**What would overturn the claim.** If R itself performs near chance under this protocol, the
protocol is inadequate to the benchmark and no conclusion about synthetic efficacy can be drawn
from it. In that case the appropriate report is the failure of the evaluation design, not a
finding about synthesis.

### 10.6 Two checks specified and not run

Two further threats have a check specified in advance and no result in this version, and they are stated so that their absence is visible rather than silent.

**Annotation convention.** Synthetic boxes are amodal and projected from vertices; benchmark boxes are human-drawn. A systematic difference in tightness would move overlap scores without any difference in detection. The check is sensitivity of every reported figure to the intersection-over-union threshold at 0.50, 0.60 and 0.75; if the ordering of the models changes with the threshold, the comparison is an artefact of annotation and must be reported at several thresholds.

**Seed dependence.** A single settlement seed may be favourable by chance. The check is repetition of the protocol across independent seeds with the between-seed dispersion reported alongside the mean; if that dispersion is of the same order as the differences reported in Section 9, those differences are not resolvable at this corpus size. Every image carries its seed in a manifest entry and the generator reproduces the settlement exactly from it (Section 11.6 states what it did not reproduce in the corpora of record), so the check is a matter of compute rather than of design.

### 10.7 What this design cannot rule out

Two boundaries of this design are structural rather than testable, and are stated in Section 11
rather than argued here: the benchmark is not a favela (Section 11.2), and the armed and unarmed
distinction is reported at 75 m and deliberately withheld at 150 m (Section 11.5). Neither is a
threat this section can check, which is why neither carries a test above.
