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

import ige
import os.path, log, os, sys, time, types, binascii, bz2
import pickle as pickle
import sqlite3

IDX_PREV = 0
IDX_NEXT = 1

class Database:

    dbSchema = "data(oid integer primary key asc, data blog not null)"
    keyMethod = int

    def __init__(self, directory, dbName, cache = 128):
        log.message("Opening database", dbName)
        self.dbName = dbName
        self.nextID = 10000
        self.cacheSize = cache
        #
        try:
            os.makedirs(directory)
        except OSError:
            pass
        # open db
        self.connection = sqlite3.connect(os.path.join(directory, "%s.sqlite" % dbName))
        # allow 8-bits strings to be handled correctly (default is unicode)
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        self.cursor.execute("create table if not exists %s" % self.dbSchema)
        self.connection.commit()
        # cache
        self.cache = {}
        self.cacheLinks = {
            "__first__": [None, "__last__"],
            "__last__": ["__first__", None],
        }
        # stats
        self.statCount = 0
        self.statHit = 0
        self.statSwap = 0
        self.statMiss = 0
        self.statCleanSwap = 0

    def _moveExistingCacheItem(self, key):
        #@log.debug("Cache MOVE ITEM", key, self.cacheLinks[key])
        # optimalization
        cl = self.cacheLinks
        # move item to the end of the chain
        prev, next = cl[key]
        cl[prev][IDX_NEXT] = next
        cl[next][IDX_PREV] = prev
        last = cl["__last__"]
        prev = last[IDX_PREV]
        cl[key] = [prev, "__last__"]
        cl[prev][IDX_NEXT] = key
        last[IDX_PREV] = key
        # print chain
        #idx = "__first__"
        #result = []
        #while idx != None:
        #    item = self.cacheLinks[idx]
        #    result.append("%s:%s" % (idx, item))
        #    idx = item[IDX_NEXT]
        #log.debug("Cache CHAIN", " ".join(result))

    def _addNewCacheItem(self, key):
        #@log.debug("Cache ADD ITEM", key)
        # check cache size
        #@log.debug("Cache size", len(self.cache), self.cacheSize)
        if len(self.cache) > self.cacheSize:
            tries = len(self.cache)
            while len(self.cache) > self.cacheSize:
                # swap out oldest item
                current = self.cacheLinks["__first__"]
                oldKey = current[IDX_NEXT]
                tries -= 1
                if tries == 0:
                    # no room in the cache -> enlarge it
                    log.debug("NO ROOM IN THE CACHE", self.dbName, len(self.cache))
                    self.cacheSize += 100
                    break
                if sys.getrefcount(self.cache[oldKey]) > 2:
                    #@log.debug("CANNOT swap out", oldKey, "refs", sys.getrefcount(self.cache[oldKey]) - 2)
                    # try next element
                    self._moveExistingCacheItem(oldKey)
                    #@log.debug("Trying to swap out", current[IDX_NEXT])
                    continue
                else:
                    #@log.debug("Swapping out", oldKey)
                    self.statSwap += 1
                    #TODOif not self.cache[oldKey]._v_modified:
                    #TODO    self.statCleanSwap += 1
                    prev, next = self.cacheLinks[oldKey]
                    current[IDX_NEXT] = next
                    self.cacheLinks[next][IDX_PREV] = prev
                    self.put(oldKey, pickle.dumps(self.cache[oldKey], pickle.HIGHEST_PROTOCOL))
                    del self.cacheLinks[oldKey]
                    del self.cache[oldKey]
                    # found space
                    break
        # put item at the end of the chain
        last = self.cacheLinks["__last__"]
        prev = last[IDX_PREV]
        self.cacheLinks[prev][IDX_NEXT] = key
        self.cacheLinks[key] = [prev, "__last__"]
        last[IDX_PREV] = key
        # print chain
        #idx = "__first__"
        #result = []
        #while idx != None:
        #    item = self.cacheLinks[idx]
        #    result.append("%s:%s" % (idx, item))
        #    idx = item[IDX_NEXT]
        #log.debug("Cache CHAIN", " ".join(result))

    def _updateCacheItem(self, key):
        if key in self.cache:
            return self._moveExistingCacheItem(key)
        return self._addNewCacheItem(key)

    def _delCacheItem(self, key):
        #@log.debug("Cache DEL ITEM", key)
        prev, next = self.cacheLinks[key]
        self.cacheLinks[prev][IDX_NEXT] = next
        self.cacheLinks[next][IDX_PREV] = prev
        del self.cacheLinks[key]

    def __getitem__(self, key):
        key = self.keyMethod(key)
        self.statCount += 1
        if key in self.cache:
            self.statHit += 1
            self._moveExistingCacheItem(key)
            return self.cache[key]
        self.statMiss += 1
        self.cursor.execute("select * from data where oid = ?", (key,))
        row = self.cursor.fetchone()
        if row is None:
            raise ige.NoSuchObjectException(key)
        item = pickle.loads(str(row[1]))
        self._addNewCacheItem(key)
        self.cache[key] = item
        #TODOitem.setModified(0)
        return item

    def __setitem__(self, key, value):
        key = self.keyMethod(key)
        if type(value) == InstanceType:
            value.oid = key
        # set value
        self._updateCacheItem(key)
        self.cache[key] = value
        #value.setModified(0)
        # write through new objects
        if not self.has_key(key):
            raise ige.ServerException("'%s' created using set method" % key)

    def __contains__(self, key):
        return self.has_key(key)

    def __delitem__(self, key):
        key = self.keyMethod(key)
        if key in self.cache:
            self._delCacheItem(key)
            del self.cache[key]
        self.cursor.execute("delete from data where oid = ?", (key,))

    def has_key(self, key):
        key = self.keyMethod(key)
        self.cursor.execute("select oid from data where oid = ?", (key,))
        return self.cursor.fetchone() is not None


    def keys(self):
        self.cursor.execute("select oid from data")
        return [row[0] for row in self.cursor]

    def getItemLength(self, key):
        key = self.keyMethod(key)
        self.cursor.execute("select * from data where oid = ?", (key,))
        row = self.cursor.fetchone()
        if row is None:
            raise ige.NoSuchObjectException(key)
        return len(str(row[1]))

    def checkpoint(self):
        log.debug('DB Checkpoint', self.dbName)
        log.debug("Storing all objects")
        for key, value in self.cache.iteritems():
            self.put(key, pickle.dumps(value, pickle.HIGHEST_PROTOCOL))
        # commit transaction
        log.debug("Commiting transaction")
        self.connection.commit()
        log.debug("Commit completed")
        # TODO clear cache?
        # self.cache.clear()
        # self.cacheLinks.clear()
        # stats TODO: reenable
        self.cursor.execute("select * from data")
        items = 0
        for i in self.cursor:
            items += 1
        if self.statCount > 0:
            log.debug("****** %s" % self.dbName)
            log.debug("Items: %10d" % items)
            log.debug("Count: %10d" % self.statCount)
            log.debug("Hit  : %10d [%02d %%]" % (self.statHit, int(self.statHit * 100 / self.statCount)))
            log.debug("Miss : %10d [%02d %%]" % (self.statMiss, int(self.statMiss * 100 / self.statCount)))
            log.debug("Swap : %10d [%02d %%]" % (self.statSwap, int(self.statSwap * 100 / self.statCount)))
            log.debug("CSwap: %10d [%02d %%]" % (self.statCleanSwap, int(self.statCleanSwap * 100 / self.statCount)))
            log.debug("******")
        # more stats
        self.statCount = 0
        self.statHit = 0
        self.statMiss = 0
        self.statSwap = 0
        self.statCleanSwap = 0

    def commit(self):
        pass
        #log.debug("COMMIT?")
        #self.txn.commit()
        #self.txn = dbEnv.txn_begin()

    def checkpointDatabase(self):
        # checkpoint db (TODO can be moved into the separate process?)
        log.debug("Metakit Checkpoint")

    def shutdown(self):
        log.message('DB Shutting down', self.dbName)
        self.checkpoint()
        del self.connection

    def clear(self):
        log.message("Deleting database", self.dbName)
        self.cursor.execute("delete from data")
        self.connection.commit()
        self.cache.clear()
        self.cacheLinks = {
            "__first__": [None, "__last__"],
            "__last__": ["__first__", None],
        }
        log.debug("Database is empty")

    def create(self, object, id = None):
        #@log.debug("Creating new object", id)
        if not id:
            id = self.nextID
            while self.has_key(id):
                id += 1
            self.nextID = id + 1
            id = self.keyMethod(id)
            object.oid = id
        elif hasattr(object, "oid") and object.oid != id:
            id = self.keyMethod(id)
            log.message("Object OID '%s' != forced OID '%s' - FIXING" % (object.oid, id))
            object.oid = id
        else:
            id = self.keyMethod(id)
        #@log.debug("OID =", id)
        if self.has_key(id):
            raise ige.ServerException("'%s' created twice" % id)
        self.cache[id] = object
        self._addNewCacheItem(id)
        self.put(id, pickle.dumps(object, pickle.HIGHEST_PROTOCOL))
        return id

    def delete(self, key):
        del self[key]

    def get(self, key, default = None):
        if self.has_key(key):
            return self[key]
        else:
            return default

    def put(self, key, data):
        self.cursor.execute("select oid from data where oid = ?", (key,))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("update data set data = ? where oid = ?", (sqlite3.Binary(data), key))
        else:
            self.cursor.execute("insert into data (oid, data) values (?, ?)", (key, sqlite3.Binary(data)))
        #per put commits impacts performance significantly
        #self.connection.commit()

    def restore(self, filename):
        log.message("Restoring database from file", filename)
        fh = file(filename, "r")
        line = fh.readline().strip()
        if line != "IGE OUTER SPACE BACKUP VERSION 1":
            raise ige.ServerException("Incorrect header: %s" % line)
        while True:
            key = fh.readline().strip()
            if key == "END OF BACKUP":
                break
            data = fh.readline().strip()
            key = int(binascii.a2b_hex(key))
            data = binascii.a2b_hex(data)
            #@log.debug("Storing key", key)
            self.put(key, data)
        log.message("Database restored")

    def backup(self, basename):
        self.checkpoint()
        filename = "%s-%s.osbackup" % (basename, self.dbName)
        log.message("Creating backup", filename)
        fh = file(filename, "w") #bz2.BZ2File(filename, "w")
        fh.write("IGE OUTER SPACE BACKUP VERSION 1\n")
        for key in self.keys():
            fh.write(binascii.b2a_hex(str(key)))
            fh.write("\n")
            fh.write(binascii.b2a_hex(pickle.dumps(self[key], pickle.HIGHEST_PROTOCOL)))
            fh.write("\n")
        fh.write("END OF BACKUP\n")
        fh.close()
        log.message("Backup completed")

class DatabaseString(Database):

    dbSchema = "data(oid text primary key asc, data blog not null)"
    keyMethod = str

    def restore(self, filename, include = None):
        log.message("Restoring database from file", filename)
        fh = file(filename, "r")
        line = fh.readline().strip()
        if line != "IGE OUTER SPACE BACKUP VERSION 1":
            raise ige.ServerException("Incorrect header: %s" % line)
        imported = 0
        skipped = 0
        while True:
            key = fh.readline().strip()
            if key == "END OF BACKUP":
                break
            data = fh.readline().strip()
            key = binascii.a2b_hex(key)
            if include and not include(key):
                skipped += 1
                continue
            imported += 1
            data = binascii.a2b_hex(data)
            #@log.debug("Storing key", key)
            self.put(key, data)
        log.message("Database restored (%d imported, %d skipped)" % (imported, skipped))

