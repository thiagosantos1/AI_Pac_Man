import pygame

# each tile can have more than one wall
# and each wall it's a rectange
# it's easier to control colision
class Wall(pygame.Rect):

	walls_imgHorizon = pygame.image.load('../Images/Background/Walls/text6Horizon.png')
	walls_imgVert = pygame.image.load('../Images/Background/Walls/text6Vert.png')
	def __init__(self, x,y,width, height, horizon):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vertical = False
		self.horizontal = False

		# resize the pictures, according with monitor resolution
		#Wall.walls_imgHorizon = pygame.transform.scale(Wall.walls_imgHorizon, (width, height))
		#Wall.walls_imgVert = pygame.transform.scale(Wall.walls_imgVert, (width, height))
		if horizon: 
			self.img = Wall.walls_imgHorizon
			self.horizontal = True
			self.vertical = False
		else:
			self.img = Wall.walls_imgVert
			self.horizontal = False
			self.vertical = True


		pygame.Rect.__init__(self, (x,y) , (self.width, self.height) )


	def draw_wall(self,screen, color):
		#screen.blit(self.img, self)

		if self.vertical:
			# vertical right
			pygame.draw.line(screen, color, [self.x,self.y],[self.x,self.height+self.y],4)

		if self.horizontal:
			# horizontal botton
			pygame.draw.line(screen, color, [self.x,self.y],[self.width + self.x,self.y],4)


	def remove_wall(self):
		self.horizontal = False
		self.vertical = False






