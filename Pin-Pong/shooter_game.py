from pygame import *
from random import randint
from time import time as timer
#створи вікно гри
window = display.set_mode((500, 500))
display.set_caption('Стрелялка')
#задай фон сцени
background = transform.scale(image.load('Phon.png'), (500, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 500 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("Pyla.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 420)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 720:
            self.rect.y = 0
            self.rect.x = randint(80, 420)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid('asteroid.png', randint(30, 420), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('Vrag.png', randint(80, 420), -40, 80, 50, randint(2, 3))
    monsters.add(monster)

font.init()
font1 = font.SysFont('Arial', 36)

life = 3
lost = 0
score = 0
bullets = sprite.Group()

rel_time = False

num_fire = 0
life = 3

ship = Player("Igrok.png", 5, 500 - 100, 80, 100, 8)
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0,0))
        text = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        clock.tick(FPS)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render('идет перезарядка...', 1, (150, 0, 0,))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('Vrag.png', randint(80, 420), -40, 80, 50, randint(2, 3))
            monsters.add(monster)
        if score >= 10:
            finish = True
            win = font1.render('YOU WIN!!!', True, (255, 255, 255))
            window.blit(win, (200, 200))
        if life == 0 or lost >= 3:
            finish = True
            lose = font1.render('YOU LOSE!!!', True, (180, 0, 0))
            window.blit(lose, (200, 200))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (470, 10))
        display.update()
    time.delay(20)