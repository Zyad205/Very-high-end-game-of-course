import pygame


class Line(pygame.sprite.Sprite):
    def __init__(self, groups: list, pos: tuple, width: int, height: int, png):
        """The init func
        Parameters:
        - Groups (list): The pygame sprite groups to be added in
        - Pos (tuple[int]): The position of the up left corner of the line
        - Width (int): The width of the line
        - Height (int): The height of the line
        - Png (): A loaded pygame image"""

        super().__init__(groups)

        self.image = png

        self.rect = pygame.rect.Rect(*pos, width, height)

        


