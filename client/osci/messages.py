

#
# This module contains messages
#
import ige.ospace.Const as Const
from ige import NoSuchObjectException
import client, types, string, res, gdata
from ige import log
from ige.ospace import Rules

#
# Transform routines
#
def techID2Name(techID):
    if techID >= 1000:
        return _(client.getTechInfo(techID).name.encode())
    else:
        return client.getPlayer().shipDesigns[techID].name

def objID2Name(objID):
    obj = client.get(objID, noUpdate = 0, publicOnly = 1)
    return getattr(obj, 'name', res.getUnknownName())

def objIDList2Names(objIDs):
    names = []
    for objID in objIDs:
        obj = client.get(objID, noUpdate = 1, publicOnly = 1)
        if hasattr(obj, 'owner') and obj.owner != obj.oid:
            try:
                owner = _(' (%s)') % client.get(obj.owner, noUpdate = 1, publicOnly = 1).name
            except AttributeError:
                owner = ''
        else:
            owner = ''
        text = _('%s%s') % (getattr(obj, 'name', res.getUnknownName()), owner)
        names.append(text)
    return string.join(names, ', ')

def minesReport((damageCaused, killsCaused, minesTriggered)):
    lines = []
    techs = minesTriggered.keys()
    for techID in techs:
        techName = client.getTechInfo(techID).name.encode()
        text = _('%d of the %s detonated, causing %d damage, killing %d ships in the process.') %\
                    (minesTriggered[techID],
                    techName,
                    damageCaused.get(techID, 0),
                    killsCaused.get(techID, 0))
        lines.append(text)
    return '\n'.join(lines)

def delayTurns(startTurn):
    return res.formatTime(startTurn + Rules.galaxyStartDelay)

def stratID2Name(resID):
    return _(gdata.stratRes[resID])

def float2percent(number):
    return int(number * 100)

def plType2Name(plType):
    return gdata.planetTypes[plType]

def designID2Name(designID):
    return client.getPlayer().shipDesigns[designID].name

def queueID2Name(queueID):
    return res.globalQueueName(queueID)

def votes2Txt((votes, voters)):
    lines = []
    nominated = sorted(votes, key=lambda a: votes[a], reverse = True)
    for playerName in nominated:
        if playerName == None:
            continue
        l = []
        for name in voters[playerName]:
            l.append(name)
        text = "   %s got %d votes from %s." % (
            playerName,
            votes[playerName],
            ", ".join(l),
        )
        lines.append(text)
    if None in votes:
        l = []
        for name in voters[None]:
            l.append(name)
        text = "   %s abstained [%d votes]." % (
            ", ".join(l),
            votes[None],
        )
        lines.append(text)
    return "\n".join(lines)

def impMsg(msg):
    return "\n".join(msg)

def listing(names):
    if len(names) == 1:
        return names[0]
    conj = _(" and ")
    text = conj.join([", ".join(names[:-1]), names[-1]])
    return text
#
# Data
#

# severity codes
CRI = 3
MAJ = 2
MIN = 1
INFO = 0
NONE = INFO

# i18n (delayed translation)
def N_(msg): return msg

msgData = {}

def addMsg(msgID, name, transform = None, severity = NONE):
    global msgData
    msgData[msgID] = (name, transform, severity)

addMsg(Const.MSG_COMPLETED_RESEARCH, N_('Research completed: %(1)s'), (techID2Name,), CRI)
addMsg(Const.MSG_WASTED_SCIPTS, N_('%(1)d research points not used.'), severity = MIN)
addMsg(Const.MSG_CANNOTBUILD_SHLOST, N_('Cannot build on planet - ship may be lost.'), severity = CRI)
addMsg(Const.MSG_CANNOTBUILD_NOSLOT, N_('Cannot build on planet - no free slot.'), severity = CRI)
# NOT NEEDED addMsg(MSG_DESTROYED_BUILDING, N_('Structure destroyed: %(1)s'), (techID2Name,), MAJ)
addMsg(Const.MSG_WASTED_PRODPTS, N_('Construction problem: no task\n\n%(1)d construction points were not used because there was no task to fulfill.'), (int,), severity = INFO)
addMsg(Const.MSG_LOST_PLANET, N_('Planet lost.'), severity = CRI)
addMsg(Const.MSG_COMPLETED_STRUCTURE, N_('Structure completed: %(1)s'), (techID2Name,), MIN)
addMsg(Const.MSG_DEPLOY_HANDLER, N_('A deployment of %(1)s was completed'), (techID2Name,), MIN)
addMsg(Const.MSG_COMPLETED_SHIP, N_('Ship completed: %(1)s'), (techID2Name,), MIN)
addMsg(Const.MSG_GAINED_PLANET, N_('New planet.'), severity = CRI)
addMsg(Const.MSG_COMBAT_RESULTS, N_('Combat with: %(4)s. HP lost: we %(1)d, they %(2)d.\n\nEnemy lost %(2)d HP, we lost %(1)d HP and %(3)d ships/structures. We attacked/were attacked by %(4)s.'), (int, int, int, objIDList2Names), MAJ)
addMsg(Const.MSG_COMBAT_LOST, N_('Battle lost: we were defeated by %(1)s.'), (objID2Name,), CRI)
addMsg(Const.MSG_DESTROYED_FLEET, N_('Fleet destroyed.'), severity = CRI)
addMsg(Const.MSG_COMBAT_WON, N_('Battle won: we defeated %(1)s.'), (objID2Name,), CRI)
addMsg(Const.MSG_NEW_GOVCENTER, N_('A new government center established.'), severity = CRI)
addMsg(Const.MSG_REVOLT_STARTED, N_('Planet revolt started - production halved for the next turns.'), severity = CRI)
addMsg(Const.MSG_REVOLT_ENDED, N_('Planet revolt ended - production restored.'), severity = CRI)
addMsg(Const.MSG_INVALID_TASK, N_('Construction of %(1)s is not valid - construction suspended.'), (techID2Name,), severity = CRI)
addMsg(Const.MSG_NOSUPPORT_POP, N_('Population decreased.\n\nPopulation of this planet has decreased. Build more facilities producing food.'), severity = CRI)
addMsg(Const.MSG_COMPLETED_PROJECT, N_('Project finished: %(1)s'), (techID2Name,), MIN)
addMsg(Const.MSG_ENABLED_TIME, N_('Time in galaxy started to run...'), severity = CRI)
addMsg(Const.MSG_DISABLED_TIME, N_('Time in galaxy stopped...'), severity = CRI)
addMsg(Const.MSG_MISSING_STRATRES, N_('Strategic resource missing: %(1)s'), (stratID2Name,), MAJ)
addMsg(Const.MSG_DELETED_RESEARCH, N_('Research task deleted: %(1)s'), (techID2Name,), CRI)
addMsg(Const.MSG_EXTRACTED_STRATRES, N_('Strategic resource extracted: %(1)s'), (stratID2Name,), MIN)
addMsg(Const.MSG_EXTRACTED_ANTIMATTER_SYNTH, N_('Strategic resource synthesized: 4 units of %(1)s'), (stratID2Name,), MIN)
addMsg(Const.MSG_DOWNGRADED_PLANET_ECO, N_('Planet downgraded to: %(1)s'), (plType2Name,), CRI)
addMsg(Const.MSG_UPGRADED_PLANET_ECO, N_('Planet upgraded to: %(1)s'), (plType2Name,), CRI)
addMsg(Const.MSG_UPGRADED_SHIP, N_('Ship upgraded from %(1)s to %(2)s'), (unicode,unicode), MIN)
addMsg(Const.MSG_DELETED_DESIGN, N_('Obsolete ship design deleted: %(1)s'), (unicode,), CRI)
addMsg(Const.MSG_CANNOT_UPGRADE_SR, N_('Cannot upgrade ship from %(1)s to %(2)s\n\nCannot upgrade ship from %(1)s to %(2)s because of we have not enough of %(3)s.'), (unicode,unicode,stratID2Name), MAJ)
addMsg(Const.MSG_DAMAGE_BY_SG, N_('Malfunctional Star Gate, lost %(1)d %% HP\n\nOur fleet has arrived at system with no or malfunctional Star Gate or Comm/Scann Center. Every ship lost %(1)d %% hitpoints due to intensive deceleration.'), (int,), MAJ)
addMsg(Const.MSG_GAINED_FAME, N_('Gained %(1)d fame.'), severity = INFO)
addMsg(Const.MSG_LOST_FAME, N_('Lost %(1)d fame.'), severity = CRI)
addMsg(Const.MSG_GAINED_TECH, N_('Gained %(1)s technology at sublevel %(2)d.'), (techID2Name, int), severity = INFO)
addMsg(Const.MSG_ENTERED_WORMHOLE, N_('Your fleet entered a wormhole at %(1)s and exited at %(2)s.'), (unicode,unicode), severity = MIN)
addMsg(Const.MSG_NOT_ENTERED_WORMHOLE, N_('Cannot enter wormhole - ship may be lost.'), severity = MIN)
addMsg(Const.MSG_FOUND_WORMHOLE, N_('You have located a wormhole'), severity = MIN) #todo
addMsg(Const.MSG_FUEL_LOST_ORBITING, N_('Fleet lost.\n\n We lost contact with the %(1)s after they ran out of fuel in the system %(2)s.'), (unicode, objID2Name), severity = MAJ)
addMsg(Const.MSG_FUEL_LOST_FLYING, N_('Fleet lost.\n\n We lost contact with the %(1)s after they ran out of fuel en route to the system %(2)s.'), (unicode, objID2Name), severity = MAJ)
addMsg(Const.MSG_QUEUE_TASK_ALLOTED, N_('Task alloted.\n\nGlobal queue \"%(1)s\" alloted %(2)s.'), (queueID2Name, techID2Name), severity = MAJ)
addMsg(Const.MSG_MINES_OWNER_RESULTS, N_('Our minefield triggered: HP / ships destroyed: %(3)s / %(4)s.\n\nForces of %(1)s triggered our minefield. Report:\n\n%(2)s'), (objIDList2Names,minesReport,int,int), severity = MAJ)
addMsg(Const.MSG_MINES_FLEET_RESULTS, N_('Hostile minefield triggered: HP / ships lost: %(1)s / %(2)s.\n\nOur fleet triggered enemy minefield, losing %(1)s HP resulting in destruction of %(2)s ships.'), (int,int), severity = MAJ)

# GNC
addMsg(Const.MSG_GNC_EMR_FORECAST, N_("EMR Forecast\n\nLevel of the electromagnetic radiation is believed to be about %(1)d %% of the average level for the next %(2)s turns"), (float2percent, res.formatTime), severity = MIN)
addMsg(Const.MSG_GNC_EMR_CURRENT_LVL, N_("EMR Forecast\n\nCurrent level of the electromagnetic radiation is about %(1)d %% of the average level."), (float2percent,), severity = MIN)
addMsg(Const.MSG_GNC_VOTING_COMING, N_("Elections!\n\nIt's %(1)s turns before elections! Don't hesitate and vote for the best commander!"), (res.formatTime,), severity = MAJ)
addMsg(Const.MSG_GNC_VOTING_NOWINNER, N_("Election results! Nobody won...\n\nThe results from the last elections have been published. Nobody was strong enough to be elected as a leader of our galaxy. Can we find such person another day?\n\nThe official election results follow:\n\n%(1)s\n\n"), (votes2Txt,), severity = MAJ)
addMsg(Const.MSG_GNC_VOTING_LEADER, N_("Election results! Leader elected!\n\nThe results from the last elections have been published. %(1)s has proved to be the most supported person and has been elected as our Leader. May be, %(1)s can become an Imperator one day.\n\nThe official election results follow:\n\n%(2)s\n\n"), (unicode, votes2Txt,), severity = MAJ)
addMsg(Const.MSG_GNC_VOTING_IMPERATOR, N_("Election results! Imperator elected!\n\nThe results from the last elections have been published. %(1)s has proved to be the most supported person and has been elected as our glorified Imperator. Congratulations - you proved to be the best of all of us!\n\nThe official election results follow:\n\n%(2)s\n\n"), (unicode, votes2Txt,), severity = MAJ)

addMsg(Const.MSG_GNC_GALAXY_FINISHED, N_("Galaxy %(2)s knows its winner - Imperator %(1)s\n\nToday the galaxy %(2)s has been united and the peace has been restored. Majority of commanders voted for Imperator %(1)s as their supreme leader. Congratulations, Imperator, you were brave and wise!\n\nMessage from imperator:\n%(3)s"), (unicode, unicode, impMsg), severity = MAJ)
addMsg(Const.MSG_GNC_GALAXY_GENERATOR, N_("Galaxy %(1)s generation is completed. Galaxy specifications:\n\n%(2)s"), (unicode, votes2Txt,), severity = INFO)
addMsg(Const.MSG_GNC_GALAXY_AUTO_FINISHED, N_("Galaxy %(1)s has ended\n\nToday the galaxy %(1)s has been automatically ended.\n\nReason:\n%(2)s"), (unicode, impMsg), severity = MAJ)
addMsg(Const.MSG_GNC_GALAXY_BRAWL_WON, N_("Galaxy %(1)s has ended\n\nAll hail to the conqueror! Galaxy %(1)s is finally on the brink of peace. After years of conquest, all opposition has been decimated and Sovereign %(2)s stands as the sole usurper of the galaxy."), (unicode, unicode), severity = MAJ)
addMsg(Const.MSG_GNC_GALAXY_COOP_WON, N_("Galaxy %(1)s has ended\n\nAll citizens of galaxy %(1)s rejoice. Peace is finally here!. After years of fending of attacks of barbaric empires, stalwart defence by %(2)s prevailed, and ensured further generations can live in prosperity."), (unicode, listing), severity = MAJ)
addMsg(Const.MSG_GNC_GALAXY_CREATED, N_("Boom of galactic civilizations is here\n\nDark ages are past, and new empires are reaching galactic age at breakneck speed and with fervor never seen before. True space race is predicted to start on %(1)s of universal time."), (delayTurns,), severity = MAJ)

# i18n
del N_

#
# Interface
#

def getMsgText(msgID, data):
    msg, transform, severity = msgData.get(msgID, (None, None, None))
    # create default messages
    if not msg:
        return _('ERROR\nMissing text for msg %d: %s') % (msgID, repr(data))
    # there is message text -> create message
    # force unicode
    msg = _(msg)
    if data == None:
        return msg
    try:
        # tranform data
        newData = {}
        if not (type(data) == types.ListType or type(data) == types.TupleType):
            data = (data,)
        if transform:
            index = 1
            for tranFunc in transform:
                newData[str(index)] = tranFunc(data[index - 1])
                index += 1
        else:
            index = 1
            for item in data:
                newData[str(index)] = item
                index += 1
        text = msg % newData
    except Exception, e:
        # wrong arguments -> default message
        log.warning("Error while formating message")
        return _('ERROR\nWrong format for msg %d: %s\nException: %s: %s\nFormat: %s') % (msgID, repr(data), str(e.__class__), str(e), msg)
    return text

def getMsgSeverity(msgID):
    return msgData.get(msgID, (None, None, NONE))[2]

def getFullMessageText(message):
    """Gets full text of automaticaly generated message

    If message has no data to generate, it returns empty
    string.
    """
    text = ""
    if message.has_key("data"):
        sourceID, msgID, locationID, turn, data = message["data"]
        sev = getMsgSeverity(msgID)
        currTurn = client.getTurn()
        player = client.getPlayer()
        # source
        if sourceID != Const.OID_NONE and sourceID != player.oid:
            obj = client.get(sourceID, noUpdate = 1, publicOnly = 1)
            if obj:
                if hasattr(obj,'customname') and obj.customname:
                        source = _('"%s"') % obj.customname
                else:
                        source = getattr(obj, 'name', res.getUnknownName())
            else:
                source = _('N/A')
        else:
            source = _('-')
        text = '%s%s\n' % (text, _("Source: %s") % source)
        # location
        if locationID != Const.OID_NONE:
            obj = client.get(locationID, noUpdate = 1, publicOnly = 1)
            location = getattr(obj, 'name', res.getUnknownName())
        else:
            location = _('-')
        text = '%s%s\n' % (text, _("Location: %s") % location)
        text = '%s%s\n' % (text, _("Severity: %s") % _(gdata.msgSeverity[sev]))
        text = '%s%s\n' % (text, _("Time: %s [%s]") % (
            res.formatTime(turn),
            res.formatTime(turn - currTurn),
        ))
        text = '%s%s\n' % (text, "")
        text = '%s%s\n' % (text, getMsgText(msgID, data))

    return text
