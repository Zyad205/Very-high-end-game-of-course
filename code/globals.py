from sys import argv
from os.path import dirname

DEBUGGING = True

# PATHS
MAIN_DIR = dirname(dirname(argv[0]))
SMAIN_DIR = MAIN_DIR + "/"
PLAYER_PATHS = [SMAIN_DIR + "graphics/player/idle",
                SMAIN_DIR + "graphics/player/run",
                SMAIN_DIR + "graphics/player/land"]
OBSTACLES_PATHS = [SMAIN_DIR + "graphics/obstacles/line.png",
                   SMAIN_DIR + "graphics/obstacles/box.png"]
MAPS_PATHS = [SMAIN_DIR + "maps/main.tmx"]

# PLAYER
PLAYER_IMG_MULTI = 3

# SIZES
TILE_SIZE = 64
MAP_SIZE = (1280, 720)