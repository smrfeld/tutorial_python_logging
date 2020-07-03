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
