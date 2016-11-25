import threading,random,time
queue = []# 需要借助一个模拟的全局队列
con = threading.Condition()

class Producer(threading.Thread):
    def __init__(self,name):
        super(Producer,self).__init__()#必须要手动调用父类的init才行
        self.name = name

    def run(self):
        while True:
            if con.acquire():#先手动尝试获取全局条件变量锁
                if len(queue)>10:
                    print('producer waiting...')
                    con.wait()#不符合条件就等待，并自动释放锁
                else:
                    elem = random.randrange(100)
                    queue.append(elem)
                    print('%s produce elem %s, now size is %s' % (self.name,elem,len(queue)))
                    time.sleep(random.random())
                    con.notify()#唤醒其它线程，但并不会自动释放锁
                    con.release()#手动释放锁

class Consumer(threading.Thread):
    def __init__(self,name):
        super(Consumer,self).__init__()
        self.name = name

    def run(self):
        while True:
            if con.acquire():
                if len(queue) < 1:
                    print('consumer waiting...')
                    con.wait()
                else:
                    elem = queue.pop()
                    print('\033[31;1m%s consume elem %s, now size is %s\033[0m' % (self.name,elem,len(queue)))
                    time.sleep(random.random())
                    con.notify()
                    con.release()

if __name__ == '__main__':
    for i in range(3):
        Producer(i).start()
    for i in range(3):
        Consumer(i).start()