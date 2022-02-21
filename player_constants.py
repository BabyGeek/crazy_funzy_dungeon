CHARACTER_IMAGES_PATH = 'resources/images/characters/{}'
CHARACTER_MAPS_PATH = 'resources/maps'
PLAYER_SPRITE_IMAGE_SUFFIX = '_32x32.png'
PLAYER_SPRITE_W, PLAYER_SPRITE_H = (32, 46)

PLAYERS_SPRITES_OPTIONS = {
    'Bob': {
        'images_per_animations': 6,
        'images_for_reading'   : 18,
        'speed'           : 200,
        'base_speed'           : [6, 6],
        'states'               : [
            'idle',
            'idle_anim',
            'phone',
            'reading',
            'run',
            'sit3',
        ],
        'idle_state'     : 'idle',
        'idle_anim_state': 'idle_anim',
        'phone_state'    : 'phone',
        'reading_state'  : 'reading',
        'run_state'      : 'run',
        'sit_state'      : 'sit3',
    }
}