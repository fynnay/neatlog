logger

Very simple but fancy looking logging module.
It's based on python's standard logging module and uses the colorlog module written by Sam Clements (@borntyping on GitHub) and colorama by Jonathan Hartley (@tartley on GitHub) to output colored logs to the console on Mac, Linux and Windows.

If you quickly want to create informative and easy to read logs with some flexibility this is the right module.
If you want lots for flexibility this is not the right module.

#### Basic usage
You can log messages like in print() without using placeholders or converting values to strings.
```python
from logger import logger
LOG = logger._Logger('test')
LOG.debug("I have",99, "problems","but a",type(()),"ain't one.")
LOG.info('info')
LOG.warning('warning')
LOG.error('error')
LOG.critical('critical')
LOG.exception("exception")
```

#### Enable file handler
```python
LOG.setFilePath("/Users/local/Desktop/test.log")
LOG.enableFileHandler(True)
```

#### Change level
Input levelname as a string or use the [standard values](https://docs.python.org/2/library/logging.html#logging-levels) defined by the python 'logging' module
```python
LOG.setLevel('debug')
LOG.setLevel('info')
LOG.setLevel('warning')
LOG.setLevel('error')
LOG.setLevel('critical')
LOG.setLevel('exception')
LOG.setLevel(20)
```

#### Change verbosity
The filehandler always has maximum verbosity.
You can however change the verbosity of the console handler
```python
LOG.setVerbosity(20)
```

Feel free to suggest stuff or point out bugs etc..
