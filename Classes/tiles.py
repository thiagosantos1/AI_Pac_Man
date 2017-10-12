import pygame 
from wall import Wall
import random

# class tiles save each tile(square) of the maze
# Each tile is resposible to save its neighbors 
class Tile(pygame.Rect): 

	widthTile = 0
	heightTile = 0
	total_tiles = 1 # wanna keep of how many tiles we have
	def __init__(self,width, height, x=0, y=0):
		self.idTile = Tile.total_tiles
		self.neighbors = list()
		self.walls = list()
		self.finishedTime = 0
		self.discoveryTIme = 0
		self.fully_visited = False
		self.color = 'black' # black to not explore yet / red to being explored / blue to done exploring
		self.x = x
		self.y = y

		Tile.total_tiles +=1

		# not set yet
		if Tile.widthTile  == 0 or Tile.heightTile ==0:

			Tile.widthTile = width
			Tile.heightTile = height

		pygame.Rect.__init__(self, (x,y) , (Tile.widthTile, Tile.heightTile) )

	#each tile can add its own neighbors
	def add_neighbor(self, tile):
		if tile not in self.neighbors:
			self.neighbors.append(tile)
			random.shuffle(self.neighbors)	

	# true or false if it's to add a wall on horizontal or vertical from that square
	def add_wall(self, horizontal, vertical):
		# add a new object wall that it's a rectangle to the tile
		if horizontal:
			x = self.x
			y = self.y + int(Tile.heightTile)
			height = 7
			width = int(Tile.widthTile)
			self.walls.append(Wall(x,y,width,height,True))

		if vertical:
			x = self.x + int(Tile.widthTile)
			y = self.y
			height = int(Tile.heightTile)
			width = 7
			self.walls.append(Wall(x,y,width,height,False))

	def draw_tile_walls(self,screen,color):
		for i in range(0, len(self.walls)):
			self.walls[i].draw_wall(screen, color)


	def removeWall(self,direVertical):
		for i in range(0, len(self.walls)):
			if(direVertical and self.walls[i].vertical):
				self.walls[i].remove_wall()
			elif( (not direVertical) and self.walls[i].horizontal):
				self.walls[i].remove_wall()


	@staticmethod
	def reset():
		Tile.total_tiles=1
		Tile.widthTile = 0
		Tile.heightTile = 0









