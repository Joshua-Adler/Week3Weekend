import keyboard
import random
import webbrowser
import os
import math

import elements

class Game():
	
	#Determines the score of a player's (or dealer's) cards
	def card_sum(self, cards):
		sum = 0
		for card in cards:
			sum += min(card.value, 10)
		return sum

	def make_deck(self):
		deck = []
		for value in range(1, 14):
			for suit in range(4):
				deck.append(elements.Card(value, suit))
		random.shuffle(deck)
		return deck

	#Deal out the first 4 cards
	def start_deal(self):
		self.dealer = [self.deck.pop() for i in range(2)]
		self.player = [self.deck.pop() for i in range(2)]

	#Start a new game
	def restart(self):
		keyboard.unhook_all()
		Game(self.screen)

	#Go back to the menu
	def menu(self):
		keyboard.unhook_all()
		Menu(self.screen)

	#Switches the buttons to the end buttons
	def end_game(self):
		self.playing_buttons.deactivate()
		self.end_buttons.activate()

	def stand(self):
		#Get scores
		dealer_score = self.card_sum(self.dealer)
		score = self.card_sum(self.player)
		#Make the player win or lose
		if score >= dealer_score:
			self.state = 'win'
		else:
			self.state = 'lose'
		self.end_game()
		#Show the end screen
		self.draw()
		self.draw_cards(5, self.dealer)
		self.screen.text((61, 8), f"Dealer Score: {dealer_score}", True)
		self.screen.show()

	def hit(self):
		#Grab a new card
		self.player.append(self.deck.pop())
		#Check if the player is over 21, make them lose if so
		if self.card_sum(self.player) > 21:
			self.state = 'lose'
			self.end_game()
		#Redraw screen
		self.draw()
		self.screen.show()

	def __init__(self, screen):
		#Set default state, determines what to draw
		self.state = 'playing'
		#Create play buttons
		buttons = [
			elements.Button((45, 24), 'Hit', self.hit),
			elements.Button((75, 24), 'Stand', self.stand),
			elements.Button((110, 4), 'Menu', self.menu)
		]
		self.playing_buttons = elements.ButtonManager(buttons, screen)
		self.playing_buttons.activate()
		#Create end buttons
		buttons = [
			elements.Button((45, 24), 'Restart', self.restart),
			#quit() wasn't working
			elements.Button((75, 24), 'Quit', lambda: os._exit(0)),
			elements.Button((110, 4), 'Menu', self.menu)
		]
		self.end_buttons = elements.ButtonManager(buttons, screen)
		self.screen = screen
		#Initiate the first steps of the game
		self.deck = self.make_deck()
		self.start_deal()
		self.draw()

	#Draws the cards you give it at the given y position
	def draw_cards(self, y, cards):
		cen = len(cards) / 2
		for i in range(len(cards)):
			cards[i].draw((math.floor((i - cen) * 9) + 62, y), self.screen)

	def draw(self):
		#Draw the dealer's and player's cards
		self.screen.clear()
		self.screen.text((61, 4), 'Dealer', True)
		self.draw_cards(5, self.dealer)
		self.screen.text((64, 6), '???')
		self.screen.text((61, 11), 'Player', True)
		self.draw_cards(12, self.player)
		#Draw the player's score
		score = self.card_sum(self.player)
		self.screen.text((61, 15), f"Player Score: {score}", True)
		#Figure out which buttons to draw
		if self.state == 'playing':
			self.playing_buttons.draw()
		else:
			self.end_buttons.draw()
			if self.state =='win':
				#Figure out which ending message to draw
				if self.card_sum(self.player) == 21 and len(self.player) == 2:
					self.screen.text((61, 18), 'You Win! Blackjack!', True)
				else: 
					self.screen.text((61, 18), 'You Win!', True)
			else:
				self.screen.text((61, 18), 'You Lose.', True)
				
		self.screen.show()


class Menu():

	#Opens the game
	def play(self):
		keyboard.unhook_all()
		Game(self.screen)

	#Opens the instructions in your browser
	def help(self):
		webbrowser.open("https://classroom.google.com/u/0/c/MzUwNzEzNzEyMDkz/a/MzcwODM5OTEzMDgy/details")

	def __init__(self, screen):
		self.screen = screen
		#Create menu buttons
		buttons = [
			elements.Button((60, 8), 'Play', self.play),
			elements.Button((43, 23), 'Help', self.help),
			#quit() wasn't working
			elements.Button((77, 23), 'Quit', lambda: os._exit(0))
		]
		self.btnmgr = elements.ButtonManager(buttons, screen)
		self.btnmgr.activate()
		self.draw()

	def draw(self):
		#Draw the explanatory info
		self.screen.clear()
		self.screen.text((2, 1), "Use the arrow keys to navigate.")
		self.screen.text((2, 2), "Press shift to use.")
		#Draw the buttons
		self.btnmgr.draw()
		self.screen.show()