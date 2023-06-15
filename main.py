import pygame as pg
from sys import exit

WIDTH = 650
HEIGHT = 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Title')
#pg.display.set_icon()

FPS = 60

clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()


    pg.display.update()
    clock.tick(FPS)