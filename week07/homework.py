# 动物类
from abc import ABCMeta, abstractmethod, ABC
class Animals(metaclass=ABCMeta):
    # @abstractmethod
    # def __new__(cls, *args, **kwargs):
    #     raise Exception('未指定动物不可以实例化！')
    @abstractmethod
    def __init__(self):
        self.animalType = '食草' #类型
        self.nature = '还行' #性格
        self.shape = '一般' #体型
        self.isBeast = False #是否属于凶猛动物

    # 判断是否猛兽
    def checkBeast(self,):
        animalShape = {'小': 1, '中等':2, '大':3}
        keys = animalShape.keys()
        if self.shape in keys:
            if self.animalType == '食肉' and self.nature == '凶猛' and animalShape[self.shape] >= 2 :
                isBeast = True
                print('该动物是猛兽！')
                return isBeast
            else:
                print('该动物不是猛兽')
                return False
        else:
            print('该动物不是猛兽')
            return False

# 猫科类
class Cat(Animals):
    shouts = '瞄~' #叫声
    # def __new__(cls, *args, **kwargs):
    #     return object.__new__(cls)
    def __init__(self, _name='', _animalType='', _shape='', _nature=''):
        super().__init__() #继承父属性
        self.name = '1' #名字
        self.isPet = False #是否宠物
        # print(f'{self.animalType},{self.shape},{self.nature}')
        self.animalType = _animalType
        self.shape = _shape
        self.nature = _nature
        # print(f'{self.animalType},{self.shape},{self.nature}')

# 动物园类
class Zoo(object):
    def __init__(self, _name):
        self.name = _name
        self.cages = [] # 笼子，用来关动物
    
    # 添加动物
    def add_animal(self, animal):
        for a in self.cages:
            if id(a) == id(animal):
                raise Exception('动物园已经有该动物了！')
        self.cages.append(animal)

    # 查看动物园里是否有该类动物
    def __getattr__(self, item): 
        for a in self.cages:
            if type(a).__name__ == item:
                print('动物园有该种类动物！')
                return True
        print('动物园没有这类动物！')   
        return False
    
# 定义“动物”、“猫”、“动物园”三个类，动物类不允许被实例化。
# 动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
# 猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，猫类继承自动物类。
# 动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # a = Animals()
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # z.add_animal(cat1)
    print(cat1.checkBeast())
    print(Cat.shouts)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat')
