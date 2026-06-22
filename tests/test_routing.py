from devotional_engine.engine import route_after_failure
from devotional_engine.states import State

def test_routes():
    assert route_after_failure(["D1 [BOTH] bad"]) is State.COMPOSE_PROSE
    assert route_after_failure(["D1 [POEM] bad", "D2 [POEM] bad"]) is State.COMPOSE_POEM
    assert route_after_failure(["V4 invalid"]) is State.DIRECTOR_BRIEF
    assert route_after_failure(["[CHRISTOLOGY] bad"]) is State.CANONICAL_CORRESPONDENCE
