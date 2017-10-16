import pygame
from tiles import Tile
from random import randint
from wall import Wall
from character import Character
from maze import Maze

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

		self.speed_x = Tile.widthTile//2 # speed per FPS player walk
		self.speed_y = Tile.heightTile//2

		self.direction = 'e' # starts facing east( rotates when move)
		self.rotate    = None # if rotate is set, rotate then the img

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

		screen.blit(self.img, (self.x, self.y))


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

				self.currenTileNum = self.targetTileNumber
				self.targetTileNumber = None

	def setTarget(self):

		if(self.rotate == 'e'):
			target = self.currenTileNum +1
			if ( (target in range(1, len(Maze.tilesMaze) +1) ) and (target-1) % Maze.size_maze !=0 ):

				if Maze.tilesMaze[self.currenTileNum].is_walkable('e'): # the currently that holds the left wall
					self.targetTileNumber = target
					super().set_x_y_target(Maze.tilesMaze[target]) # pass the tile you are wishing to go to

		elif(self.rotate == 'w'):
			target = self.currenTileNum - 1
			if( (target in range(1, len(Maze.tilesMaze) +1) ) and target % Maze.size_maze !=0):

				if Maze.tilesMaze[target].is_walkable('w'):
					self.targetTileNumber = target
					super().set_x_y_target(Maze.tilesMaze[target])

		elif(self.rotate == 'n'):
			target = self.currenTileNum - Maze.size_maze
			if target in range(1, len(Maze.tilesMaze) +1):

				if Maze.tilesMaze[target].is_walkable('n'):
					self.targetTileNumber = target
					super().set_x_y_target(Maze.tilesMaze[target])

		elif(self.rotate == 's'):
			target = self.currenTileNum + Maze.size_maze
			if target in range(1, len(Maze.tilesMaze) +1):

				if Maze.tilesMaze[self.currenTileNum].is_walkable('s'):
					self.targetTileNumber = target
					super().set_x_y_target(Maze.tilesMaze[target])




