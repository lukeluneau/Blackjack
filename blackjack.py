'''
FUCNTIONALITY

Players play hands
	test insert
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
import random
import string
import time

DECK = {}
SUITS = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
FACES = ['Jack', 'Queen', 'King', 'Ace']
CARDS = list(range(2,11)) + FACES
for card in CARDS:
	for suit in SUITS:
		if (card in FACES) and (card != 'Ace'):
			DECK['%s of %s' % (card, suit)] = 10
		
		# elif card == 'Ace':
		else:
			DECK['%s of %s' % (card, suit)] = card

NO = set(['no', 'n'])
YES = set(['y', 'yes', 'yee'])

def new_deck(size):
	'''
	Create a new deck dictionary containing the number of
	decks, SIZE.
	size: number of decks
	returns: dictionary of cards
	'''
	new_deck = {}
	for i in range(size):
		for card, value in DECK.items():
			if card in new_deck.keys():
				new_deck[card] += 1
			else:
				new_deck[card] = 1
	return new_deck

def select_random_cards(deck, amount):
	'''
	Selects a random item from a dictionary, 
	decriments the items value by 1, and
	returns the item.
	deck: (dictionary) card:number of cards in the deck
	returns: (string) card
	'''
	items = []
	for item, value in deck.items():
		if value > 0:
			items.append(item)
	cards = []
	for i in range(amount):
		choice = random.choice(items)
		value = deck[choice]
		deck[choice] -= 1
		if value == 0:
			del deck[choice]
		cards.append(choice)
	return cards


class House():
	def __init__(self, table_min=10, table_max=5000, deck_size=1):
		self.table_min = table_min
		self.table_max = table_max
		self.deck_size = deck_size

		self.players = []
		self.winnings = 0
		self.deck = None
		self.get_deck()

	
	def get_deck(self):
		self.deck = new_deck(self.deck_size)

	def add_player(self, player):
		self.players.append(player)

	def deal(self, player, replay=False, recommendations=False):
		# Introduction
		print('-------------------------------')

		if not replay:
			print('Would you like to play a hand?')
			player_input = input('Y or N?')

			if player_input.lower() == 'n':
				print('Quitter')
				return
			else:
				print('Let\'s play...')
			print()


		# Show a dealer card
		dealer_hand = select_random_cards(self.deck, 2)
		print('Dealer shows card:', dealer_hand[0])
		print()

		# Player starts with their cards
		player.new_hand(select_random_cards(self.deck, 2))
		print('Your cards are:', player.get_hand())
		print()

		# Check if the player won
		if player.get_hand_score() == 21:
			player.win()
			print('Winner Winner Chicken Dinner!')
			print()
			return self.replay(player, True)

		# While loop
		# Player decides if they want to hit, stay, or bust

		# Implement handle split
		current_hand = player.get_hand()
		c1, c2 = current_hand[0], current_hand[1]
		# sp = False
		if DECK[c1] == DECK[c2]:
			split_hands = input('Do you want to split hands?')
			if split_hands in YES:
				player.split_hand()

		playing_hands = 1 if not player.split else 2

		for h in range(playing_hands):
			next_move = self.ask_player_to_hit(player.get_hand(h), recommendations)
			while next_move and player.get_hand_score(h) < 21:
				next_card = select_random_cards(self.deck, 1)
				player.hit(next_card[0], h)

				print('Your cards are:', player.get_hand(h))
				print()

				# Check Player Bust
				if player.get_hand_score(h) > 21:
					player.lose()
					print('You BUSTED, loser.')
					print()
					return self.replay(player, True)

				next_move = self.ask_player_to_hit(player.get_hand(h), recommendations)

		# Dealer shows their cards
		print('Dealer Cards:', dealer_hand)
		print()

		while count_hand(dealer_hand) < 17:
			dealer_hand.append(select_random_cards(self.deck, 1)[0])
			print('Dealer Cards:', dealer_hand)
			print()
			time.sleep(2)

		if count_hand(dealer_hand) > 21:
			player.win()
			print('The Dealer BUSTED!  YOU WIN.')
			print()
			
		for h in range(playing_hands):

			if count_hand(dealer_hand) < player.get_hand_score(h):
				player.win()
				print('You beat the Dealer!')
				print()
				

			else:
				player.lose()
				print('You lost to the Dealer.')
				print()

		self.replay(player, True)

	def ask_player_to_hit(self, hand=None, h=0, recommendations=False):
		if recommendations and hand != None:
			standard_strategy(hand[h])
		player_input = input('Would you like to hit? ')
		if player_input.lower() in NO:
			print('Ok')
			print()
			return False
		return True

	def replay(self, player, again):
		player_input = input('Would you like to replay? ')
		if player_input.lower() in NO:
			print('Bye...')
			print()
		else:
			return self.deal(player, again)
		
	def print_deck(self):
		''' trouble shooting ''' 
		print(self.deck)



class Player():
	def __init__(self, name, purse, strategy, bet):
		self.name = name
		self.purse, self.initial = purse, purse
		self.strategy = strategy
		self.winnings = 0
		self.bet = bet
		self.hand = []
		self.split = False
	def get_name(self):
		return self.name
	def get_strategy(self):
		return self.strategy
	def get_hand(self, h=0):
		return self.hand[h][:]
	def get_hand_score(self, h=0):
		return count_hand(self.hand[h])
	def new_hand(self, cards):
		self.hand = [cards]
	def hit(self, card, h=0):
		self.hand[h].append(card)
	def split_hand(self):
		self.hand = [[self.hand[0][0]],[self.hand[0][1]]]
		self.split = True
	def win(self):
		self.purse += self.bet
	def lose(self):
		self.purse -= self.bet




def count_hand(hand, bust=22):
	count = 0
	aces = 0
	for card in hand:
		value = DECK[card]
		if isinstance(value, int):
			count += value
		else:
			aces += 1
	while count < (bust -  11) and aces > 0:
		count += 11
		aces -= 1
	while aces > 0:
		count += 1
		aces -= 1
	return count



def standard_strategy(hand):
	'''
	Hit on 16, Hold on 17
	'''
	ChickenDinner = 21 # Can change to see how outcomes change

	count = count_hand(ChickenDinner+1)

	# Should never be this case
	if count > ChickenDinner:
		# Busted
		return -1

	if count > (ChickenDinner - 5):
		# Stand
		print('I recommend that you stay.')
		print()
		return 0

	# Hit
	print('I recommend that you hit.')
	print()
	return 1



if __name__ == '__main__':

	p = Player('Luke', 
					  1000, 
					  standard_strategy, 
					  10)

	house = House()
	house.add_player(p)
	# p.get_hand()
	house.deal(p)



			


