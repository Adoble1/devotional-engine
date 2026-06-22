from devotional_engine import (
    StageName,
    planning_stage,
    run_stage_cycle,
    tool_use_stage,
    verification_stage,
)


def test_planning_stage_names_boundaries():
    report = planning_stage(
        "Improve a devotional paragraph",
        objectives=("truthful", "beautiful"),
        constraints=("chapter-grounded",),
    )
    assert report.stage is StageName.PLANNING
    assert not report.failures
    assert report.artifacts[0].content["stages"] == ("planning", "tool_use", "verification", "reflection")


def test_empty_plan_stops_tool_use():
    plan = planning_stage("")
    tool_report = tool_use_stage(plan, outputs=("unused",))
    assert plan.failures
    assert tool_report.failures == ("tool-use skipped because planning failed",)


def test_verification_discards_failed_parts_and_recombines_verified_parts():
    def has_chapter_evidence(artifact):
        return bool(artifact.evidence), "missing chapter evidence"

    _, _, verification, reflection = run_stage_cycle(
        "Revise Psalm 23 poem",
        outputs=(
            {
                "id": "kept_line",
                "content": "The cup cannot hold its brim.",
                "evidence": ("cup",),
                "tags": ("image",),
            },
            {
                "id": "discarded_line",
                "content": "A beautiful emotional tenderness happens.",
                "evidence": (),
                "tags": ("padding",),
            },
        ),
        checks={"has_chapter_evidence": has_chapter_evidence},
    )
    assert [artifact.artifact_id for artifact in verification.accepted] == ["kept_line"]
    assert [item.artifact.artifact_id for item in verification.rejected] == ["discarded_line"]
    assert reflection.improved_version["content"] == ("The cup cannot hold its brim.",)
    assert "A beautiful emotional tenderness happens." not in reflection.improved_version["content"]


def test_verification_can_reject_superfluous_qualia_words():
    embodied_words = {"cup", "bread", "oil", "shadow", "road", "water", "table"}
    padding_words = {"beautiful", "emotional", "tenderness", "aching"}

    def qualia_is_grounded(artifact):
        words = {word.strip(".,;:!?").lower() for word in str(artifact.content).split()}
        grounded = words & embodied_words
        padding = words & padding_words
        if padding and not grounded:
            return False, "emotional language lacks embodied chapter detail"
        return True, ""

    plan = planning_stage("Separate genuine felt detail from ornament")
    tool_report = tool_use_stage(
        plan,
        outputs=(
            {"id": "felt", "content": "Oil darkens the lifted head.", "evidence": ("oil",)},
            {"id": "ornament", "content": "Beautiful aching tenderness remains.", "evidence": ("feeling",)},
        ),
    )
    verification = verification_stage((plan, tool_report), {"qualia_is_grounded": qualia_is_grounded})
    assert [artifact.artifact_id for artifact in verification.accepted] == ["felt"]
    assert "emotional language lacks embodied" in verification.rejected[0].reason
