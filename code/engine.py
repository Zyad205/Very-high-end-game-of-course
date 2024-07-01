import pygame
from os import walk


class Animation:
    def __init__(
            self,
            folder_path: str,
            animation_speed: float,
            img_multi: int = 1,
            play_once: bool = False):
        """It will control the animations by you calling the update function,
        you provide the folder that has the images

        Note:
        - Retrieve current image by accessing the image attribute

        Parameters:
        - Folder_path (str): The folder the contains the animations
        - Animation_speed (float): The speed to update the images
        - Img_multi (int): A multiplier for the images size
        - Play_once (bool)": Should the animation play once or play continuously"""


        # Get the images
        self.images = []
        self.load_folder(folder_path, img_multi)

        self.animation_speed = animation_speed
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.play_once = play_once

        
    def load_folder(self, path: str, img_multi) -> None:
        """Retrieves the images from the folder to self.images

        Parameters:
        - Path (str): The path to the folder
        - Img_multi (int): A multiplier for the images size"""

        for _, __, images in walk(path): # Get a list of the images
            for image_path in images: # Iterate through the images
                # Make the full path
                full_path = path + "/" + image_path
                image = pygame.image.load(full_path).convert_alpha()
                if img_multi >= 1 and isinstance(img_multi, int):
                    image = pygame.transform.scale_by(image, img_multi)
                # Append
                self.images.append(image)
        if len(self.images) == 0:
            error = f"Couldn't load images from {path}"
            raise RuntimeError(error)

    def update(self) -> bool:
        """Updates the image
        Return:
        - Bool: Returns true if play once is on and we reached last image and
        false otherwise"""
        return_value = False

        self.image_index += self.animation_speed
        if self.image_index >= len(self.images):
            self.image_index = 0

            if self.play_once:
                return_value = True

        self.image = self.images[int(self.image_index)]

        return return_value

    def reset(self) -> None:
        """Reset the animation to the first animation"""
        self.image_index = 0
        self.image = self.images[0]

class AnimationController:
    def __init__(
            self,
            animations: dict[str, Animation],
            play_once_names: list[str],
            first_animation: str):
        """The init func
        
        Parameters:
        - Animations (dict[str, Animation]): A dictionary of animations objects
        - Play_once_names (list[str]): A list of the names of the animations that
        will play once
        -First_animation (str): The name of the first loaded animation"""


        self.animations = animations
        self.play_once_names = play_once_names
        self.current_animation = first_animation
        self.animation = animations[first_animation]
        self.play_animation(first_animation)

        self.animation_ended = False

        self.image = self.animation.image


    def play_animation(self, animation: str, override: bool = False) -> None:
        """Plays a new animation if it's not currently playing and no play
        once animation is playing

        Parameters:
        - Animation (str): The name of the new animation
        - Override (bool): Should override a currently playing play once
        animation"""
        if self.current_animation == animation:
            return False
        
        if self.current_animation in self.play_once_names:
            if self.animation_ended or override:
                self.change_animation(animation)
                return True
        else:
            self.change_animation(animation)
            return True
                                      

    def change_animation(self, new_animation: str) -> None:
        """Changes the current animation
        Parameters:
        - New_animation (str): The name of the new animation"""
        
        self.animation.reset()
        self.animation = self.animations[new_animation]
        self.current_animation = new_animation

    def update(self):
        """Updates the current animation and the image attribute"""

        self.animation_ended = self.animation.update()
        self.image = self.animation.image

class Effect(Animation):
    def __init__(
            self,
            folder_path: str,
            animation_speed: float,
            img_multi: int = 1) -> None:
        """The init func

        Parameters:
        - Folder_path (str): The folder the contains the animations
        - Animation_speed (float): The speed to update the images
        - Img_multi (int): A multiplier for the images size"""

        super().__init__(folder_path, animation_speed, img_multi, 1)

        self.screen = pygame.display.get_surface()

        self.playing = False

    def play(self) -> None:
        """Starts playing the effect if it's not currently playing"""

        if not self.playing:
            # do shit
            self.playing = True
            self.reset()

    def draw(self, pos, flip: bool = 0) -> None:
        """Draw the particles

        Parameters:
        - Position (tuple[int]): The coordinates for the midbottom of the animation
        - Flip (bool): Flip the image on x axis or not"""

        if self.playing:
            rect = self.image.get_rect()

            rect.midbottom = pos
            img = pygame.transform.flip(self.image, flip, 0)
            
            self.screen.blit(img, rect)

            if self.update():
                self.playing = False


# Code author clear code
# Youtube https://www.youtube.com/@ClearCode
# Github https://github.com/clear-code-projects
# Project code taken from https://github.com/clear-code-projects/Super-Pirate-World
# If anybody reading this if you have money give some to this guy
# he deserves it
class Timer:
    def __init__(self, duration: int, func= None, repeat: bool = False):
        """The init func

        Parameters:
        - Duration (int): The duration in ms
        - Func (function): A function to be called when the timer finishes
        - Repeat (bool): Should the timer reactive after it finishes"""

        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False
        self.repeat = repeat

    def activate(self) -> None:
        """Start the timer and resets it"""
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self) -> None:
        """Stops the timer"""

        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self) -> None:
        """Updates the timer and checks if the timer has ended"""

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()

            self.deactivate() 

class StatusBar:
    def __init__(
            self, 
            max_num: int,
            current_num: int,
            active_bar_color: str,
            bg_bar_color: str,
            outline_color: str,
            draw_bg: bool,
            draw_outline: bool,
            width: int,
            height: int,
            center_pos: tuple[int]):
        """The init function
        
        Parameters:
        - Max num(int): The maximum number for the stat
        - Current num(int): The starting value for the stat
        - Active bar color(str): The active bar color in hex
        - Bg bar color(str): The background bar color in hex
        - Outline color(str): The outline color in hex
        - Draw bg(bool): Wether to draw the bg or not
        - Draw outline(bool): Wether to draw the outline or not
        - Width (int): The width of the bar
        - height (int): The height of the bar
        - Center pos(tuple[int]): The coordinates for the middle of the bar
        """
        
        # Attributes
        self.max_num = max_num
        self.current_num = current_num

        self.active_bar_color = active_bar_color
        self.bg_bar_color = bg_bar_color
        self.outline_color = outline_color

        self.draw_bg = draw_bg
        self.draw_outline = draw_outline

        self.width = width
        self.height = height
        self.center_pos = center_pos

        self.stat_width = self.width * self.current_num / self.max_num
        self.stat_width = int(self.stat_width)

        self.bg_bar = pygame.rect.Rect(0, 0, width, height)
        self.active_bar = pygame.rect.Rect(0, 0, self.stat_width, height)

        self.bg_bar.center = center_pos
        self.active_bar.topleft = self.bg_bar.topleft

        self.display = pygame.display.get_surface()

        
    def update_pos(self, new_center: tuple[int]) -> None:
        """Updates the position of the bar
        
        Parameters:
        - New center(tuple[int]): New coordinates for the center of the bar"""
        self.bg_bar.center = new_center
        self.active_bar.topleft = self.bg_bar.topleft

    def update_stat(self, new_num: int) -> None:
        """Changes the stat value and the width or progression of the active bar
        
        Parameters
        - New num(int): The new value"""
        self.current_num = new_num

        self.stat_width = self.width * self.current_num / self.max_num
        self.stat_width = int(self.stat_width)

        self.active_bar.width = self.stat_width
        self.active_bar.topleft = self.bg_bar.topleft

    def draw(self, x_offset: int = 0) -> None:
        """Draws the bar
        
        Parameters:
        - X offset(int): The x offset for the camera"""
        if self.draw_bg:
            rect = self.bg_bar.copy()
            rect.x -= x_offset
            pygame.draw.rect(self.display, self.bg_bar_color, rect)

        rect = self.active_bar.copy()
        rect.x -= x_offset
        pygame.draw.rect(self.display, self.active_bar_color, rect)

        if self.draw_outline:
            rect = self.bg_bar.copy()
            rect.x -= x_offset
            rect.x -= 2
            rect.y -= 2
            rect.width += 4
            rect.height += 4
            pygame.draw.rect(self.display, self.outline_color, rect, 2, 2)