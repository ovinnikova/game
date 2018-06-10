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


#BG img
bg = pygame.image.load(os.path.join("data", "bg.png")).convert_alpha()
y = 0

#Player img
player_img = pygame.image.load(os.path.join("data", "player_ship.png")).convert_alpha()
player_img2 = pygame.image.load(os.path.join("data", "pl.jpg")).convert_alpha()

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
        self.speedx = 0
        

        #Movement while pressing keys
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            self.image = player_img2
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx

        #Bg borders for player
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0






#Groupping all sprites
all_sprites = pygame.sprite.Group()

#Creating new object as instance of player class
player = Player()
#Adding player sprites to all sprites
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


    #Drawing scrolling BG
    rel_y = y % bg.get_rect().height
    screen.blit(bg, (0, rel_y - bg.get_rect().height))
    if rel_y < HEIGHT:
        screen.blit(bg, (0, rel_y))
    y -= 1
   

    #Srawing sprites
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()











