import time
from random import seed, randint

import numpy as np


class Controller:
    def __init__(self, repository, args):
        self.repo = repository
        self.populationSize = args[0]
        self.individualSize = args[1]
        self.iterations = args[2]
        self.mutationP = args[3]
        self.crossoverP = args[4]
        self.statistics = []
        self.statisticsIter = []

    def setPopulationSize(self, newSize):
        self.populationSize = newSize

    def setIndividualSize(self, newSize):
        self.individualSize = newSize

    def setIterations(self, newIterations):
        self.iterations = newIterations

    def setMutation(self, newMutationP):
        self.mutationP = newMutationP

    def setCrossoverP(self, newCrossoverP):
        self.crossoverP = newCrossoverP

    def iteration(self, population, startPos):

        parentsSelected = population.selection(int(self.populationSize * 0.7))
        new = []

        while len(new) + len(parentsSelected) < self.populationSize:
            i1 = randint(0, len(parentsSelected) - 1)
            i2 = randint(0, len(parentsSelected) - 1)
            if parentsSelected[i1] != parentsSelected[i2]:
                c1, c2 = parentsSelected[i1].crossover(parentsSelected[i2], self.crossoverP)
                c1.mutate(self.mutationP)
                c2.mutate(self.mutationP)
                c1.fitness(self.repo.cmap, startPos)
                c2.fitness(self.repo.cmap, startPos)
                new.append(c1)
                new.append(c2)

        parentsSelected.extend(new)
        population.setPopulation(parentsSelected)
        return population
        
    def run(self, population, startPos, stat):
        averageFitness = []

        for i in range(self.iterations):
            population.evaluate(self.repo.cmap, startPos)
            population = self.iteration(population, startPos)
            averageFitness.append(population.getAverageFitness())
            if stat:
                self.statisticsIter.append((population.getAverageFitness(), population.getAverageStd()))

        self.statistics.append((np.average(averageFitness), np.std(averageFitness)))

    def solver(self):
        startPos = [0, 0]
        startPos[0] = randint(0, 19)
        startPos[1] = randint(0, 19)
        while self.repo.cmap.surface[startPos[0]][startPos[1]] != 0:
            startPos[0] = randint(0, 19)
            startPos[1] = randint(0, 19)

        populations = []

        for i in range(30):
            stat = False
            randomSeed = time.time()
            seed(randomSeed)

            population = self.repo.createPopulation([self.populationSize, self.individualSize])
            populations.append(population)
            if i == 7:
                stat = True
            self.run(population, startPos, stat)

        bestPopulation = sorted(populations, key=lambda j: j.getAverageFitness(), reverse=True)[0]
        bestIndividual = sorted(bestPopulation.getPopulation(), key=lambda k: k.getFitness(), reverse=True)[0]
        path = bestIndividual.path(startPos)
        return path

       