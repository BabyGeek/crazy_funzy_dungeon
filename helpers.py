import pygame, sys

facings_directions = {
    'left': (-1, 0),
    'right': (1, 0),
    'up': (0, -1),
    'down': (0, 1),
}

def get_direction_velocity_for_facing(facing):
    return facings_directions[facing]

def quit_game():
    pygame.quit()
    sys.exit(-1)
    quit();

