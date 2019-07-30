import pygame

class Button:
    def __init__(self, image, pos):
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos