import pygame, numpy, json, sys, ctypes
from pygame.locals import *

from roommap import RoomMap
from character import Character
from enemy import Enemy
from button import Button

# Window and framerates
FPS = 30
WINDOWWIDTH = 1600
WINDOWHEIGHT = 900
CELLSIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Other
DATA = {"playerX":0, "playerY":0}

def main():
    global FPSCLOCK, DISPLAYSURF

    ctypes.windll.user32.SetProcessDPIAware()
    pygame.init()
    pygame.mixer.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption("Dungeon Bound")

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
    global DATA
    
    # set up game
    direction = None
    saving = False
    posDat = {}
    upds = ()

    #set up character
    player = Character(50, 50)
    player.xPos = DATA['playerX']
    player.yPos = DATA['playerY']

    #testing
    test = RoomMap("floor")
    testFoe = Enemy("Skelleboi", 20, {'standard':5, })

    while(True):
        #event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(upds)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate(upds)
                elif event.key == K_d:
                    direction = "right"
                elif event.key == K_a:
                    direction = "left"
                elif event.key == K_w:
                    direction = "up"
                elif event.key == K_s:
                    direction = "down"
                elif event.key == K_p:
                    saving = True
        
        #movement controller
        if player.xPos == 0 and direction == 'left':
            direction = None
            combat(player, testFoe)
        if player.xPos == 9 and direction == 'right':
            direction = None
        if player.yPos == 0 and direction == 'up':
            direction = None
        if player.yPos == 9 and direction == 'down':
            direction = None
        player.move(direction)
        direction = None

        # drawing
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(pygame.image.load("src/art/st_floor.png"), (200, 200, 50, 50))
        drawRoom(test.map)
        drawChar(player)
        pygame.display.update()
        
        #saves
        if saving == True:
            saving = False
            posDat.update({'playerX':player.xPos, 'playerY':player.yPos})
            upds = (posDat,)
        
        FPSCLOCK.tick(FPS)


def combat(player, enemy):
    mouseX = 0
    mouseY = 0
    clicked = False
    attackButton = Button("src/art/attack_button.png", (550, 600))
    playerDamage = 0
    enemyDamage = 0
    
    while(True):
        #event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(())
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                clicked = True

        #event controller
        if attackButton.rect.collidepoint((mouseX, mouseY)) and clicked:
            clicked = False
            playerDamage = player.attack('standard')
            enemyDamage = enemy.attacks[numpy.random.choice(('standard',))]

        #wombat controller
        enemy.health -= playerDamage
        player.health -= enemyDamage
        playerDamage = 0
        enemyDamage = 0
        if enemy.health <= 0:
            fightWon()
            return
                
        #drawing
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(attackButton.image, attackButton.rect)
        drawCombatHUD(player.health, player.mana)
        drawEnemyHUD(enemy.name, enemy.health)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def fightWon():
    None

def drawCombatHUD(health, mana):
    fontHUD = pygame.font.Font("freesansbold.ttf", 36)
    nameSurf = fontHUD.render("Hero", True, WHITE)
    nameRect = nameSurf.get_rect()
    healthSurf = fontHUD.render("Health: "+str(health), True, WHITE)
    healthRect = healthSurf.get_rect()
    manaSurf = fontHUD.render("Mana: "+str(mana), True, WHITE)
    manaRect = manaSurf.get_rect()
    nameRect.topleft = (50, 50)
    healthRect.topleft = (50, nameRect.bottom + 15)
    manaRect.topleft = healthRect.bottomleft
    DISPLAYSURF.blit(nameSurf, nameRect)
    DISPLAYSURF.blit(healthSurf, healthRect)
    DISPLAYSURF.blit(manaSurf, manaRect)

def drawEnemyHUD(name, health):
    fontHUD = pygame.font.Font("freesansbold.ttf", 36)
    nameSurf = fontHUD.render(name, True, WHITE)
    nameRect = nameSurf.get_rect()
    healthSurf = fontHUD.render("Health: "+str(health), True, WHITE)
    healthRect = healthSurf.get_rect()
    nameRect.topright = (WINDOWWIDTH - 50, 50)
    healthRect.topright = (WINDOWWIDTH - 50, nameRect.bottom + 15)
    DISPLAYSURF.blit(nameSurf, nameRect)
    DISPLAYSURF.blit(healthSurf, healthRect)


def drawChar(char):
    x = char.xPos * CELLSIZE + 100
    y = char.yPos * CELLSIZE + 150
    char.rect.topleft = (x, y)
    DISPLAYSURF.blit(char.image, char.rect)

def drawRoom(room):
    for x in range(len(room)):
        for y in range(len(room[x])):
            DISPLAYSURF.blit(room[x][y].image, room[x][y].rect)


def terminate(upds):
    saveDat(upds)
    pygame.quit()
    sys.exit()

def saveDat(upds):
    global DATA
    for save in upds:
        DATA.update(save)
    with open("src/savegame.json", "w") as save:
        json.dump(DATA, save)

def loadDat():
    global DATA
    with open("src/savegame.json", "r") as load:
        DATA = json.load(load)

if __name__ == "__main__":
    main()