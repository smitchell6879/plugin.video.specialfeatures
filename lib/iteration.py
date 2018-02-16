from lib.sys_init import *
from lib.querylib import *
from lib.importexport import *
ip         = imPort()
ep         = exPort()

class resultFILTER:
    '''Start checking for extras'''
    def router(self,query):
        result = QUERY().router(query)
        self.checker = list()
        self.vR = self.verifyRes(query,result)
        if self.vR is True:
            self.sortDir(query,result)
            self.verifyDir(self.checker)


    '''Checking results''' 
    def verifyRes(self,query,result):
        if 'result' in result:
            if result['result']['limits']['total'] != 0:
                return True
            else:
                error("NO LUCK ADD VIDEOS TO YOUR LIBRARY")
    '''Setting up Directories to check'''
    def sortDir(self,query,result):
        for self.item in result['result']['{}'.format(query)]:
            self.resultVar()
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
                if '/' in self.f:
                    self.pb = os.path.join(os.path.split(self.f)[0]+'/',folder)+'/'
                else:
                    self.pb = os.path.join(os.path.split(self.f)[0]+'\\',folder)+'\\'
            self.l.update({'path':self.pb})
            self.checker.append(self.l)
        return self.checker
    '''Verifing the Directories are there then attempt to get videos'''
    def verifyDir(self,checks):
        for self.item in checks:
            self.bonus=list()
            self.verify = xbmcvfs.exists(self.item['path'])
            if self.verify == 1:
                self.folder,self.file = xbmcvfs.listdir(self.item['path'])
                if len(self.file)>0:
                    for self.fle in self.file:
                        self.ef = ""
                        self.ef = self.verifyFile(self.fle,self.item['path'])
                        if self.ef is not None:
                            self.sfle = os.path.splitext(self.fle)[0]
                            if sfnfo:
                                self.sf = ip.upDate(self.ef)
                            if self.sf == None:
                                self.sf={'title':self.sfle,'path':self.ef, 'sorttitle': self.sfle}
                            self.bonus.append(self.sf)
                if len(self.folder)>0:
                    for self.fold in self.folder:
                        self.ep = ""
                        self.ep=self.verifySub(self.fold,self.item['path'])
                        if self.ep is not None:
                            if sfnfo:
                                self.sf = ip.upDate(self.ep)
                            if self.sf == None:
                                self.sf={'title':self.fold,'path':self.ep,'sorttitle':self.fold}
                            self.bonus.append(self.sf)
            if len(self.bonus)>0:
                self.item.update({'bonus':self.bonus})
                carList.append(self.item)
            # else:
            #     return
    '''Getting Files'''
    def verifyFile(self,file,sp):
        self.dump = False
        self.sfil = os.path.join(sp,file)
        if exclude != '':
            self.d = re.search(exclude,self.sfil)
        else:
            self.d = ''
        if self.d:
            self.dump = True
        if not self.dump:
            return self.sfil
        return
    '''Our Extras folder has folders checking for 
            bluray and then dvds'''
    def verifySub(self,direct,sp):
        if '/' in self.f:
            self.sd = os.path.join(sp,direct)+'/'
        else:
            self.sd = os.path.join(sp,direct)+'\\'
        self.folder, self.file = xbmcvfs.listdir(self.sd)
        for self.itm in self.folder:
            if '/' in self.f:
                if 'BDMV' in self.itm:
                    self.ep = os.path.join(os.path.join(self.sd,self.itm)+'/','index.bdmv')
                elif 'VIDEO_TS' in self.itm:
                    self.ep = os.path.join(os.path.join(self.sd,self.itm)+'/','VIDEO_TS.IFO')
            elif '\\' in self.f:
                if 'BDMV' in self.itm:
                    self.ep = os.path.join(os.path.join(self.sd,self.itm)+'\\','index.bdmv')
                elif 'VIDEO_TS' in self.itm:
                    self.ep = os.path.join(os.path.join(self.sd,self.itm)+'\\','VIDEO_TS.IFO')
        self.verify = xbmcvfs.exists(self.ep)
        if self.verify == 1:
            return self.ep
        else:
            return
    def resultVar(self):
        self.tid = None
        self.mid = None
        self.tag = None
        self.top = None
        self.tr  = None
        self.co  = None
        try:
            self.tid = self.item['tvshowid']
        except:
            self.mid = self.item['movieid']
            self.tr = self.item['trailer']
            self.top = self.item['top250']
            self.tag = self.item['tag']
            self.co = self.item['country']
        self.t = self.item['title']
        self.y = self.item['year']
        self.f = self.item['file']
        self.m = self.item['mpaa']
        self.p = self.item['plot']
        self.pr = self.item['premiered']
        self.d = self.item['dateadded']
        self.v = self.item['votes']
        self.r = self.item['rating']
        self.ur = self.item['userrating']
        self.st = self.item['studio']
        self.a = self.item['art']
        self.c = self.item['cast']
        self.g = self.item['genre']
        self.ar = self.item['ratings']
        self.st = self.item['sorttitle']
        self.l = {'mid':self.mid,'tid':self.tid,'file':self.f,'title':self.t,'year':self.y,'mpaa':self.m,'plot':self.p,
                  'premiered':self.pr,'dateadded':self.d,'votes':self.v,'rating':self.r,'userrating':self.ur,'ratings':self.ar,
                  'trailer':self.tr,'top250':self.top,'studio':self.st,'art':self.a,'cast':self.c,'genre':self.g,'tag':self.tag,
                  'country':self.co, 'sorttitle':self.st}
class dbEnterExit:
    def initDb(self,action,item=""):
        if action == 'update':
            if Build().checkout()>0:
                home.setProperty('SFQUERY','true')
                self.sql = SQL()
                self.sql.setControl()
                self.insertDb()
                home.clearProperty('SFQUERY')
        elif action == 'clean':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.detchDb()
            home.clearProperty('SFQUERY')
        elif action == 'movies':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.queryDb('movies')
            home.clearProperty('SFQUERY')
            return carList
        elif action == 'tvshows':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.queryDb('tvshows')
            home.clearProperty('SFQUERY')
            return carList
        elif action == 'file':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.queryDb('file',item)
            home.clearProperty('SFQUERY')
            return fliList
        elif action == 'quikchk':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.queryDb('quikchk',item)
            home.clearProperty('SFQUERY')
            return self.result
        elif action == 'smallup':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.queryDb('smallup',item)
            home.clearProperty('SFQUERY')
        elif action == 'export':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.queryDb('export')
            home.clearProperty('SFQUERY')
        elif action == 'quikchk2':
            home.setProperty('SFQUERY','true')
            self.sql = SQL()
            self.sql.setControl()
            self.queryDb('quikchk2')
            home.clearProperty('SFQUERY')
    def insertDb(self):
        self.cst = 1
        bgdc(lang(30000),lang(30051))
        for self.item in carList:
            self.pct = float(self.cst)/float(len(carList))*100
            bgdu(int(self.pct),lang(30000),"{0} {1}{2}{3}".format(lang(30051),self.cst,lang(30052),len(carList)))
            #Movies
            if self.item['tid'] is None:
                self.entry = self.sql.exeCute('fw_movies',self.item['file'],'one')
                if self.entry is None:
                    self.input = (self.item['file'], self.item['title'],self.item['year'], self.item['plot'],
                                  self.item['rating'], self.item['votes'], self.item['dateadded'], self.item['mpaa'],
                                  self.item['premiered'], self.item['userrating'], self.item['top250'],
                                  self.item['trailer'], self.item['sorttitle'], self.item['mid']
                                  )
                    self.sql.exeCute('in_movies', self.input,'com')
            #TV Shows
            if self.item['mid'] is None:
                self.entry = self.sql.exeCute('fw_tvshows',self.item['file'],'one')
                if self.entry is None:
                    self.input = (self.item['file'], self.item['title'],self.item['year'], self.item['plot'],
                                  self.item['rating'], self.item['votes'], self.item['dateadded'], self.item['mpaa'],
                                  self.item['premiered'], self.item['userrating'], self.item['top250'],
                                  self.item['trailer'], self.item['sorttitle'], self.item['tid']
                                  )
                    self.sql.exeCute('in_tvshows', self.input,'com')
            #Bonus
            for self.bitem in self.item['bonus']:
                self.entry = self.sql.exeCute('fw_special2',self.bitem['path'],'one')
                if self.entry is None:
                    self.input = (self.item['file'],self.bitem['title'],self.bitem['path'],self.bitem['sorttitle'],self.bitem.get('plot'))
                    self.sql.exeCute('in_special', self.input,'com')
            #Art
            for self.aitem in self.item['art']:
                self.var = (self.item['file'],self.aitem)
                self.entry = self.sql.exeCute('fw_art2',self.var,'onev')
                if self.entry is None:
                    self.input = (self.item['file'],self.aitem,self.item['art'][self.aitem])
                    self.sql.exeCute('in_art', self.input,'com')
            #Cast
            for self.citem in self.item['cast']:
                self.var = (self.item['file'],self.citem['name'])
                self.entry = self.sql.exeCute('fw_cast2',self.var,'onev')
                if self.entry is None:
                    self.cname = self.citem.get('name')
                    self.cthumb = self.citem.get('thumbnail')
                    self.crole = self.citem.get('role')
                    self.corder = self.citem.get('order')
                    self.input = (self.item['file'],self.cname,self.cthumb,self.crole,self.corder)
                    self.sql.exeCute('in_cast', self.input,'com')
            self.cst+=1
        bgdcc()
    def verIfy(self,path):
        return xbmcvfs.exists(path)
    def detchDb(self):
        self.cst = 1
        bgdc(lang(30000),lang(30053))
        self.trAsh = list()
        self.entry = self.sql.exeCute('all_special','','all')
        for self.item in self.entry:
            if mysql == 'true':
                self.verify = self.verIfy(self.item['file'])
                if self.verify == 0:
                    self.trAsh.append(self.item['file'])
            else:
                self.verify = self.verIfy(self.item[0])
                if self.verify == 0:
                    self.trAsh.append(self.item[0])
        for self.item in self.trAsh:
            self.sql.exeCute('d_special',self.item,'com2')
        self.trAsh = list()
        self.entry = self.sql.exeCute('all_movies','','all')
        for self.item in self.entry:
            if mysql == 'true':     
                self.verify = self.verIfy(self.item['file'])
                if self.verify == 0:
                    self.trAsh.append(self.item['file'])
            else:   
                self.verify = self.verIfy(self.item[0])
                if self.verify == 0:
                    self.trAsh.append(self.item[0])
        for self.item in self.trAsh:
            self.pct = float(self.cst)/float(len(trAsh))*100
            bgdu(int(self.pct),lang(30000),"{0} {1}{2}{3}".format(lang(30053),self.cst,lang(30052),len(trAsh)))
            self.sql.exeCute('d_movies',self.item,'com2')
            self.sql.exeCute('d_art',self.item,'com2')
            self.sql.exeCute('d_cast',self.item,'com2')
            self.cst+=1
        self.cst=1
        self.trAsh = list()
        self.entry = self.sql.exeCute('all_tvshows','','all')
        for self.item in self.entry:
            if mysql == 'true':
                self.verify = self.verIfy(self.item['file'])
                if self.verify == 0:
                    self.trAsh.append(self.item['file'])
            else:
                self.verify = self.verIfy(self.item[0])
                if self.verify == 0:
                    self.trAsh.append(self.item[0])
        for self.item in self.trAsh:
            self.pct = float(self.cst)/float(len(trAsh))*100
            bgdu(int(self.pct),lang(30000),"{0} {1}{2}{3}".format(lang(30053),self.cst,lang(30052),len(trAsh)))
            self.sql.exeCute('d_tvshows',self.item,'com2')
            self.sql.exeCute('d_art',self.item,'com2')
            self.sql.exeCute('d_cast',self.item,'com2')
            self.cst+=1
    def queryDb(self,category,item=''):
        if category == 'movies':
            self.entry = self.sql.exeCute('all_movies','','all')
            if self.entry:
                for self.item in self.entry:
                    if mysql == 'true':
                        self.art = {}
                        self.cast = list()
                        self.ivar = (self.item['file'],)
                        self.aentry = self.sql.exeCute('fw_art',self.ivar,'allv')
                        if self.aentry:
                            for self.aitem in self.aentry:
                                    self.artl= {self.aitem['type']:self.aitem['location']}
                                    self.art.update(self.artl)
                        self.centry  = self.sql.exeCute('fw_cast',self.ivar,'allv')
                        for self.citem in self.centry:
                            self.actor={'name'       : self.citem['name'],
                                        'thumbnail'  : self.citem['thumbnail'],
                                        'role'       : self.citem['role'],
                                        'order'      : self.citem['ordr'],
                                        }          
                            self.cast.append(self.actor) 
                        self.input = {'file':self.item['file'], 'title':self.item['title'], 'year':self.item['year'],'plot':self.item['plot'],
                                      'rating':self.item['rating'], 'votes':self.item['votes'], 'dateadded':self.item['dateadded'], 'mpaa':self.item['mpaa'],
                                      'premiered':self.item['premiered'], 'userrating':self.item['userrating'],'top250':self.item['top250'], 'art':self.art,
                                      'trailer':self.item['trailer'], 'sorttitle':self.item['sorttitle'], 'movieid':self.item['mid'], 'cast':self.cast
                                      }
                    else:
                        self.art = {}
                        self.cast = list()
                        self.ivar = (self.item[0],)
                        self.aentry = self.sql.exeCute('fw_art',self.ivar,'allv')
                        if self.aentry:
                            for self.aitem in self.aentry:
                                    self.artl= {self.aitem[1]:self.aitem[2]}
                                    self.art.update(self.artl)
                        self.centry  = self.sql.exeCute('fw_cast',self.ivar,'allv')
                        for self.citem in self.centry:
                            self.actor={'name'       : self.citem[1],
                                        'thumbnail'  : self.citem[2],
                                        'role'       : self.citem[3],
                                        'order'      : self.citem[4],
                                        }          
                            self.cast.append(self.actor) 
                        self.input = {'file':self.item[0], 'title':self.item[1], 'year':self.item[2],'plot':self.item[3],
                                      'rating':self.item[4], 'votes':self.item[5], 'dateadded':self.item[5], 'mpaa':self.item[7],
                                      'premiered':self.item[8], 'userrating':self.item[9],'top250':self.item[10], 'art':self.art,
                                      'trailer':self.item[11], 'sorttitle':self.item[12], 'movieid':self.item[13], 'cast':self.cast
                                      }
                    carList.append(self.input)
            return carList
        elif category == 'tvshows':
            self.entry = self.sql.exeCute('all_tvshows','','all')
            if self.entry:
                for self.item in self.entry:
                    if mysql == 'true':
                        self.art = {}
                        self.cast = list()
                        self.ivar = (self.item['file'],)
                        self.aentry = self.sql.exeCute('fw_art',self.ivar,'allv')
                        if self.aentry:
                            for self.aitem in self.aentry:
                                    self.artl= {self.aitem['type']:self.aitem['location']}
                                    self.art.update(self.artl)
                        self.centry  = self.sql.exeCute('fw_cast',self.ivar,'allv')
                        for self.citem in self.centry:
                            self.actor={'name'       : self.citem['name'],
                                        'thumbnail'  : self.citem['thumbnail'],
                                        'role'       : self.citem['role'],
                                        'order'      : self.citem['ordr'],
                                        }          
                            self.cast.append(self.actor) 
                        self.input = {'file':self.item['file'], 'title':self.item['title'], 'year':self.item['year'],'plot':self.item['plot'],
                                      'rating':self.item['rating'], 'votes':self.item['votes'], 'dateadded':self.item['dateadded'], 'mpaa':self.item['mpaa'],
                                      'premiered':self.item['premiered'], 'userrating':self.item['userrating'],'top250':self.item['top250'], 'art':self.art,
                                      'trailer':self.item['trailer'], 'sorttitle':self.item['sorttitle'], 'tvshowid':self.item['tid'], 'cast':self.cast
                                      }
                    else:
                        self.art = {}
                        self.cast = list()
                        self.ivar = (self.item[0],)
                        self.aentry = self.sql.exeCute('fw_art',self.ivar,'allv')
                        if self.aentry:
                            for self.aitem in self.aentry:
                                    self.artl= {self.aitem[1]:self.aitem[2]}
                                    self.art.update(self.artl)
                        self.centry  = self.sql.exeCute('fw_cast',self.ivar,'allv')
                        for self.citem in self.centry:
                            self.actor={'name'       : self.citem[1],
                                        'thumbnail'  : self.citem[2],
                                        'role'       : self.citem[3],
                                        'order'      : self.citem[4],
                                        }          
                            self.cast.append(self.actor) 
                        self.input = {'file':self.item[0], 'title':self.item[1], 'year':self.item[2],'plot':self.item[3],
                                      'rating':self.item[4], 'votes':self.item[5], 'dateadded':self.item[5], 'mpaa':self.item[7],
                                      'premiered':self.item[8], 'userrating':self.item[9],'top250':self.item[10], 'art':self.art,
                                      'trailer':self.item[11], 'sorttitle':self.item[12], 'tvshowid':self.item[13], 'cast':self.cast
                                      }
                    carList.append(self.input)
            return carList
        elif category == 'file':
            self.ivar = (item,)
            self.entry = self.sql.exeCute('fw_special',self.ivar,'allv')
            if self.entry:
                for self.item in self.entry:
                    if mysql == 'true':
                        self.art = {}
                        self.cast = list()
                        self.aentry = self.sql.exeCute('fw_art',self.ivar,'allv')
                        if self.aentry:
                            for self.aitem in self.aentry:
                                    self.artl= {self.aitem['type']:self.aitem['location']}
                                    self.art.update(self.artl)
                        self.centry  = self.sql.exeCute('fw_cast',self.ivar,'allv')
                        for self.citem in self.centry:
                            self.actor={'name'       : self.citem['name'],
                                        'thumbnail'  : self.citem['thumbnail'],
                                        'role'       : self.citem['role'],
                                        'order'      : self.citem['ordr'],
                                        }          
                            self.cast.append(self.actor) 
                        self.input = {'file':self.item['file'], 'title':self.item['title'], 'path':self.item['bpath'],'sorttitle':self.item['sorttitle'],
                                      'plot':self.item['plot'], 'art':self.art, 'cast':self.cast
                                      }
                    else:
                        self.art = {}
                        self.cast = list()
                        self.aentry = self.sql.exeCute('fw_art',self.ivar,'allv')
                        if self.aentry:
                            for self.aitem in self.aentry:
                                    self.artl= {self.aitem[1]:self.aitem[2]}
                                    self.art.update(self.artl)
                        self.centry  = self.sql.exeCute('fw_cast',self.ivar,'allv')
                        for self.citem in self.centry:
                            self.actor={'name'       : self.citem[1],
                                        'thumbnail'  : self.citem[2],
                                        'role'       : self.citem[3],
                                        'order'      : self.citem[4],
                                        }          
                            self.cast.append(self.actor) 
                        self.input = {'file':self.item[0], 'title':self.item[1], 'path':self.item[2],'sorttitle':self.item[3],
                                      'plot':self.item[4], 'art':self.art, 'cast':self.cast
                                      }
                    fliList.append(self.input)
            return fliList
        elif category == 'quikchk':
            try:
                self.entry = self.sql.exeCute('fw_special3',item,'allv')
                for self.item in self.entry:
                    if mysql == 'true':
                        self.result = {'file':self.item['file'],'title':self.item['title'],'path':self.item['bpath'],'sorttitle':self.item['sorttitle'], 'plot':self.item['plot']}
                    else:
                        self.result = {'file':self.item[0],'title':self.item[1],'path':self.item[2],'sorttitle':self.item[3], 'plot':self.item[4]}
                return self.result
            except:
                error("Cant get result")
                quit()
        elif category == 'smallup':
            self.ivar = (item.get('title'),item.get('sorttitle'),item.get('plot'),item.get('file'),item.get('path'))
            self.test = (item['path'],)
            self.sql.exeCute('up_special',self.ivar,'com')
        elif category == 'export':
            self.entry = self.sql.exeCute('all_special','','all')
            ep.writeTree(self.entry)
        elif category == 'quikchk2':
            self.entry = self.sql.exeCute('fw_special',xbmc.getInfoLabel("ListItem.FileNameAndPath"),'one')
            if self.entry is None:
                home.clearProperty('sf_info')
            else:
                home.setProperty('sf_info','true')
    def quckEdit(self):
        self.qvar=unquote(xbmc.getInfoLabel("Container.FolderPath")).split('=')[3],xbmc.getInfoLabel("Container().ListItem().Label")
        self.bonus = dbEnterExit().initDb('quikchk',self.qvar)
        self.title = self.bonus['title']
        self.sorttitle = self.bonus['sorttitle']
        self.plot = self.bonus['plot']
        self.choice = dialog.contextmenu(['Edit title', 'Edit sort title', 'Edit plot'])
        if self.choice == 0:
            self.title = dialog.input(lang(30000), defaultt=self.bonus['title'], type=xbmcgui.INPUT_ALPHANUM)
        elif self.choice == 1:
            self.sorttitle = dialog.input(lang(30000), defaultt=self.bonus['sorttitle'], type=xbmcgui.INPUT_ALPHANUM)
        elif self.choice == 2:
            self.plot = dialog.input(lang(30000), defaultt=self.bonus['plot'], type=xbmcgui.INPUT_ALPHANUM)
        elif self.choice == -1:
            quit()
        self.update = {'file':self.bonus['file'],'title':self.title,'path':self.bonus['path'],'sorttitle':self.sorttitle,'plot':self.plot}
        dbEnterExit().initDb('smallup',self.update)
        xbmc.executebuiltin('Container.Update({})'.format(xbmc.getInfoLabel('Container.FolderPath')))
        quit()



    