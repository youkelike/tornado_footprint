from contextlib import contextmanager

@contextmanager#这个装饰器会给下面的函数添加两个方法__enter__和__exit__，两个方法里的主要代码都是next语句
def make_context():
    print('enter context')
    try:
        yield 1
        print('between two yield')
    except Exception as e:
        print('here is exception')

# a = make_context()#调用带有yield的函数只会返回一个生成器，并不会执行函数中的代码
# next(a)或者a.send()时才会执行函数内部代码

# with语句只能作用于有__enter__和__exit__两个方法的对象，
# 内部逻辑是在执行with冒号后的代码前调用对象的__enter__方法，并把__enter__的执行返回值赋给as后面的变量
# ，在执行完with子代码块后，调用对象的__exit__方法，如果子代码块中发生异常，异常会把异常参数（type,value,traceback）传入__exit__方法中
# ，如果__exit__返回False或None，异常会被主动raise,如果返回True什么都不会发生
with make_context() as value:
    print(value)
    raise Exception