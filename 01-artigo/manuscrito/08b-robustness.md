## 10. Robustness and Alternative Explanations

> **Provenance note.** Quantities appear as `[X]` until measured, and each check is reported whether
> or not its outcome is favourable.

Each threat below is named, given a check, and given an explicit condition that would overturn the
result it protects; where the check has not been run, the text says so. Stating that condition in
advance is what distinguishes a check from a defence written after seeing the number. Each
overturning condition below was fixed before the corresponding measurement was run; the two made
more precise afterwards, in Sections 10.1 and 10.3, were changed before their tests and say so.

### 10.1 The corpus is small, and small corpora flatter themselves

**Threat.** The synthetic corpus is generated, so its size is a choice rather than a constraint, and
a detector trained on few scenes can memorise them. An earlier pilot of this pipeline used 40
training images and reached mAP50 of 0.077 on its own validation split, against 0.79 for the corpus
of record with 180 images at 4K (Section 9.2). The pilot is reported here because it is instructive,
not because it is a result: it establishes that this pipeline is capable of failing, and points to
scene count as one candidate cause, which the check below would test and which has not been
isolated.

**Check.** Learning curve over the number of distinct generated scenes, holding the illumination
regimes balanced and the tiling protocol fixed. A related comparison has been run at a fixed 180
images, one settlement against six (Section 9.2): 0.0102 against 0.0190 on the real test set. It
varies the variety of settlement at a fixed number of scenes, so it is not a point on this curve,
which remains `[X]`.

**What would overturn the claim.** If performance on the real test set does not rise from the
smallest corpus to the largest by more than the between-seed dispersion of Section 10.6, scene count
is not the operative variable and the conclusion of Section 9 must be restated as a property of the
generator rather than of corpus size. This wording adds a direction and a margin to an earlier one
that asked only whether the two were separated, and is fixed here, before the curve has been run.

### 10.2 Apparent size, not synthesis, may explain the transfer gap

**Threat.** Section 8.1 reports that the synthetic target at 4K and the real benchmark target cover
near-identical median area, 301 and 300 square pixels, the second with the benchmark's training and
validation splits pooled. That match is a property of the rendering resolution we selected, and it
does not extend to the long side, which is 20.6 against 25.0 pixels. Where it is not exact, as on
the long side, a transfer failure attributable to scale could be mistaken for a failure attributable
to synthesis.

**Check.** The real test set is additionally evaluated after rescaling so that its target size
distribution matches the training corpus by construction. The label format is normalised, so
rescaling the image leaves the annotation unchanged and the control is clean.

This check has already been run once, on the pilot reported in Section 9, and its outcome is given
here rather than withheld: mAP50 of 0.0055 at native scale against 0.0061 at matched scale, a
difference of 0.0006 (`06-resultados/sim2real_morro_v1.json`). On that pilot, matching the scale did
not recover performance. Because the pilot did not learn its own domain (Section 9), that outcome is
uninformative about scale as a confound: it neither supports nor rules out the explanation most
favourable to us. On the corrected corpus only the native-scale half has been run: 0.0102 (Section
9.2). The pilot matched the benchmark to the corpus on the median long side of the box. On the
corrected corpus the two targets match closely in median area but not on the long side, as the
threat above records, and because they differ in shape no uniform rescaling matches both. The
matched-scale half was dropped before the native-scale figure was known, on the argument that
rescaling by area would leave the benchmark essentially where it is; that argument is not a
measurement, and a rescaling on the long side, as in the pilot, has not been run. What still differs
at matched area is shape, which Section 10.4 tests.

**What would overturn the claim.** If the two figures diverge substantially on the corrected corpus,
scale is a live confound after all and the efficacy ratio in Section 9.2 must be reported at matched
scale only. On the corrected corpus this condition has not been evaluated.

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

**Check.** Per-regime performance on a held-out synthetic split, six regimes, balanced: `[X]`.
Ablation against a corpus generated under hard sun only, evaluated on the full six-regime split and
on the real test set: `[X]`.

**What would overturn the claim.** If per-regime performance is not higher under overcast than under
both hard sun and rain, the only gap that Section 8.3 approaches resolving, or if hard sun is not
among the two weakest regimes, the mechanism proposed in Section 8.3 is wrong and the operational
implication in Section 11 is withdrawn. The image statistics would still stand, but they would be
describing something other than detector difficulty. The ablation in the check above carries no
overturning condition and is reported descriptively. An earlier wording of this condition referred
to raw contrast, from a superseded measurement in which hard sun had the largest raw difference, and
a later one asked that performance order with contrast against local clutter without saying over
which regimes; both are corrected here, before the per-regime test has been run.

### 10.4 Capture geometry against scene content

**Threat.** The central comparison of this article attributes a performance difference to camera
placement. It could instead reflect any of the incidental differences between the two synthetic
arms.

**Check.** The two models are trained on corpora generated with the same settings (though not from
the same code: the nadir corpus predates the five-model weapon library of Section 7.4, so its armed
figures carry one of three rifle patterns or a pistol and are held forward with probability 0.46
rather than 0.42), the same settlement seed, the same material library, the same illumination
regimes, the same share of armed and unarmed figures and the same annotation procedure, with the
same training recipe and the same number of images, both at 4K. What differs is the camera: pitch,
drawn between 26 and 52 degrees and recorded per image, altitude (120 m for the oblique camera) and
its jitter. One further setting differs because the camera does: the nadir corpus keeps figures
within a square around the camera axis whose side is 0.52 of the nadir frame width (`--enquadro
quadrado` in `07-blender/scripts/gen_morro.py`), the filter that produced it, while the oblique
corpus places them anywhere the projected frame covers, since an oblique frame is not a square on
the ground. At the centre of the frame and at the nominal 120 m, the oblique camera puts the ground
sampling distance between about 4.3 and 6.3 cm per pixel across the pitch range, a span the altitude
jitter widens, against 4.88 for the nadir corpus, so the change of camera moves the shape of the
target (h/w 1.46 against 0.98) and leaves its size in the same range, somewhat larger in area (456
against 301 square pixels). Pitch is set from the VisDrone training split rather than from the
validation split on which both models are scored, so that the calibration does not consume the test
set. Result: 0.0614 for the oblique model against 0.0102 for the nadir model on the real test set.
The figure of 0.1055 for S-oblique-six (Section 9.3) is not a result of this check: that corpus also
changes the settlements, the pitch range, the figures, which carry nothing, and the placement of the
camera.

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

### 10.6 Two checks specified and not run

Two further threats have a check specified in advance and no result in this version, and they are stated so that their absence is visible rather than silent.

**Annotation convention.** Synthetic boxes are amodal and projected from vertices; benchmark boxes are human-drawn. A systematic difference in tightness would move overlap scores without any difference in detection. The check is sensitivity of every reported figure to the intersection-over-union threshold at 0.50, 0.60 and 0.75; if the ordering of the models changes with the threshold, the comparison is an artefact of annotation and must be reported at several thresholds.

**Seed dependence.** A single settlement seed, and a single training run per model, may be favourable by chance. The check is repetition of the protocol across independent seeds with the between-seed dispersion reported alongside the mean; if that dispersion is of the same order as the differences reported in Section 9, those differences are not resolvable at this corpus size. Every image carries its seed in a manifest entry and the generator reproduces the settlement exactly from it (Section 11.6 names the three corpora whose figures it did not reproduce), so the check is a matter of compute rather than of design.

### 10.7 What this design cannot rule out

Two boundaries of this design are structural rather than testable, and are stated in Section 11
rather than argued here: the benchmark is not a favela (Section 11.2), and the armed and unarmed
distinction is reported at 75 m and 35 m and deliberately withheld at 150 m (Section 11.5). Neither
is a threat this section can check, which is why neither carries a test above.
