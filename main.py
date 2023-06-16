import pygame as pg
import os
from sys import exit

# TODO: make rectthing class, make collision with ball and players
# TODO: make score, make loosing screen, make proper game loop
# TODO: make platforms draw with for loop

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "player.png")).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, 550))
        
        self.dx = 10
        self.dy = 10

    def movement(self):
        key = pg.key.get_pressed()
        if key[pg.K_a] or key[pg.K_LEFT]:
            self.rect.x -= self.dx
        if key[pg.K_d] or key[pg.K_RIGHT]:
            self.rect.x += self.dx

    def border(self):
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0

    def update(self):
        self.movement()
        self.border()


class Ball(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "ball.png")).convert_alpha()
        self.rect = self.image.get_rect(midbottom=(WIDTH//2, 450))

        self.dx = 5
        self.dy = 5

    def movement(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.dx *= -1
        
        if self.rect.top <= 0:
            self.dy *= -1

    #! Temporary code for development
    def restart(self):
        if self.rect.bottom >= HEIGHT:
            self.rect.midbottom = (WIDTH//2, 450)   

    def collision_with_player(self, player):
        if self.rect.colliderect(player.rect):
            self.dy *= -1

    def update(self, player):
        self.restart()
        self.collision_with_player(player)
        self.movement()


class GreenPlatform(pg.sprite.Sprite):
    def __init__(self):
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "platform_01.png")).convert_alpha()
        self.rect = self.green.get_rect(midbottom = (10, 30))
        self.max_platform = 10

    def draw_platforms(self):
        pass


WIDTH = 650
HEIGHT = 600
GREY = (188, 194, 190)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Breakout')

start_screen_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "start_screen.png")).convert_alpha()
start_screen_surf_bigger = pg.transform.scale(start_screen_surf, (WIDTH, HEIGHT))

FPS = 60

clock = pg.time.Clock()

player_group = pg.sprite.GroupSingle(Player())
ball_group = pg.sprite.GroupSingle(Ball())

start_screen = True
gameplay = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                start_screen = False
                gameplay = True

    if start_screen:
        screen.blit(start_screen_surf_bigger, (0, 0))

    if gameplay:
        screen.fill(GREY)
        player_group.update()
        player_group.draw(screen)
        ball_group.update(player_group.sprite)
        ball_group.draw(screen)

    pg.display.update()
    clock.tick(FPS)