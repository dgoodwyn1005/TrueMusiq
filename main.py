import sys
import pygame

import Constants as C
import AudioPlayer

from engine import Engine
from home import Home
from upload import Upload
from search import Search
from library import Library
from individual import Individual
from current import Current
from playlist import Playlist

pygame.init()
AudioPlayer.initialize()

window = pygame.display.set_mode((C.SCREEN_WIDTH, C.SCREEN_HEIGHT))
pygame.display.set_caption("TrueMusiq")

current_screen = None
individual_screen = None
home_screen = None

playlist_screen = Playlist()
upload_screen = Upload()

current_screen = Current(None)
individual_screen = Individual(current_screen)
home_screen = Home(current_screen, individual_screen)

current_screen.home_screen = home_screen

library_screen = Library(current_screen, individual_screen)
search_screen = Search(current_screen, playlist_screen)

screens = {
    "HOME": home_screen,
    "UPLOAD": Upload(),
    "SEARCH": search_screen,
    "LIBRARY": library_screen,
    "INDIVIDUAL": individual_screen,
    "CURRENT": current_screen,
    "PLAYLIST": playlist_screen
}

application = Engine(window, screens, "HOME")
application.run()

pygame.quit()
sys.exit()
