import pygame

class AudioPlayer:
    def __init__(self):
        self.current_song = None

    def set_song(self, songname):
        self.current_song = songname
        try:
            pygame.mixer.music.load(self.current_song)
            print(f"[DEBUG] Loaded song: {self.current_song}")
        except pygame.error as e:
            print(f"[ERROR] Failed to load song: {e}")

    def play_song(self):
        if self.current_song:
            pygame.mixer.music.play()
            print(f"[DEBUG] Playing: {self.current_song}")
        else:
            print("[ERROR] No song set before calling play_song().")

    def pause_song(self):
        pygame.mixer.music.pause()
        print("[DEBUG] Song paused")

    def resume_song(self):
        pygame.mixer.music.unpause()
        print("[DEBUG] Song resumed")

    def restart_song(self):
        pygame.mixer.music.rewind()
        print("[DEBUG] Song restarted")

    def end_song(self):
        pygame.mixer.music.stop()
        print("[DEBUG] Song stopped")
        self.current_song = None

    def get_current_time(self):
        return int(pygame.mixer.music.get_pos() / 1000)

    def set_current_time(self, time):
        if self.current_song:
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(time)
            print(f"[DEBUG] Set song position to {time} sec")

    def is_playing(self):
        return pygame.mixer.music.get_busy()

def initialize():
    pygame.mixer.init()
