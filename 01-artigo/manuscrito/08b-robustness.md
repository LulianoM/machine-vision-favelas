## Robustness and Alternative Explanations

> **Status note, 2026-09-20.** This section is specified before measurement, not after. Every
> subsection below states, in advance, the condition under which the corresponding claim would be
> withdrawn. Those conditions were fixed while the corpus was still rendering, and the text
> commits to reporting each check whether or not it is favourable. Quantities appear as `[X]`
> until measured.

This forum has no discussants. A robustness argument that lives in an appendix, or in the
authors' confidence, is not available to the reader. The section is therefore numbered, placed in
the body, and organised so that each threat is named, tested, and given an explicit condition that
would overturn the result it protects.

Two commitments govern what follows. Each check was specified before the corresponding
measurement was run. Each is reported regardless of outcome.

### 8.1 The corpus is small, and small corpora flatter themselves

**Threat.** The synthetic corpus is generated, so its size is a choice rather than a constraint,
and a detector trained on few scenes can memorise them. An earlier pilot of this pipeline used 40
training images and reached mAP50 of 0.077 on its own validation split, against 0.676 obtained by
a previous arm of this project with 473 images. The pilot is reported here because it is
instructive, not because it is a result: it establishes that this pipeline is capable of failing,
and identifies scene count as one of two causes.

**Check.** Learning curve over the number of distinct generated scenes, holding the illumination
regimes balanced and the tiling protocol fixed: `[X]`.

**What would overturn the claim.** If performance on the real test set does not separate the
largest corpus from the smallest, scene count is not the operative variable and the conclusion of
Section 7 must be restated as a property of the generator rather than of corpus size.

### 8.2 Apparent size, not synthesis, may explain the transfer gap

**Threat.** Section 6.1 reports that the synthetic target at 4K and the real benchmark target are
of near-identical median size, 24.6 and 25.0 pixels. That match is a property of the rendering
resolution we selected. If it were not exact, a transfer failure attributable to scale could be
mistaken for a failure attributable to synthesis.

**Check.** The real test set is additionally evaluated after rescaling so that its target size
distribution is matched to the training corpus by construction. The label format is normalised, so
rescaling the image leaves the annotation unchanged and the control is clean. Results: `[X]` at
native scale, `[X]` at matched scale.

**What would overturn the claim.** If the two figures differ substantially, scale remains a live
confound and the efficacy ratio in Section 7.2 must be reported at matched scale only.

This subsection also records a correction. An earlier version of this analysis reported a
2.49-fold scale gap between corpus and benchmark and treated it as an inherent altitude domain
shift. It was an artefact of rendering the corpus at 1920 by 1080 rather than at 4K. The claim is
withdrawn, and the check above exists so that the same error is detectable rather than assumed
absent.

### 8.3 Illumination: the prediction that runs against intuition

**Threat.** Section 6.3 measures that hard sunlight yields the largest raw figure-to-background
difference and the worst contrast against local clutter, and predicts that the detector will
perform better under overcast than under hard sun. A measurement of image statistics is not a
measurement of detector behaviour, and the prediction could simply be wrong.

**Check.** Per-regime performance on a held-out synthetic split, six regimes, balanced: `[X]`.
Ablation against a corpus generated under hard sun only, evaluated on the full six-regime split
and on the real test set: `[X]`.

**What would overturn the claim.** If per-regime performance does not order inversely with raw
contrast, or if hard sun is not among the weakest regimes, the mechanism proposed in Section 6.3
is wrong and the operational implication in Section 9 is withdrawn. The image statistics would
still stand, but they would be describing something other than detector difficulty.

### 8.4 Capture geometry against scene content

**Threat.** The central comparison of this article attributes a performance difference to camera
placement. It could instead reflect any of the incidental differences between the two synthetic
arms.

**Check.** The two arms are generated from the same code, the same settlement seed, the same
material library, the same illumination regimes and the same annotation procedure. The camera
pitch and altitude are the only parameters that differ, and they are calibrated on the
height-to-width ratio measured in Section 6.2 rather than chosen. Result: `[X]`.

**What would overturn the claim.** If the oblique arm does not outperform the nadir arm, capture
geometry is not the dominant term, and Section 7.3 must conclude that the limitation lies in
synthesis rather than viewpoint. That outcome is reportable and is not treated here as a failure
of the study.

### 8.5 The ceiling may be low for reasons unrelated to us

**Threat.** A low transfer figure is uninterpretable without knowing what the test set permits.
Small-object aerial detection is difficult for real-data models too, and a reader has no way to
distinguish a weak synthetic method from a hard benchmark.

**Check.** Model R, trained on the real training split of the same benchmark under the same
detector, the same input size and the same schedule: `[X]`. All synthetic figures are reported as
a ratio to it.

**What would overturn the claim.** If R itself performs near chance under this protocol, the
protocol is inadequate to the benchmark and no conclusion about synthetic efficacy can be drawn
from it. In that case the appropriate report is the failure of the evaluation design, not a
finding about synthesis.

### 8.6 Annotation convention as a source of spurious difference

**Threat.** Boxes in the synthetic corpus are amodal and generated by vertex projection; boxes in
the benchmark are human-drawn. A systematic difference in how tightly boxes bound their target
would move intersection-over-union scores without any difference in detection.

**Check.** Distribution of box area and aspect ratio in both corpora is reported in Section 6.
Sensitivity of the reported figures to the intersection-over-union threshold: `[X]`.

**What would overturn the claim.** If the ordering of the three models changes with the threshold,
the comparison is an artefact of annotation tightness and must be reported at multiple thresholds
rather than at the conventional one.

### 8.7 Determinism and reproducibility

**Threat.** A generated corpus that cannot be regenerated is not auditable, and a single seed may
be favourable by chance.

**Check.** Every image carries its seed, illumination regime, camera altitude and pitch in a
manifest entry, and the generator reproduces any image exactly from that entry. The full protocol
is repeated across `[X]` independent settlement seeds, and the dispersion between them is reported
alongside the mean.

**What would overturn the claim.** If between-seed dispersion is of the same order as the
differences reported in Section 7, those differences are not resolvable with this corpus size and
must be reported as inconclusive.

### 8.8 What this design cannot rule out

Two limitations are structural rather than testable within this study, and are stated here rather
than left to the reader to notice.

The benchmark is not a favela. VisDrone records dense urban scenes, which is the closest publicly
available proxy, but the morphology the generator reproduces is specifically that of consolidated
self-built settlement on a hillside. A transfer figure obtained on this benchmark bounds
generalisation to dense aerial scenes; it does not establish performance over Jacarezinho, and no
claim of the latter is made anywhere in this article.

The class distinction between armed and unarmed figures is not evaluated at all, for the reason
given in Section 7.5. Its exclusion is a limitation of scope that is also a deliberate ethical
choice, and Section 9 treats it as such rather than as a gap to be closed in future work.
