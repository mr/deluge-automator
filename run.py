#!/usr/bin/python2
#Copyright (c) 2013 Matthew Robinson
#
#See the file LICENSE for copying permission.

from callbacks import on_connect_success, on_connect_fail, options

from deluge.ui.client import client
from twisted.internet import reactor

d = client.connect(
    host=options['host'],
    port=int(options['port']),
    username=options['username'],
    password=options['password']
)

d.addCallback(on_connect_success)
d.addErrback(on_connect_fail)

reactor.run()

reactor.addSystemEventTrigger('before', 'shutdown', client.disconnect)
