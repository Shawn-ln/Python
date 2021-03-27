class Toy(object):  # 此处此类可理解为设计一个Toy的蓝图
    # 赋值定义类属性，记录所有玩具数量
    count = 0

    def __init__(self, name):  # 用于实例初始化
        self.name = name
        # 类属性 +1
        Toy.count += 1

    @classmethod  # 此装饰器表示是类方法，类方法无需创建实例对象即可调用，最为灵活
    def show_toy_count(cls):
        print('玩具对象的数量 %d' % cls.count, cls)

    @staticmethod  # 此装饰器表示是静态方法，静态方法本质上是封装在类对象内的的函数，常用于测试
    def hi():
        print('Hello!')

    # 实例方法
    def beybey(self):
        print('Sad！', self)


# 创建实例对象
toy1 = Toy('乐高')
toy1.hand = 2
toy2 = Toy('泰迪熊')
toy3 = Toy('哥斯拉')
print(toy1.name, toy2.name, toy3.name)

# 点语法调用类方法与静态方法，如：类名.方法
Toy.show_toy_count()
Toy.hi()
# 实例对象调用类方法时，与类对象调用类方法无异，但实际上调用仍通过实例对象继承的类对象
toy1.show_toy_count()
print(toy1.hand)
# 实例对象调用静态方法时，与类对象调用静态方法无异，但实际上调用仍通过实例对象继承的类对象
toy2.hi()
# 实例对象调用实例方法,Python的解释器内部，当我们调用toy3.beybey()时，实际上Python解释成Toy.beybey(toy3)
toy3.beybey()
# Toy.beybey()  # 错误语法，self必须指向实例对象，此处实例方法指向类对象而不是实例对象
Toy.beybey(toy3)
# 类与其实例的类型和内存地址
print(type(Toy), id(Toy), type(toy3), id(toy3))
