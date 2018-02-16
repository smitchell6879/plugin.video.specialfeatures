from lib.sys_init import *
from lib.build_list import *

def tables():
    TABLES= {   'tvshows'             :'CREATE TABLE IF NOT EXISTS tvshows (tvshowid TEXT,file TEXT,title TEXT,year TEXT,mpaa TEXT, plot TEXT, sorttitle TEXT, premiered TEXT, originaltitle TEXT, dateadded TEXT, imdbnumber TEXT, label TEXT, votes TEXT,  rating TEXT, userrating TEXT)',
                'movies'              :'CREATE TABLE IF NOT EXISTS movies (movieid TEXT,file TEXT,title TEXT, year TEXT,mpaa TEXT, plot TEXT, sorttitle TEXT,premiered TEXT,originaltitle TEXT,dateadded TEXT,imdbnumber TEXT,label TEXT,tagline TEXT, votes TEXT, rating TEXT, userrating TEXT, trailer TEXT, top250 TEXT,setid TEXT, _set TEXT)',
                'art'                 :'CREATE TABLE IF NOT EXISTS art (dbtype TEXT, file TEXT, bpath TEXT, type TEXT, location TEXT, season TEXT)',
                'actors'              :'CREATE TABLE IF NOT EXISTS actors ( dbtype TEXT, id TEXT, name TEXT, thumbnail TEXT, role TEXT, ordr TEXT)',
                # 'directors'           :'CREATE TABLE IF NOT EXISTS directors ( dbtype TEXT, id TEXT, name TEXT)',
                # 'genres'              :'CREATE TABLE IF NOT EXISTS genres ( dbtype TEXT, id TEXT, genre TEXT)',
                # 'writers'             :'CREATE TABLE IF NOT EXISTS writers ( dbtype TEXT, id TEXT, writer TEXT)',
                # 'studios'             :'CREATE TABLE IF NOT EXISTS studios ( dbtype TEXT, id TEXT, studio TEXT)',
                # 'countries'           :'CREATE TABLE IF NOT EXISTS countries ( dbtype TEXT, id TEXT, country TEXT)',
                # 'tags'                :'CREATE TABLE IF NOT EXISTS tags ( dbtype TEXT, id TEXT, tag TEXT)',
                'special'             :'CREATE TABLE IF NOT EXISTS special (dbtype TEXT, id TEXT, season TEXT, title TEXT, bpath TEXT, sfnfo TEXT)',
                # 'multidisc'          :'CREATE TABLE IF NOT EXISTS multidisc (m_file TEXT, m_real TEXT, m_title TEXT, m_year TEXT, m_plot TEXT, m_rating TEXT, m_mpaa TEXT, m_dateadded TEXT)',
                }
    return TABLES

def q_sql():
    QUERY= {    's_specialfeatures'  :'SELECT * FROM specialfeatures WHERE m_path=%s',
                'specialall'         :'SELECT * FROM special',
                'moviesall'          :'SELECT * FROM movies',
                'tvshowsall'         :'SELECT * FROM tvshows',
                'specialfolder'      :'SELECT * FROM special WHERE dbtype=%s',
                'special'            :'SELECT * FROM special WHERE bpath=%s',
                'aspecial'           :'SELECT * FROM special WHERE dbtype=%s AND id=%s',
                'aactors'            :'SELECT * FROM actors WHERE dbtype=%s AND id=%s',
                'tvshows'            :'SELECT * FROM tvshows WHERE file=%s',
                'movies'             :'SELECT * FROM movies WHERE file=%s',
                'genres'             :'SELECT * FROM genres WHERE id=%s',
                'amovies'            :'SELECT * FROM movies',
                'atvshows'           :'SELECT * FROM tvshows',
                'art'                :'SELECT * FROM art WHERE bpath=%s AND file=%s',
                'aart'               :'SELECT * FROM art WHERE dbtype=%s AND bpath=%s',
                'mart'               :'SELECT * FROM art WHERE dbtype=%s AND file=%s',
                'actors'             :'SELECT * FROM actors WHERE id=%s',
                'writers'            :'SELECT * FROM writers WHERE id=%s',
                'countries'          :'SELECT * FROM countries WHERE id=%s',
                'studios'            :'SELECT * FROM studios WHERE id=%s',
                'tags'               :'SELECT * FROM tags WHERE id=%s',
                'directors'          :'SELECT * FROM directors WHERE id=%s',
                'ispecial'           :'INSERT INTO special VALUES (%s,%s,%s,%s,%s,%s)',
                'itvshows'           :'INSERT INTO tvshows VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                'imovies'            :'INSERT INTO movies VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                'idirectors'         :'INSERT INTO directors VALUES (%s,%s,%s)',
                'igenres'            :'INSERT INTO genres VALUES (%s,%s,%s)',
                'iwriters'           :'INSERT INTO writers VALUES (%s,%s,%s)',
                'icountries'         :'INSERT INTO countries VALUES (%s,%s,%s)',
                'istudios'           :'INSERT INTO studios VALUES (%s,%s,%s)',
                'itags'              :'INSERT INTO tags VALUES (%s,%s,%s)',
                'iart'               :'INSERT INTO art VALUES (%s,%s,%s,%s,%s,%s)',
                'iactors'            :'INSERT INTO actors VALUES (%s,%s,%s,%s,%s,%s)',
                'd_specialfeatures'  :'DELETE FROM specialfeatures WHERE file=%s',
                'd_movies'           :'DELETE FROM movies WHERE file=%s',
                'd_art'              :'DELETE FROM art WHERE file=%s',
                'd_actors'           :'DELETE FROM actors WHERE file=%s',
                'dp_specialfeatures' :'DELETE FROM specialfeatures WHERE m_path=%s',
            }
    return QUERY
def q_lite():
    QUERY= {    's_specialfeatures'  :'SELECT * FROM specialfeatures WHERE m_path=?',
                'specialall'         :'SELECT * FROM special',
                'moviesall'          :'SELECT * FROM movies',
                'tvshowsall'         :'SELECT * FROM tvshows',
                'specialfolder'      :'SELECT * FROM special WHERE dbtype=?',
                'special'            :'SELECT * FROM special WHERE bpath=?',
                'aspecial'           :'SELECT * FROM special WHERE dbtype=? AND id=?',
                'aactors'            :'SELECT * FROM actors WHERE dbtype=? AND id=?',
                'tvshows'            :'SELECT * FROM tvshows WHERE file=?',
                'movies'             :'SELECT * FROM movies WHERE file=?',
                'genres'             :'SELECT * FROM genres WHERE id=?',
                'amovies'            :'SELECT * FROM movies',
                'atvshows'           :'SELECT * FROM tvshows',
                'art'                :'SELECT * FROM art WHERE bpath=? AND file=?',
                'aart'               :'SELECT * FROM art WHERE dbtype=? AND bpath=?',
                'mart'               :'SELECT * FROM art WHERE dbtype=? AND file=?',
                'actors'             :'SELECT * FROM actors WHERE id=?',
                'writers'            :'SELECT * FROM writers WHERE id=?',
                'countries'          :'SELECT * FROM countries WHERE id=?',
                'studios'            :'SELECT * FROM studios WHERE id=?',
                'tags'               :'SELECT * FROM tags WHERE id=?',
                'directors'          :'SELECT * FROM directors WHERE id=?',
                'ispecial'           :'INSERT INTO special VALUES (?,?,?,?,?,?)',
                'itvshows'           :'INSERT INTO tvshows VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                'imovies'            :'INSERT INTO movies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                'idirectors'         :'INSERT INTO directors VALUES (?,?,?)',
                'igenres'            :'INSERT INTO genres VALUES (?,?,?)',
                'iwriters'           :'INSERT INTO writers VALUES (?,?,?)',
                'icountries'         :'INSERT INTO countries VALUES (?,?,?)',
                'istudios'           :'INSERT INTO studios VALUES (?,?,?)',
                'itags'              :'INSERT INTO tags VALUES (?,?,?)',
                'iart'               :'INSERT INTO art VALUES (?,?,?,?,?,?)',
                'iactors'            :'INSERT INTO actors VALUES (?,?,?,?,?,?)',
                'd_specialfeatures'  :'DELETE FROM specialfeatures WHERE file=?',
                'd_movies'           :'DELETE FROM movies WHERE file=?',
                'd_art'              :'DELETE FROM art WHERE file=?',
                'd_actors'           :'DELETE FROM actors WHERE file=?',
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
        self.con    = sqlite3.connect('{}'.format(dbdir))
        self.cu     = self.con.cursor()
        self.tables = tables()
        for self.table in self.tables:
            self.command = self.tables.get(self.table)
            self.cu.execute('{}'.format(self.command))
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
            self.con = sqlite3.connect('{}'.format(dbdir))
            self.queries = q_lite()
        global con
        con = self.con
        global cu
        cu = self.con.cursor()
        global queries
        queries = self.queries
        return
    def execute(self,query="",var="",mode=""):
            self.command = queries.get('{}'.format(query))
            if mode == 'one':
                cu.execute(self.command,(var,))
                return cu.fetchone()
            if mode == 'onev':
                cu.execute(self.command,var)
                return cu.fetchone()
            elif mode == 'all':
                cu.execute(self.command)
                return cu.fetchall()
            elif mode == 'allv':
                cu.execute(self.command,var)
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
        self.tt = list()
        if aupdb == 'true':
            note(txt=lang(30061))
        self.q              = QUERYSQL()
        self.q.setControl()
        self.sfa = LISTS().build()
        self.sfat = len(self.sfa)
        if aupdb == 'false':
            dialpro.create(lang(30000),lang(30012)+' {}'.format(self.sfat))
        else:
            dialbg.create(lang(30000),lang(30012)+' {}'.format(self.sfat))
        self.pc=1
        self.ti=1
        for self.i in self.sfa:
            '''This is the list of videos with bonuses to  iterate thru the list to add to database
            file we get info about the parent folder or the original video series'''
            # time.sleep(1)
            self.sf = self.i.get('bonus')
            for self.sfitem in self.sf:
                self.dbt= self.sfitem.get('dbt')
            if self.dbt =='movies':
                self.file = self.i.get('file')
                self.entry = self.q.execute('movies',self.file,'one')
                if self.entry is None:
                    self.sfi = (self.i.get('movieid'),self.i.get('file'),self.i.get('title'),self.i.get('year'),self.i.get('mpaa'),self.i.get('plot'),self.i.get('sorttitle'),
                                self.i.get('premiered'),self.i.get('originaltitle'),self.i.get('dateadded'),self.i.get('imdbnumber'),self.i.get('label'),self.i.get('votes'),
                                self.i.get('rating'),self.i.get('userrating'),self.i.get('tagline'),self.i.get('trailer'),self.i.get('top250'),self.i.get('setid'),self.i.get('set'),)
                    self.q.execute('imovies', self.sfi,'com')
            if self.dbt == 'tvshows':
                self.file = self.i.get('file')
                self.entry = self.q.execute('tvshows',self.file,'one')
                if self.entry is None:
                    self.sfi = (self.i.get('tvshowid'),self.i.get('file'),self.i.get('title'),self.i.get('year'),self.i.get('mpaa'),self.i.get('plot'),self.i.get('sorttitle'),
                                self.i.get('premiered'),self.i.get('originaltitle'),self.i.get('dateadded'),self.i.get('imdbnumber'),self.i.get('label'),self.i.get('votes'),
                                self.i.get('rating'),self.i.get('userrating'))
                    self.q.execute('itvshows',self.sfi,'com')


            
            

            self.percent    = float(self.pc)/float(self.sfat)*100
            self.mid = self.i.get("movieid")
            self.tvid =self.i.get("tvshowid")
            self.id = ""
            self.title = ""
            self.t = self.i.get('title')
            self.y = self.i.get('year')
            self.c = self.i.get('cast')
            self.year = ""
            self.sf = self.i.get('bonus')
            self.file = self.i.get('file')
            ''' This is where we start actually sorting bonuses'''
            for self.bi in self.sf:
                self.bt = self.bi.get('bt')
                self.bp = self.bi.get('bp')
                self.nfo = self.bi.get('info')
                self.dbt = self.bi.get('dbt')
                self.ss = self.bi.get('ss')
                self.artky = self.bi.get('artkey')
                if self.dbt == 'movies':
                    self.id = self.mid
                else:
                    self.id = self.tvid
                self.arow = (self.bp,self.file)
                self.entry = self.q.execute('art',self.arow,'onev')
                if self.entry is None:
                    for self.ai in self.artky:
                        self.atype = self.ai
                        self.loco = self.bi.get('{}'.format(self.atype))
                        self.i = (self.dbt,self.file,self.bp,self.atype,self.loco,self.ss)
                        self.q.execute('iart',self.i,'com')
                self.entry = self.q.execute('special',self.bp,'one')
                if self.entry is None:
                    self.sfi = (self.dbt,self.id,self.ss,self.bt,self.bp,self.nfo)
                    self.q.execute('ispecial', self.sfi,'com')
                self.entry = self.q.execute('actors',self.id,'one')
                if self.entry is None:
                    for self.ic in self.c:
                        self.name   = self.ic.get('name')
                        self.thumb  = self.ic.get('thumbnail')
                        self.role   = self.ic.get('role')
                        self.order  = self.ic.get('order')
                        self.i      = (self.dbt,self.id,self.name,self.thumb,self.role,self.order)
                        self.q.execute('iactors',self.i,'com')
                


                self.ti += 1
            if aupdb == 'false':
                dialpro.update(int(self.percent),lang(30059)+' {}' .format(self.pc)+lang(30016)+ '{}'.format(self.sfat),'{} ({})'.format(self.t,self.y))
                self.pc += 1
                if dialpro.iscanceled():
                    return
            else:
                dialbg.update(int(self.percent),lang(30059)+' {}' .format(self.pc)+lang(30016)+ '{}'.format(self.sfat),'{} ({})'.format(self.t,self.y))
                self.pc += 1

        home.clearProperty('LHUPDATING')
        if aupdb == 'false':
            # xbmc.executebuiltin('Dialog.Close(all)')
            dialog.ok(lang(30000),lang(30013))
        else:
            note(txt=lang(30063))
        if home.getProperty('SFFIRSTRUN'):
            home.clearProperty('SFFIRSTRUN')
            # xbmc.executebuiltin('RunAddon({})'.format(addonid))
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
        self.query  = '{jsonrpc: 2.0, method: VideoLibrary.GetMovies,params: {properties: [file], sort: { method: label } }, id: 1}'
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
    def buildfiles(self,dbtype,file):
        self.q              = QUERYSQL()
        self.q.setControl()
        home.setProperty('SFUPDATING','true')
        self.get = (file,)
        if dbtype == 'movies':
            self.entry = self.q.execute('movies',self.get,'allv')
            for self.item in self.entry:
                if mysql == 'true':
                    self.sqlfiles_rebuild(self.item,dbtype)
                else:
                    self.lite_files(self.item,dbtype)
        if dbtype == 'tvshows':
            self.entry = self.q.execute('tvshows',self.get,'allv')
            for self.item in self.entry:
                if mysql == 'true':
                    self.sqlfiles_rebuild(self.item,'seasons')
                else:
                    self.lite_files(self.item,'tvshows')

        self.total          = len(filelist)
        home.clearProperty('SFUPDATING')
        if self.total == 0:
            self.scan = dialog.yesno(lang(30000),lang(30003),lang(30004))
            if self.scan == 1:
                text('made it')
                xbmc.executebuiltin('RunScript(plugin.specialfeatures,scandb)')
                return
            else:
                return
        else:
            return filelist
    def buildfolders(self,dbtype):
        self.q              = QUERYSQL()
        self.q.setControl()
        home.setProperty('SFUPDATING','true')
        if dbtype == 'movies':
            self.entry = self.q.execute('moviesall',mode='all')
        elif dbtype == 'tvshows':
            self.entry = self.q.execute('tvshowsall',mode='all')
        for self.item in self.entry:
            if mysql == 'true':
                self.sql_folders(self.item,dbtype)
            else:
                self.lite_folders(self.item,dbtype)        
        self.total          = len(filelist)
        home.clearProperty('SFUPDATING')
        if self.total == 0:
            self.scan = dialog.yesno(lang(30000),lang(30003),lang(30004))
            if self.scan == 1:
                xbmc.executebuiltin('RunScript(plugin.specialfeatures,scandb)')
                return
            else:
                return
        else:
            return filelist
    # def sqlfiles_rebuildall(self,item):
    #     self.id = item.get('id')
    #     self.dbt = item.get('dbtype')
    #     self.file = item.get('bpath')
    #     self.nitem ={'title':item.get('title'),'file':item.get('bpath')}
    #     self.row = (self.dbt,self.file)
    #     self.entry = self.q.execute('aart',self.row,'allv')
    #     self.art={}
    #     for self.item in self.entry:
    #         self.artl= {'{}'.format(self.item.get('type')):'{}'.format(self.item.get('location'))}
    #         self.art.update(self.artl)
    #     self.entry          = self.q.execute('aactors',self.row,'allv')
    #     for self.item in self.entry:
    #         self.actor={'name'       : self.item.get('name',''),
    #                     'thumbnail'  : self.item.get('thumbnail',''),
    #                     'role'       : self.item.get('role',''),
    #                     'order'      : self.item.get('ordr',''),
    #                     }            
    #         cast.append(self.actor)
    #     self.nitem.update({'cast':cast})
    #     self.nitem.update({'art':self.art})
    #     return filelist.append(self.nitem)
    def lite_files(self,item,dbt):
        self.id = item[0]
        self.dbt = dbt
        self.file = item[1]
        self.row = (self.dbt,self.id)
        self.entry = self.q.execute('aspecial',self.row,'allv')
        for self.item in self.entry:
            self.nitem ={'title':self.item[3],'file':self.item[4],'id':item[0]}
            self.row = (dbt,self.item[4])
            self.entry = self.q.execute('aart',self.row,'allv')
            self.art={}
            self.cast=list()
            for self.item in self.entry:
                self.artl= {self.item[3]:self.item[4]}
                self.art.update(self.artl)
            self.entry          = self.q.execute('aactors',self.row,'allv')
            for self.item in self.entry:
                self.actor={'name'       : self.item[2],
                            'thumbnail'  : self.item[3],
                            'role'       : self.item[4],
                            'order'      : self.item[5],
                            }             
                self.cast.append(self.actor)
            self.nitem.update({'cast':cast})
            self.nitem.update({'art':self.art})
            filelist.append(self.nitem)
        return filelist
   
    def lite_folders(self,item,dbt):
        self.id = item[0]
        self.file = item[1]
        self.nitem ={'title':item[2],'file':item[1],'id':item[0]}
        self.arow = (dbt,'{}'.format(self.file))
        self.row = (dbt,self.id)
        self.entry = self.q.execute('mart',self.arow,'allv')
        self.art={}
        self.cast=list()
        for self.item in self.entry:
            info(self.item)
            self.artl= {'{}'.format(self.item[3]):'{}'.format(self.item[4])}
            self.art.update(self.artl)
        self.entry  = self.q.execute('aactors',self.row,'allv')
        for self.item in self.entry:
            self.actor={'name'       : self.item[2],
                        'thumbnail'  : self.item[3],
                        'role'       : self.item[4],
                        'order'      : self.item[5],
                        }            
            self.cast.append(self.actor)
        self.nitem.update({'cast':self.cast})
        self.nitem.update({'art':self.art})
        return filelist.append(self.nitem)
    # def buildallfiles(self):
    #     self.q              = QUERYSQL()
    #     self.q.setControl()
    #     home.setProperty('SFUPDATING','true')
    #     self.entry = self.q.execute('specialall',mode='all')
    #     for self.item in self.entry:
    #         if mysql == 'true':
    #             self.sqlfiles_rebuildall(self.item)
    #         else:
    #             self.litefiles_rebuild(self.item)
        

    #     self.total          = len(filelist)
    #     home.clearProperty('SFUPDATING')
    #     if self.total == 0:
    #         self.scan = dialog.yesno(lang(30000),lang(30003),lang(30004))
    #         if self.scan == 1:
    #             xbmc.executebuiltin('RunScript(plugin.specialfeatures,scandb)')
    #             return
    #         else:
    #             return
    #     else:
    #         return filelist
    

  