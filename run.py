#!/usr/bin/env python
# -*- coding: utf-8 -*-

from actions import app
from subprocess import call

pin = '1234'


if __name__ == "__main__":
    call(['bluetooth-agent %s &' % pin], shell=True)
    app.debug = True
    app.run('0.0.0.0')
