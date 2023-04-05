# -*- coding: utf-8 -*-

import pygame, time
from utils import *


def initPyGame(dimension):
    # init the pygame
    pygame.init()
    logo = pygame.image.load("./logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("drone exploration with AE")
    
    # create a surface on screen that has the size of 800 x 480
    screen = pygame.display.set_mode(dimension)
    screen.fill(WHITE)
    return screen


def closePyGame():
    # closes the pygame
    running = True
    # loop for events
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    pygame.quit()
    

def displaySensors(image, start, sensors):
    mark1 = pygame.Surface((20, 20))
    mark1.fill((255, 182, 193))
    mark = [pygame.Surface((20,20)) for i in range(len(sensors))]
    for i in range(len(sensors)):
        mark[i].fill((221, 160, 221))

    image.blit(mark1, (start[1] * 20, start[0] * 20))
    for i in range(len(sensors)):
        image.blit(mark[i], (sensors[i][1] * 20,sensors[i][0] * 20))

    return image


def image(currentMap, colour = BLUE, background = WHITE):
    # creates the image of a map
    
    imagine = pygame.Surface((currentMap.n * 20, currentMap.m * 20))
    brick = pygame.Surface((20,20))
    brick.fill(colour)
    imagine.fill(background)
    for i in range(currentMap.n):
        for j in range(currentMap.m):
            if currentMap.surface[i][j] == 1:
                imagine.blit(brick, (j * 20, i * 20))
                
    return imagine


def displayWithPath(image, move):
    mark = pygame.Surface((20, 20))
    mark.fill(GREEN)
    image.blit(mark, (move[1] * 20, move[0] * 20))

    return image


def displayDrone(image, drone, move):
    image.blit(drone, (move[1] * 20, move[0] * 20))
    return image


def displayEnergy(image, energy):

    mark = [pygame.Surface((20,20)) for i in range(len(energy))]
    for i in range(len(energy)):
        mark[i].fill((255, 255, 0))
    for i in range(len(energy)):
        image.blit(mark[i], (energy[i][1] * 20,energy[i][0] * 20))

    return image


def visualise(currentMap):
    screen = initPyGame((400, 400))
    screen.blit(image(currentMap), (0,0))
    pygame.display.flip()
    pygame.time.delay(500)
    closePyGame()
