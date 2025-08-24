import logging
from inspect import isclass
from typing import Optional, Type

import pytest
from pytest_lazyfixture import lazy_fixture as lf


class TestLogger:
    def test_get_header(
            self,
            monkeypatch,
            date_time_now,
            host_name,
            os_name,
            f_logger,
            f_header,
    ):
        monkeypatch.setattr("platform.uname", lambda: (os_name, host_name))

        value = f_logger.getHeader()
        assert value == f_header

    @pytest.mark.parametrize(
        ["state", "expected"],
        [
            [False, 999],
            [True, lf("f_level")]
        ]
    )
    def test_enable_console_handler(
            self,
            state,
            expected,
            f_logger,
        ):
        f_logger.enableConsoleHandler(state)

        assert f_logger._consoleHandler.level == expected

    @pytest.mark.parametrize(
        ["state", "file_path", "expected"],
        [
            [True, None, ValueError],
            [False, None, None],
            [True, lf("f_file_path"), lf("f_level")],
        ]
    )
    def test_enable_file_handler(
            self,
            state,
            file_path,
            expected,
            f_logger,
    ):
        def exe():
            return f_logger.enableFileHandler(state, filePath=file_path)

        if isclass(expected) and issubclass(expected, Exception):
            with pytest.raises(expected):
                exe()
        else:
            exe()

            if expected is None:
                assert f_logger._fileHandler is None
            else:
                # FileHandler always has the lowest level to log everything
                assert f_logger._fileHandler.level == logging.DEBUG


    def test_set_file_path(self):
        pytest.fail()

    def test_file_path(self):
        pytest.fail()

    def test_set_level(self):
        pytest.fail()

    def test_set_verbosity(self):
        pytest.fail()
