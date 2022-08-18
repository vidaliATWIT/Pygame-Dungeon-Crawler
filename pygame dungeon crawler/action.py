from dmutil import dmutil as dmutil
import enum
class Action():
	def __init__(self, owner="", opponent=""):
		self.owner=owner
		self.opponent=opponent
		self.target_action=False
	
	def execute(self):
		pass
	
	def isTargetAction(self):
		return self.target_action
		
	def setOwner(self, owner):
		self.owner=owner
	def setOpponent(self, opponent):
		self.opponent=opponent
	def getOwner(self):
		return self.owner
	def getOpponent(self):
		return self.opponent
	
class Attack(Action):
	def __init__(self, owner, opponent=""):
		super().__init__(owner, opponent)
		self.hit=False #bool
		self.dmg=0 #random dmg
		self.target_action=True
	
	def execute(self):
		self.owner.setDefending(False)
		dmg = dmutil.roll(self.owner.getDmg())
		###Rolls over opponent ac, adds owner attack mod and atk bonus to roll
		hitflag = dmutil.rollOver(d=20, target=self.opponent.getAc(), mod=(dmutil.getMod(self.owner.getAtk())+self.owner.getAtkBonus()))
		if (hitflag):
			self.opponent.redHp(dmg)
			return('{0} hit {1} for {2} points of damage!'.format(self.owner.getName(), self.opponent.getName(), dmg))
		else:
			return('{0} missed!'.format(self.owner.getName()))

class Defend(Action):
	def __init__(self, owner):
		super().__init__(owner, "none")
	
	def execute(self):
		self.owner.defending=True
		return ('{0} is defending!'.format(self.owner.getName()))

class Run(Action):
	def __init__(self, owner):
		super().__init__(owner, "none")
	
	def execute(self):
		if (dmutil.rollUnder(20, self.owner.getSpd())):
			return ('{0} ran away!'.format(self.owner.getName()))
		else:
			return ('{0} could not escape!'.format(self.owner.getName()))

class ActionType(enum.Enum):
	fight="F)ight"
	run="R)un"
	defend="D)efend"

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
