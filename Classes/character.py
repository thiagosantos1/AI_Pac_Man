# Copyright by Thiago Santos
# All rights reserved

import pygame
from tiles import Tile 
from maze import Maze
from random import randint
from wall import Wall

# This class is the based of any character in the game, currently one or future feature

# each character is the same size of each tile. that way we can control colision

class Character(pygame.Rect):

	width_char = 0
	height_char = 0

	def __init__(self, x, y, tileNum, img, AI): # AI means which alg the charac is using

		width = Tile.widthTile 
		height = Tile.heightTile

		# not set yet
		if Character.height_char  == 0 or Character.width_char ==0:

			Character.width_char = width
			Character.height_char = height

		# each character is gonna have a variable to control next square to go on
		# if it's empty, means no new goal
		self.tx, self.ty = None,None
		# also, save the tile number that wishes to go
		self.targetTileNumber = None

		# save the tile our character is currently at
		self.currenTileNum = tileNum;

		self.img = img
		
		self.AI = AI # save what kind of AI the monster is gonna be implemented with

		#inherance from pygame rectange
		pygame.Rect.__init__(self,x,y,Character.width_char, Character.height_char)


	def rotate(self, direction):

		if direction == 's':
			if self.direction != 's': # direction is where the next target of the player is, but then if you go all north, 
            # it's gonna reasignment/load the picture all the time, every loop. So then, whe put if self.direction !='n'
            # it's mean if we are going all north, we are gonna laod and rotate just once, in the first loop. It saves memory 
				self.direction = 's'
				south = pygame.transform.rotate(self.original_img, 90)
				self.img = pygame.transform.flip(south, False, True)

		elif direction == 'n':
			if self.direction != 'n':
				self.direction = 'n'
				self.img = pygame.transform.rotate(self.original_img, 90) # CCW

		elif direction == 'e':
			if self.direction != 'e':
				self.direction = 'e'
				self.img = self.original_img # original image already points to east

		elif direction == 'w':
			if self.direction != 'w':
				self.direction = 'w'
				self.img = pygame.transform.flip(self.original_img, True, False)

		self.scale_img()

	def scale_img(self):

		if self.rotate != None: # rotate everytime you change the direction
			width = Tile.widthTile #- (Tile.widthTile * 0,20)
			height = Tile.heightTile# - (Tile.heightTile * 0,15)
			self.img = pygame.transform.scale(self.img, (width,height ))
			#Survivor.survivor_img = pygame.transform.scale(Survivor.survivor_img, (width,height ))
			self.rotate = None

	def set_x_y_target(self, tile):
		# if you dont have a target set yet
		if self.tx == None and self.ty ==None:
			self.tx = tile.x
			self.ty = tile.y

	def get_tile_number(self):
		return self.currenTileNum

	def set_tile_number(self,new_tile):
		self.currenTileNum = new_tile

	# this method make the movement smotly, instead of move a whole position, we move part of, so then it's like we
    # are walking in the path
	def movement(self, clock_elapsed):

		if self.tx != None and self.ty != None: # Target is set

			X = self.x - self.tx
			Y = self.y - self.ty

			if X < 0: # --->
				self.x += self.speed_x #* clock_elapsed
			elif X > 0: # <----
				self.x -= self.speed_x #* clock_elapsed

			if Y > 0: # up
				self.y -= self.speed_y #* clock_elapsed
			elif Y < 0: # dopwn
				self.y += self.speed_y #* clock_elapsed

			if X == 0 and Y == 0:
				self.tx, self.ty = None, None

				self.set_tile_number(self.targetTileNumber)
				self.targetTileNumber = None

	# very similar to the set_Target - but in this case it sets automatictly 
	# you already runned BFS or DFS to find the path, now you gonna update and move to next tile
	def set_AI_target(self, search_type):

		# Target is not set but there is a target to be set in the list
		if self.tx == None and self.ty == None and len(self.list_target) >0: 
			# get next tile # if wanna run in different algorithm, just have to 
			# change how you get the tile in the list
			# BFS saves the next target in the last position like a stack
			# DFS is like a queue
			#BFS - #target = self.list_target.pop(len(self.list_target)-1) 
			#DFS - #target = self.list_target.pop(0) # end of the list
			if search_type == 'BFS' or search_type == 'A_Star':
				target = self.list_target.pop(len(self.list_target)-1) 
			elif search_type == 'DFS_Dum' or search_type == 'DFS':
				target = self.list_target.pop(0) # end of the list
			# set the direction to move forward
			if self.currenTileNum +1 == Maze.tilesMaze[target].idTile:
				self.rotate = 'e'
			elif self.currenTileNum -1 == Maze.tilesMaze[target].idTile:
				self.rotate = 'w'
			elif self.currenTileNum - Maze.size_maze == Maze.tilesMaze[target].idTile:
				self.rotate = 'n'

			elif self.currenTileNum + Maze.size_maze == Maze.tilesMaze[target].idTile:
				self.rotate = 's'

			# based on the direction choosen to move, set a target to move
			self.setTarget()


	def setTarget(self):

		# set target based on the direction you wanna to move forward
		if(self.rotate == 'e'):
			target = self.currenTileNum +1
			if ( (target in range(1, len(Maze.tilesMaze) +1) ) and (target-1) % Maze.size_maze !=0 ):

				if Maze.tilesMaze[self.currenTileNum].is_walkable('e'): # the currently that holds the right wall
					self.targetTileNumber = target
					self.set_x_y_target(Maze.tilesMaze[target]) # pass the tile you are wishing to go to

		elif(self.rotate == 'w'):
			target = self.currenTileNum - 1
			if( (target in range(1, len(Maze.tilesMaze) +1) ) and target % Maze.size_maze !=0):

				if Maze.tilesMaze[target].is_walkable('w'):
					self.targetTileNumber = target
					self.set_x_y_target(Maze.tilesMaze[target])

		elif(self.rotate == 'n'):
			target = self.currenTileNum - Maze.size_maze
			if target in range(1, len(Maze.tilesMaze) +1):

				if Maze.tilesMaze[target].is_walkable('n'):
					self.targetTileNumber = target
					self.set_x_y_target(Maze.tilesMaze[target])

		elif(self.rotate == 's'):
			target = self.currenTileNum + Maze.size_maze
			if target in range(1, len(Maze.tilesMaze) +1):

				if Maze.tilesMaze[self.currenTileNum].is_walkable('s'):
					self.targetTileNumber = target
					self.set_x_y_target(Maze.tilesMaze[target])
	 


	def resetPath(self):

		self.ready_to_set_goal = False # not ready to go yet(path not calculated yer)
		self.list_target.clear()





