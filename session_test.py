import tornado.ioloop
import tornado.web
import os,time
from hashlib import sha1

session_container = {}#全局字典用于保存每个登录用户的session
create_session_id = lambda: sha1(bytes('%s%s' % (os.urandom(6),time.time()),encoding='utf-8')).hexdigest()

class Session(object):
    cookie_name = '__sessionID__'#客户端用于保存session_id的cookie字段名
    def __init__(self,request):#这个类与下面的XXXHandler类没有继承关系，需要传入它们的实例作为参数
        session_id = request.get_cookie(Session.cookie_name)
        if session_id:
            self._id = session_id
        else:
            self._id = create_session_id()
        request.set_cookie(Session.cookie_name,self._id)#无论之前有没有cookie,都需要重新设置

    def __setitem__(self, key, value):
        if self._id in session_container:
            session_container[self._id][key] = value
        else:
            session_container[self._id] = {key:value}

    def __getitem__(self, key):
        return session_container[self._id].get(key)

    def __delitem__(self, key):
        del session_container[self._id][key]

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        # 这是个钩子方法，在所有请求方法之前执行，所以这个方法中添加的对象属性所有子类中都可用
        # 在创建Session实例时传入自己，建立双向关系
        self.my_session = Session(self)

class MainHandler(BaseHandler):
    def get(self):
        print(self.my_session['user'])
        print(self.my_session['pos'])
        self.write('index')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html',**{'status':''})

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username == 'zs' and password == '111':
            self.my_session['user'] = 'zs'
            self.my_session['pos'] = '113.32'
            self.redirect('/index')#内部跳转
        else:
            self.render('login.html',**{'status':'用户名或密码错误'})#参数要以命名参数的形式传入


settings = {
    'template_path': 'template',
    'login_url': '/login'
}
application = tornado.web.Application([
    (r'/index',MainHandler),
    (r'/login',LoginHandler),
],**settings)#settings参数要以命名参数的形式传入

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()