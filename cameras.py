import pygame
vec = pygame.math.Vector2
from abc import ABC, abstractmethod
from constants import *

class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.CONST = vec(-DISPLAY_W / 2 + player.rect.w / 2, -DISPLAY_H / 2 + player.rect.h / 2)

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()

class CamScroll(ABC):
    def __init__(self, camera,player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)

class Border(CamScroll):
    def __init__(self, camera, player, map_rect):
        CamScroll.__init__(self, camera, player)
        self.border_left, self.border_right = 0, map_rect.width
        self.border_top, self.border_bottom = 0, map_rect.height - 20

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.border_left, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.border_right - DISPLAY_W)
        self.camera.offset.y = max(self.border_top, self.camera.offset.y)
        self.camera.offset.y = min(self.camera.offset.y, self.border_bottom - DISPLAY_H)
        

class Auto(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)

    def scroll(self):
        self.camera.offset.x += 1










