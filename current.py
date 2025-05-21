import pygame

import Constants as C
from screen_properties import ScreenProperties
from Button import Button as b
from ProgressBar import ProgressBar as pb
from AudioPlayer import AudioPlayer
from SQLdata import Database

BACKGROUND_COLOR = C.DARK_BLUE_PURPLE
TEXT_COLOR = C.CREAM
TEXT_RECT_COLOR = C.DARK_CREAM
BUTTON_COLOR = C.BLACK
BUTTON_HOVER_COLOR = C.SLATE_GREY
PROGRESS_BASE_COLOR = C.BLACK
PROGRESS_COLOR = C.RED
PLAY_PAUSE_COLOR = C.RED

class Current(ScreenProperties):
    def __init__(self, home_screen):
        super(Current, self).__init__()
        self.home_screen = home_screen
        self.db = Database()
        self.audio = AudioPlayer()

        self.current_song = None
        self.songs_to_play = []
        self.song_index = 0

        self.started = False
        self.paused = True

        # Buttons
        self.back_button = b("<--", BUTTON_COLOR, BUTTON_HOVER_COLOR, C.SCREEN_WIDTH - 100, C.SCREEN_HEIGHT - 50, 100, 50)
        self.play_button = b(C.play_icon, PLAY_PAUSE_COLOR, BUTTON_HOVER_COLOR, 375, 450, 50, 50)
        self.pause_button = b(C.pause_icon, PLAY_PAUSE_COLOR, BUTTON_HOVER_COLOR, 375, 450, 50, 50)
        self.restart_button = b(C.back_icon, BUTTON_COLOR, BUTTON_HOVER_COLOR, 275, 450, 50, 50)
        self.next_button = b(C.next_icon, BUTTON_COLOR, BUTTON_HOVER_COLOR, 475, 450, 50, 50)

        self.buttons = [
            self.back_button,
            self.play_button,
            self.pause_button,
            self.restart_button,
            self.next_button
        ]

        self.progress = pb(PROGRESS_BASE_COLOR, PROGRESS_COLOR, 100, 300, C.SCREEN_WIDTH - 200, 15)

    def draw(self, surface):
        surface.blit(pygame.transform.scale(C.current_bg, (C.SCREEN_WIDTH, C.SCREEN_HEIGHT)), (0, 0))
        self.song_text(surface)

        for button in self.buttons:
            if button == self.pause_button and self.paused:
                continue
            if button == self.play_button and not self.paused:
                continue
            button.draw(surface)

        self.progress.draw(surface)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_state = "HOME"
            self.done = True

        for button in self.buttons:
            if (button == self.pause_button and self.paused) or (button == self.play_button and not self.paused):
                continue

            if button.check_pressed(self.mouse, event):
                button.pressed = False

                if button == self.back_button:
                    self.next_state = "HOME"
                    self.done = True

                elif button == self.play_button:
                    if not self.started:
                        self.play_song()
                    elif self.paused:
                        self.audio.resume_song()
                        print("[DEBUG] Resuming song")
                    self.paused = False
                    self.started = True

                elif button == self.pause_button:
                    if self.audio.is_playing():
                        self.audio.pause_song()
                        print("[DEBUG] Pausing song")
                        self.paused = True

                elif button == self.restart_button:
                    self.audio.restart_song()
                    self.audio.set_current_time(0)
                    self.paused = False
                    self.started = True

                elif button == self.next_button:
                    self.audio.end_song()
                    self.song_index = (self.song_index + 1) % len(self.songs_to_play)
                    self.set_current_song(self.songs_to_play[self.song_index])
                    if not self.paused:
                        self.play_song()
                    else:
                        self.started = False

        return super().get_event(event)

    def update(self, delta_time):
        self.buttons = [
            self.back_button,
            self.restart_button,
            self.next_button,
            self.pause_button if not self.paused else self.play_button
        ]

        for button in self.buttons:
            button.check_hovered(self.mouse)

        if self.current_song:
            self.progress.set_time(self.audio.get_current_time())
            self.progress.set_max_time(self.current_song[5])

        return super().update(delta_time)

    def song_text(self, surface):
        if not self.current_song:
            return

        title_label = C.HEADER_FONT.render(self.current_song[0], True, TEXT_COLOR)
        artist_label = C.SUBHEADER_FONT.render(self.current_song[1], True, TEXT_COLOR)

        playlist_label = None
        if self.current_song[2] != "None":
            playlist_label = C.FONT.render(self.current_song[2], True, TEXT_COLOR)

        surface.blit(title_label, (C.SCREEN_WIDTH / 2 - title_label.get_width() / 2, 50))
        surface.blit(artist_label, (C.SCREEN_WIDTH / 2 - artist_label.get_width() / 2, 125))

        if playlist_label:
            surface.blit(playlist_label, (C.SCREEN_WIDTH / 2 - playlist_label.get_width() / 2, 350))

        current_time = format_seconds_to_mmss(self.audio.get_current_time())
        end_time = format_seconds_to_mmss(self.current_song[5])

        duration_current_label = C.FONT.render(current_time, True, TEXT_COLOR)
        duration_end_label = C.FONT.render(end_time, True, TEXT_COLOR)

        surface.blit(duration_current_label, (100, 325))
        surface.blit(duration_end_label, (self.progress.get_x() + self.progress.get_width() - duration_end_label.get_width(), 325))

    def play_song(self):
        if not self.current_song:
            print("[ERROR] No song to play")
            return

        self.started = True
        self.paused = False

        print(f"[DEBUG] Playing song: {self.current_song[0]}")
        self.audio.set_song(C.MUSIC_FILES + "/" + self.current_song[4])
        self.audio.play_song()

        self.home_screen.add_song(self.current_song)
        if self.current_song[2] != "None":
            self.home_screen.add_playlist(self.current_song[2])

    def set_current_song(self, song_data):
        self.current_song = song_data
        self.audio.set_song(C.MUSIC_FILES + "/" + self.current_song[4])
        print(f"[DEBUG] Set current song: {self.current_song[0]}")

    def set_songs_to_play(self, songs):
        self.songs_to_play = songs
        self.song_index = 0
        if songs:
            self.set_current_song(songs[0])

def format_seconds_to_mmss(seconds):
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i" % (minutes, seconds)
