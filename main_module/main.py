import pygame as pg
import math
from pygame.locals import *
from constants import *

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()


class Crosshair:
    def __init__(self, image_path=CROSSHAIR_PATH):
        super().__init__()
        # if we create crosshair, hide the mouse arrow
        pg.mouse.set_visible(False)

        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.update()

    def update(self):
        self.rect.center = pg.mouse.get_pos()

    def draw(self, win):
        self.update()
        win.blit(self.image, self.rect)


class Player:
    def __init__(self, surf_size, fire_rate=20,
                 image_path=PLAYER_PATH, sound_path=S_GUNSHOT_PATH):
        self.image = pg.image.load(image_path).convert_alpha()
        self.rotated_image = None
        self.rect = None
        self.fire_rate = fire_rate
        self.gun_sound = sound_path
        self._center = tuple((x // 2 for x in surf_size))
        self.angle = 0
        self.bullets = pg.sprite.Group()

    def shoot(self):
        if len(self.bullets) < self.fire_rate:
            self.bullets.add(Bullet(self.angle, self.rect.center))
            pg.mixer.Sound(self.gun_sound).play(maxtime=500)

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
        for bullet in self.bullets:
            if bullet.rect.x not in range(0, win.get_width()):
                self.bullets.remove(bullet)
            elif bullet.rect.y not in range(0, win.get_height()):
                self.bullets.remove(bullet)

        self.bullets.update()
        self.bullets.draw(win)
        win.blit(self.rotated_image, self.rect)


class Bullet(pg.sprite.Sprite):
    def __init__(self, angle, gun_pos, image_path=BULLET_PATH, speed=20):
        super().__init__()
        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.scale(self.image, (20, 20))
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=gun_pos)
        self.angle = angle
        self.speed = speed

    def update(self, *args):
        radians = -math.radians(self.angle)
        x, y = self.rect.center
        x = x + self.speed * math.cos(radians)
        y = y + self.speed * math.sin(radians)
        self.rect = self.image.get_rect(center=(x, y))


def main_loop():
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # hero
    hero = Player(screen.get_size())

    # crosshair
    crosshair = Crosshair()

    # background
    background = pg.image.load('../tile_floor.png').convert_alpha()
    background = pg.transform.scale(background, (800, 600))

    clock = pg.time.Clock()

    # delay between shots in milliseconds
    shoot_delay = 100  # 0.1 секунда

    # var to track the last shooting time
    last_shoot_time = 0

    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False

        current_time = pg.time.get_ticks()

        left_mouse, *other_buttons = pg.mouse.get_pressed()
        if left_mouse:
            if current_time - last_shoot_time >= shoot_delay:
                hero.shoot()
                last_shoot_time = current_time

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
