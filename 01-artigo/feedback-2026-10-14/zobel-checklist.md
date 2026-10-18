# Zobel checklist for the revision of 2026-10-14

Source: Justin Zobel, *Writing for Computer Science*, 3rd edition (Springer, 2014). Pages below are the book's printed page numbers (the PDF viewer's counter runs 3 to 10 pages ahead; use the PDF bookmarks, one per chapter and section). Rules are paraphrased. The chapter-end checklists are worth reading whole: hypotheses p. 49, writing up pp. 72-73, editing pp. 195-196, experimentation pp. 214-215, statistics pp. 233-236, ethics p. 264.

Chapters mined: 3 (Reading and Reviewing), 4 (Hypotheses, Questions, and Evidence), 5 (Writing a Paper), 6 (Good Style), 7 (Style Specifics), 9 (Numbers, Percentages), 11 (Graphs, Figures, and Tables), 13 (Editing), 14 (Experimentation), 15 (Statistical Principles), 17 (Ethics).

## A. Checklist

### Structure

1. Near the start, in this order: place the work in accepted knowledge, state the hypothesis or idea, say what is new and what is evaluated, then justify it; readers scan, so the important statements come first. [Ch. 5, p. 56]
2. Abstract in five moves (area, specific problem, existing solutions and their limits, proposed solution, how it was evaluated and what came out), with concrete numbers and no citations, acronyms or "we review the literature". [Ch. 5, p. 57]
3. Introduction = expanded abstract: topic, problem, key references, approach, scope and limitations, outcomes and why they matter, all stated up front with no suspense; its opening paragraphs say what was done, not how, never start with "In this paper", and must be intelligible to any likely reader. [Ch. 5, pp. 57-58; Ch. 7, pp. 97-98]
4. The body gives background and terminology, the chain of reasoning that leads to the conclusions, experiment descriptions sufficient for reproduction, and precise definitions of the hypothesis and major concepts; the structure is visible in the headings. [Ch. 5, p. 58]
5. IMRaD headings are optional in computer science, but their elements are not: background, previous work, proposal, experimental design, results, analysis and discussion must each exist, each in one place. [Ch. 5, p. 59]
6. Separate background (what the reader needs to follow the contribution) from previous work (alternatives the paper improves on); together they fix the state of the art and the baselines. [Ch. 5, p. 59]
7. Keep the literature review in one section rather than scattered where it is used; it sets the expectation for the contribution and lets the reader judge the depth of understanding. [Ch. 5, pp. 60-61]
8. The results section is an assembly of evidence; what the evidence means has to be explained, analyzed and interpreted, never left as a dump of uninterpreted numbers after a description of methods. [Ch. 5, p. 59]
9. Do not organize the body as a chronological log of experiments; present the evidence the argument needs, in the order the argument needs it, and open each results subsection with a one-line overview of what was observed before amplifying. [Ch. 5, p. 55]
10. Conclusions: concise statement of the important results and their significance, the limitations (stated or restated), open questions and variations to explore; the heading is "Conclusions". [Ch. 5, p. 61]
11. Choose the section titles before writing; if some material fits no section, the structure is wrong; keep checking that the paper has not drifted from the aims written down at the start. [Ch. 5, pp. 63-64]
12. Make the structure explicit (a short summary at the start and end of each section, a linking sentence into the next, a reason for every definition before it appears); two heading levels suffice, and topics of equal relevance get similar depth. [Ch. 6, pp. 80-81; Ch. 7, p. 96]
13. Early drafts repeat themselves, especially with several authors or sections written separately: find the same material in different places, merge or cut, and re-read moved text in its new context. [Ch. 13, p. 192; Ch. 5, p. 65]

### Research questions and evidence

14. Research question, hypothesis, the phenomenon expected if the hypothesis holds, and the evidence to be collected form one chain; the paper's structure follows that chain, and a referee who cannot find the hypothesis assumes something is wrong. [Ch. 4, p. 36; Ch. 3, p. 28]
15. State the hypothesis specifically and with its scope; say explicitly what is not being claimed; a qualifying condition makes the claim more precise and therefore stronger. [Ch. 4, pp. 36-37]
16. The hypothesis must be testable and falsifiable ("comparable" and "relatively easy" cannot be tested); say what result would disprove it, and choose the tests most likely to fail if it is false, including the extremes. [Ch. 4, pp. 37, 42, 48-49]
17. "first hypothesize, then test" (p. 38): a hypothesis or experiment fine-tuned on the data yields observations, not confirmation; tests should be as blind as possible. [Ch. 4, p. 38]
18. Distinguish an observation phase (learning about the object, tuning parameters) from a confirmation phase (testing hypotheses); parameters tuned on one dataset are validated only on other data, and choosing parameters to suit data invalidates the research. [Ch. 14, pp. 201-202]
19. Write the explicit argument that connects each piece of evidence to the hypothesis; numbers alone do not persuade. [Ch. 4, pp. 38-39]
20. Play the inquisitor: list the likely objections, rebut what can be rebutted, concede the rest, and put unrefuted objections in the paper rather than setting them aside. [Ch. 4, p. 39]
21. Four forms of evidence (proof, model, simulation, experiment): synthetic data is a simulation, an artificial and controlled test that must be verified against reality; computing a model's predictions is never an "experiment". [Ch. 4, pp. 41-42]
22. State what is measured and how, show that the quantitative measure follows from the qualitative aim, name the compromises of the measure, and beware of optimizing to a benchmark. [Ch. 4, pp. 43-44]
23. A detector that beats a baseline on new data is weak evidence unless the result is predictive and explains why; renaming or inflated terms ("intelligent", "semantic") add no contribution. [Ch. 4, pp. 37-38, 45]

### Experiments and statistics

24. Tests must be fair, not built to support the hypothesis; baselines are the best current method, implemented to a high standard, plus the first thing a reasonable person would try; never an outdated or weak one. [Ch. 14, pp. 198-199]
25. For every dataset: source, gathering mechanism, sufficiency in volume and in number of datasets, required domain knowledge, limits and biases, and what the results would look like if the hypothesis were false. [Ch. 14, pp. 199-201]
26. One dataset rarely persuades (the reader suspects tuning); check that multiple datasets are really independent, and never clean data in a way that favours the method. [Ch. 14, pp. 200-202]
27. Artificial data embodies a model with assumptions and simplifications: state them, state what the data does not test, and validate against real data, which is the strongest defence. [Ch. 14, pp. 202, 214]
28. Claims hold only for the scale and conditions tested; extrapolation must be argued; success in a special case is not general; a somewhat worse method is not "equivalent". [Ch. 14, pp. 202-204]
29. Consider alternative interpretations of every result (implementation quality, settings, caching, measurement noise, the particular input chosen) and design tests to eliminate them; a negative result may only show that the test fell short. [Ch. 14, p. 203; Ch. 15, p. 228]
30. Sanity checks before reporting: counts that must add up, behaviour at the boundaries, a rough prior guess of the outcome, seeding with cases of known answer. [Ch. 14, pp. 203-204]
31. Do not pick through several measures of the same quality to find a significant one; do report measures that capture distinct qualities in tension (false positives and true positives, precision and recall). [Ch. 14, pp. 204-205]
32. A trend across a range is more robust than one number; explain anomalies instead of discarding them; evaluate pipeline components separately; vary each factor independently and widely enough to show its trend. [Ch. 14, pp. 205-207]
33. Experiments are only valuable if reproducible: singleton results are valueless; failures are reported as prominently as successes; preliminary and dead-end experiments are sketched briefly, not hidden. [Ch. 14, pp. 212-213]
34. Vary one variable at a time, design out extraneous factors, define the population and the sample, and repeat with different random partitions or seeds; a single score is misleading and a single input may be meaningless. [Ch. 15, pp. 218-221]
35. Report variability (standard deviation, quantiles or a distribution plot) with every average, and report averages only to the precision the standard error justifies (1.2 s, not 1.161 s); a mean over a few runs can hide outliers and manufacture "surprising" findings. [Ch. 15, pp. 222-223]
36. Use a hypothesis test to show that an improvement is real, say which test and why, and remember that small effects need many trials (power); "better on average" without a test is not a result. [Ch. 15, pp. 224-225]
37. Confirmation bias: a success reported without the failures, tuning and exploration that preceded it is not sound science. [Ch. 15, p. 231]

### Results presentation (tables and figures)

38. Present a number only because it is evidence for a hypothesis, not because the program produced it; no flood of statistics, and each graph or table conveys new information. [Ch. 11, p. 157]
39. Graphs: the varied parameter on x, the output on y, marked points, few lines, no gridlines or decoration, legend clear of the curves, fonts as in the text. [Ch. 11, p. 158]
40. Comparable graphs share axis scales; a ratio-scale y axis starts at 0 or the caption says why not; use log axes when behaviour spans orders of magnitude; never let a graph imply what the data cannot support. [Ch. 11, pp. 160-166]
41. Tables are for exact values and dataset properties: logical hierarchy, few rules, no empty cells (dash plus explanation), decimals aligned, not dense; a simple relationship is better stated in a sentence. [Ch. 11, pp. 171-174]
42. Do not rely on a table to carry an essential result; show it in a graph or a sentence and keep the table for reference. [Ch. 11, p. 176]
43. Captions are self-contained (parameters, abbreviations, conditions) and every figure and table is numbered, introduced and discussed in the text or dropped; units in every label, representative numbers repeated in the text, figures updated when terminology changes. [Ch. 11, pp. 176-178]
44. Digits for reported quantities, the same precision within a unit, no spurious accuracy, approximations marked as such, the same figure never quoted with different values; for percentages say what is a percentage of what, separate points from relative change, and never turn 2 of 5 into "40 %". [Ch. 9, pp. 139-142]
45. Do not join points with lines where interpolation is meaningless; sort or aggregate points to make a pattern visible. [Ch. 15, pp. 231-233]

### Style

46. Every sentence necessary, one idea per sentence or paragraph, one topic per section, short words and short sentences; cut waffle and padding ("in general", "note that", "the fact that", "a number of"). [Ch. 6, pp. 76-77; Ch. 7, pp. 117-118]
47. Do not overqualify: state the result plainly, then the conditions under which it may not hold; at most one hedge per sentence; drop "very", "quite", "simply", "somewhat". [Ch. 6, p. 77; Ch. 7, p. 110]
48. Active voice and "we" to mark the paper's own contribution against existing results; avoid "it is shown that" and "this paper shows". [Ch. 6, pp. 81-82]
49. Be specific, not obfuscating: "savings of 12 to 33 %" rather than "large savings"; avoid vague words ("important", "performance", "efficient", "difficult"); no bold conclusions from thin evidence and no excessive claims about one's own work. [Ch. 6, p. 83; Ch. 7, pp. 108-109]
50. No straw men (contrast the new with the current, not with the fictitious or the ancient; cite evidence, not opinion; flag beliefs as beliefs); describe cited work fairly, name the authors of discussed references ("Marsden [16]", not "[16]"), and make self-citations visible as such. [Ch. 6, pp. 84-88]
51. A paragraph has one topic announced in its first sentence; link paragraphs by repeating the key term, not with "this" or "it"; vary sentence openings and do not chain "however", "moreover", "thus". [Ch. 7, pp. 99-101, 105]
52. Tense: present for enduring truths and for the text itself, past for what was done and observed, future only in conclusions; comparisons complete (better than what?); parallel structure for complementary ideas. [Ch. 7, pp. 105-106]
53. Define every term, abbreviation and acronym once, on first use, in a consistent format, then use the same word for the same concept; introduce an acronym only if it is used often and never re-expand it; use "theory", "hypothesis" and "proposition" in their formal senses. [Ch. 7, pp. 107-108, 113, 115, 120; Ch. 13, p. 196]
54. Final editing pass for consistency: headings match content, same precision for the same kind of value, same format and orientation for all tables, caption on every figure, consistent units and reference format; then read the whole paper in one sitting and have someone else read it. [Ch. 13, pp. 193-196]

### Ethics and reproducibility

55. Misrepresentation includes implying confidence that limited experiments do not support: few runs with high variance, parameters tuned to the test input, unreported failed experiments; codes of conduct condemn the last explicitly. [Ch. 17, p. 261]
56. Report negative as well as positive results and describe every experimental issue or limitation that could have affected the outcome; a weak or badly implemented baseline borders on deception. [Ch. 17, p. 261]
57. Disclose conflicts of interest and commercial relationships in the text or to the editor; confidential or proprietary data needs permission and must be declared. [Ch. 17, p. 263]
58. Keep notebooks, code versions, configurations, inputs and logs; run experiments from scripts that record parameters and dates; be able to rerun and get the same outcome, and be ready to show the setup to others. [Ch. 14, p. 212; Ch. 17, pp. 262, 264]
59. Publish code and data where possible (it signals confidence and creates baselines); where data cannot be shared, say so and say why. [Ch. 14, p. 214; Ch. 17, p. 264]
60. Limitations are stated in the paper, at least in the conclusions; admitting them and asking "what else would explain these results?" is a mark of competence, not weakness; any study with people evaluating a system needs an ethics statement. [Ch. 5, pp. 61, 66; Ch. 14, p. 210; Ch. 17, p. 264]

## B. Rules most relevant to this manuscript's reviewer feedback

The reviewer's written feedback, his proposed six-section outline (Introduction; Related Work; Methodology; Experimental Results and Discussion; Limitations and Ethical Considerations; Conclusions and Future Work) and his voice notes reduce to six complaints. For each, the rules above that apply and the concrete action they imply.

**1. Methods are explained inside the results.** Rules 4, 5, 8, 11, 13, 25, 58. Every "how" (generator, corpora, annotation convention, training protocol, checkpoint selection, metric definitions, pre-specified criteria) has exactly one home, Materials and Methods; Zobel's own example separates "Experimental setup" from "Results and discussion" (p. 59). A results subsection then opens with one sentence naming the experiment, the data and the figure or table, followed by what was observed (rule 9). If a paragraph in Results cannot be removed without leaving a method unexplained, the method is in the wrong section. Current files most affected: `07b-results-placeholder.md`, `06b-model-free-evidence.md`, `08b-robustness.md`.

**2. Conclusions are drawn inside the results.** Rules 8, 9, 10, 19, 28, 52. Zobel is slightly more permissive than the reviewer: he allows each result to be read where it is shown (p. 55, p. 59), so a sentence saying what a table shows, why a case is typical or what an anomaly might be stays in Results. What moves to the Discussion is the step from observation to claim: what the result means for RQ1 to RQ3, for the literature, for acquisition practice and for dual use, and its significance. Test by tense and verb: "was", "fell", "rose" belong in Results; "shows that", "implies", "we conclude" belong in Discussion and Conclusions. The "what held and what did not" summary (planned 5.6) stays in Results only if it is a mechanical pass/fail against criteria fixed in Methods (rule 18).

**3. The paper repeats itself** (the voice notes name the symptoms: the same acronym expanded many times, concepts re-explained, monotonous connectors). Rules 7, 12, 13, 38, 51, 53, 54. Give each concept one home (GSD, the ceiling, the annotation convention, the dual-use argument, the Jacarezinho context) and cross-reference elsewhere. Only two repetitions are sanctioned: the introduction states the outcomes (rule 3) and the conclusions restate them (rule 10). Run a pass that expands each acronym once, lists every place a concept is defined, and merges the second and later occurrences; then the one-sitting read (rule 54).

**4. Research questions are not aligned with what was measured.** Rules 14, 15, 16, 22, 27, 28, and Zobel's warning about papers whose results are unrelated to their conclusions (Ch. 5, p. 69). Build one table in Methods with a row per research question: hypothesis, measure, experiment, data (synthetic or real), pre-specified criterion. Every Results subsection answers one row; the Discussion answers each question in turn. For the armed/unarmed question, write the scope into the question itself (measured on synthetic data only, at the stated GSDs): a qualifying condition strengthens the claim (rule 15). The title and abstract must match that scope (rules 2 and 3; Ch. 7, p. 96 on titles that promise more than the work delivers).

**5. Confirmatory and exploratory analyses are mixed.** Rules 16, 17, 18, 33, 34, 36, 37. Label every experiment as confirmatory (hypothesis and criterion fixed before the run) or exploratory (configuration introduced after seeing results). Exploratory results are reported as observations that motivate a future confirmatory test: no significance language, not in the hypothesis summary. Separate the validation results used for checkpoint selection from results on independent images, and say so in Methods (the reviewer's item 1.2 is Zobel's p. 202). For the voice-note complaint that model differences are nearly identical: without repetitions, variance and a test (rules 34 to 36), close scores cannot be called an improvement, and a somewhat worse model cannot be called equivalent (rule 28).

**6. No explicit limitations and ethics section.** Rules 10, 20, 27, 47, 55, 56, 57, 59, 60. Adopt the reviewer's section 5, "Limitations and Ethical Considerations", and gather there everything now spread across `09b-technical-limitations.md`, `08b-robustness.md` and the Limitations and Delimitations subsections of `07-conclusion.md`: limits of the synthetic data (sensor, noise, blur, compression, figure diversity), of the benchmark as a stand-in for the target domain, of the number of runs and seeds, plus the unrefuted objections (rule 20). Ethics in the same section: dual-use risk, conflicts of interest, the data that cannot be shared and why, and a statement on human subjects. Once limitations live there, remove the hedges scattered through the text (rule 47) and have the Conclusions point to the section rather than restate it in full.

One structural note: the reviewer's outline merges Results and Discussion into one section and puts Limitations and Ethics in its own section. Zobel accepts a combined "Results and discussion" (p. 59) and puts limitations in the conclusions (p. 61); the two are compatible if, inside the combined section, each experiment's observations come first and its interpretation follows, and the limitations section is cross-referenced from the conclusions.
