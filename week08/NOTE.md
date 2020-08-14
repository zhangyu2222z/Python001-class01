### 本周主要学习内容如下：
#### 主要学习python的高阶语法，包括变量，容器序列深浅拷贝，函数，协程等部分

##### 一、变量赋值
python 一切皆对象，传递的都是对象

```
因此
a = [1, 2, 3]
b = a
a = [4, 5, 6]
中，最后a和b不是同一个对象
而
a = [1, 2, 3]
b = a
a[0],a[1],a[2] = 4, 5, 6
中，是同一对象，因为第一个例子中，a已经指向了一个新的(列表)内存地址
```
变量赋值：<br>
可变数据类型：
- 列表 list
- 字典 dict
不可变数据类型：
- 整型 int
- 浮点型 float
- 字符串型 string
- 元组 tuple


##### 二、容器序列深浅拷贝

序列
另一种分类方式
- 可变序列 list、bytearray、array.array、collections.deque 和 memoryview。 • 不可变序列 tuple、str 和 bytes。
序列分类
- 容器序列：list、tuple、collections.deque 等，能存放不同类型的数据 容器序列可以存放不同类型的数据。
- 扁平序列：str、bytes、bytearray、memoryview (内存视图)、array.array 等，存放的是相同类型的数据 扁平序列只能容纳一种类型。

容器序列存在深拷贝、浅拷贝问题
- 注意：非容器（数字、字符串、元组）类型没有拷贝问题
```
# 容器序列的深浅拷贝问题

old_list = [ i for i in range(1, 11)]

new_list1 = old_list
new_list2 = list(old_list)
#new_list1 is new_list2 False

# 切片操作
new_list3 = old_list[:]
#old_list is new_list3 False

# 嵌套对象
old_list.append([11, 12])

import copy
new_list4 = copy.copy(old_list) #浅拷贝
new_list5 = copy.deepcopy(old_list) #深拷贝

assert new_list4 == new_list5 #True 
assert new_list4 is new_list5 #False AssertionError 

old_list[10][0] = 13
# new_list4 浅拷贝，内容会随着old_list变化而变化
# new_list5 深拷贝，相当于创建一个新的list，但是内容是old_list内容，如果old_list内容发生变化，new_list5不会随之变化
```
##### 三、字典与扩展内置数据类型
字典中的key，必须是hash的(不可变)<br>
如：<br>
dict[{}]和dict[[1,2,3]]是会报错的，因为key是可变的，是非哈希的

使用 collections 扩展内置数据类型<br>
collections 提供了加强版的数据类型<br>
https://docs.python.org/zh-cn/3.6/library/collections.html<br>
namedtuple -- 带命名的元组<br>
Python元组的升级版本 -- namedtuple(具名元组)<br>

因为元组的局限性：不能为元组内部的数据进行命名，所以往往我们并不知道一个元组所要表达的意义，所以在这里引入了 collections.namedtuple<br> 这个工厂函数，来构造一个带字段名的元组。具名元组的实例和普通元组消耗的内存一样多，因为字段名都被存在对应的类里面。这个类跟普通的对象实例比起来也要小一些，因为 Python 不会用__dict__来存放这些实例的属性。<br>
namedtuple 对象的定义如以下格式：
```
collections.namedtuple(typename, field_names, verbose=False, rename=False)
```
返回一个具名元组子类 typename，其中参数的意义如下：
- typename：元组名称
- field_names: 元组中元素的名称
- rename: 如果元素名称中含有 python 的关键字，则必须设置为 rename=True
- verbose: 默认就好

使用namedtuple例子：
```
import collections
Point = collections.namedtuple('Point', ['x', 'y’])
p = Point(11, y=22)
print(p[0] + p[1])
x, y = p
print(p.x + p.y)
print(p)
```
deque 双向队列<br>

```
from collections import deque
d = deque('uvw')
d.append('xyz')
d.appendleft('rst')
```

Counter 计数器<br>

```
from collections import Counter
mystring = ['a','b','c','d','d','d','d','c','c','e']
# 取得频率最高的前三个值
cnt = Counter(mystring)
cnt.most_common(3)
cnt['b']
```

使用namedtuple重载运算符<br>
```
import numpy as np
'''
计算欧式距离
'''

vector1 = np.array([1, 2, 3])
vector2 = np.array([4, 5, 6])

op1 = np.sqrt(np.sum(np.square(vector1-vector2)))
op2 = np.linalg.norm(vector1-vector2)


from collections import namedtuple
from math import sqrt
Point = namedtuple('Ponit', ['x','y','z'])

class Vector(Point):
    def __init__(self, p1, p2, p3):
        super(Vector).__init__()
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    # 魔术方法，自定义减法
    def __sub__(self, other):
        tmp = (self.p1 - other.p1)**2+(self.p2 - other.p2)**2+(self.p3 - other.p3)**2
        return sqrt(tmp)

p1 = Vector(1, 2, 3)
p2 = Vector(4, 5, 6)

p1-p2
```

##### 四、函数：
函数是可调用对象<br>
函数需要关注什么
- 调用
- 作用域
- 参数
- 返回值

函数调用：<br>
如func是传递函数对象；func()是调用函数

变量作用域：<br>
高级语言对变量的使用：
- 变量声明
- 定义类型（分配内存空间大小）
- 初始化（赋值、填充内存）
- 引用（通过对象名称调用对象内存数据）
**Python 和高级语言有很大差别，在模块、类、函数中定义，才有作用域的概念。**

注意：<br>1、变量同名不同作用域；<br>2、变量查找顺序；<br>
Python 作用域遵循 LEGB 规则。<br>
LEGB 含义解释：
- L-Local(function)；函数内的名字空间
- E-Enclosing function locals；外部嵌套函数的名字空间（例如closure） 
- G-Global(module)；函数定义所在模块（文件）的名字空间
- B-Builtin(Python)；Python 内置模块的名字空间

```
# L G
x = 'Global'
def func2():
    x = 'Enclosing'
    def func3():
        x = 'Local'

        print (x) # Local
    func3()
print(x) # Global
func2()

# E
x = 'Global'
def func4():
    x = 'Enclosing'
    def func5():
        return x
    return func5

var = func4() # 返回函数对象，函数体形成闭包
print( var() ) # Enclosing

# B
print (dir (__builtins__) )
```
参数：<br>
参数分类：
- 必选参数
- 默认参数
- 可变参数
- 关键字参数
- 命名关键字参数

参数是函数-高阶函数<br>
有些函数比较简单，封装成 Lambda 表达式<br>

一般可变长参数定义如下：

```
def func(*args, **kargs):
    pass
```

kargs 获取关键字参数<br>
args 获取其他参数<br>

示例：
```
def func(*args, **kargs):
    print(f'args: {args}')
    print(f'kargs:{kargs}')

func(123, 'xz', name='xvalue')
# 结果：
# args:(123,'xz')
# kargs:{'name','xvalue'}
# func(123, 'xz', {'name':'xvalue', 'name2':'222'})
# func(123, 'xz', name='xvalue', name2='222')
```

偏函数<br>
functools.partial：返回一个可调用的 partial 对象<br>
使用方法：
```
partial(func,*args,**kw)
```

注意：<br>
- func 是必须参数
- 至少需要一个 args 或 kw 参数

```
# 偏函数
def add(x, y):
    return x + y

import functools
add_1 = functools.partial(add, 1)
add_1(10)

import itertools
g = itertools.count()
next(g)
next(g)
auto_add_1 = functools.partial(next, g)
auto_add_1()

sorted(['bob', 'about', 'Zoo', 'Credit'])
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)
```

⾼阶函数：<br>
高阶：参数是函数、返回值是函数<br>
常见的高阶函数：map、reduce、filter、apply<br>
apply 在 Python2.3 被移除，reduce 被放在 functools 包中<br>
推导式和生成器表达式可以替代 map 和 filter 函数<br>

map (函数， 序列) 将序列中每个值传入函数，处理完成返回为 map 对象

```
number = list(range(11))
def square(x):
return x**2
print(list(map(square, number)))
print(dir(map(square, number)))
```

filter (函数，序列)将序列中每个值传入函数，符合函数条件的返回为 filter 对象

```
# map
def square(x):
    return x**2
# map，将第二个参数中的值依次调用第一个参数（函数对象）
m = map(square, range(10))
next(m)
list(m)
# 等价功能的推导式
[square(x) for x in range(10)]
dir(m)

# reduce
# reduce(f, [x1, x2, x3]) = f(f(x1, x2), x3)
from functools import reduce
def add(x, y):
    return x + y

# 右侧中两两根据第一个参数操作
reduce(add, [1, 3, 5, 7, 9])
#25

# filter
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
```

Lambda 表达式:<br>
Lambda 只是表达式，不是所有的函数逻辑都能封装进去

```
k = lambda x:x+1
print(k(1))
```

Lambda 表达式后面只能有一个表达式
- 实现简单函数的时候可以使用 Lambda 表达式替代
- 使用高阶函数的时候一般使用 Lambda 表达式

**函数操作时经常用到两个标准库：functools，itertools；需要熟练掌握**

返回值和闭包：<br>
返回的关键字
- yield
- return


返回的对象
- 可调用对象--闭包(装饰器)


yield返回：生成器，返回可迭代对象<br>
return返回：正常值和闭包(装饰器)<br>

关于yield：
- 在函数中使用 yield 关键字，可以实现生成器。
- 生成器可以让函数返回可迭代对象。
- yield 和 return 不同，return 返回后，函数状态终止，yield保持函数的执行状态，返回后，函数回到之前保存的状态继续执行。
- 函数被 yield 会暂停，局部变量也会被保存。
- 迭代器终止时，会抛出 StopIteration 异常。

```
print([ i for i in range(0,11)]) 
替换为
print(( i for i in range(0,11)))
gennumber = ( i for i in range(0,11))
print(next(gennumber))
print(next(gennumber))
print(next(gennumber))
# print(list(gennumber))
print([i for i in gennumber ])

Iterables： 包含 __getitem__() 或 __iter__() 方法的容器对象
Iterator： 包含 next() 和 __iter__() 方法
Generator： 包含 yield 语句的函数
```


```
alist = [1, 2, 3, 4, 5]
hasattr( alist, '__iter__' )  # True       
hasattr( alist, '__next__' )  # False

for i in  alist:
    print(i)

# 结论一  列表是可迭代对象，或称作可迭代（iterable）,
#         不是迭代器（iterator）

# __iter__方法是 iter() 函数所对应的魔法方法，
# __next__方法是 next() 函数所对应的魔法方法

###########################

g = ( i for i in range(5))
g  #<generator object>

hasattr( g, '__iter__' )  # True    
hasattr( g, '__next__' )  # True

g.__next__()
next(g)
for i in g:
    print(i)

# 结论二 生成器实现完整的迭代器协议


##############################
# 类实现完整的迭代器协议

class SampleIterator:
    def __iter__(self):
        return self

    def __next__(self):
        # Not The End
        if ...:
            return ...
        # Reach The End
        else:
            raise StopIteration

# 函数实现完整的迭代器协议
def SampleGenerator():
    yield ...
    yield ...
    yield ...  # yield语句
# 只要一个函数的定义中出现了 yield 关键词，则此函数将不再是一个函数，
# 而成为一个“生成器构造函数”，调用此构造函数即可产生一个生成器对象。
```

yield from 是表达式，对 yield 进行了扩展

```
def ex1():
    yield 1
    yield 2
    return 3
    
def ex2():
    ex1_result = yield from ex1()
    print(f'ex1 : {ex1_result}')
    yield None
```

```
# Python3.3之后引入了新语法 yield from
def ex1():
    yield 1
    yield 2
    return 3

def ex2():
    ex1_result = yield from ex1()
    print(f'ex1 : {ex1_result}')
    yield None

gen1 = ex1()
gen1.send(None) # 1
gen1.send(None) # 2
gen1.send(None) # send 执行到return 返回 StopIteration: 3

for i in ex2():
    print(i)
# 1
# 2
# ex1:3
# None

##########################
def bottom():
# Returning the yield lets the value that goes up the call stack to come right back
# down.
    return (yield 42)

def middle():
    return (yield from bottom())

def top():
    return (yield from middle())

# Get the generator.
gen = top()
value = next(gen)
print(value) # Prints '42'.
try:
    value = gen.send(value * 2)
except StopIteration as exc:
    value = exc.value
print(value) # Prints '84'
```

itertools的三个常见无限迭代器:
```
import itertools

count = itertools.count()  # 计数器
next(count)
next(count)
next(count)

###############
cycle = itertools.cycle( ('yes', 'no') ) # 循环遍历
next(cycle)
next(cycle)
next(cycle)

###############
repeat = itertools.repeat(10, times=2)  # 重复
next(repeat)
next(repeat)
next(repeat)

```
有限迭代器:
```
for j in itertools.chain('ABC',[1, 2, 3]) :
    print(j)

```
yield from:

```
# Python3.3 引入了 yield from 
# PEP-380
def chain(*iterables):
    for it in iterables:
        for i in it:
            yield i

s = 'ABC'
t = [1, 2, 3]
list(chain(s, t))

def chain2(*iterables):
    for i in iterables:
        yield from i   # 替代内层循环

list(chain2(s, t))
```


关于生成器(迭代器)的注意事项：<br>

字典产生的迭代器，字典不可以插入新内容，否则失效报错<br>
列表尾部插入新内容，列表不会报错<br>
迭代器遍历结束，内容耗尽，迭代器就失效<br>
```
# 迭代器有效性测试
a_dict = {'a':1, 'b':2}
a_dict_iter = iter(a_dict)

next(a_dict_iter)

a_dict['c']=3

next(a_dict_iter)
# RuntimeError: 字典进行插入操作后，字典迭代器会立即失效

# 尾插入操作不会损坏指向当前元素的List迭代器,列表会自动变长

# 迭代器一旦耗尽，永久损坏
x = iter([ y for y in range(5)])
for i in x:
    i
x.__next__()
```

yield表达式：<br>
yield可以返回值，也可以接收参数；<br>
yield可以使程序暂停；<br>

```
def jumping_range(up_to):
    index = 0
    while index < up_to:
        jump = yield index # yield会让程序暂停，保留内部变量
        print(f'jump is {jump}')
        if jump is None:
            jump = 1   # next() 或者 send(None)
        index += jump 
        print(f'index is {index}')

if __name__ == '__main__':
    iterator = jumping_range(5)
    print(next(iterator)) # 0 会执行到 yield index，并且程序暂停
    print(iterator.send(2)) # 2 send 会执行方法中 jump = yield index 这句
    print(next(iterator)) # 3
    print(iterator.send(-1)) # 2
    for x in iterator: # 此处相当于 执行next和send
        print(x) # 3,
```


关于return：<br>
闭包示例：

```
#v1
def line_conf():
    b = 10
    def line(x):
        '''如果line()的定义中引用了外部的变量'''
        return 2*x+b
    return line       

b = -1
my_line = line_conf()
print(my_line(5))

# 编译后函数体保存的局部变量
print(my_line.__code__.co_varnames)
# 编译后函数体保存的自由变量
print(my_line.__code__.co_freevars)
# 自由变量真正的值
print(my_line.__closure__[0].cell_contents)

#v2
def line_conf(a, b):
    def line(x):
        return a*x + b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))

# v3
# 与line绑定的是line_conf()传入的a,b
a=100
b=200
def line_conf(a, b):
    def line(x):
        return a*x+b
    return line

line1 = line_conf(1, 1)
line2 = line_conf(4, 5)
print(line1(5), line2(5))




#####################
# 函数和对象比较有哪些不同的属性
# 函数还有哪些属性
def func(): 
    pass
func_magic = dir(func)

# 常规对象有哪些属性
class ClassA():
    pass
obj = ClassA()
obj_magic = dir(obj)

# 比较函数和对象的默认属性
set(func_magic) - set(obj_magic)
```

装饰器：<br>
增强而不改变原有函数<br>
装饰器强调函数的定义态而不是运行态<br>
装饰器语法糖的展开：

```
@decorate
def target():
    print('do something')
def target():
    print('do something') 
target = decorate(target)
```
target 表示函数<br>
target() 表示函数执行<br>
new = func 体现“一切皆对象”，函数也可以被当做对象进行赋值<br>

装饰器相当于对原有函数进行了加工改造，变成了新函数，执行时会执行加工改造后的函数逻辑；<br>

被装饰函数
- 被修饰函数带参数
- 被修饰函数带不定长参数
- 被修饰函数带返回值


```
# 装饰器在模块导入的时候自动运行
# testmodule.py
def decorate(func):
    print('running in modlue')
    def inner():
        return func()
    return inner

@decorate
def func2():
    pass
    
import testmodule
# from testmodule import func2
# 导入时会自动运行
```
框架中使用装饰器:

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
   return '<h1>hello world </h1>'

# app.add_url_rule('/', 'index')

if __name__ == '__main__':
   app.run(debug=True)



# 注册
@route('index',methods=['GET','POST'])
def static_html():
    return  render_template('index.html')

# 等效于
static_html = route('index',methods=['GET','POST'])(static_html)()


def route(rule, **options):
    def decorator(f):
        endpoint = options.pop("endpoint", None)
        # 使用类似字典的结构以'index'为key 以 method static_html  其他参数为value存储绑定关系
        self.add_url_rule(rule, endpoint, f, **options)
        return f
    return decorator

###############################

# 包装
def html(func):
    def decorator():
        return f'<html>{func()}</html>'
    return decorator

def body(func):
    def decorator():
        return f'<body>{func()}</body>'
    return decorator

@html
@body
def content():
    return 'hello world'

content()
```
针对于被装饰函数的装饰器例子：<br>
被装饰函数带定长参数的装饰器：<br>
装饰器内部函数参数要与被装饰函数参数一致
```
def outer(func):
    def inner(a,b):
        print(f'inner: {func.__name__}')
        print(a,b)
        func(a,b)
    return inner

@outer
def foo(a,b):
    print(a+b)
    print(f'foo: {foo.__name__}') # 此时已经替换成了装饰器内部函数inner
    
foo(1,2)
```

被装饰函数带不定长参数的装饰器：

```
def outer2(func):
    def inner2(*args,**kwargs):
        func(*args,**kwargs)
    return inner2

@outer2
def foo2(a,b,c):
    print(a+b+c)
    
foo2(1,3,5)
```

被装饰函数带返回值的装饰器：

```
def outer3(func):
    def inner3(*args,**kwargs):
        ###
        ret = func(*args,**kwargs)
        ###
        return ret
    return inner3

@outer3
def foo3(a,b,c):
    return (a+b+c)
    
print(foo3(1,3,5))
```
针对于装饰器的例子：<br>
带参数的装饰器：

```
def outer_arg(bar):
    def outer(func):
        def inner(*args,**kwargs):
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

# 相当于outer_arg('foo_arg')(foo)()
@outer_arg('foo_arg')
def foo(a,b,c):
    return (a+b+c)
    
print(foo(1,3,5))
```
多个装饰器（装饰器堆叠）：

```
@classmethod
@synchronized(lock)
def foo(cls):
    pass

# 上面你等价于如下：按照一定顺序
def foo(cls):
    pass
foo2 = synchronized(lock)(foo)
foo3 = classmethod(foo2)
foo = foo3
```

python自带的内置装饰器：<br>
1、@wraps()：
```
# functools.wraps
# @wraps接受一个函数来进行装饰
# 并加入了复制函数名称、注释文档、参数列表等等的功能
# 在装饰器里面可以访问在装饰之前的函数的属性
# @functools.wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)
# 用于在定义包装器函数时发起调用 update_wrapper() 作为函数装饰器。 
# 它等价于 一个偏函数 partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)。

from time import ctime,sleep
from functools import wraps
def outer_arg(bar):
    def outer(func):
        # 结构不变增加wraps
        @wraps(func)
        def inner(*args,**kwargs):
            print("%s called at %s"%(func.__name__,ctime()))
            ret = func(*args,**kwargs)
            print(bar)
            return ret
        return inner
    return outer

@outer_arg('foo_arg')
def foo(a,b,c):
    """  __doc__  """
    print(foo.__name__) # 注意，使用@wraps后此时打印的依然是foo，而不是inner
    return (a+b+c)
    
print(foo.__name__)
print(foo(1,2,3))
```

flask 使用@wraps()的案例:
```
from functools import wraps
 
def requires_auth(func):
    @wraps(func)
    def auth_method(*args, **kwargs):
        if not auth:
            authenticate()
        return func(*args, **kwargs)
    return auth_method

@requires_auth
def func_demo():
    pass
```
使用@wrap实现日志记录：

```
from functools import wraps
 
def logit(logfile='out.log'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = func.__name__ + " was called"
            print(log_string)
            with open(logfile, 'a') as opened_file:
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator
 
@logit()
def myfunc1():
    pass
 
myfunc1()
# Output: myfunc1 was called
 
@logit(logfile='func2.log')
def myfunc2():
    pass
 
myfunc2()
```
可以使用wrapt包替代@wraps
wrapt包 https://wrapt.readthedocs.io/en/latest/quick-start.html

```
#  @wrapt.decorator
#  def wrapper(func, instance, args, kwargs):

import wrapt

def with_arguments(myarg1, myarg2):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        return wrapped(*args, **kwargs)
    return wrapper

@with_arguments(1, 2)
def function():
    pass
```
2、lru_cache

```
# functools.lru_cache
# 《fluent python》的例子
# functools.lru_cache(maxsize=128, typed=False)有两个可选参数
# maxsize代表缓存的内存占用值，超过这个值之后，就的结果就会被释放
# typed若为True，则会把不同的参数类型得到的结果分开保存
import functools
@functools.lru_cache()
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)

if __name__=='__main__':
    import timeit
    print(timeit.timeit("fibonacci(6)", setup="from __main__ import fibonacci"))
```

类的装饰器 ：
装饰类
DataClass Python3.7 支持的新装饰器
其他内置类装饰器
- classmethod
- staticmethod
- property

```
# 装饰器对方法调用运行进行加工
from functools import wraps

class MyClass(object):
    def __init__(self, var='init_var', *args, **kwargs):
        self._v = var
        super(MyClass, self).__init__(*args, **kwargs)
    
    def __call__(self, func):
        # 类的函数装饰器
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            func_name = func.__name__ + " was called"
            print(func_name)
            return func(*args, **kwargs)
        return wrapped_function

def myfunc():
    pass

MyClass(100)(myfunc)()
##############################################
# 装饰器对方法调用次数计数
class Count(object):
    def __init__(self,func):
        self._func = func
        self.num_calls = 0
    
    def __call__(self, *args, **kargs):
        self.num_calls += 1
        print(f'num of call is {self.num_calls}')
        return self._func(*args, **kargs)

@Count
def example():
    print('hello')

example()
print(type(example))

#############################################
# 装饰器对类进行加工
def decorator(aClass):
    class newClass(object):
        def __init__(self, args):
            self.times = 0
            self.wrapped = aClass(args)
            
        def display(self):
            # 将runtimes()替换为display()
            self.times += 1
            print("run times", self.times)
            self.wrapped.display()
    return newClass

@decorator
class MyClass(object):
    def __init__(self, number):
        self.number = number
    # 重写display
    def display(self):
        print("number is",self.number)

six = MyClass(6)
for i in range(5):
    six.display()
```

```
# 函数参数观察器
import functools
def trace(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print(f, args, kwargs)
        result = f(*args, **kwargs)
        print(result)
    return decorated_function
@trace
def greet(greeting, name):
    return '{}, {}!'.format(greeting, name)

greet('better','me')
```

```
# Python3.7 引入 Data Class  PEP557

class MyClass:
    def __init__(self, var_a, var_b):
        self.var_a = var_a
        self.var_b = var_b

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            return False
        return (self.var_a, self.var_b) == (other.var_a, other.var_b)
        
var3 = MyClass('x','y')
var4 = MyClass('x','y')

var3 == var4

from dataclasses import dataclass
@dataclass
class MyClass:
    var_a: str
    var_b: str

var_1 = MyClass('x','y')
var_2 = MyClass('x','y')

# 不用在类中重新封装 __eq__

var_1 == var_2
# 存在的问题: var_a var_b不能作为类属性访问
```

##### 五、对象协议与鸭子类型：

这里说的协议是什么？是让Python这种动态类型语言实现多态的方式。
- 在面向对象编程中，协议是非正式的接口，是一组方法，但只是一种文档，语言不对施加特定的措施或者强制实现。
- 虽然协议是非正式的，在Python中，应该把协议当成正式的接口。
- Python中存在多种协议，用于实现鸭子类型（对象的类型无关紧要，只要实现了特定的协议（一组方法）即可）。
- 需要成为相对应的鸭子类型，那就实现相关的协议，即相关的__method__。例如实现序列协议(len__和__getitem)，这个类就表现得像序列。
- 协议是正式的，没有强制力，可以根据具体场景实现一个具体协议的一部分。例如，为了支持迭代，只需实现__getitem__，不需要实现__len__。
- 在Python文档中，如果看到“文件类对象“（表现得像文件的对象），通常说的就是协议，这个对象就是鸭子类型。这是一种简短的说法，意思是：“行为基本与文件一致，实现了部分文件接口，满足上下文相关需求的东西。”

鸭子类型(Duck Typing)
- When I see a bird that walks like a duck and swims like a duck and quacks like a duck, I call that bird a duck. - James Whitcomb Riley
- 不关注对象的类型，而关注对象的行为(方法)。它的行为是鸭子的行为，那么可以认为它是鸭子。

容器类型协议
1.__str__打印对象时，默认输出该方法的返回值
2.__getitem__和__setitem__和__delitem__字典索引操作
3.__iter__迭代器
4.__call__可调用对象协议

比较大小的协议
- __eq__方法
- __gt__方法

描述符协议和属性交互协议
- __get__方法
- __set__方法

可哈希对象
- __hash__方法

上下文管理器<br>
with 上下文表达式的用法<br>
使用__enter__和__exit__实现上下文管理器<br>

示例：
```
class Foo(object):
    # 用与方法返回
    def __str__(self):
        return '__str__ is called'

    # 用于字典操作
    def __getitem__(self, key):
        print(f'__getitem__ {key}') 
    
    def __setitem__(self, key, value):
        print(f'__setitem__ {key}, {value}')
    
    def __delitem__(self, key):
        print(f'__delitem__ {key}')

    # 用于迭代
    def __iter__(self):
        return iter([i for i in range(5)])


# __str__
bar = Foo()
print(bar)

# __XXitem__
bar['key1']
bar['key1']='value1'
del bar['key1']

# __iter__
for i in bar:
    print(i)
```

```
import math
print('The value of Pi is approximately %5.3f.' % math.pi)

print('{1} and {0}'.format('spam', 'eggs'))

print('The story of {0}, {1}, and {other}.'.format(
    'Bill', 'Manfred', other='Georg'))

firstname = 'yin'
lastname = 'wilson'
print('Hello, %s %s.' % (lastname, firstname))
print('Hello, {1} {0}.'.format(firstname, lastname))
print(f'Hello, {lastname} {firstname}.')

f'{ 2 * 5 }'

class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f'hello, {self.first_name} {self.last_name}.'

    def __repr__(self):
        return f'hello, {self.first_name} {self.last_name}.'

me = Person('yin', 'wilson')

print(f'{me}')
#str()函数：将值转化为适于人阅读的字符串的形式
#repr()函数：将值转化为供解释器读取的字符串形式
```

```
# typing 类型注解(type hint)

# 与鸭子类型相反的是静态类型，声明变量的时候就要指定类型，如果使用其他类型对变量赋值就会报错

def func(text: str, number: int) -> str:
    return text * number

func('a', 5)
```

##### 六、协程简介：
协程多数情况配合多线程；<br>

协程和线程的区别：
- 协程是异步的，线程是同步的
- 协程是非抢占式的，线程是抢占式的
- 线程是被动调度的，协程是主动调度的
- 协程可以暂停函数的执行，保留上一次调用时的状态，是增强型生成器
- 协程是用户级的任务调度，线程是内核级的任务调度
- 协程适用于 IO 密集型程序，不适用于 CPU 密集型程序的处理

python3.5 版本引入了 await 取代 yield from 方式

```
import asyncio
async def py35_coro():
    await stuff()
```

注意：
- 当使用await时候，要把它放到函数中；
- await 接收的对象必须是 awaitable 对象；

awaitable 对象定义了 __await__() 方法<br>

awaitable 对象有三类：
- 协程 coroutine
- 任务 Task
- 未来对象 Future


```
async def py35_func():
    await sth()
```



```
# 注意： await 接收的对象必须是awaitable对象
# awaitable 对象定义了__await__()方法
# awaitable 对象有三类
# 1 协程 coroutine
# 2 任务 Task
# 3 未来对象 Future
#####################
import asyncio
async def main():
    print('hello')
    await asyncio.sleep(3)
    print('world')

# asyncio.run()运行最高层级的conroutine
asyncio.run(main())
# hello
# sleep 3 second
# world

#################
# 协程调用过程： 
# 调用协程时，会被注册到ioloop，返回coroutine对象
# 用ensure_future 封装为Future对象
# 提交给ioloop
```

##### 七、aiohttp简介:
aiohttp是一个为Python提供异步HTTP<br> 客户端/服务端编程，基于asyncio(Python用于支持异步编程的标准库)的异步库。<br>
使用时需要安装<br>

核心功能：
- 同时支持客户端使用和服务端使用。
- 同时支持服务端WebSockets组件和客户端WebSockets组件，开箱即用呦。
- web服务器具有中间件，信号组件和可插拔路由的功能。

示例1 搭建客户端
```
import aiohttp
import asyncio

url = 'http://httpbin.org/get'

async def fetch(client, url):
    # get 方式请求url
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()

async def main():
    # 获取session对象
    async with aiohttp.ClientSession() as client:
        html = await fetch(client, url)
        print(html)

loop = asyncio.get_event_loop()
task = loop.create_task(main())
loop.run_until_complete(task)
# Zero-sleep 让底层连接得到关闭的缓冲时间
loop.run_until_complete(asyncio.sleep(0))
loop.close()
```
示例2：搭建http服务端

```
# Web Server
from aiohttp import web

# views
async def index(request):
    return web.Response(text='hello aiohttp')

# routes
def setup_routes(app):
    app.router.add_get('/', index) # 找到上方视图index

# app
app = web.Application()
setup_routes(app)
web.run_app(app, host='127.0.0.1', port=8080) # 此处才是启动应用


# 官方文档
# https://hubertroy.gitbooks.io/aiohttp-chinese-documentation/content/aiohttp%E6%96%87%E6%A1%A3/ServerTutorial.html
```

示例3 访问多个url

```
import aiohttp
import asyncio

urls = [
    'http://httpbin.org',
    'http://httpbin.org/get',
    'http://httpbin.org/ip',
    'http://httpbin.org/headers'
]

async def  crawler():
    async with aiohttp.ClientSession() as session:
        futures = map(asyncio.ensure_future, map(session.get, urls))
        for task in asyncio.as_completed(futures):
            print(await task)

if __name__ == "__main__":
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(asyncio.ensure_future(crawler()))
```

示例4 配合多进程

```
from multiprocessing import Pool
import asyncio
import time


async def test(time):
    await asyncio.sleep(time)

async def main(num):
    start_time = time.time()
    tasks = [asyncio.create_task(test(1)) for proxy in range(num)]
    [await t for t in tasks]
    print(time.time() - start_time)


def run(num):
    asyncio.run(main(num))


if __name__ == "__main__":
    start_time = time.time()
    p = Pool()
    for i in range(4):
        p.apply_async(run, args=(2500,))
    p.close()
    p.join()
    print(f'total {time.time() - start_time}')
```


