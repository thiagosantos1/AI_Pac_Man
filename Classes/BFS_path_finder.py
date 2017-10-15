import pygame
from tiles import Tile
from random import randint
from wall import Wall
from character import Character
from maze import Maze
from survivor import Survivor
from bonus import Bonus


# this classe simulates a graph search with BFS to find the shortest path from survivor to the Bonus


class BFS_path_finder():
