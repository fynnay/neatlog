import inspect
import logging
import platform
import datetime

import colorlog


class ContextFilter(logging.Filter):
    """
    Injects contextual information into the log:
    - Whitespace after level for better readability
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
        record.lvl = self.equalIndent(record)
        return True


class _Logger(logging.Logger):
    """
    Easy to set up, clean, readable logs.
    """
    def __init__(self, name, level=logging.DEBUG, filePath=None, color=True, verbosity=10):
        # Ensure highest level for logger
        super().__init__(name, level=logging.NOTSET)

        # Private attrs
        self._filePath = filePath
        self._useColor = color
        self._verbosity = verbosity
        self._level = getLoggingLevel(level)

        # Add filters for equal indenting
        self.addFilter(ContextFilter())

        # Prevent duplicate logs in previously created loggers
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
        """
        Builds text for the file handler's log file header
        """
        topScript = getParentScript(top=True)[0]
        header    = "---- LOG ----\nFile  : %s\nDate  : %s\nHost  : %s\nOS    : %s\n\n"%\
        (topScript,
         datetime.datetime.now(),
         platform.uname()[1],
         platform.uname()[0].lower())
        return header

    def enableConsoleHandler(self, state):
        """
        Enables the stream handler for console output
        """
        # Check if there is already a StreamHandler
        if state:
            self._consoleHandler.setLevel(self._level)
        else:
            self._consoleHandler.setLevel(999)

    def enableFileHandler(self, state, filePath=None):
        """
        Toggle the file handler on/off

        Args:
            state: True=on, False=off
            filePath: Specify the file path the file handler should write to

        Raises
            - ValueError: If filepath is not set before or provided here
            - ValueError: If state value type is not True or False
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

            # Append header to file.
            # TODO: Only add if file doesn't exist yet
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
        """
        Set the file path that the file handler writes to
        """
        self._filePath = filePath

    def filePath(self):
        """
        Returns file path, that the file handler writes to
        """
        return self._filePath

    def setLevel(self, level):
        """
        Sets the logging level of the stream handler.

        Accepts logging enum or str:

        - "notset", "debug", "info", "warning", "error", "exception"
        - logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
        """
        loggingLevel = getLoggingLevel(level)

        if loggingLevel is None:
            raise ValueError("Invalid logging level '%s'"%level)

        else:
            self._level = loggingLevel
            self._consoleHandler.setLevel(loggingLevel)

    def setVerbosity(self, level):
        """
        Set amount of information displayed by the console handler:

         0 : level + message
        10 : level + functionName + message
        20 : level + filename + functionName + message
        30 : level + filename + functionName + line + message
        40 : level + time + filename + functionName + line + message

        Args:
            level: Int
        """
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
    """
    Returns the levelName's corresponding logging level enum

    Args:
        levelName: Lower-case string logging level name

    Returns:
        The logging level
    """
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

    Example:
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

    Args:
        top: Get the topmost function in the chain that caused this fucntion to be called, defaults to False

    Returns:
        return: Function
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
    Returns the logger with `name`, if it exists
    otherwise creates a new one and returns that.

    Args:
        name: Name of the logger
        level: Set the logger's logging level
        filePath: File path to log file
        color: Use color in console handler [True,[False]]
        verbosity: Amount of information to output

    Returns:
        An existing logger with `name` or
        a new logger with the specified settings
    """
    logger = MANAGER.get(name)
    if logger is None:
        newLogger = _Logger(name, level, filePath, color, verbosity)
        logger = MANAGER.register(name, newLogger)
    return logger
