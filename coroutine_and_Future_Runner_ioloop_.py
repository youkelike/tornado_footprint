import tornado.ioloop
from tornado.gen import coroutine
from tornado.concurrent import Future

# coroutine内部会执行的操作：
#   调用传入的async_sum，获得返回的生成器对象<gen>
#   执行一次<gen>，进入async_sum代码内部，遇到yield后获得返回的future对象<fu>
#   执行Runner(<gen>，<在coroutine里新建的TracebackFuture对象>，<fu>)
#
#   Runner内部：
#       给一个匿名方法<lambda f: Runner.run()>加上ioloop的stack_context
#       ，接着包装成另一个匿名函数
#           <lambda future: ioloop.add_callback(<上面的匿名方法>,future)>
#       ，然后放到<fu>的回调列表
#       。【当达到<fu>的回调执行条件后】，它的执行结果就是把上面第一个匿名方法添加到了ioloop的回调列表
#       ，进入ioloop的下一次循环后，就会执行Runner.run()
#       ，Runner.run()内部代码会执行<fu>的send方法，从而执行流程重新回到<fu>内部

@coroutine
def async_sum(a,b):
    print('begin calculate:sum %s+%s' % (a,b))
    future = Future()# 不需要传任何参数,这就是上面指的<fu>

    # 某个耗时的任务
    def callback(a,b):
        print('calculating the sum of %s+%s' % (a,b))
        future.set_result(a+b)# 【设置<fu>满足回调执行条件，并把耗时的异步任务结果传递给<fu>】

    # 把耗时的任务异步执行，放到ioloop的回调队列里
    tornado.ioloop.IOLoop.instance().add_callback(callback,a,b)

    # 在离开时把<fu>返回给调用环境，下次进入时获得异步耗时任务的返回结果
    result = yield future

    print('after yielded')
    print('the %s+%s=%s' % (a,b,result))

def main():
    async_sum(2,3)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()