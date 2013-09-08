from fabric.api import sudo, settings, puts, hide
from fabphile.common import check

def pip_install_requirements(requirements):
    "Install all python/pip packages in this requirements file"
    check(requirements, "You must provide a path to requirements.txt")
    with settings(hide('everything')):
        sudo("pip install -r %s" % requirements)

def pip_install(package_name=None):
    "Install a single, list-of or requirements.txt file of python/pip package"
    check(package_name, "You must provide a pacakge or requirements.txt")
    if package_name.endswith('.txt'):
        return pip_install_requirements(package_name)

    if type(package_name) == type([]):
        package_name = " ".join(package_name)
        
    puts("Installing packages in %s" % package_name)
    with settings(hide('everything')):
        sudo("pip install %s" % package_name)
