from collections.abc import Callable
import math
import random

import pygame
from pygame.locals import *

from .consts import *
from .graphics import Display
from .simulation import Simulation
from .missile_control import missile_controller


random.seed(1)

pygame.init()


class Game:

    def __init__(self, plane_controller: Callable, render: bool = True):
        self.render = render
        self.sim = Simulation(plane_controller, missile_controller)

        self.clock = pygame.time.Clock()
        if self.render:
            self.display = Display()

        self.start_time = pygame.time.get_ticks()

    def run(self) -> int | None:

        while self.sim.active:
            dt = self.clock.tick(FPS) / 1000
            pygame.display.set_caption(f"{self.clock.get_fps():.0f}")

            self.update(dt)
            if self.render:

                if not self.display.update(self.sim):
                    pygame.quit()
                    return None

        end_time = pygame.time.get_ticks()
        pygame.quit()

        return math.floor((end_time - self.start_time) / 1000)

    def update(self, dt):

        self.sim.update(dt)

    pygame.quit()
