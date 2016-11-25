import tornado.ioloop
import tornado.stack_context
import functools

ioloop = tornado.ioloop.IOLoop.instance()
times = 0

def callback():
    print('run callback')
    raise ValueError('except in callback')

def wrapper(func):
    '''
    抽象出来的主函数和异步函数共用的异常处理
    异步函数的异常捕获代码写在主函数中是不能正常捕获的，单独在异步函数中写异常捕获也不太优雅
    '''
    try:
        func()
    except Exception as e:
        print('main exception: %s' % e)

def async_task():
    global times
    times += 1
    print('run async task %s' % times )
    # functools.partial调用的结果是产生一个偏函数
    # ioloop.add_callback中的参数callback只能接异步函数名，没有地方再给异步函数传参数，偏函数整好派上用场，
    # 原先调用wrapper方式：wrapper(func1)
    # 转为偏函数：wrapper2 = functools.partial(wrapper,func1)
    # 偏函数调用方式：wrapper2()，且与原先的调用方式效果一模一样，
    ioloop.add_callback(callback=functools.partial(wrapper,callback))

if __name__ == '__main__':
    wrapper(async_task)#把主函数也放到通用的异常捕获代码里运行，就是把不同的函数放到同一个函数代码里去调用
    ioloop.start()