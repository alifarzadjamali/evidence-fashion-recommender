"""Rebuild presentation audits from the immutable canonical fashion-rule CSV.

This script never edits ``fashion_rules.csv``.  It regenerates only the three
derived, human-readable audit tables stored beside that frozen research input.
"""

from __future__ import annotations

import argparse
import re
from difflib import SequenceMatcher
from itertools import combinations
from pathlib import Path

import pandas as pd

from evidence_fashion.kb_audit import coverage_matrix, load_canonical_rules


def normalized_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def source_registry(rules: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    metadata = [
        "source_title",
        "source_author_or_org",
        "source_year",
        "source_access_date",
        "source_validation_status",
    ]
    for source_url, group in rules.groupby("source_url_or_reference", sort=True):
        if group[metadata].nunique().gt(1).any():
            raise ValueError(f"Inconsistent source metadata for {source_url}")
        first = group.iloc[0]
        rows.append(
            {
                "source_url_or_reference": source_url,
                **{field: first[field] for field in metadata},
                "rule_count": len(group),
                "rule_ids": "|".join(group["rule_id"]),
                "distinct_locators": group["source_locator"].nunique(),
                "reliability_labels": "|".join(
                    sorted(set(group["source_reliability"].str.lower()))
                ),
            }
        )
    return pd.DataFrame(rows)


def similarity_audit(rules: pd.DataFrame, threshold: float) -> pd.DataFrame:
    columns = [
        "left_rule_id",
        "right_rule_id",
        "sequence_similarity",
        "same_target",
        "same_query_applicability",
        "same_source_page",
        "audit_decision",
    ]
    rows: list[dict[str, object]] = []
    records = rules.to_dict("records")
    for left, right in combinations(records, 2):
        similarity = SequenceMatcher(
            None, normalized_text(left["rule_text"]), normalized_text(right["rule_text"])
        ).ratio()
        if similarity < threshold:
            continue
        rows.append(
            {
                "left_rule_id": left["rule_id"],
                "right_rule_id": right["rule_id"],
                "sequence_similarity": similarity,
                "same_target": left["recommended_category"]
                == right["recommended_category"],
                "same_query_applicability": left["applicable_query_categories"]
                == right["applicable_query_categories"],
                "same_source_page": left["source_url_or_reference"]
                == right["source_url_or_reference"],
                "audit_decision": "review_required",
            }
        )
    return pd.DataFrame(rows, columns=columns)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kb", type=Path, default=Path("data/kb/fashion_rules.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/kb"))
    parser.add_argument("--similarity-threshold", type=float, default=0.90)
    args = parser.parse_args()

    rules = load_canonical_rules(args.kb)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "coverage_matrix.csv": coverage_matrix(rules).reset_index(),
        "kb_source_registry.csv": source_registry(rules),
        "kb_rule_similarity_audit.csv": similarity_audit(
            rules, args.similarity_threshold
        ),
    }
    for name, table in outputs.items():
        table.to_csv(args.output_dir / name, index=False, lineterminator="\n")
        print(f"{name}: {len(table)} rows")


if __name__ == "__main__":
    main()
