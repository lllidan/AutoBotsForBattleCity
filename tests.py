# -*- coding: utf-8 -*-
import threading
import Model_Controller
import time,sys
import pygame
# 测试迭代器
# print (1.0 in [i for i in range(35)])
# 测试range范围
# for i in range(2):
#     print i
# -------------------------------------------------------------------------------------------------
# p = threading.Thread(target=Model_Controller.GameController().col_mapinfo)
# p.start()
# # 游戏主进程启动
# Model_Controller.GameController().gamestart(s=0, n=1)

# print(q)
# q.put(game)
# gc1 = Model_Controller.GameController()
# gc1.gamestart(game, 0, 1)
# p = threading.Thread(target=Model_Controller.GameController().gamestart, args=(0, 1))
# p.start()
# q.put(game)
# gc1.gamestart(game, 0, 1)
# -----------------------------------------------------------------------------
# self.func_task()
# global timer  # 定义全局变量
# 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
# timer = threading.Timer(10, self.func_timer)  # 10秒调用一次函数
#
# print("线程名称={},\n正在执行的线程列表:{},\n正在执行的线程数量={},\n当前激活线程={}\n".format(
#     timer.getName(), threading.enumerate(), threading.active_count(), timer.isAlive)

# timer.start()  # 启用定时器
# 测试列表自动生成
# mapinfo = [[] for i in range(4)]
# print mapinfo

# 测试输出流重定向
#打印输出到log.txt

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

principal = 1000 # 初始金额
rate = 0.05      # 利率
numyears = 5     # 年数

year = 1


while year <= numyears:
    principal = principal * (1 + rate)
    # print >> f, "%3d %0.2f" % (year, principal)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    time.sleep(1)
    year += 1
pygame.rect