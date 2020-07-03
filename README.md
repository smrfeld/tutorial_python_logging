# Tutorial on using Python's logging module

A short guide to getting starting with Python's `logging` module.

[Link to Medium article.](https://medium.com/@oliver.k.ernst/stop-using-pythons-print-for-your-library-786a1016f792)

<img src="cover.jpg" alt="drawing" width="400"/>

We've all done this:
```
print("here")
result = foo.do_something()
print("worked")
# print(result)
# print("OK")
another_result = bar.do_something()
# print(another result)
print("didnt work")
```
This is ridiculous!

Use Python's logging module to clean up your logs.

All the code for the package can be found [here](https://github.com/smrfeld/tutorial_python_logging).

## Requirements

None - `logging` is built in. Note that we will be using `python3`.

## A simple logging example

Let's dive in with a simple logging example
```
import logging

if __name__ == "__main__":

    # Set up logging
    # Ensure that all messages can be handled on the output stream
    # To quiet different levels in the logs, we will quiet the specific logger,
    # not the whole stream
    handlerPrint = logging.StreamHandler()
    handlerPrint.setLevel(logging.DEBUG)

    # A logger with name my_logger will be created
    # and then add it to the print stream
    log = logging.getLogger("my_logger")
    log.addHandler(handlerPrint)

    # Log a little
    log.debug("[hidden] This is for debugging")
    log.info("[hidden] This is for info")
    log.warning("This is for warnings")
    log.error("This is for errors")

    # Log a little more
    log.setLevel(logging.DEBUG)
    log.debug("Again, this is for debugging")
    log.info("Again, this is for info")
    log.warning("Again, this is for warnings")
    log.error("Again, this is for errors")
```
The output will be:
```
This is for warnings
This is for errors
Again, this is for debugging
Again, this is for info
Again, this is for warnings
Again, this is for errors
```
Notice that there is a `StreamHandler` called `handlerPrint`, and a `logger` called `log`. 
* Many different type of handlers exist as described [here](https://docs.python.org/3/library/logging.handlers.html). They control where the output of the logs go.
* You can create many different loggers with the `getLogger(name)` command - if the logger with the given name does not exist, it will be created.
* Loggers can be assigned one or more handlers.

When do messages appear? Only if both the `handler` and the `logger` allow it. The possible logging levels are:
```
DEBUG
INFO
WARNING
ERROR
```
The default level is `WARNING`.

Here we first turned the `handler` logging level to `DEBUG`, but the `logger` level is still the default `WARNING`. 
Therefore, only the warning messages appear from the first part.
```
This is for warnings
This is for errors
```
Next we turn on the `logger` to be `DEBUG` as well - now all messages will appear:
```
Again, this is for debugging
Again, this is for info
Again, this is for warnings
Again, this is for errors
```

## Configuration options

Next we should dive into configuration options:
```
import logging

if __name__ == "__main__":

    # Set up logging
    # Ensure that all messages can be handled on the output stream
    # To quiet different levels in the logs, we will quiet the specific logger,
    # not the whole stream
    handlerPrint = logging.StreamHandler()
    handlerPrint.setLevel(logging.DEBUG)

    # A logger with name my_logger will be created
    # and then add it to the print stream
    log = logging.getLogger("my_logger")
    log.addHandler(handlerPrint)

    # Set up the format
    formatter = logging.Formatter('%(asctime)25.25s | %(levelname)10.10s | %(filename)20.20s | %(message)s')
    handlerPrint.setFormatter(formatter)

    # Turn on all levels of logging
    log.setLevel(logging.DEBUG)

    # Log a little
    log.debug("This is for debugging")
    log.info("This is for info")
    log.warning("This is for warnings")
    log.error("This is for errors")
```
The output will be:
```
2020-07-03 11:22:05,323 |      DEBUG |     configuration.py | This is for debugging
2020-07-03 11:22:05,323 |       INFO |     configuration.py | This is for info
2020-07-03 11:22:05,323 |    WARNING |     configuration.py | This is for warnings
2020-07-03 11:22:05,323 |      ERROR |     configuration.py | This is for errors
```
Fancy! 

A complete list of formatting options is [here](https://docs.python.org/3/library/logging.html#logrecord-attributes).

## Writing logs to files

A common use scenario is writing logs to a file. Simply add a new handler:
```
import logging
import logging.handlers
from pathlib import Path

if __name__ == "__main__":

    # Set up logging
    # Ensure that all messages can be handled on the output stream
    # To quiet different levels in the logs, we will quiet the specific logger,
    # not the whole stream
    handlerPrint = logging.StreamHandler()
    handlerPrint.setLevel(logging.DEBUG)

    # Make new log every hour with 23 backups for the other hours
    log_dir = "./logs/"
    # Ensure directory exists
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    handlerWrite = logging.handlers.TimedRotatingFileHandler(
        log_dir + "logs.log",
        when="h",
        interval=1,
        backupCount=23)
    handlerWrite.setLevel(logging.DEBUG)   

    # A logger with name my_logger will be created
    # and then add it to the print stream
    log = logging.getLogger("my_logger")
    log.addHandler(handlerPrint)
    log.addHandler(handlerWrite)

    # Set up the format
    formatter = logging.Formatter('%(asctime)25.25s | %(levelname)10.10s | %(filename)20.20s | %(message)s')
    handlerPrint.setFormatter(formatter)
    handlerWrite.setFormatter(formatter)

    # Turn on all levels of logging
    log.setLevel(logging.DEBUG)

    # Log a little
    log.debug("This is for debugging")
    log.info("This is for info")
    log.warning("This is for warnings")
    log.error("This is for errors")
```
Notice the steps:
1. We created a new `TimedRotatingFileHandler` called `handlerWrite`. It writes to a `log` directory. 
    Every hour, a new file will be created (`when="h"` and `interval=1`). The new files will have an index number appended to them.
    A maximum of `24` files will exist - `backupCount=23` plus the normal `logs.log` file. After this, logs will be overwritten.
2. Add the handler to the logger.
3. Set up the format for the handler. Here it is the same as for the print handler, but it can also be different.

## Using the logging module in your library

[Here](https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library) are the official docs on configuring the logging module for your library.
But I'll give you my unofficial take: the goals are two-fold:
* Get global control over your module, letting you set the level for all your classes/methods.
* Get local control over every class.
This is exactly what the division between `handlers` and `loggers` will let us do.

The scheme is:
* Set up either one `logger` for your module, or if there are enough classes, one for each class. Put the names into the **documentation**.
* Set up the formatter as desired, but just **once for your entire module**. Different output formats in the same module look terrible and are confusing.
* If you want to collect all the logs from all the classes in a single file, also set up a **single file** that returns a configured `TimedRotatingFileHandler` (or whetever handler you like).
* Remember that there are **two controls** for the logging level - the `loggers` and the `handlers`. The default level for both is `WARNING`. 
    The `DEBUG` level should only be relevant for you or other developers, but `INFO` may be interesting for everyone. 
    I therefore recommend to turn your `loggers` levels to `INFO` by default.

Let us create a module called `mypackage` with the following files:
```
mypackage/__init__.py
mypackage/foo.py
mypackage/bar.py
mypackage/logging_options.py
test_mypackage.py
```
Let's look at the logging options first:
```
import logging
import logging.handlers
from pathlib import Path

# Set up print handler
handlerPrint = logging.StreamHandler()

# Allow everything to be printed
handlerPrint.setLevel(logging.DEBUG)

# Set up rotating file handler
log_dir = "./mypackage_logs/"
Path(log_dir).mkdir(parents=True, exist_ok=True)
log_fname = "mypackage.log"
handlerWrite = logging.handlers.TimedRotatingFileHandler(
    log_dir + log_fname,
    when="h",
    interval=1,
    backupCount=23)

# Allow everything to be printed
handlerWrite.setLevel(logging.DEBUG)

# Set up the formatter globally
formatter = logging.Formatter('%(asctime)25.25s | %(levelname)10.10s | %(filename)20.20s | %(message)s')
handlerPrint.setFormatter(formatter)
handlerWrite.setFormatter(formatter)

# Common method to create a logger
def setup_logger(name):

    # A logger with name my_logger will be created
    # and then add it to the print stream
    log = logging.getLogger(name)
    
    # Turn on INFO by default
    # Leave DEBUG for developers
    log.setLevel(logging.INFO)
    
    # Add logger to the handlers
    log.addHandler(handlerPrint)
    log.addHandler(handlerWrite)

    return log
```
Here, we set up formatting and `handlers` for the entire module. In the `foo.py` and `bar.py` files, we use them as follows:
```
from . import logging_options

class Foo:

    def __init__(self):
        # Setup logging
        self.log = logging_options.setup_logger("foo")

    def do_something(self):

        self.log.warning("--- Starting do_something ---")

        self.log.info("Counting for 10 seconds")

        cumulative = 0
        for count in range(0,10):
            self.log.info("count: %d" % count)

            cumulative += count
            self.log.debug("cumulative count: %d" % cumulative)

            if count == 3:
                self.log.error("quitting early!")
                break

        self.log.warning("--- Finished do_something ---")
```
and `bar.py`:
```
from . import logging_options

class Bar:

    def __init__(self):
        # Setup logging
        self.log = logging_options.setup_logger("bar")

    def do_something(self):

        self.log.warning("--- Starting do_something ---")

        self.log.info("Counting for 5 seconds")

        cumulative = 0
        for count in range(0,5):
            self.log.info("count: %d" % count)

            cumulative += count
            self.log.debug("cumulative count: %d" % cumulative)

            if count == 2:
                self.log.error("quitting early!")
                break

        self.log.warning("--- Finished do_something ---")
```
In the the test method `test_mypackage.py`, we can see how to selectively control output:
```
import mypackage
import logging

if __name__ == "__main__":

    # Try it
    # Only INFO and higher will be shown
    f = mypackage.Foo()
    f.do_something()

    # Turn on all the logs
    logging.getLogger("foo").setLevel(logging.DEBUG)
    f.do_something()

    # Turn off info for everything in print but not in write
    mypackage.logging_options.handlerPrint.setLevel(logging.WARNING)

    # Try bar
    b = mypackage.Bar()
    b.do_something()
```
The output in the print stream is:
```
2020-07-03 12:42:34,401 |    WARNING |               foo.py | --- Starting do_something ---
2020-07-03 12:42:34,402 |       INFO |               foo.py | Counting for 10 seconds
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 0
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 1
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 2
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 3
2020-07-03 12:42:34,402 |      ERROR |               foo.py | quitting early!
2020-07-03 12:42:34,402 |    WARNING |               foo.py | --- Finished do_something ---
2020-07-03 12:42:34,403 |    WARNING |               foo.py | --- Starting do_something ---
2020-07-03 12:42:34,403 |       INFO |               foo.py | Counting for 10 seconds
2020-07-03 12:42:34,403 |       INFO |               foo.py | count: 0
2020-07-03 12:42:34,403 |      DEBUG |               foo.py | cumulative count: 0
2020-07-03 12:42:34,403 |       INFO |               foo.py | count: 1
2020-07-03 12:42:34,403 |      DEBUG |               foo.py | cumulative count: 1
2020-07-03 12:42:34,403 |       INFO |               foo.py | count: 2
2020-07-03 12:42:34,403 |      DEBUG |               foo.py | cumulative count: 3
2020-07-03 12:42:34,404 |       INFO |               foo.py | count: 3
2020-07-03 12:42:34,404 |      DEBUG |               foo.py | cumulative count: 6
2020-07-03 12:42:34,404 |      ERROR |               foo.py | quitting early!
2020-07-03 12:42:34,404 |    WARNING |               foo.py | --- Finished do_something ---
2020-07-03 12:42:34,404 |    WARNING |               bar.py | --- Starting do_something ---
2020-07-03 12:42:34,405 |      ERROR |               bar.py | quitting early!
2020-07-03 12:42:34,405 |    WARNING |               bar.py | --- Finished do_something ---
```
and in the log file:
```
2020-07-03 12:42:34,401 |    WARNING |               foo.py | --- Starting do_something ---
2020-07-03 12:42:34,402 |       INFO |               foo.py | Counting for 10 seconds
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 0
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 1
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 2
2020-07-03 12:42:34,402 |       INFO |               foo.py | count: 3
2020-07-03 12:42:34,402 |      ERROR |               foo.py | quitting early!
2020-07-03 12:42:34,402 |    WARNING |               foo.py | --- Finished do_something ---
2020-07-03 12:42:34,403 |    WARNING |               foo.py | --- Starting do_something ---
2020-07-03 12:42:34,403 |       INFO |               foo.py | Counting for 10 seconds
2020-07-03 12:42:34,403 |       INFO |               foo.py | count: 0
2020-07-03 12:42:34,403 |      DEBUG |               foo.py | cumulative count: 0
2020-07-03 12:42:34,403 |       INFO |               foo.py | count: 1
2020-07-03 12:42:34,403 |      DEBUG |               foo.py | cumulative count: 1
2020-07-03 12:42:34,403 |       INFO |               foo.py | count: 2
2020-07-03 12:42:34,403 |      DEBUG |               foo.py | cumulative count: 3
2020-07-03 12:42:34,404 |       INFO |               foo.py | count: 3
2020-07-03 12:42:34,404 |      DEBUG |               foo.py | cumulative count: 6
2020-07-03 12:42:34,404 |      ERROR |               foo.py | quitting early!
2020-07-03 12:42:34,404 |    WARNING |               foo.py | --- Finished do_something ---
2020-07-03 12:42:34,404 |    WARNING |               bar.py | --- Starting do_something ---
2020-07-03 12:42:34,404 |       INFO |               bar.py | Counting for 5 seconds
2020-07-03 12:42:34,404 |       INFO |               bar.py | count: 0
2020-07-03 12:42:34,404 |       INFO |               bar.py | count: 1
2020-07-03 12:42:34,404 |       INFO |               bar.py | count: 2
2020-07-03 12:42:34,405 |      ERROR |               bar.py | quitting early!
2020-07-03 12:42:34,405 |    WARNING |               bar.py | --- Finished do_something ---
```
We can therefore control output selectively for:
* Different streams, such as printing and different file handlers.
* Different classes / methods.
* The entire module all at once.

## Final thoughts

That does it for me, I'm tired of logging and blogging. All the code for the package can be found [here](https://github.com/smrfeld/tutorial_python_logging).

In a future part I will discuss logging in `C++` using `spdlog`.