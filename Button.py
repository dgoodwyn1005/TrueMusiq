import pygame
import Constants as C

class Button:
    def __init__(self, label, color, hover_color, x, y, width, height):
        self.label = label  # Can be a string or a icon
        self.color = color
        self.hover_color = hover_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.pressed = False
        self.hovered = False

        self.is_text = self.check_if_text(label)

    def draw(self, surface):
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.hover_color if self.hovered else self.color, button_rect, border_radius=3)

        if self.is_text:
            font = C.BUTTON_FONT
            text_surface = font.render(self.label, True, C.WHITE)
            text_pos = (
                self.x + (self.width - text_surface.get_width()) / 2,
                self.y + (self.height - text_surface.get_height()) / 2
            )
            surface.blit(text_surface, text_pos)
        else:
            icon_surface = self.label
            icon_pos = (
                self.x + (self.width - icon_surface.get_width()) / 2,
                self.y + (self.height - icon_surface.get_height()) / 2
            )
            surface.blit(icon_surface, icon_pos)

    def check_pressed(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_mouse_over(mouse_pos):
                self.pressed = True
                return True
        return False

    def check_hovered(self, mouse_pos):
        self.hovered = self.is_mouse_over(mouse_pos)
        return self.hovered

    def is_mouse_over(self, mouse_pos):
        mx, my = mouse_pos
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def set_pos(self, new_pos):
        self.x, self.y = new_pos

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height

    def set_text(self, new_label):
        self.label = new_label
        self.is_text = self.check_if_text(new_label)

    def check_if_text(self, data):
        return not isinstance(data, pygame.Surface)