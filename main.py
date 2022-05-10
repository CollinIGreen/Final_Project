
import pygame
import time
import random


pygame.init()

import numpy as np
import numpy as savetxt
import numpy as asarray
from tempfile import TemporaryFile
outfile = TemporaryFile()
##from IPython.display import clear_output
import random
import time, pickle, os
#clear_output(wait=True)

class SNAKEAI():
    def __init__(self):
        self.xdim = 400
        self.ydim = 400
        self.qTable = np.load('test.csv')
        self.catalogue = np.load('catalogue.csv', allow_pickle=True)
        self.screen = pygame.display.set_mode([self.xdim, self.ydim])
        self.SnakeC = (0, 255, 0)
        self.AppleC = (255, 0, 0)
        self.AppleP = []
        self.SHeadS = 10
        self.SHeadP = [self.xdim-10, self.ydim-10]
        self.SSegments = [self.SHeadP]
        self.SLen = 0
        self.direction = ""
        self.running = True
        self.LDir = ""
    def Gen_Disp(self):
        self.screen = pygame.display.set_mode([self.xdim, self.ydim])
        for i in range(len(self.SSegments)):
            pygame.draw.rect(self.screen, self.SnakeC, pygame.Rect(self.SSegments[i][0], self.SSegments[i][1], self.SHeadS, self.SHeadS))
        pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(self.SSegments[0][0], self.SSegments[0][1], self.SHeadS, self.SHeadS))
        pygame.draw.rect(self.screen, self.AppleC, pygame.Rect(self.AppleP[0], self.AppleP[1], self.SHeadS, self.SHeadS))
        pygame.display.flip()
        #time.sleep(1)
    def Check_For_Blockage(self, pos):
        if pos[0] < 0 or pos[0] > self.xdim-self.SHeadS or pos[1] < 0 or pos[1] > self.ydim-self.SHeadS:
            return False
        else:
            for nPos in self.SSegments:
                if nPos == pos:
                    return False
        return True
    def find_Nearest_Blockage(self, dir):
        count = self.SHeadS
        check = True
        if dir == "right":
            while check == True:
                check = self.Check_For_Blockage([self.SHeadP[0] + count, self.SHeadP[1]])
                count += self.SHeadS
        elif dir == "left":
            while check == True:
                check = self.Check_For_Blockage([self.SHeadP[0] - count, self.SHeadP[1]])
                count += self.SHeadS
        elif dir == "down":
            while check == True:
                check = self.Check_For_Blockage([self.SHeadP[0], self.SHeadP[1]+count])
                count += self.SHeadS
        elif dir == "up":
            while check == True:
                check = self.Check_For_Blockage([self.SHeadP[0], self.SHeadP[1]-count])
                count += self.SHeadS
        return count/self.SHeadS
    def CheckCollision(self):
        for seg in range(1,len(self.SSegments)):
            if self.SSegments[seg] == self.SHeadP:
                return False
        return True
    def add_Seg(self):
        self.SSegments.insert(0, self.SHeadP)
        if self.SLen < len(self.SSegments):
            self.SSegments.pop(len(self.SSegments) - 1)
    def Add_Food(self):
        x = random.randint(1, (self.xdim/10)-1)*10
        y = random.randint(1, (self.ydim/10)-1)*10
        count = 0
        while count < len(self.SSegments):
            if self.SSegments[count] == [x, y]:
                x = random.randint(1, (self.xdim/10)-1) * 10
                y = random.randint(1, (self.ydim/10)-1) * 10
                count = 0
            count += 1
        self.AppleP = [x, y]
    def move_Snake(self):
        self.running = True
        self.Add_Food()
        #print(self.AppleP)
        while self.running == True:
            time.sleep(.1)
            self.screen = pygame.display.set_mode([self.xdim, self.ydim])
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != "right":
                        self.direction = "left"
                    if event.key == pygame.K_RIGHT and self.direction != "left":
                        self.direction = "right"
                    if event.key == pygame.K_UP and self.direction != "down":
                        self.direction = "up"
                    if event.key == pygame.K_DOWN and self.direction != "up":
                        self.direction = "down"
            if self.direction == "left":
                self.SHeadP = [self.SHeadP[0] - 10, self.SHeadP[1]]
            if self.direction == "right":
                self.SHeadP = [self.SHeadP[0] + 10, self.SHeadP[1]]
            if self.direction == "up":
                self.SHeadP = [self.SHeadP[0], self.SHeadP[1] - 10]
            if self.direction == "down":
                self.SHeadP = [self.SHeadP[0], self.SHeadP[1] + 10]
            if self.xdim-10 < self.SHeadP[0] or self.SHeadP[0] < 0 or self.ydim-10 < self.SHeadP[1] or self.SHeadP[1]< 0:
                #print(self)
                return
            if self.direction != "":
                check = self.CheckCollision()
                if check == False:
                    return
            if self.AppleP == self.SHeadP:
                self.SLen = self.SLen + 1
                self.Add_Food()
            self.add_Seg()
            self.Gen_Disp()
    def avoid_edge(self):
        if self.SHeadP == [0, 0] or self.SHeadP == [self.xdim-10, self.ydim-10] or self.SHeadP == [self.xdim-10, 0] or self.SHeadP == [0, self.ydim-10]:
           if self.SHeadP == [0, 0]:
               if self.direction == "up":
                   return "right"
               else:
                   return "down"
           elif self.SHeadP == [self.xdim-10, 0]:
               if self.direction == "up":
                   return "left"
               else:
                   return "down"
           elif self.SHeadP == [0, self.ydim-10]:
               if self.direction == "down":
                   return "right"
               else:
                   return "up"
           elif self.SHeadP == [self.xdim-10, self.ydim-10]:
               if self.direction == "down":
                   return "left"
               else:
                   return "up"

        elif self.SHeadP[0] == 0:
            if self.direction == "left":
                if abs(self.AppleP[1]-self.SHeadP[1]) == self.AppleP[1]-self.SHeadP[1]:
                    return "up"
                else:
                    return "down"

        elif self.SHeadP[0] == self.xdim-10:
            if self.direction == "right":
                if abs(self.AppleP[1]-self.SHeadP[1]) == self.AppleP[1]-self.SHeadP[1]:
                    return "up"
                else:
                    return "down"

        elif self.SHeadP[1] == 0:
            if self.direction == "up":
                if abs(self.AppleP[0]-self.SHeadP[0]) == self.AppleP[0]-self.SHeadP[0]:
                    return "right"
                else:
                    return "left"

        elif self.SHeadP[1] == self.ydim-10:
            if self.direction == "down":
                if abs(self.AppleP[0]-self.SHeadP[0]) == self.AppleP[0]-self.SHeadP[0]:
                    return "right"
                else:
                    return "left"
        return self.direction
    def targetApple(self):
        if self.SHeadP != self.AppleP:
            if self.SHeadP[0] == self.AppleP[0]:
                if self.SHeadP[1] <= self.AppleP[1]:
                    if self.direction != "up":
                        self.LDir = self.direction
                        self.direction = "down"

                elif self.SHeadP[1] > self.AppleP[1]:
                    if self.direction != "down":
                        self.LDir = self.direction
                        self.direction = "up"
            elif self.SHeadP[1] == self.AppleP[1]:
                if self.SHeadP[0] <= self.AppleP[0]:
                    if self.direction != "left":
                        self.LDir = self.direction
                        self.direction = "right"

                elif self.SHeadP[0] > self.AppleP[0]:
                    if self.direction != "right":
                        self.LDir = self.direction
                        self.direction = "left"

            elif self.SHeadP[0] != self.AppleP[0] and self.SHeadP[1] != self.AppleP[1]:
                if abs(self.AppleP[0] - self.SHeadP[0]) < abs(self.AppleP[1] - self.SHeadP[1]):
                    if self.SHeadP[0] <= self.AppleP[0]:
                        if self.direction != "left":
                            self.LDir = self.direction
                            self.direction = "right"
                        elif abs(self.AppleP[1] - self.SHeadP[1]) == self.AppleP[1] - self.SHeadP[1]:
                            self.LDir = self.direction
                            self.direction = "down"
                        else:
                            self.LDir = self.direction
                            self.direction = "up"
                    elif self.SHeadP[0] > self.AppleP[0]:
                        if self.direction != "right":
                            self.LDir = self.direction
                            self.direction = "left"
                        elif abs(self.AppleP[1] - self.SHeadP[1]) == self.AppleP[1] - self.SHeadP[1]:
                            self.LDir = self.direction
                            self.direction = "down"
                        else:
                            self.LDir = self.direction
                            self.direction = "up"

                elif abs(self.AppleP[0] - self.SHeadP[0]) > abs(self.AppleP[1] - self.SHeadP[1]):
                    if self.SHeadP[1] <= self.AppleP[1]:
                        if self.direction != "up":
                            self.LDir = self.direction
                            self.direction = "down"
                        elif abs(self.AppleP[0] - self.SHeadP[0]) == self.AppleP[0] - self.SHeadP[0]:
                            self.LDir = self.direction
                            self.direction = "right"
                        else:
                            self.LDir = self.direction
                            self.direction = "left"

                    elif self.SHeadP[1] > self.AppleP[1]:
                        if self.direction != "down":
                            self.LDir = self.direction
                            self.direction = "up"
                        elif abs(self.AppleP[0] - self.SHeadP[0]) == self.AppleP[0] - self.SHeadP[0]:
                            self.LDir = self.direction
                            self.direction = "right"
                        else:
                            self.LDir = self.direction
                            self.direction = "left"
    def incramentSnake(self):
        if self.direction == "left":
            self.SHeadP = [self.SHeadP[0] - 10, self.SHeadP[1]]
        if self.direction == "right":
            self.SHeadP = [self.SHeadP[0] + 10, self.SHeadP[1]]
        if self.direction == "up":
            self.SHeadP = [self.SHeadP[0], self.SHeadP[1] - 10]
        if self.direction == "down":
            self.SHeadP = [self.SHeadP[0], self.SHeadP[1] + 10]
    def collision_AI(self):
        self.running = True
        self.Add_Food()
        self.direction = "up"
        while self.running == True:
            time.sleep(.1)
            self.screen = pygame.display.set_mode([self.xdim, self.ydim])
            self.direction = self.avoid_edge()
            self.incramentSnake()
            if self.xdim-10 < self.SHeadP[0] or self.SHeadP[0] < 0 or self.ydim-10 < self.SHeadP[1] or self.SHeadP[1]< 0:\
                return
            if self.direction != "":
                check = self.CheckCollision()
                if check == False:
                    return
            if self.AppleP == self.SHeadP:
                self.SLen = self.SLen + 1
                self.Add_Food()
            self.add_Seg()
            self.Gen_Disp()
    def check_for_snake(self):
        if self.direction == "up":
            for i in self.SSegments:
                if [self.SHeadP[0], self.SHeadP[1] - 10] == i:
                    return False
        elif self.direction == "down":
            for i in self.SSegments:
                if [self.SHeadP[0], self.SHeadP[1]+10] == i:
                    return False
        elif self.direction == "right":
            for i in self.SSegments:
                if [self.SHeadP[0]+10, self.SHeadP[1]] == i:
                    return False
        elif self.direction == "left":
            for i in self.SSegments:
                if [self.SHeadP[0]-10, self.SHeadP[1]] == i:
                    return False
    def Tally_Points(self):
        points = abs(self.SHeadP[0]-self.AppleP[0])+abs(self.SHeadP[1]-self.AppleP[1])
        collision = self.CheckCollision()
        if collision == False:
            points -= 1000
        if self.SHeadP[0] < 0 or self.xdim-self.SHeadS < self.SHeadP[0] or self.SHeadP[1] < 0 or self.ydim-self.SHeadS < self.SHeadP[1]:
            points -= 1000
        if self.AppleP == self.SHeadP:
            points += 100
        return points
    def Blocked_Directions(self):
        list = ["up", "down", "right", "left"]
        count = 0
        while count < self.SLen and list != []:
            if [self.SHeadP[0] - 10, self.SHeadP[1]] == self.SSegments[count] or self.SHeadP[0]-10 < 0:
                for i in range(len(list)):
                    if list[i] == "left":
                        list[i] = None
                        break
            if [self.SHeadP[0] + 10, self.SHeadP[1]] == self.SSegments[count] or self.xdim <= self.SHeadP[0]+10:
                for i in range(len(list)):
                    if list[i] == "right":
                        list[i] = None
                        break
            if [self.SHeadP[0], self.SHeadP[1]-10] == self.SSegments[count] or self.SHeadP[1]-10 < 0:
                for i in range(len(list)):
                    if list[i] == "up":
                        list[i] = None
                        break
            if [self.SHeadP[0], self.SHeadP[1]+10] == self.SSegments[count] or self.ydim <= self.SHeadP[0]+10:
                for i in range(len(list)):
                    if list[i] == "down":
                        list[i] = None
                        break
            count += 1
        holder = list
        list = []
        for i in holder:
            if i != None:
                list.append(i)
        return list
    def set_Snake(self):
        self.xdim = 100
        self.ydim = 100
        self.screen = pygame.display.set_mode([self.xdim, self.ydim])
        self.SnakeC = (0, 255, 0)
        self.AppleC = (255, 0, 0)
        self.AppleP = []
        self.SHeadS = 10
        self.SHeadP = [self.xdim/2, self.ydim/2]
        self.SSegments = [self.SHeadP]
        self.SLen = 0
        self.direction = ""
        self.running = True
        self.LDir = ""
        self.running = True
        self.Add_Food()
    def AI_Snake1(self):
        self.xdim = 100
        self.ydim = 100
        self.screen = pygame.display.set_mode([self.xdim, self.ydim])
        self.SnakeC = (0, 255, 0)
        self.AppleC = (255, 0, 0)
        self.AppleP = []
        self.SHeadS = 10
        self.SHeadP = [self.xdim/2, self.ydim/2]
        self.SSegments = [self.SHeadP]
        self.SLen = 0
        self.direction = ""
        self.running = True
        self.LDir = ""
        self.running = True
        self.Add_Food()
        while self.running == True:
            self.screen = pygame.display.set_mode([self.xdim, self.ydim])
            self.targetApple()
            state = None
            for i in range(len(self.catalogue)):
                array = [self.catalogue[i][0], self.catalogue[i][1], self.catalogue[i][2]]
                if array == [self.SHeadP, self.SSegments, self.AppleP]:
                    state = i
                    break
            directions = ["up", "down", "right", "left"]
            if state != None:
                self.direction = directions[np.argmax(self.qTable[state])]
            self.incramentSnake()
            if self.xdim-10 < self.SHeadP[0] or self.SHeadP[0] < 0 or self.ydim-10 < self.SHeadP[1] or self.SHeadP[1]< 0:
                return
            if self.direction != "":
                check = self.CheckCollision()
                if check == False:
                    self.running = False
            if self.AppleP == self.SHeadP:
                self.SLen = self.SLen + 1
                self.Add_Food()
            self.add_Seg()
            self.Gen_Disp()
        return self.SLen
    def AI_Snake(self):
        self.xdim = 400
        self.ydim = 400
        self.screen = pygame.display.set_mode([self.xdim, self.ydim])
        self.SnakeC = (0, 255, 0)
        self.AppleC = (255, 0, 0)
        self.AppleP = []
        self.SHeadS = 10
        self.SHeadP = [self.xdim - 10, self.ydim - 10]
        self.SSegments = [self.SHeadP]
        self.SLen = 0
        self.direction = ""
        self.running = True
        self.LDir = ""
        self.running = True
        self.Add_Food()
        while self.running == True:
            self.screen = pygame.display.set_mode([self.xdim, self.ydim])
            keys = pygame.key.get_pressed()
            self.targetApple()
            self.direction = self.avoid_edge()
            check = self.check_for_snake()
            if check == False:
                AVdir = self.Blocked_Directions()
                holder = 0
                holder2 = 0
                if len(AVdir) != 0:
                    for z in AVdir:
                        holder2 = self.find_Nearest_Blockage(z)
                        if holder < holder2:
                            holder = holder2
                            self.direction = z
            self.incramentSnake()
            if self.xdim-10 < self.SHeadP[0] or self.SHeadP[0] < 0 or self.ydim-10 < self.SHeadP[1] or self.SHeadP[1]< 0:
                return
            if self.direction != "":
                check = self.CheckCollision()
                if check == False:
                    self.running = False
            if self.AppleP == self.SHeadP:
                self.SLen = self.SLen + 1
                self.Add_Food()
            self.add_Seg()
            self.Gen_Disp()
        return self.SLen

class find_position:
    def find_curr_pos(self, array, identifier):
        for l in range(len(array)):
            if (array[l] == identifier):
                return l
        return -1
class Training:
    def __init__(self):
        self.catalogue = []
        self.q_table = np.zeros((1000000, 4))
        self.game = SNAKEAI()
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.5
        self.viable = False
        self.all_epoch = []
        self.all_penalties = []
        self.catalogue.append([self.game.SHeadP, self.game.SSegments, self.game.AppleP])
    def Train_Q_Table(self):
        checker = find_position()
        for i in range(1, 1000000):
            self.game.set_Snake()
            self.board_pos = [self.game.SHeadP, self.game.SSegments, self.game.AppleP]
            epochs, penalties, reward, = 0, 0, 0
            state = 0
            for x in range(int(self.game.xdim/10)):
                for y in range(int(self.game.ydim/10)):
                    self.game.AppleP = [x * 10, y * 10]
                    while self.game.running == True:
                        self.viable = False
                        moves = ["up", "down", "right", "left"]  # self.game.Blocked_Directions()
                        state = checker.find_curr_pos(self.catalogue, self.board_pos)
                        # print(self.game.SHeadP)
                        if (state == -1):
                            state = len(self.catalogue)
                            self.catalogue.append(self.board_pos)
                        if random.uniform(0, 1) < self.epsilon:
                            action = random.randint(0, len(moves) - 1)
                        else:
                            action = np.argmax(self.q_table[state])
                        if (len(moves) != 0):
                            if (action > len(moves)):
                                action = random.randint(1, len(moves))
                                self.game.direction = moves[action - 1]
                            else:
                                self.game.direction = moves[action - 1]
                        self.game.incramentSnake()
                        # print(self.game.SHeadP)
                        if self.game.direction != "":
                            check = self.game.CheckCollision()
                            if check == False:
                                self.game.running = False
                            if self.game.SHeadP[0] < 0 or self.game.xdim - self.game.SHeadS < self.game.SHeadP[0] or self.game.SHeadP[1] < 0 or self.game.ydim - self.game.SHeadS < self.game.SHeadP[1]:
                                self.game.running = False
                        # print(self.game.running)
                        if self.game.AppleP == self.game.SHeadP:
                            self.game.SLen = self.game.SLen + 1
                            self.game.Add_Food()
                        self.game.add_Seg()
                        self.game.Gen_Disp()
                        nextState = action
                        reward = self.game.Tally_Points()
                        # print(reward)
                        old_value = self.q_table[state, action]
                        next_max = np.max(self.q_table[nextState])
                        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
                        self.q_table[state, action] = new_value
                        if reward == -10:
                            penalties += 1
                        epochs += 1
                        # print(reward)
            if i % 100 == 0:
                print(len(self.catalogue))
                print("Episode: ", i)
                #print(self.game.AppleP)
        outfile = TemporaryFile()
        with open('test.csv', 'wb') as f:
            np.save(f, np.array(self.q_table))
        with open('catalogue.csv', 'wb') as z:
            np.save(z, np.array(self.catalogue, object))
#hello = Training()
#hello.Train_Q_Table()
hello = ""
outfile = TemporaryFile()

while hello != "True":
     hello = str(input("AI1 or AI2: "))
     if hello == "AI1":
        snakegame = SNAKEAI()
        snakegame.AI_Snake1()
     elif hello == "AI2":
         snakegame = SNAKEAI()
         snakegame.AI_Snake()
