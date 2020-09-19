

import math
import random
import sys

import Const
import Rules
import Utils

from ige import log

def finishStructOUTPOST(tran, source, target, tech):
    log.debug("Finishing OUTPOST", tech.id, "target", target.oid)
    # setup morale if colonizing noninhabited planet
    if target.storPop == 0:
        target.morale = Rules.maxMorale
    # try to change owner of planet
    tran.gameMngr.cmdPool[target.type].changeOwner(tran, target, source.owner)
    # increase population
    target.storPop += tech.unpackPop
    target.maxPop += tech.unpackPop

def finishStructSPORECOLONY(tran, source, target, tech):
    log.debug("Finishing SPORE COLONY", tech.id, "target", target.oid)
    # setup morale if colonizing noninhabited planet
    if target.storPop == 0:
        target.morale = Rules.maxMorale
    # try to change owner of planet
    tran.gameMngr.cmdPool[target.type].changeOwner(tran, target, source.owner)
    # increase population
    target.storPop += tech.unpackPop
    target.maxPop += tech.unpackPop

    if target.plSlots > 1:
        for i in range(len(target.slots),target.plSlots-1):
            target.slots.insert(0, Utils.newStructure(tran, 9013, source.owner, hpRatio = Rules.structFromShipHpRatio))

def finishStructGOVCENTER(tran, source, target, tech):
    player = tran.db[source.owner]
    # delete old center
    planet = tran.db[player.planets[0]]
    slots = planet.slots[:] # copy
    slots.reverse()
    govStr = 0
    for slot in slots:
        tech = Rules.techs[slot[Const.STRUCT_IDX_TECHID]]
        if tech.govPwr > 0 and planet.oid != target.oid:
            planet.slots.remove(slot)
            break
        elif tech.govPwr > 0:
            if govStr == 1:
                planet.slots.remove(slot)
                break
            else:
                govStr = 1
    # setup new one (move planet with new centre to the first position)
    player.planets.remove(target.oid)
    player.planets.insert(0, target.oid)
    # message
    Utils.sendMessage(tran, target, Const.MSG_NEW_GOVCENTER, target.oid, None)

def validateTRUE(tran,source,target,tech):
    return 1;

## Ecosystem initiation
def validateProjectECOINIT3(tran, source, target, tech):
    return target.plBio == 0 and target.plType not in ('G', 'A', '-')

def finishProjectECOINIT3(tran, source, target, tech):
    target.plBio = Rules.projECOINIT3PlBio

## Habitable Surface Expansion
def validateProjectADDSLOT3(tran, source, target, tech):
    return target.plSlots < target.plMaxSlots and target.plType not in ('G', 'A', '-')

def finishProjectADDSLOT3(tran, source, target, tech):
    target.plSlots += 1

## Terraforming
def validateDeployTERRAFORM3(tran, source, target, tech):
    return validateProjectTERRAFORM3(tran, source, target, tech) and \
        target.owner==source.owner

def validateProjectTERRAFORM3(tran, source, target, tech):
    spec = Rules.planetSpec[target.plType]
    solarminus = 0
    solarplus = 0
    if target.solarmod > 0:
        solarplus = target.solarmod
    if target.solarmod < 0:
        solarminus = target.solarmod
    #log.debug("En:",target.plEn,", Plus:",solarplus,", Minus:",solarminus,", Reqs:",spec.upgradeEnReqs)
    return spec.upgradeTo != None and \
        target.plEn + solarplus >= spec.upgradeEnReqs[0] and \
        target.plEn + solarminus <= spec.upgradeEnReqs[1] and \
        target.plBio >= spec.maxBio

def finishProjectTERRAFORM3(tran, source, target, tech):
    target.plType = Rules.planetSpec[target.plType].upgradeTo

## Uber Terraforming
def validateDeployTERRAFORMALIGNMENT6(tran, source, target, tech):
    return validateProjectTERRAFORMALIGNMENT6(tran, source, target, tech) and \
        target.owner==source.owner

def validateProjectTERRAFORMALIGNMENT6(tran, source, target, tech):
    log.debug('Validating TERRAFORM ALIGNMENT');
    spec = Rules.planetSpec[target.plType]
    return (target.plEnv < Rules.envMax or target.plBio < spec.upgradeEnReqs[0] or target.plBio > spec.upgradeEnReqs[1])

def finishProjectTERRAFORMALIGNMENT6(tran, source, target, tech):
    log.debug('Finishing TERRAFORM ALIGNMENT');
    spec = Rules.planetSpec[target.plType]
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    enAvg = int((spec.upgradeEnReqs[0] + spec.upgradeEnReqs[1]) / 2)
    delta = int(float(tech.data) * techEff)
    if target.plEn < enAvg:
        target.plEn = min(target.plEn+delta,enAvg)
    elif target.plEn > enAvg:
        target.plEn = max(target.plEn-delta,enAvg)
    target.plBio = min(target.plBio+int(delta/2),Rules.envMax)
    if validateProjectTERRAFORM3(tran, source, target, tech):
        target.plType = Rules.planetSpec[target.plType].upgradeTo

## Tech level advancement
def finishResTLAdvance(tran, player, tech):
    improvement = player.techs[tech.id]
    if improvement >= 3:
        player.techLevel = max(player.techLevel, tech.level + 1)
        player.race = tech.data

## Holidays
def finishProjectHOLIDAYS1(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    # no battle
    system = tran.db[source.compOf]
    if system.combatCounter == 0:
        source.morale = min(source.morale + int(tech.moraleTrgt * techEff), Rules.maxMorale)

## Produce resources
def finishProjectPRODRSRC(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    # raw resources
    target.storBio += int(tech.prodBio * techEff)
    target.storEn += int(tech.prodEn * techEff)
    # sci pts
    if target.owner != Const.OID_NONE:
        owner = tran.db[target.owner]
        owner.sciPoints += int(tech.prodSci * techEff)

## Produce strategic resource
def finishProjectNF(tran, source, target, tech):
    if target.owner != Const.OID_NONE:
        techEff = Utils.getTechEff(tran, tech.id, source.owner)
        # TODO success shall depend on the level of the technology
        owner = tran.db[target.owner]
        stratRes = int(tech.data)
        owner.stratRes[stratRes] = owner.stratRes.get(stratRes, 0) + Rules.stratResAmountSmall

## Antimatter transmutation
def finishProjectNF2(tran, source, target, tech):
    if target.owner != Const.OID_NONE:
        techEff = Utils.getTechEff(tran, tech.id, source.owner)
        # TODO success shall depend on the level of the technology
        owner = tran.db[target.owner]
        stratRes = int(tech.data)
        owner.stratRes[stratRes] = owner.stratRes.get(stratRes, 0) + 4 * Rules.stratResAmountBig
        Utils.sendMessage(tran, target, Const.MSG_EXTRACTED_ANTIMATTER_SYNTH, target.oid, stratRes)

## Upgrade ships
def finishProjectUPGRADESHIPS(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    # fleet upgrade pool
    if target.owner != Const.OID_NONE:
        owner = tran.db[target.owner]
        owner.fleetUpgradePool += int(tech.prodProd * techEff)

## Deep scan
def finishProjectDEEPSPACESCAN(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    target.scannerPwr = min(int(float(tech.data) * techEff * target.scannerPwr), Rules.scannerMaxPwr)
    system = tran.db[target.compOf]
    system.scannerPwrs[target.owner] = max(system.scannerPwrs.get(target.owner, 0), target.scannerPwr)

## improve environment
def finishProjectIMPRENV(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    target.plEnv += int(float(tech.data) * techEff)

## QDev
def validateProjectCondPl(tran, source, target, tech):
    return target.plType == 'G'

def finishProjectCondPl(tran, source, target, tech):
    target.plType = 'R'
    target.plDiameter = target.plDiameter / 10
    target.plMaxSlots = target.plDiameter / 1000
    target.plSlots = target.plMaxSlots / 2

def validateProjectAssemblePl(tran, source, target, tech):
    return target.plType == 'A'

def finishProjectAssemblePl(tran, source, target, tech):
    target.plType = 'D'
    target.plDiameter = (random.randrange(1, 7) + random.randrange(1, 7) + 2) * 1000
    target.plMaxSlots = target.plDiameter / 1000
    target.plSlots = target.plMaxSlots / 2

def finishProjectAsteroidMining(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    minerals = min(int(float(tech.data) * techEff), target.plMin)
    # now, transfer only minerals up to 200 on source planet
    minerals = min(minerals, 200 - source.plMin)
    target.plMin -= minerals
    source.plMin += minerals

def validateProjectBioEnrich(tran, source, target, tech):
    spec = Rules.planetSpec['E']
    return spec.upgradeTo != None and \
        target.plEn >= spec.upgradeEnReqs[0] and \
        target.plEn <= spec.upgradeEnReqs[1]

def finishProjectBioEnrich(tran, source, target, tech):
    target.plType = 'I'
    target.plBio = 200
    target.storPop = 1000

def validateProjectMinEnrich(tran, source, target, tech):
    return 1

def finishProjectMinEnrich(tran, source, target, tech):
    target.plMin = 200
    target.storPop = 1000

def validateProjectShiftPlDown(tran, source, target, tech):
    return target.plEn < 200

def finishProjectShiftPlDown(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    target.plEn = min(200, int(target.plEn + int(tech.data) * techEff))
    system = tran.db[target.compOf]
    tran.gameMngr.cmdPool[system.type].sortPlanets(tran, system, None)

def validateProjectShiftPlUp(tran, source, target, tech):
    return target.plEn > 0

def finishProjectShiftPlUp(tran, source, target, tech):
    techEff = Utils.getTechEff(tran, tech.id, source.owner)
    target.plEn = max(0, int(target.plEn - int(tech.data) * techEff))
    system = tran.db[target.compOf]
    tran.gameMngr.cmdPool[system.type].sortPlanets(tran, system, None)

## Pirate colonization
def OLDgetPirateFameMod(tran, player, system):
    mod = 1.0
    for planetID in system.planets:
        planet = tran.db[planetID]
        if planet.owner == player.oid:
            # minimum reached, don't check rest
            return 0.0
        elif planet.plStratRes in (Const.SR_TL3A, Const.SR_TL3B, Const.SR_TL3C):
            mod = min(mod, Rules.pirateTL3StratResColonyCostMod)
    return mod

def distToNearestPiratePlanet(tran,obj,srcObj):
    # srcObj can be Planet or System type
    dist = sys.maxint
    for objID in obj.planets:
        pirPl = tran.db[objID]
        d = math.hypot(srcObj.x - pirPl.x, srcObj.y - pirPl.y)
        if d < dist:
            dist = d
    return dist

def getPirateFameMod(tran, player, system):
    mod = 1.0
    for planetID in system.planets:
        planet = tran.db[planetID]
        if getattr(planet, 'owner', Const.OID_NONE) == player.oid:
            # minimum reached, don't check rest
            return 0.0
        elif getattr(planet, 'plStratRes', None) in (Const.SR_TL3A, Const.SR_TL3B, Const.SR_TL3C):
            mod = min(mod, Rules.pirateTL3StratResColonyCostMod)
    dist = distToNearestPiratePlanet(tran, player, system)
    if Rules.pirateGainFamePropability(dist) > 0:
        mod = Rules.pirateColonyFameZoneCost(dist)
    else:
        mod = Rules.pirateColonyPlayerZoneCost(dist)
    return mod

def validateStructPIROUTPOST(tran, source, target, tech):
    player = tran.db[source.owner]
    if source.type == Const.T_FLEET and target.owner != player.oid:
        mod = getPirateFameMod(tran, player, tran.db[target.compOf])
        return player.pirateFame >= int(mod * Rules.pirateColonyCostMod * len(player.planets))
    else:
        return True

def finishStructPIROUTPOST(tran, source, target, tech):
    log.debug("Finishing PIRATE OUTPOST", tech.id, "target", target.oid)
    player = tran.db[source.owner]
    famePenalty = 0
    if source.type == Const.T_FLEET:
        mod = getPirateFameMod(tran, player, tran.db[target.compOf])
        log.debug(source.owner, "DEPLOYING MODULE -- BEFORE", player.pirateFame, mod)
        famePenalty = int(mod * Rules.pirateColonyCostMod * len(player.planets))
        log.debug(source.owner, "DEPLOYING MODULE -- AFTER", player.pirateFame - famePenalty, famePenalty)
    finishStructOUTPOST(tran, source, target, tech)
    player.pirateFame -= famePenalty
