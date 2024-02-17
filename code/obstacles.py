import pygame
from globals import TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, groups: list, pos: tuple, surf):
        """The init func
        Parameters:
        - Groups (list): The pygame sprite groups to be added in
        - Pos (tuple[int]): The position of the up left corner of the line
        - surf (): A loaded pygame image"""

        super().__init__(groups)

        self.image = surf

        self.rect = pygame.rect.Rect(*pos, TILE_SIZE, TILE_SIZE)
        self.mask = pygame.mask.from_surface(self.image)




