# Arts used by https://0x72.itch.io/16x16-industrial-tileset
# Background used by https://free-game-assets.itch.io/free-city-backgrounds-pixel-art
# https://styloo.itch.io/pixel-grass-and-flowers
# https://arks.itch.io/witchcraft-spritesheet
import pygame
from debug import debug
from globals import *
from level import Level
               

class Main:
    def __init__(self):

        # Initialize pygame
        pygame.init()

        # Screen properties
        
        if DEBUGGING:
            flags = pygame.SCALED
        else:
            flags = pygame.FULLSCREEN | pygame.SCALED
        
        self.screen_size = MAP_SIZE

        # Screen creation
        self.screen = pygame.display.set_mode(self.screen_size, flags)
        pygame.display.set_caption("Very high end game")

        self.level = Level(MAPS_PATHS[0], BG_PATH)
        self.offset = 0
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
                

            self.level.run(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
            

if __name__ == "__main__":
    main = Main()
