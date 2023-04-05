import pickle,pygame,sys
from pygame.locals import *
from random import random, randint
import numpy as np


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()

        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1

        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y-1]==0:
                self.y = self.y - 1
        if self.y < 19:
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                self.y = self.y + 1

    def moveDSF(self, detectedMap, visited, stack):
        if stack:
            if (self.x, self.y) not in visited:
                #print("position " + str((self.x, self.y)))
                visited.add((self.x, self.y))
                pygame.time.delay(100)
                if self.x > 0:
                    if detectedMap.surface[self.x-1][self.y] == 0:
                        stack.append((self.x - 1, self.y))

                if self.y > 0:
                    if detectedMap.surface[self.x][self.y - 1] == 0:
                        stack.append((self.x, self.y - 1))

                if self.x < 19:
                    if detectedMap.surface[self.x + 1][self.y] == 0:
                        stack.append((self.x + 1, self.y))

                if self.y < 19:
                    if detectedMap.surface[self.x][self.y + 1] == 0:
                        stack.append((self.x, self.y + 1))

            coord = stack.pop()
            self.x = coord[0]
            self.y = coord[1]
