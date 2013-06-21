import base64
import os

from monitor import monitor
from run import options, m

from deluge.ui.client import client
from twisted.internet import reactor


def mainLoop():
    monitordir = os.path.expanduser(options['monitordir'])
    if monitordir[len(monitordir) - 1] != '/':
        monitordir += '/'

    files = monitor.checkdirectory(monitordir)
    for i in range(0, len(files)):
        files[i] = monitordir + files[i]

    print files

    m.cleanTorrents()

    if not files:
        reactor.callLater(10, mainLoop)
    else:
        for tfile in files:
            print tfile
            readData(tfile)
        reactor.callLater(10, mainLoop())


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


def on_torrent_added_fail(result):
    print "Add torrent failed!"
    print "result: ", result


def on_connect_success(result):
    print "Connection was successful!"
    print "result: ", result
    mainLoop()


def on_connect_fail(result):
    print "Connection failed!"
    print "result: ", result
