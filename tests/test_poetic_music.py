from devotional_engine import POETIC_MUSIC_PROFILE, analyze_euphony, build_poetic_music_brief, has_midline_caesura
from devotional_engine import EngineConfig
from devotional_engine.harness import run_deterministic_harness


def test_melodic_line_has_fewer_harsh_clusters_than_stiff_line():
    stiff = analyze_euphony("The dark rock blocks the track.")
    melodic = analyze_euphony("The heavy shadow veils the road.")
    assert melodic["harsh_cluster_count"] < stiff["harsh_cluster_count"]
    assert melodic["soft_consonant_ratio"] > stiff["soft_consonant_ratio"]


def test_midline_caesura_requires_a_real_interior_pause():
    assert has_midline_caesura("The waters rise; the gates awaken")
    assert not has_midline_caesura("Waters roar and mountains fall")


def test_profile_allows_trochaic_shift_without_forcing_it():
    meter = POETIC_MUSIC_PROFILE["meter"]
    assert "trochaic inversion" in meter["variation"]
    assert "not on every line" in meter["limit"]
    assert "do not infer English stress mechanically" in meter["warning"]


def test_battle_chapter_preserves_mixed_sonic_texture():
    brief = build_poetic_music_brief(
        {
            "emotional_movement": "fear becomes praise",
            "divine_action": "The LORD is strong in battle.",
            "physical_vocabulary": ["gate", "battle", "stone"],
        }
    )
    assert brief["roughness_warranted"] is True
    assert brief["sonic_mode"] == "mixed texture"


def test_dense_harsh_clusters_warn_when_music_check_enabled(context):
    context.poem = "Dark rock blocks track; cracked rock locks back."
    _, warnings = run_deterministic_harness(context, EngineConfig(warn_poem_music=True))
    assert any("D28" in warning for warning in warnings)
