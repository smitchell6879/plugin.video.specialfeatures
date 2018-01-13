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


def init_db():
    _dialog.ok(_addon.getLocalizedString(30000),_addon.getLocalizedString(30010))
    _home.setProperty('SF_upadateing','true')
    _db_done=xbmcvfs.delete(_db_dir)
    get_movielist()
    total_m=len(movielist)
    _dialog.ok(_addon.getLocalizedString(30000),str(total_m)+_addon.getLocalizedString(30011)) 
    _dialpro.create(_addon.getLocalizedString(30000),_addon.getLocalizedString(30012)+str(total_m))
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
    pc = 1  
    for item in movielist:
        percent = float(pc)/float(total_m)*100 
        uid = item.get('uniqueid','')
        m_tmdb = uid.get('tmdb','')
        m_title = item.get('title','')
        m_year = item.get('year','')
        m_file = str(item.get('file',''))
        art = item.get('art','')
        m_fanart = art.get('fanart','')
        m_poster = art.get('poster', '')
        m_cast = item.get('cast','')
        m_plot = item.get('plot','')
        m_rating = item.get('rating','')
        m_mpaa = item.get('mpaa','')
        m_dateadded = item.get('dateadded','')
        # m_genre = item.get('genre','')
        # for item in m_genre:
        #     _dialog.textviewer("",str(item))
        sf_extras = item.get('sf_extras','')
        if _dialpro.iscanceled():
            xbmc.executebuiltin('ActivateWindow(home)')
            return
        _db_cu.execute('SELECT * FROM movies WHERE m_file=?', (m_file,))
        _entry = _db_cu.fetchone()
        if _entry is None:
            _db_cu.execute('INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?)', (m_file, m_title, m_year, m_plot, m_rating, m_mpaa, m_dateadded))
            _db_con.commit()
        _db_cu.execute('SELECT * FROM art WHERE m_file=?', (m_file,))
        _entry = _db_cu.fetchone()
        if _entry is None:
            _db_cu.execute('INSERT INTO art VALUES (?, ?, ?)', (m_file, m_fanart, m_poster))
            _db_con.commit()
        _db_cu.execute('SELECT * FROM specialfeatures WHERE m_file=?', (m_file,))
        _entry = _db_cu.fetchone()
        if _entry is None:
            for item in sf_extras:
                sf_title = item.get('sf_title','')
                sf_path = item.get('sf_path', '')
                _db_cu.execute('INSERT INTO specialfeatures VALUES (?, ?, ?)', (m_file, sf_title, sf_path))
                _db_con.commit()
        _db_cu.execute('SELECT * FROM actors WHERE m_file=?', (m_file,))
        _entry = _db_cu.fetchone()
        if _entry is None:
            for item in m_cast:
                m_thumbnail=''
                m_name=item.get('name','')
                m_thumbnail=item.get('thumbnail')
                m_role=item.get('role')
                m_order=item.get('order')
                _db_cu.execute('INSERT INTO actors VALUES (?, ?, ?, ?, ?)', (m_file, m_name, m_thumbnail, m_role, m_order))
                _db_con.commit()
        _dialpro.update(int(percent),"Updating Library {} out of {}".format(pc,total_m),"{} ({})".format(m_title,m_year),)
        pc+=1
    xbmc.executebuiltin("Dialog.Close(all)")
    _home.clearProperty('SF_upadateing')
    _dialog.ok(_addon.getLocalizedString(30000),_addon.getLocalizedString(30013),_addon.getLocalizedString(30014))
    xbmc.executebuiltin('ActivateWindow(Home)')
    return
def query_db():
    json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies","params": {"properties": ["title","genre","year","rating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art","userrating","ratings","premiered","uniqueid"], "sort": { "method": "label" } }, "id": 1}')
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    jsonobject = simplejson.loads(json_query)
    return jsonobject
def get_movielist():
    jsonobject = query_db()
    if jsonobject.has_key('result') and jsonobject['result'].has_key('movies'):
        for item in jsonobject['result']['movies']:
            m_title = item.get('title', '')
            totals.append(m_title)
        total_m = len(totals)
        _dialpro.create(_addon.getLocalizedString(30000), 'Scanning Library')
        pc = 1
        for item in jsonobject['result']['movies']:
            percent = float(pc)/float(total_m)*100
            m_title = item.get('title', '')
            m_year  = str(item.get('year', ''))
            m_file  = str(item.get('file', ''))
            _dialpro.update(int(percent),_addon.getLocalizedString(30015)+"{}"+_addon.getLocalizedString(30016)+"{}".format(pc,total_m),"{} ({})".format(m_title,m_year),)
            pc+=1
            if _dialpro.iscanceled():
                xbmc.executebuiltin('ActivateWindow(Home)')
                return
            if "BDMV" in m_file:
                if "\BDMV" in m_file:
                    m_path, dump = m_file.strip().split("\BDMV")
                    m_path = m_path+"\\"+_addon.getSetting('extras-folder')+"\\"
                elif "/BDMV" in m_file:
                    m_path, dump = m_file.strip().split("/BDMV")
                    m_path = m_path+"/"+_addon.getSetting('extras-folder')+"/"
            elif "VIDEO_TS" in m_file:
                if "\VIDEO_TS" in m_file:
                    m_path, dump, dump = m_file.strip().split("\VIDEO_TS")
                    m_path = m_path+"\\"+_addon.getSetting('extras-folder')+"\\"
                elif "/VIDEO_TS" in m_file:
                    m_path, dump, dump = m_file.strip().split("/VIDEO_TS")
                    m_path = m_path+"/"+_addon.getSetting('extras-folder')+"/"
            else:
                m_=os.path.basename(m_file)
                m_path, dump = m_file.strip().split(m_)
                if "/" in m_file:
                    m_path = m_path+_addon.getSetting('extras-folder')+"/"
                else:
                    m_path = m_path+_addon.getSetting('extras-folder')+"\\"
            if xbmcvfs.exists(m_path):
                sf_extras=list()
                dirs, files = xbmcvfs.listdir(m_path)
                for file in files:
                    skip = False
                    if _addon.getSetting("excludefilestype") != "":
                        m = re.search(_addon.getSetting("excludefilestype"), file)
                    else:
                        m = ""
                    if m:
                        skip = True
                    if not skip:
                        # _dialog.ok("",str(file))
                        sf_title = os.path.splitext(file)[0]
                        # _dialog.ok("",str(sf_title))
                        sf_path = m_path+file 
                        sf_extras.append({'sf_title': sf_title, 'sf_path': sf_path})
                for sf_title in dirs:
                    if "/" in m_file:
                        _dir = m_path+sf_title+"/"
                    else:
                        _dir = m_path+sf_title+"\\"
                    dirs,files=xbmcvfs.listdir(_dir)
                    for _dir_ in dirs:
                        if _dir_ == "BDMV":
                            if "/" in m_file:
                                sf_path = _dir+_dir_+"/index.bdmv"
                            else:
                                sf_path = _dir+_dir_+"\index.bdmv"
                            sf_extras.append({'sf_title': sf_title, 'sf_path': sf_path})
                        elif _dir_ == "VIDEO_TS":
                            if "/" in m_file:
                                sf_path = _dir+_dir_+"/VIDEO_TS.IFO"
                            else:
                                sf_path = _dir+_dir_+"\VIDEO_TS.IFO"
                            sf_extras.append({'sf_title': sf_title, 'sf_path': sf_path})                        
                item.update({'sf_extras':sf_extras})
                movielist.append(item)
        _dialpro.close()
    if len(movielist) < 1:
        close()
    else:
        return movielist
def close():    
        _dialog.ok(_addon.getLocalizedString(30003),_addon.getLocalizedString(30004))
        xbmc.executebuiltin("ActivateWindow("+str(window)+")")
def query_li():
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
def context():
    addon_data=xbmcvfs.exists(_addon_set)
    status=_addon.getSetting("context-menu")
    if status == "true":
        status=_addon.getLocalizedString(30052)
        yes=_addon.getLocalizedString(30055)
    else:
        status=_addon.getLocalizedString(30053)
        yes=_addon.getLocalizedString(30054)
    menu=_dialog.yesno(_addon.getLocalizedString(30056),_addon.getLocalizedString(30057)+" "+str(status),yeslabel=yes,nolabel=_addon.getLocalizedString(30058)) 
    
    if status == _addon.getLocalizedString(30052) and menu == 1:
        if addon_data:
            read = ET.parse(_addon_set)
            line = read.getroot()
            for line in line:
                l = line.attrib
                l = l.get('id')
                if l == 'context-menu':
                    li=line.text
                    if li == 'true':
                        # line.text = str('false')
                        # read.write(_addon_set)
                        _addon.setSetting(id='context-menu', value='false')
                        _dialog.ok(_addon.getLocalizedString(30000),_addon.getLocalizedString(30017)) 
                        return
            
    elif status == _addon.getLocalizedString(30053) and menu == 1:
        if addon_data:
            read = ET.parse(_addon_set)
            line = read.getroot()
            for line in line:
                l = line.attrib
                l = l.get('id')
                if l == 'context-menu':
                    li=line.text
                    if li == 'false':
                        # line.text = str('true')
                        # read.write(_addon_set)
                        _addon.setSettingBool(id='context-menu',value=1)
                        _dialog.ok(_addon.getLocalizedString(30000),_addon.getLocalizedString(30017)) 

                        return
    else:
        return

if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1] == 'scandb':
            init_db()
        elif sys.argv[1] == 'listitem':
            query_li()
        elif sys.argv[1] == 'quit':
            context()
	else:
		if xbmcgui.getCurrentWindowId() == 10025:
			xbmc.executebuiltin('Container.Update(\"%s\",return)' % _url)
		else:
			xbmc.executebuiltin('ActivateWindow(videos, \"%s\",return)' % _url)

    

