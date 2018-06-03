import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

pygame.init()

#Screen settings
(width, height) = (450, 450)
screen = pygame.display.set_mode((width, height))

#Loop for opening and closing the window
running = True
while  running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


#Window Title
pygame.display.set_caption('GOTY')