import pygame
from pygame.locals import *
from pygame.math import Vector2

from . import Explosions, Missiles, Plane, detect_colisions
from dataclasses import dataclass


@dataclass
class missile_api:
    position: Vector2
    id: str


@dataclass
class plane_api:
    position: Vector2
    heading: float
    target_heading: float


class Simulation:

    def __init__(self, plane_controller, missile_controller):
        self.plane = Plane(Vector2(0, 0))
        self.plane_controller = plane_controller
        self.missile_controller = missile_controller
        self.missiles = Missiles()
        self.explosions = Explosions()

    @property
    def active(self):
        return self.plane.health > 0

    def update(self, dt):
        alive = self.plane.update(dt)

        new_target = self.plane_controller(
            plane_api(
                self.plane.position, self.plane.heading, self.plane.target_heading
            ),
            [
                missile_api(i.position, i.id)
                for i in self.missiles.get_visable(self.plane)
            ],
        )
        if new_target:
            self.plane.set_target_heading(new_target)

        self.missiles.update(dt, self.plane, self.missile_controller)
        self.explosions.update()

        # Colisions
        colisions = detect_colisions(self.plane, self.missiles)
        for colision in colisions:
            self.explosions.add(colision)

        return alive
