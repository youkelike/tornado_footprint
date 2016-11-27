
#
class Configurable(object):
    def __init__(self):
        print('configurable init')

    def __new__(cls, *args, **kwargs):
        print('configurable new')
        print(cls)
        # 最后一个括号里参数数量和父类中new方法的参数数量一样,至少一个
        # 。这里父类是object,只用一个参数，参数是哪个类就返回那个类的对象(一定要return!)
        # ，后面是在实例化EPollIOLoop，所以这里的cls是EPollIOLoop
        # ，cls和最后一个括号中的第一个参数一致时，才会接着调用init方法
        # return super(Configurable, cls).__new__(cls)
        return super(Configurable, cls).__new__(PollIOLoop)

class PollIOLoop(Configurable):
    @classmethod
    def print_cls(cls):
        print('pollioloop method print_cls,', cls)

    def retu_cls(self):
        return PollIOLoop

class EPollIOLoop(PollIOLoop):
    def child(self):
        print('epollioloop')

if __name__ == '__main__':
    # 实例化时第一个调用的是new方法，自己没有定义这个方法就会去父类中找
    e = EPollIOLoop()
    print(e)