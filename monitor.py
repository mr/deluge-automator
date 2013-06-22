#Copyright (c) 2013 Matthew Robinson
#
#See the file LICENSE for copying permission.

import os
import string

from deluge.ui.client import client


class Monitor(object):
    def __init__(self):
        self.trackerlist = {"animebyt.es", "bakabt.me",
                            "speed.cd", "what.cd", "waffles.fm"}
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
