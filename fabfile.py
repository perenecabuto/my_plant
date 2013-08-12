# -*- coding: utf-8 -*-

import os
from datetime import datetime

from fabric.api import task, run, local, put, cd, env
from fabric.context_managers import prefix


if env.user == os.environ['USER']:
    env.user = 'deployer'

env.hosts = ['lukazupareli.net']

app_name = 'my_plant'
app_dir = '/opt/apps/' + app_name
current_dir = app_dir + '/current'
packfile_name = 'git-HEAD.tar.gz'

sockfile_path = '/tmp/myplant-uwsgi.sock'
pidfile_path = '/tmp/myplant-uwsgi.pid'

bluetooth_pin = 1234


@task
def deploy():
    copy_data()
    install_requirements()
    restart()


@task
def install_requirements():
    with cd(current_dir):
        with prefix('workon ' + app_name):
            run('pip install -r requirements.txt')


@task
def install_deps():
    run('sudo apt-get install bluez python-dev python-bluez')


@task
def setup():
    run('mkdir -p ' + app_dir)
    run('mkvirtualenv --system-site-packages ' + app_name)


@task
def copy_data():
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    deploy_dir = '%s/%s' % (app_dir, timestamp)
    run('mkdir -p ' + deploy_dir)

    local('git archive --format=tar.gz HEAD > ' + packfile_name)
    put(packfile_name, app_dir)
    local('rm ' + packfile_name)

    deploy_packfile_path = '%s/%s' % (app_dir, packfile_name)

    with cd(deploy_dir):
        run('tar zxf %s -C %s' % (deploy_packfile_path, deploy_dir))
        run('rm -rf ' + current_dir)
        run('ln -sf %s %s' % (deploy_dir, current_dir))


@task
def restart():
    with cd(current_dir):
        with prefix('workon ' + app_name):
            run('nohup bluetooth-agent %s &' % bluetooth_pin)
            run('uwsgi --stop %s; true' % pidfile_path)
            run('uwsgi -p 2 --log-master --daemonize --chmod-socket=666 -s %s --pidfile %s -w actions:app --logto /var/log/myplant-error.log --logto2 /var/log/myplant.log' % (sockfile_path, pidfile_path))
