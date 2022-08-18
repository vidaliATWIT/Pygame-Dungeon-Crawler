import enum
import being
import action
import random
import monsterFactory 
import view
from action import ActionType

"""General purpose classes"""

class StateMachine:
	
	def __init__(self, view=""):
		self.mCurrentState=None
		self.mStates = {}
		self.view=view
	
	def Update(self):
		"""Update game state after user input"""
		self.mCurrentState.Update()
		
	def Render(self):
		"""Render correct display given current state"""
		self.mCurrentState.Render()

	def Change(self, stateName, glob=""):
		"""Change current state to a different one"""
		if (self.mCurrentState!=None):
			self.mCurrentState.OnExit()
		self.mCurrentState = self.mStates[stateName]
		self.mCurrentState.OnEnter(glob)
	
	def ProcessInput(self, inp):
		"""Take user input"""
		self.mCurrentState.ProcessInput(inp)
	
	def Add(self, name, state):
		"""
		Add a new state to the machine
		Used during initialization of state machine
		"""
		self.mStates[name]=state
	
	def isGameOver(self):
		return self.mCurrentState.isGameOver()
	
	def getView(self):
		return self.view

class IState:
	def Update(self):
		"""Update current state"""
		pass
	def Render(self):
		"""Render for current state"""
		pass
	def OnEnter(self):
		"""Execute action when state is entered"""
		pass
	def ProcessInput(self):
		"""Process input"""
		pass
	def OnExit(self):
		"""Execute action when state is exited"""
		pass
	
	def isGameOver(self):
		"""Verify if game is over"""
		pass
		

"""Combat Classes"""

class combatState(IState):
	def __init__(self, state_machine="", view=""):
		"""
		Instantiates all of the fields needed to run combat
		NOTE: All of these get passed by reference between this high-level combat-state
		and all of the sub-states: select_action, select_target, and execute
		"""
		self.mActions = [] 
		self.pc = []
		self.monsters = []
		self.mCombatStates = StateMachine() 
		self.gStateMachine = state_machine
		self.view=view
	
	def OnEnter(self, glob):
		"""
		On Enter, initialize the pc field and monsters field
		Add select_action, select_target, and execute states
		Then set the combatState to "select_action"
		"""
		self.pc = glob.pc()
		self.monsters = glob.monsters()
		self.mCombatStates.Add(StateEnum.decide, playerDecideState(self.mActions, self.mCombatStates, self.view))
		self.mCombatStates.Add(StateEnum.execute, executeState(self.mActions, self.mCombatStates, self.view))
		self.mCombatStates.Add(StateEnum.gameOver,gameOverState(self.mCombatStates, self.view))
		self.mCombatStates.Change(StateEnum.decide, glob)
		self.glob=glob
		self.round=0
	
	def Update(self):
		self.mCombatStates.Update()
		if (self.mCombatStates.mCurrentState.isCombatOver()):
			self.gStateMachine.Change(StateEnum.explore,self.glob)
		self.round+=1
		
	def Render(self):
		'''
		General function for rendering combat
		'''
		if not self.hasCombatBegan(): ##First round of combat
			print("You've been attacked")
			self.view.renderInfo("You've been attacked")
		else:
			
			self.view.renderCombatMenu()
			if len(self.monsters)>0: ##render enemy sprite if there are still enemies to render
				self.view.renderEnemySprite(self.monsters[0].getName())
			print(self.monsters)
			self.view.renderMonsterList(map(lambda x: x.getName(), self.monsters))
			self.mCombatStates.Render()
		self.view.screen_display.update()
	def ProcessInput(self, inp):
		if (self.hasCombatBegan()): ##Once round is not 0
			self.mCombatStates.ProcessInput(inp)
	
	def OnExit(self):
		pass
	
	def isGameOver(self):
		return self.mCombatStates.isGameOver()
	
	def hasCombatBegan(self):
		'''Helper method for checking if round is past 0'''
		return self.round!=0
		

class playerDecideState(IState):

	def __init__(self, action_queue, state_machine, view=""):
		self.action_queue=action_queue
		self.state_machine=state_machine
		self.pc = []
		self.monsters = []
		self.action = ""
		self.glob = ""
		self.isActionSelected=False
		self.isTargetSelected=False
		self.pcPointer = 0 ##Pointer for which index getActivePC will try
		self.view=view
		self.actionDict = {'f':ActionType.fight, 'd':ActionType.defend, 'r':ActionType.run}
	
	def OnEnter(self, glob):
		"""On enter, reset all fields"""
		self.pc = glob.pc()
		self.monsters = glob.monsters()
		self.glob=glob
		self.action_queue = []
		
	def Update(self):
		"""
		If action was taken, check if target action,
		else, change mode to execute
		"""
		if self.isActionSelected:
			if (not self.isTargetAction() or self.isTargetSelected):
				self.action_queue.append(self.action)
				self.cleanUpActionFields()
		
		if self.allActionsSet():
			self.glob.set_action_queue(self.action_queue)
			self.state_machine.Change(StateEnum.execute, self.glob)
				
				
	def Render(self):
		'''
		If action is not selected render possible actions, else render possible targets
		'''
		string_list = [(self.getActivePC().getName()+": ")]
		i=1
		print(self.getActivePC().getName())
		if (not self.isActionSelected):
			string_list+=map(lambda x: x.value, self.getActivePC().getActions())##this line returns a list of valid ActionType (enum) which are mapped to return the string value
		else:
			for mon in self.monsters:
				string_list.append(str(i) + ") " + mon.getName())
				print(mon.getName())
				i+=1
		print(string_list)
		self.view.renderOptions(string_list)
		
	def OnExit(self):
		self.cleanUpActionFields()
		self.pcPointer=0
	
	def ProcessInput(self, inp):
		"""Pass user input and generate action"""
		act=inp
		action_type = ""

		if (not self.isActionSelected): # If no action selected
			self.isActionSelected = True
			if act=="f" and self.isValidAction(inp):
				self.action = action.Attack(self.getActivePC())
			elif act=="d" and self.isValidAction(inp):
				self.action = action.Defend(self.getActivePC())
			elif act=="r" and self.isValidAction(inp):
				self.action = action.Run(self.getActivePC())
			else: ##Input/action was not valid
				self.isActionSelected=False
				print("No action selected")
				return
		elif (self.isTargetAction() and not self.isTargetSelected): ##If target action and target not selected
			if inp.isnumeric:
				act=int(inp)
				if (act<len(self.monsters) and act>=0):
					self.action.setOpponent(self.monsters[act])
					self.isTargetSelected=True
		else:
			print("invalid input")
	
	def isTargetAction(self):
		"""
		Helper method to verify whether the current action needs
		a target
		"""
		if self.action!="":
			return self.action.isTargetAction()
	
	def getActivePC(self):
		"""Returns the active player character"""
		return self.pc[self.pcPointer]
		
	def getMonsterAt(self, i):
		if i<len(self.monsters) and i>=0:
			return self.monsters[0]
	
	def allActionsSet(self):
		"""Verifies that all player actions have been set"""
		return self.pcPointer == (len(self.pc))
	
	def cleanUpActionFields(self):
		"""
		Clears action fields and flags
		and increments PC pointer
		"""
		self.isActionSelected=False
		self.isTargetSelected=False
		self.action=""
		self.pcPointer+=1
	
	def isCombatOver(self):
		return False
	
	def isValidAction(self, inp):
		'''Checks dictionary matching input keys to action type'''
		return self.actionDict[inp] in self.getActivePC().getActions()
			
	
class executeState(IState):
	
	def __init__(self, action_queue, state_machine, view=""):
		self.action_queue=action_queue
		self.state_machine=state_machine
		self.pc = []
		self.monsters = []
		self.info_pointer = 0
		self.info_list = []
		self.render_strings = []
		self.glob=""
		self.gameOverFlag=False
		self.view=view
		self.isCombatOverFlag=False
		self.ranAway=False
		
	def OnEnter(self, glob):
		self.pc = glob.pc()
		self.monsters = glob.monsters()
		self.action_queue = glob.action_queue()
		self.glob=glob
		self.generateMonsterActions()
		self.sortActionsBySpeed()
		self.executeActions()
		self.cleanUp()
	
	def Update(self):
		self.info_pointer+=1
		if self.info_pointer==len(self.render_strings):
			if (len(self.pc)==0):
				self.state_machine.Change(StateEnum.gameOver,False)
			elif (len(self.monsters)==0 or self.ranAway):
				print("combat is over!")
				self.isCombatOverFlag=True
			else:
				self.state_machine.Change(StateEnum.decide, self.glob)
	
	def Render(self):
		'''Renders results of actions step by step'''
		self.view.renderInfo(self.render_strings[self.info_pointer])
		print(self.render_strings[self.info_pointer])
		
	def OnExit(self):
		self.render_strings = []
		self.action_queue = []

	
	def ProcessInput(self, inp):
		pass
	
	def generateMonsterActions(self):
		for mon in self.monsters:
			pc_index = min(2, random.randint(0,len(self.pc)-1))
			tempAction = action.Attack(mon, self.pc[pc_index])
			self.action_queue.append(tempAction)
			
	def sortActionsBySpeed(self):
		"""
		Sorts actions based on character speed
		"""
		print(self.action_queue)
		sorted(self.action_queue, key=lambda x: x.getOwner().getSpd())
	
	def executeActions(self):
		"""
		Execute all actions in queue
		"""
		for action in self.action_queue:
			action_out = action.execute()
			self.render_strings.append(action_out)
			if "ran" in action_out: ##This handles running away succesfully
				self.ranAway=True
		self.janitor()
		
	
	def cleanUp(self):
		self.info_pointer = 0
		self.info_list = []
		self.render_string=""
	
	def janitor(self):
		"""
		If anybody dies, get them out of the lists
		"""
		for character in self.pc:
			if character.getHp()<=0:
				self.render_strings.append(character.getName() + " has died!")
				self.pc.remove(character)
		for mon in self.monsters:
			if mon.getHp()<=0:
				self.render_strings.append(mon.getName() + " has died!")
				self.monsters.remove(mon)	
	def isCombatOver(self):
		return self.isCombatOverFlag

class gameOverState():
	
	def __init__(self, mStates, view):
		self.misc = 0
		self.view = view
		self.mStates=mStates
		self.gameOverFlag=False
		self.exit=False
	
	def OnEnter(self, flag):
		self.exit=flag
	
	def Render(self):
		if self.exit:
			outstring = "You've escaped the dungeon!"
		else:
			outstring = "You died! Game over!"
		self.view.renderInfo(outstring)
		self.view.screen_display.update()
		print(outstring)
	def Update(self):
		if self.exit and self.misc==0:
			self.misc+=1
		else:
			self.gameOverFlag=True
	def ProcessInput(self, i):
		pass
	def OnExit(self):
		pass
	def isGameOver(self):
		return self.gameOverFlag
	def isCombatOver(self):
		return False
	
class StateEnum(enum.Enum):
	decide="decide"
	selectAction="select_action"
	selectTarget="select_target"
	execute="execute"
	gameOver="gameover"
	explore="explore"
	combat="combat"
	
class CombatGlob():
	'''
	This class facilitates sticking together data for easy transfer between combat states
	In this case it sticks together the pc party, the monsters as well as the action queue
	This is transfered between execute and playerDecide states'''
	def __init__(self, pc='', monsters='',action_queue=''):
		self._pc=pc
		self._monsters=monsters
		self._action_queue=action_queue
	
	def pc(self):
		return self._pc
	def monsters(self):
		return self._monsters
	def action_queue(self):
		return self._action_queue
	
	def set_pc(self, pc):
		self._pc=pc
	def set_monsters(self, monsters):
		self._monsters=monsters
	def set_action_queue(self, action_queue):
		self._action_queue=action_queue

"""Main"""

def main(args):
	micro_view = view.micro_view()
	pc = [being.pc("Gib", 1, 2, 2, 2, 2, 1)]
	mf = monsterFactory.monsterFactory()
	monster = [mf.getGoblin()]
	glob = CombatGlob(pc, monster)
	c_state = combatState(None, micro_view)
	c_state.OnEnter(glob)
	
	while (not c_state.isGameOver()):
		#render
		c_state.Render()
		#take input
		pc_in = input("What do you?")
		c_state.ProcessInput(pc_in)
		#update
		c_state.Update()
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
