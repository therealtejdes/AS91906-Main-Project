"""Imagelist."""
from os.path import exists
import pygame
BLACK = (0, 0, 0)
# this classes Job is to load images
# o that it can be used for multiple sprites


class ImageList():


    """Imagelist class."""
    
    def __init__(self, filename, width, height, fallback_color=(BLACK)):
        """Imagelist init function."""
        self._images = [] 
        count = 0        
        # Attempt to load disk assets if they exist
        while filename and exists(filename + str(count) + '.png'):
            image = pygame.image.load(filename + str(count) + '.png')
            scaled = pygame.transform.smoothscale(image, [width, height])
            self._images.append(scaled)
            count += 1
        if not self._images:
            # the screen will cut to black
            fallback_surface = pygame.Surface((width, height))
            fallback_surface.fill(fallback_color)
            self._images.append(fallback_surface)

    def get_images(self):
        """Draws the images with the image property."""
        return self._images
    images = property(get_images, None, None)


# testing
if __name__ == "__main__":
    pygame.init() 
    #Initializes the start of pygame
    
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    TEST_X=50
    TEST_Y=50
    TEST_W=64
    TEST_H=64
    TEST_FILES = "images\\test\\test"
    image_obj= ImageList(TEST_FILES, TEST_W, TEST_H)
    clock = pygame.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
    pygame.display.set_caption("SNAKED")


    # Pygame has been initialised. 
    

    # Loop for while not qutting
    quit_game = False
    while not quit_game: # recieves all events from the user(user inputs)
        for event in pygame.event.get(): # checks if the event is a quit type
            if event.type == pygame.QUIT:
                quit_game = True

        count = 0
        for image in image_obj.images:
            image_rect= pygame.Rect(TEST_X + (count * (TEST_W+20)), TEST_Y, TEST_W, TEST_H)
            screen.blit(image,image_rect)
            count +=1
        
        
    

        pygame.display.flip()
        clock.tick(60)

    pygame.quit() #exits pygame
    quit()

# testing
# may be removed when programme is completed
if __name__ == "__main__":
    pygame.init() 
    #Initializes the start of pygame
    
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    TEST_X=50
    TEST_Y=50
    TEST_W=64
    TEST_H=64
    TEST_FILES = "images\\test\\test"
    image_obj= ImageList(TEST_FILES, TEST_W, TEST_H)
    clock = pygame.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
    pygame.display.set_caption("SNAKED")


    # Pygame has been initialised. 
    

    # Loop for while not qutting
    quit_game = False
    while not quit_game: # recieves all events from the user(user inputs)
        for event in pygame.event.get(): # checks if the event is a quit type
            if event.type == pygame.QUIT:
                quit_game = True

        count = 0
        for image in image_obj.images:
            image_rect= pygame.Rect(TEST_X + (count * (TEST_W+20)), TEST_Y, TEST_W, TEST_H)
            screen.blit(image,image_rect)
            count +=1
        
        
    

        pygame.display.flip()
        clock.tick(60)

    pygame.quit() #exits pygame
    quit()