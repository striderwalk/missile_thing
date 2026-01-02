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
    background = make_background(camera.position)

    run = True
    while run:

        control_plane(plane, missiles.get_visable(plane))
        prev_background = background
        background = make_background(camera.position)
        prev_background.set_alpha(50)
        background.blit(prev_background, (0, 0))
        win.blit(background, (0, 0))

        if len(missiles.missiles) < 3:
            missiles.spawn_missile(plane)

        plane.update(missiles.missiles[0])
        missiles.update(plane)

        camera.update(plane)

        win.blit(plane.get_image(), camera.apply(plane.position))

        missiles.draw(win, camera)

        label = myfont.render(
            f"{plane.hits},({round(plane.x)},{round(plane.y)})",
            1,
            (128, 255, 128),
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
