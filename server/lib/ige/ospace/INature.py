
import time

import Const

from ige import log
from ige.IDataHolder import IDataHolder
from ige.IObject import public
from IPlayer import IPlayer

class INature(IPlayer):

    typeID = Const.T_NATURE

    def init(self, obj):
        IPlayer.init(self, obj)
        #
        obj.name = u'NATURE'
        obj.login = '*NATURE*'

    @public(Const.AL_ADMIN)
    def processINITPhase(self, tran, obj, data):
        IPlayer.processINITPhase(self, tran, obj, data)
        obj.lastLogin = time.time()

    @public(Const.AL_ADMIN)
    def processPRODPhase(self, tran, obj, data):
        return None

    @public(Const.AL_ADMIN)
    def processBATTLEPhase(self, tran, obj, data):
        return None

    def getDiplomacyWith(self, tran, obj, playerID):
        # this AI battles with overyone
        # make default
        dipl = IDataHolder()
        dipl.type = Const.T_DIPLREL
        dipl.pacts = {}
        if obj.oid == playerID:
            dipl.relation = Const.REL_UNITY
        else:
            dipl.relation = Const.REL_ENEMY
        dipl.relChng = 0
        dipl.lastContact = tran.db[Const.OID_UNIVERSE].turn
        dipl.contactType = Const.CONTACT_NONE
        dipl.stats = None
        return dipl

    def isPactActive(self, tran, obj, partnerID, pactID):
        return 0
