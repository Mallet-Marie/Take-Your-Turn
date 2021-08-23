#sprite classes

from settings import *
import pygame as pg
import math
import random

class Player(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.og_image = self.game.player_imgs[0]
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
        self.last_shoot = pg.time.get_ticks()
        self.shoot_delay = 2000
        self.last_check = pg.time.get_ticks()
        self.check_delay = 350
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
        now = pg.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            spell = Spell(self.game, self.rot, self, BLUE, SPEED, 25, 25, 'player')
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
                    self.image = self.game.player_imgs[1]
                    #self.rotate()
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
                    self.image = self.game.player_imgs[2]
                    #self.rotate()
            if keys[pg.K_UP] and not keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
                self.vy = -SPEED
                self.rot = 0
                self.image = self.game.player_imgs[3]
                #self.rotate()
            if keys[pg.K_DOWN] and not keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
                self.vy = SPEED
                self.rot = 180
                self.image = self.game.player_imgs[0]
                #self.rotate()

    def check_area(self):
        if self.game.area != 5:
            if self.game.area == 1:
                if self.rect.right >= WIDTH-10:
                    self.rect.right = WIDTH - 10
                elif self.rect.left <= 10:
                    self.game.area = 3
                    self.rect.left += WIDTH
                    self.game.kill_all() #remove all enemy sprites when moving to new area
                    self.game.check_area()
                    for i in range(2): #spawns new enemies
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()
                elif self.rect.top <= 10:
                    self.game.area = 2
                    self.game.kill_all()
                    self.game.check_area()
                    for i in range(2):
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()
                    self.rect.top += HEIGHT
                elif self.rect.bottom >= HEIGHT-10:
                    self.rect.bottom = HEIGHT-10
                    
            elif self.game.area == 2:
                if self.rect.right >= WIDTH-10:
                    self.rect.right = WIDTH - 10
                elif self.rect.left <= 10:
                    self.game.area = 4
                    self.rect.left += WIDTH
                    self.game.kill_all()
                    self.game.check_area()
                    for i in range(2):
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()                
                elif self.rect.top <= 10:
                    self.rect.top = 10
                elif self.rect.bottom >= HEIGHT-10:
                    self.game.area = 1
                    self.rect.bottom -= HEIGHT - 10
                    self.game.kill_all()
                    self.game.check_area()
                    for i in range(2):
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()

            elif self.game.area == 3:
                if self.rect.right >= WIDTH-10:
                    self.game.area = 1
                    self.rect.right -= WIDTH
                    self.game.kill_all()
                    self.game.check_area()
                    for i in range(2):
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()
                elif self.rect.left <= 10:
                    self.rect.left = 10
                elif self.rect.top <= 10:
                    self.game.area = 4
                    self.game.kill_all()
                    self.game.check_area()
                    for i in range(2):
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()
                    self.rect.top += HEIGHT
                elif self.rect.bottom >= HEIGHT-10:
                    self.rect.bottom = HEIGHT-10

            elif self.game.area == 4:
                if self.rect.right >= WIDTH-10:
                    self.game.area = 2
                    self.rect.right -= WIDTH
                    self.game.kill_all()
                    self.game.check_area()
                    for i in range(2):
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()
                elif self.rect.left <= 10:
                    self.rect.left = 10
                elif self.rect.top <= 10:
                    self.rect.top = 10
                elif self.rect.bottom >= HEIGHT-10:
                    self.game.area = 3
                    self.rect.bottom -= HEIGHT - 10
                    self.game.kill_all()
                    self.game.check_area()
                    for i in range(2):
                        self.game.spawn()
                    for i in range(2):
                        self.game.spawn_ranged()

    def update(self):
        self.vx = 0
        self.vy = 0
        self.move()
        #self.vel = ((self.vx*math.sin(math.radians(self.rot)))+(self.vy*math.cos(math.radians(self.rot))))
        #print(self.vel)
        now = pg.time.get_ticks()
        if now - self.last_check > self.check_delay:
            self.last_check = now
            self.check_area()
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
        self.image = self.game.mummy_imgs[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(50, WIDTH-50), random.randrange(50, HEIGHT-50))
        self.speed = 1
        self.moving_left = False
        self.moving_right = False
        self.can_move = True
        self.type = 'melee'

    def update(self):
        for i, m in enumerate(self.game.mobs):
            if m == self:
                continue
            if m.rect.colliderect(self.rect):
                if self.rect.y < m.rect.y:
                    self.rect.y -= self.speed
                if self.rect.y > m.rect.y:
                    self.rect.y += self.speed
                if self.rect.y == m.rect.y:
                    self.rect.y += random.randint(-1, 1)
        NEW_WIDTH = WIDTH - 100
        if self.can_move:
            if self.rect.centerx > self.game.player.rect.centerx:
                self.rect.x -= self.speed
                self.image = self.game.mummy_imgs[1]
            elif self.rect.centerx < self.game.player.rect.centerx:
                self.rect.x += self.speed
                self.image = self.game.mummy_imgs[0]
            if self.rect.centery > self.game.player.rect.centery:
                self.rect.y -= self.speed
            elif self.rect.centery < self.game.player.rect.centery:
                self.rect.y += self.speed

    def attack(self):
        pass

    def rotate(self):
        pass
    
class Spell(pg.sprite.Sprite):
    def __init__(self, game, angle, player, colour, speed, x, y, spawn):
        pg.sprite.Sprite.__init__(self)
        if spawn == 'mob':
            self.image = game.poison_img
            self.image = pg.transform.scale(self.image, (x, y))
        elif spawn == 'player':
            self.image = pg.Surface((x, y))
            self.image.fill(colour)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.image = pg.transform.rotate(self.image, angle)
        old_center = self.rect.center 
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.player = player

        self.type = 'ranged'
        if angle == 0:
            self.vx = 0
            self.vy = -speed
            self.rect.centerx = self.player.rect.centerx
            self.rect.bottom = self.player.rect.centery
        elif angle == 270:
            self.vx = speed
            self.vy = 0
            self.rect.centerx = self.player.rect.right
            self.rect.centery = self.player.rect.centery
        elif angle == 180:
            self.vx = 0
            self.vy = speed
            self.rect.centerx = self.player.rect.centerx
            self.rect.top = self.player.rect.centery
        elif angle == 90:
            self.vx = -speed
            self.vy = 0
            self.rect.centerx = self.player.rect.left
            self.rect.centery = self.player.rect.centery       
        elif angle == 45:
            self.vx = -speed * math.cos(math.radians(angle))
            self.vy = -speed * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.left
            self.rect.bottom = self.player.rect.centery
        elif angle == 135:
            self.vx = speed * math.cos(math.radians(angle))
            self.vy = speed * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.left
            self.rect.top = self.player.rect.centery
        elif angle == 225:
            self.vx = -speed * math.cos(math.radians(angle))
            self.vy = -speed * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.right
            self.rect.top = self.player.rect.centery
        elif angle == 315:
            self.vx = speed * math.cos(math.radians(angle))
            self.vy = speed * math.sin(math.radians(angle))
            self.rect.centerx = self.player.rect.right
            self.rect.bottom = self.player.rect.centery     
        self.vx *= 1.5
        self.vy *= 1.5

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.bottom < -30 or self.rect.left < -30 or self.rect.right > WIDTH+30 or self.rect.top > HEIGHT+30:
            self.kill()    

class Ranged_Mob(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.snake_imgs[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(50, WIDTH-50), random.randrange(50, HEIGHT-50))
        self.speed = 1
        self.moving_left = False
        self.moving_right = False
        self.last_update = pg.time.get_ticks()
        self.type = 'melee'

    def update(self):
        for i, m in enumerate(self.game.mobs):
            if m == self:
                continue
            if m.rect.colliderect(self.rect):
                if self.rect.y < m.rect.y:
                    self.rect.y -= self.speed
                if self.rect.y > m.rect.y:
                    self.rect.y += self.speed
                if self.rect.y == m.rect.y:
                    self.rect.y += random.randint(-1, 1)
        NEW_WIDTH = WIDTH - 100
        if self.rect.right <= NEW_WIDTH and not self.moving_left:
            self.image = self.game.snake_imgs[2]
            self.rect.x += self.speed
            self.moving_right = True
        if self.rect.right > NEW_WIDTH:
            self.moving_right = False
        if self.rect.left >= 100 and not self.moving_right:
            self.rect.x -= self.speed
            self.image = self.game.snake_imgs[0]
            self.moving_left = True
        if self.rect.left < 100:
            self.moving_left = False
        now = pg.time.get_ticks()           
        if now - self.last_update >= 3000:
            self.last_update = now
            self.attack()

    def attack(self):
        for i in range(8):
            thorn = Spell(self.game, i*45, self, WHITE, SPEED/1.5, 10, 10, 'mob')
            self.game.projectiles.add(thorn)
            self.game.all_sprites.add(thorn)

class Pickup(pg.sprite.Sprite):
    def __init__(self, game, center):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.type = str(random.choices(['health', 'mana'], weights=(50, 50), k=1))
        self.type = self.type.replace('[', '')
        self.type = self.type.replace(']', '')
        self.type = self.type.replace("'", '')
        if self.type == 'health':
            self.image = pg.Surface((25, 25))
            self.image.fill(WHITE)
        elif self.type == 'mana':
            self.image = pg.Surface((25, 25))
            self.image.fill(BLUE)
        
        #self.image = self.game.pickup_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
     