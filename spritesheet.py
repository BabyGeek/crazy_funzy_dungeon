import pygame
import json


class Spritesheet:
    def __init__(self, filename, tile_width, tile_height, crop = False):
        self.crop = crop
        self.filename = filename
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()


    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h)).convert_alpha()
        sprite.set_colorkey((0,0,0))
        
        if self.crop:
            offset = h - self.sprite_sheet.get_height()
            y -= offset
            
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, sprite_id):
        sprite_x = sprite_id % self.data['columns'] * self.tile_width
        sprite_y = (sprite_id // self.data['columns']) * self.tile_height

        x, y, w, h = sprite_x, sprite_y, self.tile_width, self.tile_height
        image = self.get_sprite(x, y, w, h)
        return image