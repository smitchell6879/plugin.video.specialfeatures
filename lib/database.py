from lib.sys_init import *
from lib.build_list import *

def tables():
    TABLES= {   'movies'             :'CREATE TABLE IF NOT EXISTS movies (m_file TEXT, m_title TEXT, m_year TEXT, m_plot TEXT, m_rating TEXT, m_mpaa TEXT, m_dateadded TEXT)',
                'art'                :'CREATE TABLE IF NOT EXISTS art (m_file TEXT, m_fanart TEXT, m_poster TEXT)',
                'actors'             :'CREATE TABLE IF NOT EXISTS actors (m_file TEXT, m_name TEXT, m_thmbnail TEXT, m_role TEXT, m_order TEXT)',
                'specialfeatures'    :'CREATE TABLE IF NOT EXISTS specialfeatures (m_file TEXT, m_title TEXT, m_path TEXT)',
                'multidisc'          :'CREATE TABLE IF NOT EXISTS multidisc (m_file TEXT, m_real TEXT, m_title TEXT, m_year TEXT, m_plot TEXT, m_rating TEXT, m_mpaa TEXT, m_dateadded TEXT)',
                }
    return TABLES
def q_sql():
    QUERY= {    's_specialfeatures'  :'SELECT * FROM specialfeatures WHERE m_path=%s',
                'sa_specialfeatures' :'SELECT * FROM specialfeatures WHERE m_file=%s',
                'sr_specialfeatures' :'SELECT * FROM specialfeatures',
                's_movies'           :'SELECT * FROM movies WHERE m_file=%s',
                'sa_movies'          :'SELECT * FROM movies',
                's_art'              :'SELECT * FROM art WHERE m_file=%s',
                's_actors'           :'SELECT * FROM actors WHERE m_file=%s',
                'i_specialfeatures'  :'INSERT INTO specialfeatures VALUES (%s,%s,%s)',
                'i_movies'           :'INSERT INTO movies VALUES (%s, %s, %s, %s, %s, %s, %s)',
                'i_art'              :'INSERT INTO art VALUES (%s, %s, %s)',
                'i_actors'           :'INSERT INTO actors VALUES (%s, %s, %s, %s, %s)',
                'd_specialfeatures'  :'DELETE FROM specialfeatures WHERE m_file=%s',
                'd_movies'           :'DELETE FROM movies WHERE m_file=%s',
                'd_art'              :'DELETE FROM art WHERE m_file=%s',
                'd_actors'           :'DELETE FROM actors WHERE m_file=%s',
                'dp_specialfeatures' :'DELETE FROM specialfeatures WHERE m_path=%s',
            }
    return QUERY
def q_lite():
    QUERY= {    's_specialfeatures'  :'SELECT * FROM specialfeatures WHERE m_path=?',
                'sa_specialfeatures' :'SELECT * FROM specialfeatures WHERE m_file=?',
                'sr_specialfeatures' :'SELECT * FROM specialfeatures',
                's_movies'           :'SELECT * FROM movies WHERE m_file=?',
                'sa_movies'          :'SELECT * FROM movies',
                's_art'              :'SELECT * FROM art WHERE m_file=?',
                's_actors'           :'SELECT * FROM actors WHERE m_file=?',
                'i_specialfeatures'  :'INSERT INTO specialfeatures VALUES (?,?,?)',
                'i_movies'           :'INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?, ?)',
                'i_art'              :'INSERT INTO art VALUES (?, ?, ?)',
                'i_actors'           :'INSERT INTO actors VALUES (?, ?, ?, ?, ?)',
                'd_specialfeatures'  :'DELETE FROM specialfeatures WHERE m_file=?',
                'd_movies'           :'DELETE FROM movies WHERE m_file=?',
                'd_art'              :'DELETE FROM art WHERE m_file=?',
                'd_actors'           :'DELETE FROM actors WHERE m_file=?',
                'dp_specialfeatures' :'DELETE FROM specialfeatures WHERE m_path=?',
            }
    return QUERY

class MYSQL:
    def __init__(self):
        info("MYSQL DB and TABLES being built")
        self.conI = connect(host=ipadd, port=ipport, user=user,password=pword,charset=charSet, cursorclass=cuType)
        self.cuI = self.conI.cursor()
        self.command = "CREATE DATABASE IF NOT EXISTS {}".format(dbName)
        self.cuI.execute(self.command)
        self.conO = connect(host=ipadd,port=ipport,user=user,password=pword,db=dbName,charset=charSet,cursorclass=cuType)
        self.cuO = self.conO.cursor()
        self.tables = tables()
        for self.table in self.tables:
            self.command = self.tables.get(self.table)
            self.cuO.execute(self.command)
        self.conI.close()
        self.conO.close()
        return
class SQLITE:
    def __init__(self):
        info("SQLITE3 DB and TABLES being built")
        if not xbmcvfs.exists(dbdir):
            xbmcvfs.mkdir(addir)
        self.con    = sqlite3.connect("{}".format(dbdir))
        self.cu     = self.con.cursor()
        self.tables = tables()
        for self.table in self.tables:
            self.command = self.tables.get(self.table)
            self.cu.execute("{}".format(self.command))
            self.con.commit()
        info("SQLITE3 DB built!!!")
        return
class QUERYSQL:
    def setControl(self):
        info("QUERYING DATABASE")
        if mysql == 'true':
            MYSQL()
            self.con = connect(host=ipadd,port=ipport,user=user,password=pword,db=dbName,charset=charSet,cursorclass=cuType)
            self.queries = q_sql()
        else:
            SQLITE()
            self.con = sqlite3.connect("{}".format(dbdir))
            self.queries = q_lite()
        global con
        con = self.con
        global cu
        cu = self.con.cursor()
        global queries
        queries = self.queries
    def execute(self,query="",var="",mode=""):
            self.command = queries.get('{}'.format(query))
            if mode == 'one':
                cu.execute(self.command,(var,))
                return cu.fetchone()
            elif mode == 'all':
                cu.execute(self.command)
                return cu.fetchall()
            elif mode == 'allv':
                cu.execute(self.command,(var,))
                return cu.fetchall()
            elif mode == 'com':
                cu.execute(self.command,var)
                con.commit()
            elif mode == "":
                cu.execute(self.command)
                con.commit()
            return
class UPDATEDB:
    def __init__(self):
        home.setProperty('LHUPDATING','true')
        if aupdb == 'true':
            note(txt=lang(30061))
        self.q              = QUERYSQL()
        self.q.setControl()
        self.bonus          = LISTS().bonus()
        self.total          = len(self.bonus)
        if aupdb == 'false':
            dialpro.create(lang(30000),lang(30012)+"{}".format(self.total))
        else:
            dialbg.create(lang(30000),lang(30012)+"{}".format(self.total))
        self.pc=1
        for self.item in self.bonus:
            self.percent    = float(self.pc)/float(self.total)*100
            self.title      = self.item.get('title','')
            self.year       = self.item.get('year','')
            self.file       = self.item.get('file','')
            self.art        = self.item.get('art','')
            self.fanart     = self.art.get('fanart','')
            self.poster     = self.art.get('poster','')
            self.cast       = self.item.get('cast','')
            self.plot       = self.item.get('plot','')
            self.rating     = self.item.get('rating','')
            self.mpaa       = self.item.get('mpaa','')
            self.dateadded  = self.item.get('dateadded','')
            self.bonus      = self.item.get('bonus','')
            if aupdb == 'false':
                dialpro.update(int(self.percent),lang(30059)+" {} ".format(self.pc)+lang(30016)+" {}".format(self.total),"{} ({})".format(self.title,self.year))
                self.pc += 1
                if dialpro.iscanceled():
                    return
            else:
                dialbg.update(int(self.percent),lang(30059)+" {} ".format(self.pc)+lang(30016)+" {}".format(self.total),"{} ({})".format(self.title,self.year))
                self.pc += 1
            for self.item in self.bonus:
                self.b_title        = self.item.get('b_title','')
                self.b_path         = self.item.get('b_path','')
                self.entry          = self.q.execute('s_specialfeatures',self.b_path,'one')
                if self.entry is None:
                    self.v          = (self.file, self.b_title, self.b_path,)
                    self.q.execute('i_specialfeatures',self.v,'com')
                self.entry          = self.q.execute('s_movies',self.file,'one')
                if self.entry is None:
                    self.v          = (self.file, self.title, self.year, self.plot, self.rating, self.mpaa, self.dateadded,)
                    self.q.execute('i_movies',self.v,'com')
                self.entry          = self.q.execute('s_art',self.file,'one')
                if self.entry is None:
                    self.v          = (self.file,self.fanart,self.poster,)
                    self.q.execute('i_art',self.v,'com')
                self.entry          = self.q.execute('s_actors',self.file,'one')
                if self.entry is None:
                    for self.item in self.cast:
                        self.name   = self.item.get('name','')
                        self.thumb  = self.item.get('thumbnail','')
                        self.role   = self.item.get('role','')
                        self.order  = self.item.get('order','')
                        self.v      = (self.file,self.name,self.thumb,self.role,self.order,)
                        self.q.execute('i_actors',self.v,'com')
            info('Special Features for '+self.title+' Added')
        home.clearProperty('LHUPDATING')
        if aupdb == 'false':
            xbmc.executebuiltin("Dialog.Close(all)")
            dialog.ok(lang(30000),lang(30013))
        else:
            note(txt=lang(30063))
        if home.getProperty('SFFIRSTRUN'):
            home.clearProperty('SFFIRSTRUN')
            xbmc.executebuiltin('RunAddon({})'.format(addonid))
        info('Database Updated')

        return
class CLEANUP:
    def __init__(self):
        home.setProperty('LHUPDATING','true')
        # if aupdb == 'true':
        note(txt=lang(30060))
        self.q              = QUERYSQL()
        self.q.setControl()
        self.entry          = self.q.execute('sr_specialfeatures',"",'all')
        self.list = self.checkkodi()
        self.trash = list()
        if mysql == 'true':
            self.sqlclean(self.entry,self.list)
        else:
            self.liteclean(self.entry,self.list)
        # if aupdb == 'true':
        note(txt=lang(30064))

    def checkkodi(self):
        self.query  = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies","params": {"properties": ["file"], "sort": { "method": "label" } }, "id": 1}'
        self.result = QUERYKODI().jsonquery(self.query)
        self.files = list()
        if 'result' in self.result and 'movies' in self.result['result']:
            for self.item in self.result['result']['movies']:
                self.files.append(self.item.get('file',''))
        return self.files
    def sqlclean(self,entry,list):
        for self.item in entry:
            self.file = self.item.get('m_file','')
            self.path = self.item.get('m_path','')
            self.chkp = xbmcvfs.exists(self.path)
            if self.chkp != 1:
                self.trash.append({'m_path':self.path})
            try:
                self.chk = list.index(self.file)
            except:
                self.trash.append({'m_file':self.file})
        for self.item in self.trash:
            try:
                self.v = (self.item.get('m_file',''),)
                self.q.execute('d_movies',self.v,'com')
                self.q.execute('d_specialfeatures',self.v,'com')
                self.q.execute('d_art',self.v,'com')
                self.q.execute('d_actors',self.v,'com')
            except:
                info('NO MOVIES to DELETE')
            try:
                self.v = (self.item.get('m_path',''),)
                self.q.execute('dp_specialfeatures',self.v,'com')
            except:
                info('NO EXTRAS to DELETE')
        self.entry    = self.q.execute('sa_movies',"",'all')
        for self.item in self.entry:
            # info('trying {}'.format(self.item))
            self.file = self.item.get('m_file','')
            self.v    = (self.file,)
            self.chk = self.q.execute('sa_specialfeatures',self.file,'one')
            if self.chk == None:
                self.v = (self.file,)
                self.q.execute('d_movies',self.v,'com')
                self.q.execute('d_specialfeatures',self.v,'com')
                self.q.execute('d_art',self.v,'com')
                self.q.execute('d_actors',self.v,'com')
        return
    def liteclean(self,entry,list):
        for self.item in entry:
            self.file = self.item[0]
            self.path = self.item[2]
            self.chkp = xbmcvfs.exists(self.path)
            if self.chkp != 1:
                self.trash.append({'m_path':self.path})
            try:
                self.chk = list.index(self.file)
            except:
                self.trash.append({'m_file':self.file})
        for self.item in self.trash:
            try:
                self.v = (self.item.get('m_file',''),)
                self.q.execute('d_movies',self.v,'com')
                self.q.execute('d_specialfeatures',self.v,'com')
                self.q.execute('d_art',self.v,'com')
                self.q.execute('d_actors',self.v,'com')
            except:
                info('NO MOVIES to DELETE')
            try:
                self.v = (self.item.get('m_path',''),)
                self.q.execute('dp_specialfeatures',self.v,'com')
            except:
                info('NO EXTRAS to DELETE')
        self.entry    = self.q.execute('sa_movies',"",'all')
        for self.item in self.entry:
            # info('trying {}'.format(self.item))
            self.file = self.item[0]
            self.v    = (self.file,)
            self.chk = self.q.execute('sa_specialfeatures',self.file,'one')
            if self.chk == None:
                self.v = (self.file,)
                self.q.execute('d_movies',self.v,'com')
                self.q.execute('d_specialfeatures',self.v,'com')
                self.q.execute('d_art',self.v,'com')
                self.q.execute('d_actors',self.v,'com')
        return
class VIEWS:
    def build_folders(self):
        self.q              = QUERYSQL()
        self.q.setControl()
        home.setProperty('SFUPDATING','true')
        self.entry          = self.q.execute('sa_movies','','all')
        for self.item in self.entry:
            if mysql == 'true':
                self.sql_rebuild(self.item)
            else:
                self.lite_rebuild(self.item)
        self.total          = len(folderlist)
        home.clearProperty('LHUPDATING')
        if self.total == 0:
            self.scan = dialog.yesno(lang(30000),lang(30003),lang(30004))
            home.setProperty('SFFIRSTRUN','true')
            if self.scan == 1:
                xbmc.executebuiltin("RunScript(plugin.specialfeatures,scandb)")
                return
            else:
                return
        else:
            return folderlist
    def build_files(self,file):
        self.q              = QUERYSQL()
        self.q.setControl()
        home.setProperty('SFUPDATING','true')
        self.entry          = self.q.execute('s_movies',file,'allv')
        for self.item in self.entry:
            if mysql == 'true':
                self.sqlfiles_rebuild(self.item)
            else:
                self.litefiles_rebuild(self.item)
        self.total          = len(filelist)
        home.clearProperty('SFUPDATING')
        if self.total == 0:
            self.scan = dialog.yesno(lang(30000),lang(30003),lang(30004))
            if self.scan == 1:
                ''' NEED TO ADD RUNSCRIPT ONCE GETING IT SET UP'''
                return
            else:
                return
        else:
            return filelist
    def sqlfiles_rebuild(self,item):
        self.file           = item.get('m_file','')
        self.nitem          ={'file':self.file, 'title':item.get('m_title',''), 'year':item.get('m_year',''), 'plot':item.get('m_plot',''), 'rating':item.get('m_rating',''), 'mpaa':item.get('m_mpaa',''), 'dateadded':item.get('m_dateadded','')}
        self.entry          = self.q.execute('s_art',self.file,'allv')
        for self.item in self.entry:
            self.art        ={'fanart':self.item.get('m_fanart',''), 'poster':self.item.get('m_poster','')}
            self.nitem.update({'art':self.art})
        self.entry          = self.q.execute('sa_specialfeatures',self.file,'allv')
        for self.item in self.entry:
            bonus.append({'b_title':self.item.get('m_title',''),'b_path':self.item.get('m_path','')})
        self.nitem.update({'bonus':bonus})
        self.entry          = self.q.execute('s_actors',self.file,'allv')
        for self.item in self.entry:
            self.actor={'name'       : self.item.get('m_name',''),
                        'thumbnail'  : self.item.get('m_thmbnail',''),
                        'role'       : self.item.get('m_role',''),
                        'order'      : self.item.get('m_order',''),
                        }            
            cast.append(self.actor)
        self.nitem.update({'cast':cast})
        return filelist.append(self.nitem)
    def litefiles_rebuild(self,item):
        self.file           = item[0]
        self.nitem          ={'file':item[0], 'title':item[1], 'year':item[2], 'plot':item[3], 'rating':item[4], 'mpaa':item[5], 'dateadded':item[6]}
        self.entry          = self.q.execute('s_art',self.file,'allv')
        for self.item in self.entry:
            self.art        ={'fanart':self.item[1], 'poster':self.item[2]}
            self.nitem.update({'art':self.art})
        self.entry          = self.q.execute('sa_specialfeatures',self.file,'allv')
        for self.item in self.entry:
            bonus.append({'b_title':self.item[1],'b_path':self.item[2]})
        self.nitem.update({'bonus':bonus})
        self.entry          = self.q.execute('s_actors',self.file,'allv')
        for self.item in self.entry:
            self.actor={'name'       : self.item[1],
                        'thumbnail'  : self.item[2],
                        'role'       : self.item[3],
                        'order'      : self.item[4],
                        }            
            cast.append(self.actor)
        self.nitem.update({'cast':cast})
        return filelist.append(self.nitem)
    def sql_rebuild(self,item):
        self.file           = item.get('m_file','')
        self.nitem          ={'file':self.file, 'title':item.get('m_title',''), 'year':item.get('m_year',''), 'plot':item.get('m_plot',''), 'rating':item.get('m_rating',''), 'mpaa':item.get('m_mpaa',''), 'dateadded':item.get('m_dateadded','')}
        self.entry          = self.q.execute('s_art',self.file,'allv')
        for self.item in self.entry:
            self.art        ={'fanart':self.item.get('m_fanart',''), 'poster':self.item.get('m_poster','')}
            self.nitem.update({'art':self.art})
        self.entry          = self.q.execute('sa_specialfeatures',self.file,'allv')
        for self.item in self.entry:
            bonus.append({'b_title':self.item.get('m_title',''),'b_path':self.item.get('m_path','')})
        self.nitem.update({'bonus':bonus})
        self.entry          = self.q.execute('s_actors',self.file,'allv')
        for self.item in self.entry:
            self.actor={'name'       : self.item.get('m_name',''),
                        'thumbnail'  : self.item.get('m_thmbnail',''),
                        'role'       : self.item.get('m_role',''),
                        'order'      : self.item.get('m_order',''),
                        }            
            cast.append(self.actor)
        self.nitem.update({'cast':cast})
        return folderlist.append(self.nitem)
    def lite_rebuild(self,item):
        self.file           = item[0]
        self.nitem          ={'file':item[0], 'title':item[1], 'year':item[2], 'plot':item[3], 'rating':item[4], 'mpaa':item[5], 'dateadded':item[6]}
        self.entry          = self.q.execute('s_art',self.file,'allv')
        for self.item in self.entry:
            self.art        ={'fanart':self.item[1], 'poster':self.item[2]}
            self.nitem.update({'art':self.art})
        self.entry          = self.q.execute('sa_specialfeatures',self.file,'allv')
        for self.item in self.entry:
            bonus.append({'b_title':self.item[1],'b_path':self.item[2]})
        self.nitem.update({'bonus':bonus})
        self.entry          = self.q.execute('s_actors',self.file,'allv')
        for self.item in self.entry:
            self.actor={'name'       : self.item[1],
                        'thumbnail'  : self.item[2],
                        'role'       : self.item[3],
                        'order'      : self.item[4],
                        }            
            cast.append(self.actor)
        self.nitem.update({'cast':cast})
        return folderlist.append(self.nitem)

