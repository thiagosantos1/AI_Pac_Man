# Copyright by Thiago Santos
# All rights reserved

import pygame

# function to draw in the screen
# when you put paramter = value, it's become the default valor if nothing is pass
def text_to_screen(screen, text, x, y, size = 15,
            color = (255, 255, 255), font_type = 'monospace'):

    text = str(text) # it comes as a object
    #font = pygame.font.Font(font_type, size)
    font = pygame.font.SysFont(font_type, size)
    #font.set_bold()
    text = font.render(text, True, color)
    screen.blit(text, (x, y)) # display on screen

