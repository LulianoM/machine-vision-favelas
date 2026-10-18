<!-- Manuscrito completo na ordem de leitura do PDF de 30/09/2026, com os numeros de secao que o montador atribui. Gerado em 17/10/2026 para a revisao; nao editar. -->

<!-- ARQUIVO DE ORIGEM: 01-introduction.md -->

# Machine Vision from the Global South: Synthetic Data and the Acquisition Limits of Armed-Person Detection in Dense Favelas

## Abstract

Claims that aerial machine vision can tell an armed person from an unarmed one are acted on without
stating the acquisition conditions under which the distinction is visible at all. This article
treats that as a measurable question, using procedurally generated synthetic corpora of a dense
favela.

Ground sampling distance, the width of ground one pixel spans, fixes the target. At 4.88 cm per
pixel, with the camera pointing straight down at 150 m, a person occupies 17.6 by 17.5 pixels,
within which the form of a firearm is argued not to be resolvable; the one detector trained to
separate the classes at that altitude found fewer than half of the figures and did not pass the
validity condition fixed before it was run, so the absence there remains argued rather than
measured. At 75 and 35 m the question becomes empirical. A corpus built to defeat the objection that
separability in synthetic imagery is an artefact of an invariant asset, five firearm models set
against nine elongated objects carried in the same territory, gives a detector that calls 24 per
cent of those objects armed at 75 m and 27 per cent at 35 m, against 16 per cent for a twin of the
35 m corpus rendered at 75 m; on 80 new frames the gap replicates, 25 against 12.5 per cent, and
holds across three training runs. Finer resolution did not reduce the confusion.

Transfer of person detection to a public real benchmark that is not a favela reaches 1.6 per cent of
a ceiling trained on a matched number of real images for the nadir acquisition taken as reference,
9.7 per cent when the same settlement is rendered from an oblique camera, and 15.3 per cent on
average over three training runs for the best oblique configuration. Given 5 or 10 per cent of the
benchmark's real training images, a generic initialisation outperformed the synthetic one, and
adding the synthetic corpus to the same real images lowered accuracy as well. Stating the conditions
under which a capability has not been shown, and what showing it would require, is a contribution of
the same kind as demonstrating one that is present.

**Keywords:** synthetic data, aerial object detection, ground sampling distance, dual use, informal settlements, favelas

## 1. Introduction

Aerial systems are already flown over policed territory in Rio de Janeiro (Section 3), and it is increasingly proposed that a camera above a city can tell an armed person from an unarmed one. What is rarely stated alongside that premise is the altitude and the sensor at which the distinction is visible at all. Answering that requires a reading of policed urban space that the aerial literature has largely not offered, and the reason it has not is the subject of what follows.

The UAV literature closest to this problem is organised around trajectory planning and policing. The first strand takes three-dimensional complexity seriously: route planning over terrain with peaks and no-fly zones (Rasoulie & Pashazadeh, 2026), through gridded urban space with high-rise obstacles (Xu, 2025), and along urban canyons by optical flow (Agrawal, Ratnoo, & Ghose, 2017), with GNSS degradation in exactly those canyons documented as a reason to fuse visual sensing (Jiang et al., 2026). When the literature turns to aerial policing, however, that complexity dissolves into planar formulations: multi-target search as a travelling-salesman variant with no treatment of altitude or vertical obstacles (Wang & Qian, 2026), patrol as optimisation over a street network (Chen, Liu, Hu, Zhang, & Pan, 2025), and routing over patrol points to maximise coverage (Yan, Hsieh, & Lai, 2025). The spatial unit is the street, inherited from ground-based policing, not the airspace volume. The same planar inheritance reappears one level down, at the level of perception, in the assumption that an aerial view of a person is a view of a standing figure. Section 8.2 measures what nadir acquisition does to that assumption.

This persistent horizontality is not merely a modeling convenience; it reveals a structural blind spot in how the field conceptualizes policed urban space, one that becomes especially consequential when the terrain itself resists a two-dimensional reading. Urban informal settlements, commonly referred to in Brazil as *favelas*, represent one of the most persistent blind spots in official spatial data infrastructures. In cities such as Rio de Janeiro, *favelas* are frequently characterized by dense, vertically expanding, self-built housing that defies the conventional cartographic and remote-sensing methods designed for planned urban grids. This spatial informality has direct consequences for public administration, urban planning, and emergency response, and, more controversially, for public-security operations, which routinely take place in these territories with limited advance knowledge of their built environment.

It is worth stressing that a vertically built *favela* is not simply a special case of mountainous terrain, and treating it as such risks eliding the specific computational and operational challenge it poses. A hillside covered in vegetation and a favela built on that same hillside do not constitute the same problem, either computationally or operationally. In a Rio de Janeiro favela, several sources of complexity co-occur: steep slopes; overlapping and vertically stacked construction; narrow alleyways; rooftop slabs (*lajes*) that are themselves informally occupied or extended; irregular stairways; buildings with no standardized geometry; access routes that are absent or poorly represented in official maps; obstacles both above and below the UAV's flight path; abrupt changes in local elevation over very short horizontal distances; visual occlusion between structures; degradation of GNSS/GPS signals; the operational need to maintain line of sight; moving pedestrians and other dynamic obstacles at street level; and, critically, an imperfect correspondence between what is observable from above and what is operationally relevant at the level of human circulation on the ground.

This distinction suggests a conceptual progression that the current literature has only partially traced: from (1) flat urban terrain, to (2) mountainous terrain, to (3) formal three-dimensional urban space, and finally to (4) vertically complex informal urban space. The fourth category remains markedly underdeveloped. UAV research on informal settlements does exist, but it is concentrated almost entirely in mapping, urban planning, and remote sensing, rather than in operational or security-oriented applications. The studies that do exist are instructive and are reviewed in Section 2: Gevaert, Persello, Sliuzas, and Vosselman (2016) in Kigali, Sithole and Mhangara (2025) in Johannesburg, and the mapping literature surveyed by da Silva, Kormann da Silva, and Westerholt (2024), all oriented to planning rather than to security. Taken together, this reveals two bodies of literature that rarely intersect. The first, UAV research in policing and defense contexts, is organized around surveillance, reconnaissance, patrol, target tracking, situational awareness, and path planning, largely within formally mapped or geometrically regular urban space. The second, UAV research on informal settlements, is organized around mapping, photogrammetry, remote sensing, three-dimensional reconstruction, urban planning, and building classification, largely divorced from operational security concerns. The intersection of these two literatures constitutes the gap this research addresses.

This article accordingly poses the following research question: **Under what acquisition conditions, and at what cost in transfer, does synthetic imagery of a dense favela support the aerial detection of an armed person?**

Our objective, correspondingly, is to establish the acquisition conditions (altitude, sensor, camera geometry, and illumination) under which a person observed from the air can be distinguished as armed or unarmed, and to measure what a detector trained on synthetic imagery alone recovers of that capability, using Jacarezinho, in Rio de Janeiro, as the site whose vertical complexity motivates the choice and whose general morphology, though not its geometry, the synthetic settlements approximate.

Two tasks are in play, and they should be separated at the outset. The vertical morphology of the settlement is what the model proposed in Section 6 is designed to classify, and it is the reason this site was chosen. The instrument evaluated in Sections 7 to 11 detects people and, at 75 and 35 m, the two lower of its three altitudes, armed people. Only the second has a public benchmark against which transfer can be measured, and only for people: we found no public aerial benchmark for the armed class. That is why it, and not the first, carries the empirical claims of this article.

This research is relevant to society and to urban studies because favelas remain systematically underrepresented in official geospatial datasets, which constrains equitable resource allocation for sanitation, risk mapping, and disaster response. It is also relevant to police institutions, because operations in vertically dense, informally built territories are widely documented as high-risk for all parties (officers, criminal actors, and, overwhelmingly, uninvolved residents), partly due to poor advance knowledge of the built environment. Finally, it is relevant to communities themselves, because the same technology that could, in principle, support safer emergency response or infrastructure planning also carries a serious risk of being repurposed for surveillance, profiling, or the operational targeting of residents who have not consented to being mapped. This dual-use tension is treated as a central, rather than peripheral, concern of this research.

The vantage point named in the title is not decorative. Three of the conditions this study works under would not arise in a study of the same problem in a mapped, consented and well-benchmarked city: there is no public benchmark for the morphological task at this scale (Section 11.3), the benchmark that does exist is an urban scene that is not a favela (Section 11.1), and no consented aerial imagery of the territory exists or can readily be obtained (Section 7.1). Working from the Global South here means working under those three absences, and much of what follows is an account of what they cost.


<!-- ARQUIVO DE ORIGEM: 02-literature-review.md -->

## 2. Literature Review

### Machine Vision and Informal Urban Environments

Machine vision applied to informal settlements has grown as a research niche at the intersection of remote sensing, computer vision, and urban studies. Several strands of recent literature ground this study.

In fact, a substantial body of work has used convolutional neural networks (CNNs) and related architectures to detect informal settlements from very-high-resolution (VHR) and low-resolution multispectral imagery, motivated by the high cost of VHR data and the frequent absence of reliable ground-truth annotations. Gram-Hansen et al. (2019) proposed a semi-automated pipeline combining domain knowledge (e.g., known roofing materials) with machine learning classifiers to convert satellite imagery into binary informal-settlement maps, explicitly addressing the challenge of poor and inconsistent official records in developing-country contexts. More recent work has extended these pipelines toward multiscale and multimodal fusion: Du, Xing, Wang, Wei, and Zhang (2024) proposed a scene-classification-assisted, texture-feature-enhanced multiscale network for large-scale informal-settlement extraction from remote sensing imagery, while Hu, Huang, Ren, and Zhang (2025) went a step further by fusing satellite imagery with street-view data in a cross-scale hierarchical perception network, explicitly aiming to recover the fine-grained structural detail that overhead imagery alone cannot capture. A parallel line of work has turned to UAV-derived imagery specifically: Sithole and Mhangara (2025) used high-resolution drone imagery and object-based machine learning to classify the Slovo Park informal settlement in Johannesburg, South Africa, resolving structural patterns at a spatial resolution unattainable from satellite platforms, an approach directly relevant to resolving vertical structure, even though its object of classification remained the building footprint rather than its vertical extension.

**The vertical dimension as an under-addressed problem.** Much of the informal-settlement detection literature reviewed above treats settlements as two-dimensional footprints, optimized for horizontal delimitation rather than vertical stratification. This is a significant theoretical gap for contexts like Rio's favelas, where informal vertical growth (additional floors, rooftop units) is a defining and rapidly changing structural feature, with direct implications for population density estimation, structural risk, and tactical navigability, none of which is captured by planar classification alone. As early as 2016, Gevaert, Persello, Sliuzas, and Vosselman had already shown, in a study of an unplanned settlement in Kigali, Rwanda, that dense buildings and steeply sloped terrain jointly (rather than separately) challenge state-of-the-art classification algorithms, and that integrating 2D radiometric, 2.5D topographic, and 3D geometric features extracted from UAV imagery improves classification accuracy in such conditions. Nearly a decade later, this concern with the vertical dimension has resurfaced in higher-impact venues focused on the Global South more broadly: Watson and Elliott (2025), writing in Scientific Reports, used high-resolution digital elevation models and deep-learning-based height prediction to reconstruct the vertical component of three cities (Nairobi, Kathmandu, and Quito), explicitly noting that Nairobi's Mukuru informal settlement is omitted from one of the open building-footprint datasets they compared and only partially mapped in OpenStreetMap, and arguing that building-scale height estimates open new possibilities for estimating population distribution and exposure to natural hazards. Taken together, these two studies (nine years apart) suggest that the vertical dimension of informality has been intermittently acknowledged as important, but has not yet been systematically integrated into either the informal-settlement detection literature or the UAV trajectory-planning literature discussed earlier.

**Synthetic data and the sim-to-real gap.** Because labeled, consented, high-resolution imagery of vertical informal structures is scarce, this study draws on the domain randomization literature developed by Tobin, Fong, Ray, Schneider, Zaremba, and Abbeel (2017) and subsequently extended through structured domain randomization (Prakash et al., 2019), which uses real-world spatial priors to constrain the placement of synthetic elements and produce more contextually plausible (if not photorealistic) training scenes. More recent, domain-specific evidence indicates that this approach transfers well to aerial and UAV-centered perception tasks. Barisic, Petric, and Bogdan (2022), publishing in IEEE Robotics and Automation Letters, rendered a synthetic aerial dataset in Blender with randomized object textures and reported mean-average-precision gains for detectors of UAVs, evaluated on two real test sets of UAV-to-UAV imagery; the conditions targeted were challenging illumination and objects that occupy a small part of the frame. In a related vein, though for industrial objects in a robotic setting rather than for aerial imagery, Horváth, Erdős, Istenes, Horváth, and Földi (2023), in IEEE Transactions on Robotics, trained a YOLOv4 detector on domain-randomized synthetic images and reported mAP50 of 86.32% in zero-shot and 97.38% in one-shot transfer, measured on 190 manually annotated real images. Together, this body of work reports that domain-randomized synthetic training (especially when combined with a modest volume of real fine-tuning data) can substantially close the sim-to-real performance gap for object detection tasks in complex, cluttered environments, a claim this article tests for aerial person detection and does not reproduce: on a public benchmark, neither pretraining on synthetic imagery nor mixing it with real images improved on a generic initialization given the same real images (Section 9.4). The reported benefit is conditional rather than general. Gains from synthetic pretraining have often been measured against ImageNet or random initialization rather than against a detector already trained on real images of the target class (McCormac et al., 2017; Tremblay et al., 2018; Lima et al., 2025). In aerial person detection, both pretraining on some synthetic corpora and mixing synthetic with real images have scored below training on the real images alone (Shen et al., 2023a, 2023b; Yim et al., 2026; Martinez-Esteso et al., 2025). This literature directly informs the synthetic-training strategy proposed in Section 6, since it offers a technically credible route to training a model without requiring extensive, consent-fraught real-world image collection inside an active informal settlement.

**Positioning this study.** Taken together, this literature suggests both a technical opportunity and an unresolved theoretical gap. On one hand, mature synthetic-training methods (Tobin et al., 2017; Prakash et al., 2019; Barisic et al., 2022; Horváth et al., 2023) could substantially reduce reliance on invasive, real-world data collection inside informal settlements, although for aerial person detection Section 9.4 finds that it did not substitute for real images. On the other hand, the vertical dimension of informality remains theoretically under-integrated (Gevaert et al., 2016; Watson & Elliott, 2025), and nearly all prior applications of machine vision to informal settlements have been framed around planning, humanitarian, or development purposes rather than security operations, a pattern also visible in the broader literature on digital mapping and community participation in informal areas (da Silva, Kormann da Silva, & Westerholt, 2024). These are the two bodies of literature the Introduction identified as rarely intersecting. This study's contribution, and its central point of critical reflection, is to examine what changes (technically, ethically, and socially) when a comparable machine vision approach is designed with an explicit public-security end use in mind, at the intersection of these two literatures.


**Aerial person detection and the resolution limit.** The evidence above concerns objects that occupy
a substantial share of the frame. The task this article evaluates does not. Kiefer, Ott and Zell
(2022) trained three detectors purely on synthetic data and evaluated them on VisDrone (Zhu et al., 2022), the
standard public benchmark for aerial detection in dense urban scenes, reporting mAP50 of 1.2, 2.4
and 10.2 against 24.6, 48.6 and 43.9 for the same architectures trained on real imagery. In a
top-down view of a crowded street, purely synthetic training recovers a fraction of what real data
achieves. Liao et al. (2026) identify where that fraction is won or lost: in an aerial synthetic
corpus built from photogrammetry they ablate two factors, and replacing a photogrammetric
reconstruction of the target site with generic assets costs 27.0 mAP50 points on YOLOv11, while removing variation in sun position, weather and viewing angle costs 30.4 on the same detector, and averaged over their detectors that second penalty is largest on truncated objects. Two operative variables follow, and neither is scene realism
in the usual sense: the ground sampling distance at which the target reaches the network, and the
provenance of the scene geometry. These two variables also qualify the transfer figures above, which were obtained on large objects in a controlled scene rather than on a person seen from 150 m.

Taken together, the literature reviewed here establishes two things and leaves two others untouched. It establishes that domain-randomized
synthesis can transfer to aerial detection tasks, though for small aerial targets it recovers only
a fraction of what real data achieves (Kiefer, Ott and Zell, 2022), and that the vertical dimension
of informality has been repeatedly recognized without being integrated. What it does not establish
is the scale at which what a person carries stops reaching a detector, or what follows when a machine vision system built for mapping is pointed at a territory under
armed policing. The first is the empirical subject of Sections 7 to 11; the second is the ethical
argument this article treats as inseparable from it.


<!-- ARQUIVO DE ORIGEM: 04-situating-the-study.md -->

## 3. Situating the Study: Violence, Policing, and Territorial Control in Rio de Janeiro



Rio de Janeiro presents a paradoxical security landscape. Homicide figures have fallen substantially since the mid-1990s. In the state series of the Instituto de Segurança Pública do Rio de Janeiro (ISP-RJ), which begins in 1991, the intentional homicide rate was highest in 1994, at 63.13 per 100,000 inhabitants (ISP-RJ, n.d.-a); the Fórum Brasileiro de Segurança Pública puts it at 17.1 per 100,000 in 2024, 10.8% below 2023 (Fórum Brasileiro de Segurança Pública, 2025, Table 3), and at 17.1 again in 2025 (Fórum Brasileiro de Segurança Pública, 2026, Table 3). In the city of Rio de Janeiro, ISP-RJ records by police district show intentional homicides falling from 2,574 in 2003, the first year of that series, to 965 in 2025, a figure that from 2024 excludes femicides, which the series records separately (ISP-RJ, n.d.-b). This decline, however, coexists with a persistently high (and in 2025, rising) rate of lethal police intervention. The Fórum Brasileiro de Segurança Pública's 20th Anuário Brasileiro de Segurança Pública recorded 798 deaths from police intervention in Rio de Janeiro state in 2025, up from 703 the year before (Fórum Brasileiro de Segurança Pública, 2026, Table 8). Against a national fall from 144 to 139, the number of police officers killed in the state rose from 28 to 51, an increase of 82.1%, so that Rio de Janeiro accounted for 51 of the 139 police deaths recorded in Brazil (Barros, 2026; Fórum Brasileiro de Segurança Pública, 2026, Table 6).

By 2025, police-caused deaths accounted for 20.5% of all intentional violent deaths in the state, placing Rio among the small group of Brazilian states with the highest documented ratio of lethal force to overall violent mortality (Fórum Brasileiro de Segurança Pública, 2026; Sousa, 2026). This dual trajectory (declining civilian homicide alongside sustained or increasing police lethality) is central to understanding why the technical and ethical questions this study raises cannot be separated from the operational environment in which any deployment would occur.

Large-scale police incursions into favelas controlled by criminal organizations have long been a recurring feature of public security policy in Rio de Janeiro, and their human cost has repeatedly drawn national and international scrutiny. On May 6, 2021, civil police carried out Operação Exceptis in the Jacarezinho favela, deploying roughly 200 to 250 officers, armored vehicles, helicopters, and a sniper in what was, at the time, the deadliest single police operation in the city's history: 27 civilians and one officer were killed (Human Rights Watch, 2021; Sullivan et al., 2021). Independent witnesses and human-rights organizations, including Human Rights Watch and Amnesty International, raised concerns that some of the dead had been executed rather than killed in exchanges of fire, and that all victims taken to hospital had already arrived dead (Al Jazeera, 2021; Human Rights Watch, 2021).

That record was surpassed four years later. On October 28, 2025, a joint operation of the civil and military police (Operação Contenção) was launched against the Comando Vermelho in the Complexo do Alemão and the Complexo da Penha, which together comprise 26 communities. It mobilized about 2,500 officers, 32 armored vehicles, 12 demolition vehicles and two helicopters (Couto, 2025; Fichino, 2025). Its judicial basis, according to the state's report to the Supreme Federal Court, was 51 arrest warrants issued by the 42nd Criminal Court of the capital, within a total of 100 that the state said it sought to serve (Fichino, 2025). The official count, updated by the Civil Police on October 30, 2025, was 121 dead: 117 civilians and four police officers (Couto & Figueiredo, 2025; Fichino, 2025). It rose to 122 when a fifth officer wounded in the operation died in November (Fórum Brasileiro de Segurança Pública, 2026; Reuters, 2025). On October 29 the Public Defender's Office of the State of Rio de Janeiro had counted 132 dead, 128 civilians and four officers (Falcão & Couto, 2025), the figure in the title of Sullivan and da Cruz (2025). By either count it was the deadliest police operation on record in Brazil (Fichino, 2025; Fórum Brasileiro de Segurança Pública, 2026). Brazilian President Luiz Inácio Lula da Silva described the outcome as "a massacre" and called for an independent investigation (CBS News, 2025), while the United Nations expressed "grave concern" over what it termed the deadliest police operation in the country's history (OPEB, 2025). Notably for the present study, the operation also marked a documented escalation in the technological means used by criminal organizations to counter police incursions: Comando Vermelho fighters used consumer drones to drop improvised explosives on police units during the confrontation, a tactic corroborated by multiple independent outlets and subsequently described by security analysts as an emerging regional pattern of drone use by organized crime in Latin America (CNN, 2026; Sullivan & da Cruz, 2025). In direct response, Rio's Civil Police has since expanded its own Coordenadoria de Operações com Aeronaves Não Tripuladas (COANT), incorporating UAVs into intelligence gathering and real-time operational monitoring (CNN, 2026), a development that situates the present study's technical proposal within an active, rapidly evolving, and already contested operational reality rather than a purely hypothetical one.

These episodes are not aberrations but recurring features of a policy model that has been subject to sustained judicial intervention. In 2019, the Brazilian Socialist Party, together with civil society organizations, filed Arguição de Descumprimento de Preceito Fundamental (ADPF) 635 (popularly known as the "ADPF das Favelas") before the Supreme Federal Court (STF), seeking to curb the high number of civilian deaths resulting from police operations in Rio's favelas. In June 2020, Justice Edson Fachin, as rapporteur, issued a preliminary injunction restricting incursions during the COVID-19 pandemic and requiring that high-risk operations be conducted only in "absolutely exceptional" circumstances, with prior notice to the Public Prosecutor's Office (Agência Brasil, 2025; Movisafe América Latina, 2025). The case remained under the Court's supervision for nearly six years, during which the state was required to report disaggregated lethality data and to equip officers and vehicles with body cameras and geolocation systems. On April 3, 2025, the STF concluded its judgment, partially validating a state-presented plan to reduce police lethality while simultaneously reversing several of the operational restrictions imposed since 2020, mandating expanded Federal Police involvement in cases with interstate implications, and requiring the state to draft a plan for the territorial reoccupation of areas controlled by criminal organizations (Gazeta do Povo, 2025; STF, 2025a, 2025b). Assessments of the ruling's practical effect diverge sharply: legal analysts noted that lethality had already fallen by more than 60% between 2019 (1,814 deaths) and 2024 (699 deaths) under the Court's earlier restrictions (JOTA, 2025), whereas critics on both ends of the political spectrum characterized the final decision as either insufficiently protective of favela residents or as an unwarranted judicial intrusion into operational policing (Causa Operária, 2025; Gazeta do Povo, 2025). The 2024 figure of 699 differs from the 703 reported above by the Fórum Brasileiro de Segurança Pública (2026); the source of the difference is not documented, and the discrepancy is itself an instance of the difficulty official statistical infrastructures have in this domain. Operação Contenção, occurring less than seven months after this ruling, has since become a central data point in the ongoing debate over whether the ADPF 635 framework meaningfully constrains lethal police conduct in practice (Agência Pública, 2025).

Structurally, these outcomes reflect difficulties that predate any single operation or judicial ruling. Rio's security forces operate against criminal organizations that maintain durable, often decades-long territorial control over specific favelas, financed largely through drug trafficking and increasingly contested by rival factions and expanding milícias (paramilitary groups frequently composed of active or former security personnel). The principal one, the Comando Vermelho, emerged as a prison gang in the Cândido Mendes penitentiary on Ilha Grande (Lessing, 2008) and was first mentioned in a prison director's report to the government in 1979 (Misse, 2011); in 2020 it was estimated to have around 30,000 members across Brazil, with secondary strongholds in Amazonas and Mato Grosso (InSight Crime, 2026). This territorial permanence, combined with the built environment of the favelas themselves, has repeatedly been described as an obstacle to policing: narrow streets often force special police units to leave their armored vehicles and to plan routes through maze-like favelas (Grillo, 2014), and incursions have met barricades, concrete ones at the entrance to Jacarezinho in 2021 and burning cars on access roads in 2025 (Sullivan et al., 2021; Sullivan & da Cruz, 2025). Dense, vertically stacked construction that obstructs sightlines, and the absence of reliable, up-to-date maps of informal circulation routes, which leaves operational planning dependent on outdated or incomplete intelligence, belong to the same obstacle; they are stated here as the premise of this study rather than as findings of the sources above.


One consequence of this record bears directly on what follows. The legal and operational category on
which the use of lethal force turns, in each of the episodes above and in the contestation that
followed them, is whether the person engaged was armed. That is a visual judgement made at speed,
and it is increasingly proposed as one an aerial system could assist. Sections 8 to 11 report what
that judgement actually demands of the acquisition: at the reference altitude of this study, 150 m,
the form of a firearm is argued not to be resolvable within the figure, an absence argued rather
than measured (Section 11.4), and at half that altitude, the highest at which a test of the
distinction passed its validity condition, it becomes measurable on synthetic imagery, with the
error profile of Section 9.5.


<!-- ARQUIVO DE ORIGEM: 05-case-jacarezinho.md -->

## 4. Rio de Janeiro's Favelas and the Case of Jacarezinho

Favelas are a defining feature of Rio de Janeiro's urban landscape, housing a substantial share of the city's population in self-built, incrementally constructed settlements that have historically developed outside formal planning and land-titling processes. Among the largest is Jacarezinho, located in the city's North Zone, bordering the neighborhoods of Jacaré, Méier, Engenho Novo, and Triagem. Estimates of its population vary considerably depending on source and methodology: municipal figures place it at approximately 37,000 residents (RioOnWatch, 2019); the 2022 national census recorded 35,458; and community and journalistic sources commonly cite figures above 60,000 (Caminhos Languages, 2025; Mistler-Ferguson, 2022), a discrepancy that is itself illustrative of the broader difficulty official spatial and demographic infrastructures have in capturing dense informal settlements accurately. Covering an area of roughly 40 hectares, Jacarezinho is considered the third-largest favela in Rio de Janeiro after Rocinha and Complexo do Alemão.

Jacarezinho's growth traces back to the early twentieth century, accelerating during the industrial boom of the nearby Méier district after World War II; by 1960 it had already become the largest favela in the city, with a population of roughly 23,000. It is also documented as having the highest concentration of Afro-Brazilian residents among Rio's favelas, a legacy connected to its historical role as a settlement point for formerly enslaved people and their descendants during the city's industrialization (RioOnWatch, 2019). Like many of Rio's favelas, it has long been dominated by the Comando Vermelho (Mistler-Ferguson, 2022). During the police raid of May 2021, fighting took place in narrow alleys and on rooftops, and concrete barricades stood at the favela's entrance (Sullivan et al., 2021).

This dynamic culminated in the May 2021 Operação Exceptis, discussed above, and again on January 19, 2022, when more than 1,200 military police officers occupied the community as part of the state's "Cidade Integrada" (Integrated City) program, an initiative meant to pair security interventions with social and infrastructure programs (Mistler-Ferguson, 2022). Whether such interventions durably alter the community's underlying informality, its unmapped circulation routes, its vertically improvised construction, and the persistence of factional control even after major operations, remains contested. What this study engages is narrower, and prior to it: whether an aerial system flown over this morphology can resolve the distinction on which the justification of lethal force turns, and under what acquisition conditions.


<!-- ARQUIVO DE ORIGEM: 03-methodology.md -->

## 5. Methodology: Research Protocol, Data Collection, and Positionality

The study combines four components: a structured literature review; a qualitative, field-informed contextualization (Sections 3 and 4); a design-science component that proposes a technical model architecture and training strategy (Section 6); and a computational component that implements that strategy, generates synthetic corpora, measures their properties independently of any detector, evaluates transfer to a public aerial benchmark against a ceiling trained on real data, tests on that benchmark alone what the synthetic corpus adds once some real images are available, and scores the armed and unarmed distinction on held-out synthetic imagery (Sections 7 to 11). These components are not run in parallel but built one on the other: the literature review identifies the gap the model is meant to address, the field contextualization supplies the empirical and situational grounding the model needs to be plausible, the design-science component translates that grounding into a concrete technical proposal, and the computational component executes it. Each model of the evaluation protocol of the fourth component was specified before that model was trained, and the protocol grew in stages as earlier results became known (Section 9); it is specified in Section 7.7 rather than here because it is long. That component instantiates the proposal of Section 6 on a different object class, the aerial detection of people, for the reason given at the opening of Section 7.

One of the researchers is an active-duty delegado (police chief) with operational familiarity with public-security activity in Jacarezinho. This gives the study access to a kind of data an outside researcher could not obtain on their own: direct professional experience, institutional knowledge of past operations, and a working understanding of the territory's built environment.

That same position, however, introduces a bias that has to be dealt with directly rather than mentioned in passing. Three points follow.

First, the researcher's institutional role shapes what gets noticed in the field. Observations tend to register tactical features (navigability, choke points, lines of sight) rather than the things a resident-centered or ethnographic account would foreground: daily life, informal economies, or the ways the community itself makes sense of its own space.

Second, access to the territory is itself a product of the researcher's institutional position, and that has consequences beyond who gets in. It affects what can be observed and, just as importantly, whether residents would be willing to speak at all, given the community's documented history of lethal police violence.

Third, none of this can be fully corrected for, only worked around. The study does so in three ways: by checking field observations against independent journalistic, human-rights, and academic sources on Jacarezinho (Sections 3 and 4); by marking tactically framed observations as such wherever they inform this article, rather than presenting them as neutral description; and by treating anything this research produces as a conceptual model, not a validated operational tool, because a data source drawn entirely from policing cannot, ethically or empirically, substitute for community consent or resident perspective.

Given these risks, the study operates under three constraints. No imagery identifying individual residents is collected or used. No precise, address-level building coordinates are published in this article or in any material derived from it. And any future field data collection would require an independent ethics review and a community engagement process external to the police institution, before any real-world deployment is considered.


<!-- ARQUIVO DE ORIGEM: 06-results-proposed-model.md -->

## 6. Design: A Machine Vision Model of Vertical Morphology

Building on the theoretical and methodological groundwork above, this study proposes, at a conceptual, non-deployed level, a machine vision model designed to classify and represent the **vertical structural morphology** of Jacarezinho, with three components:

- **A structural classification backbone**, adapted from CNN-based informal-settlement detection architectures in the literature (Section 2), retrained to distinguish between building height categories, informal rooftop additions, and material transitions (a common visual proxy for informal vertical expansion), rather than the conventional binary informal/formal footprint classification.
- **A domain-randomized synthetic training pipeline**, in which procedurally generated 3D scenes approximate the generic morphological patterns of vertically dense informal housing (irregular building heights, narrow inter-building gaps, mixed rooftop materials, informal cabling and water tanks) with randomized textures, lighting, and camera viewpoints, following the structured domain randomization approach of Prakash et al. (2019). This design choice is a direct response to the ethical and access constraints identified in Sections 2 and 5: it allows model pretraining without requiring extensive, consent-fraught real-world image capture inside the community itself.
- **A real-data fine-tuning stage, which this article specifies but does not authorise.** The sim-to-real literature shows that a modest volume of real data substantially improves generalisation from synthetic-only training, and the architecture reserves a place for it. Its use over the case study territory is contingent on a consent procedure that does not currently exist, whose feasibility under the conditions of Section 3 the Conclusion leaves open, and no imagery of that territory was collected for this work. Section 9.4 runs the stage on the public benchmark only and reports what the synthetic corpus is worth there once some real images exist.

At this stage, the study's contribution under this heading is the **conceptual architecture** described above, not a deployed system. The study does not produce, and does not claim to produce, an operationally validated targeting tool; doing so responsibly would require independent ethical review, meaningful community consultation, and a governance framework for use limitation that falls outside the scope of a single research article.

The **training strategy**, however, does not remain a proposal. Section 7 implements it, and Sections 8 to 11 report what it achieves on a different object class, the aerial detection of people, chosen because it is the only one of the two tasks with a public benchmark against which transfer can be measured. Section 11.3 states why the two results must not be read as one.


<!-- ARQUIVO DE ORIGEM: 03b-methodology-synthetic-pipeline.md -->

## 7. The Synthetic Data Generation Pipeline

The design-science component declared in Section 5 and specified in Section 6 proposes a model of
vertical morphology and a synthetic-training strategy. This section specifies the generative
procedure that implements the second of those, and reports what happens when it is executed.

A distinction has to be drawn at the outset, because the two are easy to conflate. What is
implemented and evaluated below detects people: as a single class wherever transfer to the public
benchmark is measured, and in three classes at 75 m and 35 m, armed, unarmed, and unarmed carrying a
confusable elongated object, a distinction for which we found no public aerial benchmark at these
altitudes; one further model at 150 m did not pass its validity condition (Section 9.5). Person
detection is the task this article measures, and it was chosen because it is the only one of the two
with a public benchmark against which transfer can be established. The conceptual model proposed in
Section 6 classifies built form instead: building height, rooftop addition, material transition. The
same generator already records the footprint, the storey count and the roof height of every
structure it builds, so the morphological task is a second experiment over the same infrastructure
rather than a different pipeline; what it lacks is an evaluation set, and Section 11.3 records that
absence as a finding rather than as an omission. Nothing below should be read as a validated
capability over Jacarezinho, and Section 11 restates the boundary.

### 7.1 Why synthesis, and what it does not solve

The ethical protocol of Section 5 forecloses the conventional route to a training corpus. Aerial
imagery of an inhabited favela, at a resolution sufficient to resolve built form, necessarily
captures residents, rooftop activity, and address-level geometry. Synthesis is therefore not a
technical convenience. It is the only procedure we identified that yields a labelled corpus of the
required morphological specificity without collecting imagery of residents who have not consented
and who cannot meaningfully be asked under the conditions documented in Section 3.

Synthesis substitutes one problem for another. It removes the consent problem and introduces the
transfer problem: a detector trained on rendered imagery must operate on photographs. The remainder
of this section describes the generator. Section 8 characterises the target independently of any
detector, and Sections 9 and 10 report what transfers and what does not.

### 7.2 Scene construction

Scenes are generated procedurally in Blender 5.2, executed headless with a deterministic seed, so
that the authors can regenerate the settlement, the camera and the illumination of any reported
image exactly from the seed recorded for it, and the figures as well in every corpus but the three
that Section 11.5 names. No commercial asset packs are used: surface materials and the four tree
models of the vegetation come from a public-domain library (Poly Haven, CC0), the human figures are
built from the CC0 assets of MakeHuman through MPFB (Section 7.4), and all other geometry is
authored by the generator. That choice keeps the corpus free of any imagery or geometry of the
territory and of any licensed asset, and it is paid for.

Liao et al. (2026) measure the cost: replacing a photogrammetric reconstruction of the target site
with generic assets costs 27.0 mAP50 points on YOLOv11 (their name for YOLO11, the family of the
detector used here) and 22 to 23 on average across the architectures they test. The corpora of this
article sit on the generic side of that ablation by construction, so they pay that cost; two
qualifications bound the figure, since their object class is vehicles and their evaluation is on the
site they reconstructed. Measuring the cost for this morphology would require a reconstruction of
the target site, which the protocol of Section 5 excludes, so it is quoted from their result rather
than measured here.

Layout is produced in three stages (Figure @fig{fig1_nadir}; Figure @fig{fig3_beco} shows the same
scene at street level), each addressing a specific way in which naive procedural generation betrays
itself when viewed from above.

**Parcelling.** The built core is subdivided by recursive binary partition. At each split the
boundary receives a gap drawn from a distribution whose modal value is zero, so that most dwellings
abut their neighbours, as they do in consolidated self-built settlement; because each lot is then
shrunk by 0.15 m towards its centroid and rotated about it (see Orientation below), a zero gap
leaves a narrow seam or a wedge between neighbours rather than an exactly shared wall. In the
configuration used here the gap is zero with probability 0.82, falls between 0.5 and 1.2 m with
probability 0.12, between 1.3 and 2.0 m with probability 0.052, and between 2.3 and 3.1 m with
probability 0.008. The second band is the alley, or *beco*, that defines the morphology.

**Orientation.** A single binary partition, however deformed, leaves legible straight runs of ten or
twenty dwellings, and that is the strongest visual signature of procedural generation in a nadir
view. The generator therefore divides the core into sub-districts, nine in the settlement of the
corpus of record (the 180 nadir frames at 150 m, rendered at 4K, on which S-nadir-150 is trained;
Section 8) and between 6 and 12 in the other five settlements of Section 9.2, each with an
independent orientation, separated by a Voronoi diagram, reproducing the way consolidated settlement
grows by nuclei that meet at an angle. Each lot is also rotated about its centroid by up to 0.17
radians and every corner passes through a smooth domain warp, so the statistic below measures the
three mechanisms together. The statistic is the fraction of edge energy falling within 7.5 degrees
of a cardinal axis, divided by the isotropic expectation. The measurement window covers 30 degrees
of 180, so the isotropic expectation is one sixth and unity means no preferred direction. In the
configuration of the corpus of record, rendered at 4K, the value is 0.94. The single-partition
version of the generator was not measured with this statistic, so no value is reported for it.

**Vertical accretion.** The dwelling is not a single prism. In the majority of cases with two or
more storeys the upper floor is smaller than the one below and offset towards one boundary, leaving
part of the lower slab exposed. Seen from above this produces the L-shaped footprint that
characterises the texture of the settlement, and it is the single geometric feature whose absence
most clearly reads as a grid of boxes rather than a favela. Storey count is drawn around a
low-frequency noise field, with an independent per-dwelling scatter of 0.95 storeys (standard
deviation), so that taller and shorter zones form, as they do on a real hillside.

<!--FIG:06-resultados/figuras/fig1_nadir.jpg|A generated settlement seen from the virtual survey camera: nadir, 150 m above ground, rendered at 1920 by 1080, which gives 9.76 cm per pixel. The resolution is stated because Section 8.1 shows that ground sampling distance, not scene content, sets the size of the target; the corpus used for training is rendered at 3840 by 2160 and is twice as fine. All geometry except the CC0 tree models and human figures is authored by the generator, and all materials are public domain. The three construction stages described above are visible: dwellings abutting their neighbours with alleys mostly between 0.5 and 1.2 m, nine sub-districts meeting at an angle rather than a single orthogonal grid, and upper storeys offset from the floor below, which produces the L-shaped footprints that characterise the texture.-->

Roof surfaces carry the objects that occupy them in use: water tanks in three commercial volumes,
clotheslines, stair housings, satellite dishes, stacked roofing sheets, rubble, and exposed
reinforcement bar awaiting a further storey. Aerial cabling spans between rooftop anchor points.
These are not decoration. At the ground sampling distance of the target sensor they are intended as
a main source of local clutter, although no measurement here isolates their share, and Section 8.3
measures the contrast a person presents against that immediate background, which Section 10.3 tests
as a hypothesis about detector difficulty.

<!--FIG:06-resultados/figuras/fig3_beco.jpg|The same generated scene at street level, inside an alley. The view is not used for training, which is conducted entirely from the aerial camera, and is shown because it is the check that the layout is three-dimensional built form rather than a texture painted to satisfy a top-down view.-->

### 7.3 Camera model

The virtual camera reproduces a commercially available UAV payload in a nadir survey configuration:
a Zenmuse Z30 at 1920 by 1080, corresponding to a 4.3 mm lens on a 5.37 mm sensor, or approximately
28.8 mm on a 36 mm equivalent, pointing down within 3.5 degrees of vertical at a heading drawn per
image, 150 m above ground with a per-image jitter of up to 6 m either way (3 m in the 35 m corpus of
Section 9.5 and 13 m in its twin at 150 m). The parameters are stated in full so that the
acquisition conditions evaluated here can be reproduced or contested without reference to any
particular flight. At that altitude the frame covers approximately 187 by 105 m of ground.

Rendering resolution is treated as a parameter distinct from sensor resolution, and the distinction
is consequential enough to state plainly. Ground sampling distance, not the nominal resolution of
the camera, determines whether a target survives to the network. Rendering the 150 m nadir view at
1920 by 1080 yields 9.76 cm per pixel; rendering the same view at 3840 by 2160 yields 4.88 cm per
pixel. Section 8.1 reports what this does to the target and states the limitation it introduces:
imagery rendered at 4K is easier than a single real frame from the sensor it reproduces.

A second acquisition geometry is evaluated alongside the first, and the reason is arithmetic rather
than aesthetic. At 150 m a carried object is too thin for its form to be resolved (Section 9.5), so
the generator is also run with the same sensor at 75 m, where the frame covers approximately 94 by
53 m and the ground sampling distance halves to 2.44 cm per pixel at 3840 by 2160. Halving the
distance doubles each linear dimension of the target and quadruples its area before occlusion, and
measured on the generated corpora the median instance grows from 17.6 by 17.5 pixels to 47.6 by
41.7, a factor of 6.4 in area. That exceeds the four the geometry alone gives, and part of the
excess is composition: the corpus at 75 m adds a class carrying elongated objects, whose boxes are
the largest, and taken class by class the factor is 5.2 for armed and 5.7 for unarmed figures.

The nadir altitudes are reported separately throughout, as S-nadir-150, S-nadir-75 and, in Section
9.5, S-nadir-35, because they answer different questions: the first is the altitude of the reference
acquisition specified above, and the other two are the geometries under which the distinction the
article is named after was measured.

### 7.4 Annotation

Human figures are copies of a small pool of rigged, clothed meshes built for each rendering run
(MPFB, a MakeHuman derivative; six in the corpora of Sections 9.2 to 9.5), each copy recoloured,
rescaled and posed per instance, and placed both on rooftops and in the alley network. Placement
uses an occupancy map computed from the generated footprints, so that ground placement is known to
fall in open space rather than inferred by ray casting against arbitrary geometry.

Bounding boxes are neither drawn by hand nor inferred from a segmentation pass (Figure
@fig{fig5_anotacao}). For each figure the generator projects a subsample of the body and clothing
vertices (every k-th vertex, about 500 per figure) and every vertex of any carried object into image
space, takes the axis-aligned extent, and clips it to the frame. The convention is therefore amodal
within the frame: the box covers the whole figure, including parts hidden by intervening geometry,
which is the convention used by the real benchmark against which transfer is later measured.
Occlusion is evaluated separately, by casting fourteen rays from the camera to sample points on the
figure, and instances whose visible fraction falls below 0.35 are discarded from the annotation
rather than retained as degenerate boxes. In a settlement this dense the discard rate is substantial
and expected. Over the 180 frames of the corpus of record, 4,582 figures were placed and 3,225
retained; the per-frame retained fraction has a median of 0.71 (10th percentile 0.57, 90th
percentile 0.83), so roughly three in ten figures placed yield no label; the count does not separate
the visibility threshold from the two other reasons a placed figure is dropped, a box that falls
outside the frame or a clipped box with a side below 0.002 of the frame.

<!--FIG:06-resultados/figuras/fig5_anotacao.jpg|Automatically generated annotation on four frames of the pilot corpus, rendered at 1920 by 1080 (9.76 cm per pixel at 150 m). Green marks the armed class, blue the unarmed class; boxes are drawn with a four-pixel outward offset so that they do not cover the target. The strip along the bottom shows individual targets magnified five times, with their true size in pixels printed beneath each one. At this ground sampling distance, twice as coarse as that of the corpus of record, the target is a few pixels of low-contrast texture, which is the central difficulty characterised in Section 8.-->

**Carried objects and hard negatives.** At 75 m the corpus carries three classes rather than two:
armed, unarmed, and unarmed carrying an elongated object. The third exists because of an objection
that would otherwise be fatal to any figure reported for the first. If the weapon is always the same
asset, in the same pose, at the same contrast, a detector can separate the classes on properties of
the asset library rather than on anything visible in the world. Setting weapons against objects
handled in the same way has precedents: in surveillance imagery, a pistol and a knife are set
against a smartphone, a banknote, a purse and a card (Pérez-Hernández et al., 2020), and from drones
hovering at 2 and 5 m, a rifle replica is set against a visually similar umbrella (Torkst et al.,
2026).

The corpus is built to remove that possibility. Five firearm models are generated procedurally, two
rifles, a carbine, a shotgun and a pistol, with recorded lengths of 0.20 to 1.05 m; the meshes of
the two rifles and of the shotgun are longer than the lengths recorded for them. Against them stand
nine elongated objects that a person carries in this territory, spanning 0.88 to 2.5 m: brooms,
floor squeegees, plastic pipe, reinforcement bar, planks, umbrellas, hoes, rolled mats and hose.
Weapons and objects are drawn from one palette of base colours and surface roughness, so that dark
and metallic surfaces occur on both and colour alone cannot separate the two, although light PVC and
coloured plastic occur only on objects. Both are carried through the same distribution of body
poses, held forward, at the side, slung on the back, or carried while walking, in the same
proportions. The item is placed at the right wrist, or on the back when slung, with an orientation
set per pose in the frame of the body rather than solved against the hands, so in some figures it
does not sit in the grip; the same rule places weapons and objects. However, an object whose
recorded length exceeds 1.15 m, which no weapon's recorded length does, is then re-angled in every
pose to rest on the shoulder or to point towards the ground, so most confusable objects are carried
at angles no weapon takes. A detector that separates the classes on this corpus may therefore be
using the length and silhouette of what is carried, the light and coloured materials that only
objects have, and the angle at which it is carried, which is a rule of this generator rather than an
observation of how residents carry things. Section 9.5 tests the last of these, carrying every
object exactly as a weapon is carried, and the rate at which objects are called armed does not rise;
the rate at which the detector calls a broom a rifle is reported directly in that section. Later
corpora, at 35 m and its twins at 75 m and 150 m, including the new frames rendered with their
settings, depart from this in one respect, stated where they are reported: the object is drawn in
the firing pose with probability 0.08 rather than 0.42, the probability used for the weapon, which
is closer to how such objects are carried.

### 7.5 Domain randomisation over illumination

Liao et al. (2026) measure that removing variation in sun position, weather and viewing angle costs
30.4 mAP50 points on YOLOv11, the family of the detector used here, and 17.5 on average across the
architectures they test; averaged over architectures the penalty is largest on truncated objects,
though for YOLOv11 it is smaller on truncated objects than on the whole set. The qualifications of
Section 7.2 apply: their object is vehicles and their test is on the reconstructed site.
Illumination is randomised here because it is the cheapest axis to vary and, for YOLOv11, the more
costly of the two ablations in that study (30.4 points against 27.0), though not on average across
architectures (17.5 against 22 to 23).

Rather than jittering a single sun parameter, the generator defines six internally coherent lighting
budgets (Figure @fig{fig2_climas}), each governing solar irradiance and colour, the angular diameter
of the solar disc, a band of solar elevation (46 to 74 degrees under hard sun, 9 to 25 under low
sun), sky fill and colour, atmospheric scattering density, aerosol content and a camera exposure
offset together: hard sun, low sun, overcast, haze, heavy overcast, and rain (the mean frame
luminances below include each regime's exposure offset). The angular diameter of the sun is what
separates these physically. At 0.6 degrees the shadow edge is hard; above roughly 20 degrees the
cast shadow effectively disappears, which is what a covered sky does. Mean frame luminance over the
48 images of the pilot corpus, the 1080p predecessor of the corpus of record (Section 8.3), runs
87.0 (hard sun), 56.0 (low sun), 84.6 (overcast), 94.4 (haze), 55.6 (heavy overcast) and 35.1 (rain)
of 255.

<!--FIG:06-resultados/figuras/fig2_climas.jpg|The six illumination regimes over an identical scene and identical framing. Top row: hard sun, low sun, overcast. Bottom row: haze, heavy overcast, rain. Over the 48 images of the pilot corpus, not the six panels shown, mean frame luminance runs from 94.4 (haze) to 35.1 (rain) on a scale of 0 to 255. Each regime is a coherent budget over solar irradiance, angular diameter of the solar disc, solar elevation, sky fill, scattering density, aerosol content and camera exposure, not a single brightness adjustment.-->

Each corpus sweeps the regimes in order rather than sampling them, so that a small corpus remains
balanced, and the regime of each image is recorded. This permits the per-regime analysis reported in
Section 8.3 and the per-regime test of Section 10.3.

### 7.6 Training protocol

The scale at which a target reaches the network is treated here as the governing variable, and the
reason is arithmetic before it is empirical. Downscaling a 4K frame to a 1536 pixel training input
divides every linear dimension by 2.5, so the median instance of the corpus of record, 17.6 by 17.5
pixels (Section 8.2), falls to about 7 by 7. The smallest stride of the detector is 8, so such an
instance occupies less than one cell of the finest feature map and is close to invisible to the
network by construction. Tiling has been adopted for the same reason in surveillance footage of
armed pedestrians, where downsampling erases small weapons (Hnoohom et al., 2022).

An earlier arm of this project recorded mAP50 moving from 0.116 to 0.561 between a run trained on
downscaled frames and a run trained on tiles at native scale. That pair is reported here as
consistent with the arithmetic and **not** as an isolated effect of training scale, because the two
runs differ in five further respects: detector size (YOLO11n against YOLO11s), input size (1536
against 1280), epoch count (40 against 60), initialisation (COCO weights against the checkpoint of a
previous interrupted run) and the validation set on which each score is computed (whole frames
downscaled to 1536 px against native-scale tiles). No controlled measurement of training scale alone
exists in this project. Obtaining one requires the same detector, initialisation, epoch budget and
corpus, trained once on downscaled frames and once on native-scale tiles; until it exists, no figure
in this article should be cited as an isolated effect of training scale.

Synthetic training therefore operates on tiles cut at native scale with 20 per cent overlap, never
on downscaled frames, although the scale augmentation of the recipe rescales them at random; the
real-data models, R and the fine-tuning models of Section 9.4, train on whole VisDrone images
resized so that the long side is 1280 px, which downscales the most common training size, 1400 by
1050, and the joint models of that section train on both kinds of input.

<!--TAB:params|Training and inference settings, shared by every model unless stated.-->

| Parameter | Value |
|---|---|
| Detector | YOLO11s, Ultralytics 8.4.148, PyTorch 2.14.0, CUDA 12.6 |
| Hardware | Single NVIDIA RTX 2060, 6 GB |
| Initialisation | COCO pretrained weights for every model except the synthetic-start fine-tuning models of Section 9.4, which start from S-oblique-six |
| Tile size, synthetic corpus at 4K | 1280 px at a stride of 1024 px (20 per cent overlap), with the last column and row aligned to the frame edge, so each 3840 by 2160 frame yields eight tiles and the edge tiles overlap their neighbours by more |
| Empty tiles retained as negatives | each tile without a box kept with probability 0.05; the realised share is not reported |
| Minimum retained fraction of a clipped box | 0.40 |
| Optimiser, learning rate | Ultralytics default (automatic optimiser choice), which ignores the nominal initial learning rate of 0.01 and at these training lengths selects AdamW, momentum 0.9, with an initial learning rate of 0.002 for the single-class models and 0.001429 for the three-class models, decaying linearly to 0.01 of that value after 3 warm-up epochs |
| Input size, batch | 1280 px, batch 6 |
| Augmentation | mosaic 1.0, switched off for the last 10 epochs; horizontal flip 0.5; rotation up to 10 degrees; scale gain 0.4; translation 0.1; HSV gains 0.015, 0.6 and 0.4 (rotation, scale and saturation differ from the Ultralytics defaults of 0, 0.5 and 0.7) |
| Epochs | 60, stopping early after 15 epochs without improvement in validation mAP50-95, the Ultralytics fitness that also selects the reported checkpoint; 30 for the fine-tuning and joint models of Section 9.4, selected the same way on their selection slice |
| Validation split | each rendered frame assigned to validation with probability 0.15, realised as 24 to 35 frames per corpus; split by frame and not by tile, and within a corpus the validation frames show the same settlement as the training frames, from other camera positions, with other figures and light |
| Inference | conf 0.001, NMS IoU 0.7 (Ultralytics default, not tuned), reported at IoU 0.50 and 0.50 to 0.95, and at 0.60 and 0.75 for the check of Section 10.6; on VisDrone every model receives each image resized to 1280 px on its long side, as R is trained, so the 408 validation images of 1360 by 765 are slightly reduced and images of other sizes are enlarged or reduced accordingly |
| Seeds | training seed 0 with deterministic operations (Ultralytics defaults); the 1,106 images of R drawn with seed 21; the fine-tuning and selection slices of Section 9.4 drawn with seed 2609; training seeds 1 and 2 for the five models repeated in Section 10.6 |

Splitting the validation set by frame rather than by tile is necessary because overlapping tiles of
one frame are not independent; splitting by tile would place near-duplicates on both sides.
Precision and recall reported in Section 9, except in the table of Section 9.5, are those the
Ultralytics validator returns at the confidence that maximises F1, not at the 0.001 threshold used
to compute mAP.

### 7.7 Evaluation protocol and the reference ceiling

A detector evaluated on the world in which it was trained reports a ceiling, not evidence. A low
transfer score reported alone is equally uninterpretable, because nothing establishes the scale
against which to read it. The protocol therefore trains the models below. The single-class models
are evaluated on the same real test set, VisDrone-DET validation (548 images, 13,969 person
instances: the benchmark's pedestrian and people categories merged into one class, with its other
categories and its annotated ignored regions dropped). Every model is scored by the Ultralytics
validator, under which a detection inside one of the benchmark's ignored regions counts as a false
positive; every single-class score was also recomputed under the rule of the official VisDrone
toolkit, which drops any box with half or more of its area inside such a region, and no comparison
changes order (Section 9.3). Public benchmarks that annotate a carried firearm do exist, but they
are recorded from surveillance viewpoints, not from the air (Salazar González et al., 2020; Lim et
al., 2021; Ruiz-Santaquiteria et al., 2024; Z. Li et al., 2025). The documented public aerial
datasets we found that label a person as armed were captured between 2 and 8 m above the ground, and
they attach that label to an action class or to a whole recording rather than to an annotated box
(T. Li et al., 2021; Torkst et al., 2026). The drone datasets we found with annotated firearms are
either restricted to law-enforcement agencies (Faheem et al., 2025) or were not released with the
article that describes them (AlJundi et al., 2025). Because we found no public aerial benchmark that
annotates a carried firearm at the altitudes studied here, the three-class models are scored instead
on the validation split of their own corpus, whose tiles also served for early stopping and for
selecting the checkpoint, so that split is held out from training but not from model selection; the
replication of Section 9.5 and the test of Section 11.4 score them in addition on new frames
rendered after training and used for neither training nor selection. Section 9.5 reports them
separately: scored on the world in which they were trained, their figures are ceilings rather than
evidence of transfer, so the two groups cannot be read on one scale. Every synthetic corpus holds
the same number of images, 180 for the single-class models and 200 for the three-class ones, so that
no comparison below is a comparison of the number of frames, although instance counts still differ
(Section 8.2). Table @tab{modelos} lists the models, and Figure @fig{fig9_desenho_experimental}
shows how the corpora, the models and the two kinds of test set connect.

<!--TAB:modelos|The models of the protocol, their training data and what each one establishes.-->

| Model | Training corpus | What it establishes |
|---|---|---|
| **R** | VisDrone-DET train, 1,106 images drawn at random, the number of training tiles in the synthetic corpus of record | The ceiling on the test set at matched volume |
| **S-nadir-150** | Synthetic, one settlement, camera straight down at 150 m, six illumination regimes | The method as proposed, at the acquisition geometry specified in Section 7.3 |
| **S-nadir-150-six** | The same, spread over six settlements | Whether variety of settlement is a term in the gap |
| **S-oblique** | The same settlement and generator settings, oblique camera (with the later weapon library, Section 9.3) | Whether failure is attributable to synthesis or to capture geometry |
| **S-oblique-six** | Six settlements, oblique camera at the calibrated pitch, figures carrying nothing | The best configuration of the generator tried here: the synthetic model of this article |
| **S-nadir-75** | The same generator at 75 m, three classes with hard negatives | Whether the armed and unarmed distinction is resolvable |
| **S-nadir-35**, and its twin at 75 m | At 35 m with realistic carrying poses; the same corpus rendered at 75 m | Whether resolution or carrying pose drives the confusion |
| **F-synthetic, F-generic** | 5 or 10 per cent of VisDrone-DET train (324 or 647 images), starting from S-oblique-six or from COCO | What the synthetic pretraining is worth once some real data exists |
| **F-joint** | The 890 training tiles of S-oblique-six together with the same 324 or 647 real images, starting from COCO | What the synthetic corpus is worth mixed with real data |
| Twin of S-nadir-35 at 150 m | The 35 m corpus rendered at 150 m, three classes | Whether the distinction can be measured at the reference altitude |

The reported efficacy of the synthetic method is mAP50(S) divided by mAP50(R): the fraction of the
ceiling reached without a single real training image. R is matched to the 1,106 training tiles of
the corpus of record; because tiling discards most empty tiles, the oblique models train on fewer
tiles, 968 for S-oblique and 890 for S-oblique-six, so for them the match is by frame count rather
than by training volume. The difference mAP50(S-oblique) minus mAP50(S-nadir-150) estimates, from
one training run per model, the contribution of capture geometry, one effect of which Section 8.2
measures as a factor-of-two difference in target shape between this corpus and the benchmark.

<!--FIG:06-resultados/figuras/fig9_desenho_experimental.png|The design of the experiment. One procedural generator produces every synthetic corpus; the corpora differ in camera, altitude and the classes annotated. Single-class models are scored on the real benchmark, against the ceiling R trained on a matched number of real images; three-class models are scored on the validation split of their own corpus and on new frames rendered after training. The fine-tuning and joint models use slices of the benchmark's training split and are scored on the same real test set; the synthetic-start fine-tuning models begin from S-oblique-six.-->


<!-- ARQUIVO DE ORIGEM: 06b-model-free-evidence.md -->

## 8. Model-Free Evidence

Before reporting detector performance we characterise the problem the detector is asked to solve.
The ordering follows a convention in which model-free evidence precedes estimation. It is also
substantive here: aerial person detection in dense informal settlement is usually discussed in terms
of scene realism, and the implicit assumption is that a corpus which looks more like a favela will
transfer better. The measurements below identify two variables that plausibly govern difficulty and
that no appearance metric captures.

Three corpora are used throughout, two generated and one real, and Section 8.2 adds two oblique
generated corpora; their acquisition geometry differs in ways that matter, so the parameters are
stated rather than implied.

<!--TAB:corpora|The corpora characterised in this section and their acquisition geometry.-->

| Corpus | Geometry | Render | Instances |
|---|---|---|---|
| Pilot corpus | camera within 3.5 degrees of straight down (generator setting, not recorded per image), 28.8 mm equivalent, altitude 150 m | 1920 by 1080 | 565 (train split) |
| Corpus of record | same generator and geometry, rendered at 4K | 3840 by 2160 | 3,225 |
| VisDrone-DET validation | uncontrolled, real acquisition | mixed, mostly 1360 by 765 | 13,969 |

*408 of the 548 benchmark images are 1360 by 765.*

The corpus of record renders the reference acquisition specified in Section 7.3 and is the training
corpus of model S-nadir-150 in Section 9. The pilot corpus is its 1080p predecessor, retained here
because the comparison between the two shows the effect of render resolution, although the two also
differ in the realisation of the settlement (seed 11 against 21), in the number of images (48
against 180) and in the figures placed per frame (14 to 30 against 16 to 34).

### 8.1 Ground sampling distance, not sensor resolution, sets the target size

A person viewed from directly above does not present their height. The vertical dimension, which
makes a person conspicuous in a ground level or oblique image, is exactly the dimension that does
not project in nadir. What the camera records is the plan of the figure, roughly 0.48 m shoulder to
shoulder.

<!--TAB:gsd|Target size by ground sampling distance: median long side of the annotated box and the share of instances whose shorter side falls below one stride of the detector.-->

| Corpus | Render | GSD | Median long side | Shorter side below 8 px |
|---|---|---|---|---|
| Pilot corpus | 1920 by 1080 | 9.76 cm/px | 10.1 px | 66.9 per cent |
| Corpus of record | 3840 by 2160 | 4.88 cm/px | 20.6 px | 0.8 per cent |
| VisDrone-DET val | not applicable | not applicable | 25.0 px | 30.5 per cent |

*Measured over the annotations of the corpora in the table above (the pilot corpus on its training
split, the corpus of record on both splits, the benchmark on its validation split). The smallest
stride of the detector is 8 pixels, so an instance below that size occupies less than one cell of
the finest feature map.*

Two consequences follow, pointing in opposite directions.

The first is a caution about our own headline figure. The survey camera records at 1080p. A single
frame from that camera at 150 m delivers a 10 pixel target on its long side, with two thirds of all
instances below one stride on the short side. Rendering at 4K delivers a 20.6 pixel target on its
long side. Synthetic imagery rendered at 4K is therefore materially easier than a single real frame
from the sensor it reproduces, and any performance figure must declare the ground sampling distance
to which it refers.

The column that carries the argument is the last one, and it is measured on the shorter side of the
box rather than the longer, because it is the shorter side that has to survive one stride of the
network. Read that way the benchmark is not the easy case: 30.5 per cent of its instances have a
side below 8 pixels, against 0.8 per cent of ours at 4K. Part of what any transfer figure reported
later measures is that the real benchmark contains a third of its targets at a scale no detector of
this family resolves well. These sizes are measured at native resolution; at evaluation each
benchmark image is resized to 1280 px on its long side (Section 7.6), so the share below one stride
at the network input differs somewhat from the column above.

The second was initially mistaken for a problem. At 4K the median synthetic instance covers 301
square pixels and the median instance of the real benchmark, its training and validation splits
pooled, covers 300, a ratio of 1.00. The long side does not match as closely, 20.6 against 24.0
pixels over the same pooled splits and 25.0 on the validation split alone, because the two differ in
shape rather than in size, which is the subject of Section 8.2.

We report medians rather than claiming distributional equivalence. Two medians agreeing does not
establish that two distributions agree, and the comparison below is where the distributions in fact
separate.

### 8.2 Apparent size is comparable; apparent shape is not, and it varies with pitch

Size is the wrong statistic. A detector learns a silhouette, not an area. Measuring the aspect ratio
of the same annotation sets, and separating the synthetic corpus by the camera pitch recorded at
generation, gives Table @tab{forma}:

<!--TAB:forma|Apparent shape of the target: median box dimensions and height-to-width ratio by corpus and camera geometry.-->

| Corpus and geometry | Median width | Median height | Median h/w | Instances |
|---|---|---|---|---|
| Pilot corpus, within 3.5 degrees of straight down | 8.3 px | 8.2 px | **0.98** | 565 |
| Corpus of record, same geometry at 4K | 17.6 px | 17.5 px | **0.98** | 3,225 |
| S-oblique corpus, same settlement, pitch 26 to 52 degrees recorded per image | 17.9 px | 26.4 px | **1.46** | 1,912 |
| S-oblique-six corpus, six settlements, pitch 45 to 56 degrees, figures carrying nothing | 13.3 px | 25.2 px | **1.85** | 1,521 |
| VisDrone-DET train, real acquisition | 13.0 px | 24.0 px | **1.95** | 106,396 |
| VisDrone-DET val, real acquisition | 12.0 px | 25.0 px | **2.20** | 13,969 |

*The two nadir rows carry the generator setting that produced them, which bounds the camera within
3.5 degrees of vertical but does not record it per image; the two oblique rows record pitch per
image. The benchmark rows are measured directly. Both benchmark splits are shown because the two
differ, and because the oblique arm of Section 9.3 is calibrated on the training split so that the
validation split remains untouched.*

The two nadir corpora differ by a factor of two in render resolution and by a factor of six in
instance count, and agree on this quantity to the second decimal: 0.98 in both. The real benchmark
sits at 1.95 and 2.20 on its two splits. The separation is therefore a factor of two, and it is
stable under a change of resolution that moves apparent size by the same factor.

The oblique corpus records the pitch of every image, so the same measurement can be split by camera
angle. It gives the dose-response that a contrast of two geometries cannot:

<!--TAB:pitch|Height-to-width ratio of the annotated box by camera pitch in the S-oblique corpus.-->

| Pitch recorded per image | Instances | Median h/w, all figures | Median h/w, figures carrying nothing |
|---|---|---|---|
| 26 to 30 degrees | 482 | 1.28 | 1.35 |
| 30 to 35 degrees | 512 | 1.41 | 1.50 |
| 35 to 40 degrees | 231 | 1.49 | 1.58 |
| 40 to 45 degrees | 359 | 1.64 | 1.82 |
| 45 to 50 degrees | 222 | 1.64 | 1.78 |
| 50 to 52 degrees | 106 | 1.70 | 1.97 |

*Measured from the full-frame labels.*

The ratio rises with pitch, though not strictly between 40 and 50 degrees, from 0.98 at the vertical
to 1.70 at the most oblique angle in the corpus, and for figures carrying nothing it reaches the
value of the benchmark's training split, 1.95, only between 50 and 52 degrees, where it measures
1.97 on 49 figures. Two consequences follow for Section 9.3. The oblique corpus as rendered, with
pitch drawn uniformly between 26 and 52 degrees, realised a median of 1.46 rather than the 1.95 it
was calibrated for, because most of its images sit below the angle at which the benchmark's shape is
reached. And the annotated box of an armed figure includes the weapon, which widens it: 1.38 against
1.58 for figures carrying nothing in the same images. The benchmark has no firearm category, so for
transfer to it the weapon is a source of shape mismatch rather than of signal. The combined model of
Section 9.3 is built from these two measurements, and its corpus realises a median of 1.85.

A ratio near 1.0 is the plan of a figure recorded from above, about as wide as it is long; a ratio
near 2.0 is a standing figure recorded obliquely (Figure @fig{fig8_nadir_obliquo}). At comparable
pixel area, these are different objects as far as the detector is concerned.

This is a domain shift that matters here, and no appearance-based measure of realism detects it. A
generator could be made arbitrarily more photorealistic without moving this quantity. Unlike
photorealism it is also cheap to manipulate, being a property of where the camera is placed rather
than of how the scene is built. Section 9.3 reports the S-oblique model, in which the same generator
settings render the same settlement from a tilted camera, and Section 10.4 treats the difference
between the two models as the contribution of acquisition geometry, together with the settings that
change with it.

One limit on the interpretation is stated here rather than in limitations. The nadir corpora record
a generator setting rather than a per-image pitch, and the benchmark values come from real imagery
whose acquisition geometry is not recorded at all. The oblique corpus anchors the slope on the
synthetic side; on the benchmark side only the endpoint is known.

### 8.3 Contrast against local clutter is higher under overcast than under hard sun and rain

The six illumination regimes permit a measurement bearing on acquisition practice. For every
annotated instance we computed mean luminance inside the box, mean luminance of a six pixel ring
around it, and the standard deviation of that ring. The first difference is raw contrast; the
difference divided by the ring deviation is contrast against local clutter.

Instances within one image are not independent, so the statistic is aggregated per image and the
dispersion reported is between images.

<!--TAB:contraste|Figure-to-background contrast by illumination regime in the pilot corpus: raw luminance difference and contrast against local clutter.-->

| Regime | Mean frame luminance | Raw difference (DN) | Contrast over clutter, median per image | SD between images | Instances |
|---|---|---|---|---|---|
| Hard sun | 87.0 | 15.2 | **0.64** | 0.14 | 113 |
| Low sun | 56.0 | 9.0 | 0.70 | 0.20 | 117 |
| Overcast | 84.6 | **16.4** | **0.88** | 0.26 | 122 |
| Haze | 94.4 | 9.6 | 0.79 | 0.25 | 113 |
| Heavy overcast | 55.6 | 11.2 | 0.72 | 0.38 | 91 |
| Rain | 35.1 | 6.6 | **0.63** | 0.12 | 128 |

*684 instances across 48 images, eight per regime, in the pilot corpus.*

Overcast gives both the largest raw separation between figure and background and the largest
separation once local clutter is accounted for. Hard sun and rain are the two lowest on the latter
measure, and hard sun achieves that while sitting second on raw contrast. The proposed mechanism
follows from the scene description in Section 7.2: under a hard sun the background is itself filled
with sharp cast shadow from water tanks, parapets, clotheslines and cabling, the local deviation of
the background rises, and the figure stops standing out from the disorder. Under a covered sky the
background is smoother, so a comparable difference is easier to find. The mechanism agrees with what
remote sensing reports for dense urban scenes, where shadow cast by buildings obscures much of the
information in the image and can corrupt classification (Dare, 2005), and with a drone benchmark
whose vehicle detectors performed worse in daylight than at night, which its authors attribute to
more objects and a more cluttered background, having noted that daylight brings interference from
shadows; its trackers, by contrast, performed better in daylight (Du et al., 2018). It has a
counterpart that this statistic does not capture: under a direct sun a person also casts a shadow of
their own, which detectors for aerial imagery have used as a cue (Reilly et al., 2010).

What the sample supports and what it does not should be separated. With eight images per regime and
between-image dispersion of 0.12 to 0.38, only the gap between the extremes (rain and hard sun at
0.63 and 0.64, against overcast at 0.88) approaches one standard deviation, and the ordering of the
four intermediate regimes is not resolvable at this sample size. The measurement is therefore a
hypothesis about detector difficulty, not a finding about it: a contrast statistic is not a
detection statistic. Section 10.3 states the test and the condition under which the hypothesis would
be withdrawn; the test was run and the condition is not met, and Section 11.2 draws the implication.

### 8.4 What these measurements imply for the proposal

Taken together the measurements reframe the design problem stated in Section 6. The binding
constraint is not only that a synthetic favela fails to look like a favela. At the scale at which
this task operates, the target is a few tens of pixels of low-contrast texture; its silhouette in
these corpora tracks camera pitch rather than scene content; and hard sun, which matches the
cloud-free sky and minimum solar elevation that aerial survey specifications have conventionally
required (National Geodetic Survey, 2002; Royal Institution of Chartered Surveyors [RICS], 2021), is
the regime with the second largest raw contrast and the second lowest point estimate once local
clutter is accounted for. Section 8.3 attributes this, as a proposed mechanism, to cast shadow in
the background; whether that makes detection harder is the test of Section 10.3, which finds hard
sun the weakest of the six regimes for a detector as well.

Whether these constraints can be overcome by synthesis alone, and what fraction of the
matched-volume ceiling is reached, is the subject of Section 9.


<!-- ARQUIVO DE ORIGEM: 07b-results-placeholder.md -->

## 9. Results: Transfer to Real Imagery and the Armed and Unarmed Distinction

Each model of the protocol in Section 7.7 was specified before that model was run, but the protocol
grew in stages: S-nadir-150-six, S-oblique-six, S-nadir-35 and its twins at 75 m and 150 m, and the
fine-tuning and joint models of Section 9.4 were added after earlier results in this section were
known. Section 10 declares in advance what would overturn the transfer results of Sections 9.1 to
9.3, as Section 11.4 does for the 75 m result of Section 9.5. Five models (S-oblique-six, the two
fine-tuning models at 5 per cent, S-nadir-35 and its twin at 75 m) were trained three times, with
training seeds 0, 1 and 2 on a fixed corpus (Section 10.6); every other model was trained once, so a
difference involving it carries no measured run-to-run dispersion. Nor does any VisDrone figure
carry an interval over the 548 test images, whose persons are clustered within images, so the
smaller differences between zero-shot figures, such as 0.0102 against 0.0190, rest on point
estimates alone.

Table @tab{visao} collects every model with its test set and headline figure; the sections below
give the protocol and the qualifications behind each number.

<!--TAB:visao|Results at a glance. Efficacy is mAP50 divided by that of R on the same real test set. Three-class models are scored on their own synthetic validation split, so their figures are ceilings rather than evidence of transfer.-->

| Model | Training data | Real training images | Test set | mAP50 | Efficacy |
|---|---|---|---|---|---|
| R | 1,106 images of VisDrone-DET train | 1,106 | VisDrone-DET val | 0.6311 | ceiling |
| S-nadir-150 | 180 frames, one settlement, nadir at 150 m | 0 | VisDrone-DET val | 0.0102 | 1.6 per cent |
| S-nadir-150-six | 180 frames, six settlements, nadir at 150 m | 0 | VisDrone-DET val | 0.0190 | 3.0 per cent |
| S-oblique | 180 frames, one settlement, oblique camera | 0 | VisDrone-DET val | 0.0614 | 9.7 per cent |
| S-oblique-six | 180 frames, six settlements, pitch 45 to 56 degrees | 0 | VisDrone-DET val | 0.1055 (mean of three runs 0.0967) | 16.7 per cent (15.3) |
| F-synthetic, 5 and 10 per cent | fine-tuned from S-oblique-six | 324 and 647 | VisDrone-DET val | 0.4424 and 0.5095 | 70.1 and 80.7 per cent |
| F-generic, 5 and 10 per cent | fine-tuned from COCO weights | 324 and 647 | VisDrone-DET val | 0.5220 and 0.5709 | 82.7 and 90.5 per cent |
| F-joint, 5 and 10 per cent | COCO weights, 890 synthetic tiles and the real images together | 324 and 647 | VisDrone-DET val | 0.4607 and 0.5428 | 73.0 and 86.0 per cent |
| S-nadir-75 | 200 frames, three classes, 75 m | 0 | synthetic validation | 0.579; calls 0.237 of confusable objects armed | not applicable |
| S-nadir-35 | 200 frames, three classes, 35 m | 0 | synthetic validation | 0.514; 0.273 (0.253 on new frames) | not applicable |
| Twin of S-nadir-35 at 75 m | the 35 m corpus rendered at 75 m | 0 | synthetic validation | 0.508; 0.165 (0.125 on new frames) | not applicable |
| Twin of S-nadir-35 at 150 m | the 35 m corpus rendered at 150 m | 0 | synthetic validation | did not pass its validity condition (148 of 297 figures found) | not applicable |

A pilot of the full protocol was run first, on a smaller corpus from another realisation of the
settlement rendered at 1080p. Its results are reported first, because they bound what follows and
because withholding an unfavourable pilot would make the rest of this section unreadable as
evidence.

<!--TAB:piloto|The pilot of the protocol: a two-class model trained on 40 scenes rendered at 1080p.-->

| Pilot run | Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|---|
| Pilot model (nadir, 150 m), 40 training scenes at 1080p | synthetic validation | 0.109 | 0.148 | 0.077 | 0.019 |
| same model | VisDrone-DET val, zero-shot | 0.038 | 0.031 | 0.0055 | 0.0020 |


These are not results about transfer: the model failed on its own domain, reaching 0.077 where the
corpus of record reaches 0.79 (Section 9.2), and transfer cannot be measured from a model that did
not learn. Two candidate causes are legible in the corpus statistics before any training, 40
training scenes (Section 10.1) and a render resolution at which two thirds of all instances fall
below one stride of the network (Section 8.1); neither has been isolated. The pilot also used a
different recipe (tiles and input of 640 pixels, batch 8, a budget of 120 epochs cut short by early
stopping) and two classes, armed and unarmed, so its synthetic validation figure is a mean over two
classes and is not on the single-class scale of the 0.79. What the pilot establishes is that this
pipeline is capable of failing. The rows below report the protocol re-run with both defects of the
pilot corpus corrected and with the recipe of Section 7.6.

### 9.1 Ceiling: what real training data achieves on this test set

Model R is trained on 1,106 images drawn at random from VisDrone-DET train (18,858 person
instances), the same number of training images as the tiled synthetic corpus of record, and
evaluated on VisDrone-DET validation. Holding the number of training images equal lets the ratio in
Section 9.2 speak to the data at a matched number of images, though not of instances: the images of
R hold 18,858 persons against 2,659 in the 149 training frames of the synthetic corpus of record
(3,225 in all 180). A run on the full training split (6,471 images) was started and stopped before
completion: with roughly six times as many images per epoch, it would have cost far more machine
time than the matched run to improve a denominator whose role is to be matched, not maximised.

<!--TAB:teto|The ceiling: R, trained on 1,106 real images, on VisDrone-DET val.-->

| Model | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| R (1,106 real training images) | 0.7312 | 0.5729 | 0.6311 | 0.2538 |

This figure is the denominator for everything that follows. It is not a claim about our method; it
establishes what the test set permits at this volume of data.

### 9.2 Transfer from synthetic training, nadir geometry

Model S-nadir-150 is trained only on procedurally generated imagery with the camera geometry of
Section 7.3 and evaluated on the same real test set with no real training image of any kind.

<!--TAB:nadir|S-nadir-150 on its own validation split and on the real test set, zero-shot.-->

| Evaluation set | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| Synthetic validation (ceiling of the corpus) | 0.8707 | 0.7413 | 0.7915 | 0.3656 |
| VisDrone-DET val (zero-shot) | 0.0856 | 0.0421 | 0.0102 | 0.0025 |

**Efficacy of the synthetic method** = mAP50(S-nadir-150) / mAP50(R) = 0.0102 / 0.6311 = 1.6 per cent.

**Variety of settlement at fixed volume.** The corpus of record renders one settlement. Model
S-nadir-150-six keeps every setting of the generator other than those that define the settlement,
and the number of images, fixed and spreads the 180 images over six settlements, 30 each (Figure
@fig{fig6_assentamentos}), differing in relief, forest cover, a corridor through the core (an
avenue, a narrow street or a river) and the palette of roofs and facades, and also in the extent of
the built core, the number of sub-districts, the distribution of storey counts and the share of
vacant lots. It was rendered with the later generator, so its armed figures carry the five weapon
models of Section 7.4, which the corpus of record predates.

<!--TAB:variedade|One settlement against six at a fixed number of frames, nadir at 150 m.-->

| Model | Synthetic validation mAP50 | VisDrone-DET val mAP50 | mAP50-95 | Efficacy |
|---|---|---|---|---|
| S-nadir-150, one settlement | 0.7915 | 0.0102 | 0.0025 | 1.6 per cent |
| S-nadir-150-six, six settlements | 0.6786 | 0.0190 | 0.0071 | 3.0 per cent |

Variety nearly doubles the transfer figure and lowers the score on the model's own validation split,
which is consistent with a model that has stopped memorising one scene, although the two validation
splits are different sets. From one training run per model it is a candidate term in the gap, and in
Section 9.3 it moves the transfer figure less than capture geometry does.

<!--FIG:06-resultados/figuras/fig6_assentamentos.jpg|The six settlements over which S-nadir-150-six and S-oblique-six spread their 180 images, one frame of each from the S-oblique-six corpus, all under the hard-sun regime. They differ in relief, forest cover, a corridor through the core (an avenue, a narrow street or a river) and the palette of roofs and facades. Settlement 1 is the one rendered in the corpus of record.-->

Kiefer, Ott and Zell (2022) report mAP50 on VisDrone of 1.2, 2.4 and 10.2 points for three
architectures trained purely on synthetic data, against 24.6, 48.6 and 43.9 for the same
architectures trained on real data; the YOLO row, the comparable one, gives a ratio of 23.2 per
cent. The two ratios are not directly comparable: their denominator is trained on the full training
split and scored over ten classes, ours on 1,106 images and a single person class, and their
synthetic corpus holds 40,000 game-engine images against 180 scenes here. These differences do not
all act in the same direction, so this design cannot say which ratio is the harsher.

### 9.3 Transfer from synthetic training, oblique geometry

Model S-oblique keeps the settlement, the illumination regimes and the generator settings identical;
the camera is moved (Figure @fig{fig8_nadir_obliquo}), together with the figure-placement filter
that depends on it (Section 10.4). One further difference comes from the generator's history rather
than from the camera: the nadir corpus was rendered before the five-model weapon library of Section
7.4 existed, so its armed figures carry one of three rifle patterns or a pistol and are held forward
with probability 0.46 rather than 0.42, while those of the oblique corpus carry the five models; the
share of armed figures is the same in both.

Pitch is set from the height-to-width ratio of the VisDrone **training** split, not the validation
split on which every model in this article is scored. The distinction is load-bearing: the ratio of
2.20 quoted in Section 8.2 is measured on the validation split, and calibrating a training corpus on
a statistic of the test set and then reporting the gain on that same test set would be circular. The
value used for calibration is 1.95, measured on the training split alone (Section 8.2).

This arm is therefore an adaptation of the corpus to the benchmark, and is reported as such rather
than as a discovery about acquisition geometry in general. What it tests is whether camera geometry,
which moves the mismatch identified in Section 8.2 together with the perspective of the rest of the
scene, is load-bearing on this benchmark.

<!--TAB:obliquo|Nadir against oblique acquisition on the real test set.-->

| Model | mAP50 on VisDrone-DET val | Efficacy vs. ceiling |
|---|---|---|
| S-nadir-150 | 0.0102 | 1.6 per cent |
| S-oblique | 0.0614 | 9.7 per cent |
| S-oblique-six | 0.1055 (mean of three runs 0.0967) | 16.7 per cent (15.3) |

**Difference attributable to acquisition geometry, on this benchmark** = mAP50(S-oblique) -
mAP50(S-nadir-150) = 0.0512, a factor of 6.0.

<!--FIG:06-resultados/figuras/fig8_nadir_obliquo.jpg|The same settlement under the two camera geometries compared in this section: straight down from 150 m, the reference acquisition of this study, and oblique from about 120 m, closer to the benchmark's. Below each frame, four figures carrying nothing, enlarged to the same size without smoothing. Seen from above, a person is the plan of the whole figure, about as wide as it is long, with a median height-to-width ratio of 0.98 over all figures in the nadir corpus; seen obliquely, a standing figure with its limbs, with a median of 1.58 for figures carrying nothing in the oblique corpus (1.46 over all figures), against 1.95 in the benchmark's training split (Section 8.2). Trained on each, the detector reaches 1.6 and 9.7 per cent of the real-data ceiling on the benchmark.-->

Two outcomes were reportable, and both were fixed before the run: if the oblique arm substantially
outperforms the nadir arm, acquisition geometry is load-bearing on this benchmark, consistent with
the direction of Liao et al. (2026) without extending their claim, since a single benchmark that is
not the target domain cannot support a general statement about camera position; if the two arms are
comparable, the limitation lies in synthesis rather than viewpoint. The first obtained. With the
settlement and the training recipe held fixed, the oblique model transfers 6 times better than the
nadir model, against a factor of 1.9 for six settlements instead of one, so on this benchmark the
change of camera moves the transfer figure more than variety of settlement does (that comparison was
not among the criteria, since the variety arm was added after the nadir result). The oblique figure
falls within the synthetic-only range reported by Kiefer, Ott and Zell (2022), although their
figures average ten VisDrone classes.

The oblique corpus did not reach the shape it was calibrated for, 1.46 against 1.95, for the two
reasons measured in Section 8.2. Model S-oblique-six combines the two terms and corrects the
calibration: six settlements of 30 images; pitch between 45 and 56 degrees, chosen to centre the
median of figures carrying nothing on the benchmark's shape, which in the single-settlement oblique
corpus they reach only between 50 and 52 degrees; and only such figures. Its camera placement is
also redrawn, target, pitch and heading together and at most 30 times, until the camera stands at
least 45 m above the ground beneath it and the ray through the centre of the frame first strikes the
scene within 30 m of the target rather than on forest or hillside. It is not an ablation, since
several things change at once; it is the best configuration of this generator tried here and the
model the rest of this article calls the synthetic model. Result: mAP50 0.1055 on VisDrone-DET val
(precision 0.2631, recall 0.1716, mAP50-95 0.0329), an efficacy of 16.7 per cent: 10.3 times the
nadir model and 1.7 times the single-settlement oblique model, against 0.7047 on its own synthetic
validation. Trained twice more on the same corpus with other training seeds, it reaches 0.0958 and
0.0887, so its efficacy averages 15.3 per cent over three runs, between 14.1 and 16.7; the first
run, reported above and in the table, was the best of the three. Under the official VisDrone rule
for ignored regions (Section 7.7) every mAP50 in this section rises slightly, R to 0.6548 and the
first run of S-oblique-six to 0.1074, while every efficacy falls slightly, that of S-oblique-six
from 16.7 to 16.4 per cent, and no comparison between the models of Sections 9.1 to 9.3 changes
order at an intersection-over-union of 0.50, 0.60 or 0.75. The rendered figure approaches the
calibration target without reaching it: a median height-to-width ratio of 1.85 at 13.3 by 25.2
pixels, against 1.95 at 13.0 by 24.0 in the benchmark's training split (Section 8.2). In absolute
terms, the 10.5 points of mAP50 of the first run sit just above the upper end of that synthetic-only
range and the 9.7 of the mean of three runs just inside it, under the same difference in classes,
while the ratio to our own ceiling stays below theirs (Section 9.2).

The acquisition geometry this article reproduces points straight down. An oblique corpus that
transfers better to VisDrone is informative about the benchmark, not about the acquisition that
would be flown over Jacarezinho.

### 9.4 Limited real fine-tuning, on the public benchmark only

The proposal of Section 6 reserves a stage in which the synthetic pretraining is fine-tuned on a
modest volume of real imagery. It is run here on the public benchmark only, as a line separate from
the synthetic-only results above so that the two contributions stay distinguishable, and no imagery
of the case study territory is involved.

The protocol was fixed before the run. Two slices of the VisDrone-DET training split, 5 per cent
(324 images) and 10 per cent (647 images, containing the first), each train two models: one
initialised from the synthetic model of Section 9.3 and one from the same generic initialisation as
every other model in this article. The synthetic start carries over every weight, including a
detection head already trained for one person class, whereas the generic start re-initialises the
last classification layer of the COCO head, which has eighty classes; the synthetic start therefore
begins as a working person detector, consistent with its lead in the first three epochs at 5 per
cent, although at 10 per cent the generic start leads from the first epoch, and the result below
holds despite that head start. The checkpoint is selected on a further 5 per cent of the training
split, disjoint from both, so that the validation split on which every figure here is scored is not
used for selection, which removes for this comparison the asymmetry declared in Section 10.5. All
four models train for thirty epochs with the same detector, input size and augmentation. Both starts
receive the same untuned schedule of Section 7.6, AdamW at 0.002 with three warm-up epochs, although
one of them is already a person detector, and no lower learning rate, frozen layers or longer budget
was tried for either. On the selection slice all four models reach their best mAP50 and mAP50-95
between epochs 27 and 30 of 30, so the comparison is at a fixed budget rather than at convergence,
although the generic start's lead on that slice does not narrow between epoch 20 and epoch 30.

<!--TAB:ajuste|Fine-tuning on 5 and 10 per cent of the benchmark's training split from the synthetic model and from generic weights.-->

| Real training data | F-synthetic (from S-oblique-six) | F-generic (from COCO) | Difference |
|---|---|---|---|
| 5 per cent (324 images) | 0.4424 | 0.5220 | -0.0796 |
| 10 per cent (647 images) | 0.5095 | 0.5709 | -0.0614 |

*mAP50 on VisDrone-DET val under the protocol of Section 9.1.*

<!--FIG:06-resultados/figuras/fig10_ajuste_fino.png|mAP50 on VisDrone-DET val against the number of real training images, for the three ways of using the synthetic corpus once real images exist: as the starting weights (synthetic start), mixed into the training set (joint), or not at all (generic start). Filled markers are the first training run, reported in the table; open markers are the two further runs where they exist. The dashed line is R, trained on 1,106 real images for twice as many epochs. At both volumes the generic start ends highest and the synthetic start lowest.-->

The quantity of interest is the difference at each volume: what the synthetic pretraining is worth
when real data is scarce (Figure @fig{fig10_ajuste_fino}). The expectation, stated before the run,
was that it would be largest at the smaller volume.

It is negative at both. Initialised from the synthetic model, the detector finishes 8.0 points of
mAP50 below the generic initialisation with 5 per cent of the real data and 6.1 points below with 10
per cent, and the synthetic start given 647 real images (0.5095) does not reach the generic start
given 324 (0.5220). The sign is the same in mAP50-95, the metric on which every checkpoint was
selected: -0.0368 at 5 per cent and -0.0232 at 10 per cent. The expectation stated before the run
therefore fails: the difference is not largest at the smaller volume but most negative there. Its
magnitude narrows as real data grows, but what narrows is a cost, not a benefit. On the selection
slice the generic start overtakes the synthetic one by the fourth epoch at 5 per cent and in the
first epoch at 10 per cent, after which the synthetic start leads only intermittently. Fine-tuning
does transform the synthetic model itself, from 0.1055 to 0.4424 with 324 real images, which is the
effect the sim-to-real literature reports; what it does not do here is outperform a generic start
given the same real images. Relative to the ceiling of Section 9.1, trained on 1,106 real images for
twice as many epochs, the generic start recovers 82.7 and 90.5 per cent and the synthetic start 70.1
and 80.7 per cent. Repeated at 5 per cent with training seeds 1 and 2, each synthetic start from the
S-oblique-six model of the same seed, the synthetic start reaches 0.4608 and 0.4554 and the generic
start 0.5228 and 0.5285: the lowest of the three generic runs lies above the highest synthetic one,
so the difference exceeds the spread between runs by the criterion fixed in advance (Section 10.6).
On this benchmark and at these volumes the synthetic corpus does not substitute for real data; it
costs some. One candidate explanation, not tested here, is that training on 890 tiles of generated
figures overwrites part of what the generic initialisation encodes about real people; the joint
models below, which keep that initialisation and see the real images throughout, bear on it.

**Joint training.** Pretraining is one way to use the synthetic corpus; training on synthetic and
real imagery together is the other, and it was specified with its criterion before it was run. Two
models (F-joint) start from COCO and train for 30 epochs on the 890 synthetic tiles of S-oblique-six
together with the same 324 or 647 real images, selected on the same slice. Each real image is seen
as often as in the generic start, but every epoch also carries the synthetic tiles, so these models
take more gradient steps. They reach 0.4607 at 5 per cent and 0.5428 at 10 per cent, 0.0613 and
0.0281 below the generic start given only the real images, beyond the margin fixed in advance, twice
the standard deviation of the three generic runs at 5 per cent (0.0035), a standard deviation that
at 10 per cent is borrowed from the 5 per cent runs. Mixed in, the synthetic corpus costs less than
as pretraining at an intersection-over-union of 0.50 and 0.60, though at 10 per cent not at 0.75,
but it still costs: on this benchmark neither way of adding it to real data helped. That keeping the
generic initialisation and showing the real images from the first epoch reduces the cost without
removing it suggests that the explanation offered above is at most part of the account.

This result departs from the closest precedent only in part. Kiefer, Ott and Zell (2022) pretrained
a COCO-initialised YOLO on up to 40,000 game-engine images generated to match VisDrone's traffic
scenes and found the gain on VisDrone largest with the smallest real set. Their figure 2 also shows,
however, that pretraining on only 10,000 synthetic images scored below no synthetic pretraining at
every real-data size on their maritime benchmark, and gave no consistent gain on VisDrone beyond the
smallest real set. Our corpus holds 890 tiles of six generated settlements. Negative transfer (Wang
et al., 2019) recurs in aerial person detection. On the full VisDrone training split, pretraining on
either of two public synthetic corpora scored below training from scratch at most detector sizes. A
corpus designed for diverse human motion scored above it and, combined with COCO in pretraining,
above COCO alone on the one detector size tested (Yim et al., 2026). Mixing synthetic with real
images fell below the real-only baseline in low-shot VisDrone training (Shen et al., 2023b). It
harmed the larger COCO-pretrained detectors most when real images were fewest, and much less once
the two shares were balanced (Shen et al., 2023a). With unbalanced batches, it biased a drone
detector of people at sea towards the more numerous synthetic images (Martinez-Esteso et al., 2025).
These findings are consistent with our joint-training cost, which narrows as the real share grows.
The candidate mechanism has only indirect support, from training on renders alone: retraining a
feature extractor pretrained on real images degraded detection, whereas freezing it came close to
training on real images (Hinterstoisser et al., 2019), although freezing hurt with highly randomised
scenes (Tremblay et al., 2018). At these volumes the starting weights weigh most (He et al., 2019),
and this design cannot tell which property of the corpus decides the sign: its size, its variety or
its image domain, the factor that most determines positive transfer (Mensink et al., 2022).

### 9.5 The armed and unarmed distinction, by altitude

No accuracy for the armed and unarmed distinction is reported at 150 m. At that altitude the median
instance measures 17.6 by 17.5 pixels, and a firearm is argued from resolution, not shown by
measurement, to be unresolvable within it. No model was trained to separate the classes on the
corpus of record, and a detector that did so there could be relying on the weapon being the only
elongated object any figure carries, so its separability could not be told apart from a property of
the generator. A three-class model was later trained at 150 m on a twin of the 35 m corpus described
below, identical to it in every setting except altitude and its jitter, and so with the confusable
objects the corpus of record lacks. A validity condition was fixed before it was run: the model had
to find at least half of the annotated figures, in any class. It found 148 of 297 (0.498), so its
rates are not interpretable and are not reported as a result; descriptively, it calls 0.34 of armed
figures and 0.14 of confusable objects armed, which taken at face value would separate the classes
rather than support the absence, plausibly by the length of what is carried rather than the form of
a firearm. The absence at 150 m therefore remains argued, not measured.

At 75 m the median instance measures 47.6 by 41.7 pixels, 6.4 times the area over all classes (5.2
times for armed figures alone, Section 7.3), and the corpus is built so that the artefact cannot
account for the result: five firearm models against nine elongated objects carried in the same
territory, sharing the weapons' colour and roughness palette and the same distribution of body
poses, though objects longer than any weapon are held at other angles (Section 7.4). The corpus
holds 2,887 instances in 200 images, 933 of them armed, 973 unarmed and 981 carrying a confusable
object. A second corpus at 35 m, 1.1 cm per pixel, holds 2,223 instances with a median of 121.8 by
103.1 pixels (Figure @fig{fig7_armados}).

<!--FIG:06-resultados/figuras/fig7_armados.jpg|Figures carrying a rifle, a pistol, nothing, a broom, a length of pipe or a closed umbrella at the three altitudes of this section, each cropped from a rendered frame and scaled to the same size without smoothing, so that every crop shows the pixels the detector receives. The carrying figures were chosen by eye, among isolated figures under clear light, as ones whose item sits in the hand and close to the horizontal, so that its full length shows; in many frames the item points steeply downward and appears foreshortened, or does not sit in the grip, because of how the generator places it (Section 7.4). At 35 m the weapons and the objects are distinct shapes; at 75 m they survive as lines of different length and tone; at 150 m, the reference altitude, the whole figure is a few tens of pixels, the rifle and the pistol cannot be told from the body, and a long object such as the pipe, the broom or the umbrella still shows as a line. The crops at 35 m and 75 m come from the corpus at 35 m, its twin at 75 m and the new frames rendered with their settings; those at 150 m from the twin corpus whose model did not pass its validity condition.-->

<!--TAB:armado|The armed and unarmed distinction on the validation split of each three-class corpus.-->

| Quantity | S-nadir-75 (75 m) | S-nadir-35 (35 m) | Twin of S-nadir-35 at 75 m |
|---|---|---|---|
| mAP50, three classes | 0.579 | 0.514 | 0.508 |
| Recall, armed | 0.547 | 0.569 | 0.471 |
| Precision, armed | 0.386 | 0.415 | 0.440 |
| Rate at which a confusable object is called armed | 0.237 | 0.273 | 0.165 |
| Rate at which an unarmed person with no object is called armed | 0.131 | 0.168 | 0.109 |

*Protocol: inference on the full 4K frame at native scale; for the rates, confidence 0.25 and
one-to-one matching at an intersection-over-union of 0.50 that ignores the predicted class, each
person taking the class of its best-overlapping prediction, so that a second box of another class on
the same person counts only against precision; the validation split of each corpus (27, 35 and 24
images). The threshold of 0.25 is the Ultralytics default for prediction and was not tuned; every
rate depends on it and varies with the realisation of the settlement: in the new realisation of
Section 11.4 the S-nadir-75 model calls 0.15 of confusable objects and 0.43 of armed persons armed,
against 0.237 and 0.547 here. The rates also give d′, the difference between the normal quantiles of
the armed recall and of the rate at which the other class is called armed, which under the usual
equal-variance assumption separates how well a model distinguishes two classes from how readily it
calls a figure armed: against confusable objects 0.83, 0.78 and 0.90 in the three columns, against
unarmed persons 1.24, 1.14 and 1.16; the replication below uses a log-linear correction for rates
near zero or one, under which the validation-split values against confusable objects are 0.77 and
0.89 for S-nadir-35 and its twin. The third column is the matched corpus described below.*

The fourth row is the quantity of interest. It is the synthetic estimate, unmeasured on real
imagery, of the rate at which the system would mark a resident carrying a broom, a length of pipe or
a rolled mat as armed, and it is the concrete form of the dual-use harm this article discusses.
Because each person takes only the class of the prediction matched to it, an armed box on a person
matched to a box of another class does not enter this rate, although an operator would see it as an
alert, so the rate is a lower bound on how often such a person receives an armed detection at this
threshold; the precision row counts those boxes, together with alarms on background, without
separating them. The rate is not an artefact of how the generator carries objects, although that was
a live possibility, since every object longer than 1.15 m is re-angled in every pose (Section 7.4).
In the unseen-weapon test of Section 11.4 the closed umbrella, which at 0.88 m falls below that
length and so is carried in the weapons' poses, is the object most often called armed (0.38, on 29
instances), against 0.10 for brooms (41) and 0.11 for lengths of pipe (28). The frames of that test
were rendered again with every confusable object carried exactly as a weapon is, in the weapons'
distribution of poses and at their angles, with every random draw unchanged, so that the two
versions match box for box in 49 of 50 frames. Paired object by object over 227 objects, the
S-nadir-75 model calls 0.154 of them armed as normally carried and 0.137 when carried as a weapon
(exact McNemar test, p = 0.56), and the umbrella, whose carriage did not change, stays at 0.38. By
the criterion fixed before the test the rate does not rise, and the caveat that objects carried as
weapons would be called armed more often is withdrawn.

Nor does the rate fall when the ground sampling distance is halved again, although the two corpora
differ in more than altitude. The 35 m corpus also changed how confusable objects are carried: at 75
m the object was drawn in the firing pose with probability 0.42, as the weapon is, while at 35 m it
is drawn that way with probability 0.08 and otherwise over the shoulder, at the side or in one hand,
the more realistic distribution, which confounds resolution with pose and with every other setting
that changed between the two corpora (render sampling, the share of figures placed on rooftops,
figures per frame, the radius of wires and clotheslines, the placement of candidate positions and
the settlement seed). A third corpus separates them: identical to the 35 m corpus in every setting
except altitude and its jitter, rendered at 75 m. A replication was also fixed before it was run,
with its criterion: on 80 new frames continuing the seed of the 35 m corpus, and their twins at 75
m, none used in training, the difference would count as established if the 35 m rate exceeded the
twin's at a two-sided p below 0.05, would be withdrawn if the direction reversed, and would remain
suggestive otherwise. Table @tab{gemeo} gives the two models on both sets, across three training
runs and at three overlap thresholds.

<!--TAB:gemeo|The 35 m model against its twin rendered at 75 m with every other setting held: rates at which each class is called armed on the validation splits (35 and 24 images) and on the 80 new frames of each corpus; ranges over three training runs; and the object rate on the validation split at stricter overlap thresholds. Intervals for d′ are 95 per cent by resampling frames; p from two-proportion tests without correction for clustering by frame.-->

| Quantity | S-nadir-35 (35 m) | Twin at 75 m | Difference |
|---|---|---|---|
| Confusable object called armed, validation split | 0.273 | 0.165 | 10.8 points, p = 0.06 |
| Confusable object called armed, 80 new frames | 0.253 (74 of 292) | 0.125 (36 of 288) | 12.8 points, p = 0.0001 |
| Armed person called armed, validation split | 0.569 | 0.471 | p = 0.15 |
| Armed person called armed, 80 new frames | 0.543 | 0.432 | |
| Unarmed person called armed, validation split | 0.168 | 0.109 | p = 0.22 |
| d′ against confusable objects, validation split | 0.77 | 0.89 | |
| d′ against confusable objects, 80 new frames | 0.77 (0.57 to 0.99) | 0.97 (0.77 to 1.20) | |
| Object rate over three training runs, validation split | 0.231 to 0.273 | 0.132 to 0.242 | ranges overlap |
| Object rate over three training runs, 80 new frames | 0.202 to 0.253 | 0.097 to 0.181 | ranges separate |
| Object rate, validation split, at IoU 0.60 and 0.75 | 0.223 and 0.132 | 0.165 and 0.132 | level at 0.75 |

*The two models reach the same mAP50 on their validation splits (0.514 and 0.508) and a precision of
0.415 against 0.440 on the armed class (Table @tab{armado}).*

With every other setting held, halving the ground sampling distance did not reduce the confusion: in
the first training run the 35 m model calls every class armed more often in point estimate, at the
same mAP50 and with a d′ no larger than the twin's, so the 35 m result does not appear to be an
artefact of the change of pose. On the new frames the difference in the object rate is established
by the criterion fixed in advance, and its direction holds across the three training runs there but
not on the smaller validation splits, where the ranges overlap; the rates for armed and unarmed
persons, and with them the observation that the 35 m model calls every class armed more often, do
not hold across the runs on either set. The rate also depends on the overlap required to score a
detection: at an intersection-over-union of 0.75 the 35 m model and its twin coincide on the
validation split, and against the original 75 m model, which calls 0.230 and 0.141 of objects armed
at 0.60 and 0.75, the 35 m model changes order, so by the criterion of Section 10.6 that second
comparison is an artefact of annotation and the argument rests on the matched twin. At 75 m, moving
from the original corpus to the settings of the 35 m corpus, realistic carrying poses among them, is
followed by an object rate of 0.165 against 0.237, a difference the two-proportion test does not
support (p = 0.19). Section 11.4 states the condition under which the 75 m figure would be withdrawn
and reads the altitudes together.


<!-- ARQUIVO DE ORIGEM: 08b-robustness.md -->

## 10. Robustness and Alternative Explanations

Each threat below is named, given a check, and given an explicit condition that would overturn the
result it protects; where the check has not been run, the text says so. Stating that condition in
advance is what distinguishes a check from a defence written after seeing the number. Each
overturning condition below was fixed before the corresponding measurement was run.

### 10.1 The corpus is small, and small corpora flatter themselves

**Threat.** The synthetic corpus is generated, so its size is a choice rather than a constraint, and
a detector trained on few scenes can memorise them. An earlier pilot of this pipeline used 40
training images and reached mAP50 of 0.077 on its own validation split, against 0.79 for the corpus
of record, trained on 149 of its 180 images at 4K (Section 9.2). The pilot is reported here because
it is instructive, not because it is a result: it establishes that this pipeline is capable of
failing, and points to scene count as one candidate cause, which the check below would test and
which has not been isolated.

**Check.** Learning curve over the number of distinct generated scenes, holding the illumination
regimes balanced and the tiling protocol fixed. A related comparison has been run at a fixed 180
images, one settlement against six (Section 9.2): 0.0102 against 0.0190 on the real test set. It
varies the variety of settlement at a fixed number of scenes, so it is not a point on this curve,
which was specified and has not been run.

**What would overturn the claim.** If performance on the real test set does not rise from the
smallest corpus to the largest by more than the between-seed dispersion of Section 10.6, scene count
is not the operative variable and the conclusion of Section 9 must be restated as a property of the
generator rather than of corpus size.

### 10.2 Apparent size, not synthesis, may explain the transfer gap

**Threat.** Section 8.1 reports that the synthetic target at 4K and the real benchmark target cover
near-identical median area, 301 and 300 square pixels, the second with the benchmark's training and
validation splits pooled. That match is a property of the rendering resolution we selected, and it
does not extend to the long side, which is 20.6 against 24.0 pixels over the same pooled splits.
Where it is not exact, as on the long side, a transfer failure attributable to scale could be
mistaken for a failure attributable to synthesis.

**Check.** The real test set is additionally evaluated at an input size chosen so that the median
long side of its person boxes, as they reach the network, matches that of the training corpus. The
scale has to be set through the input size, because the validator resizes every image so that its
long side equals the input size, enlarging as well as reducing, so rescaling the image files and
evaluating them at the same input size changes nothing the network sees. The input size is chosen
from the labels and image sizes alone, before any evaluation.

On the corpus of record the check was run as specified. At the protocol's input size of 1,280 pixels
the median long side of the benchmark's person boxes reaches the network at 25.33 pixels; at 1,024
it reaches it at 20.27, the closest a multiple of 32 comes to the 20.55 of the corpus of record,
while the median area falls from 283 to 181 square pixels, since no uniform rescaling matches shape.
At 1,024 pixels S-nadir-150 reaches 0.0128 against 0.0102 at the protocol's size, and R 0.5849
against 0.6311, which would put the efficacy of Section 9.2 at 2.2 rather than 1.6 per cent. What
still differs at a matched long side is shape, which Section 10.4 tests.

**What would overturn the claim.** If the two figures diverge substantially on the corpus of record,
scale is a live confound after all and the efficacy ratio in Section 9.2 must be reported at matched
scale only. "Substantially" was fixed before the matched run as a difference of more than half of
the protocol figure. The difference is a quarter of it, 0.0026 on 0.0102, so the condition is not
met and the ratio of Section 9.2 stands at the protocol's scale.

### 10.3 Illumination: the prediction that runs against intuition

**Threat.** Section 8.3 measures that overcast yields both the largest raw figure-to-background
difference and the largest ratio of contrast to local clutter, while hard sun sits second on raw
contrast and among the two lowest on the ratio. That raises the hypothesis that the detector
performs better under overcast than under hard sun. A contrast statistic is not a detection
statistic, the sample is eight images per regime, and between-image dispersion is of the same order
as several of the gaps.

**Check.** Per-regime performance on a held-out synthetic split, six regimes, balanced (Figure
@fig{fig4_dataset}). It was run on 120 new frames continuing the seed of the corpus of record, 20
per regime, none used in training, and scored with S-nadir-150 as mAP50 on the tiles of each regime,
the protocol of the synthetic ceiling of Section 9.2, and, as a secondary measure fixed with it, as
recall at confidence 0.25 on whole frames with 95 per cent intervals by resampling frames. Table
@tab{regimes} gives the result: hard sun is the weakest regime on both measures, and overcast the
strongest on mAP50, level with low sun. An ablation against a corpus generated under hard sun only,
evaluated on the full six-regime split and on the real test set, was specified and has not been run.

<!--TAB:regimes|Per-regime performance of S-nadir-150 on 120 new frames of the corpus of record, 20 per regime, none used in training: mAP50 on the tiles of each regime and recall at confidence 0.25 on whole frames, with 95 per cent intervals by resampling frames.-->

| Regime | mAP50 | Recall at 0.25 | 95 per cent interval |
|---|---|---|---|
| Hard sun | 0.675 | 0.657 | 0.591 to 0.720 |
| Heavy overcast | 0.755 | 0.768 | 0.714 to 0.816 |
| Rain | 0.759 | 0.789 | 0.748 to 0.827 |
| Haze | 0.780 | 0.726 | 0.697 to 0.757 |
| Low sun | 0.790 | 0.814 | 0.768 to 0.854 |
| Overcast | 0.791 | 0.796 | 0.760 to 0.827 |

No public aerial benchmark isolates this contrast on real imagery. VisDrone covers various weather
and lighting conditions, but for detection it records occlusion and truncation for each box and no
illumination label (Zhu et al., 2022). DroneCrowd labels its sequences as cloudy, sunny or night
and, for its proposed method and its three strongest baselines, reports larger counting errors on
sunny than on cloudy sequences, but across different scenes and crowd sizes, and for counting rather
than detection (Wen et al., 2021). Okutama-Action was captured at a single site under sunny and
cloudy conditions without results reported by condition (Barekatain et al., 2017), which makes it
the nearest candidate for a real test that holds the scene constant. In agricultural detection from
drones, a recent review reports that sunny, overcast and variable conditions did not significantly
affect model performance (Maes, 2025). The per-regime result therefore has no counterpart on real
imagery yet, and it may be specific to small targets over cluttered backgrounds.

<!--FIG:06-resultados/figuras/fig4_dataset.jpg|One annotated frame of the pilot corpus (nadir, 150 m, 1920 by 1080) from each of the six illumination regimes, with the generated boxes drawn. Green marks the armed class and blue the unarmed class. No accuracy figure for that distinction is reported at this altitude, for the reason given in Section 11.4; the 75 m and 35 m results are reported in Section 9.5. Boxes are computed from the scene geometry, not from the rendered pixels (Section 7.4), so the labelling does not depend on the regime, and the per-regime differences found by the test of this section, run on new frames of the corpus of record, cannot come from it.-->

**What would overturn the claim.** If per-regime performance is not higher under overcast than under
both hard sun and rain, the only gap that Section 8.3 approaches resolving, or if hard sun is not
among the two weakest regimes, the mechanism proposed in Section 8.3 is wrong and the operational
implication in Section 11 is withdrawn. The image statistics would still stand, but they would be
describing something other than detector difficulty. The ablation in the check above carries no
overturning condition and would be reported descriptively. Neither part of the condition is met:
overcast scores above hard sun and above rain, and hard sun is the weakest of the six regimes. What
is robust is that hard sun is the weakest regime on mAP50, eight points below the next, and that its
recall interval lies wholly below those of overcast, rain and low sun, though it overlaps those of
haze and heavy overcast; the margin of overcast over rain lies within the recall intervals. Low sun,
which also casts sharp shadows, scores level with overcast; the condition fixed in advance does not
test this, and it limits the mechanism of Section 8.3 to a partial account.

### 10.4 Capture geometry against scene content

**Threat.** The central comparison of this article attributes a performance difference to camera
placement. It could instead reflect any of the incidental differences between the two synthetic
arms.

**Check.** The two models are trained on corpora generated with the same settings (though not with
the same version of the generator: the nadir corpus predates the five-model weapon library of
Section 7.4, so its armed figures carry one of three rifle patterns or a pistol and are held forward
with probability 0.46 rather than 0.42), the same settlement seed, the same material library, the
same illumination regimes, the same share of armed and unarmed figures and the same annotation
procedure, with the same training recipe and the same number of images, both at 4K. What differs is
the camera: pitch, drawn between 26 and 52 degrees and recorded per image, altitude (120 m for the
oblique camera, with a per-image jitter of up to 36 m either way) and its jitter. One further
setting differs because the camera does: the nadir corpus keeps figures within a square around the
camera axis whose side is 0.52 of the nadir frame width, the filter that produced it, while the
oblique corpus places them anywhere the projected frame covers, since an oblique frame is not a
square on the ground. At the centre of the frame and at the nominal 120 m, the oblique camera puts
the ground sampling distance between about 4.3 and 6.3 cm per pixel across the pitch range, a span
the altitude jitter widens, against 4.88 for the nadir corpus, so the change of camera moves the
shape of the target (h/w 1.46 against 0.98) and leaves its size in the same range, somewhat larger
in area (456 against 301 square pixels). Pitch is set from the VisDrone training split rather than
from the validation split on which both models are scored, so that the calibration does not consume
the test set. Result: 0.0614 for the oblique model against 0.0102 for the nadir model on the real
test set. The figure of 0.1055 for S-oblique-six (Section 9.3) is not a result of this check: that
corpus also changes the settlements, the pitch range, the figures, which carry nothing, and the
placement of the camera.

**What would overturn the claim.** If the oblique arm does not outperform the nadir arm, capture
geometry is not the dominant term, and Section 9.3 must conclude that the limitation lies in
synthesis rather than viewpoint. That outcome is reportable and is not treated here as a failure of
the study.

### 10.5 The ceiling may be low for reasons unrelated to us

**Threat.** A low transfer figure is uninterpretable without knowing what the test set permits.
Small-object aerial detection is difficult for real-data models too, and a reader has no way to
distinguish a weak synthetic method from a hard benchmark.

**Check.** Model R, trained on 1,106 images of the real training split of the same benchmark under
the same detector, the same input size, the same initialisation and the same schedule, reaches mAP50
0.6311 (Section 9.1). All synthetic figures are reported as a ratio to it.

One asymmetry is declared here rather than left for the reader to find. Model R selects its
checkpoint on the very split it is later scored on, the 548 validation images, while the synthetic
models select theirs on a synthetic validation split. This favours R, so the efficacy ratio reported
in Section 9.2 is conservative: it understates the synthetic method rather than flattering it.

**What would overturn the claim.** If R itself performs near chance under this protocol, the
protocol is inadequate to the benchmark and no conclusion about synthetic efficacy can be drawn from
it. In that case the appropriate report is the failure of the evaluation design, not a finding about
synthesis.

### 10.6 Two checks specified in advance

Two further threats had a check specified in advance; both have since been run, under criteria fixed before the runs.

**Annotation convention.** Synthetic boxes are amodal and projected from vertices; benchmark boxes
are human-drawn. A systematic difference in tightness would move overlap scores without any
difference in detection. The check is sensitivity of every reported figure to the
intersection-over-union threshold at 0.50, 0.60 and 0.75; if the ordering of the models changes with
the threshold, the comparison is an artefact of annotation and must be reported at several
thresholds. Under both the Ultralytics validator and the official rule of Section 7.7, no pair among
those fixed for this check changes order between 0.50, 0.60 and 0.75 on the benchmark. One further
comparison of Section 9.4 does: at 10 per cent, joint training scores above the synthetic start at
0.50 and 0.60 and below it at 0.75 (0.0983 against 0.1025). Among the three-class models of Section
9.5, scored on their own synthetic splits, the order also changes: the rate at which a confusable
object is called armed places the 35 m model above the original 75 m model at 0.50 and below it at
0.60 and 0.75, and the rate at which an unarmed person is called armed does the same at 0.75 (0.076
against 0.085); against its twin the 35 m model stays above at 0.50 and 0.60 and level at 0.75
(0.132 each). By the condition stated above, the comparison between the 35 m model and the original
75 m model is therefore an artefact of annotation, and those rates are reported at the three
thresholds (Section 9.5); the comparison with the matched twin, which does not reverse, is the one
that carries the argument.

**Seed dependence.** A single settlement seed, and a single training run per model, may be
favourable by chance. The check is repetition of the protocol across independent seeds with the
between-seed dispersion reported alongside the mean; if that dispersion is of the same order as the
differences reported in Section 9, those differences are not resolvable at this corpus size. Varying
the settlement seed would be a matter of compute rather than of design, since every image records
its seed and the generator reproduces the settlement exactly from it (Section 11.5 names the three
corpora whose figures it did not reproduce). What was run is narrower: five models, S-oblique-six,
the two fine-tuning models at 5 per cent, S-nadir-35 and its twin at 75 m, retrained with training
seeds 1 and 2 on a fixed corpus, and a difference was fixed in advance as resolvable when the ranges
of the two models over their three runs do not overlap. S-oblique-six reaches 0.1055, 0.0958 and
0.0887 on the benchmark, an efficacy of 15.3 per cent on average, between 14.1 and 16.7 (Section
9.3). The advantage of the generic start in fine-tuning at 5 per cent is resolvable, with means of
0.5244 against 0.4529 (Section 9.4). The difference between the 35 m model and its twin at 75 m in
the rate at which a confusable object is called armed is resolvable on the 80 new frames of Section
9.5, where the means are 0.222 against 0.134, but not on the smaller validation splits; their rates
for armed and unarmed persons are resolvable on neither. The central comparison of Section 10.4,
between S-nadir-150 and S-oblique, was not repeated, and its factor of 6.0 rests on one run per
model. The settlement seed was not varied: each repetition retrains on the same corpus, so the
dispersion measured is that of training, not of the realisation of the scene.


<!-- ARQUIVO DE ORIGEM: 09b-technical-limitations.md -->

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


<!-- ARQUIVO DE ORIGEM: 07-conclusion.md -->

## 12. Conclusion

### Limitations

This study is conceptual rather than operational, and that status shapes every limitation that follows. Synthetic corpora have been generated and detectors trained on them, but nothing has been validated against imagery of Jacarezinho or of any other favela: the transfer figures are obtained on a public benchmark that is not a favela (Section 11.1), where the strategy reaches at best 15.3 per cent of the real-data ceiling on average over three runs and costs accuracy once real images are available (Section 9.4). Of the four acquisition conditions the objective names, only altitude was varied for the armed and unarmed distinction, and only on synthetic imagery; camera geometry was varied for person detection alone, illumination in an image statistic and a per-regime detection test (Section 10.3), and a single sensor was simulated, at two render resolutions. The transfer measured is that of person detection, since we found no public aerial benchmark that annotates a carried firearm at the altitudes studied here.

The autoethnographic material discussed in the Methodology section is a second, unavoidable limitation. One researcher's operational familiarity with Jacarezinho comes filtered through a policing role, and the study has been explicit that this yields a partial account: attentive to tactical navigability, choke points, and lines of sight, and correspondingly less attentive to the aspects of the built environment that matter most to the people who live there. The triangulation against journalistic, human-rights, and academic sources described earlier mitigates this bias; it does not remove it. A single institutional vantage point, however well triangulated, is not a substitute for resident testimony, and none was collected.

Relatedly, the contextual material assembled in Sections 3 and 4 relies heavily on journalistic and institutional reporting (ISP-RJ statistics, Fórum Brasileiro de Segurança Pública data, reports by human-rights organizations and news coverage of Operação Exceptis and Operação Contenção) rather than on peer-reviewed scholarship, for the straightforward reason that some of the events cited occurred within the last several months and have not yet been absorbed into the academic literature. Population figures for Jacarezinho illustrate the same problem at smaller scale: official census data, municipal estimates, and community sources diverge by tens of thousands of residents, and this article has no independent means of resolving that discrepancy.

Finally, the study concerns one favela in one city. Jacarezinho's topography, its population density, its specific pattern of Comando Vermelho control, and its recent operational history are not necessarily representative of Rio's other favelas, let alone of vertically dense informal settlements elsewhere in Brazil or Latin America. Nothing in the argument developed here licenses an inference from Jacarezinho to informal urban verticality in general. The acquisition limits of Sections 8 to 11 rest on ground sampling distance and on generic synthetic settlements rather than on properties of Jacarezinho, and it is in that sense that the title speaks of dense favelas.

### Delimitations

Several boundaries were set deliberately, and it is worth distinguishing them from the limitations above, since they reflect choices rather than constraints imposed by circumstance.

The study does not collect or propose to collect field data from an active informal settlement using drones, cameras, or any other means during this phase of the research. This was a design decision, made explicitly because a policing-affiliated researcher cannot ethically obtain community consent for imagery collection inside a community with the documented history of police violence described in Section 3. Any real-world data collection is deferred, by design, to a later stage requiring independent ethics review and community engagement conducted outside the police institution, a constraint stated in the Methodology section and treated here as a boundary of the current study rather than something left for future work to relax.

The study is similarly delimited to the technical question of what acquisition conditions the armed and unarmed distinction requires and what synthetic training recovers of it, and to the conceptual question of whether machine vision can represent vertical informal structure, not to the question of how such a model would be operationally deployed, integrated into an existing UAV platform, or governed once built. Questions of flight authorization, airspace regulation, chain-of-custody for any imagery produced, and integration with the broader public-security apparatus in Rio de Janeiro (including with the drone-countermeasure and UAV-intelligence capabilities Rio's Civil Police is already developing) fall outside the scope of this article.

The comparative literature review in the Introduction and Section 2 was restricted to UAV trajectory planning, aerial policing, machine vision applied to informal settlements, and synthetic training for aerial detection. It does not extend to the broader literatures on urban surveillance technology, predictive policing, or the sociology of favela pacification programs, each of which bears on this study's argument but would have diluted its specific technical focus had it been incorporated at length.

### Implications and Directions for Future Research

The most immediate implication of this study is that closing the gap it identifies (between UAV research organized around policing and UAV research organized around informal-settlement mapping) cannot happen inside a single article, and probably should not happen inside a police institution alone. The ethical protocol adopted here treats that as a starting constraint rather than an obstacle to be engineered around. A natural next step is therefore not technical refinement of the model but the design of the independent ethics review and community engagement process this article defers to: what body would conduct it, what form community consent would need to take in a territory under active criminal-organization control, and whether meaningful consent is even obtainable under those conditions are questions this study leaves open rather than presumes to answer.

On the technical side, the domain-randomisation strategy proposed here has been built and partially tested: the generator, the corpora and the evaluation protocol are reported in Sections 7 to 10, against a public aerial benchmark. A limited fine-tuning stage on that benchmark is reported separately in Section 9.4, where a generic initialisation outperformed the synthetic one at both volumes of real data, and training on synthetic and real imagery together fell short of training on the real imagery alone. What remains untested is specific rather than general: a measurement of the distinction at 150 m that passes its validity condition (Section 9.5), the controlled measurement of training scale described in Section 7.6, the full learning curve over corpus size of Section 10.1, the hard-sun ablation specified in Section 10.3, variation of the settlement seed rather than of training alone (Section 10.6), and a longer or partly frozen fine-tuning schedule that would test the explanation offered in Section 9.4. Beyond those lies the half of the work that has no evaluation infrastructure at all, the morphological task of Section 11.3, and, separately from any of it, validation against real imagery of the territory, which is the stage the ethics process described above would have to precede. An alternative to the public benchmark fixed in Section 7.7 would be publicly available, already-consented imagery of informal settlements elsewhere (Kigali, Slovo Park, and comparable sites already appear in the published literature), which would test generalisation to dense, irregular, sloped construction on a scene type closer to the target than VisDrone offers.

The population discrepancies noted above point to a further line of inquiry that has value independent of this study's security framing: better demographic and structural characterization of Rio's largest favelas would serve urban planning, disaster-risk assessment, and resource allocation regardless of whether it is ever put to security use, and researchers working in that tradition (the building-height and population-density literature discussed in Section 2) are better positioned to pursue it than a study anchored in a policing perspective.

Finally, the four-stage progression sketched in the Introduction (flat urban terrain, mountainous terrain, formal three-dimensional urban space, and vertically complex informal urban space) is offered as a starting point, not a finished framework. Testing it against other verticalized informal settlements, in Rio and beyond, would clarify whether the four-stage progression holds generally or whether Jacarezinho's specific combination of dense vertical construction and decades of factional territorial control makes it an unusually hard case rather than a representative one. Either finding would be useful, and neither can be established from a single site.

### Closing

This article set out to ask under what acquisition conditions, and at what cost in transfer,
synthetic imagery of a dense favela supports telling an armed person from an unarmed one from the
air, and what answering that question responsibly requires. Three things follow from the work
reported above.

The first is that the constraints measured here are not the ones the field usually discusses. At the
ground sampling distance of the acquisition specified in Section 7.3, a person is a few tens of
pixels of low-contrast texture, the silhouette of that target is set by where the camera is placed
rather than by how faithfully the scene is built, and under hard sun, the cloud-free condition that
aerial survey specifications have conventionally required (National Geodetic Survey, 2002; RICS,
2021), the figure shows among the lowest point estimates of contrast against local clutter of the
six regimes, and a detector trained on all six finds it hardest to detect under that regime (Section
10.3). Section 8.3 attributes this, as a hypothesis, to cast shadow in the background, which is also
the reason that guidance for three-dimensional reconstruction from drones gives for preferring an
overcast sky (Section 11.2). None of these is a question of photorealism, and none of them is
visible in any appearance-based measure of how convincing a synthetic scene looks.

The second is that synthesis buys a specific thing and not a general one. It removes the consent
problem, which in this territory is not a procedural obstacle but a substantive one, and it
introduces a transfer problem in its place. This article reports what that trade costs, on a
benchmark that is not the case study, and declines to extrapolate from it. Where some real imagery
does exist, the synthetic corpus neither substituted for it nor added to it: on that benchmark a
generic initialisation given the same real images outperformed the synthetic one at both volumes, at
5 per cent by more than the spread between three training runs, and mixing the synthetic corpus into
the real training data lowered accuracy as well.

The third is the one that matters most for the argument about dual use. The capability this pipeline
could be built towards is not uniformly available: it has been measured at 75 m and 35 m, on
synthetic imagery only, and is argued, though not shown, to disappear at 150 m, as a function of
acquisition parameters that are measurable in advance. Where it appears, it carries a false-alarm
rate against figures carrying ordinary objects, and it does not sharpen as the camera descends: at
35 m the detector calls more confusable objects armed than its twin at 75 m, not fewer, a difference
that replicates on new frames and across three training runs, although on the validation split it
vanishes at the strictest overlap threshold (Section 9.5). A claim that a system can distinguish an
armed from an unarmed person from the air is, at the altitudes and sensors described here, a claim
that can be checked before it is believed, and this article declines to make it. Stating the
conditions under which a capability has not been shown, and why, is a contribution of the same kind
as demonstrating one that has, and in this domain it is the more useful of the two.

What remains open is not primarily technical. A system that can tell an armed person from an unarmed
one and a system that is safe to point at Jacarezinho are different objects, and nothing in the
engineering reported here decides the second. That decision belongs to a process that includes the
residents of the territory, and it has not taken place.


<!-- ARQUIVO DE ORIGEM: 08-references.md -->

## 13. References

- Gram-Hansen, B., Helber, P., Varatharajan, I., Azam, F., Coca-Castro, A., Kopackova, V., & Bilinski, P. (2019). *Mapping Informal Settlements in Developing Countries using Machine Learning and Low Resolution Multi-spectral Data.* AIES '19 / arXiv:1901.00861.
- Hu, J., Huang, X., Ren, T., & Zhang, L. (2025). *Urban Informal Settlement Classification via Cross-Scale Hierarchical Perception Fusion Network Using Remote Sensing and Street View Images.* Remote Sensing, 17(23), 3841.
- Tobin, J., Fong, R., Ray, A., Schneider, J., Zaremba, W., & Abbeel, P. (2017). *Domain randomization for transferring deep neural networks from simulation to the real world.* IROS 2017.
- Prakash, A., Boochoon, S., Brophy, M., Acuna, D., Cameracci, E., State, G., et al. (2019). *Structured Domain Randomization: Bridging the Reality Gap by Context-Aware Synthetic Data.* ICRA 2019.
- Human Rights Watch (2021). *Raid in Rio de Janeiro Leaves 28 Dead.*
- Inter-American Commission on Human Rights (2021). *IACHR Condemns Police Violence in Favela Jacarezinho in Rio de Janeiro.*

Agência Brasil. (2025, April 3). STF retoma julgamento da ADPF das Favelas. https://agenciabrasil.ebc.com.br/justica/noticia/2025-04/stf-retoma-julgamento-da-adpf-das-favelas-0

Agência Nacional de Aviação Civil. (2026). *RBAC nº 100, Emenda nº 00: Requisitos gerais para aeronaves não tripuladas de uso civil* (Resolução nº 805, de 15 de junho de 2026). https://pergamum.anac.gov.br/pergamum/vinculos/RBAC100EMD00.pdf

Agência Pública. (2025, October 29). RJ tem operação mais letal de sua história seis meses após reviravolta na ADPF das Favelas. https://apublica.org/2025/10/rj-tem-operacao-mais-letal-de-sua-historia-seis-meses-apos-reviravolta-na-adpf-das-favelas/

Agrawal, P., Ratnoo, A., & Ghose, D. (2017). Inverse optical flow based guidance for UAV navigation through urban canyons. *Aerospace Science and Technology, 68*, 163-178. https://doi.org/10.1016/j.ast.2017.05.012

Al Jazeera. (2021, May 8). Death toll from police raid on Rio de Janeiro favela increases. https://www.aljazeera.com/news/2021/5/8/death-toll-from-police-raid-on-rio-de-janeiro-favela-increases

AlJundi, Z., Alsubaie, S., Faheem, M. H., Almarashi, R. M., Qazi, E.-u.-H., & Kim, J. H. (2025). Dangerous objects detection using deep learning and first responder drone. *International Journal of Digital Crime and Forensics, 16*(1), 1-18. https://doi.org/10.4018/ijdcf.367034

Barekatain, M., Marti, M., Shih, H.-F., Murray, S., Nakayama, K., Matsuo, Y., & Prendinger, H. (2017). Okutama-Action: An aerial view video dataset for concurrent human action detection. In *2017 IEEE Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)* (pp. 2153-2160). https://doi.org/10.1109/CVPRW.2017.267

Barisic, A., Petric, F., & Bogdan, S. (2022). Sim2Air: Synthetic aerial dataset for UAV monitoring. *IEEE Robotics and Automation Letters, 7*(2), 3757-3764. https://doi.org/10.1109/LRA.2022.3147337

Barros, M. (2026, July 30). Anuário aponta avanço da violência contra policiais no Rio de Janeiro. Defesa em Foco. https://www.defesaemfoco.com.br/anuario-aponta-avanco-da-violencia-contra-policiais-no-rio-de-janeiro/

Broyles, D., Hayner, C. R., & Leung, K. (2022). WiSARD: A labeled visual and thermal image dataset for wilderness search and rescue. In *2022 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)* (pp. 9467-9474). https://doi.org/10.1109/IROS47612.2022.9981298

Caminhos Languages. (2025). The largest favelas in Rio de Janeiro. https://caminhoslanguages.com/blog/favelas-in-rio-de-janeiro/

Causa Operária. (2025, April). STF julga ADPF 635 autorizando o terror policial contra favelas. https://causaoperaria.org.br/2025/stf-julga-adpf-635-autorizando-o-terror-policial-contra-favelas/

CBS News. (2025, November 4). Brazil's president calls for investigation after 121 killed in police operation against gang: "There was a massacre." https://www.cbsnews.com/amp/miami/news/brazil-president-lula-probe-police-operation-gang-massacre

Chen, Z., Liu, Y., Hu, S., Zhang, X., & Pan, Y. (2025). Deterring street crimes using aerial police: Data-driven joint station deployment and patrol path planning for policing UAVs. *Drones, 9*(6), Article 449. https://doi.org/10.3390/drones9060449

CNN. (2026, September 9). Drones are becoming organized crime's weapon of choice in Latin America. Governments are struggling to keep up. https://www.cnn.com/2026/09/09/americas/drones-crime-latin-america-latam-intl

Couto, C. (2025, October 28). Megaoperação tenta prender 100 membros do CV no Alemão e Penha (RJ). CNN Brasil. https://www.cnnbrasil.com.br/nacional/sudeste/rj/rj-megaoperacao-com-mais-de-2-mil-policiais-toma-alemao-e-penha/

Couto, C., & Figueiredo, C. (2025, October 30). Polícia atualiza para 121 o número de mortos em megaoperação no Rio. CNN Brasil. https://www.cnnbrasil.com.br/nacional/sudeste/rj/policia-atualiza-numero-de-mortos-em-megaoperacao-no-rio/

da Silva, A. A., Kormann da Silva, I. F., & Westerholt, R. (2024). Mapping the margins: A systematic scoping review of the impact of digital mapping on public participation in informal settlements. *Habitat International, 147*, Article 103040. https://doi.org/10.1016/j.habitatint.2024.103040

Dandois, J. P., Olano, M., & Ellis, E. C. (2015). Optimal altitude, overlap, and weather conditions for computer vision UAV estimates of forest structure. *Remote Sensing, 7*(10), 13895-13920. https://doi.org/10.3390/rs71013895

Dare, P. M. (2005). Shadow analysis in high-resolution satellite imagery of urban areas. *Photogrammetric Engineering & Remote Sensing, 71*(2), 169-177. https://doi.org/10.14358/PERS.71.2.169

Departamento de Controle do Espaço Aéreo. (2026). *ICA 100-40: Aeronaves não tripuladas e o acesso ao espaço aéreo brasileiro* (Portaria DECEA nº 2.094/DNOR8, de 18 de março de 2026). Comando da Aeronáutica. https://www.gov.br/defesa/pt-br/assuntos/aerolevantamento/arquivos/2026/ica-100-40-publicada-port-2094-dnor8-18-03-2026-bca-058-30-03-2026.pdf

Du, D., Qi, Y., Yu, H., Yang, Y., Duan, K., Li, G., Zhang, W., Huang, Q., & Tian, Q. (2018). The unmanned aerial vehicle benchmark: Object detection and tracking. In *Computer Vision, ECCV 2018* (Lecture Notes in Computer Science, pp. 375-391). Springer. https://doi.org/10.1007/978-3-030-01249-6_23

Du, S., Xing, J., Wang, S., Wei, L., & Zhang, Y. (2024). STMNet: Scene classification-assisted and texture feature-enhanced multiscale network for large-scale urban informal settlement extraction from remote sensing images. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 17*, 13169-13187. https://doi.org/10.1109/JSTARS.2024.3432200

European Union Aviation Safety Agency. (2019). *Acceptable Means of Compliance (AMC) and Guidance Material (GM) to Part-UAS: UAS operations in the 'open' and 'specific' categories* (Issue 1, ED Decision 2019/021/R). https://www.easa.europa.eu/sites/default/files/dfu/AMC%20&%20GM%20to%20Part-UAS%20%E2%80%94%20Issue%201.pdf

Faheem, M. H., Haq, Q. E. U., Khan, T. M., & Kim, J. H. (2025). Deep-learning-based weapon detection using drones equipped with infrared and color cameras. *International Journal of Digital Crime and Forensics, 17*(1), 1-16. https://doi.org/10.4018/ijdcf.393088

Falcão, T., & Couto, C. (2025, October 29). Número de mortes em megaoperação no Rio passa de 130, diz defensoria. CNN Brasil. https://www.cnnbrasil.com.br/nacional/sudeste/rj/numero-de-mortes-em-megaoperacao-no-rio-passa-de-120-diz-defensoria/

Fichino, D. (2025). *Operação Contenção: Análise da operação policial mais letal da história do estado do Rio de Janeiro à luz dos padrões internacionais de uso da força e de investigações* [Report]. Justiça Global. https://www.global.org.br/wp/wp-content/uploads/2025/11/2025-11-07-JG-RELATORIO-OPERACAO-CONTENCAO_VF-compactado.pdf

Fórum Brasileiro de Segurança Pública. (2025). *19º Anuário Brasileiro de Segurança Pública: 2025*. https://publicacoes.forumseguranca.org.br/handle/fbsp/279

Fórum Brasileiro de Segurança Pública. (2026). *Anuário Brasileiro de Segurança Pública 2026* (Ano 20). https://forumseguranca.org.br/wp-content/uploads/2026/07/anuario-2026.pdf

Gazeta do Povo. (2025, April 10). "ADPF das Favelas": decisão final do STF vai melhorar ou piorar de vez a segurança do Rio? https://www.gazetadopovo.com.br/vida-e-cidadania/adpf-635-decisao-final-stf-vai-melhorar-ou-piorar-rio/

GeoCue. (2025, November 27). *Flight planning: Sun angle*. GeoCue Support Knowledge Base. https://support.geocue.com/flight-planning-sun-angle/

Gevaert, C. M., Persello, C., Sliuzas, R., & Vosselman, G. (2016). Classification of informal settlements through the integration of 2D and 3D features extracted from UAV data. *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences, III-3*, 317-324. https://doi.org/10.5194/isprs-annals-III-3-317-2016

Grillo, I. (2014, September 10). Brazil's Red Command and the police who fight them. InSight Crime. https://insightcrime.org/news/analysis/brazils-red-command-rio-police-favelas-slums/

He, K., Girshick, R., & Dollár, P. (2019). Rethinking ImageNet pre-training. In *2019 IEEE/CVF International Conference on Computer Vision (ICCV)* (pp. 4917-4926). https://doi.org/10.1109/ICCV.2019.00502

Hinterstoisser, S., Lepetit, V., Wohlhart, P., & Konolige, K. (2019). On pre-trained image features and synthetic images for deep learning. In *Computer Vision, ECCV 2018 Workshops* (Lecture Notes in Computer Science, pp. 682-697). Springer. https://doi.org/10.1007/978-3-030-11009-3_42

Hnoohom, N., Chotivatunyu, P., & Jitpattanakul, A. (2022). ACF: An armed CCTV footage dataset for enhancing weapon detection. *Sensors, 22*(19), Article 7158. https://doi.org/10.3390/s22197158

Horváth, D., Erdős, G., Istenes, Z., Horváth, T., & Földi, S. (2023). Object detection using Sim2Real domain randomization for robotic applications. *IEEE Transactions on Robotics, 39*(2), 1225-1243. https://doi.org/10.1109/TRO.2022.3207619

Human Rights Watch. (2021, May 31). Brazil: Investigate Rio police command for deadly raid. https://www.hrw.org/news/2021/05/31/brazil-investigate-rio-police-command-deadly-raid

InSight Crime. (2026, September 11). Red Command (Comando Vermelho). https://insightcrime.org/brazil-organized-crime-news/red-command-profile/

Instituto de Segurança Pública do Rio de Janeiro. (n.d.-a). *Estatísticas de segurança: Série histórica anual no estado desde 1991 (taxas por 100 mil habitantes)* [Data set]. Retrieved September 30, 2026, from https://www.ispdados.rj.gov.br/Arquivos/BaseEstadoTaxaAno.csv

Instituto de Segurança Pública do Rio de Janeiro. (n.d.-b). *Estatísticas de segurança: Série histórica mensal por área de delegacia desde 01/2003* [Data set]. Retrieved September 30, 2026, from https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv

Jiang, C., Zhou, X., Chen, H., & Liu, T. (2026). UAV positioning using GNSS: A review of the current status. *Drones, 10*(2), Article 91. https://doi.org/10.3390/drones10020091

JOTA. (2025, April 13). O julgamento da ADPF das Favelas: avanços, alertas e inovações. https://tagteam.harvard.edu/hub_feeds/3884/feed_items/13579751/content

Kiefer, B., Ott, D., & Zell, A. (2022). Leveraging synthetic data in object detection on unmanned aerial vehicles. *2022 26th International Conference on Pattern Recognition (ICPR)*, 3564-3571. https://doi.org/10.1109/ICPR56361.2022.9956710

Leitão, J. P., Moy de Vitry, M., Scheidegger, A., & Rieckermann, J. (2016). Assessing the quality of digital elevation models obtained from mini unmanned aerial vehicles for overland flow modelling in urban areas. *Hydrology and Earth System Sciences, 20*(4), 1637-1653. https://doi.org/10.5194/hess-20-1637-2016

Lessing, B. (2008). As facções cariocas em perspectiva comparativa. *Novos Estudos CEBRAP*, (80), 43-62. https://doi.org/10.1590/S0101-33002008000100004

Li, T., Liu, J., Zhang, W., Ni, Y., Wang, W., & Li, Z. (2021). UAV-Human: A large benchmark for human behavior understanding with unmanned aerial vehicles. In *2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (pp. 16261-16270). https://doi.org/10.1109/CVPR46437.2021.01600

Li, Z., Yellapragada, S., Bhadresh Doshi, K., Mhasakar, P. M., Fan, H., Wei, J., Blasch, E., Zhang, B., & Ling, H. (2025). CCTV-Gun: Benchmarking handgun detection in CCTV images. In *Dynamic Data Driven Applications Systems* (Lecture Notes in Computer Science, pp. 171-181). Springer. https://doi.org/10.1007/978-3-031-94895-4_18

Liao, F., Liu, Y., Xu, W., Wang, X., Liu, G., Yang, K., & Li, J. (2026). Bridging the Sim2Real gap in UAV remote sensing: A high-fidelity synthetic data framework for vehicle detection. *Remote Sensing, 18*(2), 361. https://doi.org/10.3390/rs18020361

Lim, J., Al Jobayer, M. I., Baskaran, V. M., Lim, J. M., See, J., & Wong, K. (2021). Deep multi-level feature pyramids: Application for non-canonical firearm detection in video surveillance. *Engineering Applications of Artificial Intelligence, 97*, Article 104094. https://doi.org/10.1016/j.engappai.2020.104094

Lima, L., Andrade, F., Djenouri, Y., Pfeiffer, C., & Moura, M. (2025). Optimizing object detection for maritime search and rescue: Progressive fine-tuning of YOLOv9 with real and synthetic data. In *Proceedings of the 17th International Conference on Agents and Artificial Intelligence* (pp. 209-216). SCITEPRESS. https://doi.org/10.5220/0013112700003890

Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot sensors. *Remote Sensing, 17*(4), Article 606. https://doi.org/10.3390/rs17040606

Martinez-Esteso, J. P., Castellanos, F. J., Rosello, A., Calvo-Zaragoza, J., & Gallego, A. J. (2025). On the use of synthetic data for body detection in maritime search and rescue operations. *Engineering Applications of Artificial Intelligence, 139*, Article 109586. https://doi.org/10.1016/j.engappai.2024.109586

McCormac, J., Handa, A., Leutenegger, S., & Davison, A. J. (2017). SceneNet RGB-D: Can 5M synthetic images beat generic ImageNet pre-training on indoor segmentation? In *2017 IEEE International Conference on Computer Vision (ICCV)* (pp. 2697-2706). https://doi.org/10.1109/ICCV.2017.292

Mensink, T., Uijlings, J., Kuznetsova, A., Gygli, M., & Ferrari, V. (2022). Factors of influence for transfer learning across diverse appearance domains and task types. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 44*(12), 9298-9314. https://doi.org/10.1109/TPAMI.2021.3129870

Misse, M. (2011). Crime organizado e crime comum no Rio de Janeiro: Diferenças e afinidades. *Revista de Sociologia e Política, 19*(40), 13-25. https://doi.org/10.1590/S0104-44782011000300003

Mistler-Ferguson, S. (2022, January 27). Brazil tries to reclaim Rio's favelas: Ad infinitum. InSight Crime. https://insightcrime.org/news/brazil-tries-reclaim-rio-favelas-ad-infinitum/

Movisafe América Latina. (2025, March). ADPF 635: A protection for Rio's communities — or a green light for the expansion of organized crime? https://movisafe-americalatina.com/en/adpf-635-a-protection-for-rios-communities-or-a-green-light-for-the-expansion-of-organized-crime/

National Geodetic Survey. (2002). *General specifications for aeronautical surveys, Volume II: Airport aerial photography* (Version 14). National Oceanic and Atmospheric Administration. https://www.ngs.noaa.gov/AERO/GenSpecVol_II_v14.pdf

OPEB. (2025, November 12). Crise, calamidade e exceção: os limites dos direitos humanos na megaoperação nos complexos do Alemão e da Penha. https://opeb.org/2025/11/12/crise-calamidade-e-excecao-os-limites-dos-direitos-humanos-na-megaoperacao-nos-complexos-do-alemao-e-da-penha/

Operating limitations for small unmanned aircraft, 14 C.F.R. § 107.51. Retrieved September 30, 2026, from https://www.law.cornell.edu/cfr/text/14/107.51

Pérez-Hernández, F., Tabik, S., Lamas, A., Olmos, R., Fujita, H., & Herrera, F. (2020). Object detection binary classifiers methodology based on deep learning to identify small objects handled similarly: Application in video surveillance. *Knowledge-Based Systems, 194*, Article 105590. https://doi.org/10.1016/j.knosys.2020.105590

Pix4D. (2022, April 20). *5 key things we wish we knew before flying a drone*. Pix4D Blog. https://www.pix4d.com/blog/tips-for-successful-drone-flights

Pix4D. (n.d.). *Best practices for image acquisition and photogrammetry*. PIX4D Documentation. Retrieved September 30, 2026, from https://support.pix4d.com/hc/best-practices-for-image-acquisition-and-photogrammetry

Rasoulie, F., & Pashazadeh, S. (2026). 3D UAV path optimization using a task-allocation and archive-guided mutation particle swarm optimization algorithm. *Scientific Reports, 16*(1), Article 24356. https://doi.org/10.1038/s41598-026-42372-8

Reilly, V., Solmaz, B., & Shah, M. (2010). Geometric constraints for human detection in aerial imagery. In *Computer Vision, ECCV 2010* (Lecture Notes in Computer Science, pp. 252-265). Springer. https://doi.org/10.1007/978-3-642-15567-3_19

Reuters. (2025, November 22). Fifth police officer dies after Brazil's deadliest anti-drug raid. Investing.com. https://www.investing.com/news/world-news/fifth-police-officer-dies-after-brazils-deadliest-antidrug-raid-4374110

RioOnWatch. (2019, May 3). Jacarezinho from a resident's view. https://rioonwatch.org/?p=31407

Royal Institution of Chartered Surveyors. (2021). *Earth observation and aerial surveys* (6th ed.; RICS professional standard, global, reissued January 2023). RICS. https://www.rics.org/content/dam/ricsglobal/documents/standards/Earth%20observation%20and%20aerial%20surveys_reissue%20Jan%202023.pdf

Ruiz-Santaquiteria, J., Muñoz, J. D., Maigler, F. J., Deniz, O., & Bueno, G. (2024). Firearm-related action recognition and object detection dataset for video surveillance systems. *Data in Brief, 52*, Article 110030. https://doi.org/10.1016/j.dib.2024.110030

Salazar González, J. L., Zaccaro, C., Álvarez-García, J. A., Soria Morillo, L. M., & Sancho Caparrini, F. (2020). Real-time gun detection in CCTV: An open problem. *Neural Networks, 132*, 297-308. https://doi.org/10.1016/j.neunet.2020.09.013

Shen, Y.-T., Lee, H., Kwon, H., & Bhattacharyya, S. S. (2023b). Progressive transformation learning for leveraging virtual images in training. In *2023 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (pp. 835-844). https://doi.org/10.1109/CVPR52729.2023.00087

Shen, Y.-T., Lee, Y., Kwon, H., Conover, D. M., Bhattacharyya, S. S., Vale, N., Gray, J. D., Leong, G. J., Evensen, K., & Skirlo, F. (2023a). Archangel: A hybrid UAV-based human detection benchmark with position and pose metadata. *IEEE Access, 11*, 80958-80972. https://doi.org/10.1109/ACCESS.2023.3299235

Sithole, L., & Mhangara, P. (2025). Classification of informal settlements using novel object-based machine learning algorithms and drone imagery, Slovo Park, Johannesburg, South Africa. *International Journal of Remote Sensing*. https://doi.org/10.1080/01431161.2025.2518504

Slade, G., Anderson, K., Graham, H. A., & Cunliffe, A. M. (2025). Repeated drone photogrammetry surveys demonstrate that reconstructed canopy heights are sensitive to wind speed but relatively insensitive to illumination conditions. *International Journal of Remote Sensing, 46*(1), 24-41. https://doi.org/10.1080/01431161.2024.2377832

Sousa, R. (2026). Mortes violentas intencionais no Brasil em 2025: Entre avanços históricos e desafios persistentes. Fórum Brasileiro de Segurança Pública. https://fontesegura.forumseguranca.org.br/mortes-violentas-intencionais-no-brasil-em-2025-entre-avancos-historicos-e-desafios-persistentes/

Sullivan, J. P., & da Cruz, J. de A. (2025, November 2). Third generation gangs strategic note no. 59: Police raid "Megaoperação Contenção" on Comando Vermelho leads to 132 killed. Small Wars Journal. https://smallwarsjournal.com/2025/11/02/third-generation-gangs-strategic-note-no-59-police-raid-megaoperacao-contencao-on-comando-vermelho-leads-to-132-killed/

Sullivan, J. P., Bunker, R., & da Cruz, J. de A. (2021, May 26). Third generation gangs strategic note no. 36: High casualty civil police raid in Rio de Janeiro's Jacarezinho favela raises human rights concerns. Small Wars Journal. https://smallwarsjournal.com/2021/05/26/third-generation-gangs-strategic-note-no-36-high-casualty-civil-police-raid-rio-de/

Supremo Tribunal Federal. (2025a, March 26). STF avança em solução conjunta para letalidade policial no RJ, diz presidente. https://noticias.stf.jus.br/postsnoticias/stf-avanca-em-solucao-conjunta-para-letalidade-policial-no-rj-diz-presidente-do-stf/

Supremo Tribunal Federal. (2025b, April 3). ADPF das Favelas: STF homologa parcialmente plano do Estado do Rio de Janeiro para reduzir letalidade policial. https://noticias.stf.jus.br/postsnoticias/adpf-das-favelas-stf-homologa-parcialmente-plano-do-estado-do-rio-de-janeiro-para-reduzir-letalidade-policial/

Torkst, C., Rangel, P., & Efigenio, J. (2026). *Dual-UAV dataset for detection and localization of armed individuals* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18746168

Tremblay, J., Prakash, A., Acuna, D., Brophy, M., Jampani, V., Anil, C., To, T., Cameracci, E., Boochoon, S., & Birchfield, S. (2018). Training deep networks with synthetic data: Bridging the reality gap by domain randomization. In *2018 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*. https://doi.org/10.1109/CVPRW.2018.00143

Wang, D., & Qian, X. (2026). Police UAV path planning method based on improved PSO using AFS and HJS. *Scientific Reports, 16*(1), Article 12417. https://doi.org/10.1038/s41598-026-40670-9

Wang, Z., Dai, Z., Póczos, B., & Carbonell, J. (2019). Characterizing and avoiding negative transfer. In *2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (pp. 11285-11294). https://doi.org/10.1109/CVPR.2019.01155

Watson, C. S., & Elliott, J. R. (2025). Narrowing the gap for city building height predictions. *Scientific Reports, 15*(1), Article 29913. https://doi.org/10.1038/s41598-025-15929-2

Wen, L., Du, D., Zhu, P., Hu, Q., Wang, Q., Bo, L., & Lyu, S. (2021). Detection, tracking, and counting meets drones in crowds: A benchmark. In *2021 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (pp. 7808-7817). https://doi.org/10.1109/CVPR46437.2021.00772

Xu, G. (2025). A comparative study of drones path planning and bezier curve optimization based on multi-strategy search algorithm. *PLOS One, 20*(7), Article e0326633. https://doi.org/10.1371/journal.pone.0326633

Yan, S., Hsieh, T.-H., & Lai, Y.-C. (2025). Enhancing public safety through integrated UAV and police patrols. *Socio-Economic Planning Sciences, 102*, Article 102334. https://doi.org/10.1016/j.seps.2025.102334

Yim, J., Lee, H., Eum, S., Shen, Y.-T., Zhang, Y., Kwon, H., & Bhattacharyya, S. S. (2026). SynPlay: Large-scale synthetic human data with real-world diversity for aerial-view perception. In *2026 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)* (pp. 938-947). https://doi.org/10.1109/WACV61042.2026.00098

Zhu, P., Wen, L., Du, D., Bian, X., Fan, H., Hu, Q., & Ling, H. (2022). Detection and tracking meet drones challenge. *IEEE Transactions on Pattern Analysis and Machine Intelligence, 44*(11), 7380-7399. https://doi.org/10.1109/TPAMI.2021.3119563
