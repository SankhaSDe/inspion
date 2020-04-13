import sys
sys.path.append('../')

import socket
import json
import logging
import pytest
from server.config import MessageTypes as mt, ClientTypes as ct, UdpStatus as us

SERVER_UDP_IP = "127.0.0.1"
SERVER_UDP_PORT = 9999

LOCAL_UDP_IP = "127.0.0.1"
LOCAL_UDP_PORT = 10001

payload_01 = json.dumps([1,0,111111111111,185185133,185185134,1234567891])

@pytest.fixture
def sock():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((LOCAL_UDP_IP, LOCAL_UDP_PORT))
    return sock

def test_send_first_message(sock):
    print('dummy')
    pass
