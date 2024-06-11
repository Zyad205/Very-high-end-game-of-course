import pygame
from engine import *
from globals import *
from debug import debug

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, semi_obstacles, x_limits=MAP_SIZE):

        # The father init func
        super().__init__(groups)

        # Animations        
        self.animations = {"idle": Animation(PLAYER_PATHS["idle"], 0.06, PLAYER_IMG_MULTI),
                           "run": Animation(PLAYER_PATHS["run"], 0.15, PLAYER_IMG_MULTI),
                           "land": Animation(PLAYER_PATHS["land"], 0.15, PLAYER_IMG_MULTI, 1),
                           "attack": Animation(PLAYER_PATHS["attack"], 0.2, PLAYER_IMG_MULTI, 1),
                           "s_attack": Animation(PLAYER_PATHS["s_attack"], 0.15, PLAYER_IMG_MULTI, 1)}
        
        self.animation_controller = AnimationController(
            self.animations,
            ["land", "attack", "s_attack"],
            "idle")

        # Effects
        self.effects = {"land": Effect(PLAYER_PATHS["effect_land"], 0.2, PLAYER_EFFECTS_MULTI),
                        "attack": Effect(PLAYER_PATHS["effect_attack"], 0.3, PLAYER_EFFECTS_MULTI)}

        self.active_effects = []

        # Attributes
        self.rect = pygame.rect.Rect(0, 0, 42, 42)
        self.rect.midbottom = (400, 720)

        self.hitbox = self.rect.copy()
        self.hitbox = self.hitbox.inflate(-10, 0)
        self.hitbox.center = self.rect.center
        
        self.obstacles = obstacles
        self.semi_obstacles = semi_obstacles

         # 1 - Left, 0 - Right
        self.direction = 0
        self.type = "player"

        self.x_offset_platform = None
        self.platform_on = None

        # Y axis
        self.jump = False
        self.gravity = 1
        self.y_speed = 0
        self.jump_power = 21
        self.can_jump = True
        

        # World limits
        self.X_LIMITS = x_limits
        self.Y_LIMIT = 720

        # Timers
        self.timers = {
            "attack": Timer(700),
            "s_attack": Timer(3000)
        }
    
    def update_timers(self):
        """Updates all timers"""

        for timer in self.timers.values():
            timer.update()


    def update(self) -> None:
        """Yes"""
        self.animation_controller.update()
        self.image = pygame.transform.flip(
            self.animation_controller.image,
            flip_x=self.direction,
            flip_y=False)
        
        self.old_rect = self.rect.copy()

        self.update_timers()
        self.input()
            
    def input(self) -> None:
        """Checks for all player related input"""

        keys = pygame.key.get_pressed()
        
        input_vector = pygame.math.Vector2(0, 0)

        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_w]:
            input_vector.y = 1

        self.movement(input_vector)
        if keys[pygame.K_l]:
            self.attack()
        if keys[pygame.K_j]:
            self.s_attack()

    def movement(self, vector: pygame.math.Vector2):
        """Moves the player according to the the input_vector

        Parameters:
        - Vector (pygame.math.Vector2): The vector taken from input"""
        if vector.x != 0:
            self.rect.x += vector.x * 5
            if vector.x > 0:
                self.direction = 0
            else:
                self.direction = 1

            self.animation_controller.play_animation("run")
            self.re_calc_semi_platform()
        else:
            self.animation_controller.play_animation("idle")
            self.platform_movement()

        self.hitbox.centerx = self.rect.centerx

        self.collisions("horizontal")

        if vector.y != 0 and self.can_jump:
            self.can_jump = False
            self.y_speed -= self.jump_power
        
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        self.hitbox.centery = self.rect.centery
        self.collisions("vertical")
        self.semi_collision()

            
    def collisions(self, direction: str):
        """Checks for collisions

        Parameters:
        - Direction (str): The axis which to check for collision in"""
    
        if direction == "horizontal":
            # World borders first
            # Right
            if self.rect.right > self.X_LIMITS[1]:
                self.rect.right = self.X_LIMITS[1]
            # Left
            if self.rect.left < self.X_LIMITS[0]:
                self.rect.left = self.X_LIMITS[0]
            
            # Obstacles
            self.temp_rect = self.rect.copy()
            self.rect = self.hitbox.copy()
            sprite = pygame.sprite.spritecollide(self, self.obstacles, False)
            if len(sprite) > 0:
                sprite = sprite[0]
            else:
                self.rect = self.temp_rect.copy()
                return
            
            if self.direction: # Going right
                self.hitbox.left = sprite.rect.right
            else: # Going left
                self.hitbox.right = sprite.rect.left

            self.rect = self.temp_rect.copy()
            self.rect.centerx = self.hitbox.centerx

        elif direction == "vertical":
            landed = False
            
            # Main land
            if self.rect.bottom > self.Y_LIMIT:
                self.rect.bottom = self.Y_LIMIT
                landed = True

            # Collisions with platforms
            self.temp_rect = self.rect.copy()
            self.rect = self.hitbox.copy()
            sprite = pygame.sprite.spritecollide(self, self.obstacles, False)
            if len(sprite) > 0: # Makes sure a collision was made
                sprite = sprite[0]
                self.rect = self.temp_rect.copy()

                if self.y_speed > 0: # Falling
                    self.rect.bottom = sprite.rect.top
                    landed = True
                else: # Jumping
                    self.rect.top = sprite.rect.bottom
                    self.y_speed = 0

                self.hitbox.centery = self.rect.centery
                
            else:
                self.rect = self.temp_rect.copy()

            if landed: # Landing effects
                if not self.can_jump and self.y_speed > 30:
                    # Effects
                    if self.animation_controller.play_animation("land"):
                        self.play_effect("land")
                # Attributes
                self.y_speed = 0
                self.can_jump = True            
    
    def semi_collision(self):
        """Checks for collisions

        Parameters:
        - Direction (str): The axis which to check for collision in"""
    
        landed = False
        # Collisions with platforms
        sprite = pygame.sprite.spritecollide(self, self.semi_obstacles, False)
        if len(sprite) > 0: # Makes sure a collision was made
            if self.platform_on in sprite:
                sprite = self.platform_on
            else:
                sprite = sprite[0]
            

            if self.y_speed > 0: # Falling
                if self.old_rect.bottom <= sprite.rect.top:
                    self.rect.bottom = sprite.rect.top
                    landed = True
                    self.set_semi_platform(sprite)

        else:
            self.set_semi_platform(None)

        if landed: # Landing effects
            if not self.can_jump and self.y_speed > 30:
                # Effects
                if self.animation_controller.play_animation("land"):
                    self.play_effect("land")
            # Attributes
            self.y_speed = 0
            self.can_jump = True            
    
    def set_semi_platform(self, sprite):
        if sprite == None:
            self.platform_on = None
            return
        
        if self.platform_on != sprite:
            self.platform_on = sprite
            self.x_offset_platform = self.rect.centerx - sprite.rect.centerx
        
    def re_calc_semi_platform(self):
        if self.platform_on is not None:
            self.x_offset_platform = self.rect.centerx - self.platform_on.rect.centerx

    def platform_movement(self):
        if self.platform_on is not None:
            self.rect.centerx = self.platform_on.rect.centerx + self.x_offset_platform

    def attack(self):
        """Attacks"""
        if not self.timers["attack"].active:
            self.animation_controller.play_animation("attack", True)
            self.play_effect("attack")
            self.timers["attack"].activate()

    def s_attack(self):
        """Uses the s attack"""
        if not self.timers["s_attack"].active:
            self.animation_controller.play_animation("s_attack", True)
            self.play_effect("attack")
            self.timers["s_attack"].activate()

    def play_effect(self, effect: str):
        """Plays an effect if it's not playing

        Parameters:
        - Effect (str): The name of the effect in the effects dict"""
        if not effect in self.active_effects:
            self.active_effects.append(effect)
            self.effects[effect].play()

    def draw_effects(self, x_offset: int):
        """Draws all active effects

        Parameters:
        - X_offset (int): The x_offset from the map drawing"""
        for effect in self.active_effects:
            the_effect = self.effects[effect]
            rect = self.rect.copy()
            rect.x -= x_offset

            if effect == "land":
                the_effect.draw(rect.midbottom)

            elif effect == "attack":

                if self.direction:
                    pos = rect.midleft
                else:
                    pos = rect.midright

                pos = [*pos] # Unpacks the tuple into a list
                pos[1] += 10
                the_effect.draw(pos, self.direction)

            # Clears the finished effects
            if not the_effect.playing:
                self.active_effects.remove(effect)
