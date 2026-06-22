from copy import deepcopy
from .config import EngineConfig
from .evaluator import run_beauty_pass, validate_evaluation
from .exceptions import AgentOutputError, ValidationError
from .harness import chapter_arc_gate, run_deterministic_harness
from .american_literature import build_style_brief, match_american_patterns
from .classical_hymnody import build_hymnody_brief
from .poetic_music import build_poetic_music_brief
from .ledger import update_ledger
from .renderer import render_artifact, validate_artifact_structure
from .states import State

CHAPTER_DESIGN_FIELDS = {"chapter_start", "chapter_end", "emotional_movement", "divine_action", "physical_vocabulary", "central_theological_claim", "christward_fulfillment", "reader_felt_experience", "chapter_design_summary"}
RISK_FIELDS = {"risk_id", "risk_description", "why_it_matters", "avoidance_rule", "evaluator_check"}
ART_DIRECTION_FIELDS = {"register", "pace", "sentence_music", "image_density", "emotional_color", "opening_mode", "poem_tone", "ending_resonance", "avoid"}
CREATIVE_DIVERGENCE_MINIMUMS = {"threshold_phrase_candidates": 5, "introduction_opening_candidates": 3, "governing_image_candidates": 3, "christology_framing_candidates": 2, "poem_arc_candidates": 2, "title_candidates": 3, "epigraph_candidates": 3}
DIRECTOR_BRIEF_FIELDS = {"chapter_burden", "opening_movement", "closing_movement", "central_thought", "emotional_charge", "transcendent_force", "selected_threshold_phrase", "threshold_phrase_rationale", "governing_image", "image_lexicon", "image_head_terms", "anchor_terms", "chapter_specific_terms", "christology_required_echoes", "christology_pathway", "application_target", "theological_terminus", "negative_constraints", "poem_plan", "semantic_proof_chain"}
PROSE_FIELDS = {"title", "epigraph", "focus_bible_verses", "introduction", "reflection", "christ_fulfillment", "application", "prayer", "next_in_sequence"}
CONTRADICTION_VERDICTS = {"Pass", "Pass with revisions", "Fail"}


def _required(output, fields, role):
    missing = fields - output.keys()
    if missing or any(output.get(k) in (None, "") for k in fields):
        raise ValidationError(f"{role} missing required fields: {', '.join(sorted(missing or {k for k in fields if output.get(k) in (None, '')}))}")
    return output


def validate_risks(output):
    risks = output.get("risks") if isinstance(output, dict) else output
    if not isinstance(risks, list) or not risks or any(not isinstance(r, dict) or RISK_FIELDS - r.keys() for r in risks):
        raise ValidationError("theological risk register must contain complete risk dictionaries")
    return risks


def validate_divergence(output):
    _required(output, set(CREATIVE_DIVERGENCE_MINIMUMS), "creative_divergence_agent")
    for key, minimum in CREATIVE_DIVERGENCE_MINIMUMS.items():
        if not isinstance(output[key], list) or len(output[key]) < minimum:
            raise ValidationError(f"{key} requires at least {minimum} candidates")
    return output


def validate_contradiction_result(result):
    if not isinstance(result, dict):
        raise ValidationError("contradiction_editor output must be a dictionary")
    verdict = result.get("verdict")
    if verdict not in CONTRADICTION_VERDICTS:
        raise ValidationError("contradiction_editor verdict invalid")
    revisions = result.get("required_revisions", [])
    if not isinstance(revisions, list):
        raise ValidationError("contradiction_editor required_revisions must be a list")
    return result


def _source_ready(ctx, config):
    text = (ctx.source_text or "").strip()
    return len(text) >= config.source_min_chars


def route_after_failure(fails: list[str]) -> State:
    if any("[SOURCE]" in f for f in fails): return State.SOURCE_TEXT
    if any("[RENDERING]" in f for f in fails): return State.RENDERING
    if any("[CHRISTOLOGY]" in f or "[CANON]" in f for f in fails): return State.CANONICAL_CORRESPONDENCE
    if any("[ARC]" in f or "V4" in f for f in fails): return State.DIRECTOR_BRIEF
    if any("[VOICE]" in f or "[INTRO]" in f for f in fails): return State.COMPOSE_PROSE
    if any("[BOTH]" in f for f in fails): return State.COMPOSE_PROSE
    if fails and all("[POEM]" in f for f in fails): return State.COMPOSE_POEM
    if any("[PROSE]" in f for f in fails): return State.COMPOSE_PROSE
    return State.ESCALATED


def apply_editorial_smoothing(ctx, adapter, config=None):
    config = config or EngineConfig(); before = {"prose": deepcopy(ctx.prose), "artifact": ctx.artifact}
    edited = adapter.call("editorial_smoother", {"prose": deepcopy(ctx.prose), "immutable": {"poem": ctx.poem, "focus_bible_verses": ctx.prose.get("focus_bible_verses"), "threshold_phrase": ctx.brief.get("selected_threshold_phrase")}})
    candidate = edited.get("prose", edited)
    allowed = PROSE_FIELDS - {"focus_bible_verses", "christ_fulfillment"}
    for key in allowed:
        if key in candidate: ctx.prose[key] = candidate[key]
    ctx.prose["focus_bible_verses"] = before["prose"].get("focus_bible_verses", "")
    ctx.prose["christ_fulfillment"] = before["prose"].get("christ_fulfillment", "")
    fails, warnings = run_deterministic_harness(ctx, config); ctx.warnings.extend(warnings)
    if fails:
        ctx.prose, ctx.artifact = before["prose"], before["artifact"]
        ctx.warnings.append("EDITORIAL_ROLLBACK: deterministic failure")
        return False
    ctx.artifact = render_artifact(ctx); ctx.scores["editorial_smoothing_applied"] = True
    return True


def _call(adapter, role, ctx):
    return adapter.call(role, {"chapter_ref": ctx.chapter_ref, "source_text": ctx.source_text, "context": ctx})


def apply_american_literary_style(ctx, config):
    if ctx.literary_style:
        return
    signals = [
        ctx.chapter_ref,
        ctx.source_text,
        ctx.working_rendering,
        " ".join(str(item) for item in ctx.chapter_design_map.get("physical_vocabulary", [])),
        ctx.chapter_design_map.get("emotional_movement", ""),
        ctx.chapter_design_map.get("central_theological_claim", ""),
        ctx.chapter_design_map.get("christward_fulfillment", ""),
    ]
    matches = match_american_patterns(signals, limit=config.american_style_match_limit) if config.enable_american_literary_patterns else []
    ctx.literary_style = build_style_brief(matches)
    if config.enable_classical_hymnody:
        ctx.literary_style["classical_hymnody"] = build_hymnody_brief(ctx.chapter_design_map)
    else:
        ctx.literary_style.pop("classical_hymnody", None)
    if config.enable_poetic_music:
        ctx.literary_style["poetic_music"] = build_poetic_music_brief(ctx.chapter_design_map)
    else:
        ctx.literary_style.pop("poetic_music", None)


def run_engine(ctx, adapter, config=None):
    config = config or EngineConfig(); state = State.INIT
    try:
        while state not in (State.DONE, State.ESCALATED):
            if len(ctx.trace) >= config.max_state_transitions:
                ctx.failed_checks = ["[BOTH] max state transitions exceeded"]
                state = State.ESCALATED
                break
            ctx.trace.append(state)
            if state == State.INIT: state = State.SOURCE_TEXT
            elif state == State.SOURCE_TEXT:
                out = _call(adapter, "source_agent", ctx); ctx.source_layer = out; ctx.source_text = out.get("source_text", ctx.source_text)
                if not _source_ready(ctx, config):
                    ctx.failed_checks = ["[SOURCE] source text missing or too short"]
                    state = State.ESCALATED
                else:
                    state = State.RENDERING
            elif state == State.RENDERING:
                ctx.rendering_layer = _call(adapter, "translator", ctx); ctx.working_rendering = ctx.rendering_layer.get("working_rendering", ctx.source_text)
                if not ctx.working_rendering.strip():
                    ctx.failed_checks = ["[RENDERING] working rendering missing"]
                    state = State.ESCALATED
                else:
                    state = State.CHAPTER_DESIGN_MAP
            elif state == State.CHAPTER_DESIGN_MAP: ctx.chapter_design_map = _required(_call(adapter, "chapter_design_mapper", ctx), CHAPTER_DESIGN_FIELDS, "chapter_design_mapper"); state = State.CANONICAL_CORRESPONDENCE
            elif state == State.CANONICAL_CORRESPONDENCE: ctx.correspondence = _call(adapter, "canonist", ctx); state = State.THEOLOGICAL_RISK_REGISTER
            elif state == State.THEOLOGICAL_RISK_REGISTER: ctx.theological_risk_register = validate_risks(_call(adapter, "theological_risk_agent", ctx)); state = State.HISTORICAL_LINGUISTIC_CONTEXT
            elif state == State.HISTORICAL_LINGUISTIC_CONTEXT: ctx.historical_linguistic = _call(adapter, "historian_linguist", ctx); state = State.COMMENTARY_GROUNDING
            elif state == State.COMMENTARY_GROUNDING:
                ctx.commentary_grounding = _call(adapter, "commentary_agent", ctx)
                apply_american_literary_style(ctx, config)
                state = State.ART_DIRECTION
            elif state == State.ART_DIRECTION: ctx.art_direction = _required(_call(adapter, "art_director", ctx), ART_DIRECTION_FIELDS, "art_director"); state = State.CREATIVE_DIVERGENCE
            elif state == State.CREATIVE_DIVERGENCE: ctx.creative_divergence = validate_divergence(_call(adapter, "creative_divergence_agent", ctx)); state = State.DIRECTOR_BRIEF
            elif state == State.DIRECTOR_BRIEF: ctx.brief = _required(_call(adapter, "director", ctx), DIRECTOR_BRIEF_FIELDS, "director"); state = State.CHAPTER_ARC_GATE
            elif state == State.CHAPTER_ARC_GATE:
                failures = chapter_arc_gate(ctx, config)
                if failures:
                    ctx.gate_revisions += 1
                    if ctx.gate_revisions > config.max_gate_revisions: ctx.failed_checks = failures; state = State.ESCALATED
                    else: state = route_after_failure(failures)
                else: state = State.BRIEF_GATE
            elif state == State.BRIEF_GATE: state = State.COMPOSE_PROSE
            elif state == State.COMPOSE_PROSE: ctx.prose = _required(_call(adapter, "composer", ctx), PROSE_FIELDS, "composer"); state = State.VOICE_REVIEW
            elif state == State.VOICE_REVIEW:
                review = _call(adapter, "voice_keeper", ctx)
                if review.get("approved", True): state = State.COMPOSE_POEM
                else:
                    ctx.voice_revisions += 1
                    if ctx.voice_revisions > config.max_voice_revisions:
                        ctx.failed_checks = ["[VOICE] max voice revisions exceeded"]
                        state = State.ESCALATED
                    else:
                        state = State.COMPOSE_PROSE
            elif state == State.COMPOSE_POEM: ctx.poem = _call(adapter, "poet", ctx).get("poem", ""); state = State.DETERMINISTIC_CHECK
            elif state == State.DETERMINISTIC_CHECK:
                failures, warnings = run_deterministic_harness(ctx, config); ctx.failed_checks = failures; ctx.warnings.extend(warnings)
                if failures:
                    ctx.checker_loops += 1
                    state = State.ESCALATED if ctx.checker_loops > config.max_checker_loops else route_after_failure(failures)
                else: state = State.BEAUTY_PASS
            elif state == State.BEAUTY_PASS:
                beauty = run_beauty_pass(ctx, _call(adapter, "beauty_pass_agent", ctx), ctx.warnings, config); ctx.scores.update(beauty)
                if beauty["beauty_score"] < 8:
                    ctx.beauty_loops += 1
                    if ctx.beauty_loops > config.max_beauty_loops:
                        ctx.failed_checks = ["[BOTH] max beauty revisions exceeded"]
                        state = State.ESCALATED
                    else:
                        state = State.COMPOSE_POEM if beauty.get("fault_target") == "poem" else State.COMPOSE_PROSE
                else: state = State.EVALUATE
            elif state == State.EVALUATE:
                evaluation = _call(adapter, "evaluator", ctx); ctx.scores["evaluation"] = evaluation; failures = validate_evaluation(evaluation)
                if failures:
                    ctx.eval_passes += 1; state = State.ESCALATED if ctx.eval_passes > config.max_eval_passes else route_after_failure(failures)
                else: state = State.CONTRADICTION_EDITOR
            elif state == State.CONTRADICTION_EDITOR:
                result = validate_contradiction_result(_call(adapter, "contradiction_editor", ctx)); ctx.scores["contradiction_editor"] = result
                if result.get("verdict") == "Fail":
                    ctx.contradiction_loops += 1
                    if ctx.contradiction_loops > config.max_contradiction_loops:
                        ctx.failed_checks = ["[BOTH] max contradiction revisions exceeded"]
                        state = State.ESCALATED
                    else:
                        state = route_after_failure(result.get("required_revisions", ["[BOTH] contradiction failure"]))
                elif result.get("verdict") == "Pass with revisions":
                    ctx.contradiction_loops += 1
                    if ctx.contradiction_loops > config.max_contradiction_loops:
                        ctx.failed_checks = ["[BOTH] max contradiction revisions exceeded"]
                        state = State.ESCALATED
                    else:
                        state = route_after_failure(result.get("required_revisions", ["[PROSE] revisions required"]))
                else: state = State.EDITORIAL_SMOOTHING
            elif state == State.EDITORIAL_SMOOTHING:
                ctx.editorial_loops += 1
                if ctx.editorial_loops > config.max_editorial_loops: state = State.ESCALATED
                else: apply_editorial_smoothing(ctx, adapter, config); state = State.POST_EDIT_VALIDATION
            elif state == State.POST_EDIT_VALIDATION:
                failures, warnings = run_deterministic_harness(ctx, config); ctx.warnings.extend(warnings)
                if failures: ctx.failed_checks = failures; state = State.ESCALATED
                else: state = State.LEDGER_UPDATE
            elif state == State.LEDGER_UPDATE: update_ledger(ctx); state = State.EMIT_ARTIFACT
            elif state == State.EMIT_ARTIFACT:
                ctx.artifact = render_artifact(ctx)
                if not validate_artifact_structure(ctx.artifact): raise ValidationError("artifact structure invalid")
                state = State.DONE
        ctx.trace.append(state)
    except Exception as exc:
        ctx.error = f"{type(exc).__name__}: {exc}"; state = State.ESCALATED
        if not ctx.trace or ctx.trace[-1] != State.ESCALATED: ctx.trace.append(State.ESCALATED)
    return ctx
