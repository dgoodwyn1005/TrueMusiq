import pygame

import Constants as C

from screen_properties import ScreenProperties
from Button import Button as b
from InvisibleButton import InvisibleButton as ib
from SQLdata import Database

class Home(ScreenProperties):
    def __init__(self, current_screen=None, individual_screen=None):
        super(Home, self).__init__()
        pygame.display.set_caption("TrueMusiq")
        self.show_coords = False

        self.db = Database()
        self.current_screen = current_screen  # Can be assigned later
        self.individual_screen = individual_screen  # Can be assigned later

        self.song_list = []
        self.playlist_list = []

        self.buttons = [
            b("Upload New Music", C.CHARCOAL_BLACK, C.OFF_BLACK, (C.SCREEN_WIDTH / 2) - 75, C.SCREEN_HEIGHT - 75, 150, 60),
            b("Search", C.CHARCOAL_BLACK, C.OFF_BLACK, C.SCREEN_WIDTH - 110, C.SCREEN_HEIGHT - 75, 60, 60),
            b("Library", C.CHARCOAL_BLACK, C.OFF_BLACK, 50, C.SCREEN_HEIGHT - 75, 60, 60),
            b(C.musicNote_icon, C.GREYISH_GOLD_COLOR, C.GREYISH_GOLD_COLOR, C.SCREEN_WIDTH - 75, 45, 50, 50)
        ]

        self.invisible_buttons = [ib(C.OFF_BLACK, 0, 0, 0, 0, 0) for _ in range(3)]
        self.p_invisible_buttons = [ib(C.OFF_BLACK, 0, 0, 0, 0, 0) for _ in range(3)]

    def draw(self, surface):
        scaled_bg = pygame.transform.scale(C.home_bg, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
        surface.blit(scaled_bg, scaled_bg.get_rect(center=self.screen_rect.center))

        self.text_labels(surface)

        for button in self.buttons:
            button.draw(surface)

        for ibtn in self.invisible_buttons + self.p_invisible_buttons:
            ibtn.draw(surface)

        if self.show_coords:
            self.temp_mouse_coords(surface)

        self.song_labels(surface)
        self.playlist_labels(surface)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quit = True
            elif event.key == pygame.K_m:
                self.show_coords = not self.show_coords

        for button in self.buttons:
            if button.check_pressed(self.mouse, event):
                button.pressed = False
                label = button.label

                if label == "Upload New Music":
                    self.next_state = "UPLOAD"
                    self.done = True
                elif label == "Search":
                    self.next_state = "SEARCH"
                    self.done = True
                elif label == "Library":
                    self.next_state = "LIBRARY"
                    self.done = True
                elif button == self.buttons[3]:  # current_button
                    if self.current_screen and self.current_screen.current_song:
                        self.next_state = "CURRENT"
                        self.done = True

        for idx, ibtn in enumerate(self.invisible_buttons):
            if ibtn.check_pressed(self.mouse, event):
                if idx < len(self.song_list):
                    ibtn.pressed = False
                    if self.current_screen:
                        self.current_screen.set_songs_to_play([self.song_list[idx]])
                        self.current_screen.set_current_song(self.song_list[idx])
                        self.current_screen.play_song()
                        self.next_state = "CURRENT"
                        self.done = True

        for idx, ibtn in enumerate(self.p_invisible_buttons):
            if ibtn.check_pressed(self.mouse, event):
                if idx < len(self.playlist_list):
                    ibtn.pressed = False
                    if self.individual_screen:
                        self.individual_screen.current_playlist = self.playlist_list[idx]
                        self.next_state = "INDIVIDUAL"
                        self.done = True

        return super().get_event(event)

    def update(self, delta_time):
        for button in self.buttons:
            button.check_hovered(self.mouse)

        for i, ibtn in enumerate(self.invisible_buttons):
            if i < len(self.song_list):
                ibtn.check_hovered(self.mouse)

        for i, ibtn in enumerate(self.p_invisible_buttons):
            if i < len(self.playlist_list):
                ibtn.check_hovered(self.mouse)

        return super().update(delta_time)

    def text_labels(self, surface):
        title_label = C.TRUEMUSIQ_FONT.render("TrueMusiq", True, C.CREAM)
        surface.blit(title_label, ((C.SCREEN_WIDTH - title_label.get_width()) / 2, 15))

        surface.blit(C.SUBHEADER_FONT.render("Recent Songs", True, C.CREAM), (125, C.SCREEN_HEIGHT / 3.4))
        surface.blit(C.SUBHEADER_FONT.render("Recent Playlist", True, C.CREAM), (C.SCREEN_WIDTH - 325, C.SCREEN_HEIGHT / 3.4))

    def song_labels(self, surface):
        y_gap = C.SCREEN_HEIGHT / 3
        y_offset = 100

        for idx, song in enumerate(self.song_list[:3]):
            title = C.FONT.render(f"{song[0]} - ", True, C.CREAM)
            artist = C.FONT.render(song[1], True, C.CREAM)
            y = (idx + 1) * (y_gap - 80) + y_offset
            surface.blit(title, (125, y))
            surface.blit(artist, (125 + title.get_width(), y))

            ibtn = self.invisible_buttons[idx]
            ibtn.set_pos((125, y))
            ibtn.set_width(title.get_width() + artist.get_width())
            ibtn.set_height(title.get_height())

    def playlist_labels(self, surface):
        y_gap = C.SCREEN_HEIGHT / 3
        y_offset = 100

        for idx, name in enumerate(self.playlist_list[:3]):
            label = C.FONT.render(name, True, C.CREAM)
            x, y = C.SCREEN_WIDTH - 325, (idx + 1) * (y_gap - 80) + y_offset
            surface.blit(label, (x, y))

            ibtn = self.p_invisible_buttons[idx]
            ibtn.set_pos((x, y))
            ibtn.set_width(label.get_width())
            ibtn.set_height(label.get_height())

    def temp_mouse_coords(self, surface):
        coords = self.font.render(" ".join(map(str, self.mouse)), True, C.CREAM, C.DARK_CREAM)
        surface.blit(coords, (C.SCREEN_WIDTH - 75, 25))

    def add_song(self, song):
        if song not in self.song_list:
            if len(self.song_list) >= 3:
                self.song_list.pop(0)
            self.song_list.append(song)
            print(self.song_list)

    def add_playlist(self, playlist):
        if playlist not in self.playlist_list:
            if len(self.playlist_list) >= 3:
                self.playlist_list.pop(0)
            self.playlist_list.append(playlist)
            print(self.playlist_list)
