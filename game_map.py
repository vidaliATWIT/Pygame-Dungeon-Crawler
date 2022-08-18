import tile
from item import Item

class MapLevel():
	def __init__(self, width=20, length=20, wall_trim="", floor_trim="", door_trim=""):
		self.wall_trim = tile.Trim.tech1_wall
		self.floor_trim = tile.Trim.tech1_floor
		self.ceiling_trim = tile.Trim.tech1_ceil
		self.door_trim = tile.Trim.tech1_door
		self.term_trim=tile.Trim.tech1_term
		string_map =["wwwwwwwwwwwwwwwwwwww",
					 "wkffff0wfffffffffffw",
			    	 "wwlwwwwwwwwwwwwffffw",
					 "wffwwwwffffffffffffw",
				     "wwfwwwwfwwwwwwwfwffw",
					 "wfffffffwfffffffwffw",
					 "wwwwwwfwkffffffffffw",
					 "wfwwwwfwwwwwwwwwwwww",
			     	 "wfwwwwfwfffffffffffw",
					 "wwwwwwfwfwwwwwwwwwww",
					 "wffffwfwfwffffwwfffw",
					 "wwffwwfwfwfwfffffwfw",
					 "wffffwfwfwfwfffffwfw",
			  	     "wffffffffwfwfffffwfw",
			         "wfwwwwwwwwwwwwdwwwww",
				     "wfffffffflfffffffffw",
					 "wwwwwwwwwwwwwwdwwwww",
					 "wwwwwwwwwwwwwwfwfffw",
					 "wefffffffffffffwfffw",
					 "wwwwwwwwwwwwwwwwwwww"]
		self.width = len(string_map[0])
		self.height = len(string_map)
		self.levelMap = self.generateMapArray(string_map)
	
	def generateMapArray(self, mapList):
		"""
		Takes human readable map and converts it into a 2D array of tiles.
		"""
		i, j = 0,0
		levelMap = {}
		for line in mapList:
			i = 0
			for char in line:
					if char=='w':
						in_tile = tile.Wall("Wall", self.wall_trim)
					elif char=='f':
						in_tile = tile.Floor("Floor", self.floor_trim)
					elif char=='d':
						in_tile = tile.Door("Door", self.door_trim)
					elif char=='k': #key
						in_tile = tile.Floor("Floor", self.floor_trim, Item("Key", 10))
					elif char=='l': #locked door
						in_tile = tile.Door("Locked Door", self.door_trim, True) 
					elif char.isdigit() or char=='t': #terminal
						in_tile = tile.Terminal("Term", self.term_trim, self.getNote(char))
					elif char=='e':
						in_tile = tile.Exit("Exit",self.door_trim)
					levelMap[(i, j)]= in_tile
					i+=1
			j+=1
		return levelMap
	
	def getTileAt(self, x, y):
		return self.levelMap.get((x,y))
	
	def setTileAt(self, x, y, tile):
		self.levelMap[(x,y)]=tile
	
	def getNote(self, char):
		if char=='0':
			return "Find a key to unlock the door."
		elif char=='1':
			return "You must escape to the podbay!"
		elif char=='2':
			return "You'll have to find another key"
			
def main(args):
	gmap = MapLevel()
	
	for i in range(gmap.height):
		for j in range(gmap.width):
			print(gmap.getTileAt(j, i).name)

	#gmap.getRelativeDistance(5, 5, "N")
	#gmap.directionTest(2,2, "W")
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
