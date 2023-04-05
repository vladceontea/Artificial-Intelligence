# -*- coding: utf-8 -*-
import pickle
from random import *

from domain.Individual import *
import numpy as np


class Population:
    def __init__(self, populationSize=0, individualSize=0):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize) for x in range(populationSize)]

    def evaluate(self, cmap, currentPos):
        for individual in self.__v:
            individual.fitness(cmap, currentPos)

    def selection(self, k):

        selected = sorted(self.__v, key=lambda i: i.getFitness(), reverse=True)
        return selected[:k]

    def getSize(self):
        return self.__populationSize

    def getPopulation(self):
        return self.__v

    def setPopulation(self, newPopulation):
        self.__v = newPopulation

    def getAverageFitness(self):
        fitness = []
        for individual in self.__v:
            fitness.append(individual.getFitness())

        return np.average(fitness)

    def getAverageStd(self):
        fitness = []
        for individual in self.__v:
            fitness.append(individual.getFitness())

        return np.std(fitness)
