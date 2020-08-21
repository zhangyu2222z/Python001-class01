### 本周主要学习内容如下：
#### 主要学习Django部分核心源码，DjangoWeb相关功能以及其他python框架简介

##### 一、Django核心源码
1、URLconf的partial偏函数：
URLconf-URL调度器
典型写法：

```
urlpatterns = [
    path('douban', views.books_short),
    re_path(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive), 
]
```
学习思路：<br>
根据path()和re_path(),进一步了解到两个方法都会调用functools的partial函数；如果想理解底层实现方案：
- 首先就要阅读官方文档；
- 然后自己用python重新实现核心方法逻辑(也就是所谓的造轮子)；
- 之后再自己写一个方便记忆的例子；

**老师学习源代码思考过程**：<br>
以偏函数partial为例：<br>
从源码层面对比path()、re_path() 区别<br>

```
path = partial(_path, Pattern=RoutePattern)
re_path = partial(_path, Pattern=RegexPattern)
```

查看partial具体实现：

```
def partial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*args, *fargs, **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc
```
阅读实现过程可知partial中逻辑：
- 1. 包括闭包(装饰器)
- 2. 怎么实现参数处理的
- 3. 除了实现功能，还考虑了哪些额外的功能

再阅读官方文档，根据具体例子理解：

```
# 官方文档 demo
from functools import partial
basetwo = partial(int, base=2)
basetwo.__doc__ = 'Convert base 2 string to an int.'
basetwo('10010')
```
最后总结partial注意事项：
- 1 partial 第一个参数必须是可调用对象
- 2 参数传递顺序是从左到右，但不能超过原函数参数个数
- 3 关键字参数会覆盖 partial 中定义好的参数

2、URLconf的include 函数：
源码：

```
# site-packages/django/urls/conf.py
def include(arg, namespace=None):
    if isinstance(arg, tuple):
        pass
    if isinstance(urlconf_module, str):
        # 重点逻辑
        urlconf_module = import_module(urlconf_module)
        patterns = getattr(urlconf_module, 'urlpatterns', urlconf_module)
        app_name = getattr(urlconf_module, 'app_name', app_name)
        #
    if isinstance(patterns, (list, tuple)):
        pass
    return (urlconf_module, app_name, namespace)
```

include就是为了加载子项目中urlpatterns，其中加了很多内部处理；<br>

3、view视图请求响应流程：<br>
请求与响应<br>
HttpRequest 创建与 HttpResponse 返回是一次 HTTP 请求的标准行为。<br>
Path 将请求传递给view视图函数，request怎么得到的？如何返回的？<br>
HttpRequest 由 WSGI 创建，HttpResponse 由开发者创建。<br>
View 视图抽象出的两大功能：返回一个包含被请求页面内容的 HttpResponse 对象，或者抛出一个异常，比如 Http404 。<br>

view视图请求过程：<br>
WSGI会创建请求过程；<br>
manage.py中，WSGI会自动将HttpRequest封装为request对象；<br>
from django.http import HttpRequest 包含大量的属性和方法，如：<br>
self.META = {} # 包含所有的HTTP头部<br>
self.GET = QueryDict(mutable=True) # 包含HTTP GET的所有参数<br>
HttpRequest中__init__中会初始化请求属性，以及很多元信息；<br>
其中GET以及POST属性是通过QueryDict获取；<br>
QueryDict 继承自 MultiValueDict，MultiValueDict 又继承自 dict<br>
QueryDict对传过来的有重复key的值进行进一步优化，会将重复key对应的值进行合并为一个list<br>

```
class MultiValueDict(dict):
    def __init__(self, key_to_list_mapping=()):
        super().__init__(key_to_list_mapping)
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, super().__repr__())
    def __getitem__(self, key):
... ...
```

view视图响应过程：<br>
返回带有内容的httpReponse对象，或者返回异常信息，如异常页面和请求错误码<br>
响应返回包括：HttpResponse对象，render，redirect<br>
其中返回HttpResponse示例如下：<br>

```
def test1(request):
    # 已经引入了HttpResponse
    # from django.http import HttpResponse
    response1 = HttpResponse()
    response2 = HttpResponse("Any Text", content_type="text/plain")
    return response1
def test2(request):
    # 使用HttpResponse的子类
    from django.http import JsonResponse
    response3 = JsonResponse({'foo': 'bar'}) # response.content
    # 当做字典用时候会，该key-value会自动添加到Http头部信息中
    response3['Age'] = 120
    
    # 没有显式指定 404
    from django.http import HttpResponseNotFound
    response4 = HttpResponseNotFound('<h1>Page not found</h1>')
    return response4
```

httpRequest和httpReponse具体说明也可以查看Django官方文档，包括其中的属性，方法以及用法例子；<br>

HttpResponse⼦类：
- HttpResponse.content：响应内容
- HttpResponse.charset：响应内容的编码
- HttpResponse.status_code：响应的状态码
- JsonResponse 是 HttpResponse 的子类，专门用来生成 JSON 编码的响应。

整个请求响应完整流程：<br>
- 1、http客户端请求访问到modwsgi，先经过请求中间件做一些校验判断，如果校验出问题直接通过响应中间件返回给客户端；
- 2、如果校验无问题，会经过urls.py找到对应视图中间件进行处理；
- 3、通过视图中间件找到对应视图，视图中是自己的业务逻辑，如果涉及到持久层，则会通过模型和数据库交互；
- 4、视图也会调用模板生成对应内容生成响应，通过返回中间件返回给客户端；

4、model模型：<br>
自增主键创建：<br>
为什么自定义的 Model 要继承 models.Model ? <br>
- 不需要显式定义主键
- 自动拥有查询管理器对象
- 可以使用 ORM API 对数据库、表实现 CRUD

**自增主键的生成过程**：models.Model的元类ModelBase(父类必为type)，其中的魔术方法__new__返回值是一个类；该魔术方法再创建类时会初始化元属性，会创建Options的实例，并且调用_prepare函数，往类中添加属性，其中会判断是否有主键，如果没有主键属性，父类也没有主键，就会默认添加一个自增的主键属性；<br>

查询管理器：
从数据库查询时经常用到类似以下语句
```
def books_short(request):
    shorts = T1.objects.all()
```
其中objects指的就是查询管理器；<br>
查询管理器是定义在django/db/models/manager.py中，和默认自增主键一样通过_prepare函数，传递给自定义model；<br>
manager.py中的Manager类 继承自 BaseManagerFromQuerySet 类，拥有 QuerySet 的大部分方法，get、create、filter 等方法都来自 QuerySet；

```
class Manager(BaseManager.from_queryset(QuerySet)):
    pass

BaseManager：
def from_queryset(cls, queryset_class, class_name=None):
        if class_name is None:
            class_name = '%sFrom%s' % (cls.__name__, queryset_class.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_class,
            **cls._get_queryset_methods(queryset_class),
        })
...


def get_queryset(self):
        """
        Return a new QuerySet object. Subclasses can override this method to
        customize the behavior of the Manager.
        """
        return self._queryset_class(model=self.model, using=self._db, hints=self._hints)

```
在使用T1.objects，实际上的objects就是BaseManager类的实例，
上面代码中Manager的父类BaseManager.from_queryset(QuerySet)，会自动创建返回默认BaseManagerFromQuerySet类；<br>
而BaseManagerFromQuerySet类继承了QuerySet类，并且有QuerySet类的各种属性， T1.objects.all()会**动态的**创建QuerySet类实例并且返回，所以shorts = 这句实际上是QuerySet类实例；<br>

5、template模板：
模板引擎通过render加载html文件：
加载模板文件主要步骤是加载settings配置-读取并加载引擎-通过引擎读取指定目录的html模板文件；<br>

render实现源码：<br>

```
def render(request, template_name, context=None, content_type=None, status=None, 
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)
```
render主要是对Response进行进一步封装，加载html模板核心逻辑在于render_to_string函数；<br>
render_to_string函数：

```
def render_to_string(template_name, context=None, request=None,using=None):
    if isinstance(template_name, (list, tuple)):
        ...
    else:
        template = get_template(template_name, using=using)
    return template.render(context, request)
```
其中get_template使用了_engine_list方法获得后端模板

```
def _engine_list(using=None):
    # 该方法返回Template文件列表，
    # engines是一个EngineHandler类的实例
    return engines.all()
```
EngineHandler会加载settings.py中的TEMPLATES配置：

```
class EngineHandler:
    @cached_property
    def templates(self):
        self._templates = settings.TEMPLATES
        # 遍历模板后端配置
        for tpl in self._templates:
            tpl = {
            'NAME': default_name,
            'DIRS': [],
            'APP_DIRS': False,
            'OPTIONS': {},
            **tpl,
            }
        templates[tpl['NAME']] = tpl
        backend_names.append(tpl['NAME'])
        return templates
```
模板引擎读取完配置后，接着就加载具体模板文件：<br>
加载模板文件通过Engine类进行，接着继续看get_template<br>

```
def get_template(template_name, using=None):
    ...
    # engine定义在初始化函数中，是Engine类的实例
    # Engine类在 site-packages/django/template/engine.py 文件中
    return engine.get_template(template_name

# site-packages/django/template/engine.py
class Engine:
    def get_template(self, template_name):
        template, origin = self.find_template(template_name)
        if not hasattr(template, 'render'):
            # template needs to be compiled
            template = Template(template, origin, template_name, engine=self)
            return template
```
其中find_template会调用get_template，通过 get_template() 获得 template 对象；<br>
注意：
- get_template 的实现来自 FilesystemLoader 的父类，找到 contents对象并构造了 Template 对象进行返回。
- get_template_loaders() 增加了一个列表：['django.template.loaders.filesystem.Loader','django.template.loaders.app_directories.Loader’] 并把这个列表里的元素实例化成了 Loader 对象的实例化实现底层文件的加载。

```
def find_template(self, name, dirs=None, skip=None):
    tried = []
    for loader in self.template_loaders:
        try:
            template = loader.get_template(name, skip=skip)
            return template, template.origin
            except TemplateDoesNotExist as e:
                tried.extend(e.tried)
        raise TemplateDoesNotExist(name, tried=tried)

# site-packages/django/template/backends/base.py
class BaseEngine
    @cached_property
    def template_dirs(self):
        template_dirs = tuple(self.dirs)
        if self.app_dirs:
            template_dirs += get_app_template_dirs(self.app_dirname)
        return template_dirs

# site-packages/django/template/utils.py
@functools.lru_cache()
def get_app_template_dirs(dirname):
    template_dirs = [
        str(Path(app_config.path) / dirname)
        for app_config in apps.get_app_configs()
            if app_config.path and (Path(app_config.path) / dirname).is_dir()
    ]
    return tuple(template_dirs)
```
模板文件渲染：
主要还是通过render，render是通过django/template/base.py中的Template类返回实现；<br>

```
class Template:
    def __init__()：
        # source存储的是模版文件中的内容
        self.source = str(template_string) # May be lazy
    def render(self, context):
        return self._render(context)
    def _render(self, context):
        # 模板内容会分割成nodelist
        return self.nodelist.render(context)
```
如果是 Node 类型，则会调用 render_annotated方法获取渲染结果，否则直接将元素本身作为结果，继续跟踪 bit = node.render_annotated(context)。

```
# Node类的两个子类

# 一般就是静态文本内容
class TextNode(Node):
    def render(self, context):
        # 返回对象(字符串)本身
        return self.s

# VariableNode指的是带有控制逻辑部分的内容，会根据语法解析器FilterExpression处理
class VariableNode(Node):
    def render(self, context):
    try:
        # 使用resolve()解析后返回
        output = self.filter_expression.resolve(context)

# 语法解析器
class FilterExpression:
    def resolve(self, context, ignore_failures=False):
# 如何解析引用了类class Lexer:
class Lexer:
    def tokenize(self):
        # split分割匹配的子串并返回列表
        # tag_re是正则表达式模式对象
        for bit in tag_re.split(self.template_string):
        ... ...
        return result
    # 定义四种token类型
    def create_token(self, token_string, position, lineno, in_tag):
        if in_tag and not self.verbatim:
        # 1 变量类型，开头为{{ 
        if token_string.startswith(VARIABLE_TAG_START):
            return Token(TokenType.VAR, token_string[2:-2].strip(), position, lineno)
        # 2 块类型，开头为{%
        elif token_string.startswith(BLOCK_TAG_START):
            if block_content[:9] in ('verbatim', 'verbatim '):
                self.verbatim = 'end%s' % block_content
                return Token(TokenType.BLOCK, block_content, position, lineno)
        # 3 注释类型，开头为{#
        elif token_string.startswith(COMMENT_TAG_START):
            content = ''
            if token_string.find(TRANSLATOR_COMMENT_MARK):
                content = token_string[2:-2].strip()
                return Token(TokenType.COMMENT, content, position, lineno)
            else:
                # 0 文本类型， 字符串字面值
                return Token(TokenType.TEXT, token_string, position, lineno)
```

##### 二、DjangoWeb部分
1、管理界面：
管理页面的设计哲学：
- 管理后台是一项缺乏创造性和乏味的工作，Django 全自动地根据模型创建后台界面。 
- 管理界面不是为了网站的访问者，而是为管理者准备的。

后台管理界面：Django服务的ip:端口/admin<br>
创建管理员账号：$ python manage.py createsuperuser<br>

增加模型：

```
./index/admin.py
from .models import Type, Name
# 注册模型
admin.site.register(Type)
admin.site.register(Name)
```
注意点：<br>
1)settings.py中必须配置好：

```
INSTALLED_APPS = [
    ####  内置的后台管理系统
    'django.contrib.admin',
    ...]
```
否则用不了；<br>
2)引入模型，必须是类名；<br>
3)settings.py数据库配置正确；<br>
4)migrate命令将后台管理需要的表导入指定数据库；<br>

2、表单：<br>
html形式：<br>

```
<form action="result.html" method="post">
    username:<input type="text" name="username" /><br>
    password:<input type="password" name="password" /> <br>
    <input type="submit" value="登录">
</form>
```

后台生成形式：<br>
views中调用forms相关校验功能<br>
```
# form.py
from django import forms
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)

# html：
<form action="/login2" method="post">
{% csrf_token %}
{{ form }}
<input type="submit" value="Login">
</form>

```

html通过url找到views.py对应的函数使用表单：
```
# views.py
# 该函数处理两种请求方式，如果是GET，就将表单元素对象返回给页面展示，如果是POST说明是表单提交，做验证逻辑；
def login2(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 读取表单的返回值
            cd = login_form.cleaned_data 
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                # 登陆用户
                login(request, user)  
                return HttpResponse('登录成功')
            else:
                return HttpResponse('登录失败')
    # GET
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'form2.html', {'form': login_form})

```
3、表单CSRF防护：<br>
CSRF:跨站请求攻击<br>
防止CSRF:POST页面添加csrf token : {% csrf_token %}<br>
csrf防护在settings中中间件配置,只对post请求做防护：

```
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    ...
]
```
如果只针对个别post请求做csrf防护，可以不需要配置中间件，直接在代码中添加@csrf_protect或@csrf_exempt，具体如下：<br>
@csrf_protect是进行csrf验证，@csrf_exempt是免除csrf验证<br>
```
from django.views.decorators.csrf import csrf_exempt, csrf_protect
@csrf_exempt
def result(request):
    return render(request, 'result.html')
```
如果是ajax请求，也要添加csrf token；<br>

4、用户管理认证：<br>
Django自带了用户认证模块，以及对会话的处理；<br>

首先配置验证中间件：

```
MIDDLEWARE = [
    ...
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]
```

然后是代码部分，Django用户验证主要用到django.contrib.auth包：一般主要用到login，authenticate，logout
```
from .form import LoginForm
from django.contrib.auth import authenticate, login
def login2(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 读取表单的返回值
            cd = login_form.cleaned_data 
            # 验证用户信息
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                # 登陆用户 保存会话
                login(request, user)  
                return HttpResponse('登录成功')
            else:
                return HttpResponse('登录失败')
    # GET
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, 'form2.html', {'form': login_form})
```
需要验证的用户信息，可以通过Django命令行进行创建：
- 首先进入Django的shell命令控制台：python manage.py shell
- 导入验证模块：from django.contrib.auth.model import User
- 然后user = User.objects.create_user('name', 'email', 'password') 语句创建用户实例，user.save()会利用Django自己的ORM在数据库中保存该用户信息，保存到数据库的用户密码会加密；

5、信号
- 发生事件，通知应用程序
- 支持若干信号发送者通知一组接收者
- 解耦

信号使用方法：

函数方式注册回调函数

```
from django.core.signals import request_started
request_started.connect(my_callback1)
```

装饰器方式注册回调函数

```
from django.core.signals import request_finished
from django.dispatch import receiver
@receiver(request_finished)
def my_callback2(sender, **kwargs):
    pass
```

##### 三、Django相关其他功能
1、中间件
Django中间件：全局改变输入或输出轻量级的、低级的“插件”系统对请求、响应处理的钩子框架(**作用类似拦截器？**)<br>
自定义一个中间件(参数固定写法)：

```
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
class Middle1(MiddlewareMixin):
    def process_request(self,request):
        print('中间件请求')
    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('中间件视图')
    def process_exception(self, request, exception):
        print('中间件异常')
    def process_response(self, request, response):
        print('中间件响应')
        return response
```
编写之后，在settings.py中设置（注意中间件是按照配置顺序运行）

```
MIDDLEWARE = [
    ...
    'index.middleware.Middle1'
]
```

2、web服务部署生产：
通常很多公司部署服务都会通过中转服务进行接收请求再转发到对应服务器，比如使用apache，nginx，gunnicorn等；<br>
其中一般Django服务会配合gunnicorn部署生产，gunicorn是一个wsgi http server；<br>
Django结合gunnicorn

```
# 安装gunicorn
pip install gunicorn
# 在项目目录执行
gunicorn MyDjango.wsgi
```
gunicorn --help|more

3、celery定时器：
- Celery 是分布式消息队列
- 使用 Celery 实现定时任务

celery架构基本是分四个部分：
- 定时任务(celery beat)和异步任务(async task) 作为生产者；
- 任务执行单元(celery worker)是作为消费者，实际执行任务；
- 消息中间件(Broker)：生产者向消息中间件注册；任务执行单元向消息中间件订阅；
- 执行结果保存在结果存储；

先安装结果存储部分(老师使用redis)；
启动redis服务：redis-server /path/to/redis.conf

安装celery：

```
pip install celery
# python的redis驱动
pip install redis==2.10.6
# celery的redis插件
pip install celery-with-redis
# django的celery插件
pip install django-celery

# 创建项目，新建app
django-admin startproject MyDjango
python manager.py startapp djcron

settings.py添加配置
INSTALL_APPS=[
# 定时器
'djcelery',
# 自定义app
'djcron'
]

迁移生成表
python manage.py migrate

# settings.py中配置django时区

# 引入调度任务
from celery.schedules import crontab
# 引入时间偏移
from celery.schedules import timedelta
import djcelery
# 初始化加载
djcelery.setup_loader()
# 后端存储代理人
BROKER_URL = 'redis://:123456@127.0.0.1:6379/' 
# 引入app的任务
CELERY_IMPORTS = ('djcron.tasks') 
# 时区 会覆盖django时区
CELERY_TIMEZONE = 'Asia/Shanghai' 
# 定时任务调度器
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler' 
==========================
MyDjango下创建cerely.py
import os
from celery import Celery,platforms
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE','MyDjango.settings')
app = Celery('MyDjango')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
platforms.C_FORCE_ROOT = True


==========================
# 在 __init__.py 增加
# 使用绝对引入，后续使用import引入会忽略当前目录下的包
from __future__ import absolute_import
# 引入MyDjango下的cerely.py
from .celery import app as celery_app

# mysql部分
import pymysql
pymysql.install_as_MySQLdb()
==========================
djcorn下新建tasks.py：
from MyDjango.celery import app

# 封装成任务
@app.task()
def task1():
    return 'test1'
@app.task()
def task2():
    return 'test2'

# 启动 Celery
# 启动生产者
celery -A MyDjango beat -l info
# 启动消费者
celery -A MyDjango worker -l info
```
可通过django后台管理添加计划任务


##### 四、其他框架
flask：轻量级，可插拔，同样MTV理念；
简单例子：先pip安装

```
from flask import Flask
app = Flask(__name__)

@app.route('/') # url
def hello_world():
    return 'Hello, World!'

# 启动
$ export FLASK_APP=hello.py
$ flask run
```
模板：jinja2

上下文：request 上下文与 session 上下文
当有请求到达WSGI，django会产生httprequest对象，flask会生成request上下文；
作用非常相似；
```
from flask import Flask,Request
from flask.globals import _request_ctx_stack

app = Flask(__name__)

@app.route('/')
def index():
    # 获取ctx对象
    ctx = _request_ctx_stack.top 
    # Request 上下文管理
    print(ctx)  
    print(ctx.request.method)  # GET
    return 'index'

if __name__ == '__main__':
    app.run()
```

信号：Flask 从 0.6 开始，通过 Blinker 提供了信号支持
```
pip install blinker

from flask import Flask
from flask import signals

app = Flask(__name__)

def func1(*argv):
    print('func1')
    
# 在发起请求之前执行func1函数
signals.request_started.connect(func1)

@app.route('/')
def func():
    print('View Function')
    return "ok"

if __name__ == '__main__':
    app.run()
```

tornador：<br>
web框架，也是底层I/O库<br>

Tornado 的同步 IO 与异步 IO：

```
http_client = HTTPClient()
http_client = AsyncHTTPClient()
```

官方例子：
```
from tornado.httpclient import HTTPClient

# sync
def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)
    return response.body

# async
from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future

def async_fetch_future(url):
    http_client = AsyncHTTPClient()
    my_future = Future()
    fetch_future = http_client.fetch(url)
    fetch_future.add_done_callback(
        lambda f: my_future.set_result(f.result()))
    return my_future
```

Tornado 路由映射

```
# 路由映射
application = tornado.web.Application([
    (r"/", MainHandler),
])


import tornado.ioloop
import tornado.web                              

class MainHandler(tornado.web.RequestHandler):  
    def get(self):                              
        self.write("Hello, world")
        # self.render("index.html")              

#路由映射 类似views
application = tornado.web.Application([         
    (r"/", MainHandler),                   
])

if __name__ == "__main__":
    application.listen(8000)                    
    tornado.ioloop.IOLoop.instance().start()

三种网络框架特点：
# gevent 代码好维护
# twisted 稳定性最好
# tornado 兼容性最好
```


