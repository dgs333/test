from typing import Any
import pygame as pg
from random import randint

pg.init()
pg.font.init()


#hello

class Base_sprite(pg.sprite.Sprite):
    def __init__(self, pic, x, y, w, h, hb_x=0, hb_y=0):
        super().__init__()
        self.picture = pg.transform.scale(pg.image.load(pic), (w, h))
        self.image = self.picture
        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        center = self.rect.center
        self.rect.width = self.rect.width- self.rect.width/100*hb_x
        self.rect.height = self.rect.height- self.rect.height/100*hb_y
        self.rect.center = center
        self.delta_x = self.rect.x - x
        self.delta_y = self.rect.y - y


    def draw(self):
        mw.blit(self.picture, (self.rect.x-self.delta_x, self.rect.y-self.delta_y))
        #pg.draw.rect(mw, (255,0,0), self.rect, 3)


class Hero(Base_sprite):
    speed = 7
    energy = 0
    points = 1
    health = 100


    lvl = 1
    kd = 20
    miss = 0
    speed_spawn = 0

    def update(self):
        self.energy += 1
        keys = pg.key.get_pressed()
        if keys[pg.K_a] and self.rect.x >= 5:
            self.rect.x -= self.speed

        if keys[pg.K_d] and self.rect.x <= win_w - self.rect.w:
            self.rect.x += self.speed

        if keys[pg.K_SPACE]:
            self.fire()
    
    def draw(self):
        super().draw()
        g = 255/100*self.health
        
        if g < 0:
            g = 0
        
        r = 255 - g
        if r > 255:
            r = 255
        b = 0
        
        rect = pg.Rect(self.rect.x, self.rect.bottom+5, self.rect.width/100*self.health, 5)
        pg.draw.rect(mw, (r,
                          g,
                          b), rect)
    
        

    def fire(self):
        if self.energy >= self.kd:
            shoot_sound.play()
            self.energy = 0
            bullet = Bullet("pula.png", self.rect.x +
                            self.rect.width/2-15/2, self.rect.y-40, 15, 40)
            bullets.add(bullet)


    def lvl_up(self):
        if self.points % 20 == 0:
            self.kd -= 0.1
            self.speed += 0.1
            self.points += 1
            self.lvl += 1
            if self.health <= 90:
                self.health += 10
            

class Bullet(Base_sprite):
    

    speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            bullets.remove(self)

                # print(hero.points)


class Star(Base_sprite):
    speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_h:
            stars.remove(self)


class Nlo(Base_sprite):
    speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_h:
            ufos.remove(self)
            hero.miss += 1

class Boom(pg.sprite.Sprite):
    def __init__(self, ufo_center, boom_sprites, booms) -> None:
        super().__init__()            
        self.frames = boom_sprites        
        self.frame_rate = 1   
        self.frame_num = 0
        self.image = boom_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = ufo_center
        self.add(booms)
    
    def next_frame(self):
        self.image = self.frames[self.frame_num]
        self.frame_num += 1
        if self.frame_num > len(self.frames)-1:
            self.frame_num = 0
        
    
    def update(self):
        self.next_frame()
        if self.frame_num == len(self.frames)-1:
            self.kill()

class Meteor(Boom):
    def __init__(self, center, meteor_sprites, meteors) -> None:
        super().__init__(center, meteor_sprites, meteors)
        self.speed_y = randint(1, 10)
        self.speed_x = randint(-2, 2)


    def update(self):
        self.next_frame()
        self.rect.x += self.speed_x 
        self.rect.y += self.speed_y
        #print(self.rect.y, self.speed_y)

        

def make_stars():
    size = randint(20, 81)
    star = Star('star2.png', randint(0, win_w), -10, size, size)
    star.speed = randint(3, 20)
    stars.add(star)


def make_Nlos():
    nlo = Nlo('ufo2.png', randint(0, win_w-70), -10, 70, 55, 0, 20)
    ufos.add(nlo)

def set_text(text, x,y, color=(255,1,1)):
    mw.blit(f1.render(text, True, color), (x, y))


def sprites_load(folder, file_name, size, colorkey=(0,0,0)):    
    sprites = []
    load = True
    num = 1
    while load:
        try:
            spr = pg.image.load(f'{folder}\\{file_name}{num}.png')
            spr = pg.transform.scale(spr,size)
            if colorkey: spr.set_colorkey(colorkey)
            sprites.append(spr)
            num += 1
        except:
            load = False
    return sprites


win_w = 1000
win_h = 700
mw = pg.display.set_mode((win_w, win_h))
pg.display.set_caption("")
fon = pg.transform.scale(pg.image.load("fon3.jpg"), (win_w, win_h))

clock = pg.time.Clock()
mw.blit(fon, (0, 0))


pg.mixer.init()
pg.mixer.music.load('space.ogg')
pg.mixer.music.play()
shoot_sound = pg.mixer.Sound('fire.ogg')
boom_sound = pg.mixer.Sound("Boom1.ogg")


hero = Hero("hero2.png", win_w/2-35, win_h-85-10-10, 70, 85)

stars = pg.sprite.Group()
#stars = []
ufos = pg.sprite.Group()
bullets = pg.sprite.Group()
booms = pg.sprite.Group()
meteors = pg.sprite.Group()

boom_sprite = sprites_load("boom4", 'boom', (80, 80))
meteors_sprite = [
    sprites_load("meteor1", 'meteor', (80, 80)),
    sprites_load("meteor1", 'meteor', (70, 70)),
    sprites_load("meteor1", 'meteor', (60, 60)),
    sprites_load("meteor1", 'meteor', (50, 50)),
    sprites_load("meteor1", 'meteor', (40, 40)),
    sprites_load("meteor1", 'meteor', (30, 30)),

]#sprites_load("meteor1", 'meteor', (80, 80))

y_win = pg.transform.scale(pg.image.load("lose.jpg"), (win_w, win_h))
y_lose = pg.transform.scale(pg.image.load('lose.jpg'), (win_w, win_h))

f1 = pg.font.Font(None, 36)
f2 = pg.font.Font(None, 20)


ticks = 0
win = False
game = True
play = True
while play:
    mw.blit(fon, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            play = False
    
    if ticks % 15 == 0:
        make_stars()

    if ticks % 45 - hero.speed_spawn == 0:
        make_Nlos()

    if ticks % 50 == 0:
        Meteor((randint(0, win_w), -100), meteors_sprite[randint(0, len(meteors_sprite)-1)], meteors)
        #pass
    
    if game:

        stars.update()
        ufos.update()
        bullets.update()
        booms.update()
        hero.update()
        meteors.update()

        colides = pg.sprite.groupcollide(bullets, ufos, True, True)
        for ufo, bullet in colides.items():
            boom_sound.play()
            Boom(ufo.rect.center, boom_sprite, booms)
            hero.points += 1
        
        if pg.sprite.spritecollide(hero, ufos, False):
            hero.health -= 3
            if hero.health <= 0:
                game = False


        stars.draw(mw)
        ufos.draw(mw)
        bullets.draw(mw)
        booms.draw(mw)
        meteors.draw(mw)
        
        set_text(f'Очки: {hero.points}', 20, 20)
        set_text(f'Пропущено: {hero.miss}', 20, 50)
        
        
        
        
        

        hero.draw()
        


        #hero.lvl_up()

    else:
        mw.blit(y_lose, (0, 0))

    

    pg.display.update()
    clock.tick(60)
    ticks += 1
    # print(len(stars))



