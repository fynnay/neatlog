# xlog.py

import logging

# Adding the 'username' and 'funcname' specifiers
# They must be attributes of the log record

# Custom log record
class OurLogRecord(logging.LogRecord):
    def __init__(self, name, level, fn, lno, msg, args, exc_info, func):
        # Don't pass all args to LogRecord constructor bc it doesn't expect "extra"
        logging.LogRecord.__init__(self, name, level, fn, lno, msg, args, exc_info, func)
        # Adding format specifiers is as simple as adding attributes with
        # same name to the log record object:
        self.funcname = calling_func_name()

class OurLogger(logging.getLoggerClass()):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None):
        # Don't pass all makeRecord args to OurLogRecord bc it doesn't expect "extra"
        rv = OurLogRecord(name, level, fn, lno, msg, args, exc_info, func)
        # Handle the new extra parameter.
        # This if block was copied from Logger.makeRecord
        if extra:
            for key in extra:
                if (key in ["message", "asctime"]) or (key in rv.__dict__):
                    raise KeyError("Attempt to overwrite %r in LogRecord" % key)
                rv.__dict__[key] = extra[key]
        return rv

# Register our logger
logging.setLoggerClass(OurLogger)


# Current user
def current_user():
    import pwd, os
    try:
        return pwd.getpwuid(os.getuid()).pw_name
    except KeyError:
        return "(unknown)"

# Calling Function Name
def calling_func_name():
    return calling_frame().f_code.co_name

import os, sys
def calling_frame():
    f = sys._getframe()

    while True:
        if is_user_source_file(f.f_code.co_filename):
            return f
        f = f.f_back

def is_user_source_file(filename):
    return os.path.normcase(filename) not in (_srcfile, logging._srcfile)

def _current_source_file():
    if __file__[-4:].lower() in ['.pyc', '.pyo']:
        return __file__[:-4] + '.py'
    else:
        return __file__

_srcfile = os.path.normcase(_current_source_file())

# INIT
# Test the logger
import time
samples = 3 # How many times to run over the iterations
iterations = 1000 # How many logs to create
ch = logging.StreamHandler()
LOG = logging.getLogger("xlog")
# LOG.addHandler(ch)
LOG.setLevel(logging.DEBUG)
xlFinalTime = 0
for i in range(0, samples):
    xlStartTime = time.time()
    for j in range(0, iterations):
        LOG.debug('test')
    xlFinalTime += time.time()-xlStartTime
xlFinalTime /= samples
print(xlFinalTime)
