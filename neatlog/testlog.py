import logging
from . import colorlog

class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log:
    - Add whitespace after loglevels to get more readable logs
    - Custom 'parentFunction'
    """
    def equalIndent(self,record):
        if record.levelname == "DEBUG":
            outp = "DEBUG   "
        elif record.levelname == "INFO":
            outp = "INFO    "
        elif record.levelname == "WARNING":
            outp = "WARNING "
        elif record.levelname == "ERROR":
            outp = "ERROR   "
        elif record.levelname == "CRITICAL":
            outp = "CRITICAL"
        return outp

    def filter(self, record):
        # Equal indent beginning
        record.lvl = self.equalIndent(record)
        return True

class Logger(logging.getLoggerClass()):
    def __init__(self, name, level=None, filePath=None, color=True, verbosity=10):
        super(Logger, self).__init__(name)
        # Prevent loggers from sending their output to loggers created earlier, thus displaying the same output twice.
        self.propagate = False

        # Formatters
        self.colorFormatter = colorlog.ColoredFormatter("%(log_color)s%(lvl)s : %(name)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s","%H:%M:%S")
        self.colorFormatter.log_colors = {
            'DEBUG':    'cyan',
            'INFO':     'white',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }
        # Handlers
        self.streamHandler = colorlog.StreamHandler()
        self.addHandler(self.streamHandler)
        self.streamHandler.setFormatter(self.colorFormatter)

        # Create level dict
        self.levelDict = {
            "notset"    : logging.NOTSET,
            "debug"     : logging.DEBUG,
            "info"      : logging.INFO,
            "warning"   : logging.WARNING,
            "error"     : logging.ERROR,
            "exception" : logging.CRITICAL
        }

        # Add filter
        self.addFilter(ContextFilter())

    def setLevel(self, level):
        if level:
            if isinstance(level, str):
                level = self.levelDict[level]
            super(Logger, self).setLevel(level)

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
