import pygame
MID_NIGHT_BLUE =(0, 24, 50) # for the button background colors
MAROON = (128, 0, 0) # for the button text and border colors.
SCALED_BUTTON_FONT = 0.5
BUTTON_RADIUS = 3
BUTTON_TEXT_RENDER = 2
BUTTON_FONT_SIZE = 12
class Button():
    MIN_BUTTON_W = 10
    MIN_BUTTON_H = 10
    CLICK_OFFSET = 5

    DEFAULT_FONT = 'Sans New Roman' # the font of my buttons  
    DEFAULT_FONT_SIZE = 40

    FONT_COLOR = MAROON
    HIGHLIGHT_COLOR = pygame.Color('darkgrey')
    BG_COLOR = MID_NIGHT_BLUE
    BORDER_COLOR = (MAROON)


    # button innit function
    def __init__(self, text, x, y, w, h, callback=None):
        # init internal variables
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._mouse_over = False
        self._button_down = False
        self._disabled = False  
        self._border = 4        

        if w < Button.MIN_BUTTON_W:
            self._w = Button.MIN_BUTTON_W
        else:
            self._w = w
        if h < Button.MIN_BUTTON_H:
            self._h = Button.MIN_BUTTON_H
        else:
            self._h = h
            
        self._text = text
        # color coded definitions effected
        self._font_color = Button.FONT_COLOR
        self._bg_color = Button.BG_COLOR
        self._border_color = Button.BORDER_COLOR
        self._highlight_color = Button.HIGHLIGHT_COLOR
        self._down = False
        self._action = callback # callback has been defined above
        
        # font propertes
        self._font = pygame.font.SysFont(Button.DEFAULT_FONT, Button.DEFAULT_FONT_SIZE)
    def click(self):
        if self._action is None:
            print("No action function set for button:", self._text)
        else:
            self._action()

    def contains(self, x, y):
        return self.get_rect().collidepoint(x, y)
    
    def get_rect(self):
        return pygame.Rect(self._x, self._y, self._w, self._h)

    def mouse_move(self, x, y):
        if not self._disabled:
            if self.contains(x, y):
                self._mouse_over = True
            else:
                self._mouse_over = False

    def mouse_click(self, event):
        if not self._disabled:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self._mouse_over:
                    self._button_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._button_down and self._mouse_over:
                    if self._action is not None:
                        self._action() # im' clicked
                    else:
                        print("button", self._text, "has no function set") # in the case if my button isn't working 
                self._button_down = False

    def set_action(self, action_function):
        self._action = action_function
    def get_action(self):
        return self._action
    action = property(get_action, set_action)

    def draw(self, screen):
        # buttons that are scaled 
        scaled_font_size = int(self._h * SCALED_BUTTON_FONT) 
        # the font of the buttons are directly proportionally scaled to the buttons
        self._font = pygame.font.SysFont(Button.DEFAULT_FONT, max(BUTTON_FONT_SIZE, scaled_font_size))
        # the radius of the buttons, order for them to be rounded
        radius = int(self._h * BUTTON_RADIUS)
        # draws the rectangle
        pygame.draw.rect(screen, self._border_color, self.get_rect(), border_radius=radius)
        inner_rad= pygame.Rect(self._x + self._border, self._y + self._border, self._w - self._border*2, self._h - self._border*2)
        # for the perfect inner shape, value of the border is subtracted from the radius
        inner_radius = max(0, radius - self._border)
        # draws the updated button curved
        pygame.draw.rect(screen, self._bg_color, inner_rad, border_radius= inner_radius)

        # draws the text
        color = self._font_color
        offset = 0 # so that button doesn't lag
        if self._mouse_over:
            if self._button_down:
                offset = Button.CLICK_OFFSET
            else:
                color = self._highlight_color
        # rendering code for my text
        # creates the rendered text as a surface
        rendered_text = self._font.render(self._text, True, color, self._bg_color)
        # gets the rectangle for this surface
        rendered_text_rect = rendered_text.get_rect() 
        rendered_text_rect.center = (self._x + self._w / BUTTON_TEXT_RENDER + offset, self._y + self._h / BUTTON_TEXT_RENDER + offset)
        # tells where the button is to be drawn 
        screen.blit(rendered_text, rendered_text_rect)

