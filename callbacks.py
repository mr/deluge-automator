import base64
import os

from monitor import Monitor, checkdirectory
import processargs

from deluge.ui.client import client
from twisted.internet import reactor

m = Monitor()
options = processargs.readConfig(os.path.expanduser("~/.deluge-automator"))


def mainLoop():
    monitordir = os.path.expanduser(options['monitordir'])
    if monitordir[len(monitordir) - 1] != '/':
        monitordir += '/'

    files = checkdirectory(monitordir)
    for i in range(0, len(files)):
        files[i] = monitordir + files[i]

    m.cleanTorrents()

    if files:
        for tfile in files:
            readData(tfile)
    reactor.callLater(10, mainLoop)


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
