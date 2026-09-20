## 9. Results: Transfer to Real Imagery

> **Provenance note.** Quantities marked `[X]` are pending measurement and are not to be filled by
> estimation. The protocol in Section 4.7 was fixed before any of them was run, and Section 10
> declares in advance what would overturn each claim.

A pilot of the full protocol was run before the corpus reached its final size. Its results are
reported first, because they bound what follows and because withholding an unfavourable pilot
would make the rest of this section unreadable as evidence.

| Pilot run | Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| S-nadir, 40 training scenes at 1080p | synthetic validation | 0.109 | 0.148 | 0.077 | 0.019 |
| same model | VisDrone-DET val, zero-shot | 0.038 | 0.031 | 0.0055 | 0.0020 |
| same model | VisDrone-DET val, scale-matched | 0.041 | 0.037 | 0.0061 | 0.0009 |

*Source: `06-resultados/sim2real_morro_v1.json`.*

These are not results about transfer. The model failed on its own domain, reaching 0.077 where an
earlier arm of this project reached 0.676, and transfer cannot be measured from a model that did
not learn. Sections 10.1 and 10.2 identify the two causes, both properties of the pilot corpus
rather than of the method: it contained 40 training scenes against 473, and it was rendered at
1080p, which doubles the ground sampling distance and places a quarter of all instances below one
stride of the network (Section 8.1).

The pilot does establish one thing a favourable result could not. This pipeline is capable of
failing, and the failure is legible in the corpus statistics before any training. The rows below
report the protocol re-run with both defects corrected.

### 9.1 Ceiling: what real training data achieves on this test set

Model R, trained on VisDrone-DET train (6,471 images, 106,396 instances) and evaluated on
VisDrone-DET validation.

| Model | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| R (real training data) | `[X]` | `[X]` | `[X]` | `[X]` |

This figure is the denominator for everything that follows. It is not a claim about our method; it
establishes what the test set permits.

### 9.2 Transfer from synthetic training, nadir geometry

Model S-nadir, trained only on procedurally generated imagery with the camera geometry of the 2022
survey flight, evaluated on the same real test set with no real training image of any kind.

| Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Synthetic validation (ceiling of the corpus) | `[X]` | `[X]` | `[X]` | `[X]` |
| VisDrone-DET val (zero-shot) | `[X]` | `[X]` | `[X]` | `[X]` |

**Efficacy of the synthetic method** = mAP50(S-nadir) / mAP50(R) = `[X]`.

Kiefer, Ott and Zell (2022) report low single-digit mAP for purely synthetic training evaluated
on VisDrone. That order of magnitude is given as the scale on which to read the row above, not as
a defence of it. The exact interval reported by those authors is not quoted here because the
reference has not yet been checked against the published proceedings. What this article reports is the ratio to the ceiling, together with the comparison in
Section 9.3.

### 9.3 Transfer from synthetic training, oblique geometry

Model S-oblique. Identical generator, identical settlement, identical illumination regimes; only
the camera is moved.

Pitch is set from the height-to-width ratio of the VisDrone **training** split, not the validation
split on which every model in this article is scored. The distinction is load-bearing: the ratio
of 2.20 quoted in Section 8.2 is measured on the validation split, and calibrating a training
corpus on a statistic of the test set and then reporting the gain on that same test set would be
circular. The value used for calibration is `[X]`, measured on the training split alone.

This arm is therefore an adaptation of the corpus to the benchmark, and is reported as such rather
than as a discovery about acquisition geometry in general. What it isolates is whether the
mismatch identified in Section 8.2 is load-bearing on this benchmark.

| Model | mAP50 on VisDrone-DET val | Efficacy vs. ceiling |
|---|---|---|
| S-nadir | `[X]` | `[X]` |
| S-oblique | `[X]` | `[X]` |

**Difference attributable to acquisition geometry, on this benchmark** =
mAP50(S-oblique) - mAP50(S-nadir) = `[X]`.

Two outcomes are possible and both are reportable. If the oblique arm substantially outperforms
the nadir arm, acquisition geometry is load-bearing relative to scene content on this benchmark.
That is consistent with the direction of Liao et al. (2026) without extending their claim, since
a single benchmark that is not the target domain cannot support a general statement about camera
position. If the two arms are comparable, the limitation lies in synthesis rather than viewpoint,
and the conclusion narrows accordingly.

The survey flight this article reproduces is nadir. An oblique corpus that transfers better to
VisDrone is informative about the benchmark, not about the acquisition that would be flown over
Jacarezinho.

<!--FIG:06-resultados/figuras/fig4_dataset.jpg|One annotated frame from each of the six illumination regimes, with the generated boxes drawn. Green marks the armed class and blue the unarmed class, and no accuracy figure for that distinction is reported anywhere in this article, for the reason given in Section 11.5. The figure is included to show that annotation and occlusion handling behave identically across regimes, so that per-regime performance differences in Section 10.3 cannot be attributed to the labelling.-->

### 9.4 Limited real fine-tuning

Model S-nadir pretrained, then fine-tuned on 5 and 10 per cent of VisDrone-DET train, against R
trained on the same fractions from scratch.

| Real data used | S pretrained then fine-tuned | R from scratch | Difference |
|---|---|---|---|
| 5 per cent | `[X]` | `[X]` | `[X]` |
| 10 per cent | `[X]` | `[X]` | `[X]` |
| 100 per cent | `[X]` | `[X]` | `[X]` |

This is the quantity with the clearest practical meaning for the proposal in Section 6: how much
consent-bounded real imagery the synthetic pretraining removes the need for. The literature
surveyed in Section 2 suggests that 5 to 20 per cent of real data recovers 85 to 95 per cent of
performance given good synthetic pretraining; whether that holds at this ground sampling distance
and in this scene type is an open question that these rows answer.

### 9.5 What is deliberately not reported here

The detector distinguishes two classes in the synthetic corpus, armed and unarmed. No accuracy
figure for that distinction is reported here. Section 8.1 measures the median target at approximately 25 pixels on its long side, and at 4K the
median box measures roughly 18.5 by 22.9 pixels. A firearm is not resolvable within a region of
that size. In the synthetic corpus the distinction is nevertheless learnable, because the weapon
is always the same model in the same pose at the same contrast, which makes it an artefact of the
generator rather than a visual property of the world. Reporting a class accuracy under those
conditions would be exactly the inferential leap that Section 2 of this article criticises in the
existing literature, and it is therefore withheld. The point is returned to in Section 11.
