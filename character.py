import pygame

class Character:
    
    def __init__(self, name, hp, mp):
        self.name = name
        self.health = hp
        self.mana = mp
        self.abilities = []
        self.inventory = []
