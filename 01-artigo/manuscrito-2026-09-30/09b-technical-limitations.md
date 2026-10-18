## 11. Technical Scope, Acquisition Implications, and What Is Not Claimed

This section states the boundary of the technical contribution. It is placed before the Conclusion
because the ethical argument that follows depends on the boundary being explicit, and because
several of the limitations below are properties of the measurement rather than qualifications added
after the fact.

### 11.1 The benchmark is not the target domain

VisDrone records dense urban scenes from uncontrolled acquisition. It is the closest publicly
available proxy, and it is not a favela. The morphology this generator reproduces is specifically
that of consolidated self-built settlement on a hillside: abutting dwellings, alleys mostly under
1.2 m, upper storeys offset from the floor below.

A transfer figure obtained on VisDrone measures generalisation to the dense urban scenes that
benchmark records. It does not establish performance over Jacarezinho, and no claim of that kind is
made anywhere in this article. Establishing it would require annotated real imagery of the territory
itself, which the ethical protocol of Section 5 forecloses and which this project has deliberately
not collected.

A second consequence follows. The oblique arm of Section 9.3 is calibrated to the benchmark, but the
acquisition geometry this work reproduces points straight down. An oblique corpus that transfers
better to VisDrone tells us about VisDrone: it does not recommend an acquisition geometry for the
case study, and the nadir figure, the lower one, is the one that bears on it. The only acquisition
implication this article draws is that of Section 11.2, limited to synthetic imagery and one
detector, and it concerns how to fly, not whether to acquire imagery of the case study territory,
which nothing in this article recommends.

### 11.2 The acquisition implication, and the condition under which it is withdrawn

Section 8.3 measures contrast against local clutter lower under hard sun and rain than under
overcast, and proposes as the mechanism that the background under a hard sun is itself filled with
cast shadow from rooftop objects. A detector evaluated per regime finds hard sun the hardest regime,
as that mechanism predicts, but scores low sun, which also casts sharp shadows, level with overcast,
which the mechanism does not predict (Section 10.3). The practical implication is therefore narrower
than the mechanism: for detecting people over a roofscape of this kind, a covered sky is preferable
to a high sun, provided that the cloud base leaves the flight in visual meteorological conditions.

Which practice this runs against should be stated, because three are easily conflated. It runs
against the specifications of aerial survey photography, which ask for imagery free of cloud and
cloud shadow and set a minimum elevation for the sun. One of them admits a high, thin overcast only
if it reduces neither the light nor the shadows of ground objects, and requires the sun never to be
lower than 30 degrees and ideally between 40 and 60 degrees, because of the intermediate-size
shadows produced (National Geodetic Survey, 2002); another asks for at least 15 degrees and warns
that lower sun angles may produce deep shadows in urban areas (RICS, 2021). Both control shadow
through the elevation of the sun, not by avoiding direct sunlight. Hard sun, drawn here between 46
and 74 degrees (Section 7.5), falls within what they ask for, and over this roofscape the shadow
they tolerate, and in one case seek, is the clutter measured in Section 8.3. Low sun, drawn between
9 and 25 degrees, lies below the minimum of the first specification and partly below that of the
second, so the survey convention selects the weakest of the six regimes and excludes one of the
strongest.

Guidance for mapping with drones is divided, and the division follows the product. For
three-dimensional reconstruction, a recent review of mapping practice finds overcast conditions
preferable because dark shadows are absent, while noting that sunny conditions still give good
results in most studies (Maes, 2025); a photogrammetry software vendor recommends an overcast day
for its diffuse light and advises against direct sunlight because of the harsh shadows it creates
(Pix4D, 2022; Pix4D, n.d.); and a drone survey of an urban area judged overcast preferable for its
elevation models, although only one of its flights was overcast and the effect was much weaker than
that of altitude (Leitão et al., 2016). For orthomosaics, by contrast, the same review recommends
uninterrupted sun, which permits fast shutter speeds and so avoids motion blur (Maes, 2025), and at
least one vendor of drone mapping sensors recommends a solar elevation above 30 degrees (GeoCue,
2025). The empirical record on reconstruction is itself mixed (Dandois et al., 2015; Slade et al.,
2025). The measurement therefore extends to the detection of people a preference that part of this
guidance already states for reconstruction, rather than overturning a settled practice; and it
carries the cost that the other part names, since under a covered sky less light reaches the sensor
and a slower shutter or a higher gain is needed, a trade-off that the per-regime test was not
designed to measure.

Nor is the question one of flight rules. These set minima for visibility and for distance from cloud
(14 C.F.R. § 107.51), define operation within visual line of sight as operation in visual
meteorological conditions (Agência Nacional de Aviação Civil [ANAC], 2026), ask that the weather be
verified as compatible with the manufacturer's manual (European Union Aviation Safety Agency [EASA],
2019), or prohibit operation under precipitation, wind or fog (Departamento de Controle do Espaço
Aéreo [DECEA], 2026). None of them asks for sunshine, and an overcast sky whose base lies well above
the flight is compatible with all of them.

Two qualifications follow. The favourable regime is overcast, not rain, and in Brazil operation
under precipitation is excluded in any case (DECEA, 2026). And operations that answer to events
rather than to a schedule, such as search and rescue, which can occur anywhere and at any time
(Broyles et al., 2022), cannot choose their light; for them the finding bears on the robustness a
detector needs, not on when to fly.

### 11.3 Two tasks share a pipeline and must not be conflated

The model proposed in Section 6 classifies built form. What is implemented in Section 7 and
evaluated in Sections 9 and 10 detects people. They share the generator, the annotation procedure,
the randomisation and the scale analysis; they do not share the object class, and no performance
figure reported here transfers from one to the other.

Person detection was implemented because a public benchmark exists for it and the question at issue
was whether synthesis transfers at all. The morphological task has no equivalent public benchmark at
this ground sampling distance, which is itself a finding worth recording: the evaluation
infrastructure for the morphological task that Section 6 proposes does not currently exist.

### 11.4 Where the armed and unarmed distinction exists, and where it does not

The distinction has been measured at 75 m and at 35 m, on synthetic imagery, and only argued at 150
m, where the one model trained for it did not pass its validity condition (Section 9.5). Where it is
measured it carries the error profile of Section 9.5, which calls about one confusable object in
four armed, and it does not sharpen as the camera descends: with every other setting held, the twin
at 75 m calls 16 per cent of objects armed against 27 at 35 m, and 12.5 against 25 on new frames, a
difference established at the protocol's overlap threshold that shrinks under stricter ones. No
threshold for calling the capability present was fixed in advance. A claim that a system
distinguishes an armed from an unarmed person from the air is, at the altitudes and sensors
described here, a claim that can be checked before it is believed, and nothing in this article
recommends acquisition over the case study territory.

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

### 11.5 Reproducibility, and what a reader cannot check

Every generated image records its seed, illumination regime and camera altitude. The settlement is
reproduced exactly from the seed; the figures in it are not, in the three corpora rendered before
the defect was found (the pilot corpus, the corpus of record and the original 75 m corpus), because
the human generator drew from an unseeded random stream, a defect since closed. The settlement, the
camera and the illumination of every reported image are therefore reproducible by the authors from
what each image records, and the exact placement of figures is reproducible only for corpora
generated after the fix. Camera pitch is recorded per image only in corpora generated after the
generator began recording it; the two nadir corpora of Section 8.2 predate it, which is why their
rows carry the generator setting rather than a per-image value, and the note to that table says so.
Every training setting is stated in Section 7.6, although repeating a run would also require the
corpus, which does not accompany the article. Training is deterministic under a fixed seed, and five
models were repeated with two further training seeds (Section 10.6).

Neither the corpora nor the code accompany the article, so a reader cannot check the corpus itself.
What a reader can check is the benchmark, VisDrone, distributed by its own authors, and the
parameters stated in Sections 7.2 to 7.7; every asset the generator draws on is public domain
(Sections 7.2 and 7.4), and the earlier arm behind the 0.116 to 0.561 pair of Section 7.6 draws
building footprints from OpenStreetMap. Exploratory work that preceded this article used a
photogrammetric reconstruction built from imagery that cannot be released; the protocol of Section 5
excludes it, and no measurement reported here derives from it.
