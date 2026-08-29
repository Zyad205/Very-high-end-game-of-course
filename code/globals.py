from sys import argv
from os.path import dirname, join
import pathlib

DEBUGGING = False

# PATHS
MAIN_DIR = dirname(dirname(argv[0]))
MAIN_DIR = pathlib.Path(MAIN_DIR)

PLAYER_PATH_I = MAIN_DIR / "graphics" / "player" / "images"
PLAYER_PATH_E = MAIN_DIR / "graphics" / "player" / "effects"

PLAYER_PATHS = {
    "idle": PLAYER_PATH_I / "idle",
    "run": PLAYER_PATH_I / "run",
    "land": PLAYER_PATH_I / "land",
    "attack": PLAYER_PATH_I / "attack",
    "hit": PLAYER_PATH_I / "hit",
    "effect_land": PLAYER_PATH_E / "land",
    "effect_attack": PLAYER_PATH_E / "attack"}

SATYR_PATH_I = MAIN_DIR / "graphics" / "enemies" / "satyr" / "images"
SATYR_PATH_E = MAIN_DIR / "graphics" / "enemies" / "satyr" / "effects"

VIRTUALGUY_PATHS = {
    "idle": SATYR_PATH_I / "idle",
    "run": SATYR_PATH_I / "run",
    "hit": SATYR_PATH_I / "dead",
    "effect_hit": SATYR_PATH_E / "hit"
}
BTN_PATH = MAIN_DIR / "graphics" / "start_btn.png"

# ENEMY
ENEMIES_IMG_MULTI = {"virtualguy": 3}
ENEMY_HITBOX_SIZE = (56, 56)
ENEMY_DRAW_OFFSET = {
    "idle": (0, 5),
    "run": (0,5),
    "hit": (0, 5)
}

# PLAYER
PLAYER_IMG_MULTI = 3
PLAYER_EFFECTS_MULTI = 4
PLAYER_HITBOX_SIZE = (32, 42)
PLAYER_ATTACK_HITBOX_SIZE = (77, 42)


MAPS_PATHS = [MAIN_DIR / "maps" / "main.tmx"]

BG_PATH = MAIN_DIR / "graphics" / "bg.png"

# SIZES
TILE_SIZE = 64
MAP_SIZE = (1280, 720)
