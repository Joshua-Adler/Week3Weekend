import time

import graphics
import pages

#Make sure the terminal is the right size
graphics.set_terminal_size((120, 30))
#The screen has to be 2 chars shorter than the actual terminal because the terminal adds extra newlines on the bottom
screen = graphics.Screen((120, 28))

#Start up the main menu
pages.Menu(screen)

#A little bit hacky, but it keeps the program running while it awaits user input
#It also means that you can't play Blackjack for 278 days straight >:)
time.sleep(1e6)