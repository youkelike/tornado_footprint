from tornado import web,gen
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient

url = 'http://view.news.qq.com/original/intouchtoday/n3715.html'
class GetPageHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        client = AsyncHTTPClient()
        response = yield client.fetch(url,method='GET')
        self.write(response.body.decode('gbk'))
        self.finish()

application = web.Application([
    (r'/getpage',GetPageHandler)
],autoreload=True)

application.listen(8001)
IOLoop.current().start()