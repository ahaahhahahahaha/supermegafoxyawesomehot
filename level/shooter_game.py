#Create your own shooter

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, char_img, x, y, char_width, char_height, char_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(char_img), (char_width, char_height))
        self.speed = char_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width:
            self.rect.x += self.speed

    def fire(self):
        bullet= Bullet('bullet.png', self.rect.x, self.rect.y, 9, 5, 3)
        list_bullets.add(bullet)


class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed

        if self.rect.y > win_height:
            self.rect.y = 0
            missed += 1

class Bullet (GameSprite):
    def update(self):
        self.rect.y -= self.speed
        
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.Font("Arial", 80)


win_width = 700
win_height = 500
missed = 0
score = 0

win = font1.render('YOU WIN!', True, (255, 255, 255 ))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")

background = GameSprite('galaxy.jpg', 0, 0, win_width, win_height, 0)
rocket_ronnie = Player("rocket.png", 100, win_height - 100, 30, 50, 5)

list_enemies = sprite.Group()
for i in range(6):
    random_x = randint(0, win_width)
    speed = randint(1, 5)
    stinkyenemies = Enemy("ufo.png", random_x, 0, 50, 30, speed)
    list_enemies.add(stinkyenemies)

list_bullets = sprite.Group()





finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket_ronnie.fire() 
                fire_sound.play()
                

    if not finish:
        background.reset()
        rocket_ronnie.update()
        rocket_ronnie.reset()
        list_enemies.update()
        list_enemies.draw(window)
        list_bullets.update()
        list_bullets.draw(window)

        font2 = font.Font (None, 20)
        score_text= font2.render("Score: "+ str(score), False, (255, 255, 255))
        missed_text = font2.render("Missed: " + str(missed), False, (255, 255, 255))
        window.blit(score_text, (50, 100))
        window.blit(missed_text, (50, 200))

        if sprite.spritecollide(rocket_ronnie, list_enemies, False) or missed > 3:
            finish = True
            window.blit(lose, (win_width/2, win_height/2))

        if sprite.groupcollide(list_bullets, list_enemies, True, True):
            score += 1
            random_X = randint( 0, win_width)
            alien = Enemy("ufo.png", random_X, 0, 100, 100, 2)
            list_enemies.add(alien)

            if score >= 20:
                finish = True
                window.blit(win, (win_width/2, win_height/2))
        

    display.update()
    time.delay(50)