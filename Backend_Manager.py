import time
import random
import os
import json
import logging
import jsonpickle
from threading import Timer
from random import shuffle
from tkinter import messagebox

from .Network import *
from .Game_Managers import *
from .RepeatedTimer import *
from .ConfigData import *
from .TwitterInterface import *

"""
GAME STATE ENUMERATIONS
- Standby       0
- Setup         1
- Countdown     2
- Playing       3
- End           4
"""

logger = logging.getLogger('logger')

class Backend_Manager():
    def __init__(self):
        self.gameSettings = GameSettings()
        self.backendLog = []
        self.startTime = self.getCurrentTime()
        self.networkManager = Network_Manager()
        self.networkManager.scores.updateGameSettings(self.gameSettings)
        self.gameState = 0
        self.oldTeamLeader = 0
        self.gameNo = 1
        self.reportLogs = []
        self.activePhasers = [False for i in range(64)]
        self.twitterInterface = TwitterInterface()

        self.flag_updatedReportLog = False

        #new way
        self.globalSettings_scoring = []
        self.globalSettings_weapons = []
        self.globalSettings_powerups = []
        self.globalSettings_networkUnitProfiles = []
        self.globalSettings_stats = []
        self.globalSettings_games = []

        self.loadConfiguration()

    def updateGlobalSettings(self, newSettings):
        self.globalSettings_scoring = newSettings['scoring']
        self.globalSettings_weapons = newSettings['weapons']
        self.globalSettings_powerups = newSettings['powerups']
        self.globalSettings_networkUnitProfiles = newSettings['networkUnitProfiles']
        self.globalSettings_stats = newSettings['stats']
        self.globalSettings_games = newSettings['games']

    #this function builds a GameSettings object from the global list and the Data object
    def buildSettings(self, gameSettings):
        newGameSettings = GameSettings()
        newGameSettings.IDname = gameSettings.IDname
        newGameSettings.coreSettings = gameSettings.coreSettings
        newGameSettings.classicSettings = gameSettings.classicSettings
        newGameSettings.ctfSettings = gameSettings.ctfSettings
        newGameSettings.territoriesSettings = gameSettings.territoriesSettings
        newGameSettings.zombiesSettings = gameSettings.zombiesSettings
        for i in range(8):
            newGameSettings.teams[i] = gameSettings.teams[i]
            newGameSettings.stats[i] = gameSettings.stats[i]
        newGameSettings.teamScoring = gameSettings.teamScoring
        newGameSettings.playerScoring = gameSettings.playerScoring
        for i in range(16):
            newGameSettings.weapons[i] = gameSettings.weapons[i]
            newGameSettings.powerups[i] = gameSettings.powerups[i]
        for i in range(8):
            newGameSettings.networkUnitProfiles[i] = gameSettings.networkUnitProfiles[i]

        self.gameSettings = newGameSettings
        return newGameSettings

    def appendReportLog(self, state):
        duration = int(self.getElapsedTime() / 1000)
        if(state == "Cancelled"):
            durationString = "00:00"
        else:
            mins = int(duration/60)
            if(mins < 10):
                minsStr = "0"
            else:
                minsStr = ""
            minsStr += str(mins)
            secs = int(duration%60)
            if(secs <10):
                secsStr = "0"
            else:
                secsStr = ""
            secsStr += str(secs)
            durationString = minsStr + ":" + secsStr

        log = {"gameNo":self.gameNo, "timeStamp":time.strftime("%d/%m/%Y, %H:%M", time.localtime(int(self.startTime / 1000))), "state":state, "duration":durationString, "gameIDName":self.gameSettings.IDname, "playerCount":self.networkManager.scores.getNumPlayersInLastGame()}

        self.reportLogs.append(log)
        self.newLog = log
        self.flag_updatedReportLog = True

    def getReportLogs(self):
        return self.reportLogs

    def loadConfiguration(self):
        self.backend_print("Loading configuration.")
        fileDirectory = (os.path.join(os.path.dirname(__file__), os.pardir) + "\\Configuration\configuration.txt")
        try:
            file = open(fileDirectory, 'r')
            content = file.readline()
            file.close()
            self.config = jsonpickle.decode(content)
            self.networkManager.initialise(self.config.brokerIP)
            for i in range(96):
                self.networkManager.assignDevice(i, self.config.names[i], self.config.deviceTypes[i], self.config.serialNums[i], self.config.macs[i])
            set0 = CCARD_LIST(0, self.config.ccards[:8])
            self.networkManager.sendMessage(set0, True)
            set1 = CCARD_LIST(1, self.config.ccards[8:16])
            self.networkManager.sendMessage(set1, True)
            self.backend_print("Configuration loaded. CCARD IDs sent.")
            if(self.config.twitterEnabled):
                self.twitterInterface.connectToTwitter(self.config.consumer_key, self.config.consumer_secret, self.config.token, self.config.token_secret)
            self.networkManager.setAdvancedConfig(self.config.holsterCharging, self.config.ignoreBatteryState, self.config.phaserOnlyLowVoltage, self.config.phaserLowVoltage, self.config.phaserFirmware)
            rssi = QCONFIGRSSI(self.config.rssiThreshold)
            self.networkManager.sendMessage(rssi, True)
        except FileNotFoundError:
            self.backend_print("Error - could not find configuration file - loading defaults. Not sending CCARD info.")
            self.config = ConfigData()

    def applyPreset(self, number):
        if(number >= self.getNumOfPresets()):
            self.backend_print("Couldn't apply preset " + str(number) + " - doesn't exist.")
            return
        if(self.gameState == 0 or self.gameState == 4):
            self.gameSettings = self.buildSettings(self.globalSettings_games[number])
        if(self.gameState == 1):
            self.gameSettings = self.buildSettings(self.globalSettings_games[number])
            #CALCULATE TEAMS
            self.calculateTeamsForCurrentSettings()
            self.sendGameSettingsToDevices()
            self.updateScores()
            self.sendGameState()

    def getScoresheetData(self):
        return self.networkManager.scores.getLastScoresListForScoresheet()

    def calculateTeamsForCurrentSettings(self, debugPrints = False):
        availablePhasersList = self.networkManager.getAvailablePhasersList(False)  # SET TRUE TO FORCE ALL AVAILABLE FOR DEBUGGING
        self.backend_print("Calculating team assignments... " + str(len(availablePhasersList)) + " phasers available.")

        for i in range(64):
            for x in range(8):
                self.gameSettings.teams[x].removePlayerFromTeam(i)

        assignmentListParser = 0
        playersAssignedToTeam = [0 for i in range(8)]
        teamCounter = 0

        phaseOne = False
        phaseTwo = False

        #assign minimum number of players
        assignedInThisPass = False
        while (phaseOne == False):
            if (assignmentListParser >= len(availablePhasersList)):
                #self.backend_print("RAN OUT OF PHASERS TO ASSIGN")
                phaseOne = True
                phaseTwo = True
            else:
                if(self.gameSettings.teams[teamCounter].minimumPlayers > playersAssignedToTeam[teamCounter]):
                    self.gameSettings.teams[teamCounter].addPlayerToTeam(availablePhasersList[assignmentListParser])
                    playersAssignedToTeam[teamCounter] += 1
                    assignmentListParser += 1
                    assignedInThisPass = True
                teamCounter += 1
                if (teamCounter == 8):
                    teamCounter = 0
                    if(assignedInThisPass == False):
                        phaseOne = True
                    assignedInThisPass = False
        if(debugPrints):
            self.backend_print("Finished phase one. " + str(assignmentListParser) + str(" devices assigned:"))
            string = ""
            for i in range(7):
                string += ("Team " + str(i) + ": " + str(playersAssignedToTeam[i]) + ", ")
            string += ("Team " + str(i) + ": " + str(playersAssignedToTeam[7]))
            self.backend_print(string)

        teamCounter = 0
        #assign remaining players, or until max numbers reached for all teams
        assignedInThisPass = False
        while (phaseTwo == False):
            if (assignmentListParser >= len(availablePhasersList)):
                phaseTwo = True
            else:
                if((self.gameSettings.teams[teamCounter].maximumPlayers > playersAssignedToTeam[teamCounter]) or self.gameSettings.teams[teamCounter].maximumPlayers == -1):
                    self.gameSettings.teams[teamCounter].addPlayerToTeam(availablePhasersList[assignmentListParser])
                    playersAssignedToTeam[teamCounter] += 1

                    assignmentListParser += 1
                    assignedInThisPass = True
                teamCounter += 1
                if (teamCounter == 8):
                    teamCounter = 0
                    if(assignedInThisPass == False):
                        phaseTwo = True
                    assignedInThisPass = False
                if(assignmentListParser >= len(availablePhasersList)):
                    if(debugPrints):
                        self.backend_print("No more teams to assign phasers to.")
                    phaseTwo = True

        self.backend_print("Finished team assignments. " + str(assignmentListParser) + str(" devices assigned:"))
        string = ""
        for i in range(7):
            string += ("Team " + str(i) + ": " + str(playersAssignedToTeam[i]) + ", ")
        string += ("Team " + str(7) + ": " + str(playersAssignedToTeam[7]))
        self.backend_print(string)

        self.playingList = [False for _ in range(64)]
        for i in range(8):
            idlist = self.gameSettings.teams[i].getIDListForMessage()
            for j in range(64):
                if(idlist[j] == True):
                    self.playingList[j] = True


    def getNumOfPresets(self):
        return len(self.globalSettings_games)

    def getPresetName(self, id):
        return self.globalSettings_games[id].IDname

    def getCurrentTime(self):
        return int(round(time.time() * 1000))

    def getElapsedTime(self):
        return self.getCurrentTime() - self.startTime

    def backend_print(self, text):
        string = "[" + time.strftime("%H:%M:%S") + "][BACKEND] " + text
        #print(string)
        self.backendLog.append(string)
        logger.info(text)

    def game_print(self, text):
        string = "[" + time.strftime("%H:%M:%S") + "][GAME] " + text
        #print(string)
        self.backendLog.append(string)
        logger.info(text)

    def getInUseDevicesList(self):
        deviceList = []
        for i in range(len(self.networkManager.devices)):
            if(self.networkManager.devices[i].inUse):
                deviceList.append(self.networkManager.devices[i])
        return deviceList

    def sendGameSettingsToDevices(self):
        self.networkManager.network_print("Sending Game Settings")
        # send core settings
        core = SETTINGS_CORE(self.gameSettings.coreSettings)
        self.networkManager.sendMessage(core, True)

        # send game specific settings
        if (self.gameSettings.coreSettings.type == 0):
            specific = SETTINGS_CLASSIC(self.gameSettings.classicSettings)
            self.networkManager.sendMessage(specific, True)
        if(self.gameSettings.coreSettings.type == 2):
            specific = SETTINGS_CTF(self.gameSettings.ctfSettings)
            self.networkManager.sendMessage(specific, True)
        elif (self.gameSettings.coreSettings.type == 3):
            specific = SETTINGS_ZOMBIES(self.gameSettings.zombiesSettings)
            self.networkManager.sendMessage(specific, True)

        # send teams
        for i in range(8):
            # print("colour: " + str(gameSettings.teams[i].colour.red) + ", " + str(gameSettings.teams[i].colour.green) + ", " + str(gameSettings.teams[i].colour.blue))
            team1 = SETTINGS_TEAM1(i, self.gameSettings.teams[i])
            self.networkManager.sendMessage(team1, True)
            team2 = SETTINGS_TEAM2(i, self.gameSettings.teams[i])
            self.networkManager.sendMessage(team2, True)

        # send weapons
        for i in range(16):
            weapon = SETTINGS_WEAPON(i, self.gameSettings.weapons[i])
            self.networkManager.sendMessage(weapon, True)

        # send powerups
        for i in range(16):
            powerup = SETTINGS_POWERUP(i, self.gameSettings.powerups[i])
            self.networkManager.sendMessage(powerup, True)

        # send stat1
        for i in range(8):
            stat1 = SETTINGS_STAT1(i, self.gameSettings.stats[i])
            stat2 = SETTINGS_STAT2(i, self.gameSettings.stats[i])
            self.networkManager.sendMessage(stat1, True)
            self.networkManager.sendMessage(stat2, True)

        # send netunit profiles
        for i in range(8):
            profile = NETWORKUNIT_PROFILE(i, self.gameSettings.networkUnitProfiles[i])
            self.networkManager.sendMessage(profile, True)

        # send net unit assignments
        assignments = NETWORKUNIT_ASSIGN(self.gameSettings.networkUnitProfiles)
        self.networkManager.sendMessage(assignments, True)

        # send game events
        classic = EVENT_CLASSIC(self.vip_vipsList, -1)
        self.networkManager.sendMessage(classic, True)

        ctf = EVENT_CTF(self.flag_flagCarriers, self.flag_flagCappedBy, self.flag_available)
        self.networkManager.sendMessage(ctf, True)


    def sendControlCardID(self, id, group = 0):
        message = CCARD_ADD(id, group)
        self.networkManager.sendMessage(message, False)
        pass

    def sendClearControlCards(self, group = 0):
        message = CCARD_CLR(group)
        self.networkManager.sendMessage(message, False)
        pass

    def enterStandby(self):
        self.game_print("GAME STATE -> STANDBY")
        self.gameState = 0
        self.sendGameState()

    def enterSetup(self):
        self.game_print("GAME STATE -> SETUP")
        if(self.networkManager.getConnected() == False):
            messagebox.showerror("QCore Backend Error", "MQTT Broker not connected. Game control functions unavailable.")
            return
        self.gameState = 1

        #CALCULATE TEAMS BEFORE SENDING
        self.calculateTeamsForCurrentSettings()

        self.vip_vipsList = [-1 for i in range(20)]
        self.vip_vipsAssigned = False
        self.juggernaut_juggernautAssigned = False
        self.juggernaut = -1
        self.juggernaut_transfers = 0

        self.flag_flagCarriers = [-1 for i in range(8)]
        self.flag_flagCappedBy = [-1 for i in range(8)]
        self.flag_available = [False for i in range(8)]

        self.flag_availableTimers = [0 for i in range(8)]

        self.sendGameSettingsToDevices()
        self.sendGameState()

        incorrectFirmwareVersionsList = []

        for i in range(8):
            for j in range(32):
                if(self.gameSettings.networkUnitProfiles[i].ids[j] == True):
                    if(self.config.networkUnitFirmware != "" and (self.networkManager.devices[j+64].firmwareVersion != self.config.networkUnitFirmware)):
                        incorrectFirmwareVersionsList.append(j)

        if(len(incorrectFirmwareVersionsList) > 0):
            warningString = "Warning - Network unit firmware version " + self.config.networkUnitFirmware + " required by advanced configuration. Following IDs have a different version: "
            for j in range(len(incorrectFirmwareVersionsList)):
                warningString += self.networkManager.devices[incorrectFirmwareVersionsList[j]+64].name
                warningString += ", "
            warningString = warningString[:-2]  #remove last two characters
            messagebox.showinfo("Network Unit Firmware Invalid", warningString)

    def enterCountdown(self):
        self.game_print("GAME STATE -> COUNTDOWN")
        if(self.networkManager.getConnected() == False):
            from tkinter import messagebox
            messagebox.showerror("QCore Backend Error", "MQTT Broker not connected. Game control functions unavailable.")
            return
        self.gameState = 2
        self.sendGameState()
        self.startTime = self.getCurrentTime() + 5000

        self.networkManager.scores.startScoring(self.gameSettings, self.networkManager.getDeviceNamesList(), self.playingList)
        self.clearScoreboardLog()
        self.writeToScoreboardLog("GAME START IN 5 SECONDS...")

    def enterPlaying(self):
        self.game_print("GAME STATE -> PLAYING")
        for i in range(64):
            self.activePhasers[i] = False
        self.gameState = 3
        self.sendGameState()
        self.gameNo += 1

        if(self.gameSettings.coreSettings.type == 2):   #ctf
            Timer(self.gameSettings.ctfSettings.flagCapturedResetDelay, self.flag_sendStartupStates).start()

        self.oldTeamLeader = 7
        self.scoreTimer = RepeatedTimer(5, self.updateScores)
        self.statusTimer = RepeatedTimer(5, self.sendGameState)
        self.writeToScoreboardLog("GAME STARTED!")

    def enterGameEnd(self, finishCondition):
        self.game_print("GAME STATE -> END")
        self.updateScores()  # one last score update
        self.networkManager.scores.finishScoring()
        self.gameState = 4
        self.gameEndTime = self.getCurrentTime()
        self.appendReportLog(finishCondition)   #has to be after scoring finishes
        try:
            self.scoreTimer.stop()
            self.statusTimer.stop()
        except AttributeError:
            pass
        """
        for i in range(64):
            self.game_print("Score " + str(i) + " " + str(self.networkManager.scores.deviceScores[i].score))
        for i in range(8):
            self.game_print("Team score " + str(i) + " " + str(self.networkManager.scores.teamScores[i]))
        """
        if(finishCondition == "Cancelled"):
            self.enterStandby()
        else:
            self.sendGameState()
            twitterString = ""
            if(self.networkManager.scores.getNumPlayersInLastGame() > 0):
                twitterString += '\"'
                twitterString += self.gameSettings.coreSettings.name
                twitterString += "\" finished at "
                twitterString += str(time.strftime("%H:%M:%S"))
                twitterString += ": "
                if(self.gameSettings.coreSettings.friendlyFireMode != 3):   #sol
                    for i in range(8):
                        if(self.networkManager.scores.teamsActive[i] == True):
                            twitterString += str(self.gameSettings.teams[i].name)
                            twitterString += ": "
                            twitterString += str(self.networkManager.scores.teamScores[i])
                            twitterString += ", "
                        twitterString + "\n"
                scorePositions = self.networkManager.scores.getPlayerScorePositions()
                first = -1
                for i in range(64):
                    if(scorePositions[i][1] == 1):
                        first = i
                        break

                twitterString += "Top Gun: "
                twitterString += str(first)
                twitterString += " - "
                twitterString += str(self.networkManager.devices[first].name)
                twitterString += " - "
                twitterString += str(self.networkManager.scores.deviceScores[first].score)
                self.twitterInterface.postToTwitter(twitterString)
        self.writeToScoreboardLog("GAME FINISHED")

    def sendGameState(self):
        elapsedTime = 0
        if(self.gameState == 3):
            elapsedTime = self.getElapsedTime()
        message = GAMESTATUS(self.gameState, 0, elapsedTime)
        self.networkManager.mqtt_publish(message.topicString, message.messageString, True)

        if (self.gameState == 3):
            timeRemaining = int((self.gameSettings.coreSettings.time * 60) - (self.getElapsedTime() / 1000))
        else:
            timeRemaining = int(self.gameSettings.coreSettings.time * 60)
        scoreboardMessage = str("{\"GAMESTATUS\":" + str(self.gameState)+", \"GAMENAME\":\"" + self.gameSettings.coreSettings.name + "\", \"REMAINING\":" + str(timeRemaining) + "}")
        self.networkManager.mqtt_publish("QNET/SCOREBOARD/STATUS", scoreboardMessage, True)

    def backend_loop(self):
        #handle incoming messages
        while(len(incomingMessageQueue) > 0):
            message = incomingMessageQueue.pop()
            if(message.type == "QDEBUG"):
                pass
            elif(message.type == "REG_REQ"):
                id = self.networkManager.handleRegRequest(message)
            elif(message.type == "HIT"):
                self.game_print("HIT: " + str(message.shooterID) + " hit " + str(message.targetID) + " with " + str(message.weaponID) + " on location " + str(message.hitLocation))
                self.networkManager.devices[message.targetID].kickCommunicationTimer()
                if(self.gameState == 3):
                    """
                    if(message.shooterID >= 0 and message.shooterID <= 95 and message.targetID >= 0 and message.targetID <= 95 and ((message.weaponID <= 15 and message.weaponID >= 0) or message.shooterID >= 64) and message.hitLocation <= 6 and message.hitLocation >= 0):
                        self.handleHit(message.shooterID, message.targetID, message.weaponID, message.hitLocation, message.targetHealth, message.targetShield, message.flags)
                    else:
                        self.backend_print("Warning - Invalid hit detected: " + str(message.shooterID) + ", " + str(message.targetID) + ", " + str(message.weaponID) + ", " + str(message.hitLocation))
                    """
                    newHitEvent = Event_Hit(self.gameSettings, message.shooterID, message.targetID, message.weaponID, message.hitLocation, message.targetHealth, message.targetShield, message.flags, self.vip_vipsList, self.juggernaut, self.flag_flagCarriers)
                    if(newHitEvent.isValid()):
                        self.handleHitEvent(newHitEvent)
                    else:
                        self.backend_print("Warning - Invalid hit detected! Ignoring.")

            elif(message.type == "STATUS"):
                if(message.networkID != 255):
                    #self.backend_print("STATUS: " + str(message.networkID) + " Batt: " + str(message.battVol) + "V. Charging: " + str(message.charging))
                    self.networkManager.devices[message.networkID].updateDeviceStatus(message.battVol, message.charging)
                pass
            elif(message.type == "ACK"):
                pass

        if(self.gameState == 2):
            if(self.getElapsedTime() >= 0):
                self.enterPlaying()
        elif(self.gameState == 3):
            if(self.getElapsedTime() >= (self.gameSettings.coreSettings.time * 60000)):
                self.enterGameEnd("Finished")

            if(self.gameSettings.coreSettings.type == 0):   #classic
                if(self.gameSettings.classicSettings.gameMode == 0): #classic
                    pass
                elif(self.gameSettings.classicSettings.gameMode == 1):   #VIP
                    if(self.vip_vipsAssigned == False):
                        if(self.getElapsedTime() >= 30000):
                            self.backend_print("Assigning VIPs...")
                            self.vip_vipsAssigned = True
                            activePhasers = [Device.netID for Device in self.networkManager.devices if Device.isActive()]

                            countTeamsActive = len([Team for Team in self.gameSettings.teams if (Team.maximumPlayers != 0)])
                            activeTeams = [False for i in range(8)]
                            for i in range(8):
                                activeTeams[i] = (self.gameSettings.teams[i].maximumPlayers != 0)

                            #work out number of VIPS required
                            vipsRequired = (self.gameSettings.classicSettings.vipsPerTeam * countTeamsActive)
                            vipsPerTeam = self.gameSettings.classicSettings.vipsPerTeam
                            if(vipsRequired > 20):
                                self.backend_print("Too many VIPs requested, maximum 20!")
                                vipsRequired = int(20 / countTeamsActive) * countTeamsActive    #it looks daft but this is right
                                vipsPerTeam = int(20 / countTeamsActive)

                            self.backend_print(str(len(activePhasers)) + " phasers active over " + str(countTeamsActive) + " teams. " + str(vipsRequired) + " vips to assign.")

                            #work out how many active phasers are on each team
                            activePhaserByTeam = [[] for i in range(8)]
                            for i in range(len(activePhasers)):
                                phaserTeam = self.gameSettings.findTeam(activePhasers[i])
                                if(phaserTeam != -1):
                                    activePhaserByTeam[phaserTeam].append(activePhasers[i])

                            #randomly shuffle the IDs so we can pick from the start [0]
                            for i in range(8):
                                shuffle(activePhaserByTeam[i])

                            newVIPS = []
                            for i in range(len(activeTeams)):
                                if(activeTeams[i] == True):
                                    for j in range(vipsPerTeam):
                                        if(j < len(activePhaserByTeam[i])):
                                            newVIPS.append(activePhaserByTeam[i][j])
                                        else:
                                            self.backend_print("Not enough active phasers for team " + str(i) + ". Not all vips assigned!")
                            self.backend_print(str(len(newVIPS)) + " vips assigned in total.")

                            self.vip_vipsList = [-1 for i in range(20)]
                            for i in range(len(newVIPS)):
                                self.vip_vipsList[i] = newVIPS[i]

                            msg = EVENT_CLASSIC(self.vip_vipsList, self.juggernaut)
                            self.networkManager.sendMessage(msg, True)
                elif(self.gameSettings.classicSettings.gameMode == 2):   #JUGGERNAUT
                    if(self.juggernaut_juggernautAssigned == False):
                        if(self.getElapsedTime() >= 30000):
                            self.backend_print("Assigning Juggernaut...")
                            self.juggernaut_juggernautAssigned = True
                            activePhasers = [Device.netID for Device in self.networkManager.devices if Device.isActive()]
                            shuffle(activePhasers)
                            if(len(activePhasers) > 0):
                                self.backend_print("Juggernaut assigned to player " + str(activePhasers[0]))
                                self.juggernaut = activePhasers[0]
                            else:
                                self.backend_print("No active phaser to assign juggernaut to!")

                            msg = EVENT_CLASSIC(self.vip_vipsList, self.juggernaut)
                            self.networkManager.sendMessage(msg, True)

                elif(self.gameSettings.classicSettings.gameMode == 3):   #ELIMINATOR
                    pass
                elif(self.gameSettings.classicSettings.gameMode == 4):   #SCAVENGER
                    pass
            elif(self.gameSettings.coreSettings.type == 1): #territories
                if(self.gameSettings.territoriesSettings.gameMode == 0):    #DOMINATION
                    pass
                elif(self.gameSettings.territoriesSettings.gameMode == 1):  #KOTH
                    pass
                elif(self.gameSettings.territoriesSettings.gameMode == 2):  #TOW
                    pass
            elif(self.gameSettings.coreSettings.type == 2): #CTF
                pass
            elif(self.gameSettings.coreSettings.type == 3): #ZOMBIES
                pass
        elif(self.gameState == 4):
            #THIS NEVER LEAVES STATE 4
            if((self.getCurrentTime() - self.gameEndTime) >= 60000):
                self.enterStandby()

    def handleHitEvent(self, event):
        """
        Kick activity Monitors
        """
        if(event.shooterIsPhaser()):
            if(self.networkManager.scores.deviceScores[event.shooterID].playing):
                self.activePhasers[event.shooterID] = True
                self.networkManager.devices[event.shooterID].kickActiveTimer()

        if(event.targetIsPhaser()):
            if(self.networkManager.scores.deviceScores[event.targetID].playing):
                self.activePhasers[event.targetID] = True
                self.networkManager.devices[event.targetID].kickActiveTimer()

        if(event.targetID == event.shooterID):
            self.backend_print("Player " + str(event.targetID) + " registered active.")
            return

        """
        Score the hit
        """
        self.networkManager.scores.setVIPSandJuggernaut(self.vip_vipsList, self.juggernaut)
        self.networkManager.scores.appendHit(event.shooterID, event.targetID, event.weaponID, event.hitLocation, event.flags, event.wasEliminated())

        """
        Handle game specific functionality
        """
        infected = False

        if (self.gameSettings.coreSettings.type == 0):  # classic
            if (self.gameSettings.classicSettings.gameMode == 0):  # classic
                pass
            elif (self.gameSettings.classicSettings.gameMode == 1):  # VIP
                #Were they a vip? or FORCE VIP CHANGE ON RECHARGE
                if(event.targetWasVIP() and (event.wasEliminated() or (event.targetIsPhaser() and event.shooterIsNetworkUnit() and event.getShooterNetworkUnitProfile().mode == 5))):
                    vipSlot = self.vip_vipsList.index(event.targetID)
                    self.vip_vipsList[vipSlot] = -1   #clear the VIP from the list
                    self.backend_print("VIP eliminated, player " + str(event.targetID) + " from team " + str(event.getTargetTeam()))

                    #do we need to assign a new VIP?
                    if(self.gameSettings.classicSettings.vipEliminationMode == False):
                        team = event.getTargetTeam()
                        teamActivePhasersNotVIP = [Device.netID for Device in self.networkManager.devices if (Device.isActive() and (self.gameSettings.findTeam(Device.netID) == team) and (not Device.netID in self.vip_vipsList) and (Device.netID != event.targetID))]
                        if(len(teamActivePhasersNotVIP) == 0):
                            self.backend_print("Could not find a valid player to give VIP to!")
                        else:
                            shuffle(teamActivePhasersNotVIP)    #randomise
                            self.vip_vipsList[vipSlot] = teamActivePhasersNotVIP[0]
                            self.backend_print("Assigning VIP to " + str(teamActivePhasersNotVIP[0]))


                    #send out the update
                    msg = EVENT_CLASSIC(self.vip_vipsList, self.juggernaut)
                    self.networkManager.sendMessage(msg, True)

            elif (self.gameSettings.classicSettings.gameMode == 2):  # JUGGERNAUT
                #was the sender the juggernaut
                if(event.shooterWasJuggernaut() and (self.gameSettings.classicSettings.juggernautTransferMode == 2) and ((self.juggernaut_transfers < self.gameSettings.classicSettings.juggernautMaxTransfers) or self.gameSettings.classicSettings.juggernautMaxTransfers == -1)):  #reverse
                    self.backend_print("Juggernaut tagged someone. Reverse transfer mode. Reassigning...")
                    self.juggernaut_transfers += 1
                    self.juggernaut = event.targetID
                    self.networkManager.scores.deviceScores[self.juggernaut].JUGG_BECAME += 1
                    self.backend_print("Juggernaut assigned to receiver, player " + str(self.juggernaut))
                    msg = EVENT_CLASSIC(self.vip_vipsList, self.juggernaut)
                    self.networkManager.sendMessage(msg, True)

                    #was the receiver the juggernaut
                elif(event.targetWasJuggernaut() and event.wasEliminated() and ((self.juggernaut_transfers < self.gameSettings.classicSettings.juggernautMaxTransfers) or self.gameSettings.classicSettings.juggernautMaxTransfers == -1)):
                    self.juggernaut_transfers += 1
                    self.backend_print("Juggernaut Eliminated. Reassigning...")
                    if(self.gameSettings.classicSettings.juggernautTransferMode == 0):  #Shooter
                        self.juggernaut = event.shooterID
                        self.backend_print("Juggernaut assigned to shooter, player " + str(self.juggernaut))
                        self.networkManager.scores.deviceScores[self.juggernaut].JUGG_BECAME += 1
                        msg = EVENT_CLASSIC(self.vip_vipsList, self.juggernaut)
                        self.networkManager.sendMessage(msg, True)
                    elif(self.gameSettings.classicSettings.juggernautTransferMode == 1):    #Random
                        activePhasers = [Device.netID for Device in self.networkManager.devices if Device.isActive()]
                        shuffle(activePhasers)
                        self.juggernaut = activePhasers[0]
                        self.backend_print("Juggernaut assigned randomly to player " + str(self.juggernaut))
                        self.networkManager.scores.deviceScores[self.juggernaut].JUGG_BECAME += 1
                        msg = EVENT_CLASSIC(self.vip_vipsList, self.juggernaut)
                        self.networkManager.sendMessage(msg, True)
            elif (self.gameSettings.classicSettings.gameMode == 3):  # ELIMINATOR
                pass
        elif (self.gameSettings.coreSettings.type == 1):  # territories
            if (self.gameSettings.territoriesSettings.gameMode == 0):  # DOMINATION
                pass
            elif (self.gameSettings.territoriesSettings.gameMode == 1):  # KOTH
                pass
            elif (self.gameSettings.territoriesSettings.gameMode == 2):  # TOW
                pass
        elif (self.gameSettings.coreSettings.type == 2):  # CTF
            if(event.targetIsPhaser()):

                #player is at a network unit
                if(event.shooterIsNetworkUnit()):
                    profileNumber = self.gameSettings.findNetworkUnitProfile(event.shooterID)
                    profile = self.gameSettings.networkUnitProfiles[profileNumber]

                    #player is at a flag station
                    if(profile.mode == 3):
                        #player is at an enemy flag station
                        if(profile.teamAffiliation != event.getTargetTeam()):
                            #player is at an enemy flag station and the flag is available
                            if(self.flag_available[profile.teamAffiliation]):
                                #player is at an enemy flag station, the flag is available and they don't already have a flag
                                if(not event.targetHasFlag()):
                                    self.flag_available[profile.teamAffiliation] = False
                                    self.flag_flagCarriers[profile.teamAffiliation] = event.targetID
                                    self.flag_sendFlagUpdate()
                                    self.backend_print(str(event.targetID) + " has taken team " + str(profile.teamAffiliation) + "'s flag")
                                    self.networkManager.scores.applyScoringEvent(Event_Score_CTF_TookFlag(event.targetID, self.gameSettings))
                        #player is at a friendly flag station
                        elif(profile.teamAffiliation == event.getTargetTeam()):
                            #player is at a friendly flag station with a flag
                            if(event.targetID in self.flag_flagCarriers):
                                teamsFlagThatWasCaptured = self.flag_flagCarriers.index(event.targetID)
                                self.flag_flagCarriers[teamsFlagThatWasCaptured] = -1
                                self.flag_sendFlagUpdate(event.targetID, teamsFlagThatWasCaptured)
                                self.flag_makeFlagAvailableAfterTime(self.gameSettings.ctfSettings.flagCapturedResetDelay, teamsFlagThatWasCaptured)
                                self.backend_print(str(event.targetID) + " has captured team " + str(teamsFlagThatWasCaptured) + "'s flag")
                                self.networkManager.scores.applyScoringEvent(Event_Score_CTF_FlagCapture(event.targetID, self.gameSettings))
                    elif(profile.mode == 5):
                        if(event.targetHasFlag()):
                            teamsFlagThatPlayerHad = self.flag_flagCarriers.index(event.targetID)
                            self.flag_flagCarriers[teamsFlagThatPlayerHad] = -1
                            self.flag_sendFlagUpdate()
                            self.flag_makeFlagAvailableAfterTime(self.gameSettings.ctfSettings.flagDropResetDelay, teamsFlagThatPlayerHad)
                            self.backend_print(str(event.targetID) + " dropped team " + str(teamsFlagThatPlayerHad) + "'s flag")
                            self.networkManager.scores.applyScoringEvent(Event_Score_CTF_HitFlagCarrier(event.targetID, self.gameSettings))

                #player has been hit by a player
                else:
                    #the player hit, had a flag
                    if(event.targetHasFlag()):
                        if(event.wasFriendlyFire()):
                            return
                        teamsFlagThatPlayerHad = self.flag_flagCarriers.index(event.targetID)
                        self.flag_flagCarriers[teamsFlagThatPlayerHad] = -1
                        self.flag_sendFlagUpdate()
                        self.flag_makeFlagAvailableAfterTime(self.gameSettings.ctfSettings.flagDropResetDelay, teamsFlagThatPlayerHad)
                        self.backend_print(str(event.targetID) + " dropped team " + str(teamsFlagThatPlayerHad) + "'s flag")
                        self.networkManager.scores.applyScoringEvent(Event_Score_CTF_HitFlagCarrier(event.targetID, self.gameSettings))
                    elif(event.shooterHasFlag() and event.wasFriendlyFire() and self.gameSettings.ctfSettings.flagPass and event.getWeaponType() == ENUM_Weapon.FLAG):
                        teamsFlagThatPlayerHad = self.flag_flagCarriers.index(event.shooterID)
                        self.flag_flagCarriers[teamsFlagThatPlayerHad] = event.targetID
                        self.flag_sendFlagUpdate()
                        #self.backend_print(str(receiver) + " dropped team " + str(teamsFlagThatPlayerHad) + "'s flag")
                        self.backend_print(str(event.shooterID) + " passed team " + str(teamsFlagThatPlayerHad) + "'s flag to " + str(event.targetID))

        elif (self.gameSettings.coreSettings.type == 3):  # ZOMBIES
            if (event.shooterIsPhaser() and event.targetIsPhaser()):
                if (event.wasEliminated()):  # eliminated
                    if (event.getTargetTeam() != 6 and event.getTargetTeam() != 7):  # was a survivor
                        # move teams, update
                        self.gameSettings.teams[event.getTargetTeam()].removePlayerFromTeam(event.targetID)
                        self.gameSettings.teams[6].addPlayerToTeam(event.targetID)
                        for i in range(8):
                            team1 = SETTINGS_TEAM1(i, self.gameSettings.teams[i])
                            self.networkManager.sendMessage(team1, True)
                            team2 = SETTINGS_TEAM2(i, self.gameSettings.teams[i])
                            self.networkManager.sendMessage(team2, True)
                        infected = True

                        # count survivors
                        count = 0
                        for i in range(64):
                            if (self.activePhasers[i]):
                                team = self.gameSettings.findTeam(i)
                                if (team != 6 and team != 7):
                                    count += 1
                        if (count == 0 and self.getElapsedTime() >= 120000):  # end game if all survivors are now zombies
                            self.enterGameEnd("Finished")

        """
        Handle powerup hits
        """
        deflectorShield = False
        virus = False

        if (event.shooterIsPhaser() and event.targetIsPhaser()):
            powerupFlag = event.getPowerupHitFlag()
            if(powerupFlag == ENUM_Powerup.DEFLECTORSHIELD):
                deflectorShield = True
            elif(powerupFlag == ENUM_Powerup.VIRUS):
                virus = True

        """
        Handle Scoreboard
        """
        scoreBoardLogText = ""
        if (event.shooterIsPhaser() and event.targetIsPhaser()):
            if (deflectorShield):
                scoreBoardLogText += str(self.networkManager.devices[event.targetID].name)
                scoreBoardLogText += " deflected a shot back to "
                scoreBoardLogText += str(self.networkManager.devices[event.shooterID].name)
            elif (virus):
                scoreBoardLogText += str(self.networkManager.devices[event.targetID].name)
                scoreBoardLogText += " disabled "
                scoreBoardLogText += str(self.networkManager.devices[event.shooterID].name)
                scoreBoardLogText += " with a virus!"
            elif (infected):
                scoreBoardLogText += str(self.networkManager.devices[event.targetID].name)
                scoreBoardLogText += " was turned to a zombie by "
                scoreBoardLogText += str(self.networkManager.devices[event.shooterID].name)
            elif(event.getHitLocation() == ENUM_HitLocations.BACK):
                scoreBoardLogText += str(self.networkManager.devices[event.shooterID].name)
                scoreBoardLogText += " assassinated "
                scoreBoardLogText += str(self.networkManager.devices[event.targetID].name)
            else:
                weapon = event.getWeaponType()
                if weapon == ENUM_Weapon.PHASER or weapon == ENUM_Weapon.AUTORIFLE or weapon == ENUM_Weapon.BURSTRIFLE:
                    shotStr = " tagged "
                elif weapon == ENUM_Weapon.SNIPER:
                    shotStr = " sniped "
                elif weapon == ENUM_Weapon.BLASTER:
                    shotStr = " blasted "
                elif weapon == ENUM_Weapon.SYSTEMHACK:
                    shotStr = " hacked into "
                elif weapon == ENUM_Weapon.RECHARGER:
                    shotStr = " recharged "
                elif weapon == ENUM_Weapon.NANOVIRUS:
                    shotStr = " installed a nanovirus into "
                elif weapon == ENUM_Weapon.RESTORE:
                    shotStr = " restored "
                elif weapon == ENUM_Weapon.SABOTAGE:
                    shotStr = " sabotaged the "
                elif weapon == ENUM_Weapon.FLAG:
                    shotStr = " passed the flag to "
                else:
                    shotStr = ""
                scoreBoardLogText += str(self.networkManager.devices[event.shooterID].name)
                scoreBoardLogText += shotStr
                scoreBoardLogText += str(self.networkManager.devices[event.targetID].name)

                # tag streaks
                tagStreakScoreboardText = ""
                tagStreak = self.networkManager.scores.deviceScores[event.shooterID].currentTagStreak
                if (tagStreak == 3 or tagStreak == 5 or tagStreak == 7 or tagStreak == 10):
                    tagStreakScoreboardText += str(self.networkManager.devices[event.shooterID].name)
                    tagStreakScoreboardText += " is on a " + str(tagStreak) + " tag streak!"
                    self.writeToScoreboardLog(tagStreakScoreboardText)

                # eliminated
                if (event.wasEliminated()):
                    eliminatedScoreboardText = str(self.networkManager.devices[event.targetID].name)
                    eliminatedScoreboardText += " was eliminated!"
                    self.writeToScoreboardLog(eliminatedScoreboardText)

        elif (event.shooterIsPhaser() and event.targetIsNetworkUnit()):
            netUnitProfile = self.gameSettings.findNetworkUnitProfile(event.targetID)
            if (self.gameSettings.networkUnitProfiles[netUnitProfile].mode == 1):
                scoreBoardLogText += str(self.networkManager.devices[event.shooterID].name)
                if (self.gameSettings.networkUnitProfiles[netUnitProfile].teamAffiliation == -1):
                    scoreBoardLogText += " tagged a bonus target!"
                else:
                    scoreBoardLogText += " tagged "
                    scoreBoardLogText += str(self.gameSettings.teams[self.gameSettings.networkUnitProfiles[
                        netUnitProfile].teamAffiliation].name)
                    scoreBoardLogText += "'s bonus target!"
                self.writeToScoreboardLog(scoreBoardLogText)
        elif (event.shooterIsNetworkUnit() and event.targetIsPhaser()):
            netUnitProfile = self.gameSettings.findNetworkUnitProfile(event.shooterID)
            if (self.gameSettings.networkUnitProfiles[netUnitProfile].mode == 2):
                scoreBoardLogText += str(self.networkManager.devices[event.targetID].name)
                scoreBoardLogText += " got a powerup!"
                self.writeToScoreboardLog(scoreBoardLogText)
            elif (self.gameSettings.networkUnitProfiles[netUnitProfile].mode == 5):
                scoreBoardLogText += str(self.networkManager.devices[event.targetID].name)
                scoreBoardLogText += " recharged at a terminal"
                self.writeToScoreboardLog(scoreBoardLogText)

    def updateScores(self):
        playerPositions = self.networkManager.scores.getPlayerScorePositions()
        teamPositions = self.networkManager.scores.getTeamScorePositions()

        #Uncomment these for position debugging information
        #print(playerPositions)
        #print(teamPositions)

        for i in range(len(playerPositions)):
            team = self.gameSettings.findTeam(i)
            if(team != -1):
                teamScore = teamPositions[team][0]
                teamPosition = teamPositions[team][1]
            else:
                teamScore = 0
                teamPosition = 0

            playerScore = playerPositions[i][0]
            playerPosition = playerPositions[i][1]

            message = SCOREUPDATE(i, playerScore, teamScore, playerPosition, teamPosition)
            self.networkManager.mqtt_publish(message.topicString, message.messageString, True, log=False)

            #Scoreboard
            #playerTopic = "QNET/SCOREBOARD/PLAYER/" + str(i)
            playerTopic = "QNET/SCOREBOARD/PLAYER"
            if(team == -1):
                team = 0        #scoreboard only accepts 0-7
            playerMessage = "{\"TEAMID\":" + str(team) + ", \"PLAYERID\": " + str(i) + ", \"PLAYERNAME\": \"" + self.networkManager.devices[i].name
            playerMessage += "\", \"SCORE\":" + str(playerScore) + ", \"ACTIVE\":"
            if(playerPositions[i][2] == True):
                playerMessage += "1"
            else:
                playerMessage += "0"
            #scoreboard doesn't used POSITION, rather it uses FLAGS for 1st-3rd
            playerMessage += ", \"POSITION\":" + str(playerPosition) + ", \"FLAGS\":" + str(playerPosition) + "}"
            #print(playerMessage)
            self.networkManager.mqtt_publish_noLimit(playerTopic, playerMessage, True, log=False)

        for i in range(8):
            teamTopic = "QNET/SCOREBOARD/TEAM/" + str(i)
            teamString = "{\"TEAMNAME\": \"" + self.gameSettings.teams[i].name + "\", "
            teamString += "\"SCORE\":" + str(self.networkManager.scores.teamScores[i]) + ", "
            teamString += "\"POSITION\":" + str(teamPositions[i][1]) + ", "
            teamString += "\"ACTIVE\":"
            if(teamPositions[i][2] == True):
                teamString += "1, "
            else:
                teamString += "0, "
            teamString += "\"RED\":"
            teamString += str(self.gameSettings.teams[i].red) + ", "
            teamString += "\"GREEN\":"
            teamString += str(self.gameSettings.teams[i].green) + ", "
            teamString += "\"BLUE\":"
            teamString += str(self.gameSettings.teams[i].blue) + ", "
            teamString += "\"FORECOLOR\":"
            if(self.gameSettings.teams[i].red + self.gameSettings.teams[i].green + self.gameSettings.teams[i].blue >= 400):
                teamString += "\"0x000000\"" + "}" #black text
            else:
                teamString += "\"0xFFFFFF\"" + "}"  #white text
            self.networkManager.mqtt_publish_noLimit(teamTopic, teamString, True, log=False)

        #if the game isn't solo, do a team position check
        if(self.gameSettings.coreSettings.friendlyFireMode != 3):
            #check for tied lead
            teamsInFirstPlaceCount = 0
            for i in range(8):
                if(teamPositions[i][1] == 1):
                    teamsInFirstPlaceCount += 1

            if(teamsInFirstPlaceCount == 1):
                for i in range(8):
                    if(teamPositions[i][1] == 1):
                        if(i != self.oldTeamLeader):
                            self.writeToScoreboardLog(self.gameSettings.teams[i].name + " has taken the lead!")
                            self.oldTeamLeader = i
                            self.backend_print("LEAD CHANGED: " + str(i))
                            break


    def writeToScoreboardLog(self, text):       #untested
        if (self.gameState == 3):
            timeRemaining = int((self.gameSettings.coreSettings.time * 60) - (self.getElapsedTime() / 1000))
        else:
            timeRemaining = int(self.gameSettings.coreSettings.time * 60)
        timeMins = int(timeRemaining / 60)
        minsStr = ""
        if(timeMins < 10):
            minsStr += "0"
        minsStr += str(timeMins)

        timeSecs = int(timeRemaining % 60)
        secsStr = ""
        if(timeSecs < 10):
            secsStr += "0"
        secsStr += str(timeSecs)
        timeStr = minsStr + ":" + secsStr
        string = "[" + timeStr + "] " + text
        payloadString = "{\"newfeed\":\"" + string + "\"}"
        self.networkManager.mqtt_publish("QNET/SCOREBOARD/LIVEFEED", payloadString)

    def clearScoreboardLog(self):
        self.networkManager.mqtt_publish_noLimit("QNET/SCOREBOARD/CLEARFEED", "CLEAR")
        self.backend_print("Clearing scoreboard log feed")


    """
    GAME SPECIFIC FUNCTIONS
    """
    def flag_makeFlagAvailableAfterTime(self, time, team):
        Timer(time, self.flag_makeFlagAvailable, [team]).start()

    def flag_makeFlagAvailable(self, team):
        self.flag_available[team] = True
        self.backend_print("Team " + str(team) + "'s flag is now available")
        self.flag_sendFlagUpdate()

    def flag_sendFlagUpdate(self, capturedPlayer = -1, capturedTeam = 0):
        self.flag_flagCappedBy = [-1 for i in range(8)]
        self.flag_flagCappedBy[capturedTeam] = capturedPlayer
        message = EVENT_CTF(self.flag_flagCarriers, self.flag_flagCappedBy, self.flag_available)
        self.networkManager.sendMessage(message, True)

    def flag_sendStartupStates(self):
        if(self.gameSettings.ctfSettings.gameMode == 1):    #one flag
            self.flag_available = [0 for i in range(8)]
            self.flag_available[self.gameSettings.ctfSettings.defendingTeam] = 1
        else:
            self.flag_available = [1 for i in range(8)]
        message = EVENT_CTF(self.flag_flagCarriers, self.flag_flagCappedBy, self.flag_available)
        self.networkManager.sendMessage(message, True)