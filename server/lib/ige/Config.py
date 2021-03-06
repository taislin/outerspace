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

from configparser import ConfigParser

class Config:
    """Encapsulation of configparser class.

    Attributes of this class represents sections
    of config file. If some want to assing value
    to section, an AttruteError is thrown, except
    None value, which removes section with given
    name. When asking for nonexisting section,
    section with same name is created. For
    existing section an instance of Section class
    is returned.
    """
    def __init__(self, _file, defaults = dict()):
        setattr(self,"_config",ConfigParser(defaults))
        setattr(self,"_file",_file)
        self._config.read(_file)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def sections(self):
        return self._config.sections()

    def save(self, _file = None):
        if _file is None:
            _file = self._file
        with open(_file, 'w') as fh:
            self._config.write(fh)

class Section:
    """Represent section of configparser class.

    Attributes of this class represents options
    of given section. when asking for option
    value None value is returned if given option
    does not exist, otherwise option value is
    returned.
    """
    def __init__(self, config, name):
        setattr(self,"_config",config)
        setattr(self,"section",name)

    def __getattr__(self, name):
        if self._config.has_option(self.section, name):
            return self._config.get(self.section, name)
        else:
            return None

    def __setattr__(self, name, value):
        if value is None:
            self._config.remove_option(self.section, name)
            if not self._config.options(self.section):
                # no option -- delete me
                self._config.remove_section(self.section)
        else:
            self._config.set(self.section, name, str(value))
