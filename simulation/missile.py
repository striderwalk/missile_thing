from collections.abc import Callable
import math
import random
import uuid

import pygame
from pygame.math import Vector2 as Vector

from ..colours import *
from . import Flyer
from .sim_consts import *


def random_vector() -> Vector:
    t = random.uniform(0, 2 * math.pi)
    return Vector(math.cos(t), math.sin(t))


def distance(this: Vector, that: Vector) -> float:

    return math.hypot(this.x - that.x, this.y - that.y)


class Missile(Flyer):

    max_speed = MISSILE_SPEED
    turning_speed = MISSILE_TURNING_RADIUS

    def __init__(self, position: Vector, velocity: Vector):
        super().__init__(position, velocity)

        self.has_seen_plane = False
        self.active = True
        self.been_hit = False
        self.lifetime = random.randint(500, 1500)

        self.rect = pygame.Rect(self.x, self.y, 40, 40)

        self.id = uuid.uuid1()

    def get_image(self, debug: bool) -> pygame.Surface:
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        surface.fill(CLEAR)
        vel = self.velocity.normalize() * 15

        pygame.draw.line(
            surface,
            MISSILE_GREY,
            (20 - vel.x / 2, 20 - vel.y / 2),
            (20 + vel.x / 2, vel.y / 2 + 20),
            5,
        )

        pygame.draw.circle(surface, DEBUG_GREEN, (20 + vel.x, 20 + vel.y), 2)

        if debug:
            pygame.draw.circle(surface, (255, 0, 0), (20, 20), HIT_RADIUS / 2, width=3)

        return surface

    def hit(self):
        self.been_hit = True
        self.active = False

    def update(self, dt: float, plane):

        self.lifetime -= 1
        if self.lifetime < 0:
            self.active = False
            return

        if distance(self.position, plane.position) > SPAWN_RADIUS * 1.5:
            self.active = False
            return

        if not self.active:
            return

        self.has_seen_plane |= distance(self.position, plane.position) < 35

        self.update_movement(dt)


class Missiles:

    def __init__(self):
        self.missiles = []

    def __iter__(self):
        yield from self.missiles

    def add(self, missile: Missile):
        self.missiles.append(missile)

    def remove(self, missile: Missile):
        self.missiles.remove(missile)

    def draw(self, win: pygame.Surface, camera, debug: bool = False):
        for missile in self.missiles:
            win.blit(
                missile.get_image(debug), camera.apply(missile.position, missile.rect)
            )

    def update(self, dt: float, plane, controller: Callable):

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

    def get_visable(self, plane) -> list[Missile]:
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
