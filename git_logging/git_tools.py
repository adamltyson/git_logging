"""
git
===============

Wrappers around gitpython to return information about the git repository
for debugging

"""


import os
import imp

# Change this to your software
import seaborn as program_name


class GitError(Exception):
    """
    Exception if gitpython cannot be found or if it fails
    (Typical in production environments).
    """

    pass


class GitHead:
    """
    Class to parse a repo.heat.commit object from gitpython, and return
    more informative properties
    """

    def __init__(self, head_commit):
        self.hash = head_commit.hexsha
        self.committer_name = head_commit.committer.name
        self.committer_email = head_commit.committer.email
        self.message = head_commit.summary
        self.datetime = head_commit.authored_datetime.strftime(
            "Date: %Y-%m-%d, Time: %H-%M-%S"
        )


class GitInfo:
    """
    Class to parse a repo object from gitpython, and return more informative
    properties
    """

    def __init__(self, repo):
        self.head = GitHead(repo.head.commit)


def get_git_info(repo_path):
    """
    Returns a class with useful information about the git repository.
    (if there is one). Will only work with "dev" installs (otherwise
    gitpython is not installed)
    :return:
    """

    try:
        import git

    except ImportError:
        raise GitError
        return None

    try:
        repo = git.Repo(repo_path)
        return GitInfo(repo)

    except git.InvalidGitRepositoryError:
        raise GitError
        return None


def write_git_info(file):
    """
    Writes useful information about the git repository to the log file.
    :param file: Log file
    :return: file with git information written
    """
    file.write("\n\n\n**************  GIT INFO  *********" "*****\n\n")
    try:
        module_path = imp.find_module(program_name.__name__)[1]
        module_path = os.path.split(module_path)[0]
        git_info = get_git_info(module_path)

        file.write("Commit hash: {} \n".format(git_info.head.hash))
        file.write("Commit message: {} \n".format(git_info.head.message))
        file.write("Commit date & time: {} \n".format(git_info.head.datetime))
        file.write("Commit author: {} \n".format(git_info.head.committer_name))
        file.write(
            "Commit author email: {}".format(git_info.head.committer_email)
        )
    # If cellfinder is not in a git repo
    except GitError:
        file.write("No git environment found")
