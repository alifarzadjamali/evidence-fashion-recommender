"""Audit the compact frozen release without rerunning model-dependent stages."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path, PureWindowsPath

import numpy as np
import pandas as pd

from evidence_fashion.kb_audit import coverage_matrix, load_canonical_rules

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "artifacts" / "release"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def recorded_hash_matches(path: Path, expected: str) -> tuple[bool, str]:
    data = path.read_bytes()
    if sha256(data) == expected:
        return True, "exact"
    # The release was created on Windows. Git may normalise tracked text files to LF.
    if b"\r\n" not in data and sha256(data.replace(b"\n", b"\r\n")) == expected:
        return True, "git_line_ending_normalised"
    return False, "mismatch"


def read_jsonl(name: str) -> list[dict[str, object]]:
    return [json.loads(line) for line in (RELEASE / name).read_text(encoding="utf-8").splitlines()]


def recommendation_means(rankings: list[dict[str, object]]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    methods = ("minilm_text", "clip_image", "clip_text", "fused_clip", "evidence_rerank")
    for record in rankings:
        case = record["case"]
        positives = {
            item_id
            for item_id, relevant in zip(
                case["candidate_item_ids"], case["candidate_relevance"], strict=True
            )
            if relevant
        }
        for method in methods:
            ranked = record["ranked_candidate_ids"][method]
            rank = next((i + 1 for i, item_id in enumerate(ranked) if item_id in positives), None)
            rows.append(
                {
                    "method": method,
                    "hr_at_1": float(rank == 1),
                    "hr_at_5": float(rank is not None and rank <= 5),
                    "hr_at_10": float(rank is not None and rank <= 10),
                    "ndcg_at_1": float(rank == 1),
                    "ndcg_at_5": 1 / np.log2(rank + 1) if rank and rank <= 5 else 0.0,
                    "ndcg_at_10": 1 / np.log2(rank + 1) if rank and rank <= 10 else 0.0,
                    "mrr": 1 / rank if rank else 0.0,
                }
            )
    return pd.DataFrame(rows).groupby("method").mean(numeric_only=True)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    manifest = json.loads((RELEASE / "release_manifest.json").read_text(encoding="utf-8"))
    portability = Counter()
    for recorded_name, expected in {**manifest["files"], **manifest["figures"]}.items():
        name = PureWindowsPath(recorded_name).name
        directory = (
            RELEASE
            if recorded_name in manifest["files"]
            else ROOT / "artifacts" / "figures"
        )
        path = directory / name
        require(path.exists(), f"Missing released artifact: {path}")
        valid, mode = recorded_hash_matches(path, expected)
        require(valid, f"Hash mismatch: {path}")
        portability[mode] += 1

    rules = load_canonical_rules(ROOT / "data" / "kb" / "fashion_rules.csv")
    require(len(rules) == 200, "Canonical KB must contain 200 rules")
    require(
        rules.groupby("recommended_category").size().eq(40).all(),
        "Canonical KB must contain 40 rules per target category",
    )
    require(rules["source_url_or_reference"].nunique() == 39, "Unexpected KB source count")
    derived_coverage = coverage_matrix(rules).reset_index()
    stored_coverage = pd.read_csv(ROOT / "data" / "kb" / "coverage_matrix.csv")
    pd.testing.assert_frame_equal(derived_coverage, stored_coverage, check_names=False)

    rankings = read_jsonl("candidate_rankings.jsonl")
    require(len(rankings) == 1000, "Expected 1,000 recommendation cases")
    require(
        len({row["case"]["query_outfit_id"] for row in rankings}) == 734,
        "Expected 734 unique query outfits",
    )
    recomputed = recommendation_means(rankings)
    released = pd.read_csv(RELEASE / "recommendation_metrics_with_ci.csv")
    released = released[(released["aggregation"] == "micro") & (released["category"] == "all")]
    for row in released.itertuples(index=False):
        require(
            np.isclose(recomputed.loc[row.method, row.metric], row.estimate, atol=1e-12),
            f"Recommendation metric mismatch: {row.method}/{row.metric}",
        )

    explanations = read_jsonl("explanations.jsonl")
    extractions = read_jsonl("extractions.jsonl")
    verifications = read_jsonl("verifications.jsonl")
    require(len(explanations) == 3000, "Expected 3,000 attempted explanation cells")
    accepted_explanations = [row for row in explanations if row["status"] == "accepted"]
    accepted_extractions = [row for row in extractions if row["status"] == "accepted"]
    accepted_verifications = [row for row in verifications if row["status"] == "accepted"]
    require(len(accepted_explanations) == 2969, "Expected 2,969 accepted explanations")
    require(len(accepted_extractions) == 2965, "Expected 2,965 accepted extractions")
    require(len(accepted_verifications) == 2861, "Expected 2,861 accepted verifications")
    require(
        sum(len(row["claims"]) for row in accepted_extractions) == 17710,
        "Expected 17,710 extracted claims",
    )
    claims = [claim for row in accepted_verifications for claim in row["claims"]]
    require(len(claims) == 16804, "Expected 16,804 verified claims")
    require(
        not any(
            claim["trace_support"] == "supported"
            and claim["full_kb_support"] != "supported"
            for claim in claims
        ),
        "Trace-subset/full-KB consistency invariant failed",
    )

    trace_counts = Counter(claim["trace_support"] for claim in claims)
    full_counts = Counter(claim["full_kb_support"] for claim in claims)
    require(trace_counts["supported"] == 2058, "Unexpected trace-supported claim count")
    require(full_counts["supported"] == 2095, "Unexpected full-KB-supported claim count")
    word_means = (
        pd.DataFrame(accepted_explanations).groupby("condition")["word_count"].mean().to_dict()
    )
    require(np.isclose(word_means["no_rag"], 62.104), "Unexpected No-RAG word mean")
    require(np.isclose(word_means["rule_rag"], 64.827773), "Unexpected Rule-RAG word mean")

    contrasts = pd.read_csv(RELEASE / "explanation_paired_contrasts.csv")
    overall = contrasts[contrasts["scope"] == "overall"].set_index("metric")
    expected_effects = {
        "trace_support_rate": (498, 0.21016210498481688),
        "full_kb_support_rate": (498, 0.2140414604203972),
        "unsupported_item_fact_rate": (53, 0.006289308176100628),
        "trace_supported_claims_per_100_words": (498, 1.5975608742682565),
    }
    for metric, (cases, estimate) in expected_effects.items():
        require(int(overall.loc[metric, "paired_cases"]) == cases, f"Pair count mismatch: {metric}")
        require(np.isclose(overall.loc[metric, "estimate"], estimate), f"Effect mismatch: {metric}")

    print("PASS: frozen release hashes and deterministic results verified")
    print(f"Hash modes: {dict(portability)}")
    print("Recommendation cases: 1000; explanation cells: 3000; verified claims: 16804")


if __name__ == "__main__":
    main()
