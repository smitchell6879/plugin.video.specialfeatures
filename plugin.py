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
from libs.db_defaults import dbFunctions
import json as simplejson

dbF=dbFunctions()


class SpecialFeatures:
    def vars(self):
        self._url        = sys.argv[0]
        self._handle     = int(sys.argv[1])
        self._addon_dir  = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/')
        self._addon_set  = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/settings.xml')
        self._db_dir     = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/specialfeatures.db')
        self._addon      = xbmcaddon.Addon()
        self._play       = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        self._debug      = "true"
        self._dialog     = xbmcgui.Dialog()
        self._dialpro    = xbmcgui.DialogProgress()
        # self.movielist   = []
        self.totals      = []
        self.cast        = []
        self.sf_extras   = []
        self.item        = ""

    def list_moviefolders(self):
        # self.vars()
        xbmcplugin.setContent(self._handle, 'movies')
        self.movielist      = dbF.query_mfdb()
        for self.item in self.movielist:       
            self._listitem  = xbmcgui.ListItem(label=str(self.item.get('title', '')))
            self.art        = self.item.get('art','')
            self.fanart     = self.art.get('fanart','')
            self.poster     = self.art.get('poster', '')
            self.url        = self.get_url( title=str(self.item.get('title', '')), action='listing', category=str(self.item.get('file', '')))
            self.is_folder  = True
            self._listitem.setArt({'fanart': self.fanart, 'poster': self.poster})
            self._listitem.setProperty('IsPlayable', 'true')
            self._listitem.setCast(self.item.get('cast',''))
            self._listitem.setInfo('video',{'title': str(self.item.get('title', '')), 'year': str(self.item.get('year', '')), 'plot': self.item.get('plot', ''),'path': self.item.get('file',''), 'rating': self.item.get('rating', ''), 'mpaa': self.item.get('mpaa', ''), 'dateadded': self.item.get('dateadded', '')})
            xbmcplugin.addDirectoryItem(self._handle, self.url, self._listitem, self.is_folder)
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE )
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_MPAA_RATING )
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_VIDEO_YEAR )
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_VIDEO_RATING )
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_DATEADDED  )
        xbmcplugin.endOfDirectory(self._handle)
    def list_specialfeatures(self,category,title):
        self.vars()
        self.movielist=dbF.query_sfdb(category)
        xbmcplugin.setPluginCategory(self._handle, title)
        xbmcplugin.setContent(self._handle, 'movies')
        for self.item in self.movielist:     
            self.art        = self.item.get('art','')
            self.fanart     = self.art.get('fanart','')
            self.poster     = self.art.get('poster', '')
            self.year       = self.item.get('year','')
            self.plot       = self.item.get('plot','')
            self.cast       = self.item.get('cast','')
            self.path       = self.item.get('file','')
            self.rating     = self.item.get('rating','')
            self.mpaa       = self.item.get('mpaa','')
            self.dateadded  = self.item.get('dateadded','')
            self.sf_extras  = self.item.get('sf_extras', '')
            for self.item in self.sf_extras:
                self.title  = self.item.get('sf_title','')
                self.video  = self.item.get('sf_path','')
                self._listitem = xbmcgui.ListItem(label=title)
                self._listitem.setArt({'fanart': self.fanart, 'poster': self.poster})
                self._listitem.setProperty('IsPlayable', 'true')
                self._listitem.setCast(self.cast)
                self._listitem.setInfo('video',{'title':self.title, 'year': self.year, 'plot': self.plot, 'path':self.path, 'rating':self.rating, 'mpaa':self.mpaa, 'dateadded':self.dateadded})
                self.url = self.get_url(action='play', video=self.video)
                self.is_folder = False
                xbmcplugin.addDirectoryItem(self._handle, self.url, self._listitem, self.is_folder)
        if len(self.sf_extras) > 1:
            if self._addon.getSetting("play_all") == 'true':
                self._playall = xbmcgui.ListItem(label=self._addon.getLocalizedString(30025))
                self._playall.setArt({'fanart': self.fanart, 'poster': self.poster})
                self._playall.setProperty('IsPlayable', 'true')
                self._playall.setCast(self.cast)
                self._playall.setInfo('video',{'year': self.year, 'plot':self._addon.getLocalizedString(30038), 'path':self.path, 'rating':self.rating, 'mpaa':self.mpaa, 'dateadded':self.dateadded})
                self.url = self.get_url(action='playall', category=category)
                xbmcplugin.addDirectoryItem(self._handle,self.url, self._playall, self.is_folder)
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE )
        xbmcplugin.endOfDirectory(self._handle)
    def get_url(self,**kwargs):
        return '{0}?{1}'.format(self._url,urlencode(kwargs))
    def play_video(self,path):
        self.play_item = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(self._handle, True, listitem=self.play_item)
    def playlist(self,category):
        self.vars()
        self._play.clear()
        self.movielist = dbF.query_sfdb(category)
        for self.item in self.movielist:     
            self.art       = self.item.get('art','')
            self.fanart    = self.art.get('fanart','')
            self.poster    = self.art.get('poster', '')
            self.year      = self.item.get('year','')
            self.plot      = self.item.get('plot','')
            self.cast      = self.item.get('cast','')
            self.path      = self.item.get('file','')
            self.rating    = self.item.get('rating','')
            self.mpaa      = self.item.get('mpaa','')
            self.dateadded = self.item.get('dateadded','')
            self.sf_extras = self.item.get('sf_extras', '')
            for self.item in self.sf_extras:
                self.title=self.item.get('sf_title','')
                self.video=self.item.get('sf_path','')
                self._listitem = xbmcgui.ListItem(label=self.title)
                self._listitem.setArt({'fanart': self.fanart, 'poster': self.poster})
                self._listitem.setCast(self.cast)
                self._listitem.setInfo('video',{'title':self.title, 'year': self.year, 'plot': self.plot, 'path':self.path, 'rating':self.rating, 'mpaa':self.mpaa, 'dateadded':self.dateadded})
                self._play.add(url=self.video,listitem=self._listitem)
        xbmc.Player().play(self._play)
    def router(self,paramstring):
        self.vars()
        self.params = dict(parse_qsl(paramstring))
        if self.params:
            if paramstring.strip().split('=')[0]=='window':
                self.window = self.params.get('window','')
                self.list_moviefolders()
            elif self.params['action'] == 'listing':
                self.list_specialfeatures(self.params['category'], self.params['title'])
            elif self.params['action'] == 'play':
                self.play_video(self.params['video'])
            elif self.params['action'] == 'playall':
                self.playlist(self.params['category'])
            else:
                raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
        else:
            self.list_moviefolders()
if __name__ == '__main__':
    dbF.endcoding()
    SpecialFeatures().router(sys.argv[2][1:])


#### NOTES #####
# "title","genre","year","rating","director","trailer","tagline","plot","plotoutline",
# "originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country",
# "imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart",
# "thumbnail","file","sorttitle","resume","setid","dateadded","tag","art","userrating",
# "ratings","premiered","uniqueid"
#
#.encode('ascii', 'ignore')


# def init_db():
#     if not xbmcvfs.exists(_db_dir):
#         xbmcvfs.mkdir(_addon_dir)
#     global _db_con
#     _db_con = sqlite3.connect(str(_db_dir))
#     global _db_cu
#     _db_cu  = _db_con.cursor()
#     _db_cu.execute('CREATE TABLE IF NOT EXISTS movies (m_fileb TEXT, m_title TEXT, m_year TEXT, m_plot TEXT, m_rating TEXT, m_mpaa TEXT, m_dateadded TEXT)')
#     _db_cu.execute('CREATE TABLE IF NOT EXISTS art (m_tfile TEXT, m_fanart TEXT, m_poster TEXT)')
#     _db_cu.execute('CREATE TABLE IF NOT EXISTS specialfeatures (m_tfile TEXT, m_title TEXT, m_path TEXT)')
#     _db_cu.execute('CREATE TABLE IF NOT EXISTS actors (m_tfile TEXT, m_name TEXT, m_thmbnail TEXT, m_role TEXT, m_order TEXT)')
#     _db_con.commit()
#     return
# def query_sdb():
#     dbF.init_db()
#     _db_cu.execute('SELECT * FROM movies')
#     _entry = _db_cu.fetchall()
#     for item in _entry:
#         m_file=item[0]
#         new_item={'file':item[0], 'title':item[1], 'year':item[2], 'plot':item[3], 'rating':[4], 'mpaa':[5], 'dateadded':[6]}
#         _db_cu.execute('SELECT * FROM art WHERE m_file=?', (m_file,))
#         _entry = _db_cu.fetchall()
#         for item in _entry:
#             art={'fanart':item[1], 'poster':item[2]}
#             new_item.update({'art':art})
#         _db_cu.execute('SELECT * FROM specialfeatures WHERE m_file=?', (m_file,))
#         _entry = _db_cu.fetchall()
#         for item in _entry:
#             sf_extras.append({'sf_title': item[1], 'sf_path': item[2]})
#         new_item.update({'sf_extras':sf_extras})
#         _db_cu.execute('SELECT * FROM actors WHERE m_file=?', (m_file,))
#         _entry = _db_cu.fetchall()
#         for item in _entry:
#             actor={'name'       : item[1],
#                    'thumbnail'  : item[2],
#                    'role'       : item[3],
#                    'order'      : item[4],}            
#             cast.append(actor)
#         new_item.update({'cast':cast})
#         movielist.append(new_item)
#     total_m=len(movielist)
#     if total_m == 0:
#         close()
#     else:
#         return movielist
# def query_sfdb(file):
#     init_db()
#     m_file=file
#     _db_cu.execute('SELECT * FROM movies WHERE m_file=?', (m_file,))
#     _entry = _db_cu.fetchall()
#     for item in _entry:
#         new_item={'file':m_file, 'title':item[1], 'year':item[2], 'plot':item[3], 'rating':[4], 'mpaa':[5], 'dateadded':[6]}
#         _db_cu.execute('SELECT * FROM art WHERE m_file=?', (m_file,))
#         _entry = _db_cu.fetchall()
#         for item in _entry:
#             art={'fanart':item[1], 'poster':item[2]}
#             new_item.update({'art':art})
#         _db_cu.execute('SELECT * FROM specialfeatures WHERE m_file=?', (m_file,))
#         _entry = _db_cu.fetchall()
#         for item in _entry:
#             sf_extras.append({'sf_title': item[1], 'sf_path': item[2]})
#         new_item.update({'sf_extras':sf_extras})
#         _db_cu.execute('SELECT * FROM actors WHERE m_file=?', (m_file,))
#         _entry = _db_cu.fetchall()
#         for item in _entry:
#             actor={'name'       : item[1],
#                    'thumbnail'  : item[2],
#                    'role'       : item[3],
#                    'order'      : item[4],}            
#             cast.append(actor)
#         new_item.update({'cast':cast})
#         movielist.append(new_item)
#     return movielist
# def close():    
#         scan=_dialog.yesno(_addon.getLocalizedString(30000),_addon.getLocalizedString(30003),_addon.getLocalizedString(30004))
#         if scan == 1:
#             xbmc.executebuiltin("RunScript(plugin.specialfeatures,scandb)")

