# -*- coding: utf-8 -*-
import tanks,AI_Agent
import time
import pygame
import threading
import util,sys

game = tanks.Game()
tanks.castle = tanks.Castle()
event = threading.Event()
sys.stdout = util.Logger()
class GameController():

    def __init__(self):
        print ("生成游戏控制对象")
        pass

    # @staticmethod
    def gamestart(self, s=0, n=1):
        """    游戏逻辑控制，第一个参数标识启动的关卡，第二个标识玩家数；默认从第一关以第一个文件开始    """
        # stage = 0 to 34 mark stage1 - stage 35
        # nr_of_players = 1 or 2 for 1 player or 2 players
        # game = tanks.Game()
        # tanks.castle = tanks.Castle()
        # GameController.game.stage = s
        # GameController.game.nr_of_players = n

        game.stage = s
        game.nr_of_players = n
        print ("测试即将展开，选择关卡为第 {} 关，游玩人数为 {} 人".format(int(s)+1, int(n)))
        game.nextLevel()
        # start game
        # p = threading.Thread(target=game.nextLevel())
        # ai1 = AI_Agent.ai_agent()
        # q = threading.Thread(target=ai1.operations())
        # p.start()
        # q.start()

        game.nextLevel()

    @staticmethod
    def coll_mapinfo():
        """收集游戏信息"""
        # global players, bullets, enemies
        # print ("收集游戏信息--\n")
        # mapinfo = [[] for i in range(4)]
        mapinfo = []
        mapinfo.append([])
        mapinfo.append([])
        mapinfo.append([])
        mapinfo.append([])
        # event.wait()
        for bullet in tanks.bullets:
            if bullet.owner == bullet.OWNER_ENEMY:
                nrect = bullet.rect.copy()
                mapinfo[0].append([nrect, bullet.direction, bullet.speed])
        for enemy in tanks.enemies:
            nrect=enemy.rect.copy()
            mapinfo[1].append([nrect, enemy.direction,  enemy.speed,  enemy.type])
        for tile in game.level.mapr:
            nrect = pygame.Rect(tile.left,  tile.top,  16,  16)
            mapinfo[2].append([nrect, tile.type])
        for player in tanks.players:
            nrect=player.rect.copy()
            mapinfo[3].append([nrect, player.direction, player.speed, player.shielded])
            # print ("[玩家位置： {}；玩家方向： {}；玩家速度：{}；玩家防御状态：{}]".format(nrect, player.direction, player.speed, player.shielded))

        # timer = threading.Timer(10, self.func_timer)  # 10秒调用一次函数
        #
        # print("正在执行的线程数量={},\n当前激活线程={}\n".format(
        #     threading.enumerate(), threading.active_count()))
        return mapinfo


