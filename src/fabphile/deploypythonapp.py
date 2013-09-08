#!/usr/bin/python

from fabric.api import cd, put, run
from fabphile.virtualenv import mkvirtualenv, virtualenv
from fabphile.common import check
from fabphile.django import run_manage
from fabphile.pip import pip_install
from fabphile.git import archive

def deploy(application=None):
    """Deploy a gitrepo app to a remote service.
    You need to be in the local git repo of the application for this to work.
    """
    source_tar = "%s.tar" % application
    deploy_dir = "/opt/%s" % application

    check(application, "Must provide an application to deploy")
    
    archive(source_tar)
    put(source_tar, "/tmp/")

    run("mkdir -p %s" % deploy_dir)
    run("chown %s:%s %s" % (application, application, deploy_dir))
    
    mkvirtualenv(deploy_dir)
    with virtualenv(deploy_dir):
        pip_install("requirements.txt")
    
    with cd(deploy_dir):
        run("tar xf /tmp/%s" % source_tar)
        
    return deploy_dir
    
def deploy_django(application=None):
    """Deploy a gitrepo app to a remote service.
    You need to be in the local git repo of the application for this to work.
    """
    deploy_dir = deploy(application)
    with cd(deploy_dir):
        run_manage("syncdb --noinput")
        run_manage("collectstatic --noinput")

