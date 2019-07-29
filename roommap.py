import pygame

from floortile import FloorTile

class RoomMap:

    def __init__(self, type):
        self.map = []
        if type == "floor":
            for x in range(10):
                self.map.append([])
                for y in range(10):
                    self.map[x].append(FloorTile("st_floor"))
                    if y == 0 and x == 0:
                        self.map[x][y].rect.topleft = (100,150)
                    elif y == 0 and x != 0:
                        self.map[x][y].rect.topleft = self.map[x-1][y].rect.topright
                    else:
                        self.map[x][y].rect.topleft = self.map[x][y-1].rect.bottomleft
