from tornado import ioloop,gen,iostream
from tornado.tcpclient import TCPClient

@gen.coroutine
def trans():
    stream = yield TCPClient().connect('localhost','8080')#建立连接后返回的是iostream对象
    try:
        for msg in ('hey','guys','i feel good','over'):
            yield stream.write(bytes(msg,encoding='utf-8'))
            back = yield stream.read_bytes(20,partial=True)
            print(back)
    except iostream.StreamClosedError as e:
        pass

if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(trans)#run_sync内部会先启动消息循环，执行传入的函数，最后结束消息循环