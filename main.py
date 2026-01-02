import math
import random
import time

import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vector

from consts import *
from missile import Missile, Missiles
from plane import Plane, control_plane
from clouds import make_backgroud


class Camera:
    def __init__(self):
        self.x = 0
        self.target_x = 0
        self.y = 0
        self.target_y = 0

        self.dead_x = 150
        self.dead_y = 150

    @property
    def position(self):
        return Vector(self.x, self.y)

    def apply(self, position):

        return (
            position.x - self.x + SCREEN_WIDTH / 2,
            position.y - self.y + SCREEN_HEIGHT / 2,
        )

    def update(self, plane):
        # Horizontal scrolling
        screen_x, screen_y = self.apply(plane.position)

        if screen_x < SCREEN_WIDTH / 2 - self.dead_x:
            self.target_x = self.x - self.dead_x / 2
        elif screen_x > SCREEN_WIDTH / 2 + self.dead_x:
            self.target_x = self.x + self.dead_x / 2

        # Vertical scrolling
        if screen_y < SCREEN_HEIGHT / 2 - self.dead_y:
            self.target_y = self.y - self.dead_y / 2
        elif screen_y > SCREEN_HEIGHT / 2 + self.dead_y:
            self.target_y = self.y + self.dead_y / 2

        if abs(self.x - self.target_x) > 5:
            delta = self.x - self.target_x

            self.x -= math.ceil(abs(delta / 100)) * delta / abs(delta)
        if abs(self.y - self.target_y) > 5:
            delta = self.y - self.target_y

            self.y -= math.ceil(abs(delta / 100)) * delta / abs(delta)


def main():

    pygame.init()
    myfont = pygame.font.SysFont("Arial", 64)

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    camera = Camera()

    plane = Plane(pygame.math.Vector2(0, 0))
    missiles = Missiles()
    missiles.spawn_missile(plane)

    run = True
    while run:

        camera.update(plane)

        control_plane(plane, missiles.get_visable(plane))

        win.blit(make_backgroud(camera.position), (0, 0))

        if len(missiles.missiles) < 1:
            missiles.spawn_missile(plane)

        plane.update(missiles.missiles[0])
        missiles.update(plane)

        # plane.draw(win)
        win.blit(plane.get_image(), camera.apply(plane.position))

        missiles.draw(win, camera)

        label = myfont.render(
            f"{plane.hits},({round(camera.x)},{round(camera.y)})", 1, (128, 255, 128)
        )
        win.blit(label, (10, 10))
        pygame.display.flip()
        clock.tick(120)
        win.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False


if __name__ == "__main__":
    main()
