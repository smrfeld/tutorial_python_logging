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
