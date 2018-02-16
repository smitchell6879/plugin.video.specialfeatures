from lib.sys_init import *
# import xbmc
# from addon import li_main
# from libs.db_defaults import dbFunctions

if __name__ == '__main__':
    if len(sys.argv)>1:
        if sys.argv[1] == 'scandb':
            dbFunctions().scn_db()
        elif sys.argv[1] == 'listitem':
            li_main().__init__()
        elif sys.argv[1] == 'cleandb':
            dbFunctions().cln_db()
        elif sys.argv[1] == 'test':
            QUERY()
    else:
        if xbmcgui.getCurrentWindowId() == 10025:
            xbmc.executebuiltin('Container.Update(\"%s\",return)' % _url)
        else:
            xbmc.executebuiltin('ActivateWindow(videos, \"%s\",return)' % _url)




def jsonquery():
        # self.query  = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies","params": {"properties": ["title","genre","year","rating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art","userrating","ratings","premiered","uniqueid"], "sort": { "method": "label" } }, "id": 1}'
        self.query  = '{"jsonrpc": "2.0", "method": "VideoLibrary.TVShows","params": {"properties": ["title","genre","year","rating","plot","studio","mpaa","cast","playcount","episode","imdbnumber","premiered","votes","lastplayed","fanart","thumbnail","file","originaltitle","sorttitle","episodeguide","season","watchedepisodes","dateadded","tag","art","userrating","ratings","runtime","uniqueid"], "sort": { "method": "label" } }, "id": 1}'
        self.jsonq = xbmc.executeJSONRPC("{}".format(query))
        self.json  = json.loads(self.jsonq)
        text(self.json)
        
# def context():
#     addon_data=xbmcvfs.exists(_addon_set)
#     status=_addon.getSetting("context-menu")
#     if status == "true":
#         status=_addon.getLocalizedString(30005)
#         yes=_addon.getLocalizedString(30008)
#     else:
#         status=_addon.getLocalizedString(30007)
#         yes=_addon.getLocalizedString(30006)
#     menu=_dialog.yesno(_addon.getLocalizedString(30009),_addon.getLocalizedString(30023)+" "+str(status),yeslabel=yes,nolabel=_addon.getLocalizedString(30024)) 
    
#     if status == _addon.getLocalizedString(30005) and menu == 1:
#         if addon_data:
#             read = ET.parse(_addon_set)
#             line = read.getroot()
#             for line in line:
#                 l = line.attrib
#                 l = l.get('id')
#                 if l == 'context-menu':
#                     li=line.text
#                     if li == 'true':
#                         # line.text = str('false')
#                         # read.write(_addon_set)
#                         _addon.setSetting(id='context-menu', value='false')
#                         _dialog.ok(_addon.getLocalizedString(30000),_addon.getLocalizedString(30017)) 
#                         return
            
#     elif status == _addon.getLocalizedString(30007) and menu == 1:
#         if addon_data:
#             read = ET.parse(_addon_set)
#             line = read.getroot()
#             for line in line:
#                 l = line.attrib
#                 l = l.get('id')
#                 if l == 'context-menu':
#                     li=line.text
#                     if li == 'false':
#                         _addon.setSettingBool(id='context-menu',value=1)
#                         _dialog.ok(_addon.getLocalizedString(30000),_addon.getLocalizedString(30017)) 

#                         return
#     else:
#         return
