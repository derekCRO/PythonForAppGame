import paho.mqtt.client as mqtt_client
import time
import socket
import logging
from logging import handlers
import os


from .Class_Device import *
#from .MQTT_Functions import *
from .Message_Handlers import *
from .Message_Classes.Outgoing_Messages import *
from .Score_Recording import *

if not os.path.exists('LOGS/MQTT'):
    os.makedirs('LOGS/MQTT')

logger = logging.getLogger('logger')
mqttLogger = logging.getLogger('mqttLogger')
#mqttLogger_handler = logging.handlers.RotatingFileHandler('LOGS/MQTT/mqtt_logging.log')
#fileHandler = logging.handlers.TimedRotatingFileHandler('LOGS/LAUNCHER/launcher_logging.log', when='midnight')
mqttLogger_handler = logging.handlers.TimedRotatingFileHandler('LOGS/MQTT/mqtt_logging.log', when='midnight')
mqttLogger_formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
mqttLogger_handler.setFormatter(mqttLogger_formatter)
mqttLogger.addHandler(mqttLogger_handler)
mqttLogger.setLevel(logging.INFO)


class Network_Manager():
    def __init__(self):
        self.devices = [Device(i) for i in range(255)]
        self.networkLog = []
        self.outgoingMessageQueue = []
        self.scores = Score_Recorder()

        self.mqtt = mqtt_client.Client()
        self.mqttLog = []
        self.mqttMessageQueue = []
        self.mqttConnected = False
        self.subscriptionList = []

        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_disconnect = self.on_disconnect
        self.mqtt.on_message = self.on_message
        self.mqtt.on_publish = self.on_publish
        self.mqtt.on_subscribe = self.on_subscribe
        self.mqtt.on_unsubscribe = self.on_unsubscribe

        self.mqtt.max_inflight_messages_set(128)

        self.subscriptionList.append("QDEBUG")
        self.subscriptionList.append("QNET/REG/REQ")
        for i in range(96):
            self.subscriptionList.append("QNET/HITS/#")
            self.subscriptionList.append("QNET/STATUS/#")

    def initialise(self, ip):
        self.broker_ip = ip
        self.mqtt.loop_start()
        self.mqtt_connect()

    def setAdvancedConfig(self, holsterCharging, ignoreBatteryState, phaserOnlyLowVoltage, phaserLowVoltage, phaserFirmware):
        self.config_holsterCharging = holsterCharging
        self.config_ignoreBatteryState = ignoreBatteryState
        self.config_phaserOnlyLowVoltage = phaserOnlyLowVoltage
        self.config_phaserLowVoltage = phaserLowVoltage
        self.config_phaserFirmware = phaserFirmware

    def assignDevice(self, id, name, type, serial, mac):
        self.devices[id].assignDevice(type, mac, serial, name)

    def mqtt_print(self, text):
        string = "[" + time.strftime("%H:%M:%S") + "][MQTT] " + text
        #print(string)
        self.mqttLog.append(string)
        logger.info(text)

    def getDeviceNamesList(self):
        return [Device.name for Device in self.devices]

    def on_connect(self, client, userdata, flags, rc):
        if(rc == 0):
            self.mqttConnected = True
            self.mqtt_print("Connected to broker. Sent SYS_START.")
            for i in range(len(self.subscriptionList)):
                self.mqtt.subscribe(self.subscriptionList[i], 1)
            sysStart = SYSTEM_STATE(1)
            self.mqtt_publish(sysStart.topicString, sysStart.messageString)
        else:
            self.mqttConnected = False
            self.mqtt_print("Failed connection")

    def on_disconnect(self, client, userdata, rc):
        self.mqttConnected = False
        self.mqtt_print("Disconnected from broker")

    def on_message(self, client, userdata, message):
        mqttLogger.info(
            "Received - Len: " + str(len(message.payload.decode())) + ". Topic: \"" + message.topic + "\". Payload: \"" + message.payload.decode() + "\".")
        handleMQTTMessage(message)

    def on_publish(self, client, userdata, mid):
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        pass

    def on_unsubscribe(self, client, userdata, mid):
        pass

    def loop(self):
        pass

    def mqtt_connect(self):
        try:
            self.mqtt.connect(self.broker_ip, 1883, 60)
        except socket.error as e:
            self.mqtt_print("Couldn't connect to broker.")
            self.mqttConnected = False

    def mqtt_publish(self, topic, payload, retain = False, log=True):
        if(len(payload) > 99):
            self.mqtt_print("ERROR- Payload Too Long. Length" + str(len(payload)) + ". Topic: \"" + topic + "\", Payload: \"" + payload + "\"")
            if(log == True):
                mqttLogger.info("Failed to send - Len: " + str(len(payload)) + ". Topic: \"" + topic + "\". Payload: \"" + payload + "\". Retain: " + str(retain))
        else:
            self.mqtt.publish(topic, payload, 1, retain)
            if (log == True):
                mqttLogger.info("Sent - Len: " + str(len(payload)) + ". Topic: \"" + topic + "\". Payload: \"" + payload + "\". Retain: " + str(retain))

    def mqtt_publish_noLimit(self, topic, payload, retain = False, log=True):
        self.mqtt.publish(topic, payload, 1, retain)
        if(log == True):
            mqttLogger.info("Sent - Len: " + str(len(payload)) + ". Topic: \"" + topic + "\". Payload: \"" + payload + "\". Retain: " + str(retain))

    def getAvailablePhasersList(self, forceForDebug = False):
        list = []
        for i in range(64):
            if(forceForDebug):
                list.append(i)
                continue
            if(self.devices[i].isOnline() != True):
                continue
            if(self.devices[i].charging and self.config_holsterCharging == False):
                continue
            if(self.config_phaserFirmware != "" and self.config_phaserFirmware != self.devices[i].firmwareVersion):
                continue
            if(self.config_ignoreBatteryState != True and ((self.devices[i].type == 1 and self.devices[i].batteryVoltage <= float(self.config_phaserLowVoltage)) or (self.devices[i].type == 3 and self.devices[i].batteryVoltage <= float(self.config_phaserOnlyLowVoltage)))):
                continue
            list.append(i)
            #if(self.devices[i].isOnline() and not self.devices[i].charging and (((self.devices[i].type == 1) and (self.devices[i].batteryVoltage > 9.5)) or ((self.devices[i].type == 3)) and (self.devices[i].batteryVoltage > 8.5)) or (forceForDebug == True)):
                #list.append(i)
        return list

    def network_print(self, text):
        string = "[" + time.strftime("%H:%M:%S") + "][NETWORK] " + text
        #print(string)
        self.networkLog.append(string)
        logger.info(text)

    def sendMessage(self, message, retain=False):
        self.mqtt_publish(message.topicString, message.messageString, retain)

    def handleRegRequest(self, message):
        id = -1
        newDevice = True
        # look for an existing network ID
        for i in range(255):
            if (self.devices[i].serialNum == message.serialNum):
                id = i
                newDevice = False
        # assign a new netID
        if (id == -1):
            if (message.deviceType == 1 or message.deviceType == 3):  # phaserwithpack or phaser only
                for i in range(64):
                    if (self.devices[i].inUse == False):
                        id = i
                        break
            elif (message.deviceType == 2):  # network unit
                for i in range(64, 96):
                    if (self.devices[i].inUse == False):
                        id = i
                        break
            else:  # unknown
                self.network_print("Couldn't assign netID - Unknown device type. Serial: " + message.serialNum)
                return -1
            if (id == -1):
                self.network_print("Couldn't assign netID - Too many devices assigned. Serial: " + message.serialNum)
                return -1
        # assign the device and reply
        self.devices[id].assignDevice(message.deviceType, message.senderMAC, message.serialNum)
        self.devices[id].setDeviceFirmware(message.firmwareVersion)
        response = REG_RESP(message.serialNum, id, self.devices[id].name)
        self.sendMessage(response)

        printString = "Registered "
        if (newDevice):
            printString += ("new ")
        printString += "device " + str(message.serialNum) + ", " + hex(message.senderMAC) + " to ID " + str(id) + " with name " + self.devices[id].name
        self.network_print(printString)

        return id

    def getConnected(self):
        return self.mqttConnected