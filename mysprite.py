from os.path import exists
import pygame
from imagelist import ImageList
import time


class MySprite():
    def __init__(self, x, y, w, h, images, screen):
        white = (188, 227, 199) #This is a tuple (Snake Variable)
        gold = (255, 215, 0) #(Token variable)
        black = (37, 37, 37) #(For the score alongside other inputs)
        red = (255, 0, 0) #(For the screen when the game is over)


        valid = True
        self._y = y #Classifies Y as only Y
        self._w = w #Classifies w as only w
        self._h = h #Classifies h as only h
        self._x = x #Classifies x as only x
        self._xd=0
        self._yd=0

        self._images = images
        self._screen = screen

        self._current_frame = 0
        self._start_frame = 0
        self._end_frame = 0
        self._delay = -1
        self._repeat= False
        self._next_move = time.time()
        self._move_delay = 0

        if x>=0 and x<=SCREEN_WIDTH:
            self._x = x
        else:
            print("INVALID")
            exit(0)

        if y>=0 and y<=SCREEN_HEIGHT:
            self._y = y
        else:
            print("INVALID")
            exit(0)

        if w>=0 and w<=SCREEN_WIDTH:
            self._w = w
        else:
            print("INVALID")
            exit(0)

        if h>=0 and h<=SCREEN_HEIGHT:
            self._h = h
        else:
            print("INVALID")
            exit(0)

    def get_rect(self):
        return(self._x,self._y,self._w, self._h)


    def get_x(self):
        return self._x

    def set_x(self, x):
        if x>=0 and x<= SCREEN_WIDTH:
            self._x = x
        elif x<0:
            self._x = 0
        else:
            self._x = SCREEN_WIDTH - 1

    def get_y(self):
        return self._y

    def set_y(self, y):
        if y>=0 and y<= SCREEN_HEIGHT:
            self._y = y
        elif y<0:
            self._y = 0
        else:
            self._y = SCREEN_HEIGHT - 1
        
    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def set_pos(self, x, y):
        self.set_x(x)
        self.set_y(y)

    def move(self, x_delta=None, y_delta=None, delay = None):
        if not x_delta is None:
            self._xd = x_delta
        if not y_delta is None:
            self.yd = y_delta
        if not delay is None:
            self._move_delay = delay
            self._next_move = time.time() + delay

        if time.time() > self._next_move:
            self.set_x(self._x + self._xd)
            self.set_y(self._y + self._yd)
            self._next_move = self._next_move + self._move_delay


    # collision code
    def collide (self, x, y, w, h):
        if x>self._x + self._w or\
           y > self.__y + self.__h or\
           x + w < self.__x or \
            y + h < self.__y:
            return False
        else:
            return True
        
    # Animation cod 
    def set_animation(self, start_frame, end_frame=0, delay=0, repeat=1):
        if start_frame >=0 and start_frame < len(self._images.images):
            self._start_frame = start_frame
        #
        if end_frame >=0 and end_frame < len(self._images.images) and start_frame <= end_frame:
            self._end_frame = end_frame

        if delay >=0:
            self._delay = delay

        if repeat:
            self._delay = True
        else:
            self._repeat = False

        self._next_frame = time.time() + delay


    def animate(self, reset_animation = False):
        # If we are animating
        if reset_animation == True:
        # If we are resetting the animation 
            self._current_frame = self._start_frame
        else:
            if time.time()> self._next_frame:
                # go to the next frame 
                pass

        self_next_frame = self._next_frame +self._delay
        # This shows that the next frame will pop up 

        
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._h, self._w)
       
    def draw(self):
        self._screen.blit(self._images.images[self._current_frame], self.get_rect()) 
        # This is coded as to how often the graphic will appear.
        

# TESTING CODE
if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    TEST_X=50
    TEST_Y=50
    TEST_W=64
    TEST_H=64
    TEST_FILES = "images\\test\\test"
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
    pygame.display.set_caption('SNAKED')
    # Pygame has been initialised. 

    image_rect= pygame.Rect(TEST_H, TEST_W, TEST_X, TEST_Y)
    image_obj = ImageList("images\\test\\test", 64, 64)

    test_imagelist = ImageList(TEST_FILES, TEST_W, TEST_H)

    sprite1 = MySprite(TEST_X, TEST_Y, TEST_H, TEST_W)

    spritelist = []
    spritelist.append(MySprite(TEST_X, TEST_Y, TEST_H, TEST_W, image_obj, screen))
    spritelist [-1].set_animation(0, 3, 0.1, True)
    spritelist.append(MySprite, TEST_X+TEST_W, TEST_Y, TEST_W, TEST_H, image_obj, screen)

    # Loop for while not qutting

    quit_game = False
    while not quit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True

        # This section of the code draws, animates and 


            pygame.display.flip()


    pygame.quit()
    quit()
    # This allows for the window to be manually exited.
   
    
