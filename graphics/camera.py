import pygame
from pygame.math import Vector2 as Vector

from .disp_consts import *


class Camera:
    def __init__(self):
        self.position = Vector(0, 0)

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    def apply(
        self, position: Vector, rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
    ) -> Vector:

        return (
            position
            - self.position
            + Vector(SCREEN_WIDTH, SCREEN_HEIGHT) / 2
            - Vector(rect.size) / 2
        )

    def update(self, plane) -> None:

        self.position = plane.position
