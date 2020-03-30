# -*- coding: utf-8 -*-
import threading, datetime,sys
import Model_Controller
import AI_Agent, util
print "输出重定向"
sys.stdout = util.Logger()

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
    numOfPlayers = 1
    numOfStage = 0

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
    print datetime.datetime.now().strftime('[DEBUG]%Y-%m-%d %H:%M:%S')
    # 模拟进程，启动！
    # 根据玩家数，启动对应数量的模拟程式

    gc = Model_Controller.GameController()
    ai1 = AI_Agent.AiAgent()

    # p = threading.Thread(target=ai1.operations)
    p = threading.Thread(target=ai1.robotmoving)

    # q = threading.Thread(target=gc.gamestart)
    # q.start()
    p.start()
    gc.gamestart(numOfStage, numOfPlayers)
    # ----------------------------------------------------------------------------

