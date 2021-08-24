import pygame as pg
from pygame import mouse
from pygame.constants import *
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize pygame and create window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font = pg.font.Font('Pro EB.otf', 32)
        self.intro_background = pg.image.load('tile3.png')

    def new(self):
        # start new game

        self.all_sprites = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.mobs = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        for i in range(3):
            self.mob = Mob(self)
            self.mob.game = self
            self.mobs.add(self.mob)
            self.all_sprites.add(self.mob)
        for i in range(2):
            self.r_mob = Ranged_Mob(self)
            self.enemies.add(self.r_mob)
            self.mobs.add(self.r_mob)
            self.all_sprites.add(self.r_mob)

        self.attack = pg.sprite.Group()
        self.run()

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()

    def update(self):
        # Game loop update
        self.all_sprites.update()
        hit = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hit and not self.player.immortal:
            self.player.hit()
            self.player.health -= 1
            if self.player.health <= 0:
                self.player.kill()
                self.running = False
                self.playing = False

        attack_hit = pg.sprite.groupcollide(
            self.mobs, self.attack, True, False)
        for hit in attack_hit:
            hit.kill()

    def event(self):
        # Game loop events
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
        # Game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_health(self.screen, 5, 5, self.player.health)
        self.draw_mana(self.screen, 5, 30, self.player.mana)
        # Update the display
        pg.display.update()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    def draw_health(self, surf, x, y, health):
        for i in range(health):
            heart_img = pg.Surface((15, 15))
            heart_img.fill(GREEN)
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

    def intro_screen(self):
        intro = True

        title = self.font.render('Temple Raiders', True, BLACK)
        title_rect = title.get_rect(x=(WIDTH/2) - 125, y=(HEIGHT/2) - 125)
        play_button = Button((WIDTH/2) - 50, (HEIGHT/2) - 75, 50, 100,
                             WHITE, BLACK, 'Play', 32)
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pg.mouse.get_pos()
            mouse_pressed = pg.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pg.display.update()


g = Game()
g.intro_screen()

# g.show_start_screen()
while g.running:
    g.new()
    # g.show_go_screen()

pg.quit()
