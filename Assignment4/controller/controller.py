
import time
from random import randint

import numpy as np
import pygame

from domain.Ant import Ant
from domain.Map import Map


class Controller:
    def __init__(self, args):
        self.__noEpoch = args[0]
        self.__noAnts = args[1]
        self.__alpha = args[2]
        self.__beta = args[3]
        self.__rho = args[4]
        self.__q0 = args[5]
        self.__noSensors = args[6]
        self.__energy = args[7]
        self.__cmap = Map()

    def set_noEpoch(self, new):
        self.__noEpoch = new

    def set_noAnts(self, new):
        self.__noAnts = new

    def set_alpha(self, new):
        self.__alpha = new

    def set_beta(self, new):
        self.__beta = new

    def set_rho(self, new):
        self.__rho = new

    def set_q0(self, new):
        self.__q0 = new

    def set_noSensors(self, new):
        self.__noSensors = new

    def set_energy(self, new):
        self.__energy = new

    def get_map(self):
        return self.__cmap

    def sensor_energy(self, sensor):
        sensor_energy = []
        sensor_energy_total = []
        currX = sensor[0]
        currY = sensor[1]
        for i in range(1, 6):
            sensor_energy.append([0, 0, 0, 0])
            sensor_energy_total.append(4)
            if not self.possible(currX-i, currY):
                sensor_energy[-1][0] = 1
                sensor_energy_total[-1] -= 1
            if not self.possible(currX+i, currY):
                sensor_energy[-1][1] = 1
                sensor_energy_total[-1] -= 1
            if not self.possible(currX, currY-i):
                sensor_energy[-1][2] = 1
                sensor_energy_total[-1] -= 1
            if not self.possible(currX, currY+i):
                sensor_energy[-1][3] = 1
                sensor_energy_total[-1] -= 1

            if len(sensor_energy) > 1:
                for j in range(4):
                    if sensor_energy[-2][j] == 1:
                        if sensor_energy[-1][j] != 1:
                            sensor_energy[-1][j] = 1
                            sensor_energy_total[-1] -= 1

        return sensor_energy, sensor_energy_total

    def epoch(self, startX, startY, sensors, trace, distances):
        antSet = [Ant(startX, startY, self.__cmap, sensors, distances) for i in range(self.__noAnts)]

        for i in range(self.__noSensors):
            for x in antSet:
                x.add_moves(self.__q0, self.__alpha, self.__beta, trace)

        d_trace = [1.0 / antSet[i].fitness() for i in range(len(antSet))]

        for i in range(20*20):
            for j in range(20*20):
                trace[i][j] = (1-self.__rho) * trace[i][j]

        for i in range(len(antSet)):
            for j in range(len(antSet[i].get_path())-1):
                x = antSet[i].get_path()[j]
                y = antSet[i].get_path()[j + 1]
                trace[x][y] = trace[x][y] + d_trace[i]

        f = [[antSet[i].fitness(), i] for i in range(len(antSet))]
        f = min(f)

        return antSet[f[1]]

    def init_positions(self):
        startPos = [0, 0]
        startPos[0] = randint(0, 19)
        startPos[1] = randint(0, 19)
        while self.__cmap.surface[startPos[0]][startPos[1]] != 0:
            startPos[0] = randint(0, 19)
            startPos[1] = randint(0, 19)

        sensorPos = []
        for i in range(self.__noSensors):
            sensorPos.append([0, 0])
            sensorPos[i][0] = randint(0, 19)
            sensorPos[i][1] = randint(0, 19)
            while self.__cmap.surface[sensorPos[i][0]][sensorPos[i][1]] != 0:
                sensorPos[i][0] = randint(0, 19)
                sensorPos[i][1] = randint(0, 19)

        return startPos, sensorPos

    def solver(self):

        startPos, sensorPos = self.init_positions()

        distances, paths = self.distance_sensors(sensorPos, startPos)

        print(distances)
        print(sensorPos)
        print(startPos)

        solution = None
        best_sol = None
        trace = [[1 for i in range(20*20)] for j in range(20*20)]

        for i in range(self.__noEpoch):
            solution = self.epoch(startPos[0], startPos[1], sensorPos, trace, distances)

            if best_sol is None:
                best_sol = solution

            if solution.fitness() < best_sol.fitness():
                best_sol = solution

        total_path = []
        total_length = 0
        best_path_partial = []

        for i in range(len(best_sol.get_path()[:-1])):
            first = best_sol.get_path()[i]
            last = best_sol.get_path()[i + 1]
            if total_length + distances[first][last] >= self.__energy:
                break
            else:
                if len(total_path) != 0:
                    total_path.pop()
                    best_path_partial.pop()
                best_path_partial.append(first)
                best_path_partial.append(last)
                total_length = total_length + distances[first][last]
                total_path.extend(paths[first][last])

        remaining_energy = self.__energy - total_length
        sensor_energy = []
        sensor_energy_total = []

        if total_length != best_sol.fitness():

            sensorPos_partial = []
            for i in best_path_partial[1:]:
                sensorPos_partial.append(sensorPos[i])

            for i in range(len(sensorPos_partial)):
                sensor_energy.append(self.sensor_energy(sensorPos_partial[i])[0])
                sensor_energy_total.append(self.sensor_energy(sensorPos_partial[i])[1])
            cells = self.handle_energy(sensor_energy, sensor_energy_total, sensorPos_partial, remaining_energy)

        else:

            for i in range(len(sensorPos)):
                sensor_energy.append(self.sensor_energy(sensorPos[i])[0])
                sensor_energy_total.append(self.sensor_energy(sensorPos[i])[1])
            cells = self.handle_energy(sensor_energy, sensor_energy_total, sensorPos, remaining_energy)

        return total_length, total_path, startPos, sensorPos, cells

    def handle_energy(self, sensor_energy, sensor_energy_total, sensorPos, energy):

        print("The energy for sensors is " + str(energy))

        energy_cells = []
        possible_energy = []
        possible_energy_total = []
        energy_pos = [0 for i in range(len(sensorPos))]
        for i in range(len(sensorPos)):
            possible_energy.append(sensor_energy[i][0])
            possible_energy_total.append(sensor_energy_total[i][0])

        while energy > 0:
            if possible_energy_total == [-1 for i in range(len(sensorPos))]:
                break
            max_value = max(possible_energy_total)
            max_index = possible_energy_total.index(max_value)

            if possible_energy[max_index][0] == 0 and energy > 0 \
                    and [sensorPos[max_index][0]-(energy_pos[max_index]+1), sensorPos[max_index][1]] not in (energy_cells or sensorPos):
                energy -= 1
                energy_cells.append([sensorPos[max_index][0]-(energy_pos[max_index]+1), sensorPos[max_index][1]])
            if possible_energy[max_index][1] == 0 and energy > 0 \
                    and [sensorPos[max_index][0]+(energy_pos[max_index]+1), sensorPos[max_index][1]] not in (energy_cells or sensorPos):
                energy -= 1
                energy_cells.append([sensorPos[max_index][0]+(energy_pos[max_index]+1), sensorPos[max_index][1]])
            if possible_energy[max_index][2] == 0 and energy > 0 \
                    and [sensorPos[max_index][0], sensorPos[max_index][1]-(energy_pos[max_index]+1)] not in (energy_cells or sensorPos):
                energy -= 1
                energy_cells.append([sensorPos[max_index][0], sensorPos[max_index][1]-(energy_pos[max_index]+1)])
            if possible_energy[max_index][3] == 0 and energy > 0 \
                    and [sensorPos[max_index][0], sensorPos[max_index][1]+(energy_pos[max_index]+1)] not in (energy_cells or sensorPos):
                energy -= 1
                energy_cells.append([sensorPos[max_index][0], sensorPos[max_index][1]+(energy_pos[max_index]+1)])

            energy_pos[max_index] += 1
            if energy_pos[max_index] > 4:
                possible_energy_total[max_index] = -1
                possible_energy[max_index] = [-1, -1, -1, -1]
            else:
                possible_energy_total[max_index] = sensor_energy_total[max_index][energy_pos[max_index]]
                possible_energy[max_index] = sensor_energy[max_index][energy_pos[max_index]]

        print("The remaining energy (if there is any) is " + str(energy))

        return energy_cells

    def possible(self, x, y):
        if 0 <= x < 20 and 0 <= y < 20 and self.__cmap.surface[x][y] != 1:
            return True
        return False

    def distance_sensors(self, sensors, start):

        distances = [[0 for i in range(self.__noSensors+1)] for j in range(self.__noSensors+1)]
        paths = [[[] for i in range(self.__noSensors+1)] for j in range(self.__noSensors+1)]

        for i in range(self.__noSensors):
            for j in range(i + 1, self.__noSensors):
                path = self.searchAStar(sensors[i][0], sensors[i][1], sensors[j][0], sensors[j][1])
                dist = len(path)-1
                distances[i][j] = distances[j][i] = dist
                paths[i][j] = path
                paths[j][i] = path[::-1]

        for i in range(self.__noSensors):
            path = self.searchAStar(sensors[i][0], sensors[i][1], start[0], start[1])
            dist = len(path)-1
            paths[i][self.__noSensors] = path
            paths[self.__noSensors][i] = path[::-1]
            distances[i][self.__noSensors] = distances[self.__noSensors][i] = dist

        return distances, paths

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
                return path

            if currentX > 0:
                if self.__cmap.surface[currentX - 1][currentY] == 0 and (currentX - 1, currentY) not in visited:
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
                if self.__cmap.surface[currentX][currentY - 1] == 0 and (currentX, currentY - 1) not in visited:
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
                if self.__cmap.surface[currentX + 1][currentY] == 0 and (currentX + 1, currentY) not in visited:
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
                if self.__cmap.surface[currentX][currentY + 1] == 0 and (currentX, currentY + 1) not in visited:
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