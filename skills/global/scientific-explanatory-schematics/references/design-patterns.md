# Design patterns for high-quality scientific explanatory schematics

Use this reference when selecting a diagram type or redesigning a poor workflow/mechanism figure.

## Source-informed design principles

- **Cell Press graphical abstract guidance:** a graphical abstract should be one clear visual message with a clear start/end, simple labels, sparse text, biological/contextual grounding, and no excessive speculative detail or clutter. Source: https://crosstalk.cell.com/hubfs/Files/GA_guide.pdf
- **PLOS graphical abstract rules:** define the key message for the audience; choose layout by process type; support reading direction with arrows; use text to clarify ambiguous visuals; use color consistently; seek feedback before/during/after. Source: https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1011789
- **PLOS better figures rules:** identify the message first, write captions, do not trust default styles, use color intentionally, avoid misleading encodings and chartjunk, and prioritize message over beauty. Source: https://journals.plos.org/ploscompbiol/article?id=10.1371%2Fjournal.pcbi.1003833
- **Nature Reviews artwork guidance:** use top-left to bottom-right information flow unless a true cycle is needed; create visual hierarchy with focus, saturation, detail, and muted context; avoid icons used only as decoration; keep arrow styles meaningful. Source: https://www.nature.com/documents/natrev-artworkguide.pdf
- **Image-based figure reporting guidance:** figures and legends should be self-explanatory; labels, symbols, annotations, scale, and color must be explained; important annotations should be colorblind accessible and can be double-coded by hue plus shape/line style. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC8041175/

## Pattern selection table

| Pattern | Use when | Layout grammar | Avoid |
|---|---|---|---|
| Evidence cascade | You need to show how raw objects become evidence, candidates, rankings, or validated links. | Staged funnel or layered path: raw data → preprocessing → evidence generation → filtering/ranking → validation. | Making every stage an equal box; implying validation occurred when it has not. |
| Parallel multimodal route | Two or more data modalities converge, e.g. NMR metabolome + BGC/GCF genome evidence. | Separate lanes with matched stages; convergence layer; final decision/ranking. | Crossing arrows; hiding modality-specific uncertainty. |
| Architecture map | Readers need to understand model components, encoders, embeddings, losses, or trained/frozen parts. | Inputs on left, encoders/modules in middle, shared space/scorer/output on right; use line styles for training/inference. | Mixing data pipeline and model internals in one overloaded panel. |
| Decision gate | A workflow has pass/fail criteria, filters, thresholds, or review steps. | Gates/diamonds or checkpoint bars; each gate has input, criterion, pass action, fail action. | Using gates without stating criteria. |
| Mechanism model | You need to explain a biological/computational mechanism or hypothesis. | Context → actors → interaction → output; mark uncertainty with dashed lines or question tags. | Drawing causal arrows for merely correlated observations. |
| Comparison matrix | Methods, candidates, or risks need side-by-side comparison. | Rows = methods/candidates; columns = capabilities, assumptions, evidence, limitations. | Using icons where a table is clearer. |
| Figure navigator | A paper has several important source figures that support different route steps. | Technical route strip plus callouts: Fig 1/2/3 mapped to specific steps and claims. | Replacing source figure reading with an abstract route only. |
| Confounding map | Observed association may be driven by taxonomy, batch, expression, environment, or sampling. | DAG-like map: confounders point to both exposure and outcome; controls shown as gates or adjustment layers. | Treating confounders as minor notes when they affect interpretation. |

## How to avoid the low-quality box-arrow look

Replace “same-size rectangles + arrows” with a design grammar:

1. **Choose lanes or layers:** data modality, time, evidence strength, model component, or risk/control layer.
2. **Create a focal point:** the most important step/result should be visually heavier, more saturated, or centrally placed.
3. **Mute context:** background steps can be thin, gray, or smaller; not every item deserves equal emphasis.
4. **Make arrows semantic:** data flow, inference, ranking, validation, feedback, and uncertainty need distinguishable arrow styles.
5. **Use direct labels:** label elements near the objects; reduce legends and abbreviations.
6. **Use grouped shapes:** containers, braces, or swimlanes show structure better than drawing many boxes.
7. **Split overloaded figures:** if a diagram is both route, mechanism, model architecture, and results summary, make two or three figures.

## Project-style patterns for NMR × GCF literature notes

For a project connecting NMR features to GCF/BGC evidence, prefer separate figures rather than one huge overview:

1. **Current technical route overview:** two parallel lanes — strain/sample metadata → NMR features and genome/BGC/GCF features → candidate NMR–GCF pairs → weak labels/rules → ranker → validation/readout. This helps a project overview note.
2. **Model architecture schematic:** NMR encoder and GCF encoder feed a shared representation or scorer; show training signals, PU/MIL/ranking loss, and output candidate list. This helps explain deep-model choices.
3. **Evidence and risk map:** evidence sources on one side, confounders/controls on the other; show which risks are controlled, uncontrolled, or planned. This helps prevent overclaim.
4. **Paper figure navigator:** map original paper Figure/Table evidence onto project modules, e.g. NMR peak picking, GCF representation, linking score, validation, confounders.

## Layout heuristics

- Linear process: left-to-right or top-to-bottom.
- Cycle: circular only when the process truly cycles and has a clear entry/focal point.
- Static comparison: two columns, nested detail, or matrix.
- Multi-omics integration: parallel lanes that converge.
- Evidence strength: vertical stack or funnel from raw observation to stronger validation.
- Uncertainty/risk: side band, dashed links, warning color role, or separate risk panel.
