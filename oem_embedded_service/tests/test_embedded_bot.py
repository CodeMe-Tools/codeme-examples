"""Tests verifying the third-party sample application embeds Codeme via OEM SDK."""

import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from embedded_bot import AutonomousReviewBot


def test_review_bot_clean_code():
    bot = AutonomousReviewBot()
    target = Path("repos/codeme-community/src/codeme/syntax/__init__.py").resolve()
    report = bot.review_submission(target)

    assert report["verdict"] == "APPROVED"
    assert report["passed"] is True
    assert "syntax" in report["engines_evaluated"]
    assert report["third_party_telemetry"]["embedding_model"] == "direct_sdk_invocation"
    assert len(report["diagnostics"]) == 0


def test_review_bot_broken_syntax(tmp_path):
    bot = AutonomousReviewBot()
    bad_file = tmp_path / "broken.py"
    bad_file.write_text("def broken():\n    return (\n", encoding="utf-8")

    report = bot.review_submission(bad_file)
    assert report["verdict"] == "REJECTED"
    assert report["passed"] is False
    assert len(report["diagnostics"]) > 0
    assert any("CDM-" in d["code"] for d in report["diagnostics"])
