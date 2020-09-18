#
#  Copyright 2001 - 2016 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of Pygame.UI.
#
#  Pygame.UI is free software; you can redistribute it and/or modify
#  it under the terms of the Lesser GNU General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
#  Pygame.UI is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  Lesser GNU General Public License for more details.
#
#  You should have received a copy of the Lesser GNU General Public License
#  along with Pygame.UI; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from . import Const
from Widget import Widget, registerWidget

class Button(Widget):

    def __init__(self, parent, **kwargs):
        Widget.__init__(self, parent)
        # data
        setattr(self,'text', None)
        setattr(self,'icons', [])
        # flags
        setattr(self,'toggle', 0)
        setattr(self,'pressed', 0)
        setattr(self,'highlighted', 0)
        setattr(self,'action', None)
        setattr(self,'rmbAction', None)
        setattr(self,'hoverAction', None)
        setattr(self,'_processingMB1', 0)
        setattr(self,'_processingMB3', 0)
        self.processKWArguments(kwargs)
        parent.registerWidget(self)

    def draw(self, surface):
        self.theme.drawButton(surface, self)
        return self.rect

    def processMB1Down(self, evt):
        self.theme.playButtonSound(self)
        self.pressed = not self.pressed
        self._processingMB1 = 1
        return Const.NoEvent

    def processMB1Up(self, evt):
        self._processingMB1 = 0
        if self.pressed and not self.toggle:
            if self.pressed:
                self.theme.playButtonSound(self)
            self.pressed = 0
            self.processAction(self.action)
        elif self.toggle:
            self.processAction(self.action)
        return Const.NoEvent

    def processMB1UpMissed(self, evt):
        self._processingMB1 = 0
        return Widget.processMB1UpMissed(self, evt)

    def onMouseOut(self):
        if (self.pressed or self.toggle) and self._processingMB1:
            self.theme.playButtonSound(self)
            self.pressed = not self.pressed
        else:
            self.highlighted = 0
            self.processAction(self.hoverAction, self.highlighted)
        return Widget.onMouseOut(self)

    def onMouseOver(self):
        if self._processingMB1:
            self.theme.playButtonSound(self)
            self.pressed = not self.pressed
        else:
            self.highlighted = 1
            self.processAction(self.hoverAction, self.highlighted)
        return Widget.onMouseOver(self)

    def onFocusLost(self):
        self._processingMB1 = 0
        self._processingMB3 = 0
        return Widget.onFocusLost(self)

    def processMB3Down(self, evt):
        self._processingMB3 = 1
        if self.rmbAction and not self.toggle:
            self.pressed = not self.pressed
        return Const.NoEvent

    def processMB3Up(self, evt):
        if self._processingMB3:
            self.processAction(self.rmbAction)
        if self.rmbAction and self.pressed and not self.toggle:
            if self.pressed:
                self.theme.playButtonSound(self)
            self.pressed = 0
        self._processingMB3 = 0
        return Const.NoEvent


registerWidget(Button, 'button')
