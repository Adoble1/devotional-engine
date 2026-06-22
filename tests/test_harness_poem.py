from devotional_engine.config import EngineConfig
from devotional_engine.harness import CHECK_REGISTRY, check_rhyme, check_stanza_count, check_syllable_pattern
from devotional_engine.text_utils import split_stanzas

STRICT_CONFIG = EngineConfig(poem_form="common_meter")

def test_four_and_five_stanzas(context, valid_poem):
    assert not check_stanza_count(context, STRICT_CONFIG)[0]
    context.poem = valid_poem + "\n\n" + split_stanzas(valid_poem)[0][0] + "\n" + "\n".join(split_stanzas(valid_poem)[0][1:])
    assert not check_stanza_count(context, STRICT_CONFIG)[0]

def test_six_stanzas_fail(context, valid_poem):
    context.poem = "\n\n".join(["\n".join(split_stanzas(valid_poem)[0])] * 6)
    assert check_stanza_count(context, STRICT_CONFIG)[0]

def test_wrong_line_count_fails(context):
    context.poem += "\nextra"
    assert check_stanza_count(context, STRICT_CONFIG)[0]

def test_wrong_meter_fails(context):
    context.poem = context.poem.replace("The Lord has heard my cry today", "Short line", 1)
    assert check_syllable_pattern(context, STRICT_CONFIG)[0]

def test_obvious_rhyme_failure(context):
    context.poem = context.poem.replace("And set his love on me", "And set his love on stone", 1)
    assert check_rhyme(context, STRICT_CONFIG)[0]

def test_open_poem_allows_coda_and_irregular_stanzas(context):
    context.poem = """The day of trouble shakes the ground,
And cuts the breathless air;
We look toward the holy hill,
To find our rescue there.

The iron breaks beneath the weight, but we will stand in Him."""
    assert not check_syllable_pattern(context, EngineConfig())[0]
    assert not check_rhyme(context, EngineConfig())[0]
    assert not check_stanza_count(context, EngineConfig())[0]

def test_registry_has_required_checks():
    assert {"D0", "D1", "D2", "D3", "D8", "D13", "D14", "D17", "D18", "D27", "V4", "T1", "S1"} <= CHECK_REGISTRY.keys()
