
import time

import Const

from ige import log
from ige.IObject import public
from IPlayer import IPlayer

class IAIPlayer(IPlayer):

    typeID = Const.T_AIPLAYER

    def init(self, obj):
        IPlayer.init(self, obj)
        #
        obj.name = u'Rebels'
        obj.login = '*'

    def register(self, tran, obj, galaxyID):
        log.debug("Reregistering player", obj.oid)
        counter = 1
        while 1:
            obj.name = u'Rebel faction %d' % counter
            obj.login = '*AIP*rebels%d' % counter
            if galaxyID in tran.gameMngr.accountGalaxies(obj.login):
                counter += 1
                continue
            tran.gameMngr.registerPlayer(obj.login, obj, obj.oid)
            log.debug("Player registered")
            tran.db[Const.OID_UNIVERSE].players.append(obj.oid)
            tran.gameMngr.clientMngr.createAIAccount(obj.login, obj.name, 'ais_rebel')
            break
        # grant techs and so on
        self.cmd(obj).update(tran, obj)

    @public(Const.AL_ADMIN)
    def processINITPhase(self, tran, obj, data):
        IPlayer.processINITPhase(self, tran, obj, data)
        obj.lastLogin = time.time()
        # delete itself if there are no fleets and planets
        if not obj.fleets and not obj.planets:
            self.cmd(obj).delete(tran, obj)
