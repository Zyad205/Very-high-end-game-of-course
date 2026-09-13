import pygame
from globals import BOLD_PIXEL_FONT

font = pygame.font.Font(BOLD_PIXEL_FONT, 25)

class Button:
    def __init__(self, text, x, y, normal_color, hover_color, text_color, font_size=32):
        self.text = text
        self.position = (x, y)

        self.normal_color = normal_color
        self.hover_color = hover_color
        
        # Initialize font and render text
        self.rendered_text = font.render(text, False, text_color)
        self.text_rect = self.rendered_text.get_rect(topleft=self.position)
        self.text_rect.width += 15
        self.text_rect.height += 5
        
        
        self.is_hovered = False

    def draw(self, surface):
        # Change color dynamically based on hover state
        color = self.hover_color if self.is_hovered else self.normal_color
        
        # Draw button body and centered text
        pygame.draw.rect(surface, color, self.text_rect, border_radius=8)
        surface.blit(self.rendered_text, self.text_rect)

    def check_hover(self, mouse_pos):
        # check if mouse coordinate is inside the button bounding box
        self.is_hovered = self.text_rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        # Trigger an action only if the mouse clicked down while hovering
        if event.button == 1:
            if self.is_hovered:
                return True
        return False
