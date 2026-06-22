import json
from pathlib import Path

import pytest

from devotional_engine import (
    EngineContext,
    ExternalModelAdapterConfig,
    HumanApproval,
    MockAgentAdapter,
    State,
    UnconfiguredExternalModelAdapter,
    build_audit_record,
    require_human_approval,
    run_engine,
    validate_external_adapter_config,
    write_audit_record,
)
from devotional_engine.config import ROLE_CONFIG
from devotional_engine.exceptions import AgentOutputError, ValidationError


def _done_context():
    path = Path(__file__).parents[1] / "examples" / "psalm19_mock_outputs.json"
    return run_engine(EngineContext(chapter_ref="Psalm 19"), MockAgentAdapter(json.loads(path.read_text())))


def test_human_approval_requires_completed_run():
    approval = HumanApproval("reviewer", True, True, True, True)
    with pytest.raises(ValidationError):
        require_human_approval(EngineContext(chapter_ref="Psalm 1"), approval)


def test_human_approval_records_required_signoffs():
    ctx = _done_context()
    approval = HumanApproval("reviewer", True, True, True, True, notes="Approved for test.")
    record = require_human_approval(ctx, approval)
    assert record["reviewer"] == "reviewer"
    assert ctx.ledger["approvals"][-1]["scripture_rights_confirmed"]


def test_human_approval_rejects_missing_signoff():
    ctx = _done_context()
    approval = HumanApproval("reviewer", True, False, True, True)
    with pytest.raises(ValidationError):
        require_human_approval(ctx, approval)


def test_audit_record_omits_artifact_body_and_writes_jsonl(tmp_path):
    ctx = _done_context()
    record = build_audit_record(ctx, model_versions={"mock": "fixture"}, source_metadata={"translation": "mock"})
    path = write_audit_record(record, tmp_path / "audit.jsonl")
    data = json.loads(path.read_text().strip())
    assert data["status"] == State.DONE.name
    assert data["chapter_ref"] == "Psalm 19"
    assert "artifact" not in data


def test_external_adapter_config_requires_all_roles():
    config = ExternalModelAdapterConfig(provider="test", model_by_role={"source_agent": "model"})
    failures = validate_external_adapter_config(config)
    assert failures
    assert "translator" in failures[0]


def test_external_adapter_config_accepts_full_role_map():
    config = ExternalModelAdapterConfig(
        provider="test",
        model_by_role={role: "model" for role in ROLE_CONFIG},
    )
    assert validate_external_adapter_config(config) == []


def test_unconfigured_external_adapter_fails_closed():
    config = ExternalModelAdapterConfig(
        provider="test",
        model_by_role={role: "model" for role in ROLE_CONFIG},
    )
    adapter = UnconfiguredExternalModelAdapter(config)
    with pytest.raises(AgentOutputError):
        adapter.call("source_agent", {})
