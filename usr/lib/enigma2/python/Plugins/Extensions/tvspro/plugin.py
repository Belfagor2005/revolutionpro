# -*- coding: utf-8 -*-
#!/usr/bin/python
'''
Info http://t.me/tivustream
****************************************
*        coded by Lululla              *
*           thank's Pcd                *
*             12/05/2021               *
****************************************
'''
from __future__ import print_function
try:
       from Plugins.Extensions.SubsSupport import SubsSupport, initSubsSettings
       from Plugins.Extensions.tvspro.lib.Utils2 import *
except:
       from Plugins.Extensions.tvspro.lib.Utils import *
from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Pixmap import Pixmap, MultiPixmap
from Components.ServiceEventTracker import ServiceEventTracker, InfoBarBase
from Components.Sources.List import List
from Components.Sources.Source import Source
from Components.Sources.StaticText import StaticText
from Components.config import ConfigSubsection, config, configfile, ConfigText, ConfigDirectory, ConfigSelection,ConfigYesNo,ConfigEnableDisable
from Screens.InfoBarGenerics import InfoBarSeek, InfoBarAudioSelection, InfoBarNotifications, InfoBarMenu, InfoBarSubtitleSupport
from Screens.LocationBox import LocationBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import SCOPE_PLUGINS
from Tools.Directories import resolveFilename, fileExists, copyfile, pathExists
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from enigma import ePixmap
from enigma import eSize, eListbox, eListboxPythonMultiContent, iServiceInformation, eServiceReference
from enigma import getDesktop, gFont
from enigma import loadPNG, loadJPG
from os.path import splitext
from twisted.web.client import downloadPage
import glob
import json
import six
import sys
# import urllib2
# from Tools.LoadPixmap import LoadPixmap
PY3 = sys.version_info[0] == 3
if PY3:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
    from urllib.parse import urlparse, urlencode, quote
else:
    from urllib2 import urlopen, Request, URLError, HTTPError
    from urlparse import urlparse
    from urllib import urlencode, quote

print('Py3: ',PY3)

THISPLUG = '/usr/lib/enigma2/python/Plugins/Extensions/tvspro/'
DESKHEIGHT = getDesktop(0).size().height()
HD = getDesktop(0).size()

def getversioninfo():
    currversion = '1.0'
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
currversion = getversioninfo()
Version = currversion + ' - 15.05.2021'
title_plug = '..:: TivuStream Pro Revolution V. %s ::..' % Version
name_plug = 'TivuStream Pro Revolution'
res_plugin_path = THISPLUG + 'res/'
skin_path = THISPLUG
# Credits = 'Info http://t.me/tivustream'
# Credits2 = 'Maintener @Lululla @Pcd'
# dir_enigma2 = '/etc/enigma2/'
# service_types_tv = '1:7:1:0:0:0:0:0:0:0:(type == 1) || (type == 17) || (type == 22) || (type == 25) || (type == 134) || (type == 195)'
SREF = ""

def checkStr(txt):
    if PY3:
        if isinstance(txt, type(bytes())):
            txt = txt.decode('utf-8')
    else:
        if isinstance(txt, type(six.text_type())):
            txt = txt.encode('utf-8')
    return txt
######
global defpic, dblank

eDreamOS = False
try:
    from enigma import eMediaDatabase
    eDreamOS = True
except:
    eDreamOS = False

if HD.width() > 1280:
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

def getUrl(url):
    print("Here in client2 getUrl url =", url)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urlopen(req)
    link=response.read()
    response.close()
    print("Here in client2 link =", link)
    return link

# def getUrl(url):
    # return[]
    # try:
        # import requests
        # link = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0'}).text
        # return link
    # except ImportError:
        # req = Request(url)
        # req.add_header('User-Agent', 'TVS')
        # response = urlopen(req, None, 3)
        # link = response.read()
        # response.close()
        # return link
    # except:
        # return
    # return

def getUrl2(url, referer):
    # if PY3 == 3:
        # # url = url.encode()
        # url = six.binary_type(url,encoding="utf-8")
    print("Here in client2 getUrl2 url =", url)
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer', referer)
    response = urlopen(req)
    link=response.read()
    response.close()
    return link
    # return checkStr(link)

#config
mdchoice = [
            ("4097", _("IPTV(4097)")),
            ("1", _("Dvb(1)")),
            ("8193", _("eServiceUri(8193)")),
            ]

if os.path.exists("/usr/bin/gstplayer"):
    mdchoice.append(("5001", _("Gstreamer(5001)")))
if os.path.exists("/usr/bin/exteplayer3"):
    mdchoice.append(("5002", _("Exteplayer3(5002)")))
config.plugins.tvspro = ConfigSubsection()
config.plugins.tvspro.services = ConfigSelection(default='4097', choices=mdchoice)
config.plugins.tvspro.cachefold = ConfigDirectory("/media/hdd", False)
config.plugins.tvspro.thumb = ConfigSelection(default = "True", choices = [("True", _("yes")),("False", _("no"))])
cfg = config.plugins.tvspro

class ConfigEx(Screen, ConfigListScreen):

    def __init__(self, session):
        if eDreamOS:
            skin = skin_path + 'ConfigOs.xml'
        else:
            skin = skin_path + 'Config.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
            f.close()
        Screen.__init__(self, session)
        self.setup_title = _("SETUP PLUGIN")
        self.onChangedEntry = [ ]
        self.session = session
        # self['title'] = Label(_('Setup Plugin'))
        self["status"] = Label()
        self["statusbar"] = Label()
        self['key_red'] = Label('Exit')
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
        if callback is not None and len(callback):
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
        self.list.append(getConfigListEntry(_("Cache folder"), cfg.cachefold,_("Configure Folder Cache Path (eg.: /media/hdd), Enigma restart required")))
        self.list.append(getConfigListEntry(_("Show thumbpic ?"), cfg.thumb,_("Show Thumbpics ? Enigma restart required")))
        self['config'].list = self.list
        self["config"].setList(self.list)
        self.setInfo()

    def setInfo(self):
        entry = str(self.getCurrentEntry())
        if entry == _('Services Player Reference type'):
            self['description'].setText(_("Configure Service Player Reference, Enigma restart required"))
            return
        if entry == _('Cache folder'):
            self['description'].setText(_("Configure Folder Cache Path (eg.: /media/hdd), Enigma restart required"))
            return
        if entry == _('Skin resolution-(restart e2 after change)'):
            self['description'].setText(_("Configure Skin Resolution Screen, Enigma restart required"))
            return
        if entry == _('Show thumbpic ?'):
            self['description'].setText(_("Show Thumbpics ? Enigma restart required"))
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
        if path is not None:
            if self.setting == 'cachefold':
                config.plugins.tvspro.cachefold.setValue(path)
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
    if HD.width() > 1280:
        nw = 300
    else:
        nw = 200
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
            name = name.replace("&", "")
            name = name.replace(":", "")
            name = name.replace("(", "-")
            name = name.replace(")", "")
            name = name.replace(" ", "")
            name = name.replace("'", "")
            name = name.replace("/", "-")
        except:
            pass
        url = pics[j]
        if url is None:
            url = ""
        url = url.replace(" ", "%20")
        url = url.replace("ExQ", "=")
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
        if not fileExists(picf):
            if THISPLUG in url:
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
                        p = getUrl2(url1, referer)
                        #-----------------
                        f1=open(tpicf,"wb")
                        f1.write(p)
                        f1.close()
                    else:
                        print("Going in urlopen url =", url)
                        p = getUrl(url)
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
        try:
            if eDreamOS == False:
                try:
                    import Image
                except:
                    from PIL import Image
                im = Image.open(tpicf)
                # imode = im.mode
                # if im.mode == "JPEG":
                    # im.save("xxx.jpg")
                    # in most case, resulting jpg file is resized small one
                # if imode.mode in ["RGBA", "P"]:
                    # imode = imode.convert("RGB")
                    # rgb_im.save("xxx.jpg")
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
                # im.save(tpicf)
##########################
        except:
            tpicf = defpic
        pix.append(j)
        pix[j] = picf
        j = j+1
    cmd1 = "cp " + tmpfold + "/* " + picfold + " && rm " + tmpfold + "/* &"
    print("In getpics final cmd1=", cmd1)
    os.system(cmd1)
    return pix
#-----------------

#menulist
class AnimMain(Screen):

    def __init__(self, session, menuTitle, nextmodule, names, urls, infos, pics = []):
        Screen.__init__(self, session)
        self.session = session
        skin = skin_path + 'AnimMain.xml'
        with open(skin, 'r') as f:
          self.skin = f.read()
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
        self["actions"] = NumberActionMap(["OkCancelActions", "EPGSelectActions", "MenuActions", "DirectionActions", "NumberActions", "ColorActions"],
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
        if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/TMBD/plugin.pyo"):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo"):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)
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
        # infos epg no work on play movie last click ok  !!! mistery!
        # inf = self.index
        # self["info"].setText(self.infos[inf])
        
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
        if HD.width() > 1280:
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
        ##print "menu keyNumber:", number
        # Calculate index
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
        """
        selection = self.tlist[idx]
        print "selection =", selection
        if selection is not None:
            selection[1]()
        """
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
                vid2 = nextVideos1(self.session, name, url)
                vid2.startSession()
            except:
                pass
        elif '&page' not in str(url) and self.nextmodule == 'Videos1':
            print('video1 and play next sss  ', self.nextmodule)
            if 'tvseriesId' in str(url):
                try:
                    vid2 = Videos6(self.session, name, url) #atv 6.5
                    vid2.startSession()
                except:
                    pass
            else:
                print('video1 and play next xx : ', self.nextmodule)
                self.session.open(Playstream1, name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos4' :
                print("AnimMain Going in nextVideos4")
                try:
                    vid2 = nextVideos4(self.session, name, url)
                    vid2.startSession()
                except:
                    pass

        elif 'listMovie' in str(url) and self.nextmodule == 'Videos4':
            print("AnimMain Going listmovie in Videos4")
            try:
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif 'movieId' in str(url) : # and self.nextmodule == 'Videos4':
            print('AnimMain videos5 moveid')
            try:
                vid2 = Videos5(self.session, name, url)
                vid2.startSession()
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
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos2":
            print("In animeMain Going in Videos2 name =", name)
            print("In animeMain Going in Videos2 url =", url)
            try:
                vid2 = Videos2(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos3":
            print("In AnimMain Going in Videos3")
            try:
                vid2 = Videos3(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos4":
            print("in AnimMain Going in Videos4")
            try:
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos5":
            print("In AnimMain Going in Videos5")
            try:
                vid2 = Videos5(self.session, name, url)
                vid2.startSession()
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
            global search
            search = False
            name = str(result) #self.namex
            url = self.urlx + str(result)
            try:
                vid2 = nextVideos4(self.session, name, url)
                vid2.startSession()
            except:
                pass
#-----------------
#menupic
class GridMain(Screen):

    def __init__(self, session, menuTitle, nextmodule, names, urls, infos, pics = []):
        Screen.__init__(self, session)
        self.session = session
        skin = skin_path + 'GridMain.xml'
        with open(skin, 'r') as f:
          self.skin = f.read()
        print("In Gridmain names 1= ", names)
        print("In Gridmain urls 1 = ", urls)
        print("In Gridmain pics 1= ", pics)
        print("In Gridmain nextmodule = ", nextmodule)        
        title = menuTitle
        self["title"] = Button(title)
        tmpfold = config.plugins.tvspro.cachefold.value + "/tvspro/tmp"
        picfold = config.plugins.tvspro.cachefold.value + "/tvspro/pic"
        pics = getpics(names, pics, tmpfold, picfold)
        print("In Gridmain pics = ", pics)
        self.pos = []
        if HD.width() > 1280:
            self.pos.append([48,94])
            self.pos.append([408,94])
            self.pos.append([778,94])
            self.pos.append([1148,94])
            self.pos.append([1516,94])
            self.pos.append([48,544])
            self.pos.append([408,544])
            self.pos.append([778,544])
            self.pos.append([1148,544])
            self.pos.append([1516,544])
        else:
            self.pos.append([20,50])
            self.pos.append([266,50])
            self.pos.append([510,50])
            self.pos.append([750,50])
            self.pos.append([990,50])
            self.pos.append([20,350])
            self.pos.append([266,350])
            self.pos.append([510,350])
            self.pos.append([750,350])
            self.pos.append([990,350])

        print("self.pos =", self.pos)

        self.name = menuTitle
        self.nextmodule = nextmodule

        self.urls1 = urls
        self.pics = pics
        self.names1 = names
        self.infos = infos
        self["info"] = Label()

        list = []
        list = names
        self["menu"] = List(list)
        for x in list:
           print("x in list =", x)
        self["frame"] = MovingPixmap()
        self["label1"] = StaticText()
        self["label2"] = StaticText()
        self["label3"] = StaticText()
        self["label4"] = StaticText()
        self["label5"] = StaticText()
        self["label6"] = StaticText()
        self["label7"] = StaticText()
        self["label8"] = StaticText()
        self["label9"] = StaticText()
        self["label10"] = StaticText()
        self["label11"] = StaticText()
        self["label12"] = StaticText()
        self["label13"] = StaticText()
        self["label14"] = StaticText()
        self["label15"] = StaticText()
        self["label16"] = StaticText()
        self["pixmap1"] = Pixmap()
        self["pixmap2"] = Pixmap()
        self["pixmap3"] = Pixmap()
        self["pixmap4"] = Pixmap()
        self["pixmap5"] = Pixmap()
        self["pixmap6"] = Pixmap()
        self["pixmap7"] = Pixmap()
        self["pixmap8"] = Pixmap()
        self["pixmap9"] = Pixmap()
        self["pixmap10"] = Pixmap()
        self["pixmap11"] = Pixmap()
        self["pixmap12"] = Pixmap()
        self["pixmap13"] = Pixmap()
        self["pixmap14"] = Pixmap()
        self["pixmap15"] = Pixmap()
        self["pixmap16"] = Pixmap()
        self["actions"] = NumberActionMap(["OkCancelActions", "EPGSelectActions", "MenuActions", "DirectionActions", "NumberActions"],
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
        i = 0
        ip = 0
        self.index = 0
        self.ipage = 1
        self.icount = 0
        ln = len(self.names1)
        self.npage = int(float(ln/10)) + 1
        print("self.npage =", self.npage)
        print("Going in openTest")
        self.onLayoutFinish.append(self.openTest)

    def cancel(self):
        self.close()

    def exit(self):
       self.close()

    def showIMDB(self):
        itype = self.index
        name = self.names1[itype]
        if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/TMBD/plugin.pyo"):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif os.path.exists("/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo"):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = name
            text = charRemove(text_clear)
            HHHHH = text
            self.session.open(IMDB, HHHHH)
        else:
            text_clear = name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def paintFrame(self):
        
        print("In paintFrame self.index, self.minentry, self.maxentry =", self.index, self.minentry, self.maxentry)
        # if self.maxentry < self.index or self.index < 0:
        #     return
        print("In paintFrame self.ipage = ", self.ipage)
        ifr = self.index - (10*(self.ipage-1))
        print("ifr =", ifr)
        ipos = self.pos[ifr]
        print("ipos =", ipos)
        
        #key down crash end of list
        inf = self.index
        if inf is not None or inf != -1:
            self["info"].setText(self.infos[inf])
            print('infos: ', inf)

        self["frame"].moveTo( ipos[0], ipos[1], 1)
        self["frame"].startMoving()


    def openTest(self):
        print("self.index, openTest self.ipage, self.npage =", self.index, self.ipage, self.npage)
        if self.ipage < self.npage:
            self.maxentry = (10*self.ipage)-1
            self.minentry = (self.ipage-1)*10
            #self.index 0-11
            print("self.ipage , self.minentry, self.maxentry =", self.ipage, self.minentry, self.maxentry)

        elif self.ipage == self.npage:
            print("self.ipage , len(self.pics) =", self.ipage, len(self.pics))
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage-1)*10
            print("self.ipage , self.minentry, self.maxentry B=", self.ipage, self.minentry, self.maxentry)
            i1 = 0
            blpic = dblank #THISPLUG + "res/pics/blank.png"
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

            print("self.names1[idx] B=", self.names1[idx])
            self["label" + str(i+1)].setText(self.names1[idx])
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
        #   if self.index < 0:
        #       self.index = self.maxentry
        #       self.paintFrame()
        print("keyup self.index, self.minentry 2 = ", self.index, self.minentry)
        print("keyup self.ipage = ", self.ipage)
        if self.index < (self.minentry):
            if self.ipage > 1:
                self.ipage = self.ipage - 1
                self.openTest()
        ##  self.paintFrame()
            elif self.ipage == 1:
        #   self.close()
                return #edit lululla
                # self.paintFrame()
            else:
                # return
               self.paintFrame()
        else:
            # return
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
        url = self.urls1[itype]
        name = self.names1[itype]
        print("In GridMain name =", name)
        print("In GridMain self.nextmodule =", self.nextmodule)

        if name == "Config":
            self.session.open(ConfigEx)

        elif name == "About":
            self.session.open(Abouttvr)

        elif 'Search' in str(name):
            search = True
            # from Screens.VirtualKeyBoard import VirtualKeyBoard
            print('Search go movie: ', search)
            self.search_text(name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos1':
            print("In AnimMain Going in Videos1")
            try:
                vid2 = nextVideos1(self.session, name, url)
                vid2.startSession()
            except:
                pass
        elif '&page' not in str(url) and self.nextmodule == 'Videos1':
            print('video1 and play next sss  ', self.nextmodule)
            if 'tvseriesId' in str(url):
                try:
                    vid2 = Videos6(self.session, name, url) #atv 6.5
                    vid2.startSession()
                except:
                    pass
            else:
                print('video1 and play next xx : ', self.nextmodule)
                self.session.open(Playstream1, name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos4' :
                print("AnimMain Going in nextVideos4")
                try:
                    vid2 = nextVideos4(self.session, name, url)
                    vid2.startSession()
                except:
                    pass

        elif 'listMovie' in str(url) and self.nextmodule == 'Videos4':
            print("AnimMain Going listmovie in Videos4")
            try:
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif 'movieId' in str(url) : # and self.nextmodule == 'Videos4':
            print('AnimMain videos5 moveid')
            try:
                vid2 = Videos5(self.session, name, url)
                vid2.startSession()
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
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos2":
            print("In animeMain Going in Videos2 name =", name)
            print("In animeMain Going in Videos2 url =", url)
            try:
                vid2 = Videos2(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos3":
            print("In AnimMain Going in Videos3")
            try:
                vid2 = Videos3(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos4":
            print("in AnimMain Going in Videos4")
            try:
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except:
                pass

        elif self.nextmodule == "Videos5":
            print("In AnimMain Going in Videos5")
            try:
                vid2 = Videos5(self.session, name, url)
                vid2.startSession()
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
            global search
            search = False
            name = self.namex
            url = self.urlx + str(result)
            try:
                vid2 = nextVideos4(self.session, name, url)
                vid2.startSession()
            except:
                return
                pass
#-----------------
#main exe
class tvspromain(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = RSList([])
        title = _(name_plug)
        self["title"] = Button(title)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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

class Videos6(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        url = self.url
        print("Videos1 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        ###py3
        #content = six.ensure_str(content)
        # print("In Videos1 content =", content)
        y = json.loads(content)
        i = 0
        #[COLOR yellow]Umbria[\/COLOR]
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
                # url = (y["items"][i]["link"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                print("In Videos4 info =", info)
                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                    # print('name', name)
                    # print('url', url)
                    # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
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

class Videos1(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        url = self.url
        print("Videos1 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        ###py3
        #content = six.ensure_str(content)
        # print("In Videos1 content =", content)
        y = json.loads(content)
        i = 0
        #[COLOR yellow]Umbria[\/COLOR]
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
                # url = (y["items"][i]["link"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                print("In Videos4 info =", info)
                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                    # print('name', name)
                    # print('url', url)
                    # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
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
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        url = self.url
        print("Videos1 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        #py3
        #content = six.ensure_str(content)
        # print("In Videos1 content =", content)
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
                # url = (y["items"][i]["link"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                print("In Videos4 info =", info)
                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                    # print('name', name)
                    # print('url', url)
                    # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
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

class Videos2(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        url = self.url
        print("Videos2 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        #py3
        #content = six.ensure_str(content)
        # print("In Videos2 content =", content)
        y = json.loads(content)
        i = 0
        #[COLOR yellow]Umbria[\/COLOR]
        while i<100:
            try:
                print('In getVideos y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In Videos2 name =", name)
                url = (y["items"][i]["externallink"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                info = (y["items"][i]["info"])
                print("In Videos4 info =", info)
                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                # print('name', name)
                # print('url', url)
                # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
                i = i+1
            except:
                break
        title = name_plug
        if "Live" in self.name:
            nextmodule = "Videos3"
        elif "Film" in self.name:
            nextmodule = "Videos4"
        elif "Serie" in self.name:
            nextmodule = "Videos1"

        print("In Videos2 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos2 Going in GridMain")
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
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        url = self.url
        print("Videos3 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        #py3
        #content = six.ensure_str(content)
        # print("In Videos3 content =", content)
        y = json.loads(content)
        i = 0
        #[COLOR yellow]Umbria[\/COLOR]
        while i<100:
            try:
                print('In getVideos y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In Videos3 name =", name)
                try:
                    url = (y["items"][i]["link"])
                except:
                    url = (y["items"][i]["yatse"])
                # url = (y["items"][i]["link"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                pic = pic.replace("\\", "")
                info = (y["items"][i]["info"])
                print("In Videos4 info =", info)
                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                    # print('name', name)
                    # print('url', url)
                    # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
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
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        # self["info"].setText(self.name)
        url = self.url
        print("Videos4 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        ## py3
        #content = six.ensure_str(content)
        # print("In Videos4 content =", content)
        y = json.loads(content)
        i = 0
        #[COLOR yellow]Umbria[\/COLOR]
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
                print("In Videos4 info =", info)

                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                    # print('name', name)
                    # print('url', url)
                    # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
                i = i+1
            except:
                break
        title = name_plug
        nextmodule = "Videos5"
        print("In Videos4 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        print("In Videos4 nextmodule =", nextmodule)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos3 Going in GridMain")
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
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        # self["info"].setText(self.name)
        url = self.url
        print("nextVideos4 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        #py3
        #content = six.ensure_str(content)
        # print("In nextVideos4 content =", content)
        y = json.loads(content)
        i = 0
        #[COLOR yellow]Umbria[\/COLOR]
        while i<100:
            try:
                print('In nextVideos4 y["items"][i]["title"] =', y["items"][i]["title"])
                name = (y["items"][i]["title"])
                n1 = name.find("]", 0)
                n2 = name.find("[", n1)
                name = name[(n1+1):n2]
                print("In nextVideos4 name =", name)
                url = (y["items"][i]["externallink"])
                url = url.replace("\\", "")
                print("In nextVideos4 url =", url)
                pic = (y["items"][i]["thumbnail"])
                pic = pic.replace("\\", "")
                print("In nextVideos4 pic =", pic)

                info = (y["items"][i]["info"])
                print("In Videos4 info =", info)

                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                    # print('name', name)
                    # print('url', url)
                    # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
                i = i+1
            except:
                break
        title = name_plug
        nextmodule = "Videos4"
        print("In nextVideos4 config.plugins.tvspro.thumb.value =", config.plugins.tvspro.thumb.value)
        print("In nextVideos4 nextmodule =", nextmodule)
        if config.plugins.tvspro.thumb.value == "True":
            print("In Videos3 Going in GridMain")
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
        self["menu"] = RSList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        url = self.url
        print("Videos5 url =", url)
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        content = getUrl(url)
        #py3
        #content = six.ensure_str(content)
        # print("In Videos5 content =", content)
        y = json.loads(content)
        i = 0
        #[COLOR yellow]Umbria[\/COLOR]
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
                # url = (y["items"][i]["link"])
                url = url.replace("\\", "")
                pic = (y["items"][i]["thumbnail"])
                pic = pic.replace("\\", "")
                info = (y["items"][i]["info"])
                print("In Videos5 info =", info)
                # name = name.encode('ascii','ignore')
                # url = url.encode('ascii','ignore')
                # pic = pic.encode('ascii','ignore')
                # if PY3:
                    # name = name.decode("utf-8")
                    # url = url.decode("utf-8")
                    # pic = pic.decode("utf-8")
                    # print('name', name)
                    # print('url', url)
                    # print('pic', pic)
                info = info.replace("\r\n","")
                self.names.append(str(name))
                self.urls.append(str(url))
                self.pics.append(str(pic))
                self.infos.append(str(info))
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
        title = _(name_plug)
        self["title"] = Button(title)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"],
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
        continfo += _("== thank's to @PCD and LINUXSAT-SUPPORT.COM \n")
        continfo += _("========================================\n")
        continfo += _("NOTA BENE:\n")
        continfo += _("Le liste create ad HOC contengono indirizzi liberamente e gratuitamente\n")
        continfo += _("trovati in rete e non protetti da sottoscrizione o abbonamento.\n")
        continfo += _("Il server di riferimento strutturale ai progetti rilasciati\n")
        continfo += _("non e' fonte di alcun stream/flusso.\n")
        continfo += _("Assolutamente VIETATO utilizzare queste liste senza autorizzazione.\n")
        continfo += _("========================================\n")
        continfo += _("DISCLAIMER: \n")
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
        self.list = []
        self['list'] = RSList([])
        self['info'] = Label()
        self['info'].setText('Select Player')
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions', 'TimerEditActions'], {'red': self.cancel,
         'green': self.okClicked,
         'back' : self.cancel,
         'cancel': self.cancel,
         'ok': self.okClicked}, -2)
        self.name1 = name
        self.url = url
        print('In Playstream1 self.url =', url)
        global srefInit
        self.initialservice = self.session.nav.getCurrentlyPlayingServiceReference()
        srefInit = self.initialservice
        self.onLayoutFinish.append(self.openTest)
        return

    def openTest(self):
        url = self.url
        self.names = []
        self.urls = []
        self.names.append('Play Now')
        self.urls.append(str(url))
        self.names.append('Play HLS')
        self.urls.append(str(url))
        self.names.append('Play TS')
        self.urls.append(str(url))
        # self.names.append('Preview')
        # self.urls.append(str(url))
        showlist(self.names, self['list'])

    def okClicked(self):
        idx = self['list'].getSelectionIndex()
        if idx is None:
            return
        self.name = self.names[idx]
        self.url = self.urls[idx]

        if "youtube" in str(self.url):
            self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            return

        if idx == 0:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            print('In playVideo url D=', self.url)
            self.play()
        elif idx == 1:
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
        elif idx == 2:
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

        elif idx == 3:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            print('In playVideo url D=', self.url)
            self.play2()
        else:
            self.name = self.names[idx]
            self.url = self.urls[idx]
            print('In playVideo url D=', self.url)
            self.play()
        return

    def playfile(self, serverint):
        self.serverList[serverint].play(self.session, self.url, self.name)

    def play(self):
        desc = ' '
        url = self.url
        name = self.name1
        self.session.open(Playstream2, name, url, desc)
        # return
        self.close()

    def play2(self):
        desc = ' '
        self['info'].setText(self.name)

        url = self.url
        url = url.replace(':', '%3a')
        print('In tvspro url =', url)
        ref = '4097:0:1:0:0:0:0:0:0:0:' + url
        sref = eServiceReference(ref)
        print('SREF: ', sref)
        sref.setName(self.name1)
        self.session.nav.playService(sref)


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

class Playstream2(Screen, InfoBarMenu, InfoBarBase, InfoBarSeek, InfoBarNotifications, InfoBarAudioSelection, TvInfoBarShowHide):#,InfoBarSubtitleSupport
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 4000

    def __init__(self, session, name, url, desc):
        global SREF
        Screen.__init__(self, session)
        self.session = session
        self.skinName = 'MoviePlayer'
        title = 'Play Stream'
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarAudioSelection.__init__(self)
        # InfoBarSubtitleSupport.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self['actions'] = ActionMap(['WizardActions',
         'MoviePlayerActions',
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
        url = url.replace(':', '%3a')
        url = url.replace(' ','%20')
        self.icount = 0
        self.desc = desc
        self.pcip = 'None'
        self.url = url
        self.name = name
        self.state = self.STATE_PLAYING
        self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
        SREF = self.srefOld
        self.onLayoutFinish.append(self.cicleStreamType)
        self.onClose.append(self.cancel)
        return

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
        debug = True
        sTitle = ''
        sServiceref = ''
        try:
            servicename, serviceurl = getserviceinfo(sref)
            if servicename is not None:
                sTitle = servicename
            else:
                sTitle = ''
            if serviceurl is not None:
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
        if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/TMBD/plugin.pyo"):
            from Plugins.Extensions.TMBD.plugin import TMBD
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(TMBD, text, False)
        elif fileExists("/usr/lib/enigma2/python/Plugins/Extensions/IMDb/plugin.pyo"):
            from Plugins.Extensions.IMDb.plugin import IMDB
            text_clear = self.name
            text = charRemove(text_clear)
            self.session.open(IMDB, text)
        else:
            text_clear = self.name
            self.session.open(MessageBox, text_clear, MessageBox.TYPE_INFO)

    def openPlay(self,servicetype, url):
        url = url
        ref = str(servicetype) +':0:1:0:0:0:0:0:0:0:' + str(url)
        print('final reference :   ', ref)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        from itertools import cycle, islice
        self.servicetype = str(config.plugins.tvspro.services.value)# '4097'
        print('servicetype1: ', self.servicetype)
        url = str(self.url)

        # if "youtube" in str(url):
            # desc = self.name
            # from youtube_dl import YoutubeDL
            # '''
            # ydl_opts = {'format': 'best'}
            # ydl_opts = {'format': 'bestaudio/best'}
            # '''
            # ydl_opts = {'format': 'best'}
            # ydl = YoutubeDL(ydl_opts)
            # ydl.add_default_info_extractors()
            # result = ydl.extract_info(url, download=False)
            # url = result["url"]
            # # self.session.open(Playstream2, name, url, desc)

        if "youtube" in str(self.url):
            self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            return

        currentindex = 0
        # streamtypelist = ["4097", "1"]
        streamtypelist = ["4097"]
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
        self.servicetype = int(next(nextStreamType))
        print('servicetype2: ', self.servicetype)
        self.openPlay(self.servicetype, url)

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(SREF)
        if self.pcip != 'None':
            url2 = 'http://' + self.pcip + ':8080/requests/status.xml?command=pl_stop'
            resp = urlopen(url2)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except:
                pass
        self.close()

    def leavePlayer(self):
        self.close()

def charRemove(text):
    char = ["1080p",
     "2018",
     "2019",
     "2020",
     "2021",
     "480p",
     "4K",
     "720p",
     "ANIMAZIONE",
     "APR",
     "AVVENTURA",
     "BIOGRAFICO",
     "BDRip",
     "BluRay",
     "CINEMA",
     "COMMEDIA",
     "DOCUMENTARIO",
     "DRAMMATICO",
     "FANTASCIENZA",
     "FANTASY",
     "FEB",
     "GEN",
     "GIU",
     "HDCAM",
     "HDTC",
     "HDTS",
     "LD",
     "MAFIA",
     "MAG",
     "MARVEL",
     "MD",
     "ORROR",
     "NEW_AUDIO",
     "POLIZ",
     "R3",
     "R6",
     "SD",
     "SENTIMENTALE",
     "TC",
     "TEEN",
     "TELECINE",
     "TELESYNC",
     "THRILLER",
     "Uncensored",
     "V2",
     "WEBDL",
     "WEBRip",
     "WEB",
     "WESTERN",
     "-",
     "_",
     ".",
     "+",
     "[",
     "]"]

    myreplace = text
    for ch in char:
            myreplace = myreplace.replace(ch, "").replace("  ", " ").replace("       ", " ").strip()
    return myreplace

def main(session, **kwargs):
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
