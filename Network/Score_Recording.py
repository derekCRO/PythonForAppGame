from .Settings import Class_Scoring
from .Event_Scoring import *
import time
import datetime
import logging
import jsonpickle
import os

logger = logging.getLogger('logger')

class Score_Recorder():
    def __init__(self):
        self.deviceScores = [Device_Scoring() for i in range(96)]
        self.teamScores = [0] * 8
        self.teamsActive = [False] * 8
        self.hits = []
        self.hitEvents = []
        self.startTime = time.strftime("%d/%m/%Y, %H:%M") #game ID
        self.deviceNames = ["? DEVICE NAME ?" for i in range(96)]

        self.finalisedScoresList = []
        self.newScoresheetsAvailable = False

       # self.finishScoring()


    def applyScoringEvent(self, scoringEvent):
        for i in range(len(scoringEvent.ScoringEvents)):
            event = scoringEvent.ScoringEvents[i]
            if(isinstance(event, Event_Score_Generic)):                 #holds a recursive scoring event
                self.applyScoringEvent(event)
            elif(isinstance(event, Event_Score_Team)):                  #is a team score change
                if(event.team < 0 or event.team > 7):
                    logger.info("Invalid scoring event - team " + str(event.team))
                else:
                    self.teamScores[event.team] += event.scoreChange

            elif(isinstance(event, Event_Score_Player)):                #is a player score change
                self.deviceScores[event.player].score += event.scoreChange

            elif(isinstance(event, Event_Score_Player_Stat)):           #is a player stat change
                self.deviceScores[event.player].stats[event.statKey] += event.statChange

            logger.info("Invalid scoring event type.")



    def appendHit(self, sender, receiver, weaponType, hitLoc, flags, eliminated):
        newHit = Hit(sender, receiver, weaponType, hitLoc, flags)

        if(sender < 64):
            if(self.deviceScores[sender].playing != True):
                logger.info("Sender Invalid - ID " + str(sender))
                return
        if(receiver < 64):
            if(self.deviceScores[receiver].playing != True):
                logger.info("Receiver Invalid - ID " + str(receiver))
                return

        self.deviceScores[sender].active = True
        self.deviceScores[receiver].active = True
        #team set active below

        if(sender < 64 and receiver < 64):
            if(flags <= 15 and flags >= 0):
                deflectorShield = False
                virus = False
                if ((flags != -1) and (flags <= 15) and (flags >= 0)):  # powerup flag
                    powerup = self.gameSettings.powerups[flags]
                    if (powerup.type == 4):  # deflector shield
                        deflectorShield = True
                    elif (powerup.type == 8):  # virus
                        virus = True
                logger.info("Virus or Deflector Shield shot came in - scoring aborted")
                return

        senderTeam = self.gameSettings.findTeam(sender)
        receiverTeam = self.gameSettings.findTeam(receiver)

        #general scoring
        if (sender < 64):  # sent by a player
            if (receiver < 64):  # hit a player

                if(senderTeam == -1):
                    logger.info("Couldn't find team for player: " + sender + ". Abandoning scoring for this tag.")
                    return
                if(receiverTeam == -1):
                    logger.info("Couldn't find team for player: " + receiver + ". Abandoning scoring for this tag.")
                    return

                if((senderTeam == receiverTeam) and
                       ((self.gameSettings.coreSettings.friendlyFireMode == 0) or (self.gameSettings.coreSettings.friendlyFireMode == 1))): #friendly fire
                    self.deviceScores[sender].HITFRIENDLY += 1
                    self.deviceScores[receiver].HITBYFRIENDLY += 1
                    self.deviceScores[sender].score += self.gameSettings.playerScoring.hitOwnTeam
                    self.teamScores[senderTeam] += self.gameSettings.teamScoring.hitOwnTeam
                    self.teamsActive[senderTeam] = True
                    self.teamsActive[receiverTeam] = True
                else:
                    #update player stats
                    self.deviceScores[sender].PLAYERS_TAGGED += 1
                    self.deviceScores[receiver].TIMES_TAGGED += 1
                    #tag streak
                    self.deviceScores[sender].currentTagStreak += 1
                    self.deviceScores[receiver].currentTagStreak = 0
                    if(self.deviceScores[sender].currentTagStreak > self.deviceScores[sender].LONGEST_TAG_STREAK):
                        self.deviceScores[sender].LONGEST_TAG_STREAK = self.deviceScores[sender].currentTagStreak
                    # update weapon stats
                    if (self.gameSettings.weapons[weaponType].type == 0):
                        self.deviceScores[sender].WPN_STANDARD += 1
                    elif (self.gameSettings.weapons[weaponType].type == 1):
                        self.deviceScores[sender].WPN_AUTORIFLE += 1
                    elif (self.gameSettings.weapons[weaponType].type == 2):
                        self.deviceScores[sender].WPN_SNIPER += 1
                    elif (self.gameSettings.weapons[weaponType].type == 3):
                        self.deviceScores[sender].WPN_BLASTER += 1
                    elif (self.gameSettings.weapons[weaponType].type == 4):
                        self.deviceScores[sender].WPN_BURSTRIFLE += 1
                    elif (self.gameSettings.weapons[weaponType].type == 5):
                        self.deviceScores[sender].WPN_SYSTEMHACK += 1
                    elif (self.gameSettings.weapons[weaponType].type == 6):
                        self.deviceScores[sender].WPN_RECHARGER += 1
                    elif (self.gameSettings.weapons[weaponType].type == 7):
                        self.deviceScores[sender].WPN_NANOVIRUS += 1
                    elif (self.gameSettings.weapons[weaponType].type == 8):
                        self.deviceScores[sender].WPN_RESTORE += 1
                    elif (self.gameSettings.weapons[weaponType].type == 9):
                        self.deviceScores[sender].WPN_SABOTAGE += 1
                    if(hitLoc == 5):
                        self.deviceScores[sender].HIT_PHASER += 1
                        self.deviceScores[receiver].HIT_ON_PHASER += 1
                    elif(hitLoc == 0):                    #back
                        self.deviceScores[sender].ASSASSINATIONS += 1
                        self.deviceScores[receiver].ASSASSINATED += 1
                        self.deviceScores[sender].HIT_BACK += 1
                        self.deviceScores[receiver].HIT_ON_BACK += 1
                    elif (hitLoc == 1):
                        self.deviceScores[sender].HIT_FR += 1
                        self.deviceScores[receiver].HIT_ON_FR += 1
                    elif (hitLoc == 2):
                        self.deviceScores[sender].HIT_FL += 1
                        self.deviceScores[receiver].HIT_ON_FL += 1
                    elif (hitLoc == 3):
                        self.deviceScores[sender].HIT_SR += 1
                        self.deviceScores[receiver].HIT_ON_SR += 1
                    elif (hitLoc == 4):
                        self.deviceScores[sender].HIT_SL += 1
                        self.deviceScores[receiver].HIT_ON_SL += 1
                    # update team scores
                    if(senderTeam != -1 and receiverTeam != -1):
                        if(self.gameSettings.coreSettings.type != 3):   #zombies are handled below
                            # update player scores
                            self.deviceScores[sender].score += self.gameSettings.playerScoring.hitOpponent
                            self.deviceScores[receiver].score += self.gameSettings.playerScoring.hitByOpponent
                            self.teamScores[senderTeam] += self.gameSettings.teamScoring.hitOpponent
                            self.teamScores[receiverTeam] += self.gameSettings.teamScoring.hitByOpponent
                            self.teamsActive[senderTeam] = True
                            self.teamsActive[receiverTeam] = True
            else:
                profile = self.gameSettings.findNetworkUnitProfile(receiver)
                if (profile == -1):
                    logging.error("Couldn't find a team for receiver device ID" + str(receiver))
                    return  # do nothing, something went wrong here

                profileType = self.gameSettings.networkUnitProfiles[profile].mode
                if (profileType == 0):  # effects
                    pass
                elif (profileType == 1):  # target
                    self.deviceScores[sender].TARGETS_HIT += 1
                    self.deviceScores[sender].score += self.gameSettings.playerScoring.hitTarget
                    self.teamScores[self.gameSettings.findTeam(sender)] += self.gameSettings.teamScoring.hitTarget
                    pass
                elif (profileType == 2):  # powerup
                    pass
                elif (profileType == 3):  # flag
                    pass
                elif (profileType == 4):  # territory
                    pass
                elif (profileType == 5):  # recharger
                    pass
                else:                     #unknown profile type
                    pass
        else:
            profile = self.gameSettings.findNetworkUnitProfile(sender)
            if (profile == -1 or receiver >= 64):
                logging.error("Couldn't find a profile for sender network ID " + str(sender))
                return  # do nothing, something went wrong here

            profileType = self.gameSettings.networkUnitProfiles[profile].mode
            if (profileType == 0):  # effects
                pass
            elif (profileType == 1):  # target
                pass
            elif (profileType == 2):  # powerup
                self.deviceScores[receiver].POWERUPS_FROM_TERMINALS += 1
                pass
            elif (profileType == 3):  # flag
                pass
            elif (profileType == 4):  # territory
                pass
            elif (profileType == 5):  # recharger
                pass
            else:  # unknown profile type
                pass

        #Game type specific scoring
        if(self.gameSettings.coreSettings.type == 0):       #classic
            if(self.gameSettings.classicSettings.gameMode == 1):    #vip
                senderIsVIP = sender in self.vips
                receiverIsVIP = receiver in self.vips
                if (senderIsVIP):
                    self.deviceScores[receiver].score += self.gameSettings.playerScoring.hitByVIP
                    self.teamScores[receiverTeam] += self.gameSettings.teamScoring.hitByVIP
                    self.deviceScores[receiver].VIP_HITBY += 1
                    self.deviceScores[sender].VIP_HITOTHERS += 1
                if (receiverIsVIP):
                    self.deviceScores[sender].score += self.gameSettings.playerScoring.hitVIP
                    self.teamScores[senderTeam] += self.gameSettings.teamScoring.hitVIP
                    self.deviceScores[sender].VIP_HIT += 1
            if(self.gameSettings.classicSettings.gameMode == 2):    #juggernaut
                senderIsJuggernaut = (sender == self.juggernaut)
                receiverIsJuggernaut = (receiver == self.juggernaut)
                if(senderIsJuggernaut):
                    self.deviceScores[receiver].score += self.gameSettings.playerScoring.hitByJuggernaut
                    self.teamScores[receiverTeam] += self.gameSettings.teamScoring.hitByJuggernaut
                    self.deviceScores[receiver].JUGG_HITBY += 1
                    self.deviceScores[sender].JUGG_HITOTHERS += 1
                if(receiverIsJuggernaut):
                    self.deviceScores[sender].score += self.gameSettings.playerScoring.hitByJuggernaut
                    self.teamScores[senderTeam] += self.gameSettings.teamScoring.hitByJuggernaut
                    self.deviceScores[sender].JUGG_HIT += 1
            pass
        elif(self.gameSettings.coreSettings.type == 1):     #territories

            pass
        elif(self.gameSettings.coreSettings.type == 2):     #CTF

            pass
        elif(self.gameSettings.coreSettings.type == 3):     #zombies
            if(senderTeam <= 63 and senderTeam >= 0 and receiverTeam <= 63 and receiverTeam >= 0):
                senderTeam = self.gameSettings.findTeam(sender)
                receiverTeam = self.gameSettings.findTeam(receiver)
                self.teamsActive[senderTeam] = True
                self.teamsActive[receiverTeam] = True
                if(receiverTeam != 6 and receiverTeam != 7):    #survivor
                    if(senderTeam == 6):                                                    #zombies
                        self.deviceScores[receiver].score += self.gameSettings.playerScoring.survivorTaggedByZombie
                        self.deviceScores[sender].score += self.gameSettings.playerScoring.zombieTaggedSurvivor
                        self.teamScores[receiverTeam] += self.gameSettings.teamScoring.survivorTaggedByZombie
                        self.teamScores[senderTeam] += self.gameSettings.teamScoring.zombieTaggedSurvivor
                        self.deviceScores[sender].ZOMB_HIT_SURVIVORS_AS_ZOMBIE += 1
                        if(eliminated):
                            self.deviceScores[sender].ZOMB_TURNED_SURVIVORS += 1
                            self.deviceScores[receiver].score += self.gameSettings.playerScoring.survivorTurnedToZombie
                            self.deviceScores[sender].score += self.gameSettings.playerScoring.zombieTurnedSurvivor
                            self.teamScores[receiverTeam] += self.gameSettings.teamScoring.survivorTurnedToZombie
                            self.teamScores[senderTeam] += self.gameSettings.teamScoring.zombieTurnedSurvivor
                    elif(senderTeam == 7):                                                  #alphas
                        self.deviceScores[receiver].score += self.gameSettings.playerScoring.survivorTaggedByZombie
                        self.deviceScores[sender].score += self.gameSettings.playerScoring.alphaTaggedSurvivor
                        self.teamScores[receiverTeam] += self.gameSettings.teamScoring.survivorTaggedByZombie
                        self.teamScores[senderTeam] += self.gameSettings.teamScoring.zombieTaggedSurvivor
                        self.deviceScores[sender].ZOMB_HIT_SURVIVORS_AS_ZOMBIE += 1
                        if (eliminated):
                            self.deviceScores[sender].ZOMB_TURNED_SURVIVORS += 1
                            self.deviceScores[receiver].score += self.gameSettings.playerScoring.survivorTurnedToZombie
                            self.deviceScores[sender].score += self.gameSettings.playerScoring.zombieTurnedSurvivor
                            self.teamScores[receiverTeam] += self.gameSettings.teamScoring.survivorTaggedByZombie
                            self.teamScores[senderTeam] += self.gameSettings.teamScoring.zombieTurnedSurvivor
                    else:                                                                    #survivor team
                        self.deviceScores[receiver].score += self.gameSettings.playerScoring.hitByOpponent
                        self.deviceScores[sender].score += self.gameSettings.playerScoring.hitOpponent
                        self.teamScores[receiverTeam] += self.gameSettings.teamScoring.hitByOpponent
                        self.teamScores[senderTeam] += self.gameSettings.teamScoring.hitOpponent
                        self.deviceScores[sender].ZOMB_HIT_SURVIVORS_AS_SURVIVOR += 1
                elif(receiverTeam == 6):
                    self.deviceScores[receiver].score += self.gameSettings.playerScoring.zombieTaggedBySurvivor
                    self.deviceScores[sender].score += self.gameSettings.playerScoring.survivorTaggedZombie
                    self.teamScores[receiverTeam] += self.gameSettings.teamScoring.zombieTaggedBySurvivor
                    self.teamScores[senderTeam] += self.gameSettings.teamScoring.survivorTaggedZombie
                    self.deviceScores[sender].ZOMB_HIT_ZOMBIES_AS_SURVIVOR += 1
                elif(receiverTeam == 7):
                    self.deviceScores[receiver].score += self.gameSettings.playerScoring.alphaTaggedBySurvivor
                    self.deviceScores[sender].score += self.gameSettings.playerScoring.survivorTaggedZombie
                    self.teamScores[receiverTeam] += self.gameSettings.teamScoring.alphaTaggedBySurvivor
                    self.teamScores[senderTeam] += self.gameSettings.teamScoring.survivorTaggedZombie
                    self.deviceScores[sender].ZOMB_HIT_ZOMBIES_AS_SURVIVOR += 1

        self.hits.append(newHit)

    def appendHitEvent(self, event):
        self.hitEvents.append(event)

        if(event.shooterIsPhaser() and self.deviceScores[event.shooterID].playing != True):
            logger.info("Sender Invalid - ID " + str(event.shooterID))
            return
        if(event.targetIsPhaser() and self.deviceScores[event.targetID].playing != True):
            logger.info("Receiver Invalid - ID " + str(event.targetID))
            return

        self.deviceScores[event.shooterID].active = True
        self.deviceScores[event.targetID].active = True

        if(event.getPowerupHitFlag() != -1):    #was a powerup hit
            powerup = event.getPowerupHitFlag()
            if(powerup == ENUM_Powerup.DEFLECTORSHIELD):
                self.deviceScores[event.shooterID].PWRUP_DEFLECT_HITBY += 1
                self.deviceScores[event.targetID].PWRUP_DEFLECT += 1
            elif(powerup == ENUM_Powerup.VIRUS):
                self.deviceScores[event.shooterID].PWRUP_VIRUS_HITBY += 1
                self.deviceScores[event.targetID].PWRUP_VIRUS += 1

        if(event.shooterIsPhaser()):
            if(event.targetIsPhaser()):

                # if a player shot a player
                if(event.wasFriendlyFire()
                        and ((self.gameSettings.coreSettings.friendlyFireMode == 0)
                            or (self.gameSettings.coreSettings.friendlyFireMode == 1))):
                    self.deviceScores[event.shooterID].HITFRIENDLY += 1
                    self.deviceScores[event.targetID].HITBYFRIENDLY += 1
                    self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.hitOwnTeam
                    self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.hitOwnTeam
                    self.teamsActive[event.getShooterTeam()] = True
                    self.teamsActive[event.getTargetTeam()] = True
                else:
                    #update player stats
                    self.deviceScores[event.shooterID].PLAYERS_TAGGED += 1
                    self.deviceScores[event.targetID].TIMES_TAGGED += 1
                    #tag streak
                    self.deviceScores[event.shooterID].currentTagStreak += 1
                    self.deviceScores[event.targetID].currentTagStreak = 0
                    if(self.deviceScores[event.shooterID].currentTagStreak > self.deviceScores[event.shooterID].LONGEST_TAG_STREAK):
                        self.deviceScores[event.shooterID].LONGEST_TAG_STREAK = self.deviceScores[event.shooterID].currentTagStreak

                    # update weapon stats
                    if (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.PHASER):
                        self.deviceScores[event.shooterID].WPN_STANDARD += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.AUTORIFLE):
                        self.deviceScores[event.shooterID].WPN_AUTORIFLE += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.SNIPER):
                        self.deviceScores[event.shooterID].WPN_SNIPER += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.BLASTER):
                        self.deviceScores[event.shooterID].WPN_BLASTER += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.BURSTRIFLE):
                        self.deviceScores[event.shooterID].WPN_BURSTRIFLE += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.SYSTEMHACK):
                        self.deviceScores[event.shooterID].WPN_SYSTEMHACK += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.RECHARGER):
                        self.deviceScores[event.shooterID].WPN_RECHARGER += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.NANOVIRUS):
                        self.deviceScores[event.shooterID].WPN_NANOVIRUS += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.RESTORE  ):
                        self.deviceScores[event.shooterID].WPN_RESTORE += 1
                    elif (self.gameSettings.weapons[event.getWeaponType()].type == ENUM_Weapon.SABOTAGE):
                        self.deviceScores[event.shooterID].WPN_SABOTAGE += 1

                    # update hit location stats
                    if(event.hitLocation == ENUM_HitLocations.PHASER):
                        self.deviceScores[event.shooterID].HIT_PHASER += 1
                        self.deviceScores[event.targetID].HIT_ON_PHASER += 1
                    elif(event.hitLocation == ENUM_HitLocations.BACK):                    #back
                        self.deviceScores[event.shooterID].ASSASSINATIONS += 1
                        self.deviceScores[event.targetID].ASSASSINATED += 1
                        self.deviceScores[event.shooterID].HIT_BACK += 1
                        self.deviceScores[event.targetID].HIT_ON_BACK += 1
                    elif (event.hitLocation == ENUM_HitLocations.FRONT_RIGHT):
                        self.deviceScores[event.shooterID].HIT_FR += 1
                        self.deviceScores[event.targetID].HIT_ON_FR += 1
                    elif (event.hitLocation == ENUM_HitLocations.FRONT_LEFT):
                        self.deviceScores[event.shooterID].HIT_FL += 1
                        self.deviceScores[event.targetID].HIT_ON_FL += 1
                    elif (event.hitLocation == ENUM_HitLocations.SHOULDER_RIGHT):
                        self.deviceScores[event.shooterID].HIT_SR += 1
                        self.deviceScores[event.targetID].HIT_ON_SR += 1
                    elif (event.hitLocation == ENUM_HitLocations.SHOULDER_LEFT):
                        self.deviceScores[event.shooterID].HIT_SL += 1
                        self.deviceScores[event.targetID].HIT_ON_SL += 1

                    # update team scores
                    if(self.gameSettings.coreSettings.type != 3):   #zombies are handled below
                        # update player scores
                        self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.hitOpponent
                        self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.hitByOpponent
                        self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.hitOpponent
                        self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.hitByOpponent
                        self.teamsActive[event.getShooterTeam()] = True
                        self.teamsActive[event.getTargetTeam()] = True

                #a player shot a network unit
            else:
                profileMode = event.getTargetNetworkUnitProfileMode()

                if (profileMode == ENUM_NetworkUnitMode.EFFECTS):  # effects
                    pass
                elif (profileMode == ENUM_NetworkUnitMode.TARGET):  # target
                    self.deviceScores[event.shooterID].TARGETS_HIT += 1
                    self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.hitTarget
                    self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.hitTarget
                    pass
                elif (profileMode == ENUM_NetworkUnitMode.POWERUPTERMINAL):  # powerup
                    pass
                elif (profileMode == ENUM_NetworkUnitMode.FLAGSTATION):  # flag
                    pass
                elif (profileMode == ENUM_NetworkUnitMode.TERRITORY):  # territory
                    pass
                elif (profileMode == ENUM_NetworkUnitMode.RECHARGER):  # recharger
                    pass
                else:  # unknown profile type
                    pass
        else:
            profileMode = event.getShooterNetworkUnitProfileMode()

            if (profileMode == ENUM_NetworkUnitMode.EFFECTS):  # effects
                pass
            elif (profileMode == ENUM_NetworkUnitMode.TARGET):  # target
                pass
            elif (profileMode == ENUM_NetworkUnitMode.POWERUPTERMINAL):  # powerup
                self.deviceScores[event.targetID].POWERUPS_FROM_TERMINALS += 1
                pass
            elif (profileMode == ENUM_NetworkUnitMode.FLAGSTATION):  # flag
                pass
            elif (profileMode == ENUM_NetworkUnitMode.TERRITORY):  # territory
                pass
            elif (profileMode == ENUM_NetworkUnitMode.RECHARGER):  # recharger
                pass
            else:  # unknown profile type
                pass

        #Game type specific scoring
        if(self.gameSettings.coreSettings.type == 0):       #classic
            if(self.gameSettings.classicSettings.gameMode == 1):    #vip
                if (event.shooterWasVIP()):
                    self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.hitByVIP
                    self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.hitByVIP
                    self.deviceScores[event.targetID].VIP_HITBY += 1
                    self.deviceScores[event.shooterID].VIP_HITOTHERS += 1
                if (event.targetWasVIP()):
                    self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.hitVIP
                    self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.hitVIP
                    self.deviceScores[event.shooterID].VIP_HIT += 1
            if(self.gameSettings.classicSettings.gameMode == 2):    #juggernaut
                if(event.shooterWasJuggernaut()):
                    self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.hitByJuggernaut
                    self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.hitByJuggernaut
                    self.deviceScores[event.targetID].JUGG_HITBY += 1
                    self.deviceScores[event.shooterID].JUGG_HITOTHERS += 1
                if(event.targetWasJuggernaut()):
                    self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.hitByJuggernaut
                    self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.hitByJuggernaut
                    self.deviceScores[event.shooterID].JUGG_HIT += 1
            pass
        elif(self.gameSettings.coreSettings.type == 1):     #territories

            pass
        elif(self.gameSettings.coreSettings.type == 2):     #CTF

            pass
        elif(self.gameSettings.coreSettings.type == 3):     #zombies
            self.teamsActive[event.getShooterTeam()] = True
            self.teamsActive[event.getTargetTeam()] = True
            if(event.getTargetTeam() != 6 and event.getTargetTeam() != 7):    #survivor
                if(event.getShooterTeam() == 6):                                                    #zombies
                    self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.survivorTaggedByZombie
                    self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.zombieTaggedSurvivor
                    self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.survivorTaggedByZombie
                    self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.zombieTaggedSurvivor
                    self.deviceScores[event.shooterID].ZOMB_HIT_SURVIVORS_AS_ZOMBIE += 1
                    if(event.wasEliminated()):
                        self.deviceScores[event.shooterID].ZOMB_TURNED_SURVIVORS += 1
                        self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.survivorTurnedToZombie
                        self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.zombieTurnedSurvivor
                        self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.survivorTurnedToZombie
                        self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.zombieTurnedSurvivor
                elif(event.getShooterTeam() == 7):                                                  #alphas
                    self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.survivorTaggedByZombie
                    self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.alphaTaggedSurvivor
                    self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.survivorTaggedByZombie
                    self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.zombieTaggedSurvivor
                    self.deviceScores[event.shooterID].ZOMB_HIT_SURVIVORS_AS_ZOMBIE += 1
                    if (event.wasEliminated()):
                        self.deviceScores[event.shooterID].ZOMB_TURNED_SURVIVORS += 1
                        self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.survivorTurnedToZombie
                        self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.zombieTurnedSurvivor
                        self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.survivorTaggedByZombie
                        self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.zombieTurnedSurvivor
                else:                                                                    #survivor team
                    self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.hitByOpponent
                    self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.hitOpponent
                    self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.hitByOpponent
                    self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.hitOpponent
                    self.deviceScores[event.shooterID].ZOMB_HIT_SURVIVORS_AS_SURVIVOR += 1
            elif(event.getTargetTeam() == 6):
                self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.zombieTaggedBySurvivor
                self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.survivorTaggedZombie
                self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.zombieTaggedBySurvivor
                self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.survivorTaggedZombie
                self.deviceScores[event.shooterID].ZOMB_HIT_ZOMBIES_AS_SURVIVOR += 1
            elif(event.getTargetTeam() == 7):
                self.deviceScores[event.targetID].score += self.gameSettings.playerScoring.alphaTaggedBySurvivor
                self.deviceScores[event.shooterID].score += self.gameSettings.playerScoring.survivorTaggedZombie
                self.teamScores[event.getTargetTeam()] += self.gameSettings.teamScoring.alphaTaggedBySurvivor
                self.teamScores[event.getShooterTeam()] += self.gameSettings.teamScoring.survivorTaggedZombie
                self.deviceScores[event.shooterID].ZOMB_HIT_ZOMBIES_AS_SURVIVOR += 1


    def clear(self):
        for i in range(8):
            self.teamScores[i] = 0
        self.hits.clear()
        self.hitEvents.clear()
        for i in range(96):
            self.deviceScores[i].clear()

    def score_print(self, text):
        string = "[" + time.strftime("%H:%M:%S") + "][SCORING] " + text
        #print(string)
        logging.info(text)

    def startScoring(self, gameSettings, deviceNamesList, playingList):
        self.clear()
        self.deviceNames = deviceNamesList
        self.gameSettings = gameSettings
        for i in range(64):
            self.deviceScores[i].score = self.gameSettings.playerScoring.startingPoints
            self.deviceScores[i].active = False
            self.deviceScores[i].playing = playingList[i]
        for i in range(8):
            self.teamScores[i] = self.gameSettings.teamScoring.startingPoints
            self.teamsActive[i] = False
        self.startTime = time.strftime("%d/%m/%Y, %H:%M")
        self.startTimeRaw = time.time()

    def setVIPSandJuggernaut(self, vips, juggernaut):
        self.vips = vips
        self.juggernaut = juggernaut

    def finishScoring(self):
        self.finalisedScoresList.append(self.getScoresListForScoresheet())
        self.newScoresheetsAvailable = True
        #self.lastScoresList = self.getScoresListForScoresheet()

        #fileString = 'ERROR_REPORTS/ErrorReport-{date:%Y-%m-%d_%H-%M-%S}.zip'.format( date=datetime.datetime.now() )
        directoryName = "SCORES/{date:%m-%Y}/{date:%d}/".format(date=datetime.datetime.fromtimestamp(self.startTimeRaw))

        #directoryName = "SCORES/" + time.strftime("%m-%Y", self.startTimeRaw) + time.strftime("%d", self.startTimeRaw)
        if not os.path.exists(directoryName):
            os.makedirs(directoryName)
            self.score_print("Created new directory: " + directoryName)
        #with open(time.strftime("%H-%M", self.startTimeRaw) + ".json", 'a') as file:
        with open(directoryName + "/{date:%H-%M}.json".format(date=datetime.datetime.fromtimestamp(self.startTimeRaw)), 'a') as file:
            file.write(jsonpickle.encode(self.gameSettings) + '\n')
            [file.write(self.deviceScores[i].getJSONString() + '\n') for i in range(len(self.deviceScores))]
            [file.write(self.hits[i].getJSONString() + '\n') for i in range(len(self.hits))]

    def updateGameSettings(self, gameSettings):     #MUST BE CALLED
        self.gameSettings = gameSettings

    def getPlayerScorePositions(self):
        playerList = []
        for i in range(64):         #get all of the players
            playerList.append([self.deviceScores[i].score, -1, self.deviceScores[i].active])

        activePlayerList = []       #get the active players
        for i in range(len(playerList)):
            if(playerList[i][2] == True):
                activePlayerList.append([i, playerList[i]])

        if(len(activePlayerList) != 0):
            #sort active players and handle draws
            sortedPlayers = sorted(activePlayerList, key=lambda players: players[1][0], reverse=True)   #sort by score
            sortedPlayers[0][1][1] = 1     #first place
            for i in range(len(sortedPlayers) - 1):
                if(sortedPlayers[i+1][1][0] == sortedPlayers[i][1][0]):
                    sortedPlayers[i+1][1][1] = sortedPlayers[i][1][1]
                else:
                    sortedPlayers[i+1][1][1] = i+2
            if(len(activePlayerList) != 1):
                playerList[sortedPlayers[i+1][0]][1] = sortedPlayers[i+1][1][1]

        return playerList

    def getTeamScorePositions(self):
        teamList = []
        for i in range(8):         #get all of the teams
            teamList.append([self.teamScores[i], -1, self.teamsActive[i]])

        activeTeamList = []       #get the active teams
        for i in range(len(teamList)):
            if(teamList[i][2] == True):
                activeTeamList.append([i, teamList[i]])

        if(len(activeTeamList) != 0):
            #sort active players and handle draws
            sortedTeams = sorted(activeTeamList, key=lambda teams: teams[1][0], reverse=True)   #sort by score
            sortedTeams[0][1][1] = 1     #first place
            for i in range(len(sortedTeams) - 1):
                if(sortedTeams[i+1][1][0] == sortedTeams[i][1][0]):
                    sortedTeams[i+1][1][1] = sortedTeams[i][1][1]
                else:
                    sortedTeams[i+1][1][1] = i+2
            if(len(activeTeamList) != 1):
                teamList[sortedTeams[i+1][0]][1] = sortedTeams[i+1][1][1]

        return teamList

    def getNumPlayersInLastGame(self):
        scoreListLen = len(self.finalisedScoresList)
        if (scoreListLen == 0):
            return 0
        else:
            return len(self.finalisedScoresList[scoreListLen - 1][0])

    def getLastScoresListForScoresheet(self):
        scoreListLen = len(self.finalisedScoresList)
        self.newScoresheetsAvailable = False
        if(scoreListLen == 0):
            return None
        else:
            return self.finalisedScoresList[scoreListLen - 1]

    def getScoresListForScoresheet(self):
        count = 0
        for i in range(64):
            if(self.deviceScores[i].active == True):
                count += 1
        scoresList = []
        scorePositions = self.getPlayerScorePositions()
        for i in range(64):
            #if(1):
            if(self.deviceScores[i].active == True):
                playerScores = []
                playerScores.append("Quasar Hemel")
                playerScores.append("179 Marlowes")
                playerScores.append("www.quasarhemel.co.uk")
                playerScores.append("01442 213200")
                playerScores.append(self.deviceScores[i].HIT_SR)
                playerScores.append(self.deviceScores[i].HIT_FR)
                playerScores.append(self.deviceScores[i].HIT_SL)
                playerScores.append(self.deviceScores[i].HIT_FL)
                playerScores.append(self.deviceScores[i].HIT_BACK)
                playerScores.append(self.deviceScores[i].HIT_PHASER)

                playerScores.append(self.gameSettings.coreSettings.name)
                teamCount = 0
                for x in range(8):
                    if(self.teamsActive[x] == True):
                        teamCount += 1

                if(teamCount > 1):
                    for x in range(8):
                        if(self.teamsActive[x]):
                            playerScores.append(self.gameSettings.teams[x].name)
                        else:
                            playerScores.append("")

                    for x in range(8):
                        if(self.teamsActive[x]):
                            playerScores.append(self.teamScores[x])
                        else:
                            playerScores.append("")
                else:
                    for x in range(16):
                        playerScores.append("")

                playerScores.append("PLAYERS TAGGED")
                playerScores.append(self.deviceScores[i].PLAYERS_TAGGED)
                playerScores.append("TIMES TAGGED")
                playerScores.append(self.deviceScores[i].TIMES_TAGGED)
                playerScores.append(" ")
                playerScores.append(" ")
                playerScores.append("TAG RATIO")
                tagRatio = 0
                if(self.deviceScores[i].PLAYERS_TAGGED != 0 and self.deviceScores[i].TIMES_TAGGED != 0):
                    tagRatio = format(float(self.deviceScores[i].PLAYERS_TAGGED / self.deviceScores[i].TIMES_TAGGED), '.2f')
                playerScores.append(tagRatio)
                playerScores.append("TARGETS HIT")
                playerScores.append(self.deviceScores[i].TARGETS_HIT)
                playerScores.append("POWERUPS ACQUIRED")
                playerScores.append(self.deviceScores[i].POWERUPS_FROM_TERMINALS)
                playerScores.append(" ")
                playerScores.append(" ")
                playerScores.append("LONGEST TAG STREAK")
                playerScores.append(self.deviceScores[i].LONGEST_TAG_STREAK)
                playerScores.append("ASSASSINATED")
                playerScores.append(self.deviceScores[i].ASSASSINATED)
                playerScores.append("PHASER TAGS")
                playerScores.append(self.deviceScores[i].WPN_STANDARD)
                playerScores.append("AUTORIFLE TAGS")
                playerScores.append(self.deviceScores[i].WPN_AUTORIFLE)
                playerScores.append("BURST-RIFLE TAGS")
                playerScores.append(self.deviceScores[i].WPN_BURSTRIFLE)

                playerScores.append(str(i) + " - " + self.deviceNames[i])  #NUM - NAME
                playerScores.append(self.gameSettings.teams[self.gameSettings.findTeam(i)].name)
                playerScores.append(" ")    #membership number
                playerScores.append(" ")    #membership team name
                playerScores.append(self.startTime)
                playerScores.append("Score: " + str(self.deviceScores[i].score))
                try:
                    playerScores.append("Position: " + str(scorePositions[i][1]) + " / " + str(count))
                except ValueError:
                    playerScores.append("Position: ? / " + str(count))
                playerScores.append(i)
                scoresList.append(playerScores)
        return [scoresList, self.startTime]

class Hit():
    def __init__(self, sender, receiver, weaponType, hitLoc, flags):
        self.sender = sender
        self.receiver = receiver
        self.weaponType = weaponType
        self.hitLoc = hitLoc
        self.flags = flags
        self.hitTime = int(time.time())

    def getJSONString(self):
        return jsonpickle.encode(self)

class Device_Scoring():
    def __init__(self):
        self.clear()

    def clear(self):
        self.score = 0
        self.active = False
        self.playing = False

        self.currentTagStreak = 0

        #new way of doing stat tracking 5.4.0+
        self.stats = {
            "JUGG_HIT" : 0,
            "JUGG_HIT" : 0,
            "JUGG_HITBY" : 0,
            "JUGG_HITOTHERS" : 0,
            "JUGG_BECAME" : 0,
            "VIP_HIT" : 0,
            "VIP_HITBY" : 0,
            "VIP_HITOTHERS" : 0,
            "ELIM_LASTMAN" : 0,
            "TERR_CAPTURED" : 0,
            "TERR_DEFENCE" : 0,
            "TERR_OFFENCE" : 0,
            "TERR_HELD" : 0,
            "FLAG_CAPTURED" : 0,
            "FLAG_TAKEN" : 0,
            "FLAG_PASSED" : 0,
            "FLAG_DROPPED" : 0,
            "FLAG_HELD" : 0,
            "ZOMB_HIT_ZOMBIES_AS_SURVIVOR" : 0,
            "ZOMB_HIT_SURVIVORS_AS_ZOMBIE" : 0,
            "ZOMB_TURNED_SURVIVORS" : 0,
            "ZOMB_HIT_SURVIVORS_AS_SURVIVOR" : 0,
            "PLAYERS_TAGGED" : 0,
            "TIMES_TAGGED" : 0,
            "POWERUPS_USED" : 0,
            "LONGEST_TAG_STREAK" : 0,
            "TARGETS_HIT" : 0,
            "WPN_STANDARD" : 0,
            "WPN_AUTORIFLE" : 0,
            "WPN_SNIPER" : 0,
            "WPN_BLASTER" : 0,
            "WPN_BURSTRIFLE" : 0,
            "WPN_SYSTEMHACK" : 0,
            "WPN_RECHARGER" : 0,
            "WPN_NANOVIRUS" : 0,
            "WPN_RESTORE" : 0,
            "WPN_SABOTAGE" : 0,
            "PWRUP_SPY" : 0,
            "PWRUP_STEALTH" : 0,
            "PWRUP_INVULN" : 0,
            "PWRUP_DEFLECT" : 0,
            "PWRUP_VIRUS" : 0,
            "TAG_STREAK_REWARDS" : 0,
            "ASSASSINATIONS" : 0,
            "ASSASSINATED" : 0,
            "RELOADED" : 0,
            "HITREFLEX" : 0,
            "PWRUP_SPY_HITBY" : 0,
            "PWRUP_STEALTH_HITBY" : 0,
            "PWRUP_DEFLECT_HITBY" : 0,
            "PWRUP_VIRUS_HITBY" : 0,
            "HITFRIENDLY" : 0,
            "HITBYFRIENDLY" : 0,

            "HIT_ON_FR" : 0,
            "HIT_ON_FL" : 0,
            "HIT_ON_SR" : 0,
            "HIT_ON_SL" : 0,
            "HIT_ON_PHASER" : 0,
            "HIT_ON_BACK" : 0,

            "HIT_BACK" : 0,
            "HIT_FR" : 0,
            "HIT_FL" : 0,
            "HIT_SR" : 0,
            "HIT_SL" : 0,
            "HIT_PHASER" : 0,

            "POWERUPS_FROM_TERMINALS" : 0
            
        }

        # old way of stat tracking <= 5.3.2
        self.JUGG_HIT = 0
        self.JUGG_HITBY = 0
        self.JUGG_HITOTHERS = 0
        self.JUGG_BECAME = 0
        self.VIP_HIT = 0
        self.VIP_HITBY = 0
        self.VIP_HITOTHERS = 0
        self.ELIM_LASTMAN = 0
        self.TERR_CAPTURED = 0
        self.TERR_DEFENCE = 0
        self.TERR_OFFENCE = 0
        self.TERR_HELD = 0
        self.FLAG_CAPTURED = 0
        self.FLAG_TAKEN = 0
        self.FLAG_PASSED = 0
        self.FLAG_DROPPED = 0
        self.FLAG_HELD = 0
        self.ZOMB_HIT_ZOMBIES_AS_SURVIVOR = 0
        self.ZOMB_HIT_SURVIVORS_AS_ZOMBIE = 0
        self.ZOMB_TURNED_SURVIVORS = 0
        self.ZOMB_HIT_SURVIVORS_AS_SURVIVOR = 0
        self.PLAYERS_TAGGED = 0
        self.TIMES_TAGGED = 0
        self.POWERUPS_USED = 0
        self.LONGEST_TAG_STREAK = 0
        self.TARGETS_HIT = 0
        self.WPN_STANDARD = 0
        self.WPN_AUTORIFLE = 0
        self.WPN_SNIPER = 0
        self.WPN_BLASTER = 0
        self.WPN_BURSTRIFLE = 0
        self.WPN_SYSTEMHACK = 0
        self.WPN_RECHARGER = 0
        self.WPN_NANOVIRUS = 0
        self.WPN_RESTORE = 0
        self.WPN_SABOTAGE = 0
        self.PWRUP_SPY = 0
        self.PWRUP_STEALTH = 0
        self.PWRUP_INVULN = 0
        self.PWRUP_DEFLECT = 0
        self.PWRUP_VIRUS = 0
        self.TAG_STREAK_REWARDS = 0
        self.ASSASSINATIONS = 0
        self.ASSASSINATED = 0
        self.RELOADED = 0
        self.HITREFLEX = 0
        self.PWRUP_SPY_HITBY = 0
        self.PWRUP_STEALTH_HITBY = 0
        self.PWRUP_DEFLECT_HITBY = 0
        self.PWRUP_VIRUS_HITBY = 0
        self.HITFRIENDLY = 0
        self.HITBYFRIENDLY = 0

        self.HIT_ON_FR = 0
        self.HIT_ON_FL = 0
        self.HIT_ON_SR = 0
        self.HIT_ON_SL = 0
        self.HIT_ON_PHASER = 0
        self.HIT_ON_BACK = 0

        self.HIT_BACK = 0
        self.HIT_FR = 0
        self.HIT_FL = 0
        self.HIT_SR = 0
        self.HIT_SL = 0
        self.HIT_PHASER = 0

        self.POWERUPS_FROM_TERMINALS = 0

    def getJSONString(self):
        return jsonpickle.encode(self)