# -*- coding: utf-8 -*-
import tanks
import time
import pygame
import Main




class GameController():

    def __init__(self):
        pass


    def gamestart(self,game, s=0, n=1):
        """    游戏逻辑控制，第一个参数标识启动的关卡，第二个标识玩家数；默认从第一关以第一个文件开始    """
        # stage = 0 to 34 mark stage1 - stage 35
        # nr_of_players = 1 or 2 for 1 player or 2 players

        game.stage = s
        game.nr_of_players = n
        # print ("测试即将展开，选择关卡为第 {} 关，游玩人数为 {} 人".format(int(s)+1, int(n)))

        # start game
        game.nextLevel()

    def get_mapinfo(self, game):
        """采集游戏信息"""
        print ("开始采集--")
        while True:
            time.sleep(5)
            mapinfo = []
            mapinfo.append([])
            mapinfo.append([])
            mapinfo.append([])
            mapinfo.append([])
            for bullet in tanks.bullets:
                print "searching bullet"
                if bullet.owner == bullet.OWNER_ENEMY:
                    nrect=bullet.rect.copy()
                    mapinfo[0].append([nrect,bullet.direction,bullet.speed])
            for enemy in tanks.enemies:
                nrect=enemy.rect.copy()
                mapinfo[1].append([nrect,enemy.direction,enemy.speed,enemy.type])
            # for tile in tanks.game.level.mapr:
            # 	nrect=pygame.Rect(tile.left, tile.top, 16, 16)
            # 	mapinfo[2].append([nrect,tile.type])
            for player in game.players :
                nrect=player.rect.copy()
                mapinfo[3].append([nrect,player.direction,player.speed,player.shielded])
            print(mapinfo)
        return mapinfo

