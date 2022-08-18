import pygame
import random
import json
import time
from spritesheet import SpriteSheet
from monsterFactory import monsterFactory

class micro_view():
	
	def __init__(self):
		pygame.init()
		self.screen_width=320
		self.screen_height=256
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		self.screen_display = pygame.display
		
		#wall/floor sprites for dungeon
		sprite_file= 'images/tech1.png'#'images/bigbrick2.png'
		sprite_json =open('images/tech1.json')#'images/bigbrick2.json')
		sprite_data = json.load(sprite_json)
		spritesheet = SpriteSheet(sprite_file)
		self.sprite_library = self.generateSpriteLibrary(sprite_data, spritesheet)
		
		#menu sprites for combat
		self.monster_tab = pygame.image.load('images/monster_tab.png')
		self.monster_tab_x,self.monster_tab_y=20,10
		self.info_tab = pygame.image.load('images/log_tab.png')
		self.info_tab_x,self.info_tab_y=56,35
		self.option_tab = pygame.image.load('images/option_tab.png')
		self.option_tab_x,self.option_tab_y=30,170
		self.look_tab=pygame.image.load('images/display_tab.png')
		self.look_tab_x,self.look_tab_y=170,10
		self.enemy_sprite=pygame.image.load('images/goblin.png')
		
		#monster sprites
		self.monster_sprites = self.generateMonsterSprites()
		
		self.gameFont = pygame.font.Font('fonts/msxFont.ttf', 14)
		
		self.pygame=pygame 

	def generateSpriteLibrary(self, json, spritesheet):
		'''
		Returns a library of all sprites using their name as key.
		Each contained dictionary is sprites organized by 'relative position'
		e.g. dict.get(-1, 0) to get the sprite of a tile directly to the player's left
		'''
		sprite_library = {}
		layers = json['layers']
		for val in layers:
			sprite_dict = {}
			for tile in val.get('tiles'):
				key = (tile.get('tile').get('x'), tile.get('tile').get('z'))
				screen_x, screen_y = (tile.get('screen').get('x'), tile.get('screen').get('y'))
				coords_x, coords_y = (tile.get('coords').get('x'), tile.get('coords').get('y'))
				width, height = (tile.get('coords').get('w'), tile.get('coords').get('h'))
				
				#image setup
				image_rect = (coords_x, coords_y, width, height)
				image = spritesheet.image_at(image_rect)
				image.set_colorkey((0,255,0)) #will turn green screen to transparent
				
				if tile.get('flipped')==True:
					image = self.flipImage(image)
					screen_x-=width
				sprite_dict[key] = sprite(image, screen_x, screen_y, width, height, val.get('name'))
			sprite_library[val.get('name')] = sprite_dict
		return sprite_library
	
			
	def flipImage(self, image):
		image = image.copy()
		return pygame.transform.flip(image, True, False)
	
	def render_ground_tile(self, coord, floor_trim, ceil_trim):
		"""
		Renders a ground tile with accompnaying ceiling tile
		"""
		if self.spriteExists(coord, floor_trim):
			sprites = [self.getSprite(coord, floor_trim), self.getSprite(coord, ceil_trim)]
			for sprite in sprites:
				self.screen.blit(sprite.image, (sprite.x, sprite.y))
			
			
	def render_wall_tile(self, coord, trim):
		"""
		Renders a sprite of type wall given a tupple of coords, and a trim.
		This method handles stitching front and side sprites to properly display Wall tiles
		"""
		if self.spriteExists(coord, trim):
			sprite = self.getSprite(coord, trim)
			if (coord[0]<0 and coord[1]<0): #if image is to the left
				center_sprite = self.getSprite((0, coord[1]), trim)
				l_x = sprite.x - center_sprite.width
				self.screen.blit(center_sprite.image, (l_x, sprite.y))
			elif (coord[0]>0 and coord[1]<0): #if image is to the right
				center_sprite = self.getSprite((0, coord[1]), trim)
				r_x = sprite.x + sprite.width
				self.screen.blit(center_sprite.image, (r_x, sprite.y))
			self.screen.blit(sprite.image, (sprite.x, sprite.y))
		
		
	def getSprite(self, coord, trim):
		"""
		Given a tupple of coordinates and the tile trim, returns a sprite fromt the sprite library dict
		"""
		try:
			return self.sprite_library.get(trim).get(coord)
		except:
			print("This sprite does not exist!")
	
	def spriteExists(self, coord, trim):
		if trim in self.sprite_library:
			if coord in self.sprite_library.get(trim):
				return True
		return False
		
	'''
	Combat Menu Functions
	'''
		
	def renderCombatMenu(self):
		''' 
		Renders the option tab, monster tab, and info tabs in their correct position
		'''
		self.screen.fill((0,0,0))
		self.screen.blit(self.option_tab, (self.option_tab_x,self.option_tab_y))
		self.screen.blit(self.monster_tab,(self.monster_tab_x,self.monster_tab_y))
		self.screen.blit(self.look_tab,(self.look_tab_x, self.look_tab_y))
		
	def renderInfo(self, string):
		'''
		Takes a string and renders it to scree at info tab
		'''
		x = self.info_tab_x+10
		y = self.info_tab_y+20
		string_render = self.gameFont.render(string,True,(255,255,255))
		self.screen.blit(self.info_tab,(self.info_tab_x,self.info_tab_y))
		self.screen.blit(string_render,(x,y))
	
	def renderMonsterList(self,monsterList):
		'''
		Takes a list of all monster names and renders them to screen at monster tab
		'''
		x = self.monster_tab_x+10
		y = self.monster_tab_y+20
		index = 1
		for monsterName in monsterList:
			monsterName = str(index) + ") " + monsterName
			name_render = self.gameFont.render(monsterName,True,(255,255,255))
			self.screen.blit(name_render, (x, y))
			y+=16
			index+=1
	
	def renderOptions(self,optionList):
		'''
		Takes a list of strings and renders them to screen at option tab
		'''
		x=self.option_tab_x+10
		y=self.option_tab_y+20
		for option in optionList:
			option_render=self.gameFont.render(option,True,(255,255,255))
			self.screen.blit(option_render,(x,y))
			x+=len(option)*6
	
	def renderStringOption(self,string):
		'''
		Takes a single string and renders it to screen at option tab
		'''
		x=self.option_tab_x+10
		y=self.option_tab_y+20
		string_render = self.gameFont.render(string,True,(255,255,255))
		self.screen.blit(string)
	
	def renderEnemySprite(self, enemy_name=''):
		'''
		Takes enemy name and renders the appropriate sprite
		Else renders default goblin image
		'''
		if enemy_name!='':
			self.enemy_sprite=self.monster_sprites[enemy_name]
		self.enemy_sprite.set_colorkey((0,255,0))
		self.screen.blit(self.enemy_sprite, (self.look_tab_x+5, self.look_tab_y+20))
		
	
	def generateMonsterSprites(self):
		'''Generate a dictionary that uses monster names as key to access sprite'''
		monster_sprites = {}
		monster_list = monsterFactory.getListOfMonsters()
		for monster in monster_list:
			print(monster.getSpriteFile())
			sprite = pygame.image.load(monster.getSpriteFile())
			monster_sprites[monster.getName()] = sprite
		return(monster_sprites)
		
		
class sprite():
	
	def __init__(self, image, x, y, width, height, trim="ColorfulTile"):
		self.image=image
		self.x=x #x value for where to display on screen
		self.y=y #y value for where to display on screen
		self.width = width
		self.height = height
		self.trim=trim
	
def main(args):
	view = micro_view()
	
	'''
	Working example of how rendering might work in controller
	'''
	game_map = {
	(-1, -2):'d', (1, -2):'d', (0, -2):'d', 
	(-1, -1):'f', (1, -1):'f', (0, -1):'f', 
	(-1, 0):'f',  (1, 0):'f', (0, 0):'f'}

	game_map2 = {
		(0,-2):'w', (1,-2):'f'
	}
	view.screen.fill((0,0,0))
	
	for coord in game_map.keys():
		print(coord)
		tile = game_map.get(coord)
		
		if tile=='f':
			if coord in view.sprite_library.get('tech1_floor'):
				view.render_ground_tile(coord, 'tech1_floor', 'tech1_ceil')
		elif tile=='w':
			if coord in view.sprite_library.get('tech1_wall'):
				view.render_wall_tile(coord, 'tech1_wall')
		elif tile=='d':
			if coord in view.sprite_library.get('tech1_door'):
				view.render_wall_tile(coord, 'tech1_door')
					
	pygame.display.update()
	
	time.sleep(5)
	
	'''
	##Render combat info
	monsterList = ["Pig", "Lobcheck", "Goose"]
	optionList = ["F)ight", "D)efend", "R)un", "C)ast"]
	view.screen.fill((0,0,0))
	view.renderCombatMenu()
	view.renderInfo("Goblin died!")
	view.renderMonsterList(monsterList)
	view.renderOptions(optionList)
	pygame.display.update()
	
	time.sleep(10)
	'''
	

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
