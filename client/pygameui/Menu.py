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
import pygame
from . import Const
from Window import Window
from SimpleGridLM import SimpleGridLM
from Title import Title
from ActiveLabel import ActiveLabel
from math import ceil

class Menu(Window):

    def __init__(self, parent, **kwargs):
        Window.__init__(self, parent)
        # data
        setattr(self,"title",None)
        setattr(self,"items",None)
        setattr(self,"looseFocusClose",1)
        setattr(self,"columns",1)
        setattr(self,"decorated",0)
        setattr(self,"layoutManager",SimpleGridLM())
        setattr(self,"width",10)
        setattr(self,"_labels",[])
        self.processKWArguments(kwargs)
        # subscribe action
        # add title
        Title(self, id = "_menuTitle")

    def show(self, pos = None):
        self._menuTitle.layout = (0, 0, self.width, 1)
        self._menuTitle.text = self.title
        if not pos:
            pos = pygame.mouse.get_pos()
        index = 0
        width = int(1.0 * self.width / self.columns)
        perColumn = ceil(1.0 * len(self.items) / self.columns)
        currentLeft = 0
        currentVert = 0
        for item in self.items:
            if not hasattr(item, 'align'):
                item.align = Const.ALIGN_W
            elif not item.align:
                item.align = Const.ALIGN_W
            if len(self._labels) <= index:
                label = ActiveLabel(self, align = item.align, enabled = item.enabled)
                label.subscribeAction("*", self.actionHandler)
                self._labels.append(label)
            label = self._labels[index]
            label.layout = (currentLeft, currentVert + 1, width, 1)
            label.text = item.text
            if hasattr(item, "action"):
                label.action = item.action
            else:
                label.action = None
            if hasattr(item, "data"):
                label.data = item.data
            else:
                label.data = None
            index += 1
            currentVert += 1
            if currentVert == perColumn:
                currentVert = 0
                currentLeft += width
        rowSize, colSize = self.app.theme.getGridParams()
        self.rect = pygame.Rect(pos[0], pos[1], self.width * colSize, (perColumn + 1) * rowSize)
        return Window.show(self)

    def actionHandler(self, widget, action, data):
        self.hide()
        self.processAction(action, widget.data)

    def processKeyUp(self, evt):
        return Const.NoEvent


    def processKeyDown(self, evt):
        for item in self.items:
            if getattr(item,'hotkeymod',False):
                if getattr(item,'hotkey',False) == evt.unicode and pygame.key.get_mods() & getattr(item,'hotkeymod',False):
                    self.hide()
                    self.processAction(item.action, False)
            elif getattr(item,'hotkey',False) == evt.unicode:
                self.hide()
                self.processAction(item.action, False)
        if evt.key == pygame.K_ESCAPE:
            self.hide()
        return Const.NoEvent
