import deck
import player
import strategies 
import responses
import string
import time

# TODO: make a better way to get responses
NO = set(['no', 'n'])
YES = set(['y', 'yes', 'yee'])

# get general deck mapping card->value pairs
DECK = deck.get_deck_mapping()

class House():
	def __init__(self, table_min=10, table_max=5000, deck_size=1):
		self.table_min = table_min
		self.table_max = table_max
		self.deck_size = deck_size

		self.players = []
		self.winnings = 0
		self.deck = None
		self.get_new_deck()

	
	def get_new_deck(self):
		self.deck = deck.new_deck(self.deck_size)

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

		if len(self.deck) < 10:
			self.get_new_deck()

		# Show a dealer card
		dealer_hand = deck.select_random_cards(self.deck, 2)
		print('Dealer shows card:', dealer_hand[0])
		print()

		# Player starts with their cards
		player.new_hand(deck.select_random_cards(self.deck, 2))
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
		if deck.splittable(c1, c2):
			split_hands = input('Do you want to split hands?')
			if split_hands in YES:
				player.split_hand()

		playing_hands = 1 if not player.split else 2

		for h in range(playing_hands):
			next_move = self.ask_player_to_hit(player.get_hand(h), recommendations)
			while next_move and player.get_hand_score(h) < 21:
				next_card = deck.select_random_cards(self.deck, 1)
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
			dealer_hand.append(deck.select_random_cards(self.deck, 1)[0])
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
			strategies.standard_strategy(hand[h])
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

# TODO: move into another class
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