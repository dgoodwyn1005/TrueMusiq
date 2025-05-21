import pygame

import Constants as C

class ProgressBar(object):
    def __init__(self, color, progress_color, x, y, width, height):
        self.color = color
        self.progress_color = progress_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.time = 0
        self.max_time = 30

    def draw(self, surface):
        full_rect = (self.x, self.y, self.width, self.height)

        time_frac = (self.get_time() / self.get_max_time())

        duration_rect = (self.x, self.y, time_frac * self.width, self.height)

        pygame.draw.rect(surface, self.color, full_rect)
        pygame.draw.rect(surface, self.progress_color, duration_rect)

    def check_pressed(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
                if mouse_pos[1] > self.y and mouse_pos[1] <= (self.y + self.height):
                    self.pressed = True
                
        return self.pressed
    
    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time

    def get_max_time(self):
        return self.max_time

    def set_max_time(self, max_time):
        self.max_time = max_time

    def get_width(self):
        return self.width
    
    def get_x(self):
        return self.x