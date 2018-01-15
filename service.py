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
_monitor    = xbmc.Monitor()
_debug      = "true"
_dialog     = xbmcgui.Dialog()
_dialpro    = xbmcgui.DialogProgress()
movielist   = []
totals      = []
cast        = []
sf_extras   = []
item        = ""


def init_db():
    if not xbmcvfs.exists(_db_dir):
        xbmcvfs.mkdir(_addon_dir)
    global _db_con
    _db_con = sqlite3.connect(str(_db_dir))
    global _db_cu
    _db_cu  = _db_con.cursor()
    _db_cu.execute('CREATE TABLE IF NOT EXISTS movies (m_file TEXT, m_title TEXT, m_year TEXT, m_plot TEXT, m_rating TEXT, m_mpaa TEXT, m_dateadded TEXT)')
    _db_cu.execute('CREATE TABLE IF NOT EXISTS art (m_file TEXT, m_fanart TEXT, m_poster TEXT)')
    _db_cu.execute('CREATE TABLE IF NOT EXISTS specialfeatures (m_file TEXT, m_title TEXT, m_path TEXT)')
    _db_cu.execute('CREATE TABLE IF NOT EXISTS actors (m_file TEXT, m_name TEXT, m_thmbnail TEXT, m_role TEXT, m_order TEXT)')
    _db_con.commit()
    return
def li_query(path):
    init_db()
    m_file=path
    movielist=[]
    _db_cu.execute('SELECT * FROM movies WHERE m_file=?', (m_file,))
    _entry = _db_cu.fetchall()
    for item in _entry:
        new_item={'file':m_file, 'title':item[1], 'year':item[2], 'plot':item[3], 'rating':[4], 'mpaa':[5], 'dateadded':[6]}
        _db_cu.execute('SELECT * FROM art WHERE m_file=?', (m_file,))
        _entry = _db_cu.fetchall()
        for item in _entry:
            art={'fanart':item[1], 'poster':item[2]}
            new_item.update({'art':art})
        _db_cu.execute('SELECT * FROM specialfeatures WHERE m_file=?', (m_file,))
        _entry = _db_cu.fetchall()
        for item in _entry:
            sf_extras.append({'sf_title': item[1], 'sf_path': item[2]})
        new_item.update({'sf_extras':sf_extras})
        _db_cu.execute('SELECT * FROM actors WHERE m_file=?', (m_file,))
        _entry = _db_cu.fetchall()
        for item in _entry:
            actor={'name'       : item[1],
                   'thumbnail'  : item[2],
                   'role'       : item[3],
                   'order'      : item[4],}            
            cast.append(actor)
        new_item.update({'cast':cast})
        movielist.append(new_item)
    if len(movielist) == 0:
        _home.clearProperty('sf_info')
        _home.clearProperty("extrasnxt")
    elif len(movielist) != 0:
        _home.setProperty('sf_info','true')
        if _addon.getSetting("context-menu") == "true":
            _home.setProperty("extrasnxt", "true")
        else:
            _home.clearProperty("extrasnxt")

    return
def query_li():
    title = xbmc.getInfoLabel("ListItem.Label")
    path = xbmc.getInfoLabel("ListItem.FileNameAndPath")
    li_query(path)
    _db_con.close()
    return


def main():
    while not _monitor.abortRequested():
        if _home.getProperty('SF_upadateing') != 'true': 
            try:
                query_li()
            except:
                pass
        if _monitor.waitForAbort(.6):
            break


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()

    

