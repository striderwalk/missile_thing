from pygame.math import Vector2 as Vector

from consts import *


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
