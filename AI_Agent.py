# -*- coding: utf-8 -*-
import random, time, multiprocessing, sys, queue, threading, pygame
import Model_Controller, tanks, util

sys.stdout = util.Logger()
class AiAgent():

    def __init__(self):
        print ("ai_agent正在初始化")
        self.mapinfo = []
        self.encoded_map = []
        self.map_width = 13
        self.map_height = 13
        self.encoded_player_top = -1
        self.encoded_player_left = -1

        #坐标轴左上为原点:上    右   下    左
        self.dir_top =  [-1,   0,   1,    0]
        self.dir_left = [0,    1,   0,   -1]

        # 子弹近防系统所需信息
        self.dangerous_map = []

        # 姿态修正
        self.adjusting = False

        # 指令队列
        self.orderlists = queue.Queue()

    # rect对象:				[left, top, width, height] : [左上角X坐标。左上角的Y坐标,矩形的宽度,矩形的高度]

    # mapinfo[0]: 			bullets [rect, direction, speed]]
    # mapinfo[1]: 			enemies [rect, direction, speed, type]]
    # mapinfo[2]: 			tile 	[rect, type] (empty don't be stored to mapinfo[2])
    # mapinfo[3]: 			player 	[rect, direction, speed, Is_shielded]]

    # castle_rect:			[12*16, 24*16, 32, 32]
    # tile_type:			0:empty 1:brick 2:steel 3:water 4:grass 5:froze
    # direction:            0:上  1:右  2:下 3:左
    # enemy_type:			0:TYPE_BASIC 1:TYPE_FAST 2:TYPE_POWER 3:TYPE_ARMOR
    # shoot:				0:none 1:shoot
    # move_dir:				0:Up 1:Right 2:Down 3:Left 4:None
    # keep_action:			0:The tank work only when you Update_Strategy.
    #                       1:the tank keep do previous action until new Update_Strategy.

    def operations(self):

        # print ("--------汽车人，出击--------")
        while True:
            # 等待关卡对象level对象生成
            if hasattr(Model_Controller.game, "level") is True:
                break
            print ("--------等待游戏开始--------")

        # 操作开始
        while True:

            # --------------------战斗信息分析系统--------------------
            self.mapinfo = Model_Controller.GameController.coll_mapinfo()

            # 战斗信息分类
            # 子弹信息----bullets [[rect, direction, speed],...]
            bullets = self.mapinfo[0]
            # 敌人信息----enemies [[rect, direction, speed, type],...]
            enemies = self.mapinfo[1]
            # 障碍物信息 = tile [[rect, type],...]
            tiles = self.mapinfo[2]
            # 玩家信息 [[rect, direction, speed, Is_shielded],...]
            player1 = self.mapinfo[3][0]
            # player2 = self.mapinfo[3][0]
            # 1号玩家位置
            player1_left = player1[0][0]
            player1_top = player1[0][1]
            # 2号玩家位置
            # player2_left = player2[0][0]
            # player2_top = player2[0][1]

            # for i in range(100000):
            #     a = 2 + i

            # 地图解析
            self.encode_map(bullets, enemies, tiles, player1)
            # self.print_encoded_map()

            # python解释器100行切换GIL锁，手动实现调度
            for i in range(100):
                i *= 1

            # shoot = random.randint(0, 1)

            # move_dir = random.randint(0, 4)

            # 默认保持原有指令
            keep_action = 1


            # 将坐标转化为单位元素（一个坦克大小为32 * 32）
            self.encoded_player_left = player1_left / 32
            self.encoded_player_top = player1_top / 32

            # 获取当前朝向
            player_dire = player1[1]

            # 修正因无法整除产生的偏移
            adjust_top = self.encoded_player_top * 32
            adjust_left = self.encoded_player_left * 32

            # 执行战斗指令
            # self.activate_strategy(self.orderlists)

            # --------------------战斗策略生成系统--------------------

            # 子弹躲避系统
            # move = self.dodge_bullets(bullets, player1_top, player1_left)
            # if (move != -1):
            #     print "侦测到在途的聚变打击，进行机动躲避"
            #     # self.Update_Strategy(self.orderlists, 0, move, 1)
            #     continue
                # break

            # 1. 移动到32的整数倍位置，防止计算出的路径被卡住
            # 所有路径点以左上角坐标代替，因此在纠正时以左上坐标为准，向其移动

            if (player_dire == 1 or player_dire == 3):
                if (player1_top - adjust_top > 15):
                    # print "adjust top"
                    self.Update_Strategy(self.orderlists, 0, 0, keep_action)
                    # continue
                    break
            elif (player_dire == 0 or player_dire == 2):
                if (player1_left - adjust_left > 15):
                    # print "adjust left"
                    self.Update_Strategy(self.orderlists, 0, 3, keep_action)
                    continue
                    # break
            # 2. 查找周围5格范围内的相关元素
            # 探测附近的子弹
            move = self.check_bullets(bullets)
            if (move != -1):
                # print "发现子弹，和他互怼"
                self.Update_Strategy(self.orderlists, 1, move, 1)
                continue
                # break
            # 探测周围敌人坦克
            move = self.check_tanks()
            if (move != -1):
                # print "Found Tank"
                self.Update_Strategy(self.orderlists, 1, move, 1)
                continue
                # break
            # 3. 根据周围的敌人、子弹，指定行进路线
            self.generate_dangerous_map(bullets, enemies)
            move = self.bfs()
            if (move == -1):
                move = random.randint(0, 4)
                self.Update_Strategy(self.orderlists, 1, move, 0)
            else:
                self.Update_Strategy(self.orderlists, 0, move, keep_action)

            # 执行战斗指令
            # self.activate_Strategy(self.orderlists)

            break

        # #keep_action = 0


        #-----------
        # self.Update_Strategy(self.orderlists,shoot,move_dire,keep_action)

    def dodge_bullets(self, bullets, player_top, player_left):
        """ 判断子弹与自己的相对位置，如不在近处，无需躲避"""
        range = 100
        for bullet in bullets:
            bullet_top = bullet[0][1]
            bullet_left = bullet[0][0]
            bullet_bottom = bullet[0][1] + bullet[0][3]
            bullet_right = bullet[0][0] + bullet[0][2]
            bullet_h_mid = (bullet_top + bullet_bottom) / 2
            bullet_v_mid = (bullet_left + bullet_right) / 2
            bullet_dir = bullet[1]
            # top part of player tank
            if ((bullet_bottom > player_top and bullet_bottom <= player_top + 10) or (bullet_h_mid > player_top and bullet_h_mid <= player_top + 10)):
                if ((player_left < bullet_left and player_left + range > bullet_left and bullet_dir == 3) or (player_left > bullet_left and player_left - range < bullet_left and  bullet_dir == 1)):
                    return 2
            # bottom part of player tank
            if ((bullet_top > player_top + 16 and bullet_top <= player_top + 26) or (bullet_h_mid > player_top + 16 and bullet_h_mid <= player_top + 26)):
                if ((player_left < bullet_left and player_left + range > bullet_left and bullet_dir == 3) or (player_left > bullet_left and player_left - range < bullet_left and bullet_dir == 1)):
                    return 0
            # left part of player tank
            if ((bullet_right > player_left and bullet_right <= player_left + 10) or (bullet_v_mid > player_left and bullet_v_mid <= player_left + 10)):
                if ((player_top < bullet_top and player_top + range > bullet_top and bullet_dir == 0) or (player_top > bullet_top and player_top - range < bullet_top and bullet_dir == 2)):
                    return 1
            # right part of player tank
            if (bullet_left > player_left + 16 and bullet_left <= player_left + 26 or (bullet_v_mid > player_left + 16 and bullet_v_mid <= player_left + 26)):
                if ((player_top < bullet_top and player_top + range > bullet_top and bullet_dir == 0) or (player_top > bullet_top and player_top - range < bullet_top and bullet_dir == 2)):
                    return 3

        return -1

    def check_bullets(self, bullets):
        """输入子弹，判断碰撞可能性"""
        for bullet in bullets:
            # 获得子弹的左上和右下的坐标
            encoded_bullet_left = bullet[0][0] / 32
            encoded_bullet_top = bullet[0][1] / 32
            encoded_bullet_right = (bullet[0][0] + bullet[0][2]) / 32
            encoded_bullet_bottom = (bullet[0][1] + bullet[0][3]) / 32
            bullet_dire = bullet[1]

            # 子弹与坦克处于同一列
            if (encoded_bullet_left == self.encoded_player_left):

                # 子弹朝下，射向我方坦克，向上射击与子弹抵消，反之向下射击
                if (encoded_bullet_top < self.encoded_player_top and bullet_dire == 2):
                    # print ("子弹向下运动，转向上方射击")
                    return 0
                elif (encoded_bullet_top > self.encoded_player_top and bullet_dire == 0):
                    # print ("子弹向上运动，转向下方射击")
                    return 2
            # 子弹与坦克处于同一行
            if (encoded_bullet_top == self.encoded_player_top):
                # 子弹朝右，射向我方坦克，向左射击与子弹抵消，反之向右射击
                if (encoded_bullet_left < self.encoded_player_left and bullet_dire == 1):
                    # print ("子弹向右运动，转向左方射击")
                    return 3
                elif (encoded_bullet_left > self.encoded_player_left and bullet_dire == 3):
                    # print ("子弹向左运动，转向右方射击")
                    return 1

        return -1

    def check_tanks(self):
        # print "查找是否有敌人在设计方向上"
        for i in range(4):
            current_left = self.encoded_player_left
            current_top = self.encoded_player_top
            # print ("查找在 {} 方向上的敌人".format(i))
            for j in range(12):
                current_left = current_left + self.dir_left[i]
                current_top = current_top + self.dir_top[i]
                if (current_left < 0 or current_left >= 13 or current_top < 0 or current_top >= 13 or self.encoded_map[current_top][current_left] == '@'):
                    break
                if (self.encoded_map[current_top][current_left] == 'E'):
                    # print "enemy was found"
                    return i

        return -1

    def encode_map(self, bullets, enemies, tiles, player):
        # print ("--------------------讯号传入中--------------------")
        result = [['_' for x in range(self.map_width)] for y in range(self.map_height)]
        # print ("共发现 {} 颗子弹".format(len(bullets)))
        for bullet in bullets:
            b_left = bullet[0][0] / 32
            b_top = bullet[0][1] / 32
            if (b_left >= 0 and b_left < 13 and b_top >= 0 and b_top < 13):
                result[b_top][b_left] = 'B'

            b_right = (bullet[0][0] + bullet[0][2]) / 32
            b_bottom = (bullet[0][1] + bullet[0][3]) / 32
            if (b_right >= 0 and b_right < 13 and b_bottom >= 0 and b_bottom < 13):
                result[b_bottom][b_right] = 'B'

        # print ("共发现 {} 个 敌人".format(len(enemies)))
        for enemy in enemies:
            e_left = enemy[0][0]
            e_top = enemy[0][1]
            result[e_top / 32][e_left / 32] = 'E'
        # print ("共载入 {} 个 地图元素".format(len(tiles)))
        for tile in tiles:
            t_left = tile[0][0]
            t_top = tile[0][1]
            t_type = tile[1]
            if (t_type == 1 or t_type == 2 or t_type == 3):
                result[t_top / 32][t_left / 32] = '@'

        player_left = player[0][0]
        player_top = player[0][1]

        result[player_top / 32][player_left / 32] = 'P'

        self.encoded_map = result

    def generate_dangerous_map(self, bullets, enemies):
        result = [[False for x in range(self.map_width)] for y in range(self.map_height)]

        # 敌方子弹可能出现的位置为危险位置
        for bullet in bullets:
            b_left = bullet[0][0] / 32
            b_top = bullet[0][1] / 32
            b_right = (bullet[0][0] + bullet[0][2]) / 32
            b_bottom = (bullet[0][1] + bullet[0][3]) / 32
            b_dir = bullet[1]

            # 产生错误位置，删除
            if (b_left >= 0 and b_left < 13 and b_top >= 0 and b_top < 13):
                result[b_top][b_left] = True

            current_top = b_top
            current_left = b_left
            current_bottom = b_bottom
            current_right = b_right

            # 在子弹前进方向上的1个单位为危险位置
            for i in range(4):
                current_top = current_top + self.dir_top[b_dir]
                current_left = current_left + self.dir_left[b_dir]
                current_bottom = current_bottom + self.dir_top[b_dir]
                current_right = current_right + self.dir_left[b_dir]
                if (current_left >= 0 and current_left < 13 and current_top >= 0 and current_top < 13):
                    result[current_top][current_left] = True
                if (current_right >= 0 and current_right < 13 and current_bottom >= 0 and current_bottom < 13):
                    result[current_bottom][current_right] = True


        # 敌方坦克前进方向可能发射子弹，为危险位置
        for enemy in enemies:
            e_left = enemy[0][0] / 32
            e_top = enemy[0][1] / 32
            e_dir = enemy[1]

            # 载入错误的位置，抛弃
            # if (e_left < 0 or e_left >= 13 or e_top < 0 or e_top >= 13):
            #     continue;

            result[e_top][e_left] = True

            current_top = e_top
            current_left = e_left

            # 面向方向的两个单位为危险位置
            for i in range(1, 3):
                current_top = current_top + self.dir_top[e_dir]
                current_left = current_left + self.dir_left[e_dir]
                if (current_left < 0 or current_left >= 13 or current_top < 0 or current_top >= 13):
                    continue
                result[current_top][current_left] = True
        self.dangerous_map = result

    def print_encoded_map(self):
        """打印出解析后的地图"""
        print ("--------------------")
        for i in range(13):
            for j in range(13):
                sys.stdout.write(self.encoded_map[i][j])
            sys.stdout.write("\n")

    def bfs(self):
        q = queue.Queue()

        player_left = 0
        player_top = 0
        # 玩家位置确认
        for i in range(self.map_height):
            for j in range(self.map_width):
                if (self.encoded_map[i][j] == 'P'):
                    player_top = i
                    player_left = j
                    break

        # 设置访问集合，False表示未访问，True表示已访问
        visited = [[False for x in range(self.map_width)] for y in range(self.map_height)]

        visited[player_top][player_left] = True
        # 查找队列初始化，将当前位置的上下左右四个节点加入队列中（除去障碍物、危险位置、地图外的点）
        for i in range(4):  # 4
            new_top = player_top + self.dir_top[i]
            new_left = player_left + self.dir_left[i]
            if (new_left < 0 or new_left >= 13 or new_top < 0 or new_top >= 13 or self.dangerous_map[new_top][new_left] == True):
                continue
            if (self.encoded_map[new_top][new_left] != '@'):
                # 入队新节点（x坐标，y坐标，从原点到达这个点移动的方向）
                q.put([new_top, new_left, i])
                visited[new_top][new_left] = True

        result_move = -1

        while not q.empty():
            temp = q.get()
            current_top = temp[0]
            current_left = temp[1]
            direction = temp[2]
            visited[current_top][current_left] = True
            # 当前节点存在地方坦克，则返回到达此节点需要行进的路线
            if (self.encoded_map[current_top][current_left] == 'E'):
                # print "found enemy"
                result_move = direction
                return result_move
            # 当前节点无敌方坦克，则将直接相邻的四个节点中的合法节点加入队列
            for i in range(4):
                new_top = current_top + self.dir_top[i]
                new_left = current_left + self.dir_left[i]
                if (new_left < 0 or new_left >= 13 or new_top < 0 or new_top >= 13):
                    continue
                if (visited[new_top][new_left] == False and self.encoded_map[new_top][new_left] != '@'):
                    q.put([new_top, new_left, direction])

        return result_move


    def Update_Strategy(self, orderlist, shoot, move_dire, keep_action):
        if orderlist.empty() is True:
            orderlist.put([shoot, move_dire, keep_action])
            # print ("增加新指令")
            # print ("add new order to the list:fire:{}, move_dire:{}".format(shoot, move_dire))
            return True
        else:
            return False

    def activate_strategy(self, orderlists):

        (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)
        # rate = random.randint(0, 1)
        # if rate < 0.1:
        #     orderlists.clear()
        time.sleep(0.025)
        # order:shoot(1:开火；0：不开火), move_dire(0:上,1:右,2:下,3:左), keep_action(1:保持；0：更新)
        # 任务队列为空，不执行任何任务
        if orderlists.empty() is True:
            print ("无任务，原地待命")
            return 0
        else:
            order = orderlists.get()
            # print orderlists.qsize()
            # print order
            player = tanks.players[0]

            if player.state == player.STATE_ALIVE and not Model_Controller.game.game_over and Model_Controller.game.active:

                if order[1] < 4:
                    if order[0] == 1:
                        player.fire()
                        # if player.fire() and tanks.play_sounds:
                        #     tanks.sounds["fire"].play()

                    player.pressed[order[1]] = True
                    if player.pressed[0] is True:
                        player.move(DIR_UP)
                        player.pressed[0] = False
                        # print "向上走"

                    elif player.pressed[1] is True:
                        player.move(DIR_RIGHT)
                        player.pressed[1] = False
                        # print "向右走"

                    elif player.pressed[2] is True:

                        player.move(DIR_DOWN)
                        player.pressed[2] = False
                        # print "向下走"

                    elif player.pressed[3] is True:
                        player.move(DIR_LEFT)
                        player.pressed[3] = False
                        # print "向左走"


            player.update(0.05)
            # if order[1] < 4:
            #     player.pressed[order[1]] = False

    def robotmoving(self):
        while True:
            self.activate_strategy(self.orderlists)
            self.operations()

    # 改进路径算法：a*
    # --------------------施工中--------------------
    def aStarSearch(self):

        enemies = self.mapinfo[1]
        result_move = -1

        if not enemies:
            return -1
        visited = [[False for x in range(self.map_width)] for y in range(self.map_height)]
        fringe = util.PriorityQueue()
        # x = self.nearest(self.rect.left, 16)
        # y = self.nearest(self.rect.top, 16)
        player_left = 0
        player_top = 0

        for i in range(self.map_height):
            for j in range(self.map_width):
                if (self.encoded_map[i][j] == 'P'):
                    player_top = i
                    player_left = j
                    break

        start = (player_left, player_top)
        fringe.push((start, []), self.heuristic(start))

        while not fringe.isEmpty():
            node, actions = fringe.pop()
            if self.isGoalState(node):
                print "self", self.rect.topleft, "node: ", node, "cost of actions: ", self.getCostOfActions(
                    actions), "Heuristic: ", self.heuristic(node)
                return actions
            if not node in visited:
                visited.add(node)

            for curNode, curAction in self.getSuccessors(node):
                if self.isGoalState(curNode):
                    fringe.push((curNode, actions + [curAction]),
                                self.getCostOfActions(actions + [curAction]) + self.heuristic(curNode))
                if not curNode in visited:
                    visited.add(curNode)
                    fringe.push((curNode, actions + [curAction]),
                                self.getCostOfActions(actions + [curAction]) + self.heuristic(curNode))
        return result_move

    def hcost(self, position):
        enemies = []
        for i in range(self.map_height):
            for j in range(self.map_width):
                if (self.encoded_map[i][j] == 'E'):
                    enemies.append((i, j))

        nearest_enemy = 0
        bonus_value = 0
        lowest_enemy = 0

        for enemy in enemies:
            enemy_position = (enemy[0], enemy[1])
            distance = util.manhattanDistance(position, enemy_position)
            if nearest_enemy < distance:
                nearest_enemy = distance
            if lowest_enemy < enemy.rect.top:
                lowest_enemy = enemy.rect.top
        if lowest_enemy > 200:
            lowest_enemy = lowest_enemy * 10
        heuristic_value = nearest_enemy - lowest_enemy
        return heuristic_value
