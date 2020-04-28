__all__ = ['SERVER_LOG_FILE_NAME','SERVER_LOG_LEVEL','BINDING_IP','BINDING_PORT','RUN_SERVER',
           'messageTypes','clientTypes','udpStatus']

import logging

SERVER_LOG_FILE_NAME = "udp_server.log"
SERVER_LOG_LEVEL = logging.DEBUG

BINDING_IP = '127.0.0.1'
BINDING_PORT = 9999

RUN_SERVER = True
DATA_EXPIRATION_TIME = 60000 # milliseconds

class MessageTypes:
    ClientToServer_INIT_CLIENT = 1
    ServerToClient_INIT_CLIENT_ACK = 2
    ClientToServer_INIT_CLIENT_DONE = 3
    ServerToClient_NEW_CLIENT_ADDED = 4
    ClientToServer_UPDATE_LOCATION = 5
    ServerToClient_UPDATE_LOCATION_ACK = 6
    ClientToClient_UPDATE_LOCATION = 7
    ClientToClient_UPDATE_LOCATION_ACK = 8

class ClientTypes:
    USER = 0
    ERICKSHAW = 1

class UdpStatus:
    UDP_ENABLED = 1
    UDP_DISABLED = 0
    UDP_UNKNOWN = -1

messageTypes = MessageTypes()
clientTypes = ClientTypes()
udpStatus = UdpStatus()
