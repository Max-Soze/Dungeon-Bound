import pygame

class Character:
    
    def __init__(self, name, hp, mp):
        self.name = name
        self.health = hp
        self.mana = mp
        self.abilities = []
        self.inventory = []
        self.xPos = 5
        self.yPos = 5
        self.image_front = pygame.image.load("src/art/evil_knight.png")
        self.image = self.image_front
        self.rect = self.image_front.get_rect()
