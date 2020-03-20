# -*- coding: utf-8 -*-
import multiprocessing,time,Queue
import tanks,Model_Controller,AI_Agent



class GameStart():
    def __init__(self):
        # pass
        self.gc = Model_Controller.GameController()

    def start(self):

        # self.gc = Model_Controller.GameController()
        # gc1.gameStart(game, 0, 1)
        # gc2 = Model_Controller.GameController()
        p = multiprocessing.Process(target=self.gc.gameStart, args=(0, 1))
        # p.start()
        # q = multiprocessing.Process(target=gc2.get_mapinfo)
        # q = multiprocessing.Process(target=gc2.get_mapinfo)

        # q.start()

    def func_task(self):
        print("执行任务中...")

    def func_timer(self):

        self.func_task()
        global timer  # 定义全局变量
        # 定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
        timer = threading.Timer(10, self.func_timer)  # 10秒调用一次函数

        print("线程名称={},\n正在执行的线程列表:{},\n正在执行的线程数量={},\n当前激活线程={}\n".format(
            timer.getName(), threading.enumerate(), threading.active_count(), timer.isAlive)
        )

        timer.start()  # 启用定时器


if __name__ == "__main__":

    print("--------------------link start--------------------")

    game = tanks.Game()
    tanks.castle = tanks.Castle()
    # game.showMenu()
    q = Queue.Queue()
    # ----------------------------------------------------------------------------
    print(q)
    q.put(game)
    gc1 = Model_Controller.GameController()
    # # gc1.gamestart(game, 0, 1)
    # gc2 = Model_Controller.GameController()
    p = multiprocessing.Process(target=gc1.gamestart, args=(q,0, 1, ))
    p.start()
    # q.put(game)
    # q = multiprocessing.Process(target=gc2.get_mapinfo, args=(q,))
    # q.start()
    # gc1.gamestart(game, 0, 1)
    # ----------------------------------------------------------------------------

