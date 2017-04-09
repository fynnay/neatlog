import os
import inspect
import traceback
import platform
from datetime import datetime
from getParentCaller import main as getPC
import logging
import colorlog

class _Logger(object):
    '''
        NAME
            _Logger - For simple logging and generating a logfile

        DESCRIPTION
            # Create a new logger:
            LOG = _Logger("logger-name")
            
            The format of the logs looks like this:
            format : <scriptname>  -     <time>     -  <function name>  - <line>  - <log level>  - <log message>
            example: pCore.py      -  11:20:53,849  -        main       -   101   -    ERROR     - something
            
            # How to log stuff at different levels
            LOG.debug("something")
            LOG.info("something")
            LOG.warning("something")
            LOG.error("something")
            LOG.critical("something")
            LOG.exception("something")

            # Change level of the console logger
            By default only errors, critical and exceptions are written to the console.
            If yo uwant to show more levels call any of the following
                'debug' | 'info' | 'warning' | 'error' | 'critical'
            in LOG.setLevel('debug'):
            Revert to default:
            LOG.verbose(False)

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
                Path to the current log-file
            
            formatter
                Access the Formatter to change format of the logs.
                This is the default Formatter:
                    self.formatter = logging.Formatter("%(asctime)s:%(msecs)d - %(funcName)s - %(lineno)d - %(levelname)s : %(message)s","%H:%M:%S")

        FUNCTIONS:
            enableFileHandler

    '''
    def __init__(self,name,logPath=None,color=True):
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
        self.debug     = self.logger.debug
        self.info      = self.logger.info
        self.warning   = self.logger.warning
        self.error     = self.logger.error
        self.critical  = self.logger.critical
        self.exception = self.logger.exception

        # Create header to be written at the top of the .log file
        topScript = getPC(top=True)[0]
        self.header    = "---- LOG ----\nFile  : %s\nDate  : %s\nHost  : %s\nOS    : %s\n\n%s\n\n"%\
        (topScript,
        datetime.now(),
        platform.uname()[1],
        platform.uname()[0].lower(),
        "<scriptname> - <time> - <function name> - <line> - <log level> - <log message>")
        
        # Create Color Formatter
        self.colorFormatter = colorlog.ColoredFormatter('%(log_color)s%(levelname)s : %(name)s :: %(funcName)s >> %(message)s')
        # Set colors
        self.colorFormatter.log_colors['DEBUG'] = 'green'
        self.colorFormatter.log_colors['INFO'] = 'white'
        # Create Regular Formatter
        self.chFormatter    = logging.Formatter('%(levelname)s : %(name)s :: %(funcName)s : %(message)s')
        self.formatter      = logging.Formatter('%(levelname)s : %(name)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s',"%H:%M:%S")

        # Filepath used by the FileHandler. Has to be set before enabling the FileHandler
        self.filePath = logPath
        self.fh       = None

        # Create console handler
        self.chVerbose = False # Switch console handler log level between DEBUG and ERROR
        self.ch = colorlog.StreamHandler()
        if color is True:
            self.ch.setFormatter(self.colorFormatter)
        else:
            self.ch.setFormatter(self.chFormatter)
        self.enableConsoleHandler(True)

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

def test():
    LOG = _Logger("logging_howto.py")
    LOG.setLevel('debug')

    # Create some logs from lowest to highest level
    LOG.debug("Houston, we have a %s", "thorny problem")
    LOG.info('info')
    LOG.warning('warning')
    LOG.error('error')
    LOG.critical('critical')
    LOG.exception("exception")

# HOW TO USE
if __name__ == "__main__":
    test()
