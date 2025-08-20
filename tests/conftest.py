import datetime

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


@pytest.fixture
def top_script() -> str:
    return neatlog.neatlog.getParentScript(top=True)[0]


@pytest.fixture
def date_time_now(monkeypatch) -> datetime.datetime:
    value = datetime.datetime(2025, 9, 15, 18, 30, 24)

    class MockDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return value

    monkeypatch.setattr("datetime.datetime", MockDatetime)

    return datetime.datetime.now()


@pytest.fixture
def host_name() -> str:
    return "host01"


@pytest.fixture
def os_name() -> str:
    return "linux"


@pytest.fixture
def f_header(top_script, date_time_now, os_name, host_name):
    header = (
        f"---- LOG ----\n"
        f"File  : {top_script}\n"
        f"Date  : {date_time_now}\n"
        f"Host  : {host_name}\n"
        f"OS    : {os_name}\n"
        f"\n"
    )
    return header
