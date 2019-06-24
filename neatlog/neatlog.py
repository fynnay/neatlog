import os
import inspect
import platform
from datetime import datetime
import logging
from . import colorlog

__version__ = "2.0.1"

#------------------------------
# LOGGER
#------------------------------
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

class _Logger(logging.Logger):
    '''
        NAME
            _Logger - For simple logging and generating a logfile

        DESCRIPTION
            For all who want clean, readable logs but don't want to spend time setting them up.

        DATA
            logger
                See :py:func:'logging.getLogger' or :py:class:'logging.Logger'

            filePath
                Path of the log-file.

            color
                Enable/Disable using color in console log.

            verbosityLevel
                see docstring of function 'setVerbosity'

        FUNCTIONS:
            enableFileHandler

    '''
    def __init__(self, name, level=logging.DEBUG, filePath=None, color=True, verbosity=10):
        super(_Logger, self).__init__(name, level=logging.NOTSET) # Ensure highest level for logger
        # VARIABLES
        self._filePath = filePath
        self._useColor = color
        self._verbosity = verbosity
        self._level = getLoggingLevel(level)

        # Add filters for equal indenting
        self.addFilter(ContextFilter())

        # Prevent logger from sending their output to loggers created earlier, thus displaying the same output twice.
        self.propagate = False

        # Formatters
        self._consoleFormat = ""
        self._consoleFormatter = colorlog.ColoredFormatter()
        self._consoleColors = {
            'DEBUG':    'cyan',
            'INFO':     'white',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        }
        self._consoleFormatter.log_colors = self._consoleColors
        plainFormatString = ["%(lvl)s : %(name)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s","%H:%M:%S"]
        self._plainFormatter = logging.Formatter(plainFormatString[0], plainFormatString[1])

        # Console handler
        self._consoleHandler = logging.StreamHandler()
        self.addHandler(self._consoleHandler)
        self.enableConsoleHandler(True)
        # Set level and verbosity
        self.setLevel(self._level)
        self.setVerbosity(level=verbosity)

        # File handler
        self._fileHandler = None

    def getHeader(self):
        """Returns the string that will be in the top of the log file written to by the fileHandler

        :return: Header text
        :rtype: str
        """
        topScript = getParentScript(top=True)[0]
        header    = "---- LOG ----\nFile  : %s\nDate  : %s\nHost  : %s\nOS    : %s\n\n"%\
        (topScript,
        datetime.now(),
        platform.uname()[1],
        platform.uname()[0].lower())
        return header

    def enableConsoleHandler(self, state):
        # Check if there is already a StreamHandler
        if state:
            self._consoleHandler.setLevel(self._level)
        else:
            self._consoleHandler.setLevel(999)

    def enableFileHandler(self, state, filePath=None):
        """Enable/disable fileHandler.

        :param state: True or False
        :type state: bool
        :param filePath: Path to file for logging entries, defaults to None. Overwrites filePath set earlier.
        :type filePath: str, optional
        :raises ValueError: If filepath is not set before or provided here
        :raises ValueError: If state is not True or False
        """
        if state is False:
            # Remove any file handlers
            for handler in reversed(self.handlers):
                if isinstance(handler,logging.FileHandler):
                    self.removeHandler(handler)
            self._fileHandler = None
        elif state is True:
            if filePath:
                self.setFilePath(filePath)
            # Check if filePath is set
            if self._filePath is None:
                raise ValueError("Filepath is not set. You need to set it with setFilePath before enabling the fileHandler.")
                return
            # Append header to file
            tempfile = open(self._filePath, 'a')
            tempfile.write(self.getHeader())
            tempfile.close()
            # Check if there is already a FileHandler
            fhExists = False
            for h in self.handlers:
                if isinstance(h, logging.FileHandler):
                    fhExists = True
                    break
            if fhExists is False:
                self._fileHandler = logging.FileHandler(self._filePath)
                self._fileHandler.setLevel(logging.DEBUG)
                self._fileHandler.setFormatter(self._plainFormatter)
                self.addHandler(self._fileHandler)
        else:
            raise ValueError("Invalid State. Can only be True or False")

    def setFilePath(self, filePath):
        '''
        Sets filePath variable.
        '''
        self._filePath = filePath

    def filePath(self):
        """Returns filepath

        :return: File path
        :rtype: str
        """
        return self._filePath

    def setLevel(self, level):
        """Sets the level for the stream handler.

        :param level: Level to be set. Can be one of:
            "notset", "debug", "info", "warning", "error", "exception"
            or
            logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
        :type level: str | int
        :raises ValueError: [description]
        """
        loggingLevel = getLoggingLevel(level)
        if loggingLevel is None:
            raise ValueError("Invalid logging level '%s'"%level)
        else:
            self._level = loggingLevel
            self._consoleHandler.setLevel(loggingLevel)

    def setVerbosity(self, level):
        '''
        Set amount of information displayed by the console handler:
        0  : level + message
        10 : level + functionName + message
        20 : level + filename + functionName + message
        30 : level + filename + functionName + line + message
        40 : level + time + filename + functionName + line + message

        :param level : <int>
        '''
        if not isinstance(level, int):
            raise ValueError("level must be %s"%(type(1)))
        # Set verbosity
        self._verbosity = level
        # Build console formatter string
        chStr = ""
        # Add Color
        if self._useColor is True:
            chStr += "%(log_color)s"
        # Build message
        if self._verbosity >= 0 :
            chStr += "%(lvl)s"
        if self._verbosity >= 40 :
            chStr += " : "
            chStr += "%(asctime)s.%(msecs)d"
        if self._verbosity >= 20 :
            chStr += " : "
            chStr += "%(filename)s"
        if self._verbosity >= 10 :
            chStr += " : "
            chStr += "%(funcName)s"
        if self._verbosity >= 30 :
            chStr += " : "
            chStr += "%(lineno)d"
        chStr += " >> "
        chStr += "%(message)s"
        if self._useColor:
            self._consoleFormatter = colorlog.ColoredFormatter(chStr, log_colors=self._consoleColors)
        else:
            self._consoleFormatter = logging.Formatter(chStr)
        self._consoleHandler.setFormatter(self._consoleFormatter)

def getLoggingLevel(levelName):
    loggingLevel = None
    levelDict = {
        "notset"    : logging.NOTSET,
        "debug"     : logging.DEBUG,
        "info"      : logging.INFO,
        "warning"   : logging.WARNING,
        "error"     : logging.ERROR,
        "exception" : logging.CRITICAL
    }
    if levelName:
        if levelName in levelDict.keys():
            loggingLevel = levelDict[levelName]
        elif levelName in levelDict.values():
            loggingLevel = levelName
        elif isinstance(levelName, int):
            loggingLevel = levelName
    return loggingLevel

def getParentFunc(top=False,ancestor=0):
    """
    !! DEPRECATED FUNCTION - WILL BE REMOVED IN A FUTURE VERSION !!
    Returns the name of the function that called this function.
    param: ancestor : <int> : Positive values get older ancestors, negative values get younger ancestors. Stops when reaching <module> level.
    param: top : <bool>     : Get the oldest ancestor that is a function. Stops before reaching <module> level.

    Excample:
    def first():
        return second()

    def second():
        print( getParentFunc() )
        print( getParentFunc(ancestor=1) )
        print( getParentFunc(ancestor=2) )
        print( getParentFunc(ancestor=-1) )
        print( getParentFunc(top=True) )
        return
    first()
    # Output:
    >>> second
    >>> first
    >>> <module>
    >>> getParentFunc
    >>> first
    """
    insp = inspect.getouterframes( inspect.currentframe() )
    if top is True:
        ret = insp[len(insp)-2][3]
    else:
        pos = 1+ancestor
        # Make sure pos is not more or lens than len(insp)
        while True:
            if pos >=len(insp):
                pos -= 1
            elif pos < 0:
                pos+=1
            else:
                break
        ret = insp[pos][3]
    return ret

def getParentScript(top=False):
    """
    !! DEPRECATED FUNCTION - WILL BE REMOVED IN A FUTURE VERSION !!
    Gets the path to the script that called this function

    :param top: Get the topmost function in the chain that caused this fucntion to be called, defaults to False
    :type top: bool, optional
    :return: Function
    :rtype: function
    """    
    # Inspect current call stack
    insp    = inspect.getouterframes(inspect.currentframe(),2)
    # Get path of the parent script of this one. If there is none, get the topmost ancestor.
    csPath  = insp[1][1] if not insp[1][1] is None and not insp[1] is None else insp[len(insp)-1][1]
    # Get topmost ancestor if *top is True
    if top is True:
        csPath = insp[len(insp)-1][1]

    # Return as list, to prevent having to rewrite all scripts that use this function if you add more things to return later.
    return [csPath]

#------------------------------
# MANAGER
#------------------------------
class Manager(object):
    """
    Keeps track of all loggers created
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
        newLogger = _Logger(name, level, filePath, color, verbosity)
        logger = MANAGER.register(name, newLogger)
    return logger
