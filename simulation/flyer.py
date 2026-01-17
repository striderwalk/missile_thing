import math

from pygame.math import Vector2 as Vector

from ..consts import *


class Flyer:
    max_speed = 1
    turning_speed = 1

    def __init__(self, position, velocity=Vector(0, 1)):
        self.position = position
        self.velocity = velocity
        self.heading = 0
        self.target_heading = 0

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def limit_speed(self):
        self.velocity = self.velocity.normalize() * self.max_speed

    def update_movement(self, dt):

        self.update_heading(dt)
        self.limit_speed()
        self.position += self.velocity * dt

    def update_heading(self, dt):
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

    def set_target_heading(self, angle):

        self.target_heading = angle
