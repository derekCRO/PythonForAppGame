import re
from Backend.Network.Message_Classes.Base_Classes import *

class REG_REQ(IncomingMessage):
    def __init__(self, message):
        self.type = "REG_REQ"
        self.topicString = "QNET/REG/REQ"
        self.messageString = message
        self.senderMAC = self.getMAC()

        payload = self.getPayload()
        self.serialNum = int(payload[0])
        self.deviceType = int(payload[1])
        if(len(payload) > 2):
            self.firmwareVersion = payload[2]
        else:
            self.firmwareVersion = "Unknown"

class QDEBUG(IncomingMessage):
    def __init__(self, message):
        self.type = "QDEBUG"
        self.topicString = "QDEBUG"
        self.messageString = message
        self.senderMAC = self.getMAC()

class HIT(IncomingMessage):
    def __init__(self, topic, message):
        self.type = "HIT"
        self.topicString = topic
        self.messageString = message
        self.senderMAC = self.getMAC()

        payload = self.getPayload()
        self.targetID = int(payload[0])
        self.weaponID = int(payload[1])
        self.hitLocation = int(payload[2])
        self.targetHealth = int(payload[3])
        self.targetShield = int(payload[4])
        if(len(payload) >= 6):
            self.flags = int(payload[5])
        else:
            self.flags = -1
        #get the first number from the topic string. this could break easily...
        self.shooterID = [int(s) for s in self.topicString.split('/') if s.isdigit()][0]

class STATUS(IncomingMessage):
    def __init__(self, topic, message):
        self.type = "STATUS"
        self.topicString = topic
        self.messageString = message
        self.senderMAC = self.getMAC()

        payload = self.getPayload()
        self.battVol = float(payload[0])
        self.charging = True if int(payload[1]) == 1 else False
        self.gameID = payload[2]
        #get the first number from the topic string. this could break easily...
        self.networkID = [int(s) for s in self.topicString.split('/') if s.isdigit()][0]

        self.back = 0
        self.fr = 0
        self.fl = 0
        self.sr = 0
        self.sl = 0

        if(len(payload) >= 8):
            self.back = int(payload[3])
            self.fr = int(payload[4])
            self.fl = int(payload[5])
            self.sr = int(payload[6])
            self.sl = int(payload[7])

class ACK(IncomingMessage):
    def __init__(self, topic, message):
        self.type = "ACK"
        self.topicString = topic
        self.messageString = message
        self.senderMAC = self.getMAC()