#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import *
from datetime import datetime

env.hosts = ['34.205.65.74', '54.173.1.197']
env.user = 'ubuntu'
env.key_filename = 'school'

def do_clean(number=0):
    """
    Deletes unnecessary archives on web servers
    """
    number = int(number)
    if number < 0:
        return
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    with cd('/data/web_static/releases'):
        run('ls -1t | tail -n +{} | xargs -I {} rm -rf {}'.format(number))

    with cd('/data/web_static/versions'):
        local('ls -1t | tail -n +{} | xargs -I {} rm -rf {}'.format(number))

if __name__ == "__main__":
    do_clean()

