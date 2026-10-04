#!/usr/bin/python3
from fabric.api import *
from os.path import exists
from datetime import datetime
from fabric.api import local
import os

env.hosts = ['34.205.65.74', '54.173.1.197']
env.user = 'ubuntu'


def do_pack():
    '''
    Fabric script that generates a .tgz archive from the
    contents of the web_static
    '''

    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"
    archive_path = 'versions/web_static_' + time_stamp

    local('mkdir -p versions/')

    full_filename = local('tar -cvzf {} web_static/'.format(archive_path))

    if full_filename.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """
    Depploy to yoru webs server
    """
    if exists(archive_path) is False:
        return False
    file_name = archive_path.split('/')[1]
    file_path = '/data/web_static/releases'
    try:
        put(archive_path, '/tmp/')
        release = '{}{}'.format(file_path, file_name[:-4])
        run('sudo mkdir -p {}'.format(release))
        run('sudo tar -xzf /tmp/{} -C {}/'.format(file_name, release))
        run('rm /tmp/{}'.format(file_name))
        run('sudo mv {}/web_static/* {}/'.format(release, release))
        run('sudo rm -rf {}/web_static'.format(release))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}/ /data/web_static/current'.format(release))
        return True
    except Exception:
        return False


def deploy():
    '''
    Full deployment!
    '''
    do_pack_deploy = do_pack()
    if not do_pack_deploy:
        return False
    deployed = do_deploy(do_pack_deploy)
    return deployed
