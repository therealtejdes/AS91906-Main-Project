# import section
import pygame
import time
import json
import sys
import button
import random # for the food 
from os.path import exists
from imagelist import ImageList # class extracted from the other file
from mysprite import MySprite # class extracted from other file 
from button import Button # class extracted from the other file
# all pygame modules have been activated 
pygame.init()

# important logistical values for my screen 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE) #avoids the usage of magic numbers

# Logistical values for scaling

SCALED_WIDTH = 800
SCALED_HEIGHT = 600 

# Logistical values for my buttons
# These values remain constant for all buttons
# all buttons will be featured on the main menu
BUTTON_WIDTH = 200
BUTTON_HEIGHT= 100
# positions the button in the center of the screen 
BUTTON_CENTER = 300 # 

# Values for the back button 
# placed on the left hand side of game screen
BUTTON_X = 20
BUTTON_Y = 20
BACK_BUTTON_WIDTH = 200
BACK_BUTTON_HEIGHT = 50
BACK_BUTTON_PADDING = 20

# Purpose will be defined within the menu class

MENU_FONT_SIZE = 100

MESSAGE_FONT = pygame.font.SysFont("Arial", 50)

SETTINGS_SCALE_INTEGER = 460
HIGH_SCORE_SCALE_INTEGER = 380
START_SCALE_INTEGER = 300
DRAWN_START_SCALE_INTEGERR = 25
DRAWN_HIGH_SCORE_SCALE_INTEGERR = 25
DRAWN_SETTING_SCALE_INTEGERR = 25
# convert alpha allows for the image to be bplaced upon much easier
CHECKERBOARD = pygame.image.load("CHECKERBOARD.png").convert_alpha()
TILESIZE_X = 16 # in relation to make the snake move
TILESIZE_Y = 16

# gameplay caption:
pygame.display.set_caption("SNAKED, By Tej Desai") 

# tuples containing the RGB colors
# purpose to group together multiple dat units into one string
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255) 
MAROON = (128, 0, 0) # These will be changed as the colors for my code will be different
GOLD = (255, 215, 0)
NAVY_BLUE = (0, 0, 128)

# pygame clock (running)
clock = pygame.time.Clock()

#since Imagelist and Mysprite are already defined, in multiple other files
# Menu class starts here

# food class
#class Token():

# snake class 
class Snake():
    # snake movement variables
    HEAD = 0
    TAIL = -1
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    VECTOR = [(0,-1), (1,0), (0,1), (-1,0)] # direction for snakes novements
    
    def __init__ (self,screen, x, y, direction = UP):
        self._x = x
        self._y = y
        self._direction = direction
        self._screen = screen
        self._color = WHITE
        self._length = 3
        self.snake_size = 20
        self._move_speed = 0.10
        self._seg_list = []
        self._head_image = ImageList("images/snake_head", TILESIZE_X, TILESIZE_Y, WHITE)# the tilesize is required because its scales the image
        self._tail_image = ImageList("image/snake_tail", TILESIZE_X, TILESIZE_Y, WHITE)
        self._next_move = time.time() + self._move_speed # using the pythons time function into the speed
        self.reset()


    # this is the definitoin 
    def reset(self):
        self._seg_list = [] # snakes head into a list
        for i in range (self._length): # length of the snake repeats
            component_x = self._x - (i * Snake.VECTOR[self._direction][0] * TILESIZE_X) # grabs the vector value up (0)
            component_y = self._y -(i * Snake.VECTOR[self._direction][1] * TILESIZE_Y) # grabs the vector value up (-1)
            img_show = self._head_image if i == 0 else self._tail_image
            # this draws the tail and head of the snake using the scaling
            # a "mysprite" object
            sprite_show = MySprite(component_x, component_y, TILESIZE_X, TILESIZE_Y, img_show,self._screen) # screen is passed first liek its in the innit function
            # the sprite seg list is empty so: 
            self._seg_list.append(sprite_show) #


    def direction(self, changing_dir):
        movements = {
            Snake.UP: Snake.DOWN, # if its snake up, then snake down should be deactivated
            Snake.DOWN: Snake.UP, # 
            Snake.RIGHT: Snake.LEFT,
            Snake.LEFT: Snake.RIGHT
            }
        if changing_dir != movements[self._direction]: # if the movement is true
             # if the movements are being checked, then the function is passed
            self._direction = changing_dir

    def update_position(self):
     if time.time() > self._next_move:
            self._next_move = time.time() + self._move_speed
            updated_x = self._seg_list[0].x +(Snake.VECTOR[self._direction][0] * TILESIZE_X) # snake taken from the list is drawn to the vector notation
            updated_y = self._seg_list[0].y +(Snake.VECTOR[self._direction][1] * TILESIZE_Y) 
            respawned_head = MySprite(updated_x, updated_y, TILESIZE_X,TILESIZE_Y,self._head_image, self._screen) # the updated head
            self._seg_list.insert(0, respawned_head)

       # removes the tail 
            if len(self._seg_list) > 1:
                self._seg_list[1]._images =self._tail_image
            if len(self._seg_list) > self._length:
                self._seg_list.pop()
          
    def check_collision(self): #definition that functions for if/when the snake hits the wall
        if not self._seg_list:
            return False
        snake_head = self._seg_list[0]
        # if the coordinates of the snakes head exceed the value of the screens width of s
        if snake_head.x < 0 or snake_head.x>=SCREEN_WIDTH or snake_head.y<0 or snake_head.y>=SCREEN_HEIGHT:
            return True

        for component in self._seg_list[1:]:
            if snake_head.x == component.x and snake_head.y == component.y:
                return True
        return False
    def draw(self):
        for component in self._seg_list:
            component.draw()


class Menu():
    def __init__(self): # "self" makes sure that the class wont be touched
        # self._ values start here:
        # tracker variable defined in order to spearate the main and sub menu
        self.state = "menu"
        # font for the title surf defined
        self.font = pygame.font.SysFont("Sans New Roman", MENU_FONT_SIZE)
        # scaled code
        self.scale_x = SCREEN_WIDTH / SCALED_WIDTH
        self.scale_y = SCREEN_HEIGHT / SCALED_HEIGHT
        # images to be scaled to screen 

        # list for main buttons
        
        start_button = Button("START",int(BUTTON_CENTER * self.scale_x), 
                   # the center dimension is now scaled
                   int(START_SCALE_INTEGER * self.scale_y), 
                   # width of the "START" button is now scaled to the screens width
                   int(BUTTON_WIDTH * self.scale_x),
                   # height of the "START" button is now scaled to the screens heght
                   int(BUTTON_HEIGHT * self.scale_y))

        # process repeated for other buttons
            # High score button
            # the value of scale x = 800/600 = 1.33
            # the values of scale y = 600/600 = 1
            # the buttons are being scaled 1.33w and 1h
        high_score_button = Button("HIGH SCORE", int(BUTTON_CENTER * self.scale_x),
                   # center dimension of the "High Score" button is now scaled  
                   int(HIGH_SCORE_SCALE_INTEGER * self.scale_y), 
                   int(BUTTON_WIDTH * self.scale_x),
                   int(BUTTON_HEIGHT * self.scale_y))

            # Settings Button
        settings_button = Button("SETTINGS", int(BUTTON_CENTER * self.scale_x), 
                   int(SETTINGS_SCALE_INTEGER * self.scale_y), 
                   int(BUTTON_WIDTH * self.scale_x), 
                   int(BUTTON_HEIGHT * self.scale_y))
        
        # the lambda code is an inline shortcut function
        # this takes in a number of multiple arguements but only has one expression
        start_button.action = lambda: self.set_state("start")
        high_score_button.action = lambda: self.set_state("high_score")
        settings_button.action = lambda: self.set_state("settings")

        # list of buttons to be redifined
        self.buttons = [ start_button, high_score_button, settings_button]
      
        # The back button, for returning back to home menu
        # adds the width 
        # A back button for the sub-screens
        
        Escape_x = int(SCREEN_WIDTH - (BACK_BUTTON_WIDTH * self.scale_x) - (BACK_BUTTON_PADDING * self.scale_x))
        Escape_y = int(BUTTON_Y * self.scale_y) 

        # values for the back button:
        self.back_button = Button("ESC", Escape_x, Escape_y,
        int(BACK_BUTTON_WIDTH * self.scale_x), 
        int(BACK_BUTTON_HEIGHT * self.scale_y))


        self.back_button.action = lambda: self.set_state("menu")
        # returns to menu

    def set_state(self, new_state):
        # updates the current screen variable when called by either button press
        self.state = new_state
        if new_state == "start":
                global Snake_sprite
                Snake_sprite = Snake(screen, 400, 300) # part of the screen where the snake will appear

    # definition handles incoming inputs, in this case if/when the buttons are pressed
    def handle_events(self, event):
        # click event will be passed down through all three main buttons
        if self.state == "menu":
            for button in self.buttons:
                button.mouse_click(event)
        # the click will only be passed down to the back button
        else:
            self.back_button.mouse_click(event)

    def mouse_click(self, w, h):
        global screen, SCREEN_WIDTH, SCREEN_HEIGHT
        # variables defined to letters
        SCREEN_WIDTH, SCREEN_HEIGHT = w, h
        # screen displays new scaled width of the code
        self.scale_x = SCREEN_WIDTH / SCALED_WIDTH
        self.scale_y = SCREEN_HEIGHT / SCALED_HEIGHT
        
        self.__init__()

 # beggining of running the calculations
    # mouse calculations are run
    def update(self): # constants within the definition defined. 
        mouse_pos = pygame.mouse.get_pos() #with the usage of pygame module. finds the x and y coordinates of mouse
        mx, my = mouse_pos
        # if on main menu, the 3 buttons will change colors if mouse is hovering over them
        if self.state == "menu":
            for button in self.buttons:
                button.mouse_move(mx, my)
        else:
            self.back_button.mouse_move(mx, my) # so that the escape button can be progressed.
        

    # definiton for drawing the buttons
    def draw(self, surface):
        surface.fill(BLACK) #paints the entire canvas in Black
        scaled_font = int(67 * self.scale_y)
        current_font = pygame.font.SysFont("Sans New Roman", max(12, scaled_font))
        # font/blit loop
        # If the main menu has been opened
        if self.state == "menu":
            # this will be the title that has been drawn above gameplay 
            # render means to put the text on to the surface of the screen 
            game_title = current_font.render("SNAKED", True, NAVY_BLUE)
            # "screen.blit" copies the rendered text onto the center of the screen
            surface.blit(game_title, (SCREEN_WIDTH // 2 - game_title.get_width() // 2, int(100 * self.scale_y))) #screen width divided by two

            for button in self.buttons:
                # arranges to draw the three buttons on the screen 
                button.draw(surface) # draws all three buttons on the screen 
                
        # if the menu state switches to the "start" screen:
        elif self.state == "start":
            screen.blit(CHECKERBOARD, (0,0))
            # draw method for the back button
            self.back_button.draw(surface) # the surface of the button is drawn to the upper side of the screen 

        # if the user switches the menu state to the "High_Score" screen    
        elif self.state == "high_score":
            High_Score_Font = current_font.render("HIGH SCORE", True, NAVY_BLUE) #font engine converts the text into an image surface
            surface.blit(High_Score_Font, (SCREEN_WIDTH // 2 - High_Score_Font.get_width() // 2, int(DRAWN_HIGH_SCORE_SCALE_INTEGERR * self.scale_y)))
            
            self.back_button.draw(surface)

        # if the user switches menu state to the "Settings" screen    
        elif self.state == "settings":
            Settings_Font = current_font.render("USER SETTINGS", True, NAVY_BLUE)
            surface.blit(Settings_Font, (SCREEN_WIDTH // 2 - Settings_Font.get_width() // 2, int(DRAWN_SETTING_SCALE_INTEGERR * self.scale_y)))
            self.back_button.draw(surface)


# this is the definition for the message that will appear when the user dies
# not apart of any other 
def message(msg, text_colour):
        text = MESSAGE_FONT.render(msg, True, text_colour)
        text_box = text.get_rect(center=(300, 360))
        screen.blit(text, text_box)


# The main loop for the game
menu = Menu()
Snake_sprite = None

game_run = True
while game_run:
    for event in pygame.event.get():
        # if the close box is clicked on the window
        if event.type == pygame.QUIT:
            # the running control is false
            game_run = False
        elif event.type == pygame.VIDEORESIZE:
           # been defined in previous definition
           menu.mouse_click(event.w, event.h)

        if menu.state == "start" and Snake_sprite is not None: # if start button is pressed and the snake instance is true
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Snake_sprite.direction(Snake.UP) # if the user has pressed up, move the snake up
                elif event.key == pygame.K_DOWN:
                    Snake_sprite.direction(Snake.DOWN)
                elif event.key == pygame.K_RIGHT:
                    Snake_sprite.direction(Snake.RIGHT)
                elif event.key == pygame.K_LEFT:
                    Snake_sprite.direction(Snake.LEFT)



        menu.handle_events(event)
    # system loop tick components in order are executed
    menu.update()
    menu.draw(screen)

    if menu.state == "start" and Snake_sprite is not None:
        Snake_sprite.update_position()
        Snake_sprite.draw()
        menu.back_button.draw(screen) # Keep button drawn over the snake
        
        if Snake_sprite.check_collision(): # if snake hits the wall
            message("GAME OVER", MAROON) # calls back the definition and colors it as maroon
            pygame.display.flip()
            time.sleep(2) # time taken to return to Menu screen and exit
            menu.set_state("menu") # returns to main menu

    pygame.display.flip()
    # screen to to 50 fps
    clock.tick(50)

# signals the end of all pygame modules

pygame.quit()
# ensures that the game closes down without freezzing 
sys.exit()


    
    
    

