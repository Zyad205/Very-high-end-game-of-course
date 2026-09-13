import pygame
from globals import BOLD_PIXEL_FONT

class Button:
    def __init__(self, text, x, y, width, height, normal_color, hover_color, text_color, font_size=32):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text_color = text_color
        
        # Initialize font and render text
        self.font = pygame.font.Font(BOLD_PIXEL_FONT, font_size)
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        
        self.is_hovered = False

    def draw(self, surface):
        # Change color dynamically based on hover state
        color = self.hover_color if self.is_hovered else self.normal_color
        
        # Draw button body and centered text
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        surface.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        # check if mouse coordinate is inside the button bounding box
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        # Trigger an action only if the mouse clicked down while hovering
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False
