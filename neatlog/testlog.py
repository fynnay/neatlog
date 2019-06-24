import logging
from . import colorlog

class Logger(logging.Logger):
    def __init__(self, name, level=None, filePath=None, color=True, verbosity=10):
        super().__init__(name)
        # Prevent loggers from sending their output to loggers created earlier, thus displaying the same output twice.
        self.propagate = False

        # Formatters
        self.colorFormatter = colorlog.ColoredFormatter("%(log_color)s%(levelname)s : %(name)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s","%H:%M:%S")
        self.plainFormatter = logging.Formatter("%(levelname)s : %(name)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s","%H:%M:%S")
        self.colorFormatter.log_colors['DEBUG'] = 'green'
        # Handlers
        self.streamHandler = colorlog.StreamHandler()
        self.streamHandler.setFormatter(self.colorFormatter)
        self.addHandler(self.streamHandler)

        # Set level to level
        self.levelDict = {
            "notset"    : logging.NOTSET,
            "debug"     : logging.DEBUG,
            "info"      : logging.INFO,
            "warning"   : logging.WARNING,
            "error"     : logging.ERROR,
            "exception" : logging.CRITICAL
        }

    def setLevel(self, level):
        if isinstance(level, str):
            level = self.levelDict[level]
            super().setLevel(level)

    def setVerbosity(self, verbosity):
        pass

class Manager(object):
    """
    Keeps track of all created loggers
    """
    def __init__(self):
        self.loggers = {}

    def get(self, name):
        """
        Returns an already registered logger
        """
        return self.loggers.get(name)

    def register(self, name, logger):
        """
        Register a new logger and returns it
        """
        self.loggers[name] = logger
        return self.get(name)

MANAGER = Manager()

def getLogger(name, level='error', filePath=None, color=True, verbosity=10):
    """
    Returns an existing logger with the specified name, if one exists.
    If no logger with the specified name exists, register a new one and return that.
    :name      : <str>  -- Name of the logger
    :level     : <str>  -- Level of the logger ['debug', 'info', 'warning', 'error', 'critical', 'exception']
    :filePath  : <str>  -- File path to log file
    :color     : <bool> -- Use color in console handler [True,[False]]
    :verbosity : <int>  -- Amount of information to output
    """
    logger = MANAGER.get(name)
    if logger is None:
        newLogger = Logger(name, level, filePath, color, verbosity)
        logger = MANAGER.register(name, newLogger)
    return logger

getLogger('test')
