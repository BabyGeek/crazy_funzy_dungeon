import pygame, os
from level_constants import *
from spritesheet import *
from constants import *
                
class Border(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.borders
        self._layer = BORDER_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Decoration(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, layer = DECORATION_TOP_LAYER, stable_layer = False):
        self.groups = game.all_sprites, game.decorations
        self._layer = layer
        self.stable_layer = stable_layer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.walls
        self._layer = WALL_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = image
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, open_actions, animated_image, type):
        self._layer = DOOR_LAYER
        self.groups = game.all_sprites, game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.rect = pygame.Rect(x ,y, w, h)
        self.current_index = 0
        self.animated_image = animated_image
        self._layer = self.rect.bottom
        
        self.load_animations()
        
        self.open_actions = open_actions
        self.last_updated = 0
        
        self.is_open = False
        self.is_activated = False
        self.animating = False
        
        self.type = type
        
    def load_animations(self):
        self.animations = []
        filename = os.path.join(os.getcwd(), IMAGES_FOLDER, 'maps', 'animations', self.animated_image)
        spritesheet = Spritesheet(filename, self.rect.width, self.rect.height)
        
        for i in range(spritesheet.data['columns']):
            self.animations.append(spritesheet.parse_sprite(i)) 
            
        self.image = self.animations[self.current_index]
        
    def open_animation(self):
        if self.is_open:
            return
        
        if not self.is_activated or not self.animations:
            return
        
        self.animating = True
        
        
                
    def update(self):
        if self.animating:
            now = pygame.time.get_ticks()
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_index = (self.current_index + 1) % len(self.animations)
                
                if self.current_index == len(self.animations) - 1:
                    self.current_index = -1
                    self.is_open = True
                    self.animating = False
                
            self.image = self.animations[self.current_index]
            
        if not self.is_open:
            self.image = self.animations[self.current_index]
            
        if self.is_open:
            self.image = self.animations[-1]
                
    def check_doors_state(self, player):
        if 'any' in self.open_actions:
            self.is_activated = True
        
        for action in player.actions:
            if action in self.open_actions:
                self.is_activated = True
        
        
class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name):
        self.groups = game.all_sprites, game.NPCs
        self._layer = NPC_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        
        self.current_index = 0
        self.animated_image = name + '_idle_anim_32x32.png'
        
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        self.load_animations()
        
        self.last_updated = 0
        self.animating = True
        self.is_speaking = False
        
    def load_animations(self):
        self.animations = []
        filename = os.path.join(os.getcwd(), IMAGES_FOLDER, 'NPC', self.animated_image)
        spritesheet = Spritesheet(filename, self.rect.width, self.rect.height)
        
        for i in range(spritesheet.data['columns']):
            self.animations.append(spritesheet.parse_sprite(i)) 
            
        self.image = self.animations[self.current_index]
        
    def update(self):
        if self.animating:
            
            now = pygame.time.get_ticks()
        
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_index = (self.current_index + 1) % len(self.animations)
                self.current_image = self.animations[self.current_index]
                    
            self.image = self.current_image.convert_alpha()
        
        