import pygame as pg
from os import path
from pygame.constants import *
from settings import *
from sprites import *

img_dir = path.join(path.dirname(__file__), 'img')
aud_dir = path.join(path.dirname(__file__), 'aud')

class Game:
    def __init__(self):
        # initialize pygame and create window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font = pg.font.Font('Pro EB.otf', 48)
        self.font2 = pg.font.Font('Pro EB.otf', 24)
        self.intro_background = pg.image.load(path.join(img_dir, 'back.png')).convert()
        self.intro_background = pg.transform.scale(self.intro_background, (WIDTH, HEIGHT))
        self.game_over = False
        self.win = False

    def new(self):
        #start new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.mobs = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        for i in range(2):
            self.spawn()
        self.spawn_ranged()
        self.temples = pg.sprite.Group()
        self.temple = Temple(self)
        self.temples.add(self.temple)
        self.entry = Door(self)
        self.doors = pg.sprite.Group()
        self.doors.add(self.entry)
        self.pickups = pg.sprite.Group()
        self.attack = pg.sprite.Group()
        self.kills = 0
        self.arena_kills = 0
        self.entry_is_open = False
        self.level = 0
        self.or_level = 0
        self.win = False
        self.area = 1
        self.check_area()

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
                self.playing = False
                self.game_over = True
        
        hit = pg.sprite.spritecollide(self.player, self.projectiles, False)
        if hit and not self.player.immortal:
            self.player.hit()
            self.player.health -= 1
            self.player.rect.x += 20
            self.player.rect.y += 20
            if self.player.health <= 0:
                self.player.kill()
                self.playing = False
                self.game_over = True

        attack_hit = pg.sprite.groupcollide(self.mobs, self.attack, True, False)
        for hit in attack_hit:
            hit.kill()
            self.kills+=1
            if self.area == 5:
                self.arena_kills += 1
            if random.random() >= 0.7:
                if hit.type != 'ranged':
                    self.pickup = Pickup(self, hit.rect.center)
                    self.all_sprites.add(self.pickup)
                    self.pickups.add(self.pickup)
        
        pickups = pg.sprite.spritecollide(self.player, self.pickups, True)
        for pickup in pickups:
            if pickup.type == 'health':
                if self.player.health < self.player.max_health:
                    self.player.health += 1
            if pickup.type == 'mana':
                self.player.mana += 10
                if self.player.mana >= self.player.max_mana:
                    self.player.mana = self.player.max_mana
        
        door = pg.sprite.spritecollide(self.player, self.doors, False)
        if self.entry_is_open:
            for door in door:
                self.level = 1
                self.area = 5
                for sprite in self.pickups:
                    sprite.kill()
                for sprite in self.projectiles:
                    sprite.kill()
                self.entry_is_open = False
                self.check_area()

        if self.area == 5:
            if len(self.mobs.sprites()) == 0:
                if self.arena_kills >= 15:
                    self.win = True
                    self.game_over = False
                    self.playing = False
                else:
                    self.level += 1

        if self.level != self.or_level:
            for i in range(self.level):
                self.spawn()
            for i in range(self.level-1):
                self.spawn_ranged() 
            self.or_level = self.level

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
        self.screen.blit(self.background, self.background_rect)
        if len(self.mobs.sprites()) == 0 and self.kills >= 1 and self.area != 5:
            self.entry_is_open = True
        if self.entry_is_open:
            self.temples.draw(self.screen)
            self.doors.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.draw_health(self.screen, 5, 5, self.player.health)
        self.draw_mana(self.screen, 5, 30, self.player.mana)
        # Update the display
        pg.display.update()

    def spawn(self):
        self.mob = Mob(self)
        self.mobs.add(self.mob)
        self.all_sprites.add(self.mob)
    
    def spawn_ranged(self):
        self.r_mob = Ranged_Mob(self)
        self.mobs.add(self.r_mob)
        self.all_sprites.add(self.r_mob)
        self.d_mob = Dash_Mob(self)
        self.mobs.add(self.d_mob)
        self.all_sprites.add(self.d_mob)
    
    def kill_all(self):
        for sprite in self.mobs:
            sprite.kill()
        for projectile in self.projectiles:
            projectile.kill()
        for pickup in self.pickups:
            pickup.kill()

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
            self.player.max_mana = 150
            self.player.max_health = 7
            self.player.health = 5
            self.player.mana = 125
            self.background = self.tile_imgs[1]
        self.background_rect = self.background.get_rect()

    def load(self):
        self.door_img = pg.image.load(path.join(img_dir, 'tile6.png')).convert()
        self.mana_img = pg.image.load(path.join(img_dir, 'mana.png')).convert()
        self.mana_img.set_colorkey(BLACK)
        self.door_img.set_colorkey(BLACK)
        self.door_img = pg.transform.scale2x(self.door_img)
        self.tile_imgs = []
        for i in range(1, 6):
            filename = 'tile{}.png'.format(i)
            img = pg.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img = pg.transform.scale(img, (WIDTH, HEIGHT))
            self.tile_imgs.append(img)
        self.heart_img = pg.image.load(path.join(img_dir, 'heart.png')).convert()
        self.empty_heart_img = pg.image.load(path.join(img_dir, 'empty_heart.png')).convert()
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

        self.u_move_anim = []
        self.d_move_anim = []
        self.r_move_anim = []
        self.l_move_anim = []

        for i in range(4):
            filename = 'r_move{}.png'.format(i)
            img = pg.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img = pg.transform.scale2x(img)
            self.r_move_anim.append(img)

            filename2 = 'l_move{}.png'.format(i)
            img2 = pg.image.load(path.join(img_dir, filename2)).convert()
            img2.set_colorkey(BLACK)
            img2 = pg.transform.scale2x(img2)
            self.l_move_anim.append(img2)

            filename3 = 'u_move{}.png'.format(i)
            img3 = pg.image.load(path.join(img_dir, filename3)).convert()
            img3.set_colorkey(BLACK)
            img3 = pg.transform.scale2x(img3)
            self.u_move_anim.append(img3)

            filename4 = 'd_move{}.png'.format(i)
            img4 = pg.image.load(path.join(img_dir, filename4)).convert()
            img4.set_colorkey(BLACK)
            img4 = pg.transform.scale2x(img4)
            self.d_move_anim.append(img4)
            
        self.u_attack_img = pg.image.load(path.join(img_dir, 'u_attack.png')).convert()
        self.d_attack_img = pg.image.load(path.join(img_dir, 'd_attack.png')).convert()
        self.r_attack_img = pg.image.load(path.join(img_dir, 'r_attack.png')).convert()
        self.l_attack_img = pg.image.load(path.join(img_dir, 'l_attack.png')).convert()

        self.u_attack_img = pg.transform.scale2x(self.u_attack_img)
        self.d_attack_img = pg.transform.scale2x(self.d_attack_img)
        self.r_attack_img = pg.transform.scale2x(self.r_attack_img)
        self.l_attack_img = pg.transform.scale2x(self.l_attack_img)

        self.u_attack_img.set_colorkey(BLACK)
        self.d_attack_img.set_colorkey(BLACK)
        self.r_attack_img.set_colorkey(BLACK)
        self.l_attack_img.set_colorkey(BLACK)

        self.sword_img = pg.image.load(path.join(img_dir, 'u_sword.png')).convert()

        self.spell_image = pg.image.load(path.join(img_dir, 'spell.png')).convert()
        self.spell_image = pg.transform.scale2x(self.spell_image)

        self.dash_mob_image = pg.image.load(path.join(img_dir, 'dash_mob.png')).convert()
        self.dash_mob_image = pg.transform.scale(self.dash_mob_image, (100, 70))
        
        pg.display.set_icon(self.d_move_anim[0])
    
    def draw_health(self, surf, x, y, health):
        for i in range(health):
            heart_img = self.heart_img
            heart_img.set_colorkey(BLACK)
            heart_rect = heart_img.get_rect()
            heart_rect.x = x+25*i
            heart_rect.y = y
            surf.blit(heart_img, heart_rect)

        for i in range(self.player.max_health):
            heart_img = self.empty_heart_img
            heart_img.set_colorkey(BLACK)
            heart_rect = heart_img.get_rect()
            heart_rect.x = x+25*i
            heart_rect.y = y
            surf.blit(heart_img, heart_rect)
        
    def draw_mana(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        if self.player.max_mana == 100:
            fill = (pct/self.player.max_mana) * BAR_LENGTH
            outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
            fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        elif self.player.max_mana == 150:
            fill = (pct/self.player.max_mana) * 1.5*BAR_LENGTH
            outline_rect = pg.Rect(x, y, BAR_LENGTH*1.5, BAR_HEIGHT)
            fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, BLUE, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)        

    def intro_screen(self):
        intro = True
        
        if not self.game_over and not self.win:
            self.load()
            pg.mixer.music.load(path.join(aud_dir, 'THE_DESERT_-_MUSIC_OF_DESERT_Download_Royalty_Free_Vlog_Music_Free_Copyright-safe_Music.ogg'))
            pg.mixer.music.set_volume(0.2)
            pg.mixer.music.play(loops=-1)
            title = self.font.render('Temple Raiders', True, BLACK)
            title_rect = title.get_rect(x=(WIDTH/2) - 125, y=(HEIGHT/2) - 125)
            play_button = Button((WIDTH/2) - 50, (HEIGHT/2) - 75, 50, 100,
                                    WHITE, BLACK, 'Play', 32)
            instructions = self.font2.render('Arrow keys or WASD to Move', True, BLACK)
            instructions2 = self.font2.render('C to use Spell, Spacebar to use Sword', True, BLACK)
            instructions_rect = instructions.get_rect()
            instructions2_rect = instructions2.get_rect()
            instructions_rect.centerx = WIDTH/2
            instructions_rect.centery = HEIGHT/2 - 200
            instructions2_rect.centerx = WIDTH/2
            instructions2_rect.centery = HEIGHT/2 - 250
            title_rect = title.get_rect(x=(WIDTH/2) - 125, y=(HEIGHT/2) - 125)


        elif self.game_over: 
            title = self.font.render('Game Over', True, BLACK)
            title_rect = title.get_rect(x=(WIDTH/2) - 125, y=(HEIGHT/2) - 125)
            play_button = Button((WIDTH/2) - 50, (HEIGHT/2) - 75, 50, 200,
                                    WHITE, BLACK, 'Try Again', 32)
            print(self.area)

        elif self.win:
            title = self.font.render('You Win', True, BLACK)
            title_rect = title.get_rect(x=(WIDTH/2) - 125, y=(HEIGHT/2) - 125)
            play_button = Button((WIDTH/2) - 50, (HEIGHT/2) - 75, 50, 200,
                                    WHITE, BLACK, 'Play Again', 32)

        title_rect.centerx = WIDTH/2
        play_button.rect.centerx = WIDTH/2
        
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    intro = False
                    self.running = False
                    self.playing == False

            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            if not self.game_over and not self.win:
                self.screen.blit(instructions, instructions_rect)
                self.screen.blit(instructions2, instructions2_rect)
            self.clock.tick(FPS)
            pg.display.update()

g = Game()
g.intro_screen()
while g.running:
    g.new()
    g.intro_screen()

pg.quit()