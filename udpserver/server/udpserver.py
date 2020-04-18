"""
The UDP server code. Functionalities are as below:
1.
2.
3.

Reference:
https://docs.python.org/3/library/asyncio-protocol.html
Sections:
 - Datagram Protocols
 - UDP Echo Server
 - UDP Echo Client
"""

__all__ = ['start_udp_server']

import asyncio
import json
from server.serverlog import debug,error,critical,exception
from server.config import messageTypes as mt, udpStatus as us, BINDING_IP, BINDING_PORT, RUN_SERVER
from server.local_data import local_data

class ServerProtocol:
    """
    The UDP server implementation to communicate with clients
    """
    def __init__(self):
        pass

    def connection_made(self, transport):
        """
        This call back function is called when a connection is made with local port.
        The transport argument is the transport representing the connection.
        The protocol is responsible for storing the reference to its transport.
        """
        try:
            debug(f'Transport: {transport}')
            self.transport = transport
        except Exception as ex:
            exception(f'Exception[connection_made] - {ex}')

    def datagram_received(self, data, addr):
        """
        This call back function is called when a datagram is received. data is a bytes
        object containing the incoming data. addr is the address of the peer sending
        the data; the exact format depends on the transport.
        """
        try:
            client_ip, client_port, data_in = addr[0], addr[1], json.loads(data.decode())
            debug(f'Received data[datagram_received] - {data_in}')
            self.handle_message(client_ip, client_port, data_in)
            # # [2] update internal data and search neatby peer clients
            # ip_list, msg = handle_message(client_ip, client_port, data_in)
            # # [3] send acknowledgement to client
            # data_out = json.dumps({'mt': mt.ServerToClient_INIT_CLIENT_ACK, 'msg': msg})
            # self.send(data_out, client_ip, client_port)
            # # [4] send the update to other Clients
            # data_out = json.dumps({'mt': mt.ServerToClient_NEW_CLIENT_ADDED, 'msg': msg})
            # for item in ip_list:
            #     self.send(data_out, item['ip'], item['port'])
        except Exception as ex:
            exception(f'Exception[datagram_received] - {ex}')

    def handle_message(self, client_ip, client_port, data):
        try:
            msg_type = data['mt']
            msg = data['msg']

            if (msg_type == mt.ClientToServer_INIT_CLIENT):
                # [1] update internal data
                local_data.insert(ctype=msg[0], cid=msg[1], lat=msg[2], lon=msg[3],
                                    ip=client_ip, port=client_port, update=msg[6], udp=us.UDP_UNKNOWN)
                # [2] search near-by
                search_result = local_data.search(lat=msg[2],lon=msg[3])
                # [3] send reply back to client
                data_out = json.dumps({'mt': mt.ServerToClient_INIT_CLIENT_ACK, 'msg': search_result})
                self.send(ip=client_ip, port=client_port, data=data_out)
                # [4] send update to peers
                for item in search_result:
                    self.send(ip=item[4], port=item[5], data=data_out)

            elif (msg_type == mt.ClientToServer_INIT_CLIENT_DONE):
                # [1] update internal data
                local_data.insert(ctype=msg[0], cid=msg[1], lat=msg[2], lon=msg[3],
                                    ip=client_ip, port=client_port, update=msg[6], udp=us.UDP_ENABLED)

            elif (msg_type == mt.ClientToServer_UPDATE_LOCATION):
                # [1] update internal data
                local_data.insert(ctype=msg[0], cid=msg[1], lat=msg[2], lon=msg[3],
                                    ip=client_ip, port=client_port, update=msg[6], udp=us.UDP_ENABLED)
                # [2] search near-by
                search_result = local_data.search(lat=msg[2],lon=msg[3])
                # [3] send reply back to client
                data_out = json.dumps({'mt': mt.ServerToClient_INIT_CLIENT_ACK, 'msg': search_result})
                self.send(ip=client_ip, port=client_port, data=data_out)

            elif (msg_type == mt.ServerToClient_INIT_CLIENT_ACK
               or msg_type == mt.ServerToClient_NEW_CLIENT_ADDED
               or msg_type == mt.ServerToClient_UPDATE_LOCATION_ACK
               or msg_type == mt.ClientToClient_UPDATE_LOCATION
               or msg_type == mt.ClientToClient_UPDATE_LOCATION_ACK):
                    raise Exception(f'logic issue detected: message-type{msg_type}\
                                         should not reach to server')
            else:
                    raise Exception(f'invalid message type{msg_type}')
        except Exception as ex:
            exception(f'Exception[handle_message] - {ex}')

    def send(self, ip, port, data):
        try:
            self.transport.sendto(data.encode(),(ip,port))
        except Exception as ex:
            exception(f'Exception[send] - {ex}')

    def connection_lost(self, ex):
        """
        This call back function is called when the connection is lost or closed.
        The argument is either an exception object or None. The latter means a
        regular EOF is received, or the connection was aborted or closed by
        this side of the connection.
        """
        if ex is not None:
            error(f'Exception[connection_lost] - {ex}')

    def error_received(self, ex):
        """
        This call back function is called when a previous send or receive operation
        raises an OSError. ex is the OSError instance.
        This method is called in rare conditions, when the transport (e.g. UDP) detects
        that a datagram could not be delivered to its recipient. In many conditions though,
        undeliverable datagrams will be silently dropped.
        """
        if ex is not None:
            error(f'Exception[error_received] - {ex}')


async def main_loop():
    """
    This is the main thread which starts the UDP listner thread, then sleeps in background
    """
    print(f'***** Starting UDP server *****')
    debug(f'***** Starting UDP server *****')
    # Get a reference to the event loop as we are using low-level APIs.
    loop = asyncio.get_running_loop()
    # One protocol instance will be created to serve all client requests.
    transport, protocol = await loop.create_datagram_endpoint(
                                    lambda: ServerProtocol(),
                                    local_addr=(BINDING_IP, BINDING_PORT))
    try:
        while RUN_SERVER:
            local_data.clean() # wakeup and cleanup old data
            await asyncio.sleep(3600) # value in seconds
    finally:
        transport.close()

def start_udp_server():
    """
    This is the entry point of the UDP server loop.
    """
    asyncio.run(main_loop())
