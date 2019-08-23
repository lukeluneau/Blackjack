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