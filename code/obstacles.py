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
            pos: tuple,
            surf: pygame.Surface,
            type: str,
            x_movement: int = 0):
        
        super().__init__(groups, pos, surf, type)
        
        self.x_movement = x_movement
        self.starting_x = pos[0]
        self.ending_x = pos[0] + x_movement
        self.direction = 1 # 1 right, 0 left

    def update(self):
        if not self.x_movement:
            return
        if self.direction:
            self.rect.centerx += 1
            if self.rect.centerx > self.ending_x:
                self.direction = 0
                self.rect.centerx = self.ending_x
        else:
            self.rect.centerx -= 1
            if self.rect.centerx < self.starting_x:
                self.direction = 1
                self.rect.centerx = self.starting_x

        
        
        
        
