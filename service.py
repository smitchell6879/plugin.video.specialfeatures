from lib.sys_init import *
from lib.iteration import *



if __name__ == '__main__':
    if sys.version_info[0]<3:
        encoding()
    while not monitor.abortRequested():
        if home.getProperty('SFQUERY') != 'true':
            dbEnterExit().initDb('quikchk2')
        if monitor.waitForAbort(.8):
            break