import pygame
from globals import *
from player import *
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from obstacles import *
from entities import *
from random import randint
class Level:
    def __init__(self, tmx_map: str, bg_path: str):
        """The init func

        Parameters:
        - Tmx_map (str): The path for the map
        - Bg_path (str): The path for the background image"""

        self.screen = pygame.display.get_surface()
        # Groups
        self.visible_sprites = VisibleSprites()
        self.obstacle_sprites = pygame.sprite.Group()
        self.semi_obstacles_sprites = pygame.sprite.Group()
        
        
        # Setting up the map
        self.setup_map(tmx_map)
        
        # The main background
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, MAP_SIZE)

        # The x_offset for the map drawing
        self.offset = 0

    def setup_map(self, tmx_map):
        """Loads the tmx map
        
        Parameters:
        - Tmx_map (str): The path for the map"""
        tmx_map = load_pygame(tmx_map)
        
        self.width = tmx_map.width * TILE_SIZE

        # For the background textures
        floor = tmx_map.get_layer_by_name("bg_tex")
        groups = [self.visible_sprites]
        # Iterating through them
        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "shades")


        # Objectssssssssss
        floor = tmx_map.get_layer_by_name("objects")
        groups = [self.visible_sprites, self.semi_obstacles_sprites]
        # Drawing them
        for obj in floor:
            SemiCollidablePlatform(
                groups,
                (obj.x, obj.y + 16 - obj.height),
                obj.image,
                "semi_obstacles",
                300,
                randint(400, 1000) / 500)

        # Creating the player
        self.player = Player(
            [self.visible_sprites],
            self.obstacle_sprites,
            self.semi_obstacles_sprites,
            [0, 3000])
        
        # For the foreground textures
        floor = tmx_map.get_layer_by_name("fg_tex")
        groups = [self.visible_sprites]
        # Iterating through them
        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "shades")

        # For the obstacles
        floor = tmx_map.get_layer_by_name("main")
        groups = [self.visible_sprites, self.obstacle_sprites]
        # Iterating through them
        for tile in floor.tiles():
            Tile(groups, (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE + 16), tile[2], "obstacle")
        
        self.enemy = WitchCraft(self.visible_sprites)

    def run(self, screen: pygame.Surface):
        """Called to updates the whole level
        
        Parameters:
        - Screen (pygame.Surface): The main display"""
        self.screen.blit(self.background, (0,0))

        self.semi_obstacles_sprites.update()
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
        

    def draw(self, screen: pygame.Surface, offset: int):
        """Draws the whole map and player effects and calculates the x offset
        
        Parameters:
        - Screen (pygame.Surface): The main display
        - Offset (int): The x_offset for the map drawing"""
        for sprite in self.sprites():
            if sprite.type == "player":
                width = sprite.image.get_width()
                width = 42 - width
                width = int(width / 2)

                rect = sprite.rect.copy()
                rect.x -= offset
                screen.blit(sprite.image, (rect.x + width, rect.y))
                sprite.draw_effects(offset)                
                # pygame.draw.rect(screen, "yellow", rect, 2)
            else:
                rect = sprite.rect.copy()
                rect.x -= offset
                screen.blit(sprite.image, rect)
                # if sprite.type != "shades":
                #     pygame.draw.rect(screen, "red", rect, 1)


