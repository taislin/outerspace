

import gdata
from dialog import ProgressDlg
from dialog import PlayerSelectDlg
import pygame
from ige import log

# module globals
progressDlg = None

def onInitConnection():
    pass

def onConnInitialized():
    pass

def onCmdBegin():
    if gdata.mainGameDlg:
        gdata.mainGameDlg.onCmdInProgress(1)
    else:
        gdata.cmdInProgress = 1
    gdata.app.update()

def onCmdEnd():
    if gdata.mainGameDlg:
        gdata.mainGameDlg.onCmdInProgress(0)
    else:
        gdata.cmdInProgress = 0
    gdata.app.update()

def onUpdateStarting():
    global progressDlg
    log.debug("onUpdateStarting")
    if not progressDlg:
        progressDlg = ProgressDlg(gdata.app)
    progressDlg.display(_('Updating OSCI database...'), 0, 1)

def onUpdateProgress(curr, max, text = None):
    global progressDlg
    log.debug("onUpdateProgress")
    progressDlg.setProgress(text, curr, max)

def onUpdateFinished():
    global progressDlg
    log.debug("onUpdateFinished")
    try:
        progressDlg.hide()
    except:
        log.warning("Cannot delete progressDlg window")
    for dialog in gdata.updateDlgs:
        dialog.update()

def onNewMessages(number):
    gdata.mainGameDlg.messagesDlg.update()

def onWaitingForResponse():
    #pygame.event.pump()
    while pygame.event.poll().type != pygame.NOEVENT:
        pass
