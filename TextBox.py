import pygame
import time

import Constants as C

class TextBox(object):
    def __init__(self, color, x, y, width, height, max):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.active = False

        self.user_text = ""
        self.max = 15

    def draw(self, surface):
        box_rect = (self.x, self.y, self.width, self.height)
        text_font = C.FONT
        box_text = text_font.render(self.user_text, True, C.BLACK)
        text_pos = (self.x + 5, (self.y + self.height / 2) - box_text.get_height() / 2)

        pygame.draw.rect(surface, self.color, box_rect)
        surface.blit(box_text, text_pos)

        if self.active:
            if time.time() % 1 > 0.5:
                text_rect = box_text.get_rect(topleft=text_pos)
                cursor = pygame.Rect(text_rect.topright, (2, box_text.get_height()))
                pygame.draw.rect(surface, C.BLACK, cursor)

    def update_text(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN: 
                #Backspace 
                if event.key == pygame.K_BACKSPACE:  
                    self.user_text = self.user_text[:-1] 
                else: 
                    if len(self.user_text) < self.max:
                        self.user_text += event.unicode

    def check_pressed(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
                if mouse_pos[1] > self.y and mouse_pos[1] <= (self.y + self.height):
                    self.active = True
                else:
                    self.active = False
            else:
                self.active = False
                
        return self.active
    
    def get_text(self):
        return self.user_text