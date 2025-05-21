import os
import pygame
pygame.init()

# CONSTANTS

# Music Files Folder
MUSIC_FILES = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) + "/uploadedMusic"

#SCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#BACKGROUNDS
home_bg = pygame.image.load("images/abstract_background.jpg")
search_bg = pygame.image.load("images/abstract_background.jpg")

playlist_bg = pygame.image.load("images/gradient_delftBlue.jpeg")

current_bg = pygame.image.load("images/gradient_auburn.jpeg")

upload_bg = pygame.image.load("images/gradient_lightGrey.jpeg")

library_bg = pygame.image.load("images/gradient_slateGrey.jpeg")
individual_bg = pygame.image.load("images/gradient_slateGrey.jpeg")

#ICONS
play_icon = pygame.image.load("images\icons\play.png")
pause_icon = pygame.image.load("images\icons\pause.png")
next_icon = pygame.image.load("images/icons/next.png")
back_icon = pygame.image.load("images/icons/back.png")
shuffle_icon = pygame.image.load("images\icons\shuffle.png")
musicNote_icon = pygame.image.load("images\icons\music_note.png")
playlist_icon = pygame.image.load("images\icons\playlist.png")

# TEXT
WHITE_FONT_COLOR = (255, 255, 255)
FONT_SIZE = 24
#FONT = pygame.font.Font(None, FONT_SIZE)
TRUEMUSIQ_FONT_SIZE = 75
TRUEMUSIQ_FONT = pygame.font.Font("fonts\TitilliumWeb-SemiBold.ttf", TRUEMUSIQ_FONT_SIZE)
FONT = pygame.font.Font("fonts\TitilliumWeb-SemiBold.ttf", FONT_SIZE)
HEADER_FONT_SIZE = 60
HEADER_FONT = pygame.font.Font("fonts\Saira_Condensed-Bold.ttf", HEADER_FONT_SIZE)
#HEADER_FONT = pygame.font.Font(None, HEADER_FONT_SIZE)
SUBHEADER_FONT_SIZE = 40
SUBHEADER_FONT = pygame.font.Font("fonts\Saira_Condensed-Bold.ttf", SUBHEADER_FONT_SIZE)
#SUBHEADER_FONT = pygame.font.Font(None, SUBHEADER_FONT_SIZE)
BUTTON_FONT_SIZE = 18
BUTTON_FONT = pygame.font.Font("fonts\TitilliumWeb-SemiBold.ttf", BUTTON_FONT_SIZE)
#BUTTON_FONT = pygame.font.Font(None, BUTTON_FONT_SIZE)

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CHARCOAL_BLACK = (33, 34, 34)
OFF_BLACK = (49, 54, 57)
DARK_ROYAL_PURPLE = (62, 51, 169)
DARK_BLUE_PURPLE = (78, 78, 148)
RED = (255, 0, 0)
CREAM = (255, 253, 208)
DARK_CREAM = (165, 144, 121)
SLATE_GREY = (112, 128, 144)
LIGHT_GREY = (211, 211, 211)
GREYISH_GOLD_COLOR = (190,175,150)