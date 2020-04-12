__all__ = ['handle_message']

import json
from server.data import data
from server.serverlog import debug,error
from server.config import messageTypes as mt
from server.config import udpStatus as us

def handle_message(ip,port,msg):
    """
    """
    debug(f'[{ip},{port}] {msg}')
    try:
        msg_type = msg.pop(0)
        if (msg_type == mt.ClientToServer_INIT_LOCATION):
            return handleClientToServerInitLocation(ip,port,msg)
        elif (msg_type == mt.ClientToServer_INIT_CLIENT_ACK):
            return handleClientToServerInitClientAck(ip,port,msg)
        elif (msg_type == mt.ClientToServer_UPDATE_LOCATION):
            return handleClientToServerUpdateLocation(ip,port,msg)
        elif (msg_type == mt.ServerToClient_INIT_LOCATION_ACK
           or msg_type == mt.ServerToClient_NEW_CLIENT_ADDED
           or msg_type == mt.ServerToClient_UPDATE_LOCATION_ACK
           or msg_type == mt.ClientToClient_UPDATE_LOCATION
           or msg_type == mt.ClientToClient_UPDATE_LOCATION_ACK):
            raise Exception(f'logic issue detected: message-type{msg_type}\
                                 should not reach to server')
        else:
            raise Exception(f'invalid message type{msg_type}')
    except Exception as ex:
        error(f'Exception[handle_message] - {ex}')
        return None

def handleClientToServerInitLocation(ip,port,msg):
    """
    Incoming: ClientToServer_INIT_LOCATION ( 1 )
    Outgoing: ServerToClient_INIT_LOCATION_ACK ( 2 )
              ServerToClient_NEW_CLIENT_ADDED ( 4 )
    """
    ctype,cid,lat,lon,update = msg[0],msg[1],msg[2],msg[3],msg[4]
    data.insert(ctype,cid,lat,lon,update,us.UDP_UNKNOWN,ip,port)
    search_result = data.search_nearby(cid,lat,lon)
    return create_msg_ServerToClientInitLocationAck(ip,port,search_result) + \
                create_msg_ServerToClientNewClientAdded(ip,port,msg,search_result)

def handleClientToServerInitClientAck(ip,port,msg):
    """
    Incoming: ClientToServer_INIT_CLIENT_ACK ( 3 )
    Outgoing: NA
    """
    ctype,cid,lat,lon,update = msg[0],msg[1],msg[2],msg[3],msg[4]
    data.insert(ctype,cid,lat,lon,update,us.UDP_UNKNOWN,ip,port)
    return None

def handleClientToServerUpdateLocation(ip,port,msg):
    """
    Incoming: ClientToServer_UPDATE_LOCATION ( 5 )
    Outgoing: ServerToClient_UPDATE_LOCATION_ACK ( 6 )
    """
    ctype,cid,lat,lon,update = msg[0],msg[1],msg[2],msg[3],msg[4]
    data.insert(ctype,cid,lat,lon,update,us.UDP_UNKNOWN,ip,port)
    search_result = data.search_nearby(cid,lat,lon)
    return create_msg_ServerToClientUpdateLocationAck(ip,port,search_result)

def create_msg_ServerToClientInitLocationAck(ip,port,search_result):
    """
    create message for ServerToClient_INIT_LOCATION_ACK ( 2 )
    """
    send_list = [mt.ServerToClient_INIT_LOCATION_ACK,len(search_result)]
    for item in search_result:
        send_list += item
    return [(ip,port,json.dumps(send_list))]

def create_msg_ServerToClientNewClientAdded(ip,port,msg,search_result):
    """
    create message for ServerToClient_NEW_CLIENT_ADDED ( 4 )
    """
    ctype,cid,lat,lon,update = msg[0],msg[1],msg[2],msg[3],msg[4]
    msg_to_send = json.dumps([mt.ServerToClient_NEW_CLIENT_ADDED,ctype,\
                                cid,lat,lon,update,us.UDP_UNKNOWN,ip,port])
    udp_msgs = []
    for item in search_result:
        udp_msgs.append((item[6],item[7],msg_to_send))
    return udp_msgs

def create_msg_ServerToClientUpdateLocationAck(ip,port,search_result):
    """
    create message for ServerToClient_UPDATE_LOCATION_ACK ( 6 )
    """
    send_list = [mt.ServerToClient_UPDATE_LOCATION_ACK,len(search_result)]
    for item in search_result:
        send_list += item
    return [(ip,port,json.dumps(send_list))]

