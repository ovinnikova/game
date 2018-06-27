import os
import sys
import pygame
import random
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')



pygame.init()

# SCORE
score = 0

#GAME OVER
game_over = False

# COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Screen settings
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# FPS and time module
FPS = 60
clock = pygame.time.Clock()


# Window Title
pygame.display.set_caption('GOTY')


# BG img
bg = pygame.image.load(os.path.join("data", "bg.png")).convert_alpha()
y = 0

#Cat boss imgs loading
cat_boss = []
for i in range(7):
    filename = 'catbo0{}.png'.format(i)
    img = pygame.image.load(os.path.join("data", filename)).convert_alpha()
    cat_boss.append(img)

# Explosion animations loading
explosion_anim = []
for i in range(3):
    filename = 'explosion{}.png'.format(i)
    img = pygame.image.load(os.path.join("data", filename)).convert_alpha()
    explosion_anim.append(img)

# Player img
player_img = pygame.image.load(os.path.join
    ("data", "player_ship.png")).convert_alpha()

player_img2 = pygame.image.load(os.path.join
    ("data", "player_ship2.png")).convert_alpha()

player_img3 = pygame.image.load(os.path.join
    ("data", "player_ship3.png")).convert_alpha()

player_img4 = pygame.image.load(os.path.join
    ("data", "player_ship4.png")).convert_alpha()

# Img for hp
player_hp_img = pygame.image.load(os.path.join("data", "hp.png")).convert_alpha()

# Enemy img
enemy_img = pygame.image.load(os.path.join("data", "enemy_ship.png")).convert_alpha()
enemy_img2 = pygame.image.load(os.path.join("data", "enemy_ship2.png")).convert_alpha()

#P layer bullet
player_bullet = pygame.image.load(os.path.join("data", "player_bullet.png")).convert_alpha()

# Enemy bullet
enemy_bullet = pygame.image.load(os.path.join("data", "enemy_bullet.png")).convert_alpha()

# POWERUP
hp_powerup = pygame.image.load(os.path.join("data", "powerup_hp.png")).convert_alpha()

# FIRST BOSS
boss_v1_img = pygame.image.load(os.path.join("data", "boss_v1.png")).convert_alpha()
boss_v1_death = pygame.image.load(os.path.join("data", "boss_v228.png")).convert_alpha()

# Player shooting sound
player_shoot_sound = pygame.mixer.Sound(os.path.join("data", "player_shoot.ogg"))

# Loading and playing bg sound
pygame.mixer.music.load(os.path.join("data", "bg3.ogg")) 
pygame.mixer.music.play(-1,0.0)


# FONTS
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# FUNCTION FOR DRAWING HP
def draw_hp(surf, x, y, hp, img):
    for i in range(hp):
        img_rect = img.get_rect()
        img_rect.x = x + 40 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_boss_hp(surf, x, y, amount):
    if amount < 0:
        amount = 0

    BAR_LENGTH = 400
    BAR_HEIGHT = 25
    fill = (amount / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# Creating a Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.hp = 3

    def update(self):
        self.speedx = 0

        # Movement while pressing keys + ANIMATION(imgs)!
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

        
        # Img while shooting

        # If player isnt moving
        elif (keystate[pygame.K_UP] and self.speedx == 0):
            self.image = player_img3

        # If moving
        elif (keystate[pygame.K_UP] and self.speedx != 0):
            self.image = player_img4

        # Bg borders for player
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


        if game_over:
            self.kill()

    
    # Spawning bullets
    def shoot(self):
        player_shoot_sound.play()
        pl_bullet = PlayerBull(self.rect.centerx, self.rect.top)
        all_sprites.add(pl_bullet)
        pl_bullets.add(pl_bullet)

        

# Player bullets class
class PlayerBull(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_bullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()




# Creating enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.bspeedy = random.randrange(1, 3)
        self.speedy = self.bspeedy
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 30


    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)


        if self.frame % self.frame_rate == 0:
            self.frame = 0
            self.image = enemy_img
            #self.speedy = self.bspeedy
        elif self.frame > self.frame_rate/2:
            self.image = enemy_img2
            #self.speedy = self.bspeedy+1
        self.frame += 1



        if score == 100 or game_over:
            self.kill()



# Enemy bullets class
class EnemyBull(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy=3):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom > HEIGHT:
            self.kill()


        elif score == 100 or game_over:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center



class Powerup(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = hp_powerup
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy

        if self.rect.top > HEIGHT:
            self.kill()

        elif score == 100 or game_over:
            self.kill()


# FIRST BOSS!!
class Boss_v001(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_v1_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.top = y - 300
        self.speedy = 10
        self.killed = False
        

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom == HEIGHT / 2:
            self.speedy = 0

        if score > 100:
            self.image = boss_v1_death
            self.speedy = -10
            if self.rect.bottom == HEIGHT - 800:
                self.kill()


# MEOW BOSS
class SuperBoss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = cat_boss[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.top = y - 300
        self.speedy = 3
        self.shot_animation = False
        self.shot_delay = 3
        self.shot_sprite = 1
        self.shot_timer = 0
        self.hp = 100
        



    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT / 2:
            self.speedy = 0
            ## self.rect.x += 5
            ## if self.rect.right > WIDTH:
            ##   self.rect.x -= 5
            #### UZNAT CHO NE TAK!


        if self.shot_animation:
            self.shot_timer += 1
            if self.shot_timer == self.shot_delay:
                self.shot_timer = 0
                self.shot_sprite += 1
                if self.shot_sprite >= len(cat_boss):
                    self.shot_sprite = 0
                    self.shot_timer = 0
                    self.shot_animation = False
                else:
                    self.image = cat_boss[self.shot_sprite]


        if self.hp < 0:
            self.kill()

    def start_shoot(self):
        self.shot_sprite = 0
        self.shot_timer = 0
        self.shot_animation = True

class BossBull(pygame.sprite.Sprite):
    def __init__(self, x, y, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speedy

    def update(self):
        self.rect.y -= self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()




# Groupping all sprites
all_sprites = pygame.sprite.LayeredUpdates()
enemies = pygame.sprite.Group()
pl_bullets = pygame.sprite.Group()
e_bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Creating new object as instance of player class
player = Player()



# Adding player sprites to all sprites
all_sprites.add(player)

# Spawning enemies
for i in range(3):
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)
enemy = Enemy()

boss = Boss_v001()
bossv1 = pygame.sprite.Group()

cat = SuperBoss()
catsg = pygame.sprite.Group()

# The timer is the time in seconds until the enemy shoots.
timer = random.uniform(0, 1)  # Random float 0 and 1
dt = 0


# ZA GAME LOOP
running = True
while running:

    for event in pygame.event.get():
        # Closing the window!
        if event.type == pygame.QUIT:
            running = False

        # IF up arrow - shoot
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.shoot()
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Making ENEMIES shoot bullets:
 
    # Decrease the timer by the delta time.
    timer -= dt
    if timer <= 0 and score < 100 and game_over == False:  # Ready to fire.
        # Pick a random enemy to get the x and y coords.
        random_enemy = random.choice(enemies.sprites())
        enemy_x = random_enemy.rect.centerx
        enemy_y = random_enemy.rect.bottom
        # Create a bullet and add it to the sprite groups.
        bullet = EnemyBull(enemy_x, enemy_y, random_enemy.speedy+2)
        all_sprites.add(bullet)
        e_bullets.add(bullet)
        timer = random.uniform(0, 1)  # Reset the timer.



    # clock.tick returns the time that has passed since the last frame.
    dt = clock.tick(60) / 1000  # / 1000 to convert it to seconds.

    clock.tick(FPS)

    # Update
    all_sprites.update()


    # Check if enemy hits player
    hits = pygame.sprite.spritecollide(player, enemies, False)
    for hit in hits:
        player.hp -= 1
        hit.kill()
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)

        expl = Explosion(player.rect.center)
        all_sprites.add(expl)
        if player.hp == 0:
            game_over = True  # game over!!


    # Check if bullet hits an enemy
    hits = pygame.sprite.groupcollide(enemies, pl_bullets, True, True)
    for hit in hits:
        score += 50
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
        expl = Explosion(hit.rect.center)
        all_sprites.add(expl)

        if random.random() > 0.85:
            powup = Powerup(hit.rect.center)
            all_sprites.add(powup)
            powerups.add(powup)


    # Check if powerup hits a player
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if player.hp != 3:
            player.hp += 1



    # Check if bullet hits a player
    hits = pygame.sprite.spritecollide(player, e_bullets, False)
    for hit in hits:
        player.hp -= 1
        hit.kill()
        expl = Explosion(player.rect.center)
        all_sprites.add(expl)

        if player.hp == 0:
            game_over = True  # game over!!


    # Drawing scrolling BG
    if game_over == False:
        rel_y = y % bg.get_rect().height
        screen.blit(bg, (0, rel_y - bg.get_rect().height))
        if rel_y < HEIGHT:
            screen.blit(bg, (0, rel_y))
        y -= 1

    elif game_over:
        screen.blit(bg, (0,0))


    # Drawing sprites
    all_sprites.draw(screen)
    
    # Draw boss if score == 5000!!!!!!!!! 
    # DONT FORGET TO CTRL+F AND CHANGE IT EVERYWHERE

    # FIRST BOSS

    if score >= 100 and game_over == False:
        bossv1.add(boss)
        all_sprites.add(boss)
     
        if boss.speedy == 0:
            hits = pygame.sprite.groupcollide(pl_bullets, bossv1, True, False)
            for hit in hits:
                score += 1
                expl = Explosion(boss.rect.center)
                all_sprites.add(expl, layer=100)
                all_sprites.move_to_front(expl)
                boss.killed = True

                if score == 102:
                    score -= 1

    # CAT BOSS

    if boss.killed:
        catsg.add(cat)
        all_sprites.add(cat)

        draw_boss_hp(screen, WIDTH - 600, 50, cat.hp)


        if cat.speedy == 0 and game_over == False:  # Ready to fire.

            hits = pygame.sprite.groupcollide(pl_bullets, catsg, True, False)
            for hit in hits:
                score += 1
                cat.hp -= 10

            timer -= dt
            if timer <= 0: 
                boss_x = cat.rect.centerx
                boss_y = cat.rect.bottom
                bullet = BossBull(boss_x, boss_y, boss.speedy)
                all_sprites.add(bullet)
                e_bullets.add(bullet)

                cat.start_shoot()
                

                timer = random.uniform(0, 2)

                

    if game_over == False:
        # Drawing score and player hp
        draw_text(screen, ("SCORE: " + (str(score))), 18, WIDTH / 2, 10)
        draw_hp(screen, WIDTH - 140, 5, player.hp, player_hp_img)
        # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
