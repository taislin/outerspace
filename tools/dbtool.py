#!/usr/bin/env python2


# tweak PYTHONPATH
import os
import sys
from optparse import OptionParser

# setup system path
baseDir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(baseDir, '..', 'server', 'lib'))
sys.path.insert(0, os.path.join(baseDir, '..', 'client-ai'))

import ige
from ige import log
import ige.ospace.Const as Const
from ige.SQLiteDatabase import Database, DatabaseString

# parse command line arguments
parser = OptionParser(usage = "usage: %prog [options]")
parser.add_option("",  "--configdir", dest = "configDir",
    metavar = "DIRECTORY", default = os.path.join(os.path.expanduser("~"), ".outerspace"),
    help = "Override default configuration directory",)
options, args = parser.parse_args()

gameName = 'Alpha'

gameDB = Database(os.path.join(options.configDir,"db_data"), "game_%s" % gameName, cache = 15000)
clientDB = DatabaseString(os.path.join(options.configDir,"db_data"), "accounts", cache = 100)
msgDB = DatabaseString(os.path.join(options.configDir,"db_data"), "messages", cache = 1000)
bookingDB = DatabaseString(os.path.join(options.configDir,"db_data"), "bookings", cache = 100)

# insert code


# 

for db in gameDB, clientDB, msgDB, bookingDB:
    db.shutdown()

