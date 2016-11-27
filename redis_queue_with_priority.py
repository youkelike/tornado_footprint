import redis,time

def handle(task):
    print(task)
    time.sleep(10)

def main():
    pool = redis.ConnectionPool(host='localhost',port=6379,db=0)
    r = redis.Redis(connection_pool=pool)
    while 1:
        # 阻塞的方式获取列表tasklist右边一个元素值，参数0表示tasklist为空就一直阻塞等待
        # ，可以在redis客户端模拟一个生产者：lpush tasklist 'im task 01'
        # 实现队列优先级的方式很简单（高优先级的塞到队列前，低优先级塞到队列后）：
        #       如果消费者用brpop取，生产者遇到高优先级就用rpush
        #       ，低优先级用lpush，消费者用blpop则生产者反着用。
        # 但它有一个缺点就是，不能保证高优先级之间的FIFO顺序
        #result = r.brpop('tasklist',0)

        # 更为完善的优先及队列实现方式：
        # 设置两个队列，一个放高优先级任务，一个放低优先级任务
        # ，然后改变消费者的消费方式如下，会阻塞的去两个队列里取，第一个没有再取第二个
        result = r.brpop(['high_task_queue','low_task_queue'],0)
        handle(result[1])

if __name__ == '__main__':
    main()