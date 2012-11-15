import os
import string

from deluge.core.torrentmanager import TorrentManager
from deluge.ui.client import client
from deluge.error import InvalidTorrentError


class Monitor(object):

    def __init__(self):
        self.torrentmanager = TorrentManager()
        self.trackerlist = {"animebyt.es", "bakabt.me",
                            "bitgamer.su", "speed.cd", "what.cd"}

    def addTorrent(self, torrent_id):
        self.torrentlist.append(self.torrentmanager[torrent_id])

    def cleanTorrents(self):
        for i in self.torrentlist:
            torrentchecked = self.torrentlist[i]
            privatetracker = False

            for j in self.trackerlist:
                if torrentchecked.get_tracker_host() == self.trackerlist[j]:
                    privatetracker = True
                    break

            if (torrentchecked.get_file_progress() == 1.0 and
                    torrentchecked.get_ratio() >= 1.0 and not privatetracker):

                try:
                    client.core.remove_torrent(torrentchecked.torrent_id,
                                               False)
                except InvalidTorrentError:
                    print "Clean torrents error: torrent does not exist!"


def checkdirectory(directory):
    contents = os.listdir(directory)
    i = 0
    while i < len(contents):
        if string.find(contents[i], ".torrent") > 0:
            return contents[i]
        i += 1
    return ""
