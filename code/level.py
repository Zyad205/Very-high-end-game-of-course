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
        self.visible_sprites = VisibleSprites()
        self.obstacle_sprites = pygame.sprite.Group()

        self.setup_map(tmx_map)
        

        self.background = pygame.image.load(SMAIN_DIR + "graphics/bg.png").convert()
        self.background = pygame.transform.scale(self.background, MAP_SIZE)

        self.offset = 0

    def setup_map(self, tmx_map):
        tmx_map = load_pygame(tmx_map)
        
        self.width = tmx_map.width * TILE_SIZE

        floor = tmx_map.get_layer_by_name("bg_tex")
        groups = [self.visible_sprites]
        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "shades")

        self.player = Player([self.visible_sprites], self.obstacle_sprites, [0, 3000])
            
        floor = tmx_map.get_layer_by_name("fg_tex")
        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "shades")


        floor = tmx_map.get_layer_by_name("main")
        groups = [self.visible_sprites, self.obstacle_sprites]
        

        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "obstacle")

        floor = tmx_map.get_layer_by_name("objects")
    
        for obj in floor:
            print(obj.properties)
            Tile(groups, (obj.x, obj.y + 16 - obj.height), obj.image, "obstacles")

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


        self.visible_sprites.draw(screen, self.offset)
        

class VisibleSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        

    def draw(self, screen, offset):
        for sprite in self.sprites():
            if sprite.type == "player":
                width = sprite.image.get_width()
                width = 42 - width
                width = int(width / 2)

                rect = sprite.rect.copy()
                rect.x -= offset
                screen.blit(sprite.image, (rect.x + width, rect.y))
                sprite.draw_effects(offset)                
            else:
                rect = sprite.rect.copy()
                rect.x -= offset
                screen.blit(sprite.image, rect)

            # pygame.draw.rect(screen, "white", rect, 1)
