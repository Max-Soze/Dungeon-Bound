import pygame, numpy, json, sys, ctypes
from pygame.locals import *

from roommap import RoomMap
from character import Character

# Window and framerates
FPS = 30
WINDOWWIDTH = 1600
WINDOWHEIGHT = 900
CELLSIZE = 50

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Other
DATA = {}

def main():
    global FPSCLOCK, DISPLAYSURF, ALPHAFONT

    ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    pygame.mixer.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Dungeon Bound")
    ALPHAFONT = pygame.font.Font("freesansbold.ttf", 18)

    try:
        loadDat()
    except:
        with open("src/savegame.json", "w") as init:
            json.dump(DATA, init)
    #showStart
    while(True):
        runGame()
        #gameOver

def runGame():
    # set up game
    left = False
    right = False
    up = False
    down = False

    #testing
    test = RoomMap("floor")
    player = Character("boi", 50, 50)

    while(True):
        #event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        # drawing
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(pygame.image.load("src/art/st_floor.png"), (200, 200, 50, 50))
        drawRoom(test.map)
        drawChar(player)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawChar(char):
    x = char.xPos * CELLSIZE + 100
    y = char.yPos * CELLSIZE + 150
    char.rect.topleft = (x, y)
    DISPLAYSURF.blit(char.image, char.rect)

def drawRoom(room):
    for x in range(len(room)):
        for y in range(len(room[x])):
            DISPLAYSURF.blit(room[x][y].image, room[x][y].rect)


def terminate():
    saveDat()
    pygame.quit()
    sys.exit()

def saveDat():
    global DATA
    with open("src/savegame.json", "w") as save:
        json.dump(DATA, save)

def loadDat():
    global DATA
    with open("src/savegame.json", "r") as load:
        DATA = json.load(load)

if __name__ == "__main__":
    main()