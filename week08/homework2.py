# 自定义一个 python 函数，实现 map() 函数的功能。

# class CustomIt():
#     def __init__(self, default_val, limit_val, custom_func):
#         self.val = default_val
#         self.limit = limit_val
#         self.func = custom_func
#     def __iter__(self):
#         return self.val
#     def __next__(self):
#         if self.val <= self.limit:
#             self.val = self.func(self.val)
#             return self.val
#         else: 
#             raise StopIteration

def test(item):
    print(item)
    return item + 2

def customMap(custom_func, custom_coll):
    tempList = []
    for item in custom_coll:
        tempList.append(custom_func(item))
    return iter(tempList)


if __name__ == '__main__': 
    print(list(map(test, [1,2,3,4,5])))
    # pass
    print(list(customMap(test, [1,2,3,4,5])))
