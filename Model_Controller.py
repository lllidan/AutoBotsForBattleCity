# -*- coding: utf-8 -*-
import tanks
import time
import pygame
import Main
import deco


class GameController():

    game = tanks.Game()
    tanks.castle = tanks.Castle()

    def __init__(self):
        pass

    # @staticmethod
    def gamestart(self, s, n):
        """    游戏逻辑控制，第一个参数标识启动的关卡，第二个标识玩家数；默认从第一关以第一个文件开始    """
        # stage = 0 to 34 mark stage1 - stage 35
        # nr_of_players = 1 or 2 for 1 player or 2 players
        # game = tanks.Game()
        # tanks.castle = tanks.Castle()
        GameController.game.stage = s
        GameController.game.nr_of_players = n
        print ("测试即将展开，选择关卡为第 {} 关，游玩人数为 {} 人".format(int(s)+1, int(n)))

        # start game
        GameController.game.nextLevel()

    def col_mapinfo(self):
        """收集游戏信息"""
        # global players, bullets, enemies
        time.sleep(1)
        print ("开始采集--")
        while True:
            time.sleep(0.5)
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
                mapinfo[1].append([nrect,enemy.direction, enemy.speed, enemy.type])
            for tile in GameController.game.level.mapr:
                nrect = pygame.Rect(tile.left, tile.top, 16, 16)
                mapinfo[2].append([nrect,tile.type])
            for player in tanks.players:
                nrect=player.rect.copy()
                mapinfo[3].append([nrect,player.direction,player.speed,player.shielded])
            print(mapinfo[0])
        return mapinfo


