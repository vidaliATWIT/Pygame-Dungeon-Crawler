from state_machine import StateMachine as StateMachine, IState as IState, combatState as combatState, StateEnum as StateEnum, CombatGlob as CombatGlob, gameOverState as gameOverState
from view import micro_view 
from game_map import MapLevel 
from dmutil import dmutil
import tile
import enum
from monsterFactory import monsterFactory as mf
from being import pc as pc
from tile import TileType

class ExploreState(IState):
	def __init__(self, state_machine, view=""):
		self.pc = []
		self.pc_x=2
		self.pc_y=1
		self.direction=DIR.NORTH
		self.rotation_grid = {(DIR.NORTH, 'r'):DIR.EAST, (DIR.NORTH, 'l'):DIR.WEST, #Rotation grid for easy reference to rotate pc
							  (DIR.SOUTH, 'r'):DIR.WEST, (DIR.SOUTH, 'l'):DIR.EAST,
							  (DIR.EAST, 'r'):DIR.SOUTH, (DIR.EAST, 'l'):DIR.NORTH,
							  (DIR.WEST, 'r'):DIR.NORTH, (DIR.WEST, 'l'):DIR.SOUTH}
		self.gameView = view
		self.map = MapLevel()
		self.isStateOver=False
		self.gStateMachine=state_machine
		self.mf = mf()
		self.turn=0
		self.info_str='' ##when something happens render this		
	def Update(self):
		"""Update current state"""
		print(self.pc[0].getInvenory())
		self.turn+=1
		if self.randomEncounter():
			##we need to generate monsters here
			monsters = self.mf.getMonstersAtLevel(self.pc[0].getLevel())
			print(self.pc[0].getLevel())
			print(monsters)
			self.glob = CombatGlob(self.pc, [monsters[dmutil.roll(5)-1]])
			self.gStateMachine.Change(StateEnum.combat,self.glob)
		
	def Render(self):
		"""
		Render dungeon given current position
		"""
		self.gameView.screen.fill((0,0,0))
		x = self.pc_x
		y = self.pc_y

		outDict = self.altGetRelative(x,y, self.direction)
	
		for val in outDict: ##this loop has to contain all the tile types you will have to render
			this_tile = outDict.get(val)
			if this_tile.getType()==tile.TileType.Wall or this_tile.getType()==tile.TileType.Term or this_tile.getType()==tile.TileType.Door:
				self.gameView.render_wall_tile(val, this_tile.getTrim().value)
			elif this_tile.getType()==tile.TileType.Floor:
				##parse tile.trim and switch from floor to ceil
				tilestring = this_tile.getTrim().value.split("_")[0] + "_ceil"
				self.gameView.render_ground_tile(val, this_tile.getTrim().value, tilestring)
		if self.hasInfoString():
			self.gameView.renderInfo(self.info_str)
			self.info_str=''
		self.gameView.screen_display.update()
	
	def OnEnter(self, glob):
		self.pc = glob.pc()
		self.glob=glob
		self.isStateOver=False
	
	def ProcessInput(self, inp):
		"""
		Take player input and process effect
		"""
		x,y =0,0
		if inp=='w':
			y=-1
		if inp=='a':
			x=-1
		if inp=='s':
			y=1
		if inp=='d':
			x=1
		if inp=='r' or inp=='l':
			self.rotatePc(inp)
		if (x!=0 or y!=0):
			self.movePc(x,y)
		
	
	def OnExit(self):
		self.turn=0
	
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
		newTile =  self.map.getTileAt(new_x, new_y)
		if newTile.isWalkable():
			self.pc_x, self.pc_y=new_x, new_y
			if newTile.getType()==TileType.Door:
				self.movePc(x,y)  
		self.onEnterHelper(newTile.onEnter(self)) ##call newTile OnEnter and then pass the return string as argument to the helper
	
	def rotatePc(self, way='r'):
		self.direction = self.rotation_grid.get((self.direction, way))
	
	def randomEncounter(self):
		"""
		Rolls 6 turns returns a 1/6 chance to see if a random encounter happens
		"""
		if (self.turn%6==5): ##it will never trigger
			return (dmutil.roll(6)==1)
			
	def getView(self):
		return self.gameView
	
	def onEnterHelper(self, returnStr):
		'''Handles setting info_str variable if needed'''
		if returnStr!='' and returnStr!=None: ##we need to streamline this by either not returning when not necessary or always returning '' when no info_string is returned
			self.info_str=returnStr
	
	def hasInfoString(self):
		'''Checks if our info_string is anything but empty'''
		return self.info_str!=''
	
	def isGameOver(self):
		'''Checks if pc is dead or if exit has been reached'''
		return self.pc[0].isDead()
	
	def setExitFlag(self, boolv):
		self.exitFlag=boolv
	
	def getExitFlag(self):
		return self.exitFlag
	
	def getPC(self):
		return self.pc
	
	def getStateMachine(self):
		return self.gStateMachine
	
	def gameOverHelper(self):
		'''Helper method to allow other classes to trigger a game over state change'''
		self.gStateMachine.Change(StateEnum.gameOver,True)

class DIR(enum.Enum):
	NORTH="N"
	SOUTH="S"
	EAST="E"
	WEST="W"
		
def main(args):
	view = micro_view()
	monFac = mf()
	gStateMachine = StateMachine(view)
	gStateMachine.Add(StateEnum.explore, ExploreState(gStateMachine, view))
	gStateMachine.Add(StateEnum.combat, combatState(gStateMachine, view))
	gStateMachine.Add(StateEnum.gameOver, gameOverState(gStateMachine, view))
	#gStateMachine.Change(StateEnum.explore, {'pc':[pc("Jeb",20,20,20,20,20,20)]})
	glob = CombatGlob([pc("Jeb",10,10,10,10,10,10)], [monFac.getLizard()])
	gStateMachine.Change(StateEnum.explore, glob)
	viewFlag=True
	pg = view.pygame
	while not gStateMachine.isGameOver():	
		if viewFlag:
			gStateMachine.Render()
			viewFlag=False
		for event in pg.event.get():
			if event.type==pg.KEYDOWN:
				viewFlag=True
				inp=''
				if event.key==pg.K_w:
					inp='w'
				elif event.key==pg.K_s:
					inp='s'
				elif event.key==pg.K_a:
					inp='a'
				elif event.key==pg.K_d:
					inp='d'
				elif event.key==pg.K_q:
					inp='l'
				elif event.key==pg.K_e:
					inp='r'
				elif event.key==pg.K_f:
					inp='f'
				elif event.key==pg.K_r:
					inp='r'
				elif event.key==pg.K_0:
					inp='0'
				elif event.key==pg.K_1:
					inp='1'
				elif event.key==pg.K_2:
					inp='2'
				gStateMachine.ProcessInput(inp)
				gStateMachine.Update()
				
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
