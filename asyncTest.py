#==============================
# file: test.py
# info: Demonstration of how to use neatlog
#==============================
import neatlog
import time
import queue
from logging.handlers import QueueHandler, QueueListener

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
    # instantiate queue & attach it to handler
    log_queue = queue.Queue(-1)
    queue_handler = QueueHandler(log_queue)
    # instantiate our custom log handler (see question)
    remote_handler = neatlog.colorlog.StreamHandler()
    # instantiate listener
    remote_listener = QueueListener(log_queue, remote_handler)
    # attach custom handler to root logger
    LOG.enableConsoleHandler(False)
    LOG.logger.addHandler(queue_handler)
    # start the listener
    remote_listener.start()

    LOG.setLevel('debug')
    LOG.setVerbosity(100)
    LOG.debug('test')
    test()
