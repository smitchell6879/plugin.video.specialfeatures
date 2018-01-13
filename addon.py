import inspect
import os
import re
import sys
import sqlite3
import time
from urllib import urlencode
from urlparse import parse_qsl
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import xml.etree.ElementTree as ET 

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

_addon      = xbmcaddon.Addon()
_addon_dir  = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/')
_addon_set  = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/settings.xml')
_db_dir     = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/specialfeatures.db')
_sys_info   = {'window':str(xbmc.getInfoLabel('System.CurrentWindow'))}
_url_handle = "plugin://plugin.specialfeatures/?"
_handle     = "plugin://plugin.specialfeatures/" 
_url        = _url_handle + urlencode(_sys_info)
_home       = xbmcgui.Window(10000)
_debug      = "true"
_dialog     = xbmcgui.Dialog()
_dialpro    = xbmcgui.DialogProgress()
movielist   = []
totals      = []
cast        = []
sf_extras   = []
item        = ""

def main():
    title = xbmc.getInfoLabel("ListItem.Label")
    path = xbmc.getInfoLabel("ListItem.FileNameAndPath")
    url = get_url( title=str(title), action='listing', category=str(path))
    xbmc.executebuiltin('DialogBusy')

    if xbmcgui.getCurrentWindowId() == 10025:
            xbmc.executebuiltin('Container.Update(\"%s\",return)' % url)
    else:
        xbmc.executebuiltin('ActivateWindow(videos, \"%s\",return)' % url)
def get_url(**kwargs):
    return '{0}?{1}'.format(_handle, urlencode(kwargs))




    


if __name__ == '__main__':
    main()