
from ige import log
from ai import AI

class EDEN(AI):
    """ old empire is sleeping, regaining strength """
    def run(self):
        return


def run(aclient):
    ai = EDEN(aclient)
    ai.run()
    aclient.saveDB()

