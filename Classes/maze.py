# Copyright by Thiago Santos
# All rights reserved

from tiles import Tile
import random
import pygame

class Maze(pygame.Rect):

	# dictionary to save all the tiles the maze has
	tilesMaze = {}
	timeExecuted =1 # time of each node got disvovered
	#each title size depends on the screen size, that can range depending on the size of the maze
	widthMaze  = 0 
	heightMaze = 0
	yPos = 0 
	xPos = 0
	size_maze =0
	cost_walk = 10 # to move to each tile, has a cost of 10

	def __init__(self,sizeMAze,WIDTH,HEIGHT):

		Maze.widthMaze  = WIDTH
		Maze.heightMaze = HEIGHT
		Maze.size_maze = sizeMAze
		Maze.cost_walk = 10
		tileWidth = WIDTH//sizeMAze
		tileHeight = HEIGHT // sizeMAze
		# gonna make N * N maze, each position being a tile ID

		mode = sizeMAze # used to check each colum each tile belongs to
		yPos = 0 # everytime we change column, it increases by tileHeight 
		xPos = 0
		# calculate x and y positions for each tile
		for idMaze in range(1,(sizeMAze*sizeMAze) +1):
			if(idMaze // mode <1): # if it's the number by itself, the tile still belongs to that column
				x = xPos * tileWidth
				y = yPos
				xPos+=1
			else:
				if(idMaze // mode ==1): # update y position and reset X variables
					x = xPos * tileWidth
					y = yPos

				xPos =0
				yPos += tileHeight 
				mode +=sizeMAze

			

			Maze.tilesMaze[idMaze] = Tile(tileWidth,tileHeight, x,y )
		
		pygame.Rect.__init__(self, Maze.xPos, Maze.yPos, Maze.widthMaze, Maze.heightMaze)

		self._setNeighbors(sizeMAze)
		self._setWalls(sizeMAze)

		# get a cell(node) randomly 
		randomNode = random.randrange(sizeMAze*sizeMAze) + 1
		self._generateMazeDFS( Maze.tilesMaze[randomNode ] )
		#self._createMultiplePathsBFS( ) Not good, runs exponetial time by doing BFS from every node to all nodes
		self._createMultiplePathsRandom( )
	# for each cell on TilesMaze, we decide the neighbors of each one, and ask the tile to add his neighbor on its list of neighbors
	def _setNeighbors(self,sizeMAze):
		
		for u in range(1, (sizeMAze*sizeMAze) +1):	

			for t in range (1,3):
				if t ==1:
					v = u+1
				else:
					v = u+sizeMAze

				if( (t ==1 and u % sizeMAze != 0) or (t==2) ):
					if u in self.tilesMaze and v in self.tilesMaze:
						for key, value in self.tilesMaze.items():
							if key == u:
								value.add_neighbor(v)
							if key == v:
								value.add_neighbor(u)
						

	# add the walls to the maze(all walls)
	# later, we remove some of the walls to then make the maze
	# here, we add walls in all possible places(cannot walk in any square right now)
	def _setWalls(self, sizeMAze):

		mode = sizeMAze
		# used to add all to those that can have 2 walls
		for idMaze in range(1, (sizeMAze * (sizeMAze -1)) +1):
			if(idMaze // mode < 1 ): # not gonna add for the last one( it already has the right wall from the maze box)
				self.tilesMaze[idMaze].add_wall(True, True)

			else:
				self.tilesMaze[idMaze].add_wall(True, False) # don't add on vertical cause it's already has from the maze box
				mode += sizeMAze

		for idMaze in range( (sizeMAze * (sizeMAze -1)) +1, sizeMAze * sizeMAze ):
			self.tilesMaze[idMaze].add_wall(False, True) # don't add on horizontal cause it's already has from the maze box

	def _print_maze(self,screen, color):
		for key in self.tilesMaze:
			#print(("Cell: ", key, "Neighbors: ",Maze.tilesMaze[key].neighbors))
			if key < len(self.tilesMaze):
				self.tilesMaze[key].draw_tile_walls(screen, color)


	def draw_maze(self,screen, color):
		pygame.draw.line(screen, color, [0,Maze.heightMaze],[0,0],7)
		pygame.draw.line(screen, color, [0,0],[Maze.widthMaze,0],7)
		pygame.draw.line(screen, color, [0,Maze.heightMaze],[Maze.widthMaze,Maze.heightMaze],7)
		pygame.draw.line(screen, color, [Maze.widthMaze,0],[Maze.widthMaze,Maze.heightMaze],7)

		self._print_maze(screen,color)


	# start the maze generation by runing DFS, from a inicial random state cell
	# DFS chooses a node with low cost, but in this case we gonna just choose a random one
	# the path it takes, we remove the wall between that node and next node choosen
	# http://reeborg.ca/docs/en/reference/mazes.html
	def _generateMazeDFS(self, vertex):

		vertex.color = 'red'
		vertex.discoveryTIme = Maze.timeExecuted
		Maze.timeExecuted +=1

		# run dfs for each neighbor of neighbor
		for neighbor in vertex.neighbors:
			if Maze.tilesMaze[neighbor].color == 'black':
				# before call dfs for next node, we call a function to remove the wall
				# between both nodes(have to calculate the direction)

				# hold each vertex that has the wall to be removed
				vertextToRemoveWall = vertex
				# hold each of the wall has to be removed, the one horizontal or vertical
				direVertical = True 
				# means it's going right or down
				if neighbor >  vertex.idTile:

					vertextToRemoveWall = vertex # always is gonna be the currently node
					# means it's going right
					if neighbor -1 == vertex.idTile:
						
						direVertical = True

					# means it's going down
					else:
						direVertical = False

				# means it's going up or left
				else:
					# means it's going left
					if neighbor +1 == vertex.idTile:
						vertextToRemoveWall = Maze.tilesMaze[vertex.idTile - 1]
						direVertical = True

					# means it's going up
					else:
						vertextToRemoveWall = Maze.tilesMaze[vertex.idTile - Maze.size_maze]
						direVertical = False

				# remove the wall
				self._removeWall(vertextToRemoveWall, direVertical)
				# call dfs for the next randmoly node
				self._generateMazeDFS(Maze.tilesMaze[neighbor])


		vertex.color = 'blue'
		vertex.finishedTime = Maze.timeExecuted
		Maze.timeExecuted +=1

	# pass if you wanna to avoid walls or not - At first yes cause you wanna find the shortest path avoinding wall
	# Then, you not gonna avoid walls and find another path
	# then backtrack and remove any wall with this new path
	def _createMultiplePathsBFS(self ): # not using

		# the idea e to find a path from A to B - avoinding wall
		# then find a path from B to A, not avoind wall

		for tileSrc in Maze.tilesMaze: # for each tile

			for tileDest in Maze.tilesMaze: # calculate for all tiles
				
				if tileSrc != tileDest:
					Maze.resetTiles() # reset all tiles to unvisetedd
					firstPath = self._BFS(tileSrc,tileDest, True)
					Maze.resetTiles() # reset all tiles to unvisetedd
					# then set as visited for all nodes that make the path calculate in the first call
					self._setPathVisited(tileSrc,tileDest,firstPath)
					# then call again, not avoind wall, to find another wall
					secondPath = self._BFS(tileSrc,tileDest, False)
					self._removeNewWalls(tileSrc,tileDest,second)

	# based on the first path calculated, gonna set all nodes used to that path
	# to visited, so then calculate another path(alternative route)
	def _setPathVisited(self,tileSrc,tileDest,path): # not using 
		done = False
		target = tileDest
		while not done:
			target = path[target]
			if target != tileSrc:
				Maze.tilesMaze[target].color = 'red'
			else:
				done = True

	# receives the second path(that did not avoid walls - Then, gonna remove the walls)
	def _removeNewWalls(tileSrc,tileDest,newPath): # not using
		return

	# instead of using the method BFS, we just look at each node and check if there's more than 1 wall in that, then remove
	# of of the wall
	def _createMultiplePathsRandom(self ):
		for key,value in Maze.tilesMaze.items():
			if len(value.walls) >1: # if that tile holds more than 1 wall - remove one of then
				self._removeWall(value,random.choice([True, False])) # random choose one of the wall - horizontal or vertical

	def _BFS(self, src, dest, avoid_wall):

		queue = list()
		parent = {} # dictionary to save where each node came from

		vertex = Maze.tilesMaze[src] # get currently tile

		vertex.color = 'red'
		parent[vertex.idTile] = -1 # starts at this node
		done = False
		#bonus = Bonus.list_bonus[0] # can be different in the future, in case there's more than 1 in the screen
		for v in vertex.neighbors:
			# check if is walkable first
			if avoid_wall: # if has to avoid wall
				if Maze.isWalkable(vertex.idTile,v):
					queue.append(v) # add all neighbors to be explored
					parent[v] = vertex.idTile # save where it came from
			else:
				queue.append(v) # add all neighbors to be explored
				parent[v] = vertex.idTile # save where it came from

		while not done:

			vert = queue.pop(0)
			node_visited = Maze.tilesMaze[vert]
			node_visited.color = 'red'

			# you found your goal
			if vert == dest:
				done = True
				break

			# search for the neighbors of the next node
			for v in node_visited.neighbors:
				node_v = Maze.tilesMaze[v]

				if avoid_wall:
					if node_v.color == 'black' and Maze.isWalkable(node_visited.idTile,v):

						queue.append(v)
						parent[v] = node_visited.idTile # save where it came from
				elif node_v.color == 'black': # doesn't have to avoid wall( goona make another path)
					queue.append(v)
					parent[v] = node_visited.idTile # save where it came from

			if len(queue) <=0:
				done = True


		return parent

	@staticmethod
	def isWalkable(tile_src, tile_dst):

		if(tile_src+1 == tile_dst):
			target = tile_src +1

			if Maze.tilesMaze[tile_src].is_walkable('e'): # the currently that holds the right wall
				return True

		elif(tile_src -1 == tile_dst):
			target = tile_src - 1

			if Maze.tilesMaze[target].is_walkable('w'):
				return True

		elif(tile_src - Maze.size_maze == tile_dst):
			target = tile_src - Maze.size_maze

			if Maze.tilesMaze[target].is_walkable('n'):
				return True

		elif(tile_src + Maze.size_maze == tile_dst):

			target = tile_src + Maze.size_maze

			if Maze.tilesMaze[tile_src].is_walkable('s'):
				return True

		return False # is is not walkable

	def _removeWall(self, vertex, direVertical):

		vertex.removeWall(direVertical)

	def resetMaze(self):

		Maze.timeExecuted =1
		widthMaze  = 0 
		Maze.heightMaze = 0
		Maze.yPos = 0 
		Maze.xPos = 0
		Maze.size_maze =0
		Maze.tilesMaze.clear()
		Tile.reset()

	@staticmethod # reset all titles to unvisited
	def resetTiles():
		for tile in Maze.tilesMaze:
			Maze.tilesMaze[tile].color = 'black'
			Maze.tilesMaze[tile].G     = 0
			Maze.tilesMaze[tile].H     = 0

	@staticmethod
	def get_size_maze():
		return Maze.size_maze

		

		



		













