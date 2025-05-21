import pygame

import Constants as C

class PopUp(object):
    def __init__(self, text, color, width, height):
        self.text = text
        self.color = color
        self.width = width
        self.height = height

    def draw_popup(self, surface):
        popup_rect = ((C.SCREEN_WIDTH / 2) - self.width, (C.SCREEN_HEIGHT / 2) - self.height, self.width, self.height)

        popup_font = C.FONT
        popup_text = popup_font.render(self.text, True, self.color)
        popup_text_pos = (popup_rect[0] - popup_text.get_width() / 2, (popup_rect[1] + self.height / 2)
                     - popup_text.get_height() / 2)
        surface.blit(popup_text, popup_text_pos)

    def check_pressed(self, mouse_pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_pos[0] >= self.x and mouse_pos[0] <= (self.x + self.width):
                if mouse_pos[1] > self.y and mouse_pos[1] <= (self.y + self.height):
                    del self
    
    def __del__(self):
         print(f"Object {self.name} is being garbage collected")
