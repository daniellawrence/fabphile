from fabric.api import put, run, settings, hide, sudo
import json

def run_facter():
    with settings(hide('everything')):
        results = sudo("facter --json")
    facts = json.loads("%s" % results)
    return facts

def fact(key):
    facts = run_facter()
    return facts[key]
