from lib.sys_init import *

class LISTS:
    def bonus(self):
        if aupdb == 'true':
            note(txt=lang(30062))
        info("Gathering bonusmaterial")
        self.movies,self.lib = QUERYKODI().bonusmaterial()
        self.filtered(self.movies,self.lib)
        if aupdb == 'true':
            note(txt=lang(30061))
        return self.bonusmaterial
    def filtered(self,iterate,lists):
        info("Checking for Bonus Material")
        self.bonusmaterial=list()
        if aupdb == 'false':
            dialpro.create(lang(30000),lang(30015))
        else:
            dialbg.create(lang(30000),lang(30015))
        self.pc = 1
        for self.item in iterate['result']['movies']:
            time.sleep(.01)
            self.percent    = float(self.pc)/float(lists)*100
            self.title      = self.item.get('title','')
            self.year       = self.item.get('year','')
            self.file       = self.item.get('file','')
            if aupdb == 'false':
                dialpro.update(int(self.percent),lang(30015)+"{}".format(self.pc)+lang(30016)+"{}".format(lists),"{} ({})".format(self.title,self.year),)
                self.pc += 1
                if dialpro.iscanceled():
                    return
            else:
                dialbg.update(int(self.percent),lang(30015)+"{}".format(self.pc)+lang(30016)+"{}".format(lists),"{} ({})".format(self.title,self.year),)
                self.pc += 1
            if "\BDMV" in self.file:
                self.folder(self.file,"\BDMV","\\")
            elif "/BDMV" in self.file:
                self.folder(self.file,"/BDMV","/")
            elif "\VIDEO_TS" in self.file:
                self.altfolder(self.file,"\VIDEO_TS","\\")
            elif "/VIDEO_TS" in self.file:
                self.altfolder(self.file,"/VIDEO_TS","/")
            else:
                self.nfile = os.path.basename(self.file)
                self.path, self.dump = self.file.strip().split(self.nfile)
                if "/" in self.file:
                    self.path = self.path+folder+"/"
                else:
                    self.path= self.path+folder+"\\"
            self.get_bonus(self.path)

            
    def folder(self,file,ext,con):
        self.path,self.dump = file.strip().split(ext)
        self.path = self.path+con+folder+con
        return  self.path
    def altfolder(self,file,ext,con):
        self.path,self.dump,self.dump = file.strip().split(ext)
        self.path = self.path+con+folder+con
        return  self.path
    def get_bonus(self,path):
        if xbmcvfs.exists(path):
            self.bonus=list()
            self.dirs, self.files = xbmcvfs.listdir(path)
            self.get_files(self.files,path)
            self.get_folder(self.dirs,path)
            self.item.update({'bonus':self.bonus})
            self.bonusmaterial.append(self.item)
        return
    def get_folder(self,files,parent):
            for self.b_title in files:
                if "/" in parent:
                    self.dir=parent+self.b_title+"/"
                else:
                    self.dir=parent+self.b_title+"\\"
                self.dirs,self.files=xbmcvfs.listdir(self.dir)
                for self.di in self.dirs:
                    if self.di == "BDMV":
                        if "/" in parent:
                            self.b_path = self.dir+self.di+"/index.bdmv"
                        else:
                            self.b_path = self.dir+self.di+"\index.bdmv"
                        self.bonus.append({'b_title': self.b_title, 'b_path': self.b_path})
                    elif self.di == "VIDEO_TS":
                        if "/" in parent:
                            self.b_path = self.dir+self.di+"/VIDEO_TS.IFO"
                        else:
                            self.b_path = self.dir+self.di+"\VIDEO_TS.IFO"
                        self.bonus.append({'b_title': self.b_title, 'b_path': self.b_path})                        
            return
    def get_files(self,files,parent):
        for self.file in files:
            self.ignore = False
            if exclude != "":
                self.dump = re.search(exclude,self.file)
            else:
                self.dump = ""
            if self.dump:
                self.ignore = True
            if not self.ignore:
                self.b_title = os.path.splitext(self.file)[0]
                self.b_path = parent+self.file
                self.bonus.append({'b_title':self.b_title,'b_path':self.b_path})
        return
    def bonusfolders(self):
        info("Building Movie View")
        return
    


class QUERYKODI:
    def jsonquery(self,query):
        info("Making request to Kodi")
        self.jsonq = xbmc.executeJSONRPC("{}".format(query))
        # self.jsonc = unicode(self.jsonq, 'utf-8',errors='ignore')
        self.json  = json.loads(self.jsonq)
        return self.json
    def bonusmaterial(self):
        self.query  = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies","params": {"properties": ["title","genre","year","rating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art","userrating","ratings","premiered","uniqueid"], "sort": { "method": "label" } }, "id": 1}'
        self.result = self.jsonquery(self.query)
        self.totals = list()
        if 'result' in self.result:
            if self.result['result']['limits'].get('total','') != 0:
                if 'movies' in self.result['result']:
                    for self.item in self.result['result']['movies']:
                        self.totals.append(self.item.get('title',''))
                    self.total = len(self.totals)
                    if self.total > 0:
                        return self.result,self.total
                    else:
                        error("NO MOVIES AND MOVIES TO LIBRARY THEN IT WORK")
                        return
            else:
                ok(lang(30065)+"[CR]"+lang(30066))
                sys.exit(1)
                

        


