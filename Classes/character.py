import pygame
from tiles import Tile
from maze import Maze
from random import randint
from wall import Wall

# This class is the based of any character in the game, currently one or future feature

# each character is the same size of each tile. that way we can control colision

class Character(pygame.Rect):

	width = Tile.widthTile
	height = Tile.heightTile

	def __init__(self, x, y, tileNum, img):

		# each character is gonna have a variable to control next square to go on
		# if it's empty, means no new goal
		self.tx, self.ty = None,None
		# also, save the tile number that wishes to go
		self.targetTileNumber = None

		# save the tile our character is currently at
		self.currenTileNum = tileNum;

		self.img = img

		#inherance from pygame rectange
		pygame.Rect.__init__(self,x,y,Character.width, Character.height)


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

	 








