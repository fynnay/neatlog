# neatlog

Very simple but fancy looking logging module.
It's based on python's standard logging module and uses the `colorlog` module written by Sam Clements (@borntyping on GitHub) for outputting colorized logs in the terminal and `colorama` by Jonathan Hartley (@tartley on GitHub) for Windows support.

Want to quickly create informative and easy to read logs? Then this is the right module for you.
Want lots of customizability? This is not the right module for you.

![example](neatlog.png)

#### Basic usage
```python
import neatlog
LOG = neatlog.getLogger('MyLogger')
LOG.debug(f"debug {'something'}")
LOG.info("info")
LOG.warning("warning")
LOG.error("error")
LOG.critical("critical")
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

-- CHANGELOG
The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)

### [1.0.1-beta] - 2017-08-19
#### Changed
- Fixes a bug that caused the fileHandler to log the wrong parent function name
#### Added
- FileHandler now has same indentation style as consoleHandler for better readability

### [1.0.0-beta] - 2017-08-13
#### Changed
- Fixed bug messing with stacktrace, which displayed wrong linenumbers, file- and functionnames in log messages

#### Removed
- To fix the bug mentioned above, I unfortunately had to remove the functionality to pass a tuple into the log functions. Writing custom functions to for stacktracing correctly got too messy and the payoff isn't big enough. Sorry 'bout that.
