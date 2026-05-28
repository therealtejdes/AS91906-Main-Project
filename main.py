# import section
import pygame
import json
import sys
import button
from imagelist import ImageList # class extracted from the other file
from button import Button # class extracted from the other file
# all pygame modules have been activated 
pygame.init()

# important logistical values for my screen 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# usign the two values on the previous two lines of code, the screen is initialized to this
# set_mode sets the mode of the screen to the dimensions previously defined
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #avoids the usage of magic numbers

# Logistical values for my buttons
# These values remain constant for all buttons
# all buttons will be featured on the main menu
BUTTON_WIDTH = 200
BUTTON_WIDTH = 200
# positions the button in the center of the screen 
BUTTON_CENTER = 300 # 

# Values for the back button 
# This will be placed on the left hand side of my game screen
BUTTON_X = 20
BUTTON_Y = 20
BACK_BUTTON_WIDTH = 200
BACK_BUTTON_HEIGHT = 50

# Factory image 
# Purpose will be defined within the menu class
FACTORY_IMAGE_WIDTH = 200
FACTORY_IMAGE_HEIGHT = 200
FACTORY_IMAGE_COLOR = (255, 255, 255) # RGB color for white

# gameplay caption:
pygame.display.set_caption("SNAKED") #name of the game being coded
# controls the gamerate/speed of what an object does within the game play

# tuples containing the RGB colors
# purpose to group together multiple dat units into one string
WHITE = (255, 255, 255)
BLUE = (0, 0, 255) 
MAROON = (128, 0, 0) # These will be changed as the colors for my code will be different

#since Imagelist and Mysprite are already defined, no need to produce classes for them
# Menu class starts here

class Menu():
    def __innit__(self): # "self" makes sure that the class wont be touched
        # self._ values start here:
        # tracker variable defined in order to spearate the main and sub menu
        self.state = "menu"
        
        # taking from the imported image list
        # this produces the image, coded form image list
        # this image has 200 x 200p dimensions and has a color




        
    
    
    

