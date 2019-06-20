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
    # Logging
    ch = logging.StreamHandler()
    LOG = logging.getLogger("logging")
    LOG.addHandler(ch)
    LOG.setLevel(logging.DEBUG)
    startTime = time.time()
    for i in range(0, 1000):
        LOG.debug('test')
    print("finished in %s seconds"%(time.time()-startTime))

    # Colorlog
    ch = colorlog.StreamHandler()
    LOG = colorlog.getLogger("colorlog")
    LOG.addHandler(ch)
    LOG.setLevel(logging.DEBUG)
    clStartTime = time.time()
    for i in range(0, 1000):
        LOG.debug('test')
    clFinalTime = time.time()-clStartTime

    # Neatlog
    LOG = neatlog.getLogger("neatlog")
    LOG.setLevel(logging.DEBUG)
    startTime = time.time()
    for i in range(0, 1000):
        LOG.debug('test')
    print("finished in %s seconds"%(time.time()-startTime))
