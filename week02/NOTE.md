### 本周主要学习内容如下：
#### 异常处理，python对mysql操作，反爬虫，scrapy设置代理ip，分布式爬虫基本操作（scrapy与redis通信）

#### 异常处理
**异常信息**：通过Traceback函数处理，打印异常出处，显示异常类型信息<br>
**异常捕获过程**：异常是一个类，将异常消息打包成对象，根据该对象自动查找调用栈（函数调用，会打印调用栈），直到运行系统找到明确声明如何处理这些异常类的位置，所有异常都集成BaseException<br>
**常见异常**：
LookupError下的IndexError和KeyError，IOError，NameError，TypeError，AttributeError，ZeroDivisionError<br>
**捕获语句**：
```python
try:
    代码块
except (异常类1,异常类2...) as e:
    异常处理（也可以嵌套一个try except）
finally:
    最终执行代码块
```
**抛出异常动作**：
```python
raise Exception('异常信息')
```
**自定义异常**：
```python
class CustomException(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self, ErrorInfo)
        self.errorinfo = ErrorInfo
    def __str__(self):
        return self.errorinfo
try:
    raise CustomException('异常信息')
except CustomException as ce:
    # 处理代码
finally:
    # 最终执行代码
```
**简化异常信息日志第三方库**：pretty_errors

**python上下文管理**：关键字with，with可以简化异常处理，替代try except finally<br>
```python
#!/usr/bin/env python
# with_example01.py
class Sample:
    def __enter__(self):
        print "In __enter__()"
        return "Foo"
    def __exit__(self, type, value, trace):
        print "In __exit__()"
    def get_sample():
        return Sample()

with get_sample() as sample:
    print "sample:", sample
```
输出如下：
```python
In __enter__()
sample: Foo
In __exit__()
```
流程如下：<br>
__enter__()方法被执行<br>
__enter__()方法返回的值 - 这个例子中是"Foo"，赋值给变量’sample’
执行代码块，打印变量"sample"的值为 “Foo”<br>
__exit__()方法被调用<br>

#### python对mysql操作：
**安装mysql后启动mysql服务**：mysql.server start<br>
**python链接mysql两种方式**：PyMySQL、ORM<br>
1）PyMySQL<br>
安装：pip install pymysql<br>
一般流程：<br>
```
创建connection
获取cursor
CRUD操作
关闭cursor
关闭connection
```
例：<br>
```python
import pymysql
# 数据库信息
dbInfo = {‘host’:'数据库地址', 
    ’port‘:'端口', 
    'user':'用户名', 
    'password':'密码', 
    'db':'数据库实例名',
    'charset':'utf8mb4(字符集)'}

sqls = ['select 1', 'select VERSION()']
result = []
class ConnDB(object):
# 初始化读取配置(__init__可以看做为构造)
    def __init__(self, dfInfo, sqls):
        self.host = dbInfo['host']
        self.port= dbInfo['port']
        self.user= dbInfo['user']
        self.password= dbInfo['password']
        self.db= dbInfo['db']
        self.sqls = sqls 
    def run(self):
        conn = pymysql.connect(host = self.host, port = self.port, 
        user = self.user, password = self.password, db = self.db)
        # 游标建立时开启了一个隐形事务（可以回滚到此时状态）
        cur = conn.cursor()
        try:
            for command in self.sqls:
            cur.execute(command)
            result.append(cur.fetchone())
            # 关闭游标
            cur.close()
            # 提交事务
            conn.commit()
        except:
            # 异常回滚
            conn.rollback()
        # 关闭连接
        conn.close()
if __name__ = '__main__':
    db = ConnDB(dbInfo, sqls)
    db.run()
print(result)
```
关于sql语句执行结果说明：<br>
```python
# 此处执行结果实际返回的是记录条数
count = cursor.execute('select * from table')
# 真正获取数据方式：
# 获取一条数据
cursor.fetchone()
# 获取所有数据
cursor.fetchall() 
批量操作：
cursor.executemany('sql语句')
插入语句：
values = [(id, 'testuser'+str(id)) for id in range(4,15)]
cursor.executemany('INSERT INTO TABLE VALUES(%s, %s)', values)
```
#### 简单介绍反爬虫：
**服务端判断请求是不是爬虫的两种方式**：<br>
1）根据基本请求带的数据（如请求头等）判断；<br>
2）根据行为判断是不是用户通过浏览器；<br>
反反爬虫就要根据上面两种判断方式进行做针对处理，使用request和scrapy发起请求时http头文件数据尽量模拟正常浏览器访问<br>
**浏览器基本行为**：<br>
1、带htttp头信息：user-agent、referer等<br>
2、带cookie(包含加密的用户名、密码等)<br>
**主要的几个反反爬虫方案**：<br>
1、http请求头：<br>
user-agent：用到第三方库 fake-useragent来模拟不同浏览器的user-agent<br>
```python
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl = False)
# chrome的user-agent
print(f'chrome浏览器：{ua.chrome}’)
# 随机的user-agent
print(f'随机浏览器：{ua.random}')
```
浏览器打开开发者工具（如chrome的f12）
选择network，随便点击一个请求，可以查看请求头数据(包括user-agent，cookie，referer等)，替换自己本机浏览器http请求头所需数据<br>
2、cookie验证：<br>
一些网站的cookie验证，可以直接使用浏览器中http请求头的cookie内容<br>
requests使用cookie：<br>
```python
import time
import requests
from fake_useragent import UserAgent
ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent' : ua.random,
    'Referer' : 'https://accounts.douban.com/passport/login_popup?login_source=anony'
}
s = requests.Session()
# session具有保持功能， 就类似浏览器输入一次密码之后，会自动保留cookie
# 会话对象：在同一个 Session 实例发出的所有请求之间保持 cookie， 
# 期间使用 urllib3 的 connection pooling 功能。
# 向同一主机发送多个请求，底层的 TCP 连接将会被重用，从而带来显著的性能提升。
login_url = 'https://accounts.douban.com/j/mobile/login/basic'
form_data = {
    'ck':'',
    'name':'15055495@qq.com',
    'password':'',
    'remember':'false',
    'ticket':''
}
# post数据前获取cookie
#pre_login = 'https://accounts.douban.com/passport/login'
#pre_resp = s.get(pre_login, headers=headers)
# 服务器设置在本地的cookie会保存在本地
response = s.post(login_url, data=form_data, headers=headers, cookies=s.cookies)
# 登陆后可以进行后续的请求
# url2 = 'https://accounts.douban.com/passport/setting'
# 此处直接用session.get方式请求，会带着验证后的cookie中数据	 
# 会带上之前保存在seesion中的cookie，能够请求成功
response2 = s.get(url2,headers = headers)
# response3 = newsession.get(url3, headers = headers, cookies = s.cookies)
# with open('profile.html','w+') as f:
    # f.write(response2.text)
```
3、使用WebDriver模拟浏览器行为：<br>
1）、安装selenium <br>
2）、下载浏览器驱动（例如浏览器为chrome，则驱动对应为chrome driver）<br>
3）、下载之后放python解释器同级目录<br>
4）、使用webdriver获取对应浏览器实例时会找到并且调用浏览器驱动模块<br>
5）、根据代码逻辑会打开浏览器然后执行对应动作<br>
例：<br>
```python
from selenium import webdriver
import time
try:
    browser = webdriver.Chrome()
    # 需要安装chrome driver, 和浏览器版本保持一致
    # http://chromedriver.storage.googleapis.com/index.html
    browser.get('https://www.douban.com')
    time.sleep(1)
    browser.switch_to_frame(browser.find_elements_by_tag_name('iframe')[0])
    btm1 = browser.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    btm1.click()
    browser.find_element_by_xpath('//*[@id="username"]').send_keys('15055495@qq.com')
    browser.find_element_by_id('password').send_keys('test123test456')
    time.sleep(1)
    browser.find_element_by_xpath('//a[contains(@class,"btn-account")]').click()
    cookies = browser.get_cookies() # 获取cookies
    print(cookies)
    time.sleep(3)
except Exception as e:
    print(e)
finally:    
    browser.close()
补充：关于文件下载
# 小文件下载：
import requests
image_url = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
r = requests.get(image_url)
with open("python_logo.png",'wb') as f:
    f.write(r.content)
```
补充：如果文件比较大的话，那么下载下来的文件先放在内存中，内存还是比较有压力的。所以为了防止内存不够用的现象出现，我们要想办法把下载的文件分块写到磁盘中。<br>
```python
# 流文件写入
import requests
file_url = "http://python.xxx.yyy.pdf"
r = requests.get(file_url, stream=True)
with open("python.pdf", "wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            pdf.write(chunk)
```
4）、简单验证码识别：一些网站登录时候会有验证码，可以用tesseract库识别验证码<br>
```python
# 先安装依赖库libpng, jpeg, libtiff, leptonica
# linux环境下需要用到brew命令安装leptonica以及tesseract
# brew install leptonica
# 安装tesseract
# brew install  tesseract
# 与python对接需要安装的包
# pip3 install Pillow
# pip3 install pytesseract
import requests
import os
from PIL import Image
import pytesseract
# 下载图片
# session = requests.session()
# img_url = 'https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=1320441599,4127074888&fm=26&gp=0.jpg'
# agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# headers = {'User-Agent': agent}
# r = session.get(img_url, headers=headers)
# with形式，二进制形式写入文件
# with open('cap.jpg', 'wb') as f:
#     f.write(r.content)
# 打开并显示文件
im = Image.open('cap.jpg')
im.show()
# 灰度图片 先让彩色图片灰度化
gray = im.convert('L')
gray.save('c_gray2.jpg')
im.close()
# 二值化 就是让深色更深，浅色更浅
threshold = 100
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)
# 进一步灰度化图片
out = gray.point(table, '1')
out.save('c_th.jpg')
# 打开图片
th = Image.open('c_th.jpg')
# pytesseract识别图片转为字符串（类型为简中和英文）
print(pytesseract.image_to_string(th,lang='chi_sim+eng'))
# 各种语言识别库 https://github.com/tesseract-ocr/tessdata
# 放到 /usr/local/Cellar/tesseract/版本/share/tessdata
```
#### 设置代理IP
1、下载中间件设置代理ip：<br>
scrapy启动时，日志会打印一些内容，包括settings.py中相关配置信息、扩展信息、中间件信息，下载器、调度器信息等<br>
scrapy运行去掉日志<br>
scrapy crawl 爬虫名 --nolog<br>
1）scrapy使用操作系统设置的代理ip：<br>
设置系统代理ip<br>
linux下命令：export http_proxy='http://52.179.231.206:80'<br>
setting.py 增加 scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware<br>
DOWNLOADER_MIDDLEWARES属性放开屏蔽：<br>
结尾数字设置调用顺序优先级，如果不执行，则设置为None
```python
DOWNLOADER_MIDDLEWARES = {
    'proxyspider.middlewares.ProxyspiderDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'proxyspider.middlewares.RandomHttpProxyMiddleware': 400,
}
```
此属性会被 Request.meta['proxy'] 读取 http_proxy 环境变量加载代理<br>
2、自定义下载中间件设置随机	代理ip：<br>
自定义下载中间件需要重写四个方法：<br>
```python
process_request(request, spider)
request对象经过下载中间件时会被调用，优先级高的先调用
process_response(request, response, spider)
response对象经过下载中间件时会被调用，优先级高的先调用
process_exception(request, exception, spider)
当process_request(), process_response()出异常是会被调用
from_crawler(cls, crawler)
```
使用crawler创建中间件对象，并且返回<br>
1）settings.py中添加自定义代理ip列表<br>
```python
HTTP_PROXY_LIST = [
     'http://52.179.231.206:80',
     'http://95.0.194.241:9090',
]
```
2）自定义下载中间件<br>
自定义下载中间件要继承系统默认下载中间件类scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware<br>
修改from_crawler()，除了读取固定配置项，再添加读取settings.py中自定义代理ip列表，准备传给__init__()中的proxy_list参数（因为from_crawler()方法带有装饰器@classmethod，所以会在实例化(__init__())之前执行）；<br>
修改__init__()，接收proxy_list参数，修改解析方式，将proxy_list转为字典，再将字典中内容进行拆分，可以用正则或者urlparse，然后放入self.proxies中；<br>
修改_set_proxy()，随机读取self.proxies中代理ip，然后一样放入request的meta中proxy属性<br>
源码：<br>
```python
middlewares.py:
class RandomHttpProxyMiddleware(HttpProxyMiddleware):

    def __init__(self, auth_encoding='utf-8', proxy_list = None):
        self.proxies = defaultdict(list)
        for proxy in proxy_list:
            parse = urlparse(proxy)
            self.proxies[parse.scheme].append(proxy)

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('HTTP_PROXY_LIST'):
            raise NotConfigured

        http_proxy_list = crawler.settings.get('HTTP_PROXY_LIST')  
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'utf-8')

        return cls(auth_encoding, http_proxy_list)

    def _set_proxy(self, request, scheme):
        proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
```
#### 分布式爬虫：
Scrapy 原生不支持分布式，多机之间需要 redis 实现队列和管道的共享，

可以通过redis服务，以及scrapy和redis之间通信，scrapy和redis之间通信使用scrapy-redis库，实现多机的scrapy间的交互写作；**Scrapy-redis** 很好地实现了 Scrapy 和 redis 的集成。
```python
pip install scrapy-redis
```
使用 Scrapy-redis 之后 Scrapy 的主要变化：<br>
1. 使用了 RedisSpider 类替代了 Spider 类 
2. Scheduler 的 queue 由 redis 实现 
3. item pipeline 由 redis 实现 

步骤：<br>

1）启动redis服务<br>
redis-server redis.conf<br>
redis.conf为redis配置文件（ip，端口等）<br>
可以使用redis-cli命令链接redis服务<br>
2）修改settings.py<br>
爬虫逻辑几乎不用修改，主要修改配置文件settings.py<br>
主要是在settings.py中修改配置：<br>
redis服务器ip、端口<br>
修改调度器为scrapy-redis的调度器<br>
SCHEDULER = "scrapy_redis.scheduler.Scheduler"<br>
```python
# 去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# Requests的默认优先级队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'
# 将Requests队列持久化到Redis，可支持暂停或重启爬虫
SCHEDULER_PERSIST = True
# 将爬取到的items保存到Redis
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}
pipelines.py直接返回item即可被RedisPipeline调用
```


