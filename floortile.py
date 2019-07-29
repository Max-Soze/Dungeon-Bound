import pygame

class FloorTile:

    def __init__(self, type):
        self.type = type
        if self.type == "st_floor":
            self.image = pygame.image.load("src/art/st_floor.png")
        self.rect = self.image.get_rect()