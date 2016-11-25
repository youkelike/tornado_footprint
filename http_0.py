from tornado.ioloop import IOLoop
from tornado import web,gen

class ExampleHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        delay = self.get_argument('delay',5)
        yield gen.sleep(int(delay))# gen.sleep只是为了模拟异步等待
        self.write('gameover')
        self.finish()

#autoreload表示修改代码后会自动重新运行
#debug表示打印错误信息到屏幕
#cookie_secret
#static_path
#static_url_prefix
#xsrf_cookies
application = web.Application([
    (r'/exmaple',ExampleHandler),
],autoreload=True)

#以单进程方式运行
application.listen(8000)#监听端口
IOLoop.current().start()#启动消息循环

'''
#以多进程方式运行
from tornado.httpserver import HTTPServer
server = HTTPServer(application)
server.bind(8000)
server.start(4)#同时启动4个进程
'''