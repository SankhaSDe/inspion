import sys
sys.path.extend(['.','../','../../'])

import socket
import json
import logging
import pytest
from server.config import MessageTypes as mt, ClientTypes as ct, UdpStatus as us

SERVER_UDP_IP = "127.0.0.1"
SERVER_UDP_PORT = 9999

LOCAL_UDP_IP = "127.0.0.1"
LOCAL_UDP_PORT = 10001

payload_01 = {'mt': mt.ClientToServer_INIT_CLIENT,
              'msg': [1, 1234567890, 185185133, 185185133, '0.0.0.0', 0, 1234567890, 765430]}
payload_02 = {'mt': mt.ClientToServer_INIT_CLIENT_DONE,
              'msg': [1, 1234567890, 185185133, 185185133, '0.0.0.0', 0, 1234567890, 765430]}
payload_03 = {'mt': mt.ClientToServer_UPDATE_LOCATION,
              'msg': [1, 1234567890, 185185133, 185185133, '0.0.0.0', 0, 1234567890, 765430]}

@pytest.fixture
def sock():
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((LOCAL_UDP_IP, LOCAL_UDP_PORT))
    return sock


def test_send_first_message(sock):
    payload = json.dumps(payload_01)
    sock.sendto(payload.encode(), (SERVER_UDP_IP, SERVER_UDP_PORT))
    sock.settimeout(5)
    data, address = sock.recvfrom(4096)
    data_recvd = json.loads(data.decode())
    print('Data received:', data_recvd)
    assert data_recvd["mt"] == mt.ServerToClient_INIT_CLIENT_ACK
    assert payload_01["msg"][1] == data_recvd["msg"][0][1]
    payload = json.dumps(payload_02)
    sock.sendto(payload.encode(), (SERVER_UDP_IP, SERVER_UDP_PORT))


def test_send_second_message(sock):
    payload = json.dumps(payload_03)
    sock.sendto(payload.encode(), (SERVER_UDP_IP, SERVER_UDP_PORT))
    sock.settimeout(5)
    data, address = sock.recvfrom(4096)
    data_recvd = json.loads(data.decode())
    print('Data received:', data_recvd)
    assert data_recvd["mt"] == mt.ServerToClient_UPDATE_LOCATION_ACK
    assert payload_01["msg"][1] == data_recvd["msg"][0][1]

