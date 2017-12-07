# Copyright by Thiago Santos
# All rights reserved

import pygame
from tiles import Tile
from random import randint
from wall import Wall 
from character import Character
from maze import Maze
from BFS_path_finder import BFS_path_finder
from DFS_path_finder import *
from A_star_path import A_star_path
from monster import Monster

# this class is just about the survivor, that is a character

class Survivor(Character):


	survivor_img = pygame.image.load('../Images/Survivor/pac.png')
	height_survivor = 0
	width_survivor = 0			
	def __init__(self,tileNum,AI, gameMode): # revieces just the tile he wish to start at

		self.original_img = Survivor.survivor_img
		width = Tile.widthTile 
		height = Tile.heightTile

		# not set yet
		if Survivor.height_survivor  == 0 or Survivor.width_survivor ==0:

			Survivor.width_survivor = width
			Survivor.height_survivor = height

		self.original_img = pygame.transform.scale(self.original_img, (width,height ))

		self.health  = 200 # if zombie gets him, he doesn't just die, he loses health
		self.score   = 0
		self.isAlive = True
		self.monster_caught = 50 # monster caught survivor, then he loses 50 in his health
		self.gameMode = gameMode # AI means computer plays - player means somebody is playing

		self.speed_x = Tile.widthTile//2 # speed per FPS player walk
		self.speed_y = Tile.heightTile//2

		self.direction = 'e' # starts facing east( rotates when move)
		self.rotate    = None # if rotate is set, rotate then the img

		self.list_target = list() # gonna sabe all future target untill a goal. calculate after run bfs
		self.ready_to_set_goal = False # become true after run the algotihm and had fond a shortest path

		#self.future_tile_number = None # wish of next tile to move for

		x_rec = Maze.tilesMaze[tileNum].x
		y_rec = Maze.tilesMaze[tileNum].y

		super().__init__(x_rec,y_rec,tileNum, self.original_img,AI)


	# draw and update the position of the player in the screen
	def update(self, screen, clock_elapsed):

		super().rotate(self.rotate) # rotate for the direction that our survivor is point to

		# if we have a target set(move arrow), then move player
		if self.tx != None and self.ty != None: 
			self.movement(clock_elapsed)
			# if uncomment this line, it then calculates the path after every single move
			# to then avoid all ghosts - But it cost (become slow)
			#self.resetPath() # calculate again after move on tile, in order to avoid monster

		if self.gameMode == "AI":
			if not self.ready_to_set_goal and len(Bonus.list_bonus)>0 : # if path to the goal was not define yet
				if self.AI =='A_Star':
					A_star_path(self, Bonus.list_bonus[0].currenTileNum,Monster.List_Monster )
				elif self.AI =='BFS':
					BFS_path_finder(self, Bonus.list_bonus[0].currenTileNum, Monster.List_Monster )

				elif self.AI =='DFS':
					DFS_Dum_path_finder(self,Bonus.list_bonus[0].currenTileNum)
			else:
				# you gonna set next target, only and only if next target is not a ghost
				if len(self.list_target) >0:
					if not self.is_there_a_ghost(self.getNexTargetTiles()): # if there is not a ghost in the next target
						if self.AI =='A_Star':
							self.set_AI_target('A_Star')
						elif self.AI =='BFS':
							self.set_AI_target('BFS')
						elif self.AI =='DFS':
							self.set_AI_target('DFS')

					else: #there is a gost next tile
						# then, recalculate the A* path
						# if returns False(Cannot find a path), agent can then shoot and kill ghost(lose points)
						# if returns true, you can update again, reseting the path self.resetPath()
						self.resetPath() # when reset, you still calculate the same path, cause there's no ghost until it moves

		screen.blit(self.img, (self.x, self.y))

	def get_monster_caught(self):
		return self.monster_caught
	# get next 2 targets tile(if there is)
	# it returns 2 because  the problem is that next target may be a ghost, but the ghost updates first, 
	# then when robot updates it's not a ghost anymore
	def getNexTargetTiles(self):
		if self.AI == "A_Star" or self.AI == "BFS":
			if len(self.list_target) >=2:
				return [ self.list_target[len(self.list_target)-1], self.list_target[len(self.list_target)-2]  ]
			return [ self.list_target[len(self.list_target)-1] ]

		if self.AI == "DFS" or self.AI == "DFS_Dum":
			if len(self.list_target) >=2:
				return [ self.list_target[0], self.list_target[1] ]
			return [ self.list_target[0] ]

	# checks if there's a ghost around the next target
	# if so, it must take another path(not take risk)
	def is_there_a_ghost(self,nexTiles):

		for ghost in Monster.List_Monster:
			for tile in nexTiles:
				if ghost.currenTileNum == tile or self.is_there_ghost_souround_tile(tile):
					return True

		return False

	# checks if there is a ghost souround that tile - If you can walk from that tile to next tile
	def is_there_ghost_souround_tile(self, tile):

		target = tile

		if ( (target in range(1, len(Maze.tilesMaze) +1) ) ):
			
			for ghost in Monster.List_Monster:

				# east
				target = tile +1   # if cann walk in that direction - not outside of the border
				if ((target-1) % Maze.size_maze !=0 ): # if can go for that position
					if Maze.tilesMaze[tile].is_walkable('e'): # if walkable, then check if there's a ghost there
						if ghost.currenTileNum == target: # there is a ghost at that potential move
							return True 

				# west
				target = tile -1
				if target % Maze.size_maze !=0: # if can go for that position
					if Maze.tilesMaze[target].is_walkable('w'): 
						if ghost.currenTileNum == target: # there is a ghost at that potential move
							return True 

				# nourth
				target = tile - Maze.size_maze
				if target >0: # if can go for that position
					if Maze.tilesMaze[target].is_walkable('n'): 
						if ghost.currenTileNum == target: # there is a ghost at that potential move
							return True 

				#south
				target = tile + Maze.size_maze
				if target <= Maze.size_maze: # if can go for that position
					if Maze.tilesMaze[tile].is_walkable('s'): 
						if ghost.currenTileNum == target: # there is a ghost at that potential move
							return True 


		return False # there's no ghost souround that tile, it's okay ta walk


