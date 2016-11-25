import socket
from time import time

sock = socket.socket()
sock.connect(('localhost',8080))
t0 = time()
for _ in range(1000):
    sock.send(bytes('test msg',encoding='utf-8'))
    sock.recv(99)
print('time cost',time()-t0)
sock.close()