from sys import argv
from os.path import dirname

DEBUGGING = 0

# PATHS
MAIN_DIR = dirname(dirname(argv[0]))
SMAIN_DIR = MAIN_DIR + "/"

PLAYER_PATHS = [SMAIN_DIR + "graphics/player/images/idle",
                SMAIN_DIR + "graphics/player/images/run",
                SMAIN_DIR + "graphics/player/images/land",
                SMAIN_DIR + "graphics/player/images/attack",
                SMAIN_DIR + "graphics/player/images/s_attack",
                SMAIN_DIR + "graphics/player/effects/land",
                SMAIN_DIR + "graphics/player/effects/attack"]

MAPS_PATHS = [SMAIN_DIR + "maps/main.tmx"]

# PLAYER
PLAYER_IMG_MULTI = 3
PLAYER_EFFECTS_MULTI = 4

# SIZES
TILE_SIZE = 64
MAP_SIZE = (1280, 720)