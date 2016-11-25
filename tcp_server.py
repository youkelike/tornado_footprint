from tornado import ioloop,gen,iostream
from tornado.tcpserver import TCPServer

class MyTcpServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):#客户端连接进来后会创建一个iostream,然后调用这个方法，传入iostream和client的地址
        try:
            while True:
                msg = yield stream.read_bytes(20,partial=True)#接受数据需要异步
                print(msg,'from',address)
                yield gen.sleep(0.005)
                yield stream.write(msg[::-1])#发送数据也要异步
                if msg == 'over':
                    stream.close()#直接断开就可以了
        except iostream.StreamClosedError as e:
            pass

if __name__ == '__main__':
    server = MyTcpServer()#1.创建一个继承TCPServer的实例
    server.listen(8080)#2.监听端口
    server.start()#3.启动服务器
    ioloop.IOLoop().current().start()#4.启动消息循环