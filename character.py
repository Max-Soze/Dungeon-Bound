import pygame

class Character:
    
    def __init__(self, hp, mp):
        self.health = hp
        self.mana = mp
        self.attacks = {'standard':7}
        self.inventory = []
        self.xPos = 0
        self.yPos = 0
        self.image_front = pygame.image.load("src/art/player_front.png")
        self.image_back = pygame.image.load("src/art/player_back.png")
        self.image_right = pygame.image.load("src/art/player_right.png")
        self.image_left = pygame.image.load("src/art/player_left.png")
        self.image = self.image_front
        self.rect = self.image.get_rect()

    def move(self, direction):
        if direction == "right":
            self.xPos += 1
            self.image = self.image_right
        elif direction == "left":
            self.xPos -= 1
            self.image = self.image_left
        elif direction == "up":
            self.yPos -= 1
            self.image = self.image_back
        elif direction == "down":
            self.yPos += 1
            self.image = self.image_front

    def attack(self, choice):
        return self.attacks[choice]