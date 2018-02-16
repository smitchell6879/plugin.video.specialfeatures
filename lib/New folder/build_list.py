from lib.sys_init import *

class LISTS:


    def build(self):
        if aupdb == 'true':
            note(txt=lang(30062))
        info("Gathering bonusmaterial")
        self.dbt = ""
        self.sfa = list()
        self.sfm = list()
        self.sft = list()
        self.sfs = list()
        category = 'movies'
        self.movies,self.lib = QUERYKODI().bonusmaterial(category)
        self.getfiledir(self.lib,self.movies)
        category = 'tvshows'
        self.tvshows,self.lib = QUERYKODI().bonusmaterial(category)
        category = 'seasons'
        self.seasons = QUERYKODI().bonusmaterial(category)
        self.getfiledir(self.lib,self.tvshows,self.seasons)
        return self.sfa
    
    def getfiledir(self,max,iterator,iterate=''):
        if 'movies' in iterator['result']:
            self.tot = list()
            self.tl = iterator['result']['limits'].get('total','')
            if aupdb == 'false':
                dialpro.create(lang(30000),lang(30012)+' {}'.format(self.tl))
            else:
                dialbg.create(lang(30000),lang(30012)+' {}'.format(self.tl))
            self.pc=1
            for self.i in iterator['result']['movies']:
                # time.sleep(.05)
                self.percent    = float(self.pc)/float(self.tl)*100
                self.t      = self.i.get('title','')
                self.y      = self.i.get('year','')
                self.f      = self.i.get('file','')
                self.ss     = ""
                self.dbt    = 'movies'
                self.add    = False
                self.sf     = list()
                self.nfo    = ""
                if 'BDMV' in self.f:
                    if '/BDMV' in self.f:
                        self.pb=os.path.join(os.path.split(os.path.split(self.f)[0])[0]+'/',folder)+'/'
                    else:
                        self.pb=os.path.join(os.path.split(os.path.split(self.f)[0])[0]+'\\',folder)+'\\'
                elif 'VIDEO_TS' in self.f:
                    if '/VIDEO_TS' in self.f:
                        self.pb=os.path.join(os.path.split(os.path.split(self.f)[0])[0]+'/',folder)+'/'
                    else:
                        self.pb=os.path.join(os.path.split(os.path.split(self.f)[0])[0]+'\\',folder)+'\\'
                else:
                    self.pb = os.path.split(self.f)[0]
                self.chkfiledir(self.pb)
                if len(self.sf)!= 0:
                    self.i.update({'bonus':self.sf})
                    self.sfa.append(self.i)
                if aupdb == 'false':
                    dialpro.update(int(self.percent),lang(30015)+' {}' .format(self.pc)+lang(30016)+ '{}'.format(self.tl),'{} ({})'.format(self.t,self.y))
                    self.pc += 1
                    if dialpro.iscanceled():
                        exit()
                else:
                    dialbg.update(int(self.percent),lang(30015)+' {}' .format(self.pc)+lang(30016)+ '{}'.format(self.tl),'{} ({})'.format(self.t,self.y))
                    self.pc += 1
        if 'tvshows' in iterator['result']:
            self.tt = list()
            self.tl = iterator['result']['limits'].get('total','')
            if aupdb == 'false':
                dialpro.create(lang(30000),lang(30012)+' {}'.format(self.tl))
            else:
                dialbg.create(lang(30000),lang(30012)+' {}'.format(self.tl))
            self.pc=1
            for self.i in iterator['result']['tvshows']:
                # time.sleep(.05)
                self.percent    = float(self.pc)/float(self.tl)*100
                self.t      = self.i.get('title','')
                self.y      = self.i.get('year','')
                self.f      = self.i.get('file','')
                self.dbt    = 'tvshows'
                self.ss     = ""
                self.add    = False
                self.sf     = list()
                self.nfo    = ""
                if '/' in self.f:
                    self.pb = os.path.join(self.f,folder)+'/'
                else:
                    self.pb = os.path.join(self.f,folder)+'\\'
                
                self.chkfiledir(self.pb)
                for self.si in iterate['result']['seasons']:
                    self.st = self.si.get('showtitle','')
                    if self.t == self.st:
                        self.s = self.si.get('season','')
                        if self.s <=9:
                            self.ss = "Season 0{}".format(self.s)
                        else:
                            self.ss = "Season {}".format(self.s)
                        if '/' in self.f:
                            self.ps = os.path.join(os.path.join(self.f,self.ss+"/"),folder)+'/'
                        else:
                            self.ps = os.path.join(os.path.join(self.f,self.ss+"\\"),folder)+'\\'
                        self.dbt = 'seasons'
                        self.chkfiledir(self.ps)
                if len(self.sf)!= 0:
                    self.i.update({'bonus':self.sf})
                    self.sfa.append(self.i)
                if aupdb == 'false':
                    dialpro.update(int(self.percent),lang(30015)+' {}' .format(self.pc)+lang(30016)+ '{}'.format(self.tl),'{} ({})'.format(self.t,self.y))
                    self.pc += 1
                    if dialpro.iscanceled():
                        return
                else:
                    dialbg.update(int(self.percent),lang(30015)+' {}' .format(self.pc)+lang(30016)+ '{}'.format(self.tl),'{} ({})'.format(self.t,self.y))
                    self.pc += 1
        return self.sfa, self.sf        
    def chkfiledir(self,p):
        self.chk = xbmcvfs.exists(p)
        if self.chk == 1:
            self.rd,self.rf = xbmcvfs.listdir(p)
            if self.rf:
                for self.fi in self.rf:
                    self.getfile(self.fi,p)
            if self.rd:
                for self.di in self.rd:
                    self.alt = False
                    self.getfolder(self.di,p,self.alt)
    def getfile(self,f,r,a=""):
        self.e = False
        self.sfifo = 'false'
        if exclude != "":
            self.d = re.search(exclude,f)
            # info(f)
            # info(self.d)
        else:
            self.d = ""
        if self.d:
            self.e = True
        self.sfif = re.search(".sfnfo",f)
        if self.sfif:
            self.sfifo = 'true'
        if not self.e:
            self.bt = os.path.splitext(f)[0]
            self.bp = r+f
            self.artl =list()
            if self.dbt == 'movies':
                if a == True:
                        self.bt = os.path.split(os.path.split(os.path.split(r)[0])[0])[1]
                        self.bp = r
                        self.bi = {'bt':self.bt,'bp':self.bp,'dbt':self.dbt, 'info':self.sfifo,'ss':self.ss}
                        self.art = self.i.get('art')
                        for self.ai in self.art:
                            self.bi.update({'{}'.format(self.ai):'{}'.format(self.art.get('{}'.format(self.ai),''))})
                            self.artl.append(self.ai)
                        self.bi.update({'artkey':self.artl})
                        self.sf.append(self.bi)
            elif self.dbt == 'tvshows':
                self.bi ={'bt':self.bt,'bp':self.bp,'dbt':self.dbt, 'info':self.sfifo,'ss':self.ss}
                self.art = self.i.get('art','')
                for self.ai in self.art:
                    self.bi.update({'{}'.format(self.ai):'{}'.format(self.art.get('{}'.format(self.ai),''))})
                    self.artl.append(self.ai)
                self.bi.update({'artkey':self.artl})
                self.sf.append(self.bi)
            elif self.dbt == 'seasons':
                self.bi ={'bt':self.bt,'bp':self.bp,'dbt':self.dbt, 'info':self.sfifo,'ss':self.ss} 
                self.art = self.si.get('art','')
                for self.ai in self.art:
                    self.bi.update({'{}'.format(self.ai):'{}'.format(self.art.get('{}'.format(self.ai),''))})
                    self.artl.append(self.ai)
                self.bi.update({'artkey':self.artl})
                self.sf.append(self.bi)
        return self.sf
    def chkfolder(self,p):
        self.fchk = xbmcvfs.exists(p)
        if self.fchk == 1:
            for self.frd in xbmcvfs.listdir(p)[0]:
                if 'BDMV' in self.frd:
                    if '/' in p:
                        self.fi = os.path.join(os.path.join(p,self.frd)+'/',"index.bdmv")
                    else:
                        self.fi = os.path.join(os.path.join(p,self.frd)+'\\',"index.bdmv")
                if 'VIDEO_TS' in self.frd:
                    if '/' in p:
                        self.fi = os.path.join(os.path.join(p,self.frd)+'/',"VIDEO_TS.IFO")
                    else:
                        self.fi = os.path.join(os.path.join(p,self.frd)+'\\',"VIDEO_TS.IFO")
                return self.fi
    def getfolder(self,d,r,a):
        if '/' in r:
            self.d = os.path.join("{}".format(r),"{}".format(d))+'/'
        else:
            self.d = os.path.join("{}".format(r),"{}".format(d))+'\\'
            
            
        
        self.chkfolder(self.d)

        a = True

        self.getfile(os.path.split(self.fi)[1],self.fi,a)
        
    def listinfo(self,li):
        for self.i in li:
            self.t = self.i.get('title')
            self.sf = self.i.get('bonus')
            for self.isf in self.sf:
                self.dbt = self.isf.get('dbt')
                if self.dbt == 'movies':
                    self.sfm.append(self.i)
                if self.dbt == 'tvshows':
                    self.sft.append(self.i)
                if self.dbt == 'seasons':
                    self.sfs.append(self.i)
        return self.sfm, self.sfs, self.sft
        
class QUERYKODI:
    def kodiquery(self,dbtype=""):
        if dbtype == 'tvshows':
            return '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows","params": {"properties": ["title","genre","year","rating","plot","studio","mpaa","cast","playcount","episode","imdbnumber","premiered","votes","lastplayed","fanart","thumbnail","file","originaltitle","sorttitle","episodeguide","season","watchedepisodes","dateadded","tag","art","userrating","ratings","runtime","uniqueid"], "sort": { "method": "label" } }, "id": 1}'
        elif dbtype == 'seasons':
            return '{"jsonrpc": "2.0", "method": "VideoLibrary.GetSeasons","params": {"properties": ["season","showtitle","playcount","episode","fanart","thumbnail","tvshowid","watchedepisodes","art","userrating"], "sort": { "method": "label" } }, "id": 1}'
        elif dbtype == 'movies':
            return '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies","params": {"properties": ["title","genre","year","rating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art","userrating","ratings","premiered","uniqueid"], "sort": { "method": "label" } }, "id": 1}'
        else:
            sys.exit(1)
    def jsonquery(self,query):
        info("Making request to Kodi")
        self.jsonq = xbmc.executeJSONRPC("{}".format(self.kodiquery(query)))
        self.json  = json.loads(self.jsonq)
        return self.json
    def bonusmaterial(self,category=""):
        self.result = self.jsonquery(category)
        self.totals = list()
        if 'result' in self.result:
            if self.result['result']['limits'].get('total','') != 0:
                if 'movies' in self.result['result']:
                    for self.itemm in self.result['result']['movies']:
                        self.totals.append(self.itemm.get('title',''))
                    self.total = len(self.totals)
                    if self.total > 0:
                        return self.result,self.total
                    else:
                        error("NO MOVIES AND MOVIES TO LIBRARY THEN IT WORK")
                        return
                if 'tvshows' in self.result['result']:
                    for self.itemt in self.result['result']['tvshows']:
                        self.totals.append(self.itemt.get('title',''))
                    self.total = len(self.totals)
                    if self.total > 0:
                        return self.result,self.total
                    else:
                        error("NO TV SHOWS AND TV SHOWS TO LIBRARY THEN IT WORK")
                        return
                if 'seasons' in self.result['result']:
                    return self.result
            elif 'movies' in self.result['result']:
                ok(lang(30065)+"[CR]"+lang(30066))
                sys.exit(1)
            elif 'tvshows' in self.result['result']:
                ok(lang(30065)+"[CR]"+lang(30066))
                sys.exit(1)
 