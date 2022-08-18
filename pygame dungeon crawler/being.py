from action import ActionType
class being():
	
	def __init__(self, name, hp, atk, spd, arc, ac, hd):
		self.name=name
		self.atk=atk
		self.spd=spd
		self.arc=arc
		self.ac=ac
		self.dmg=1
		self.hd=hd
		self.hp=hp
		self.max_hp=hp
		self.def_bonus=0
		self.atk_bonus=0
		self.defending=False
	
	def getName(self):
		return self.name
	def getHp(self):
		return self.hp
	def setHp(self, hp):
		self.hp=hp
	def getAtk(self):
		return self.atk + self.atk_bonus
	def getSpd(self):
		return self.spd
	def getArc(self):
		return self.arc
	def getAc(self):
		return self.ac + self.def_bonus
	def setAc(self):
		return self.ac
	def getDmg(self):
		return self.dmg
	def setDmg(self, dmg):
		self.dmg = dmg
	def getDefBonus(self):
		return self.def_bonus
	def setDefBonus(self, bonus):
		self.def_bonus = bonus
	def getAtkBonus(self):
		return self.atk
	def setAtkBonus(self, bonus):
		self.atk_bonus=bonus
	def getModifier(value):
		return self.modArray[value]
	def getHd(self):
		return self.hd
	def incHp(self, hp): ##increase hp
		self.hp = min(self.hp+hp, self.max_hp)
	def redHp(self, hp): ##reduce hp
		self.hp = max(0, self.hp-hp)
	def isDefending(self):
		return self.defending
	def setDefending(self, state):
		self.defending=state
		if state:
			self.def_bonus=3
		else:
			self.def_bonus=0
	def isDead(self):
		return self.hp<=0
	
		
class monster(being):
	def __init__(self, name, hp, atk, spd, arc, ac, hd, dmg, sprite_file):
		being.__init__(self, name, hp, atk, spd, arc, ac, hd)
		self.dmg=dmg
		self.sprite_file=sprite_file
	def getSpriteFile(self):
		return self.sprite_file

class pc(being):
	def __init__(self, name, hp, atk, spd, arc, ac, hd):
		being.__init__(self, name, hp, atk, spd, arc, ac, hd)
		self.level=1
		self.xp=0
		self.dmg = 8
		self.inventory = {}
	
	def getLevel(self):
		return self.level
	def setLevel(self, level):
		self.level=level
	def incLevel(self):
		self.level+=1
	def getXp(self):
		return self.xp
	def setXp(self, xp):
		self.xp=xp
	def incXp(self, xp):
		self.xp+=xp
	def getActions(self):
		'''
		Return a list of valid actions for this character
		'''
		return [ActionType.fight, ActionType.defend, ActionType.run]
	
	def addItem(self, item):
		self.inventory[item.getName()] = item
	def removeItem(self, item):
		if self.inventory.contains(item.getName()):
			self.inventory.remove(item.getName())
		else:
			print("Item not in inventory")

	
	def hasKey(self):
		return "Key" in self.inventory
	
	def getInvenory(self):
		return self.inventory
	
	
	
def main(args):
	johnPc = pc("John", 10, 13, 13, 13, 16, 8)
	johnPc.redHp(20)
	monsterMan = monster("Goblin", 10, 13, 13, 13, 12, 8, 5, "image")
	beingList = [johnPc, monsterMan]
	
	for being in beingList:
		print('{0} {1} {2} {3} {4}'.format(being.getName(), being.getHp(), being.getAtk(), being.getSpd(), being.getArc()))
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
