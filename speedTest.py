#==============================
# file: test.py
# info: Demonstration of how to use neatlog
#==============================
import neatlog
from neatlog import colorlog
import logging
import time

def test():
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
    ch = logging.StreamHandler()
    LOG = logging.getLogger("logging")
    LOG.addHandler(ch)
    LOG.setLevel(logging.DEBUG)
    lgFinalTime = 0
    for i in range(0, samples):
        lgStartTime = time.time()
        for i in range(0, iterations):
            LOG.debug('test')
        lgFinalTime += time.time()-lgStartTime
    lgFinalTime /= samples

    # Colorlog
    ch = colorlog.StreamHandler()
    LOG = colorlog.getLogger("colorlog")
    LOG.addHandler(ch)
    LOG.setLevel(logging.DEBUG)
    clFinalTime = 0
    for i in range(0, samples):
        clStartTime = time.time()
        for i in range(0, iterations):
            LOG.debug('test')
        clFinalTime += time.time()-clStartTime
    clFinalTime /= samples

    # Neatlog
    LOG = neatlog.getLogger("neatlog")
    LOG.setLevel('debug')
    nlFinalTime = 0
    for i in range(0, samples):
        nlStartTime = time.time()
        for i in range(0, iterations):
            LOG.debug('test')
        nlFinalTime += time.time()-clStartTime
    nlFinalTime /= samples

    # RESULTS
    print("'logging'  logged %s logs in %s seconds on average"%(samples, lgFinalTime))
    print("'colorlog' logged %s logs in %s seconds on average"%(samples, clFinalTime))
    print("'neatlog'  logged %s logs in %s seconds on average"%(samples, nlFinalTime))
