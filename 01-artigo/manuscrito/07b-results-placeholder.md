## Results: Transfer to Real Imagery

> **Status note, 2026-09-20. THIS SECTION IS NOT WRITTEN.** It is a scaffold with declared
> placeholders. The synthetic corpus at 4K is still rendering and the three models have not been
> trained. Every `[X]` below marks a quantity that must come from a measurement recorded in
> `06-resultados/`, with the command that produced it. No figure in this section may be estimated,
> inferred from an earlier arm, or filled in from expectation. Where a result comes out
> unfavourable it is reported as it is: the protocol in Section 3.7 was fixed before the
> measurement, and Section 8 declares in advance what would overturn each claim.

### 7.1 Ceiling: what real training data achieves on this test set

Model R, trained on VisDrone-DET train (6,471 images, 106,396 instances) and evaluated on
VisDrone-DET validation.

| Model | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| R (real training data) | `[X]` | `[X]` | `[X]` | `[X]` |

This figure is the denominator for everything that follows. It is not a claim about our method; it
establishes what the test set permits.

### 7.2 Transfer from synthetic training, nadir geometry

Model S-nadir, trained only on procedurally generated imagery with the camera geometry of the 2022
survey flight, evaluated on the same real test set with no real training image of any kind.

| Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Synthetic validation (ceiling of the corpus) | `[X]` | `[X]` | `[X]` | `[X]` |
| VisDrone-DET val (zero-shot) | `[X]` | `[X]` | `[X]` | `[X]` |

**Efficacy of the synthetic method** = mAP50(S-nadir) / mAP50(R) = `[X]`.

Calibration note to be retained in the final text: Kiefer, Ott and Zell (ICPR 2022) report 1.2 to
2.4 mAP for purely synthetic training evaluated on VisDrone. A low absolute figure here is
consistent with the literature and is not by itself evidence that this generator failed. The
informative quantity is the ratio above, and the comparison in 7.3.

### 7.3 Transfer from synthetic training, oblique geometry

Model S-oblique. Identical generator, identical settlement, identical illumination regimes; only
the camera is moved, to a pitch and altitude calibrated on the height-to-width ratio of 2.20
measured in Section 6.2.

| Model | mAP50 on VisDrone-DET val | Efficacy vs. ceiling |
|---|---|---|
| S-nadir | `[X]` | `[X]` |
| S-oblique | `[X]` | `[X]` |

**Isolated cost of capture geometry** = mAP50(S-oblique) - mAP50(S-nadir) = `[X]`.

Interpretation to be written once measured. Two outcomes are possible and both are reportable.
If the oblique arm substantially outperforms the nadir arm, the finding is that capture geometry
dominates scene realism, which extends the result of Liao et al. (2026) from the origin of scene
geometry to the position of the camera. If the two arms are comparable, the failure is
attributable to synthesis itself rather than to viewpoint, and the appropriate conclusion is a
narrower claim about what this pipeline supports.

### 7.4 Limited real fine-tuning

Model S-nadir pretrained, then fine-tuned on 5 and 10 per cent of VisDrone-DET train, against R
trained on the same fractions from scratch.

| Real data used | S pretrained then fine-tuned | R from scratch | Difference |
|---|---|---|---|
| 5 per cent | `[X]` | `[X]` | `[X]` |
| 10 per cent | `[X]` | `[X]` | `[X]` |
| 100 per cent | `[X]` | `[X]` | `[X]` |

This is the quantity with the clearest practical meaning for the proposal in Section 5: how much
consent-bounded real imagery the synthetic pretraining removes the need for. The literature
surveyed in Section 2 suggests that 5 to 20 per cent of real data recovers 85 to 95 per cent of
performance given good synthetic pretraining; whether that holds at this ground sampling distance
and in this scene type is an open question that these rows answer.

### 7.5 What is deliberately not reported here

The detector distinguishes two classes in the synthetic corpus, armed and unarmed. Those class
figures are not reported in this section, and the decision is stated rather than left implicit.
Section 6.1 measures the median target at approximately 25 pixels on its long side, and at 4K the
median box measures roughly 18.5 by 22.9 pixels. A firearm is not resolvable within a region of
that size. In the synthetic corpus the distinction is nevertheless learnable, because the weapon
is always the same model in the same pose at the same contrast, which makes it an artefact of the
generator rather than a visual property of the world. Reporting a class accuracy under those
conditions would be exactly the inferential leap that Section 2 of this article criticises in the
existing literature, and it is therefore withheld. The point is returned to in Section 9.
