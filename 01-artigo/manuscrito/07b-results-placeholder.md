## 9. Results: Transfer to Real Imagery

> **Provenance note.** Quantities marked `[X]` are pending measurement and are not to be filled by
> estimation. The protocol in Section 7.7 was fixed before any of them was run, and Section 10
> declares in advance what would overturn each claim.

A pilot of the full protocol was run before the corpus reached its final size. Its results are
reported first, because they bound what follows and because withholding an unfavourable pilot
would make the rest of this section unreadable as evidence.

| Pilot run | Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| S-nadir-150, 40 training scenes at 1080p | synthetic validation | 0.109 | 0.148 | 0.077 | 0.019 |
| same model | VisDrone-DET val, zero-shot | 0.038 | 0.031 | 0.0055 | 0.0020 |
| same model | VisDrone-DET val, scale-matched | 0.041 | 0.037 | 0.0061 | 0.0009 |

*Source: `06-resultados/sim2real_morro_v1.json`.*

These are not results about transfer. The model failed on its own domain, reaching 0.077 where an
earlier arm of this project reached 0.676, and transfer cannot be measured from a model that did
not learn. Sections 10.1 and 10.2 identify the two causes, both properties of the pilot corpus
rather than of the method: it contained 40 training scenes against 473, and it was rendered at
1080p, which doubles the ground sampling distance and places two thirds of all instances below one
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

Model S-nadir-150, trained only on procedurally generated imagery with the camera geometry of Section 7.3,
evaluated on the same real test set with no real training image of any kind.

| Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Synthetic validation (ceiling of the corpus) | `[X]` | `[X]` | `[X]` | `[X]` |
| VisDrone-DET val (zero-shot) | `[X]` | `[X]` | `[X]` | `[X]` |

**Efficacy of the synthetic method** = mAP50(S-nadir-150) / mAP50(R) = `[X]`.

Kiefer, Ott and Zell (2022) report mAP@50 on VisDrone for three architectures trained purely on
synthetic data: 1.2 for EfficientDet-D0, 2.4 for Faster R-CNN and 10.2 for YOLO, against 24.6,
48.6 and 43.9 respectively for the same architectures trained on real data. The YOLO row is the
comparable one, since this article trains YOLO, and it gives a ratio of 23.2 per cent.

The two ratios are not directly comparable, and the reason matters more than the gap. Their
denominator is a detector trained on real imagery from a different domain and evaluated on
VisDrone; ours is trained on the VisDrone training split and evaluated on its validation split.
Ours is the harsher denominator, so our ratio understates the method relative to theirs by an
amount this design cannot quantify. What this article reports is the ratio to its own declared
ceiling, together with the comparison in Section 9.3.

### 9.3 Transfer from synthetic training, oblique geometry

Model S-oblique. Identical generator, identical settlement, identical illumination regimes; only
the camera is moved.

Pitch is set from the height-to-width ratio of the VisDrone **training** split, not the validation
split on which every model in this article is scored. The distinction is load-bearing: the ratio
of 2.20 quoted in Section 8.2 is measured on the validation split, and calibrating a training
corpus on a statistic of the test set and then reporting the gain on that same test set would be
circular. The value used for calibration is 1.95, measured on the training split alone (Section 8.2).

This arm is therefore an adaptation of the corpus to the benchmark, and is reported as such rather
than as a discovery about acquisition geometry in general. What it isolates is whether the
mismatch identified in Section 8.2 is load-bearing on this benchmark.

| Model | mAP50 on VisDrone-DET val | Efficacy vs. ceiling |
|---|---|---|
| S-nadir-150 | `[X]` | `[X]` |
| S-oblique | `[X]` | `[X]` |

**Difference attributable to acquisition geometry, on this benchmark** =
mAP50(S-oblique) - mAP50(S-nadir-150) = `[X]`.

Two outcomes are possible and both are reportable. If the oblique arm substantially outperforms
the nadir arm, acquisition geometry is load-bearing relative to scene content on this benchmark.
That is consistent with the direction of Liao et al. (2026) without extending their claim, since
a single benchmark that is not the target domain cannot support a general statement about camera
position. If the two arms are comparable, the limitation lies in synthesis rather than viewpoint,
and the conclusion narrows accordingly.

The acquisition geometry this article reproduces points straight down. An oblique corpus that transfers better to
VisDrone is informative about the benchmark, not about the acquisition that would be flown over
Jacarezinho.

<!--FIG:06-resultados/figuras/fig4_dataset.jpg|One annotated frame from each of the six illumination regimes, with the generated boxes drawn. Green marks the armed class and blue the unarmed class. No accuracy figure for that distinction is reported at this altitude, for the reason given in Section 11.5; the 75 m result is reported in Section 9.5. The figure is included to show that annotation and occlusion handling behave identically across regimes, so that per-regime performance differences in Section 10.3 cannot be attributed to the labelling.-->

### 9.4 Real fine-tuning, deferred

The proposal of Section 6 reserves a stage in which the synthetic pretraining is fine-tuned on a modest volume of real imagery. That stage is not run in this version, and the reason is one of sequence rather than feasibility: the question this article isolates is what synthesis alone recovers, and adding real data before that figure is settled would make the two contributions inseparable. The measurement is specified in the Conclusion as the next step, on the same public benchmark and with the same protocol as Section 9.2.

### 9.5 The armed and unarmed distinction, by altitude

No accuracy for the armed and unarmed distinction is reported at 150 m. At that altitude the
median instance measures 17.6 by 17.5 pixels and a firearm is not resolvable within it. The
distinction is nevertheless learnable in a corpus where the weapon is always the same asset in
the same pose at the same contrast, which makes separability a property of the generator rather
than of the world, and reporting it would be the inferential leap this article criticises.

At 75 m the median instance measures 47.6 by 41.7 pixels, 6.4 times the area, and the corpus is
built so that the artefact cannot account for the result: five firearm models against nine
elongated objects carried in the same territory, sharing the weapons' colour and roughness
palette and the same distribution of carrying poses. The corpus holds `[X]` instances, `[X]` of
them armed, `[X]` unarmed and `[X]` carrying a confusable object.

| Quantity at 75 m | Value |
|---|---|
| mAP50, three classes | `[X]` |
| Recall, armed | `[X]` |
| Precision, armed | `[X]` |
| Rate at which a confusable object is called armed | `[X]` |
| Rate at which an unarmed person with no object is called armed | `[X]` |

The fourth row is the quantity of interest. It is the rate at which the system would mark a
resident carrying a broom, a length of pipe or a rolled mat as armed, and it is the concrete form
of the dual-use harm this article discusses. Section 10 states, for each result above, the
condition that would overturn it, and Section 11.5 reads the two altitudes together.
