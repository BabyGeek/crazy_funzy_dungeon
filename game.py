from constants import *
from player_constants import *
from level_constants import *
import pygame, sys, os
from player import Player
from cameras import Camera, Border, Follow
from renderer import Renderer
from levels import Level, NPC, Wall, Obstacle, Door

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
        self.clock = pygame.time.Clock()
        self.load_data()

      
    def load_data(self):
        pass
     
    def new(self, level = 0):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.NPCs = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.decorations = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.borders = pygame.sprite.Group()

        ## LOAD LEVEL
        self.level = Level(self, level)
        self.room = self.level.current_room
        self.get_sprite_groups()
        
        ## LOAD CAMERA
        self.camera = Camera(self.player)
        border = Border(self.camera, self.player, self.level.current_room.rect)
        
        self.camera.setmethod(border)
        
    
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.handle_inputs()
            self.update()
            self.draw()
        
    def quit():
        pygame.quit()
        sys.exit(-1) 
        
    def update(self):
        
        for door in self.doors:
            door.check_doors_state(self.player)
            
        if self.room.is_cleaned:
            self.player.add_action('cleaned')
        
        self.all_sprites.update()
        self.level.update()
        self.camera.scroll()
    
    def draw(self):
        
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.window.fill((0, 0, 0))
        
        ## DISPLAY MAP AND PLAYER
        self.level.draw_room(self.window, self.camera)
        
        for sprite in self.all_sprites:
            self.window.blit(sprite.image, (sprite.rect.x - self.camera.offset.x, sprite.rect.y - self.camera.offset.y))
        
        for decoration in self.decorations:
            if decoration.rect.bottom > self.player.rect.top and not decoration.stable_layer:
                self.all_sprites.change_layer(decoration, DECORATION_DOWN_LAYER)
            else:
                if decoration._layer == DECORATION_DOWN_LAYER:
                    self.all_sprites.change_layer(decoration, DECORATION_TOP_LAYER)
                
        #self.window.blit(self.player.image, (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y))
        
        ## PLAYER HITBOXES FOR COLLISIONS 
        #rect_feet_hitbox = pygame.draw.rect(self.window, (0, 255, 0), (self.player.feet_hitbox.x - self.camera.offset.x, self.player.feet_hitbox.y - self.camera.offset.y, self.player.feet_hitbox.width, self.player.feet_hitbox.height), 3)
        #rect_hitbox = pygame.draw.rect(self.window, (255, 0, 0), (self.player.rect.x - self.camera.offset.x, self.player.rect.y - self.camera.offset.y, self.player.rect.width, self.player.rect.height), 3)
        
        ## REFRESH SCREEN
        pygame.display.flip()

    def handle_inputs(self):
        """Handle user inputs
        """
        ## QUITTING HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            ## PLAYER KEYS
            if event.type == pygame.KEYDOWN:
                self.player.is_moving = True
                if event.key == pygame.K_SPACE:
                    self.player.is_dashing = True
                        
            if event.type == pygame.KEYUP:
                self.player.is_dashing = False
        
    def get_sprite_groups(self):
        for tile_object in self.room.tmx_data.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            
            if tile_object.name == 'npc':
                NPC(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.object_name)
        
            if tile_object.name == 'obstacle':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                
            if tile_object.name == 'door':
                Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, self.room.get_opening_actions(), tile_object.animated_image, tile_object)

    def show_start_screen(self):
        pass
    
    def show_game_over_screen(self):
        pass