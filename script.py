from lib.sys_init import *
from lib.iteration import *
from lib.importexport import *


class Routines:
    def updateDB(self):
        query = 'movies'
        query2 = 'tvshows'
        note(txt=lang(30050))
        resultFILTER().router(query)
        resultFILTER().router(query2)
        dbEnterExit().initDb('update')
        exit()
    def cleanDb(self):
        dbEnterExit().initDb('clean')
    def editInfo(self):
        dbEnterExit().quckEdit()
    def exportDb(self):
        dbEnterExit().initDb('export')
    def listItem(self):
        self.url = self.get_url(directory='files', item=home.getProperty('sf_item'), category=xbmc.getInfoLabel("ListItem.DBTYPE"))
        xbmc.executebuiltin('ActivateWindow(videos,{},return)'.format(self.url))    
    def get_url(self,**kwargs):
        return '{0}?{1}'.format("plugin://plugin.specialfeatures/",urlencode(kwargs))


   


if __name__ == '__main__':
    r = Routines()
    if sys.version_info[0]<3:
        encoding()
    if len(sys.argv)>1:
        if sys.argv[1] == 'scandb':
            r.updateDB()
        elif sys.argv[1] == 'listitem':
            r.listItem()
        elif sys.argv[1] == 'cleandb':
            r.cleanDb()
        elif sys.argv[1] == 'export':
            r.exportDb()
        elif sys.argv[1] == 'editinfo':
            r.editInfo()
        elif sys.argv[1] == 'test':
            text(xbmc.getInfoLabel("ListItem.DBTYPE"))
    else:
        xbmc.executebuiltin('Addon.OpenSettings({})'.format(addonid))