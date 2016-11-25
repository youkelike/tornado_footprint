import tornado.ioloop
import tornado.stack_context
import functools

ioloop = tornado.ioloop.IOLoop.instance()
times = 0

GLOBAL_WRAPPERS = {}
def callback():
    print('run callback')
    raise ValueError('except in callback')

def wrapper1(func):
    try:
        func()
    except Exception as e:
        print('wrapper1 exception: %s' % e)

def wrapper2(func):
    try:
        func()
    except Exception as e:
        print('wrapper2 exception: %s' % e)

def async_task():
    global times
    times += 1
    print('run async task %s' % times )
    ioloop.add_callback(callback=functools.partial(GLOBAL_WRAPPERS['context'],callback))

if __name__ == '__main__':
    '''通过一个全局变量来定义不同的执行环境，不同环境有不同的异常捕获等逻辑，
    让主函数async_task在不同的环境中运行'''
    GLOBAL_WRAPPERS['context'] = wrapper1
    wrapper1(async_task)

    GLOBAL_WRAPPERS['context'] = wrapper2
    wrapper2(async_task)


    ioloop.start()