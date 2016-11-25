from tornado.testing import gen_test,AsyncTestCase
from tornado.httpclient import AsyncHTTPClient
import unittest

class MyAsyncTest(AsyncTestCase):
    @gen_test#测试类里的所有方法都要加上这个测试装饰器
    def test_xx(self):#以test_开头的方法都会被执行，
        client = AsyncHTTPClient(self.io_loop)
        path = 'http://localhost:8000/getuser?id=1'
        responses = yield [client.fetch(path,method='GET') for _ in range(10)]
        for response in responses:
            print(response.body)

if __name__ == '__main__':
    #每次测试整体的用时不能超过 5 秒，超则报错。
    unittest.main()