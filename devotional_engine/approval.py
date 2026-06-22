from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from .exceptions import ValidationError
from .states import State


@dataclass
class HumanApproval:
    reviewer: str
    theological_approved: bool
    editorial_approved: bool
    scripture_rights_confirmed: bool
    safety_reviewed: bool
    notes: str = ""
    approved_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def require_human_approval(ctx, approval: HumanApproval) -> dict:
    if not ctx.trace or ctx.trace[-1] is not State.DONE:
        raise ValidationError("human approval requires a completed engine run")
    if ctx.failed_checks:
        raise ValidationError("human approval requires zero failed checks")
    if not ctx.artifact.strip():
        raise ValidationError("human approval requires a rendered artifact")
    if not approval.reviewer.strip():
        raise ValidationError("human approval requires a reviewer name")
    missing = [
        name for name, ok in {
            "theological_approved": approval.theological_approved,
            "editorial_approved": approval.editorial_approved,
            "scripture_rights_confirmed": approval.scripture_rights_confirmed,
            "safety_reviewed": approval.safety_reviewed,
        }.items() if not ok
    ]
    if missing:
        raise ValidationError(f"human approval incomplete: {', '.join(missing)}")
    record = asdict(approval)
    ctx.scores["human_approval"] = record
    ctx.ledger.setdefault("approvals", []).append(record)
    return record
