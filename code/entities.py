import pygame
from globals import *
from engine import *
from math import hypot
from debug import debug

def is_close(object1, object2, distance):
    return hypot(object2.x-object1.x, object2.y-object1.y) < float(distance)

class VirtualGuy(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, player):

        super().__init__(groups)

        self.animations = {
            "idle": Animation(
                VIRTUALGUY_PATHS["idle"],
                0.12,
                ENEMIES_IMG_MULTI["virtualguy"]),
            "run": Animation(
                VIRTUALGUY_PATHS["run"],
                0.15,
                ENEMIES_IMG_MULTI["virtualguy"]
            )}

        self.animation_controller = AnimationController(self.animations, [], "idle")

        self.image = self.animation_controller.image
        self.rect = self.image.get_rect(center=(200, 470))
        self.type = "enemy"

        # Y movement related attributes
        self.y_speed = 0
        self.gravity = 1
        self.Y_LIMIT = 720
        # 1 - Left, 0 - Right
        self.direction = 0

        # X speed
        self.x_speed = 0

        # Obstacles
        self.obstacles = obstacles

        # Player
        self.player = player

    def update(self):
        self.animation_controller.update()
        
        self.image = pygame.transform.flip(
            self.animation_controller.image,
            flip_x=self.direction,
            flip_y=False)
        
        close = is_close(self.rect, self.player.rect, 200)
        self.movement()

        if close:
            self.look_at_player()
        else:
            self.x_speed = 0
            self.animation_controller.play_animation("idle")

    def look_at_player(self):
        if self.player.rect.centerx - self.rect.centerx > 0:
            self.direction = 0
            self.x_speed = 1
        elif self.player.rect.centerx - self.rect.centerx < 0:
            self.direction = 1
            self.x_speed = -1
        else:
            self.x_speed = 0
            self.animation_controller.play_animation("idle")
        

    def movement(self):
        if self.x_speed != 0:
            self.rect.x += self.x_speed
            self.animation_controller.play_animation("run")
            self.collisions("horizontal")

        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        self.collisions("vertical")
    
    def collisions(self, direction):
        if direction == "horizontal":
            sprite = pygame.sprite.spritecollide(self, self.obstacles, False)
            if len(sprite) > 0:
                sprite = sprite[0]
            else:
                return
            
            if self.direction: # Going right
                self.rect.left = sprite.rect.right
            else: # Going left
                self.rect.right = sprite.rect.left

        if direction == "vertical":
            landed = False
            # Main land
            if self.rect.bottom > self.Y_LIMIT:
                self.rect.bottom = self.Y_LIMIT
                landed = True


            # Collisions with platforms
            sprite = pygame.sprite.spritecollide(self, self.obstacles, False)
            if len(sprite) > 0: # Makes sure a collision was made
                sprite = sprite[0]

                if self.y_speed > 0: # Falling
                    self.rect.bottom = sprite.rect.top
                    landed = True
                else: # Jumping
                    self.rect.top = sprite.rect.bottom
                    self.y_speed = 0

            if landed: # Landing effects
                # if not self.can_jump and self.y_speed > 30:
                #     # Effects
                #     if self.animation_controller.play_animation("land"):
                #         self.play_effect("land")
                # Attributes
                self.y_speed = 0
                self.can_jump = True   