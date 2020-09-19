

import Const

class Transaction:

    def __init__(self, gameMngr, cid = Const.OID_NONE, session = None):
        self.gameMngr = gameMngr
        self.db = gameMngr.db
        self.cid = cid
        self.session = session

    def commit(self):
        self.db.commit()
