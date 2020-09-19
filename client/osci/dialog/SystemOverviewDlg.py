

import pygameui as ui
from osci.StarMapWidget import StarMapWidget
from osci import gdata, res, client, sequip
import ige.ospace.Const as Const
from ige.ospace import ShipUtils, Rules
from ige import GameException
import math

class SystemOverviewDlg:

    def __init__(self, app):
        self.app = app
        self.showMine = 1
        self.showColonizable = 0
        self.showOtherPlayers = 0
        self.showUncolonizable = 0
        self.showProblems = 0
        self.createUI()

    def display(self):
        self.show()
        self.win.show()
        # register for updates
        if self not in gdata.updateDlgs:
            gdata.updateDlgs.append(self)

    def hide(self):
        self.win.setStatus(_("Ready."))
        self.win.hide()
        # unregister updates
        if self in gdata.updateDlgs:
            gdata.updateDlgs.remove(self)

    def update(self):
        self.show()

    def show(self):
        items = []
        player = client.getPlayer()
        #
        for systemID in client.db.keys():
            if systemID == player.oid:
                continue
            system = client.get(systemID, noUpdate=1)

            if not hasattr(system, 'planets'):
                continue
            planetsMine = 0
            planetsOwned = 0
            planetsUnowned = 0
            planetsGA = 0
            planetsNotMine = 0
            en = 0
            bio = 0
            enres = 0
            biores = 0
            stratRes = Const.SR_NONE
            refuelMax = 0
            refuelInc = 0
            upgradeShip = 0
            repairShip = 0
            speedBoost = 0
            useOwner = Const.OID_NONE
            for planetID in system.planets:
                planet = client.get(planetID, noUpdate=1)
                owner = getattr(planet, 'owner', Const.OID_NONE)
                if owner != Const.OID_NONE:
                    useOwner = owner
                    if owner == player.oid:
                        planetsMine += 1
                    else:
                        planetsOwned += 1
                        if self.showOtherPlayers:
                            planetsNotMine += 1
                    en += getattr(planet, 'changeEn', 0)
                    bio += getattr(planet, 'changeBio', 0)
                    enres += getattr(planet, 'storEn', 0)
                    biores += getattr(planet, 'storBio', 0)
                    stratRes = getattr(planet, 'plStratRes', Const.SR_NONE) if stratRes == Const.SR_NONE else stratRes
                    refuelMax = max(getattr(planet, 'refuelMax', 0), refuelMax)
                    refuelInc = max(getattr(planet, 'refuelInc', 0), refuelInc)
                    upgradeShip += getattr(planet, 'upgradeShip', 0)
                    repairShip = max(getattr(planet, 'repairShip', 0), repairShip)
                    speedBoost = max(getattr(planet, 'fleetSpeedBoost', 0), speedBoost)
                else:
                    if hasattr(planet, "plType") and planet.plType in ("A", "G"):
                        planetsGA += 1
                        if self.showUncolonizable:
                            planetsNotMine += 1
                    else:
                        planetsUnowned += 1
                        if self.showColonizable:
                            planetsNotMine += 1
            if planetsMine == 0:  # fix no-data systems
                en = '?'
                bio = '?'
                enres = '?'
                biores = '?'
            if ((planetsMine and self.showMine)
                    or (planetsOwned and self.showOtherPlayers)
                    or (planetsUnowned and self.showColonizable)
                    or (planetsGA and self.showUncolonizable)):
                if stratRes == Const.SR_NONE:
                    stratResText = ' '
                else:
                    stratResText = gdata.stratRes[stratRes]
                problem = (bio < 0 or en < 0)
                if planetsMine > 0:  # make sure you own it
                    useOwner = player.oid
                if speedBoost > 1:
                    speedBoost = int((speedBoost - 1) * 100)
                else:
                    speedBoost = ''
                if self.showProblems:
                    color = res.getSystemOverviewProblemColor(useOwner, problem)
                else:
                    color = res.getPlayerColor(useOwner)
                item = ui.Item(
                    getattr(system, 'name', res.getUnknownName()),
                    tSyPnum=planetsMine + planetsOwned + planetsUnowned + planetsGA,
                    tSyPTnum=planetsNotMine,
                    tSyPYnum=planetsMine,
                    tSyBioRes=biores,
                    tSyEnRes=enres,
                    tSyBio=bio,
                    tSyEn=en,
                    tSyRefuel=refuelInc,
                    tSyRefuelMax=refuelMax,
                    tSyRepair=(repairShip * 100),
                    tSyUpgrade=int(upgradeShip),
                    tSyGate=speedBoost,
                    tStRes=_(stratResText),
                    tSysID=systemID,
                    foreground=color,
                )
                items.append(item)
        self.win.vPlanets.items = items
        self.win.vPlanets.itemsChanged()
        # buttons
        self.win.vMine.pressed = self.showMine
        self.win.vOtherPlayers = self.showOtherPlayers
        self.win.vColonizable = self.showColonizable
        self.win.vUncolonizable = self.showUncolonizable
        self.win.vProblems = self.showProblems

    def onSelectSystem(self, widget, action, data):
        item = self.win.vPlanets.selection[0]
        player = client.getPlayer()
        system = client.get(item.tSysID, noUpdate=1)
        if item.tSyPYnum > 0:  # you own
            # show dialog
            gdata.mainGameDlg.onSelectMapObj(None, None, item.tSysID)
        else:
            # center on map
            if hasattr(system, "x"):
                gdata.mainGameDlg.win.vStarMap.highlightPos = (system.x, system.y)
                gdata.mainGameDlg.win.vStarMap.setPos(system.x, system.y)
                self.hide()
                return
            self.win.setStatus(_("Cannot show location"))

    def onShowLocation(self, widget, action, data):
        item = self.win.vPlanets.selection[0]
        system = client.get(item.tSysID, noUpdate=1)
        if hasattr(system, "x"):
            gdata.mainGameDlg.win.vStarMap.highlightPos = (system.x, system.y)
            gdata.mainGameDlg.win.vStarMap.setPos(system.x, system.y)
            self.hide()
            return
        self.win.setStatus(_("Cannot show location"))

    def onToggleCondition(self, widget, action, data):
        setattr(self, widget.data, not getattr(self, widget.data))
        self.update()

    def onClose(self, widget, action, data):
        self.hide()

    def createUI(self):
        w, h = gdata.scrnSize
        self.win = ui.Window(self.app,
                             modal=1,
                             escKeyClose=1,
                             titleOnly=w == 800 and h == 600,
                             movable=0,
                             title=_('Systems Overview'),
                             rect=ui.Rect((w - 800 - 4 * (w != 800)) / 2,
                                          (h - 600 - 4 * (h != 600)) / 2,
                                          800 + 4 * (w != 800),
                                          580 + 4 * (h != 600)),
                             layoutManager=ui.SimpleGridLM(),
        )
        self.win.subscribeAction('*', self)
        # playets listbox
        ui.Listbox(self.win, layout=(0, 0, 40, 26), id='vPlanets',
                   columns=[(_('System'), 'text', 5.75, ui.ALIGN_W),
                   (_('# Pl'), 'tSyPnum', 2, ui.ALIGN_E),
                   (_('Mine'), 'tSyPYnum', 2, ui.ALIGN_E),
                   (_('Other'), 'tSyPTnum', 2, ui.ALIGN_E),
                   (_('Biomatter'), 'tSyBioRes', 3, ui.ALIGN_E),
                   (_('Bio+-'), 'tSyBio', 2, ui.ALIGN_E),
                   (_('En'), 'tSyEnRes', 3, ui.ALIGN_E),
                   (_('En+-'), 'tSyEn', 2, ui.ALIGN_E),
                   (_('%Fuel'), 'tSyRefuel', 2.25, ui.ALIGN_E),
                   (_('%Max'), 'tSyRefuelMax', 2.25, ui.ALIGN_E),
                   (_('%Repair'), 'tSyRepair', 3, ui.ALIGN_E),
                   (_('Upgrade'), 'tSyUpgrade', 3, ui.ALIGN_E),
                   (_('+Gate %'), 'tSyGate', 3, ui.ALIGN_E),
                   (_('Strat Res'), 'tStRes', 3.75, ui.ALIGN_E)],
                   columnLabels=1, action='onSelectSystem', rmbAction="onShowLocation")
        ui.Button(self.win, layout=(0, 26, 5, 1), text=_('My Systems'), id="vMine",
                  toggle=1, action="onToggleCondition", data="showMine")
        ui.Button(self.win, layout=(5, 26, 5, 1), text=_('Other Cmdrs'), id="vOtherPlayers",
                  toggle=1, action="onToggleCondition", data="showOtherPlayers")
        ui.Button(self.win, layout=(10, 26, 5, 1), text=_('Colonizable'), id="vColonizable",
                  toggle=1, action="onToggleCondition", data="showColonizable")
        ui.Button(self.win, layout=(15, 26, 5, 1), text=_('Uncolonizable'), id="vUncolonizable",
                  toggle=1, action="onToggleCondition", data="showUncolonizable")
        ui.Button(self.win, layout=(20, 26, 5, 1), text=_('Show Problems'), id="vProblems",
                  toggle=1, action="onToggleCondition", data="showProblems")
        # status bar + submit/cancel
        ui.TitleButton(self.win, layout=(35, 27, 5, 1), text=_('Close'), action='onClose')
        ui.Title(self.win, id='vStatusBar', layout=(0, 27, 35, 1), align=ui.ALIGN_W)
        # self.win.statusBar=self.win.vStatusBar
