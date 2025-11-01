#import module
from pygame import *
from random import randint

#import music
mixer.init()
mixer.music.load("space.ogg") #backsound
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg") #bullet sound effect

#import fonts
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)

#import image/background
img_background = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"

#statistic
score = 0 #Bullet x Enemy
lost = 0 #missed Enemy
max_lost = 3 #max. missed
goal = 10 #min. kill


'''Class (Sprite property n method)'''
#class GameSprite, class utama
class GameSprite(sprite.Sprite):
    #Sprite property
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed #pixel per move
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #show Sprite
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#class Player
class Player(GameSprite):
    #Player movement (w, a, s, d)
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 100:
            self.rect.y += self.speed

    #Player fire
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

#class Enemy
class Enemy(GameSprite):
    #Enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost

        #pengulangan Enemy
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1

#class Bullet
class Bullet(GameSprite):
    #bullet movement
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


'''Window Interface'''
win_width = 700
win_height = 500

display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_background), (win_width,win_height))

#Sprite/Character/Group
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_height - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()


'''Game Looping'''
run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False #leave the game
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire() #fire
    
    if not finish:
        window.blit(background, (0,0))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1

            monster = Enemy(img_enemy, randint(80, win_height - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score >= goal:
            finish = True
            window.blit(win, (200,200))

        #score text
        txt_score = font2.render("Score:" + str(score), 1, (255,255,255))
        window.blit(txt_score, (10, 20)) #show text

        #missed text
        txt_lose = font2.render("Missed:" + str(lost), 1, (255,255,255))
        window.blit(txt_lose, (10, 50)) #show text

        #update sprite movement
        ship.update()
        monsters.update()
        bullets.update()

        #show sprite in window
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        display.update()
    time.delay(60)


