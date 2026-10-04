import pygame
from globals import *
from player import *
from pytmx.util_pygame import load_pygame
from pytmx import TiledMap
from obstacles import *
from enemies import *
from random import randint
from signals import *
from button import Button
from debug import print_debug_list
from maps import Map

def has_method(o, name: str):
    """Checks if an object has a method

    Parameters:
    - O (object): Any python object
    - Name (str): The method name

    Return:
    - Bool: Returns true if it has it false otherwise"""
    return callable(getattr(o, name, None))


class GameLoop:
    def __init__(self):
        """The init func

        Parameters:
        - Tmx_map (str): The path for the map
        - Bg_path (str): The path for the background image"""

        self.map = Map(MAPS_PATHS[0], BG_PATH)
        self.active_map = self.map            
        

        # The x_offset for the map drawing
        self.offset = 0

        # States 
        # running - paused
        self.state = "running"

        # Pause menu overlay
        self.grey_overlay = pygame.Surface(MAP_SIZE)
        self.grey_overlay.fill((50, 50, 50))
        self.grey_overlay.set_alpha(128)

        # Testing 
        self.button = Button("Run", 40, 40, "red", "grey", "white")

    def run(self, screen: pygame.Surface):
        """Called to updates the whole level
        
        Parameters:
        - Screen (pygame.Surface): The main display"""

        if self.state == "running":
            self.active_map.update()
            self.draw(screen)

        elif self.state == "paused":
            self.draw(screen)
            self.print_pause_menu(screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button.handle_event(event):
                        self.state = "running"




    def calculate_camera(self):
        # Camera
        x = self.active_map.player.rect.centerx
        half_the_map = MAP_SIZE[0] / 2
        if x > half_the_map and self.active_map.width - half_the_map > x:
            self.offset = x - half_the_map
    
    def draw(self, screen):
        self.calculate_camera()
        self.active_map.draw(screen, self.offset)
        debug(self.state)
        print_debug_list()

    def print_pause_menu(self, screen: pygame.Surface):
        screen.blit(self.grey_overlay, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        self.button.check_hover(mouse_pos)
        self.button.draw(screen)
