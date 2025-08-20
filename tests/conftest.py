import pytest


@pytest.fixture
def logger_name() -> str:
    return "MY_LOGGER"


@pytest.fixture
def level_debug_str():
    return "debug"
