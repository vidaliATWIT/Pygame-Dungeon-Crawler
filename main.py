from state_machine import StateMachine as StateMachine, IState as IState, combatState as combatState, StateEnum as StateEnum, CombatGlob as CombatGlob, gameOverState as gameOverState
from explore_state import ExploreState
from view import micro_view 
from game_map import MapLevel 
from dmutil import dmutil
import tile
import enum
from monsterFactory import monsterFactory as mf
from being import pc as pc
from tile import TileType

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
