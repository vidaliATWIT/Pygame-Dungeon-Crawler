from game_map import MapLevel 
import tile
from view import micro_view 
import enum
import time

class game_controller():
	
	def __init__(self):
		self.pc_x=2
		self.pc_y=1
		self.direction=DIR.NORTH
		self.map = MapLevel()
		self.gameView = micro_view()
		self.rotation_grid = {(DIR.NORTH, 'r'):DIR.EAST, (DIR.NORTH, 'l'):DIR.WEST, #Rotation grid for easy reference to rotate pc
							  (DIR.SOUTH, 'r'):DIR.WEST, (DIR.SOUTH, 'l'):DIR.EAST,
							  (DIR.EAST, 'r'):DIR.SOUTH, (DIR.EAST, 'l'):DIR.NORTH,
							  (DIR.WEST, 'r'):DIR.NORTH, (DIR.WEST, 'l'):DIR.SOUTH}
	
	def render(self):
		"""
		handles rendering dungeon
		"""
		self.gameView.screen.fill((0,0,0))
		x = self.pc_x
		y = self.pc_y
		
		#outDict = self.getRelativeDistance(x,y, self.direction)
		outDict = self.altGetRelative(x,y, self.direction)
	
		for val in outDict:
			this_tile = outDict.get(val)
			if this_tile.getType()==tile.TileType.Wall:
				self.gameView.render_wall_tile(val, this_tile.getTrim().value)
			elif this_tile.getType()==tile.TileType.Floor:
				self.gameView.render_ground_tile(val, this_tile.getTrim().value, 'g_stone_ceil')
		self.gameView.screen_display.update()
		
	def altGetRelative(self, x, y, direction):
		"""
		Given the pc's position will return a dict of tiles whose keys are the relative positions from the player
		The values are the tiles surrounding the player
		"""
		i, i_start=-2, -2
		j, j_start=-3, -3
		i_end = 3
		j_end = 1
		
		outDict = {}
		tile = ""
		
		while (j<1):
			i=i_start
			while (i<3):
				get_x, get_y = self.transformRelativePositions(x, y, i, j, direction)
				if (get_x, get_y) in self.map.levelMap:
					tile = self.map.levelMap.get((get_x, get_y))
					outDict[(i, j)] = tile
				i+=1
			j+=1
		return self.prepareTileDict(outDict)
		
	def transformRelativePositions(self, x, y, i, j, direction):
		"""
		Helper method to handle getting correct updated x,y values depending on rotation.
		Used in rendering and movement
		"""
		if direction==DIR.SOUTH:
			i, j = i*-1, j*-1 # flip the signs
		elif direction==DIR.EAST:
			i, j = j*-1, i # flip i and j, flip sign for j
		elif direction==DIR.WEST:
			i, j = j, i*-1 # flip i and j, flip sign for i
		return (x+i, y+j)
	
	def prepareTileDict(self, tile_dict):
		"""
		Orders the dictionary containing the tiles to render so that it follows the order, Left, Right, Center
		This permits rendering to happen in the correct order
		"""
		
		#step 1: get left limit and right limit
		min_y, min_x, max_x = min(tile_dict.keys())[1], min(tile_dict.keys())[0], max(tile_dict.keys())[0] 
		left_limit = min_x
		right_limit = max_x
		back_limit = 0
		front_limit= min_y
		
		out_dict = {}
		
		print(max(tile_dict.keys()))
		
		kx = min_x
		print("From left to 0")
		while kx<0: #from left limit to 0
			ky=min_y
			while ky<=0: #from back to front
				print(str(kx)+":"+str(ky))
				out_dict[(kx, ky)] = tile_dict.pop((kx,ky))
				ky+=1
			kx+=1
		kx = max_x
		print("From right to 0")
		while kx>0: #from right limit to 0
			ky=min_y
			while ky <= 0:
				print(str(kx)+":"+str(ky))
				out_dict[(kx, ky)] = tile_dict.pop((kx,ky))
				ky+=1
			kx-=1
		ky=min_y
		while ky <=0: #all 0 values
			out_dict[(0, ky)] = tile_dict.pop((0,ky))
			ky+=1
		tile_dict = out_dict
		return tile_dict
	
	def movePc(self, x, y):
		new_x, new_y =self.transformRelativePositions(self.pc_x, self.pc_y, x, y, self.direction)
		if self.map.getTileAt(new_x, new_y).isWalkable():
			self.pc_x, self.pc_y=new_x, new_y
	
	def rotatePc(self, way='r'):
		self.direction = self.rotation_grid.get((self.direction, way))
			
	def getPygame(self):
		return self.gameView.pygame

class DIR(enum.Enum):
	NORTH="N"
	SOUTH="S"
	EAST="E"
	WEST="W"

def main(args):
	g_con = game_controller()
	
	g_con.render()
	##time.sleep(5)
	while True:	
		for event in g_con.getPygame().event.get():
			if event.type==g_con.getPygame().KEYDOWN:
				x,y = 0,0
				if event.key==g_con.getPygame().K_w:
					y=-1
				elif event.key==g_con.getPygame().K_s:
					y=1
				elif event.key==g_con.getPygame().K_a:
					x=-1
				elif event.key==g_con.getPygame().K_d:
					x=1
				elif event.key==g_con.getPygame().K_q: #test for rotation
					g_con.rotatePc('l')
				elif event.key==g_con.getPygame().K_e:
					g_con.rotatePc('r')
				if x!=0 or y!=0:
					g_con.movePc(x, y)
				g_con.render()
	
	#while True:
	#	print("")
	#	g_con.render()
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
