from dataclasses import dataclass, field

ROLE_CONFIG = {
    "source_agent": {"temperature": 0.1}, "translator": {"temperature": 0.15},
    "chapter_design_mapper": {"temperature": 0.35}, "canonist": {"temperature": 0.25},
    "theological_risk_agent": {"temperature": 0.2}, "historian_linguist": {"temperature": 0.2},
    "commentary_agent": {"temperature": 0.2}, "art_director": {"temperature": 0.65},
    "creative_divergence_agent": {"temperature": 0.9}, "director": {"temperature": 0.55},
    "voice_keeper": {"temperature": 0.45}, "composer": {"temperature": 0.8},
    "poet": {"temperature": 1.0}, "beauty_pass_agent": {"temperature": 0.35},
    "evaluator": {"temperature": 0.1}, "contradiction_editor": {"temperature": 0.1},
    "editorial_smoother": {"temperature": 0.18},
    # Lean shared-core roles for fiction and nonfiction.
    "profile_planner": {"temperature": 0.35},
    "profile_composer": {"temperature": 0.8},
    "profile_evaluator": {"temperature": 0.1},
    "profile_reviser": {"temperature": 0.45},
}
MAX_GATE_REVISIONS = 2
MAX_CHECKER_LOOPS = 3
MAX_EVAL_PASSES = 2
MAX_EDITORIAL_LOOPS = 2
MAX_VOICE_REVISIONS = 2
MAX_BEAUTY_LOOPS = 2
MAX_CONTRADICTION_LOOPS = 2
MAX_STATE_TRANSITIONS = 250


@dataclass
class EngineConfig:
    threshold_min_words: int = 3
    threshold_max_words: int = 9
    poem_form: str = "open"
    poem_stanza_counts: tuple[int, ...] = (4, 5)
    open_poem_min_lines: int = 4
    open_poem_max_lines: int = 40
    breath_word_limit: int = 28
    source_min_chars: int = 20
    enable_american_literary_patterns: bool = True
    enable_classical_hymnody: bool = True
    enable_poetic_music: bool = True
    american_style_match_limit: int = 4
    require_full_focus_verses: bool = False
    require_key_verse_selection: bool = False
    enforce_same_chapter_reference_style: bool = False
    warn_unnecessary_adverbs: bool = False
    warn_image_physics: bool = False
    warn_explanatory_poem: bool = False
    warn_grounded_qualia: bool = False
    warn_poem_music: bool = False
    strict_beauty_warnings: bool = False
    beauty_warning_ids: tuple[str, ...] = ("D24", "D25", "D26", "D27")
    qualia_min_grounded_terms: int = 2
    qualia_max_emotion_to_grounded_ratio: int = 3
    focus_verses_min_words: int = 35
    profiled_max_revisions: int = 1
    mode: str = "devotional"
    # v6.5 coherence contract. Hard checks protect the plan boundary; warnings
    # surface repetition or theme displacement without forcing safe sameness.
    enforce_instruction_coherence: bool = True
    enforce_title_opening_distinction: bool = True
    warn_cross_section_repetition: bool = True
    warn_theme_displacement: bool = True
    max_state_transitions: int = MAX_STATE_TRANSITIONS
    max_gate_revisions: int = MAX_GATE_REVISIONS
    max_checker_loops: int = MAX_CHECKER_LOOPS
    max_eval_passes: int = MAX_EVAL_PASSES
    max_editorial_loops: int = MAX_EDITORIAL_LOOPS
    max_voice_revisions: int = MAX_VOICE_REVISIONS
    max_beauty_loops: int = MAX_BEAUTY_LOOPS
    max_contradiction_loops: int = MAX_CONTRADICTION_LOOPS
    role_config: dict = field(default_factory=lambda: ROLE_CONFIG.copy())
