import pygame
import json
from imagelist import ImageList
from mysprite import MySprite
pygame.init()

# TESTING CODE
# Imported from "My sprite"
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

        for sprite in spritelist:
            sprite.draw
            sprite.animate
            sprite.move(1, 0, 1)

            

            pygame.display.flip()


    pygame.quit()
    quit()
    # This allows for the window to be manually exited.
   