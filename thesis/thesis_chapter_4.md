# Chapter 4

# Results

## 4.1 Introduction

This chapter reports the frozen final five-stage experiment. Every result is derived from the canonical Stage 1--5 artifacts; no model was called during final analysis. Results follow the pipeline: preflight, recommendation evaluation, explanation generation, extraction and verification, then paired claim-level contrasts. A claim described as unsupported is unsupported by the supplied source under the frozen protocol; it is not thereby false in the world. Citation syntax is also kept separate from citation entailment.

The explanation intervention is narrow and controlled. No-RAG and Rule-RAG explain the same locked recommendation for the same case and generator. Both receive common context A. Rule-RAG alone receives the complete retained reranking trace B. The experiment therefore measures the effect of making stored decision evidence available during generation, rather than comparing explanations of different recommendations.

## 4.2 Final preflight and frozen design

Stage 1 passed the final preflight gate. Dataset and split inputs, embeddings, candidate-pool construction, prompts, schemas, and output hashes were frozen before confirmatory work. The final knowledge base contains 200 curated fashion rules, exactly 40 each for bags, bottoms, outerwear, shoes, and tops. The audit confirmed unique identifiers, complete provenance, and no exact or threshold-defined near duplicates.

Validation-only grids fixed the operational point: image/text fusion of 0.40/0.60, CLIP/evidence reranking of 0.75/0.25, and a maximum of five eligible rules per candidate. These checks are not pooled with confirmatory results. Crucially, the complete retained trace saved during reranking is the same record supplied as Rule-RAG evidence. No separate explanation-time retrieval occurred.

## 4.3 Recommendation results

The recommendation evaluation contained 1,000 held-out cases, 200 per category, drawn from 734 underlying query outfits. Confidence intervals use 5,000 percentile bootstrap replicates clustered by query outfit. The task remains controlled same-category candidate-pool ranking, with held-out outfit co-occurrence as an offline relevance proxy.

\Needspace{18\baselineskip}

| Method | HR@1 | HR@5 | HR@10 | NDCG@5 | NDCG@10 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MiniLM text | 4.8% | 12.0% | 17.7% | 8.4% | 10.3% | 10.2% |
| CLIP image | 3.2% | 12.6% | 22.0% | 7.9% | 10.9% | 10.0% |
| CLIP text | 3.5% | 13.8% | 21.2% | 8.6% | 11.0% | 10.1% |
| Fused CLIP | 4.5% | 14.3% | 23.1% | 9.4% | 12.2% | 11.4% |
| Evidence rerank | 3.8% | 13.2% | 22.5% | 8.5% | 11.4% | 10.6% |

*Table 4.1. Micro-averaged recommendation effectiveness on 1,000 frozen test cases. Values are shown as percentages; unrounded estimates and confidence intervals remain in the released table.*

Fused CLIP was the strongest tested conventional retrieval pathway. Evidence reranking did not improve these aggregate relevance measures, so it must not be presented as an accuracy improvement. It did, however, change the top-ranked recommendation in 26.5% of cases, with mean top-five overlap of 3.859, mean top-one evidence-score gain of 0.1473, and mean pre-to-post rank shift of 0.566. One hundred and forty-eight of the 200 rules occurred in at least one locked trace. The symbolic component therefore materially participated in the decisions it later helped explain.

## 4.4 Explanation completion and pairing

Five hundred evidence-eligible locked recommendations, balanced at 100 cases per category, formed the explanation study. Gemma 4 12B, Llama 3.1 8B Instruct, and Ministral 3 14B Instruct generated both conditions, giving 3,000 attempted cells. Stage 2 accepted 2,969 explanations. The 31 terminal failures were all Llama Rule-RAG responses exceeding the shared 75-word limit after permitted retries; none was replaced or silently repaired.

Final inference therefore uses generator-specific complete pairs: Gemma 474, Llama 438, and Ministral 456. For the overall estimate, generator-level within-case differences are averaged before resampling, leaving 498 underlying cases with at least one complete generator pair. This prevents multiple generator outputs for a case being treated as independent observations and avoids raw unequal condition totals.

## 4.5 Extraction and verification completion

Qwen 3.5 9B extracted atomic claims from the 2,969 accepted explanations. Stage 3 accepted 2,965 extraction records containing 17,710 claims; four terminal extraction failures were retained. Phi-4 14B then verified claims against A, the exact trace, the full-KB candidate packet, and observed citations. Stage 4 accepted 2,861 verification records covering 16,804 claims. The 104 terminal verification failures remain in the canonical missingness record.

The verifier preserves separate fields for `trace_support`, `full_kb_support`, `common_reference_support`, and `citation_entailment`. Of the verified claims, 2,058 were trace-supported and 2,095 were supported by the full KB packet. Common-reference support was 961 supported, 13 not supported, and 15,830 not applicable. Citation entailment was 1,820 entails, 5,502 does not entail, and 9,482 not applicable.

A deterministic correction addressed 163 logically impossible labels where trace support was supported but full-KB support was not supported. For every affected claim, the trace rule was confirmed to occur in its full-KB packet. Only the full-KB label was changed to supported; no model was rerun and no other field was altered. The final invariant is explicit: trace support implies full-KB support.

## 4.6 Paired explanation results

Primary contrasts use 5,000 paired percentile bootstrap replicates clustered by underlying case [2], with Holm adjustment across four prespecified overall metrics [3]. Table 4.2 presents Rule-RAG minus No-RAG. Positive values favour Rule-RAG except for UIFR, where lower is preferable.

For metric \(m\), the reported effect is the average within-case difference after first averaging the available generator-specific complete-pair differences:

\[
\widehat{\Delta}_m=
\frac{1}{|Q|}\sum_{q\in Q}
\left(\frac{1}{|G_q|}\sum_{g\in G_q}
\bigl[m(E^{\mathrm{RuleRAG}}_{qg})-m(E^{\mathrm{NoRAG}}_{qg})\bigr]\right).
\tag{4.1}
\]

Here, \(Q\) is the set of underlying cases with at least one complete pair and \(G_q\) is the available generator set for case \(q\). The expression clarifies why three generator outputs for one case are not treated as three independent cases.

\Needspace{18\baselineskip}

| Metric | Paired cases | Difference | 95% CI | Holm-adjusted p |
| --- | ---: | ---: | ---: | ---: |
| Reranking-trace claim support rate | 498 | +21.02 pp | +19.72 to +22.37 pp | 0.0016 |
| Full-KB claim support rate | 498 | +21.40 pp | +20.11 to +22.71 pp | 0.0016 |
| Unsupported Item-Fact Rate | 53 | +0.63 pp | -5.03 to +5.66 pp | 0.9042 |
| Trace-supported claims per 100 words | 498 | +1.60 | +1.48 to +1.72 | 0.0016 |

*Table 4.2. Overall paired explanation contrasts (Rule-RAG minus No-RAG). Rate differences are percentage points; density remains in claims per 100 words.*

Rule-RAG substantially increased claims supported by both the exact trace and the wider final KB packet. The increase of 1.60 trace-supported claims per 100 words shows that the result is not merely an effect of output volume. For No-RAG, agreement with hidden B is post-hoc alignment; for Rule-RAG, support is evidence-grounded because B was available in the prompt.

Figure 4.1 visualises the four contrasts on their correct units, separating rate differences from claim density.

![](../artifacts/figures/final_explanation_paired_contrasts_corrected.png){width=95%}

*Figure 4.1. Paired explanation contrasts with 95% case-clustered bootstrap intervals.*

UIFR is inconclusive. It applies only when both paired explanations contain the relevant common-reference item-fact claim type, leaving 53 pairs. The interval includes both small benefit and small harm, so it cannot justify a corpus-wide claim that Rule-RAG reduces item-fact overreach.

## 4.7 Robustness, citations, and research questions

The primary support effects were positive for every generator. Trace-support differences were +25.09 percentage points for Gemma, +26.74 for Llama, and +11.35 for Ministral; full-KB differences were +25.22, +27.26, and +11.77 points. All corresponding confidence intervals excluded zero. All five categories also showed positive trace and full-KB support differences, with intervals excluding zero. This establishes directional robustness within the tested roster and categories, not universal generalisation.

Citation markers improve inspectability but are not treated as support. A claim can carry a malformed, irrelevant, or non-entailing rule identifier. The verified citation-entailment field is therefore essential: the experiment demonstrates source provenance and stronger source-grounded claim rates, but not that citation syntax alone validates a claim.

RQ1 is supported: trace exposure increased trace support by 21.02 points and full-KB support by 21.40 points. RQ2 is inconclusive because UIFR has sparse complete-pair eligibility. RQ3 is answered conservatively: citation syntax does not demonstrate citation entailment. RQ4 is supported for the primary support outcomes, whose direction held across all generators and categories; it is limited by failure asymmetry and sparse UIFR eligibility.

## 4.8 Missingness and failure accounting

The pipeline retained failure records at every stage. Of 3,000 generation attempts, 2,969 explanations were accepted. Of these, 2,965 were successfully extracted and 2,861 completed verification. This yields a final claim-verification coverage of 16,804 claims from 2,861 explanation records. Failures were not converted to zero claims, favourable labels, or synthetic replacements. Such handling would create a false appearance of complete coverage and could bias a comparison if a condition were more difficult to parse or verify.

The generation failures were not balanced: all 31 occurred in Llama Rule-RAG. This is a protocol-compliance limitation rather than evidence that Rule-RAG fails semantically. Still, it matters because a complete-pair estimate describes retained paired outputs, not the behaviour of cells that failed the output contract. The generator-specific pairing policy addresses the immediate statistical issue: it prevents a Rule-RAG total of 469 being compared with a No-RAG total of 500 as if the observations were paired. It does not turn missing outputs into evidence of success.

Verification failure was smaller but present in both conditions. Gemma had 22 No-RAG and three Rule-RAG terminal verification failures; Llama had 18 and 16; Ministral had 22 and 23. These counts show why missingness must be reported by generator and condition rather than as one aggregate percentage. The final results should be interpreted with the associated denominator table, particularly for secondary outcomes whose eligibility is already restricted.

## 4.9 Statistical checks

The overall explanation analysis uses the underlying case as the resampling unit because outputs from different generators share the same locked recommendation and evidence. The analysis first computes each available generator-specific paired difference, then averages available generator effects within case, and finally bootstraps cases. This procedure respects both repeated measurement and unequal complete-pair availability. It is more conservative than treating the 1,368 complete case--generator pairs as independent rows.

The reported confidence intervals are percentile intervals from 5,000 paired bootstrap replicates. Holm correction is applied across the four prespecified overall explanation outcomes. The three positive support outcomes have the smallest attainable two-sided bootstrap p-value in this design, 0.0004 before adjustment and 0.0016 after adjustment. This does not make the effects universally valid; it means that, conditional on the frozen cases, models, and evaluator, the observed paired support differences are precise and unlikely to have arisen from resampling variation alone.

The UIFR result illustrates why effect size, eligibility, and precision must be read together. Its point estimate is close to zero and its interval is much wider than those of the primary support metrics. The limiting factor is not merely a lack of arithmetic power; it is that a common-reference item-fact outcome is substantively defined only for a small subset of paired explanations. Reporting it as a null result with its denominator is more informative than either omitting it or extrapolating it to every output.

## 4.10 Reproducibility and audit trail

The final analysis is reproducible from frozen records rather than from regenerated language. Stage manifests bind the input and output hashes for each stage, including the final recommendation, explanation, extraction, verification, and analysis tables. The release record identifies the final verification SHA-256 as `0f554e58be51c0529c59814f3c5de379ec66c02afbb8fa2c5e48249a32ae9b3e`. The final implementation also passed `ruff check .` and 54 automated tests. These checks do not validate the substantive fashion rules or the models' semantic judgements, but they make record substitution, schema drift, and broken joins detectable.

The joins between stages were exact. Three thousand explanation records were attempted; 2,969 accepted Stage-2 outputs entered extraction; 2,965 accepted Stage-3 records entered verification; and 2,861 accepted Stage-4 records provided canonical claim labels. Claim identifiers were preserved from extraction into verification. The final analysis reads the Stage-4 schema directly, including trace support, full-KB support, common-reference support, and citation entailment. It does not use the legacy outcome names or intermediate experimental tables.

One provenance amendment is reported rather than concealed. The Stage-1 manifest preserves the original prompt-configuration hash and records that the final Stage-4 verifier contract used an authorised corrected configuration. The release is bound to the actual final prompt and configuration hashes. This was an interface and consistency correction, not a performance-oriented regeneration: no generator, extractor, or verifier call was repeated. The distinction is material because transparent provenance is preferable to pretending that a later detected contract defect never occurred.

## 4.11 Chapter summary

The recommendation experiment showed that fused CLIP was the strongest tested pathway overall, whereas evidence reranking was lower on every reported aggregate metric. The rule component nevertheless changed the top-ranked item in 26.5% of cases and produced an inspectable trace for the explanation experiment.

Under generator-specific complete pairing and case-clustered inference, Rule-RAG increased trace support by 21.02 percentage points, full-KB support by 21.40 points, and trace-supported claim density by 1.60 claims per 100 words. The UIFR comparison was inconclusive because only 53 pairs were eligible. These are source-specific automated-evaluation results, not evidence of human preference or universal factual correctness. Chapter 5 interprets their implications and limitations.

## References

[1] Järvelin, K. and Kekäläinen, J. (2002) ‘Cumulated gain-based evaluation of IR techniques’, *ACM Transactions on Information Systems*, 20(4), pp. 422–446. https://doi.org/10.1145/582415.582418.

[2] Efron, B. and Tibshirani, R.J. (1993) *An Introduction to the Bootstrap*. New York: Chapman & Hall/CRC. https://doi.org/10.1007/978-1-4899-4541-9.

[3] Holm, S. (1979) ‘A simple sequentially rejective multiple test procedure’, *Scandinavian Journal of Statistics*, 6(2), pp. 65–70. https://doi.org/10.2307/4615733.

[4] Jacovi, A. and Goldberg, Y. (2020) ‘Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?’, *Proceedings of ACL 2020*, pp. 4198–4205. https://doi.org/10.18653/v1/2020.acl-main.386.
