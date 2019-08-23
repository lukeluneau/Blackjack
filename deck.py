import random

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

def get_deck_mapping():
	return DECK

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