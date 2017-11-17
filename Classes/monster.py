# an idea would be - Run the path find everytime, to check the monster position update
import pygame
from tiles import Tile
import random 
from wall import Wall
from character import Character
from maze import Maze
from BFS_path_finder import BFS_path_finder
from DFS_path_finder import *
from survivor import *
from A_star_path import A_star_path

class Monster(Character):


	monster_imgs = [pygame.image.load('../Images/Aliens/1.png'),
					pygame.image.load('../Images/Aliens/2.png'),
					pygame.image.load('../Images/Aliens/3.png'),
					pygame.image.load('../Images/Aliens/4.png'),
					pygame.image.load('../Images/Aliens/5.png'),
					pygame.image.load('../Images/Aliens/6.png'),]
	height_monster = 0
	width_monster  = 0
	health = 100
	speed_x = 0 
	speed_y = 0
	List_Monster = [] # save all the zombies created

	spaw_ready = False

	def __init__(self,tileNum, AI):

		self.original_img = Monster.monster_imgs[random.randrange(len(Monster.monster_imgs))]
		self.original_img = pygame.transform.scale(self.original_img, (Tile.widthTile ,Tile.heightTile ))
		self.health = Monster.health
		x_rec = Maze.tilesMaze[tileNum].x
		y_rec = Maze.tilesMaze[tileNum].y

		# not set yet
		if Monster.height_monster  == 0 or Monster.width_monster ==0:
			Monster.width_monster = Tile.widthTile 
			Monster.height_monster = Tile.heightTile
			Monster.speed_x = Tile.widthTile//2 # speed per FPS player walk
			Monster.speed_y = Tile.heightTile//2

		self.speed_x = Monster.speed_x
		self.speed_y = Monster.speed_y

		self.list_target = list() # gonna sabe all future target untill a goal. calculate after run BFS or DFS
		self.ready_to_set_goal = False # become true after run the algotihm and had fond a shortest path
		self.isAlive = True

		self.direction = 'e' # starts facing east( rotates when move)
		self.rotate    = None # if rotate is set, rotate then the img

		super().__init__(x_rec,y_rec,tileNum, self.original_img, AI)
		Monster.List_Monster.append(self)

	@staticmethod
	def reset():
		index=len(Monster.List_Monster)-1

		while index>=0:
			del Monster.List_Monster[index]
			index-=1

	@staticmethod
	def spawn(survivor, total_frames, FPS):
		global spaw_ready

		if total_frames % (FPS * 3) == 0 and not Monster.spaw_ready and total_frames >0:
			Monster.reset() # reset and set 3 new monsters

			for x in range(3):
				randTile = random.randrange(Maze.get_size_maze())
				while randTile == survivor.get_tile_number(): 
					randTile = random.randrange(Maze.get_size_maze())

				Monster(randTile)

			Monster.spaw_ready = True

	def getRandPosition(self,survivor_tile):
		randTile = random.randrange(Maze.get_size_maze())
		while randTile == survivor_tile: 
			randTile = random.randrange(Maze.get_size_maze())
		#return randTile
		return Maze.get_size_maze() * Maze.get_size_maze()-1
	#@staticmethod
	def update(self,screen, clock_elapsed, survivor):

		# if we have a target set(move arrow), then move player
		if self.tx != None and self.ty != None and len(Bonus.list_bonus)>0: 
			self.movement(clock_elapsed)

		if not self.ready_to_set_goal and len(Bonus.list_bonus)>0: # if path to the goal was not define yet
			if survivor.get_tile_number() != self.get_tile_number() :
				if self.AI =='BFS': 
					BFS_path_finder(self,survivor.get_tile_number(),Monster.List_Monster)
				elif self.AI =='DFS':
					DFS_Dum_path_finder(self, survivor.get_tile_number())
				elif self.AI =='A_Star':
					A_star_path(self, survivor.get_tile_number(),Monster.List_Monster)
		else:
			if self.AI =='BFS':
				self.set_AI_target('BFS')
			elif self.AI =='DFS':
				self.set_AI_target('DFS_Dum')
			elif self.AI =='A_Star':
						self.set_AI_target('A_Star')

		# then draw the zombies
		screen.blit(self.img, (self.x, self.y))

		if self.colliderect(survivor):

			survivor.score -= survivor.get_monster_caught()
			self.ready_to_set_goal = False
			self.tx = None 
			self.ty = None
			self.list_target.clear()

		if len(self.list_target) <=0:
			self.ready_to_set_goal = False
			self.tx = None 
			self.ty = None



	#@staticmethod
	def reset_all_path(self):
		#for monster in Monster.List_Monster:
		self.resetPath()





