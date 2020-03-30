# -*- coding: utf-8 -*-
"""
例子：求函数的运行时间和函数的返回值
"""
import time, sys, heapq
import functools            ##调用 functools.wraps() 装饰器所需要的模块

class Logger(object):
    def __init__(self, filename="log.txt"):
        self.terminal = sys.stdout
        self.log = open(filename, "a+")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
sys.stdout = Logger()

# 废弃，对于以exit()退出，无法捕捉
# def log_kind(kind):
#     def add_log(fun):
#         @functools.wraps(fun)
#         def wrapper(*args, **kwargs):
#             start_time = time.time()
#             res = fun(*args, **kwargs)
#             end_time = time.time()
#             print('<%s>[%s] 函数名: %s, 运行时间: %.6f, 运行返回值结果: %d'
#                   %(kind,time.ctime(),fun.__name__,end_time - start_time,res))
#             return res
#         return wrapper
#     return add_log

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.

      实现优先级队列数据结构。 每个插入的项目都有一个与之关联的优先级，客户端通常
      对快速检索队列中最低优先级的项目感兴趣。 此数据结构允许O（1）访问最低优先级的项目。
      请注意，此 优先队列 不允许您更改项目的优先级。 但是，您可以多次插入具有不同优先级的同一项目。
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0


def manhattanDistance(pos1, pos2):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs(pos1[0] -pos2[0] ) + abs(pos1[1] - pos2[1])
