# This part of the code is the button 
import pygame

class Button():

    # logical values are defined
	MIN_BUTTON_W = 100
	MIN_BUTTON_H = 50
	def __init__(self, x, y, w, h, text, font, background_color, forground_color):
		if w < Button.MIN_BUTTON_W:
			self._w = Button.MIN_BUTTON_W
		else:
			self._w = w
		if h < Button.MIN_BUTTON_H:
			self._h = Button.MIN_BUTTON_H
		else:
			self._h = h
		self._x = x
		self._y = y
		self._text = text
		self._font = font
		self._background_color = background_color
		self._forground_color = forground_color
		self._down = False
		self._action = None

    # function for rect
    # checks for x and y
	def get_rect(self):
		return pygame.Rect(self._x, self._y, self._w, self._h)

    # only checks for x and y
    # due to that the rectangle is already defined in the previous function
	def contains(self, x, y):
		return self.get_rect().collidepoint(x, y)
	
	def set_action(self, action_function):
		if callable(action_function):
			self._action = action_function
	
    # function to call the button 
	def click(self):
		if self._action == None:
			print("No action function set for button:", self._text)
		else:
			self._action()

	# This definition will now draw the rectangle (button)
	def draw(self, screen):
		# this draws the rectangle and the forground color (border)
		pygame.draw.rect(screen, self._fg_color, self.get_rect())
        # this 
		pygame.draw.rect(screen, self._bg_color, pygame.Rect(self._x+2, self._y + 2, self._w - 4, self._h - 4))

		# draw the text
		rendered_text = self._font.render(self._text, True, self._fg_color, self._bg_color)
		rendered_text_rect = rendered_text.get_rect()
		rendered_text_rect.center = (self._x + self._w / 2, self._y + self._h / 2)
		screen.blit(rendered_text, rendered_text_rect)
