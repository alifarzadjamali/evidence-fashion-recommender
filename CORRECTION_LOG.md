# Substantive correction log

Grammar, punctuation, and routine formatting edits are omitted. All entries below affect scientific description, provenance, reproducibility, or submission packaging.

| ID | Area | Correction | Authoritative basis |
|---|---|---|---|
| C001 | Dataset | Replaced obsolete prepared counts with 47,872 items and 19,094 outfits. | Stage-1 manifest and prepared-data audit |
| C002 | Splits | Corrected outfit quotas to 13,365/2,864/2,865 for development/validation/test. | Frozen split manifest |
| C003 | Leakage | Corrected exact-image audit to 18 groups, 9 initially cross-split, and 12 outfit reassignments (9 component, 3 quota restoration). | Stage-1 duplicate-image audit |
| C004 | Rule retrieval | Replaced the obsolete MiniLM/bonus/reliability description with Qwen 3 embedding, explicit applicability gates, equal weights, and zero bonus. | Final code and configuration |
| C005 | Evidence score | Corrected the rule-score equation from a five-rule mean to 0.7 maximum plus 0.3 mean over the retained eligible set. | Final reranking implementation |
| C006 | Trace cardinality | Replaced “exactly five” language with the complete retained trace of up to five rules; documented empty ranking traces and 1–5-rule explanation traces. | Candidate rankings and explanation cases |
| C007 | Recommendation inference | Removed an unsupported claim of 28 Holm-corrected recommendation contrasts and an unsupported no-penalty/equivalence interpretation. | Released tables contain per-method clustered intervals, not pairwise recommendation tests |
| C008 | Claim counts | Removed obsolete 10,703/8,666 claim totals and reported the verified 17,710 extracted and 16,804 verified claims. | Stage-3 and Stage-4 release files |
| C009 | Length | Replaced obsolete 52.84/60.55 and legacy pilot wording with accepted-output means of 62.104/64.828 under the 45–75-word contract. | Released explanation records |
| C010 | Models | Corrected generator range from 3.2B–12.2B to 8.0B–13.9B parameters. | Frozen model configuration |
| C011 | KB positioning | Replaced “expert knowledge/rules” claims with manually curated, source-grounded experimental fashion rules and explicitly disclaimed universal truth or professional certification. | Frozen KB provenance fields |
| C012 | Stage 4 | Verified and proportionately documented the deterministic 163-label full-KB subset-consistency correction. | Canonical verifications and final report |
| C013 | Results language | Standardised absolute rate changes as percentage points and kept claim density in claims per 100 words. | Released paired-contrast table |
| C014 | Figure | Replaced the misleading one-axis plot that multiplied density by 100 with a corrected two-panel presentation figure; retained the frozen original. | Released contrasts and figure-generation code |
| C015 | KB audits | Regenerated stale coverage, source-registry, and similarity-audit files from the unchanged 200-rule KB. | `scripts/rebuild_kb_audits.py` |
| C016 | KB sources | Added a dated 39-URL reachability record while preserving frozen titles/years for reproducibility. | Live audit on 23 September 2026 |
| C017 | References | Verified cited works, added primary URLs/DOIs, consolidated duplicate chapter lists, and removed uncited Spearman material from the final bibliography. | Publisher/proceedings/DOI records |
| C018 | Related work | Added Li et al. (2024) and Zhai et al. (2025) for current positioning without changing the experiment. | Original journal and ICCV records |
| C019 | Future work | Added the independent dataset-grounded compatibility KG only as future work, with provenance, cross-dataset separation, and CP/FITB validation requirements. | Thesis scope and user instruction |
| C020 | Code validation | Added a deterministic compact-release audit and KB-derived-audit test; final suite is 54 passing tests. | Local test and lint runs |
| C021 | Release portability | Documented CRLF/LF hash portability for five Windows-authored text artifacts without changing frozen manifests. | Byte-level hash comparison |
| C022 | Repository | Moved superseded human-validation planning and the stale SNCS document to a labelled provenance archive. | Repository cleanup audit |
| C023 | Paper | Reconciled the active paper's rule-scoring, trace-cardinality, prompt-length, and terminology descriptions with the final implementation. | Final code/configuration and release |
| C024 | Thesis package | Added front matter, abstract, abbreviations, consolidated source/reference list, regenerated chapter DOCX files, and built the final DOCX/PDF. | Edited chapter sources and build script |
| C025 | Test count | Replaced stale “55 tests,” then updated the final count to 54 after adding the KB-derived-audit test. | `uv run pytest -q` |
| C026 | API diagnostics | Replaced raw Ollama HTTP/connection tracebacks with model- and endpoint-specific failure messages; no inference behaviour or frozen output changed. | Local prerequisite/integrity-check failure audit |
| C027 | Pipeline diagnostics | Made prerequisite and stage failures exit with concise actionable messages instead of full tracebacks. | `scripts/run_final_pipeline.py --check` |
