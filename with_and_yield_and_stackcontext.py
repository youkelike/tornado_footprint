import tornado
import tornado.ioloop
import contextlib

ioloop = tornado.ioloop.IOLoop.instance()

# 第一种写法：自己实现上下文管理协议，并在__exit__方法中处理异常
class Contextor(object):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if all([exc_type, exc_val, exc_tb]):
            print('handle except')
            print('exception %s' % exc_val)
        return True

# 第二种写法：使用内置装饰器实现上下文管理协议，用yield的特点处理异常
# @contextlib.contextmanager
# def Contextor():
#     try:
#         yield
#     except Exception as e:
#         print('handle except')
#         print('exception %s' % e)
#     finally:
#         print('release')

def call_back():
    print('run call_back')
    raise ValueError('except in call_back')

def async_task():
    print('run async task')
    ioloop.add_callback(callback=call_back)

def main():
    with tornado.stack_context.StackContext(Contextor):
        async_task()
    print('end')

if __name__ == '__main__':
    main()
    ioloop.start()