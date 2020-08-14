# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。

from functools import wraps
import time, datetime
def timer(func):
    @wraps(func)
    def timerfunction(*args, **kwargs):
        print(f'开始执行')
        beginTime = datetime.datetime.now()
        # result = func(*args, **kwargs)
        func(*args, **kwargs)
        endTime = datetime.datetime.now()
        print(f'运行时间：{endTime - beginTime}')
    return timerfunction

@timer
def test1(a_val, b_val, list1):
    for item in list1:
        time.sleep(1)
        print(a_val + b_val + item)
    # return list1 + list2

@timer
def test2(a_val, dict1):
    d_it = iter(dict1)
    for key in d_it:
        time.sleep(2)
        print(a_val + dict1[key])

if __name__ == '__main__': 
    test1(10,30,[2,4,5,7,8])
    test2(15, {'5':5,'10':10,'20':20})