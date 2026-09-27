## 11. Technical Scope, Acquisition Implications, and What Is Not Claimed

This section states the boundary of the technical contribution. It is placed before the Conclusion
because the ethical argument that follows depends on the boundary being explicit, and because
several of the limitations below are properties of the measurement rather than qualifications added
after the fact.

### 11.1 The scale finding is arithmetic, not an established effect

Section 7.6 argues that training scale governs whether a target reaches the network, and supports
the argument by arithmetic: the median instance of the corpus of record, about 7 by 7 pixels once
the frame is downscaled to a 1536 pixel input, occupies less than one cell of the finest feature map
of a detector whose smallest stride is 8. The empirical pair quoted alongside it, mAP50 moving from
0.116 to 0.561 (files in Section 7.6), comes from two runs of an earlier arm that differ in five
further respects, and it is therefore consistent with the argument rather than evidence for it.

Obtaining the controlled measurement requires one experiment that has not been run: the same
detector, the same initialisation, the same epoch budget and the same corpus, trained once on
downscaled frames and once on native-scale tiles. Until that exists, this article does not report an
isolated effect of training scale, and no figure in it should be cited as one.

### 11.2 The benchmark is not the target domain

VisDrone records dense urban scenes from uncontrolled acquisition. It is the closest publicly
available proxy, and it is not a favela. The morphology this generator reproduces is specifically
that of consolidated self-built settlement on a hillside: shared party walls, alleys under 1.2
metres, upper storeys offset from the floor below.

A transfer figure obtained on VisDrone measures generalisation to the dense urban scenes that
benchmark records. It does not establish performance over Jacarezinho, and no claim of that kind is
made anywhere in this article. Establishing it would require annotated real imagery of the territory
itself, which the ethical protocol of Section 5 forecloses and which this project has deliberately
not collected.

A second consequence follows. Section 9.3 reports an oblique arm calibrated to the benchmark, but
the acquisition geometry this work reproduces points straight down. An oblique corpus that transfers
better to VisDrone tells us about VisDrone. It does not recommend an acquisition geometry for the
case study, and Section 11.3 is the only acquisition recommendation this article makes. The size of
the effect is itself the clearest statement of this limit: the same settlement rendered from a
tilted camera scores 6 times the nadir figure on VisDrone (0.0614 against 0.0102), not because it is
a better model of a settlement seen from a drone at 150 m, but because it resembles the benchmark's
acquisition. The best oblique configuration scores 10 times (0.1055), but it is not an ablation:
besides the camera it adds six settlements and keeps only figures carrying nothing, chosen because
their shape is closer to the benchmark's, so that factor is not attributable to acquisition alone
(Section 9.3). The nadir figure is the one that bears on the case study, and it is the lower one.

### 11.3 The acquisition implication, and the condition under which it is withdrawn

Section 8.3 measures contrast against local clutter lower under hard sun and rain than under
overcast, and proposes as the mechanism that the background under a hard sun is itself filled with
cast shadow from rooftop objects. If that mechanism holds when a detector is evaluated per regime,
the practical implication is direct and runs against the conventional preference for flying in clear
weather.

The implication is stated conditionally because the evidence is conditional. Eight images per
regime, with between-image dispersion of 0.12 to 0.38, resolves only the gap between the extremes at
roughly one standard deviation and does not resolve the ordering of the four intermediate regimes at
all. Section 10.3 specifies the test, which has not been run. If per-regime detector performance is
not higher under overcast than under both hard sun and rain, or if hard sun is not among the two
weakest regimes, this implication is withdrawn and the contrast measurement stands only as a
description of the imagery.

### 11.4 Two tasks share a pipeline and must not be conflated

The model proposed in Section 6 classifies built form. What is implemented in Section 7 and
evaluated in Sections 9 and 10 detects people. They share the generator, the annotation procedure,
the randomisation and the scale analysis; they do not share the object class, and no performance
figure reported here transfers from one to the other.

Person detection was implemented because a public benchmark exists for it and the question at issue
was whether synthesis transfers at all. The morphological task has no equivalent public benchmark at
this ground sampling distance, which is itself a finding worth recording: the evaluation
infrastructure for the morphological task that Section 6 proposes does not currently exist.

### 11.5 Where the armed and unarmed distinction exists, and where it does not

No accuracy figure for the armed and unarmed distinction is reported at 150 m, the altitude this
article takes as its reference acquisition. The omission is argued from resolution rather than
measured, and this section states the conditions that produce it.

At 150 m with the camera pointing straight down, rendered at the 4.88 cm per pixel of the corpus of
record, the median annotated instance measures 17.6 by 17.5 pixels. A firearm subtends a fraction of
that and is not resolvable within the region. A detector trained on such a corpus can still separate
the two classes, and that is precisely the problem: in a corpus where a weapon, drawn from three
rifle patterns and a pistol in four carrying poses, is the only elongated object any figure carries,
separability cannot be told apart from the regularity of the asset library. An accuracy figure
obtained there would be the inferential move this article criticises, a number produced under
controlled synthetic conditions and presented as evidence of a capability that would be exercised on
real people in a real territory.

Two changes make the question empirical rather than foreclosed, and both are reported in Section 9.
Halving the altitude to 75 m raises the median instance to 47.6 by 41.7 pixels, a 6.4-fold increase
in area over all classes and 5.2-fold for armed figures alone, at which the firearm occupies a
region the network can in principle resolve. And the corpus at that altitude is built to remove the
artefact, by the construction specified in Section 7.4: the weapons are set against elongated
objects carried in the same territory, drawn from the same colour and roughness palette and carried
through the same distribution of body poses, although objects longer than any weapon are held at
other angles (Section 7.4). A detector that separates the classes on that corpus cannot be doing so
by colour alone, and the rate at which it calls a broom a rifle is reported in Section 9.5.

The distinction between altitudes is the contribution, and it is stated as a condition rather than a
recommendation. At 150 m the capability is argued from resolution, not measured, to be absent: no
corpus with confusable objects was rendered at that altitude. At 75 m it exists in the sense that
the classes are separated above chance on the synthetic validation split, with the error profile of
Section 9.5, which calls 24 per cent of confusable objects armed; no threshold for calling the
capability present was fixed in advance. The measurements do not show it improving as resolution
increases further: at 35 m the same rate is 27 per cent. Whether that reflects a limit of what these
figures and carrying poses allow a detector to learn, or the change of pose distribution between the
two corpora, is what the matched corpus of Section 9.5 addresses, and in one training run per model
it points away from the pose. Rendered at 75 m with every setting of the 35 m corpus, the rate is 16
per cent against 27 at 35 m: with the pose held, the finer ground sampling distance did not reduce
the confusion, and the 35 m model calls every class armed more often rather than separating them
better, a difference that is suggestive rather than established at these sample sizes (Section 9.5).
Either way, a claim that a system distinguishes an armed from an unarmed person from the air is, at
the altitudes and sensors described here, a claim that can be checked before it is believed. Nothing
in this article recommends acquisition over the case study territory.

The 75 m figure itself would be withdrawn under a condition this article states rather than
delegates, and fixes before running: if the detector's recall on firearm models it has never seen
falls below four fifths of its recall on the models it was trained on, then what it separates is the
asset library and not the object, and no figure from that corpus should be read as a capability. The
test renders 50 new frames at 75 m, in a new realisation of the settlement and with the generator
settings of the training corpus, in which half the firearms are drawn from the five training models
and half from two models that enter no training corpus, a rifle of 1.10 m, longer than the recorded
length of any of the five (the longest, a shotgun, is recorded at 1.05 m) but inside their range as
modelled, since the meshes of the two training rifles and of the shotgun are longer than their
recorded lengths, and a compact submachine gun of 0.55 m, inside it, so that the test measures the
asset rather than a new size. The type of every annotated instance is recorded, so the two recalls
come from the same images under the same light. Recall on seen models: 0.400 (50 of 125); on unseen
models: 0.466 (61 of 131), a ratio of 1.16 (approximate 95 per cent interval 0.88 to 1.54, which
ignores the clustering of boxes within the 50 frames and is therefore optimistic) against the
threshold of 0.80, which the criterion applies to the ratio itself, so the condition is not met and
the 75 m figure stands (`06-resultados/holdout_armas_criterio.json`, produced by
`holdout_criterio.py`). The per-model rates, from 15 to 69 instances each and without intervals
(`06-resultados/holdout_armas_armado_75.json`, produced by `06-resultados/confusao_armado.py` in
step B2 of `07-blender/scripts/rodada3.py`), are consistent with the detector generalising to length
and silhouette rather than to the asset: the unseen 1.10 m rifle is called armed at 0.50, among the
seen long arms (0.34 to 0.52), the unseen 0.55 m submachine gun at 0.43, the pistol at 0.20, and a
closed umbrella, 0.88 m long, at 0.38. The generalisation that passes this test is plausibly the one
that produces the confusion of Section 9.5. Every rate at which a class is called armed is lower in
the new realisation than on the validation split (armed recall 0.43 in
`holdout_armas_armado_75.json` against 0.55 in `06-resultados/confusao_armado_75.json`), which does
not affect the comparison, made within the same images.

### 11.6 Reproducibility, and what a reader cannot check

Every generated image carries its seed, illumination regime and camera altitude in a manifest entry.
The settlement is reproduced exactly from the seed; the figures in it were not, in the three corpora
rendered before the defect was found (the pilot corpus, the corpus of record and the original 75 m
corpus), because the human generator drew from an unseeded random stream, a defect found and closed
after those corpora were rendered. The settlement, the camera and the illumination of every reported
image are therefore reproducible from the manifest, and the exact placement of figures is
reproducible only for corpora generated after the fix. Camera pitch is recorded per image only in
corpora generated after that field was added; the two nadir corpora of Section 8.2 predate it, which
is why their rows carry the generator setting rather than a per-image value, and the table says so.
The hyperparameter and inference table of Section 7.6 is in the body of the article, rather than in
an appendix, so that every parameter needed to reproduce a run is in the article itself.

What a reader cannot check from this article is the corpus itself, although the reason is logistical
rather than legal: every corpus generated for this article is redistributable by construction, since
all geometry other than the CC0 human figures of Section 7.4 and the CC0 tree models of Section 7.2
is authored by the generator and all surface materials are public domain; the earlier arm behind the
0.116 to 0.561 pair of Section 7.6 draws building footprints from OpenStreetMap, and the real
benchmark, VisDrone, is distributed by its own authors. Earlier branches of this project were built
on photogrammetric reconstruction of imagery that cannot be released, and no measurement reported in
this article derives from them.
