import datetime
import logging
from pathlib import Path

import pytest

import neatlog


@pytest.fixture
def f_logger_name() -> str:
    return "MY_LOGGER"


@pytest.fixture
def f_logger(
        f_logger_name,
        f_level,
) -> neatlog.neatlog._Logger:
    return neatlog.neatlog._Logger(f_logger_name, level=f_level)


@pytest.fixture(params=[
    lambda x: x.debug,
    lambda x: x.info,
    lambda x: x.warning,
    lambda x: x.error,
    lambda x: x.critical,
    lambda x: x.exception,
])
def f_get_logger_method(
        request,
):
    lamb = request.param
    return lamb


@pytest.fixture(params=[
    logging.NOTSET,
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL,
])
def f_level(request):
    return request.param


@pytest.fixture
def f_level_str(f_level):
    return logging.getLevelName(f_level).lower()


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


@pytest.fixture
def f_file_name() -> str:
    return "MyLogger.log"


@pytest.fixture
def f_file_path(tmp_path, f_file_name) -> Path:
    return Path(tmp_path) / f_file_name


@pytest.fixture
def f_message() -> str:
    return "something something loggy McLogFace"