from contextlib import contextmanager

@contextmanager
def make_context():
    print('enter')
    try:
        yield {}
    except RuntimeError as e:
        print('error',e)
    finally:
        print('exit')

# 到这里make_context引用的是被contextmanager装饰后返回的内层函数
# ，执行它<make_context()>才会在内层函数内部某各地方调用原来的make_context来得到一个生成器
# ，加上内层函数其它代码的作用，最终会返回一个被加上了上下文协议方法后的生成器
# ，其中的方法__enter__主要作用就是调用生成器的send方法，执行生成器内部代码直到遇到yield返回
# ，然后执行with体中的代码，完了后调用__exit__（主要代码也是调用生成器的send方法）再次进入生成器
print(make_context())
with make_context() as value:#
    print(value)