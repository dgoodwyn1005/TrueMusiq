import pygame
import math

import Constants as C
from screen_properties import ScreenProperties
from Button import Button as b
from InvisibleButton import InvisibleButton as ib
from TextBox import TextBox as tb
from SQLdata import Database

class Playlist(ScreenProperties):
    def __init__(self):
        super(Playlist, self).__init__()
        self.db = Database()

        self.current_song = None
        self.playlist_list = []
        self.current_playlist_choices = []

        self.min_number = 1
        self.max_number = 1

        self.buttons = [
            b("<", C.BLACK, C.SLATE_GREY, C.SCREEN_WIDTH - 65, 375, 25, 25),
            b(">", C.BLACK, C.SLATE_GREY, C.SCREEN_WIDTH - 30, 375, 25, 25),
            b("Submit", C.BLACK, C.SLATE_GREY, C.SCREEN_WIDTH - 200, 250, 100, 50),
            b("<--", C.BLACK, C.SLATE_GREY, C.SCREEN_WIDTH - 100, C.SCREEN_HEIGHT - 50, 100, 50)
        ]

        self.invisible_buttons = [ib(C.SLATE_GREY, 0, 0, 0, 0, 0) for _ in range(3)]
        self.textboxes = [tb(C.WHITE, 100, 200, C.SCREEN_WIDTH - 200, 30, 20)]

        self.update_playlist_list()

    def draw(self, surface):
        scaled_bg = pygame.transform.scale(C.playlist_bg, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        surface.blit(scaled_bg, scaled_bg.get_rect(center=self.screen_rect.center))

        for button in self.buttons:
            button.draw(surface)

        for textbox in self.textboxes:
            textbox.draw(surface)

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.current_playlist_choices):
                ibtn.draw(surface)

        self.song_text(surface)
        self.create_playlist_text(surface)
        self.playlist_labels(surface)
        self.button_number_label(surface)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = "HOME"
            self.done = True

        for button in self.buttons:
            if button.check_pressed(self.mouse, event):
                button.pressed = False
                match button.label:
                    case "<--":
                        self.next_state = "HOME"
                        self.done = True
                    case "Submit":
                        self.handle_submit()
                    case "<":
                        if self.min_number > 1:
                            self.min_number -= 1
                            self.update_playlist_list()
                    case ">":
                        if self.min_number < self.max_number:
                            self.min_number += 1
                            self.update_playlist_list()

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.current_playlist_choices) and ibtn.check_pressed(self.mouse, event):
                ibtn.pressed = False
                playlist_name = self.current_playlist_choices[i]
                if self.current_song and self.current_song[2] != playlist_name:
                    self.db.add_to_playlist(playlist_name, self.current_song[0], self.current_song[1])
                    print("Added to playlist:", playlist_name)
                    self.update_playlist_list()
                else:
                    print("Already in playlist:", playlist_name)

        for textbox in self.textboxes:
            textbox.check_pressed(self.mouse, event)
            textbox.update_text(event)

        return super().get_event(event)

    def update(self, delta_time):
        for button in self.buttons:
            button.check_hovered(self.mouse)

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.current_playlist_choices):
                ibtn.check_hovered(self.mouse)

        return super().update(delta_time)

    def song_text(self, surface):
        if self.current_song:
            title = C.HEADER_FONT.render(self.current_song[0], True, C.CREAM)
            artist = C.SUBHEADER_FONT.render(self.current_song[1], True, C.CREAM)

            surface.blit(title, (C.SCREEN_WIDTH / 2 - title.get_width() / 2, 20))
            surface.blit(artist, (C.SCREEN_WIDTH / 2 - artist.get_width() / 2, 85))

    def create_playlist_text(self, surface):
        text = C.FONT.render("Enter New Playlist Name", True, C.CREAM)
        surface.blit(text, (C.SCREEN_WIDTH / 2 - text.get_width() / 2, 165))

    def playlist_labels(self, surface):
        split = (C.SCREEN_HEIGHT / 2) / 3
        start = (self.min_number - 1) * 3
        extra_distance = 300

        self.current_playlist_choices = self.playlist_list[start:start + 3]

        if not self.current_playlist_choices:
            no_playlists = C.HEADER_FONT.render("No Playlist Found", True, C.CREAM)
            surface.blit(no_playlists, (C.SCREEN_WIDTH / 2 - no_playlists.get_width() / 2, 400))
            return

        for i, name in enumerate(self.current_playlist_choices):
            label = C.SUBHEADER_FONT.render(name, True, C.CREAM)
            y = ((i + 1) * (split - 20)) + extra_distance
            surface.blit(label, (100, y))

            ibtn = self.invisible_buttons[i]
            ibtn.set_pos((100, y))
            ibtn.set_width(label.get_width())
            ibtn.set_height(label.get_height())

    def button_number_label(self, surface):
        label = self.font.render(f"{self.min_number} of {self.max_number}", True, C.CREAM)
        surface.blit(label, (C.SCREEN_WIDTH - 62, 340))

    def update_playlist_list(self):
        self.playlist_list = self.db.get_all_playlists()
        self.max_number = max(1, math.ceil(len(self.playlist_list) / 3))
        self.current_playlist_choices = []

    def handle_submit(self):
        text = self.textboxes[0].get_text().strip()
        if not text or text in self.playlist_list:
            print("Must enter a unique playlist name.")
            return

        if self.current_song and self.current_song[2] != text:
            self.db.add_to_playlist(text, self.current_song[0], self.current_song[1])
            print("Created and added to new playlist:", text)
            self.update_playlist_list()

    def set_current_song(self, song_data):
        self.current_song = song_data
        self.min_number = 1
        self.update_playlist_list()
