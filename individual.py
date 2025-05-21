import pygame
import math
import random

import Constants as C
from screen_properties import ScreenProperties
from Button import Button as b
from InvisibleButton import InvisibleButton as ib
from SQLdata import Database

class Individual(ScreenProperties):
    def __init__(self, current_screen):
        super(Individual, self).__init__()
        self.db = Database()
        self.current_screen = current_screen

        self.current_playlist = None
        self.song_list = []
        self.current_song_choices = []

        self.min_number = 1
        self.max_number = 1

        self.buttons = [
            b("<", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 65, 75, 25, 25),
            b(">", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 30, 75, 25, 25),
            b("<--", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 100, C.SCREEN_HEIGHT - 50, 100, 50),
            b(C.play_icon, C.DARK_BLUE_PURPLE, C.OFF_BLACK, (C.SCREEN_WIDTH / 2) - 75, C.SCREEN_HEIGHT - 100, 50, 50),
            b(C.shuffle_icon, C.DARK_ROYAL_PURPLE, C.OFF_BLACK, (C.SCREEN_WIDTH / 2) + 25, C.SCREEN_HEIGHT - 100, 50, 50)
        ]

        self.invisible_buttons = [ib(C.OFF_BLACK, 0, 0, 0, 0, 0) for _ in range(8)]

    def draw(self, surface):
        scaled_bg = pygame.transform.scale(C.individual_bg, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        surface.blit(scaled_bg, scaled_bg.get_rect(center=self.screen_rect.center))

        for button in self.buttons:
            button.draw(surface)

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.current_song_choices):
                ibtn.draw(surface)

        self.button_number_label(surface)
        self.playlist_label(surface)
        self.song_labels(surface)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = "HOME"
            self.done = True

        for button in self.buttons:
            if button.check_pressed(self.mouse, event):
                button.pressed = False
                if button.label == "<--":
                    self.next_state = "LIBRARY"
                    self.done = True
                elif button.label == "<":
                    if self.min_number > 1:
                        self.min_number -= 1
                        self.update_song_list()
                elif button.label == ">":
                    if self.min_number < self.max_number:
                        self.min_number += 1
                        self.update_song_list()
                elif button == self.buttons[3]:  # play
                    self.play_songs(self.song_list, shuffle=False)
                elif button == self.buttons[4]:  # shuffle
                    self.play_songs(self.song_list, shuffle=True)

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.current_song_choices) and ibtn.check_pressed(self.mouse, event):
                ibtn.pressed = False
                self.play_songs([self.current_song_choices[i]])

        return super().get_event(event)

    def update(self, delta_time):
        for button in self.buttons:
            button.check_hovered(self.mouse)

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.current_song_choices):
                ibtn.check_hovered(self.mouse)

        return super().update(delta_time)

    def playlist_label(self, surface):
        if self.current_playlist:
            label = C.HEADER_FONT.render(self.current_playlist, True, C.CREAM)
            surface.blit(label, (C.SCREEN_WIDTH / 2 - label.get_width() / 2, 15))

    def song_labels(self, surface):
        split = C.SCREEN_HEIGHT / 8
        start = (self.min_number - 1) * 8
        extra_y = 75

        ordered = self.order_song_list(self.song_list)
        self.current_song_choices = ordered[start:start + 8]

        for i, song in enumerate(self.current_song_choices):
            y = (i + 1) * (split - 20) + extra_y
            spot = C.FONT.render(str(song[3]), True, C.CREAM)
            title = C.FONT.render(f"{song[0]} - ", True, C.CREAM)
            author = C.FONT.render(song[1], True, C.CREAM)
            duration = C.FONT.render(self.format_seconds(song[5]), True, C.CREAM)

            surface.blit(spot, (15, y))
            surface.blit(title, (50, y))
            surface.blit(author, (50 + title.get_width(), y))
            surface.blit(duration, (125 + title.get_width() + author.get_width(), y))

            ibtn = self.invisible_buttons[i]
            ibtn.set_pos((50, y))
            ibtn.set_width(title.get_width() + author.get_width())
            ibtn.set_height(title.get_height())

    def button_number_label(self, surface):
        label = self.font.render(f"{self.min_number} of {self.max_number}", True, C.CREAM)
        surface.blit(label, (C.SCREEN_WIDTH - 65, 40))

    def update_song_list(self):
        if self.current_playlist:
            self.db.reorder_playlist_spots(self.current_playlist)
            self.song_list = self.db.get_songs_in_playlist(self.current_playlist)
            self.max_number = max(1, math.ceil(len(self.song_list) / 8))

    def order_song_list(self, songs):
        return sorted(songs, key=lambda song: song[3])  # sort by playlist spot

    def format_seconds(self, seconds):
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02}:{seconds:02}"

    def play_songs(self, songs, shuffle=False):
        if not songs:
            return
        playlist = random.sample(songs, len(songs)) if shuffle else songs
        self.current_screen.set_songs_to_play(playlist)
        self.current_screen.set_current_song(playlist[0])
        self.current_screen.play_song()
        self.next_state = "CURRENT"
        self.done = True

    def set_current_playlist(self, playlist_name):
        self.current_playlist = playlist_name
        self.min_number = 1
        self.update_song_list()
