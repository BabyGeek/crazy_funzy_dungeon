import random, pygame, pytmx, os
from helpers import *
from level_constants import *
from renderer import Renderer
from constants import *
from spritesheet import Spritesheet


class Level:
    def __init__(self, level_number = 0):
        
        self.level = LEVELS['level_' + str(level_number)]
        self.current_room_index = DEFAULT_INDEX_START
        
        self.current_room = None
        self.actions = []
        
        self.room_cleared = 0
        self.rooms = []
                
        self.load_rooms()
        
    @property
    def name(self):
        return self.level['name']
    
    def load_rooms(self):
        """Get all rooms images for this level
        """
        
        if self.level['folder'] == START_MAP_FOLDER:
            self.current_room_index = [0, 0]
            self.rooms.append(list())
            self.rooms[0].append(Room(os.path.join(os.getcwd(), 'resources', 'maps', self.level['folder'], 'map.tmx'), self.level))
        else:
            column = 0
            for row in self.level['rooms']:
                self.rooms.append(list())
                for room in row:
                    image = random.choice([name for name in os.listdir(os.path.join(os.getcwd(), 'resources', 'maps', self.level['folder'], LEVELS_IMAGES_FOLDER[column], room)) if '.tmx' in name])
                    self.rooms[column].append(Room(os.path.join(os.getcwd(), 'resources', 'maps', self.level['folder'],  LEVELS_IMAGES_FOLDER[column], room, image), self.level))
                column += 1
                
        self.update_current_room()
            
    def update(self):
        """update current room index, check ennemies killed, and other stuffs

        """
        self.update_current_room()
    
    def draw_room(self, display, camera = None):
        """Display current room on given display, if camera is set use the camera offset to display properly

        Args:
            display ([pygame.Surface]): [Display to blit image on]
        """
        if not camera:
            display.blit(self.current_room.surface, self.current_room.rect)
        else:
            display.blit(self.current_room.surface, (self.current_room.rect.x - camera.offset.x, self.current_room.rect.y - camera.offset.y))
        
    def update_current_room(self):
        if len(self.rooms):
            self.current_room = self.rooms[self.current_room_index[0]][self.current_room_index[1]]
    
    def change_room(self, facing):
        """Change the current room index after checking if player can, in the facing given

        Args:
            facing ([string]): [string to check with helpers -- "top", 'left", "right", "down"]
        """
        direction = get_direction_velocity_for_facing(facing)
        self.current_room_index[0] += direction[0] 
        self.current_room_index[1] += direction[1] 
        
    def change_level(self, level_number):
        self.level = LEVELS['level_' + str(level_number)]
        self.current_room_index = [1, 1]
        
        self.current_room = None
        
        self.room_cleared = 0
        self.rooms = []
        
        self.load_rooms()
        
        
        
class Room:
    def __init__(self, room_image, level_options):
        self.renderer = Renderer(room_image)
        self.surface = self.renderer.map_surface
        self.rect = self.surface.get_rect()
        self.level_options = level_options
        
        self.obstacles = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        
        self.load_obstacles()
        self.load_doors()
        
    def load_obstacles(self):
        obstacles = self.level_options['obstacle_layers']
        for obstacle in obstacles:
            try:
                items = self.renderer.get_layer(obstacle)
                for x, y, image in items.tiles():
                    self.obstacles.add(Obstacle(x, y, image, SPRITE_SIZE))
            except ValueError:
                return
            
    def load_doors(self):
        doors = self.renderer.get_layer(self.level_options['door_layer'])
        
        if isinstance(doors, pytmx.TiledTileLayer):
            for x, y, image in doors.tiles():
                if image:
                    self.doors.add(Door(x, y, image, SPRITE_SIZE, self.level_options['open_door_actions']))

        elif isinstance(doors, pytmx.TiledObjectGroup):
            for object in doors:
                self.doors.add(Door(object.x, object.y, object.image, SPRITE_SIZE, self.level_options['open_door_actions'], object))
                
    def update_doors(self):
        for door in self.doors:
            door.update(self.surface)
            
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, image, sprite_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x * sprite_size,y * sprite_size, sprite_size, sprite_size)
        self.image = image.convert_alpha()
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, image, sprite_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x * sprite_size,y * sprite_size, sprite_size, sprite_size)
        self.image = image.convert_alpha()
        
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y, image, sprite_size, open_actions, object = None):
        pygame.sprite.Sprite.__init__(self)
        self.object = object
        
        if self.object:
            self.rect = pygame.Rect(x ,y, self.object.width, self.object.height)
            self.load_animations()
        else:
            self.rect = pygame.Rect(x * sprite_size,y * sprite_size, sprite_size, sprite_size)
            
        self.image = image.convert_alpha()
        self.open_actions = open_actions
        self.last_updated = 0
        self.is_open = False
        self.is_activated = False
        
    def load_animations(self):
        self.animations = []
        filename = os.path.join(os.getcwd(), IMAGES_FOLDER, 'maps', 'animations', self.object.animated_image)
        spritesheet = Spritesheet(filename, self.object.width, self.object.height)
    
        for i in range(spritesheet.data['columns']):
            self.animations.append(spritesheet.parse_sprite(i)) 
            
    def open_animation(self):
        if not self.object and not self.is_activated:
            return
        
        for i in range(len(self.animations)):
            self.image = self.animations[i]
                
        self.is_open = True
                
    def update(self, surface):
        if self.is_open and self.object:
            self.image = self.animations[-1]
        elif not self.is_open and not self.is_activated:
            self.image = self.animations[0]
        
        surface.blit(self.image, (self.rect))
                        
    def check_doors_state(self, player):
        if 'any' in self.open_actions:
            self.is_activated = True
        
        for action in player.actions:
            if action in self.open_actions:
                self.is_activated = True
        
        
        
        