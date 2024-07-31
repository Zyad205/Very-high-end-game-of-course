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

    return hypot(object_two.centerx-object_one.centerx, object_two.centery-object_one.centery) < float(distance)

class VirtualGuy(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, player, attack_signal):
        
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

        self.effects = {"hit": Effect(VIRTUALGUY_PATHS["effect_hit"], 0.3, 1)}
        self.active_effects = []

        # Attributes
        self.player = player
        self.obstacles = obstacles
        self.type = "enemy"
        self.attack_signal = attack_signal

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
        self.timers = {"hit": Timer(500), "attack": Timer(300)}

        # Health
        self.health = 100
        self.health_bar = StatusBar(
            100,
            100,
            "red",
            "yellow",
            "white",
            2,
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
        self.attack_player()

        # Update health bar pos
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
        if self.x_speed != 0 and not self.timers["hit"].active and not self.timers["attack"].active:
            self.rect.x += self.x_speed
            self.animation_controller.play_animation("run")
            self.collisions("horizontal")

        elif self.timers["hit"].active:
            if self.direction_when_hit:
                x_speed = 1
            else:
                x_speed = -1

            self.rect.x += x_speed
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
        self.play_effect("hit")

        self.direction_when_hit = self.direction

        # if self.health <= 0:
        #     self.kill()
        self.health_bar.update_stat(self.health)

        self.y_speed = -6

    def attack_player(self):
        if is_close(self.player.rect, self.rect, 30):
            if not self.timers["attack"].active:

                self.attack_signal(self.rect)
                self.timers["attack"].activate()

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

    def draw_bars(self, x_offset):
        self.health_bar.draw(x_offset)

    def draw_effects(self, x_offset: int):
        """Draws all active effects

        Parameters:
        - X_offset (int): The x_offset from the map drawing"""
        for effect in self.active_effects:
            the_effect = self.effects[effect]
            rect = self.rect.copy()
            rect.x -= x_offset

            if effect == "hit":
                rect = self.rect.copy()
                rect.y -= 5
                if self.direction_when_hit:
                    rect = rect.bottomright
                    flip = True
                else:
                    rect = rect.bottomleft
                    flip = False

                the_effect.draw(rect, flip)

            # Clears the finished effects
            if not the_effect.playing:
                self.active_effects.remove(effect)
