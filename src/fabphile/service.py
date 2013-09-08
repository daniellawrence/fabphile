from fabric.api import puts, sudo, settings, hide
from fabric.colours import green, blue, red
from fabpfile.common import check

def invoke_rc(service, action):
    "Trigger a service to perform an action."
    with settings(hide("everything"), warn_only=True, sudo_user=None):
        return sudo("/etc/init.d/{0} {1}".format(service, action))

def rc_start(service):
    "Trigger a service to perform a start."
    return invoke_rc(service, action='start')

def rc_stop(service):
    "Trigger a service to perform a stop."
    return invoke_rc(service, action='stop')

def rc_status(service):
    "Trigger a service to perform a stop."
    return invoke_rc(service, action='status')

def upstart_stop(service):
    "stop a service via upstart, and confirm that it has stopped."
    if 'stop' in upstart_status(service):
        puts("%s is already %s" % (blue(service), red('stopped')))
        return True

    # invoke upstart to stop the service
    with settings(hide('everything'), sudo_user=None):
        sudo("stop %s" % service)

    check('stop' in upstart_status(service), "Failed to stop %s." % service)

    puts(green("%s has been %s" % (blue(service), green("stopped"))))
    return True

def upstart_start(service):
    "start a service via upstart and confirm that it has started."
    if 'start' in upstart_status(service):
        puts("%s is already %s" % (blue(service), red('started')))
        return True

    # invoke upstart to start the service
    with settings(hide('everything'), sudo_user=None):
        sudo("start %s" % service)

    check('start' in upstart_status(service),
          "Failed to start %s." % service)

    puts(green("%s has been %s" % (blue(service), green("started"))))
    return True

def upstart_status(service, expected_status=None):
    "check the status of a service, return the current status."
    with settings(hide('everything'), sudo_user=None):
        results = sudo("status %s" % service)
        
    # The 2nd column is always the current status
    status = results.stdout.split()[1]
    if expected_status:
        check(expected_status in status,
              "%s was not in expected status of %s - currently in %s" %
              (service, expected_status, status))
    return status
