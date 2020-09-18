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

"""
Member variables naming convention:
    _  non watched variable (not changing visual representation of widget)
    *  'watched' variable (change of this variable will force widget update)
"""

import pygame

from . import Const

class DataHolder:
    pass

class Widget:
    def __init__(self, parent, **kwargs):
        # set attributes
        # bypass change detection
        setattr(self,'_changeReported', 0)
        setattr(self,'parent', parent)
        setattr(self,'metaType', Const.TYPE_WIDGET)
        setattr(self,'app', parent.getApp())
        setattr(self,'theme', self.app.theme)
        setattr(self,'foreground', None)
        setattr(self,'background', None)
        setattr(self,'style', None)
        setattr(self,'font', None)
        setattr(self,'align', Const.ALIGN_NONE)
        setattr(self,'tooltip', None)
        setattr(self,'tooltipTitle', None)
        setattr(self,'statustip', None)
        setattr(self,'visible', 0)
        setattr(self,'enabled', 1)
        setattr(self,'focused', 0)
        setattr(self,'mouseOver', 0)
        setattr(self,'focusable', 1)
        setattr(self,'dragSource', 0)
        setattr(self,'dragTarget', 0)
        setattr(self,'layout', None)
        setattr(self,'tags', [])
        setattr(self,'id', None)
        setattr(self,'orderNo', 0)
        setattr(self,'rect', pygame.Rect((0, 0, 0, 0)))
        setattr(self,'_handleMap', {'*': []})
        setattr(self,'data', DataHolder())
        # notify parent
        self.visible = 1
        self.processKWArguments(kwargs)

    def processKWArguments(self, kwargs):
        # process keyword arguments
        for key in kwargs:
            if hasattr(self, key):
                setattr(self,key, kwargs[key])
            else:
                raise AttributeError(key)

    def subscribeAction(self, actionName, handler):
        handleList = self._handleMap.get(actionName, [])
        handleList.append(handler)
        self._handleMap[actionName] = handleList

    def processAction(self, actionName, data = None, widget = None):
        if not actionName: return
        if not widget: widget = self
        handlers = self._handleMap.get(actionName, self._handleMap['*'])
        if handlers:
            for handler in handlers:
                if type(handler) == InstanceType:
                    handler = getattr(handler, actionName)
                handler(widget, actionName, data)
        else:
            self.parent.processAction(actionName, data, widget)

    def draw(self, surface):
        raise NotImplementedError('%s.draw' % self.__class__)

    def getSize(self):
        raise NotImplementedError

    def onFocusLost(self):
        self.focused = 0

    def onFocusGained(self):
        self.focused = 1

    def onMouseOut(self):
        self.mouseOver = 0

    def onMouseOver(self):
        self.mouseOver = 1

    def onCursorChanged(self):
        return

    def processMB1Down(self, evt):
        return Const.NoEvent

    def processMB1Up(self, evt):
        return Const.NoEvent

    def processMB1UpMissed(self, evt):
        return Const.NoEvent

    def processMB2Down(self, evt):
        return Const.NoEvent

    def processMB2Up(self, evt):
        return Const.NoEvent

    def processMB2UpMissed(self, evt):
        return Const.NoEvent

    def processMB3Down(self, evt):
        return Const.NoEvent

    def processMB3Up(self, evt):
        return Const.NoEvent

    def processMB3UpMissed(self, evt):
        return Const.NoEvent

    def processMWUp(self, evt):
        return Const.NoEvent

    def processMWDown(self, evt):
        return Const.NoEvent

    def processMMotion(self, evt):
        return Const.NoEvent

    def processKeyDown(self, evt):
        return evt

    def processKeyUp(self, evt):
        return evt

    def getApp(self):
        return self.parent.getApp()

    def redraw(self):
        self.parent.redraw(self)
        setattr(self,'_changeReported', 1)

    def __setattr__(self, name, value):
        #@name = intern(name)
        dict = self.__dict__
        if value == dict.get(name, Const.NoValue):
            return
        dict[name] = value
        if name == 'visible' and self.parent:
            self.parent.redraw(self, 1)
            dict['_changeReported'] = 1
            #@print 'set', self, name , value
        elif not self._changeReported and name[0] != '_' and self.parent:
            self.parent.redraw(self)
            dict['_changeReported'] = 1
            #@print 'set', self, name , value

    def set(self, **kwargs):
        self.processKWArguments(kwargs)

##
## All elements are registered here
##

widgets = {}

def registerWidget(widget, name):
    widgets[name] = widget
