import math
import random
import time

import pygame
from pygame.locals import *
from pygame.math import Vector2 as Vector

from consts import *
from missile import Missile, Missiles
from plane import Plane, control_plane
from clouds import make_background
from explosion import Explosions


class Camera:
    def __init__(self):
        self.position = Vector(0, 0)

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def apply(self, position):

        return position - self.position + Vector(SCREEN_WIDTH, SCREEN_HEIGHT) / 2

    def update(self, plane):

        self.position = plane.position


def main():

    pygame.init()
    myfont = pygame.font.SysFont("Arial", 32)

    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    camera = Camera()

    plane = Plane(pygame.math.Vector2(0, 0))
    missiles = Missiles()
    missiles.spawn_missile(plane)
    explosions = Explosions()
    # background = make_background(camera.position)

    run = True
    while run:
        dt = clock.tick(FPS) / 1000

        control_plane(plane, missiles.get_visable(plane))

        background = make_background(camera.position)

        win.blit(background, (0, 0))

        if len(missiles.missiles) < 5:
            missiles.spawn_missile(plane)

        plane.update(dt)

        hits = missiles.update(dt, plane)
        for hit in hits:
            explosions.add(hit)

        explosions.update()
        camera.update(plane)

        win.blit(plane.get_image(), camera.apply(plane.position))
        explosions.draw(win, camera)

        missiles.draw(win, camera)

        label = myfont.render(
            f"{plane.hits},({round(plane.x)},{round(plane.y)}, {clock.get_fps()})",
            1,
            (128, 255, 128),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False

        win.blit(label, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)

        win.fill((255, 255, 255))


if __name__ == "__main__":
    main()
