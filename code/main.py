# Arts used by https://0x72.itch.io/16x16-industrial-tileset
# Background used by https://free-game-assets.itch.io/free-city-backgrounds-pixel-art
# https://styloo.itch.io/pixel-grass-and-flowers
# https://arks.itch.io/witchcraft-spritesheet
# https://pixelfrog-assets.itch.io/pixel-adventure-1

import pygame
import debug
from globals import *
import globals 
from level import Level
               

def set_screen_mode(main: Main):
    """Creates the screen or changes it's attributes depending on the debugging value
    
    Parameters: 
    - main: The main main of the mains just pass the main object"""

    if globals.DEBUGGING:
        flags = pygame.FULLSCREEN | pygame.SCALED
    else:
        flags = pygame.FULLSCREEN | pygame.SCALED

    
    

    # Screen manipulation
    main.screen = pygame.display.set_mode(main.screen_size, flags)



class Main:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        
        self.screen_size = MAP_SIZE
        
        # Creates the main window
        set_screen_mode(self)

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F3:
                        globals.DEBUGGING = not globals.DEBUGGING
                        set_screen_mode(self)

            # Reset the debug y offset for each cycle 
            debug.y_offset = 0 
            self.level.run(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
            

if __name__ == "__main__":
    main = Main()
 