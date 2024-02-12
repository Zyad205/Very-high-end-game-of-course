# Arts used by https://penusbmic.itch.io/sci-fi-character-pack-12
# Arts used by https://0x72.itch.io/16x16-industrial-tileset

import pygame
from debug import debug

from engine import Animation
from entities import *
from obstacles import *

debugging = False


class Main:
    def __init__(self):

        # Initialize pygame
        pygame.init()

        # Screen properties 
        
        if debugging:
            flags = pygame.SCALED
        else:
            flags = pygame.FULLSCREEN | pygame.SCALED
        
        self.screen_size = (1280, 720)
        # Screen creation
        self.screen = pygame.display.set_mode(self.screen_size, flags)

        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        self.player = Player([self.visible_sprites], self.obstacle_sprites)
        self.create_obstacles()
        # Title
        pygame.display.set_caption("Very high end game")

        # Clock
        self.clock = pygame.Clock()
        # Main loop
        self.main_loop()

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit("User closed")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        exit("User closed")

                # Remove after finishing develop
            self.screen.fill("BLACK")
            self.visible_sprites.update()
            self.visible_sprites.draw(self.screen)
            # debug("IIIii")
            pygame.display.flip()
            self.clock.tick(60)

    def create_obstacles(self):
        img_1 = pygame.image.load(OBSTACLES_PATHS[0])    
        img_2 = pygame.image.load(OBSTACLES_PATHS[1])    
        groups = [self.visible_sprites, self.obstacle_sprites]
        line_one = Line(groups, (100, 600), 256, 64, img_1)
        line_two = Line(groups, (604, 500), 256, 64, img_1)
        line_three = Line(groups, (100, 200), 256, 64, img_1)
        
        box_one = Line(groups, (700, 656), 64, 64, img_2)
        box_two = Line(groups, (448, 582), 64, 64, img_2)
if __name__ == "__main__":
    main = Main()
    