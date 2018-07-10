import os
import sys
import pygame
import random
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')



pygame.init()

running = True


# COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (32, 32, 32)
LIGHTER_GREY = (48, 48, 48)

# Screen settings
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# FPS and time module
FPS = 60
clock = pygame.time.Clock()


# Window Title
pygame.display.set_caption('GOTY')


# LOADING IMAGES

#ICON
gameIcon = pygame.image.load(os.path.join("data", "imgs", "icon.png"))
pygame.display.set_icon(gameIcon)

# BG img
bg = pygame.image.load(os.path.join("data", "imgs", "bg.png")).convert_alpha()
bg_y = 0

#Cat boss imgs loading
cat_boss = []
for i in range(7):
    filename = 'catbo0{}.png'.format(i)
    img = pygame.image.load(os.path.join("data", "imgs", filename)).convert_alpha()
    cat_boss.append(img)

# Explosion animations loading
explosion_anim = []
for i in range(3):
    filename = 'explosion{}.png'.format(i)
    img = pygame.image.load(os.path.join("data", "imgs", filename)).convert_alpha()
    explosion_anim.append(img)

# Player img
player_img = pygame.image.load(os.path.join
    ("data", "imgs", "player_ship.png")).convert_alpha()

player_img2 = pygame.image.load(os.path.join
    ("data", "imgs", "player_ship2.png")).convert_alpha()

player_img3 = pygame.image.load(os.path.join
    ("data", "imgs", "player_ship3.png")).convert_alpha()

player_img4 = pygame.image.load(os.path.join
    ("data", "imgs", "player_ship4.png")).convert_alpha()

player_dmg = pygame.image.load(os.path.join
    ("data", "imgs", "player_ship_damage.png")).convert_alpha()

player_blinking_sprites = [player_img]*3 + [player_dmg]*3

# Img for hp
player_hp_img = pygame.image.load(os.path.join("data", "imgs", "hp.png")).convert_alpha()

# Enemy img
enemy_img = pygame.image.load(os.path.join("data", "imgs", "enemy_ship.png")).convert_alpha()
enemy_img2 = pygame.image.load(os.path.join("data", "imgs", "enemy_ship2.png")).convert_alpha()

# Player bullet
player_bullet = pygame.image.load(os.path.join("data", "imgs", "player_bullet.png")).convert_alpha()

# Enemy bullet
enemy_bullet = pygame.image.load(os.path.join("data", "imgs", "enemy_bullet.png")).convert_alpha()

# BOSS bullet
boss_bullet = pygame.image.load(os.path.join("data", "imgs", "boss_bull.png")).convert_alpha()

# POWERUP
hp_powerup = pygame.image.load(os.path.join("data", "imgs", "powerup_hp.png")).convert_alpha()

# FIRST BOSS
boss_v1_img = pygame.image.load(os.path.join("data", "imgs", "boss_v1.png")).convert_alpha()
boss_v1_death = pygame.image.load(os.path.join("data", "imgs", "boss_v228.png")).convert_alpha()

# LOADING IMGS END

# LOADING SOUNDS

# Player shooting sound
player_shoot_sound = pygame.mixer.Sound(os.path.join("data", "sounds", "player_shoot.ogg"))

# Cat sounds
cat_dmg_sound = pygame.mixer.Sound(os.path.join("data", "sounds", "cat_dmg.wav"))

# Loading and playing bg sound
pygame.mixer.music.load(os.path.join("data", "sounds", "bg3.ogg")) 
pygame.mixer.music.play(-1,0.0)

# LOADING SOUNDS END

# FUNC START

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

reset = False
def button(text,x,y,width,height,active,inactive,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global paused, reset, running

    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(screen, active, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "play":
                while game_loop():
                    reset = False
            elif action == "continue":
                paused = False
            elif action =="quit":
                pygame.quit()
                quit()
            elif action == "reset":
                reset = True
    else:
        pygame.draw.rect(screen, inactive, (x, y, width, height))

    draw_text(screen, text, 32, 400, y + 5)

# FUNC END


# INTRO
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.blit(bg, (0,0))
        draw_text(screen, ("MENU"), 80, WIDTH / 2, HEIGHT - 650)

        button("START", 275, 300, 250, 50, LIGHTER_GREY, GREY, "play")
        button("QUIT", 275, 400, 250, 50, LIGHTER_GREY, GREY, "quit")

        pygame.display.update()
        clock.tick(FPS)

# END OF GAME INTO FUNC

# INTRO
paused = False

def game_paused():
    global paused
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.blit(bg, (0,0))
        draw_text(screen, ("MENU"), 80, WIDTH / 2, HEIGHT - 650)
        button("CONTINUE", 275, 300, 250, 50, LIGHTER_GREY, GREY, "continue")
        button("RESET", 275, 380, 250, 50, LIGHTER_GREY, GREY, "reset")
        button("QUIT", 275, 460, 250, 50, LIGHTER_GREY, GREY, "quit")

        pygame.display.update()
        clock.tick(FPS)
        if reset:
            paused = False
            return True
    return False

# END OF GAME INTO FUNC

    

# GAME FUNC
def game_loop():
    global bg_y, running
    #GAME OVER
    game_over = False
    victory = False
    # SCORE
    score = 0

        # CLASSES
        
    # Creating a Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = player_img
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 0
            self.speedy = 0
            self.hp = 3
            self.blinking = False
            self.blink_counter = 0
            self.sprite_counter = 0

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


            if self.blinking:
                self.image = player_blinking_sprites[self.sprite_counter]
                self.sprite_counter += 1
                if self.sprite_counter >= len(player_blinking_sprites):
                    self.sprite_counter = 0
                    self.blink_counter += 1

                if self.blink_counter > 3:
                    self.blink_counter = 0
                    self.blinking = False


            if game_over:
                self.rect.bottom = HEIGHT + 100

        
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



            if score == 5000:
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


            elif score == 5000:
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

            elif score == 5000:
                self.kill()


    # FIRST BOSS!!
    class Boss_v001(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = boss_v1_img
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.top = -300
            self.speedy = 10
            self.killed = False
            

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom > HEIGHT / 2:
                self.speedy = 0

            if score > 5000:
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
            self.rect.top = -300
            self.speedy = 3
            self.speedx = 0
            self.shot_animation = False
            self.shot_delay = 3
            self.shot_sprite = 1
            self.shot_timer = 0
            self.hp = 100
            self.killed = False
            

        def update(self):
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if self.rect.bottom > HEIGHT / 2:
                self.speedy = 0


            if self.rect.right == 800 and self.speedx > 0:
                self.speedx *= -1
            elif self.rect.left == 0 and self.speedx < 0:
                self.speedx *= -1
                
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


            if self.hp <= 0:
                self.kill()
                self.killed = True

        def start_shoot(self):
            self.shot_sprite = 0
            self.shot_timer = 0
            self.shot_animation = True


        def move(self):
            if self.speedx == 0 and self.speedy == 0:
                self.speedx = 5 # *random.choice([1 ,-1])
            if self.rect.right > 760 and self.speedx > 0:
                self.speedx *= -1
            elif self.rect.left < 40 and self.speedx < 0:
                self.speedx *= -1

    class BossBull(pygame.sprite.Sprite):
        def __init__(self, x, y, speedy):
            pygame.sprite.Sprite.__init__(self)
            self.image = boss_bullet
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = speedy

        def update(self):
            self.rect.y -= self.speedy
            # kill if it moves off the top of the screen
            if self.rect.top > HEIGHT:
                self.kill()

    # CLASSES END


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



    while running:
        for event in pygame.event.get():
            # Closing the window!
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            # IF up arrow - shoot
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    stop = game_paused()
                    if stop:
                        return stop
                elif event.key == pygame.K_q:
                    pygame.quit()


        # Making ENEMIES shoot bullets:
     
         # The timer is the time in seconds until the enemy shoots.
        enemy_timer = random.uniform(0, 1)  # Random float 0 and 1
        dt = 0


        # clock.tick returns the time that has passed since the last frame.
        dt = clock.tick(FPS) / 1000  # / 1000 to convert it to seconds.

        clock.tick(FPS)


        # Decrease the timer by the delta time.
        enemy_timer -= dt
        if enemy_timer <= 0 and score < 5000 and game_over == False:  # Ready to fire.
            # Pick a random enemy to get the x and y coords.
            random_enemy = random.choice(enemies.sprites())
            enemy_x = random_enemy.rect.centerx
            enemy_y = random_enemy.rect.bottom
            # Create a bullet and add it to the sprite groups.
            bullet = EnemyBull(enemy_x, enemy_y, random_enemy.speedy+2)
            all_sprites.add(bullet)
            e_bullets.add(bullet)
            timer = random.uniform(0, 1)  # Reset the timer.




        # Update
        all_sprites.update()


        # Check if enemy hits player
        hits = pygame.sprite.spritecollide(player, enemies, False)
        for hit in hits:
            player.hp -= 1
            player.blinking = True
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
            player.blinking = True
            hit.kill()
            expl = Explosion(player.rect.center)
            all_sprites.add(expl)

            if player.hp == 0:
                game_over = True  # game over!!

        # BACKGROUND START

        # Drawing scrolling BG
        if game_over == False:
            rel_y = bg_y % bg.get_rect().height
            screen.blit(bg, (0, rel_y - bg.get_rect().height))
            if rel_y < HEIGHT:
                screen.blit(bg, (0, rel_y))
            bg_y -= 1

            # Drawing sprites
            all_sprites.draw(screen)

        elif game_over:
            screen.blit(bg, (0,0))
            draw_text(screen, ("GAME OVER"), 48, WIDTH / 2, HEIGHT - 600)
            draw_text(screen, ("PRESS ESC TO ENTER THE MENU"), 20, WIDTH / 2, HEIGHT - 530)
            draw_text(screen, ("YOU SCORED " + (str(score))), 20, WIDTH / 2, HEIGHT - 500)

        if victory:
            screen.blit(bg, (0,0))
            draw_text(screen, ("VICTORY!!"), 54, WIDTH / 2, HEIGHT - 600)
            draw_text(screen, ("YOU SCORED " + (str(score))), 20, WIDTH / 2, HEIGHT - 500)
            draw_text(screen, ("MADE WITH LOVE BY ANASTASIYA OVINNIKOVA"), 20, WIDTH / 2, HEIGHT - 450)
            draw_text(screen, ("PRESS ESC TO ENTER THE MENU"), 20, WIDTH / 2, HEIGHT - 450)

        # BACKGROUND END



        # DRAWING SPRITES
        
        

        # FIRST BOSS

        if score >= 5000:
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

                    if score == 5002:
                        score -= 1

        # CAT BOSS

        if boss.killed:
            if game_over == False and cat.killed == False:
                draw_boss_hp(screen, WIDTH - 600, 50, cat.hp)

            catsg.add(cat)
            all_sprites.add(cat)


            if cat.speedy == 0 and cat.killed == False:  # Ready to fire.

                if cat.speedx != 0:
                    hits = pygame.sprite.groupcollide(pl_bullets, catsg, True, False)
                    for hit in hits:
                        cat_dmg_sound.play()
                        score += 1
                        cat.hp -= 10
                        expl = Explosion(cat.rect.center)
                        all_sprites.add(expl, layer=100)
                        #all_sprites.move_to_front(expl)
                timer = random.uniform(0, 0.3)
                timer -= dt
                if timer <= 0: 
                    boss_x = cat.rect.centerx
                    boss_y = cat.rect.bottom
                    bullet = BossBull(boss_x, boss_y, boss.speedy)
                    all_sprites.add(bullet)
                    e_bullets.add(bullet)

                    cat.start_shoot()
                    

                    timer = random.uniform(0, 0.3)
                    cat.move()


        if cat.killed:
            player.rect.y += player.speedy
            player.speedy = -4
            if player.rect.top < 0:
                player.kill()
                victory = True


        if game_over == False and cat.killed == False:
            # Drawing score and player hp
            draw_text(screen, ("SCORE: " + (str(score))), 18, WIDTH / 2, 10)
            draw_hp(screen, WIDTH - 140, 5, player.hp, player_hp_img)
            # *after* drawing everything, flip the display
        pygame.display.flip()

    # END OF GAME FUNC


game_intro()
pygame.quit()