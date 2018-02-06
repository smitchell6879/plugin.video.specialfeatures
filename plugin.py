from lib.database import *
from lib.sys_init import *
class Router:
    def __init__(self,args):
        info("plugin directing routes")
        self.router(args[2][1:])
    def router(self,params):
        self.params = dict(parse_qsl(params))
        if self.params:
            if self.params['action']=='bonus':
                Bonus().files(self.params['category'], self.params['title'])
            elif self.params['action']=='play':
                Player().play_video(self.params['video'])
            elif self.params['action']=='playall':
                Player().playlist(self.params['category'])
            elif self.params['action']=='all':
                Bonus().folders('all')
            elif self.params['action']=='movies':
                Bonus().folders('movies')
            elif self.params['action']=='tvshows':
                Bonus().folders('tvshows')
            else:
                raise error('Invalid params:{0}!'.format(params))
        else:
            Bonus().maindir()
            # Bonus().folders()
class Bonus:
    def var(self):
        self._url           = sys.argv[0]
        self._handle        = int(sys.argv[1])
    def item_var(self):
        self.art            = self.item.get('art','')
        self.fanart         = self.art.get('fanart','')
        self.poster         = self.art.get('poster', '')
        self.year           = self.item.get('year','')
        self.plot           = self.item.get('plot','')
        self.cast           = self.item.get('cast','')
        self.path           = self.item.get('file','')
        self.rating         = self.item.get('rating','')
        self.mpaa           = self.item.get('mpaa','')
        self.dateadded      = self.item.get('dateadded','')
    def constant(self):
        self.litem.setArt({'fanart': self.fanart, 'poster': self.poster})
        self.litem.setCast(self.item.get('cast',''))
        self.litem.setInfo('video',{'title': "{}".format(self.item.get('title', '')), 'year': "{}".format(self.item.get('year', '')), 'plot': self.item.get('plot', ''),'path': self.item.get('file',''), 'rating': self.item.get('rating', ''), 'mpaa': self.item.get('mpaa', ''), 'dateadded': self.item.get('dateadded', '')})
    def folders(self,listing):
        self.var()
        self.folders = list()
        if listing == 'all':
            self.folders = VIEWS().build_folders()
        if listing == 'movies':
            self.folders = VIEWS().build_folders()
        if listing == 'tvshows':
            return
        try:
            for self.item in self.folders:
                self.litem      = xbmcgui.ListItem(label="{}".format(self.item.get('title', '')))
                self.item_var()
                self.constant()
                self.is_folder  = True
                self.url        = self.get_url(action='bonus', category=self.item.get('category', ''), title="{}".format(self.item.get('title', '')))
                self.litem.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(self._handle, self.url, self.litem, self.is_folder)
            xbmcplugin.setContent(self._handle, 'movies')
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE )
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_MPAA_RATING )
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_VIDEO_YEAR )
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_VIDEO_RATING )
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_DATEADDED  )
            xbmcplugin.endOfDirectory(self._handle)
        except:
            error("NEED TO UPDATE DATABASE OR ADD MOVIES")
            return
    def files(self,category,title):
        for self.item in VIEWS().build_files(category):
            self.litem = xbmcgui.ListItem(label=title)
            self.var()
            self.item_var()
            self.bonus  = self.item.get('bonus', '')
            for self.item in self.bonus:
                self.title  = self.item.get('b_title','')
                self.video  = self.item.get('b_path','')
                self.litem.setProperty('IsPlayable', 'true')
                # self.constant()
                self.litem.setArt({'fanart': self.fanart, 'poster': self.poster})
                self.litem.setCast(self.cast)
                self.litem.setInfo('video',{'title':self.title, 'year': self.year, 'plot': self.plot, 'path':self.path, 'rating':self.rating, 'mpaa':self.mpaa, 'dateadded':self.dateadded})
                self.url = self.get_url(action='play', video=self.video)
                self.is_folder = False
                xbmcplugin.setPluginCategory(self._handle, title)
                xbmcplugin.setContent(self._handle, 'movies')
                xbmcplugin.addDirectoryItem(self._handle, self.url, self.litem, self.is_folder)
        if len(self.bonus) > 1:
            if playall == 'true':
                self._playall = xbmcgui.ListItem(label=lang(30025))
                self._playall.setArt({'fanart': self.fanart, 'poster': self.poster})
                self._playall.setProperty('IsPlayable', 'true')
                self._playall.setCast(self.cast)
                self._playall.setInfo('video',{'year': self.year, 'plot':lang(30038), 'path':self.path, 'rating':self.rating, 'mpaa':self.mpaa, 'dateadded':self.dateadded})
                self.url = self.get_url(action='playall', category=category)
                xbmcplugin.addDirectoryItem(self._handle,self.url, self._playall, self.is_folder)
        xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE )
        xbmcplugin.endOfDirectory(self._handle)
    def maindir(self):
        self.dirvis = 'false'
        self.maindir = list()
        if showalldir =='true':
            self.maindir.append({'title':'Show All Extras','category':'all'})
            self.dirvis = 'true'
        if moviedir == 'true':
            self.maindir.append({'title':'Movie Extras','category':'movies'})
            self.dirvis = 'true'
        if tvshowdir == 'true':
            self.maindir.append({'title':'TV Show Extras','category':'tvshows'})
            self.dirvis = 'true'
        if self.dirvis == 'false':
            self.chk = dialog.yesno(lang(30000),lang(30067),lang(30068))
            if self.chk == 1:
                xbmc.executebuiltin('Addon.OpenSettings({})'.format(addonid))
            else:
                return
        self.var()
        try:
            for self.item in self.maindir:
                self.litem      = xbmcgui.ListItem(label="{}".format(self.item.get('title', '')))
                self.is_folder  = True
                self.url        = self.get_url(action=self.item.get('category', ''), category=self.item.get('category', ''), title="{}".format(self.item.get('title', '')))
                self.litem.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(self._handle, self.url, self.litem, self.is_folder)
            xbmcplugin.setContent(self._handle, 'videos')
            xbmcplugin.addSortMethod(self._handle, xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE )
            xbmcplugin.endOfDirectory(self._handle)
        except:
            error("NEED TO UPDATE DATABASE OR ADD MOVIES OR TVSHOWS")
            return
    def get_url(self,**kwargs):
        return '{0}?{1}'.format(self._url,urlencode(kwargs))
class Player:
    def play_video(self,path):
        self._handle        = int(sys.argv[1])
        self.play_item = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(self._handle, True, listitem=self.play_item)
    def playlist(self,category):
        play.clear()
        for self.item in VIEWS().build_files(category):
            self.art            = self.item.get('art','')
            self.fanart         = self.art.get('fanart','')
            self.poster         = self.art.get('poster', '')
            self.year           = self.item.get('year','')
            self.plot           = self.item.get('plot','')
            self.cast           = self.item.get('cast','')
            self.path           = self.item.get('file','')
            self.rating         = self.item.get('rating','')
            self.mpaa           = self.item.get('mpaa','')
            self.dateadded      = self.item.get('dateadded','')
            self.bonus = self.item.get('bonus', '')
            for self.item in self.bonus:
                self.title=self.item.get('b_title','')
                self.video=self.item.get('b_path','')
                self.litem = xbmcgui.ListItem(label=self.title)
                self.litem.setArt({'fanart': self.fanart, 'poster': self.poster})
                self.litem.setCast(self.cast)
                self.litem.setInfo('video',{'title':self.title, 'year': self.year, 'plot': self.plot, 'path':self.path, 'rating':self.rating, 'mpaa':self.mpaa, 'dateadded':self.dateadded})
                play.add(url=self.video,listitem=self.litem)
        xbmc.Player().play(play)          
if __name__ == '__main__':
    # encoding()
    # UPDATEDB()
    Router(sys.argv)