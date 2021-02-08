"""
面向对象技术简介
类(Class): 用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。
方法：类中定义的函数。
类变量：类变量在整个实例化的对象中是公用的。类变量定义在类中且在函数体之外。类变量通常不作为实例变量使用。
数据成员：类变量或者实例变量用于处理类及其实例对象的相关的数据。
方法重写：如果从父类继承的方法不能满足子类的需求，可以对其进行改写，这个过程叫方法的覆盖（override），也称为方法的重写。
局部变量：定义在方法中的变量，只作用于当前实例的类。
实例变量：在类的声明中，属性是用变量来表示的，这种变量就称为实例变量，实例变量就是一个用 self 修饰的变量。
继承：即一个派生类（derived class）继承基类（base class）的字段和方法。继承也允许把一个派生类的对象作为一个基类对象对待。例如，有这样一个设计：一个Dog类型的对象派生自Animal类，这是模拟"是一个（is-a）"关系（例图，Dog是一个Animal）。
实例化：创建一个类的实例，类的具体对象。
对象：通过类定义的数据结构实例。对象包括两个数据成员（类变量和实例变量）和方法。
和其它编程语言相比，Python 在尽可能不增加新的语法和语义的情况下加入了类机制。
Python中的类提供了面向对象编程的所有基本功能：类的继承机制允许多个基类，派生类可以覆盖基类中的任何方法，方法中可以调用基类中的同名方法。
对象可以包含任意数量和类型的数据。
"""

"""
类定义
语法格式如下：
class ClassName:
    <statement-1>
    .
    .
    .
    <statement-N>
类实例化后，可以使用其属性，实际上，创建一个类之后，可以通过类名访问其属性。
类对象
类对象支持两种操作：属性引用和实例化。
属性引用使用和 Python 中所有的属性引用一样的标准语法：obj.name。
类对象创建后，类命名空间中所有的命名都是有效属性名。所以如果类定义是这样:
"""
# class MyClass:
#     """一个简单的类实例"""
#     i = 123454
#     def f(self):
#         return 'hello word'
#
# # 实例化类
# x = MyClass()
#
# # 访问类的属性和方法
# print("MyClass 类的属性 i 为：", x.i)
# print("MyClass 类的方法 f 输出为：", x.f())
# -----------------------------------------------
"""
类有一个名为 __init__() 的特殊方法（构造方法），该方法在类实例化时会自动调用，像下面这样：
def __init__(self):
    self.data = []
类定义了 __init__() 方法，类的实例化操作会自动调用 __init__() 方法。如下实例化类 MyClass，对应的 __init__() 方法就会被调用:
x = MyClass()
当然， __init__() 方法可以有参数，参数通过 __init__() 传递到类的实例化操作上。例如:
"""
"""
class Complex:
    def __init__(self, realpart, imagepart):
        self.r = realpart
        self.i = imagepart
x = Complex(3.0, -4.5)
print(x.i, x.r)
-----------------------------------------------
self代表类的实例，而非类
类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的第一个参数名称, 按照惯例它的名称是self。

class Test:
    def prt(self):
        print(self)
        print(self.__class__)
t = Test()
t.prt()
以上实例执行结果为：

< __main__.Test instance at 0x100771878 >
__main__.Test

从执行结果可以很明显的看出，self代表的是类的实例，代表当前对象的地址，而
self.class 则指向类。self不是python关键字，我们把他换成runoob也是可以正常执行的:
class Test:
    def prt(runoob):
        print(runoob)
        print(runoob.__class__)
t = Test()
t.prt()
以上实例执行结果为：
< __main__.Test instance at 0x100771878 >
__main__.Test
"""
# -----------------------------------------------
"""
类的方法
在类的内部，使用def 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数self, 且为第一个参数，self
代表的是类的实例。
"""
# class people:
#     name = ''
#     age = 0
#     __weight = 0
#     def __init__(self,n , a, w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#     def speak(self):
#         print("%s 说: 我 %d 岁,体重 %d 斤！" %(self.name, self.age, self.__weight))
#
# p = people('xiaoming',10,100)
# p.speak()
# -----------------------------------------------
"""
继承
Python 同样支持类的继承，如果一种语言不支持继承，类就没有什么意义。派生类的定义如下所示:
class DerivedClassName(BaseClassName1):
    <statement-1>
    .
    .
    .
    <statement-N>
BaseClassName（示例中的基类名）必须与派生类定义在一个作用域内。除了类，还可以用表达式，基类定义在另一个模块中时这一点非常有用:
class DerivedClassName(modname.BaseClassName):
"""
# 类定义
# class people:
#     # 定义基本属性
#     name = ''
#     age = 0
#     # 定义私有属性,私有属性在类外部无法直接进行访问
#     __weight = 0
#     # 定义构造方法
#     def __init__(self, n, a, w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#     def speak(self):
#         print("%s 说: 我 %d 岁。" %(self.name, self.age))
#
# # 单继承示例
# class student(people):
#     grade = ''
#     def __init__(self, n, a, w, g):
#         # 调用父类的构函
#         people.__init__(self, n, a, w)
#         self.grade = g
#     # 覆写父类的方法
#     def speak(self):
#         print("%s 说: 我 %d 岁了，我在读 %d 年级" %(self.name, self.age, self.grade))
#
# s = student('ken',10,60,3)
# s.speak()
# print(s.name)
# print(s.age)
# print(s.grade)
# -----------------------------------------------
"""
多继承
Python同样有限的支持多继承形式。多继承的类定义形如下例:
class DerivedClassName(Base1, Base2, Base3):
    <statement-1>
    .
    .
    .
    <statement-N>
需要注意圆括号中父类的顺序，若是父类中有相同的方法名，而在子类使用时未指定，
python从左至右搜索 即方法在子类中未找到时，从左到右查找父类中是否包含方法。
"""
#类定义
# class people:
#     # 定义基本属性
#     name = ''
#     age = 0
#     # 定义私有属性,私有属性在类外部无法直接进行访问
#     __weight = 0
#     # 定义构造方法
#     def __init__(self, n, a, w):
#         self.name = n
#         self.age = a
#         self.__weight = w
#     def speak(self):
#         print("%s 说: 我 %d 岁。" %(self.name, self.age))
#
# #单继承示例
# class student(people):
#     grade = ''
#     def __init__(self, n, a, w, g):
#         # 调用父类的构函
#         people.__init__(self, n, a, w)
#         self.grade = g
#     # 覆写父类的方法
#     def speak(self):
#         print("%s 说: 我 %d 岁了，我在读 %d 年级" %(self.name, self.age, self.grade))
#
# # 另一个类，多重继承之前的准备
# class speaker():
#     topic = ''
#     name = ''
#     def __init__(self, n, t):
#         self.name = n
#         self.topic = t
#     def speak(self):
#         print("我叫 %s，我是一个演说家，我演讲的主题是 %s" %(self.name, self.topic))
#
# # 多重继承
# class sample(speaker, student):
#     a = ''
#     def __init__(self, n, a, w,g,t):
#         student.__init__(self, n, a, w, g)
#         speaker.__init__(self, n, t)
#
# test = sample("Tim", 25, 80, 4, "Python")
# test.speak()   # 方法名同，默认调用的是在括号中排前地父类的方法
# -----------------------------------------------
"""
方法重写
如果你的父类方法的功能不能满足你的需求，你可以在子类重写你父类的方法，实例如下：
super() 函数是用于调用父类(超类)的一个方法。
super() 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，
但是如果使用多继承，会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。
MRO 就是类的方法解析顺序表, 其实也就是继承父类方法时的顺序表。
语法
以下是 super() 方法的语法:
super(type[, object-or-type])
参数
type -- 类。
object-or-type -- 类，一般是 self
Python3.x 和 Python2.x 的一个区别是: Python 3 可以使用直接使用 super().xxx 代替 super(Class, self).xxx :

"""
# class parent:
#     def myMethod(self):
#         print('调用父类方法')
#
# class child(parent):
#     def myMethod(self):
#         print('调用子类方法')
#
# c = child()
# c.myMethod()
# super(child, c).myMethod()
# -----------------------------------------------
"""
情况一：子类需要自动调用父类的方法：子类不重写__init__()方法，实例化子类后，会自动调用父类的__init__()的方法。
情况二：子类不需要自动调用父类的方法：子类重写__init__()方法，实例化子类后，将不会自动调用父类的__init__()的方法。
情况三：子类重写__init__()方法又需要调用父类的方法：使用super关键词：
"""
# class A:
#     def add(self, x):
#         y = x + 1
#         print(y)
# class B(A):
#     def add(self, x):
#         super().add(x)
#
# b= B()
# print(b)
# b.add(2)
# -----------------------------------------------
"""
我们在学习 Python 类的时候，总会碰见书上的类中有 __init__() 这样一个函数，很多同学百思不得其解，其实它就是 Python 的构造方法。
构造方法类似于类似 init() 这种初始化方法，来初始化新创建对象的状态，在一个对象呗创建以后会立即调用，比如像实例化一个类：
f = FooBar()
f.init()
使用构造方法就能让它简化成如下形式：
f = FooBar()
你可能还没理解到底什么是构造方法，什么是初始化，下面我们再来举个例子：
class FooBar:
    def __init__(self):
        self.somevar = 42

>>>f = FooBar()
>>>f.somevar
我们会发现在初始化 FooBar 中的 somevar 的值为 42 之后，实例化直接就能够调用 somevar 的值；如果说你没有用构造方法初始化值得话，就不能够调用，明白了吗？
在明白了构造方法之后，我们来点进阶的问题，那就是构造方法中的初始值无法继承的问题。
"""
# class Bird:
#     def __init__(self):
#         self.hungry = True
#     def eat(self):
#         if self.hungry:
#             print('Ahahahah')
#         else:
#             print('No thanks!')
#
# class SongBird(Bird):
#     def __init__(self):
#         # Bird.__init__(self)
#         # 原理：在调用了一个实例的方法时，该方法的self参数会自动绑定到实例上（称为绑定方法）；
#         # 如果直接调用类的方法（比如Bird.__init__），那么就没有实例会被绑定，可以自由提供需
#         # 要的self参数（未绑定方法）。
#         super(SongBird, self).__init__()
#         # 使用super函数（只在新式类中有用）,原理：它会查找所有的超类，以及超类的超类，直到找到所需的特性为止。
#         self.sound = 'Squawk'
#     def sing(self):
#         print(self.sound)
#
# sb = SongBird()
# sb.sing()
# sb.eat()  # 报错，因为 SongBird 中没有 hungry 特性
# -----------------------------------------------
"""
经典的菱形继承案例，BC 继承 A，然后 D 继承 BC，创造一个 D 的对象。
     ---> B ---
A --|          |--> D
     ---> C ---
使用 super() 可以很好地避免构造函数被调用两次。
"""
# class A():
#     def __init__(self):
#         print('enter A')
#         print('leave A')
#
# class B(A):
#     def __init__(self):
#         print('enter B')
#         super().__init__()
#         print('leave B')
#
# class C(A):
#     def __init__(self):
#         print('enter C')
#         super().__init__()
#         print('leave C')
#
# class D(B, C):
#     def __init__(self):
#         print('enter D')
#         super().__init__()
#         print('leave D')
# d = D()
# -----------------------------------------------
"""
Python3 中继承遵循广度优先原则：
"""
# class A:
#     def __init__(self):
#         print('Enter A')
#         print(self)
#         print('Leave A')
#
# class B(A):
#     def __init__(self):
#         print('Enter B')
#         print(self)
#         super(B, self).__init__()
#         print('Leave B')
#
# class C(A):
#     def __init__(self):
#         print('Enter C')
#         print(self)
#         super().__init__()
#         print('Leave C')
#
# class D(B, C):
#     def __init__(self):
#         print('Enter D')
#         print(self)
#         super().__init__()
#         print('Leave D')
# """
# 1.创建 D 类的对象 d 时，自动调用 D 类的初始化方法 __init()__，此时的 self 指向 D 类创建的实例对象 d；
# 2.调用原则：D->B->C->A
# 3.在调用到 B 时，首先输出 “Enter B”，但是运行到父类 A 的初始化方法时不立即调用，反而时转向广度优先级高的 C 类，因为 A 类对于 B 类来说是深度遍历。
# """
# d = D()
# -----------------------------------------------
"""
类属性与方法
类的私有属性
__private_attrs：两个下划线开头，声明该属性为私有，不能在类的外部被使用或直接访问。在类内部的方法中使用时 self.__private_attrs。
类的方法
在类的内部，使用 def 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数 self，且为第一个参数，self 代表的是类的实例。
self 的名字并不是规定死的，也可以使用 this，但是最好还是按照约定是用 self。
类的私有方法
__private_method：两个下划线开头，声明该方法为私有方法，只能在类的内部调用 ，不能在类的外部调用。self.__private_methods。
实例
类的私有属性实例如下：
"""
# class JustCounter:
#     __sevretCount = 0
#     publicCount = 0
#
#     def count(self):
#         self.__sevretCount += 1
#         self.publicCount += 1
#         print(self.__sevretCount)
#
# counter = JustCounter()
# counter.count()
# counter.count()
# print(counter.publicCount)
# # print(counter.__secretCount)    # 报错，实例不能访问私有变量
# -----------------------------------------------
"""
类的私有方法实例如下：
"""
# class Site:
#     def __init__(self, name, url):
#         self.name = name
#         self.__url = url
#
#     def who(self):
#         print('name  : ', self.name)
#         print('url   : ', self.__url)
#
#     def __foo(self):
#         print('这是私有方法')
#
#     def foo(self):
#         print('这是公共方法')
#         self.__foo()
#
# x = Site('菜鸟教程', 'www.runoob.com')
# x.who()
# x.foo()
# # x.__foo()
# Traceback (most recent call last):
#   File "C:\python\class.py", line 412, in <module>
#     x.__foo()
# AttributeError: 'Site' object has no attribute '__foo'
# -----------------------------------------------
"""
类的专有方法：
__init__ : 构造函数，在生成对象时调用
__del__ : 析构函数，释放对象时使用
__repr__ : 打印，转换
__setitem__ : 按照索引赋值
__getitem__: 按照索引获取值
__len__: 获得长度
__cmp__: 比较运算
__call__: 函数调用
__add__: 加运算
__sub__: 减运算
__mul__: 乘运算
__truediv__: 除运算
__mod__: 求余运算
__pow__: 乘方
所有专有方法中，__init__()要求无返回值，或者返回 None。而其他方法，如__str__()、__add__()等，一般都是要返回值的
运算符重载
Python同样支持运算符重载，我们可以对类的专有方法进行重载，实例如下：
"""
# class Vector:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     def __str__(self):
#         return 'Vector (%d, %d)' % (self.a, self.b)
#
#     def __add__(self, other):
#         return Vector(self.a + other.a, self.b + other.b)
#
# v1 = Vector(2, 10)
# v2 = Vector(5,-2)
# print(v1 + v2)
# -----------------------------------------------
"""
针对 __str__ 方法给出一个比较直观的例子：
"""
# class people:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     # 如果没有重载str函数的话输出的就是一串实例地址的字符串：
#     # <__main__.people object at 0x0000024AFDB63FD0>
#     def __str__(self):
#         return '这个人的名字是%s,已经有%d岁了！' % (self.name, self.age)
#
# a = people('孙悟空', 999)
# print(a)
# -----------------------------------------------
"""
Python3 中类的静态方法、普通方法、类方法
静态方法: 用 @staticmethod 装饰的不带 self 参数的方法叫做静态方法，类的静态方法可以没有参数，可以直接使用类名调用。
普通方法: 默认有个self参数，且只能被对象调用。
类方法: 默认有个 cls 参数，可以被类和对象调用，需要加上 @classmethod 装饰器。
"""
# class Classname:
#     @staticmethod
#     def fun():
#         print('静态方法')
#
#     @classmethod
#     def a(cls):
#         print('类方法')
#
#     # 普通方法
#     def b(self):
#         print('普通方法')
#
# Classname.fun()
# Classname.a()
#
# C = Classname()
# C.fun()
# C.a()
# C.b()
# -----------------------------------------------
"""
反向运算符重载：
__radd__: 加运算
__rsub__: 减运算
__rmul__: 乘运算
__rdiv__: 除运算
__rmod__: 求余运算
__rpow__: 乘方
复合重载运算符：
__iadd__: 加运算
__isub__: 减运算
__imul__: 乘运算
__idiv__: 除运算
__imod__: 求余运算
__ipow__: 乘方
运算符重载的时候：
"""
# class Vector:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#     def __str__(self):
#         return 'Vector (%d, %d)' % (self.a, self.b)
#
#     def __repr__(self):
#         return 'Vector (%d, %d)' % (self.a, self.b)
#
#     def __add__(self, other):
#         if other.__class__ is Vector:
#             return Vector(self.a + other.a, self.b + other.b)
#         elif other.__class__ is int:
#             return Vector(self.a + other, self.b)
#
#     def __radd__(self, other):
#         """
#         反向算术运算符的重载
#         __add__运算符重载可以保证V+int的情况下不会报错，但是反过来int+V就会报错，通过反向运算符重载可以解决此问题
#         """
#         if other.__class__ is int or other.__class__ is float:
#             return Vector(self.a + other, self.b)
#         else:
#             raise ValueError('值错误')
#
#     def __iadd__(self, other):
#         """
#         复合赋值算数运算符的重载
#         主要用于列表，例如L1+=L2,默认情况下调用__add__，会生成一个新的列表，
#         当数据过大的时候会影响效率，而此函数可以重载+=，使L2直接增加到L1后面
#         """
#         if other.__class__ is Vector:
#             return Vector(self.a + other.a, self.b + other.b)
#         elif other.__class__ is int:
#             return Vector(self.a + other, self.b)
#
# v1 = Vector(2, 10)
# v2 = Vector(5, -2)
# print(v1 + v2)
# print(v1 + 5)
# print((6 + v2))
# -----------------------------------------------
"""
关于 __name__
首先需要了解 __name__ 是属于 python 中的内置类属性，就是它会天生就存在于一个 python 程序中，代表对应程序名称。
比如所示的一段代码里面（这个脚本命名为 pcRequests.py），我只设了一个函数，但是并没有地方运行它，所以当 run 了这
一段代码之后我们有会发现这个函数并没有被调用。但是当我们在运行这个代码时这个代码的 __name__ 的值为 __main__ 
（一段程序作为主线运行程序时其内置名称就是 __main__）。
"""
# import requests
# class requests(object):
#     def __init__(self, url):
#         self.url = url
#         self.result = self.getHTMLText(self.url)
#     def getHTMLText(url):
#         try:
#             r = requests.get(url, timrout = 30)
#             r.raise_for_status()
#             r.encoding = r.apparent_encoding
#             return r.text
#         except:
#             return "This is a error."
# """
# 当这个 pcRequests.py 作为模块被调用时，则它的 __name__ 就是它自己的名字：
# import pcRequestspcRequestsc=pcRequestsc.__name__
# 结果：
# 'pcRequests'
# 看到这里应该能明白，自己的 __name__ 在自己用时就是 main，当自己作为模块被调用时就是自己的名字，
# 就相当于：我管自己叫我自己，但是在朋友眼里我就是小仙女一样。
# """
# print(__name__)
# -----------------------------------------------
"""
类的专有方法中，也是存在默认优先级的，多个方法都有返回值，但一般优先取 __str__() 的返回值，如下面例子：
"""
# class Vector:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#     def __repr__(self):
#         return 'Vector (%d, %d)' % (self.b, self.a)
#     def __str__(self):
#         return 'Vector (%d, %d)' % (self.a, self.b)
#     def __add__(self, other):
#         return Vector(self.a + other.a, self.b + other.b)
#
# v1 = Vector(2, 10)
# print(v1)
# print(v1.__repr__())
# -----------------------------------------------
"""
在 Python 中，方法分为三类实例方法、类方法、静态方法。三种方法的主要区别在于参数。实例方法隐含的参数为类实例 self，而类方法隐含的参数为类本身 cls。
静态方法无隐含参数，主要为了类实例也可以直接调用静态方法。
所以逻辑上类方法应当只被类调用，实例方法实例调用，静态方法两者都能调用。主要区别在于参数传递上的区别，实例方法悄悄传递的是self引用作为参数，而类方法悄悄传递的是 cls 引用作为参数。
Python 实现了一定的灵活性使得类方法和静态方法，都能够被实例和类二者调用。
"""
# class Test(object):
#     def InstanceFun(self):
#         print("InstanceFun")
#         print(self)
#     @classmethod
#     def ClassFun(cls):
#         print("ClassFun")
#         print(cls)
#     @staticmethod
#     def StaticFun():
#         print("StaticFun")
#
# t = Test()
# t.InstanceFun()   # 输出InstanceFun，打印对象内存地址“<__main__.Test object at 0x000002178D9A3F10>”
# Test.ClassFun()   # 输出ClassFun，打印类位置 <class '__main__.Test'>
# Test.StaticFun()  # 输出StaticFun
# t.StaticFun()     # 输出StaticFun
# t.ClassFun()      # 输出ClassFun，打印类位置 <class '__main__.Test'>
# # Test.InstanceFun()   # 错误，TypeError: InstanceFun() missing 1 required positional argument: 'self'
# Test.InstanceFun(t)    # 输出InstanceFun，打印对象内存地址“<__main__.Test object at 0x00000252885C8F70>”
# # t.ClassFun(Test)       # 错误，TypeError: ClassFun() takes 1 positional argument but 2 were given
# -----------------------------------------------
"""
类的二元方法运算符重载介绍的并不全面，文中介绍的全是正向方法，其实还有反向方法，就地方法。下面补充一些。
当解释器碰到 a+b 时，会做以下事情：
从 a 类中找 __add__ 若返回值不是 NotImplemented, 则调用 a.__add__(b)。
若 a 类中没有 __add__ 方法，则检查 b 有没有 __radd__ 。如果如果有，则调用 b.__radd__(a)，若没有，则返回 NotImplemented。
接上条，若 b 也没有 __radd__ 方法，则抛出 TypeError，在错误消息中知名操作数类型不支持。
在类的方法中直接修改 self 是无效操作，即使 self 变量的地址与实例地址相同：
"""
# class C:
#     def __init__(self, a):
#         self.a = a
#     def construct(self, a):
#         c =C(a)
#         self = c
#     def getid(self):
#         print(id(self))
#         return id(self)
#
# if __name__ == '__main__':
#     c1 = C(2)
#     c1.construct(3)
#     print(id(c1))
#     print(id(c1) == c1.getid())
# -----------------------------------------------
"""
事实上 class 的私有属性在外部也是可以访问的我们可以看下文中的例子。
"""
# class People:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.__privater_var = 10
#
#     def intro(self):
#         print(f'My name is {self.name},I\'m {self.age}')
#
#     def get_var(self):
#         print(self.__privater_var)
#
#     def set_var(self, var):
#         self.__privater_var = var
#
# someone = People(name = 'jack', age = 20)
# someone.intro()
# print(someone.age)
# someone.get_var()
# someone.set_var(30)
# someone.get_var()
# # someone.__private_var   # 错误，someone.__private_var   #
# print(dir(someone))     #  获得当前someone的属性列表
# """
# ['_People__privater_var', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
#  '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
#  '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
#  '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'age', 'get_var', 'intro',
#  'name', 'set_var']
#  从打印出的结果中，我们并没有找到'_peivater_var'但是我们看到一个'_People__privater_var'.有没有想到什么？原来是被重命名了。好，我们来试试：
# """
# print(someone._People__privater_var)
# someone._People__privater_var = 40
# print(someone._People__privater_var)
# someone.get_var()
"""
所以说，私有变量的属性是可以修改的。既然Python阻止访问，一般情况下就不要访问。
"""
# -----------------------------------------------
