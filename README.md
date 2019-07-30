## git_logging

Adam Tyson | adam.tyson@ucl.ac.uk | 2019-07-30

A (hopefully) simple example of logging various information for debugging.

### Intro
`git_logging.context_logging.start_logging()` will start (multiprocessing 
aware) logging. Prior to this, information about software version, command-line 
arguments, information about the git repository and some internal variables 
will be saved to the log. This is copied nearly verbatim out of some other 
code, so it expects an `args` object which is passed around the program, and 
for `args` to also have a `paths` object. This hardcoded, but is easily 
removed/changed.

### To run example
##### Set up environment
```bash
conda create -n logging_example python=3.6
conda activate logging_example
git clone https://github.com/mwaskom/seaborn
pip install -e seaborn/
pip install multiprocessing-logging
git clone https://github.com/adamltyson/git_logging
```

##### Run example
```bash
python git_logging/EXAMPLE.py /path/to/output/log/dir loging_name LOGGING_HEADER
```

e.g.:
```bash
python git_logging/EXAMPLE.py /home/adam/Desktop logging_test TEST_LOGGING
```

You should get a log file that resembles [this]()
This example uses [seaborn](https://github.com/mwaskom/seaborn) in place of 
your own git repository. To use your own, change the import statements in:
`git_logging/context_logging` and `git_logging/git_tools`.

If you don't want/need your logging to be multiprocessing aware, then don't 
install `multiprocessing-logging` and set `multiprocessing_aware` to `False` 
when calling `context_logging.start_logging`.
