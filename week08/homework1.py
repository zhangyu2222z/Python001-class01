# 区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：

# list
# tuple
# str
# dict
# collections.deque

from collections import deque
import copy

# 校验是否容器
def checkTypeOne(obj):
    new_obj = copy.copy(obj)
    if new_obj is obj:
        if type(obj) == tuple:
            for i in range(len(obj) - 1):
                if type(obj[i]) is not type(obj[i+1]):
                    print(f'{type(obj)}是容器序列')
                    break
            print(f'{type(obj)}是扁平序列')
        else:
            print(f'{type(obj)}是扁平序列')
    else:
        print(f'{type(obj)}是容器序列')

# 校验是否可变
def checkTypeTwo(obj):
    if 'pop' in dir(obj):
        print(f'{type(obj)}是可变序列')
    else:
        print(f'{type(obj)}是不可变序列')


if __name__ == '__main__': 

    list_a = [1,2,3]
    tuple_a = (1,'2',3)
    str_a = '1,2,3'
    dict_a = {'1':1, '2':2, '3':3}
    deque_a = deque('1,2,3')

    checkTypeOne(list_a)
    checkTypeOne(tuple_a)
    checkTypeOne(str_a)
    checkTypeOne(dict_a)
    checkTypeOne(deque_a)
    checkTypeTwo(list_a)
    checkTypeTwo(tuple_a)
    checkTypeTwo(str_a)
    checkTypeTwo(dict_a)
    checkTypeTwo(deque_a)
