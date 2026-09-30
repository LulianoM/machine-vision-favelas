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
0.116 to 0.561 (Section 7.6), comes from two runs of an earlier arm that differ in five further
respects, and it is therefore consistent with the argument rather than evidence for it.

Obtaining the controlled measurement requires one experiment that has not been run: the same
detector, the same initialisation, the same epoch budget and the same corpus, trained once on
downscaled frames and once on native-scale tiles. Until that exists, this article does not report an
isolated effect of training scale, and no figure in it should be cited as one.

### 11.2 The benchmark is not the target domain

VisDrone records dense urban scenes from uncontrolled acquisition. It is the closest publicly
available proxy, and it is not a favela. The morphology this generator reproduces is specifically
that of consolidated self-built settlement on a hillside: abutting dwellings, alleys mostly under
1.2 m, upper storeys offset from the floor below.

A transfer figure obtained on VisDrone measures generalisation to the dense urban scenes that
benchmark records. It does not establish performance over Jacarezinho, and no claim of that kind is
made anywhere in this article. Establishing it would require annotated real imagery of the territory
itself, which the ethical protocol of Section 5 forecloses and which this project has deliberately
not collected.

A second consequence follows. Section 9.3 reports an oblique arm calibrated to the benchmark, but
the acquisition geometry this work reproduces points straight down. An oblique corpus that transfers
better to VisDrone tells us about VisDrone. It does not recommend an acquisition geometry for the
case study, and Section 11.3 states the only acquisition implication this article draws, limited to
synthetic imagery and one detector, and it concerns how to fly, not whether to acquire imagery of
the case study territory, which nothing in this article recommends (Section 11.5). The size of the
effect is itself the clearest statement of this limit: the same settlement rendered from a tilted
camera scores 6 times the nadir figure on VisDrone (0.0614 against 0.0102), not because it is a
better model of a settlement seen from a drone at 150 m, but most plausibly because it resembles the
benchmark's acquisition; Section 10.4 lists what else differs between the two corpora. The best
oblique configuration scores 10.3 times the nadir figure in its first training run (0.1055) and 9.5
times over the mean of three (0.0967), but it is not an ablation: besides the camera it adds six
settlements and keeps only figures carrying nothing, chosen because their shape is closer to the
benchmark's, so that factor is not attributable to acquisition alone (Section 9.3). The nadir figure
is the one that bears on the case study, and it is the lower one.

### 11.3 The acquisition implication, and the condition under which it is withdrawn

Section 8.3 measures contrast against local clutter lower under hard sun and rain than under
overcast, and proposes as the mechanism that the background under a hard sun is itself filled with
cast shadow from rooftop objects. A detector evaluated per regime finds hard sun the hardest regime,
as that mechanism predicts, but scores low sun, which also casts sharp shadows, level with overcast,
which the mechanism does not predict (Section 10.3). The practical implication is therefore narrower
than the mechanism: it concerns flying under a high sun, and it runs against the conventional
preference for flying in clear weather only to that extent.

The implication was stated conditionally because the evidence was conditional. Eight images per
regime, with between-image dispersion of 0.12 to 0.38, brought only the gap between the extremes
close to one standard deviation and did not resolve the ordering of the four intermediate regimes at
all. Section 10.3 specified a detection test and the condition under which the implication would be
withdrawn: per-regime performance not higher under overcast than under both hard sun and rain, or
hard sun not among the two weakest regimes. The test was run and the condition is not met: on 120
new frames hard sun is the weakest regime, and overcast scores above both hard sun and rain, level
on mAP50 with low sun, which has the higher recall (Section 10.3). The implication therefore stands,
on synthetic imagery and for one detector, in the narrower form given above; its robust part is that
hard sun is the weakest.

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
article takes as its reference acquisition. The absence of the capability there is argued from
resolution rather than measured, and this section states the conditions that produce it.

At 150 m with the camera pointing straight down, rendered at the 4.88 cm per pixel of the corpus of
record, the median annotated instance measures 17.6 by 17.5 pixels. A firearm subtends a fraction of
that, and its form is argued not to be resolvable within the region. A detector trained on such a
corpus might still separate the two classes, although none was trained to do so on it (S-nadir-150
detects a single person class, and the two-class pilot of Section 9 did not learn its own domain),
and that possibility is precisely the problem: in a corpus where a weapon, drawn from three rifle
patterns and a pistol in four carrying poses, is the only elongated object any figure carries,
separability could not be told apart from the regularity of the asset library. An accuracy figure
obtained there would be the inferential move this article criticises, a number produced under
controlled synthetic conditions and presented as evidence of a capability that would be exercised on
real people in a real territory. The one three-class model trained at 150 m, on a twin of the 35 m
corpus that does carry confusable objects, did not pass the validity condition fixed before it was
run (Section 9.5), so it neither confirms nor overturns this, although its descriptive rates, 0.34
of armed figures against 0.14 of confusable objects called armed, do not suggest that nothing
reaches the detector there.

Two changes make the question empirical rather than foreclosed, and both are reported in Section 9.
Halving the altitude to 75 m raises the median instance to 47.6 by 41.7 pixels, a 6.4-fold increase
in area over all classes and 5.2-fold for armed figures alone, at which the firearm occupies a
region the network can in principle resolve. And the corpus at that altitude is built to remove the
artefact, by the construction specified in Section 7.4: the weapons are set against elongated
objects carried in the same territory, drawn from the same colour and roughness palette and carried
through the same distribution of body poses, although objects longer than any weapon are held at
other angles, a difference that Section 9.5 shows does not lower the rate at which objects are
called armed. A detector that separates the classes on that corpus cannot be doing so by colour
alone, and the rate at which it calls a broom a rifle is reported in Section 9.5.

What this section contributes is a statement of where the distinction has been measured and where it
has only been argued, and it is stated as a condition rather than a recommendation. At 150 m the
capability is argued from resolution, not measured, to be absent (the one model trained there found
only 148 of 297 figures and did not pass its validity condition, Section 9.5). At 75 m it exists in
the sense that the classes are separated above chance on the synthetic validation split, with the
error profile of Section 9.5, which calls 24 per cent of confusable objects armed; no threshold for
calling the capability present was fixed in advance. The measurements do not show it improving as
resolution increases further: at 35 m the same rate is 27 per cent, although against the original 75
m corpus that comparison reverses at stricter overlap thresholds (Section 10.6). Whether that
reflects a limit of what these figures and carrying poses allow a detector to learn, or the change
of pose distribution between the two corpora, is what the matched corpus of Section 9.5 addresses,
and it points away from the pose. Rendered at 75 m with every setting of the 35 m corpus, the rate
is 16 per cent against 27 at 35 m, and on 80 new frames 12.5 against 25 (p = 0.0001), a difference
that holds across three training runs on those frames: with the pose held, the finer ground sampling
distance did not reduce the confusion, and in the first training run the 35 m model calls every
class armed more often rather than separating them better; across the three runs only the rate for
confusable objects keeps that direction. The difference is established at the overlap threshold of
the protocol and shrinks under a stricter one, vanishing at 0.75 on the validation split (Section
9.5). In any case, a claim that a system distinguishes an armed from an unarmed person from the air
is, at the altitudes and sensors described here, a claim that can be checked before it is believed.
Nothing in this article recommends acquisition over the case study territory.

The 75 m result itself would be withdrawn under a condition that this article states itself, rather
than leaving it to others, and that was fixed before the test was run: if the detector's recall on
firearm models it has never seen falls below four fifths of its recall on the models it was trained
on, then what it separates is the asset library and not the object, and no figure from that corpus
should be read as a capability. The test renders 50 new frames at 75 m, in a new realisation of the
settlement and with the generator settings of the training corpus, in which half the firearms are
drawn from the five training models and half from two models that enter no training corpus: a rifle
of 1.10 m and a compact submachine gun of 0.55 m. The rifle is longer than the recorded length of
any of the five (the longest, a shotgun, is recorded at 1.05 m) but inside their range as modelled,
since the meshes of the two training rifles and of the shotgun are longer than their recorded
lengths, and the submachine gun is inside that range, so that the test measures the asset rather
than a new size. The type of every annotated instance is recorded, so the two recalls come from the
same images under the same light. Recall is 0.400 on seen models (50 of 125) and 0.466 on unseen
models (61 of 131), a ratio of 1.16 (approximate 95 per cent interval 0.88 to 1.54, which ignores
the clustering of boxes within the 50 frames and is therefore optimistic) against the threshold of
0.80, which the criterion applies to the ratio itself, so the condition is not met and the 75 m
figure stands. The two groups are not matched in composition: the seen group includes the pistol, 20
of its 125 instances, shorter than either unseen model and the weapon least often called armed, so
part of the ratio above one reflects that composition rather than better recognition of the unseen
models; with the pistol set aside, the ratio still stays above the threshold. The per-model rates,
from 15 to 69 instances each and without intervals, are consistent with the detector generalising to
length and silhouette rather than to the asset: the unseen 1.10 m rifle is called armed at 0.50,
among the seen long arms (0.34 to 0.52), the unseen 0.55 m submachine gun at 0.43, the pistol at
0.20, and a closed umbrella, 0.88 m long, at 0.38. The generalisation that passes this test is
plausibly the one that produces the confusion of Section 9.5. Every rate at which a class is called
armed is lower in the new realisation than on the validation split (armed recall 0.43 against 0.55),
which does not affect the comparison, made within the same images.

### 11.6 Reproducibility, and what a reader cannot check

Every generated image records its seed, illumination regime and camera altitude. The settlement is
reproduced exactly from the seed; the figures in it are not, in the three corpora rendered before
the defect was found (the pilot corpus, the corpus of record and the original 75 m corpus), because
the human generator drew from an unseeded random stream, a defect since closed. The settlement, the
camera and the illumination of every reported image are therefore reproducible by the authors from
what each image records, and the exact placement of figures is reproducible only for corpora
generated after the fix. Camera pitch is recorded per image only in corpora generated after the
generator began recording it; the two nadir corpora of Section 8.2 predate it, which is why their
rows carry the generator setting rather than a per-image value, and the note to that table says so.
The hyperparameter and inference table of Section 7.6 is in the body of the article, rather than in
an appendix, so that every training setting is stated in the article itself, although repeating a
run would also require the corpus, which does not accompany it. Training is deterministic under a
fixed seed, and five models were repeated with two further training seeds (Section 10.6).

Neither the corpora nor the code accompany the article, so a reader cannot check the corpus itself.
What a reader can check is the benchmark, VisDrone, distributed by its own authors, and the
parameters stated in Sections 7.2 to 7.7; every asset the generator draws on is public domain
(Sections 7.2 and 7.4), and the earlier arm behind the 0.116 to 0.561 pair of Section 7.6 draws
building footprints from OpenStreetMap. Exploratory work that preceded this article used a
photogrammetric reconstruction built from imagery that cannot be released; the protocol of Section 5
excludes it, and no measurement reported here derives from it.
