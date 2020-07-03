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