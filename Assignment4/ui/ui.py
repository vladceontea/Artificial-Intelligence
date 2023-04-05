# -*- coding: utf-8 -*-


# imports
from controller.controller import *
from ui.gui import *
from ui.gui import initPyGame


class Ui:
    def __init__(self, controller):
        self.controller = controller

    def big_menu(self):
        print("1. Map options")
        print("2. ACO options")
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
                visualise(self.controller.get_map())
            elif command2 == "1":
                self.controller.get_map().randomMap()
            elif command2 == "2":
                name = input("Please give the name of the file: ")
                self.controller.get_map().loadMap(name)
            elif command2 == "3":
                name = input("Please give the name of the file: ")
                self.controller.get_map().saveMap(name)
            elif command2 == "5":
                done = True
                print("\n")
            else:
                print("\n")
                print("Not a valid command")
                print("\n")

    def ea_menu(self):

        done = False
        total_path = []
        startPos = []
        sensorPos = []
        cells = []
        print("\n")
        while not done:
            print("1. Setup parameters")
            print("2. Run algorithm")
            print("3. View drone moving")
            print("4. Exit ea options")

            command = input("Enter command: ")
            if command == "1":
                epochs = input("Please give the number of epochs: ")
                ants = input("Please give the number of ants: ")
                alpha = input("Please give the value of alpha: ")
                beta = input("Please give the value of beta: ")
                rho = input("Please give the value of rho: ")
                q0 = input("Please give the value of q0: ")
                sensors = input("Please give the number of sensors: ")
                energy = input("Please give the value of the energy of the drone: ")

                self.controller.set_noEpoch(epochs)
                self.controller.set_noAnts(ants)
                self.controller.set_alpha(alpha)
                self.controller.set_beta(beta)
                self.controller.set_rho(rho)
                self.controller.set_q0(q0)
                self.controller.set_noSensors(sensors)
                self.controller.set_energy(energy)

            elif command == "2":
                start = time.time()
                length, total_path, startPos, sensorPos, cells = self.controller.solver()
                end = time.time()

                print("Execution time: " + str(end - start))

                print("The best path is: ")
                print(*total_path)

                print("The length is: " + str(length))

                #if not cells:
                    #print("Not enough energy to reach all sensors")
            elif command == "3":
                if not total_path:
                    print("Need to run the solver first")
                else:
                    self.viewDrone(total_path, startPos, sensorPos, cells)
            elif command == "4":
                done = True
                print("\n")
            else:
                print("\n")
                print("Not a valid command")
                print("\n")

    def main(self):
        finished = False
        print("\n")
        self.controller.get_map().randomMap()

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

    def viewDrone(self, path, startPos, sensorPos, cells):

        screen = initPyGame((self.controller.get_map().n * 20, self.controller.get_map().m * 20))
        drone = pygame.image.load("drona.png")
        imagine = image(self.controller.get_map())

        screen.blit(displaySensors(imagine, startPos, sensorPos), (0, 0))
        pygame.display.flip()

        for move in path:
            screen.blit(displayDrone(imagine, drone, move), (0, 0))
            pygame.display.flip()
            pygame.time.delay(300)
            screen.blit(displayWithPath(imagine, move), (0, 0))
            pygame.display.flip()

        screen.blit(displayEnergy(imagine, cells), (0, 0))
        pygame.display.flip()
        screen.blit(displaySensors(imagine, startPos, sensorPos), (0, 0))
        pygame.display.flip()

        closePyGame()


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
