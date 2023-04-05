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


class Service:
    def __init__(self):
        self.map = Map()
        self.drone = Drone(0, 0)

    def searchAStar(self, initialX, initialY, finalX, finalY):
        searchQueue = [(0, [initialX, initialY])]
        path = []
        visited = []
        children = {}
        cost = {(initialX, initialY): 0}

        while searchQueue:
            searchQueue.sort(reverse=True)
            current = searchQueue.pop()
            currentX = current[1][0]
            currentY = current[1][1]
            visited.append((currentX, currentY))

            if currentX == finalX and currentY == finalY:
                path.append((finalX, finalY))
                while (initialX, initialY) not in path:
                    path.append(children[path[-1]])
                path.reverse()
                return path, visited

            if currentX > 0:
                if self.map.surface[currentX - 1][currentY] == 0 and (currentX - 1, currentY) not in visited:
                    h = abs(currentX - 1 - finalX) + abs(currentY - finalY)
                    ok = True
                    for elem in searchQueue:
                        if [currentX - 1, currentY] == elem[1]:
                            ok = False
                            if elem[0] > cost[(currentX, currentY)] + 1 + h:
                                searchQueue.remove(elem)
                                children[(currentX - 1, currentY)] = (currentX, currentY)
                                cost[(currentX - 1, currentY)] = cost[(currentX, currentY)] + 1
                                searchQueue.append((cost[(currentX - 1, currentY)] + h, [currentX - 1, currentY]))
                    if ok:
                        children[(currentX - 1, currentY)] = (currentX, currentY)
                        cost[(currentX - 1, currentY)] = cost[(currentX, currentY)] + 1
                        searchQueue.append((cost[(currentX - 1, currentY)] + h, [currentX - 1, currentY]))

            if currentY > 0:
                if self.map.surface[currentX][currentY - 1] == 0 and (currentX, currentY - 1) not in visited:
                    h = abs(currentX - finalX) + abs(currentY - 1 - finalY)
                    ok = True
                    for elem in searchQueue:
                        if [currentX, currentY - 1] == elem[1]:
                            ok = False
                            if elem[0] > cost[(currentX, currentY)] + h + 1:
                                searchQueue.remove(elem)
                                children[(currentX, currentY - 1)] = (currentX, currentY)
                                cost[(currentX, currentY - 1)] = cost[(currentX, currentY)] + 1
                                searchQueue.append((cost[(currentX, currentY - 1)] + h, [currentX, currentY - 1]))
                    if ok:
                        children[(currentX, currentY - 1)] = (currentX, currentY)
                        cost[(currentX, currentY - 1)] = cost[(currentX, currentY)] + 1
                        searchQueue.append((cost[(currentX, currentY - 1)] + h, [currentX, currentY - 1]))

            if currentX < 19:
                if self.map.surface[currentX + 1][currentY] == 0 and (currentX + 1, currentY) not in visited:
                    h = abs(currentX + 1 - finalX) + abs(currentY - finalY)
                    ok = True
                    for elem in searchQueue:
                        if [currentX + 1, currentY] == elem[1]:
                            ok = False
                            if elem[0] > cost[(currentX, currentY)] + h + 1:
                                searchQueue.remove(elem)
                                children[(currentX + 1, currentY)] = (currentX, currentY)
                                cost[(currentX + 1, currentY)] = cost[(currentX, currentY)] + 1
                                searchQueue.append((cost[(currentX + 1, currentY)] + h, [currentX + 1, currentY]))
                    if ok:
                        children[(currentX + 1, currentY)] = (currentX, currentY)
                        cost[(currentX + 1, currentY)] = cost[(currentX, currentY)] + 1
                        searchQueue.append((cost[(currentX + 1, currentY)] + h, [currentX + 1, currentY]))

            if currentY < 19:
                if self.map.surface[currentX][currentY + 1] == 0 and (currentX, currentY + 1) not in visited:
                    h = abs(currentX - finalX) + abs(currentY + 1 - finalY)
                    ok = True
                    for elem in searchQueue:
                        if [currentX, currentY + 1] == elem[1]:
                            ok = False
                            if elem[0] > cost[(currentX, currentY)] + h + 1:
                                searchQueue.remove(elem)
                                children[(currentX, currentY + 1)] = (currentX, currentY)
                                cost[(currentX, currentY + 1)] = cost[(currentX, currentY)] + 1
                                searchQueue.append((cost[(currentX, currentY + 1)] + h, [currentX, currentY + 1]))
                    if ok:
                        children[(currentX, currentY + 1)] = (currentX, currentY)
                        cost[(currentX, currentY + 1)] = cost[(currentX, currentY)] + 1
                        searchQueue.append((cost[(currentX, currentY + 1)] + h, [currentX, currentY + 1]))


    def searchGreedy(self, initialX, initialY, finalX, finalY):

        searchQueue = [(0, [initialX, initialY])]
        path = []
        visited = []
        children = {}

        while searchQueue:
            searchQueue.sort(reverse=True)
            current = searchQueue.pop()
            currentX = current[1][0]
            currentY = current[1][1]
            visited.append((currentX, currentY))

            if currentX == finalX and currentY == finalY:
                path.append((finalX, finalY))
                while (initialX, initialY) not in path:
                    path.append(children[path[-1]])
                path.reverse()
                return path, visited

            if currentX > 0:
                if self.map.surface[currentX - 1][currentY] == 0 and (currentX - 1, currentY) not in visited:
                    h = abs(currentX - 1 - finalX) + abs(currentY - finalY)
                    searchQueue.append((h, [currentX - 1, currentY]))
                    children[(currentX - 1, currentY)] = (currentX, currentY)

            if currentY > 0:
                if self.map.surface[currentX][currentY - 1] == 0 and (currentX, currentY - 1) not in visited:
                    h = abs(currentX - finalX) + abs(currentY - 1 - finalY)
                    searchQueue.append((h, [currentX, currentY - 1]))
                    children[(currentX, currentY - 1)] = (currentX, currentY)

            if currentX < 19:
                if self.map.surface[currentX + 1][currentY] == 0 and (currentX + 1, currentY) not in visited:
                    h = abs(currentX + 1 - finalX) + abs(currentY - finalY)
                    searchQueue.append((h, [currentX + 1, currentY]))
                    children[(currentX + 1, currentY)] = (currentX, currentY)

            if currentY < 19:
                if self.map.surface[currentX][currentY + 1] == 0 and (currentX, currentY + 1) not in visited:
                    h = abs(currentX - finalX) + abs(currentY + 1 - finalY)
                    searchQueue.append((h, [currentX, currentY + 1]))
                    children[(currentX, currentY + 1)] = (currentX, currentY)


    def dummysearch(self):
        # example of some path in test1.map from [5,7] to [7,11]
        return [[5, 7], [5, 8], [5, 9], [5, 10], [5, 11], [6, 11], [7, 11]]