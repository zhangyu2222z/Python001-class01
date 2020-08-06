
### 本周主要学习内容如下：
#### 本周主要学习面向对象编程相关：面向对象基本概念，类，以及类的成员，描述器和属性描述符,以及常用几个设计模式，和mixin

##### 面向对象编程：
- 可以用现实世界中的对象和python的对象类比
- 对象是一个数据以及相关行为的集合
- python2中类为经典类，python3的类为新式类
- 类的两大成员：属性和方法

#### 一、属性：
类属性和对象属性<br>
类属性字段在内存中只保存一份<br>
对象属性在每个对象都保存一份<br>

示例：
```python
# GOD
class Human(object):
    # 静态字段
    live = True

    def __init__(self, name):
        # 普通字段
        self.name = name

man = Human('Adam')
woman = Human('Eve')

# 有静态字段,live属性
Human.__dict__
# 有普通字段,name属性
man.__dict__

# 实例可以使用普通字段也可以使用静态字段
man.name
man.live = False # 注意：此时man中live属性是实例字段
# 查看实例属性
man.__dict__ #普通字段有live变量
man.live
woman.live

# 类可以使用静态字段
Human.live

# 可以为类添加静态字段
Human.newattr = 1
dir(Human)
Human.__dict__

# 内置类型不能增加属性和方法，setattr(类，属性名，属性值)
# 注意：可以新建类，继承内置类型，在新建的类添加属性
setattr(list, 'newattr', 'value')
# TypeError

# 显示object类的所有子类
# __bases__获取父类
# __subclasses__获取子类
print( ().__class__.__bases__[0].__subclasses__() )

# I have a dream
class MyFirstClass:
    pass

a = MyFirstClass()
b = MyFirstClass()

# 不同内存地址，两个不同对象
type(a)
id(a)
id(b)

a.__class__()
b.__class__()

# 注意：类也是对象
c = MyFirstClass
d = c()
d.__class__()
```

对象属性说明：
```python
class Human2(object):
    # 人为约定不可修改 final
    _age = 0

    # 私有属性 private
    __fly = False

    # 魔术方法，不会自动改名
    # 如 __init__

# 自动改名机制
Human2.__dict__
```

#### 二、方法
对象方法说明：<br>
实例化方法：至少一个self参数，表示该方法对象<br>
类方法：至少一个cls参数，表示该方法的类 @classmethod<br>
静态方法：类调用，无参数 @staticmethod<br>

三种方法在内存中都归属于类<br>
注意：<br>
__init__是初始化函数，并不是构造，__init__实例化会调用；<br>
__new__是构造；有且有一个；<br>

类方法：
```python
# 让实例的方法成为类的方法
class Kls1(object):
    bar = 1
    def foo(self):
        print('in foo')
    # 使用类属性、方法
    @classmethod
    def class_foo(cls):
        print(cls.bar)
        print(cls.__name__)
        cls().foo()

Kls1.class_foo()

class Story(object):
    snake = 'Python'
    def __init__(self, name):
        self.name = name
    # 类的方法
    @classmethod
    def get_apple_to_eve(cls):
        return cls.snake

s = Story('anyone')
# get_apple_to_eve 是bound方法，查找顺序是先找s的__dict__是否有get_apple_to_eve,如果没有，查类Story;
print(s.get_apple_to_eve)
# 类和实例都可以使用
print(s.get_apple_to_eve())
print(Story.get_apple_to_eve())
# print(type(s).__dict__['get_apple_to_eve'].__get__(s,type(s)))
# print(type(s).__dict__['get_apple_to_eve'].__get__(s,type(s)) == s.get_apple_to_eve)
```
@classmethod方法中的cls总是当前类，比如父类和子类都有相同类方法，如果调用子类类方法，cls总是子类<br>
```python
class Kls3():
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
    
    @classmethod
    def pre_name(cls,name):
        fname, lname = name.split('-')
        return cls(fname, lname)
    
    def print_name(self):
        print(f'first name is {self.fname}')
        print(f'last name is {self.lname}')

me3 = Kls3.pre_name('wilson-yin')
me3.print_name()
```
@classmethod可以实现一部分构造函数的功能<br>

父子类对于类方法示例：<br>
简单来讲，对象调用方法时就是先从对象中找，找不到再从类中找，再找不到就会从类的父类找，一层一层往上找；<br>
```python
class Fruit(object):
    total = 0

    @classmethod
    def print_total(cls):
        print(cls.total)
        print(id(Fruit.total))
        print(id(cls.total))

    @classmethod
    def set(cls, value):
        print(f'calling {cls} ,{value}')
        cls.total = value

class Apple(Fruit):
    pass

class Orange(Fruit):
    pass

Apple.set(100)
Orange.set(200)
org=Orange()
org.set(300)
Apple.print_total()
Orange.print_total() 
```

静态方法：<br>
静态方法一般用来做功能上转化，比如，类型转换，逻辑判断,初始化实例<br>
示例：
```python
import datetime
class Story(object):
    snake = 'Python'
    def __init__(self, name):
        self.name = name
    # 静态的方法
    @staticmethod
    def god_come_go():
        if datetime.datetime.now().month % 2 :
             print('god is coming')
    
Story.god_come_go()

# 静态方法可以由类直接调用
# 因为不传入self 也不传入 cls ，所以不能使用类属性和实例属性
```

三种方法对比：
```python
class Foo(object):
    """类三种方法语法形式"""

    def instance_method(self):
        print("是类的实例方法，只能被实例对象调用")

    @staticmethod
    def static_method():
        print("是静态方法")

    @classmethod
    def class_method(cls):
        print("是类方法")

foo = Foo()
foo.instance_method()
foo.static_method()
foo.class_method()
print('----------------')
Foo.static_method()
Foo.class_method()

```

#### 三、描述器和属性描述符：
需要先了解__getattribute__和__getattr__:<br>
在类中，需要对实例获取属性这一行为进行操作，可以使用__getattribute__和__getattr__<br>
异同：<br>
都可以对实例属性进行获取拦截；<br>
__getattr__适用于未定义的属性；<br>
__getattribute__对所有属性的访问都会调用该方法；<br>


```python
__getattribute__()：
class Human2(object):  
    """
    getattribute对任意读取的属性进行截获
    """  
    def __init__(self):
        self.age = 18
    def __getattribute__(self,item):
        print(f' __getattribute__ called item:{item}')

h1 = Human2()

h1.age
h1.noattr

class Human2(object):  
    """
    拦截已存在的属性
    """  
    def __init__(self):
        self.age = 18
    def __getattribute__(self,item):
        print(f' __getattribute__ called item:{item}')
        return super().__getattribute__(item)
h1 = Human2()

print(h1.age)
# 存在的属性返回取值
print(h1.noattr)
# 不存在的属性返回 AttributeError
# AttributeError，访问不存在的属性
# 由__getattribute__(self,name)抛出

AttributeError捕获处理：
class Human2(object):    
    def __getattribute__(self, item):
        """
        将不存在的属性设置为100并返回,模拟getattr行为
        """
        print('Human2:__getattribute__')
        try:
            return super().__getattribute__(item)
        except Exception as e:
            self.__dict__[item] = 100
            return 100
h1 = Human2()

print(h1.noattr)

```
__getattr__()：
```python
class Human2(object):  
    """
    属性不在实例的__dict__中,__getattr__被调用
    """
    def __init__(self):
        self.age = 18

    def __getattr__(self, item): 
        print(f' __getattr__ called item:{item}')
        # 不存在的属性返回默认值 'OK'
        return 'OK'

h1 = Human2()

print(h1.age)
print(h1.noattr)

class Human2(object):  
    def __init__(self):
        self.age = 18

    def __getattr__(self, item): 
        # 对指定属性做处理:fly属性返回'superman',其他属性返回None
        self.item = item
        if self.item == 'fly':
            return 'superman'


h1 = Human2()

print(h1.age)
print(h1.fly)
print(h1.noattr)

# 属性不存在，返回None
```

__getattribute__()和__getattr__()同时存在时：
```python
class Human2(object):    
    """
    同时存在的调用顺序
    """
    def __init__(self):
        self.age = 18

    def __getattr__(self, item): 

        print('Human2:__getattr__')
        return 'Err 404 ,你请求的参数不存在'

    def __getattribute__(self, item):
        print('Human2:__getattribute__')
        return super().__getattribute__(item)

h1 = Human2()

# 如果同时存在，执行顺序是 __getattribute__ > __getattr__ > __dict__
__dict__如果也没找到，就会报AttributeError

print(h1.age)
print(h1.noattr)
# 注意输出，noattr的调用顺序
```
需要注意：
1、无论属性存在与否，都会调用__getattribute__，对调用性能有损耗；
2、使用__getattr__()时，__dict__如果依然没有属性，然后使用hasattr判断时，即使能返回true；因此很多内置方法可能出现不一致；

描述器：实现特定协议(描述符)的类 __getattribute__的底层原理是描述器；
属性描述符property：
property类需要实现 __get__方法， __set__方法 , __delete__方法

Django中property：django/db/models/base.py
```python
class Model(metaclass=ModelBase):
    def _get_pk_val(self, meta=None):
        meta = meta or self._meta
        return getattr(self,meta.pk.attname)
    def _set_pk_val(self, value):
        return setattr(self,self._meta.pk.attname,value)

    pk = property(_get_pk_val, _set_pk_val)
```
通过property形式，模拟实现__getattribute__描述器
```python
class Desc(object):
    """
    通过打印来展示描述器的访问流程
    """
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        print(f'__get__{instance} {owner}')
        return self.name

    def __set__(self, instance, value):
        print(f'__set__{instance} {value}')
        self.name = value

    def __delete__(self, instance):
        print(f'__delete__{instance}')
        del self.name

class MyObj(object):
    a = Desc('aaa')
    b = Desc('bbb')

my_object = MyObj()
print(my_object.a)

my_object.a = 456
print(my_object.a)
```

property装饰器：
@property 底层包括 fset，fget，fdelete，其实就是__get__方法， __set__方法 , __delete__方法
```python
class Human2(object):
    def __init__(self):
        self._gender = None
    # 将方法封装成属性
    @property
    def gender2(self):
        print(self._gender)

    # 支持修改
    @gender2.setter
    def gender2(self,value):
        self._gender = value

    # 支持删除
    @gender2.deleter
    def gender2(self):
        del self._gender


h = Human2()
# 相当于把方法封装成一个属性
h.gender = 'F'
h.gender
del h.gender
```
另一种property写法
gender  = property(get_, set_, del_, '属性描述信息')
```python
class C:
    def __init__(self):
        self._x = None
 
    def getx(self):
        return self._x
 
    def setx(self, value):
        self._x = value
 
    def delx(self):
        del self._x
 
    x = property(getx, setx, delx, "I'm the 'x' property.")
```

被装饰函数建议使用相同的gender2
使用setter 并不能真正意义上实现无法写入，gender被改名为 _Article__gender

property本质并不是函数，而是特殊类（实现了数据描述符的类）
如果一个对象同时定义了__get__()和__set__()方法，则称为数据描述符，
如果仅定义了__get__()方法，则称为非数据描述符，如__getattribute__

property的优点：
- 1 代码更简洁，可读性、可维护性更强。
- 2 更好的管理属性的访问。
- 3 控制属性访问权限，提高数据安全性。



#### 四、面向对象-继承：
面向对象特性：封装、继承、多态
python支持单继承， 多继承

python3中所有类都继承自object，一切皆对象，类也是对象

新式类和经典类区别：
当前类或者父类继承了object类，那么该类为新式类，否则为经典类

object和type关系：
- object和type都属于type类(class type)
- type类由type元类自身创建，object类由type类创建
- object的父类为空，没有继承任何类
- type的父类为object类(class object)

补充：
- type 的类型是 type，type 在类型关系的顶端。
- object 的父类为 ()，说明 object 不继承任何类，object在继承关系的顶端。
- object 是一个类。
- object 类是 type 类的实例。
- type 类继承自 object 类。
- 像 type 这种类，实例化后的对象是类，这种类称作 原类(metaclass) 

```python
In [27]: type.__class__                                                  
Out[27]: type
In [28]: type.__bases__                                              
Out[28]: (object,)
In [29]: object.__class__                                            
Out[29]: type
In [30]: object.__bases__                                       
Out[30]: ()
```
继承方式：
单一继承，多重继承，菱形继承(钻石继承)，继承机制MRO，MRO的C3算法

```python
# 父类
class People(object):
    def __init__(self):
        self.gene = 'XY'
    def walk(self):
        print('I can walk')

# 子类
class Man(People):
    def __init__(self,name):
        self.name = name
    def work(self):
        print('work hard')

class Woman(People):
    def __init__(self,name):
        self.name = name    
    def shopping(self):
        print('buy buy buy')

p1 = Man('Adam')
p2 = Woman('Eve')

# 问题1 gene有没有被继承？
# 没有，因为子类中__init__只有name属性，会覆盖父类中gene属性；
子类继承父类属性：
# 父类
class People(object):
    def __init__(self, name):
        self.gene = 'XY'
        # 假设人人都有名字
        self.name = name
    def walk(self):
        print('I can walk')

# 子类
class Man(People):
    def __init__(self,name):
        # 找到Man的父类People，把类People的对象转换为类Man的对象
        super().__init__(name)

    def work(self):
        print('work hard')

# 问题2 People的父类是谁？
# object

# 问题3 能否实现多重层级继承
# 可以

# 问题4 能否实现多个父类同时继承
# 可以
class Son(Man, Woman):
    pass
```
钻石继承：
```python
class BaseClass(object):
    num_base_calls = 0
    def call_me(self):
        print ("Calling method on Base Class")
        self.num_base_calls += 1

class LeftSubclass(BaseClass):
    num_left_calls = 0
    def call_me(self):
        print ("Calling method on Left Subclass")
        self.num_left_calls += 1

class RightSubclass(BaseClass):
    num_right_calls = 0
    def call_me(self):
        print("Calling method on Right Subclass")
        self.num_right_calls += 1

class Subclass(LeftSubclass,RightSubclass):
    pass

a = Subclass()
a.call_me()

print(Subclass.mro())

子类调用方法顺序如下：
# 广度优先， 另外Python3 中不加(object)也是新式类，但是为了代码不会误运行在python2下产生意外结果，仍然建议增加
# >>> Subclass.mro()
# [<class '__main__.Subclass'>, <class '__main__.LeftSubclass'>, <class '__main__.RightSubclass'>, <class '__main__.BaseClass'>, <class 'object'>]

#  如果修改RightSubclass 的 父类为 Object，则调用顺序：
# >>> Subclass.mro()
# [<class '__main__.Subclass'>, <class '__main__.LeftSubclass'>, <class '__main__.BaseClass'>, <class '__main__.RightSubclass'>, <class 'object'>]
```
基本上调用顺序：按照继承顺序的从左到右，父类深度顺序的从下到上；
经典类调用顺序则是深度优先；


有向无环路图(DAG)：<br>
DAG原本为一种数据结构，因为DAG的拓扑结构带来的优异特性，经常被用于处理动态规则，寻求最短路径；<br>
也可以按照 有向无环路图(DAG)方式确定继承关系，根据入度为0，从左到右的优先顺序，确定继承关系；<br>

方法重载：
python中没有实现重载
```pyhton
class  Klass(object):
    def A(self):
        pass
    def A(self,a, b):
        print(f'{a},{b}')

inst = Klass()
# 没有实现重载
inst.A()
```

五、设计原则和设计模式：
SOLID五大设计原则：
- 单一责任原则 The Single Responsibility Principle
- 开放封闭原则 The Open Closed Principle
- 里氏替换原则 The Liskov Substitution Principle
- 依赖倒置原则 The Dependency Inversion Principle
- 接口分离原则 The Interface Segregation Principle


```
构造函数：__new__<br>
__init__ 和 __new__ 的区别：<br>
__new__ 是实例创建之前被调用，返回该实例对象，是静态方法<br>
__init__ 是实例对象创建完成后被调用，是实例方法<br>
__new__ 先被调用，__init__ 后被调用<br>
__new__ 的返回值（实例）将传递给 __init__ 方法的第一个参数，__init__ 给这个实例设置相关参数<br>
```


常用设计模式：
1、单例：对象只存在一个实例
```python
# 装饰器实现单实例模式
def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton 
class MyClass:
    pass

m1 = MyClass()
m2 = MyClass()
print(id(m1))
print(id(m2))
```
使用构造创建，单线程单例
```python
class Singleton2(object):
	__isinstance = False  # 默认没有被实例化
	def __new__(cls, *args, **kwargs):
		if cls.__isinstance:  
			return cls.__isinstance  # 返回实例化对象
		cls.__isinstance = object.__new__(cls)  # 实例化
		return cls.__isinstance
```

object定义了一个名为Singleton的单例，它满足单例的3个需求：
- 一是只能有一个实例；
- 二是它必须自行创建这个实例；
- 三是它必须自行向整个系统提供这个实例。

适合多线程情况的单例：

```
import threading
class Singleton(object):
    objs = {}
    objs_locker = threading.Lock()
    def __new__(cls, *args, **kargs):
        if cls in cls.objs:
            return cls.objs[cls]
        cls.objs_locker.acquire()
        try:
            if cls in cls.objs: ## double check locking
                return cls.objs[cls]
            cls.objs[cls] = object.__new__(cls)
        finally:
            cls.objs_locker.release()
```
利用经典的双检查锁机制，确保了在并发环境下Singleton的正确实现。
但这个方案并不完美，至少还有以下两个问题：
- 如果Singleton的子类重载了__new__()方法，会覆盖或者干扰Singleton类中__new__()的执行，
- 虽然这种情况出现的概率极小，但不可忽视。
- 如果子类有__init__()方法，那么每次实例化该Singleton的时候，
- __init__()都会被调用到，这显然是不应该的，__init__()只应该在创建实例的时候被调用一次。
- 这两个问题当然可以解决，比如通过文档告知其他程序员，子类化Singleton的时候，请务必记得调用父类的__new__()方法；
- 而第二个问题也可以通过偷偷地替换掉__init__()方法来确保它只调用一次。
- 但是，为了实现一个单例，做大量的、水面之下的工作让人感觉相当不Pythonic。
- 这也引起了Python社区的反思，有人开始重新审视Python的语法元素，发现模块采用的其实是天然的单例的实现方式。
- 所有的变量都会绑定到模块。
- 模块只初始化一次。

import机制是线程安全的（保证了在并发状态下模块也只有一个实例）。
当我们想要实现一个游戏世界时，只需简单地创建World.py就可以了。

```
# World.py
import Sun
def run():
    while True:
        Sun.rise()
        Sun.set()

# main.py
import World
World.run()

```

2、工厂模式：
简单工厂模式
```
class Human(object):
    def __init__(self):
        self.name = None
        self.gender = None

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

class Man(Human):
    def __init__(self, name):
        print(f'Hi,man {name}')

class Woman(Human):
    def __init__(self, name):
        print(f'Hi,woman {name}')

class Factory:
    def getPerson(self, name, gender):
        if gender == 'M':
            return Man(name)
        elif gender == 'F':
            return Woman(name)
        else:
            pass

if __name__ == '__main__':
    factory = Factory()
    person = factory.getPerson("Adam", "M")



# 返回在函数内动态创建的类
def factory2(func):
    class klass: pass
    #setattr需要三个参数:对象、key、value
    setattr(klass, func.__name__, func)
    return klass

def say_foo(self): 
    print('bar')

Foo = factory2(say_foo)
foo = Foo()
foo.say_foo()
```
类工厂模式：

```
# 返回在函数内动态创建的类
def factory2(func):
    class klass: pass
    #setattr需要三个参数:对象、key、value
    # 给klass类添加一个方法
    setattr(klass, func.__name__, func)
    
    # 添加一个类方法 调用时：Foo.say_foo()
    # setattr(klass, func.__name__, classmethod(func))
    
    return klass

def say_foo(self): 
    print('bar')

# 返回一个类
Foo = factory2(say_foo)
# 创建这个类的实例
foo = Foo()
foo.say_foo()
```

元类：

- 元类是关于类的类，是类的模板。
- 元类是用来控制如何创建类的，正如类是创建对象的模板一样。
- 元类的实例为类，正如类的实例为对象
- 创建元类的两种方法
- 1. class
- 2. type
- type（类名，父类的元组（根据继承的需要，可以为空，包含属性的字典（名字和值））

使用type元类创建类：
```
def hi():
    print('Hi metaclass')

# type的三个参数:类名、父类的元组、类的成员
Foo = type('Foo',(),{'say_hi':hi})
foo = Foo
foo.say_hi()
# 元类type首先是一个类，所以比类工厂的方法更灵活多变，可以自由创建子类来扩展元类的能力
```

重点理解：使用元类创建自定义字典。初始化带有一些自定义功能
```
def pop_value(self,dict_value):
    for key in self.keys():
        if self.__getitem__(key) == dict_value:
            self.pop(key)
            break

# 元类要求,必须继承自type    
class DelValue(type):
    # 元类要求，必须实现new方法
    def __new__(cls,name,bases,attrs):
        attrs['pop_value'] = pop_value
        return type.__new__(cls,name,bases,attrs)
 
class DelDictValue(dict,metaclass=DelValue):
    # python2的用法，在python3不支持
    # __metaclass__ = DelValue
    pass

d = DelDictValue()
d['a']='A'
d['b']='B'
d['c']='C'
d.pop_value('C')
for k,v in d.items():
    print(k,v)
```



抽象基类
抽象基类（abstract base class，ABC）用来确保派生类实现了基类中的特定方法。
使用抽象基类的好处：
-   避免继承错误，使类层次易于理解和维护。
-   无法实例化基类。
-   如果忘记在其中一个子类中实现接口方法，要尽早报错。

```
from abc import ABCMeta, abstractmethod
class Base(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass
    @abstractmethod
    def bar(self):
        pass

class Concrete(Base):
    def foo(self):
        pass

c = Concrete() # TypeError
```

minin模式：
在程序运行过程中，重定义类的继承，即动态继承。好处：
- 可以在不修改任何源代码的情况下，对已有类进行扩展
- 进行组件的划分

```
def mixin(Klass, MixinKlass):
    Klass.__bases__ = (MixinKlass,) + Klass.__bases__

class Fclass(object):
    def text(self):
        print('in FatherClass')

class S1class(Fclass):
    pass

class MixinClass(object):
    def text(self):
        # 注意！：此处的super，执行mixin(S1class, MixinClass)后，
        # 再执行s1.text()时，会先找S1class的text，找不到会
        # 找MixinClass的text，此时方法中执行super().text()；
        # 其中的super指的是S1class的父类，并不是MixinClass的
        # 父类，因此super().text()实际是执行Fclass的text
        return super().text()
        # print('in MixinClass')

class S2class(S1class, MixinClass):
    pass

print(f' test1 : S1class MRO : {S1class.mro()}')
s1 = S1class()
s1.text()

mixin(S1class, MixinClass)
print(f' test2 : S1class MRO : {S1class.mro()}')
s1 = S1class()
s1.text()


print(f' test3 : S2class MRO : {S2class.mro()}')
s2 = S2class()
s2.text()

```

《Python GUI Programming with Tkinter》
Mixin类无法单独使用，必须和其他类混合使用，来加强其他类

```
class Displayer():
    def display(self, message):
        print(message)

class LoggerMixin():
    def log(self, message, filename='logfile.txt'):
        with open(filename, 'a') as fh:
            fh.write(message)

    def display(self, message):
        # 此处super会按照MRO顺序找LoggerMixin之后的类，也就是Displayer，
        # 然后执行Displayer的display
        # 而self指的是MySubClass的实例，所以self.log(message)是执行
        # MySubClass的log，而其中又执行了super().log，再按照MRO顺序
        # 会调用LoggerMixin的log
        super(LoggerMixin, self).display(message)
        self.log(message)

class MySubClass(LoggerMixin, Displayer):
    def log(self, message):
        super().log(message, filename='subclasslog.txt')

subclass = MySubClass()
subclass.display("This string will be shown and logged in subclasslog.txt")
print(MySubClass.mro())
```
注意python的super的意义和java中super并不完全一样，python的super是有按照MRO顺序的含义，并非完全的找父类；