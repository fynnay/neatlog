#==============================
# file: test.py
# info: Demonstration of how to use neatlog
#==============================
import neatlog
from neatlog import colorlog
import logging
import time

def test():
    one()

def one():
    two()

def two():
    three()

def three():
    four()

def four():
    five()

def five():
    six()

def six():
    last()

def last():
    # Create some logs from lowest to highest level
    LOG.debug('debug {0}'.format("something"))
    LOG.info('info')
    LOG.warning('warning')
    LOG.error('error')
    LOG.critical('critical')
    try:
        1/0
    except:
        LOG.exception("lol")

if __name__ == '__main__':
    samples = 3 # How many times to run over the iterations
    iterations = 1000 # How many logs to create

    # Logging
    fm = logging.Formatter("%(levelname)s : %(filename)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s","%H:%M:%S")
    ch = logging.StreamHandler()
    ch.setFormatter(fm)
    LOG = logging.getLogger("logging")
    LOG.addHandler(ch)
    LOG.setLevel(logging.DEBUG)
    lgFinalTime = 0
    for i in range(0, samples):
        lgStartTime = time.time()
        for j in range(0, iterations):
            LOG.debug('test')
        lgFinalTime += time.time()-lgStartTime
    lgFinalTime /= samples

    # Colorlog
    fm = colorlog.ColoredFormatter("%(log_color)s%(levelname)s : %(filename)s :: %(asctime)s.%(msecs)d - %(funcName)s - %(lineno)d >> %(message)s","%H:%M:%S")
    ch = colorlog.StreamHandler()
    ch.setFormatter(fm)
    LOG = colorlog.getLogger("colorlog")
    LOG.addHandler(ch)
    LOG.setLevel(logging.DEBUG)
    clFinalTime = 0
    for i in range(0, samples):
        clStartTime = time.time()
        for j in range(0, iterations):
            LOG.debug('test')
        clFinalTime += time.time()-clStartTime
    clFinalTime /= samples

    # Neatlog
    LOG = neatlog.getLogger("neatlog", color=False)
    LOG.setLevel('debug')
    LOG.setVerbosity(100)
    nlFinalTime = 0
    for i in range(0, samples):
        nlStartTime = time.time()
        for j in range(0, iterations):
            LOG.debug('test')
        nlFinalTime += time.time()-nlStartTime
    nlFinalTime /= samples
    test()

    # RESULTS
    print("'logging'  logged %s logs in %s seconds on average"%(iterations, lgFinalTime))
    print("'colorlog' logged %s logs in %s seconds on average"%(iterations, clFinalTime))
    print("'neatlog'  logged %s logs in %s seconds on average"%(iterations, nlFinalTime))
