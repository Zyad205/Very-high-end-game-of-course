import pygame
from globals import *


# This class isn't final and still under work until i know 
# how exactly i will go about it
class Signals:
    def __init__(self, level):
        self.level = level

    def player_attacking(self, attack_type, hitbox=pygame.Rect):
        if hitbox.colliderect(self.level.enemy):
            if attack_type == "attack":
                self.level.enemy.get_hit(25)

    def virtual_guy_attacking(self, hitbox=pygame.Rect):
        if hitbox.colliderect(self.level.player):
            self.level.player.get_hit(10, hitbox)