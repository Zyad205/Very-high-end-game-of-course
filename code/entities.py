import pygame
from globals import *
from engine import *

class WitchCraft(pygame.sprite.Sprite):
    def __init__(self, groups):

        super().__init__(groups)

        self.animations = {"idle": Animation(WITCHCRAFT_PATHS["idle"], 0.06, 4)}

        self.animation_controller = AnimationController(self.animations, [], "idle")

        self.image = self.animation_controller.image
        self.rect = self.image.get_rect(center=(400, 500))
        self.type = "witch"

    def update(self):
        self.animation_controller.update()
        self.image = self.animation_controller.image