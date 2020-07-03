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