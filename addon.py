import xbmc
import xbmcgui
import time
from libs.lib_monitor import libMonitor
from libs.db_defaults import dbFunctions

class li_main:
    def __init__(self):
        self.vars()
        xbmc.executebuiltin('Dialog.Close(all)')
        time.sleep(.2)
        # xbmc.executebuiltin('ActivateWindow(10138)')
        # time.sleep(.2)
        # xbmc.executebuiltin('Dialog.Close(all,true)')

        if self.window == 10025:
            xbmc.executebuiltin('Container.Update(\"%s\",return)' % self.url)
        else:
            xbmc.executebuiltin('ActivateWindow(videos, \"%s\",return)' % self.url)
    def vars(self):
        self.dbF    = dbFunctions()
        self.UP     = libMonitor()
        self.title  = xbmc.getInfoLabel("ListItem.Label")
        self.path   = xbmc.getInfoLabel("ListItem.FileNameAndPath")
        self.url    = self.dbF.get_url( title=str(self.title), action='listing', category=str(self.path))
        self.window = xbmcgui.getCurrentWindowId()
        
if __name__ == '__main__':
    li_main()

######## UPDATED 011718