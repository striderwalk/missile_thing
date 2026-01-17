import math

from pygame.math import Vector2 as Vector

from ..consts import *


class Flyer:
    max_speed: float = 1
    turning_speed: float = 1

    def __init__(self, position: Vector, velocity: Vector = Vector(0, 1)):
        self.position: Vector = position
        self.velocity: Vector = velocity
        self.heading: float = 0
        self.target_heading: float = 0

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    def limit_speed(self):
        self.velocity = self.velocity.normalize() * self.max_speed

    def update_heading(self, dt: float):
        self.heading %= 2 * math.pi
        self.target_heading %= 2 * math.pi

        dheading = self.target_heading - self.heading

        turning_speed_dt = self.turning_speed * dt
        if abs(dheading) < turning_speed_dt:
            self.heading += dheading
        else:
            self.heading += turning_speed_dt * dheading / abs(dheading)

        new_x = math.cos(self.heading)
        new_y = math.sin(self.heading)
        self.velocity = Vector(new_x, new_y)

    def set_target_heading(self, angle: float):

        self.target_heading = angle

    def update_movement(self, dt: float):

        self.update_heading(dt)
        self.limit_speed()
        self.position += self.velocity * dt
