#!/usr/bin/python
# -*- coding: utf-8 -*-

# '''
# Info http://t.me/tivustream
# ****************************************
# *        coded by Lululla              *
# *          skin by MMark               *
# *             02/07/2023               *
# ****************************************
# '''

from __future__ import print_function
from . import _, getversioninfo
from .lib import Utils
from .lib import html_conv
from .lib.Console import Console as xConsole

from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.config import (
    ConfigEnableDisable,
    ConfigDirectory,
    ConfigSelection,
    getConfigListEntry,
    configfile,
    config,
    ConfigYesNo,
    ConfigSubsection,
)
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import (
    MultiContentEntryPixmapAlphaTest,
    MultiContentEntryText)
from Components.Pixmap import (Pixmap, MovingPixmap)
from Components.ProgressBar import ProgressBar
from Components.ServiceEventTracker import (ServiceEventTracker, InfoBarBase)
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from itertools import cycle, islice
from os.path import (splitext, exists as file_exists)
from Plugins.Plugin import PluginDescriptor
from PIL import Image, ImageFile
from Screens.InfoBarGenerics import (
    InfoBarSubtitleSupport,
    InfoBarMenu,
    InfoBarSeek,
    InfoBarAudioSelection,
    InfoBarNotifications,
)
from Screens.LocationBox import LocationBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.Directories import SCOPE_PLUGINS, resolveFilename
from Tools.Downloader import downloadWithProgress
from enigma import (
    eListboxPythonMultiContent,
    eServiceReference,
    eTimer,
    gFont,
    iPlayableService,
    loadPNG,
    RT_HALIGN_LEFT,
    RT_VALIGN_CENTER,
    getDesktop,
)
from requests import get, exceptions
from requests.exceptions import HTTPError
from twisted.internet.reactor import callInThread
from datetime import datetime
import codecs
import json
import os
import re
import requests
import six
import sys
from six.moves.urllib.request import urlopen
from six.moves.urllib.request import Request
from six.moves.urllib.parse import urlparse

ImageFile.LOAD_TRUNCATED_IMAGES = True
_session = None
THISPLUG = resolveFilename(SCOPE_PLUGINS, "Extensions/{}/".format('tvspro'))
PY3 = sys.version_info.major >= 3


if PY3:
    from http.client import HTTPConnection
    from urllib.parse import urlparse
    PY3 = True
else:
    from httplib import HTTPConnection
    from urlparse import urlparse

HTTPConnection.debuglevel = 1

global defpic, dblank
_session = None
name_plug = 'TVS Pro Revolution'
currversion = getversioninfo()
Version = currversion + ' - 05.09.2024'
title_plug = '..:: TVS Pro Revolution V. %s ::..' % Version
referer = 'https://tivustream.website'
installer_url = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL0JlbGZhZ29yMjAwNS9yZXZvbHV0aW9ucHJvL21haW4vaW5zdGFsbGVyLnNo'
developer_url = 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9CZWxmYWdvcjIwMDUvcmV2b2x1dGlvbnBybw=='
skin_path = THISPLUG
res_plugin_path = os.path.join(THISPLUG, 'res/')
pngx = os.path.join(res_plugin_path, 'pics/setting2.png')
SREF = ""
piccons = os.path.join(THISPLUG, 'res/img/')
piconinter = os.path.join(piccons, 'inter.png')
piconlive = os.path.join(piccons, 'tv.png')
piconmovie = os.path.join(piccons, 'cinema.png')
piconsearch = os.path.join(piccons, 'search.png')
piconseries = os.path.join(piccons, 'series.png')
# pixmaps = os.path.join(piccons, 'backg.png')
nextpng = 'next.png'
prevpng = 'prev.png'
folder_path = "/tmp/tvspro/"


if not os.path.exists(folder_path):
    os.makedirs(folder_path)

screenwidth = getDesktop(0).size()
if screenwidth.width() == 2560:
    skin_path = THISPLUG + '/res/skins/uhd/'
    defpic = THISPLUG + '/res/pics/defaultL.png'
    dblank = THISPLUG + '/res/pics/blankL.png'

elif screenwidth.width() == 1920:
    skin_path = THISPLUG + '/res/skins/fhd/'
    defpic = THISPLUG + '/res/pics/defaultL.png'
    dblank = THISPLUG + '/res/pics/blankL.png'
else:
    skin_path = THISPLUG + '/res/skins/hd/'
    defpic = THISPLUG + '/res/pics/default.png'
    dblank = THISPLUG + '/res/pics/blank.png'


if sys.version_info >= (2, 7, 9):
    try:
        import ssl
        sslContext = ssl._create_unverified_context()
    except BaseException:
        sslContext = None

# https twisted client hack #
sslverify = False
try:
    from twisted.internet import ssl
    from twisted.internet._sslverify import ClientTLSOptions
    sslverify = True
except ImportError:
    pass

if sslverify:
    class SNIFactory(ssl.ClientContextFactory):
        def __init__(self, hostname=None):
            self.hostname = hostname

        def getContext(self):
            ctx = self._contextFactory(self.method)
            if self.hostname:
                ClientTLSOptions(self.hostname, ctx)
            return ctx


def piconlocal(name):

    pngs = [
        ["tv", "movie"],
        ["commedia", "commedia"],
        ["comedy", "commedia"],
        ["thriller", "thriller"],
        ["family", "family"],
        ["famiglia", "family"],
        ["azione", "azione"],
        ["dramma", "dramma"],
        ["drama", "dramma"],
        ["western", "western"],
        ["biografico", "biografico"],
        ["storia", "biografico"],
        ["documentario", "biografico"],
        ["romantico", "romantico"],
        ["romance", "romantico"],
        ["horror", "horror"],
        ["musica", "musical"],
        ["show", "musical"],
        ["guerra", "guerra"],
        ["bambini", "bambini"],
        ["bianco", "bianconero"],
        ["tutto", "toto"],
        ["cartoni", "cartoni"],
        ["bud", "budterence"],
        ["documentary", "documentary"],
        ["crime", "crime"],
        ["mystery", "mistery"],
        ["mistero", "mistery"],
        ["giallo", "mistery"],
        ["fiction", "fiction"],
        ["adventure", "mistery"],
        ["action", "azione"],
        ["007", "007"],
        ["sport", "sport"],
        ["teatr", "teatro"],
        ["variet", "teatro"],
        ["giallo", "teatro"],
        ["extra", "extra"],
        ["sexy", "fantasy"],
        ["erotic", "fantasy"],
        ["animazione", "bambini"],
        ["search", "search"],

        ["abruzzo", "regioni/abruzzo"],
        ["basilicata", "regioni/basilicata"],
        ["calabria", "regioni/calabria"],
        ["campania", "regioni/campania"],
        ["emilia", "regioni/emiliaromagna"],
        ["friuli", "regioni/friuliveneziagiulia"],
        ["lazio", "regioni/lazio"],
        ["liguria", "regioni/liguria"],
        ["lombardia", "regioni/lombardia"],
        ["marche", "regioni/marche"],
        ["molise", "regioni/molise"],
        ["piemonte", "regioni/piemonte"],
        ["puglia", "regioni/puglia"],
        ["sardegna", "regioni/sardegna"],
        ["sicilia", "regioni/sicilia"],
        ["toscana", "regioni/toscana"],
        ["trentino", "regioni/trentino"],
        ["umbria", "regioni/umbria"],
        ["veneto", "regioni/veneto"],
        ["aosta", "regioni/valledaosta"],

        ["mediaset", "mediaset"],
        ["nazionali", "nazionali"],
        ["news", "news"],

        ["rai", "rai"],
        ["webcam", "relaxweb"],
        ["relax", "relaxweb"],
        ["vecchi", "vecchi"],
        ["muto", "vecchi"],
        ["'italiani", "movie"],

        ["fantascienza", "fantascienza"],
        ["fantasy", "fantasy"],
        ["fantasia", "fantasia"],
        ["film", "movie"],
        ["samsung", "samsung"],
        ["plutotv", "plutotv"]
    ]

    for png in pngs:
        piconlocal = 'backg.png'
        if png[0] in str(name).lower():
            piconlocal = str(png[1]) + ".png"
            break

    if 'prev' in name.lower():
        piconlocal = prevpng
    elif 'next' in name.lower():
        piconlocal = nextpng

    print('>>>>>>>> ' + str(piccons) + str(piconlocal))
    path = os.path.join(piccons, piconlocal)
    return str(path)


class rvList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        if screenwidth.width() == 2560:
            self.l.setItemHeight(60)
            textfont = int(42)
            self.l.setFont(0, gFont('Regular', textfont))
        elif screenwidth.width() == 1920:
            self.l.setItemHeight(50)
            textfont = int(30)
            self.l.setFont(0, gFont('Regular', textfont))
        else:
            self.l.setItemHeight(40)
            textfont = int(24)
            self.l.setFont(0, gFont('Regular', textfont))


def rvoneListEntry(name):
    res = [name]
    pngx = os.path.join(res_plugin_path, 'pics/setting2.png')
    if screenwidth.width() == 2560:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    5, 5), size=(
                    50, 50), png=loadPNG(pngx)))
        res.append(
            MultiContentEntryText(
                pos=(
                    90,
                    0),
                size=(
                    1200,
                    50),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    elif screenwidth.width() == 1920:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    5, 5), size=(
                    40, 40), png=loadPNG(pngx)))
        res.append(
            MultiContentEntryText(
                pos=(
                    70,
                    0),
                size=(
                    1000,
                    50),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    else:
        res.append(
            MultiContentEntryPixmapAlphaTest(
                pos=(
                    3, 0), size=(
                    40, 40), png=loadPNG(pngx)))
        res.append(
            MultiContentEntryText(
                pos=(
                    50,
                    0),
                size=(
                    500,
                    40),
                font=0,
                text=name,
                color=0xa6d1fe,
                flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
    return res


def showlist(datal, list):
    plist = []
    for name in datal:  # Iterazione più pythonica
        plist.append(rvoneListEntry(name))
    list.setList(plist)


"""
def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(rvoneListEntry(name))
        icount += 1
        list.setList(plist)
"""


mdpchoices = [
    ("4097", ("IPTV(4097)")),
    ("1", ("Dvb(1)")),
]
players = [
    ("/usr/bin/gstplayer", ("5001", "Gstreamer(5001)")),
    ("/usr/bin/exteplayer3", ("5002", "Exteplayer3(5002)")),
    ("/usr/bin/apt-get", ("8193", "DreamOS GStreamer(8193)"))
]
mdpchoices.extend(choice for path, choice in players if file_exists(path))

config.plugins.tvspro = ConfigSubsection()
cfg = config.plugins.tvspro

cfg.services = ConfigSelection(default='4097', choices=mdpchoices)
cfg.thumb = ConfigSelection(
    default="True", choices=[
        ("True", _("yes")), ("False", _("no"))])
cfg.movie = ConfigDirectory("/media/hdd/movie")
cfg.cachefold = ConfigDirectory("/media/hdd", False)


try:
    from Components.UsageConfig import defaultMoviePath
    downloadpath = defaultMoviePath()
    cfg.movie = ConfigDirectory(default=downloadpath)
    cfg.cachefold = ConfigDirectory(default=downloadpath)
except BaseException:
    if os.path.exists("/usr/bin/apt-get"):
        cfg.movie = ConfigDirectory(default='/media/hdd/movie')
        # ConfigDirectory(default='/media/hdd')
        cfg.cachefold = str(cfg.movie.value)

Path_Movies = str(cfg.movie.value) + '/'
Path_Cache = str(cfg.cachefold.value).replace('movie', 'tvspro')
if not os.path.exists(Path_Cache):
    os.makedirs(Path_Cache)


def returnIMDB(text_clear):
    TMDB = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('TMDB'))
    tmdb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('tmdb'))
    IMDb = resolveFilename(SCOPE_PLUGINS, "Extensions/{}".format('IMDb'))
    text = html_conv.html_unescape(text_clear)
    if os.path.exists(TMDB):
        try:
            from Plugins.Extensions.TMBD.plugin import TMBD
            _session.open(TMBD.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", str(e))
        return True

    elif os.path.exists(tmdb):
        try:
            from Plugins.Extensions.tmdb.plugin import tmdb
            _session.open(tmdb.tmdbScreen, text, 0)
        except Exception as e:
            print("[XCF] Tmdb: ", str(e))
        return True

    elif os.path.exists(IMDb):
        try:
            from Plugins.Extensions.IMDb.plugin import main as imdb
            imdb(_session, text)
        except Exception as e:
            print("[XCF] imdb: ", str(e))
        return True
    else:
        _session.open(MessageBox, text, MessageBox.TYPE_INFO)
        return True
    return False


def threadGetPage(
        url=None,
        file=None,
        key=None,
        success=None,
        fail=None,
        *args,
        **kwargs):
    print('[threadGetPage] url, file, key, args, kwargs', url,
          "   ", file, "   ", key, "   ", args, "   ", kwargs)
    try:
        url = url.rstrip('\r\n').rstrip().replace("%0A", "")
        response = get(url, verify=False)
        response.raise_for_status()
        if file is None:
            success(response.content)
        elif key is not None:
            success(response.content, file, key)
        else:
            success(response.content, file)
    except HTTPError as httperror:
        print('[threadGetPage] Http error: ', httperror)
        # fail(error)  # E0602 undefined name 'error'
    except exceptions.RequestException as error:
        print(error)


def getpics(names, pics, tmpfold, picfold):
    # from PIL import Image
    global defpic
    defpic = defpic
    pix = []

    if cfg.thumb.value == "False":
        npic = len(pics)
        i = 0
        while i < npic:
            pix.append(defpic)
            i += 1
        return pix

    cmd = "rm " + tmpfold + "/*"
    os.system(cmd)

    npic = len(pics)
    j = 0

    while j < npic:
        name = names[j]
        if name is None or name == '':
            name = "Video"
        url = pics[j]
        ext = str(os.path.splitext(url)[-1])
        picf = os.path.join(picfold, str(name + ext))
        tpicf = os.path.join(tmpfold, str(name + ext))

        if os.path.exists(picf):
            if ('stagione') in str(name.lower()):
                cmd = "rm " + picf
                os.system(cmd)

            cmd = "cp " + picf + " " + tmpfold
            print("In getpics fileExists(picf) cmd =", cmd)
            os.system(cmd)

        # test remove this
        # if os.path.exists(tpicf):
            # cmd = "rm " + tpicf
            # os.system(cmd)

        if not os.path.exists(picf):
            # if plugin_path in url:
            if THISPLUG in url:
                try:
                    cmd = "cp " + url + " " + tpicf
                    print("In getpics not fileExists(picf) cmd =", cmd)
                    os.system(cmd)
                except BaseException:
                    pass
            else:
                # now download image
                try:
                    url = url.replace(" ", "%20").replace("ExQ", "=")
                    url = url.replace("AxNxD", "&").replace("%0A", "")
                    poster = Utils.checkRedirect(url)
                    if poster:
                        ''''
                        # if PY3:
                            # poster = poster.encode()
                        '''

                        if "|" in url:
                            n3 = url.find("|", 0)
                            n1 = url.find("Referer", n3)
                            n2 = url.find("=", n1)
                            url = url[:n3]
                            referer = url[n2:]
                            p = Utils.getUrl2(url, referer)
                            with open(tpicf, 'wb') as f1:
                                f1.write(p)
                        else:
                            try:
                                '''
                                # print("Going in urlopen url =", url)
                                # p = Utils.gettUrl(url)
                                # with open(tpicf, 'wb') as f1:
                                    # f1.write(p)
                                '''
                                try:
                                    with open(tpicf, 'wb') as f:
                                        f.write(
                                            requests.get(
                                                url,
                                                stream=True,
                                                allow_redirects=True).content)
                                    print(
                                        '=============11111111=================\n')
                                except Exception as e:
                                    print("Error: Exception", e)
                                    print(
                                        '===========2222222222=================\n')
                                    callInThread(
                                        threadGetPage,
                                        url=poster,
                                        file=tpicf,
                                        success=downloadPic,
                                        fail=downloadError)

                                    '''
                                    print(e)
                                    open(tpicf, 'wb').write(requests.get(poster, stream=True, allow_redirects=True).content)
                                    '''
                            except Exception as e:
                                print("Error: Exception 2")
                                print(e)

                except BaseException:
                    cmd = "cp " + defpic + " " + tpicf
                    os.system(cmd)
                    print('cp defpic tpicf')

        if not file_exists(tpicf):
            cmd = "cp " + defpic + " " + tpicf
            os.system(cmd)

        if file_exists(tpicf):
            try:
                size = [168, 223]
                if screenwidth.width() == 2560:
                    size = [294, 440]
                elif screenwidth.width() == 1920:
                    size = [220, 330]

                file_name, file_extension = os.path.splitext(tpicf)
                try:
                    im = Image.open(tpicf).convert("RGBA")
                    # shrink if larger
                    try:
                        im.thumbnail(size, Image.Resampling.LANCZOS)
                    except BaseException:
                        im.thumbnail(size, Image.ANTIALIAS)
                    imagew, imageh = im.size
                    # enlarge if smaller
                    try:
                        if imagew < size[0]:
                            ratio = size[0] / imagew
                            try:
                                im = im.resize(
                                    (int(imagew * ratio), int(imageh * ratio)), Image.Resampling.LANCZOS)
                            except BaseException:
                                im = im.resize(
                                    (int(imagew * ratio), int(imageh * ratio)), Image.ANTIALIAS)

                            imagew, imageh = im.size
                    except Exception as e:
                        print(e)
                    # # no work on PY3
                    # # crop and center image
                    # bg = Image.new("RGBA", size, (255, 255, 255, 0))
                    # im_alpha = im.convert("RGBA").split()[-1]
                    # bgwidth, bgheight = bg.size
                    # bg_alpha = bg.convert("RGBA").split()[-1]
                    # temp = Image.new("L", (bgwidth, bgheight), 0)
                    # temp.paste(im_alpha, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)), im_alpha)
                    # bg_alpha = ImageChops.screen(bg_alpha, temp)
                    # bg.paste(im, (int((bgwidth - imagew) / 2), int((bgheight - imageh) / 2)))
                    # im = bg
                    im.save(file_name + ".png", "PNG")
                except Exception as e:
                    print(e)
                    im = Image.open(tpicf)
                    try:
                        im.thumbnail(size, Image.Resampling.LANCZOS)
                    except BaseException:
                        im.thumbnail(size, Image.ANTIALIAS)
                    im.save(tpicf)
            except Exception as e:
                print("******* picon resize failed *******")
                print(e)
                tpicf = defpic
        else:
            print("******* make picon failed *******")
            tpicf = defpic

        pix.append(j)
        pix[j] = picf
        j += 1

    cmd1 = "cp " + tmpfold + "/* " + picfold
    os.system(cmd1)

    cmd1 = "rm " + tmpfold + "/* &"
    os.system(cmd1)
    return pix


def downloadPic(output, poster):
    try:
        if output is not None:
            f = open(poster, 'wb')
            f.write(output)
            f.close()
    except Exception as e:
        print('downloadPic error ', e)
    return


def downloadError(output):
    print('output error ', output)
    pass


def savePoster(dwn_poster, url_poster):
    with open(dwn_poster, 'wb') as f:
        f.write(
            requests.get(
                url_poster,
                stream=True,
                allow_redirects=True).content)
        f.close()


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
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self["actions"] = ActionMap(["MenuActions", "DirectionActions", "ColorActions", "OkCancelActions"], {
            "ok": self.okClicked,
            "cancel": self.close,
            "red": self.close,
            "green": self.okClicked
        }, -1)
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.infos = []
        self.menu = [
            [_("About"), _("Information Us"), ""],
            [_("Config"), _("Setup Plugin"), ""],
            [_("Live TV"), _("Live TV Stream"), "https://tivustream.website/urls/e2live"],
            [_("Film"), _("Film and Movie"), "https://tivustream.website/urls/e2movie"],
            [_("Serie"), _("Series"), "https://tivustream.website/urls/e2series"],
            [_("Search"), _("Search your Movie"), "https://tivustream.website/php_filter/kodi19/kodi19.php?mode=movie&query="],
        ]

        self.session.open(AnimMain, name_plug, "Videos2", self.menu)

    def okClicked(self):
        pass

    def cancel(self):
        self.session.nav.playService(self.srefInit)
        self.close()


class AnimMain(Screen):
    def __init__(self, session, menuTitle, nextmodule, menu):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        skin = os.path.join(skin_path, 'AnimMain.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.menu = menu
        self.nextmodule = nextmodule
        self.pos = []
        self["title"] = Button(menuTitle)
        self["pointer"] = Pixmap()
        self["info"] = Label()
        self["label1"] = StaticText()
        self["label2"] = StaticText()
        self["label3"] = StaticText()
        self["label4"] = StaticText()
        self["label5"] = StaticText()
        self["key_red"] = Button(_("Cancel"))
        self["key_yellow"] = Button(_("Update"))
        self.nop = len(self.menu)
        self.index = 0
        self.Update = False
        self['actions'] = ActionMap(['OkCancelActions',
                                     'HotkeyActions',
                                     'InfobarEPGActions',
                                     'MenuActions',
                                     'ChannelSelectBaseActions',
                                     'DirectionActions'], {'ok': self.okbuttonClick,
                                                           # 'up': self.up,
                                                           # 'down': self.down,
                                                           'left': self.key_left,
                                                           'right': self.key_right,
                                                           'yellow': self.update_me,  # update_me,
                                                           'yellow_long': self.update_dev,
                                                           'info_long': self.update_dev,
                                                           'infolong': self.update_dev,
                                                           'showEventInfoPlugin': self.update_dev,
                                                           'menu': self.closeRecursive,
                                                           'green': self.okbuttonClick,
                                                           'cancel': self.closerm,
                                                           'red': self.closerm}, -1)
        self.timer = eTimer()
        if os.path.exists('/var/lib/dpkg/status'):
            self.timer_conn = self.timer.timeout.connect(self.check_vers)
        else:
            self.timer.callback.append(self.check_vers)
        self.timer.start(500, 1)
        self.onShown.append(self.openTest)

    def check_vers(self):
        remote_version = '0.0'
        remote_changelog = ''
        req = Request(Utils.b64decoder(installer_url), headers=headers)
        page = urlopen(req).read()
        if PY3:
            data = page.decode("utf-8")
        else:
            data = page.encode("utf-8")
        if data:
            lines = data.split("\n")
            for line in lines:
                if line.startswith("version"):
                    remote_version = line.split("=")
                    remote_version = line.split("'")[1]
                if line.startswith("changelog"):
                    remote_changelog = line.split("=")
                    remote_changelog = line.split("'")[1]
                    break
        self.new_version = remote_version
        self.new_changelog = remote_changelog
        if currversion < remote_version:
            self.Update = True
            self['key_yellow'].show()
            self.session.open(
                MessageBox,
                _('New version %s is available\n\nChangelog: %s\n\nPress info_long or yellow_long button to start force updating.') %
                (self.new_version,
                 self.new_changelog),
                MessageBox.TYPE_INFO,
                timeout=5)

    def update_me(self):
        if self.Update is True:
            self.session.openWithCallback(
                self.install_update,
                MessageBox,
                _("New version %s is available.\n\nChangelog: %s \n\nDo you want to install it now?") %
                (self.new_version,
                 self.new_changelog),
                MessageBox.TYPE_YESNO)
        else:
            self.session.open(
                MessageBox,
                _("Congrats! You already have the latest version..."),
                MessageBox.TYPE_INFO,
                timeout=4)

    def update_dev(self):
        try:
            req = Request(
                Utils.b64decoder(developer_url), headers={
                    'User-Agent': 'Mozilla/5.0'})
            page = urlopen(req).read()
            data = json.loads(page)
            remote_date = data['pushed_at']
            strp_remote_date = datetime.strptime(
                remote_date, '%Y-%m-%dT%H:%M:%SZ')
            remote_date = strp_remote_date.strftime('%Y-%m-%d')
            self.session.openWithCallback(
                self.install_update,
                MessageBox,
                _("Do you want to install update ( %s ) now?") %
                (remote_date),
                MessageBox.TYPE_YESNO)
        except Exception as e:
            print('error xcons:', e)

    def install_update(self, answer=False):
        if answer:
            cmd1 = 'wget -q "--no-check-certificate" ' + \
                Utils.b64decoder(installer_url) + ' -O - | /bin/sh'
            self.session.open(
                xConsole,
                'Upgrading...',
                cmdlist=[cmd1],
                finishedCallback=self.myCallback,
                closeOnSuccess=False)
        else:
            self.session.open(
                MessageBox,
                _("Update Aborted!"),
                MessageBox.TYPE_INFO,
                timeout=3)

    def myCallback(self, result=None):
        print('result:', result)
        return

    def key_menu(self):
        return

    def info(self):
        self.inf = " "
        try:
            self.inf = self.nextlink[1]
        except BaseException:
            pass
        if self.inf:
            try:
                self["info"].setText(self.inf)
            except BaseException:
                self["info"].setText('')
        print("In AnimMain infos nextlink[1] =", self.inf)

    def closerm(self):
        self.close()

    def openTest(self):
        nextname = islice(cycle(self.menu), self.index, None)
        menu1 = next(nextname)
        menu2 = next(nextname)
        menu3 = next(nextname)
        menu4 = next(nextname)
        menu5 = next(nextname)
        self["label1"].setText(menu1[0])
        self["label2"].setText(menu2[0])
        self["label3"].setText(menu3[0])
        self["label4"].setText(menu4[0])
        self["label5"].setText(menu5[0])

        self.nextlink = menu3
        if screenwidth.width() == 2560:
            dpointer = os.path.join(res_plugin_path, "pics/pointerFHD.png")
            self["pointer"].instance.setPixmapFromFile(dpointer)
        elif screenwidth.width() == 1920:
            dpointer = os.path.join(res_plugin_path, "pics/pointerFHD.png")
            self["pointer"].instance.setPixmapFromFile(dpointer)
        else:
            dpointer = os.path.join(res_plugin_path, "pics/pointerHD.png")
            self["pointer"].instance.setPixmapFromFile(dpointer)
        self.info()

    def key_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = self.nop - 1
        self.openTest()

    def key_right(self):
        self.index += 1
        if self.index > self.nop - 1:
            self.index = 0
        self.openTest()

    def closeRecursive(self):
        self.close(True)

    def okbuttonClick(self):
        name = self.nextlink[0]
        url = self.nextlink[2]
        if self.nextlink[0] == _("About"):
            self.session.open(Abouttvr)

        elif self.nextlink[0] == _("Config"):
            self.session.open(ConfigEx)

        elif self.nextlink[0] == _("Live TV") or self.nextlink[0] == _("Film") or self.nextlink[0] == _("Serie"):
            try:
                vid2 = Videos2(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif self.nextlink[0] == _("Search"):
            self.search_text()

    def search_text(self):
        self.namex = self.nextlink[0]
        self.urlx = self.nextlink[2]
        self.session.openWithCallback(
            self.filterChannels,
            VirtualKeyBoard,
            title=_("Filter this category..."),
            text='')

    def filterChannels(self, result=None):
        if result:
            name = str(result)
            url = self.urlx + str(result)
            try:
                vid2 = nextVideos4(self.session, name, url)
                vid2.startSession()
            except BaseException:
                return
        else:
            self.resetSearch()

    def resetSearch(self):
        global search
        search = False
        return


class Abouttvr(Screen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'Abouttvr.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        title = _(name_plug)
        self["title"] = Button(title)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["actions"] = ActionMap(["WizardActions",
                                     "InputActions",
                                     "ColorActions",
                                     'ButtonSetupActions',
                                     "DirectionActions"],
                                    {"ok": self.okClicked,
                                     "back": self.close,
                                     "cancel": self.cancel,
                                     "red": self.close,
                                     "green": self.okClicked},
                                    -1)
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self['info'].setText(self.getinfo())

    def okClicked(self):
        Screen.close(self, False)

    def getinfo(self):
        continfo = _("==  WELCOME to WWW.TIVUSTREAM.COM ==\n")
        continfo += _("== SUPPORT ON: WWW.CORVOBOYS.ORG http://t.me/tivustream ==\n")
        continfo += _("== thank's to @PCD @KIDDAC @MMARK @LINUXSAT-SUPPORT.COM\n")
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

    def cancel(self):
        self.close()


class ConfigEx(ConfigListScreen, Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        skin = os.path.join(skin_path, 'Config.xml')
        if os.path.exists('/var/lib/dpkg/status'):
            skin = os.path.join(skin_path, 'ConfigOs.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = _("SETUP PLUGIN")
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(
            self,
            self.list,
            session=self.session,
            on_change=self.changedEntry)
        self['key_red'] = Label(_('Exit'))
        self['key_green'] = Label(_('- - - -'))
        self['key_yellow'] = Button(_('Empty Cache'))
        self['title'] = Label(_('"SETUP PLUGIN"'))
        self["description"] = Label('')
        self['actions'] = ActionMap(["SetupActions", "ColorActions", "VirtualKeyboardActions"], {
            'cancel': self.extnok,
            'yellow': self.cachedel,
            'green': self.save,
            'showVirtualKeyboard': self.KeyText,
            'ok': self.Ok_edit
        }, -2)

        self.createSetup()
        self.onLayoutFinish.append(self.layoutFinished)

        if self.setInfo not in self['config'].onSelectionChanged:
            self['config'].onSelectionChanged.append(self.setInfo)

    def layoutFinished(self):
        self.setTitle(self.setup_title)

    def VirtualKeyBoardCallback(self, callback=None):
        if callback is not None and len(callback):
            self["config"].getCurrent()[1].setValue(callback)
            self["config"].invalidate(self["config"].getCurrent())

    def KeyText(self):
        sel = self['config'].getCurrent()
        if sel:
            self.session.openWithCallback(
                self.VirtualKeyBoardCallback,
                VirtualKeyBoard,
                title=self['config'].getCurrent()[0],
                text=self['config'].getCurrent()[1].value)

    def cachedel(self):
        fold = os.path.join(Path_Cache, "pic")
        Utils.cachedel(fold)
        self.mbox = self.session.open(
            MessageBox,
            _('All cache fold empty!'),
            MessageBox.TYPE_INFO,
            timeout=5)

    def createSetup(self):
        self.editListEntry = None
        self.list = []
        self.list.append(
            getConfigListEntry(
                _('Services Player Reference type'),
                cfg.services,
                _("Configure Service Player Reference, Enigma restart required")))
        self.list.append(getConfigListEntry(_("Cache folder"), cfg.cachefold, _(
            "Folder Cache Path (eg.: /media/hdd), Enigma restart required")))
        self.list.append(getConfigListEntry(_("Movie folder"), cfg.movie, _(
            "Folder Movie Path (eg.: /media/hdd/movie), Enigma restart required")))
        # self.list.append(getConfigListEntry(_("Show thumbpic ?"), cfg.thumb, _("Show Thumbpics ? Enigma restart required")))
        self['config'].list = self.list
        self["config"].l.setList(self.list)
        self.setInfo()

    def setInfo(self):
        try:
            sel = self['config'].getCurrent()[2]
            if sel:
                self['description'].setText(str(sel))
            else:
                self['description'].setText(_('SELECT YOUR CHOICE'))
            return
        except Exception as e:
            print("Error ", e)

    def changedEntry(self):
        self['key_green'].instance.setText(
            _('Save') if self['config'].isChanged() else '- - - -')
        for x in self.onChangedEntry:
            x()
        try:
            if isinstance(
                self['config'].getCurrent()[1],
                ConfigEnableDisable) or isinstance(
                self['config'].getCurrent()[1],
                ConfigYesNo) or isinstance(
                self['config'].getCurrent()[1],
                    ConfigSelection):
                self.createSetup()
        except BaseException:
            pass

    def getCurrentEntry(self):
        return self['config'].getCurrent() and self['config'].getCurrent()[
            0] or ''

    def getCurrentValue(self):
        return self['config'].getCurrent() and str(
            self['config'].getCurrent()[1].getText()) or ''

    def createSummary(self):
        from Screens.Setup import SetupSummary
        return SetupSummary

    def Ok_edit(self):
        sel = self['config'].getCurrent()[1]
        if sel and sel == cfg.cachefold:
            self.setting = 'cachefold'
            self.openDirectoryBrowser(cfg.cachefold.value)
        if sel and sel == cfg.movie:
            self.setting = 'moviefold'
            self.openDirectoryBrowser(cfg.movie.value)
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
                inhibitDirs=[
                    '/bin',
                    '/boot',
                    '/dev',
                    '/home',
                    '/lib',
                    '/proc',
                    '/run',
                    '/sbin',
                    '/sys',
                    '/var'],
                minFree=15)
        except Exception as e:
            print('openDirectoryBrowser get failed: ', e)

    def openDirectoryBrowserCB(self, path=None):
        if path is not None:
            if self.setting == 'cachefold':
                cfg.cachefold.setValue(path)
            if self.setting == 'moviefold':
                cfg.movie.setValue(path)
        return

    def save(self):
        if self['config'].isChanged():
            for x in self['config'].list:
                x[1].save()
            self.mbox = self.session.open(
                MessageBox,
                _('Settings saved correctly!'),
                MessageBox.TYPE_INFO,
                timeout=5)
            cfg.save()
            configfile.save()
        self.close()

    def extnok(self, answer=None):
        from Screens.MessageBox import MessageBox
        if answer is None:
            if self["config"].isChanged():
                self.session.openWithCallback(
                    self.extnok, MessageBox, _("Really close without saving settings?"))
            else:
                self.close()
        elif answer:
            for x in self["config"].list:
                x[1].cancel()
            self.close()
        return


class GridMain(Screen):
    def __init__(
            self,
            session,
            menuTitle,
            nextmodule,
            names,
            urls,
            infos,
            pics=[]):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        skin = os.path.join(skin_path, 'GridMain.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        title = menuTitle
        self.name = menuTitle
        self.nextmodule = nextmodule
        self["title"] = Button(title)
        self.pos = []

        if screenwidth.width() == 2560:
            self.pos.append([180, 80])
            self.pos.append([658, 80])
            self.pos.append([1134, 80])
            self.pos.append([1610, 80])
            self.pos.append([2084, 80])
            self.pos.append([180, 720])
            self.pos.append([658, 720])
            self.pos.append([1134, 720])
            self.pos.append([1610, 720])
            self.pos.append([2084, 720])

        elif screenwidth.width() == 1920:
            self.pos.append([122, 42])
            self.pos.append([478, 42])
            self.pos.append([834, 42])
            self.pos.append([1190, 42])
            self.pos.append([1546, 42])
            self.pos.append([122, 522])
            self.pos.append([478, 522])
            self.pos.append([834, 522])
            self.pos.append([1190, 522])
            self.pos.append([1546, 522])
        else:
            self.pos.append([95, 22])
            self.pos.append([335, 22])
            self.pos.append([555, 22])
            self.pos.append([795, 22])
            self.pos.append([1035, 22])
            self.pos.append([90, 342])
            self.pos.append([330, 342])
            self.pos.append([550, 342])
            self.pos.append([790, 345])
            self.pos.append([1030, 342])

        tmpfold = os.path.join(Path_Cache, "tmp")
        picfold = os.path.join(Path_Cache, "pic")

        picx = getpics(names, pics, tmpfold, picfold)
        # print("In Gridmain pics = ", pics)
        self.urls = urls
        self.pics = picx
        self.names = names
        self.infos = infos

        list = []
        list = names

        self["info"] = Label()
        self["menu"] = List(list)
        for x in list:
            print("x in list =", x)
        self["frame"] = MovingPixmap()

        self.PIXMAPS_PER_PAGE = 10
        i = 0
        while i < self.PIXMAPS_PER_PAGE:
            self["label" + str(i + 1)] = StaticText()
            self["pixmap" + str(i + 1)] = Pixmap()
            i += 1
        self.npics = len(self.names)
        self.npage = int(float(self.npics // self.PIXMAPS_PER_PAGE)) + 1
        self.index = 0
        self.maxentry = len(list) - 1
        self.ipage = 1

        self["actions"] = ActionMap(["OkCancelActions",
                                     "EPGSelectActions",
                                     "MenuActions",
                                     "DirectionActions",
                                     "NumberActions"],
                                    {"ok": self.okClicked,
                                     "epg": self.showIMDB,
                                     "info": self.showIMDB,
                                     "cancel": self.cancel,
                                     "left": self.key_left,
                                     "right": self.key_right,
                                     "up": self.key_up,
                                     "down": self.key_down})
        self.onLayoutFinish.append(self.openTest)

    def showIMDB(self):
        idx = self.index
        text_clear = self.names[idx]
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    def info(self):
        itype = self.index
        self.inf = self.infos[itype]
        # self.inf = ''
        try:
            self.inf = self.infos[itype]
        except BaseException:
            pass
        if self.inf:
            try:
                self["info"].setText(self.inf)
                # print('infos: ', self.inf)
            except BaseException:
                self["info"].setText('')
                # print('except info')
        print("In GridMain infos =", self.inf)

    def paintFrame(self):
        try:
            # If the index exceeds the maximum number of items, it returns to
            # the first item
            if self.index > self.maxentry:
                self.index = self.minentry
            self.idx = self.index
            name = self.names[self.idx]
            self['info'].setText(str(name))
            ifr = self.index - (self.PIXMAPS_PER_PAGE * (self.ipage - 1))
            ipos = self.pos[ifr]
            self["frame"].moveTo(ipos[0], ipos[1], 1)
            self["frame"].startMoving()
        except Exception as e:
            print('Error in paintFrame: ', e)

    def openTest(self):
        if self.ipage < self.npage:
            self.maxentry = (self.PIXMAPS_PER_PAGE * self.ipage) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE

        elif self.ipage == self.npage:
            self.maxentry = len(self.pics) - 1
            self.minentry = (self.ipage - 1) * self.PIXMAPS_PER_PAGE
            i1 = 0
            while i1 < self.PIXMAPS_PER_PAGE:
                self["label" + str(i1 + 1)].setText(" ")
                self["pixmap" + str(i1 + 1)].instance.setPixmapFromFile(dblank)
                i1 += 1
        self.npics = len(self.pics)
        i = 0
        i1 = 0
        self.picnum = 0
        ln = self.maxentry - (self.minentry - 1)
        while i < ln:
            idx = self.minentry + i
            # self["label" + str(i + 1)].setText(self.names[idx])  # this show
            # label to bottom of png pixmap
            pic = self.pics[idx]
            if not os.path.exists(self.pics[idx]):
                pic = dblank
            self["pixmap" + str(i + 1)].instance.setPixmapFromFile(pic)
            i += 1
        self.index = self.minentry
        self.paintFrame()

    def key_left(self):
        # Decrement the index only if we are not at the first pixmap
        if self.index >= 0:
            self.index -= 1
        else:
            # If we are at the first pixmap, go back to the last pixmap of the
            # last page
            self.ipage = self.npage
            self.index = self.npics - 1
        # Check if we need to change pages
        if self.index < self.minentry:
            self.ipage -= 1
            if self.ipage < 1:  # If we go beyond the first page
                self.ipage = self.npage
                self.index = self.npics - 1  # Back to the last pixmap of the last page
            self.openTest()
        else:
            self.paintFrame()

    def key_right(self):
        # Increment the index only if we are not at the last pixmap
        if self.index < self.npics - 1:
            self.index += 1
        else:
            # If we are at the last pixmap, go back to the first pixmap of the
            # first page
            self.index = 0
            self.ipage = 1
            self.openTest()
        # Check if we need to change pages
        if self.index > self.maxentry:
            self.ipage += 1
            if self.ipage > self.npage:  # If we exceed the number of pages
                self.index = 0
                self.ipage = 1  # Back to first page
            self.openTest()
        else:
            self.paintFrame()

    def key_up(self):
        if self.index >= 5:
            self.index -= 5
        else:
            if self.ipage > 1:
                self.ipage -= 1
                self.index = self.maxentry  # Back to the last line of the previous page
                self.openTest()
            else:
                # If we are on the first page, go back to the last pixmap of
                # the last page
                self.ipage = self.npage
                self.index = self.npics - 1
                self.openTest()
        self.paintFrame()

    def key_down(self):
        if self.index <= self.maxentry - 5:
            self.index += 5
        else:
            if self.ipage < self.npage:
                self.ipage += 1
                self.index = self.minentry  # Back to the top of the next page
                self.openTest()
            else:
                # If we are on the last page, go back to the first pixmap of
                # the first page
                self.index = 0
                self.ipage = 1
                self.openTest()
        self.paintFrame()

    def okClicked(self):
        itype = self.index
        url = self.urls[itype]
        name = self.names[itype]

        if name == _("Config"):
            self.session.open(ConfigEx)

        elif name == _("About"):
            self.session.open(Abouttvr)

        elif _('Search') in str(name):
            global search
            search = True
            # print('Search go movie: ', search)
            self.search_text(name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos1':
            # print("In GridMain Going in Videos1")
            try:
                vid2 = nextVideos1(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass
        elif '&page' not in str(url) and self.nextmodule == 'Videos1':
            # print('In GridMain video1 and play next sss  ', self.nextmodule)
            if 'tvseriesId' in str(url):
                try:
                    vid2 = Videos6(self.session, name, url)  # atv 6.5
                    vid2.startSession()
                except BaseException:
                    pass
            else:
                # print('In GridMain video1 and play next xx : ', self.nextmodule)
                self.session.open(Playstream1x, name, url)

        elif '&page' in str(url) and self.nextmodule == 'Videos4':
            # print("In GridMain Going in nextVideos4")
            try:
                vid2 = nextVideos4(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif 'listMovie' in str(url) and self.nextmodule == 'Videos4':
            # print("In GridMain Going listmovie in Videos4")
            try:
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif 'movieId' in str(url):  # and self.nextmodule == 'Videos4':
            # print('In GridMain videos5 moveid')
            try:
                vid2 = Videos5(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif self.nextmodule == "Play":
            # print("In GridMain Going in Playstream1x")
            try:
                self.session.open(Playstream1x, name, url)
            except BaseException:
                pass

        elif self.nextmodule == "PlaySeries":
            # print("In GridMain Going in PlaySeries")
            try:
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif self.nextmodule == "Videos2":
            # print("In GridMain Going in Videos2 name =", name)
            # print("In GridMain Going in Videos2 url =", url)
            try:
                vid2 = Videos2(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif self.nextmodule == "Videos3":
            # print("In GridMain Going in Videos3")
            try:
                vid2 = Videos3(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif self.nextmodule == "Videos4":
            # print("In GridMain Going in Videos4")
            try:
                vid2 = Videos4(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass

        elif self.nextmodule == "Videos5":
            # print("In GridMain Going in Videos5")
            try:
                vid2 = Videos5(self.session, name, url)
                vid2.startSession()
            except BaseException:
                pass
        else:
            self.close()

    def search_text(self, name, url):
        self.namex = name
        self.urlx = url
        self.session.openWithCallback(
            self.filterChannels,
            VirtualKeyBoard,
            title=_("Filter this category..."),
            text=name)

    def filterChannels(self, result=None):
        if result:
            name = str(result)
            url = self.urlx + str(result)
            try:
                vid2 = nextVideos4(self.session, name, url)
                vid2.startSession()
            except BaseException:
                return
        else:
            self.resetSearch()

    def resetSearch(self):
        global search
        search = False
        return

    def cancel(self):
        self.close()

    def exit(self):
        self.close()


class Videos2(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)
        self.name = name
        self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        response = json.loads(content)
        i = 0
        while i < 100:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(response["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)
                url = str(response["items"][i]["externallink"])
                pic = str(response["items"][i]["thumbnail"])
                if _('serie') not in self.name.lower():
                    pic = piconlocal(name)
                info = str(response["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)
                info = info.replace('---', ' ')
                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        title = name_plug
        if _("Live") in self.name:
            nextmodule = "Videos3"
        elif _("Film") in self.name:
            nextmodule = "Videos4"
        elif _("Serie") in self.name:
            nextmodule = "Videos1"

        if cfg.thumb.value == "True":
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class Videos6(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)

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
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i < 100:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(y["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)

                url = (y["items"][i]["link"])
                pic = (y["items"][i]["thumbnail"])
                info = str(y["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)

                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        nextmodule = "Videos1"
        if cfg.thumb.value == "True":
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class Videos1(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)
        self.name = name
        self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i < 100:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(y["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)

                url = (y["items"][i]["link"])
                pic = (y["items"][i]["thumbnail"])
                info = str(y["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)

                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        title = name_plug
        nextmodule = "Videos1"
        if cfg.thumb.value == "True":
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class nextVideos1(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)

        self.name = name
        self.url = url
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i < 100:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(y["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)
                url = (y["items"][i]["link"])
                pic = (y["items"][i]["thumbnail"])

                if _('serie') not in self.name.lower():
                    pic = piconlocal(name)

                info = str(y["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)

                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        title = name_plug
        nextmodule = "Videos1"
        if cfg.thumb.value == "True":
            print("In nextVideos1 Going in GridMain")
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class Videos3(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)

        self.name = name
        self.url = url
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i < 100:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(y["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)

                url = (y["items"][i]["link"])
                pic = (y["items"][i]["thumbnail"])
                info = str(y["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)

                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        title = name_plug
        nextmodule = "Play"
        if cfg.thumb.value == "True":
            print("In Videos3 Going in GridMain")
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class Videos4(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)

        self.name = name
        self.url = url
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i < 100:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(y["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)

                url = str(y["items"][i]["externallink"])
                pic = str(y["items"][i]["thumbnail"])
                info = str(y["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)

                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        title = name_plug
        nextmodule = "Videos5"
        if cfg.thumb.value == "True":
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class nextVideos4(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)

        self.name = name
        self.url = url
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i < 100:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(y["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)
                url = str(y["items"][i]["externallink"])
                pic = str(y["items"][i]["thumbnail"])
                info = str(y["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)

                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        title = name_plug
        nextmodule = "Videos4"
        if cfg.thumb.value == "True":
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class Videos5(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        self.list = []
        self["menu"] = List(self.list)
        self["menu"] = rvList([])
        self["title"] = Button(name)
        self["info"] = Label()
        self["info"].setText(title_plug)
        self["pixmap"] = Pixmap()
        self["key_red"] = Button(_("Cancel"))
        self["key_green"] = Button(_("Select"))
        self["actions"] = ActionMap(["WizardActions", "InputActions", "ColorActions", 'ButtonSetupActions', "DirectionActions"], {
                                    "ok": self.okClicked, "back": self.close, "red": self.close, "green": self.okClicked}, -1)

        self.name = name
        self.url = url
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.startSession)

    def startSession(self):
        self.names = []
        self.urls = []
        self.pics = []
        self.infos = []
        url = self.url
        content = Utils.ReadUrl2(url, referer)
        if PY3:
            content = six.ensure_str(content)
        y = json.loads(content)
        i = 0
        while i < 1:
            name = ""
            url = ""
            pic = ""
            try:
                name = str(y["items"][i]["title"])
                name = re.sub(r'\[.*?\]', "", name)
                name = Utils.cleanName(name)

                url = (y["items"][i]["link"])
                pic = (y["items"][i]["thumbnail"])
                info = str(y["items"][i]["info"])
                info = re.sub(r'\r\n', '', info)

                self.names.append(name)
                self.urls.append(url)
                self.pics.append(pic)
                self.infos.append(html_conv.html_unescape(info))
                i += 1
            except Exception as e:
                print(e)
                break

        title = name_plug
        nextmodule = "Play"
        print("In Videos5 nextmodule =", nextmodule)
        if cfg.thumb.value == "True":
            print("In Videos5 Going in GridMain")
            self.session.open(
                GridMain,
                title,
                nextmodule,
                self.names,
                self.urls,
                self.infos,
                pics=self.pics)

    def okClicked(self):
        pass


class TvInfoBarShowHide():
    """ InfoBar show/hide control, accepts toggleShow and hide actions, might start
    fancy animations. """
    STATE_HIDDEN = 0
    STATE_HIDING = 1
    STATE_SHOWING = 2
    STATE_SHOWN = 3
    skipToggleShow = False

    def __init__(self):
        self["ShowHideActions"] = ActionMap(["InfobarShowHideActions"], {
            "toggleShow": self.OkPressed,
            "hide": self.hide
        }, 0)

        self.__event_tracker = ServiceEventTracker(screen=self, eventmap={
            iPlayableService.evStart: self.serviceStarted
        })
        self.__state = self.STATE_SHOWN
        self.__locked = 0
        self.hideTimer = eTimer()
        try:
            self.hideTimer_conn = self.hideTimer.timeout.connect(
                self.doTimerHide)
        except BaseException:
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
        except BaseException:
            self.__locked = 0
        if self.execing:
            self.show()
            self.hideTimer.stop()
            self.skipToggleShow = False

    def unlockShow(self):
        try:
            self.__locked -= 1
        except BaseException:
            self.__locked = 0
        if self.__locked < 0:
            self.__locked = 0
        if self.execing:
            self.startHideTimer()

    def debug(obj, text=""):
        print(text + " %s\n" % obj)


class Playstream1x(Screen):
    def __init__(self, session, name, url):
        Screen.__init__(self, session)
        self.session = session
        global _session
        _session = session
        skin = os.path.join(skin_path, 'Playstream1x.xml')
        with codecs.open(skin, "r", encoding="utf-8") as f:
            self.skin = f.read()
        self.setup_title = ('Select Player Stream')
        self.list = []
        self['list'] = rvList([])
        self['info'] = Label()
        self['info'].setText(name)
        self['key_red'] = Button(_('Exit'))
        self['key_green'] = Button(_('Select'))
        self['progress'] = ProgressBar()
        self['progresstext'] = StaticText()
        self["progress"].hide()
        self.downloading = False
        self['actions'] = ActionMap(['MoviePlayerActions',
                                     'MovieSelectionActions',
                                     'ColorActions',
                                     'DirectionActions',
                                     'ButtonSetupActions',
                                     'OkCancelActions'],
                                    {'red': self.cancel,
                                     'green': self.okClicked,
                                     'back': self.cancel,
                                     'cancel': self.cancel,
                                     'leavePlayer': self.cancel,
                                     'rec': self.runRec,
                                     'instantRecord': self.runRec,
                                     'ShortRecord': self.runRec,
                                     'ok': self.okClicked},
                                    -2)

        self.name1 = name
        self.url = url
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.onLayoutFinish.append(self.openTest)
        return

    def runRec(self):
        self.namem3u = self.name1
        self.urlm3u = self.url
        if self.downloading is True:
            self.session.open(
                MessageBox,
                _('You are already downloading!!!'),
                MessageBox.TYPE_INFO,
                timeout=5)
            return
        else:
            if '.mp4' or '.mkv' or '.flv' or '.avi' in self.urlm3u:
                self.session.openWithCallback(
                    self.download_m3u, MessageBox, _(
                        "DOWNLOAD VIDEO?\n%s" %
                        self.namem3u), type=MessageBox.TYPE_YESNO, timeout=10, default=False)
            else:
                self.downloading = False
                self.session.open(
                    MessageBox,
                    _('Only VOD Movie allowed or not .ext Filtered!!!'),
                    MessageBox.TYPE_INFO,
                    timeout=5)

    def download_m3u(self, result=None):
        if result:
            path = urlparse(self.urlm3u).path
            ext = splitext(path)[1]
            if ext != '.mp4' or ext != '.mkv' or ext != '.avi' or ext != '.flv':  # or ext != 'm3u8':
                ext = '.mp4'
            fileTitle = re.sub(r'[\<\>\:\"\/\\\|\?\*\[\]]', '_', self.namem3u)
            fileTitle = re.sub(r' ', '_', fileTitle)
            fileTitle = re.sub(r'_+', '_', fileTitle)
            fileTitle = fileTitle.replace(
                "(",
                "_").replace(
                ")",
                "_").replace(
                "#",
                "").replace(
                "+",
                "_").replace(
                    "\'",
                    "_").replace(
                        "'",
                        "_").replace(
                            "!",
                            "_").replace(
                                "&",
                "_")
            fileTitle = fileTitle.replace(
                " ",
                "_").replace(
                ":",
                "").replace(
                "[",
                "").replace(
                "]",
                "").replace(
                    "!",
                    "_").replace(
                        "&",
                "_")
            fileTitle = fileTitle.lower() + ext
            self.in_tmp = os.path.join(Path_Movies, fileTitle)
            self.downloading = True
            self.download = downloadWithProgress(self.urlm3u, self.in_tmp)
            self.download.addProgress(self.downloadProgress)
            self.download.start().addCallback(self.check).addErrback(self.showError)

        else:
            self.downloading = False

    def downloadProgress(self, recvbytes, totalbytes):
        self["progress"].show()
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (
            recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes))

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
        self.session.open(
            MessageBox,
            _('Download Failed!!!'),
            MessageBox.TYPE_INFO,
            timeout=5)

    def openTest(self):
        url = self.url
        self.names = []
        self.urls = []
        self.names.append('Play Now')
        self.urls.append(url)
        self.names.append('Download Now')
        self.urls.append(url)
        self.names.append('Play HLS')
        self.urls.append(url)
        self.names.append('Play TS')
        self.urls.append(url)
        self.names.append('Streamlink')
        self.urls.append(url)
        showlist(self.names, self['list'])

    def okClicked(self):
        idx = self['list'].getSelectionIndex()
        if idx is not None or idx != -1:
            self.name = self.names[idx]
            self.url = self.urls[idx]

            if idx == 0:
                print('In playVideo url D=', self.url)
                self.play()

            elif idx == 1:
                print('In playVideo url D=', self.url)
                self.runRec()

            elif idx == 2:
                try:
                    os.remove('/tmp/hls.avi')
                except BaseException:
                    pass
                header = ''
                cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/tvspro/lib/hlsclient.py" "' + \
                    self.url + '" "1" "' + header + '" + &'
                print('In playVideo cmd =', cmd)
                os.system(cmd)
                os.system('sleep 3')
                self.url = '/tmp/hls.avi'
                self.play()
            elif idx == 3:
                url = self.url
                try:
                    os.remove('/tmp/hls.avi')
                except BaseException:
                    pass
                cmd = 'python "/usr/lib/enigma2/python/Plugins/Extensions/tvspro/l/tsclient.py" "' + url + '" "1" + &'
                print('hls cmd = ', cmd)
                os.system(cmd)
                os.system('sleep 3')
                self.url = '/tmp/hls.avi'
                self.play()
            else:
                if idx == 4:
                    print('In playVideo url D=', self.url)
                    self.play2()
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
        if Utils.isStreamlinkAvailable():
            desc = self.name
            name = self.name1
            url = self.url
            url = url.replace(':', '%3a')
            ref = '5002:0:1:0:0:0:0:0:0:0:' + \
                'http%3a//127.0.0.1%3a8088/' + str(url)
            sref = eServiceReference(ref)
            print('SREF: ', sref)
            sref.setName(self.name1)
            self.session.open(Playstream2, name, sref, desc)
            self.close()
        else:
            self.session.open(
                MessageBox,
                _('Install Streamlink first'),
                MessageBox.TYPE_INFO,
                timeout=5)

    def cancel(self):
        try:
            self.session.nav.stopService()
            self.session.nav.playService(self.srefInit)
            self.close()
        except BaseException:
            pass


class Playstream2(
        Screen,
        InfoBarMenu,
        InfoBarBase,
        InfoBarSeek,
        InfoBarNotifications,
        InfoBarAudioSelection,
        TvInfoBarShowHide,
        InfoBarSubtitleSupport):
    STATE_IDLE = 0
    STATE_PLAYING = 1
    STATE_PAUSED = 2
    ENABLE_RESUME_SUPPORT = True
    ALLOW_SUSPEND = True
    screen_timeout = 4000

    def __init__(self, session, name, url, desc):
        global streaml, _session
        _session = session
        streaml = False
        Screen.__init__(self, session)
        self.session = session
        self.skinName = 'MoviePlayer'
        InfoBarMenu.__init__(self)
        InfoBarNotifications.__init__(self)
        InfoBarBase.__init__(self, steal_current_service=True)
        TvInfoBarShowHide.__init__(self)
        InfoBarSubtitleSupport.__init__(self)
        InfoBarAudioSelection.__init__(self)
        try:
            self.init_aspect = int(self.getAspect())
        except BaseException:
            self.init_aspect = 0
        self.new_aspect = self.init_aspect
        self.srefInit = self.session.nav.getCurrentlyPlayingServiceReference()
        self.service = None
        self.allowPiP = False
        self.desc = desc
        self.url = url
        self.name = name
        self.state = self.STATE_PLAYING
        self['actions'] = ActionMap(['WizardActions',
                                     'MoviePlayerActions',
                                     'MovieSelectionActions',
                                     'MediaPlayerActions',
                                     'EPGSelectActions',
                                     'MediaPlayerSeekActions',
                                     'ColorActions',
                                     'ButtonSetupActions',
                                     'InfobarShowHideActions',
                                     'InfobarActions',
                                     'InfobarSeekActions'],
                                    {'leavePlayer': self.cancel,
                                     'epg': self.showIMDB,
                                     'info': self.showIMDB,
                                     'tv': self.cicleStreamType,
                                     'stop': self.leavePlayer,
                                     'cancel': self.cancel,
                                     'back': self.cancel},
                                    -1)
        InfoBarSeek.__init__(self, actionmap='InfobarSeekActions')

        if '8088' in str(self.url):
            self.onFirstExecBegin.append(self.slinkPlay)
        else:
            self.onFirstExecBegin.append(self.cicleStreamType)
        return

    def getAspect(self):
        try:
            aspect = AVSwitch().getAspectRatioSetting()
        except BaseException:
            pass
        return aspect

    def getAspectString(self, aspectnum):
        return {
            0: '4:3 Letterbox',
            1: '4:3 PanScan',
            2: '16:9',
            3: '16:9 always',
            4: '16:10 Letterbox',
            5: '16:10 PanScan',
            6: '16:9 Letterbox'
        }[aspectnum]

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
            AVSwitch.setAspectRatio(aspect)
        except BaseException:
            pass

    def av(self):
        temp = int(self.getAspect())
        temp += 1
        if temp > 6:
            temp = 0
        self.new_aspect = temp
        self.setAspect(temp)

    def showIMDB(self):
        text_clear = self.name
        if returnIMDB(text_clear):
            print('show imdb/tmdb')

    def slinkPlay(self):
        ref = str(self.url)
        ref = ref.replace(':', '%3a').replace(' ', '%20')
        print('final reference 1:   ', ref)
        ref = "{0}:{1}".format(ref, self.name)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def openPlay(self, servicetype, url):
        url = url.replace(':', '%3a').replace(' ', '%20')
        ref = str(servicetype) + ':0:1:0:0:0:0:0:0:0:' + \
            str(url)  # + ':' + self.name
        if streaml is True:
            ref = str(servicetype) + ':0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + \
                str(url) + ':' + self.name
        print('final reference 2:   ', ref)
        sref = eServiceReference(ref)
        sref.setName(self.name)
        self.session.nav.stopService()
        self.session.nav.playService(sref)

    def cicleStreamType(self):
        # global streaml
        from itertools import cycle, islice
        self.servicetype = str(cfg.services.value)
        print('servicetype1: ', self.servicetype)
        url = str(self.url)
        if str(splitext(url)[-1]) == ".m3u8":
            if self.servicetype == "1":
                self.servicetype = "4097"
        currentindex = 0
        streamtypelist = ["4097"]
        """
        # if "youtube" in str(self.url):
            # self.mbox = self.session.open(MessageBox, _('For Stream Youtube coming soon!'), MessageBox.TYPE_INFO, timeout=5)
            # return
        # if Utils.isStreamlinkAvailable():
            # streamtypelist.append("5002")  # ref = '5002:0:1:0:0:0:0:0:0:0:http%3a//127.0.0.1%3a8088/' + url
            # streaml = True
        # elif os.path.exists("/usr/bin/gstplayer"):
            # streamtypelist.append("5001")
        # if os.path.exists("/usr/bin/exteplayer3"):
            # streamtypelist.append("5002")
            """
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

    def showVideoInfo(self):
        if self.shown:
            self.hideInfobar()
        if self.infoCallback is not None:
            self.infoCallback()
        return

    def showAfterSeek(self):
        if isinstance(self, TvInfoBarShowHide):
            self.doShow()

    def cancel(self):
        if os.path.exists('/tmp/hls.avi'):
            os.remove('/tmp/hls.avi')
        self.session.nav.stopService()
        self.session.nav.playService(self.srefInit)
        if not self.new_aspect == self.init_aspect:
            try:
                self.setAspect(self.init_aspect)
            except BaseException:
                pass
        self.close()

    def leavePlayer(self):
        self.close()


def main(session, **kwargs):
    try:
        _session = session

        try:
            os.mkdir(os.path.join(Path_Cache, "pic"))
        except BaseException:
            pass

        try:
            os.mkdir(os.path.join(Path_Cache, "tmp"))
        except BaseException:
            pass

        exo = tvspromain(_session)
        exo.startSession()
    except BaseException:
        import traceback
        traceback.print_exc()
        pass


def Plugins(**kwargs):
    icona = 'icon.png'
    extDescriptor = PluginDescriptor(
        name=name_plug,
        description=_(title_plug),
        where=PluginDescriptor.WHERE_EXTENSIONSMENU,
        icon=icona,
        fnc=main)
    result = [
        PluginDescriptor(
            name=name_plug,
            description=title_plug,
            where=PluginDescriptor.WHERE_PLUGINMENU,
            icon=icona,
            fnc=main)]
    result.append(extDescriptor)
    return result
