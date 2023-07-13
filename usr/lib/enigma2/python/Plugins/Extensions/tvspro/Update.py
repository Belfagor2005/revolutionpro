#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
PY3 = sys.version_info.major >= 3
print("Update.py")


def upd_done():
    from os import popen, system
    cmd01 = "wget http://patbuweb.com/revolutionlite/tvspro.tar -O /tmp/tvspro.tar ; tar -xvf /tmp/tvspro.tar -C /"
    cmd02 = "wget --no-check-certificate -U 'Enigma2 - tvspro Plugin' -c 'http://patbuweb.com/revolutionlite/tvspro.tar' -O '/tmp/tvspro.tar'; tar -xvf /tmp/tvspro.tar -C /"
    cmd22 = 'find /usr/bin -name "wget"'
    res = popen(cmd22).read()
    if 'wget' not in res.lower():
        cmd23 = 'apt-get update && apt-get install wget'
        popen(cmd23)
    try:
        popen(cmd02)
    except:
        popen(cmd01)
    system('rm -rf /tmp/tvspro.tar')
    return

'''


import os
import sys
from twisted.web.client import downloadPage
PY3 = sys.version_info.major >= 3
print("Update.py")
aa = '/tmp/tvspro.tar'


def upd_done():
    print("In upd_done")
    xfile = 'http://patbuweb.com/revolutionlite/tvspro.tar'
    if PY3:
        xfile = b"http://patbuweb.com/revolutionlite/tvspro.tar"
        print("Update.py in PY3")
    import requests
    response = requests.head(xfile)
    if response.status_code == 200:
        # print(response.headers['content-length'])
        print("Code 200 upd_done xfile =", xfile)
        downloadPage(xfile, aa).addCallback(upd_last)
    elif response.status_code == 404:
        print("Error 404")
    else:
        return


def upd_last(fplug):
    import time
    import os
    time.sleep(5)
    if os.path.isfile(aa) and os.stat(aa).st_size > 10000:
        cmd = "tar -xvf /tmp/tvspro.tar -C /"
        print("cmd A =", cmd)
        os.system(cmd)
        os.remove('/tmp/tvspro.tar')
    return
'''