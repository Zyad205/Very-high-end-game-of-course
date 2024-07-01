import pygame
from globals import *
from engine import *
from math import hypot
from debug import debug

def is_close(object_one, object_two, distance: int):
    """Checks if two rect are close or not
    
    Parameters:
    - Object one: The first rectangle
    - Object two: The second rectangle
    - Distance (int): The furthest distance that could be between them
    
    Returns
    - Bool: Returns true is they are near false otherwise"""

    return hypot(object_two.x-object_one.x, object_two.y-object_one.y) < float(distance)

class VirtualGuy(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, player):
        
        # The father init function
        super().__init__(groups)

        # Animations
        self.animations = {
            "idle": Animation(
                VIRTUALGUY_PATHS["idle"],
                0.12,
                ENEMIES_IMG_MULTI["virtualguy"]),
            "run": Animation(
                VIRTUALGUY_PATHS["run"],
                0.15,
                ENEMIES_IMG_MULTI["virtualguy"]),
            "hit": Animation(
                VIRTUALGUY_PATHS["hit"],
                0.2,
                ENEMIES_IMG_MULTI["virtualguy"],
                True
            )}

        # Animation controller
        self.animation_controller = AnimationController(self.animations, ["hit"], "idle")

        # Attributes
        self.player = player
        self.obstacles = obstacles
        self.type = "enemy"
        
        self.image = self.animation_controller.image
        self.rect = self.image.get_rect(center=(200, 470))

        # Y movement related attributes
        self.y_speed = 0
        self.gravity = 1
        self.Y_LIMIT = 720

        # 1 - Left, 0 - Right
        self.direction = 0

        # X speed
        self.x_speed = 0

        # Timers
        self.timers = {"hit": Timer(500)}

        # Health
        self.health = 100
        self.health_bar = StatusBar(
            100,
            100,
            "red",
            "yellow",
            "white",
            False,
            True,
            80,
            10,
            self.rect.center)

    def update(self):
        """The logic update function"""
        self.animation_controller.update()
        
        self.image = pygame.transform.flip(
            self.animation_controller.image,
            flip_x=self.direction,
            flip_y=False)
        
        # Updates timers
        self.update_timers()
        
        # Checks if the player is close
        close = is_close(self.rect, self.player.rect, 200)

        
        if close:
            self.look_at_player()
        else:
            self.x_speed = 0
            self.animation_controller.play_animation("idle")

        self.movement()
        rect = self.rect.copy()
        rect.y -= 40
        self.health_bar.update_pos(rect.center)

    def look_at_player(self):
        """Changes the direction based on the player position"""

        if self.player.rect.centerx - self.rect.centerx > 0: # Player to the right
            self.direction = 0
            self.x_speed = 1

        elif self.player.rect.centerx - self.rect.centerx < 0: # Player to the left
            self.direction = 1
            self.x_speed = -1

        else:
            self.x_speed = 0 # We are at the player position
            self.animation_controller.play_animation("idle")
        

    def movement(self):
        if self.x_speed != 0 and not self.timers["hit"].active:
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

                # Attributes
                self.y_speed = 0
                self.can_jump = True

    def get_hit(self, damage):
        self.animation_controller.play_animation("hit", 1)
        self.timers["hit"].activate()
        self.health -= damage
        if self.health <= 0:
            self.kill()
        self.health_bar.update_stat(self.health)
        
    def update_timers(self):
        """Updates all timers"""

        for timer in self.timers.values():
            timer.update()
    
    def draw_bars(self, x_offset):
        self.health_bar.draw(x_offset)

