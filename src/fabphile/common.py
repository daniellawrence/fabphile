import sys
from fabric.colors import red
from fabric.api import puts

def check(boolean, message):
    if not boolean:
        puts(red(message))
        sys.exit(1)
