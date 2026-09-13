import pygame
from globals import *
from engine import *
from math import hypot
from debug import *

class CollidableEntity(pygame.sprite.Sprite):
    def __init__(self, groups):
        """Meant to be overridden by child class"""

        super().__init__(groups)

    def collisions(self, direction):
        """Checks for the collisions after each axis movement
        
        Parameters:
        - Direction (str): The direction
        """
        played_animation = None

        if direction == "horizontal":
            sprite = pygame.sprite.spritecollide(self, self.obstacles, False) 
            if len(sprite) > 0: # Makes sure a collision is made
                sprite = sprite[0]
            else:
                return
            
            direction = 1
            if self.old_hitbox.x - self.hitbox.x < 0:
                direction = 0

            if direction: # Going right
                self.hitbox.left = sprite.rect.right
            else: # Going left
                self.hitbox.right = sprite.rect.left

        if direction == "vertical":
            landed = False
            # Main land
            if self.hitbox.bottom > self.Y_LIMIT:
                self.hitbox.bottom = self.Y_LIMIT
                landed = True


            # Collisions with platforms
            sprite = pygame.sprite.spritecollide(self, self.obstacles, False)
            if len(sprite) > 0: # Makes sure a collision was made
                sprite = sprite[0]

                if self.y_speed > 0: # Falling
                    self.hitbox.bottom = sprite.rect.top
                    landed = True
                else: # Jumping
                    self.hitbox.top = sprite.rect.bottom
                    self.y_speed = 0


            if landed: # Landing effects
                if self.hit_rebounce: self.hit_rebounce -= 1

                if not self.can_jump and self.y_speed > 30:
                    # Effects
                    played_animation = "land"
                # Attributes
                self.y_speed = 0
                self.can_jump = True

                if self.hit_rebounce:
                    self.y_speed = -12
                
                return played_animation

    def semi_collision(self):
        """Checks for collisions"""
    
        landed = False
        played_animation = None
        # Collisions with platforms

        sprite = pygame.sprite.spritecollide(self, self.semi_obstacles, False)
        if len(sprite) > 0: # Makes sure a collision was made
            if self.platform_on in sprite:
                sprite = self.platform_on
            else:
                sprite = sprite[0]
            
            # To make sure the player is falling and also on top of the platform not started falling while 
            # he was under it doesn't make sense while i'm writing it But without it 
            if self.y_speed > 0: # Falling
                if self.old_hitbox.bottom <= sprite.rect.top: 
                    self.hitbox.bottom = sprite.rect.top
                    landed = True
                    
                    self.set_semi_platform(sprite)

        else:
            self.set_semi_platform(None)


        if landed: # Landing effects
            if not self.can_jump and self.y_speed > 30:
                # Effects
                played_animation = "land"
            # Attributes
            self.y_speed = 0
            self.can_jump = True

            return played_animation

    def set_semi_platform(self, sprite):
        """Changes the stored variable for the platform player is on
        and calculates the new offset from this platform
        
        Parameters:
        - Sprite: The sprite for the platform"""
        if sprite == None:
            self.platform_on = None
            return
        
        if self.platform_on != sprite:
            self.platform_on = sprite
            self.x_offset_platform = self.hitbox.centerx - sprite.rect.centerx
        
    def recalculate_semi_platform(self):
        """Recalculates the offset from the platform incase the player moved while on platform"""
        if self.platform_on is not None:
            self.x_offset_platform = self.hitbox.centerx - self.platform_on.rect.centerx

    def platform_movement(self):
        """Moves the player with the platform movement"""
        if self.platform_on is not None:
            self.hitbox.centerx = self.platform_on.rect.centerx + self.x_offset_platform

    def update_timers(self):
        """Updates all timers"""

        for timer in self.timers.values():
            timer.update()

    def play_effect(self, effect: str):
        """Plays an effect if it's not playing

        Parameters:
        - Effect (str): The name of the effect in the effects dict"""
        if not effect in self.active_effects:
            self.active_effects.append(effect)
            self.effects[effect].play() 
