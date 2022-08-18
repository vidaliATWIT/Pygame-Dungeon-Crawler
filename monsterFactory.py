import random 
from being import monster
import enum

class monsterFactory():
	
	def createMonster(self, name, hd, dmg, ac, atk, spd, arc, sprite_file):
		return monster(name, self.getHpFromHd(hd), 0,0,0, ac, hd, dmg, sprite_file)
		
	def getHpFromHd(self, hd):
		max_hp=8*hd
		return random.randint(1*hd, max_hp)
	
	def getGoblin(self):
		return self.createMonster("Goblin", 1, 6, 13, atk=12, spd=9, arc=5, sprite_file='images/goblin.png')
	
	def getHarpy(self):
		return self.createMonster("Harpy", 3, 10, 12, atk=9, spd=14, arc=10, sprite_file='images/pixie.png') 
	
	def getLizard(self):
		return self.createMonster("Lizard", 1, 6, 12, atk=12, spd=7, arc=10, sprite_file='images/lizard.png')
	
	def getGhost(self):
		return self.createMonster("Ghost", 1, 8, 8, atk=13, spd=3, arc=15, sprite_file='images/ghost.png')
	
	def getBarbarian(self):
		return self.createMonster("Barbarian", 2, 10, 8, atk=15, spd=3, arc=3, sprite_file='images/barbarian.png')
	
	def getGoatman(self):
		return self.createMonster("Goatman", 2, 6, 12, atk=10, spd=10, arc=10, sprite_file='images/goatman.png')
		
		
	def getMonstersAtLevel(self, i):
		"""
		Returns a party of monster of adequate level for player character.
		"""
		outList = []
		if (i>=1):
			outList+=[self.getLizard(), self.getGoblin(), self.getGhost(), self.getLizard(), self.getHarpy()]
		if (i>=2):
			outList+=[self.getBarbarian(), self.getGoatman()]
		return outList
	
	

	def getListOfMonsters():
		'''
		Returns a list of all monsters
		'''
		mf = monsterFactory()
		return [mf.getLizard(), mf.getGoblin(), mf.getHarpy(), mf.getGhost(), mf.getHarpy(), mf.getBarbarian(), mf.getGoatman()]

class MonsterNames(enum.Enum):
	Goblin="Goblin"
	Harpy="Harpy"
	Lizard="Lizard"
		

def main(args):
	monfac = monsterFactory()
	gob = monfac.getHarpy()
	print("{0} attacked for {1} dmg! His AC was {2} WOW!".format(gob.getName(), gob.getDmg(), gob.getAc()))
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
