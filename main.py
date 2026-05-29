# import section
import pygame
import time
import json
import sys
import button
from imagelist import ImageList # class extracted from the other file
from mysprite import MySprite # class extracted from other file 
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
BUTTON_HEIGHT= 200
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
        self.test_image_factory = ImageList(FACTORY_IMAGE_WIDTH, FACTORY_IMAGE_HEIGHT, FACTORY_IMAGE_COLOR) # since red has been defined, name can just be stated
        # coordinates of the defined sprite that will be taken from mysprite
        # the test image will extract this from the image list 
        self.sprite = MySprite(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.test_image_factory)
        self.sprite_group = pygame.sprite.Group(self.sprite)
        # the sprte has been put into a container groups
        # theis makes importing/exporting and drawing the sprite much easier 

        # the definition structure for my three buttons
        # My code will have three distinct buttons
        # the magic number values will be swapped out with the previously defined values
        self.buttons = [
            Button("START", BUTTON_CENTER, 200, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: self.set_state("start")),
            Button("HIGH SCORE", BUTTON_CENTER, 280, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: self.set_state("high_score")),
            Button("SETTINGS", BUTTON_CENTER, 360, BUTTON_WIDTH, BUTTON_HEIGHT, lambda: self.set_state("settings"))
        ]
        # the lambda code is an incline shortcut function
        # when the button is pressed (mentioned in button class), its call back is triggered and 
        # self_set_state runs as it's new string
        # a separate button will be created in order to return back to the menu

        # The back button, for returning back to home menu
        # The code for this will follow the same structure as previous three buttons 
        # A back button for the sub-screens
        self.back_button = Button("Back to Menu", BUTTON_X, BUTTON_Y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT lambda: self.set_state("menu"))
        # usage of magic numebers avoided


    def set_state(self, new_state):
        # updates the current screen variable when called by either button press
        self.state = new_state

    # This definition handles incoming inputs, in this case if/when the buttons are pressed
    def handle_events(self, event):
        # click event will be passed down through all three main buttons
        if self.state == "menu":
            for button in self.buttons:
                button.handle_event(event)
        # the click will only be passed down to the back button
        else:
            self.back_button.handle_event(event)




        
    
    
    

