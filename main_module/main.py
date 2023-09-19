import pygame as pg
import math
from pygame.locals import *

WIDTH = 800
HEIGHT = 600
FPS = 60


def main_loop():
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    center_x, center_y = screen.get_size()
    center_x, center_y = center_x // 2, center_y // 2

    # Clear the screen
    screen.fill('purple')

    turret_original = pg.image.load('../machine-gun_icon.png').convert_alpha()
    t_width, t_height = turret_original.get_size()
    turret_original = pg.transform.scale(turret_original,
                                         (t_width // 3, t_height // 3))

    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False

        pos = pg.mouse.get_pos()

        # calc the rotation angle
        x_dist = pos[0] - center_x
        y_dist = -(pos[1] - center_y)
        angle = math.degrees(math.atan2(y_dist, x_dist))

        turret = pg.transform.rotate(turret_original, angle - 10)
        turret_rect = turret.get_rect(center=(center_x, center_y))

        # Clear the screen
        screen.fill('purple')
        # update the main surface
        screen.blit(turret, turret_rect)

        pg.display.update()
        clock.tick(FPS)

    pg.quit()


if __name__ == '__main__':
    main_loop()
