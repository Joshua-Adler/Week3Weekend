import math
import keyboard

import graphics

#Card values to be displayed based on their numeric value
CARD_VALUES = {
	1: 'A',
	2: '2',
	3: '3',
	4: '4',
	5: '5',
	6: '6',
	7: '7',
	8: '8',
	9: '9',
	10: '10',
	11: 'J',
	12: 'Q',
	13: 'K'
}

#Card suits to be displayed based on their (arbitrary) IDs
CARD_SUITS = {
	0: '♠',
	1: '♣',
	2: '♥',
	3: '♦'
}

class Card():

	def __init__(self, value, suit):
		self.value = value
		self.suit = suit
		#Make a new screen to store the card's image
		self.tex = graphics.Screen((7, 3))
		#Draw the border
		self.tex.rect((1, 0), (6, 1), '─')
		self.tex.rect((1, 2), (6, 3), '─')
		self.tex.set((0, 0), '┌')
		self.tex.set((6, 0), '┐')
		self.tex.set((0, 2), '└')
		self.tex.set((6, 2), '┘')
		self.tex.set((0, 1), '│')
		self.tex.set((6, 1), '│')
		#Draw the value and suit
		self.tex.text((2, 1), str(CARD_VALUES[self.value]))
		self.tex.text((4, 1), str(CARD_SUITS[self.suit]))

	def draw(self, pos, screen):
		screen.blit(pos, self.tex)


class Button():

	def __init__(self, pos, msg, cmd, padding=(2, 1)):
		self.pos = pos
		self.msg = msg
		self.cmd = cmd
		self.padding = padding
		self.selected = False

	def draw(self, screen):
		hlen = len(self.msg) // 2
		#Figure out the top right and bottom left corners of the button
		top_right = (self.pos[0] - hlen - self.padding[0], self.pos[1] - self.padding[1])
		bottom_left = (self.pos[0] + hlen + self.padding[0] + len(self.msg) % 2, self.pos[1] + self.padding[1] + 1)
		#Selected buttons have a brighter border
		if self.selected:
			screen.rect((top_right[0] - 2, top_right[1] - 1), (bottom_left[0] + 2, bottom_left[1] + 1), '█')
		else:
			screen.rect((top_right[0] - 2, top_right[1] - 1), (bottom_left[0] + 2, bottom_left[1] + 1), '░')
		#Clear some empty space and put the button's message in it
		screen.rect(top_right, bottom_left, ' ')
		screen.text(self.pos, self.msg, True)

class ButtonManager():

	#Presses a button
	def use(self, e):
		self.curbut.cmd()

	#Finds the closest button in a cone outwards from a button in a direction
	def get_best(self, thresh, dir, oldbut):
		best = 1e9
		#Coordinate/screenspace adjustments
		oldbut.pos = (oldbut.pos[0] / 2, oldbut.pos[1])
		for button in self.buttons:
			#Button can't move to itself
			if button != oldbut:
				#Coordinate/screenspace adjustments
				button.pos = (button.pos[0] / 2, button.pos[1])
				#Dot product of direction moving in and direction to the button
				dot = (dir[0] * (button.pos[0] - oldbut.pos[0]) + dir[1] * (button.pos[1] - oldbut.pos[1]))
				dist = math.dist(button.pos, oldbut.pos)
				#Check if the button is within a certain angle of the direction and is the closest button
				if dot / dist > thresh and dist < best:
					best = dist
					self.curbut = button
				button.pos = (int(button.pos[0] * 2), button.pos[1])
		oldbut.pos = (int(oldbut.pos[0] * 2), oldbut.pos[1])

	#Gets the optimal target button for moving from one to another in a direction
	def select(self, dir):
		oldbut = self.curbut
		#Try to find a button in the direction of the arrow key pressed
		self.get_best(0.8, dir, oldbut)
		if oldbut == self.curbut:
			#If none is found, settle for a button that the direction doesn't point AWAY from
			self.get_best(0, dir, oldbut)
		#If a button has been found, move to it and redraw/update the portion of the screen
		if oldbut != self.curbut:
			oldbut.selected = False
			oldbut.draw(self.screen)
			self.curbut.selected = True
			self.curbut.draw(self.screen)
			self.screen.show()

	#Add all the hooks for button usage
	def activate(self):
		keyboard.on_press_key('shift', self.use)
		keyboard.on_press_key('left', lambda e: self.select((-1, 0)))
		keyboard.on_press_key('right', lambda e: self.select((1, 0)))
		keyboard.on_press_key('up', lambda e: self.select((0, -1)))
		keyboard.on_press_key('down', lambda e: self.select((0, 1)))

	#Remove the hooks
	def deactivate(self):
		keyboard.unhook_all()

	def __init__(self, buttons, screen):
		self.screen = screen
		self.buttons = buttons
		self.curbut = self.buttons[0]
		self.curbut.selected = True
		

	def draw(self):
		for button in self.buttons:
			button.draw(self.screen)