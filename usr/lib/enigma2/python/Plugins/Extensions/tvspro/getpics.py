#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
****************************************
*        coded by Lululla              *
*           thank's Pcd                *
*             24/04/2022               *
*       skin by MMark                  *
****************************************
Info http://t.me/tivustream
'''
from __future__ import print_function
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap, MovingPixmap
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Sources.Source import Source
from Components.Sources.StaticText import StaticText
from Components.config import ConfigSubsection, config, configfile, ConfigText, ConfigDirectory, ConfigSelection,ConfigYesNo,ConfigEnableDisable
from Screens.InfoBarGenerics import InfoBarShowHide, InfoBarSubtitleSupport, InfoBarSummarySupport, \
	InfoBarNumberZap, InfoBarMenu, InfoBarEPG, InfoBarSeek, InfoBarMoviePlayerSummarySupport, \
	InfoBarAudioSelection, InfoBarNotifications, InfoBarServiceNotifications
from Screens.InfoBar import InfoBar
from Screens.InfoBar import MoviePlayer
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import fileExists
from Tools.Directories import resolveFilename
from enigma import eEnv, iPlayableService
from enigma import eServiceCenter
from enigma import eServiceReference
from enigma import eTimer, eActionMap
from enigma import iServiceInformation
from os.path import splitext
from time import time, localtime, strftime
import glob
import os
import re
import six
import socket
import sys
from . import Utils
global skin_path, tmpfold, picfold
global defpic, dblank
_session = None


try:
    import Image
except:
    from PIL import Image


PY3 = sys.version_info.major >= 3
print('Py3: ',PY3)

if PY3:
        import http.client
        from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
        from urllib.error import URLError, HTTPError
        from urllib.request import urlopen, Request
        from urllib.parse import urlparse
        from urllib.parse import parse_qs, urlencode, quote
        unicode = str; unichr = chr; long = int
        PY3 = True
else:
# if os.path.exists('/usr/lib/python2.7'):
        from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
        from urllib2 import urlopen, Request, URLError, HTTPError
        from urlparse import urlparse, parse_qs
        from urllib import urlencode, quote
        import httplib
        import six


global Path_Movies, defpic, dblank, res_plugin_path, skin_path

plugin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/".format('tvspro'))

def getversioninfo():
    currversion = '1.5'
    version_file = plugin_path + 'version'
    if os.path.exists(version_file):
        try:
            fp = open(version_file, 'r').readlines()
            for line in fp:
                if 'version' in line:
                    currversion = line.split('=')[1].strip()
        except:
            pass
    return (currversion)

currversion = getversioninfo()
Version = currversion + ' - 26.12.2021'
title_plug = '..:: TivuStream Pro Revolution V. %s ::..' % currversion
name_plug = 'TivuStream Pro Revolution'
res_plugin_path = plugin_path + 'res/'
# skin_path = plugin_path
defpic = res_plugin_path + "pics/defaultL.png"
dblank = res_plugin_path + "pics/blankL.png"
SREF = ""

skin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/hd/".format('tvspro'))
if Utils.isFHD():
    skin_path = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/res/skins/fhd/".format('tvspro'))

if Utils.DreamOS():
    skin_path = skin_path + 'dreamOs/'
try:
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False
if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

def make_request(url):
    try:
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0')
        response = urlopen(req)
        # response = checkStr(urlopen(req))
        link = response.read()
        response.close()
        print("link =", link)
        return link
    except:
        e = URLError #, e:
        print('We failed to open "%s".' % url)
        if hasattr(e, 'code'):
            print('We failed with error code - %s.' % e.code)
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)

#menulist
pos = []
if Utils.isFHD():
    pos.append([35,80])
    pos.append([395,80])
    pos.append([755,80])
    pos.append([1115,80])
    pos.append([1475,80])
    pos.append([35,530])
    pos.append([395,530])
    pos.append([755,530])
    pos.append([1115,530])
    pos.append([1475,530])
else:
    pos.append([20,50])
    pos.append([260,50])
    pos.append([500,50])
    pos.append([740,50])
    pos.append([980,50])
    pos.append([20,350])
    pos.append([260,350])
    pos.append([500,350])
    pos.append([740,350])
    pos.append([980,350])

def getpics(names, pics, tmpfold, picfold):
    global defpic
    defpic = defpic
    print("In getpics tmpfold =", tmpfold)
    print("In getpics picfold =", picfold)
    if Utils.isFHD():
        nw = 300
    else:
        nw = 200

    pix = []
    if config.plugins.tvspro.thumb.value == False:
        npic = len(pics)
        i = 0
        while i < npic:
            pix.append(defpic)
            i = i+1
        return pix

    cmd = "rm " + tmpfold + "/*"
    os.system(cmd)

    npic = len(pics)
    j = 0
    print("In getpics names =", names)
    print("In getpics pics =", pics)
    while j < npic:
        name = names[j]
        print("In getpics name =", name)
        if name is None:
            name = "Video"
        try:
            name = name.replace("&", "").replace(":", "").replace("(", "-")
            name = name.replace(")", "").replace(" ", "").replace("'", "")
            name = name.replace("/", "-")
            name = Utils.decodeHtml(name)
        except:
            pass

        url = pics[j]
        if url is None:
            url = ""
        url = url.replace(" ", "%20")
        url = url.replace("ExQ", "=")
        url = url.replace("AxNxD", "&")
        # print("In getpics url =", url)
#-----------------
        ext = str(os.path.splitext(url)[-1])
        picf = picfold + "/" + name + ext
        tpicf = tmpfold + "/" + name + ext
#-----------------
        if fileExists(picf):
            if ('Stagione') in str(name):
                cmd = "rm " + picf
                os.system(cmd)
            cmd = "cp " + picf + " " + tmpfold
            print("In getpics fileExists(picf) cmd =", cmd)
            os.system(cmd)
    #-----------------
        if fileExists(tpicf):
            if ('Stagione') in str(name):
                cmd = "rm " + tpicf
                os.system(cmd)
    #-----------------
        if not fileExists(picf):
            if plugin_path in url:
                try:
                    cmd = "cp " + url + " " + tpicf
                    print("In getpics not fileExists(picf) cmd =", cmd)
                    os.system(cmd)
                except:
                    pass
            else:
                try:
                    if "|" in url:
                        n3 = url.find("|", 0)
                        n1 = url.find("Referer", n3)
                        n2 = url.find("=", n1)
                        url1 = url[:n3]
                        referer = url[n2:]
                        p = Utils.getUrl2(url1, referer)
                        f1=open(tpicf,"wb")
                        f1.write(p)
                        f1.close()
                    else:
                        print("Going in urlopen url =", url)
                        fpage = Utils.AdultUrl(url)
                        f1=open(tpicf,"wb")
                        f1.write(fpage)
                        f1.close()

                except:
                    cmd = "cp " + defpic + " " + tpicf
                    os.system(cmd)

        if not fileExists(tpicf):
        # else:
            print("In getpics not fileExists(tpicf) tpicf=", tpicf)
            cmd = "cp " + defpic + " " + tpicf
            print("In getpics not fileExists(tpicf) cmd=", cmd)
            os.system(cmd)
            try:
                #start kiddac code
                size = [200, 200]
                if Utils.isFHD():
                    size = [300, 300]
                im = Image.open(tpicf).convert('RGBA')
                im.thumbnail(size, Image.ANTIALIAS)
                # crop and center image
                bg = Image.new('RGBA', size, (255, 255, 255, 0))
                imagew, imageh = im.size
                im_alpha = im.convert('RGBA').split()[-1]
                bgwidth, bgheight = bg.size
                bg_alpha = bg.convert('RGBA').split()[-1]
                temp = Image.new('L', (bgwidth, bgheight), 0)
                temp.paste(im_alpha, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)), im_alpha)
                bg_alpha = ImageChops.screen(bg_alpha, temp)
                bg.paste(im, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)))
                im = bg
                im.save(tpicf, 'PNG')

            #end kiddac code

                # im = Image.open(tpicf)#.convert('RGBA')
                # # imode = im.mode
                # # if im.mode == "JPEG":
                    # # im.save(tpicf)
                    # # # in most case, resulting jpg file is resized small one
                # # if imode.mode in ["RGBA", "P"]:
                    # # imode = imode.convert("RGB")
                    # # rgb_im.save(tpicf)
                # # if imode != "P":
                    # # im = im.convert("P")
                # # if im.mode != "P":
                    # # im = im.convert("P")
                # w = im.size[0]
                # d = im.size[1]
                # r = float(d)/float(w)
                # d1 = r*nw
                # if w != nw:
                    # x = int(nw)
                    # y = int(d1)
                    # im = im.resize((x,y), Image.ANTIALIAS)
                # im.save(tpicf, quality=100, optimize=True)
            except Exception as e:
                   print("******* picon resize failed *******")
                   print(str(e))

        else:
            tpicf = defpic
        pix.append(j)
        pix[j] = picf
        j = j+1

    cmd1 = "cp " + tmpfold + "/* " + picfold + " && rm " + tmpfold + "/* &"
    # print("In getpics final cmd1=", cmd1)
    os.system(cmd1)
    os.system('sleep 1')
    return pix


class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {"toggleShow": self.OkPressed,
         "hide": self.hide}, 0)
        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={iPlayableService.evStart: self.serviceStarted})
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(self.doTimerHide)
        except:
            self.hideTimer.callback.append(self.doTimerHide)
        self.hideTimer.start(5000, True)
        self.onShow.append(self.__onShow)
        self.onHide.append(self.__onHide)

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            self.hideTimer.stop()
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

    def OkPressed(self):
        self.toggleShow()

    def toggleShow(self):
        if self.skipToggleShow:
            self.skipToggleShow = False
            return
        if self.__state == self.STATE_HIDDEN:
            self.show()
            self.hideTimer.stop()
        else:
            self.hide()
            self.startHideTimer()

    def lockShow(self):
        try:
            self.__locked += 1
        except:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()

    def debug(obj, text = ""):
        print(text + " %s\n" % obj)

# class M3uPlay2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarAudioSelection, TvInfoBarShowHide):#,InfoBarSubtitleSupport
class M3uPlay2(
    InfoBarBase,
    InfoBarMenu,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarSubtitleSupport,
    InfoBarNotifications,
    TvInfoBarShowHide,
    Screen
):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 4000

    def __init__(self, session, name, url):
        global SREF, streaml
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.skinName = 'MoviePlayer'
        title = name
        streaml = False
        for x in InfoBarBase, \
                InfoBarMenu, \
                InfoBarSeek, \
                InfoBarAudioSelection, \
                InfoBarSubtitleSupport, \
                InfoBarNotifications, \
                TvInfoBarShowHide:
            x.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self['actions'] = ActionMap(['MoviePlayerActions',
         'MovieSelectionActions',
         'MediaPlayerActions',
         'EPGSelectActions',
         'MediaPlayerSeekActions',
         'SetupActions',
         'ColorActions',
         'InfobarShowHideActions',
         'InfobarActions',
         'InfobarSeekActions'], {'leavePlayer': self.cancel,
         'epg': self.showIMDB,
         'info': self.showIMDB,
         'stop': self.leavePlayer,
         'cancel': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        self.service = None
        service = None
        self.pcip = 'None'
        self.icount = 0
        self.url = url
        self.name = Utils.decodeHtml(name)
        self.state = self.STATE_PLAYING
        SREF = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onClose.append(self.cancel)
        # if '8088' in str(self.url):
            # # self.onLayoutFinish.append(self.slinkPlay)
            # self.onFirstExecBegin.append(self.slinkPlay)
        # else:
            # # self.onLayoutFinish.append(self.cicleStreamType)
            # self.onFirstExecBegin.append(self.cicleStreamType)
        self.onLayoutFinish.append(self.openPlay)


    def getAspect(self):
        return AVSwitch().getAspectRatioSetting()

    def getAspectString(self, aspectnum):
        return {0: _('4:3 Letterbox'),
         1: _('4:3 PanScan'),
         2: _('16:9'),
         3: _('16:9 always'),
         4: _('16:10 Letterbox'),
         5: _('16:10 PanScan'),
         6: _('16:9 Letterbox')}[aspectnum]

    def setAspect(self, aspect):
        map = {0: '4_3_letterbox',
         1: '4_3_panscan',
         2: '16_9',
         3: '16_9_always',
         4: '16_10_letterbox',
         5: '16_10_panscan',
         6: '16_9_letterbox'}
        config.av.aspectratio.setValue(map[aspect])
        try:
            AVSwitch().setAspectRatio(aspect)
        except:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp = temp + 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showinfo(self):
        # debug = True
        sTitle = ''
        sServiceref = ''
        try:
            servicename, serviceurl = getserviceinfo(sref)
            if servicename != None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl != None:
                sServiceref = serviceurl
            else:
                sServiceref = ''
            currPlay = self.session.nav.getCurrentService()
            sTagCodec = currPlay.info().getInfoString(iServiceInformation.sTagCodec)
            sTagVideoCodec = currPlay.info().getInfoString(iServiceInformation.sTagVideoCodec)
            sTagAudioCodec = currPlay.info().getInfoString(iServiceInformation.sTagAudioCodec)
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec : ' + str(sTagAudioCodec)
            self.mbox = self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        except:
            pass
        return
    def showIMDB(self):
        TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
        IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
        if os.path.exists(TMDB):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name

            text = Utils.charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists(IMDb):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name

            text = Utils.charRemove(text_clear)
            self.session.open(IMDB, text)

        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openPlay(self):
        url = str(self.url)
        name = self.name
        servicetype = '4097'
        ref = '4097:0:1:0:0:0:0:0:0:0:' + url
        if config.plugins.tvspro.services.value == 'Gstreamer':
                # ref = '5001:0:1:0:0:0:0:0:0:0:' + url
                servicetype = '5001'
        elif config.plugins.tvspro.services.value == 'Exteplayer3':
                # ref = '5002:0:1:0:0:0:0:0:0:0:' + url
                servicetype = '5002'
        elif config.plugins.tvspro.services.value == 'eServiceUri':
                # ref = '8193:0:1:0:0:0:0:0:0:0:' + url
                servicetype = '8193'
        elif config.plugins.tvspro.services.value == 'Dvb':
                ref = '1:0:1:0:0:0:0:0:0:0:' + url
                servicetype = '1'
        else:
            # if config.plugins.tvspro.services.value == 'Iptv':
              ref =   "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3a"), name.replace(":", "%3a"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        global streml
        streaml = False
        from itertools import cycle, islice
        self.servicetype = str(config.plugins.tvspro.services.value)
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(os.path.splitext(self.url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
        # if "youtube" in str(self.url):
            # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            # return
        if isStreamlinkAvailable():
            streamtypelist.append("5002") #ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            streaml = True
        if os.path.exists("/usr/bin/gstplayer"):
            streamtypelist.append("5001")
        if os.path.exists("/usr/bin/exteplayer3"):
            streamtypelist.append("5002")
        if os.path.exists("/usr/bin/apt-get"):
            streamtypelist.append("8193")
        for index, item in enumerate(streamtypelist, start=0):
            if str(item) == str(self.servicetype):
                currentindex = index
                break
        nextStreamType = islice(cycle(streamtypelist), currentindex + 1, None)
        self.servicetype = str(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openPlay(self.servicetype, url)
    def up(self):
        pass

    def down(self):
        # pass
        self.up()

    def doEofInternal(self, playing):
        self.close()

    def __evEOF(self):
        self.end = True

    def ok(self):
        if self.shown:
            self.hideInfobar()
        else:
            self.showInfobar()

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback != None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.isfile('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(SREF)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        streaml = False
        self.close()

    def leavePlayer(self):
        self.close()

