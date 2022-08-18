import enum
class Tile():
	def __init__(self, name, trim):
		self.name=name
		self.trim=trim
		self.walkable=True
		self.locked=False
		self.t_type = None
	
	def isWalkable(self):
		return self.walkable
	def getTrim(self):
		return self.trim
	def getName(self):
		return self.name
	def isLocked(self):
		return self.locked
	def getType(self):
		return self.t_type
	def onEnter(self, param):
		pass
class Wall(Tile):
	def __init__(self, name, trim):
		Tile.__init__(self, name, trim)
		self.walkable=False
		self.t_type = TileType.Wall

class Floor(Tile):
	def __init__(self, name, trim, item=''):
		Tile.__init__(self, name, trim)
		self.t_type = TileType.Floor
		self.item=item
		
	def hasItem(self):
		return self.item!=''

	def getItem(self):
		return self.item
		
	def setItem(self, i):
		self.item=i
	
	def onEnter(self, eState):
		'''
		If there's an item here add it to the PC. 
		Then clear item to prevent duplicates.
		Return info confirming PC has found item string.
		'''
		pc = eState.getPC()[0]
		outStr=''
		if self.hasItem():
			pc.addItem(self.getItem())
			outStr = pc.getName() + " found a " + self.item.getName()
			self.item=''
		print(outStr)
		return outStr
		
class Door(Tile):
	def __init__(self, name, trim, locked_flag=False):
		Tile.__init__(self, name, trim)
		self.locked=locked_flag
		self.t_type = TileType.Door
	
	def onEnter(self, eState):
		'''If door is locked check if PC has key, if so unlock'''
		pc = eState.getPC()[0]
		if self.locked:
			if pc.hasKey():
				self.locked=False
				return "You've unlocked the door"
			else:
				return "The door is locked!"
		return ""
	
	def isWalkable(self):
		'''If unlocked, it is walkable'''
		return not self.locked

class Terminal(Tile):
	'''Returns a note upon collide'''
	def __init__(self, name, trim, text):
		Tile.__init__(self,name,trim)
		self.t_type = TileType.Term
		self.text=text
		self.walkable=False
	
	def onEnter(self,eState):
		'''return string associated with this terminal'''
		return self.text

class Exit(Tile):
	'''Exits game when walked over'''
	def __init__(self,name,trim):
		Tile.__init__(self,name,trim)
		self.t_type=TileType.Door
		self.walkable=False
	def onEnter(self,eState):
		'''Set explore flag to true'''
		eState.gameOverHelper()
		return ''

class Trim(enum.Enum):
	g_stone_wall="g_stone_wall"
	g_stone_ceil="g_stone_ceil"
	g_stone_floor="g_stone_floor"
	g_stone_door="g_stone_door"
	tech1_wall='tech1_wall'
	tech1_floor='tech1_floor'
	tech1_ceil='tech1_ceil'
	tech1_door='tech1_door'
	tech1_term='tech1_term'
	
class TileType(enum.Enum):
	Wall="WALL"
	Floor="FLOOR"
	Door="DOOR"
	Term="TERM"
	
def main(args):
	
	floor = Floor("Stone Floor", Trim.g_stone_floor)
	wall = Wall("Stone Wall", Trim.g_stone_wall)
	door = Door("Stone Door", Trim.g_stone_door)
	
	for tile in [floor, wall, door]:
		print("Tile is: " + tile.getName() + " " + repr(tile.getTrim()) + " " + str(tile.isWalkable()) + " " + str(type(tile)))
	
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
