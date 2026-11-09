"""Sample third-party application embedding Codeme engines via codeme-oem-sdk.

Demonstrates programmatic execution, independent structured telemetry,
and total isolation from CLI presentation formatting.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional
from codeme_oem_sdk import CodemeEngineClient, InvocationResult


class AutonomousReviewBot:
    """Third-party autonomous review agent embedding Codeme engine."""

    def __init__(self, client: Optional[CodemeEngineClient] = None):
        self.client = client or CodemeEngineClient()

    def review_submission(
        self,
        target_path: str | Path,
        fix: bool = False,
    ) -> Dict[str, Any]:
        """Runs multi-engine analysis programmatically and returns a custom review report."""
        p = Path(target_path).resolve()
        engines_run: List[str] = []
        all_diagnostics: List[Dict[str, Any]] = []
        total_tokens_saved = 0
        total_duration_ms = 0.0
        passed = True

        # 1. Syntax Verification
        syntax_res: InvocationResult = self.client.syntax(p, fix=fix)
        engines_run.append("syntax")
        total_tokens_saved += syntax_res.token_metrics.estimated_tokens_saved
        total_duration_ms += syntax_res.duration_ms
        if syntax_res.status != "success":
            passed = False
            all_diagnostics.extend([d.to_dict() for d in syntax_res.diagnostics])

        # 2. Quality Verification (if syntax passed)
        if passed:
            quality_res: InvocationResult = self.client.quality(p, fix=fix)
            engines_run.append("quality")
            total_tokens_saved += quality_res.token_metrics.estimated_tokens_saved
            total_duration_ms += quality_res.duration_ms
            if quality_res.status != "success":
                passed = False
                all_diagnostics.extend([d.to_dict() for d in quality_res.diagnostics])

        # 3. Invariant Verification
        if passed and p.is_dir():
            inv_res: InvocationResult = self.client.invariant(p, invariant_class="all")
            engines_run.append("invariant")
            total_tokens_saved += inv_res.token_metrics.estimated_tokens_saved
            total_duration_ms += inv_res.duration_ms
            if inv_res.status != "success":
                passed = False
                all_diagnostics.extend([d.to_dict() for d in inv_res.diagnostics])

        return {
            "verdict": "APPROVED" if passed else "REJECTED",
            "passed": passed,
            "target": str(p),
            "engines_evaluated": engines_run,
            "total_duration_ms": round(total_duration_ms, 2),
            "diagnostics": all_diagnostics,
            "token_metrics": {
                "estimated_tokens_saved": total_tokens_saved,
                "efficiency_gain": "high" if total_tokens_saved > 0 else "nominal",
            },
            "third_party_telemetry": {
                "bot_version": "1.0.0",
                "embedding_model": "direct_sdk_invocation",
            },
        }
