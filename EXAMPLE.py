import sys
import logging

from git_logging import context_logging


class MadeUpPaths:
    def __init__(self):
        self.path1 = "/path/to/the_first_place"
        self.path2 = "/path/to/the_second_place"
        self.path3 = "/path/to/the_third_place"


class MadeUpArgs:
    def __init__(self):
        self.arg1 = True
        self.another_arg = "path/to/somewhere"
        self.the_last_arg = 1000

        self.paths = MadeUpPaths()


def main(directory, filename, log_header):
    # These should be set by your software
    args = MadeUpArgs()
    verbose = True

    context_logging.start_logging(
        directory,
        filename=filename,
        args=args,
        verbose=verbose,
        log_header=log_header,
        multiprocess_aware=True,
    )

    logging.info("This is an info message")
    logging.debug("This is a debug message")
    logging.warning("This fun logging experience is about to end :(")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
