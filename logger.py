import os
import inspect
import traceback
import platform
from datetime import datetime
import logging
import colorlog

from random import choice

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
        record.topFunc = getParentFunc(top=True)
        # How many levels to step to reach the function that called one of the log functions (debug, info etc.)
        record.parentFunc = getParentFunc(ancestor=6)
        # Equal indent beginning
        record.lvl = self.equalIndent(record)
        return True

class _Logger():
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
    def __init__(self,name,filePath=None,color=True,verbosity=0):
        # Set color usage
        self.useColor = color
        # Name the logger
        if color is True:
            self.logger = colorlog.getLogger(name)
        else:
            self.logger = logging.getLogger(name)

        # Add filters
        f = ContextFilter()
        self.logger.addFilter(f)

        # Prevent loggers from sending their output to loggers created earlier, thus displaying the same output twice.
        self.logger.propagate = False
        
        # Set Log level
        self.logger.setLevel(logging.DEBUG)
        
        # Set formatter according to console verbosity
        self.chVerbosity = verbosity
        self.chFormatter    = None
        self.fhFormatter    = None

        # Console handler
        self.ch = colorlog.StreamHandler()
        self.setVerbosity()
        self.enableConsoleHandler(True)

        # File handler
        self.fh = None
        self.filePath = filePath
        fhStr = ["%(levelname)s : %(name)s :: %(asctime)s.%(msecs)d - %(parentFunc)s - %(lineno)d >> %(message)s","%H:%M:%S"]
        self.fhFormatter = logging.Formatter(fhStr[0],fhStr[1])

    def formatForLogging(self,inp):
        msg = " ".join( [str(i) for i in inp] )
        return msg

    def debug(self,*args,**kwargs):
        return self.logger.debug(self.formatForLogging(args))

    def info(self,*args,**kwargs):
        return self.logger.info(self.formatForLogging(args))

    def warning(self,*args,**kwargs):
        return self.logger.warning(self.formatForLogging(args))

    def error(self,*args,**kwargs):
        return self.logger.error(self.formatForLogging(args))

    def critical(self,*args,**kwargs):
        return self.logger.critical(self.formatForLogging(args))

    def exception(self,*args,**kwargs):
        # Use 'error' level to avoid parentFunc detection problems
        return self.logger.error(self.formatForLogging(args),exc_info=True)

    def enableConsoleHandler(self,state):
        # Check if there is already a StreamHandler
        chExists = False
        for h in self.logger.handlers:
            if isinstance(h,logging.StreamHandler):
                chExists = True
        # Only add a StreamHandler if none have been found
        if chExists == False:
            self.logger.addHandler(self.ch)
        if state is False:
            self.ch.setLevel(100)
        elif state is True:
            self.ch.setLevel(logging.ERROR)

    def getHeader(self):
        topScript = getParentScript(top=True)[0]
        header    = "---- LOG ----\nFile  : %s\nDate  : %s\nHost  : %s\nOS    : %s\n\n"%\
        (topScript,
        datetime.now(),
        platform.uname()[1],
        platform.uname()[0].lower())
        return header

    def enableFileHandler(self,state):
        '''
        Enable/disable fileHandler.
        You have to setFilePath before you can do this.
        '''
        if state is False:
            # Remove any file handlers
            for h in self.logger.handlers:
                if isinstance(h,logging.FileHandler):
                    self.logger.removeHandler(h)
            self.fh = None
        elif state is True:
            # Check if filePath is set
            if self.filePath is None:
                raise ValueError("self.filePath is None. You need to set it before enabling the fileHandler.")
                return
            # Append header to file
            tempfile = open(self.filePath,'a')
            tempfile.write(self.getHeader())
            tempfile.close()
            # Check if there is already a FileHandler
            fhExists = False
            for h in self.logger.handlers:
                if isinstance(h,logging.FileHandler):
                    fhExists = True
            if fhExists == False:
                self.fh = logging.FileHandler(self.filePath)
                self.fh.setLevel(logging.DEBUG)
                self.fh.setFormatter(self.fhFormatter)
                self.logger.addHandler(self.fh)
        else:
            raise ValueError("Invalid State. Can only be True or False")

    def setFilePath(self,inp):
        '''
        Sets filePath variable.
        '''
        self.filePath = inp

    def setLevel(self,inpState):
        '''
        Sets the level for the stream handler.
        '''
        state = inpState.lower() if isinstance(inpState,str) else inpState
        if state == 'debug':
            self.ch.setLevel(logging.DEBUG)
        elif state == 'info':
            self.ch.setLevel(logging.INFO)
        elif state == 'warning':
            self.ch.setLevel(logging.WARNING)
        elif state == 'error':
            self.ch.setLevel(logging.ERROR)
        elif state == 'critical':
            self.ch.setLevel(logging.CRITICAL)
        elif isinstance(state,int):
            self.ch.setLevel(state)
        else:
            raise ValueError("No such state '%s'"%inpState)

    def setVerbosity(self,level=0):
        '''
        Set amount of information displayed by the console handler:
        0  : level + message
        10 : level + functionName + message
        20 : level + fileName + functionName + message
        30 : level + fileName + functionName + line + message
        '''
        if not isinstance(level,int):
            raise ValueError("level must be <int>")

        self.chVerbosity = level
        
        # Console Formatter
        chStr = ""
        if self.useColor is True:
            chStr += "%(log_color)s"
        
        # Build message
        if self.chVerbosity >= 0 :
            chStr += "%(lvl)s"
        if self.chVerbosity >= 20 :
            chStr += " : "
            chStr += "%(name)s"
        if self.chVerbosity >= 10 :
            chStr += " : "
            chStr += "%(parentFunc)s"
        if self.chVerbosity >= 30 :
            chStr += " : "
            chStr += "%(lineno)d"
        chStr += " >> "
        chStr += "%(message)s"
        
        if self.useColor:
            self.chFormatter = colorlog.ColoredFormatter(chStr)
            # Set colors
            self.chFormatter.log_colors['DEBUG'] = 'green'
            self.chFormatter.log_colors['INFO'] = 'white'
        else:
            self.chFormatter = logging.Formatter(chStr)
        self.ch.setFormatter(self.chFormatter)


def getParentFunc(top=False,ancestor=0):
    """
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
    '''
    Gets the path to the script that called this function
    '''    
    # Inspect current call stack
    insp    = inspect.getouterframes(inspect.currentframe(),2)
    # Get path of the parent script of this one. If there is none, get the topmost ancestor.
    csPath  = insp[1][1] if not insp[1][1] is None and not insp[1] is None else insp[len(insp)-1][1]
    # Get topmost ancestor if *top is True
    if top is True:
        csPath = insp[len(insp)-1][1]

    # Return as list, to prevent having to rewrite all scripts that use this function if you add more things to return later.
    return [csPath]

def test():
    LOG = _Logger("logging_howto.py")
    LOG.setLevel('debug')
    LOG.setVerbosity(10)

    # Create some logs from lowest to highest level
    LOG.debug("I have",99, "problems","but a",type(()),"ain't one.")
    LOG.info('info')
    LOG.warning('warning')
    LOG.error('error')
    LOG.critical('critical')
    LOG.exception("lol")

# HOW TO USE
if __name__ == "__main__":
    test()
