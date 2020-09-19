

from main_ai import runAIClient

def runAIPool(options):
    import copy
    import sys
    import os
    import time
    import tempfile
    import traceback
    import multiprocessing
    import re
    import copy

    from ai_parser import AIList


    games = []
    if options.game:
        games.append(options.game)
    else:
        # support for games autodetect is not implemented
        raise NotImplementedError

    aiPool = multiprocessing.Pool(processes = options.procs)

    results = []
    for gameName in games:
        aiList = AIList(options.configDir)
        for record in aiList.getAll():
            optAI = copy.copy(options)
            optAI.configDir = os.path.join(options.configDir, 'ai_data', gameName)
            optAI.login = record.login
            optAI.password = record.password
            optAI.ai = record.aiType
            optAI.game = gameName
            optAI.test = False
            results.append(aiPool.apply_async(runAIClient, [optAI]))
    aiPool.close()
    for result in results:
        try:
            result.get()
        except Exception as exc:
            # having pass or continue here prevents exception from being printed
            # What the actual hell?
            True
    aiPool.join()
    sys.exit()

