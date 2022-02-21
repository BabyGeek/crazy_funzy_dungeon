
"""
This is a test of using the pytmx library with Tiled.
"""
import pygame
import pytmx
from game_objects import *


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """
    def __init__(self, game, filename):
        self.game = game
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.object_images = []
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.map_surface = self.make_map()
        self.current_frame = 0

    def render(self, surface):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        
        if self.tmx_data.background_color:
            surface.fill(self.tmx_data.background_color)
        else:
            surface.fill((0, 0, 0))

        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if image:
                        if layer.name == 'walls' or 'wall' in layer.name:
                            Wall(self.game, x * tw, y * th, image.convert_alpha())
                        elif 'decoration' in layer.name:
                            if 'top' in layer.name:
                                Decoration(self.game, x * tw, y * th, image.convert_alpha(), stable_layer=True)
                            else:
                                Decoration(self.game, x * tw, y * th, image.convert_alpha())
                        elif layer.name == 'borders' or 'border' in layer.name:
                            Border(self.game, x * tw, y * th, image.convert_alpha())
                            
                        else:
                            surface.blit(image.convert_alpha() , (x * tw, y * th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                pass

            elif isinstance(layer, pytmx.TiledImageLayer):
                if image:
                    surface.blit(image , (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface
    
    def get_layer(self, layer_name):
        return self.tmx_data.get_layer_by_name(layer_name)