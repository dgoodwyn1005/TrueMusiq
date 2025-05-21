import pygame
import time

import Constants as C

from screen_properties import ScreenProperties
from Button import Button as b
from TextBox import TextBox as tb
from fileManagement import FileManager, Metadata
from SQLdata import Database

class Upload(ScreenProperties):
    def __init__(self):
        super(Upload, self).__init__()

        self.fm = FileManager()
        self.md = Metadata()
        self.db = Database()

        # Buttons
        self.buttons = [
            b("New Song", C.CHARCOAL_BLACK, C.OFF_BLACK, 100, 200, 300, 300),
            b("<--", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 100, C.SCREEN_HEIGHT - 50, 100, 50),
            b("Submit", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 225, 450, 100, 50)
        ]

        # TextBoxes
        self.textboxes = [
            tb(C.WHITE, 500, 240, 250, 50, 20),  # Title
            tb(C.WHITE, 500, 340, 250, 50, 20)   # Author
        ]

        self.song_file = None
        self.error_message = ""
        self.error_start_time = None
        self.error_duration = 2.5

    def draw(self, surface):
        scaled_bg = pygame.transform.scale(C.upload_bg, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        surface.blit(scaled_bg, scaled_bg.get_rect(center=self.screen_rect.center))

        header_label = C.HEADER_FONT.render("Upload New Music", True, C.CREAM)
        surface.blit(header_label, (C.SCREEN_WIDTH / 2 - header_label.get_width() / 2, 50))

        for button in self.buttons:
            button.draw(surface)

        for textbox in self.textboxes:
            textbox.draw(surface)

        if self.song_file:
            self.show_selected_song(surface)

        self.textbox_labels(surface)

        if self.error_start_time:
            self.draw_error(surface)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = "HOME"
            self.done = True

        for button in self.buttons:
            if button.check_pressed(self.mouse, event):
                button.pressed = False
                if button.label == "<--":
                    self.next_state = "HOME"
                    self.done = True
                elif button.label == "New Song":
                    self.song_file = self.fm.choose_file()
                    print("Selected file:", self.song_file)
                elif button.label == "Submit":
                    self.handle_submit()

        for textbox in self.textboxes:
            textbox.check_pressed(self.mouse, event)
            textbox.update_text(event)

        return super().get_event(event)

    def update(self, delta_time):
        for button in self.buttons:
            button.check_hovered(self.mouse)

        if self.error_start_time and time.time() - self.error_start_time > self.error_duration:
            self.error_start_time = None

        return super().update(delta_time)

    def show_selected_song(self, surface):
        label = self.font.render(self.song_file, True, C.CREAM)
        surface.blit(label, (C.SCREEN_WIDTH / 2 - label.get_width() / 2, 150))

    def textbox_labels(self, surface):
        title = self.font.render("Title", True, C.CREAM)
        author = self.font.render("Author", True, C.CREAM)
        surface.blit(title, (500, 200))
        surface.blit(author, (500, 300))

    def draw_error(self, surface):
        error_surface = pygame.Surface((C.SCREEN_WIDTH // 2, C.SCREEN_HEIGHT // 2))
        error_surface.fill((200, 200, 200))
        x = (C.SCREEN_WIDTH - error_surface.get_width()) // 2
        y = (C.SCREEN_HEIGHT - error_surface.get_height()) // 2
        surface.blit(error_surface, (x, y))

        text = C.FONT.render(self.error_message, True, C.BLACK)
        rect = text.get_rect(center=(x + error_surface.get_width() // 2, y + error_surface.get_height() // 2))
        surface.blit(text, rect)

    def handle_submit(self):
        title = self.textboxes[0].get_text()
        author = self.textboxes[1].get_text()

        if not self.song_file:
            self.set_error("Select a song first!")
            return

        if not title or not author:
            self.set_error("Must enter title and author!")
            return

        if self.fm.new_file(self.song_file):
            song_link = self.fm.convert_to_basename(self.song_file)
            self.md.set_selected_song(C.MUSIC_FILES + "/" + song_link)
            duration = int(self.md.get_duration())
            song = [title, author, "None", "None", song_link, duration]
            self.db.add_song(song)
            self.set_error("Success!")

    def set_error(self, message):
        self.error_message = message
        self.error_start_time = time.time()
