#
#  Copyright 2001 - 2016 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of Outer Space.
#
#  Outer Space is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  Outer Space is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Outer Space; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from .gdata import GData
from .dialog import ProgressDlg
from .dialog import PlayerSelectDlg
import pygame
from ige import log

# module globals
progressDlg = None

def onInitConnection():
    pass

def onConnInitialized():
    pass

def onCmdBegin():
    if GData.mainGameDlg:
        GData.mainGameDlg.onCmdInProgress(1)
    else:
        GData.cmdInProgress = 1
    GData.app.update()

def onCmdEnd():
    if GData.mainGameDlg:
        GData.mainGameDlg.onCmdInProgress(0)
    else:
        GData.cmdInProgress = 0
    GData.app.update()

def onUpdateStarting():
    global progressDlg
    log.debug("onUpdateStarting")
    if not progressDlg:
        progressDlg = dialog.ProgressDlg(GData.app)
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
    for dialog in GData.updateDlgs:
        dialog.update()

def onNewMessages(number):
    GData.mainGameDlg.messagesDlg.update()

def onWaitingForResponse():
    #pygame.event.pump()
    while pygame.event.poll().type != pygame.NOEVENT:
        pass
