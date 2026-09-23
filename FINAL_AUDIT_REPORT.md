# Final audit report

Audit date: 23 September 2026  
Scope: frozen MPhil experiment, thesis, references, knowledge base, released results, code, and repository presentation

## Final recommendation

**NOT READY — administrative and institutional items only.**

The scientific narrative, deterministic results, code checks, KB audit, consolidated thesis, and PDF render are complete and internally consistent. The generated thesis is not submission-ready until the candidate replaces the title-page placeholders, inserts the exact University of Salford/PGR declaration, confirms the applicable institutional template, and replaces the placeholder author in `CITATION.cff`. No institutional wording or personal data was inferred.

## Repository audit status

- The active entry point is `scripts/run_final_pipeline.py`; frozen configuration is in `configs/experiment.yaml`, `configs/models.yaml`, and `configs/prompts.yaml`.
- The final experiment is the five-stage release under `artifacts/release/`. Earlier planning and a stale journal-format document are labelled under `archive/` and are not active evidence.
- The immutable KB remains `data/kb/fashion_rules.csv`, SHA-256 `59cec6821d32ca78d57e0a8dee592c55c9100b6ca9ebbf17a43301a46bd30e77`.
- The canonical verification file remains SHA-256 `0f554e58be51c0529c59814f3c5de379ec66c02afbb8fa2c5e48249a32ae9b3e`.
- `uv run ruff check .` passes. `uv run pytest -q` passes with **54 tests**.
- `uv run python scripts/audit_final_release.py` passes and independently checks release hashes, ranking metrics, case counts, claim counts, word counts, final contrasts, the KB distribution, and the trace-subset invariant.
- The prerequisite-only full-pipeline check correctly identifies six unavailable local Ollama model tags on this machine. Model-dependent stages were not rerun because their frozen inputs and outputs are preserved and the experiment is closed.

## Thesis consistency status

- The five chapters were edited and consolidated into `thesis/final_thesis.md` with one 28-item cited reference list.
- `thesis/final_thesis.docx` and the 69-page A4 `thesis/final_thesis.pdf` render successfully.
- The abstract, introduction, methodology, results, discussion, limitations, future work, and conclusion now use one narrative: multimodal fusion was strongest overall; evidence reranking did not improve aggregate recommendation effectiveness; the retained trace made the symbolic decision contribution explicit; and trace access substantially improved measured explanation support.
- The KB is consistently described as a manually curated, source-grounded experimental resource, not universal truth, an automatically learned ontology, or independently certified expert guidance.
- “Decision trace” now means the complete retained symbolic trace used by the reranker. It is not presented as a complete explanation of CLIP's latent computation.
- Research questions are answered explicitly. Recommendation effectiveness is kept separate from explanation faithfulness.
- The proposed dataset-grounded compatibility KG appears only in future work and has no reported result.

## Numerical result verification

All values below were recomputed or counted from the compact release rather than copied from thesis prose.

| Item | Verified value |
|---|---:|
| Prepared dataset | 47,872 items; 19,094 outfits |
| Outfit-disjoint split | 13,365 development; 2,864 validation; 2,865 test outfits |
| Exact-image audit | 18 duplicate groups; 9 initially cross-split; 12 reassigned outfits (9 component, 3 quota restoration) |
| Recommendation cases | 1,000; 200 per category; 734 unique query outfits |
| Candidate pools | 976 × 100; 22 × 101; 2 × 102 candidates |
| Fused CLIP | HR@1 4.5%; HR@5 14.3%; HR@10 23.1%; NDCG@5 9.43%; NDCG@10 12.23%; MRR 11.44% |
| Evidence rerank | HR@1 3.8%; HR@5 13.2%; HR@10 22.5%; NDCG@5 8.47%; NDCG@10 11.45%; MRR 10.56% |
| Top-ranked item changed | 265/1,000 (26.5%) |
| Locked-rule coverage | 148/200 rules |
| Explanation experiment | 500 cases; 3 generators; 3,000 attempted cells |
| Accepted records | 2,969 explanations; 2,965 extractions; 2,861 verifications |
| Claims | 17,710 extracted; 16,804 verified |
| Accepted mean length | No-RAG 62.104 words; Rule-RAG 64.828 words |
| Trace-support contrast | +21.02 percentage points; 95% CI +19.72 to +22.37; 498 paired cases |
| Full-KB-support contrast | +21.40 percentage points; 95% CI +20.11 to +22.71; 498 paired cases |
| UIFR contrast | +0.63 percentage points; 95% CI -5.03 to +5.66; 53 paired cases; inconclusive |
| Trace-supported claim density | +1.60 claims/100 words; 95% CI +1.48 to +1.72; 498 paired cases |

The thesis uses “percentage points” for rate differences and retains claim density in its native claims-per-100-words unit.

## Source-of-truth map

| Thesis claim | Definitive artifact | Producing/checking code | Frozen configuration/input |
|---|---|---|---|
| Dataset, split, and leakage controls | `artifacts/release/final_stage1_preflight_manifest.json` | `scripts/prepare_data.py`, `scripts/finalize_stage1_preflight.py` | `configs/experiment.yaml`, pinned `Marqo/polyvore` revision |
| Recommendation metrics | `artifacts/release/recommendation_metrics_with_ci.csv` and `candidate_rankings.jsonl` | `scripts/run_final_recommendations.py`, `scripts/run_final_stage5_analysis.py`, `scripts/audit_final_release.py` | Frozen embeddings, candidate pools, 0.40/0.60 fusion |
| Evidence participation and trace | `artifacts/release/candidate_rankings.jsonl` and `explanation_cases.jsonl` | `src/evidence_fashion/rule_retrieval.py`, recommendation stage | Frozen KB, Qwen embedding, 0.75/0.25 reranking, top-k maximum 5 |
| Generation counts and word lengths | `artifacts/release/explanations.jsonl` | `scripts/run_final_explanations.py`, release audit | Frozen generator roster and prompts |
| Extracted and verified claims | `artifacts/release/extractions.jsonl`, `verifications.jsonl` | Stage-3/4 scripts and grounding contracts | Frozen extractor/verifier models and schemas |
| Explanation effects, CIs, and p-values | `artifacts/release/explanation_paired_contrasts.csv` | `scripts/run_final_stage5_analysis.py` | 5,000 case-cluster bootstrap replicates, seed 42, Holm family of four |
| KB size, distribution, and sources | `data/kb/fashion_rules.csv` | `src/evidence_fashion/kb_audit.py`, `scripts/rebuild_kb_audits.py` | Frozen 200-rule CSV and SHA-256 |

## Stage-4 consistency correction

The released code and records support the stated deterministic correction. There were **163** claims for which `trace_support` was `supported` but `full_kb_support` was `not_supported`, despite the trace rule occurring in that record's full-KB packet. Only `full_kb_support` was changed to `supported`; no model was rerun and no other field changed. The canonical output now contains zero violations of the invariant that trace support implies full-KB support. The thesis reports this as a logical consistency correction, not as new semantic assessment.

## KB verification

- 200 rules; 40 per recommendation category; 39 unique source URLs.
- Rule IDs are unique; all required provenance and applicability fields are present; all categories are valid.
- No exact normalised rule-text duplicate and no pair at or above the frozen 0.90 sequence-similarity review threshold.
- Derived coverage, similarity, and source-registry tables were regenerated from the unchanged frozen KB.
- All 39 source pages were reachable through at least one browser/HTTP audit route on 23 September 2026. Live titles and dates can change; frozen experiment metadata was preserved instead of rewriting the research artifact.
- All rules carry the frozen medium-reliability and bounded-enrichment metadata. This provenance is disclosed rather than reinterpreted as professional certification.

## Reference audit status

- Every cited thesis reference was checked against a DOI, publisher proceedings page, original repository, or other primary record where available.
- Duplicate chapter bibliographies were consolidated; uncited Spearman material was excluded automatically.
- DOI/primary URLs were added for the principal datasets, encoders, recommendation methods, RAG, explanation evaluation, bootstrap, and Holm procedure.
- Two recent positioning references were added without changing the experiment: Li et al. (2024) on attribute-augmented explainable fashion compatibility and Zhai et al. (2025) on text-conditioned outfit generation.
- The review explicitly states that this thesis does not seek a new state-of-the-art outfit-compatibility architecture.
- No unverifiable thesis citation remains known. Web sources used by the KB are separately listed in `data/kb/kb_source_url_audit_2026-09-23.csv`.

## Figure and table audit

- The original frozen contrast figure incorrectly scaled claim density by 100 and labelled all four outcomes as percentage points.
- The frozen file was retained for provenance. A corrected two-panel PNG/SVG separates the three rate outcomes from claim density and is the version used in the thesis.
- The recommendation and explanation tables use consistent precision and explicitly distinguish percentage points from claims per 100 words.
- The final PDF was inspected at the title page, abstract, key tables, corrected figure, and bibliography. No clipped figure, table overflow, accidental blank page, or unresolved cross-reference was found.

## Reproducibility status

Deterministic reproduction from the compact release is complete. The audit reproduces every final recommendation estimate and validates the principal released explanation contrasts and counts without model calls. A full fresh run additionally requires the pinned Polyvore dataset, Hugging Face revisions, embedding storage, and six exact local Ollama models. Those external assets are not redistributed. Git line-ending normalisation changes the byte hash of five Windows-authored CSV/SVG files; the audit accepts and reports the exact CRLF-equivalent hash while rejecting substantive byte changes.

## Claim ledger

| Major statement | Classification | Basis |
|---|---|---|
| Fused CLIP was stronger overall than corresponding CLIP image/text configurations | Supported by experiment | Released candidate rankings and recommendation table |
| Evidence reranking improved overall recommendation performance | Rejected by experiment | All reported aggregate values are below fused CLIP |
| The rule component materially changed decisions | Supported by experiment | 265 top-one changes and participation diagnostics |
| The stored rule packet is the exact symbolic evidence used by reranking | Supported by implementation/artifacts | Candidate traces, hashes, and reranking code |
| Trace access improved measured trace and full-KB claim support | Supported by experiment | Paired clustered contrasts with Holm adjustment |
| Rule-RAG reduced unsupported item facts | Not established | UIFR interval crosses zero; only 53 eligible pairs |
| The KB is universal or professionally certified | Rejected | Frozen provenance describes curated, bounded experimental rules |
| Human preference or factual correctness was validated | Not established/limitation | No human study or independent semantic annotation |
| Dataset-grounded compatibility KG | Future work | No completed experiment or result |

## Unresolved items

1. Replace candidate name, student ID, school/department, supervisors, and submission date placeholders.
2. Insert the exact required University of Salford/PGR declaration and obtain any required signature.
3. Confirm the applicable institutional template, margins, binding, pagination, and reference style with the current PGR guidance or supervisor.
4. Replace the placeholder author in `CITATION.cff` and the author/affiliation/contact placeholders in the active paper; add ORCID only if applicable.
5. If a clean machine reproduction is required for examination, provision the exact Ollama model tags/digests and external dataset/model caches listed in the README.
