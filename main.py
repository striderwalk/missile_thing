import math
import random

import pygame
from pygame.locals import *

from consts import *
from graphics import Display
from simulation import Simulation
from missile_control import control_missile
from plane_control import control_plane

DRAWING = True


class PlaneGame:
    def __init__(self):
        self.sim = Simulation(control_plane, control_missile)

        self.clock = pygame.time.Clock()
        self.display = Display()

        self.start_time = pygame.time.get_ticks()

    def run(self):

        while self.sim.active:
            dt = self.clock.tick(FPS)
            self.update(dt)
            if DRAWING:
                if not self.display.update(self.sim):
                    pygame.quit()
                    return

        end_time = pygame.time.get_ticks()
        pygame.quit()

        return math.floor((end_time - self.start_time) / 1000)

    def update(self, dt):

        self.sim.update(dt)

    pygame.quit()


if __name__ == "__main__":
    random.seed(1)

    pygame.init()
    game = PlaneGame()
    game.run()
