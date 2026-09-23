# Evidence-Constrained Multimodal Fashion Recommendation

This repository contains the frozen experiment and thesis materials for a study of
evidence-constrained multimodal fashion recommendation. It evaluates controlled sampled-pool
recommendation across `tops`, `bottoms`, `shoes`, `outerwear`, and `bags`, then tests whether
explanations conditioned on the exact source-grounded fashion-rule trace used for reranking are
more evidentially grounded.

The sole active knowledge base is `data/kb/fashion_rules.csv`: 200 manually curated,
source-grounded experimental rules, 40 for each target category. It is not a universal fashion
ontology or independently certified professional guidance. The confirmatory operating point is
fixed at 0.40 image / 0.60 CLIP text and 0.75 CLIP / 0.25 rule evidence with up to five applicable
rules. Validation grids are descriptive sensitivity analyses only.

The frozen results are deliberately mixed. Fused CLIP was the strongest tested conventional
ranking pathway overall; evidence reranking did not improve aggregate recommendation metrics.
The reranker did create an inspectable decision trace, and supplying that exact trace to the
explanation generator increased trace-supported claim rate by 21.02 percentage points and
full-KB-supported claim rate by 21.40 points in the final paired experiment.

The run is governed by five approval-gated stages:

1. preflight, clean reset, and final freeze;
2. final recommendations and 3,000 fresh explanations;
3. fresh atomic-claim extraction;
4. fresh claim verification;
5. final analysis and release closure.

Canonical runtime outputs are under `.runtime/current/`; compact reproducibility materials are
published only after release in `artifacts/release/`. Earlier development outputs are not active
results.

## Active scope

The active tree contains the final experiment, its frozen release artefacts, and the paper and
thesis materials. A small `archive/` retains explicitly labelled superseded material for research
provenance; archived files are not active results and are not part of the published pipeline.

## Repository guide

- `src/` contains the package implementation.
- `scripts/` contains the staged analysis and release utilities.
- `data/` contains tracked metadata and the frozen knowledge base; generated datasets are ignored.
- `artifacts/release/` contains the immutable compact release; `artifacts/tables/` and
  `artifacts/figures/` contain presentation copies and regenerated figures.
- `paper/` contains the manuscript sources and submission-ready document files.
- `thesis/` contains the edited chapter sources, consolidated thesis source, bibliography, and
  rendered document files.
- `FINAL_AUDIT_REPORT.md`, `SUBMISSION_CHECKLIST.md`, and `CORRECTION_LOG.md` record the final
  submission audit and outstanding author/institutional actions.

## Reproduce the final run

The repository contains code, configuration, the frozen 200-rule knowledge base, and the compact
published results. It intentionally does **not** contain the Polyvore dataset, model caches,
embedding arrays, runtime outputs, or Ollama model files. A fresh run therefore requires the
following before execution.

1. Python 3.11, Git, and [uv](https://docs.astral.sh/uv/). Create the environment with
   `uv sync --frozen --extra dev`.
2. Network access to the public Hugging Face dataset
   [`Marqo/polyvore`](https://huggingface.co/datasets/Marqo/polyvore). The pipeline downloads the
   pinned revision `8c782ee447faf2d2a0402ac883cf07d3b3f43e1c` recorded in
   [`configs/experiment.yaml`](configs/experiment.yaml).
3. Local cached copies of the exact Hugging Face model revisions. Run
   `uv run python scripts/cache_huggingface_models.py`; this downloads the MiniLM and CLIP
   revisions recorded in [`configs/models.yaml`](configs/models.yaml). The pipeline deliberately
   uses local-only model loading after this step.
4. A running Ollama server compatible with the configured `http://127.0.0.1:11434` endpoint and
   these exact model tags: `qwen3-embedding:0.6b`, `gemma4:12b`,
   `llama3.1:8b-instruct-q8_0`, `ministral-3:14b-instruct-2512-q4_K_M`, `qwen3.5:9b`, and
   `phi4:14b`. Their expected revisions and recorded immutable digests are in
   [`configs/models.yaml`](configs/models.yaml). Use the configured tags and inspect the local
   Ollama model metadata before running; model tags can otherwise be mutable.
5. Adequate local disk, memory, and preferably GPU resources for the dataset embeddings and the
   listed local models. The pipeline is designed for sequential local-model execution, not a
   lightweight laptop run.

First validate the local setup without downloading data or generating outputs:

```bash
uv run python scripts/run_final_pipeline.py --check
```

For repository-only verification, run:

```bash
uv run python scripts/audit_final_release.py
uv run pytest -q
uv run ruff check .
```

The release audit accepts either the exact recorded hashes or the corresponding Git-normalised LF
form for five Windows-authored text artifacts; it reports which form was found. It then recomputes
the recommendation metrics and checks the final explanation counts and trace-subset invariant.

Then run all stages in order. This writes a new isolated reproduction package and never overwrites
the committed final results:

```bash
uv run python scripts/run_final_pipeline.py --run
```

By default, outputs are placed below `.runtime/reproductions/<timestamp>/`. To choose a location,
pass `--run-root D:\path\to\new-run`. The generated release directory contains its own manifests,
tables, figures, and hashes for comparison with the committed release package.

The Docker image runs the same prerequisite check by default. For a containerized run, mount the
Hugging Face cache and make Ollama reachable from the container (for example, set the endpoint in
a copied models configuration to `http://host.docker.internal:11434`); direct host execution is
the supported default.
