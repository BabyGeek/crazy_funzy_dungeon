from level_constants import PLAYER_LAYER
from constants import *
from level_constants import *
from player_constants import *
from game_objects import Wall
import pygame, os
from spritesheet import Spritesheet
from helpers import *
vec = pygame.math.Vector2



class Player(pygame.sprite.Sprite):
    def __init__ (self, game, x, y, name = "Bob"):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.facing = 'down'
        
        self.is_moving = False
        self.is_dashing = False
        self.is_activating = False
        
        self.name = name
        self.options = PLAYERS_SPRITES_OPTIONS[self.name]
        self.images = {}
        
        self.state = self.options['idle_state']
        self.load_sprites()
        
        self.current_frame = self.get_start_frame()
        self.last_updated = 0
        
        self.current_image = self.images[self.state][self.current_frame]
        self.image = self.current_image.convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.left, self.rect.top = x, y
        self.feet_hitbox = self.rect.inflate(0, -30)
        
        self.speed = self.options['speed']
        
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        
        self.actions = []
        
    def load_sprites(self):
        for state in self.options['states']:
            self.images[state] = []
            filename = self.name + IMAGE_NAME_SEPARATOR + state + PLAYER_SPRITE_IMAGE_SUFFIX
            filename = os.path.join(CHARACTER_IMAGES_PATH.format(self.name), filename)
            action_spritesheet = Spritesheet(filename, PLAYER_SPRITE_W, PLAYER_SPRITE_H, crop = True)
            
            for i in range(action_spritesheet.data['columns']):
                self.images[state].append(action_spritesheet.parse_sprite(i)) 
    
    def get_keys(self):
        self.vel = vec(0, 0)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_e]:
            self.is_activating = True
        
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.facing = 'left'
            self.vel.x = -self.speed
            
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.facing = 'right'
            self.vel.x = self.speed
            
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.facing = 'up'
            self.vel.y = -self.speed
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.facing = 'down'
            self.vel.y = self.speed
            
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
            
        if self.vel == vec(0, 0):
            self.is_moving = False
            
            
                 
    def collide_with_walls(self, direction):
                
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
                
            if hits:
                if self.vel.x > 0:
                    if self.feet_hitbox.top < hits[0].rect.bottom:
                        self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    if self.feet_hitbox.top < hits[0].rect.bottom:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.obstacles, False)
                
            if hits:
                if self.vel.y > 0:
                    if self.feet_hitbox.bottom < hits[0].rect.bottom:
                        self.pos.y = hits[0].rect.top - self.rect.height
                    
                if self.vel.y < 0:
                    if self.feet_hitbox.top <= hits[0].rect.bottom:
                        offset = self.rect.height - self.feet_hitbox.height
                        self.pos.y = hits[0].rect.bottom - offset
                        print(offset, self.pos.y, hits[0].rect.bottom)
                    
                self.vel.y = 0
                self.rect.y = self.pos.y
                
                

    
    def collide_with_doors(self, direction):
                
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.doors, False)
            if hits:
                if hits[0].is_open:
                    return
                
                if self.vel.x > 0:
                    if self.feet_hitbox.top < hits[0].rect.bottom:
                        self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    if self.feet_hitbox.top < hits[0].rect.bottom:
                        self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.doors, False)
                
            if hits:
                if hits[0].is_open:
                    return
                
                if self.vel.y > 0:
                    if self.feet_hitbox.bottom < hits[0].rect.bottom:
                        self.pos.y = hits[0].rect.top - self.rect.height
                    
                if self.vel.y < 0:
                    if self.feet_hitbox.top <= hits[0].rect.bottom:
                        offset = self.rect.height - self.feet_hitbox.height
                        self.pos.y = hits[0].rect.bottom - offset
                    
                self.vel.y = 0
                self.rect.y = self.pos.y
            
    def update(self):
        self.get_keys()
        
        self.move()
        
        self.pos += self.vel * self.game.dt
        
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.collide_with_doors('x')
            
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
        self.collide_with_doors('y')
            
        self.check_door_collide()
        self.check_npc_activation()
            
        self.feet_hitbox.topleft = self.rect.topleft
        self.feet_hitbox.top = self.rect.top + (self.rect.height - self.feet_hitbox.height)
        
        self.set_state()
        self.animate()
        
    def animate(self):
        now = pygame.time.get_ticks()
        
        if now - self.last_updated > 150:
            self.last_updated = now
            if self.state == self.options['idle_state']:
                self.current_frame = self.current_frame
                self.current_image = self.images[self.state][self.get_start_frame()]
            else:
                images = self.images[self.state][self.get_start_frame():self.get_start_frame() + self.options['images_per_animations']]
                self.current_frame = (self.current_frame + 1) % len(images)
                self.current_image = images[self.current_frame]
                
            self.image = self.current_image.convert_alpha()

    def get_start_frame(self):
        number_of_frames = len(self.images[self.state]) // 4
            
        if self.facing == 'down':
            return 3 * number_of_frames
        elif self.facing == 'left':
            return 2 * number_of_frames
        elif self.facing == 'up':
            return number_of_frames
        elif self.facing == 'right':
            return 0
            
    def move(self):
        if not self.is_moving:
            return False

        if self.is_dashing:
            self.vel *= 2
    
    def set_state(self):
        self.state = self.options['idle_anim_state']
        
        if self.is_moving:
            self.state = self.options['run_state']
            
    def check_door_collide(self):
        if self.game.doors:
            doors = pygame.sprite.spritecollide(self, self.game.doors, False)
            if doors:
                if doors[0].is_activated and not doors[0].is_open:
                    self.vel = vec(0, 0)
                    doors[0].open_animation()
    
    def check_npc_activation(self):
        if self.game.doors:
            npcs = pygame.sprite.spritecollide(self, self.game.NPCs, False)
            if npcs:
                npc = npcs[0]
                if not npc.is_speaking:
                    pass
    
    def draw(self, display, camera = None):
        if not camera:
            display.blit(self.current_image, self.rect)
        else:
            display.blit(self.current_image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
            
    def add_action(self, action):
        self.actions.append(action)