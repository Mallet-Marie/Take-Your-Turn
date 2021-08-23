import pygame as pg
from os import path
from pygame.constants import *
from settings import *
from sprites import *

img_dir = path.join(path.dirname(__file__), 'img')

class Game:
    def __init__(self):
        # initialize pygame and create window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        #start new game
        self.load()
        self.check_area()
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.mobs = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.enemies = []
        for i in range(2):
            self.spawn()
        for i in range(2):
            self.spawn_ranged()
        self.pickups = pg.sprite.Group()
        self.attack = pg.sprite.Group()
        self.run()

    def run(self):
        #Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.event()
            self.update()      
            self.draw()

    def update(self):
        #Game loop update
        self.all_sprites.update()
        hit = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hit and not self.player.immortal:
            self.player.hit()
            self.player.health -= 1
            self.player.rect.x += 20
            self.player.rect.y += 20
            if self.player.health <= 0:
                self.player.kill()
                self.running = False
                self.playing = False
        
        hit = pg.sprite.spritecollide(self.player, self.projectiles, False)
        if hit and not self.player.immortal:
            self.player.hit()
            self.player.health -= 1
            self.player.rect.x += 20
            self.player.rect.y += 20
            if self.player.health <= 0:
                self.player.kill()
                self.running = False
                self.playing = False

        attack_hit = pg.sprite.groupcollide(self.mobs, self.attack, True, False)
        for hit in attack_hit:
            hit.kill()
            if random.random() >= 0:
                if hit.type != 'ranged':
                    self.pickup = Pickup(self, hit.rect.center)
                    self.all_sprites.add(self.pickup)
                    self.pickups.add(self.pickup)
        
        pickups = pg.sprite.spritecollide(self.player, self.pickups, True)
        for pickup in pickups:
            if pickup.type == 'health':
                if self.player.health < 5:
                    self.player.health += 1
            if pickup.type == 'mana':
                self.player.mana += 10
                if self.player.mana >= 100:
                    self.player.mana = 100

    def event(self):
        #Game loop events
        for event in pg.event.get():
        # check for closing window
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.player.attack()
                if event.key == K_c:
                    if self.player.mana >= 25:
                        self.player.shoot()

    def draw(self):
        #Game loop draw
        self.screen.fill(BLACK)
        self.rel_x = self.x % self.background_rect.width
        self.screen.blit(self.background, self.background_rect)
        if self.rel_x < WIDTH:
            self.screen.blit(self.background, (self.rel_x, 0))
        self.all_sprites.draw(self.screen)
        self.draw_health(self.screen, 5, 5, self.player.health)
        self.draw_mana(self.screen, 5, 30, self.player.mana)
        # Update the display
        pg.display.update()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
    
    def spawn(self):
        self.mob = Mob(self)
        self.enemies.append(self.mob)
        self.mobs.add(self.mob)
        self.all_sprites.add(self.mob)
    
    def spawn_ranged(self):
        self.r_mob = Ranged_Mob(self)
        self.enemies.append(self.r_mob)
        self.mobs.add(self.r_mob)
        self.all_sprites.add(self.r_mob)
    
    def kill_all(self):
        for sprite in self.mobs:
            sprite.kill()

    def check_area(self):
        if self.area == 1:
            self.background = self.tile_imgs[0]
        elif self.area == 2:
            self.background = self.tile_imgs[4]
        elif self.area == 3:
            self.background = self.tile_imgs[2]
        elif self.area == 4:
            self.background = self.tile_imgs[3]
        elif self.area == 5:
            self.background = self.tile_imgs[1]
        self.background_rect = self.background.get_rect()

    def load(self):
        self.tile_imgs = []
        for i in range(1, 6):
            filename = 'tile{}.png'.format(i)
            img = pg.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img = pg.transform.scale(img, (WIDTH, HEIGHT))
            self.tile_imgs.append(img)
        self.heart_img = pg.image.load(path.join(img_dir, 'heart.png')).convert()
        self.poison_img = pg.image.load(path.join(img_dir, 'poison.png')).convert()
        self.snake_imgs = []
        self.snake_imgs_list = ['snake.png', 'snake1.png', 'snake2.png', 'snake3.png']
        for img in self.snake_imgs_list:
            img = pg.image.load(path.join(img_dir, img)).convert()
            img.set_colorkey(BLACK)
            self.snake_imgs.append(img)
        self.mummy_imgs = []
        self.mummy_imgs_list = ['mummy.png', 'mummy1.png']
        for img in self.mummy_imgs_list:
            img = pg.image.load(path.join(img_dir, img)).convert()
            img.set_colorkey(BLACK)
            img = pg.transform.scale2x(img)
            self.mummy_imgs.append(img)
        self.player_imgs = []
        self.player_imgs_list = ['player2.png', 'player3.png', 'player4.png', 'player5.png']
        for img in self.player_imgs_list:
            img = pg.image.load(path.join(img_dir, img)).convert()
            img = pg.transform.scale(img,(64,64))
            img.set_colorkey(BLACK)
            self.player_imgs.append(img)
        self.x = 0
        self.area = 1
    
    def draw_health(self, surf, x, y, health):
        for i in range(health):
            heart_img = self.heart_img
            heart_img.set_colorkey(BLACK)
            heart_rect = heart_img.get_rect()
            heart_rect.x = x+25*i
            heart_rect.y = y
            surf.blit(heart_img, heart_rect)
        
    def draw_mana(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        fill = (pct/100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, BLUE, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)        

g = Game()
#g.show_start_screen()
while g.running:
    g.new()
    #g.show_go_screen()

pg.quit()