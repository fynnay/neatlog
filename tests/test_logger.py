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
        ["already_on", "expected_level"],
        [
            [True, logging.WARNING],
            [False, logging.DEBUG],
        ]
    )
    @pytest.mark.parametrize(
        ["state", "file_path", "expected"],
        [
            [None, None, ValueError],
            [True, None, ValueError],
            [False, None, None],
            [True, lf("f_file_path"), lf("f_level")],
        ]
    )
    def test_enable_file_handler(
            self,
            monkeypatch,
            f_file_path,
            already_on,
            expected_level,
            state,
            file_path,
            expected,
            f_logger,
    ):
        mocked_file_handler = None
        mocked_level = logging.WARNING

        if already_on:
            monkeypatch.setattr(f_logger, "_filePath", f_file_path)
            mocked_file_handler = logging.FileHandler(f_file_path)
            mocked_file_handler.setLevel(mocked_level)
            monkeypatch.setattr(f_logger, "_fileHandler", mocked_file_handler)
            monkeypatch.setattr(f_logger, "handlers", [mocked_file_handler])

        def exe():
            return f_logger.enableFileHandler(state, filePath=file_path)

        if (already_on is False or state is None) and isclass(expected) and issubclass(expected, Exception):
            with pytest.raises(expected):
                exe()
        else:
            exe()

            if expected is None:
                assert f_logger._fileHandler is None
            else:
                assert f_logger._fileHandler.level == expected_level

    @pytest.mark.parametrize(
        ["file_path", "expected"],
        [
            [lf("f_file_path"), lf("f_file_path")],
            [None, None],
        ]
    )
    def test_set_file_path(
            self,
            file_path,
            expected,
            f_logger,
    ):
        f_logger.setFilePath(file_path)
        assert f_logger._filePath == file_path

    @pytest.mark.parametrize(
        ["file_path", "expected"],
        [
            [lf("f_file_path"), lf("f_file_path")],
            [None, None],
        ]
    )
    def test_file_path(
            self,
            monkeypatch,
            file_path,
            expected,
            f_logger,
    ):
        monkeypatch.setattr(f_logger, "_filePath", file_path)
        assert f_logger.filePath() == expected

    @pytest.mark.parametrize(
        ["level", "expected"],
        [
            [lf("f_level_str"), lf("f_level")],
            [lf("f_level"), lf("f_level")],
            [14, 14],
            [0, 0],
            [None, ValueError]
        ]
    )
    def test_set_level(
            self,
            monkeypatch,
            level,
            expected,
            f_logger,
    ):
        monkeypatch.setattr(f_logger, "_level", None)

        def exe():
            f_logger.setLevel(level)

        if expected is ValueError:
            with pytest.raises(expected):
                exe()
        else:
            exe()
            assert f_logger._level == expected

    @pytest.mark.parametrize(
        ["color_on"],
        [
            [True],
            [False],
        ]
    )
    @pytest.mark.parametrize(
        ["verbosity", "expected"],
        [
            [0.0, ValueError],
            [None, ValueError],
            [-10, " >> %(message)s"],
            [0, "%(lvl)s >> %(message)s"],
            [10, "%(lvl)s : %(funcName)s >> %(message)s"],
            [20, "%(lvl)s : %(filename)s : %(funcName)s >> %(message)s"],
            [30, "%(lvl)s : %(filename)s : %(funcName)s : %(lineno)d >> %(message)s"],
            [40, "%(lvl)s : %(asctime)s.%(msecs)d : %(filename)s : %(funcName)s : %(lineno)d >> %(message)s"],
            [100, "%(lvl)s : %(asctime)s.%(msecs)d : %(filename)s : %(funcName)s : %(lineno)d >> %(message)s"],
        ]
    )
    def test_set_verbosity(
            self,
            monkeypatch,
            verbosity,
            color_on,
            expected,
            f_logger,
    ):
        def exe():
            f_logger.setVerbosity(verbosity)

        monkeypatch.setattr(f_logger, "_verbosity", None)
        monkeypatch.setattr(f_logger, "_useColor", color_on)

        if expected is ValueError:
            with pytest.raises(expected):
                exe()
        else:
            exe()
            if color_on is True:
                expected_mod = f"%(log_color)s{expected}"
            else:
                expected_mod = f"{expected}"

            assert f_logger._consoleFormatter._fmt == expected_mod

    def test_log(
            self,
            monkeypatch,
            f_message,
            f_level,
            f_logger,
            f_get_logger_method,
    ):
        monkeypatch.setattr(f_logger, "_level", f_level)
        logger_method = f_get_logger_method(f_logger)
        logger_method(f_message)
