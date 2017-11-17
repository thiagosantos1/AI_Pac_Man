import pygame
from tiles import Tile
from random import randint
from wall import Wall
from maze import Maze
from bonus import Bonus


# this classe simulates a graph search with BFS to find the shortest path from survivor to the Bonus

# let's calculate the path, then go(don't show going each steap untill reach gol)

def BFS_path_finder(character, goal, avoid_agents): # avoid_agents in this case is the monsters

	parent = {}
	parent = BFS(character, goal, avoid_agents, True) # it's getting lost here - forever loop
	# if did't find a path avoind all ghosts 
	if goal not in parent:
		parent.clear()
		parent = BFS(character, goal, avoid_agents,  False) # then calculate one without thinking about the ghost

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

def BFS(character, goal, avoid_agents, avoidGhost):

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
		if avoidGhost:
			if Maze.isWalkable(vertex.idTile,v) and there_is_not_monster(v,avoid_agents):
				queue.append(v) # add all neighbors to be explored
				parent[v] = vertex.idTile # save where it came from
		else:
			if Maze.isWalkable(vertex.idTile,v):
				queue.append(v) # add all neighbors to be explored
				parent[v] = vertex.idTile # save where it came from

	while not done:
		vert = queue.pop(0) # the error is here - when pop, is not removing
		node_visited = Maze.tilesMaze[vert]
		node_visited.color = 'red'
		#print(node_visited.idTile) # it's repeting here, getting nodes already seen

		# you found your goal
		if vert == goal:
			done = True
			break

		# search for the neighbors of the next node
		for v in node_visited.neighbors:
			node_v = Maze.tilesMaze[v]

			if node_v.color =='black' and v not in queue and Maze.isWalkable(node_visited.idTile,v):
				if avoidGhost:
					if there_is_not_monster(v,avoid_agents):
						queue.append(v)
						parent[v] = node_visited.idTile # save where it came from
				else:
					queue.append(v)
					parent[v] = node_visited.idTile # save where it came from

		if len(queue) <=0:
			done = True

	return parent

def there_is_not_monster(tile_dst,avoid_agents):

	for monster in avoid_agents:
		if tile_dst == monster.currenTileNum:
			return False
	return True




