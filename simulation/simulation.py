import pygame
from pygame.locals import *
from pygame.math import Vector2

from . import Explosions, Missiles, Plane, detect_colisions


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

        self.missiles.update(dt, self.plane, self.missile_controller)
        self.plane_controller(self.plane, self.missiles.get_visable(self.plane))
        self.explosions.update()

        # Colisions
        colisions = detect_colisions(self.plane, self.missiles)
        for colision in colisions:
            self.explosions.add(colision)

        return alive
