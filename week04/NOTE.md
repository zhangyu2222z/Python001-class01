### 本周主要学习内容如下：
#### scrapy并发参数优化原理，多进程，多线程相关知识

#### 1、scrapy并发参数优化以及原理：
scrapy比requests爬取数据效率快的一个原因是因为，scrapy是异步爬取，请求是并发的；可以在settings.py中进行相关设置：<br>
```python
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 设置最大并发请求
#CONCURRENT_REQUESTS = 32
# Configure a delay for requests for the same website (default: 0)
# 设置下载延迟（秒），防止爬取过快
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# 针对每个域名或者ip的最大并发请求数
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
```
scrapy底层引擎：基于Twisted的异步I/O框架<br>
简单模拟scrapy底层代码：<br>
**注：以下注释为自己理解，后面可能会更改**<br>
```python
from twisted.internet import defer
from twisted.web.client import getPage
from twisted.internet import reactor

# 页面响应调用
def response(*args, **kwargs):
    # print(args, kwargs)
    print('返回网页的内容')

# 响应后执行函数（响应事件触发回调）
def callback(*args):
    print('执行了一个回调',args)

# 预开始一个页面请求，生成并返回一个带有回调列表的deferred对象（延迟加载对象）
@defer.inlineCallbacks
def start(url):
    d = getPage(url.encode('utf-8'))
    d.addCallback(response)
    d.addCallback(callback)
    yield d

# 结束所有动作，终止反应堆循环
def stop(*args, **kwargs):
    reactor.stop()

urls = ['http://www.baidu.com','http://www.sougou.com']
# deferred延迟对象列表
li = []

for url in urls:
    ret = start(url)
    li.append(ret)
print(li)

# 加载deferred延迟对象列表
d = defer.DeferredList(li)
# 添加终止操作，无论回调列表执行完毕，亦或是发生异常，都将结束反应堆循环
d.addBoth(stop)
# 反应堆开始循环，正式开始执行发起请求-等待响应-执行回调...等动作循环
reactor.run()
```
#### 2、多进程相关知识：
##### 1）创建进程：<br>
产生新进程方式：os、multiprocessing<br>
方案1：使用os库<br>
```python
# 只支持mac或者linux系统
import os
import time

res = os.fork()
print('1111111111')
# 执行结果：
# 1111111111
# 1111111111
# # fork函数一旦运行就会生出一条新的进程，2个进程一起执行导致输出了2行

print(f'res == {res}')
# 进程的父子关系：在一个进程A中产生一个进程B，那么进程B相对进程A就是子进程，A则为父进程；
if res == 0:
    print(f'我是子进程,我的pid是:{os.getpid()}我的父进程id是:{os.getppid()}')
else:
    print(f'我是父进程,我的pid是: {os.getpid()}')

# fork()运行时，会有2个返回值，返回值为大于0时，此进程为父进程，
# 且返回的数字为子进程的PID；当返回值为0时，此进程为子进程。
# 注意：父进程结束时，子进程并不会随父进程立刻结束。同样，父进程不会等待子进程执行完。
# 注意：os.fork()无法在windows上运行。
```
方案2：使用multiprocessing形式<br>
一种是使用Process类<br>
```python
# 参数
# multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})

# - group：分组，实际上很少使用
# - target：表示调用对象，你可以传入方法的名字
# - name：别名，相当于给这个进程取一个名字
# - args：表示被调用对象的位置参数元组，比如target是函数a，
#   他有两个参数m，n，那么args就传入(m, n)即可
# - kwargs：表示调用对象的字典

from multiprocessing import Process

def f(name):
    print(f'hello {name}')

if __name__ == '__main__':
    p = Process(target=f, args=('john',))
    p.start()
    p.join()
# join([timeout])
# 如果可选参数 timeout 是 None （默认值），则该方法将阻塞，
# 直到调用 join() 方法的进程终止。如果 timeout 是一个正数，
# 它最多会阻塞 timeout 秒。
# 请注意，如果进程终止或方法超时，则该方法返回 None 。
# 检查进程的 exitcode 以确定它是否终止。
# 一个进程可以合并多次。
# 进程无法并入自身，因为这会导致死锁。
# 尝试在启动进程之前合并进程是错误的。
```
另一种是使用继承Process的类<br>
```python
# multiprocessing.Process的run()方法
import os
import time
from multiprocessing import Process

class NewProcess(Process): #继承Process类创建一个新类
    def __init__(self,num):
        self.num = num
        super().__init__()

    def run(self):  #重写Process类中的run方法.
        while True:
            print(f'我是进程 {self.num} , 我的pid是: {os.getpid()}')
            time.sleep(1)

for i in range(2):
    p = NewProcess(i)
    p.start()
# 当不给Process指定target时，会默认调用Process类里的run()方法。
# 这和指定target效果是一样的，只是将函数封装进类之后便于理解和调用。
```

##### 2）多进程调试：<br>
调试方法一：打印调试
```python
import time
from multiprocessing import Process
import os
def run():
    print("子进程开启")
    time.sleep(2)
    print("子进程结束")

if __name__ == "__main__":
    print("父进程启动")
    p = Process(target=run)
    p.start()
    p.join()  
    print("父进程结束")

```
调试方法二：根据进程内置函数、属性
```python
# 根据进程id，进程名称、父进程id等判断
from multiprocessing import Process
import os
import multiprocessing

def debug_info(title):
    print('-'*20)
    print(title)
    print('模块名称:', __name__)
    print('父进程:', os.getppid())
    print('当前进程:', os.getpid())
    print('-'*20)

def f(name):
    debug_info('function f')
    print('hello', name)

if __name__ == '__main__':
    debug_info('main')
    p = Process(target=f, args=('bob',))
    p.start()
    for p in multiprocessing.active_children():
        print(f'子进程名称: {p.name}  id: { str(p.pid) }' )
    print('进程结束')
    print(f'CPU核心数量: { str(multiprocessing.cpu_count()) }')
    p.join()
```
##### 3）进程间通信：<br>
一个进程内的变量无法与另一个进程进行共享，因此进程之间通信用到的==共享形式主要为队列，管道，共享内存，资源竞争问题靠加锁机制解决。==<br>
其中进程通信大部分时候用的主要是队列共享方式。<br>
##### 进程之间通信方案1：队列共享<br>
```python
from multiprocessing import Process, Queue
import os, time

def write(q):
    print("启动Write子进程：%s" % os.getpid())
    for i in ["A", "B", "C", "D"]:
        q.put(i)  # 写入队列
        time.sleep(1)
    print("结束Write子进程：%s" % os.getpid())

def read(q):
    print("启动Read子进程：%s" % os.getpid())
    while True:  # 阻塞，等待获取write的值
        value = q.get(True)
        print(value)
    print("结束Read子进程：%s" % os.getpid())  # 不会执行

if __name__ == "__main__":
    # 父进程创建队列，并传递给子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    # pr进程是一个死循环，无法等待其结束，只能强行结束
    # （写进程结束了，所以读进程也可以结束了）
    pr.terminate()
    print("父进程结束")
```
##### 进程之间通信方案2：管道共享<br>
```python
# 管道
# 官方文档
# Pipe() 函数返回一个由管道连接的连接对象，默认情况下是双工（双向）
from multiprocessing import Process, Pipe
def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
# 返回的两个连接对象 Pipe() 表示管道的两端。
# 每个连接对象都有 send() 和 recv() 方法（相互之间的）。
# 请注意，如果两个进程（或线程）同时尝试读取或写入管道的 同一 端，
# 则管道中的数据可能会损坏。当然，同时使用管道的不同端的进程不存在损坏的风险。
```
##### 进程之间通信方案3：内存共享<br>
```python
# 在进行并发编程时，通常最好尽量避免使用共享状态。
# 共享内存 shared memory 可以使用 Value 或 Array 将数据存储在共享内存映射中
# 这里的Array和numpy中的不同，它只能是一维的，不能是多维的。
# 同样和Value 一样，需要定义数据形式，否则会报错
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in a:
        a[i] = -a[i]

if __name__ == '__main__':
    # 下面两个num、arr定义为强类型时，就会使用内存
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])

# 将打印
# 3.1415927
# [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
# 创建 num 和 arr 时使用的 'd' 和 'i' 
# 参数是 array 模块使用的类型的 typecode ： 'd' 表示双精度浮点数， 'i' 表示有符号整数。
# 这些共享对象将是进程和线程安全的。
```
##### 利用加锁机制解决资源争抢问题：<br>
```python
# 加进程锁
# 为了解决不同进程抢共享资源的问题，我们可以用加进程锁来解决。
import multiprocessing as mp
import time

# 在job()中设置进程锁的使用，保证运行时一个进程的对锁内内容的独占
def job(v, num, l):
    l.acquire() # 锁住
    for _ in range(5):
        time.sleep(0.1) 
        v.value += num # 获取共享内存
        print(v.value, end="|")
    l.release() # 释放

def multicore():
    l = mp.Lock() # 定义一个进程锁
    v = mp.Value('i', 0) # 定义共享内存
    # 进程锁的信息传入各个进程中
    p1 = mp.Process(target=job, args=(v,1,l)) 
    p2 = mp.Process(target=job, args=(v,3,l)) 
    p1.start()
    p2.start()
    p1.join()
    p2.join()

if __name__ == '__main__':
    multicore()

# 运行一下，让我们看看是否还会出现抢占资源的情况
# 显然，进程锁保证了进程p1的完整运行，然后才进行了进程p2的运行

# 在某些特定的场景下要共享string类型，方式如下：
from ctypes import c_char_p
str_val = mp.Value(c_char_p, b"Hello World")
```
##### 4）进程池相关知识：<br>
在开发多进程程序时，一般进程数最大值为机器的cpu数，如果所有的进程都执行完毕，需要启动新的进程运行，会很不方便，这时候就用到进程池；<br>
进程池需要用到multiprocessing.pool<br>
使用进程池的一般流程：<br>
- 创建进程池，大小为逻辑CPU个数；<br>
- 创建进程，放入进程池，可以设置异步或者同步；<br>
- 确保没有进程创建后，关闭进程池；<br>
- 进程池实例调用join函数，等待所有子进程执行完毕，接着执行主进程；<br>
- 后续进程池也可以调用terminate函数，强制关闭进程池；<br>
==**特别注意：进程池实例调用join函数时，一定要放在close函数或者用terminate函数后面，否则发生死锁！**==<br>
##### 
详细进程池使用示例：<br>
```python
# Pool 类表示一个工作进程池
# 如果要启动大量的子进程，可以用进程池的方式批量创建子进程
from multiprocessing.pool import Pool
from time import sleep, time
import random
import os

def run(name):
    print("%s子进程开始，进程ID：%d" % (name, os.getpid()))
    start = time()
    sleep(random.choice([1, 2, 3, 4]))
    end = time()
    print("%s子进程结束，进程ID：%d。耗时0.2%f" % (name, os.getpid(), end-start))

if __name__ == "__main__":
    print("父进程开始")
    # 创建多个进程，表示可以同时执行的进程数量。默认大小是CPU的核心数
    p = Pool(4)
    for i in range(10):
        # 创建进程，放入进程池统一管理
        p.apply_async(run, args=(i,))
    # 如果我们用的是进程池，在调用join()之前必须要先close()，
    # 并且在close()之后不能再继续往进程池添加新的进程
    
    # 补充：创建进程池可以使用with关键字，也可以使用map，
    #       imap形式创建进程放入进程池
    # with Pool(processes=4) as pool:         # 进程池包含4个进程
    #   print(pool.map(f, range(10)))       # 输出 "[0, 1, 4,..., 81]"
    #   it = pool.imap(f, range(10))        # map输出列表，imap输出迭代器
    #   print(it)               
    #   print(next(it))                     #  "0"
    #   print(next(it))                     #  "1"
    #   print(it.next(timeout=1))           #  "4" 
    
    p.close()
    # 进程池对象调用join，会等待进程池中所有的子进程结束完毕再去结束父进程
    p.join()
    print("父进程结束。")
    p.terminate()

# close()：如果我们用的是进程池，在调用join()之前必须要先close()，
# 并且在close()之后不能再继续往进程池添加新的进程
# join()：进程池对象调用join，会等待进程池中所有的子进程结束完毕再去结束父进程
# terminate()：一旦运行到此步，不管任务是否完成，立即终止。
```
#### 3、多线程相关知识：
- 进程和线程：进程占用计算资源比较多，线程的运行都是存在于一个进程中，因此计算资源开销远比进程低很多；一个进程占用一个物理CPU，多个线程才会占用一个物理CPU<br>
- 线程阻塞和非阻塞：针对发起方角度，发起调用后，是等待(阻塞)还是进行其他操作(非阻塞)；<br>
- 同步和异步：被调用方角度，被调用后马上响应(同步)，或者完成其他操作后在响应(异步)；<br>
- 并行和并发：并发指多个线程同时访问同一个资源，并行指多个资源被同时被多个线程访问；<br>
####
##### 1）创建线程
创建多线程两种方式：函数方式和实例方式。<br>
函数方式：<br>
```python
# 这个函数名可随便定义
def run(n):
    print("current task：", n)

if __name__ == "__main__":
    t1 = threading.Thread(target=run, args=("thread 1",))
    t2 = threading.Thread(target=run, args=("thread 2",))
    t1.start()
    t2.start()
    
# 调用方
# 阻塞  得到调用结果之前，线程会被挂起
# 非阻塞 不能立即得到结果，不会阻塞线程

# 被调用方 
# 同步 得到结果之前，调用不会返回
# 异步 请求发出后，调用立即返回，没有返回结果，通过回调函数得到实际结果
```
实例方式：<br>
```python
import threading

class MyThread(threading.Thread):
    def __init__(self, n):
        super().__init__() # 重构run函数必须要写
        self.n = n

    def run(self):
        print("current task：", self.n)

if __name__ == "__main__":
    t1 = MyThread("thread 1")
    t2 = MyThread("thread 2")

    t1.start()
    t2.start()
    # 将 t1 和 t2 加入到主线程中
    t1.join()
    t2.join()
```
线程调试：<br>
is_alive()：判断线程是否活动；<br>
getName()：获取线程名称；<br>
##### 2）线程锁
- 线程的锁一般包括：lock()、RLock()、Condition()、信号量模型、事件锁以及定时器；<br>
- 和进程的锁类似，在需要锁的代码片段开始和结束添加加锁和解锁代码；<br>
- 其中lock()和RLock()都是普通锁，区别在于，lock()不可嵌套和RLock()可以嵌套(RLock可重入锁)；<br>
- Condition()为条件锁；<br>
- 信号量方式是通过计数器，实现经典管程的信号量模型<br>
- 事件锁，根据事件状态来决定线程是否阻塞还是继续执行
- 定时器，休眠指定时间后继续执行
#####
一般锁示例如下：<br>
- lock()函数形式：<br>
```python
import threading
import time

num = 0
mutex = threading.Lock()

class MyThread(threading.Thread):
    def run(self):
        global num
        time.sleep(1)
        if mutex.acquire(1):    # 加锁 
            num = num + 1
            print(f'{self.name} : num value is  {num}')
        mutex.release()   #解锁

if __name__ == '__main__':
    for i in range(5):
        t = MyThread()
        t.start()
```
- RLock()函数形式：<br>
```python
import threading
import time
# Lock普通锁不可嵌套，RLock普通锁可嵌套
mutex = threading.RLock()

class MyThread(threading.Thread):
    def run(self):
        if mutex.acquire(1):
            print("thread " + self.name + " get mutex")
            time.sleep(1)
            mutex.acquire()
            mutex.release()
        mutex.release()

if __name__ == '__main__':
    for i in range(5):
        t = MyThread()
        t.start()
```
条件锁示例：
```python
# 条件锁：该机制会使线程等待，只有满足某条件时，才释放n个线程
import threading
 
def condition():
    ret = False
    r = input(">>>")
    if r == "yes":
        ret = True
    return ret
 
def func(conn,i):
    # print(i)
    conn.acquire()
    conn.wait_for(condition)  # 这个方法接受一个函数的返回值
    print(i+100)
    conn.release()
 
c = threading.Condition()
for i in range(10):
    t = threading.Thread(target=func,args=(c,i,))
    t.start()

# 条件锁的原理跟设计模式中的生产者／消费者（Producer/Consumer）模式类似
```
信号量示例：
```python
# 信号量：内部实现一个计数器，占用信号量的线程数超过指定值时阻塞
import time
import threading
 
def run(n):
    semaphore.acquire()
    print("run the thread: %s" % n)
    time.sleep(1)
    semaphore.release()

num = 0
semaphore = threading.BoundedSemaphore(5)  # 最多允许5个线程同时运行
for i in range(20):
    t = threading.Thread(target=run,args=(i,))
    t.start()
```
事件锁示例：
```python
# 事件： 定义一个flag，set设置flag为True ，clear设置flag为False
import threading
 
def func(e,i):
    print(i)
    e.wait()  # 检测当前event是什么状态，如果是红灯，则阻塞，如果是绿灯则继续往下执行。默认是红灯。
    print(i+100)
 
event = threading.Event()
for i in range(10):
    t = threading.Thread(target=func,args=(event,i))
    t.start()
 
event.clear()  # 主动将状态设置为红灯
inp = input(">>>")
if inp == "1":
    event.set()# 主动将状态设置为绿灯
```
定时器示例：
```python
# 定时器： 指定n秒后执行
from threading import Timer
def hello():
    print("hello, world")
t = Timer(1,hello)  # 表示1秒后执行hello函数
t.start()
```
##### 3）线程队列
线程中用到的队列包括：
- 普通队列queue.Queue、
- 优先级队列queue.PriorityQueue、

queue.Queue：<br>
普通队列与进程中的队列用法一样，都符合FIFO特点，并且==线程安全==，线程队列常用函数：<br>
```python
import queue
q = queue.Queue(5)
q.put(111)        # 存队列
q.put(222)
q.put(333)
print(q.get())    # 取队列 Queue.get(block=True, timeout=None)
                  # 如果可选参数 block 是 true 并且 timeout 是 None 
                  # (默认值)，则在必要时阻塞至项目可得到
print(q.get())
q.task_done()     # 每次从queue中get一个数据之后，当处理好相关问题，最后调用该方法，
                  # 以提示q.join()是否停止阻塞，让线程继续执行或者退出
print(q.qsize())  # 队列中元素的个数， 队列的大小
print(q.empty())  # 队列是否为空
print(q.full())   # 队列是否满了
```
队列实现的生产者和消费者模型：<br>
wait()会直接释放锁，而notify()要等到下个wait()（或者是代码块结束，没测试，但八九不离十感觉）出现时才释放锁。<br>
同时notify()如果没有对应wait()相当于没写代码。<br>
说明：经测试，生产者和消费者线程中的self.con.release()并未执行？<br>
```python
import queue
import threading
import random
import time

writelock = threading.Lock()

class Producer(threading.Thread):
    def __init__(self, q, con, name):
        super(Producer, self).__init__()
        self.q = q
        self.name = name
        self.con =con
        print(f'Producer {self.name} Started')
    
    def run(self):
        while 1:
            global writelock
            self.con.acquire()  # 获得锁对象
            if self.q.full():   # 队列满
                with writelock:
                    print('Queue is full , producer wait')
                self.con.wait()  # 等待资源
            else:
                value = random.randint(0,10)
                with  writelock:
                    print(f'{self.name} put value {self.name} {str(value)} in queue')
                self.q.put( (f'{self.name} : {str(value)}') ) # 放入队列
                self.con.notify()   # 通知消费者
                time.sleep(1)
        self.con.release()

class Consumer(threading.Thread):
    def __init__(self, q, con, name):
        super(Consumer, self).__init__()
        self.q = q
        self.name = name
        self.con =con
        print(f'Consumer {self.name} Started')

    def run(self):
        while 1:
            global writelock
            self.con.acquire()
            if self.q.empty():   # 队列空
                with writelock:
                    print('Queue is empty , consumer wait')
                self.con.wait()  # 等待资源
            else:
                value = self.q.get()
                with writelock:
                    print(f'{self.name} get value {value} from queue')              
                self.con.notify()   # 通知生产者
                time.sleep(1)
        self.con.release()

if __name__ == '__main__':
    q = queue.Queue(10)
    con = threading.Condition()   # 条件变量锁
    p1 = Producer(q, con, 'P1')
    p1.start()
    p2 = Producer(q, con, 'P2')
    p2.start()
    c1 = Consumer(q, con, 'C1')
    c1.start()
```
queue.PriorityQueue：<br>
优先级队列中，每个元素都是元组，元素中包括优先级序号和元素内容，数字越小优先级越高，相同优先级的先进先出；<br>
```python
import queue
q = queue.PriorityQueue()
q.put((1,"work"))
q.put((-1,"life"))
q.put((1,"drink"))
q.put((-2,"sleep"))
print(q.get())
print(q.get())
print(q.get())
print(q.get())
```
其他队列：<br>
queue.LifoQueue 后进先出队列,类似堆栈<br>
q.deque 双向队列<br>
##### 4）线程池
用法与进程池类似，用于管理多个线程，主要分为两类：<br>
一般线程池：
```python
import requests
from multiprocessing.dummy import Pool as ThreadPool

urls = [
   'http://www.baidu.com',
   'http://www.sina.com.cn',
   'http://www.163.com',
   'http://www.qq.com',
   'http://www.taobao.com',            
   ]

# 开启线程池
pool = ThreadPool(4)
# 获取urls的结果
results = pool.map(requests.get, urls)
# 关闭线程池等待任务完成退出
pool.close()
pool.join()

for  i in results:
    print(i.url)
```
更高级线程池(3.2版本之后封装)：
```python
# Python3.2 中引入了 concurrent.futures 库，利用这个库可以非常方便的使用多线程、多进程
from concurrent.futures import ThreadPoolExecutor
import time

def func(args):
    print(f'call func {args}')
    
if __name__ == "__main__":
    seed = ['a', 'b', 'c', 'd']
    # 参数为线程数
    with ThreadPoolExecutor(3) as executor:
        executor.submit(func, seed)
    time.sleep(1)

    with ThreadPoolExecutor(3) as executor2:
        executor2.map(func, seed)
    time.sleep(1)

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(pow, 2, 3)
        print(future.result())
```
executor.submit与executor2.map区别在于，如果传入的参数是个集合，submit会将集合当做整体传入可调用对象，map会逐个讲集合元素传入指定可调用对象。<br>
使用ThreadPoolExecutor也要注意避免多个线程依赖其他线程资源导致的死锁。<br>
##### 5）GIL(全局解释器锁)
==CPU密集型操作时，单线程和多线程执行时间几乎无差别==。主要原因涉及到python的解释器，主流解释器CPython，底层存在GIL全局解释器锁。因此多线程实际上其实是伪并发（争抢时间片）。<br>

**GIL(全局解释器锁)**
- 每个进程只有一个GIL
- 拿到GIL可以使用CPU
- CPython解释器不是真正意义上的多线程，属于伪并发

多个线程抢GIL，只有一个线程可以拿到GIL，拿到GIL后执行I/O操作(读写磁盘、内存、数据包等)时会释放GIL，这时所有线程又开始争抢GIL。<br>
==因此多线程适合爬虫这种I/O密集型操作。==


作业涉及到其他知识点：<br>
sys.argv<br>
argparse模块<br>