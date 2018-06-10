#==============================
# file: test.py
# info: Demonstration of how to use neatlog
#==============================
import neatlog

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
    LOG = neatlog.getLogger("logging_howto",level='error', color=True)
    LOG.setLevel('debug')
    LOG.setVerbosity(30)
    LOG.debug('test')
    test()
