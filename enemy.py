import pygame, numpy

class Enemy:
    
    def __init__(self, name, hp, pos, image, bigImage, attacks):
        self.name = name
        self.health = hp
        self.attacks = attacks
        self.xPos, self.yPos = pos
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.bigImage = pygame.image.load(bigImage)
        self.bigRect = self.bigImage.get_rect()
        self.defeated = False

    def attack(self, choice):
        standardDMG = numpy.random.randint(4,8)
        self.attacks.update({'standard':standardDMG})
        return self.attacks[choice]