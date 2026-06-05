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

# Logistical values for scaling
#constants updated for scaling:
# target base resolution
BASE_WIDTH = 800
BASE_HEIGHT = 600 

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

# pygame clock (running)
clock = pygame.time.Clock()
#since Imagelist and Mysprite are already defined, no need to produce classes for them
# Menu class starts here

class Menu():
    def __init__(self): # "self" makes sure that the class wont be touched
        # self._ values start here:
        # tracker variable defined in order to spearate the main and sub menu
        self.state = "menu"
        # font for the title surf defined
        self.font = pygame.font.SysFont("Arial", 67)
        # scaled code
        self.scale_x = SCREEN_WIDTH / BASE_WIDTH
        self.scale_y = SCREEN_HEIGHT / BASE_HEIGHT
        # images to be scaled to screen 
        self.scale_factory_x = int(FACTORY_IMAGE_WIDTH * self.scale_x)
        self.scale_factory_y = int(FACTORY_IMAGE_HEIGHT * self.scale_y)
        # taking from the imported image list
        # this produces the image, coded form image list
        # this image has dimensions and color
        self.test_image_factory = ImageList(FACTORY_IMAGE_WIDTH, FACTORY_IMAGE_HEIGHT, FACTORY_IMAGE_COLOR) # since red has been defined, name can just be stated
        # coordinates of the defined sprite that will be taken from mysprite
        # the test image will extract this from the image list 
        self.sprite = MySprite(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.test_image_factory)
        self.sprite_group = pygame.sprite.Group(self.sprite)
        # theis makes importing/exporting and drawing the sprite much easier 

        # list for main buttons
        
        start_button = Button(int(BUTTON_CENTER * self.scale_x), 
                   # the center dimension is now scaled
                   int(200 * self.scale_y), 
                   # width of the "START" button is now scaled to the screens width
                   int(BUTTON_WIDTH * self.scale_y),
                   # height of the "START" button is now scaled to the screens heght
                   int(BUTTON_HEIGHT * self.scale_x), 
                   "START"),

        # process repeated for other buttons
            # High score button
        high_score_button = Button(int(BUTTON_CENTER * self.scale_x),
                   # center dimension of the "High Score" button is now scaled  
                   int(280 * self.scale_y), 
                   int(BUTTON_WIDTH * self.scale_x),
                   int(BUTTON_HEIGHT * self.scale_y), 
                   "HIGH_SCORE")

            # Settings Button
        settings_button = Button(int(BUTTON_CENTER * self.scale_x), 
                   int(360 * self.scale_y), 
                   int(BUTTON_WIDTH * self.scale_x), 
                   int(BUTTON_HEIGHT * self.scale_y), 
                   "SETTINGS")
        
        # the lambda code is an incline shortcut function
        # when the button is pressed (mentioned in button class), its call back is triggered
        start_button.action = lambda: self.set_state("start")
        high_score_button.action = lambda: self.set_state("high_score")
        settings_button.action = lambda: self.set_state("settings")

        # list of buttons to be redifined
        self.buttons = [ start_button, high_score_button, settings_button]
      
        # The back button, for returning back to home menu
        # adds the width 
        # A back button for the sub-screens
        # also to be sclaled
        self.escape = Button(int(BUTTON_X * self.scale_x), 
        int(BUTTON_Y * self.scale_y), 
        int(BACK_BUTTON_WIDTH * self.scale_x), 
        int(BACK_BUTTON_HEIGHT * self.scale_y),
        "ESC" )

        self.escape.action = lambda: self.set_state("menu")
        # returns to menu


    def set_state(self, new_state):
        # updates the current screen variable when called by either button press
        self.state = new_state

    # definition handles incoming inputs, in this case if/when the buttons are pressed
    def handle_events(self, event):
        # click event will be passed down through all three main buttons
        if self.state == "menu":
            for button in self.buttons:
                button.mouse_click(event)
        # the click will only be passed down to the back button
        else:
            self.back_button.mouse_click(event)

 # beggining of running the calculations
    # mouse calculations are run
    def update(self): # constants within the definition defined. 
        mouse_pos = pygame.mouse.get_pos() #with the usage of pygame module. finds the x and y coordinates of mouse
        # if on main menu, the 3 buttons will change colors if mouse is hovering over them
        if self.state == "menu":
            for button in self.buttons:
                button.mouse_move(mouse_pos)
        else:
            self.back_button.mouse_move(mouse_pos)
            # If hovered over "start", the mysprite instance is updated
            if self.state == "start":
                self.sprite_group.update() # mysprite updated using the group function

    # Screen Grpahics rendering definiton
    def draw(self, surface):
        # surface.fill controls the canvas of the screen 
        surface.fill(MAROON) #paints the entire canvas in dark grey
        
        # font/blit loop
        # If the main menu has been opened
        if self.state == "menu":
            # "main menu string has become an image suface"
            # this will be the title that has been drawn above gameplay 
            title_surf = self.font.render("SNAKED", True, WHITE)
            # "screen.blit" copies the rendered text onto the center of the screen
            surface.blit(title_surf, (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, 100)) #screen width divided by two
           # the class "button" that has been mentioned in the self.button list
            for button in self.buttons:
                # arranges to draw the three buttons on the screen 
                # this is done by the .draw() function
                button.draw(surface)
                
        # if the menu state switches to the "start" screen:
        elif self.state == "start":
            # Once "START" is clicked, this condition becomes true
            # this initializes the next four lines of code
            # this will be the title that has been drawn above
            title_surf = pygame.font.render("SNAKED", True, WHITE) # font engine converts the text "SNAKED" into an image surface
            # blit takes the defined title_surf and puts it on the main window canvas
            # the coordinates specifies 200 pixels from the top left 
            # AND the 25 pixels downwards
            surface.blit(title_surf, (200, 25))
            # sprites postion is updated/viewed
            self.sprite_group.draw(surface)
            # draw method for the back button
            # using the back buttons coordinates, the background rectangle is rendered
            # #Back to menu text is overlayed on the screen"
            # the user can escape the screen and return to the main menu
            self.back_button.draw(surface)

        # process is repeated for the other buttons

        # if the user switches the menu state to the "High_Score" screen    
        elif self.state == "high_score":
            title_surf = self.font.render("CURRENT USER HIGH SCORE", True, WHITE) #font engine converts the text into an image surface
            surface.blit(title_surf, (200, 25))
            self.sprite_group.draw(surface)
            self.back_button.draw(surface)

        # if the user switches menu state to the "Settings" screen    
        elif self.state == "settings":
            title_surf = pygame.font.render("USER SETTINGS", True, WHITE)
            surface.blit(title_surf, (200, 25))
            self.sprite_group.draw(surface)
            self.back_button.draw(surface)
# class ends here

# The main loop for the menu starts here
# this is not apart of the class
menu = Menu()
# boolian control variable establishing 
# initates the main game loop keeping the application open
running = True
while running:
    for event in pygame.event.get():
        # if the close box is clicked on the window
        if event.type == pygame.QUIT:
            # the running control is false
            running = False
        
        menu.mouse_click(event)
    # system loop tick components in order are executed
    menu.update()
    # once updated, the required coordinates will be plotted to surface canvas frame
    menu.draw(screen)

    # the flip function swaps the hidden drawn layer to the visible screen layer
    # coded to show the now updated graphics of the screen 
    pygame.display.flip()
    # execution is paused briefly as the screen is set to 60 frames per second
    clock.tick(60)

# signals the end of all pygame modules
pygame.quit()
# ensures that the game closes down without freezzing 
sys.exit()




        
    
    
    

