import xbmc
import xbmcgui
from lib.lib_monitor import libMonitor
from lib.lib_monitor import Player
from lib.db_defaults import dbFunctions
_dialog     = xbmcgui.Dialog()


class main:
    def vars(self):
        self.home       = xbmcgui.Window(10000)
        self.monitor    = xbmc.Monitor()
        self.dbF        = dbFunctions()
        self.UP         = libMonitor()
        self.playtime       = Player()


    def __init__(self):
        self.vars()
        self.dbF.endcoding()
        while not self.monitor.abortRequested():
            self.UP
            # self.path = xbmc.getInfoLabel("ListItem.FileNameAndPath")
            self.cc = xbmc.getInfoLabel("System.CurrentControl")            
            if self.home.getProperty('SF_updateing') != 'true':
                self.playtime.init(self.cc)
                self.dbF.query_li()
            if self.monitor.waitForAbort(.75):
                break


if __name__ == '__main__':    
    main()

###################### Updated 011718