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

_url        = sys.argv[0]
_handle     = int(sys.argv[1])
_addon_dir  = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/')
_addon_set  = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/settings.xml')
_db_dir     = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/specialfeatures.db')
_addon      = xbmcaddon.Addon()
_play       = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
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
    _db_cu.execute('CREATE TABLE IF NOT EXISTS movies (m_fileb TEXT, m_title TEXT, m_year TEXT, m_plot TEXT, m_rating TEXT, m_mpaa TEXT, m_dateadded TEXT)')
    _db_cu.execute('CREATE TABLE IF NOT EXISTS art (m_tfile TEXT, m_fanart TEXT, m_poster TEXT)')
    _db_cu.execute('CREATE TABLE IF NOT EXISTS specialfeatures (m_tfile TEXT, m_title TEXT, m_path TEXT)')
    _db_cu.execute('CREATE TABLE IF NOT EXISTS actors (m_tfile TEXT, m_name TEXT, m_thmbnail TEXT, m_role TEXT, m_order TEXT)')
    _db_con.commit()
    return
def query_sdb():
    init_db()
    _db_cu.execute('SELECT * FROM movies')
    _entry = _db_cu.fetchall()
    for item in _entry:
        m_file=item[0]
        new_item={'file':item[0], 'title':item[1], 'year':item[2], 'plot':item[3], 'rating':[4], 'mpaa':[5], 'dateadded':[6]}
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
    total_m=len(movielist)
    if total_m == 0:
        close()
    else:
        return movielist
def query_sfdb(file):
    init_db()
    m_file=file
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
    return movielist
def close():    
        scan=_dialog.yesno(_addon.getLocalizedString(30000),_addon.getLocalizedString(30003),_addon.getLocalizedString(30004))
        if scan == 1:
            xbmc.executebuiltin("RunScript(plugin.specialfeatures,scandb)")
def list_moviefolders():
    xbmcplugin.setContent(_handle, 'movies')
    query_sdb()
    for item in movielist:       
        _listitem = xbmcgui.ListItem(label=str(item.get('title', '')))
        art = item.get('art','')
        fanart = art.get('fanart','')
        poster = art.get('poster', '')
        _listitem.setArt({'fanart': fanart, 'poster': poster})
        _listitem.setProperty('IsPlayable', 'true')
        _listitem.setCast(item.get('cast',''))
        _listitem.setInfo('video',{'title': str(item.get('title', '')), 'year': str(item.get('year', '')), 'plot': item.get('plot', ''),'path': item.get('file',''), 'rating': item.get('rating', ''), 'mpaa': item.get('mpaa', ''), 'dateadded': item.get('dateadded', '')})
        url = get_url( title=str(item.get('title', '')), action='listing', category=str(item.get('file', '')))
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, _listitem, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE )
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_MPAA_RATING )
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_VIDEO_YEAR )
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_DATEADDED  )
    xbmcplugin.endOfDirectory(_handle)
def list_specialfeatures(category,title):
    query_sfdb(category)
    xbmcplugin.setPluginCategory(_handle, title)
    xbmcplugin.setContent(_handle, 'movies')
    for item in movielist:     
        art       = item.get('art','')
        fanart    = art.get('fanart','')
        poster    = art.get('poster', '')
        year      = item.get('year','')
        plot      = item.get('plot','')
        cast      = item.get('cast','')
        path      = item.get('file','')
        rating    = item.get('rating','')
        mpaa      = item.get('mpaa','')
        dateadded = item.get('dateadded','')
        sf_extras = item.get('sf_extras', '')
        for item in sf_extras:
            title=item.get('sf_title','')
            video=item.get('sf_path','')
            _listitem = xbmcgui.ListItem(label=title)
            _listitem.setArt({'fanart': fanart, 'poster': poster})
            _listitem.setProperty('IsPlayable', 'true')
            _listitem.setCast(cast)
            _listitem.setInfo('video',{'title':title, 'year': year, 'plot': plot, 'path':path, 'rating':rating, 'mpaa':mpaa, 'dateadded':dateadded})
            url = get_url(action='play', video=video)
            is_folder = False
            xbmcplugin.addDirectoryItem(_handle, url, _listitem, is_folder)
    if _addon.getSetting("play_all") == 'true':
        _playall = xbmcgui.ListItem(label="Play All")
        url = get_url(action='playall', category=category)
        xbmcplugin.addDirectoryItem(_handle, url, _playall, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE )
    xbmcplugin.endOfDirectory(_handle)
def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))
def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)
def playlist(category):
    query_sfdb(category)
    _play.clear()
    for item in movielist:     
        art       = item.get('art','')
        fanart    = art.get('fanart','')
        poster    = art.get('poster', '')
        year      = item.get('year','')
        plot      = item.get('plot','')
        cast      = item.get('cast','')
        path      = item.get('file','')
        rating    = item.get('rating','')
        mpaa      = item.get('mpaa','')
        dateadded = item.get('dateadded','')
        sf_extras = item.get('sf_extras', '')
        for item in sf_extras:
            title=item.get('sf_title','')
            video=item.get('sf_path','')
            _listitem = xbmcgui.ListItem(label=title)
            _listitem.setArt({'fanart': fanart, 'poster': poster})
            _listitem.setCast(cast)
            _listitem.setInfo('video',{'title':title, 'year': year, 'plot': plot, 'path':path, 'rating':rating, 'mpaa':mpaa, 'dateadded':dateadded})
            _play.add(url=video,listitem=_listitem)
    xbmc.Player().play(_play)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if paramstring.strip().split('=')[0]=='window':
            global window
            window = params.get('window','')
            list_moviefolders()
        elif params['action'] == 'listing':
            list_specialfeatures(params['category'], params['title'])
        elif params['action'] == 'play':
            play_video(params['video'])
        elif params['action'] == 'playall':
            playlist(params['category'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_moviefolders()
if __name__ == '__main__':
    router(sys.argv[2][1:])


#### NOTES #####
# "title","genre","year","rating","director","trailer","tagline","plot","plotoutline",
# "originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country",
# "imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart",
# "thumbnail","file","sorttitle","resume","setid","dateadded","tag","art","userrating",
# "ratings","premiered","uniqueid"


