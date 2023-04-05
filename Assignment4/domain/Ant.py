# -*- coding: utf-8 -*-
import pickle
from random import *
from utils import *
import numpy as np


class Ant:

    def __init__(self, startX, startY, cmap, sensors, distances):
        self.__path = [len(sensors)]
        self.__length = 0
        self.__cmap = cmap
        self.__sensors = sensors
        self.__startX = startX
        self.__startY = startY
        self.__distances = distances

    def get_path(self):
        return self.__path

    def fitness(self):
        return self.__length

    def next_moves(self):
        new = []
        for i in range(len(self.__sensors)):
            if i not in self.__path:
                new.append(i)
        return new.copy()

    def add_moves(self, q0, alpha, beta, trace):
        p = [0 for i in range(len(self.__sensors))]

        nextSteps = self.next_moves().copy()

        if len(nextSteps) == 0:
            return False

        for i in nextSteps:
            p[i] = self.dist_moves(i)

        p = [(p[i] ** beta) * (trace[self.__path[-1]][i] ** alpha) for i in range(len(p))]
        if random() < q0:
            p = [[i, p[i]] for i in range(len(p))]
            p = max(p, key=lambda a: a[1])
            self.__path.append(p[0])
            self.__length += self.__distances[self.__path[-1]][self.__path[-2]]
        else:
            s = sum(p)
            if s == 0:
                return choice(nextSteps)
            p = [p[i] / s for i in range(len(p))]
            p = [sum(p[0:i + 1]) for i in range(len(p))]
            r = random()
            i = 0
            while r > p[i]:
                i = i + 1
            self.__path.append(i)
            self.__length += self.__distances[self.__path[-1]][self.__path[-2]]

        return True

    def dist_moves(self, a):
        dummy = Ant(self.__startX, self.__startY, self.__cmap, self.__sensors, self.__distances)
        dummy.path = self.__path.copy()
        dummy.path.append(a)
        return len(self.__sensors) + 1 - len(dummy.next_moves())
