import pygame, numpy, json, sys, ctypes
from pygame.locals import *


# Window and framerates
FPS = 30
WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

DATA = []

def main():
    global FPSCLOCK, DISPLAYSURF, ALPHAFONT

    ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    pygame.mixer.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Dungeon Bound")
    ALPHAFONT = pygame.font.Font("freesansbold.ttf", 18)

    try:
        loadDat()
    except:
        with open("savegame.json", "w") as init:
            json.dump(DATA, init)
    #showStart
    while(True):
        runGame()

def runGame():
    # set up game
    left = False
    right = False
    up = False
    down = False

    while(True):
        #event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()


def combat():
    None


def terminate():
    saveDat()
    pygame.quit()
    sys.exit()

def saveDat():
    global DATA
    with open("savegame.json", "w") as save:
        json.dump(DATA, save)

def loadDat():
    global DATA
    with open("savegame.json", "r") as load:
        DATA = json.load(load)

if __name__ == "__main__":
    main()