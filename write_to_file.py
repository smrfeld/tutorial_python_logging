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