from lib.sys_init import *
from lib.database import *



if __name__ == '__main__':
    if sys.version_info[0]<3:
        encoding()
    if len(sys.argv)>1:
        if sys.argv[1] == 'scandb':
            UPDATEDB()
        # elif sys.argv[1] == 'listitem':
        #     li_main().__init__()
        elif sys.argv[1] == 'cleandb':
            CLEANUP()
        # elif sys.argv[1] == 'scandbmd':
        #     dbFunctions().scn_dbmd()
        # elif sys.argv[1] == 'test':
        #     SpecialFeatures()
        #     # dbFunctions().test()

    else:
        xbmc.executebuiltin('Addon.OpenSettings({})'.format(addonid))

# def context():
#     addon_data=xbmcvfs.exists(_addon_set)
#     status=_addon.getSetting("context-menu")
#     if status == "true":
#         status=_addon.getLocalizedString(30005)
#         yes=_addon.getLocalizedString(30008)
#     else:
#         status=_addon.getLocalizedString(30007)
#         yes=_addon.getLocalizedString(30006)
#     menu=_dialog.yesno(_addon.getLocalizedString(30009),_addon.getLocalizedString(30023)+" "+"{}".format(status),yeslabel=yes,nolabel=_addon.getLocalizedString(30024)) 
    
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
#                         # line.text = "{}".format('false')
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
