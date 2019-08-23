from deck import *
from house import *
from strategies import *

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

