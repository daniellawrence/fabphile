from fabric.api import settings, hide, puts, run
from fabphile.common import check

def _invoke_aptget(apt_command, args=[]):
    "Invoke the aptget command"
    ALLOWED_APT_COMMAND = ['install', 'remove', 'update']
    command_arguments = ""
    check(apt_command in ALLOWED_APT_COMMAND, "%s command is not allowed" % apt_command)
    if type(args) == type([]):
        command_arguments = " ".join(args)
    else:
        command_arguments = args
    with settings(hide('everything')):
        results = run("apt-get %s %s" % (apt_command, command_arguments))
    return results

def _invoke_dpkg(args=[]):
    "invoke the dpkg command"
    command_arguments = ""
    if type(args) == type([]):
        command_arguments = " ".join(args)
    else:
        command_arguments = args
    return run("dpkg %s" % command_arguments)

def _install(package):
    "Install without looking"
    _invoke_aptget("install", ['-y', package])
    
def install(package):
    "Install a package via apt"
    check(package, "You must provide a package to installed")
    
    if package_is_not_installed(package):
        _install(package)
    return package_is_installed(package)

def latest(package):
    "Ensure the package is installed and upto date"
    check(package, "You must provide a package to installed & upgraded")
    install(package)
    upgrade(package)

def _remove(package):
    "Remove without looking"
    _invoke_aptget("remove", ['-y', package])
    
def remove(package):
    "Remove a package via apt"
    check(package, "You must provide a package to be removed")
    
    if package_is_not_installed(package):
        puts("%s is already removed" % package)
        return True
    _remove(package)
    
def update():
    "Just run apt-get update"
    _invoke_aptget("update")

def _upgrade(package):
    "upgrade the system or package"
    _invoke_aptget("upgrade",package)
    
def upgrade(package=None):
    "upgrade the system or package"
    check(package, "You must provide a package to be upgraded")
        
    if package and package_is_not_installed(package):
        install(package)
    _upgrade("upgrade",package)

def package_is_not_installed(package):
    "True if a package is not installed"
    return not package_is_installed(package)

def package_is_installed(package):
    "True if a package is installed"
    check(package, "You must provide a package to be checked")
    install_list = _invoke_dpkg("--get-selections %s" % package)
    installed_packages = []
    for line in install_list:
        if not line.endswith('install'):
            continue
        installed_packages.apend(line.split()[0])
    if package in installed_packages:
        return True
    else:
        return False
