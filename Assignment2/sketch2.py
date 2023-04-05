

# import the pygame module, so you can use it
import pickle,pygame,time
from pygame.locals import *
from random import random, randint
import numpy as np


#Creating some colors
BLUE  = (0, 0, 255)
GRAYBLUE = (50,120,120)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#define directions
UP = 0
DOWN = 2
LEFT = 1
RIGHT = 3

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]


class Map():
    def __init__(self, n = 20, m = 20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))
    
    def randomMap(self, fill = 0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill :
                    self.surface[i][j] = 1
                
    def __str__(self):
        string=""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
                
    def saveMap(self, numFile = "test.map"):
        with open(numFile,'wb') as f:
            pickle.dump(self, f)
            f.close()
        
    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
        
    def image(self, colour = BLUE, background = WHITE):
        imagine = pygame.Surface((400,400))
        brick = pygame.Surface((20,20))
        brick.fill(BLUE)
        imagine.fill(WHITE)
        for i in range(self.n):
            for j in range(self.m):
                if (self.surface[i][j] == 1):
                    imagine.blit(brick, ( j * 20, i * 20))
                
        return imagine        
        

class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1
        
        if self.y > 0:
            if pressed_keys[K_LEFT] and detectedMap.surface[self.x][self.y-1]==0:
                self.y = self.y - 1
        if self.y < 19:        
            if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                 self.y = self.y + 1
                  
    def mapWithDrone(self, mapImage):
        drona = pygame.image.load("drona.png")
        mapImage.blit(drona, (self.y * 20, self.x * 20))
        
        return mapImage


def searchAStar(mapM, droneD, initialX, initialY, finalX, finalY):
    screen = pygame.display.set_mode((400, 400))
    screen.fill(WHITE)
    screen.blit(droneD.mapWithDrone(mapM.image()), (0, 0))
    pygame.display.flip()
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
        #pygame.time.delay(100)

        if currentX == finalX and currentY == finalY:
            path.append((finalX, finalY))
            while (initialX, initialY) not in path:
                path.append(children[path[-1]])
            path.reverse()
            return path, visited

        if currentX > 0:
            if mapM.surface[currentX - 1][currentY] == 0 and (currentX - 1, currentY) not in visited:
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
            if mapM.surface[currentX][currentY - 1] == 0 and (currentX, currentY - 1) not in visited:
                h = abs(currentX - finalX) + abs(currentY - 1 - finalY)
                ok = True
                for elem in searchQueue:
                    if [currentX, currentY-1] == elem[1]:
                        ok = False
                        if elem[0] > cost[(currentX, currentY)] + h + 1:
                            searchQueue.remove(elem)
                            children[(currentX, currentY - 1)] = (currentX, currentY)
                            cost[(currentX, currentY - 1)] = cost[(currentX, currentY)] + 1
                            searchQueue.append((cost[(currentX, currentY - 1)] + h, [currentX, currentY - 1]))
                if ok:
                    children[(currentX, currentY - 1)] = (currentX, currentY)
                    cost[(currentX, currentY - 1)] = cost[(currentX, currentY)] + 1
                    searchQueue.append((cost[(currentX, currentY-1)] + h, [currentX, currentY - 1]))

        if currentX < 19:
            if mapM.surface[currentX + 1][currentY] == 0 and (currentX + 1, currentY) not in visited:
                h = abs(currentX + 1 - finalX) + abs(currentY - finalY)
                ok = True
                for elem in searchQueue:
                    if [currentX + 1, currentY] == elem[1]:
                        ok = False
                        if elem[0] > cost[(currentX, currentY)] + h+1:
                            searchQueue.remove(elem)
                            children[(currentX + 1, currentY)] = (currentX, currentY)
                            cost[(currentX + 1, currentY)] = cost[(currentX, currentY)] + 1
                            searchQueue.append((cost[(currentX + 1, currentY)] + h, [currentX + 1, currentY]))
                if ok:
                    children[(currentX + 1, currentY)] = (currentX, currentY)
                    cost[(currentX + 1, currentY)] = cost[(currentX, currentY)] + 1
                    searchQueue.append((cost[(currentX + 1, currentY)] + h, [currentX + 1, currentY]))

        if currentY < 19:
            if mapM.surface[currentX][currentY + 1] == 0 and (currentX, currentY + 1) not in visited:
                h = abs(currentX - finalX) + abs(currentY + 1 - finalY)
                ok = True
                for elem in searchQueue:
                    if [currentX, currentY+1] == elem[1]:
                        ok = False
                        if elem[0] > cost[(currentX, currentY)] + h + 1:
                            searchQueue.remove(elem)
                            children[(currentX, currentY + 1)] = (currentX, currentY)
                            cost[(currentX, currentY + 1)] = cost[(currentX, currentY)] + 1
                            searchQueue.append((cost[(currentX, currentY + 1)] + h, [currentX, currentY + 1]))
                if ok:
                    children[(currentX, currentY + 1)] = (currentX, currentY)
                    cost[(currentX, currentY + 1)] = cost[(currentX, currentY)] + 1
                    searchQueue.append((cost[(currentX, currentY+1)] + h, [currentX, currentY + 1]))

        screen.blit(droneD.mapWithDrone(mapM.image()), (0, 0))
        pygame.display.flip()


def searchGreedy(mapM, droneD, initialX, initialY, finalX, finalY):
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)
    screen.blit(droneD.mapWithDrone(mapM.image()), (0, 0))
    pygame.display.flip()
    searchQueue = [(0, [initialX, initialY])]
    path = []
    visited = []
    children = {}

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
            return path, visited

        if currentX > 0:
            if mapM.surface[currentX - 1][currentY] == 0 and (currentX-1, currentY) not in visited:
                h = abs(currentX - 1 - finalX) + abs(currentY - finalY)
                searchQueue.append((h, [currentX - 1, currentY]))
                children[(currentX-1, currentY)] = (currentX, currentY)

        if currentY > 0:
            if mapM.surface[currentX][currentY - 1] == 0 and (currentX, currentY-1) not in visited:
                h = abs(currentX - finalX) + abs(currentY - 1 - finalY)
                searchQueue.append((h, [currentX, currentY-1]))
                children[(currentX, currentY-1)] = (currentX, currentY)

        if currentX < 19:
            if mapM.surface[currentX + 1][currentY] == 0 and (currentX+1, currentY) not in visited:
                h = abs(currentX + 1 - finalX) + abs(currentY - finalY)
                searchQueue.append((h, [currentX + 1, currentY]))
                children[(currentX+1, currentY)] = (currentX, currentY)

        if currentY < 19:
            if mapM.surface[currentX][currentY + 1] == 0 and (currentX, currentY+1) not in visited:
                h = abs(currentX - finalX) + abs(currentY + 1 - finalY)
                searchQueue.append((h, [currentX, currentY+1]))
                children[(currentX, currentY+1)] = (currentX, currentY)

        screen.blit(droneD.mapWithDrone(mapM.image()), (0, 0))
        pygame.display.flip()

def dummysearch():
    #example of some path in test1.map from [5,7] to [7,11]
    return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]
    
def displayWithPath(image, path, visited):
    mark = pygame.Surface((20,20))
    mark.fill(GREEN)
    markv = pygame.Surface((20,20))
    markv.fill((255,255,0))
    for move in visited:
        image.blit(markv, (move[1] *20, move[0] * 20))
    for move in path:
        image.blit(mark, (move[1] *20, move[0] * 20))

    mark1 = pygame.Surface((20,20))
    mark1.fill((255,182,193))
    mark2 = pygame.Surface((20,20))
    mark2.fill((221,160,221))
    image.blit(mark1, (path[0][1]*20, path[0][0]*20))
    image.blit(mark2, (path[-1][1]*20, path[-1][0]*20))

    return image


# define a main function
def main():

    # we create the map
    m = Map()
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")


    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    while True:
        x = randint(0, 19)
        y = randint(0, 19)
        if m.surface[x, y] == 0:
            break

    #create drone
    d = Drone(x, y)



    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)


    # define a variable to control the main loop
    running = True

    screen.blit(d.mapWithDrone(m.image()), (0, 0))
    pygame.display.flip()

    while True:
        finalX = randint(0, 19)
        finalY = randint(0, 19)
        if m.surface[finalX, finalY] == 0:
            break

    initialX = d.x
    initialY = d.y

    print(initialX, initialY)
    print(finalX, finalY)
    startAStar = time.time()
    path, visited = searchAStar(m, d, initialX, initialY, finalX, finalY)
    print("AStar execution time: " + str((time.time() - startAStar)))
    print(*path)
    print("AStar length: " + str(len(path)))

    screen.blit(displayWithPath(m.image(), path, visited),(0,0))
    pygame.display.flip()
    time.sleep(10)

    startGreedy = time.time()
    path, visited = searchGreedy(m, d, initialX, initialY, finalX, finalY)
    print("Greedy execution time: " + str((time.time() - startGreedy)))
    print(*path)
    print("Greedy length: " + str(len(path)))

    screen.blit(displayWithPath(m.image(), path, visited),(0,0))
    pygame.display.flip()
    time.sleep(10)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()