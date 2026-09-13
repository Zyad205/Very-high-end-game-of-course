import pygame
from engine import *
from globals import *
from debug import *
from entities import CollidableEntity

class Player(CollidableEntity):
    def __init__(self, groups, obstacles, semi_obstacles, attack_signal, x_limits=MAP_SIZE):

        # The father init func
        super().__init__(groups)

        # Animations        
        self.animations = {"idle": Animation(PLAYER_PATHS["idle"], 0.06, PLAYER_IMG_MULTI),
                           "run": Animation(PLAYER_PATHS["run"], 0.15, PLAYER_IMG_MULTI),
                           "land": Animation(PLAYER_PATHS["land"], 0.15, PLAYER_IMG_MULTI, 1),
                           "attack": Animation(PLAYER_PATHS["attack"], 0.2, PLAYER_IMG_MULTI, 1),
                           "hit": Animation(PLAYER_PATHS["hit"], 0.15, PLAYER_IMG_MULTI, 1)}
        
        self.animation_controller = AnimationController(
            self.animations,
            "idle")
 
        # Effects
        self.effects = {"land": Effect(PLAYER_PATHS["effect_land"], 0.2, PLAYER_EFFECTS_MULTI),
                        "attack": Effect(PLAYER_PATHS["effect_attack"], 0.3, PLAYER_EFFECTS_MULTI)}

        self.active_effects = []

        # Attributes
        self.rect = pygame.rect.Rect(0, 0, 42, 42)
        self.rect.midbottom = (400, 720)

        # Hitboxes
        self.hitbox = pygame.Rect(*self.rect.topleft, PLAYER_HITBOX_SIZE[0], PLAYER_HITBOX_SIZE[1])

        self.hitbox.center = self.rect.center
        self.attack_hitbox = pygame.Rect(*self.rect.topleft, PLAYER_ATTACK_HITBOX_SIZE[0], PLAYER_ATTACK_HITBOX_SIZE[1])
        self.attack_hitbox.center = self.rect.center
        

        # Obstacles
        self.obstacles = obstacles
        self.semi_obstacles = semi_obstacles

        # Attack signal
        self.attacking_signal = attack_signal

         # 1 - Left, 0 - Right
        self.direction = 0
        self.type = "player"

        # Variables for the semi collidable obstacles
        self.x_offset_platform = None
        self.platform_on = None

        # Y axis
        self.jump = False
        self.gravity = 1
        self.y_speed = 0
        self.jump_power = 21
        self.can_jump = True
        self.hit_rebounce = 0
        

        self.health = 100
        self.health_bar = StatusBar(
            100,
            100,
            "#00e1ff",
            "#ff3224",
            "#e0dec8",
            4,
            1,
            1,
            330,
            15,
            (180, 25))

        # World limits
        self.X_LIMITS = x_limits
        self.Y_LIMIT = 720

        # Timers
        self.timers = {
            "attack": Timer(500),
            "hit": Timer(200)
        }


    def update(self) -> None:
        """The logic update function"""
        self.animation_controller.update()
        self.image = pygame.transform.flip(
            self.animation_controller.image,
            flip_x=self.direction,
            flip_y=False)
    
        self.update_timers()

        # Because pygame need a sprite object to check for collision with a group of sprites not a rect
        # We copy the hitbox inside the player sprite rect then run the test and after if return its original rect

        # Yes we use it don't delete
        self.old_hitbox = self.hitbox.copy()
        temp_rect = self.rect.copy()
        self.rect = self.hitbox

        input_vector, attacked = self.input()

        self.movement(input_vector)

        if attacked:
            self.attack()

        self.rect = temp_rect.copy()
        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery
            
    def input(self) -> None:
        """Checks for all player related input and calls the movement functions"""

        keys = pygame.key.get_pressed()
        
        input_vector = pygame.math.Vector2(0, 0)
        attacked = False

        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_w]:
            input_vector.y = 1
        
        if keys[pygame.K_l]:
            attacked = True
        
        return input_vector, attacked

    def movement(self, vector: pygame.math.Vector2):
        """Moves the player according to the the input_vector

        Parameters:
        - Vector (pygame.math.Vector2): The vector taken from input"""
        
        # Applies movement based on direction of the hit
        if self.hit_rebounce:
            x_speed = 0.7
            if self.direction_when_hit:
                x_speed = -x_speed

            vector.x = x_speed


        if vector.x != 0:
            self.hitbox.x += vector.x * 5
                
            if vector.x > 0:
                self.direction = 0
            else:
                self.direction = 1

            if self.hit_rebounce:
                self.direction = not self.direction_when_hit

            self.animation_controller.play_animation("run")
            self.recalculate_semi_platform()

        else:
            self.animation_controller.play_animation("idle")
            self.platform_movement()

        self.collisions("horizontal")

        # Vertical movement
        if vector.y != 0 and self.can_jump:
            self.can_jump = False
            self.y_speed -= self.jump_power
        
        self.y_speed += self.gravity
        self.hitbox.y += self.y_speed

        
        played_animation = self.collisions("vertical")

        # VFX
        if played_animation == "land":
            if self.animation_controller.play_animation(played_animation):
                self.play_effect("land")

        if not self.hit_rebounce:            
            played_animation = self.semi_collision()

            # VFX
            if played_animation == "land":
                if self.animation_controller.play_animation(played_animation):
                    self.play_effect("land")

        if self.direction:
            self.attack_hitbox.right = self.hitbox.right
        else:
            self.attack_hitbox.left = self.hitbox.left

        self.attack_hitbox.bottom = self.hitbox.bottom
            
                    
    def attack(self):
        """Attacks"""
        if not self.timers["attack"].active:
            self.animation_controller.play_animation("attack", True)
            self.play_effect("attack")

            if self.direction:
                self.attack_hitbox.right = self.rect.right    
            else:
                self.attack_hitbox.left = self.rect.left

            self.attacking_signal("attack", self.attack_hitbox)
            self.timers["attack"].activate()

    def get_hit(self, damage: int, hitbox):  
        """Hitbox passed is of the enemy attacking"""
        
        self.health -= damage
        self.health_bar.update_stat(self.health)
        self.hit_rebounce = 2


        direction = 0 
        if hitbox.centerx - self.rect.centerx > 0:
            direction = 1 

        self.y_speed = -14

        self.direction_when_hit = direction

        self.animation_controller.play_animation("hit", True)
        
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

    def draw_bars(self, offset):
        self.health_bar.draw()
