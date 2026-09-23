# Submission checklist

## Completed

- [x] Frozen experiment identified and separated from deprecated material.
- [x] Recommendation metrics recomputed from 1,000 candidate-ranking records.
- [x] Explanation counts, pair counts, word counts, claims, support labels, and contrasts verified.
- [x] Stage-4 163-label deterministic correction verified and disclosed.
- [x] Frozen KB hash preserved; rule count, categories, identifiers, provenance, duplicates, and source URLs audited.
- [x] Stale KB coverage, similarity, and source-registry tables regenerated.
- [x] Thesis methodology reconciled with code/configuration.
- [x] Recommendation and explanation conclusions reconciled with frozen outputs.
- [x] References checked against primary records and consolidated.
- [x] Recent related work added only for positioning.
- [x] Corrected contrast figure generated without altering the frozen historical figure.
- [x] Final thesis Markdown, DOCX, and 69-page A4 PDF generated.
- [x] PDF title page, abstract, tables, figure, equations, bibliography, and page flow visually inspected.
- [x] Repository instructions updated; deprecated planning/document files archived and labelled.
- [x] Deterministic release audit passes.
- [x] `ruff check .` passes.
- [x] 54 automated tests pass.

## Candidate actions required before submission

- [ ] Replace every bracketed title-page placeholder in `thesis/front_matter.md`.
- [ ] Insert the exact University of Salford/PGR declaration and complete any signature requirement.
- [ ] Complete or remove acknowledgements.
- [ ] Confirm the current institutional formatting/template requirements; rebuild with `uv run python scripts/build_final_thesis.py`.
- [ ] Replace the placeholder author in `CITATION.cff` and the author/affiliation/contact placeholders in the active paper.
- [ ] Review personal data, acknowledgements, ethics/disclosure wording, and any required AI-use statement with the supervisor.
- [ ] Open the rebuilt PDF on the submission machine and perform a final page-by-page check.
- [ ] Confirm the submitted filename and repository/archive packaging required by the programme.

Current status: **NOT READY until the candidate/institutional items above are completed.**
