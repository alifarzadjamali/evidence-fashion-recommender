from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

from evidence_fashion.kb_audit import coverage_matrix, load_canonical_rules


def test_derived_kb_audits_match_frozen_rules(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "scripts/rebuild_kb_audits.py",
            "--output-dir",
            str(tmp_path),
        ],
        check=True,
    )
    rules = load_canonical_rules("data/kb/fashion_rules.csv")
    stored_coverage = pd.read_csv(tmp_path / "coverage_matrix.csv")
    pd.testing.assert_frame_equal(
        coverage_matrix(rules).reset_index(), stored_coverage, check_names=False
    )

    registry = pd.read_csv(tmp_path / "kb_source_registry.csv")
    assert len(registry) == 39
    assert registry["rule_count"].sum() == 200
    assert set("|".join(registry["rule_ids"]).split("|")) == set(rules["rule_id"])
    assert pd.read_csv(tmp_path / "kb_rule_similarity_audit.csv").empty
