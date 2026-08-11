import pygame
import globals

pygame.init()
font = pygame.font.Font(None, 30)
y_offset = 0 


def debug(info: str, x: int = 0, y: int = None):
    """Display information on the screen to debug,
    will auto increment y value for correct displaying

    Parameters:
    - Info (str): The information need to be displayed
    - X (int): The x position for the information
    - Y (int): The Y position for the information"""
    global y_offset

    if not globals.DEBUGGING:
        return
    # Get screen
    screen = pygame.display.get_surface()
    text = str(info)

    # Get the correct y based on if its passed or not
    if y is None:
        y = y_offset
        y_offset += 25


    rendered_text = font.render(text, color="WHITE", antialias=False)
    rect = rendered_text.get_rect(topleft=(x,y))

    pygame.draw.rect(screen, "BLACK", rect)
    screen.blit(rendered_text, rect)
