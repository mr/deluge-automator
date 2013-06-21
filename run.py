#Copyright (c) 2013 Matthew Robinson
#
#See the file LICENSE for copying permission.

import os

from monitor import Monitor
from callbacks import on_connect_success, on_connect_fail
import processargs

from deluge.ui.client import client
from twisted.internet import reactor

options = processargs.readConfig(os.path.expanduser("~/.deluge-automator"))

d = client.connect(
    host=options['host'],
    port=int(options['port']),
    username=options['username'],
    password=options['password']
)

m = Monitor()

d.addCallback(on_connect_success)
d.addErrback(on_connect_fail)

reactor.run()

reactor.addSystemEventTrigger('before', 'shutdown', client.disconnect)
