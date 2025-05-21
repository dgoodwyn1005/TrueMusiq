import pygame

import Constants as C

class InvisibleButton(object):
    def __init__(self, hover_color, x, y, width, height, transparency):
        self.hover_color = hover_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.transparency = 75
        self.pressed = False
        self.hovered = False

    def draw(self, surface):
        button_rect = (self.x, self.y, self.width, self.height)
        if self.hovered:
            temp_surface = pygame.Surface(pygame.Rect(button_rect).size, pygame.SRCALPHA)
            temp_surface.set_alpha(self.transparency)
            pygame.draw.rect(temp_surface, self.hover_color, temp_surface.get_rect())
            surface.blit(temp_surface, button_rect)

    def check_pressed(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
                if mouse_pos[1] > self.y and mouse_pos[1] <= (self.y + self.height):
                    self.pressed = True
                
        return self.pressed

    def check_hovered(self, mouse_pos):
        if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
            if mouse_pos[1] > self.y and mouse_pos[1] <= (self.y + self.height):
                self.hovered = True
            else:
                self.hovered = False
        else:
            self.hovered = False

        return self.hovered
    
    def set_pos(self, new_pos):
        self.x = new_pos[0]
        self.y = new_pos[1]

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height