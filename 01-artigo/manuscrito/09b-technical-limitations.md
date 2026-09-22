## 11. Technical Scope, Acquisition Implications, and What Is Not Claimed

This section states the boundary of the technical contribution. It is placed before the
Conclusion because the ethical argument that follows depends on the boundary being explicit, and
because several of the limitations below are properties of the measurement rather than
qualifications added after the fact.

### 11.1 The scale finding is arithmetic, not an established effect

Section 7.6 argues that training scale governs whether a target reaches the network, and supports
the argument by arithmetic: a 4 pixel instance occupies less than one cell of the finest feature
map of a detector whose smallest stride is 8. The empirical pair quoted alongside it, mAP50 moving
from 0.116 to 0.561, comes from two runs of an earlier arm that differ in four further respects,
and it is therefore consistent with the argument rather than evidence for it.

Obtaining the controlled measurement requires one experiment that has not been run: the same
detector, the same initialisation, the same epoch budget and the same corpus, trained once on
downscaled frames and once on native-scale tiles. Until that exists, this article does not report
an isolated effect of training scale, and no figure in it should be cited as one.

### 11.2 The benchmark is not the target domain

VisDrone records dense urban scenes from uncontrolled acquisition. It is the closest publicly
available proxy, and it is not a favela. The morphology this generator reproduces is specifically
that of consolidated self-built settlement on a hillside: shared party walls, alleys under 1.2
metres, upper storeys offset from the floor below.

A transfer figure obtained on VisDrone bounds generalisation to dense aerial urban scenes. It does
not establish performance over Jacarezinho, and no claim of that kind is made anywhere in this
article. Establishing it would require annotated real imagery of the territory itself, which the
ethical protocol of Section 5 forecloses and which this project has deliberately not collected.

A second consequence follows. Section 9.3 reports an oblique arm calibrated to the benchmark, but
the acquisition geometry this work reproduces points straight down. An oblique corpus that transfers better to
VisDrone tells us about VisDrone. It does not recommend an acquisition geometry for the case
study, and Section 11.3 is the only acquisition recommendation this article makes.

### 11.3 The acquisition implication, and the condition under which it is withdrawn

Section 8.3 measures that contrast against local clutter is lowest under hard sun and rain and
highest under overcast, because the background under a hard sun is itself filled with cast shadow
from rooftop objects. If that mechanism holds when a detector is evaluated per regime, the
practical implication is direct and runs against the conventional preference for flying in clear
weather.

The implication is stated conditionally because the evidence is conditional. Eight images per
regime, with between-image dispersion of 0.12 to 0.38, resolves only the gap between the extremes
at roughly one standard deviation and does not resolve the ordering of the four intermediate
regimes at all. Section 10.3 specifies the test. If per-regime detector performance does not order
inversely with raw contrast, this implication is withdrawn and the contrast measurement stands
only as a description of the imagery.

### 11.4 Two tasks share a pipeline and must not be conflated

The model proposed in Section 6 classifies built form. What is implemented and
evaluated in Sections 9 and 10 detects people. They share the generator, the annotation procedure,
the randomisation and the scale analysis; they do not share the object class, and no performance
figure reported here transfers from one to the other.

Person detection was implemented because a public benchmark exists for it and the question at
issue was whether synthesis transfers at all. The morphological task has no equivalent public
benchmark at this ground sampling distance, which is itself a finding worth recording: the
evaluation infrastructure for the task the article actually proposes does not currently exist.

### 11.5 Where the armed and unarmed distinction exists, and where it does not

No accuracy figure for the armed and unarmed distinction is reported at 150 m, the altitude this
article takes as its reference acquisition. The omission is a result, not a gap, and this section states
the conditions that produce it.

At 150 m with the camera pointing straight down, rendered at the 4.88 cm per pixel of the corpus
of record, the median annotated instance measures 17.6 by 17.5
pixels. A firearm subtends a fraction of that and is not resolvable within the region. A detector
trained on such a corpus can still separate the two classes, and that is precisely the problem:
in a corpus where the weapon is always the same asset, in the same pose, at the same contrast,
separability measures the regularity of the asset library rather than a visual property of the
world. An accuracy figure obtained there would be the inferential move this article criticises,
a number produced under controlled synthetic conditions and presented as evidence of a capability
that would be exercised on real people in a real territory.

Two changes make the question empirical rather than foreclosed, and both are reported in Section
9. Halving the altitude to 75 m raises the median instance to 47.6 by 41.7 pixels, a 6.4-fold
increase in area, at which the firearm occupies a region the network can in principle resolve.
And the corpus at that altitude is built to remove the artefact, by the construction specified in
Section 7.4: the weapons are set against elongated objects carried in the same territory, drawn
from the same colour and roughness palette and carried through the same distribution of poses. A
detector that separates the classes on that corpus cannot be doing so by colour, and the rate at
which it calls a broom a rifle is reported in Section 9.5.

The distinction between the two altitudes is the contribution, and it is stated as a condition
rather than a recommendation. The capability is not a fixed property of the method: it appears
and disappears as a function of acquisition parameters that can be measured before any system is
bought or flown. A claim that a system distinguishes an armed from an unarmed person from the air
is, at the altitudes and sensors described here, a claim that can be checked before it is
believed. The 75 m figure itself would be withdrawn under a condition this article states rather
than delegates: if a detector trained on four of the five firearm models fails to hold its recall
on the fifth, then what it separates is the asset library and not the object, and no figure from
that corpus should be read as a capability. That held-out test has not been run: `[X]`.
and nothing in this article recommends acquisition over the case study territory.

### 11.6 Reproducibility, and what a reader cannot check

Every generated image carries its seed, illumination regime and camera altitude in a manifest
entry, and the generator reproduces any image exactly from that entry. Camera pitch is recorded
per image only in corpora generated after the field was added, which is why Section 8.2 reads
pitch from the manifest for one corpus and from the generator setting for the other, and says so
in the table. The hyperparameter
and inference tables in Section 7.6 are in the body of the article for the same reason.

What a reader cannot check from this article is the corpus itself, although the reason is
logistical rather than legal: every corpus behind every number reported here is redistributable by
construction, since all geometry is authored by the generator and all surface materials are public
domain. Earlier branches of this project were built on photogrammetric reconstruction of imagery
that cannot be released, and no measurement reported in this article derives from them.
