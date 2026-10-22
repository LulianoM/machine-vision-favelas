# Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Favelas

## Abstract

Claims that aerial machine vision can tell an armed person from an unarmed one are acted on without stating the acquisition conditions that make the distinction visible. No public aerial benchmark annotates carried firearms, so the scale at which they stop reaching a detector is open. On procedural corpora of a dense favela we characterised the target by ground sampling distance (ground width per pixel), camera pitch and illumination. Detectors trained only on them were scored against a ceiling trained on as many real images, on an urban, mostly oblique benchmark and on a nadir one in wilderness; confusion of firearms with ordinary elongated objects was measured synthetically at 150, 75 and 35 m. Straight down from 150 m (4.88 cm per pixel) a person spans 17.6 by 17.5 pixels and a firearm's form is argued to be lost. On the urban benchmark, synthetic-only training reached 2.2 per cent of the ceiling for that acquisition and 15.3 for the best oblique configuration (three-run means); on the nadir one the order reversed, 62.7 against 42.1 per cent. With 5 or 10 per cent of real images, the synthetic corpus lowered accuracy, as pretraining under four fine-tuning schedules and mixed in. At 75 and 35 m detectors called 24 and 27 per cent of ordinary objects armed, finer resolution not reducing it; at 150 m a weaker separation remained, read as a shortcut. Stating the conditions under which a capability has not been shown is a checkable contribution relevant to dual use.

**Keywords:** synthetic data, aerial object detection, ground sampling distance, dual use, informal settlements, favelas

## Introduction

### 1.1 Problem statement

Aerial systems are already flown over policed territory in Rio de Janeiro, where lethal force turns on a single judgement, whether the person engaged was armed (Section 3.3), and it is increasingly proposed that a camera above a city can tell an armed person from an unarmed one. What is rarely stated alongside that premise, and what decides whether the distinction is visible at all, is the acquisition condition; claims that omit it are acted on. That condition has five terms: the altitude of the unmanned aerial vehicle (UAV); its sensor and lens; the ground sampling distance (GSD) that these produce, that is, the width of ground one pixel spans; the camera pitch, whether the camera points straight down (nadir) or obliquely; and the illumination. We treat it as a measurable question, on procedurally generated synthetic corpora of a dense favela.

Urban informal settlements, known in Brazil as favelas, are among the most persistent blind spots of official spatial data infrastructures: dense, vertically expanding, self-built housing defies the methods designed for planned urban grids. The same technology that could support safer emergency response there can be repurposed for surveillance, profiling or the targeting of residents who have not consented to being mapped, a dual-use tension we treat as central.

The vantage point named in the title is not decorative. Three conditions of this study would not arise in a mapped, consented and well-benchmarked city. No consented aerial imagery of the territory exists or can readily be obtained, so every training image is synthetic (Section 4.1). The public benchmarks on which transfer can be measured show either a dense urban scene that is not a favela, mostly from an oblique camera, or people in wilderness seen from directly above (Section 6.5). Nor does any public test set exist for what distinguishes this territory, the vertical morphology of the settlement and what a person carries, at the GSD of a survey flight (Sections 2.3 and 6.6). Working from the Global South means working under those three absences.

### 1.2 Research gap

Closest to this problem, UAV research plans trajectories and patrols (Section 2.1). Route planning models three-dimensional obstacles, whereas aerial policing reduces the city to planar formulations whose spatial unit is the street, inherited from ground-based policing, not the airspace volume. The same inheritance reappears at the level of perception, in the assumption that an aerial view of a person is a view of a standing figure (Section 5.1).

A vertically built favela is not a special case of mountainous terrain. A hillside covered in vegetation and a favela built on that same hillside do not constitute the same problem, either computationally or operationally: stacked construction, narrow alleys and occlusion between structures co-occur there (Section 3.2), and what is observable from above corresponds imperfectly to what matters at street level. Of the progression from flat urban terrain, to mountainous terrain, to formal three-dimensional urban space, to vertically complex informal urban space, the fourth category remains underdeveloped.

UAV research on informal settlements exists, but for mapping, reconstruction and building classification rather than security (Section 2.1). The two literatures, one on surveillance and patrol over formally mapped space and one on mapping informal space, rarely meet, and their intersection is the gap this research addresses.

Section 2 reviews both literatures and the evidence on synthetic training for aerial detection, which transfers but, for small aerial targets, recovers only a fraction of what real data achieves. What that evidence does not establish, the scale at which what a person carries stops reaching a detector, is the empirical subject of this article.

### 1.3 Objective and research questions

Our objective is to establish the acquisition conditions (altitude, sensor, camera geometry and illumination) under which a person observed from the air can be distinguished as armed or unarmed, and to measure what a detector trained on synthetic imagery alone recovers of the detection of the person, on which that distinction rests. Jacarezinho, in Rio de Janeiro, is the site whose vertical complexity motivates the choice and whose general morphology, though not its geometry, the synthetic settlements approximate (Section 3.2).

Three research questions follow; Section 4.6 defines the experiments, A to D, that answer them.

**RQ1.** How much of the person-detection accuracy obtained with real training images does a detector trained only on synthetic imagery of a dense settlement recover on public real aerial benchmarks, and which parameters of acquisition and scene (camera pitch, apparent target size, settlement variety) determine that fraction? Experiment A answers it; Experiment D adds, on synthetic frames only, how detection varies with illumination.

**RQ2.** Once a small number of real training images is available, 5 or 10 per cent of the benchmark's training split, does the synthetic corpus add accuracy, used as pretraining or mixed into the training set? Experiment B answers it.

**RQ3.** On synthetic imagery alone, at which GSDs (4.88, 2.44 and 1.14 cm per pixel from a nadir camera, which the reference camera reaches at 150, 75 and 35 m) can a detector separate a person carrying a firearm from one carrying an ordinary elongated object, and at what rate does it call the latter armed? Experiment C answers it.

The armed and unarmed distinction was studied on synthetic imagery only, because no public aerial benchmark annotates a carried firearm at these GSDs, and the transfer measured under RQ1 and RQ2 is that of person detection. The classification of the settlement's built form, which the site invites, has no evaluation set; Section 6.6 states it as future work.

### 1.4 Contributions and organisation of the paper

The article makes five contributions. First, a characterisation of the aerial target by GSD, camera pitch and illumination that depends on no detector. Second, transfer fractions for person detection against a ceiling trained on a matched number of real images, nadir against oblique and one settlement against six, on an urban benchmark seen mostly obliquely and on a nadir one, where the order of the two geometries reverses. Third, the finding that on the urban benchmark the synthetic corpus lowered accuracy once 5 or 10 per cent of real images existed, as pretraining under four fine-tuning schedules and mixed in. Fourth, a synthetic measurement of the confusion between firearms and ordinary elongated objects at the GSDs of 75 and 35 m, replicated on new frames and across training runs, and at the GSD of 150 m a weaker separation which, since a firearm's form is argued to be lost there, is read as a shortcut rather than as a capability. Fifth, the position that a statement of the conditions under which a capability has not been shown is a checkable contribution, of the same kind as demonstrating one, and the one that bears on dual use.

Section 2 reviews the related work, Section 3 presents the study context, Section 4 describes the materials and methods, including the four experiments and the criteria fixed before each was run, and Section 5 reports the target characterisation and then one experiment per subsection. Section 6 discusses the results against the literature and states the implications, the limitations and the future work in one place, and Section 7 answers the three questions.
