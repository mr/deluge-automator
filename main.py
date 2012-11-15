import base64
import monitor
from monitor import Monitor
import time
import os

from deluge.ui.client import client
from twisted.internet import reactor

from deluge.log import setupLogger
setupLogger()

d = client.connect(host='', port=0,
                        username="", password="")
m = Monitor()


def on_torrent_added_success(result, tfile):
    print "Torrent added successfully!"
    print "result: ", result
    m.addTorrent(result)
    os.remove(tfile)
    time.sleep(10)
    start()


def start():
    m.cleanTorrents

    tfile = "/home/matt/Downloads/"
    while tfile == "/home/matt/Downloads/":
        time.sleep(10)
        tfile = "/home/matt/Downloads/" + monitor.checkdirectory(
            "/home/matt/Downloads")

    f = open(tfile, "rb")
    data = f.read()
    f.close()

    client.core.add_torrent_file(
        tfile,
        base64.encodestring(data), None).addCallback(
            on_torrent_added_success, tfile)


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
