import neatlog


def test_get_logger(logger_name):
    logger = neatlog.getLogger(logger_name)
    assert isinstance(logger, neatlog.neatlog._Logger)
