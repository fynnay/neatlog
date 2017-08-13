import neatlog

def main():
    LOG.debug('test')

if __name__ == '__main__':
    LOG = neatlog._Logger("logging_howto",color=False)
    LOG.setLevel('debug')
    LOG.setVerbosity(30)

    LOG.debug('test')
    main()