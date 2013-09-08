from os.path import basename
from fabric.api import run, settings, hide, local
from fabphile.common import check

ALLOWED_GIT_COMMAND = [
    'clone', 'fetch', 'pull', 'commit', 'push', 'update', 'describe']


def invoke_git(git_command, args=[]):
    command_arguments = ""
    check(git_command in ALLOWED_GIT_COMMAND,
          "%s command is not allowed" % git_command)
    if args.isinstance(list):
        command_arguments = " ".join(args)
    else:
        command_arguments = args

    with settings(hide('everything')):
        results = run("git %s %s" % (git_command, command_arguments))
    return results


def current_dir_is_gitrepo():
    "Ensure the current directory is already a git-repo"
    with settings(hide('everything'), warn_only=True):
        git_revparse = run("git rev-parse")
    return git_revparse.succeeded


def clone(git_repo):
    "Clone a report git repo into the current directory"
    check(current_dir_is_gitrepo(), "You can't clone in an existing git-repo")
    invoke_git("clone", git_repo)


def fetch():
    "fetch the current git repo"
    check(not current_dir_is_gitrepo(),
          "You can only update an existing git-repo")
    invoke_git("fetch")


def push():
    "push the current git repo"
    check(not current_dir_is_gitrepo(),
          "You can only update an existing git-repo")
    invoke_git("push")


def commit(commit_message):
    "commit changes the current git repo"
    check(not current_dir_is_gitrepo(),
          "You can only update an existing git-repo")
    invoke_git("commit", ['-m', commit_message])


def update(git_repo):
    "Update the current git repo"
    check(not current_dir_is_gitrepo(),
          "You can only update an existing git-repo")
    invoke_git("update")


def archive(archive_name):
    "Create a archive from the current git repo"
    check(current_dir_is_gitrepo(),
          "You can only archive an existing git-repo")
    invoke_git("archive", "--format=tar %s" % archive_name)


def version():
    "Return the current version"
    check(not current_dir_is_gitrepo(),
          "You can only descibe an existing git-repo")
    with settings(hide('everything')):
        return local("git describe --abbrev=1", caputure=True)


def reponame():
    "Return the repo-name"
    check(not current_dir_is_gitrepo(),
          "You can only descibe an existing git-repo")
    with settings(hide('everything')):
        git_path = local("git rev-parse --show-toplevel", capture=True)
    current_reponame = basename(git_path)
    return current_reponame
