import xbmc
import xbmcgui
from libs.lib_monitor import libMonitor
from libs.db_defaults import dbFunctions


class main:
    def vars(self):
        self.home       = xbmcgui.Window(10000)
        self.monitor    = xbmc.Monitor()
        self.dbF        = dbFunctions()
        self.UP         = libMonitor()

    def __init__(self):
        self.vars()
        self.dbF.endcoding()
        while not self.monitor.abortRequested():
            self.UP
            if self.home.getProperty('SF_updateing') != 'true':
                self.dbF.query_li()
            if self.monitor.waitForAbort(.6):
                break


if __name__ == '__main__':    
    main()

###################### Updated 011718