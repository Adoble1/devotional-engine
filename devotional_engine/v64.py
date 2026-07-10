from __future__ import annotations

from .blueprint import approve_blueprint, build_blueprint, validate_script_alignment
from .engine import run_engine as run_engine_v63
from .states import State


class BlueprintGateAdapter:
    """Adapter decorator that inserts the v6.4 plan-before-surface boundary."""

    def __init__(self, delegate):
        self.delegate = delegate

    def call(self, role: str, payload: dict) -> dict:
        ctx = payload.get("context")
        if role == "composer" and ctx is not None and ctx.blueprint is None:
            ctx.trace.append(State.STORY_PLAN_BLUEPRINT)
            ctx.blueprint = build_blueprint(ctx)
            # Legacy v6.3 risk fixtures lack status/severity metadata. They remain
            # constraints, but only explicitly unresolved high/critical risks block.
            ctx.blueprint.unresolved_risks = [
                risk
                for risk in ctx.blueprint.theological_risk_register
                if str(risk.get("status", "")).lower() in {"open", "unresolved"}
                and str(risk.get("severity", "")).lower() in {"high", "critical"}
            ]
            ctx.trace.append(State.BLUEPRINT_VALIDATION)
            findings = approve_blueprint(ctx.blueprint)
            ctx.blueprint_findings = findings
            if findings:
                fields = ", ".join(sorted({finding.field for finding in findings}))
                raise ValueError(f"Story Plan Blueprint failed validation: {fields}")
        result = self.delegate.call(role, payload)
        if role == "poet" and ctx is not None and ctx.blueprint is not None:
            poem = result.get("poem", "") if isinstance(result, dict) else ""
            ctx.alignment_findings = validate_script_alignment(ctx.blueprint, ctx.prose, poem)
            if ctx.alignment_findings:
                ctx.warnings.extend(
                    f"BLUEPRINT_ALIGNMENT {finding.code}: {finding.field}: {finding.message}"
                    for finding in ctx.alignment_findings
                )
        return result


def run_engine(ctx, adapter, config=None):
    """Run v6.4 using the existing guarded engine plus a mandatory blueprint gate."""
    return run_engine_v63(ctx, BlueprintGateAdapter(adapter), config)
