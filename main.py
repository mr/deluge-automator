import base64
import time
import os

#from monitor import Monitor
import monitor
import processargs

from deluge.ui.client import client
from twisted.internet import reactor

from deluge.log import setupLogger
setupLogger()

options = processargs.readConfig("/home/matt/.deluge-automator")

d = client.connect(
    host=options['host'],
    port=int(options['port']),
    username=options['username'],
    password=options['password']
)

#m = Monitor()


def on_torrent_added_success(result, tfile):
    print "Torrent added successfully!"
    print "result: ", result
    #m.addTorrent(result)
    os.remove(tfile)
    time.sleep(10)
    start()


def on_torrent_added_fail(result):
    print "Add torrent failed!"
    print "result: ", result


def start():
    #m.cleanTorrents

    tfile = options['monitordir']
    while tfile == options['monitordir']:
        time.sleep(10)
        tfile = options['monitordir'] + monitor.checkdirectory(
            options['monitordir'])

    f = open(tfile, "rb")
    data = f.read()
    f.close()

    t = client.core.add_torrent_file(tfile,
                                     base64.encodestring(data), None)

    t.addCallback(on_torrent_added_success, tfile)
    t.addErrback(on_torrent_added_fail)


def on_connect_success(result):
    print "Connection was successful!"
    print "result: ", result

    start()


d.addCallback(on_connect_success)


def on_connect_fail(result):
    print "Connection failed!"
    print "result: ", result


d.addErrback(on_connect_fail)

reactor.run()
