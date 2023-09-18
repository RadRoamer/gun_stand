import pygame as pg
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
FPS = 60


def main_loop():
    running = True

    screen = pg.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

        screen.fill('white')
        pg.display.update()
        clock.tick(FPS)
    pg.quit()


if __name__ == '__main__':
    main_loop()