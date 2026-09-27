# Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Self-Built Settlements

## Abstract

Claims that aerial machine vision can tell an armed person from an unarmed one are acted on
without stating the acquisition conditions under which the distinction is visible at all. This
article treats that as the measurable question it is, using a procedurally generated synthetic
corpus of a dense self-built settlement.

Ground sampling distance, the ground area a single pixel covers, not scene realism, fixes the target. At 4.88 cm per pixel, the ground sampling distance of the corpus of record, with the camera
pointing straight down at 150 m, a person occupies 17.6 by 17.5
pixels and a firearm is not resolvable within that region. Halving the altitude enlarges the
median box of a figure more than five-fold, and the question becomes empirical rather than foreclosed.

The corpus is built to defeat the objection that separability in synthetic imagery is an artefact
of an invariant asset: five firearm models are set against nine elongated objects carried in the
same territory, brooms, rebar, pipe, umbrellas, drawn from the same colour and roughness palette,
so that colour alone cannot separate the classes. False positives on those hard negatives
are reported against altitude.

Transfer to real aerial imagery, a public urban benchmark that is not a favela, is reported as a ratio to what a detector trained on real data
achieves on the same test set: 1.6 per cent for the nadir acquisition taken as reference,
9.7 per cent when the same settlement is rendered from an oblique camera, and 16.7 per cent for
the best oblique configuration, six settlements at a pitch recalibrated to the benchmark. Given 5 or 10 per cent of the benchmark's real training
images, a generic initialisation outperformed the synthetic one, in one training run per model. No armed and unarmed accuracy is
reported at 150 m: at that ground sampling distance a carried object reaches the image as a thin
line whose form cannot be resolved, an absence argued from resolution rather than measured, and a
figure obtained there could not be told apart from the regularity of our asset library. Stating the conditions
under which a capability is absent is a contribution of the same kind as demonstrating one that
is present.

**Keywords:** synthetic data, aerial object detection, ground sampling distance, dual use,
informal settlements

## Introduction

Aerial systems are already being bought and flown on the premise that a camera above a city can tell an armed person from an unarmed one. What is rarely stated alongside that premise is the altitude and the sensor at which the distinction is visible at all. Answering that requires a reading of policed urban space that the aerial literature has largely not offered, and the reason it has not is the subject of what follows.

The UAV literature closest to this problem is organised around trajectory planning and policing. The first strand takes three-dimensional complexity seriously: route planning over terrain with peaks and no-fly zones (Rasoulie & Pashazadeh, 2026), through gridded urban space with high-rise obstacles (Xu, 2025), and along urban canyons by optical flow (Agrawal, Ratnoo, & Ghose, 2017), with GNSS degradation in exactly those canyons documented as a reason to fuse visual sensing (Jiang et al., 2026). When the literature turns to aerial policing, however, that complexity dissolves into planar formulations: multi-target search as a travelling-salesman variant with no treatment of altitude or vertical obstacles (Wang & Qian, 2026), patrol as optimisation over a street network (Chen, Liu, Hu, Zhang, & Pan, 2025), and routing over patrol points to maximise coverage (Yan, Hsieh, & Lai, 2025). The spatial unit is the street, inherited from ground-based policing, not the airspace volume. The same planar inheritance reappears one level down, at the level of perception, in the assumption that an aerial view of a person is a view of a standing figure. Section 8.2 measures what nadir acquisition does to that assumption.

This persistent horizontality is not merely a modeling convenience; it reveals a structural blind spot in how the field conceptualizes policed urban space, one that becomes especially consequential when the terrain itself resists a two-dimensional reading. Urban informal settlements, commonly referred to in Brazil as *favelas*, represent one of the most persistent blind spots in official spatial data infrastructures. In cities such as Rio de Janeiro, *favelas* are frequently characterized by dense, vertically expanding, self-built housing that defies the conventional cartographic and remote-sensing methods designed for planned urban grids. This spatial informality has direct consequences for public administration, urban planning, and emergency response, and, more controversially, for public-security operations, which routinely take place in these territories with limited advance knowledge of their built environment.

It is worth stressing that a vertically built *favela* is not simply a special case of mountainous terrain, and treating it as such risks eliding the specific computational and operational challenge it poses. A hillside covered in vegetation and a favela built on that same hillside do not constitute the same problem, either computationally or operationally. In a Rio de Janeiro favela, several sources of complexity co-occur: steep slopes; overlapping and vertically stacked construction; narrow alleyways; rooftop slabs (*lajes*) that are themselves informally occupied or extended; irregular stairways; buildings with no standardized geometry; access routes that are absent or poorly represented in official maps; obstacles both above and below the UAV's flight path; abrupt changes in local elevation over very short horizontal distances; visual occlusion between structures; degradation of GNSS/GPS signals; the operational need to maintain line of sight; moving pedestrians and other dynamic obstacles at street level; and, critically, an imperfect correspondence between what is observable from above and what is operationally relevant at the level of human circulation on the ground.

This distinction suggests a conceptual progression that the current literature has only partially traced: from (1) flat urban terrain, to (2) mountainous terrain, to (3) formal three-dimensional urban space, and finally to (4) vertically complex informal urban space. The fourth category remains markedly underdeveloped. UAV research on informal settlements does exist, but it is concentrated almost entirely in mapping, urban planning, and remote sensing, rather than in operational or security-oriented applications. The exceptions are instructive and are reviewed in Section 2: Gevaert, Persello, Sliuzas, and Vosselman (2016) in Kigali, Sithole and Mhangara (2025) in Johannesburg, and the mapping literature surveyed by da Silva, Kormann da Silva, and Westerholt (2024), all oriented to planning rather than to security. Taken together, this reveals two bodies of literature that rarely intersect. The first, UAV research in policing and defense contexts, which is organized around surveillance, reconnaissance, patrol, target tracking, situational awareness, and path planning, largely within formally mapped or geometrically regular urban space. The second, UAV research on informal settlements, that is organized around mapping, photogrammetry, remote sensing, three-dimensional reconstruction, urban planning, and building classification, largely divorced from operational security concerns. The intersection of these two literatures constitutes the gap this research addresses.

This article accordingly poses the following research question: **Under what acquisition conditions, and at what cost in transfer, does synthetic imagery of a dense self-built settlement support the aerial detection of an armed person?**

Our objective, correspondingly, is to establish the acquisition conditions (altitude, sensor, camera geometry, and illumination) under which a person observed from the air can be distinguished as armed or unarmed, and to measure what a detector trained on synthetic imagery alone recovers of that capability, using Jacarezinho, in Rio de Janeiro, as the morphology the synthetic corpus reproduces and as the site whose vertical complexity motivates the choice.

Two object classes are in play, and they should be separated at the outset. The vertical morphology of the settlement is what the model proposed in Section 6 is designed to classify, and it is the reason this site was chosen. The instrument evaluated in Sections 7 to 11 detects people and, at 75 and 35 m, the two lower of its three altitudes, armed people. Only the second has a public benchmark against which transfer can be measured, for people though not for the armed class, which is why it, and not the first, carries the empirical claims of this article.

This research is relevant to society and to urban studies because favelas remain systematically underrepresented in official geospatial datasets, which constrains equitable resource allocation for sanitation, risk mapping, and disaster response. It is also relevant to police institutions, because operations in vertically dense, informally built territories are widely documented as high-risk for all parties (officers, criminal actors, and, overwhelmingly, uninvolved residents), partly due to poor advance knowledge of the built environment. Finally, it is relevant to communities themselves, because the same technology that could, in principle, support safer emergency response or infrastructure planning also carries a serious risk of being repurposed for surveillance, profiling, or the operational targeting of residents who have not consented to being mapped. This dual-use tension is treated as a central, rather than peripheral, concern of this research.

The vantage point named in the title is not decorative. Three of the conditions this study works under would not arise in a study of the same problem in a mapped, consented and well-benchmarked city: there is no public benchmark for the morphological task at this scale (Section 11.4), the benchmark that does exist is an urban scene that is not a favela (Section 11.2), and no consented aerial imagery of the territory exists or can readily be obtained (Section 7.1). Working from the Global South here means working under those three absences, and much of what follows is an account of what they cost.
