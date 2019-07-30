import pygame

class Enemy:
    
    def __init__(self, name, hp, attacks):
        self.name = name
        self.health = hp
        self.attacks = attacks