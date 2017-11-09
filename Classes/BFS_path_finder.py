import pygame
from tiles import Tile
from random import randint
from wall import Wall
from maze import Maze
from bonus import Bonus


# this classe simulates a graph search with BFS to find the shortest path from survivor to the Bonus

# let's calculate the path, then go(don't show going each steap untill reach gol)

def BFS_path_finder(character, goal):

	queue = list()
	parent = {} # dictionary to save where each node came from
	Maze.resetTiles() # reset all tiles to unvisetedd

	vertex = Maze.tilesMaze[character.currenTileNum] # get currently tile

	vertex.color = 'red'
	parent[vertex.idTile] = -1 # starts at this node
	done = False
	#bonus = Bonus.list_bonus[0] # can be different in the future, in case there's more than 1 in the screen
	for v in vertex.neighbors:
		# check if is walkable first
		if isWalkable(vertex.idTile,v):
			queue.append(v) # add all neighbors to be explored
			parent[v] = vertex.idTile # save where it came from

	while not done:

		vert = queue.pop(0)
		node_visited = Maze.tilesMaze[vert]
		node_visited.color = 'red'

		# you found your goal
		if vert == goal:
			done = True
			break

		# search for the neighbors of the next node
		for v in node_visited.neighbors:
			node_v = Maze.tilesMaze[v]

			if node_v.color == 'black' and isWalkable(node_visited.idTile,v):

				queue.append(v)
				parent[v] = node_visited.idTile # save where it came from

		if len(queue) <=0:
			done = True


	# then set the nodes to character to visit
	done = False
	target = goal
	character.list_target.append(target)
	while not done:
		target = parent[target]
		if target != character.currenTileNum:
			character.list_target.append(target)
		else:
			done = True

	character.ready_to_set_goal = True


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



