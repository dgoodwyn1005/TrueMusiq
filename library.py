import pygame
import math
import random

import Constants as C
from screen_properties import ScreenProperties
from Button import Button as b
from SQLdata import Database


class Library(ScreenProperties):
    def __init__(self, current_screen, individual_screen):
        super(Library, self).__init__()

        self.db = Database()
        self.current_screen = current_screen
        self.individual_screen = individual_screen

        self.min_number = 1
        self.max_number = 1
        self.first_update = False
        self.selecting = False

        self.playlist_list = []
        self.current_playlist_choices = []
        self.selected_playlist = set()

        # Buttons
        self.buttons = [
            b("<", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 65, 75, 25, 25),
            b(">", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 30, 75, 25, 25),
            b("<--", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 100, C.SCREEN_HEIGHT - 50, 100, 50),
            b("", C.CHARCOAL_BLACK, C.OFF_BLACK, 25, C.SCREEN_HEIGHT - 40, 30, 30),  # selection_mode
            b(C.play_icon, C.RED, C.OFF_BLACK, 260, C.SCREEN_HEIGHT - 60, 50, 50),
            b(C.shuffle_icon, C.DARK_ROYAL_PURPLE, C.OFF_BLACK, 340, C.SCREEN_HEIGHT - 60, 50, 50)
        ]

        self.playlist_buttons = [
            b(" ", C.CHARCOAL_BLACK, C.OFF_BLACK, 100, 50, 150, 150),
            b(" ", C.CHARCOAL_BLACK, C.OFF_BLACK, 400, 50, 150, 150),
            b(" ", C.CHARCOAL_BLACK, C.OFF_BLACK, 100, (C.SCREEN_HEIGHT / 2) - 75, 150, 150),
            b(" ", C.CHARCOAL_BLACK, C.OFF_BLACK, 400, (C.SCREEN_HEIGHT / 2) - 75, 150, 150),
            b(" ", C.CHARCOAL_BLACK, C.OFF_BLACK, 100, C.SCREEN_HEIGHT - 200, 150, 150),
            b(" ", C.CHARCOAL_BLACK, C.OFF_BLACK, 400, C.SCREEN_HEIGHT - 200, 150, 150)
        ]

    def draw(self, surface):
        scaled_bg = pygame.transform.scale(C.library_bg, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        surface.blit(scaled_bg, scaled_bg.get_rect(center=self.screen_rect.center))

        for button in self.buttons:
            button.draw(surface)

        for i, button in enumerate(self.playlist_buttons):
            if i < len(self.current_playlist_choices):
                button.draw(surface)

        # Selection label
        label = "Multiple" if self.selecting else "Single"
        text = C.FONT.render(label, True, C.CREAM)
        surface.blit(text, (10, self.buttons[3].y - 45))

        self.title(surface)
        self.button_number_label(surface)
        self.playlist_names(surface)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.first_update = False
            self.next_state = "HOME"
            self.done = True

        for button in self.buttons:
            if button.check_pressed(self.mouse, event):
                button.pressed = False
                if button.label == "<--":
                    self.next_state = "HOME"
                    self.done = True
                    self.first_update = False
                elif button.label == "<":
                    if self.min_number > 1:
                        self.min_number -= 1
                        self.update_playlists()
                elif button.label == ">":
                    if self.min_number < self.max_number:
                        self.min_number += 1
                        self.update_playlists()
                elif button == self.buttons[3]:  # selection_mode
                    self.selecting = not self.selecting
                    self.selected_playlist.clear()
                    button.color = C.GREYISH_GOLD_COLOR if self.selecting else C.CHARCOAL_BLACK
                    for pbtn in self.playlist_buttons:
                        pbtn.color = C.CHARCOAL_BLACK
                elif button == self.buttons[4]:  # play
                    self.play_selected(shuffle=False)
                elif button == self.buttons[5]:  # shuffle
                    self.play_selected(shuffle=True)

        for i, pbtn in enumerate(self.playlist_buttons):
            if i < len(self.current_playlist_choices) and pbtn.check_pressed(self.mouse, event):
                pbtn.pressed = False
                playlist = self.current_playlist_choices[i]

                if not self.selecting:
                    self.individual_screen.set_current_playlist(playlist)
                    self.next_state = "INDIVIDUAL"
                    self.done = True
                    self.first_update = False
                else:
                    if playlist in self.selected_playlist:
                        self.selected_playlist.remove(playlist)
                        pbtn.color = C.CHARCOAL_BLACK
                    else:
                        self.selected_playlist.add(playlist)
                        pbtn.color = C.GREYISH_GOLD_COLOR

        return super().get_event(event)

    def update(self, delta_time):
        if not self.first_update:
            self.update_playlists()
            self.first_update = True

        for button in self.buttons:
            button.check_hovered(self.mouse)

        for i, pbtn in enumerate(self.playlist_buttons):
            if i < len(self.current_playlist_choices):
                pbtn.check_hovered(self.mouse)

        return super().update(delta_time)

    def title(self, surface):
        for i, letter in enumerate("LIBRARY"):
            label = C.SUBHEADER_FONT.render(letter, True, C.CREAM)
            surface.blit(label, (C.SCREEN_WIDTH - 50, 150 + i * 50))

    def button_number_label(self, surface):
        text = self.font.render(f"{self.min_number} of {self.max_number}", True, C.CREAM)
        surface.blit(text, (C.SCREEN_WIDTH - 65, 40))

    def playlist_names(self, surface):
        start = (self.min_number - 1) * 6
        self.current_playlist_choices = self.playlist_list[start:start + 6]

        if not self.current_playlist_choices:
            no_text = C.HEADER_FONT.render("No Playlists Available", True, C.CREAM)
            surface.blit(no_text, (C.SCREEN_WIDTH / 2 - no_text.get_width() / 2, 300))
            return

        for i, playlist in enumerate(self.current_playlist_choices):
            self.playlist_buttons[i].set_text(playlist)

    def update_playlists(self):
        self.playlist_list = self.db.get_all_playlists()
        self.current_playlist_choices = []
        self.max_number = math.ceil(len(self.playlist_list) / 6)

    def play_selected(self, shuffle=False):
        if self.selected_playlist:
            songs = []
            for playlist in self.selected_playlist:
                songs.extend(self.db.get_songs_in_playlist(playlist))

            if shuffle:
                songs = random.sample(songs, len(songs))

            self.current_screen.set_songs_to_play(songs)
            self.current_screen.set_current_song(songs[0])
            self.current_screen.play_song()

            self.next_state = "CURRENT"
            self.done = True
