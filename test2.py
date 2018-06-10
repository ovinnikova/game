import os, sys
import pygame
import random
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')



pygame.init()

#COLORS
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

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

        #Movement while pressing keys + ANIMATION!
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
            self.image = player_img2
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
            self.image = player_img2
        self.rect.x += self.speedx
        if self.speedx == 0:
            self.image = player_img


        #Bg borders for player
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    
    #Spawning bullets
    def shoot(self):
        pl_bullet = PlayerBull(self.rect.centerx, self.rect.top)
        all_sprites.add(pl_bullet)
        pl_bullets.add(pl_bullet)
        

#Player bullets class
class PlayerBull(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()




#Creating enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((140,90))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 3)


    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)




#Groupping all sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
pl_bullets = pygame.sprite.Group()

#Creating new object as instance of player class
player = Player()
#Adding player sprites to all sprites
all_sprites.add(player)

#Spawning enemies
for i in range(3):
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)


#ZA GAME LOOP
running = True
while  running:

    for event in pygame.event.get():
        #Closing the window!
        if event.type == pygame.QUIT:
            running = False

        #IF up arrow - shoot
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.shoot()

    clock.tick(FPS)

    #Update
    all_sprites.update()


    #Check if enemy hits player
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False  #for test - if hits, game over!!


    # Check if bullet hits an enemy
    hits = pygame.sprite.groupcollide(enemies, pl_bullets, True, True)
    for hit in hits:
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)


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











