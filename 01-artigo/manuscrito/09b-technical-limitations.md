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
the survey flight this work reproduces is nadir. An oblique corpus that transfers better to
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

The model proposed in Section 5 and Section 6 classifies built form. What is implemented and
evaluated in Sections 9 and 10 detects people. They share the generator, the annotation procedure,
the randomisation and the scale analysis; they do not share the object class, and no performance
figure reported here transfers from one to the other.

Person detection was implemented because a public benchmark exists for it and the question at
issue was whether synthesis transfers at all. The morphological task has no equivalent public
benchmark at this ground sampling distance, which is itself a finding worth recording: the
evaluation infrastructure for the task the article actually proposes does not currently exist.

### 11.5 What the class distinction is not, and why it is withheld

The synthetic corpus carries two classes, armed and unarmed, inherited from the 2022 project that
originated this line of work. No accuracy figure for that distinction appears anywhere in this
article, and the omission is deliberate rather than pending.

The median annotated instance measures roughly 18.5 by 22.9 pixels at 4K. A firearm is not
resolvable within a region of that size. The distinction is nevertheless learnable in the
synthetic corpus, because the weapon is always the same model, in the same pose, at the same
contrast, which makes separability an artefact of the generator rather than a visual property of
the world. An accuracy figure obtained under those conditions would measure the regularity of our
own asset library.

Reporting it would also be the exact inferential move this article criticises in Section 2: a
number produced under controlled synthetic conditions, presented as evidence of a capability that
would be exercised on real people in a real territory. The measurement is withheld on both
grounds, and the ethical ground is the one that would hold even if the technical ground did not.

### 11.6 Reproducibility, and what a reader cannot check

Every generated image carries its seed, illumination regime and camera altitude in a manifest
entry, and the generator reproduces any image exactly from that entry. Camera pitch is recorded
per image only in corpora generated after the field was added, which is why Section 8.2 reads
pitch from the manifest for one corpus and from the generator setting for the other, and says so
in the table. The hyperparameter
and inference tables in Section 7.6 are in the body of the article for the same reason.

What a reader cannot check from this article is the corpus itself. The procedurally generated arms
are redistributable by construction, since all geometry is authored and all materials are public
domain, but the photogrammetric arms of this project are derived from operational imagery that
cannot be released. Where a measurement in Section 8 uses a photogrammetric arm, the table says
so.
