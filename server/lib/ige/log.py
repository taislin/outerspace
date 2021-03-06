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

import time
import string
import sys
import traceback, inspect, os.path

__startTime = time.time()

errorLog = None
msgLog = None

LEVEL_DEBUG = 40
LEVEL_MESSAGE = 30
LEVEL_WARNING = 20
LEVEL_ERROR = 10
LEVEL_FATAL = 0

level = LEVEL_DEBUG

__srcfile = os.path.splitext(__file__)
if __srcfile[1] in [".pyc", ".pyo"]:
    __srcfile = __srcfile[0] + ".py"
else:
    __srcfile = __file__

def setErrorLog(filename):
    global errorLog
    ensureDirectoryExists(filename)
    errorLog = open(filename, 'w')

def setMessageLog(filename):
    global msgLog
    ensureDirectoryExists(filename)
    msgLog = open(filename, 'w')

def ensureDirectoryExists(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

def setLevel(aLevel):
    global level
    level = aLevel

def __getTime():
    diff = int(time.time() - __startTime)
    secs = diff % 60
    mins = diff % 3600 / 60
    hours = diff / 3600
    return time.strftime('%Y-%m-%d %H:%M:%S')
    #@return time.strftime('%H:%M:%S')
    #@return '%02d:%02d:%02d [%s]' % (hours, mins, secs, time.strftime('%Y%m%d%H%M%S'))
    #@return '%02d:%02d:%02d' % (hours, mins, secs)

def __getCaller():
    return "-- "
    f = inspect.stack()[2]
    # be smart and try to get oid of object
    frame = f[0]
    name = frame.f_globals['__name__']
    #if len(name) > 15:
    #    name = '..%s' % name[-13:]
    if frame.f_locals.has_key('obj') and hasattr(frame.f_locals['obj'], 'oid'):
        return '%s %d [oid=%s]' % (
            name,
            frame.f_lineno,
            frame.f_locals['obj'].oid
        )
    return '%s %d' % (name, frame.f_lineno)

def debug(*args):
    if level < LEVEL_DEBUG:
        return
    conc = ""
    for item in args:
        conc = conc + str(item) + " "
    print(str(__getTime())+' DBG '+str(__getCaller())+conc)
    
    if msgLog:
        msgLog.flush()

def message(*args):
    if level < LEVEL_MESSAGE:
        return
    conc = ""
    for item in args:
        conc = conc + str(item) + " "
    print(str(__getTime())+' MSG '+str(__getCaller())+conc)
    
    if msgLog:
        msgLog.flush()

def warning(*args):
    if level < LEVEL_WARNING:
        return
    # TODO lock!
    print(str(__getTime())+' WAR '+str(__getCaller()))
    for item in args:
        print(str(item))
    if sys.exc_info() != (None, None, None):
        print(79 * '-')
        traceback.print_exc(file=sys.stdout)
        print(79 * '-')
    if errorLog:
        print(errorLog+str(__getTime())+' WAR '+str(__getCaller()))
        for item in args:
            print >> errorLog, str(item),
        print >> errorLog
        if sys.exc_info() != (None, None, None):
            print >> errorLog, 79 * '-'
            traceback.print_exc(file=errorLog)
            print >> errorLog, 79 * '-'
        errorLog.flush()
    if msgLog:
        print(str(msgLog)+str(__getTime())+' WAR '+str(__getCaller()))
        for item in args:
            print >> msgLog, str(item),
        print >> msgLog
        if sys.exc_info() != (None, None, None):
            print >> msgLog, 79 * '-'
            traceback.print_exc(file=msgLog)
            print >>msgLog, 79 * '-'
        msgLog.flush()

def error(*args):
    print(str(__getTime())+' ERR '+str(__getCaller()))
    for item in args:
        print(str(item))
    
    if sys.exc_info() != (None, None, None):
        print(79 * '-')
        traceback.print_exc(file=sys.stdout)
        print(79 * '-')
    if errorLog:
        print(errorLog+str(__getTime())+' ERR '+str(__getCaller()))
        for item in args:
            print >> errorLog, str(item),
        print >> errorLog
        if sys.exc_info() != (None, None, None):
            print >> errorLog, 79 * '-'
            traceback.print_exc(file=errorLog)
            print >> errorLog, 79 * '-'
        errorLog.flush()
    if msgLog:
        print(str(msgLog)+str(__getTime())+' ERR '+str(__getCaller()))
        for item in args:
            print >> msgLog, str(item),
        print >> msgLog
        if sys.exc_info() != (None, None, None):
            print >> msgLog, 79 * '-'
            traceback.print_exc(file=msgLog)
            print >>msgLog, 79 * '-'
        msgLog.flush()
    sys.exit(1)

def exception(*args):
    if level < LEVEL_WARNING:
        return
    # TODO lock!
    print(str(__getTime())+' EXC '+str(__getCaller()))
    for item in args:
        print(str(item))
    
    if sys.exc_info() != (None, None, None):
        print(79 * '-')
        traceback.print_exc(file=sys.stdout)
        print(79 * '-')
    if errorLog:
        print(errorLog+str(__getTime())+' EXC '+str(__getCaller()))
        for item in args:
            print >> errorLog, str(item),
        print >> errorLog
        if sys.exc_info() != (None, None, None):
            print >> errorLog, 79 * '-'
            traceback.print_exc(file=errorLog)
            print >> errorLog, 79 * '-'
        errorLog.flush()
    if msgLog:
        print(str(msgLog)+str(__getTime())+' EXC '+str(__getCaller()))
        for item in args:
            print >> msgLog, str(item),
        print >> msgLog
        if sys.exc_info() != (None, None, None):
            print >> msgLog, 79 * '-'
            traceback.print_exc(file=msgLog)
            print >>msgLog, 79 * '-'
        msgLog.flush()
