from __future__ import annotations

from .coherence import CoherenceGateAdapter
from .config import EngineConfig
from .profiles import WritingMode, normalize_mode
from .v64 import run_engine as run_engine_v64


def run_engine(ctx, adapter, config=None):
    """Run the full v6.5 devotional pipeline.

    v6.5 keeps the v6.4 blueprint boundary and adds one coherence contract
    between the director brief and the finished devotional. Fiction and
    nonfiction continue to use ``run_profiled_engine`` so devotional concerns
    do not leak into other profiles.
    """

    mode = normalize_mode(getattr(ctx, "mode", WritingMode.DEVOTIONAL.value))
    if mode is not WritingMode.DEVOTIONAL:
        raise ValueError(
            "run_engine is the full devotional pipeline. "
            "Use run_profiled_engine with WritingRequest for fiction or nonfiction."
        )
    resolved_config = config or EngineConfig()
    return run_engine_v64(ctx, CoherenceGateAdapter(adapter, resolved_config), resolved_config)
