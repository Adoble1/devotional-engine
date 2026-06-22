import pytest
from devotional_engine.harness import validate_threshold_phrase

@pytest.mark.parametrize("phrase", ["Love speaks before thunder.", "Heaven bowed to rescue.", "The gift is God.", "The silence has grown long.", "The faithful word has vanished."])
def test_passes(phrase): assert validate_threshold_phrase(phrase)

@pytest.mark.parametrize("phrase", ["God is always faithful.", "Faith wins in the end.", "Hope rises in darkness.", "There is a kind of fear.", "Sometimes life feels hard.", "The heart grows restless."])
def test_fails(phrase): assert not validate_threshold_phrase(phrase)
