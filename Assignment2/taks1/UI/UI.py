from Service import Service
from Model.Map import Map
from Model.Drone import Drone

import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np

BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class UI:
    def __init__(self, s):
        self.service = s

    def displayStartFinish(self, image, initialX, initialY, finishX, finishY):
        mark1 = pygame.Surface((20, 20))
        mark1.fill((255, 182, 193))
        mark2 = pygame.Surface((20, 20))
        mark2.fill((221, 160, 221))

        image.blit(mark1, (initialY * 20, initialX * 20))
        image.blit(mark2, (finishY * 20,finishX * 20))

        return image

    def displayVisited(self, image, visited):

        markv = pygame.Surface((20, 20))
        markv.fill((255, 255, 0))

        for move in visited[1:-1]:
            image.blit(markv, (move[1] * 20, move[0] * 20))

        return image

    def displayWithPath(self, image, move):
        mark = pygame.Surface((20, 20))
        mark.fill(GREEN)
        image.blit(mark, (move[1] * 20, move[0] * 20))

        return image

    def displayDrone(self, image, drone, move):

        image.blit(drone, (move[1] * 20, move[0] * 20))

        return image

    def show(self):

        self.service.map.loadMap("test1.map")
        pygame.init()

        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Path in simple environment")
        drone = pygame.image.load("drona.png")

        while True:
            x = randint(0, 19)
            y = randint(0, 19)
            if self.service.map.surface[x, y] == 0 and (x,y) != (0,1) and (x,y) != (0,0) and (x,y) != (5,19) and (x,y) != (19,5):
                break

        self.service.drone = Drone(x, y)

        screen = pygame.display.set_mode((400, 400))
        screen.fill(WHITE)

        screen.blit(self.service.drone.mapWithDrone(self.service.map.image()), (0, 0))
        pygame.display.flip()

        while True:
            finalX = randint(0, 19)
            finalY = randint(0, 19)
            if self.service.map.surface[finalX, finalY] == 0 and (finalX,finalY) != (0,1) and (finalX,finalY) != (0,0) and (finalX,finalY) != (5,19) and (finalX,finalY) != (19,5):
                break

        initialX = self.service.drone.x
        initialY = self.service.drone.y

        print(initialX, initialY)
        print(finalX, finalY)

        startAStar = time.time()
        path, visited = self.service.searchAStar(initialX, initialY, finalX, finalY)
        endAStar = time.time()
        print("AStar execution time: " + str((endAStar - startAStar)))
        print(*path)
        print("AStar length: " + str(len(path)))

        astarImage = self.service.map.image()
        screen.blit(self.displayStartFinish(astarImage, initialX, initialY, finalX, finalY), (0, 0))
        screen.blit(self.displayVisited(astarImage, visited), (0, 0))
        pygame.display.flip()

        for move in path[1:-1]:
            screen.blit(self.displayDrone(astarImage, drone, move), (0, 0))
            pygame.display.flip()
            pygame.time.delay(300)
            screen.blit(self.displayWithPath(astarImage, move), (0, 0))
            pygame.display.flip()

        time.sleep(10)

        startGreedy = time.time()
        path, visited = self.service.searchGreedy(initialX, initialY, finalX, finalY)
        endGreedy = time.time()
        print("Greedy execution time: " + str((endGreedy - startGreedy)))
        print(*path)
        print("Greedy length: " + str(len(path)))

        greedyImage = self.service.map.image()
        screen.blit(self.displayStartFinish(greedyImage, initialX, initialY, finalX, finalY), (0, 0))
        screen.blit(self.displayVisited(greedyImage, visited), (0, 0))

        for move in path[1:-1]:
            screen.blit(self.displayDrone(greedyImage, drone, move), (0, 0))
            pygame.display.flip()
            pygame.time.delay(300)
            screen.blit(self.displayWithPath(greedyImage, move), (0, 0))
            pygame.display.flip()

        time.sleep(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
