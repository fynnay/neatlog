neatlog

Very simple but fancy looking logging module.
It's based on python's standard logging module and uses the colorlog module written by Sam Clements (@borntyping on GitHub) and colorama by Jonathan Hartley (@tartley on GitHub) to output colored logs to the console on Mac, Linux and Windows.

If you quickly want to create informative and easy to read logs with some flexibility this is the right module.
If you want lots for flexibility this is not the right module.

![example](http://i.imgur.com/mC4lBOQ.png)

#### Basic usage
You can log messages like in print() without using placeholders or converting values to strings.
```python
import neatlog
LOG = neatlog._Logger('test')
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
LOG.setLevel(20)
```

#### Change verbosity
This settings is to change how much info is included in each log.
The consolehandler verbosity default is 10.
The filehandler always has maximum verbosity so it prints as much info as possible to the logfile.
You can however change the verbosity of the console handler
```python
LOG.setVerbosity(0)  # Level, message
LOG.setVerbosity(10) # Level, function, message
LOG.setVerbosity(20) # Level, file, function, message
LOG.setVerbosity(30) # Level, file, function, line, message
LOG.info("something")
```

Feel free to suggest stuff or point out bugs etc..
