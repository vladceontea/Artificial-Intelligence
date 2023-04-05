from Model.Drone import Drone
from Model.Environment import Environment
from Model.Map import DMap
import pickle,pygame,sys

from pygame.locals import *
from random import random, randint
import numpy as np

WHITE = (255, 255, 255)

class Service:
    def __init__(self):
        self.e = Environment()
        self.m = DMap()
        x = randint(0, 19)
        y = randint(0, 19)
        self.d = Drone(x, y)

    def maze(self):

        self.e.loadEnvironment("test2.map")
        pygame.init()
        # load and set the logo
        logo = pygame.image.load("logo32x32.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption("drone exploration")

        # we position the drone somewhere in the area
        x = randint(0, 19)
        y = randint(0, 19)

        # cream drona

        # create a surface on screen that has the size of 800 x 480
        screen = pygame.display.set_mode((800, 400))
        screen.fill(WHITE)
        screen.blit(self.e.image(), (0, 0))

        # define a variable to control the main loop
        running = True
        visited = set()
        stack = [(self.d.x, self.d.y)]
        start = True
        # main loop
        while running:
            # event handling, gets all event from the event queue
            for event in pygame.event.get():
                # only do something if the event is of type QUIT
                if event.type == pygame.QUIT:
                    # change the value to False, to exit the main loop
                    running = False
                '''
                if event.type == KEYDOWN:
                    # use this function instead of move
                    d.moveDSF(m, visited, stack)
                    #print("Stack is" + str(stack))
                    #print("Visited is" + str(visited))
                    #d.move(m)
                '''
            # use this function instead of move

            if not start:
                self.d.moveDSF(self.m, visited, stack)
                # print("Stack is" + str(stack))
                # print("Visited is" + str(visited))

            if not stack:
                running = False
            start = False
            self.m.markDetectedWalls(self.e, self.d.x, self.d.y)
            screen.blit(self.m.image(self.d.x, self.d.y), (400, 0))
            pygame.display.flip()

        pygame.quit()
