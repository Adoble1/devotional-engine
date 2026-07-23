from dataclasses import dataclass, field


@dataclass
class EngineContext:
    chapter_ref: str
    source_text: str = ""
    mt_text: str = ""
    lxx_text: str = ""
    working_rendering: str = ""
    source_layer: dict = field(default_factory=dict)
    rendering_layer: dict = field(default_factory=dict)
    scripture_provenance: dict = field(default_factory=dict)
    chapter_design_map: dict = field(default_factory=dict)
    correspondence: dict = field(default_factory=dict)
    theological_risk_register: list = field(default_factory=list)
    historical_linguistic: dict = field(default_factory=dict)
    commentary_grounding: dict = field(default_factory=dict)
    ontological_overlay: dict = field(default_factory=dict)
    art_direction: dict = field(default_factory=dict)
    literary_style: dict = field(default_factory=dict)
    creative_divergence: dict = field(default_factory=dict)
    brief: dict = field(default_factory=dict)
    blueprint: object | None = None
    blueprint_findings: list = field(default_factory=list)
    alignment_findings: list = field(default_factory=list)
    grounding_packet: dict = field(default_factory=dict)
    integrated_review: dict = field(default_factory=dict)
    pipeline_mode: str = ""
    prose: dict = field(default_factory=dict)
    poem: str = ""
    artifact: str = ""
    ledger: dict = field(default_factory=lambda: {"entries": []})
    warnings: list = field(default_factory=list)
    failed_checks: list = field(default_factory=list)
    scores: dict = field(default_factory=dict)
    draft_log: list = field(default_factory=list)
    trace: list = field(default_factory=list)
    gate_revisions: int = 0
    checker_loops: int = 0
    eval_passes: int = 0
    editorial_loops: int = 0
    voice_revisions: int = 0
    beauty_loops: int = 0
    contradiction_loops: int = 0
    error: str = ""
    mode: str = "devotional"
    planning_packet: object | None = None
