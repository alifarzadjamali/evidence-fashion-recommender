---
title: "Evidence-Constrained Multimodal Fashion Recommendation with Trace-Grounded Explanations"
author: "[Candidate name required]"
date: "[Submission month and year required]"
subtitle: |
  A thesis submitted in partial fulfilment of the requirements for the degree of Master of Philosophy  
  University of Salford  
  [School/department required]  
  Student ID: [Student ID required]  
  Supervisors: [Supervisor names required]
geometry: "a4paper,margin=30mm"
fontsize: 11pt
linestretch: 1.35
colorlinks: true
linkcolor: black
urlcolor: blue
toc: true
toc-depth: 3
numbersections: false
header-includes:
  - |
    ```{=latex}
    \usepackage{microtype}
    \usepackage{booktabs}
    \usepackage{longtable}
    \usepackage{graphicx}
    \usepackage{float}
    \usepackage{needspace}
    \usepackage{etoolbox}
    \AtBeginEnvironment{longtable}{\small}
    ```
include-before:
  - |
    ```{=latex}
    \clearpage
    ```
---

# Declaration

**Candidate action required before submission:** insert the exact declaration wording required by
the applicable University of Salford/PGR template, then sign or otherwise complete it in the
required form. No institutional declaration wording has been invented in this repository.

\newpage

# Acknowledgements

**Candidate action required before submission:** complete or remove this section according to the
candidate's preference and institutional requirements.

\newpage

# Abstract

Multimodal fashion recommenders can use images and product text to rank compatible items, but a
fluent explanation need not reflect evidence that influenced the ranking. This thesis investigates
an evidence-constrained pipeline that links recommendation and explanation through an explicit
decision trace. Frozen CLIP image and text representations rank same-category candidates from
held-out Polyvore outfits. A manually curated, source-grounded experimental knowledge base of 200
fashion rules supplies a separate evidence score; up to five eligible rules are retained as the
symbolic trace used in reranking. The selected item is then locked, and paired No-RAG and Rule-RAG
explanations differ only in access to that trace and its associated grounding instructions.

The recommendation experiment contains 1,000 cases across five categories. Fused CLIP was the
strongest tested method overall on the conventional top-five, top-ten, NDCG, and reciprocal-rank
measures. Evidence reranking changed the top-ranked item in 26.5% of cases but did not improve any
reported aggregate recommendation metric relative to fused CLIP. The explanation experiment used
500 evidence-eligible cases and three local generators. Under generator-specific complete pairing
and case-clustered inference, trace access increased reranking-trace claim support by 21.02
percentage points (95% CI 19.72--22.37) and full-KB claim support by 21.40 points (20.11--22.71).
Trace-supported claims per 100 words increased by 1.60 (1.48--1.72). The common-reference
Unsupported Item-Fact Rate was inconclusive because only 53 complete pairs were eligible.

The principal contribution is therefore not a state-of-the-art ranking claim. It is an auditable
evidence-to-decision-to-explanation connection: the pipeline preserves the exact symbolic evidence
that participated in reranking, reuses that evidence during explanation, and evaluates generated
claims against explicit source boundaries. The result demonstrates stronger trace-grounded support
under the frozen automated evaluator while retaining the negative ranking result and the limits of
a finite curated knowledge base and non-human explanation assessment.

\newpage

# Abbreviations

| Abbreviation | Meaning |
|---|---|
| CI | Confidence interval |
| CLIP | Contrastive Language--Image Pre-training |
| FITB | Fill in the blank |
| HR | Hit rate |
| KB | Knowledge base |
| KG | Knowledge graph |
| LLM | Large language model |
| MRR | Mean reciprocal rank |
| NDCG | Normalised discounted cumulative gain |
| RAG | Retrieval-augmented generation |
| UIFR | Unsupported Item-Fact Rate |

\newpage

# List of figures

- **Figure 4.1.** Paired explanation contrasts with 95% case-clustered bootstrap intervals.

\newpage

# List of tables

- **Table 2.1.** Representative research strands and the gap addressed by this thesis.
- **Table 4.1.** Micro-averaged recommendation effectiveness on 1,000 frozen test cases.
- **Table 4.2.** Overall paired explanation contrasts (Rule-RAG minus No-RAG).

\newpage
