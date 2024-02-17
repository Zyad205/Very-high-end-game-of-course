import pygame
from globals import *
from entities import *
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from obstacles import *

class Level:
    def __init__(self, tmx_map):

        self.screen = pygame.display.get_surface()
        # Groups
        self.visible_sprites = CustomGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player([self.visible_sprites], self.obstacle_sprites, [0, 3000])
        self.setup_map(tmx_map)
        

        self.background = pygame.image.load(SMAIN_DIR + "graphics/bg.png").convert()
        self.background = pygame.transform.scale(self.background, MAP_SIZE)

        self.offset = 0

    def setup_map(self, tmx_map):
        tmx_map = load_pygame(tmx_map)
        
        self.width = tmx_map.width * TILE_SIZE

        floor = tmx_map.get_layer_by_name("shades")
        groups = [self.visible_sprites]
        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "shades")
            
        floor = tmx_map.get_layer_by_name("main")
        groups = [self.visible_sprites, self.obstacle_sprites]
        

        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "obstacle")

        floor = tmx_map.get_layer_by_name("objects")
    
        # for obj in floor:               
        #     Tile(groups, (obj.x, obj.y + 16), obj.image, "obstacles")

    def run(self, screen):
        self.screen.blit(self.background, (0,0))

        self.visible_sprites.update()

        # Camera 1
        # x = self.player.rect.centerx - self.offset
        # if x <= 40:
        #     self.offset = self.player.rect.centerx - 40
        # elif x >= 1240:
        #     self.offset = self.player.rect.centerx - 1240
        # if self.player.rect.centerx <= 50:
        #     self.offset = 0

        # Camera 2
        x = self.player.rect.centerx
        half_the_map = MAP_SIZE[0] / 2
        if x > half_the_map and self.width - half_the_map > x:
            self.offset = x - half_the_map


        self.visible_sprites.custom_draw(screen, self.offset)
        

class CustomGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        

    def custom_draw(self, screen, offset):
        for sprite in self.sprites():
            rect = sprite.rect.copy()
            rect.x -= offset
            screen.blit(sprite.image, rect)
            # pygame.draw.rect(screen, "white", rect, 1)
            # if sprite.type == "player":
            #     pygame.draw.rect(screen, "red", rect, 2)
