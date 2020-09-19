

import pygameui as ui

class ConsoleDlg:

    def __init__(self, app):
        self.app = app
        self.createUI()

    def display(self):
        self.win.show()

    def hide(self):
        self.win.hide()

    def createUI(self):
        self.win = ui.Window(self.app,
            modal = 1,
            rect = ui.Rect(0, 20, 400, 600),
            layoutManager = ui.SimpleGridLM(),
        )
