#!/usr/bin/python2
#Copyright (c) 2013 Matthew Robinson
#
#See the file LICENSE for copying permission.

from deluge.ui.client import client
from twisted.internet import reactor

import os
import string
import argparse
import base64

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
        privatetracker = status['tracker_host'] in self.trackerlist
        print status['tracker_host']

        if status['progress'] == 100.0 and not privatetracker:
            client.core.remove_torrent(torrent_id,
                                       False)
            self.torrentlist.remove(torrent_id)
        elif privatetracker:
            self.torrentlist.remove(torrent_id)


m = Monitor()

def poll_dir(monitordir):
    directory = os.path.expanduser(monitordir)
    files = [os.path.join(directory, name) for name in os.listdir(directory)
             if name.endswith(".torrent")]

    m.cleanTorrents()

    if files:
        for tfile in files:
            readData(tfile)
    reactor.callLater(10, poll_dir)


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


def on_connect_success(result, monitordir):
    print "Connection was successful!"
    print "result: ", result
    poll_dir(monitordir)


def on_connect_fail(result):
    print "Connection failed!"
    print "result: ", result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Manage a remote deluge instance easily")
    parser.add_argument('-H', '--host', default="localhost")
    parser.add_argument('-P', '--port', default=44103)
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('-d', '--monitordir', default="~/downloads")

    args = parser.parse_args()

    d = client.connect(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password
    )

    d.addCallback(on_connect_success, args.monitordir)
    d.addErrback(on_connect_fail)

    reactor.run()

    reactor.addSystemEventTrigger('before', 'shutdown', client.disconnect)
