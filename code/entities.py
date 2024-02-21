import pygame
from engine import *
from globals import *
from debug import debug

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, obstacles, x_limits=MAP_SIZE):

        # The father init func
        super().__init__(groups)

        # Animations        
        self.animations = {"idle": Animation(PLAYER_PATHS[0], 0.06, PLAYER_IMG_MULTI),
                           "run": Animation(PLAYER_PATHS[1], 0.15, PLAYER_IMG_MULTI),
                           "land": Animation(PLAYER_PATHS[2], 0.15, PLAYER_IMG_MULTI, 1),
                           "attack": Animation(PLAYER_PATHS[3], 0.2, PLAYER_IMG_MULTI, 1),
                           "s_attack": Animation(PLAYER_PATHS[4], 0.15, PLAYER_IMG_MULTI, 1)}
        
        self.animation_controller = AnimationController(self.animations, ["land", "attack", "s_attack"], "idle")

        self.current_animation = "idle"
        self.animation = self.animations[self.current_animation]
        self.last_animation_update = False

        # Effects
        self.effects = {"land": Effect(PLAYER_PATHS[5], 0.2, PLAYER_EFFECTS_MULTI),
                        "attack": Effect(PLAYER_PATHS[6], 0.3, PLAYER_EFFECTS_MULTI)}

        self.active_effects = []

        # Attributes
        self.image = self.animation.image
        self.rect = pygame.rect.Rect(0, 0, 42, 42)
        self.rect.midbottom = (400, 720)
        
        self.obstacles = obstacles

         # 1 - Left, 0 - Right
        self.direction = 0
        self.type = "player"

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
        for timer in self.timers.values():
            timer.update()


    def update(self) -> None:
        self.animation_controller.update()
        self.image = pygame.transform.flip(
            self.animation_controller.image,
            flip_x=self.direction,
            flip_y=False)
        
        self.update_timers()
        self.old_rect = self.rect
        self.input()
            
    def input(self) -> None:

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
            
    def movement(self, vector):
        new_animation = ""
        if vector.x != 0:
            self.rect.x += vector.x * 5
            if vector.x > 0:
                self.direction = 0
            else:
                self.direction = 1

            self.animation_controller.play_animation("run")
        else:
            self.animation_controller.play_animation("idle")
        self.collisions("horizontal")
        if vector.y != 0 and self.can_jump:
            self.can_jump = False
            self.y_speed -= self.jump_power
        
        self.y_speed += self.gravity
        self.rect.y += self.y_speed
        self.collisions("vertical")
            
    def collisions(self, dir: str):
        """Checks for collisions"""
    
        if dir == "horizontal":
            # World borders first
            if self.rect.right > self.X_LIMITS[1]:
                self.rect.right = self.X_LIMITS[1]

            if self.rect.left < self.X_LIMITS[0]:
                self.rect.left = self.X_LIMITS[0]
            
            # Obstacles
            sprite = pygame.sprite.spritecollide(self, self.obstacles, False)
            if len(sprite) > 0:
                sprite = sprite[0]
            else:
                return
            if self.direction:
                self.rect.left = sprite.rect.right
            else:
                self.rect.right = sprite.rect.left

        elif dir == "vertical":
            # World borders first
            landed = False
            if self.rect.bottom > self.Y_LIMIT:
                self.rect.bottom = self.Y_LIMIT
                landed = True

            sprite = pygame.sprite.spritecollide(self, self.obstacles, False)
            if len(sprite) > 0:
                sprite = sprite[0]
                if self.y_speed > 0:
                    self.rect.bottom = sprite.rect.top
                    landed = True
                else:
                    self.rect.top = sprite.rect.bottom
                    self.y_speed = 0

            if landed:
                if not self.can_jump and self.y_speed > 30:
                    if self.animation_controller.play_animation("land"):
                        self.play_effect("land")

                self.y_speed = 0

                self.can_jump = True            
                
    def attack(self):
        if not self.timers["attack"].active:
            self.animation_controller.play_animation("attack", True)
            self.play_effect("attack")
            self.timers["attack"].activate()

    def s_attack(self):
        if not self.timers["s_attack"].active:
            self.animation_controller.play_animation("s_attack", True)
            self.play_effect("attack")
            self.timers["s_attack"].activate()

    def play_effect(self, effect: str):
        """Plays an effect
        Parameters:
        - Effect (str): The name of the effect in the effects dict"""
        if not effect in self.active_effects:
            self.active_effects.append(effect)
            self.effects[effect].play()

    def draw_effects(self, x_offset: int):
        """Draws all active effects
        Parameters:
        - X_offset (int): The x_offset for the map drawing"""
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
                pos = [*pos]
                pos[1] += 10
                the_effect.draw(pos, self.direction)

            if not the_effect.playing:
                self.active_effects.remove(effect)


    def change_animation(self, new_animation: str):
        """Changes the current animation
        Parameters:
        - New_animation (str): The name of the new animation"""
        
        
        self.animation.reset()
        self.animation = self.animations[new_animation]
        self.current_animation = new_animation