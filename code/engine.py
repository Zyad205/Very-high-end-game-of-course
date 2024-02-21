import pygame
from os import walk

class Animation:
    def __init__(
            self,
            folder_path: str,
            animation_speed: float,
            img_multi: int = 1,
            play_once: bool = False) -> None:
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
        self.animations = animations
        self.play_once_names = play_once_names
        self.current_animation = first_animation
        self.animation = animations[first_animation]
        self.play_animation(first_animation)

        self.animation_ended = False

        self.image = self.animation.image


    def play_animation(self, animation: str, override: bool = False) -> None:
        if self.current_animation == animation:
            return False
        
        if self.current_animation in self.play_once_names:
            if self.animation_ended or override:
                self.change_animation(animation)
                return True
        else:
            self.change_animation(animation)
            return True
                                      

    def change_animation(self, new_animation: str):
        """Changes the current animation
        Parameters:
        - New_animation (str): The name of the new animation"""
        
        self.animation.reset()
        self.animation = self.animations[new_animation]
        self.current_animation = new_animation

    def update(self):
        self.animation_ended = self.animation.update()
        self.image = self.animation.image

class Effect(Animation):
    def __init__(
            self,
            folder_path: str,
            animation_speed: float,
            img_multi: int = 1) -> None:
        """It will control the animations by you calling the update function,
        you provide the folder that has the images

        Note:
        - Retrieve current image by accessing the image attribute

        Parameters:
        - Folder_path (str): The folder the contains the animations
        - Animation_speed (float): The speed to update the images
        - Img_multi (int): A multiplier for the images size"""
        super().__init__(folder_path, animation_speed, img_multi, 1)

        self.screen = pygame.display.get_surface()

        self.playing = False
    def play(self):
        """"""
        if not self.playing:
            # do shit
            self.playing = True
            self.reset()

    def draw(self, pos, flip: bool = 0):
        """Draw the particles
        Parameters:
        - Position (tuple[int]): The coordinates for the midbottom of the animation
        - Flip (bool): The image or no"""
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

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            if self.func and self.start_time != 0:
                self.func()
            self.deactivate() 

