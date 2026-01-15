import random
from pygame.math import Vector2
import pygame
import math
from .sim_consts import *
from . import Flyer


class Plane(Flyer):
    max_speed = PLANE_SPEED
    turning_speed = PLANE_TURNING_SPEED

    def __init__(self, position=Vector2(0, 0)):
        super().__init__(position)
        self.health = 100
        self.hits = 0
        self.heading = -math.pi / 2

    def get_image(self):
        surface = pygame.Surface((40, 40), pygame.SRCALPHA)

        surface.fill((0, 0, 0, 0))
        pygame.draw.circle(surface, (255, 0, 0), (20, 20), 5)
        vel = self.velocity.normalize() * 15
        pygame.draw.circle(surface, (0, 255, 120), (20 + vel.x, vel.y + 20), 3)

        return surface

    def draw(self, win, camera):
        win.blit(self.get_image(), camera.apply(self.position))

    def update(self, dt):
        self.update_movement(dt)

    def hit(self):
        self.health -= 50
        self.hits += 1
