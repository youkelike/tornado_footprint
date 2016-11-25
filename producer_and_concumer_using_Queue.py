import threading,random,time,queue
que = queue.Queue(10)#使用内置模块做全局队列

class Producer(threading.Thread):
    def __init__(self,name):
        super(Producer,self).__init__()
        self.name = name

    def run(self):
        while True:#不需要手动获取和释放锁，由队列内部逻辑维护
            elem = random.randrange(100)
            que.put(elem)
            print('%s produce elem %s, now size is %s' % (self.name, elem, que.qsize()))
            time.sleep(random.random())

class Consumer(threading.Thread):
    def __init__(self,name):
        super(Consumer,self).__init__()
        self.name = name

    def run(self):
        while True:
            elem = que.get()#从队列中获取数据的时候，如果队列为空，当前线程就会发生阻塞，释放锁，直到队列被其它线程写入数据
            que.task_done()#类似与Condition的notify()方法
            print('\033[31;1m%s consume elem %s, now size is %s\033[0m' % (self.name, elem, que.qsize()))
            time.sleep(random.random())

if __name__ == '__main__':
    for i in range(3):
        Producer(i).start()
    for i in range(3):
        Consumer(i).start()