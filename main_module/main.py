import pygame as pg
import math
from pygame.locals import *
from constants import *


class Player:
    def __init__(self, surf_size, image_path=PLAYER_PATH):
        self.image = pg.image.load(image_path).convert_alpha()
        self.rotated_image = None
        self.rect = None
        self._center = tuple((x // 2 for x in surf_size))
        self.angle = 0
        self.bullets = pg.sprite.Group()

    def calc_angle(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        center_x, center_y = self._center

        # calc the rotation angle
        x_dist = mouse_x - center_x
        y_dist = -(mouse_y - center_y)

        return math.degrees(math.atan2(y_dist, x_dist))

    def update(self):
        self.angle = self.calc_angle()
        self.rotated_image = pg.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_image.get_rect(center=self._center)

    def draw(self, win):
        self.update()
        win.blit(self.rotated_image, self.rect)


class Crosshair:
    def __init__(self, image_path=None):
        super().__init__()
        # if we create crosshair, hide the mouse arrow
        pg.mouse.set_visible(False)

        if not image_path:
            # set the default crosshair
            image_path = CROSSHAIR_PATH

        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        self.rect.center = pg.mouse.get_pos()

    def draw(self, win):
        self.update()
        win.blit(self.image, self.rect)


def main_loop():
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # hero
    hero = Player(screen.get_size())

    # crosshair
    crosshair = Crosshair()

    # image icon source
    # https://ru.freepik.com/icon/%D0%BF%D1%83%D0%BB%D0%B5%D0%BC%D0%B5%D1%82_2125#fromView=search&term=pixel+gun+turret&page=1&position=52
    background = pg.image.load('../tile_floor.png').convert_alpha()
    background = pg.transform.scale(background, (800, 600))

    clock = pg.time.Clock()

    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

        keys = pg.key.get_pressed()
        if keys[K_ESCAPE]:
            running = False

        # screen.fill('purple')
        screen.blit(background, (0, 0))

        # update the main surface
        hero.draw(screen)
        crosshair.draw(screen)

        pg.display.update()
        clock.tick(FPS)

    pg.quit()


if __name__ == '__main__':
    main_loop()
