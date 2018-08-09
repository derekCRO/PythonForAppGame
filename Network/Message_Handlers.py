from .Message_Classes import *
import logging

incomingMessageQueue = []

logger = logging.getLogger('logger')

#decode the message into an appropriate MQTT message and add to queue
def handleMQTTMessage(message):
    if message.topic == "QDEBUG":
        incMessage = QDEBUG(message.payload.decode())
        incomingMessageQueue.append(incMessage)
    elif message.topic == "QNET/REG/REQ":
        incMessage = REG_REQ(message.payload.decode())
        incomingMessageQueue.append(incMessage)
    elif "HITS" in message.topic:
        incMessage = HIT(message.topic, message.payload.decode())
        incomingMessageQueue.append(incMessage)
    elif "STATUS" in message.topic:
        incMessage = STATUS(message.topic, message.payload.decode())
        incomingMessageQueue.append(incMessage)
    else:
        logger.error("MESSAGE HANDLER Couldn't decode message. Topic: \"" + message.topic + "\" : \"" + message.payload.decode() + "\"")
    pass