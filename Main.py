# -*- coding: utf-8 -*-
import threading, multiprocessing, time, Queue
import Model_Controller
import AI_Agent
import deco
import tanks



class GameStart():
    def __init__(self):
        pass
        # self.gc = Model_Controller.GameController()


    def start(self):
        pass

    def func_task(self):
        pass
        # print("执行任务中...")

    def func_timer(self):
        pass


if __name__ == "__main__":

    playerFlag = True
    stageFlag = True
    numOfPlayers = -1
    numOfStage = -1

    # while playerFlag:
    #     numOfPlayers = input("请输入开启的电脑数(1 or 2):    ")
    #     if numOfPlayers != 1 and numOfPlayers != 2:
    #         print ("玩家数目输入不合法，请重新输入")
    #     else:
    #         print ("选定玩家数目为 {} 人".format(numOfPlayers))
    #         playerFlag = False
    #
    # while stageFlag:
    #     numOfStage = input("请输入开始的关卡数(1 - 35 的整数):    ")
    #     if numOfStage not in [i for i in range(35)]:
    #         print ("玩家数目输入不合法，请重新输入")
    #     else:
    #         print ("选定开始的关卡数为第 {} 关".format(numOfStage))
    #         numOfStage -= 1
    #         stageFlag = False
    # ----------------------------------------------------------------------------
    print("--------------------link start--------------------")
    # 模拟进程，启动！
    # 根据玩家数，启动对应数量的模拟程式

    gc = Model_Controller.GameController()
    ai1 = AI_Agent.AiAgent()

    p = threading.Thread(target=ai1.operations)
    p.setDaemon(True)
    q = threading.Thread(target=gc.gamestart)
    q.start()
    p.start()

    # p = threading.Thread(target=Model_Controller.GameController.col_mapinfo)
    # p.start()
    # q = threading.Thread(target=gc.gamestart())

    # p.start()
    print "no name"



    #
    # q.start()
    # p = threading.Thread(target=ai1.operations())
    # p.start()

    # Model_Controller.GameController.gamestart(s=0, n=1)

    # p = threading.Thread(target=ai1.operations())
    # p.start()

    # p = threading.Thread(target=Model_Controller.GameController().col_mapinfo)
    # p.start()

    # 游戏主进程启动
    # Model_Controller.GameController.gamestart(s=0, n=1)
    print 1
    # p = multiprocessing.Process(target=Model_Controller.GameController.gamestart)
    # p.start()
    # ----------------------------------------------------------------------------

