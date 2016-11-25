import socket
from time import time
from tornado import ioloop

loop = ioloop.IOLoop.current()
socks = [socket.socket() for _ in range(50)]#创建50个socket对象
[sock.connect(('localhost',8080)) for sock in socks]#并全部连接到服务器
sockD = {sock.fileno(): sock for sock in socks}#为socket建立文件描述符索引
t0 = time()
n = 0

'''
def onEvent(fd,event):
    if event == loop.WRITE:
        loop.update_handler(fd,loop.READ)#发送完消息后，就是等待接收消息了，将注册等待的事件改成READ
    elif event == loop.READ:
        sock = sockD[fd]
        sock.recv(99)
        global n
        n += 1
        if n > 1000:
            print('time cost:',time()-t0)
            sock.close()
            loop.remove_handler(fd)#取消事件注册
            loop.stop()
            return
        loop.update_handler(fd,loop.WRITE)
        sock.send(b'test message')

for fd,sock in sockD.items():
    loop.add_handler(fd,onEvent,loop.WRITE)#对socket对象注册一个WRITE事件的回调函数
    sock.send(b'test message')#发送这条消息后ioloop马上会执行上面注册的回调函数,并传递文件描述符和触发回调的事件
loop.start()
'''

#上述代码在WRITE事件的回调里没有实质性的操作，也可以只注册READ事件
def onEvent(fd,event):
    if event == loop.READ:
        sock = sockD[fd]
        sock.recv(99)
        global n
        n += 1
        if n > 1000:
            print('time cost:',time()-t0)
            sock.close()
            loop.remove_handler(fd)
            loop.stop()
            return
        sock.send(b'test message')

for fd,sock in sockD.items():
    loop.add_handler(fd,onEvent,loop.READ)
    sock.send(b'test message')
loop.start()