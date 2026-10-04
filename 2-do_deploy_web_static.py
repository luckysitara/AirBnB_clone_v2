#!/usr/bin/python3
from fabric.api import *
from os.path import exists
from datetime import datetime
from fabric.api import local

env.hosts = ['35.237.103.2', '35.227.27.195']


def do_pack():
    '''
    Fabric script that generates a .tgz archive from the
    contents of the web_static
    '''
    try:
        filepath = 'versions/web_static_' + datetime.now().\
                   strftime('%Y%m%d%H%M%S') + '.tgz'
        local('mkdir -p versions')
        local('tar -zcvf versions/web_static_$(date +%Y%m%d%H%M%S).tgz\
        web_static')
        print('web_static packed: {} -> {}'.
              format(filepath, os.path.getsize(filepath)))
    except Exception:
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
        run('mkdir -p {}'.format(release))
        run('tar -xzf /tmp/{} -C {}/'.format(file_name, release))
        run('rm /tmp/{}'.format(file_name))
        run('mv {}/web_static/* {}/'.format(release, release))
        run('rm -rf {}/web_static'.format(release))
        run('rm -rf /data/web_static/current')
        run('ln -s {}/ /data/web_static/current'.format(release))
        return True
    except Exception:
        return False
