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