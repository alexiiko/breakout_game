import pygame as pg
import os
from sys import exit
pg.init()
pg.font.init()

WIDTH = 650
HEIGHT = 600
GREY = (188, 194, 190)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Breakout')

icon_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "ball.png")).convert_alpha()
pg.display.set_icon(icon_surf)

start_screen_surf = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "start_screen.png")).convert()
start_screen_surf_bigger = pg.transform.scale(start_screen_surf, (WIDTH, HEIGHT))

FPS = 60

clock = pg.time.Clock()

start_screen = True
gameplay = False
game_won = False

score = 0
score_font = pg.font.SysFont("Arial", 25)
score_surf = score_font.render(f"Score:{score}", False, (0,0,0))

text_font = pg.font.SysFont("Arial", 50)
text_surf = text_font.render("Escape to quit", False, (0,0,0))

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "player.png"))
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

player = pg.sprite.GroupSingle()
player.add(Player())


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

    def restart(self):
        global score, score_surf
        if self.rect.bottom >= HEIGHT:
            self.rect.midbottom = (WIDTH//2, 450)
            score -= 100
            if score < 0:
                score = 0
            score_surf = score_font.render(f"Score:{score}", False, (0,0,0))

    def collision_with_player(self, player):
        if self.rect.colliderect(player.rect):
            self.dy *= -1

    def collision_with_platform(self):
        global score, score_surf
        if pg.sprite.spritecollide(ball.sprite, platform_group, True):
            self.dy *= -1
            score += 100
            score_surf = score_font.render(f"Score:{score}", False, (0,0,0))

    def update(self, player):
        self.collision_with_platform()
        self.restart()
        self.collision_with_player(player)
        self.movement()

ball = pg.sprite.GroupSingle()
ball.add(Ball())


class GreenPlatform(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "platform_01.png")).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (10, 30))
        self.rect.x = x_pos
        self.rect.y = y_pos

class BluePlatform(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "platform_03.png")).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (10, 30))
        self.rect.x = x_pos
        self.rect.y = y_pos

class RedPlatform(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "platform_02.png")).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (10, 30))
        self.rect.x = x_pos
        self.rect.y = y_pos

platform_group = pg.sprite.Group()

# row 1 - 3
px_green = 10
for _ in range(5):
    platform = GreenPlatform(px_green, 30)
    platform_group.add(platform)
    px_green += 125

px_blue = 10
for _ in range(5):
    platform = BluePlatform(px_blue, 75)
    platform_group.add(platform)
    px_blue += 125

px_red = 10
for _ in range(5):
    platform = RedPlatform(px_red, 120)
    platform_group.add(platform)
    px_red += 125

# row 3 - 5
px_green = 10
for _ in range(5):
    platform = GreenPlatform(px_green, 170)
    platform_group.add(platform)
    px_green += 125

px_blue = 10
for _ in range(5):
    platform = BluePlatform(px_blue, 220)
    platform_group.add(platform)
    px_blue += 125

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
        player.update()
        player.draw(screen)
        ball.update(player.sprite)
        ball.draw(screen)
        platform_group.draw(screen)
        screen.blit(score_surf, (0, 0))

    if not bool(platform_group):
        gameplay = False
        game_won = True

    if game_won:
        key = pg.key.get_pressed()
        screen.fill(GREY)
        text_surf_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        score_surf_rect = score_surf.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(score_surf, score_surf_rect)
        screen.blit(text_surf, text_surf_rect)
        if key[pg.K_ESCAPE]:
            pg.quit()
            exit()

    pg.display.update()
    clock.tick(FPS)