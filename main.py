import pygame
import time
import json
import sys
import button
import random # for the food 
from os.path import exists #reading files
from imagelist import ImageList # class extracted from the other file
from mysprite import MySprite # class extracted from other file 
from button import Button # class extracted from the other file

#definitions for JSON (Reading, writing, previous score) (json.loads)
#definition to load the previous score
def load_previous_score():
    try: # directly references the external file 
        with open("data.json", "r") as t:
            # passes the string
            return json.load(t)
    # if the new score isn't loaded, the value remains at zero
    except:
        return {"previous_score": 0}

# definition that saves the preivous score
def save_previous_score(data):
    # when the file is opened
    with open("data.json", "w") as t:
        # indentation to make the file easier to read
        json.dump(data, t, indent=4) #converts the data into a string

# all pygame modules have been activated 
pygame.init()

# important logistical values for my screen 
ARENA_SCREEN_WIDTH = 800
ARENA_SCREEN_HEIGHT = 600
# images used for the game
SNAKE_HEAD = "images\\SNAKE_HEAD"
SNAKE_TAIL = "images\\SNAKE_TAIL"
TOKEN = "images\\TOKEN"
MENU_SNAKE = "images\\MENU_SNAKE"

screen = pygame.display.set_mode((ARENA_SCREEN_WIDTH, ARENA_SCREEN_HEIGHT), pygame.RESIZABLE) #avoids the usage of magic numbers
# snakes starting postion
SNAKES_STARTING_X_POSITION = 360
SNAKES_STARTING_Y_POSITION = 320
# Logistical values for scaling
SCALED_WIDTH = 800
SCALED_HEIGHT = 600

# tilesize for the snakes head, tail and token
TILESIZE_X = 40
TILESIZE_Y = 40
TOKEN_HEIGHT = ARENA_SCREEN_HEIGHT - TILESIZE_Y # SCREEN width - score calculator height - back button height

# Values for my buttons
# These values remain constant for all buttons
# all buttons will be featured on the main menu
BUTTON_WIDTH = 200
BUTTON_HEIGHT= 100
BUTTON_CENTER = 300 

# Values for the back button 
BUTTON_X = 20
BUTTON_Y = 20
BACK_BUTTON_WIDTH = 200
BACK_BUTTON_HEIGHT = 50
BACK_BUTTON_PADDING = 20

MENU_FONT_SIZE = 100
MESSAGE_FONT = pygame.font.SysFont("Sans New Roman", 100)

SETTINGS_SCALE_INTEGER = 460
START_SCALE_INTEGER = 300
DRAWN_START_SCALE_INTEGER = 30
DRAWN_INSTRUCTION_SCALE_INTEGER = 5
DRAWN_MENU_SCALE_INTEGER = 100

# convert alpha allows for the image to be placed upon much easier
CHECKERBOARD = pygame.image.load("CHECKERBOARD.png").convert_alpha()
# gameplay caption:
pygame.display.set_caption("SNAKED, By Tej Desai") 

# tuples containing the RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255) 
MAROON = (128, 0, 0) 
GOLD = (255, 215, 0)
NAVY_BLUE = (0, 0, 128)
AIR_FORCE_BLUE = '#004F98'
WINE_RED = '#4E0707'
# pygame clock (running)
clock = pygame.time.Clock()

SCORE_CALCULATOR = 5


# Token class
class Token():
    # init definition for the Token
    def __init__(self, screen):
        self._screen = screen
        self._w = TILESIZE_X # scaling to the snakes tile size
        self._h = TILESIZE_Y
        
        self._token = ImageList(TOKEN, self._w, self._h) # provides the image using the imagelist class
        self._x = 0 # x and y values set to zero because they token is not actively moving
        self._y = 0 
        self._token_sprite = None
        self.random_spawn() 

    # definition in order to draw my token
    def random_spawn(self):
        Colums = ARENA_SCREEN_WIDTH // self._w 
        # makes sure that the token doesn't get in the way of the the score caluclator
        # and the back button 
        Rows = TOKEN_HEIGHT // self._h
        #grid functions 
        grid_x = random.randint(3, max(2, Colums - 4)) 
        grid_y = random.randint(3, max(2, Rows - 4)) 
        
        self._x = int(grid_x * self._w) 
        self._y = int(grid_y * self._h)
        # token drawn like a mysprite object
        self._token_sprite = MySprite(self._x, self._y, self._w, self._h, self._token, self._screen) 

    # definition to draw the token on screen 
    def draw(self):
        if self._token_sprite:
            self._token_sprite.draw() 

# snake class 
class Snake():
    # internal values for the snakes movements and directions
    HEAD = 0
    TAIL = -1
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    SNAKE_VECTOR = [(0,-1), (1,0), (0,1), (-1,0)] 
    # init function for the snakes variables. 
    def __init__ (self, screen, x, y, direction = UP):
        self._x = x
        self._y = y
        self._direction = direction
        self._screen = screen # snake is to be drwan on the screen. 
        self._length = 2
        self._move_speed = 0.10 # the inital speed at which the snake will move. 
        self._seg_list = []
        self._head_image = ImageList(SNAKE_HEAD, TILESIZE_X, TILESIZE_Y) #will scale the image of the snakes head. 
        self._tail_image = ImageList(SNAKE_TAIL, TILESIZE_X, TILESIZE_Y)
        self._next_move = time.time() + self._move_speed 
        self.reset()

    # this is the definiton that will assemble the snakes body
    def reset(self):
        self._seg_list = [] #snakes body is an open list
        for i in range (self._length): # snakes length is repeating
            component_x = self._x - (i * Snake.SNAKE_VECTOR[self._direction][0] * TILESIZE_X) 
            component_y = self._y - (i * Snake.SNAKE_VECTOR[self._direction][1] * TILESIZE_Y) 
            img_show = self._head_image if i == 0 else self._tail_image # draws the snakes tail
            # draws the snake as a mysprite object
            sprite_show = MySprite(component_x, component_y, TILESIZE_X, TILESIZE_Y, img_show, self._screen) 
            self._seg_list.append(sprite_show) 

    # definition for the snakes direcitons. 
    def direction(self, changing_dir):
        # condensed into a dictionary.
        movements = {
            Snake.UP: Snake.DOWN, 
            Snake.DOWN: Snake.UP, 
            Snake.RIGHT: Snake.LEFT,
            Snake.LEFT: Snake.RIGHT
        }
        # if the inputed direction is not the oppsite
        # the this direction to the changing directions
        if changing_dir != movements[self._direction]: 
            self._direction = changing_dir

    # defintion for the snakes movements to the next step 
    def update_position(self):
        if time.time() > self._next_move:
            # pygames time module + the initial move speed (0.10)
            self._next_move = time.time() + self._move_speed
            # moves the snake from the first part of the list
            # multplies the direction by the tilesize.
            updated_x = self._seg_list[0].x + (Snake.SNAKE_VECTOR[self._direction][0] * TILESIZE_X) 
            updated_y = self._seg_list[0].y + (Snake.SNAKE_VECTOR[self._direction][1] * TILESIZE_Y) 
            # head is redrawn as a mysprite object
            respawned_head = MySprite(updated_x, updated_y, TILESIZE_X, TILESIZE_Y, self._head_image, self._screen) 
            self._seg_list.insert(0, respawned_head)

            # the the number of objects within this segmented list is more than 1 
            if len(self._seg_list) > 1:
                # the seccond part of this list is equal to the tail image
                # the tail is growing 
                self._seg_list[1]._images = self._tail_image
            # the number of objects within the segemnted list is more than the snakes length

            if len(self._seg_list) > self._length:
                # the list is being taken out itself. 
                self._seg_list.pop()
    
    # defintion for the snakes wall collision
    def wall_and_self_collision(self): 
        if not self._seg_list:
            return False
        snake_head = self._seg_list[0]
        # checks whther the snake heads' horizontal and vertical postions are more or equal to screen x and y
        # an if they are less than zero
        if snake_head.x < 0 or snake_head.x >= ARENA_SCREEN_WIDTH \
        or snake_head.y < 0 or snake_head.y >= ARENA_SCREEN_HEIGHT:
            return True

        for component in self._seg_list[1:]:
            if snake_head.x == component.x and \
                snake_head.y == component.y:
                return True
        return False

    # definition for the snakes growth and speed 
    def grow_snake_and_speed(self): 
        self._length += 1
        if self._move_speed > 0.06: # max speed floor cap
            self._move_speed -= 0.01 # rate at which the snakes velocity increases 
    # draws the snake on screen
    def draw(self):
        for component in self._seg_list:
            component.draw()

class Menu():
    # innit function fo menu
    def __init__(self): 
        # internal variables as listed. 
        self.state = "menu"
        self.font = pygame.font.SysFont("Sans New Roman", MENU_FONT_SIZE)
        # scaling dimensions
        self.scale_x = ARENA_SCREEN_WIDTH / SCALED_WIDTH # = 1
        self.scale_y = ARENA_SCREEN_HEIGHT / SCALED_HEIGHT # = 1

        # main buttons defined using the button class.
        # scaled to size as
        
        self.start_button = Button("PLAY", int(BUTTON_CENTER * self.scale_x),
                    # scaling pushed through as an integer 
                   int(START_SCALE_INTEGER * self.scale_y), 
                   int(BUTTON_WIDTH * self.scale_x),
                   int(BUTTON_HEIGHT * self.scale_y))

        self.instructions_button = Button("INSTRUCTION", int(BUTTON_CENTER * self.scale_x), 
                   int(SETTINGS_SCALE_INTEGER * self.scale_y), 
                   int(BUTTON_WIDTH * self.scale_x), 
                   int(BUTTON_HEIGHT * self.scale_y))
        
        # condensed way of using the buttons to take to other screens
        self.start_button.action = lambda: self.set_state("start")
        self.instructions_button.action = lambda: self.set_state("instructions")

        self.buttons = [self.start_button, self.instructions_button]

        # back button is padded to top right of the screen and simultaneously scaled.

        Escape_x = int(ARENA_SCREEN_WIDTH - (BACK_BUTTON_WIDTH * self.scale_x) - (BACK_BUTTON_PADDING * self.scale_x))
        Escape_y = int(BUTTON_Y * self.scale_y) 

        self.back_button = Button("ESC", Escape_x, Escape_y,
        int(BACK_BUTTON_WIDTH * self.scale_x), 
        int(BACK_BUTTON_HEIGHT * self.scale_y))

        self.back_button.action = lambda: self.set_state("menu")
        #self._menu_snake = ImageList(MENU_SNAKE) 


    #
    def set_state(self, new_state):
        self.state = new_state
        if new_state == "start":
            global Snake_sprite, Token_sprite
            Snake_sprite = Snake(screen, SNAKES_STARTING_X_POSITION, SNAKES_STARTING_Y_POSITION) 
            Token_sprite = Token(screen)

    # displays the buttons on the screen
    def event(self, event):
        if self.state == "menu":
            for button in self.buttons:
                button.mouse_click(event)
        else: 
            self.back_button.mouse_click(event) #so that the user can use the back button to go to main

    # definition for the mouse detections 
    def update(self): 
        mouse_pos = pygame.mouse.get_pos() 
        mx, my = mouse_pos
        if self.state == "menu":
            for button in self.buttons:
                button.mouse_move(mx, my)
        else:
            self.back_button.mouse_move(mx, my) 

    # definition for the mouse to scale window
    def mouse_click(self, w, h):
        global screen, ARENA_SCREEN_WIDTH, ARENA_SCREEN_HEIGHT
        ARENA_SCREEN_WIDTH, ARENA_SCREEN_HEIGHT = w, h
        self.scale_x = ARENA_SCREEN_WIDTH / SCALED_WIDTH
        self.scale_y = ARENA_SCREEN_HEIGHT / SCALED_HEIGHT
        self.__init__()

    # definition to draw the buttons
    def draw(self, surface):
        surface.fill(BLACK) # backgorund color
        scaled_font = int(MENU_FONT_SIZE * self.scale_y) #scales the menu's font
        menu_text_font = pygame.font.SysFont("Sans New Roman", max(12, scaled_font)) 
        text_font = pygame.font.SysFont("Sans New Roman", max(12, scaled_font)) 
        # done through an if and else statement 
        if self.state == "menu":
            game_title = menu_text_font.render("SNAKED", True, NAVY_BLUE)
            surface.blit(game_title, (ARENA_SCREEN_WIDTH // 2 - game_title.get_width() // 2, int(DRAWN_MENU_SCALE_INTEGER * self.scale_y)))

            for button in self.buttons:
                button.draw(surface) 
                
        elif self.state == "start":
            screen.blit(CHECKERBOARD, (0,0)) # checkerboard is drawn as a background image
            self.back_button.draw(surface) # back button is drawn on the game screen

        # if the instructions button is pressed
        elif self.state == "instructions":
            screen.fill(WINE_RED)
            # the drawn lines of text that displayed on the screen
            instructions_title_font = text_font.render("INSTRUCTIONS:", True, AIR_FORCE_BLUE)
            surface.blit(instructions_title_font, (ARENA_SCREEN_WIDTH // 3 - instructions_title_font.get_width() // 3, int(DRAWN_INSTRUCTION_SCALE_INTEGER * self.scale_y)))
            welcome_font = text_font.render("WELCOME TO SNAKED!", True, AIR_FORCE_BLUE)
            surface.blit(welcome_font, (ARENA_SCREEN_WIDTH//3 - welcome_font.get_width()//3, int(DRAWN_INSTRUCTION_SCALE_INTEGER + 150)))
            arrow_line = text_font.render("Use the arrow", True, AIR_FORCE_BLUE)
            surface.blit(arrow_line, (ARENA_SCREEN_WIDTH//3 - arrow_line.get_width()//4, int(DRAWN_INSTRUCTION_SCALE_INTEGER +300)))
            keys_line = text_font.render("keys to move snake", True, AIR_FORCE_BLUE)
            surface.blit(keys_line, (ARENA_SCREEN_WIDTH//3 - keys_line.get_width()//3, int(DRAWN_INSTRUCTION_SCALE_INTEGER +450)))
            points_line = text_font.render("Each token's worth 5 points", True, AIR_FORCE_BLUE)
            surface.blit(points_line, (ARENA_SCREEN_WIDTH//3 - points_line.get_width()//3, int(DRAWN_INSTRUCTION_SCALE_INTEGER +600)))
            caution_line = text_font.render("Hit the wall, you die!", True, AIR_FORCE_BLUE)
            surface.blit(caution_line, (ARENA_SCREEN_WIDTH//3 - caution_line.get_width()//3, int (DRAWN_INSTRUCTION_SCALE_INTEGER +750)))
            luck_line = text_font.render("GOOD LUCK GAMER!", True, AIR_FORCE_BLUE)
            surface.blit(luck_line, (ARENA_SCREEN_WIDTH//3 - luck_line.get_width()//3, int(DRAWN_INSTRUCTION_SCALE_INTEGER + 900)))

            
            self.back_button.draw(surface)

# definiton for my "Game Over" message
def message(msg, text_colour):
    text = MESSAGE_FONT.render(msg, True, text_colour)
    text_box = text.get_rect(center=(ARENA_SCREEN_WIDTH//2, SCALED_HEIGHT//2)) # so that the part is scaled
    screen.blit(text, text_box) # draws the box

# defintion for the "current score message"
def score_calculator(msg, text_colour, back_ground_colour):
    text = MESSAGE_FONT.render(msg, True, text_colour, back_ground_colour)
    text_box = text.get_rect(center=(ARENA_SCREEN_WIDTH // 6, 30)) # Center top of gameplay area
    screen.blit(text, text_box) # draws the box

# classes instanziation
main_menu = Menu()
Snake_sprite = None
Token_sprite = None
score_data = load_previous_score()
previous_score = score_data.get("previous_score", 0)
game_run = True
# while loop for game
while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # if user presses the exit button on the window 
            game_run = False

        elif event.type == pygame.VIDEORESIZE:
           main_menu.mouse_click(event.w, event.h) # actively scales the menu

        if main_menu.state == "start" and Snake_sprite is not None: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    Snake_sprite.direction(Snake.UP) # definiion is called back to move the snake up
                elif event.key == pygame.K_DOWN:
                    Snake_sprite.direction(Snake.DOWN) # definition is called back to move the snake down
                elif event.key == pygame.K_RIGHT:
                    Snake_sprite.direction(Snake.RIGHT) # definition is called back to move snake right
                elif event.key == pygame.K_LEFT:
                    Snake_sprite.direction(Snake.LEFT)# definitoin is called back to move snake left 

        main_menu.event(event)

    main_menu.update()
    main_menu.draw(screen)

    if main_menu.state == "start" and Snake_sprite is not None:
        Snake_sprite.update_position()
        
        
        if Token_sprite is not None:
            Token_sprite.draw()  
        if Token_sprite is not None and len(Snake_sprite._seg_list) > 0: 
            snake_head = Snake_sprite._seg_list[0] 
            # checks whether the snakes horizontal and vertical postitons are the same as the tokens
            if snake_head.x == Token_sprite._x and snake_head.y == Token_sprite._y: 
                # Token is drawn somewhere else
                Token_sprite.random_spawn()
                # the snake moves and grows
                Snake_sprite.grow_snake_and_speed()
        
        Snake_sprite.draw() 
        # score tracker when the main menu opens
        score_tracker = max(0, (Snake_sprite._length - 2) * SCORE_CALCULATOR) 
        # displays the score on screen
        score_display = f"SCORE: {score_tracker}" 
        # draws the score calculator on the top of the window
        score_calculator(score_display, BLACK, WHITE)
        main_menu.back_button.draw(screen) 
        
        if Snake_sprite.wall_and_self_collision(): 
            # resets the score file after the snake has died
            score_display = f"SCORE: {score_tracker} PREVIOUS SCORE:{previous_score}"
            screen.fill(BLACK)
            message("GAME OVER", WINE_RED) # appears in the middle of the screen
            pygame.display.flip()
            time.sleep(2) 
            main_menu.set_state("menu") 
            # howver if the current score exceeds the previous score
            if score_tracker > previous_score:
                previous_score = score_tracker
                # saves the updated within the json file
                save_previous_score({"previous_score": previous_score})

    pygame.display.flip()

pygame.quit()
sys.exit()


    
    