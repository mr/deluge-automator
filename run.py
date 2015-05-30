#!/usr/bin/python2
#Copyright (c) 2013 Matthew Robinson
#
#See the file LICENSE for copying permission.

from deluge.ui.client import client
from twisted.internet import reactor

import string

class Monitor(object):
    def __init__(self):
        self.trackerlist = {"animebyt.es", "bakabt.me",
                            "speed.cd", "what.cd", "waffles.fm",
                            "gazellegames.net"}
        self.torrentlist = []

    def addTorrent(self, torrent_id):
        if torrent_id is not None:
            self.torrentlist.append(torrent_id)

    def cleanTorrents(self):
        for torrent_id in self.torrentlist:
            status = client.core.get_torrent_status(torrent_id,
                                                    ['tracker_host',
                                                     'ratio',
                                                     'active_time',
                                                     'progress'])

            status.addCallback(self.cleanUp, torrent_id)

    def cleanUp(self, status, torrent_id):
        privatetracker = False
        print status['tracker_host']
        for j in self.trackerlist:
            if status['tracker_host'] == j:
                privatetracker = True
                break

        if status['progress'] == 100.0 and not privatetracker:
            client.core.remove_torrent(torrent_id,
                                       False)
            self.torrentlist.remove(torrent_id)
        elif privatetracker:
            self.torrentlist.remove(torrent_id)


def checkdirectory(directory):
    contents = os.listdir(directory)
    files = []
    for i in contents:
        if string.find(i, ".torrent") > 0:
            files.append(i)
    return files

m = Monitor()

def readConfig(config):
    f = open(config, "r")
    options = {}

    for line in f:
        if string.find(line, '#') != 0 or string.find(line, '\n') != 0:
            equals = string.find(line, "=")
            options[line[:equals]] = line[equals + 1:len(line) - 1]

    f.close()

    return options

options = readConfig(os.path.expanduser("~/.deluge-automator"))

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
