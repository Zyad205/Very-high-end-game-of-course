import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(info: str, x: int = 0, y: int = 0):
    """Display information on the screen to debug
    Parameters:
    - Info (str): The information need to be displayed
    - X (int): The x position for the information
    - Y (int): The Y position for the information"""

    # Get screen
    screen = pygame.display.get_surface()
    text = str(info)

    rendered_text = font.render(text, color="WHITE", antialias=False)
    rect = rendered_text.get_rect(topleft=(x,y))

    pygame.draw.rect(screen, "BLACK", rect)
    screen.blit(rendered_text, rect)