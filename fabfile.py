# -*- coding: utf-8 -*-

from datetime import datetime

from fabric.api import task, run, local, put, cd, env


env.user = 'deployer'
env.hosts = ['lukazupareli.net']

app_name = 'my_plant'
app_dir = '/opt/apps/' + app_name
packfile_name = 'git-HEAD.tar.gz'

sockfile_path = '/tmp/myplant-uwsgi.sock'
pidfile_path = '/tmp/myplant-uwsgi.pid'


@task
def install():
    run('apt-get install python-bluez')
    run('pip install -r requirements.txt')


@task
def deploy_detup():
    run('mkdir -p ' + app_dir)


@task
def deploy():
    now = datetime.now()
    timestamp = now.strftime('%Y%m%d-%H%M%S')
    current_dir = timestamp

    deploy_dir = '%s/%s' % (app_dir, current_dir)
    deploy_packfile_path = '%s/%s' % (app_dir, packfile_name)

    put(packfile_name, app_dir)

    with cd(deploy_dir):
        run('tar zxf %s -C %s' % (deploy_packfile_path, deploy_dir))
        run('uwsgi --stop %s; true' % pidfile_path)
        run('uwsgi --pidfile %s -s %s -w actions:app' % (pidfile_path, sockfile_path))


def pack():
    local('git archive --format=tar.gz --prefix=git-HEAD/ vHEAD > ' + packfile_name)
