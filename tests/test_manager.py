import pytest

import neatlog


@pytest.mark.parametrize(
    ["exists"],
    [
        [False],
        [True],
    ]
)
def test_get_logger(
        monkeypatch,
        f_logger_name,
        f_logger,
        exists,
):

    if exists:
        monkeypatch.setitem(
            neatlog.neatlog.MANAGER.loggers,
            f_logger_name,
            f_logger,
        )

    logger = neatlog.getLogger(f_logger_name)

    assert isinstance(logger, neatlog.neatlog._Logger)
    assert logger.name == f_logger_name

    if exists:
        assert logger is f_logger
