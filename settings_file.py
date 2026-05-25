# importing key functions
import pygame
import sys
from imagelist import ImageList
from mysprite import MySprite
import json

# setting up the window for my settings code (testing)
# Logical resolutions defined
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
#menu background colour
background_color = pygame.color.Color(37, 37, 37)
