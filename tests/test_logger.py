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

    def test_enable_file_handler(self):
        pytest.fail()

    def test_set_file_path(self):
        pytest.fail()

    def test_file_path(self):
        pytest.fail()

    def test_set_level(self):
        pytest.fail()

    def test_set_verbosity(self):
        pytest.fail()
