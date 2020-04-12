import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 9999
payload = json.dumps([1,0,111111111111,185185133,185185134,1234567891])

print('sending')
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, 10001))
sock.sendto(payload.encode(), (UDP_IP, UDP_PORT))
sock.settimeout(5)
data, address = sock.recvfrom(4096)
print(data.decode())