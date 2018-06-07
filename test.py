import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')



pygame.init()



#Screen settings
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#FPS and time module
FPS = 60
clock = pygame.time.Clock()


#Window Title
pygame.display.set_caption('GOTY')


#Loading bg img
bg = pygame.image.load(os.path.join("data", "bg.png")).convert_alpha()

#Player img
player_img = pygame.image.load(os.path.join("data", "player_ship.png")).convert_alpha()

#Loading bg sound
pygame.mixer.music.load(os.path.join("data", "bg3.ogg")) 
pygame.mixer.music.play(-1,0.0)



#Creating a Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.rect.x += self.speedx








all_sprites = pygame.sprite.Group()
player = Player()
#Creating new object as instance of player class

all_sprites.add(player)


#Loop for opening and closing the window
running = True
while  running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)

    #Update
    all_sprites.update()


    #Drawing
    screen.blit(bg, (0,0))
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()











