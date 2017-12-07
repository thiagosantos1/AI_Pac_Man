# Copyright by Thiago Santos
# All rights reserved

# file to control the logic of the game
# control user event input, movements of the characters, etc

import pygame, sys
from tiles import Tile

# function to haldle the survivor interaction with the screen
def interaction(screen, survivor):

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Movemnt of the player is gonna be not just when you press a key, but when you press or you are holding
    # that's why it goes outside of the loop events
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:# North

    	# first, before move we have to ckeck if that position is walkable
    	# so them, you first get the "new" position for that character
    	# in this case we get the number of the character, that represents
    	# his position on screen, minus how many we can move, Remember that is is to
    	# left or right, is gonna move always 1 block, if it's up or down, 18 block

        if survivor.targetTileNumber == None: # if a target is not set yet
            survivor.rotate = 'n'
            survivor.setTarget() # dont have to pass the direction, cause rotate is already set
        
             
    if keys[pygame.K_DOWN]: # South
        if survivor.targetTileNumber == None:
            survivor.rotate = 's'
            survivor.setTarget() 
    

    if keys[pygame.K_LEFT]: # West
        if survivor.targetTileNumber == None:
            survivor.rotate = 'w'
            survivor.setTarget() 
        

    if keys[pygame.K_RIGHT]: # East
        if survivor.targetTileNumber == None:
            survivor.rotate = 'e'
            survivor.setTarget() 
        








