SPRITE_SIZE = 32

LEVELS_IMAGES_FOLDER = {
    0: 'TOP',
    1: 'MIDDLE',
    2: 'BOTTOM',
}

WALL_LAYER = 0
DOOR_LAYER = 1
NPC_LAYER = 1
DECORATION_DOWN_LAYER = 2
PLAYER_LAYER = 3
ENEMY_LAYER = 3
DECORATION_TOP_LAYER = 4
BULLET_LAYER = 5
EFFECTS_LAYER = 6
BORDER_LAYER = 12

DEFAULT_INDEX_START = [1, 1]

LEVELS = {
    'level_0':{
        'name'           : 'Starting room',
        'folder'         : 'start_map',
        'ennemy_per_room'              : 4,
        'open_door_actions'            : ['cleaned'],
        'enemies_number_per_room'      : 0,
        'enemies_type'                 : [],
        'door_object_layer'            : 'doors_objects',
    },
    'level_1':{
        'name'           : 'Level 1',
        'folder'         : 'level_1',
        'rooms'     : [
            [
                'LEFT', 
                'MIDDLE', 
                'RIGHT'
            ],  
            [
                'LEFT', 
                'MIDDLE', 
                'RIGHT'
            ],  
            [
                'LEFT', 
                'MIDDLE', 
                'RIGHT'
            ],  
      ],
      'ennemy_per_room'              : 4,
      'open_door_actions'            : ['cleaned'],
    },
    'level_2':{
        'name'  : 'Level 2',
        'folder': 'level_2',
        'rooms' : [  
      ],
      'open_door_actions'            : ['cleaned'],
      'enemies_number_per_room'      : 5,
      'enemies_type'                 : [1, 6]
    },
}