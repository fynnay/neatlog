import pytest

import neatlog


@pytest.fixture
def f_logger_name() -> str:
    return "MY_LOGGER"


@pytest.fixture
def f_logger(
        f_logger_name,
) -> neatlog.neatlog._Logger:
    return neatlog.neatlog._Logger(f_logger_name)


@pytest.fixture
def level_notset_str():
    return "notset"


@pytest.fixture
def level_debug_str():
    return "debug"


@pytest.fixture
def level_info_str():
    return "info"


@pytest.fixture
def level_warning_str():
    return "warning"


@pytest.fixture
def level_error_str():
    return "error"


@pytest.fixture
def level_exception_str():
    return "exception"
