from __future__ import annotations

from .coherence import CoherenceGateAdapter, audit_prose
from .config import EngineConfig
from .profiles import WritingMode, normalize_mode
from .scripture import ScriptureProvenanceAdapter
from .states import State
from .v64 import run_engine as run_engine_v64


def _record_final_coherence(ctx, config) -> None:
    findings = audit_prose(ctx, ctx.prose, config)
    errors = [finding for finding in findings if finding.severity == "error"]
    for finding in findings:
        if finding.severity == "error":
            continue
        warning = f"COHERENCE {finding.code}: {finding.field}: {finding.message}"
        if warning not in ctx.warnings:
            ctx.warnings.append(warning)
    if not errors:
        return

    ctx.failed_checks = [
        f"[PROSE] COHERENCE {finding.code}: {finding.field}: {finding.message}"
        for finding in errors
    ]
    ctx.error = "ValidationError: final devotional coherence failed after editorial smoothing"
    if ctx.trace and ctx.trace[-1] is State.DONE:
        ctx.trace[-1] = State.ESCALATED


def run_engine(ctx, adapter, config=None):
    """Run the full v6.5 devotional pipeline.

    v6.5 keeps the v6.4 blueprint boundary and adds one coherence contract
    between the director brief and the finished devotional. Scripture source and
    rendering provenance are validated before chapter design begins, then the
    coherence contract is checked again after editorial smoothing. Fiction and
    nonfiction continue to use ``run_profiled_engine`` so devotional concerns do
    not leak into other profiles.
    """

    mode = normalize_mode(getattr(ctx, "mode", WritingMode.DEVOTIONAL.value))
    if mode is not WritingMode.DEVOTIONAL:
        raise ValueError(
            "run_engine is the full devotional pipeline. "
            "Use run_profiled_engine with WritingRequest for fiction or nonfiction."
        )
    resolved_config = config or EngineConfig()
    provenance_adapter = ScriptureProvenanceAdapter(adapter, resolved_config)
    result = run_engine_v64(
        ctx,
        CoherenceGateAdapter(provenance_adapter, resolved_config),
        resolved_config,
    )
    if result.trace and result.trace[-1] is State.DONE:
        _record_final_coherence(result, resolved_config)
    return result
