import pygame
from tiles import Tile
from random import randint
from wall import Wall
from maze import Maze
from bonus import Bonus
from monster import Monster

# since the robot may get stuck, cause it can get traped(souround by wall or by monsters)
# it returns true if found a clean path to goal, or false if not

# this classe simulates a graph search with A* algorithm
# for our heuristic h(n) function, I am gonna use the mahatan distance
# g(n) is the total cost from initial node to goal state
# Heuristic f(n) = g(n) + f(n)

# every chacacter in our game has to avoid the mosters in their path, even monster itself(they can't overlap)
# thus, besides avoiding the all, the must also avoid monsters

# gonna create two versions
# one trys to find a path avoiding ghost
# second one find a path with ghost, if there is no other option
def A_star_path(character, goal):

	parent = {}
	paretnt = A_star_path_generator(character, goal, True)

	# if did't find a path avoind all ghosts
	if goal not in parent:
		parent.clear()
		parent = A_star_path_generator(character, goal, False) # then calculate one without thinking about the ghost

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


def A_star_path_generator(character, goal, avoidGhost): # returns a dictionary with the path

	queue = list()
	parent = {} # dictionary to save where each node came from
	Maze.resetTiles() # reset all tiles to unvisetedd
	heuristic_cost = {} # save the heurist g(n) + h(n) cost of each node - Save node key and f(n)

	# get character current tile, for initial state
	vertex = Maze.tilesMaze[character.currenTileNum] # get currently tile

	vertex.color = 'red'
	parent[vertex.idTile] = -1 # starts at this node
	done = False

	for v in vertex.neighbors:
		# check if is walkable first
		if isWalkable(vertex.idTile,v):
			queue.append(v) # add all neighbors to be explored
			parent[v] = vertex.idTile # save where it came from
			# get the g(n) of that tile
			Maze.tilesMaze[v].G = get_G_value(vertex)
			Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
			heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])


	# runs A star
	while not done:
		# get the vertex with min heurist value on heuristic_cost
		min_key= (min(heuristic_cost.items(), key=lambda x: x[1]) )[0]
		queue.remove(min_key)
		heuristic_cost.pop(min_key,None)
		vert = min_key
		node_visited = Maze.tilesMaze[vert]
		node_visited.color = 'red'

		# you found your goal
		if vert == goal:
			done = True
			break

		# search for the neighbors of the next node
		for v in node_visited.neighbors:
			node_v = Maze.tilesMaze[v]

			if avoidGhost:
				# if not on queue to be explored, to add, as well it g and h cost
				if node_v.color == 'black' and isWalkable(node_visited.idTile,v) and there_is_not_monster(v):
					queue.append(v)
					parent[v] = node_visited.idTile # save where it came from
					Maze.tilesMaze[v].G = get_G_value(vertex)
					Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
					heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])

				# if it's already on queue, check if the g(n) is better(smaller) or not, if so, set as new path
				elif node_v.color == 'red' and isWalkable(node_visited.idTile,v) and there_is_not_monster(v):
					if get_G_value(vertex) < Maze.tilesMaze[v].G:
						# update then the new path
						parent[v] = node_visited.idTile # save where it came from
						Maze.tilesMaze[v].G = get_G_value(vertex)
						Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
						heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])
			else:
				# if not on queue to be explored, to add, as well it g and h cost
				if node_v.color == 'black' and isWalkable(node_visited.idTile,v):
					queue.append(v)
					parent[v] = node_visited.idTile # save where it came from
					Maze.tilesMaze[v].G = get_G_value(vertex)
					Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
					heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])

				# if it's already on queue, check if the g(n) is better(smaller) or not, if so, set as new path
				elif node_v.color == 'red' and isWalkable(node_visited.idTile,v):
					if get_G_value(vertex) < Maze.tilesMaze[v].G:
						# update then the new path
						parent[v] = node_visited.idTile # save where it came from
						Maze.tilesMaze[v].G = get_G_value(vertex)
						Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
						heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])

		#search is done
		if len(queue) <=0:
			done = True

	return parent


def get_G_value(vertex):
	return Maze.cost_walk + vertex.G 

def get_H_value(vertex, goal):
	# mahatahn distance - times cost of walk just to be more precise
	return Maze.cost_walk * (abs(vertex.x - goal.x) + abs(vertex.y - goal.y)) // Tile.widthTile

def get_F_value(vertex):
	return vertex.G + vertex.H

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


def there_is_not_monster(tile_dst):

	for monster in Monster.List_Monster:
		if tile_dst == monster.currenTileNum:
			return False
	return True



