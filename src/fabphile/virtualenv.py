from fabric.api import prefix, sudo, settings, hide
from fabirc.crontrib.files import exists
from fabphile.common import check

def mkvirtualenv(path):
    "Create a new virtualenv via the virtualenv command"
    check(path, "You must provide a path to make the virtualenv")
    with settings(hide('everything')):
        return sudo("/usr/bin/virtualenv %s" % path)

def virtualenv(path):
    "Activate the virtualenv as a prefix"
    check(path, "You must provide a path to activate the virtualenv")
    activate_script = "%/bin/activate" % path
    check(exists(activate_script), "Virtual env at '%s' is missing" % path)
    return prefix("source %s/bin/activate" % path)
