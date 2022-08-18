import random


class dmutil():
	'''
	Dungeon Master's Utility:
	Collects all useful functions and tables needed to 
	effectively run game and all pertinent mechanics.
	e.g. rolling, retrieving ability modifiers etc.
	'''
	mod_chart= [-5,-5,-4,-4,-3,-3,-2,-2, #0-7
				-1,-1, 0, 0, 1, 1, 2, 2, #8-15
				 3, 3, 4, 4, 5, 5, 6, 6] #15-23
	
	@staticmethod
	def roll(i):
		'''General purpose roll method'''
		return random.randint(1, i)
	
	@staticmethod
	def rollUnder(d, target):
		'''Method to roll under target'''
		return random.randint(1,d)<target
	
	@staticmethod
	def rollOver(d, target, mod=0):
		'''Roll over method'''
		return random.randint(1,d)+mod>target
	
	@staticmethod
	def getMod(stat):
		if (stat<len(dmutil.mod_chart) and stat>0):
			return dmutil.mod_chart[stat]
		return -1

def main(args):
	print(dmutil.rollUnder(20, 15))
	print(dmutil.getMod(3))

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
