from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import object
from lib.parse import *
from lib.pymysql import *

# import xml.etree.ElementTree as ET 
import json
import os
import re
import sys
import sqlite3
# import lib.pymysql.cursors.DictCursor
import time
import datetime
import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import xbmcplugin


''' Addon Setup'''
addon      = xbmcaddon.Addon()
addonid    = addon.getAddonInfo("id")
addonpath  = addon.getAddonInfo("path")
addir      = xbmc.translatePath(addon.getAddonInfo("profile"))
adset      = xbmc.translatePath(os.path.join(addir,"settings.xml"))
dbdir      = xbmc.translatePath(os.path.join(addir,"specialfeatures.db"))
libdir     = xbmc.translatePath(os.path.join(addonpath,'lib'))
resdir     = xbmc.translatePath(os.path.join(addonpath,'resources'))
sqldir     = xbmc.translatePath(os.path.join(libdir,'pymysql'))

sys.path.append(libdir)
sys.path.append(resdir)
sys.path.append(sqldir)

'''GUI'''
home       = xbmcgui.Window(10000)
dialpro    = xbmcgui.DialogProgress()
dialbg     = xbmcgui.DialogProgressBG()
dialog     = xbmcgui.Dialog()        

''' Plugin'''
urlhandle  = "plugin://plugin.specialfeatures/?"
althandle  = "plugin://plugin.specialfeatures/" 

'''XBMC'''
monitor    = xbmc.Monitor()
play       = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

'''General'''
winid      = {'window':"{}".format(xbmc.getInfoLabel('System.CurrentWindow'))}
time1       = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:")
dbName     = 'specialfeatures'
charSet    = "utf8mb4"
cuType     = cursors.DictCursor

# url        = urlhandle + urlencode(winid)
debug      = "true"

'''List'''
folderlist  = []
bonus       = []
cast        = []
filelist    = []
# item       = ""

'''Settings'''
playall    = addon.getSetting('playall')
showalldir = addon.getSetting('showalldir')
moviedir   = addon.getSetting('moviedir')
tvshowdir  = addon.getSetting('tvshowdir')
aclndb     = addon.getSetting('aclndb')
aupdb      = addon.getSetting('aupdb')
folder     = addon.getSetting('folder')
sfmenu     = addon.getSetting('sfmenu')
exclude    = addon.getSetting('excludetypes')
mysql      = addon.getSetting('mysql')
user       = addon.getSetting('sqluser')
pword      = addon.getSetting('sqlpass')
ipadd      = addon.getSetting('sqlip')
ipport     = int(addon.getSetting('sqlport'))


def info(txt):
        '''Something has happed, basic action tracker'''
        # if isinstance(txt, str):
        txt = "{}".format(txt)
        message = u'%s: %s' % (addonid,txt)
        xbmc.log(msg=message, level=xbmc.LOGINFO)
def notice(txt):
        '''Something has happed, basic action tracker'''
        # if isinstance(txt, str):
        txt = "{}".format(txt)
        message = u'%s: %s' % (addonid,txt)
        xbmc.log(msg=message, level=xbmc.LOGNOTICE)
def warning(txt):
        '''Something bad happen may cause errors'''
        # if isinstance(txt, str):
        txt = "{}".format(txt)
        message = u'%s: %s' % (addonid,txt)
        xbmc.log(msg=message, level=xbmc.LOGWARNING)
def error(txt):
        '''addon is about to or has crashed this may be why'''
        # if isinstance(txt, str):
        txt = "{}".format(txt)
        message = u'%s: %s' % (addonid,txt)
        xbmc.log(msg=message, level=xbmc.LOGERROR)
def debug(txt):
        '''In depth infomation about the status of addon'''
        # if isinstance(txt, str):
        txt = "{}".format(txt)
        message = u'%s: %s' % (addonid,txt)
        xbmc.log(msg=message, level=xbmc.LOGDEBUG)
def encoding():
        reload(sys)
        sys.setdefaultencoding('utf-8')
        return
def lang(txt):
    return addon.getLocalizedString(txt)
def ok(txt="",top=lang(30000)):
    dialog.ok("{}".format(top),"{}".format(txt))
def text(txt="",top=lang(30000)):
    dialog.textviewer("{}".format(top),"{}".format(txt))
def note(top=lang(30000),txt="",time=1500,sound=False):
    dialog.notification(top,txt,time=time,sound=sound)
