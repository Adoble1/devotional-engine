import pytest
from devotional_engine.config import EngineConfig
from devotional_engine.harness import check_prayer_address_and_close

@pytest.mark.parametrize("prayer", [
    "Father, help us. Through Jesus Christ our Lord. Amen.",
    "Our Father, help us. through Christ our Lord. Amen.",
    "Abba Father, help us. through Jesus Christ. Amen.",
])
def test_valid_addresses(context, prayer):
    context.prose["prayer"] = prayer
    assert not check_prayer_address_and_close(context, EngineConfig())[0]

def test_invalid_address(context):
    context.prose["prayer"] = "Lord God, help us. Amen."
    assert check_prayer_address_and_close(context, EngineConfig())[0]
