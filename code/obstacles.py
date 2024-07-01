import pygame
from globals import TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups: list, pos: tuple, surf: pygame.Surface, type: str):
        """The init func
        
        Parameters:
        - Groups (list): The pygame sprite groups to be added in
        - Pos (tuple[int]): The position of the up left corner of the line
        - surf (): A loaded pygame image"""

        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type

class SemiCollidablePlatform(Tile):
    def __init__(
            self,
            groups: list,
            pos: tuple[int],
            surf: pygame.Surface,
            type: str,
            x_movement: int = 0,
            speed: int = 1):
        """The init function
        
        Parameters:
        - Groups: The groups where the sprite get put in
        - Pos (tuple[int]): The position where the platform start moving
        - Surf (pygame.Surface): The image for the platform
        - Type (str): The type of this tile
        - X movement (int): How much will the platform move
        - Speed (int): The speed of the platform"""
        
        super().__init__(groups, pos, surf, type)
        

        self.x_movement = x_movement

        self.starting_x = pos[0]
        self.ending_x = pos[0] + x_movement

        self.direction = 1 # 1 right, 0 left\

        self.speed = speed

        self.x = self.rect.x

    def update(self):
        """Updating the platform position"""
        if not self.x_movement:
            return
        
        if self.direction:
            self.x += self.speed
            self.rect.x = self.x

            if self.rect.x > self.ending_x:
                self.direction = 0
                self.rect.x = self.ending_x
                self.x = self.rect.x
        else:
            self.x -= self.speed
            self.rect.x = self.x

            if self.rect.x < self.starting_x:
                self.direction = 1
                self.rect.x = self.starting_x
                self.x = self.rect.x

        
        
        
        
