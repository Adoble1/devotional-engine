from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping

from .exceptions import ValidationError

PUBLIC_DOMAIN_US_PUBLISHED_THROUGH = 1930
DEFAULT_PERIOD_END_YEAR = 1949
ONTOLOGY_REVIEW_DIMENSIONS = (
    "ontological_integrity",
    "affective_truth",
    "historical_diction",
    "source_discipline",
)
RESERVED_WARRANT_IDS = {"canonical_relationship", "historical_meaning", "lexical_insight"}
KJV_SURFACE_FORMS = (
    "thee", "thou", "thy", "thine", "ye", "hath", "doth", "dost",
    "shalt", "wilt", "unto", "whence", "wherein", "thereof", "verily", "saith",
)
POSTWAR_AFFECT_JARGON = (
    "emotional bandwidth", "inner child", "lived experience", "nervous system regulation",
    "process your feelings", "safe space", "self-care", "toxic positivity",
    "trauma response", "triggered", "validation journey",
)

SOURCE_DOCUMENTS: dict[str, dict[str, Any]] = {
    "bunyan_pilgrims_progress_1678": {
        "author": "John Bunyan",
        "title": "The Pilgrim's Progress",
        "publication_year": 1678,
        "source_url": "https://www.gutenberg.org/ebooks/131",
        "public_domain_basis": "Published before 1931; Project Gutenberg marks eBook 131 public domain in the USA.",
        "vocabulary": ("burden", "road", "gate", "danger", "companion", "refuge", "weariness", "deliverance", "courage", "home", "despair", "hope", "fear", "rest"),
        "guidance": ("plain movement", "concrete obstacle", "earned relief"),
        "avoid": ("archaic dialogue", "allegorical cast expansion", "KJV surface diction"),
    },
    "macdonald_unspoken_sermons_1867": {
        "author": "George MacDonald",
        "title": "Unspoken Sermons, Series I, II, and III",
        "publication_year": 1867,
        "source_url": "https://www.gutenberg.org/ebooks/9057",
        "public_domain_basis": "Published 1867-1889; Project Gutenberg marks eBook 9057 public domain in the USA.",
        "vocabulary": ("obedience", "mercy", "truth", "freedom", "conscience", "inheritance", "courage", "tenderness", "repentance", "trust", "longing", "sorrow", "gladness"),
        "guidance": ("plain spiritual reasoning", "warm directness", "quiet moral turn"),
        "avoid": ("speculation beyond the passage", "Victorian ornament", "author imitation"),
    },
    "stevenson_vailima_prayers_1916": {
        "author": "Robert Louis Stevenson",
        "title": "Prayers Written at Vailima",
        "publication_year": 1916,
        "source_url": "https://www.gutenberg.org/ebooks/616",
        "public_domain_basis": "1916 edition; Project Gutenberg marks eBook 616 public domain in the USA.",
        "vocabulary": ("kindness", "labor", "courage", "duty", "peace", "gratitude", "sorrow", "fellowship", "rest", "mercy", "hope", "patience", "cheer", "care"),
        "guidance": ("compact petition", "household plainness", "unforced warmth"),
        "avoid": ("Scots dialect", "borrowed prayer phrases", "sentimental uplift"),
    },
    "hopkins_poems_1918": {
        "author": "Gerard Manley Hopkins",
        "title": "Poems of Gerard Manley Hopkins",
        "publication_year": 1918,
        "source_url": "https://www.gutenberg.org/ebooks/22403",
        "public_domain_basis": "1918 edition; Project Gutenberg marks eBook 22403 public domain in the USA.",
        "vocabulary": ("bright", "bitter", "bruised", "bent", "flame", "fall", "falter", "grief", "glory", "wind", "stone", "wing", "darkness", "morning", "mercy"),
        "guidance": ("physical verbs", "sound pressure", "compressed image"),
        "avoid": ("sprung-rhythm pastiche", "coined compounds", "recognizable phrasing"),
    },
}
DEFAULT_SOURCE_IDS = (
    "macdonald_unspoken_sermons_1867",
    "stevenson_vailima_prayers_1916",
    "hopkins_poems_1918",
)


@dataclass(frozen=True)
class OntologyFinding:
    code: str
    field: str
    message: str
    severity: str = "error"
    repair_target: str = "ontology"


def _text(value: Any) -> str:
    return str(value or "").strip()


def _list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    return list(value) if isinstance(value, (list, tuple, set)) else [value]


def _dedupe(values: list[Any] | tuple[Any, ...]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = _text(value)
        if text and text.lower() not in seen:
            seen.add(text.lower())
            result.append(text)
    return result


def _is_mock(adapter: Any) -> bool:
    current = adapter
    for _ in range(8):
        if current is None:
            return False
        if current.__class__.__name__ == "MockAgentAdapter":
            return True
        current = getattr(current, "delegate", None)
    return False


def public_domain_source_catalog(period_end_year: int = DEFAULT_PERIOD_END_YEAR) -> list[dict[str, Any]]:
    cutoff = min(int(period_end_year), PUBLIC_DOMAIN_US_PUBLISHED_THROUGH)
    return [
        {"source_id": source_id, **record}
        for source_id, record in SOURCE_DOCUMENTS.items()
        if int(record["publication_year"]) <= cutoff
    ]


def _nodes(values: Any, grounding: Mapping[str, Any]) -> list[dict[str, Any]]:
    result = [
        {
            "id": _text(item.get("id")),
            "kind": _text(item.get("kind")).lower(),
            "name": _text(item.get("name")),
            "truth": _text(item.get("truth") or item.get("state")),
            "warrant_ids": _dedupe(_list(item.get("warrant_ids"))),
        }
        for item in _list(values)
        if isinstance(item, Mapping)
    ]
    if result:
        return result
    evidence = [
        _text(item.get("id"))
        for item in _list(grounding.get("textual_evidence"))
        if isinstance(item, Mapping) and _text(item.get("id"))
    ][:1] or ["historical_meaning"]
    return [
        {"id": "god", "kind": "divine", "name": "God", "truth": _text(grounding.get("divine_action")), "warrant_ids": evidence},
        {"id": "human", "kind": "human", "name": "the human creature", "truth": _text(grounding.get("reader_felt_experience")), "warrant_ids": evidence},
    ]


def _relations(values: Any, nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = [
        {
            "source": _text(item.get("source")),
            "relation": _text(item.get("relation") or item.get("verb")),
            "target": _text(item.get("target")),
            "warrant_ids": _dedupe(_list(item.get("warrant_ids"))),
        }
        for item in _list(values)
        if isinstance(item, Mapping)
    ]
    if result:
        return result
    warrants = list(nodes[0].get("warrant_ids", [])) if nodes else []
    return [{"source": "god", "relation": "governs and answers", "target": "human", "warrant_ids": warrants}]


def build_ontological_overlay(
    plan: Mapping[str, Any],
    grounding: Mapping[str, Any],
    *,
    period_end_year: int = DEFAULT_PERIOD_END_YEAR,
) -> dict[str, Any]:
    supplied = plan.get("ontological_overlay")
    supplied = dict(supplied) if isinstance(supplied, Mapping) else {}
    order = dict(supplied.get("order", {})) if isinstance(supplied.get("order"), Mapping) else {}
    affect = dict(supplied.get("affective_path", {})) if isinstance(supplied.get("affective_path"), Mapping) else {}
    diction = dict(supplied.get("diction", {})) if isinstance(supplied.get("diction"), Mapping) else {}
    transform = dict(plan.get("reader_transformation", {})) if isinstance(plan.get("reader_transformation"), Mapping) else {}

    nodes = _nodes(supplied.get("nodes"), grounding)
    relations = _relations(supplied.get("relations"), nodes)
    raw_source_ids = _dedupe(_list(diction.get("source_document_ids") or supplied.get("source_document_ids")))
    source_ids = raw_source_ids or list(DEFAULT_SOURCE_IDS)
    sources = [SOURCE_DOCUMENTS[source_id] for source_id in source_ids if source_id in SOURCE_DOCUMENTS]
    available = _dedupe([word for source in sources for word in source["vocabulary"]])
    selected = _dedupe(_list(diction.get("selected_vocabulary")))
    vocabulary_selection_origin = "supplied" if selected else "default"
    if not selected:
        signals = " ".join((
            _text(grounding.get("governing_claim")),
            _text(grounding.get("reader_felt_experience")),
            _text(grounding.get("historical_meaning")),
            " ".join(_text(item) for item in _list(grounding.get("physical_vocabulary"))),
        )).lower()
        matched = [word for word in available if re.search(rf"\b{re.escape(word)}\b", signals)]
        selected = (matched + available)[:12]

    return {
        "origin": "supplied" if supplied else "fallback",
        "nodes": nodes,
        "relations": relations,
        "order": {
            "true_order": _text(order.get("true_order") or grounding.get("governing_claim")),
            "disorder": _text(order.get("disorder") or grounding.get("reader_felt_experience")),
            "divine_action": _text(order.get("divine_action") or grounding.get("divine_action")),
            "restored_posture": _text(order.get("restored_posture") or transform.get("faithful_response")),
        },
        "affective_path": {
            "pressure": _text(affect.get("pressure") or grounding.get("reader_felt_experience")),
            "embodied_evidence": _dedupe(_list(affect.get("embodied_evidence") or grounding.get("physical_vocabulary"))),
            "turn": _text(affect.get("turn") or grounding.get("textual_hinge")),
            "settled_posture": _text(affect.get("settled_posture") or transform.get("new_perception")),
        },
        "diction": {
            "period_end_year": int(diction.get("period_end_year") or period_end_year),
            "public_domain_jurisdiction": "United States",
            "source_document_ids": source_ids,
            "source_selection_origin": "supplied" if raw_source_ids else "default",
            "vocabulary_selection_origin": vocabulary_selection_origin,
            "source_documents": [
                {"source_id": source_id, **{key: value for key, value in SOURCE_DOCUMENTS[source_id].items() if key != "vocabulary"}}
                for source_id in source_ids if source_id in SOURCE_DOCUMENTS
            ],
            "selected_vocabulary": selected,
            "available_vocabulary": available,
            "rules": [
                "Scripture governs truth; source documents govern vocabulary atoms, emotional restraint, and cadence only.",
                "Never quote, imitate, or reproduce a recognizable source phrase.",
                "Let emotion arise from passage-warranted bodily, relational, or material evidence.",
                "Use contemporary grammar and pronouns; KJV surface forms are prohibited.",
                "Prefer one concrete period-attested word to an explanatory sentence at the emotional peak.",
            ],
        },
    }


def validate_ontological_overlay(
    overlay: Mapping[str, Any],
    *,
    evidence_ids: set[str] | list[str] | tuple[str, ...],
    required: bool,
) -> list[OntologyFinding]:
    findings: list[OntologyFinding] = []
    evidence = {_text(item) for item in evidence_ids if _text(item)} | RESERVED_WARRANT_IDS
    if required and _text(overlay.get("origin")) != "supplied":
        findings.append(OntologyFinding("O01", "ontological_overlay", "Production planning must supply an explicit ontological overlay."))

    nodes = [item for item in _list(overlay.get("nodes")) if isinstance(item, Mapping)]
    node_ids: set[str] = set()
    kinds: set[str] = set()
    for index, node in enumerate(nodes):
        node_id = _text(node.get("id")); kind = _text(node.get("kind")).lower(); kinds.add(kind)
        if not all((node_id, kind, _text(node.get("name")), _text(node.get("truth")))):
            findings.append(OntologyFinding("O02", f"nodes.{index}", "Each node requires id, kind, name, and truth."))
        if node_id in node_ids:
            findings.append(OntologyFinding("O02", f"nodes.{index}.id", "Node ids must be unique."))
        node_ids.add(node_id)
        warrants = {_text(item) for item in _list(node.get("warrant_ids")) if _text(item)}
        if required and not warrants:
            findings.append(OntologyFinding("O03", f"nodes.{index}.warrant_ids", "Every production node needs a warrant."))
        if warrants - evidence:
            findings.append(OntologyFinding("O03", f"nodes.{index}.warrant_ids", "Node warrant is not present in the grounding packet."))
    if required and (len(nodes) < 2 or not {"divine", "human"}.issubset(kinds)):
        findings.append(OntologyFinding("O02", "nodes", "The overlay must distinguish divine and human reality."))

    relations = [item for item in _list(overlay.get("relations")) if isinstance(item, Mapping)]
    if required and not relations:
        findings.append(OntologyFinding("O04", "relations", "At least one warranted relation is required."))
    for index, relation in enumerate(relations):
        source = _text(relation.get("source")); target = _text(relation.get("target"))
        if not all((source, target, _text(relation.get("relation")))) or source not in node_ids or target not in node_ids:
            findings.append(OntologyFinding("O04", f"relations.{index}", "Relation endpoints and action must reference declared nodes."))
        warrants = {_text(item) for item in _list(relation.get("warrant_ids")) if _text(item)}
        if required and not warrants:
            findings.append(OntologyFinding("O04", f"relations.{index}.warrant_ids", "Every production relation needs a warrant."))
        if warrants - evidence:
            findings.append(OntologyFinding("O04", f"relations.{index}.warrant_ids", "Relation warrant is not present in the grounding packet."))

    for group, fields, code in (
        (dict(overlay.get("order", {})), ("true_order", "disorder", "divine_action", "restored_posture"), "O05"),
        (dict(overlay.get("affective_path", {})), ("pressure", "turn", "settled_posture"), "O06"),
    ):
        for field in fields:
            if required and not _text(group.get(field)):
                findings.append(OntologyFinding(code, field, "The ontological or affective arc is incomplete."))
    if required and not _list(dict(overlay.get("affective_path", {})).get("embodied_evidence")):
        findings.append(OntologyFinding("O06", "affective_path.embodied_evidence", "Emotion requires embodied or relational evidence."))

    diction = dict(overlay.get("diction", {}))
    try:
        period_end = int(diction.get("period_end_year", 0))
    except (TypeError, ValueError):
        period_end = 0
    if required and not 0 < period_end <= DEFAULT_PERIOD_END_YEAR:
        findings.append(OntologyFinding("O07", "diction.period_end_year", "Vocabulary sources must end before 1950."))
    source_ids = _dedupe(_list(diction.get("source_document_ids")))
    if required and _text(diction.get("source_selection_origin")) != "supplied":
        findings.append(OntologyFinding("O08", "diction.source_document_ids", "Production planning must select its source documents explicitly."))
    if required and not 2 <= len(source_ids) <= 4:
        findings.append(OntologyFinding("O08", "diction.source_document_ids", "Select two to four public-domain source documents."))
    for source_id in source_ids:
        source = SOURCE_DOCUMENTS.get(source_id)
        if source is None or int(source["publication_year"]) > min(period_end or DEFAULT_PERIOD_END_YEAR, PUBLIC_DOMAIN_US_PUBLISHED_THROUGH):
            findings.append(OntologyFinding("O08", "diction.source_document_ids", f"Source is unknown or outside the verified cutoff: {source_id}."))
    available = {_text(item).lower() for item in _list(diction.get("available_vocabulary")) if _text(item)}
    selected = {_text(item).lower() for item in _list(diction.get("selected_vocabulary")) if _text(item)}
    if selected - available:
        findings.append(OntologyFinding("O09", "diction.selected_vocabulary", "Selected vocabulary lacks source-document attestation."))
    if required and _text(diction.get("vocabulary_selection_origin")) != "supplied":
        findings.append(OntologyFinding("O09", "diction.selected_vocabulary", "Production planning must select a compact period-attested vocabulary palette."))
    if required and not selected:
        findings.append(OntologyFinding("O09", "diction.selected_vocabulary", "Select a compact period-attested vocabulary palette."))
    return findings


def composition_overlay_brief(overlay: Mapping[str, Any]) -> dict[str, Any]:
    diction = dict(overlay.get("diction", {}))
    return {
        "nodes": [dict(item) for item in _list(overlay.get("nodes")) if isinstance(item, Mapping)],
        "relations": [dict(item) for item in _list(overlay.get("relations")) if isinstance(item, Mapping)],
        "order": dict(overlay.get("order", {})),
        "affective_path": dict(overlay.get("affective_path", {})),
        "diction": {
            "period_end_year": diction.get("period_end_year"),
            "source_documents": list(diction.get("source_documents", [])),
            "selected_vocabulary": list(diction.get("selected_vocabulary", [])),
            "rules": list(diction.get("rules", [])),
            "prohibited_kjv_forms": list(KJV_SURFACE_FORMS),
            "prohibited_postwar_jargon": list(POSTWAR_AFFECT_JARGON),
        },
    }


def audit_ontology_surface(draft: Mapping[str, Any], overlay: Mapping[str, Any], *, enforce: bool) -> list[OntologyFinding]:
    if not enforce:
        return []
    fields = ("title", "epigraph", "introduction", "reflection", "christ_fulfillment", "application", "prayer", "poem", "next_in_sequence")
    text = "\n".join(_text(draft.get(field)) for field in fields); lower = text.lower()
    findings: list[OntologyFinding] = []
    found_kjv = [form for form in KJV_SURFACE_FORMS if re.search(rf"\b{re.escape(form)}\b", lower)]
    found_thou_art = bool(re.search(r"\bthou\s+art\b", lower))
    if found_kjv or found_thou_art:
        labels = found_kjv + (["thou art"] if found_thou_art else [])
        findings.append(OntologyFinding("O10", "draft", f"KJV surface diction is prohibited: {', '.join(_dedupe(labels))}.", repair_target="draft"))
    found_jargon = [phrase for phrase in POSTWAR_AFFECT_JARGON if phrase in lower]
    if found_jargon:
        findings.append(OntologyFinding("O11", "draft", f"Postwar affect jargon is outside the selected register: {', '.join(found_jargon)}.", repair_target="draft"))
    diction = dict(overlay.get("diction", {})); selected = [_text(word).lower() for word in _list(diction.get("selected_vocabulary")) if _text(word)]
    if selected and not any(re.search(rf"\b{re.escape(word)}\b", lower) for word in selected):
        findings.append(OntologyFinding("O12", "draft", "No selected period-attested word carries an emotional pressure point.", severity="warning", repair_target="draft"))
    source_names = [
        _text(source.get(key))
        for source in _list(diction.get("source_documents")) if isinstance(source, Mapping)
        for key in ("author", "title")
    ]
    if any(name and name.lower() in lower for name in source_names):
        findings.append(OntologyFinding("O13", "draft", "Source documents should remain a hidden register, not named authorities.", severity="warning", repair_target="draft"))
    return findings


def _finding_dict(finding: OntologyFinding) -> dict[str, str]:
    return {"code": finding.code, "field": finding.field, "message": finding.message, "repair_target": finding.repair_target}


class OntologicalOverlayAdapter:
    """Inject ontology and verified historical diction into the four-role path."""

    def __init__(self, delegate: Any, config: Any):
        self.delegate = delegate
        self.config = config
        self.is_mock = _is_mock(delegate)
        self.overlay: dict[str, Any] = {}
        self.surface_findings: list[OntologyFinding] = []

    def call(self, role: str, payload: Mapping[str, Any]) -> Any:
        if not bool(getattr(self.config, "enforce_ontological_overlay", True)):
            return self.delegate.call(role, payload)

        if role == "devotional_planner":
            period_end = int(getattr(self.config, "ontology_period_end_year", DEFAULT_PERIOD_END_YEAR))
            enriched = dict(payload)
            enriched["ontological_source_catalog"] = public_domain_source_catalog(period_end)
            enriched["planning_instruction"] = (
                f"{_text(payload.get('planning_instruction'))} Build an ontological overlay with divine and human nodes, "
                "warranted relations, true order, disorder, divine action, restored posture, and an affective path grounded "
                "in bodily or relational evidence. Select two to four approved public-domain source documents and a compact "
                "vocabulary palette attested in them. Scripture governs truth. Sources govern diction and emotional restraint "
                "only. Do not quote or imitate them, and do not use KJV surface language."
            ).strip()
            result = self.delegate.call(role, enriched)
            if not isinstance(result, Mapping):
                return result
            plan = dict(result); grounding = payload.get("grounding") if isinstance(payload.get("grounding"), Mapping) else {}
            overlay = build_ontological_overlay(plan, grounding, period_end_year=period_end)
            evidence_ids = {_text(item.get("id")) for item in _list(grounding.get("textual_evidence")) if isinstance(item, Mapping) and _text(item.get("id"))}
            errors = [item for item in validate_ontological_overlay(overlay, evidence_ids=evidence_ids, required=not self.is_mock) if item.severity == "error"]
            if errors:
                raise ValidationError("; ".join(f"{item.field}: {item.message}" for item in errors))
            self.overlay = overlay; plan["ontological_overlay"] = overlay
            context = payload.get("context")
            if context is not None:
                context.ontological_overlay = overlay
            return plan

        if role == "devotional_composer":
            enriched = dict(payload); packet = dict(payload.get("composition_packet", {}))
            packet["ontological_overlay"] = composition_overlay_brief(self.overlay)
            economy = dict(packet.get("economy", {})); economy["principles"] = _dedupe(_list(economy.get("principles")) + [
                "let ontology determine emotional weight: who acts, who depends, what is broken, and what God restores",
                "use period-attested vocabulary at pressure points without sounding antique",
                "name emotion only after concrete evidence has earned it",
            ]); packet["economy"] = economy
            enriched["composition_packet"] = packet
            result = self.delegate.call(role, enriched)
            if isinstance(result, Mapping):
                self.surface_findings = audit_ontology_surface(result, self.overlay, enforce=not self.is_mock)
            return result

        if role == "devotional_reviewer":
            enriched = dict(payload); protected = dict(payload.get("protected", {})); protected["ontological_overlay"] = composition_overlay_brief(self.overlay); enriched["protected"] = protected
            enriched["ontology_findings"] = [{**_finding_dict(item), "severity": item.severity} for item in self.surface_findings]
            enriched["review_instruction"] = (
                f"{_text(payload.get('review_instruction'))} Confirm God's identity and action, creaturely dependence, moral "
                "disorder, covenant relation, and faithful response. Emotional force must arise from warranted bodily or "
                "relational facts. Use contemporary grammar with pressure vocabulary drawn only from approved pre-1950 "
                "public-domain sources. Reject KJV surface forms, postwar therapeutic jargon, quotation, and pastiche."
            ).strip()
            result = self.delegate.call(role, enriched)
            if not isinstance(result, Mapping):
                return result
            review = dict(result); hard = list(_list(review.get("hard_findings"))); advisory = list(_list(review.get("advisory_findings")))
            hard.extend(_finding_dict(item) for item in self.surface_findings if item.severity == "error")
            advisory.extend(_finding_dict(item) for item in self.surface_findings if item.severity != "error")
            if not self.is_mock:
                dimensions = review.get("dimensions") if isinstance(review.get("dimensions"), Mapping) else {}
                minimum = float(getattr(self.config, "ontology_review_min_score", 8.0))
                for name in ONTOLOGY_REVIEW_DIMENSIONS:
                    try:
                        score = float(dimensions[name])
                    except (KeyError, TypeError, ValueError):
                        score = -1
                    if score < minimum:
                        hard.append({"code": "O14", "field": f"dimensions.{name}", "message": f"Ontological review score {score:g} is below {minimum:g}.", "repair_target": "review"})
            review["hard_findings"] = hard; review["advisory_findings"] = advisory
            if hard and _text(review.get("verdict")).lower() == "pass":
                review["verdict"] = "Revise" if int(payload.get("revision", 0) or 0) < int(getattr(self.config, "integrated_max_revisions", 1)) else "Fail"
            return review

        return self.delegate.call(role, payload)
