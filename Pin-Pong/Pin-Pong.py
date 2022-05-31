from pygame import *
from time import time as timer
#модули пайгейм и времени
window = display.set_mode((750, 500))
display.set_caption('Пинг-понг')
background = transform.scale(image.load('Phon.png'), (750, 500))

chetch_l = 0
chetch_r = 0
#def chetchik(a):

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

class Player1(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 500 - 120:
            self.rect.y += self.speed

class Player2(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 120:
            self.rect.y += self.speed

player1 = Player1("platforma.png", 75, 175, 30, 120, 10)
player2 = Player2("platforma.png", 625, 175, 30, 120, 10)
myachik = GameSprite("Myachik.png", 360, 210, 49, 49, 2)
finish = False
game = True

font.init()
font1 = font.SysFont('Arial', 36)

speed_x = 3
speed_y = 3

font1 = font.Font(None, 35)
lose1 = font1.render('player L win', True, (180, 0, 0))
font2 = font.Font(None, 35)
lose2 = font2.render('player R win', True, (180, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background, (0,0))
        text = font1.render(str(chetch_l) + ':' + str(chetch_r), 1, (0, 0, 0))
        window.blit(text, (350, 10))
        player1.reset()
        player2.reset()
        player1.update()
        player2.update()
        myachik.reset()
        myachik.rect.x += speed_x
        myachik.rect.y += speed_y
        if myachik.rect.y > 450 or myachik.rect.y == 0:
            speed_y *= -1
        if sprite.collide_rect(player1, myachik) or sprite.collide_rect(player2, myachik):
            speed_x *= -1
        if myachik.rect.x < 0:
            chetch_r += 1
            myachik.rect.x= 360
            myachik.rect.y= 210
        if myachik.rect.x > 700:
            chetch_l +=1
            myachik.rect.x= 360
            myachik.rect.y= 210
        if chetch_l == 20:
            window.blit(background, (0,0))
            text = font1.render(str(chetch_l) + ':' + str(chetch_r), 1, (0, 0, 0))
            window.blit(text, (350, 10))
            display.update()
            window.blit(lose1, (300, 250))
            finish = True
        if chetch_r == 20:
            window.blit(background, (0,0))
            text = font1.render(str(chetch_l) + ':' + str(chetch_r), 1, (0, 0, 0))
            window.blit(text, (350, 10))
            display.update()
            window.blit(lose2, (300, 250))
            finish = True
        display.update()
        time.delay(20)