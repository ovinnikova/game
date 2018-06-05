import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')



pygame.init()



#Screen settings
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))


#Changing the bckgr color
background_colour = (0,0,59)
screen.fill(background_colour)

#Window Title
pygame.display.set_caption('GOTY')

#Update the contents of the display
pygame.display.flip()

#Loading bg img
bg = pygame.image.load(os.path.join("data", "bg.png"))

#Loading bg sound
pygame.mixer.music.load(os.path.join("data", "bg3.ogg")) 
pygame.mixer.music.play(-1,0.0)


#Loop for opening and closing the window
running = True
while  running:

    screen.blit(bg, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()