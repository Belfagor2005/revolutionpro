# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Info http://t.me/tivustream
****************************************
*        coded by Lululla              *
*           thank's Pcd                *
*             01/12/2021               *
****************************************
'''
from __future__ import print_function
from . import _
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.FileList import FileList
from Components.Input import Input
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import MovingPixmap
from Components.Pixmap import Pixmap, MultiPixmap
from Components.ProgressBar import ProgressBar
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.ServiceList import ServiceList
from Components.Sources.List import List
from Components.Sources.Progress import Progress
from Components.Sources.Source import Source
from Components.Sources.StaticText import StaticText
from Components.Task import Task, Job, job_manager as JobManager, Condition
from Components.config import ConfigInteger, ConfigSelection, KEY_LEFT, KEY_RIGHT, KEY_0, getConfigListEntry
from Components.config import ConfigSubsection, config, configfile, ConfigText, ConfigDirectory, ConfigSelection,ConfigYesNo,ConfigEnableDisable
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.InfoBar import InfoBar
from Screens.InfoBar import MoviePlayer
from Screens.InfoBarGenerics import *
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection, InfoBarNotifications, InfoBarMenu, InfoBarSubtitleSupport
from Screens.InputBox import InputBox
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop, Standby
from Screens.TaskView import JobView
from Screens.VirtualKeyBoard import VirtualKeyBoard
from ServiceReference import ServiceReference
from Tools.Directories import SCOPE_PLUGINS, resolveFilename, pathExists, fileExists, copyfile, SCOPE_SKIN_IMAGE, SCOPE_MEDIA
from Tools.Downloader import downloadWithProgress
from Tools.LoadPixmap import LoadPixmap
from enigma import RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT
from enigma import eEnv, iPlayableService
from enigma import eServiceCenter
from enigma import eServiceReference
from enigma import eSize, eListbox, eListboxPythonMultiContent, iServiceInformation
from enigma import eTimer, quitMainloop
from enigma import gFont
from enigma import loadPNG, loadJPG, ePicLoad, gPixmapPtr, ePixmap
from os.path import splitext
from twisted.web.client import downloadPage, getPage
import os
import re
import glob
import json
import six
import sys
try:
    from Plugins.Extensions.tvspro.Utils import *
except:
    from . import Utils
_session = None
THISPLUG = '/usr/lib/enigma2/python/Plugins/Extensions/tvspro/'
PY3 = sys.version_info.major >= 3
# from six.moves.urllib.request import urlopen
# from six.moves.urllib.request import Request
# from six.moves.urllib.error import HTTPError, URLError
# from six.moves.urllib.parse import urlparse
# from six.moves.urllib.parse import quote
# from six.moves.urllib.parse import urlencode

# pythonFull = float(str(sys.version_info.major) + "." + str(sys.version_info.minor))
# pythonVer = sys.version_info.major
# PY3 = False
# if pythonFull < 3.9:
    # PY3 = True
# dreamos = False
# if DreamOS():
	# dreamos = True
# if os.path.exists('/usr/lib/python2.7'):
	# from urllib2 import urlopen, Request, URLError, HTTPError
	# from urlparse import urlparse, parse_qs
	# from urllib import quote_plus, urlencode, quote
	# import httplib
	# import six
	# from htmlentitydefs import name2codepoint as n2cp
	# from urllib import unquote_plus

# PY3 = False
# if os.path.exists('/usr/lib/python3.9'):
	# import http.client
	# from urllib.error import URLError, HTTPError
	# from urllib.request import urlopen, Request
	# from urllib.parse import urlparse
	# from urllib.parse import quote_plus, unquote_plus
	# from urllib.parse import parse_qs, urlencode, quote
	# unicode = str; unichr = chr; long = int
	# PY3 = True

if PY3:
        import http.client
        from http.client import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
        from urllib.error import URLError, HTTPError
        from urllib.request import urlopen, Request
        from urllib.parse import urlparse
        from urllib.parse import quote_plus, unquote_plus
        from urllib.parse import parse_qs, urlencode, quote
        unicode = str; unichr = chr; long = int
        PY3 = True
else:
# if os.path.exists('/usr/lib/python2.7'):
        from httplib import HTTPConnection, CannotSendRequest, BadStatusLine, HTTPException
        from urllib2 import urlopen, Request, URLError, HTTPError
        from urlparse import urlparse, parse_qs
        from urllib import quote_plus, urlencode, quote
        import httplib
        import six
        from htmlentitydefs import name2codepoint as n2cp
        from urllib import unquote_plus

try:
    from PIL import Image
except:
    import Image

HTTPConnection.debuglevel = 1

def getversioninfo():
    currversion = '1.5'
    version_file = THISPLUG + 'version'
    if os.path.exists(version_file):
        try:
            fp = open(version_file, 'r').readlines()
            for line in fp:
                if 'version' in line:
                    currversion = line.split('=')[1].strip()
        except:
            pass
    return (currversion)

global defpic, dblank
currversion = getversioninfo()
Version = currversion + ' - 15.11.2021'
title_plug = '..:: TivuStream Pro Revolution V. %s ::..' % Version
name_plug = 'TivuStream Pro Revolution'
res_plugin_path = THISPLUG + 'res/'
pngx = res_plugin_path + 'pics/setting2.png'
skin_path = THISPLUG
SREF = ""
folder_path = "/tmp/tvspro/"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

if isFHD():
    skin_path = res_plugin_path + 'skins/fhd/'
    defpic = res_plugin_path + "pics/defaultL.png"
    dblank = res_plugin_path + "pics/blankL.png"
else:
    skin_path = res_plugin_path + 'skins/hd/'
    defpic = res_plugin_path + "pics/default.png"
    dblank = res_plugin_path + "pics/blank.png"
try:
    from OpenSSL import SSL
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except:
    sslverify = False
if sslverify:
    try:
        from urlparse import urlparse
    except:
        from urllib.parse import urlparse
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx

class rvList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 22))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 26))
        self.l.setFont(4, gFont('Regular', 28))
        self.l.setFont(5, gFont('Regular', 30))
        self.l.setFont(6, gFont('Regular', 32))
        self.l.setFont(7, gFont('Regular', 34))
        self.l.setFont(8, gFont('Regular', 36))
        self.l.setFont(9, gFont('Regular', 40))
        if isFHD():
            self.l.setItemHeight(50)
        else:
            self.l.setItemHeight(40)

def rvoneListEntry(name):
    res = [name]
    if isFHD():
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1900, 50), font=7, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 6), size=(34, 25), png=loadPNG(pngx)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1000, 50), font=2, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))
    return res

def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(rvoneListEntry(name))
        icount = icount+1
        list.setList(plist)

#config
mdchoice = [
            ("4097", _("ServiceMp3(4097)")),
            ("1", _("Hardware(1)")),
            ]

if os.path.exists("/usr/bin/gstplayer"):
    mdchoice.append(("5001", _("Gstreamer(5001)")))
if os.path.exists("/usr/bin/exteplayer3"):
    mdchoice.append(("5002", _("Exteplayer3(5002)")))
config.plugins.tvspro = ConfigSubsection()
config.plugins.tvspro.services = ConfigSelection(default='4097', choices=mdchoice)
config.plugins.tvspro.thumb = ConfigSelection(default = "True", choices = [("True", _("yes")),("False", _("no"))])
config.plugins.tvspro.cachefold = ConfigDirectory("/media/hdd", False)
config.plugins.tvspro.movie = ConfigDirectory("/media/hdd/movie")
try:
    from Components.UsageConfig import defaultMoviePath
    downloadpath = defaultMoviePath()
    config.plugins.tvspro.movie = ConfigDirectory(default=downloadpath)
except:
    if os.path.exists("/usr/bin/apt-get"):
        config.plugins.tvspro.movie   = ConfigDirectory(default='/media/hdd/movie/')
cfg = config.plugins.tvspro

global Path_Movies
Path_Movies             = str(config.plugins.tvspro.movie.value)
if Path_Movies.endswith("\/\/"):
    Path_Movies = Path_Movies[:-1]
print('patch movies: ', Path_Movies)

class ConfigEx(Screen, ConfigListScreen):
    def __init__(self, session):
        skin = skin_path + 'Config.xml'
        if DreamOS():
            skin = skin_path + 'ConfigOs.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
            f.close()
        Screen.__init__(self, session)
        self.setup_title = _("SETUP PLUGIN")
        self.onChangedEntry = [ ]
        self.session = session
        self["status"] = Label()
        self["statusbar"] = Label()
        self['key_red'] = Label('Back')
        self['key_green'] = Label('Save')
        self['key_yellow'] = Button(_('Empty Cache'))
        # self["key_blue"] = Button(_(''))
        # self["key_blue"].hide()
        self["description"] = Label(_(''))
        self['actions'] = ActionMap(["SetupActions", "ColorActions", "VirtualKeyboardActions"], {
            'cancel': self.extnok,
            'yellow': self.cachedel,
            'green': self.save,
            'showVirtualKeyboard': self.KeyText,
            'ok': self.Ok_edit}, -2)
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)
        self.createSetup()
        self.onLayoutFinish.append(self.layoutFinished)
        if self.setInfo not in self['config'].onSelectionChanged:
            self['config'].onSelectionChanged.append(self.setInfo)

    def layoutFinished(self):
        self.setTitle(self.setup_title)

    def VirtualKeyBoardCallback(self, callback = None):
        if callback != None and len(callback):
            self["config"].getCurrent()[1].setValue(callback)
            self["config"].invalidate(self["config"].getCurrent())

    def KeyText(self):
        sel = self['config'].getCurrent()
        if sel:
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)

    def cachedel(self):
        fold = config.plugins.tvspro.cachefold.value + "/tvspro/pic"
        cmd = "rm " + fold + "/*"
        os.system(cmd)
        self.mbox = self.session.open(MessageBox, _('All cache fold empty!'), MessageBox.TYPE_INFO, timeout=5)

    def createSetup(self):
        self.editListEntry = None
        self.list = []
        self.list.append(getConfigListEntry(_('Services Player Reference type'), cfg.services,_("Configure Service Player Reference, Enigma restart required")))
        self.list.append(getConfigListEntry(_("Cache folder"), cfg.cachefold,_("Folder Cache Path (eg.: /media/hdd), Enigma restart required")))
        self.list.append(getConfigListEntry(_("Movie folder"), cfg.movie,_("Folder Movie Path (eg.: /media/hdd/movie), Enigma restart required")))
        self.list.append(getConfigListEntry(_("Show thumbpic ?"), cfg.thumb,_("Show Thumbpics ? Enigma restart required")))
        self['config'].list = self.list
        self["config"].setList(self.list)
        self.setInfo()

    def setInfo(self):
        entry = str(self.getCurrentEntry())
        if entry == _('Services Player Reference type'):
            self['description'].setText(_("Configure Service Player Reference, Enigma restart required"))
            return

        if entry == _('Movie folder ?'):
            self['description'].setText(_("Folder Movie Path (eg.: /media/hdd/movie), Enigma restart required"))
            return

        if entry == _('Cache folder'):
            self['description'].setText(_("Folder Cache Path (eg.: /media/hdd), Enigma restart required"))
            return

        if entry == _('Skin resolution-(restart e2 after change)'):
            self['description'].setText(_("Configure Skin Resolution Screen, Enigma restart required"))
            return

        if entry == _('Show thumbpic ?'):
            self['description'].setText(_("Show Thumbpics ? Enigma restart required"))
            return
        return

    def changedEntry(self):
        sel = self['config'].getCurrent()
        for x in self.onChangedEntry:
            x()
        try:
            if isinstance(self['config'].getCurrent()[1], ConfigEnableDisable) or isinstance(self['config'].getCurrent()[1], ConfigYesNo) or isinstance(self['config'].getCurrent()[1], ConfigSelection):
                self.createSetup()
        except:
            pass

    def getCurrentEntry(self):
        return self['config'].getCurrent() and self['config'].getCurrent()[0] or ''

    def getCurrentValue(self):
        return self['config'].getCurrent() and str(self['config'].getCurrent()[1].getText()) or ''

    def createSummary(self):
        from Screens.Setup import SetupSummary
        return SetupSummary

    def Ok_edit(self):
        ConfigListScreen.keyOK(self)
        sel = self['config'].getCurrent()[1]
        if sel and sel == config.plugins.tvspro.cachefold:
            self.setting = 'cachefold'
            self.openDirectoryBrowser(config.plugins.tvspro.cachefold.value)
        if sel and sel == config.plugins.tvspro.movie:
            self.setting = 'moviefold'
            self.openDirectoryBrowser(config.plugins.tvspro.movie.value)
        else:
            pass

    def openDirectoryBrowser(self, path):
        try:
            self.session.openWithCallback(
             self.openDirectoryBrowserCB,
             LocationBox,
             windowTitle=_('Choose Directory:'),
             text=_('Choose Directory'),
             currDir=str(path),
             bookmarks=config.movielist.videodirs,
             autoAdd=False,
             editDir=True,
             inhibitDirs=['/bin', '/boot', '/dev', '/home', '/lib', '/proc', '/run', '/sbin', '/sys', '/var'],
             minFree=15)
        except Exception as ex:
            print(ex)

    def openDirectoryBrowserCB(self, path):
        if path != None:
            if self.setting == 'cachefold':
                config.plugins.tvspro.cachefold.setValue(path)
            if self.setting == 'moviefold':
                config.plugins.tvspro.movie.setValue(path)
        return

    def save(self):
        if self['config'].isChanged():
            for x in self['config'].list:
                x[1].save()
            self.mbox = self.session.open(MessageBox, _('Settings saved correctly!'), MessageBox.TYPE_INFO, timeout=5)
            self.close()
        else:
         self.close()

    def extnok(self):
        if self['config'].isChanged():
            self.session.openWithCallback(self.cancelConfirm, MessageBox, _('Really close without saving the settings?'))
        else:
            self.close()

    def cancelConfirm(self, result):
        if not result:
            return
        for x in self['config'].list:
            x[1].cancel()
        self.close()

#getpics cover
def getpics(names, pics, tmpfold, picfold):
    global defpic
    # print("In getpics tmpfold =", tmpfold)
    # print("In getpics picfold =", picfold)
    defpic = defpic
    pix = []
    if config.plugins.tvspro.thumb.value == "False":
        defpic = defpic
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
    # print("In getpics names =", names)
    # print("In getpics pics =", pics)
    while j < npic:
        name = names[j]
        # print("In getpics name =", name)
        if name is None:
            name = "Video"
        try:
            name = name.replace("&", "").replace(":", "").replace("(", "-")
            name = name.replace(")", "").replace(" ", "").replace("'", "")
            name = name.replace("/", "-")

        except:
            pass
        url = pics[j]
        if url is None:
            url = ""
        url = url.replace(" ", "%20")
        url = url.replace("ExQ", "=")
        url = url.replace("AxNxD", "&")
        # print("In getpics url =", url)
#------- check image
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
        if not fileExists(picf):
            if THISPLUG in url:
                try:
                    cmd = "cp " + url + " " + tpicf
                    print("In getpics not fileExists(picf) cmd =", cmd)
                    os.system(cmd)
                except:
                    pass
            else:
                # now download image
                try:
                    if "|" in url:
                        n3 = url.find("|", 0)
                        n1 = url.find("Referer", n3)
                        n2 = url.find("=", n1)
                        url = url[:n3]
                        referer = url[n2:]
                        p = getUrl2(url, referer)
                        #-----------------
                        f1=open(tpicf,"wb")
                        f1.write(p)
                        f1.close()
                    else:
                        print("Going in urlopen url =", url)
                        p = ReadUrl2(url)
                        f1=open(tpicf,"wb")
                        f1.write(p)
                        f1.close()
                except:
                    cmd = "cp " + defpic + " " + tpicf
                    os.system(cmd)

        if not fileExists(tpicf):
            cmd = "cp " + defpic + " " + tpicf
            # print("In getpics not fileExists(tpicf) cmd=", cmd)
            os.system(cmd)
        # try:
            # #start kiddac code
            # size = [200, 200]
            # if screenwidth.width() > 1280:
                # size = [300, 300]
            # if os.path.exists(tpicf):
                    # try:
                        # im = Image.open(tpicf).convert('RGBA')
                        # im.thumbnail(size, Image.ANTIALIAS)
                        # # crop and center image
                        # bg = Image.new('RGBA', size, (255, 255, 255, 0))
                        # imagew, imageh = im.size
                        # im_alpha = im.convert('RGBA').split()[-1]
                        # bgwidth, bgheight = bg.size
                        # bg_alpha = bg.convert('RGBA').split()[-1]
                        # temp = Image.new('L', (bgwidth, bgheight), 0)
                        # temp.paste(im_alpha, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)), im_alpha)
                        # bg_alpha = ImageChops.screen(bg_alpha, temp)
                        # bg.paste(im, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)))
                        # im = bg
                        # im.save(tpicf, 'PNG')
                    # except Exception as e:
                        # print("******* picon resize failed *******")
                        # print(e)
            # else:
                # tpicf = defpic
            # #end kiddac code
        if isFHD():
            nw = 220
        else:
            nw = 180
        if os.path.exists(tpicf):
            try:
                im = Image.open(tpicf)#.convert('RGBA')
                # imode = im.mode
                # if im.mode == "JPEG":
                    # im.save(tpicf)
                    # # in most case, resulting jpg file is resized small one
                # if imode.mode in ["RGBA", "P"]:
                    # imode = imode.convert("RGB")
                    # rgb_im.save(tpicf)
                # if imode != "P":
                    # im = im.convert("P")
                # if im.mode != "P":
                    # im = im.convert("P")
                w = im.size[0]
                d = im.size[1]
                r = float(d)/float(w)
                d1 = r*nw
                if w != nw:
                    x = int(nw)
                    y = int(d1)
                    im = im.resize((x,y), Image.ANTIALIAS)
                im.save(tpicf, quality=100, optimize=True)
                # im.save(tpicf, 'PNG')
                # im.save(tpicf, 'JPG')
                # # im.save(tpicf)
            except Exception as e:
                   print("******* picon resize failed *******")
                   print(e)
        else:
            print("******* make picon failed *******")
            tpicf = defpic
        # except:
            # print("******* make picon failed *******")
            # tpicf = defpic
        pix.append(j)
        pix[j] = picf
        j = j+1
    cmd1 = "cp " + tmpfold + "/* " + picfold + " && rm " + tmpfold + "/* &"
    # print("In getpics final cmd1=", cmd1)
    os.system(cmd1)
    return pix

#menulist
class AnimMain(Screen):
    def __init__(self, session, menuTitle, nextmodule, names, urls, infos, pics = []):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        skin = skin_path + 'AnimMain.xml'
        with open(skin, 'r') as f:
          self.skin = f.read()
        f.close()
        self.names = names
        self.urls = urls
        self.pics = pics
        self.infos = infos
        self.nextmodule = nextmodule
        list = []
        print("self.names =", names)
        print("self.urls =", urls)
        print("menuTitle =", menuTitle)
        print("nextmodule =", nextmodule)
        nopic = len(names)
        self.pos = []
        self.index = 0
        title = menuTitle
        self["title"] = Button(title)
        self["pointer"] = Pixmap()
        self["info"] = Label()
        self["label1"] = StaticText()
        self["label2"] = StaticText()
        self["label3"] = StaticText()
        self["label4"] = StaticText()
        self["label5"] = StaticText()
        self["actions"] = ActionMap(["OkCancelActions", "EPGSelectActions", "MenuActions", "DirectionActions", "NumberActions", "ColorActions"],
        {
         "ok": self.okbuttonClick,
         "epg": self.showIMDB,
         "info": self.showIMDB,
         "cancel": self.closeNonRecursive,
         "left": self.key_left,
         "right": self.key_right,
         "up": self.key_up,
         "down": self.key_down,
         "red": self.cancel,
         "green": self.okbuttonClick,
         "yellow": self.key_menu,
         "menu": self.closeRecursive,
         "1": self.keyNumberGlobal,
         "2": self.keyNumberGlobal,
         "3": self.keyNumberGlobal,
         "4": self.keyNumberGlobal,
         "5": self.keyNumberGlobal,
         "6": self.keyNumberGlobal,
         "7": self.keyNumberGlobal,
         "8": self.keyNumberGlobal,
         "9": self.keyNumberGlobal
         })
        nop = len(self.names)
        self.nop = nop
        nh = 1
        if nop == 1:
            nh = 1
        elif nop == 2:
            nh = 2
        elif nop == 3:
            nh = 2
        elif nop == 4:
            nh = 3
        elif nop == 5:
            nh = 3
        else:
            nh = int(float(nop)/2)
        print("nop, nh =", nop, nh)
        if self.nop == 1:
            nm = self.names[0]
            self.names[0] = " "
            self.names.append(" ")
            self.names.append(nm)
            ur = self.urls[0]
            self.urls[0] = " "
            self.urls.append(" ")
            self.urls.append(ur)
            self.nop = 3
        if self.nop == 2:
            nm1 = self.names[0]
            nm2 = self.names[1]
            self.names[0] = " "
            self.names.append(nm1)
            self.names.append(nm2)
            ur1 = self.urls[0]
            ur2 = self.urls[0]
            self.urls[0] = " "
            self.urls.append(ur1)
            self.urls.append(ur2)
            self.nop = 3
            # self.index = nh
        self.index = 3
        i = 0
        ipage = 1
        self.onShown.append(self.openTest)

    def key_menu(self):
        return

    def showIMDB(self):
        if self.nop == 1:
            idx = 0
        elif self.nop == 2:
            idx = 1
        else:
            idx = self.index - 1
        name = self.names[idx]
        text_clear = name
        if is_tmdb:
            try:
                from Plugins.Extensions.tmdb import tmdb
                text = charRemove(text_clear)
                _session.open(tmdb.tmdbScreen, text, 0)
            except Exception as e:
                print("[XCF] Tmdb: ", e)
        elif is_imdb:
            try:
                from Plugins.Extensions.IMDb.plugin import main as imdb
                text = charRemove(text_clear)
                imdb(_session, text)
            except Exception as e:
                print("[XCF] imdb: ", e)

        else:
            inf = idx
            if inf and inf != '':
                text_clear = self.infos[inf]
            else:
                text_clear = name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def cancel(self):
        self.close()

    def paintFrame(self):
        pass

    def getname(self, name):
        print("Here in getname name =", name)
        if len(name) >= 60:
            namen = name[:20] + "\n" + name[20:40] + "\n" + name[40:60] + ".."
        elif 60 > len(name) >= 40:
            namen = name[:20] + "\n" + name[20:40] + name[40:] + ".."
        elif 40 > len(name) >= 20:
            namen = name[:20] + "\n" + name[20:] + ".."

        elif 20 > len(name):
            namen = name
        print("Here in getname name 2=", name)
        return namen

    def openTest(self):
        print("Here in openTest self.index, self.names =", self.index, self.names)
        i = self.index
        print("Here in openTest i =", i)
        if (i-3) > -1:
        #   name1 = self.getname(self.tlist[i-3][0])
            name1 = self.getname(self.names[i-3])
        else:
            name1 = " "
        print("Here in name1 =", name1)
        if (i-2) > -1:
        #   name2 = self.getname(self.tlist[i-2][0])
            name2 = self.getname(self.names[i-2])
        else:
            name2 = " "
        print("Here in name2 =", name2)
        #   name3 = self.getname(self.tlist[i-1][0])
        name3 = self.getname(self.names[i-1])

        #   name3 = self.names[i-1]
        print("Here in name3 =", name3)
        if i < self.nop:
        #   name4 = self.getname(self.tlist[i][0])
            name4 = self.getname(self.names[i])
        else:
            name4 = " "
        print("Here in name4 =", name4)
        if (i+1) < self.nop:
        #   name5 = self.getname(self.tlist[i+1][0])
            name5 = self.getname(self.names[i+1])
        else:
            name5 = " "
        print("Here in name5 =", name5)
        name1 = str(name1)
        name2 = str(name2)
        name3 = str(name3)
        name4 = str(name4)
        name5 = str(name5)
        self["label1"].setText(name1)
        self["label2"].setText(name2)
        self["label3"].setText(name3)
        self["label4"].setText(name4)
        self["label5"].setText(name5)
        if isFHD():
            if self.nop > 5:
                dpointer = res_plugin_path + "pics/pointerL.png"
                self["pointer"].instance.setPixmapFromFile(dpointer)
            else:
                dpointer = dblank
                self["pointer"].instance.setPixmapFromFile(dpointer)
        else:
            if self.nop > 5:
                dpointer = res_plugin_path + "pics/pointer.png"
                self["pointer"].instance.setPixmapFromFile(dpointer)
            else:
                dpointer = dblank
                self["pointer"].instance.setPixmapFromFile(dpointer)

    def key_left(self):
        self.index -= 1
        if self.index < 1:
            self.index = 1
            return
        else:
            self.openTest()

    def key_right(self):
        self.index += 1
        if self.index > self.nop:
            self.index = self.nop
            return
        else:
            self.openTest()

    def key_up(self):
        self.index -= 5
        if self.index < 1:
            self.index = 1
            return
        else:
            self.openTest()

    def key_down(self):
        self.index += 5
        if self.index > self.nop:
            self.index = self.nop
            return
        else:
            self.openTest()

    def closeNonRecursive(self):
            self.close(False)

    def closeRecursive(self):
            self.close(True)

    def createSummary(self):
            return

    def keyNumberGlobal(self, number):
        number -= 1
        if len(self["menu"].list) > number:
            self["menu"].setIndex(number)
            self.okbuttonClick()

    def okbuttonClick(self):
        if self.nop == 1:
            idx = 0
        elif self.nop == 2:
            idx = 1
        else:
            idx = self.index - 1
        print("In AnimMain okbuttonClick idx =", idx)
        name = self.names[idx]
        try:
            url = self.urls[idx]
        except:
            url = " "
        if name == "Config":
            self.session.open(ConfigEx)

        elif name == "About":
            self.session.open(Abouttvr)

        elif 'Search' in str(name):
            search = True
            print('Search go movie: ', search)
            self.search_text(name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos1':
            print("In AnimMain Going in Videos1")
            try:
                vid1 = nextVideos1(self.session, name, url)
                vid1.startSession()
            except:
                pass
        elif '&page' not in str(url) and self.nextmodule == 'Videos1':
            print('video1 and play next sss  ', self.nextmodule)
            if 'tvseriesId' in str(url):
                try:
                    vid1 = Videos6(self.session, name, url) #atv 6.5
                    vid1.startSession()
                except:
                    pass
            else:
                print('video1 and play next xx : ', self.nextmodule)
                self.session.open(Playstream1, name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos4' :
                print("AnimMain Going in nextVideos4")
                try:
                    vid4 = nextVideos4(self.session, name, url)
                    vid4.startSession()
                except:
                    pass

        # elif 'Film' in str(name) and self.nextmodule == 'Videos4':
        elif 'listMovie' in str(url) and self.nextmodule == 'Videos4':        
            print("AnimMain Going listmovie in Videos4")
            try:
                vid4 = Videos4(self.session, name, url)
                vid4.startSession()
            except:
                pass

        elif 'movieId' in str(url) : # and self.nextmodule == 'Videos4':
            print('AnimMain videos5 moveid')
            try:
                vid5 = Videos5(self.session, name, url)
                vid5.startSession()
            except:
                pass

        elif self.nextmodule == "Play":
            print("In AnimMain Going in Playstream1")
            try:
                desc = " "
                self.session.open(Playstream1, name, url)
            except:
                pass

        elif self.nextmodule == "PlaySeries":
            print("In AnimMain Going in PlaySeries")
            try:
                desc = " "
                vid4 = Videos4(self.session, name, url)
                vid4.startSession()
            except:
                pass
                
        elif self.nextmodule == "Videos2":
            print("In animeMain Going in Videos2 name =", name)
            print("In animeMain Going in Videos2 url =", url)
            print("In AnimMain Going in Nextmodule = ", self.nextmodule)
            try:
                vid2 = Videos2(self.session, name, url)
                vid2.startSession()
            except:
                pass
                
        # elif 'Film' in str(name) and self.nextmodule == "Videos2":
            # print("In animeMain Going in Videos2 name =", name)
            # print("In animeMain Going in Videos2 url =", url)
            # print("In AnimMain Going in Nextmodule = ", self.nextmodule)
            # try:
                # vid2 = Videos2(self.session, name, url)
                # vid2.startSession()
            # except:
                # pass

        # elif 'Live' in str(name) and self.nextmodule == "Videos2":
            # print("In GridMain Going in Videos2 name =", name)
            # print("In GridMain Going in Videos2 url =", url)
            # print("In GridMain Going in Nextmodule =", self.nextmodule)
            # try:
                # vid2 = Videos2(self.session, name, url)
                # vid2.startSession()
            # except:
                # pass 
                
        # elif 'Serie' in str(name) and self.nextmodule == "Videos2":
            # print("In GridMain Going in Videos2 name =", name)
            # print("In GridMain Going in Videos2 url =", url)
            # print("In GridMain Going in Nextmodule =", self.nextmodule)
            # try:
                # vid2 = Videos2(self.session, name, url)
                # vid2.startSession()
            # except:
                # pass      
                
        elif self.nextmodule == "Videos3":
            print("In AnimMain Going in Videos3")
            try:
                vid3 = Videos3(self.session, name, url)
                vid3.startSession()
            except:
                pass

        elif self.nextmodule == "Videos4":
            print("in AnimMain Going in Videos4")
            try:
                vid4 = Videos4(self.session, name, url)
                vid4.startSession()
            except:
                pass

        elif self.nextmodule == "Videos5":
            print("In AnimMain Going in Videos5")
            try:
                vid5 = Videos5(self.session, name, url)
                vid5.startSession()
            except:
                pass
        else:
            self.close()

    def search_text(self, name, url):
        self.namex = name
        self.urlx=url
        self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Filter this category..."), text='')

    def filterChannels(self, result):
        if result:
            name = str(result)
            url = self.urlx + str(result)
            try:
                vid4 = nextVideos4(self.session, name, url)
                vid4.startSession()
            except:
                return
        else:
            self.resetSearch()

    def resetSearch(self):
        global search
        search = False
        return

#-----------------
#menupic
class GridMain(Screen):
    def __init__(self, session, menuTitle, nextmodule, names, urls, infos, pics = []):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        skin = skin_path + 'GridMain.xml'
        with open(skin, 'r') as f:
          self.skin = f.read()
        f.close()
        print("In Gridmain names 1= ", names)
        print("In Gridmain urls 1 = ", urls)
        print("In Gridmain pics 1= ", pics)
        print("In Gridmain nextmodule = ", nextmodule)
        title = menuTitle
        self["title"] = Button(title)
        # tmpfold = config.plugins.tvspro.cachefold.value + "/tvspro/tmp"
        # picfold = config.plugins.tvspro.cachefold.value + "/tvspro/pic"
        # pics = getpics(names, pics, tmpfold, picfold)
        # print("In Gridmain pics = ", pics)
        self.pos = []
        if isFHD():
            self.pos.append([30,24])
            self.pos.append([396,24])
            self.pos.append([764,24])
            self.pos.append([1134,24])
            self.pos.append([1504,24])
            self.pos.append([30,468])
            self.pos.append([396,468])
            self.pos.append([764,468])
            self.pos.append([1134,468])
            self.pos.append([1504,468])
        else:
            self.pos.append([14,5])
            self.pos.append([260,5])
            self.pos.append([504,5])
            self.pos.append([744,5])
            self.pos.append([984,5])
            self.pos.append([14,305])
            self.pos.append([260,305])
            self.pos.append([504,305])
            self.pos.append([744,305])
            self.pos.append([984,305])

        print("self.pos =", self.pos)
        tmpfold = config.plugins.tvspro.cachefold.value + "/tvspro/tmp"
        picfold = config.plugins.tvspro.cachefold.value + "/tvspro/pic"
        pics = getpics(names, pics, tmpfold, picfold)
        print("In Gridmain pics = ", pics)

        self.name = menuTitle
        self.nextmodule = nextmodule

        self.urls = urls
        self.pics = pics
        self.names = names
        self.infos = infos
        self["info"] = Label()

        list = []
        list = names
        self["menu"] = List(list)
        for x in list:
           print("x in list =", x)
        self["frame"] = MovingPixmap()
        i = 0
        while i<16:
              self["label" + str(i+1)] = StaticText()
              self["pixmap" + str(i+1)] = Pixmap()
              i = i+1
        i = 0
        ip = 0
        self.index = 0
        self.ipage = 1
        self.icount = 0
        ln = len(self.names)
        self.npage = int(float(ln/10)) + 1
        print("self.npage =", self.npage)
        # self["actions"] = NumberActionMap(["OkCancelActions", "EPGSelectActions", "MenuActions", "DirectionActions", "NumberActions"],
        self["actions"] = ActionMap(["OkCancelActions", "EPGSelectActions", "MenuActions", "DirectionActions", "NumberActions"],        
            {
                "ok": self.okClicked,
                "epg": self.showIMDB,
                "info": self.showIMDB,
                "cancel": self.cancel,
                "left": self.key_left,
                "right": self.key_right,
                "up": self.key_up,
                "down": self.key_down,
            })

        print("Going in openTest")
        self.onLayoutFinish.append(self.openTest)

    def cancel(self):
        self.close()

    def exit(self):
       self.close()

    def showIMDB(self):
        itype = self.index
        name = self.names[itype]
        text_clear = name
        if is_tmdb:
            try:
                from Plugins.Extensions.tmdb import tmdb
                text = charRemove(text_clear)
                _session.open(tmdb.tmdbScreen, text, 0)
            except Exception as e:
                print("[XCF] Tmdb: ", e)
        elif is_imdb:
            try:
                from Plugins.Extensions.IMDb.plugin import main as imdb
                text = charRemove(text_clear)
                imdb(_session, text)
            except Exception as e:
                print("[XCF] imdb: ", e)
        else:
            inf = self.index
            if inf != None or inf != -1:
                text_clear = self.infos[inf]
            else:
                text_clear = name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def paintFrame(self):
        print("In paintFrame self.index, self.minentry, self.maxentry =", self.index, self.minentry, self.maxentry)
        print("In paintFrame self.ipage = ", self.ipage)
        ifr = self.index - (10*(self.ipage-1))
        print("ifr =", ifr)
        ipos = self.pos[ifr]
        print("ipos =", ipos)
        inf = self.index
        if inf != None or inf != -1:
            self["info"].setText(self.infos[inf])
            print('infos: ', inf)
        self["frame"].moveTo( ipos[0], ipos[1], 1)
        self["frame"].startMoving()

    def openTest(self):
        print("self.index, openTest self.ipage, self.npage =", self.index, self.ipage, self.npage)
        if self.ipage < self.npage:
            self.maxentry = (10*self.ipage)-1
            self.minentry = (self.ipage-1)*10
            print("self.ipage , self.minentry, self.maxentry =", self.ipage, self.minentry, self.maxentry)

        elif self.ipage == self.npage:
            print("self.ipage , len(self.pics) =", self.ipage, len(self.pics))
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage-1)*10
            print("self.ipage , self.minentry, self.maxentry B=", self.ipage, self.minentry, self.maxentry)
            i1 = 0
            blpic = dblank
            while i1 < 12:
                self["label" + str(i1+1)].setText(" ")
                self["pixmap" + str(i1+1)].instance.setPixmapFromFile(blpic)
                i1 = i1+1
        print("len(self.pics) , self.minentry, self.maxentry =", len(self.pics) , self.minentry, self.maxentry)
        self.npics = len(self.pics)
        i = 0
        i1 = 0
        self.picnum = 0
        print("doing pixmap")
        ln = self.maxentry - (self.minentry-1)
        while i < ln:
            idx = self.minentry + i
            print("i, idx =", i, idx)
            print("self.names[idx] B=", self.names[idx])
            self["label" + str(i+1)].setText(self.names[idx])
            print("idx, self.pics[idx]", idx, self.pics[idx])
            pic = self.pics[idx]
            print("pic =", pic)
            if os.path.exists(pic):
                print("pic path exists")
            else:
                print("pic path exists not")
            picd = defpic
            try:
                self["pixmap" + str(i+1)].instance.setPixmapFromFile(pic) #ok
            except:
                self["pixmap" + str(i+1)].instance.setPixmapFromFile(picd)
            i = i+1
        self.index = self.minentry
        print("self.minentry, self.index =", self.minentry, self.index)
        self.paintFrame()

    def key_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.maxentry
        self.paintFrame()

    def key_right(self):
        i = self.npics - 1
        if self.index == i:
            self.index = 0
            self.ipage = 1
            self.openTest()
        self.index += 1
        if self.index > self.maxentry:
            self.index = 0
        self.paintFrame()

    def key_up(self):
        print("keyup self.index, self.minentry = ", self.index, self.minentry)
        self.index = self.index - 5
        print("keyup self.index, self.minentry 2 = ", self.index, self.minentry)
        print("keyup self.ipage = ", self.ipage)
        if self.index < (self.minentry):
            if self.ipage > 1:
                self.ipage = self.ipage - 1
                self.openTest()
            elif self.ipage == 1:
                return
            else:
               self.paintFrame()
        else:
           self.paintFrame()

    def key_down(self):
        print("keydown self.index, self.maxentry = ", self.index, self.maxentry)
        self.index = self.index + 5
        print("keydown self.index, self.maxentry 2= ", self.index, self.maxentry)
        print("keydown self.ipage = ", self.ipage)
        if self.index > (self.maxentry):
            if self.ipage < self.npage:
                self.ipage = self.ipage + 1
                self.openTest()
            elif self.ipage == self.npage:
                self.index = 0
                self.ipage = 1
                self.openTest()
            else:
                print("keydown self.index, self.maxentry 3= ", self.index, self.maxentry)
                self.paintFrame()
        else:
            self.paintFrame()

    def okClicked(self):
        itype = self.index
        url = self.urls[itype]
        name = self.names[itype]
        print("In GridMain name =", name)
        print("In GridMain self.nextmodule =", self.nextmodule)

        if name == "Config":
            self.session.open(ConfigEx)

        elif name == "About":
            self.session.open(Abouttvr)

        elif 'Search' in str(name):
            search = True
            print('Search go movie: ', search)
            self.search_text(name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos1':
            print("In GridMain Going in Videos1")
            try:
                vid1 = nextVideos1(self.session, name, url)
                vid1.startSession()
            except:
                pass
        elif '&page' not in str(url) and self.nextmodule == 'Videos1':
            print('In GridMain video1 and play next sss  ', self.nextmodule)
            if 'tvseriesId' in str(url):
                try:
                    vid1 = Videos6(self.session, name, url) #atv 6.5
                    vid1.startSession()
                except:
                    pass
            else:
                print('In GridMain video1 and play next xx : ', self.nextmodule)
                self.session.open(Playstream1, name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos4' :
                print("In GridMain Going in nextVideos4")
                try:
                    vid4 = nextVideos4(self.session, name, url)
                    vid4.startSession()
                except:
                    pass

        # elif 'Film' in str(name) and self.nextmodule == 'Videos4':
        elif 'listMovie' in str(url) and self.nextmodule == 'Videos4':        
            print("In GridMain Going listmovie in Videos4")
            try:
                vid4 = Videos4(self.session, name, url)
                vid4.startSession()
            except:
                pass

        elif 'movieId' in str(url) : # and self.nextmodule == 'Videos4':
            print('In GridMain videos5 moveid')
            try:
                vid5 = Videos5(self.session, name, url)
                vid5.startSession()
            except:
                pass

        elif self.nextmodule == "Play":
            print("In GridMain Going in Playstream1")
            try:
                desc = " "
                self.session.open(Playstream1, name, url)
            except:
                pass

        elif self.nextmodule == "PlaySeries":
            print("In GridMain Going in PlaySeries")
            try:
                desc = " "
                vid4 = Videos4(self.session, name, url)
                vid4.startSession()
            except:
                pass

        elif self.nextmodule == "Videos2":
            print("In animeMain Going in Videos2 name =", name)
            print("In animeMain Going in Videos2 url =", url)
            print("In AnimMain Going in Nextmodule = ", self.nextmodule)
            try:
                vid2 = Videos2(self.session, name, url)
                vid2.startSession()
            except:
                pass

        # elif 'Film' in str(name) and self.nextmodule == "Videos2":
            # print("In GridMain Going in Videos2 name =", name)
            # print("In GridMain Going in Videos2 url =", url)
            # print("In GridMain Going in Nextmodule =", self.nextmodule)
            # try:
                # vid2 = Videos2(self.session, name, url)
                # vid2.startSession()
            # except:
                # pass
                
        # elif 'Live' in str(name) and self.nextmodule == "Videos2":
            # print("In GridMain Going in Videos2 name =", name)
            # print("In GridMain Going in Videos2 url =", url)
            # print("In GridMain Going in Nextmodule =", self.nextmodule)
            # try:
                # vid2 = Videos2(self.session, name, url)
                # vid2.startSession()
            # except:
                # pass          
                
        # elif 'Serie' in str(name) and self.nextmodule == "Videos2":
            # print("In GridMain Going in Videos2 name =", name)
            # print("In GridMain Going in Videos2 url =", url)
            # print("In GridMain Going in Nextmodule =", self.nextmodule)
            # try:
                # vid2 = Videos2(self.session, name, url)
                # vid2.startSession()
            # except:
                # pass                

        elif self.nextmodule == "Videos3":
            print("In GridMain Going in Videos3")
            try:
                vid3 = Videos3(self.session, name, url)
                vid3.startSession()
            except:
                pass

        elif self.nextmodule == "Videos4":
            print("In GridMain Going in Videos4")
            try:
                vid4 = Videos4(self.session, name, url)
                vid4.startSession()
            except:
                pass

        elif self.nextmodule == "Videos5":
            print("In GridMain Going in Videos5")
            try:
                vid5 = Videos5(self.session, name, url)
                vid5.startSession()
            except:
                pass
        else:
            self.close()

    def search_text(self, name, url):
        self.namex = name
        self.urlx=url
        self.session.openWithCallback(self.filterChannels, VirtualKeyBoard, title=_("Filter this category..."), text=name)

    def filterChannels(self, result):
        if result:
            name = str(result)
            url = self.urlx + str(result)
            try:
                vid4 = nextVideos4(self.session, name, url)
                vid4.startSession()
            except:
                return
        else:
            self.resetSearch()

    def resetSearch(self):
        global search
        search = False
        return

#-----------------
#main exe
class tvspromain(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        title = _(name_plug)
        self["title"] = Button(title)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Exit"))
        self["key_green"] = Button(_("Select"))
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        global SREF
        SREF = self.srefOld
        self.onLayoutFinish.append(self.startSession)
#       self.onClose.append(self.__onClose)

    def startSession(self):
        self.names = []
        self.urls = []
        self.infos = []
        self.names.append("About")
        self.names.append("Config")
        self.names.append("Live TV")
        self.names.append("Film")
        self.names.append("Serie")
        self.names.append("Search")
        self.urls.append(" ")
        self.urls.append(" ")
        self.urls.append("https://tivustream.website/urls/e2live")
        self.urls.append("https://tivustream.website/urls/e2movie")
        self.urls.append("https://tivustream.website/urls/e2series")
        self.urls.append("https://tivustream.website/php_filter/kodi19/kodi19.php?mode=movie&query=")
        self.infos.append("")
        self.infos.append("Information Us")
        self.infos.append("Setup Plugin")
        self.infos.append("Live TV Stream")
        self.infos.append("Film and Movie")
        self.infos.append("Series")
        self.infos.append("Search your Movie")
        self.session.open(AnimMain, name_plug, "Videos2", self.names, self.urls, self.infos, pics = [])

    def okClicked(self):
            pass

    def config(self):
            self.session.open(ConfigEx)

    def cancel(self):
            self.session.nav.playService(SREF)
            self.close()

class Videos2(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        global nextmodule
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("Videos2 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<100:
            try:
                print('In Videos2 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In Videos2 name =", name)
                url = (y["items"][i]["externallink"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        title = name_plug
        print('self.name is : ', self.name)
        # if str(self.name) == "Live":
            # nextmodule = "Videos3"
        # if str(self.name) == "Film":
            # nextmodule = "Videos4"
        # if str(self.name) == "Serie":
            # nextmodule = "Videos1"
        if "Live" in self.name:
            nextmodule = "Videos3"
        if "Film" in self.name:
            nextmodule = "Videos4"
        if "Serie" in self.name:
            nextmodule = "Videos1"
        print("In Videos2 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos2 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
        pass

class Videos6(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        title = name_plug
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("Videos1 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<100:
            try:
                print('In Videos6 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In Videos6 name =", name)
                try:
                    url = (y["items"][i]["link"])
                except:
                    url = (y["items"][i]["yatse"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        # nextmodule = "Play"
        nextmodule = "Videos1"
        print("In Videos6 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos6 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
        pass

class Videos1(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("Videos1 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<100:
            try:
                print('In getVideos y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In Videos1 name =", name)
                try:
                    url = (y["items"][i]["link"])
                except:
                    url = (y["items"][i]["yatse"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        title = name_plug
        # nextmodule = "Play"
        nextmodule = "Videos1"
        print("In Videos1 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos1 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
        pass

class nextVideos1(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("nextVideos1 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<100:
            try:
                print('In nextVideos1 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In nextVideos1 name =", name)
                try:
                    url = (y["items"][i]["link"])
                except:
                    url = (y["items"][i]["yatse"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        title = name_plug
        # nextmodule = "Play"
        nextmodule = "Videos1"
        print("In nextVideos1 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        if config.plugins.tvspro.thumb.value == "True":
            print("In nextVideos1 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
        pass

class Videos3(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        global SREF
        SREF = self.srefOld
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("Videos3 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<100:
            try:
                print('In Videos3 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In Videos3 name =", name)
                try:
                    url = (y["items"][i]["link"])
                except:
                    url = (y["items"][i]["yatse"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                pic = pic.replace("\\", "")
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        title = name_plug
        nextmodule = "Play"
        print("In Videos3 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        print("In Videos3 nextmodule =", nextmodule)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos3 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
        pass

class Videos4(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        global SREF
        SREF = self.srefOld
        self.onLayoutFinish.append(self.startSession)
#       self.onClose.append(self.__onClose)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("Videos4 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<100:
            try:
                print('In Videos4 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In Videos4 name =", name)
                url = (y["items"][i]["externallink"])
                url = url.replace("\\", "")
                print("In Videos4 url =", url)
                pic = (y["items"][i]["thumbnail"])
                pic = pic.replace("\\", "")
                print("In Videos4 pic =", pic)
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        title = name_plug
        nextmodule = "Videos5"
        print("In Videos4 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        print("In Videos4 nextmodule =", nextmodule)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos4 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
        pass

class nextVideos4(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        global SREF
        SREF = self.srefOld
        self.onLayoutFinish.append(self.startSession)
#       self.onClose.append(self.__onClose)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("nextVideos4 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<100:
            try:
                print('In nextVideos4 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In nextVideos4 name =", name)
                try:
                    url = (y["items"][i]["externallink"])
                except:
                    url = (y["items"][i]["link"])
                url = url.replace("\\", "")
                print("In nextVideos4 url =", url)
                pic = (y["items"][i]["thumbnail"])
                pic = pic.replace("\\", "")
                print("In nextVideos4 pic =", pic)
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        title = name_plug
        nextmodule = "Videos4"
        print("In nextVideos4 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        print("In nextVideos4 nextmodule =", nextmodule)
        if config.plugins.tvspro.thumb.value == "True":
            print("In nextVideos4 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
           pass

class Videos5(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,
            "back": self.close,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.name = name
        self.url = url
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        global SREF
        SREF = self.srefOld
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        print("Videos5 url =", url)
        content = ReadUrl2(url)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i<1:
            try:
                print('In Videos5 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                try:
                    url = (y["items"][i]["link"])
                except:
                    url = (y["items"][i]["yatse"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                pic = pic.replace("\\", "")
                info = (y["items"][i]["info"])
                info = info.replace("\r\n","")
                self.names.append(checkStr(name))
                self.urls.append(checkStr(url))
                self.pics.append(checkStr(pic))
                self.infos.append(checkStr(info))
                i = i+1
            except:
                break
        title = name_plug
        nextmodule = "Play"
        print("In Videos5 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        print("In Videos5 nextmodule =", nextmodule)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos5 Going in GridMain")
            self.session.open(GridMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)
        else:
            self.session.open(AnimMain, title, nextmodule, self.names, self.urls, self.infos, pics = self.pics)

    def okClicked(self):
        pass

class Abouttvr(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session #edit
        skin = skin_path + 'Abouttvr.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        f.close()
        title = _(name_plug)
        self["title"] = Button(title)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Back"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
        # self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],        
        {
            "ok": self.okClicked,

            "back": self.close,
            "cancel": self.cancel,
            "red": self.close,
            "green": self.okClicked,
        }, -1)
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        try:
            self['info'].setText(self.getinfo())
        except:
            self['info'].setText(_('\n\n' + 'Error downloading Info!'))

    def okClicked(self):
        Screen.close(self, False)

    def getinfo(self):
        continfo = _("==  WELCOME to WWW.TIVUSTREAM.COM ==\n")
        continfo += _("== SUPPORT ON: WWW.CORVOBOYS.COM http://t.me/tivustream ==\n")
        continfo += _("== thank's to @PCD and LINUXSAT-SUPPORT.COM\n")
        continfo += _("========================================\n")
        continfo += _("NOTA BENE:\n")
        continfo += _("Le liste create ad HOC contengono indirizzi liberamente e gratuitamente\n")
        continfo += _("trovati in rete e non protetti da sottoscrizione o abbonamento.\n")
        continfo += _("Il server di riferimento strutturale ai progetti rilasciati\n")
        continfo += _("non e' fonte di alcun stream/flusso.\n")
        continfo += _("Assolutamente VIETATO utilizzare queste liste senza autorizzazione.\n")
        continfo += _("========================================\n")
        continfo += _("DISCLAIMER:\n")
        continfo += _("The lists created at HOC contain addresses freely and freely found on\n")
        continfo += _("the net and not protected by subscription or subscription.\n")
        continfo += _("The structural reference server for projects released\n")
        continfo += _("is not a source of any stream/flow.\n")
        continfo += _("Absolutely PROHIBITED to use this lists without authorization\n")
        continfo += _("========================================\n")
        return continfo

    def keyLeft(self):
        self['list'].left()

    def keyRight(self):
        self['list'].right()

    def keyNumberGlobal(self, number):
        self['text'].number(number)

    def cancel(self):
        if os.path.exists("/tmp/hls.avi"):
            os.remove("/tmp/hls.avi")
        Screen.close(self, False)

class Playstream1(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        skin = skin_path + 'Playstream1.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        print('self.skin: ', skin)
        f.close()
        self.setup_title = ('Select Player Stream')
        self.list = []
        self['list'] = rvList([])
        self['info'] = Label()
        self['info'].setText(name)
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Select'))
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self.downloading = False
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'TimerEditActions', 'InfobarInstantRecord'], {'red': self.cancel,
         'green': self.okClicked,
         'back': self.cancel,
         'cancel': self.cancel,
         "rec": self.runRec,
         "instantRecord": self.runRec,
         "ShortRecord": self.runRec,
         'ok': self.okClicked}, -2)
        self.name1 = name
        self.url = url
        print('In Playstream1 self.url =', url)
        global srefInit
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        srefInit = self.initialservice
        self.onLayoutFinish.append(self.openTest)
        return

    def runRec(self):
        self.namem3u = self.name1
        self.urlm3u = self.url
        if self.downloading == True:
            self.session.open(MessageBox, _('You are already downloading!!!'), MessageBox.TYPE_INFO, timeout=5)
            return
        else:
            if '.mp4' or '.mkv' or '.flv' or '.avi' in self.urlm3u: # or 'm3u8':
                self.session.openWithCallback(self.download_m3u, MessageBox, _("DOWNLOAD VIDEO?\n%s" %self.namem3u ) , type=MessageBox.TYPE_YESNO, timeout = 10, default = False)
            else:
                self.downloading = False
                self.session.open(MessageBox, _('Only VOD Movie allowed or not .ext Filtered!!!'), MessageBox.TYPE_INFO, timeout=5)

    def download_m3u(self, result):
        if result:
            if not 'm3u8' in self.urlm3u:
                path = urlparse(self.urlm3u).path
                ext = '.mp4'
                ext = splitext(path)[1]
                if ext != '.mp4' or ext != '.mkv' or ext != '.avi' or ext != '.flv': # or ext != 'm3u8':
                    ext = '.mp4'
                fileTitle = re.sub(r'[\<\>\:\"\/\\\|\?\*\[\]]', '_', self.namem3u)
                fileTitle = re.sub(r' ', '_', fileTitle)
                fileTitle = re.sub(r'_+', '_', fileTitle)
                fileTitle = fileTitle.replace("(", "_").replace(")", "_").replace("#", "").replace("+", "_").replace("\'", "_").replace("'", "_").replace("!", "_").replace("&", "_")
                fileTitle = fileTitle.lower() + ext
                self.in_tmp = Path_Movies + fileTitle
                self.downloading = True
                self.download = downloadWithProgress(self.urlm3u, self.in_tmp)
                self.download.addProgress(self.downloadProgress)
                self.download.start().addCallback(self.check).addErrback(self.showError)
            else:
                self.downloading = False
                self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)
        else:
            self.downloading = False

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

    def check(self, fplug):
        checkfile = self.in_tmp
        if os.path.exists(checkfile):
            self.downloading = False
            self['progresstext'].text = ''
            self.progclear = 0
            self['progress'].setValue(self.progclear)
            self["progress"].hide()

    def showError(self, error):
        self.downloading = False
        self.session.open(MessageBox, _('Download Failed!!!'), MessageBox.TYPE_INFO, timeout=5)

    def openTest(self):
        url = self.url
        self.names = []
        self.urls = []
        self.names.append('Play Now')
        self.urls.append(checkStr(url))        
        self.names.append('Download Now')
        self.urls.append(checkStr(url))
        self.names.append('Play HLS')
        self.urls.append(checkStr(url))
        self.names.append('Play TS')
        self.urls.append(checkStr(url))
        self.names.append('Streamlink')
        self.urls.append(checkStr(url))
        showlist(self.names, self['list'])

    def okClicked(self):
        idx = self['list'].getSelectionIndex()
        if idx != None or idx != -1:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            # if "youtube" in str(self.url):
                # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
                # return
            if "youtube" in str(self.url):
                desc = self.name
                try:
                    # from youtube_dl import YoutubeDL
                    from Plugins.Extensions.tvspro.youtube_dl import YoutubeDL
                    '''
                    ydl_opts = {'format': 'best'}
                    ydl_opts = {'format': 'bestaudio/best'}
                    '''
                    ydl_opts = {'format': 'best'}
                    ydl = YoutubeDL(ydl_opts)
                    ydl.add_default_info_extractors()
                    result = ydl.extract_info(self.url, download=False)
                    self.url = result["url"]
                except:
                    pass
                self.session.open(Playstream2, self.name, self.url, desc)

            if idx == 1:
                # self.name = self.names[idx]
                self.url = self.urls[idx]
                print('In playVideo url D=', self.url)
                self.runRec()
                # return

            if idx == 0:
                self.name = self.names[idx]
                self.url = self.urls[idx]
                print('In playVideo url D=', self.url)
                self.play()
            elif idx == 2:
                print('In playVideo url B=', self.url)
                self.name = self.names[idx]
                self.url = self.urls[idx]
                try:
                    os.remove('/tmp/hls.avi')
                except:
                    pass
                header = ''
                cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/tvspro/lib/hlsclient.py" "' + self.url + '" "1" "' + header + '" + &'
                print('In playVideo cmd =', cmd)
                os.system(cmd)
                os.system('sleep 3')
                self.url = '/tmp/hls.avi'
                self.play()
            elif idx == 3:
                print('In playVideo url A=', self.url)
                url = self.url
                try:
                    os.remove('/tmp/hls.avi')
                except:
                    pass
                cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/tvspro/l/tsclient.py" "' + url + '" "1" + &'
                print('hls cmd = ', cmd)
                os.system(cmd)
                os.system('sleep 3')
                self.url = '/tmp/hls.avi'
                self.name = self.names[idx]
                self.play()
            else:
                if idx == 4:
                    self.name = self.names[idx]
                    self.url = self.urls[idx]
                    print('In playVideo url D=', self.url)
                    self.play2()
            # else:
                # self.name = self.names[idx]
                # self.url = self.urls[idx]
                # print('In playVideo url D=', self.url)
                # self.play()
            return

    def playfile(self, serverint):
        self.serverList[serverint].play(self.session, self.url, self.name)

    def play(self):
        desc = self.name
        url = self.url
        name = self.name1
        self.session.open(Playstream2, name, url, desc)
        self.close()

    def play2(self):
        if isStreamlinkAvailable():
            desc = self.name
            name = self.name1
            # if os.path.exists("/usr/sbin/streamlinksrv"):
            url = self.url
            url = url.replace(':', '%3a')
            print('In revolution url =', url)
            ref = '5002:0:1:0:0:0:0:0:0:0:' + 'http%3a//127.0.0.1%3a8088/' + str(url)
            # ref = '4097:0:1:0:0:0:0:0:0:0:' + url
            sref = eServiceReference(ref)
            print('SREF: ', sref)
            sref.setName(self.name1)
            self.session.open(Playstream2, name, sref, desc)
            self.close()
        else:
            self.session.open(MessageBox, _('Install Streamlink first'), MessageBox.TYPE_INFO, timeout=5)

    def cancel(self):
        try:
            password_mgr = HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, self.hostaddr, '', 'Admin')
            handler = HTTPBasicAuthHandler(password_mgr)
            opener = build_opener(handler)
            f = opener.open(self.hostaddr + '/requests/status.xml?command=pl_stop')
            f = opener.open(self.hostaddr + '/requests/status.xml?command=pl_empty')
        except:
            pass
        self.session.nav.stopService()
        self.session.nav.playService(srefInit)
        self.close()

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

    def serviceStarted(self):
        if self.execing:
            if config.usage.show_infobar_on_zap.value:
                self.doShow()

    def __onShow(self):
        self.__state = self.STATE_SHOWN
        self.startHideTimer()

    def startHideTimer(self):
        if self.__state == self.STATE_SHOWN and not self.__locked:
            idx = config.usage.infobar_timeout.index
            if idx:
                self.hideTimer.start(idx * 1500, True)

    def __onHide(self):
        self.__state = self.STATE_HIDDEN

    def doShow(self):
        self.hideTimer.stop()
        self.show()
        self.startHideTimer()

    def doTimerHide(self):
        self.hideTimer.stop()
        if self.__state == self.STATE_SHOWN:
            self.hide()

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

class Playstream2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarAudioSelection, TvInfoBarShowHide,InfoBarSubtitleSupport):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 4000
    def __init__(self, session, name, url, desc):
        global SREF, streaml
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.skinName = 'MoviePlayer'
        title = name
        streaml = False
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarAudioSelection.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
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
         'info': self.showinfo,
         # 'info': self.cicleStreamType,
         'tv': self.cicleStreamType,
         'stop': self.leavePlayer,
         'cancel': self.cancel,
         'back': self.cancel}, -1)
        self.allowPiP = False
        self.service = None
        service = None
        InfoBarSeek.__init__(self, actionmap='InfobarSeekActions')
        self.icount = 0
        self.desc = desc
        # self.pcip = 'None'
        self.url = url
        self.name = decodeHtml(name)
        self.state = self.STATE_PLAYING
        SREF= self.session.nav.getCurrentlyPlayingServiceReference()
        # self.onLayoutFinish.append(self.cicleStreamType)
        # self.onClose.append(self.cancel)
		# self.onClose.append(self.__onClose)
        if '8088' in str(self.url):
            # self.onLayoutFinish.append(self.slinkPlay)
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            # self.onLayoutFinish.append(self.cicleStreamType)
            self.onFirstExecBegin.append(self.cicleStreamType)
        self.onClose.append(self.cancel)
        # return

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
            message = 'stitle:' + str(sTitle) + '\n' + 'sServiceref:' + str(sServiceref) + '\n' + 'sTagCodec:' + str(sTagCodec) + '\n' + 'sTagVideoCodec:' + str(sTagVideoCodec) + '\n' + 'sTagAudioCodec :' + str(sTagAudioCodec)
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
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists(IMDb):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)
        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def slinkPlay(self, url):
        name = self.name
        ref = "{0}:{1}".format(url.replace(":", "%3A"), name.replace(":", "%3A"))
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openPlay(self, servicetype, url):
        name = self.name
        ref = "{0}:0:0:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3A"), name.replace(":", "%3A"))
        print('reference:   ', ref)
        if streaml == True:
            url = 'http://127.0.0.1:8088/' + str(url)
            ref = "{0}:0:1:0:0:0:0:0:0:0:{1}:{2}".format(servicetype, url.replace(":", "%3A"), name.replace(":", "%3A"))
            print('streaml reference:   ', ref)
        print('final reference:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        global streml
        streaml = False
        from itertools import cycle, islice
        self.servicetype = str(config.plugins.tvspro.services.value)# +':0:1:0:0:0:0:0:0:0:'#  '4097'
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

def main(session, **kwargs):
    try:
        from Plugins.Extensions.tvspro.lib.Update import upd_done
        upd_done()
    except:
        pass
    _session = session
    os.system("mkdir -p " + config.plugins.tvspro.cachefold.value + "/tvspro")
    os.system("mkdir -p " + config.plugins.tvspro.cachefold.value + "/tvspro/vid")
    os.system("mkdir -p " + config.plugins.tvspro.cachefold.value + "/tvspro/pic")
    os.system("mkdir -p " + config.plugins.tvspro.cachefold.value + "/tvspro/tmp")
    exo = tvspromain(_session)
    exo.startSession()

def Plugins(**kwargs):
    icona = 'icon.png'
    extDescriptor = PluginDescriptor(name=name_plug, description=_(title_plug), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon=icona, fnc=main)
    result = [PluginDescriptor(name=name_plug, description=_(title_plug), where=[PluginDescriptor.WHERE_PLUGINMENU], icon=icona, fnc=main)]
    result.append(extDescriptor)
    return result
