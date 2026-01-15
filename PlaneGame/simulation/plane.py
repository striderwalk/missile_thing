import random
from pygame.math import Vector2
import pygame
import math
from .sim_consts import *
from . import Flyer


def vec_polar(r, phi):
    # Pygames inbuild wont work
    return Vector2(math.cos(phi), math.sin(phi)) * r


class Plane(Flyer):
    max_speed = PLANE_SPEED
    turning_speed = PLANE_TURNING_SPEED

    def __init__(self, position=Vector2(0, 0)):
        super().__init__(position)
        self.health = 3
        self.hits = 0
        self.heading = -math.pi / 2
        self.target_heading = -math.pi / 2

        self.rect = pygame.Rect(0, 0, 40, 40)

    def get_image(self, debug):
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        surface.fill((0, 0, 0, 0))
        pygame.draw.circle(surface, (255, 0, 0), (20, 20), 5)
        vel = self.velocity.normalize() * 15
        pygame.draw.circle(surface, (0, 255, 120), (20 + vel.x, vel.y + 20), 3)

        if debug:
            pygame.draw.circle(surface, (255, 0, 0), (20, 20), HIT_RADIUS / 2, width=3)

        return surface

    def draw(self, win, camera, debug=False):
        win.blit(self.get_image(debug), camera.apply(self.position, self.rect))

        if debug:
            self.draw_debug(win, camera)

    def draw_debug(self, win, camera):

        position = camera.apply(self.position)

        rect = (
            position.x - PLANE_VISABLE_RANGE / 2,
            position.y - PLANE_VISABLE_RANGE / 2,
            PLANE_VISABLE_RANGE,
            PLANE_VISABLE_RANGE,
        )

        pygame.draw.arc(
            win,
            (0, 255, 120),
            rect,
            -self.heading + math.pi / 6,
            -self.heading - math.pi / 6,
            3,
        )

        rect = (
            position.x - PLANE_VISABLE_RANGE,
            position.y - PLANE_VISABLE_RANGE,
            PLANE_VISABLE_RANGE * 2,
            PLANE_VISABLE_RANGE * 2,
        )
        pygame.draw.arc(
            win,
            (0, 255, 120),
            rect,
            -self.heading - math.pi / 6,
            -self.heading + math.pi / 6,
            3,
        )

        l1_start = position + vec_polar(
            PLANE_VISABLE_RANGE / 2, self.heading - math.pi / 6
        )

        l1_end = position + vec_polar(PLANE_VISABLE_RANGE, self.heading - math.pi / 6)
        l2_start = position + vec_polar(
            PLANE_VISABLE_RANGE / 2, self.heading + math.pi / 6
        )
        l2_end = position + vec_polar(PLANE_VISABLE_RANGE, self.heading + math.pi / 6)

        pygame.draw.line(win, (0, 255, 120), l1_start, l1_end, 3)
        pygame.draw.line(win, (0, 255, 120), l2_start, l2_end, 3)

    def update(self, dt):
        self.update_movement(dt)

    def hit(self):
        self.health -= 1
        self.hits += 1
