import pygame as pg
import os 

class Player(pg.sprite.Sprite):
    def __init__(self):
        self.image = pg.image.load(os.path.join("OneDrive", "Desktop", "breakout_game", "graphics", "player.png")).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.dx = 10
        self.dy = 10

    def movement(self):
        key = pg.key.get_pressed()
        if key[pg.K_a] or key[pg.K_LEFT]:
            self.rect.x -= self.dx
        if key[pg.K_d] or key[pg.K_RIGHT]:
            self.rect.x += self.dx

    def update(self):
        self.movement()