from lib.sys_init import *
from lib.iteration import *



if __name__ == '__main__':
    if sys.version_info[0]<3:
        encoding()
    while not monitor.abortRequested():
    	showcon    = addon.getSetting('showcon')
    	home.setProperty('SpecialFeatures.ContextMenu',showcon)
    	if home.getProperty('SpecialFeatures.Query') != 'true':
            dbEnterExit().initDb('quikchk2')
        if monitor.waitForAbort(.6):
            break
