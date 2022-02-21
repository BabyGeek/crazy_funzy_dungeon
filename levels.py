import random, pygame, pytmx, os
from helpers import *
from level_constants import *
from renderer import Renderer
from constants import *
from game_objects import *


class Level:
    def __init__(self, game, level_number = 0):
        
        self.game = game
        self.level = LEVELS['level_' + str(level_number)]
        self.current_room_index = DEFAULT_INDEX_START
        
        self.current_room = None
        self.actions = []
        
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
            self.rooms[0].append(Room(self, os.path.join(os.getcwd(), 'resources', 'maps', self.level['folder'], 'map.tmx'), self.level))
        else:
            column = 0
            for row in self.level['rooms']:
                self.rooms.append(list())
                for room in row:
                    image = random.choice([name for name in os.listdir(os.path.join(os.getcwd(), 'resources', 'maps', self.level['folder'], LEVELS_IMAGES_FOLDER[column], room)) if '.tmx' in name])
                    self.rooms[column].append(Room(self, os.path.join(os.getcwd(), 'resources', 'maps', self.level['folder'],  LEVELS_IMAGES_FOLDER[column], room, image), self.level))
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
        self.current_room.draw(display, camera)
        
    def update_current_room(self):
        if len(self.rooms):
            self.current_room = self.rooms[self.current_room_index[0]][self.current_room_index[1]]
            self.current_room.update()
            
    
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
        
        self.rooms = []
        self.load_rooms()
        
        
        
class Room:
    def __init__(self, level, room_image, level_options):
        self.level = level
        self.renderer = Renderer(self.level.game, room_image)
        self.tmx_data = self.renderer.tmx_data
        self.level_options = level_options
        self.enemy_down = 0
        self.enemies = self.level_options['enemies_number_per_room']
        self.is_cleaned = False
        
        self.surface = self.renderer.map_surface
        self.rect = self.surface.get_rect()
     
         
    def draw(self, display, camera = None):
        if not camera:
            display.blit(self.surface, self.rect)
        else:
            display.blit(self.surface, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))
    
    def get_opening_actions(self):
        return self.level_options['open_door_actions']
    
    def update(self):
        if self.enemy_down >= self.enemies:
            self.is_cleaned = True