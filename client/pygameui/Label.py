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
from . import Widget

class Label(Widget.Widget):

    def __init__(self, parent, **kwargs):
        Widget.Widget.__init__(self, parent)
        # data
        self.text = None
        self.icons = []
        # flags
        self.processKWArguments(kwargs)
        parent.registerWidget(self)

    def draw(self, surface):
        self.theme.drawLabel(surface, self)
        return self.rect

Widget.registerWidget(Label, 'label')
