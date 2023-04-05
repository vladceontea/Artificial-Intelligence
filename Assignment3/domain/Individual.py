# -*- coding: utf-8 -*-
import pickle
from random import *

from domain.Gene import *
from utils import *
import numpy as np


class Individual:
    def __init__(self, size=0):
        self.__size = size
        self.__x = [Gene() for i in range(self.__size)]
        self.__f = None

    def getFitness(self):
        return self.__f

    def path(self, currentPos):
        path = [(currentPos[0], currentPos[1])]

        for gene in self.__x:
            newPosX = path[-1][0] + v[gene.direction][0]
            newPosY = path[-1][1] + v[gene.direction][1]

            path.append((newPosX, newPosY))
        return path

    def fitness(self, cmap, currentPos):
        self.__f = 0

        path = self.path(currentPos)
        visited = []
        for position in path:
            currPosX = position[0]
            currPosY = position[1]

            if (currPosX, currPosY) not in visited:
                if self.possible(currPosX, currPosY, cmap):
                    self.__f += 10
                    visited.append((currPosX, currPosY))

                    for direction in v:
                        newPosX = currPosX + direction[0]
                        newPosY = currPosY + direction[1]

                        while self.possible(newPosX, newPosY, cmap):
                            if (newPosX, newPosY) not in visited:
                                self.__f += 10
                                visited.append((newPosX, newPosY))

                            newPosX = newPosX + direction[0]
                            newPosY = newPosY + direction[1]
                else:
                    self.__f = self.__f - 100

    def mutate(self, mutateProbability=0.04):
        if random() < mutateProbability:
            p = randint(0, self.__size - 1)
            self.__x[p] = Gene()

    def crossover(self, otherParent, crossoverProbability=0.8):
        offspring1, offspring2 = Individual(self.__size), Individual(self.__size)
        if random() < crossoverProbability:
            p = 0.5
            for i in range(self.__size):
                if random() < p:
                    offspring1.__x[i] = self.__x[i]
                    offspring2.__x[i] = otherParent.__x[i]
                else:
                    offspring1.__x[i] = otherParent.__x[i]
                    offspring2.__x[i] = self.__x[i]

        return offspring1, offspring2

    def possible(self, x, y, cmap):
        if 0 <= x < 20 and 0 <= y < 20 and cmap.surface[x][y] != 1:
            return True
        return False
