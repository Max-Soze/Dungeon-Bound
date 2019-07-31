# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 14:21:22 2019

@author: Stanford
"""
import pygame, sys 
from pygame.locals import *  

WINDOWWIDTH = 1900
WINDOWHEIGHT = 600  

# set up the window 
pygame.init()
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
healthFont = pygame.font.Font('freesansbold.ttf', 18) 
manaFont = pygame.font.Font('freesansbold.ttf', 18) 
damageFont = pygame.font.Font('freesansbold.ttf', 28) 
# Colors
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
 
def test():
        #setnup window
    health = 350
    healthDamage = 0 
    damage = 0 
    enemyHealth = 50
    # event handler game loop
    while(True):  
        
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                pygame.quit() 
                sys.exit()  
               
        #draw HUD Window            
        DISPLAYSURF.fill(BLACK)  
        pygame.draw.rect(DISPLAYSURF, RED, (1, 1, 1900, 112))
        pygame.draw.rect(DISPLAYSURF, GRAY, (1, 1, 1900, 110)) 
        pygame.draw.aaline(DISPLAYSURF, DARKGRAY, (470, 1), (470, 110), 10)  
        pygame.draw.aaline(DISPLAYSURF, RED, (1, 106), (1900, 106), 200)  
        #draw info
        healthBar(healthDamage, health, damage)
        manaBar() 
        damageInfo(damage, enemyHealth)
        pygame.display.update()

def drawHUDWin(DISPLAYSURF): 
        pygame.draw.rect(DISPLAYSURF, RED, (1, 1, 1900, 112))
        pygame.draw.rect(DISPLAYSURF, GRAY, (1, 1, 1900, 110)) 
        pygame.draw.aaline(DISPLAYSURF, DARKGRAY, (470, 1), (470, 110), 10)  
        pygame.draw.aaline(DISPLAYSURF, RED, (1, 106), (1900, 106), 200)

def damageInfo(DISPLAYSURF, damage, enemyHealth, lastDamage):
    damageText = damageFont.render('You have taken '+str(lastDamage)+' damage.', True, BLACK, GRAY) 
    damageTextRect = damageText.get_rect()
    damageTextRect.center = (900, 30) 
    enemyText = damageFont.render('Evil Knight has '+str(enemyHealth)+' health remaining.', True, BLACK, GRAY)
    enemyTextRect = enemyText.get_rect() 
    enemyTextRect.center = (900, 80)
    DISPLAYSURF.blit(damageText, damageTextRect)  
    DISPLAYSURF.blit(enemyText, enemyTextRect)
                
def healthBar(DISPLAYSURF, health, playerHealth): 
    pygame.draw.rect(DISPLAYSURF, LIGHTRED, (20, 20, (health), 20))
    pygame.draw.rect(DISPLAYSURF, RED, (20, 20, (health), 20))  

#health text 
    healthText = healthFont.render(str(playerHealth)+'/50', True, SHADOW, GRAY)  
    healthTextRect = healthText.get_rect()
    healthTextRect.center = (420, 30) 
    DISPLAYSURF.blit(healthText, healthTextRect)

def manaBar(DISPLAYSURF):
    pygame.draw.rect(DISPLAYSURF, BLACK, (20, 60, 350, 20))
    pygame.draw.rect(DISPLAYSURF, BLUE, (20, 60, 350, 20)) 

#mana Text 
    manaText =  manaFont.render('20/20', True, SHADOW, GRAY)  
    manaTextRect = manaText.get_rect()
    manaTextRect.center = (420, 70)
    DISPLAYSURF.blit(manaText, manaTextRect)            
