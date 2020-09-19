

import log

## common exceptions
class SecurityException(Exception):
    pass

class GameException(Exception):
    pass

class CreatePlayerException(Exception):
    pass

class NoAccountException(Exception):
    pass

class ServerException(Exception):
    pass

class ServerStatusException(Exception):
    pass

class NoSuchObjectException(Exception):
    pass

class BookingMngrException(Exception):
    pass

## global settings
# runtime mode, currently supported:
#   1 - normal operations
#   0 - debug/devel operations
igeRuntimeMode = 1

def setRuntimeMode(runtimeMode):
    global igeRuntimeMode

    igeRuntimeMode = runtimeMode
    log.message("Runtime mode changed to", igeRuntimeMode)
