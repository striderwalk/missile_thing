import math
import random

import pygame
from pygame.math import Vector2 as Vector

from .sim_consts import *

from . import Flyer


def random_vector():
    t = random.uniform(0, 2 * math.pi)
    return Vector(math.cos(t), math.sin(t))


def distance(this, that):
    a = this.position
    b = that.position
    return math.hypot(a.x - b.x, a.y - b.y)


FPS = 120


class Missile(Flyer):

    max_speed = MISSILE_SPEED
    turning_speed = MISSILE_TURNING_RADIUS

    def __init__(self, position, velocity):
        super().__init__(position, velocity)

        self.has_seen_plane = False
        self.active = True
        self.been_hit = False
        self.lifetime = random.randint(500, 1500)

        self.rect = pygame.Rect(self.x, self.y, 20, 20)

        self.los_angle = 0

    def get_image(self):
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        surface.fill((255, 0, 0, 0))
        vel = self.velocity.normalize() * 15

        pygame.draw.line(
            surface,
            (111, 111, 111),
            (20 - vel.x / 2, 20 - vel.y / 2),
            (20 + vel.x / 2, vel.y / 2 + 20),
            5,
        )
        if self.active:
            pygame.draw.circle(
                surface,
                (
                    255,
                    128,
                    255,
                    255 if self.lifetime > FPS * 5 else 255 * self.lifetime / (FPS * 5),
                ),
                (20 + vel.x, 20 + vel.y),
                2,
            )

        return surface

    def hit(self):
        self.been_hit = True
        self.active = False

    def update(self, dt, plane):

        self.lifetime -= 1
        if self.lifetime < 0:
            self.active = False
            return

        if distance(self, plane) > SPAWN_RADIUS * 1.5:
            self.active = False
            return

        if not self.active:
            return

        self.has_seen_plane |= distance(self, plane) < 35

        self.update_movement(dt)


class Missiles:

    def __init__(self):
        self.missiles = []

    def __iter__(self):
        yield from self.missiles

    def add(self, missile):
        self.missiles.append(missile)

    def remove(self, missile):
        self.missiles.remove(missile)

    def draw(self, win, camera):
        for missile in self.missiles:
            win.blit(missile.get_image(), camera.apply(missile.position))

    def update(self, dt, plane, controller):
        if len(self.missiles) < MISSILE_NUMBER:
            self.spawn_missile(plane)
        removals = []
        for missile in self.missiles:
            if missile.active and not missile.been_hit:
                controller(missile, plane, dt)
                missile.update(dt, plane)
            else:
                removals.append(missile)

        for missile in removals:
            self.remove(missile)

    def spawn_missile(self, plane):

        position = random_vector() * SPAWN_RADIUS + plane.position
        missileToPlane = position - plane.position
        # turn a lil bit
        self.add(Missile(position, missileToPlane))

    def get_visable(self, plane):
        visable = []
        for missile in self.missiles:
            dis = distance(missile, plane)
            if dis < PLANE_VISABLE_RANGE:
                visable.append(missile)
            elif dis <= PLANE_VISABLE_RANGE * 1.5:
                p2m = missile.position - plane.position
                if abs(plane.velocity.angle_to(p2m)) < math.pi / 6:
                    visable.append(missile)

        return visable
