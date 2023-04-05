# -*- coding: utf-8 -*-

from domain.Map import Map
from domain.Population import Population


class Repository:
    def __init__(self):
        self.__populations = []
        self.cmap = Map()
        
    def createPopulation(self, args):
        return Population(args[0], args[1])

    def randomMap(self):
        self.cmap.randomMap()

    def loadMap(self, name):
        self.cmap.loadMap(name)

    def saveMap(self, name):
        self.cmap.saveMap(name)
