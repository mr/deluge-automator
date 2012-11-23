import os
import string

from deluge.ui.client import client
from deluge.error import InvalidTorrentError


class Monitor(object):
    def __init__(self):
        self.trackerlist = {"animebyt.es", "bakabt.me",
                            "bitgamer.su", "speed.cd", "what.cd"}
        self.torrentlist = []

    def addTorrent(self, torrent_id):
        self.torrentlist.append(torrent_id)

    def cleanTorrents(self):
        for torrent_id in self.torrentlist:
            status = client.core.get_torrent_status(torrent_id, ['tracker_host', 'ratio', 'active_time', 'progress'])
            status.addCallback(cleanUp, torrent_id)


def cleanUp(status, torrent_id):
    print status
    privatetracker = False
    for j in self.trackerlist:
        if status['tracker_host'] == j:
            privatetracker = True
            break

    if status['progress'] == 1:
        try:
            client.core.remove_torrent(torrent_id,
                                       False)
            self.torrentlist.remove([i for i,x in enumerate(self.torrentlist) if x == torrent_id])
        except InvalidTorrentError:
            print "Clean torrents error: torrent does not exist!"


def checkdirectory(directory):
    contents = os.listdir(directory)
    for i in contents:
        if string.find(i, ".torrent") > 0:
            return i
    return ""
