from os.path import exists
import pygame

# This classes job is to load images
# This is so that this can be used for multiple sprites
class ImageList():
    def __init__(self, filename, width, height):
        self._images=[] 
        count = 0        
        while exists(filename+str(count)+ '.jpg'):
            image = pygame.image.load(filename+str(count)+ '.jpg')
            scaled = pygame.transform.smoothscale(image,[width,height])
            self._images.append(scaled)
            count += 1


    def get_images(self):
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
    image_obj= ImageList(TEST_FILES, TEST_H, TEST_W)

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

    pygame.quit() #exits pygame
    quit()
