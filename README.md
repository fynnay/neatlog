logger

Very simple but fancy looking logging module.
It's based on python's standard logging module and uses the colorlog module written by Sam Clements (@borntyping on GitHub) and colorama by Jonathan Hartley (@tartley on GitHub) to output colored logs to the console on Mac, Linux and Windows.

The point of it is to let You create informative and easy to read logs without having to worry about setting up formatters or handlers and all that jazz.

Basic usage:

```python
from logger import logger
LOG = logger._Logger('test')
LOG.error('something')
```

Enable file handler:
```python
LOG.filePath = "/Users/local/Desktop/logs/test.log"
LOG.enableFileHandler(True)
LOG.debug('something')
```

Feel free to suggest stuff or point out bugs etc..
