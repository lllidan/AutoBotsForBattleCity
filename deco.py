# -*- coding: utf-8 -*-
"""
例子：求函数的运行时间和函数的返回值
"""
import time
import functools			##调用 functools.wraps() 装饰器所需要的模块

def log_kind(kind):
    def add_log(fun):
        @functools.wraps(fun)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = fun(*args, **kwargs)
            end_time = time.time()
            print('<%s>[%s] 函数名: %s, 运行时间: %.6f, 运行返回值结果: %d'
                  %(kind,time.ctime(),fun.__name__,end_time - start_time,res))
            return res
        return wrapper
    return add_log

# @log_kind('debug')
# def add(x,y):
#     time.sleep(1)
#     return x + y
#
# print (add(1,2))
