import tornado.web
import tornado.ioloop
import os,sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# print(sys.path)
from tornado_form import *

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('form.html')

    def post(self, *args, **kwargs):
        # for i in dir(self.request):
        #     print(i)
        # print(self.request.arguments)
        # print(self.request.files)
        # print(self.request.query)

        # 处理批量提交
        # list_form = ListForm(MainForm)
        # list_form.validate(self)
        # print(list_form.valid_status)
        # print(list_form.valid_dic)
        # print(list_form.error_dic)

        # 处理单个提交
        obj = MainForm()
        obj.validate(self)
        print(obj.valid_status)
        print(obj.value_dic)
        print(obj.error_dic)

        self.write('ok')

settings = {
    'template_path':'template',
}

application = tornado.web.Application([
    (r'/index',MainHandler),
],**settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()