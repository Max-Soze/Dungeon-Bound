import pygame

class Enemy:
    
    def __init__(self, name, hp, pos, image, attacks):
        self.name = name
        self.health = hp
        self.attacks = attacks
        self.xPos, self.yPos = pos
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.defeated = False