from fabric.api import sudo, settings, puts, hide
from fabric.colors import green


def run_manage(command, verbose=False):
    "Run the django manage script"
    puts("Running: manage.py %s" % green(command))
    with settings(hide('everything')):
        command_results = sudo("./manage.py %s" % command)
    if verbose:
        puts(command_results)

    return command_results
