# -*- coding: utf-8 -*-
import threading
import Model_Controller

# 测试迭代器
# print (1.0 in [i for i in range(35)])
# 测试range范围
# for i in range(2):
#     print i
# -------------------------------------------------------------------------------------------------
p = threading.Thread(target=Model_Controller.GameController().col_mapinfo)
p.start()
# 游戏主进程启动
Model_Controller.GameController().gamestart(s=0, n=1)

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