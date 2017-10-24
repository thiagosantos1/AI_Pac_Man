import pygame
from tiles import Tile
from random import randint
from wall import Wall
from maze import Maze
from bonus import Bonus

# this class simulates a graph search with DFS to find the shortest path form survivor to a goal
# there're 2 implementations in this case, DFS and Dum_DFS
# the diference is that in DFS we calculate and set the shortest path to robot
# in Dum_DFS while calculating, the robot is already moving, to simulate how DFS actually goes


path_to_take = []
done = False
def DFS_Dum_path_finder(character, goal):
	global done
	Maze.resetTiles() # reset all tiles to nunviseted
	vertex = Maze.tilesMaze[character.currenTileNum] # get currently tile to be the base of the search
	

	path_to_take.append(vertex.idTile) # add the node you are going from
	done = False
	DFS_Dum(vertex, goal )

	#print("\n\n")

	#print(path_to_take)
	for target in path_to_take:
		character.list_target.append(target)
		if target == goal: # found the goal
			break

	character.ready_to_set_goal = True
	path_to_take.clear()
		

def DFS_Dum(vertex, goal):
	global done
	vertex.color = 'red' # on stack # black means new and blue is totally being visited
	# you found your goal
	if vertex == goal:
		done = True
		return

	for v in vertex.neighbors:
		node_v = Maze.tilesMaze[v]
		if node_v.color == 'black' and isWalkable(vertex.idTile,v) and not done:
			path_to_take.append(v) # add the node you're going to
			DFS_Dum(node_v,goal)

			path_to_take.append(vertex.idTile) # add the node you came from, to go again

	vertex.color = 'blue' # if reaches here, means you go all neighbors of that node



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

