from sys import argv
from os.path import dirname

MAIN_DIR = dirname(dirname(argv[0]))
SMAIN_DIR = MAIN_DIR + "/"
PLAYER_PATHS = [SMAIN_DIR + "graphics/player/idle",
                SMAIN_DIR + "graphics/player/run",
                SMAIN_DIR + "graphics/player/land"]
OBSTACLES_PATHS = [SMAIN_DIR + "graphics/obstacles/line.png",
                   SMAIN_DIR + "graphics/obstacles/box.png"]
PLAYER_IMG_MULTI = 3