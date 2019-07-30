import logging
import os
import sys

from datetime import datetime

from git_logging import git_tools

# Change this to your software
import seaborn as program_name


def start_logging(
    output_dir,
    args=None,
    verbose=True,
    file_log_level="DEBUG",
    filename="None",
    log_header=None,
    multiprocess_aware=True,
):
    """
    :param output_dir: Directory to save the log file
    :param args: Class of options/arguements that can be written to the
    beginning of the log file
    :param bool verbose: If true, all info (i.e. 'DEBUG') is printed to
    console. Else, only 'INFO' and above. Default: True
    :param file_log_level: What level of logging to print to file.
    Default: 'DEBUG'
    :param filename: Filename for log file. Default: 'cellfinder'
    :param log_header: Header for the log file, if the args are written'
    :param multiprocess_aware: Default: True

    :return: Path to the logging file
    """
    if verbose:
        print_log_level = "DEBUG"
    else:
        print_log_level = "INFO"

    if filename is None:
        filename = program_name.__name__

    logging_file = datetime.now().strftime(filename + "_%Y-%m-%d_%H-%M-%S.log")
    logging_file = os.path.join(output_dir, logging_file)

    if args is not None:
        write_args_to_file(
            logging_file, args, output_dir, log_header=log_header
        )

    setup_logging(
        logging_file,
        print_level=print_log_level,
        file_level=file_log_level,
        multiprocess_aware=multiprocess_aware,
    )
    return logging_file


def write_args_to_file(file, args, output_dir, log_header=None):
    """
    Writes the properties of object "args" to "file", along with other
    information about how the program was called
    :param file: Output file (usually the log)
    :param args: Object with properties (e.g. the output of argparse)
    :param output_dir: Output directory of the software (in case different
    to the log)
    :param log_header: Header for the log file, if the args are written'
    """
    with open(file, "w") as file:
        if log_header is None:
            log_header = "LOG"
        file.write("**************  {}  **************\n\n".format(log_header))
        file.write(
            "Analysis carried out: "
            + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            + "\n"
        )
        file.write("Directory: " + output_dir + "\n")
        file.write("Version: {}".format(program_name.__version__))

        git_tools.write_git_info(file)

        file.write(
            "\n\n\n**************  COMMAND LINE ARGUMENTS  *********"
            "*****\n\n"
        )
        file.write("Command: {} \n".format(sys.argv[0]))
        file.write("Input arguments: {}".format(sys.argv[1:]))

        file.write("\n\n\n**************  ALL OPTIONS  **************\n\n")
        for attr, value in args.__dict__.items():
            if attr is not "paths":
                file.write("{}: {}\n".format(attr, value))

        file.write("\n\n**************  PATHS  **************\n\n")
        for path_name, path in args.paths.__dict__.items():
            file.write("{}: {}\n".format(path_name, path))

        file.write("\n\n**************  LOGGING  **************\n\n")
        file.close()


def setup_logging(
    filename, print_level="INFO", file_level="DEBUG", multiprocess_aware=True
):
    """
    Sets up (multiprocessing aware) logging.
    :param filename: Where to save the logs to
    :param print_level: What level of logging to print to console.
    Default: 'INFO'
    :param file_level: What level of logging to print to file.
    Default: 'DEBUG'
    :param multiprocess_aware: Default: True
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, file_level))

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s"
        " - %(processName)s %(filename)s:%(lineno)s"
        " - %(message)s"
    )
    formatter.datefmt = "%Y-%m-%d %H:%M:%S %p"
    fh = logging.FileHandler(filename)

    fh.setLevel(getattr(logging, file_level))
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, print_level))
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    if multiprocess_aware:
        import multiprocessing_logging

        multiprocessing_logging.install_mp_handler()
    logging.info("Begin")
