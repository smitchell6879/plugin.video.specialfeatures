import os
import re
import sys
import sqlite3
import time
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import xml.etree.ElementTree as ET 
import json as simplejson


class dbFunctions:

    def vars(self):
        self.addon      = xbmcaddon.Addon()
        self.addir      = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/')
        self.adset      = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/settings.xml')
        self.dbdir      = xbmc.translatePath('special://userdata/addon_data/plugin.specialfeatures/specialfeatures.db')
        self.sysinfo    = {'window':str(xbmc.getInfoLabel('System.CurrentWindow'))}
        self.urlhandle  = "plugin://plugin.specialfeatures/?"
        self.handle     = "plugin://plugin.specialfeatures/" 
        self.url        = self.urlhandle + urlencode(self.sysinfo)
        self.home       = xbmcgui.Window(10000)
        self.monitor    = xbmc.Monitor()
        self.debug      = "true"
        self.dialog     = xbmcgui.Dialog()
        self.dialpro    = xbmcgui.DialogProgress()
        self.movielist  = []
        self.totals     = []
        self.cast       = []
        self.sf_extras  = []
        self.item       = ""
    def init_db(self):
        self.vars()
        if not xbmcvfs.exists(self.dbdir):
            xbmcvfs.mkdir(self.addir)
        self.dbcon      = sqlite3.connect(str(self.dbdir))
        self.dbcu       = self.dbcon.cursor()
        self.dbcu.execute('CREATE TABLE IF NOT EXISTS movies (m_file TEXT, m_title TEXT, m_year TEXT, m_plot TEXT, m_rating TEXT, m_mpaa TEXT, m_dateadded TEXT)')
        self.dbcu.execute('CREATE TABLE IF NOT EXISTS art (m_file TEXT, m_fanart TEXT, m_poster TEXT)')
        self.dbcu.execute('CREATE TABLE IF NOT EXISTS specialfeatures (m_file TEXT, m_title TEXT, m_path TEXT)')
        self.dbcu.execute('CREATE TABLE IF NOT EXISTS actors (m_file TEXT, m_name TEXT, m_thmbnail TEXT, m_role TEXT, m_order TEXT)')
        self.dbcon.commit()
        return
    def scn_db(self,updb='false'):
        self.cln_db(updb)
        # self.dialog.ok(self.addon.getLocalizedString(30000),self.addon.getLocalizedString(30010))
        self.get_db(updb)
        self.total_m=len(self.movielist)
        # self.dialog.ok(self.addon.getLocalizedString(30000),str(self.total_m)+self.addon.getLocalizedString(30011)) 
        if updb == 'false':
            self.dialpro.create(self.addon.getLocalizedString(30000),self.addon.getLocalizedString(30012)+str(self.total_m))
        self.pc = 1 
        for self.item in self.movielist:
            self.percent = float(self.pc)/float(self.total_m)*100 
            self.uid = self.item.get('uniqueid','')
            self.m_tmdb = self.uid.get('tmdb','')
            self.m_title = self.item.get('title','')
            self.m_year = self.item.get('year','')
            self.m_file = self.item.get('file','')
            self.art = self.item.get('art','')
            self.m_fanart = self.art.get('fanart','')
            self.m_poster = self.art.get('poster', '')
            self.m_cast = self.item.get('cast','')
            self.m_plot = self.item.get('plot','')
            self.m_rating = self.item.get('rating','')
            self.m_mpaa = self.item.get('mpaa','')
            self.m_dateadded = self.item.get('dateadded','')
            self.sf_extras = self.item.get('sf_extras','')
            if updb == 'false':
                if self.dialpro.iscanceled():
                    xbmc.executebuiltin('ActivateWindow(home)')
                    return
            for self.item in self.sf_extras:
                self.sf_title = self.item.get('sf_title','')
                self.sf_path = self.item.get('sf_path', '')
                self.dbcu.execute('SELECT * FROM specialfeatures WHERE m_path=?', (self.sf_path,))
                self.entry = self.dbcu.fetchone()
                if self.entry is None:
                    self.dbcu.execute('INSERT INTO specialfeatures VALUES (?,?,?)',(self.m_file, self.sf_title, self.sf_path))
                    self.dbcon.commit()
                self.dbcu.execute('SELECT * FROM movies WHERE m_file=?',(self.m_file,))
                self.entry = self.dbcu.fetchone()
                if self.entry is None:
                    self.dbcu.execute('INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?)', (self.m_file, self.m_title, self.m_year, self.m_plot, self.m_rating, self.m_mpaa, self.m_dateadded))
                    self.dbcon.commit()
                self.dbcu.execute('SELECT * FROM art WHERE m_file=?', (self.m_file,))
                self.entry = self.dbcu.fetchone()
                if self.entry is None:
                    self.dbcu.execute('INSERT INTO art VALUES (?, ?, ?)', (self.m_file, self.m_fanart, self.m_poster))
                    self.dbcon.commit()
                self.dbcu.execute('SELECT * FROM actors WHERE m_file=?', (self.m_file,))
                self.entry = self.dbcu.fetchone()
                if self.entry is None:
                    for self.item in self.m_cast:
                        self.m_name=self.item.get('name','')
                        self.m_thumbnail=self.item.get('thumbnail')
                        self.m_role=self.item.get('role')
                        self.m_order=self.item.get('order')
                        self.dbcu.execute('INSERT INTO actors VALUES (?, ?, ?, ?, ?)', (self.m_file, self.m_name, self.m_thumbnail, self.m_role, self.m_order))
                        self.dbcon.commit()
            if updb == 'false':
                self.dialpro.update(int(self.percent),"Updating Library {} out of {}".format(self.pc,self.total_m),"{} ({})".format(self.m_title,self.m_year),)
                self.pc+=1
        self.home.clearProperty('SF_updateing')
        if updb == 'false':
            xbmc.executebuiltin("Dialog.Close(all)")
            self.dialog.ok(self.addon.getLocalizedString(30000),self.addon.getLocalizedString(30013),self.addon.getLocalizedString(30014))
            xbmc.executebuiltin('ActivateWindow(Home)')
            # self.dialog.notification(self.addon.getLocalizedString(30000),self.addon.getLocalizedString(30013), xbmcgui.NOTIFICATION_INFO, 5000,False)
        self.log('Database Updated')
        return
    def log(self,txt):
        if isinstance(txt, str):
            self.txt = txt.decode('utf-8')
            self.adnme = self.addon.getLocalizedString(30000)
            self.message = u'%s: %s' % (self.adnme, self.txt)
            xbmc.log(msg=self.message.encode('utf-8'), level=xbmc.LOGDEBUG)
    def cln_db(self,updb='false'):
        self.init_db()
        self.home.setProperty('SF_updateing','true')
        self.dbcu.execute('SELECT * FROM specialfeatures')
        self.entry = self.dbcu.fetchall()
        for self.item in self.entry:
            self.chk=xbmcvfs.exists(self.item[2])
            if self.chk != 1:
                self.dbcu.execute('DELETE FROM specialfeatures WHERE m_path=?',(self.item[2],))
                self.dbcon.commit()
        self.dbcu.execute('SELECT * FROM movies')
        self.entry = self.dbcu.fetchall()
        self.total_m = len(self.entry)
        if self.total_m>0:
            self.pc = 1
            self.percent = float(self.pc)/float(self.total_m)*100 
            if updb == 'false':
                self.dialpro.create(self.addon.getLocalizedString(30000),"Cleaning Database")
            for self.item in self.entry:
                self.m_file = self.item[0]
                self.dbcu.execute('SELECT * FROM specialfeatures WHERE m_file=?',(self.m_file,))
                self.sentry = self.dbcu.fetchone()
                if self.sentry is None:
                    self.dbcu.execute('DELETE FROM movies WHERE m_file=?',(self.m_file,))
                    self.dbcu.execute('DELETE FROM actors WHERE m_file=?',(self.m_file,))
                    self.dbcu.execute('DELETE FROM art WHERE m_file=?',(self.m_file,))
                    self.dbcon.commit()
                if updb == 'false':
                    self.dialpro.update(int(self.percent),"Cleaning Database")
                    self.pc+=1
        if updb == 'false':
            self.dialog.notification(self.addon.getLocalizedString(30000),self.addon.getLocalizedString(30034), xbmcgui.NOTIFICATION_INFO, 1500,False)
        self.log('Database Cleaned')
        return
    def query_kdb(self):
        self.jsonq = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies","params": {"properties": ["title","genre","year","rating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art","userrating","ratings","premiered","uniqueid"], "sort": { "method": "label" } }, "id": 1}')
        self.jsonq = unicode(self.jsonq, 'utf-8', errors='ignore')
        self.json  = simplejson.loads(self.jsonq)
        self.log('Movies Fetched')
        return self.json
    def get_db(self,updb='false'):
        self.json = self.query_kdb()
        if self.json.has_key('result') and self.json['result'].has_key('movies'):
            for self.item in self.json['result']['movies']:
                self.m_title = self.item.get('title', '')
                self.totals.append(self.m_title)
            self.total_m = len(self.totals)
            if updb == 'false':
                self.dialpro.create(self.addon.getLocalizedString(30000),self.addon.getLocalizedString(30015))
                self.pc = 1
            for self.item in self.json['result']['movies']:
                self.percent = float(self.pc)/float(self.total_m)*100
                self.m_title = self.item.get('title', '')
                self.m_year  = self.item.get('year', '')
                self.m_file  = self.item.get('file', '')
                if updb == 'false':
                    self.dialpro.update(int(self.percent),self.addon.getLocalizedString(30015)+"{}".format(self.pc)+self.addon.getLocalizedString(30016)+"{}".format(self.total_m),"{} ({})".format(self.m_title,self.m_year),)
                    self.pc+=1
                    if self.dialpro.iscanceled():
                        xbmc.executebuiltin('ActivateWindow(Home)')
                        return
                if "BDMV" in self.m_file:
                    if "\BDMV" in self.m_file:
                        self.m_path, self.dump = self.m_file.strip().split("\BDMV")
                        self.m_path = self.m_path+"\\"+self.addon.getSetting('extras-folder')+"\\"
                    elif "/BDMV" in self.m_file:
                        self.m_path, self.dump = self.m_file.strip().split("/BDMV")
                        self.m_path = self.m_path+"/"+self.addon.getSetting('extras-folder')+"/"
                elif "VIDEO_TS" in self.m_file:
                    if "\VIDEO_TS" in self.m_file:
                        self.m_path, self.dump, self.dump = self.m_file.strip().split("\VIDEO_TS")
                        self.m_path = self.m_path+"\\"+self.addon.getSetting('extras-folder')+"\\"
                    elif "/VIDEO_TS" in self.m_file:
                        self.m_path, self.dump, self.dump = self.m_file.strip().split("/VIDEO_TS")
                        self.m_path = self.m_path+"/"+self.addon.getSetting('extras-folder')+"/"
                else:
                    self.m_=os.path.basename(self.m_file)
                    self.m_path, self.dump = self.m_file.strip().split(self.m_)
                    if "/" in self.m_file:
                        self.m_path = self.m_path+self.addon.getSetting('extras-folder')+"/"
                    else:
                        self.m_path = self.m_path+self.addon.getSetting('extras-folder')+"\\"
                #Video Found
                if xbmcvfs.exists(self.m_path):
                    self.sf_extras=list()
                    self.dirs, self.files = xbmcvfs.listdir(self.m_path)
                    for self.file in self.files:
                        self.skip = False
                        if self.addon.getSetting("excludefilestype") != "":
                            self.m = re.search(self.addon.getSetting("excludefilestype"), self.file)
                        else:
                            self.m = ""
                        if self.m:
                            self.skip = True
                        if not self.skip:
                            # _dialog.ok("",str(file))
                            self.sf_title = os.path.splitext(self.file)[0]
                            # _dialog.ok("",str(sf_title))
                            self.sf_path = self.m_path+self.file 
                            self.sf_extras.append({'sf_title': self.sf_title, 'sf_path': self.sf_path})
                    for self.sf_title in self.dirs:
                        if "/" in self.m_file:
                            self.dir = self.m_path+self.sf_title+"/"
                        else:
                            self.dir = self.m_path+self.sf_title+"\\"
                        self.dirs,self.files=xbmcvfs.listdir(self.dir)
                        for self.di in self.dirs:
                            if self.di == "BDMV":
                                if "/" in self.m_file:
                                    self.sf_path = self.dir+self.di+"/index.bdmv"
                                else:
                                    self.sf_path = self.dir+self.di+"\index.bdmv"
                                self.sf_extras.append({'sf_title': self.sf_title, 'sf_path': self.sf_path})
                            elif self.di == "VIDEO_TS":
                                if "/" in self.m_file:
                                    self.sf_path = self.dir+self.di+"/VIDEO_TS.IFO"
                                else:
                                    self.sf_path = self.dir+self.di+"\VIDEO_TS.IFO"
                                self.sf_extras.append({'sf_title': self.sf_title, 'sf_path': self.sf_path})                        
                    self.item.update({'sf_extras':self.sf_extras})
                    self.movielist.append(self.item)
            self.log('List Made')
            if updb == 'false':
                self.dialpro.close()
        if len(self.movielist) < 1:
            self.close()
        else:
            return self.movielist
    def close():    
        self.dialog.ok(self.addon.getLocalizedString(30003),self.addon.getLocalizedString(30004))
        xbmc.executebuiltin("ActivateWindow("+str(self.window)+")")
    def query_li(self):
        self.title = xbmc.getInfoLabel("ListItem.Label")
        self.path = xbmc.getInfoLabel("ListItem.FileNameAndPath")
        self.li_query(self.path)
        self.dbcon.close()
        return
    def li_query(self,path):
        self.init_db()
        self.m_file=path
        self.dbcu.execute('SELECT * FROM movies WHERE m_file=?', (self.m_file,))
        self.entry = self.dbcu.fetchall()
        for self.item in self.entry:
            self.nitem={'file':self.m_file, 'title':self.item[1], 'year':self.item[2], 'plot':self.item[3], 'rating':self.item[4], 'mpaa':self.item[5], 'dateadded':self.item[6]}
            self.dbcu.execute('SELECT * FROM art WHERE m_file=?', (self.m_file,))
            self.entry = self.dbcu.fetchall()
            for self.item in self.entry:
                self.art={'fanart':self.item[1], 'poster':self.item[2]}
                self.nitem.update({'art':self.art})
            self.dbcu.execute('SELECT * FROM specialfeatures WHERE m_file=?', (self.m_file,))
            self.entry = self.dbcu.fetchall()
            for self.item in self.entry:
                self.sf_extras.append({'sf_title': self.item[1], 'sf_path': self.item[2]})
            self.nitem.update({'sf_extras':self.sf_extras})
            self.dbcu.execute('SELECT * FROM actors WHERE m_file=?', (self.m_file,))
            self.entry = self.dbcu.fetchall()
            for self.item in self.entry:
                self.actor={'name'       : self.item[1],
                       'thumbnail'  : self.item[2],
                       'role'       : self.item[3],
                       'order'      : self.item[4],}            
                self.cast.append(self.actor)
            self.nitem.update({'cast':self.cast})
            self.movielist.append(self.nitem)
        if len(self.movielist) == 0:
            self.home.clearProperty('sf_info')
            self.home.clearProperty("extrasnxt")
        elif len(self.movielist) != 0:
            self.home.setProperty('sf_info','true')
            if self.addon.getSetting("context-menu") == "true":
                self.home.setProperty("extrasnxt", "true")
            else:
                self.home.clearProperty("extrasnxt")
        return
    def endcoding(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        return
    def get_url(self,**kwargs):
        self.handle     = "plugin://plugin.specialfeatures/" 
        return '{0}?{1}'.format(self.handle, urlencode(kwargs))
    def query_mfdb(self):
        self.init_db()
        self.dbcu.execute('SELECT * FROM movies')
        self.entry = self.dbcu.fetchall()
        for self.item in self.entry:
            self.m_file=self.item[0]
            self.new_item={'file':self.item[0], 'title':self.item[1], 'year':self.item[2], 'plot':self.item[3], 'rating':self.item[4], 'mpaa':self.item[5], 'dateadded':self.item[6]}
            self.dbcu.execute('SELECT * FROM art WHERE m_file=?', (self.m_file,))
            self.entry =self.dbcu.fetchall()
            for self.item in self.entry:
                self.art={'fanart':self.item[1], 'poster':self.item[2]}
                self.new_item.update({'art':self.art})
            self.dbcu.execute('SELECT * FROM specialfeatures WHERE m_file=?', (self.m_file,))
            self.entry =self.dbcu.fetchall()
            for self.item in self.entry:
                self.sf_extras.append({'sf_title': self.item[1], 'sf_path': self.item[2]})
            self.new_item.update({'sf_extras':self.sf_extras})
            self.dbcu.execute('SELECT * FROM actors WHERE m_file=?', (self.m_file,))
            self.entry = self.dbcu.fetchall()
            for self.item in self.entry:
                self.actor={'name'       : self.item[1],
                            'thumbnail'  : self.item[2],
                            'role'       : self.item[3],
                            'order'      : self.item[4],
                            }            
                self.cast.append(self.actor)
            self.new_item.update({'cast':self.cast})
            self.movielist.append(self.new_item)
        self.total_m=len(self.movielist)
        if self.total_m == 0:
            self.scan=self.dialog.yesno(self.addon.getLocalizedString(30000),self.addon.getLocalizedString(30003),self.addon.getLocalizedString(30004))
            if self.scan == 1:
                xbmc.executebuiltin("RunScript(plugin.specialfeatures,scandb)")
            else:
                return
        else:
            return self.movielist
    def query_sfdb(self,file):
        self.init_db()
        self.dbcu.execute('SELECT * FROM movies WHERE m_file=?', (file,))
        self.entry = self.dbcu.fetchall()
        for self.item in self.entry:
            self.new_item={'file':file, 'title':self.item[1], 'year':self.item[2], 'plot':self.item[3], 'rating':[4], 'mpaa':self.item[5], 'dateadded':self.item[6]}
            self.dbcu.execute('SELECT * FROM art WHERE m_file=?', (file,))
            self.entry = self.dbcu.fetchall()
            for self.item in self.entry:
                self.art={'fanart':self.item[1], 'poster':self.item[2]}
                self.new_item.update({'art':self.art})
            self.dbcu.execute('SELECT * FROM specialfeatures WHERE m_file=?', (file,))
            self.entry = self.dbcu.fetchall()
            for self.item in self.entry:
                self.sf_extras.append({'sf_title': self.item[1], 'sf_path': self.item[2]})
            self.new_item.update({'sf_extras':self.sf_extras})
            self.dbcu.execute('SELECT * FROM actors WHERE m_file=?', (file,))
            self.entry = self.dbcu.fetchall()
            for self.item in self.entry:
                self.actor={'name'       : self.item[1],
                            'thumbnail'  : self.item[2],
                            'role'       : self.item[3],
                            'order'      : self.item[4],
                            }            
                self.cast.append(self.actor)
            self.new_item.update({'cast':self.cast})
            self.movielist.append(self.new_item)
        return self.movielist