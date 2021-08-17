#sprite classes

from settings import *
import pygame as pg
import math
import random

class Player(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.og_image = pg.Surface((50, 50))
        self.og_image.fill(GREEN)
        self.og_image.set_colorkey(BLACK)
        self.image = self.og_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.last_attack = pg.time.get_ticks()
        self.vx = 0
        self.vy = 0
        self.rot = 0
        self.delay = 500
        self.allow_move = True
        self.health = 3
        self.mana = 100
        self.immortal = False
        print("arrow keys-move, space-sword, c-spell")
        #self.vel = 0
    
    def rotate(self):
        n_image = pg.transform.rotate(self.og_image, self.rot)
        og_center = self.rect.center
        self.image = n_image
        self.rect = self.image.get_rect()
        self.rect.center = og_center

    def attack(self):
        now = pg.time.get_ticks()
        if now - self.last_attack > self.delay:
            self.last_attack = now
            sword  = Sword(self.game, self.rot, self)
            self.game.all_sprites.add(sword)
            self.game.attack.add(sword)
            self.allow_move = False
        
    def shoot(self):
        spell = Spell(self.game, self.rot, self)
        self.game.all_sprites.add(spell)
        self.game.attack.add(spell)
        self.mana -= 25

    def move(self):
        keys = pg.key.get_pressed()
        if self.allow_move:
            if keys[pg.K_RIGHT]:
                if keys[pg.K_UP]:
                    self.rot = 315
                    #calculates speed based on components so diagonal speed is same as vertical and horizontal
                    self.vx = SPEED * math.cos(math.radians(self.rot))
                    self.vy = SPEED * math.sin(math.radians(self.rot))
                elif keys[pg.K_DOWN]:
                    self.rot = 225
                    self.vx = -SPEED * math.cos(math.radians(self.rot))
                    self.vy = -SPEED * math.sin(math.radians(self.rot))
                else:
                    self.vx = SPEED
                    self.rot = 270
                    self.rotate()
            if keys[pg.K_LEFT]:
                if keys[pg.K_UP]:
                    self.rot = 45
                    self.vx = -SPEED * math.cos(math.radians(self.rot))
                    self.vy = -SPEED * math.sin(math.radians(self.rot))
                elif keys[pg.K_DOWN]:
                    self.rot = 135
                    self.vx = SPEED * math.cos(math.radians(self.rot))
                    self.vy = SPEED * math.sin(math.radians(self.rot))
                else:
                    self.vx = -SPEED
                    self.rot = 90
                    self.rotate()
            if keys[pg.K_UP] and not keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
                self.vy = -SPEED
                self.rot = 0
                self.rotate()
            if keys[pg.K_DOWN] and not keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
                self.vy = SPEED
                self.rot = 180
                self.rotate()

    def update(self):
        self.vx = 0
        self.vy = 0
        self.move()
        #self.vel = ((self.vx*math.sin(math.radians(self.rot)))+(self.vy*math.cos(math.radians(self.rot))))
        #print(self.vel)
        if self.immortal and pg.time.get_ticks() - self.immortal_timer > 1000:
            self.immortal = False
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
    
    def hit(self):
        self.immortal = True
        self.immortal_timer = pg.time.get_ticks()

class Sword(pg.sprite.Sprite):
    def __init__(self, game, angle, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 60))
        self.image.fill(WHITE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image, angle)
        old_center = self.rect.center 
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.player = player
        print(angle)
        if angle == 0:
            self.rect.centerx = self.player.rect.centerx
            self.rect.bottom = self.player.rect.centery
        elif angle == 270:
            self.rect.centerx = self.player.rect.right
            self.rect.bottom = self.player.rect.centery
        elif angle == 180:
            self.rect.centerx = self.player.rect.centerx
            self.rect.top = self.player.rect.centery
        elif angle == 90:
            self.rect.centerx = self.player.rect.left
            self.rect.bottom = self.player.rect.centery       
        elif angle == 45:
            self.rect.centerx = self.player.rect.left
            self.rect.bottom = self.player.rect.centery
        elif angle == 135:
            self.rect.centerx = self.player.rect.left
            self.rect.top = self.player.rect.centery
        elif angle == 225:
            self.rect.centerx = self.player.rect.right
            self.rect.top = self.player.rect.centery
        elif angle == 315:
            self.rect.centerx = self.player.rect.right
            self.rect.bottom = self.player.rect.centery     
        self.last_update = pg.time.get_ticks()
        
    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > FPS*2.5:
            self.last_update = now
            self.player.allow_move = True
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.og_image = pg.Surface((50, 50))
        self.og_image.fill(RED)
        self.og_image.set_colorkey(BLACK)
        self.image = self.og_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(50, WIDTH-50), random.randrange(50, HEIGHT-50))
        self.speed = 2
        self.moving_left = False
        self.moving_right = False

    def update(self):
        if self.rect.right <= WIDTH and not self.moving_left:
            self.rect.x += self.speed
            self.moving_right = True
        if self.rect.right > WIDTH:
            self.moving_right = False
        if self.rect.left >= 0 and not self.moving_right:
            self.rect.x -= self.speed
            self.moving_left = True
        if self.rect.left < 0:
            self.moving_left = False
            
    def attack(self):
        pass

    def rotate(self):
        pass
    
class Spell(pg.sprite.Sprite):
    def __init__(self, game, angle, player):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((25, 25))
        self.image.fill(BLUE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image, angle)
        old_center = self.rect.center 
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.player = player
        if angle == 0:
            self.vx = 0
            self.vy = -SPEED
            self.rect.centerx = self.player.rect.centerx
            self.rect.bottom = self.player.rect.centery
        elif angle == 270:
            self.vx = SPEED
            self.vy = 0
            self.rect.centerx = self.player.rect.right
            self.rect.centery = self.player.rect.centery
        elif angle == 180:
            self.vx = 0
            self.vy = SPEED
            self.rect.centerx = self.player.rect.centerx
            self.rect.top = self.player.rect.centery
        elif angle == 90:
            self.vx = -SPEED
            self.vy = 0
            self.rect.centerx = self.player.rect.left
            self.rect.centery = self.player.rect.centery       
        elif angle == 45:
            self.vx = -SPEED * math.cos(math.radians(angle))
            self.vy = -SPEED * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.left
            self.rect.bottom = self.player.rect.centery
        elif angle == 135:
            self.vx = SPEED * math.cos(math.radians(angle))
            self.vy = SPEED * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.left
            self.rect.top = self.player.rect.centery
        elif angle == 225:
            self.vx = -SPEED * math.cos(math.radians(angle))
            self.vy = -SPEED * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.right
            self.rect.top = self.player.rect.centery
        elif angle == 315:
            self.vx = SPEED * math.cos(math.radians(angle))
            self.vy = SPEED * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.right
            self.rect.bottom = self.player.rect.centery     
        self.last_update = pg.time.get_ticks()
        self.vx *= 1.5
        self.vy *= 1.5

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.bottom < -30 or self.rect.left < -30 or self.rect.right > WIDTH+30 or self.rect.top > HEIGHT+30:
            self.kill()         