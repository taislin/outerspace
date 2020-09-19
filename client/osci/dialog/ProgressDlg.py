

import pygameui as ui
from osci import res, gdata

class ProgressDlg:

    def __init__(self, app):
        self.app = app
        self.createUI()

    def display(self, title, min, max):
        self.win.title = title
        self.win.vProgress.min = min
        self.win.vProgress.max = max
        self.setProgress(title, min)
        self.win.show()

    def hide(self):
        self.win.destroy()

    def setProgress(self, text, current = None, max = None):
        if text:
            self.win.vText.text = [text]
        if max != None:
            self.win.vProgress.min = 0
            self.win.vProgress.max = max
        if current != None:
            self.win.vProgress.value = current
        self.app.update()


    def createUI(self):
        w, h = gdata.scrnSize
        self.win = ui.Window(self.app,
            modal = 1,
            movable = 0,
            title = _('Question'),
            rect = ui.Rect((w - 424) / 2, (h - 124) / 2, 424, 124),
            layoutManager = ui.SimpleGridLM(),
        )
        self.win.subscribeAction('*', self)
        ui.Text(self.win, layout = (5, 1, 15, 1), id = 'vText', background = self.win.app.theme.themeBackground, editable = 0)
        ui.ProgressBar(self.win, layout = (5, 2, 15, 1), id = 'vProgress')
        ui.Label(self.win, layout = (0, 0, 5, 4), icons = ((res.loginLogoImg, ui.ALIGN_W),))
        ui.Title(self.win, layout = (0, 4, 21, 1), id = 'vStatusBar', align = ui.ALIGN_W)
