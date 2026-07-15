from __future__ import annotations

from .profiles import WritingMode, normalize_mode
from .v64 import run_engine as run_engine_v64


def run_engine(ctx, adapter, config=None):
    """Run the full v6.5 devotional pipeline.

    Fiction and nonfiction use ``run_profiled_engine`` so their profile-specific
    contracts are not forced through devotional sections and theological gates.
    """

    mode = normalize_mode(getattr(ctx, "mode", WritingMode.DEVOTIONAL.value))
    if mode is not WritingMode.DEVOTIONAL:
        raise ValueError(
            "run_engine is the full devotional pipeline. "
            "Use run_profiled_engine with WritingRequest for fiction or nonfiction."
        )
    return run_engine_v64(ctx, adapter, config)
