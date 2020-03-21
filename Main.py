# -*- coding: utf-8 -*-
import threading, multiprocessing, time, Queue
import Model_Controller
import AI_Agent
import deco



class GameStart():
    def __init__(self):
        # pass
        self.gc = Model_Controller.GameController()


    def start(self):
        pass

    def func_task(self):
        pass
        # print("执行任务中...")

    def func_timer(self):
        pass
        # self.func_task()
        # global timer  # 定义全局变量
        # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
        # timer = threading.Timer(10, self.func_timer)  # 10秒调用一次函数
        #
        # print("线程名称={},\n正在执行的线程列表:{},\n正在执行的线程数量={},\n当前激活线程={}\n".format(
        #     timer.getName(), threading.enumerate(), threading.active_count(), timer.isAlive)

        # timer.start()  # 启用定时器


if __name__ == "__main__":

    playerFlag = True
    stageFlag = True
    numOfPlayers = -1
    numOfStage = -1

    while playerFlag:
        numOfPlayers = input("请输入开启的电脑数(1 or 2):    ")
        if numOfPlayers != 1 and numOfPlayers != 2:
            print ("玩家数目输入不合法，请重新输入")
        else:
            print ("选定玩家数目为 {} 人".format(numOfPlayers))
            playerFlag = False

    while stageFlag:
        numOfStage = input("请输入开始的关卡数(1 - 35 的整数):    ")
        if numOfStage not in [i for i in range(35)]:
            print ("玩家数目输入不合法，请重新输入")
        else:
            print ("选定开始的关卡数为第 {} 关".format(numOfStage))
            numOfStage -= 1
            stageFlag = False
    # ----------------------------------------------------------------------------
    print("--------------------link start--------------------")

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
    # ----------------------------------------------------------------------------

