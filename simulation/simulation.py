from collections.abc import Callable
from dataclasses import dataclass
from uuid import UUID

import pygame
from pygame.locals import *
from pygame.math import Vector2

from . import Explosions, Missiles, Missile, Plane, detect_colisions


@dataclass
class missile_api:
    position: Vector2
    id: UUID


@dataclass
class plane_api:
    position: Vector2
    health: int
    heading: float
    target_heading: float
    been_hit: bool


class Simulation:

    def __init__(
        self,
        plane_controller: Callable[[plane_api, list[missile_api]], float],
        missile_controller: Callable[[Missile, Plane], None],
    ):
        self.plane = Plane(Vector2(0, 0))
        self.plane_controller = plane_controller
        self.missile_controller = missile_controller
        self.missiles = Missiles()
        self.explosions = Explosions()

    @property
    def active(self) -> bool:
        return self.plane.health > 0

    def update(self, dt: float):
        alive = self.plane.update(dt)

        self.missiles.update(dt, self.plane, self.missile_controller)
        self.explosions.update()

        new_target = self.plane_controller(
            plane_api(
                self.plane.position,
                self.plane.health,
                self.plane.heading,
                self.plane.target_heading,
                self.plane.been_hit,
            ),
            [
                missile_api(i.position, i.id)
                for i in self.missiles.get_visable(self.plane)
            ],
        )

        if new_target:
            self.plane.set_target_heading(new_target)

        # Colisions
        colisions = detect_colisions(self.plane, self.missiles)
        for colision in colisions:
            self.explosions.add(colision)

        return alive
