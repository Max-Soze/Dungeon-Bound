import pygame, numpy, json, sys, ctypes, os
import HUD as comDisp
from pygame.locals import *

from roommap import RoomMap
from character import Character
from enemy import Enemy
from button import Button
from floortile import FloorTile

# Window and framerates
FPS = 30
WINDOWWIDTH = 1600
WINDOWHEIGHT = 900
CELLSIZE = 50

# Colors
DARKGREEN   = (  0, 155,   0)
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (171,  39,  25)
BLUE        = (  9, 109, 150)
GRAY        = (150, 150, 150)
DARKGRAY    = ( 40,  40,  40) 
SHADOW      = (192, 192, 192)
LIGHTGREEN  = (  0, 255,   0)
GREEN       = (  0, 200,   0)
LIGHTBLUE   = (  0,   0, 255)
LIGHTRED    = (255, 100, 100)
PURPLE      = (102,   0, 102)
LIGHTPURPLE = (153,   0, 153)

#Other
DATA = {"playerX":0, "playerY":0, 'skelDead':False, 'knightDead':False, 'playerHP':50}

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
    showStartScreen()
    while(True):
        runGame()
        #gameOver

def runGame():
    global DATA
    
    # set up game
    direction = None
    saving = False
    posDat = {}
    deadFoeDat = {}
    hpDat = {}
    upds = ()

    #set up character
    player = Character(50, 50)
    player.xPos = DATA['playerX']
    player.yPos = DATA['playerY']   
    player.health = DATA['playerHP']

    #testing
    test = RoomMap("floor")
    skeleton = Enemy("Evil Knight", numpy.random.randint(15, 30), (4, 6), "src/art/evil_knight.png", "src/art/evil_knight_large.png", {'standard':numpy.random.randint(4,8), })
    knight = Enemy("Evil Knight", numpy.random.randint(15, 30), (7, 3), "src/art/evil_knight.png", "src/art/evil_knight_large.png", {'standard':numpy.random.randint(4,8), })

    #load game state
    skeleton.defeated = DATA['skelDead']
    knight.defeated = DATA['knightDead']
    

    while(True):
        #event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
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
        if player.xPos == 9 and direction == 'right':
            direction = None
        if player.yPos == 0 and direction == 'up':
            direction = None
        if player.yPos == 9 and direction == 'down':
            direction = None
        player.move(direction)
        direction = None

        if player.xPos == skeleton.xPos and player.yPos == skeleton.yPos and not skeleton.defeated:
            combat(player, skeleton)
        if player.xPos == knight.xPos and player.yPos == knight.yPos and not knight.defeated:
            combat(player, knight)

        #event controller
        if player.health <= 0:
            showGameOver()

        # drawing
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(pygame.image.load("src/art/st_floor.png"), (200, 200, 50, 50))
        drawRoom(test.map)
        if not skeleton.defeated:
            drawChar(skeleton)
        if not knight.defeated:
            drawChar(knight)
        drawChar(player)
        pygame.display.update()
        
        #saves
        if saving == True:
            saving = False
            posDat.update({'playerX':player.xPos, 'playerY':player.yPos})
            deadFoeDat.update({'skelDead':skeleton.defeated, 'knightDead':knight.defeated})
            hpDat.update({'playerHP':player.health})
            upds = (posDat, deadFoeDat, hpDat)
            saveDat(upds)
        
        FPSCLOCK.tick(FPS)


def combat(player, enemy):
    mouseX = 0
    mouseY = 0
    clicked = False
    attackButton = Button("src/art/attack_button.png", (WINDOWWIDTH/2, 600))
    playerDamage = 0
    enemyDamage = 0
    lastDamage = 0
    
    while(True):
        #event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                clicked = True

        #event controller
        if attackButton.rect.collidepoint((mouseX, mouseY)) and clicked:
            clicked = False
            playerDamage = player.attack('standard')
            enemyDamage = enemy.attack(numpy.random.choice(('standard',)))
            lastDamage = enemyDamage

        #wombat controller
        enemy.health -= playerDamage
        player.health -= enemyDamage
        if enemy.health <= 0:
            fightWon(enemy)
            return
        if player.health <= 0:
            showGameOver()
                
        #drawing
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(pygame.image.load("src/art/combat_floor.png"), (0, 0, 1600, 900))
        drawFight(player, enemy)
        DISPLAYSURF.blit(attackButton.image, attackButton.rect)
        #drawCombatHUD(player.health, player.mana)
        #drawEnemyHUD(enemy.name, enemy.health)
        comDisp.drawHUDWin(DISPLAYSURF)
        comDisp.healthBar(DISPLAYSURF, player.health * 7, player.health)
        comDisp.manaBar(DISPLAYSURF)
        comDisp.damageInfo(DISPLAYSURF, enemyDamage, enemy.health, lastDamage)
        pygame.display.update()

        #Reset variables
        playerDamage = 0
        enemyDamage = 0

        FPSCLOCK.tick(FPS)

def fightWon(enemy):
    enemy.defeated = True

def drawFight(player, enemy):
    enemy.bigRect.bottomright = (WINDOWWIDTH - 230, 850)
    DISPLAYSURF.blit(enemy.bigImage, enemy.bigRect)
    player.rect_big.bottomleft = (230, 850)
    DISPLAYSURF.blit(player.image_big, player.rect_big)

def showStartScreen():
    
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()        
        startFont = pygame.font.Font('freesansbold.ttf', 100)
        startSurf = startFont.render("Dungeon Bound", True, WHITE, RED)
        startRect = startSurf.get_rect()
        startRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
        DISPLAYSURF.blit(startSurf, startRect)
        pygame.display.update()
        if checkForKeyPress():
            pygame.event.get()
            return
        FPSCLOCK.tick(FPS)

def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            else:
                return True
    return False

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

def showGameOver():
    endFont = pygame.font.Font("freesansbold.ttf", 200)
    endSurf = endFont.render("Game Over", True, RED)
    endRect = endSurf.get_rect()
    endRect.center = (WINDOWWIDTH/2, 300)
    endPic = pygame.transform.scale(pygame.image.load("src/art/player_dead.png"), (400, 400))
    endPicRect = endPic.get_rect()
    endPicRect.center = (WINDOWWIDTH/2, 600)
    while(True):
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(endPic, endPicRect)
        DISPLAYSURF.blit(endSurf, endRect)
        if checkForKeyPress():
            os.remove("src/savegame.json")
            terminate()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        

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


def terminate():
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