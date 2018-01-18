import xbmc
import xbmcaddon
import xbmcgui
from libs.db_defaults import dbFunctions

_monitor    = xbmc.Monitor()
_dialog     = xbmcgui.Dialog()
_dbF        = dbFunctions()
_addon		= xbmcaddon.Addon()
_updb		= 'true'

class libMonitor(xbmc.Monitor):
    def onScanFinished(self, library):
        if _addon.getSetting('updb') == "true":
        	_dbF.scn_db(_updb)
    def  onCleanFinished(self, library):
        if _addon.getSetting('clndb') == "true":
        	_dbF.cln_db()
    # def onSettingsChanged(self):
    # 	_dialog.ok('test1',"")







####### Updated 011818