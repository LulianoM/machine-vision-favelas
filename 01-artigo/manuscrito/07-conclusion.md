## Conclusion

### Limitations

This study is conceptual rather than operational, and that status shapes every limitation that follows. At the time of writing, a synthetic corpus has been generated and detectors have been trained on it, with the results reported in Sections 9 and 10. What has not been established is performance on real imagery of Jacarezinho or of any other favela: the transfer figures reported here are obtained on a public aerial benchmark that is not a favela, for the reasons set out in Section 11.2, and no output of this work has been validated against imagery of the case study territory. What is offered here is an architecture, a training strategy, and a measurement of what that strategy transfers to a public benchmark that is not the target domain. Whether it closes the sim-to-real gap for vertically stacked, self-built construction as such, rather than for the dense urban scenes the benchmark records, is an empirical question this article does not answer, for the reason given in Section 11.2.

The autoethnographic material discussed in the Methodology section is a second, unavoidable limitation. One researcher's operational familiarity with Jacarezinho comes filtered through a policing role, and the study has been explicit that this yields a partial account: attentive to tactical navigability, choke points, and lines of sight, and correspondingly less attentive to the aspects of the built environment that matter most to the people who live there. The triangulation against journalistic, human-rights, and academic sources described earlier mitigates this bias; it does not remove it. A single institutional vantage point, however well triangulated, is not a substitute for resident testimony, and none was collected.

Relatedly, the contextual material assembled in Sections 3 and 4 relies heavily on journalistic and institutional reporting, ISP-RJ statistics, Fórum Brasileiro de Segurança Pública data, human-rights organizations, news coverage of Operação Exceptis and Operação Contenção, rather than peer-reviewed scholarship, for the straightforward reason that some of the events cited occurred within the last several months and have not yet been absorbed into the academic literature. Population figures for Jacarezinho illustrate the same problem at smaller scale: official census data, municipal estimates, and community sources diverge by tens of thousands of residents, and this article has no independent means of resolving that discrepancy.

Finally, the study concerns one favela in one city. Jacarezinho's topography, its population density, its specific pattern of Comando Vermelho control, and its recent operational history are not necessarily representative of Rio's other favelas, let alone of vertically dense informal settlements elsewhere in Brazil or Latin America. Nothing in the argument developed here licenses an inference from Jacarezinho to informal urban verticality in general.

### Delimitations

Several boundaries were set deliberately, and it is worth distinguishing them from the limitations above, since they reflect choices rather than constraints imposed by circumstance.

The study does not collect or propose to collect field data from an active informal settlement using drones, cameras, or any other means during this phase of the research. This was a design decision, made explicitly because a policing-affiliated researcher cannot ethically obtain community consent for imagery collection inside a community with the documented history of police violence described in Section 3. Any real-world data collection is deferred, by design, to a later stage requiring independent ethics review and community engagement conducted outside the police institution, a constraint stated in the Methodology section and treated here as a boundary of the current study rather than something left for future work to relax.

The study is similarly delimited to the technical question of what acquisition conditions the armed and unarmed distinction requires and what synthetic training recovers of it, and to the conceptual question of whether machine vision can represent vertical informal structure, not to the question of how such a model would be operationally deployed, integrated into an existing UAV platform, or governed once built. Questions of flight authorization, airspace regulation, chain-of-custody for any imagery produced, and integration with the broader public-security apparatus in Rio de Janeiro (including with the drone-countermeasure and UAV-intelligence capabilities Rio's Civil Police is already developing) fall outside the scope of this article.

The comparative literature review in Section 2 was restricted to UAV trajectory planning, aerial policing, and machine vision applied to informal settlements. It does not extend to the broader literatures on urban surveillance technology, predictive policing, or the sociology of favela pacification programs, each of which bears on this study's argument but would have diluted its specific technical focus had it been incorporated at length.

### Implications and Directions for Future Research

The most immediate implication of this study is that closing the gap it identifies (between UAV research organized around policing and UAV research organized around informal-settlement mapping) cannot happen inside a single article, and probably should not happen inside a police institution alone. The ethical protocol adopted here treats that as a starting constraint rather than an obstacle to be engineered around. A natural next step is therefore not technical refinement of the model but the design of the independent ethics review and community engagement process this article defers to: what body would conduct it, what form community consent would need to take in a territory under active criminal-organization control, and whether meaningful consent is even obtainable under those conditions are questions this study leaves open rather than presumes to answer.

On the technical side, the domain-randomization strategy proposed here has been built and partially tested: the generator, the corpus and the evaluation protocol are reported in Sections 7 to 10, against a public aerial benchmark. A limited fine-tuning stage on that benchmark is reported separately in Section 9.4, where a generic initialisation outperformed the synthetic one at both volumes of real data. What remains untested is specific rather than general: the controlled measurement of training scale described in Section 11.1, the full learning curve over corpus size of Section 10.1, the per-regime illumination test specified in Section 10.3, and the two checks of Section 10.6, together with joint training on synthetic and real imagery, which Section 9.4 does not test. Beyond those lies the half of the work that has no evaluation infrastructure at all, the morphological task of Section 11.4, and, separately from any of it, validation against real imagery of the territory, which is the stage the ethics process described above would have to precede. An alternative to the public benchmark fixed in Section 7.7 would be publicly available, already-consented imagery of informal settlements elsewhere (Kigali, Slovo Park, and comparable sites already appear in the published literature), which would test generalisation to dense, irregular, sloped construction on a scene type closer to the target than VisDrone offers.

The population discrepancies noted above point to a further line of inquiry that has value independent of this study's security framing: better demographic and structural characterization of Rio's largest favelas would serve urban planning, disaster-risk assessment, and resource allocation regardless of whether it is ever put to security use, and researchers working in that tradition (the building-height and population-density literature discussed in Section 2) are better positioned to pursue it than a study anchored in a policing perspective.

Finally, the four-stage progression sketched in the Introduction (flat urban terrain, mountainous terrain, formal three-dimensional urban space, and vertically complex informal urban space) is offered as a starting point, not a finished framework. Testing it against other verticalized informal settlements, in Rio and beyond, would clarify whether the four-stage progression holds generally or whether Jacarezinho's specific combination of steep topography and decades of factional territorial control makes it an unusually hard case rather than a representative one. Either finding would be useful, and neither can be established from a single site.

### Closing

This article set out to ask under what acquisition conditions an aerial system can tell an armed
person from an unarmed one over a dense self-built settlement, and what it costs to answer that
question responsibly. Three things follow from the work reported above.

The first is that the binding constraints are not the ones the field usually discusses. At the
ground sampling distance of the acquisition specified in Section 7.3, a person is a few tens of pixels
of low contrast texture, the silhouette of that target is set by where the camera is placed rather
than by how faithfully the scene is built, and the illumination condition conventionally
preferred for flying, hard sun, is the one whose cast shadow fills the background with the clutter
that competes with the figure. None of these is a question of
photorealism, and none of them is visible in any appearance-based measure of how convincing a
synthetic scene looks.

The second is that synthesis buys a specific thing and not a general one. It removes the consent
problem, which in this territory is not a procedural obstacle but a substantive one, and it
introduces a transfer problem in its place. This article reports what that trade costs, on a
benchmark that is not the case study, and declines to extrapolate from it. Where some real
imagery does exist, the synthetic corpus did not substitute for it: on that benchmark, a generic
initialisation given the same real images outperformed the synthetic one.

The third is the one that matters most for the argument about dual use. The capability this
pipeline could be built toward is not uniformly available: it appears and disappears as a function
of acquisition parameters that are measurable in advance. Where it appears, at 75 m, it carries a
false-alarm rate against residents carrying ordinary objects, and it does not sharpen as the camera
descends: at 35 m the detector calls more of every class armed, not fewer. A claim that a system can distinguish an
armed from an unarmed person from the air is, at the altitudes and sensors described here, a claim
that can be checked before it is believed, and this article declines to make it. Stating the
conditions under which a capability does not exist is a contribution of the same kind as
demonstrating one that does, and in this domain it is the more useful of the two.

What remains open is not primarily technical. A system that can tell an armed person from an
unarmed one and a system that is safe to point at Jacarezinho are different objects, and nothing
in the engineering reported here decides the second. That decision belongs to a process
that includes the residents of the territory, and it has not taken place.
