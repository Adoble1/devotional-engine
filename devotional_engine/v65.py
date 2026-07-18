from __future__ import annotations

from dataclasses import replace

from .coherence import CoherenceGateAdapter, audit_prose
from .config import EngineConfig
from .integrated import adapter_supports_integrated_devotional, run_integrated_devotional
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


def _run_legacy(ctx, adapter, config):
    """Compatibility path for pre-v6.6 deterministic fixtures."""

    ctx.pipeline_mode = "legacy"
    provenance_adapter = ScriptureProvenanceAdapter(adapter, config)
    result = run_engine_v64(
        ctx,
        CoherenceGateAdapter(provenance_adapter, config),
        config,
    )
    if result.trace and result.trace[-1] is State.DONE:
        _record_final_coherence(result, config)
    return result


def run_engine(ctx, adapter, config=None):
    """Run the devotional engine.

    Production adapters use the four-stage integrated path: Text Grounding,
    Passage Blueprint, protected Composition, and Integrated Review. Existing
    deterministic fixtures without those four roles continue through the legacy
    compatibility runner so the refactor remains regression-safe.
    """

    mode = normalize_mode(getattr(ctx, "mode", WritingMode.DEVOTIONAL.value))
    if mode is not WritingMode.DEVOTIONAL:
        raise ValueError(
            "run_engine is the devotional pipeline. "
            "Use run_profiled_engine with WritingRequest for fiction or nonfiction."
        )

    resolved_config = config or EngineConfig()
    requested = str(getattr(resolved_config, "devotional_pipeline", "auto")).strip().lower()
    if requested not in {"auto", "integrated", "legacy"}:
        raise ValueError("devotional_pipeline must be auto, integrated, or legacy")

    use_integrated = requested == "integrated" or (
        requested == "auto" and adapter_supports_integrated_devotional(adapter)
    )
    if use_integrated:
        # Threshold phrases belonged to the legacy surface pipeline. The
        # integrated blueprint protects meaning and movement while leaving the
        # composer free to discover the opening.
        integrated_config = replace(
            resolved_config,
            threshold_min_words=0,
            threshold_max_words=0,
        )
        return run_integrated_devotional(ctx, adapter, integrated_config)
    return _run_legacy(ctx, adapter, resolved_config)
