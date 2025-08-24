# neatlog

Very simple but fancy looking logging module.
It's based on python's standard logging module and uses the `colorlog` module written by Sam Clements (@borntyping on GitHub) for outputting colorized logs in the terminal and `colorama` by Jonathan Hartley (@tartley on GitHub) for Windows support.

- Want to quickly create informative and easy to read logs?
  - ✅ This is the right module for you.
- Want lots of customizability?
  - 🚫 This is not the right module for you.

![example](neatlog.png)

# Usage

## Setup & Logging

Please note, that you can also specify the level differently - see [Change logging level](#change-logging-level).

```python
import neatlog

LOG = neatlog.getLogger("MyLogger", level="debug")

LOG.debug(f"debug {'something'}")
LOG.info("info")
LOG.warning("warning")
LOG.error("error")
LOG.critical("critical")
LOG.exception("exception")
```

## Change logging level

Set the level by name, integer or the `logging` module's [standard values](https://docs.python.org/2/library/logging.html#logging-levels).

```python
import logging
import neatlog

LOG = neatlog.getLogger("MyLogger")

LOG.setLevel("info")
LOG.setLevel(20)
LOG.setLevel(logging.INFO)
```

## Change verbosity

Change how much info is included in each log entry.

- The `ConsoleHandler`'s default verbosity is `10`.
- The `FileHandler` always uses maximum verbosity to prints as much info to the logfile as possible.

The info that's included at each verbosity is predefined to:

```python
import neatlog

LOG = neatlog.getLogger("MyLogger")

LOG.setVerbosity(0)  # level, message
LOG.setVerbosity(10) # level, function, message
LOG.setVerbosity(20) # level, file, function, message
LOG.setVerbosity(30) # level, file, function, line, message
```

## Enable file handler

```python
import neatlog

LOG = neatlog.getLogger("MyLogger")

LOG.enableFileHandler(True, filePath="/tmp/MyLogger_test.log")
```

# Dependencies

Runs on `python-3.7+` - potentially also older versions.

## Necessary

- `colorlog`
- `colorama` (on Windows)

## Dev

Not necessary, but needed to run the included [tests](tests) and see code coverage.

- [pytest](https://pypi.org/project/pytest/)
- [pytest-lazy-fixture](https://pypi.org/project/pytest-lazy-fixture/)
- [coverage](https://pypi.org/project/coverage/)

# Contribution

I'd like to keep this little module small and simple. Bug fixes (and reports) are welcome. Please suggest features in a ticket. Feel free to fork if you want to change major things.

# Development

- Set up development environment (or ride with your system interpreter if you like danger)
  - Install `python-3.7` using `pyenv` (or whatever python versions manager you like)
  - Set up a new `virtualenv` (or whatever environment manager you like)
- Get the code
  - Clone this repo
  - Checkout a (new) branch
- Install dependencies
  - Activate your `virtualenv`
  - Navigate to the repo's root folder
  - Run `pip install ".[dev]"` to install [necessary](#necessary) and [dev](#dev) dependencies

---

# CHANGELOG

Based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)

### [3.0.0] - 2025

⚠️ `colorlog` and `colorama` dependencies no longer embedded. See Dependencies section.

#### Added

- `pyproject.toml` file for better dev setup and transparent dependencies overview
    - `[windows]` dependencies section for colorama
    - `[dev]` dependencies section for development and running the tests

#### Removed

- The colorama module, which was previously embedded
- The colorlog module, which was previously embedded
- The getParentFunc function, which was deprecated in an earlier version

### Bug Fixes

Doesn't exactly *fix* these - but does remove the embedded `colorlog` and `colorama` modules and instead adding them as a dependency to the `pyproject.toml` file. This way, they can be version managed independently instead of poking around in `neatlog` to avoiding system-specific issues.

- fixes #10
- fixes #9

_Actually_ fixes these:

- fixes a bug that considered 'critical' to be an invalid logging level string
- fixes a bug that didn't consider 0 (aka NOTSET) to be a valid logging level

### [2.0.1] - 2019-07-24

Fixed a bug that prevented colors from being displayed.

### [2.0.0] - 2019-07-24

I noticed some significant slowdowns when logging a lot of messages. So this is pretty much a rewrite that fixes that. It also means that *looot* of stuff has been changed (+ hopefully improved).
Should be backwards compatible for the most part.

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
