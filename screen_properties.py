import pygame

import Constants as C

class ScreenProperties(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.font = C.FONT
        self.mouse = pygame.mouse.get_pos()

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

    def update(self, delta_time):
        self.mouse = pygame.mouse.get_pos()

    def draw(self, surface):
        pass