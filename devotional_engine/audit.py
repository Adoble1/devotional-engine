from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
from uuid import uuid4


@dataclass
class AuditRecord:
    run_id: str
    chapter_ref: str
    status: str
    trace: list[str]
    failed_checks: list[str]
    warnings: list[str]
    title: str = ""
    model_versions: dict = field(default_factory=dict)
    source_metadata: dict = field(default_factory=dict)
    approval: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def build_audit_record(ctx, model_versions=None, source_metadata=None, run_id=None) -> AuditRecord:
    return AuditRecord(
        run_id=run_id or str(uuid4()),
        chapter_ref=ctx.chapter_ref,
        status=ctx.trace[-1].name if ctx.trace else "UNKNOWN",
        trace=[state.name for state in ctx.trace],
        failed_checks=list(ctx.failed_checks),
        warnings=list(ctx.warnings),
        title=ctx.prose.get("title", ""),
        model_versions=model_versions or {},
        source_metadata=source_metadata or {},
        approval=ctx.scores.get("human_approval", {}),
    )


def write_audit_record(record: AuditRecord, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")
    return path
