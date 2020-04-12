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
from server.config import *
from server.messages import *

class ServerProtocol:
    """
    """
    def __init__(self):
        pass

    def connection_made(self, transport):
        """
        This call back function is called when a connection is made.
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
            msg = json.loads(data.decode())
            if type(msg) is not list:
                raise Exception('invlid data (not a list)')
            client_ip, client_port = addr[0], addr[1]
            reply = handle_message(client_ip, client_port, msg)
            if reply:
                for item in reply:
                    ip,port,reply_msg = item[0],item[1],item[2]
                self.transport.sendto(reply_msg.encode(),(ip,port))
        except Exception as ex:
            exception(f'Exception[datagram_received] - {ex}')

    def connection_lost(ex):
        """
        This call back function is called when the connection is lost or closed.
        The argument is either an exception object or None. The latter means a
        regular EOF is received, or the connection was aborted or closed by
        this side of the connection.
        """
        if ex is not None:
            error(f'Exception[connection_lost] - {ex}')

    def error_received(ex):
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
    """
    debug(f'***** Starting UDP server *****')
    # Get a reference to the event loop as we are using low-level APIs.
    loop = asyncio.get_running_loop()
    # One protocol instance will be created to serve all client requests.
    transport, protocol = await loop.create_datagram_endpoint(
                                    lambda: ServerProtocol(),
                                    local_addr=(BINDING_IP, BINDING_PORT))
    try:
        while RUN_SERVER:
            await asyncio.sleep(3600) # value in seconds
    finally:
        transport.close()

def start_udp_server():
    """
    This is the entry point of the UDP server loop.
    """
    asyncio.run(main_loop())
