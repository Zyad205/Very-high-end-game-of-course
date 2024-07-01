from sys import argv
from os.path import dirname

DEBUGGING = 0

# PATHS
MAIN_DIR = dirname(dirname(argv[0]))
SMAIN_DIR = MAIN_DIR + "/"

PLAYER_PATHS = {
    "idle": SMAIN_DIR + "graphics/player/images/idle",
    "run": SMAIN_DIR + "graphics/player/images/run",
    "land": SMAIN_DIR + "graphics/player/images/land",
    "attack": SMAIN_DIR + "graphics/player/images/attack",
    "s_attack": SMAIN_DIR + "graphics/player/images/s_attack",
    "effect_land": SMAIN_DIR + "graphics/player/effects/land",
    "effect_attack": SMAIN_DIR + "graphics/player/effects/attack"}



VIRTUALGUY_PATHS = {
    "idle": SMAIN_DIR + "graphics/enemies/virtualguy/idle",
    "run": SMAIN_DIR + "graphics/enemies/virtualguy/run",
    "hit": SMAIN_DIR + "graphics/enemies/virtualguy/hit"
}

ENEMIES_IMG_MULTI = {"virtualguy": 2}

MAPS_PATHS = [SMAIN_DIR + "maps/main.tmx"]
BG_PATH = SMAIN_DIR + "graphics/bg.png"
# PLAYER
PLAYER_IMG_MULTI = 3
PLAYER_EFFECTS_MULTI = 4

# SIZES
TILE_SIZE = 64
MAP_SIZE = (1280, 720)