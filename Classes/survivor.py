import pygame
from tiles import Tile
from random import randint
from wall import Wall
from character import Character
from maze import Maze
from BFS_path_finder import BFS_path_finder
from DFS_path_finder import *

# this class is just about the survivor, that is a character

class Survivor(Character):


	survivor_img = pygame.image.load('../Images/Survivor/pac.png')
	height_survivor = 0
	width_survivor = 0
	def __init__(self,tileNum): # revieces just the tile he wish to start at

		self.original_img = Survivor.survivor_img
		width = Tile.widthTile 
		height = Tile.heightTile

		# not set yet
		if Survivor.height_survivor  == 0 or Survivor.width_survivor ==0:

			Survivor.width_survivor = width
			Survivor.height_survivor = height

		self.original_img = pygame.transform.scale(self.original_img, (width,height ))

		self.health  = 500 # if zombie gets him, he doesn't just die, he loses health
		self.score   = 0
		self.isAlive = True
		self.monster_caught = -50 # monster caught survivor, then he loses 50 in his health

		self.speed_x = Tile.widthTile//2 # speed per FPS player walk
		self.speed_y = Tile.heightTile//2

		self.direction = 'e' # starts facing east( rotates when move)
		self.rotate    = None # if rotate is set, rotate then the img

		self.list_target = list() # gonna sabe all future target untill a goal. calculate after run bfs
		self.ready_to_set_goal = False # become true after run the algotihm and had fond a shortest path

		#self.future_tile_number = None # wish of next tile to move for

		x_rec = Maze.tilesMaze[tileNum].x
		y_rec = Maze.tilesMaze[tileNum].y

		super().__init__(x_rec,y_rec,tileNum, self.original_img)


	# draw and update the position of the player in the screen
	def update(self, screen, clock_elapsed):

		super().rotate(self.rotate) # rotate for the direction that our survivor is point to

		# if we have a target set(move arrow), then move player
		if self.tx != None and self.ty != None: 
			self.movement(clock_elapsed)

		if not self.ready_to_set_goal and len(Bonus.list_bonus)>0 : # if path to the goal was not define yet
			BFS_path_finder(self, Bonus.list_bonus[0] )
			#DFS_Dum_path_finder(self,Bonus.list_bonus[0].currently_tile)
		else:
			self.set_AI_target('BFS')

		screen.blit(self.img, (self.x, self.y))


	def get_monster_caught(self):
		return self.monster_caught







