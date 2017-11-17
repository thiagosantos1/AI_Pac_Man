import pygame
from tiles import Tile
from random import randint
from wall import Wall
from maze import Maze
from bonus import Bonus

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
def A_star_path(character, goal,avoid_agents):

	parent = {}
	parent = A_star_path_generator(character, goal, avoid_agents, True)

	# if did't find a path avoind all ghosts 
	if goal not in parent:
		print("Not found")
		parent.clear()
		parent = A_star_path_generator(character, goal, avoid_agents, False) 
				# then calculate one without thinking about the ghost

	print("Parent: ", parent)
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


def A_star_path_generator(character, goal, avoid_agents, avoidGhost): # returns a dictionary with the path

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
		if Maze.isWalkable(vertex.idTile,v):
			if avoidGhost:
				if not there_is_monster(v,avoid_agents):
					queue.append(v) # add all neighbors to be explored
					print("No ghost ",v)
					parent[v] = vertex.idTile # save where it came from
					# get the g(n) of that tile
					Maze.tilesMaze[v].G = get_G_value(vertex)
					Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
					heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])
			else:
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

			if Maze.isWalkable(node_visited.idTile,v):

				if avoidGhost:
					# if not on queue to be explored, to add, as well it g and h cost
					if node_v.color == 'black' and not there_is_monster(v,avoid_agents):
						queue.append(v)
						print("No ghost ",v)
						parent[v] = node_visited.idTile # save where it came from
						Maze.tilesMaze[v].G = get_G_value(vertex)
						Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
						heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])

					# if it's already on queue, check if the g(n) is better(smaller) or not, if so, set as new path
					elif node_v.color == 'red' and not there_is_monster(v,avoid_agents):
						if get_G_value(vertex) < Maze.tilesMaze[v].G:
							# update then the new path
							parent[v] = node_visited.idTile # save where it came from
							Maze.tilesMaze[v].G = get_G_value(vertex)
							Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
							heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])
				else:
					# if not on queue to be explored, to add, as well it g and h cost
					if node_v.color == 'black':
						queue.append(v)
						parent[v] = node_visited.idTile # save where it came from
						Maze.tilesMaze[v].G = get_G_value(vertex)
						Maze.tilesMaze[v].H = get_H_value(Maze.tilesMaze[v],Maze.tilesMaze[goal])
						heuristic_cost[v] = get_F_value(Maze.tilesMaze[v])

					# if it's already on queue, check if the g(n) is better(smaller) or not, if so, set as new path
					elif node_v.color == 'red':
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

def there_is_monster(tile_dst, avoid_agents):

	for monster in avoid_agents:
		if tile_dst == monster.currenTileNum:
			return True
	if is_there_ghost_souround_tile(tile_dst,avoid_agents): # cannot have ghost around the tile as well
		return True
	return False

# checks if there is a ghost souround that tile - If you can walk from that tile to next tile
def is_there_ghost_souround_tile(tile,avoid_agents):

		target = tile

		if ( (target in range(1, len(Maze.tilesMaze) +1) ) ):
			
			for ghost in avoid_agents:

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



