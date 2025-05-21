import pygame
import math
import Constants as C

from screen_properties import ScreenProperties
from Button import Button as b
from InvisibleButton import InvisibleButton as ib
from TextBox import TextBox as tb
from SQLdata import Database


class Search(ScreenProperties):
    def __init__(self, current_screen, playlist_screen):
        super(Search, self).__init__()
        self.db = Database()

        self.current_screen = current_screen
        self.playlist_screen = playlist_screen

        self.song_list = []
        self.current_song_choices = []

        self.min_number = 1
        self.max_number = 1
        self.search_by = 1  # 1=Name, 2=Artist, 3=Playlist

        self.search_tb = tb(C.WHITE, 10, 10, C.SCREEN_WIDTH - 20, 30, 30)

        self.buttons = [
            b("<", C.BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 65, 75, 25, 25),
            b(">", C.BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 30, 75, 25, 25),
            b("<--", C.BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 100, C.SCREEN_HEIGHT - 50, 100, 50),
            b("N", C.BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 60, C.SCREEN_HEIGHT / 3, 40, 40),
            b("A", C.BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 60, C.SCREEN_HEIGHT / 2, 40, 40),
            b("P", C.BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 60, C.SCREEN_HEIGHT / 1.5, 40, 40)
        ]

        self.invisible_buttons = [ib(C.OFF_BLACK, 0, 0, 0, 0, 0) for _ in range(5)]
        self.playlist_buttons = [b(C.playlist_icon, C.OFF_BLACK, C.WHITE, 0, 0, 50, 0) for _ in range(5)]

    def draw(self, surface):
        scaled_bg = pygame.transform.scale(C.search_bg, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        surface.blit(scaled_bg, scaled_bg.get_rect(center=self.screen_rect.center))

        for button in self.buttons:
            button.draw(surface)

        for ibtn in self.invisible_buttons:
            ibtn.draw(surface)

        for i, pbtn in enumerate(self.playlist_buttons):
            if i < len(self.current_song_choices):
                pbtn.draw(surface)

        self.search_tb.draw(surface)
        self.button_number_label(surface)
        self.song_labels(surface)
        self.search_label(surface)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = "HOME"
            self.done = True

        for button in self.buttons:
            if button.check_pressed(self.mouse, event):
                button.pressed = False
                label = button.label
                if label == "<--":
                    self.next_state = "HOME"
                    self.done = True
                elif label == "<":
                    if self.min_number > 1:
                        self.min_number -= 1
                        self.update_song_list()
                elif label == ">":
                    if self.min_number < self.max_number:
                        self.min_number += 1
                        self.update_song_list()
                elif label == "N":
                    self.search_by = 1
                    self.update_song_list()
                elif label == "A":
                    self.search_by = 2
                    self.update_song_list()
                elif label == "P":
                    self.search_by = 3
                    self.update_song_list()

        for i, ibtn in enumerate(self.invisible_buttons):
            if ibtn.check_pressed(self.mouse, event):
                if i < len(self.current_song_choices):
                    song = self.current_song_choices[i]
                    self.current_screen.set_songs_to_play([song])
                    self.current_screen.set_current_song(song)
                    self.current_screen.play_song()
                    self.next_state = "CURRENT"
                    self.done = True

        for i, pbtn in enumerate(self.playlist_buttons):
            if pbtn.check_pressed(self.mouse, event):
                if i < len(self.current_song_choices):
                    song = self.current_song_choices[i]
                    self.playlist_screen.set_current_song(song)
                    self.next_state = "PLAYLIST"
                    self.done = True

        self.search_tb.check_pressed(self.mouse, event)
        self.search_tb.update_text(event)

        if self.search_tb.active and event.type == pygame.KEYDOWN:
            self.update_song_list()

        return super().get_event(event)

    def update(self, delta_time):
        for button in self.buttons:
            button.check_hovered(self.mouse)

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.current_song_choices):
                ibtn.check_hovered(self.mouse)

        return super().update(delta_time)

    def update_song_list(self):
        self.song_list = []
        self.current_song_choices = []
        current_name = self.search_tb.get_text().lower()

        if self.search_by == 1:
            for song in self.db.get_all_songs():
                if song[0].lower().startswith(current_name) and current_name != "":
                    self.song_list.append(song)
        elif self.search_by == 2:
            for artist in self.db.get_all_artists():
                if artist[0].lower().startswith(current_name) and current_name != "":
                    self.song_list.extend(self.db.get_songs_by_artist(artist[0]))
        elif self.search_by == 3:
            for pl in self.db.get_all_playlists():
                if pl.lower().startswith(current_name) and current_name != "":
                    self.song_list.extend(self.db.get_songs_in_playlist(pl))

        self.max_number = max(1, math.ceil(len(self.song_list) / 5))

    def song_labels(self, surface):
        split = C.SCREEN_HEIGHT / 5
        start = (self.min_number - 1) * 5
        self.current_song_choices = self.song_list[start:start + 5]

        if not self.current_song_choices:
            no_songs = C.HEADER_FONT.render("No Songs Found", True, C.CREAM)
            surface.blit(no_songs, (C.SCREEN_WIDTH / 2 - no_songs.get_width() / 2, 200))
            return

        for i, song in enumerate(self.current_song_choices):
            title = C.SUBHEADER_FONT.render(song[0] + " - ", True, C.CREAM)
            artist = C.SUBHEADER_FONT.render(song[1], True, C.CREAM)
            y = (i + 1) * (split - 20)

            surface.blit(title, (50, y))
            surface.blit(artist, (50 + title.get_width(), y))

            self.invisible_buttons[i].set_pos((50, y))
            self.invisible_buttons[i].set_width(title.get_width() + artist.get_width())
            self.invisible_buttons[i].set_height(title.get_height())

            self.playlist_buttons[i].set_pos((50 + title.get_width() + artist.get_width() + 50, y))
            self.playlist_buttons[i].set_width(50)
            self.playlist_buttons[i].set_height(title.get_height())

    def button_number_label(self, surface):
        label = self.font.render(f"{self.min_number} of {self.max_number}", True, C.CREAM)
        surface.blit(label, (C.SCREEN_WIDTH - 65, 40))

    def search_label(self, surface):
        search_modes = {1: "Searching by Name", 2: "Searching by Artist", 3: "Searching by Playlist"}
        text = C.FONT.render(search_modes.get(self.search_by, ""), True, C.CREAM)
        surface.blit(text, (C.SCREEN_WIDTH / 2 - text.get_width() / 2, C.SCREEN_HEIGHT - 40))
