import os,signal
from time import sleep

def onsignal_term(a,b):
    print('收到SIGTERM信号')

signal.signal(signal.SIGTERM,onsignal_term)

while True:
    print('进程id:',os.getpid())
    sleep(10)