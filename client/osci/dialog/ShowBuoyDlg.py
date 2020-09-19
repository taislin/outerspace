

import pygameui as ui, string
from osci import client, gdata
import ige.ospace.Const as Const

class ShowBuoyDlg:

    def __init__(self, app):
        self.app = app
        self.createUI()

    def display(self, objID):
        player = client.getPlayer()
        text = []
        if hasattr(player, "buoys") and objID in player.buoys:
            label = _("Private buoy text")
            if player.buoys[objID][1] == Const.BUOY_TO_ALLY:
                label = u"%s%s:" % (label, _(" (visible to allies)"))
            else:
                label = u"%s:" % label
            text.append(label)
            text.extend(player.buoys[objID][0].split("\n"))
            text.append("")

        if hasattr(player, "alliedBuoys") and objID in player.alliedBuoys:
            text.append(_("Buoy texts from allies:"))
            for buoy in player.alliedBuoys[objID]:
                text.extend(buoy[0].split("\n"))
                text.append(_('(Author: %s)') % buoy[2]) #owner's name
                text.append("")

        self.win.vText.text = text
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
        self.win.show()

    def onOK(self, widget, action, data):
        self.hide()

    def createUI(self):
        w, h = gdata.scrnSize
        cols = 20
        rows = 13
        width = cols * 20 + 4
        height = rows * 20 + 24
        self.win = ui.Window(self.app,
            modal = 1,
            escKeyClose = 1,
            movable = 0,
            title = _("Show buoy text"),
            rect = ui.Rect((w - width) / 2, (h - height) / 2, width, height),
            layoutManager = ui.SimpleGridLM(),
        )
        # creating dialog window
        self.win.subscribeAction('*', self)

        s = ui.Scrollbar(self.win, layout = (cols - 1, 0, 1, rows - 1))
        t = ui.Text(self.win, id = 'vText',
            align = ui.ALIGN_W,
            layout = (0, 0, cols - 1, rows - 1),
            editable = 0
        )
        t.attachVScrollbar(s)

        ui.Title(self.win, layout = (0, rows - 1, cols - 5, 1))
        okBtn = ui.TitleButton(self.win, layout = (cols - 5, rows - 1, 5, 1), text = _("OK"), action = 'onOK')
