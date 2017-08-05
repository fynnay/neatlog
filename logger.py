import os
import inspect
import traceback
import platform
from datetime import datetime
import logging
import colorlog

class _Logger(object):
    '''
        NAME
            _Logger - For simple logging and generating a logfile

        DESCRIPTION
            # Create a new logger:
            LOG = _Logger("logger-name")
            
            # Log stuff at different levels:
            LOG.debug("something")
            LOG.info("something")
            LOG.warning("something")
            LOG.error("something")
            LOG.critical("something")
            LOG.exception("something")

            # Change level of the console logger
            By default only errors, critical and exceptions are written to the console.
            If you want to show more levels call any of the following
                'debug' | 'info' | 'warning' | 'error' | 'critical'
            with LOG.setLevel('debug'):

            # Disable/Enable the file handler
            By default the logs are only shown in the console.
            To write a full-level log you need to:
            - Define an absolute filepath:
                LOG.filePath = "/path/to/log/logFileName.log"
            - Enable the logger
                LOG.enableFileHandler(True)

            To disable the fileHandler (this won't delete any previously created logfiles):
            LOG.enableFileHandler(False)

            The filename will always start with the calling.
            The header 'File' will always be the topmost script.
            That means, if a different filename is specified, the 'File' in the header
            will still be the highest ancestor to make it easier to trace errors back to the file that caused them.

        DATA
            logger
                Access the logger to change advanced settings.

            filePath
                Path to the current log-file. You need to set this before enabling the file handler.
            
            formatter
                Access the Formatter to change format of the logs using logging.Formatter syntax.
                Example:
                    self.formatter = logging.Formatter("%(asctime)s:%(msecs)d - %(funcName)s - %(lineno)d - %(levelname)s : %(message)s","%H:%M:%S")

        FUNCTIONS:
            enableFileHandler

    '''
    def __init__(self,name,filePath=None,color=True):
        # Name the logger
        if color is True:
            self.logger = colorlog.getLogger(name)
        else:
            self.logger = logging.getLogger(name)

        # Prevent loggers from sending their output to loggers created earlier, thus displaying the same output twice.
        self.logger.propagate = False
        
        # Set Log level
        self.logger.setLevel(logging.DEBUG)

        # Create substitute functions for log methods so they can be accessec at the base of the class
        # self.debug     = self.logger.debug
        # self.info      = self.logger.info
        # self.warning   = self.logger.warning
        # self.error     = self.logger.error
        # self.critical  = self.logger.critical
        # self.exception = self.logger.exception

        # Create header to be written at the top of the .log file
        topScript = getParentCaller(top=True)[0]
        self.header    = "---- LOG ----\nFile  : %s\nDate  : %s\nHost  : %s\nOS    : %s\n\n%s\n\n"%\
        (topScript,
        datetime.now(),
        platform.uname()[1],
        platform.uname()[0].lower(),
        "<level> : <script name> :: <time> - <function name> - <line> >> <custom message>")
        
        # Create Color Formatter
        self.colorFormatter = colorlog.ColoredFormatter('%(log_color)s%(levelname)s : %(name)s :: %(funcName)s >> %(message)s')
        # Set colors
        self.colorFormatter.log_colors['DEBUG'] = 'green'
        self.colorFormatter.log_colors['INFO'] = 'white'
        # Create Regular Formatter
        self.chFormatter    = logging.Formatter('%(levelname)s : %(name)s :: %(funcName)s : %(message)s')
        self.formatter      = logging.Formatter('%(levelname)s : %(name)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s',"%H:%M:%S")

        # Filepath used by the FileHandler. Has to be set before enabling the FileHandler
        self.filePath = filePath
        self.fh       = None

        # Create console handler
        self.chVerbose = False # Switch console handler log level between DEBUG and ERROR
        self.ch = colorlog.StreamHandler()
        if color is True:
            self.ch.setFormatter(self.colorFormatter)
        else:
            self.ch.setFormatter(self.chFormatter)
        self.enableConsoleHandler(True)

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
        return self.logger.exception(self.formatForLogging(args))

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
            if self.chVerbose is True:
                self.ch.setLevel(logging.DEBUG)

    def enableFileHandler(self,state):
        if state is False:
            # Remove any file handlers
            for h in self.logger.handlers:
                if isinstance(h,logging.FileHandler):
                    self.logger.removeHandler(h)
            self.fh = None
        elif state is True:
            if self.filePath is None:
                raise ValueError("self.filePath is None. You need to set it before enabling the fileHandler.")
                return
            # Write header to file, if it doesn't exist yet.
            if not os.path.exists(self.filePath):
                tempfile = open(self.filePath,'a')
                tempfile.write(self.header)
                tempfile.close()
            # Check if there is already a FileHandler
            fhExists = False
            for h in self.logger.handlers:
                if isinstance(h,logging.FileHandler):
                    fhExists = True
            if fhExists == False:
                self.fh = logging.FileHandler(self.filePath)
                self.fh.setLevel(logging.DEBUG)
                self.fh.setFormatter(self.formatter)
                self.logger.addHandler(self.fh)
        else:
            raise ValueError("Invalid State. Can only be True or False")

    def verbose(self,state):
        '''
        Change Verbosity of the console handler.
        '''
        if state is False:
            self.ch.setLevel(logging.ERROR)
        elif state is True:
            self.ch.setLevel(logging.DEBUG)
            self.chVerbose = True
        else:
            raise ValueError("Invalid State. Can only be True or False")

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

def getParentCaller(top=False):
    '''
    Gets the path to the script
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

    # Create some logs from lowest to highest level
    LOG.debug("I have",99, "problems","but a",type(()),"ain't one.")
    LOG.info('info','15')
    LOG.warning('warning')
    LOG.error('error')
    LOG.critical('critical')
    LOG.exception("exception")

# HOW TO USE
if __name__ == "__main__":
    test()
