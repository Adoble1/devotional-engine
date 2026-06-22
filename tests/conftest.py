import pytest
from devotional_engine.models import EngineContext

STANZA = """The Lord has heard my cry today
He drew me from deep sea
He bowed the heavens down to save
And set his love on me"""

VALID_POEM = """The Lord has heard my cry today
He drew me from deep sea
He bowed the heavens down to save
And set his love on me

The cords of death wrapped my feet
He heard my cry at sea
He drew me out from waters deep
And set his love on me

The Lord became my living rock
My shield in fear and sea
He brought me into spacious grace
And set his love on me

Now praise will rise among the lands
His mercy runs to me
His king now sings the faithful name
And set his love on me"""

@pytest.fixture
def valid_poem(): return VALID_POEM

@pytest.fixture
def context(valid_poem):
    return EngineContext(chapter_ref="Psalm 18", prose={
        "title": "Love Before Thunder", "epigraph": "Love speaks before thunder.",
        "focus_bible_verses": "Psalm 18:1-3", "introduction": "Love speaks before thunder.",
        "reflection": "The Lord comes to rescue.", "christ_fulfillment": "Christ enters death and rises.",
        "application": "Call upon the Lord today.",
        "prayer": "Father, hear us. Draw near. Give faith. Keep us. Send us. Through Jesus Christ our Lord. Amen.",
        "next_in_sequence": "Psalm 19",
    }, poem=valid_poem, brief={"selected_threshold_phrase": "Love speaks before thunder.", "semantic_proof_chain": ["love", "rescue"], "opening_movement": "rescued love", "closing_movement": "love becomes praise", "central_thought": "rescued love becomes praise", "emotional_charge": "wonder", "threshold_phrase_rationale": "Love precedes the storm."}, theological_risk_register=[{"risk_id": "R1"}])
