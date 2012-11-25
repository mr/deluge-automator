import base64
import os

from monitor import Monitor
import monitor
import processargs

from deluge.ui.client import client
from twisted.internet import reactor

from deluge.log import setupLogger
setupLogger()

options = processargs.readConfig(os.path.expanduser("~/.deluge-automator"))

d = client.connect(
    host=options['host'],
    port=int(options['port']),
    username=options['username'],
    password=options['password']
)

m = Monitor()


def mainLoop():
    tfile = os.path.expanduser(options['monitordir'])
    if tfile[len(tfile)-1] != '/':
        tfile += '/'

    tfile = options['monitordir'] + monitor.checkdirectory(
        options['monitordir'])

    m.cleanTorrents()

    if tfile == options['monitordir']:
        reactor.callLater(10, mainLoop)
    else:
        readData(tfile)


def readData(tfile):
    f = open(tfile, "rb")
    data = f.read()
    f.close()

    t = client.core.add_torrent_file(tfile,
                                     base64.encodestring(data), None)

    t.addCallback(on_torrent_added_success, tfile)
    t.addErrback(on_torrent_added_fail)


def on_torrent_added_success(result, tfile):
    m.addTorrent(result)
    print "Torrent added successfully!"
    print "result: ", result
    os.remove(tfile)
    reactor.callLater(10, mainLoop())


def on_torrent_added_fail(result):
    print "Add torrent failed!"
    print "result: ", result


def on_connect_success(result):
    print "Connection was successful!"
    print "result: ", result
    mainLoop()


d.addCallback(on_connect_success)


def on_connect_fail(result):
    print "Connection failed!"
    print "result: ", result


d.addErrback(on_connect_fail)

reactor.run()

reactor.addSystemEventTrigger('before', 'shutdown', client.disconnect)
