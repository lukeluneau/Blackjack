'''
FUCNTIONALITY

Players play hands
	
Types of Play:
	Automatic
	Manual

Play Strategies:
	House Rules
	Counting Cards
	Random
	Risky

Additional Stuff:
	Splitting Hands
	21 Bonus

Player Attributes:
	Purse
	Strategy (allow to change?)
	Name
	Drunk


To Do:
	Split Hand
	Cleanup UI
	How to handle money
	Bot use
	Use a NN and try to have it learn an optimal strategy?

'''

import responses
from deck import *
from player import *
from house import *
from strategies import *

if __name__ == '__main__':

	p = Player('Luke', 
					  1000, 
					  standard_strategy, 
					  10)

	house = House()
	house.add_player(p)
	# p.get_hand()
	house.deal(p)



			


