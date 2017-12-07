# Copyright by Thiago Santos
# All rights reserved

import pygame
from tiles import Tile
from random import randint
from maze import Maze

# This Class is used to set and control where the bonus(fruit, coins, etc) is. It's the goal of the survivor to get it 


class Bonus(pygame.Rect):


	bonus_img =	[ pygame.image.load('../Images/Bonus/apple_red.png'),
					pygame.image.load('../Images/Bonus/candy_green.png'),
					pygame.image.load('../Images/Bonus/candy_red.png'),
					pygame.image.load('../Images/Bonus/candy_white.png'),
					pygame.image.load('../Images/Bonus/cherry.png'),
					pygame.image.load('../Images/Bonus/grape_blue.png'),
					pygame.image.load('../Images/Bonus/grape_orange.png'),
					pygame.image.load('../Images/Bonus/grape_red.png'),
					pygame.image.load('../Images/Bonus/kiwi.png'),
					pygame.image.load('../Images/Bonus/orange.png'),
					pygame.image.load('../Images/Bonus/pear.png'),
					pygame.image.load('../Images/Bonus/pineaple.png'),
					pygame.image.load('../Images/Bonus/strawberry.png'),
					pygame.image.load('../Images/Bonus/watermelon.png')]

	height_bonus = 0
	width_bonus  = 0
	list_bonus	 = [] # holds all bonus to be draw and catched

	bonusTimeGeneration = 0.5 # each 1 second, a new bonus will apear in the screen(after collected the last one)

	def __init__(self,tileNum): #each tile you wanna to generate 

		x_rec = Maze.tilesMaze[tileNum].x
		y_rec = Maze.tilesMaze[tileNum].y

		self.spawn_sounds = [pygame.mixer.Sound('../Sound_Effects/bonus/bonus1.wav'), 
							pygame.mixer.Sound('../Sound_Effects/bonus/bonus2.wav'),
							pygame.mixer.Sound('../Sound_Effects/bonus/bonus3.wav'),
							pygame.mixer.Sound('../Sound_Effects/bonus/bonus4.wav'), 
							pygame.mixer.Sound('../Sound_Effects/bonus/bonus5.wav'),
							pygame.mixer.Sound('../Sound_Effects/bonus/bonus6.wav')]

		width = Tile.widthTile 
		height = Tile.heightTile

		self.img = Bonus.bonus_img[randint(0,13)]
		self.img = pygame.transform.scale(self.img, (width,height ))
		self.poits = 50
		self.currenTileNum = tileNum


		# not set yet
		if Bonus.height_bonus  == 0 or Bonus.width_bonus ==0:

			Bonus.width_bonus = width
			Bonus.height_bonus = height

		pygame.Rect.__init__(self,x_rec,y_rec,width, height)

		Bonus.list_bonus.append(self)


	@staticmethod
	def spawn( total_frames, FPS, survivor):

		if total_frames % (FPS * Bonus.bonusTimeGeneration) == 0 and total_frames >0: 
			# create a new one just if there's no one in the screen(for now)
			if not Bonus.list_bonus: 


				randTile = randint(1, len(Maze.tilesMaze))

				while randTile == survivor.currenTileNum: # to not generate in the same
					randTile = randint(1, len(Maze.tilesMaze))

				bonus = Bonus(randTile)

				sound = bonus.spawn_sounds[randint(0, len(bonus.spawn_sounds) -1)]
				vol = sound.get_volume()
				sound.set_volume(min(vol*1,12))
				sound.play()

	@staticmethod
	def update(screen, survivor):

		for bonus in Bonus.list_bonus:

			screen.blit(bonus.img, (bonus.x, bonus.y))

			if bonus.colliderect(survivor):

				survivor.score += bonus.poits
				survivor.ready_to_set_goal = False # set new path to a new goal

				Bonus.list_bonus.remove(bonus)



