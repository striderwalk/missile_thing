import pygame
from pygame.math import Vector2 as Vector

from .disp_consts import *


class Camera:
    def __init__(self):
        self.position = Vector(0, 0)
        self.rect = pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT))

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
            - Vector(rect.size) / 2
            - self.position
            + Vector(SCREEN_WIDTH, SCREEN_HEIGHT) / 2
        )

    def update(self, plane) -> None:

        self.position = plane.position

        self.rect.center = self.position
