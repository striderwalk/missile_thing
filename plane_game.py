from collections.abc import Callable
import math
import random
import time

import pygame
from pygame.locals import *

from .consts import *
from .graphics import Display
from .simulation import Simulation
from .missile_control import missile_controller


random.seed(1)

pygame.init()
import time


class Clock:
    def __init__(self, time_scale=1):
        self.time_passed = 0.0
        self.prev_time = time.perf_counter()
        self.time_scale = time_scale

    def tick(self, FPS):
        cur_time = time.perf_counter()
        dt = cur_time - self.prev_time

        remaining = (1 / (FPS * self.time_scale)) - dt
        if remaining > 0:
            time.sleep(remaining)
            cur_time = time.perf_counter()
            dt = cur_time - self.prev_time

        self.time_passed += dt * self.time_scale
        self.prev_time = cur_time
        return dt * self.time_scale


class Game:

    def __init__(
        self,
        plane_controller: Callable,
        render: bool = True,
        accelerate: float = 1,
    ):
        self.render = render
        self.sim = Simulation(plane_controller, missile_controller)

        self.clock = Clock(accelerate)  # pygame.time.Clock()
        self.clock.tick(FPS)

        if self.render:
            self.display = Display()

    def run(self) -> int | None:

        dt = self.clock.tick(FPS)

        while self.sim.active:

            dt = self.clock.tick(FPS)

            if self.render:
                # pygame.display.set_caption(f"{self.clock.get_fps():.0f}")

                if not self.display.update(self.sim):
                    pygame.quit()
                    return None

            self.update(dt)

        pygame.quit()

        return math.floor(self.clock.time_passed)

    def update(self, dt):

        self.sim.update(dt)
