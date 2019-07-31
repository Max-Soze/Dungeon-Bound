#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 09:44:23 2019

@author: lucasvoss
"""

import pygame, sys
from pygame.locals import *
WINDOWWIDTH = 1600
WINDOWHEIGHT = 900
#Define Colors
#Name         (  R,   G,   B)
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
DARKGREEN   = (  0, 155,   0)
DARKGRAY    = ( 40,  40,  40)
BGCOLOR = BLACK

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
DISPLAYSURF.fill(BGCOLOR)
pygame.display.set_caption("gut Game")


def showStartScreen():
    startFont = pygame.font.Font('freesansbold.ttf', 100)
    startSurf = startFont.render("Dungeon Bound", True, WHITE, RED)
    startRect = startSurf.get_rect()
    startRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    DISPLAYSURF.blit(startSurf, startRect)
    

    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()


showStartScreen()
    
    
    
    