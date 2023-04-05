# -*- coding: utf-8 -*-


# imports
import matplotlib.pyplot as pl
from controller.controller import *
from repository.repository import *
from ui.gui import *
from ui.gui import visualise


class Ui:
    def __init__(self, controller):
        self.controller = controller

    def big_menu(self):
        print("1. Map options")
        print("2. Evolutionary algorithm options")
        print("3. Exit")

    def map_menu(self):

        done = False
        print("\n")
        while not done:
            print("1. Create a random map")
            print("2. Load a map")
            print("3. Save a map")
            print("4. Visualise map")
            print("5. Exit map options")

            command2 = input("Enter command: ")
            if command2 == "4":
                visualise(self.controller.repo.cmap)
            elif command2 == "1":
                self.controller.repo.randomMap()
            elif command2 == "2":
                name = input("Please give the name of the file: ")
                self.controller.repo.loadMap(name)
            elif command2 == "3":
                name = input("Please give the name of the file: ")
                self.controller.repo.saveMap(name)
            elif command2 == "5":
                done = True
                print("\n")
            else:
                print("\n")
                print("Not a valid command")
                print("\n")

    def ea_menu(self):
        print("1. Setup parameters")
        print("2. Run solver")
        print("3. Visualise statistics")
        print("4. View drone moving")

        done = False
        path = []
        print("\n")
        while not done:
            print("1. Setup parameters")
            print("2. Run solver")
            print("3. Visualise statistics")
            print("4. View drone moving")
            print("5. Exit ea options")

            command = input("Enter command: ")
            if command == "1":
                pop = input("Please give the population size: ")
                ind = input("Please give the individual size: ")
                it = input("Please give the number of iterations: ")
                mut = input("Please give the probability of mutation: ")
                cross = input("Please give the probability of crossover: ")

                self.controller.setPopulationSize(pop)
                self.controller.setIndividualSize(ind)
                self.controller.setIterations(it)
                self.controller.setMutation(mut)
                self.controller.setCrossoverP(cross)
            elif command == "2":
                start = time.time()
                path = self.controller.solver()
                end = time.time()

                print("Execution time: " + str(end - start))
            elif command == "3":
                if not path:
                    print("Need to run the solver first")
                else:
                    self.visualiseStatistics()
            elif command == "4":
                if not path:
                    print("Need to run the solver first")
                else:
                    self.viewDrone(path)
            elif command == "5":
                done = True
                print("\n")
            else:
                print("\n")
                print("Not a valid command")
                print("\n")

    def main(self):
        finished = False
        print("\n")
        self.controller.repo.cmap.randomMap()

        command_dict = {"1": self.map_menu,
                        "2": self.ea_menu}
        while not finished:
            self.big_menu()
            command = input("Enter command: ")
            if command in command_dict:
                command_dict[command]()
            elif command == "3":
                print("\n")
                print("Application closed")
                finished = True
            else:
                print("\n")
                print("Not a valid command")
                print("\n")

    def viewDrone(self, path):
        print("The path is :")
        print(path)
        movingDrone(self.controller.repo.cmap, path)

    def visualiseStatistics(self):
        runs = [i for i in range(30)]
        iters = [i for i in range(self.controller.iterations)]

        averageFitness = []
        standardDeviation = []
        averageIter = []
        stdIter = []

        fig, plots = pl.subplots(2)

        for i in range(len(self.controller.statistics)):
            averageFitness.append(self.controller.statistics[i][0])
            standardDeviation.append(self.controller.statistics[i][1])

        for j in range(len(self.controller.statisticsIter)):
            averageIter.append(self.controller.statisticsIter[j][0])
            stdIter.append(self.controller.statisticsIter[j][1])

        plots[0].plot(runs, averageFitness)
        plots[0].plot(runs, standardDeviation)
        plots[1].plot(iters, averageIter)
        plots[1].plot(iters, stdIter)

        pl.show()


# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls
