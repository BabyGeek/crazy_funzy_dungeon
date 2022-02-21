"""
This is a test of using the pytmx library with Tiled.
"""
import pygame
import pytmx


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm
        self.map_surface = self.make_map()

    def render(self, surface):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight

        if self.tmx_data.background_color:
            surface.fill(self.tmx_data.background_color)

        for layer in self.tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if image:
                        surface.blit(image.convert_alpha(), (x * tw, y * th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for object in layer:
                    surface.blit(object.image.convert_alpha(), (object.x, object.y))

            elif isinstance(layer, pytmx.TiledImageLayer):
                if image:
                    surface.blit(image.convert_alpha(), (0, 0))

    def make_map(self):
        temp_surface = pygame.Surface(self.size)
        self.render(temp_surface)
        return temp_surface
    
    def get_layer(self, layer_name):
        return self.tmx_data.get_layer_by_name(layer_name)