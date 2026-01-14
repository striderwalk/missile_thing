from pygame.math import Vector2 as Vector
import pygame
import math
from consts import *


class Plane:
    def __init__(self, position=Vector(0, 0)):
        self.position = position
        self.velocity = Vector(0, 1)
        self.heading = 0
        self.target_heading = 0
        self.health = 100
        self.hits = 0

    def get_image(self):
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        surface.fill((0, 0, 0, 0))
        pygame.draw.circle(surface, (255, 0, 0), (20, 20), 5)
        vel = self.velocity * 15 / FPS / 10
        pygame.draw.circle(surface, (0, 255, 120), (20 + vel.x, vel.y + 20), 3)

        return surface

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def limit_speed(self):
        self.velocity = self.velocity.normalize() * PLANE_SPEED

    def update(self, dt):

        self.update_heading()
        self.limit_speed()
        self.position += self.velocity * dt

    def update_heading(self):
        dheading = self.target_heading - self.heading

        if abs(dheading) < PLANE_TURNING_RADIUS:
            self.heading += dheading
        else:
            self.heading += PLANE_TURNING_RADIUS * dheading / abs(dheading)

        x, y = (0, 1)
        new_x = math.sin(self.heading * (math.pi * 2 / 360))
        new_y = math.cos(self.heading * (math.pi * 2 / 360))
        self.velocity = Vector(new_x, new_y)

    def hit(self):
        self.health -= 1
        self.hits += 1

    def set_heading(self, angle):

        self.target_heading = angle


def distance(this, that):
    a = this.position
    b = that.position
    return math.hypot(a.x - b.x, a.y - b.y)


def control_plane(plane, missiles):

    if not missiles:
        return
    nearest = min(missiles, key=lambda x: distance(x, plane))

    if distance(nearest, plane) < 55:
        plane.set_heading(plane.heading + 90)
