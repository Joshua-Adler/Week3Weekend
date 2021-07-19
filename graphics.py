import os
import numpy as np

#Can't really change the terminal size, but can detect it - ask the user nicely
def set_terminal_size(size):
	cur_size = os.get_terminal_size()
	while cur_size != size:
		print(f"Please resize your terminal to 120x30. It is currently {cur_size[0]}x{cur_size[1]}.")
		print("That value may be wrong in some terminals. If you're sure that your terminal is 120x30, please force-continue.")
		force = input("Press enter to continue, or enter 'F' and hit enter to force-continue.")
		if 'f' in force.lower():
			break
		size = os.get_terminal_size()

class Screen():

	def __init__(self, size):
		self.has_changes = False
		self.size = size
		self.data = np.full((size[1], size[0]), fill_value=' ', dtype='U1')

	#These drawing functions tend to have issues with things that go off-screen.
	#I didn't bother to fix those issues, since things don't tend to go off-screen and fixing them would slow the functions down

	#Draws a rectangle from top_left to bottom_right with the character ch.
	#top_left is inclusive, bottom_right is exclusive
	def rect(self, top_left, bottom_right, ch='█'):
		has_changes = True
		self.data[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = ch

	#Sets the character at the pos to ch
	def set(self, pos, ch):
		has_changes = True
		self.data[pos[1], pos[0]] = ch

	#Draws a text message at pos.
	#Gets very angry if you give it a newline, might eat your lunch
	def text(self, pos, msg, centered=False):
		has_changes = True
		cen = 0
		if centered:
			cen = len(msg) // 2
		for i in range(len(msg)):
			self.data[pos[1], pos[0] + i - cen] = msg[i]

	#Blits another image (Screen object) into this one, with the top left corner being pos
	def blit(self, pos, img):
		has_changes = True
		self.data[pos[1]:pos[1] + img.data.shape[0], pos[0]:pos[0] + img.data.shape[1]] = img.data
	
	#Clears the screen with ch
	def clear(self, ch=' '):
		has_changes = True
		self.data[:, :] = ch

	def show(self):
		has_changes = False
		print(''.join([''.join(line) for line in self.data]))